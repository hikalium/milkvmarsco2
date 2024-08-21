import time

delay = 9600
gpiopath = "/sys/class/gpio/gpio58/value";
wf = open(gpiopath, mode='wb+', buffering=False)

def calc_timeout(t):
  return time.monotonic_ns() + t * 1000000000

def wait_until(timeout):
  while time.monotonic_ns() < timeout:
    pass

timeout = calc_timeout(1/delay)
def write_gpio(v):
  global timeout
  wait_until(timeout)
  timeout += 1000000000/delay
  wf.write(b'1' if v else b'0')
  wf.flush()

# write
co2_query_bytes = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
#co2_query_bytes = [0xff, 0xaa, 0xff, 0xaa, 0xff, 0xaa, 0xff, 0xaa]
# LSB first
co2_query_bytes = [reversed(('00000000' + bin(b)[2:])[-8:]) for b in co2_query_bytes]

write_gpio(1)
write_gpio(1)
write_gpio(1)
write_gpio(1)
write_gpio(1)
write_gpio(1)
write_gpio(1)
write_gpio(1)
write_gpio(1)
for by in co2_query_bytes:
  write_gpio(0)
  for bi in by:
    write_gpio(int(bi))
  write_gpio(1)
  write_gpio(1)
  write_gpio(1)
  write_gpio(1)
  write_gpio(1)
  write_gpio(1)
  write_gpio(1)
  write_gpio(1)

