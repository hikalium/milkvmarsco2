import time

delay = 9600
num_bits = 8

in_transfer = 0
next_bit = 0
prev_value = -1

rf = open("/sys/class/gpio/gpio57/value")

def calc_timeout(t):  
  return time.monotonic_ns() + t * 1000000000
                                      
def wait_until(timeout):
  while time.monotonic_ns() < timeout: 
    pass

def read_gpio():
  v = rf.seek(0)
  v = rf.read(1)
  return 1 if v == '1' else 0

bits = []
def process_signal(prev, next):
  global timeout
  global bits 
  global in_transfer
  global next_bit
  if in_transfer == 1:
    bits.append(next)
    next_bit = next_bit + 1
    if next_bit == num_bits:
      print(bits)
      bits = []
      in_transfer = 0
  else:
    if prev == 1 and next == 0:
      timeout = timeout + 1000000000/delay/2 
      in_transfer = 1
      next_bit = 0
    else:
      timeout = timeout - 1000000000/delay/2 

timeout = calc_timeout(1/delay/2*3)
# read
while True:
  # falling edge detection
  wait_until(timeout)
  timeout = timeout + 1000000000 / delay
  next_value = read_gpio()
  process_signal(prev_value, next_value)
  if next_value != prev_value:
    prev_value = next_value;

