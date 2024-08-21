import time

results_file = open("results.txt", 'a')

result_bytes = []
result_state = 0
# 0: waiting 0xff
# 1: waiting 0x86
# 2: waiting HIGH
# 3: waiting LOW
def feed_res_byte(v):
  global result_bytes
  global result_state
  global co2_result
  if result_state == 0:
    if v == 0xff:
      result_bytes = []
      result_bytes.append(v)
      result_state += 1
    else:
      result_state = 0
  elif result_state == 1:
    if v == 0x86:
      result_bytes.append(v)
      result_state += 1
    else:
      result_state = 0
  elif result_state == 2:
    result_bytes.append(v)
    result_state += 1
    co2_result = v
  elif result_state == 3:
    result_bytes.append(v)
    co2_result *= 256
    co2_result += v
    result_state += 1
  elif result_state == 4:
    result_bytes.append(v)
    result_state += 1
  elif result_state == 5:
    result_bytes.append(v)
    result_state += 1
  elif result_state == 6:
    result_bytes.append(v)
    result_state += 1
  elif result_state == 7:
    result_bytes.append(v)
    result_state += 1
  elif result_state == 8:
    result_bytes.append(v)
    result_state += 1
    # now the data is complete
    sum = 0
    for v in result_bytes:
      sum += v
    sum = sum & 0xff
    if sum == 255:
      print("co2: ", co2_result)
      results_file.write("%s: co2: %s\n" % (time.monotonic_ns(), co2_result))
      results_file.flush()
      
    else:
      print("csum error. csum = ", sum, "value = ", co2_result)
      results_file.write("%s: csum error: %s %s\n" % (time.monotonic_ns(), sum, co2_result))
      results_file.flush()
    result_state = 0
  else:
    result_state = 0
  
    

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

def parse_bits_lsb_first(bits):
  result = 0
  shift = 0
  for b in bits:
    result += b << shift
    shift += 1
  return result

byte_count = 0
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
      res_byte = parse_bits_lsb_first(bits)
      feed_res_byte(res_byte)
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

