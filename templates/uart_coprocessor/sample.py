# Sample Circuitpython Code
import board
import busio
import digitalio
import time
import hardware.main
import hardware.fpga

PATH="/hackin7/aoc25/"
hardware.main.hw_state["fpga_overlay"].deinit()
if input("type something to update fpga: ") != "":
    h = hardware.fpga.upload_bitstream(PATH+"/coprocessor.bit")
    h.deinit()

### Configure UART GPIO #########################
class FpgaCoprocessor():
    def __init__(self):
        self.clear_pins()
        self.frame_size = 16
        self.rx_buf = bytearray()
        self.read_timeout_s = 0.25

        # TX = GP8, RX = GP9
        self.uart = busio.UART(board.GP8, board.GP9, baudrate=460800, timeout=0.1)
        
        # GPIO Pins
        self.pins = []
        gpio_pin_ids = [board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15]
        for pin_id in gpio_pin_ids:
            pin = digitalio.DigitalInOut(pin_id)
            pin.direction = digitalio.Direction.OUTPUT
            pin.value = False
            self.pins.append(pin)


    def clear_pins(self):
        ### Need clear Pins first #######################
        DATA_PINS_NO = [board.GP8, board.GP9, board.GP10, board.GP11, board.GP12]
        pins = []
        for p in DATA_PINS_NO:
            d = digitalio.DigitalInOut(p)
            d.direction = digitalio.Direction.OUTPUT
            d.value = False
            pins.append(d)
                    
        for d in pins:
            d.deinit()
    

    def reset(self):
        reset_pin = self.pins[5]
        reset_pin.value = 1
        reset_pin.value = 0


    def write_int(self, val):
        if val < 0:
            raise ValueError("value must be non negative")
        s = val.to_bytes(self.frame_size, byteorder="big")
        self.uart.write(s)


    def read_int(self):
        deadline = time.monotonic() + self.read_timeout_s

        # Keep reading until we have at least 1 frame
        while len(self.rx_buf) < self.frame_size:
            avail_bytes = self.uart.in_waiting # bytes in inoput buffer ready to be read
            if avail_bytes:
                self.rx_buf.extend(avail_bytes)
                continue

            if time_monotonic() > deadline:
                raise TimeoutError(f"UART read timed out. Need {self.frame_size} bytes but got {len(self._rx_buf)} bytes.")
            time.sleep(0) # yield

        # Read exactly 1 frame
        frame_bytes = bytes(self.rx_buf[:self.frame_size])
        del self._rx_buf[:self.frame_size]

        return int.from_bytes(frame_bytes, byte_order="big")


### Processing ##################################
fp = FpgaCoprocessor()
fp.reset()

# Print dummy message
print(fp.uart.read())

fp.pins[0].value = 1 # Forward mode
fp.pins[1].value = 0 # Forward mode
# fp.uart.write("1234567890123456"); s = fp.uart.read(); print(len(s), s[-16:])

fp.write_int(10)
print(fp.read_int())
fp.write_int(11)
print(fp.read_int())

### Previous (2nd) mode
fp.pins[0].value = 0; fp.pins[1].value = 1
fp.write_int(12)
print(fp.read_int()) # Should be 10
fp.write_int(13)
print(fp.read_int()) # Should be 11

### Addition Mode
fp.pins[0].value = 0; fp.pins[1].value = 0;
fp.write_int(11)
print(fp.read_int()) # 13 + 11 = 24
fp.write_int(10000)
print(fp.read_int()) # Should be 10011
