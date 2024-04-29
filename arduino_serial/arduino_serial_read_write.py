import time
import serial.tools.list_ports

class SerialArduinoReadWrite():
    def __init__(self):
        self.ports = serial.tools.list_ports.comports()
        self.serialInst = serial.Serial()
        self.portList = []
        self.portVar = None
        self.pkg_byte_size = 2
        
        # print(len(self.ports))
        if len(self.ports) == 1:
            self.portVar = self.ports[0].device
        else:
            for port in self.ports:
                if 'arduino' in port.description.lower():
                    self.portVar = port
                    break
            if not self.portVar:
                print('no arduino found')
                exit

        self.serialInst.baudrate = 9600
        self.serialInst.port = self.portVar
        self.serialInst.open()

        # print(self.portVar)

    def get_message(self):
        # Wait for number of bytes in input buffer to exceed the package size:
        if self.serialInst.in_waiting >= self.pkg_byte_size:
            package = self.serialInst.read(size=self.pkg_byte_size)
            # print('received msg:',end=' ')
            # print('{!r}'.format(package))
            return int(package[1] << 8 | package[0])
        return None
    
    def send_message(self, img_nr):
        # Convert img_nr [int] to 2 bytes:
        out_msg = bytes([int(img_nr >> 8), int(img_nr & 255)])

        # Check that serial is writable:
        if self.serialInst.writable():
            # Send 
            n_bytes_send = self.serialInst.write(out_msg)
            print(f'sent msg:', end=' ')
            print('{!r}'.format(int((out_msg[0] << 8) | out_msg[1])))
        else:
            print("serial inst not writable!!!")
        return

if __name__ == '__main__':
    # ports = serial.tools.list_ports.comports()
    serial_arduino = SerialArduinoReadWrite()

    print('wait for ARDUINO UNO to finish resetting after opening the serial port...')
    time.sleep(2)   # NOTE: SERIAL COMMUNICATION WITH ARDUINO UNO WILL FAIL IF THIS IS REMOVED!!!

    subsections = 20
    angle_rot_step = int(360 / subsections)

    for i in range(subsections):
        int_to_send = i * angle_rot_step
        serial_arduino.send_message(int_to_send)

        motor_is_executing_command = True
        while motor_is_executing_command:
            read = serial_arduino.get_message()
            if read is not None:
                print('received msg:',end=' ')
                print('{!r}'.format(read))
                motor_is_executing_command = False
            time.sleep(0.01)
        time.sleep(3)