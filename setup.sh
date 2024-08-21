sudo echo "hello"

function setup_gpio_in() {
  [ -d /sys/class/gpio/gpio${1} ] || sudo bash -c "echo ${1} > /sys/class/gpio/export"
  sudo bash -c "echo 'in' > /sys/class/gpio/gpio${1}/direction"
  sudo chmod 777 /sys/class/gpio/gpio${1}/value
  ls -lah /sys/class/gpio/gpio${1}/value
}
function setup_gpio_out() {
  [ -d /sys/class/gpio/gpio${1} ] || sudo bash -c "echo ${1} > /sys/class/gpio/export"
  sudo bash -c "echo 'out' > /sys/class/gpio/gpio${1}/direction"
  sudo chmod 777 /sys/class/gpio/gpio${1}/value
  ls -lah /sys/class/gpio/gpio${1}/value
}
setup_gpio_out 58 # host to sensor
setup_gpio_in 57 # sensor to host

