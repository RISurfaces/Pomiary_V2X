import serial
import time
import json


try:
    with open ("config.json") as config_f:
        config = json.load(config_f)
        RIS_SET_TIME_USB = config["RIS_SET_TIME_USB"]
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()

class RIS_usb():
    def __init__(self, port : str, id : int) -> None:
        try:
             self.port = serial.Serial(port, 115200)
             self.id = id
        except serial.SerialException:
           print("[SERIAL ERROR] Change port number in config file. Check correct port in device manager.")
           exit()
           
           
    def reset(self) -> str:
        self.port.write(bytes('!Reset\n', 'utf-8'))
        time.sleep(RIS_SET_TIME_USB)
        line = []
        while True:
            cc=str(self.port.readline().decode('utf-8').rstrip())
            print(cc)
            if cc == '#READY!':
                break
        return cc
                
    def set_BT_key(self, key : str) -> str:
        self.port.write(bytes(f'!BT-Key={key}\n', 'utf-8'))
        # Wait long enough or check self.port.NumBytesAvailable for becoming non-zero
        time.sleep(2)
        response = self.port.readline().decode('utf-8').rstrip()
        print(f"Response from setting a new Static Pass Key: {response}")
        return response
    
    def set_pattern(self, pattern : str) -> bool:
        self.port.write(bytes(f"!{pattern}\n", 'utf-8'))
        time.sleep(RIS_SET_TIME_USB)
        return True
        
    def read_EXT_voltage(self) -> str:
        self.port.write(bytes('?Vext\n', 'utf-8'))
        externalVoltage = self.port.readline().decode('utf-8').rstrip()
        print(f"External supply voltage: {externalVoltage}")
        return externalVoltage

    def read_pattern(self) -> str:
        self.port.write(bytes('?Pattern\n', 'utf-8'))
        time.sleep(RIS_SET_TIME_USB)
        response = self.port.readline().decode('utf-8').rstrip()
        print(f"Response from resetting RIS: {response}")
        return response
            
    def ris_pattern_negation(self, ris_pattern : str) -> str:
        ris_pattern = int(ris_pattern,16)
        ris_pattern = ~ris_pattern & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        ris_pattern = hex(ris_pattern)
        ris_pattern = str(ris_pattern)
        no_of_zero_to_add = 66 - len(ris_pattern)
        for i in range(no_of_zero_to_add):
            ris_pattern = ris_pattern[:2] + '0' + ris_pattern [2:]
        ris_pattern = ris_pattern.upper()
        ris_pattern = ris_pattern.replace('X', 'x')
        return ris_pattern
            
            


    