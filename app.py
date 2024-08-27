from flask import Flask, request, jsonify
from bluepy import btle

app = Flask(__name__)

def connect(mac_addr):
    peripheral = btle.Peripheral()
    peripheral.connect(mac_addr, btle.ADDR_TYPE_RANDOM)
    return peripheral

def write_pwm(peripheral, value):
    PWM_HANDLE = 17
    PWM_INDEX = 1
    data = bytearray(peripheral.readCharacteristic(PWM_HANDLE))
    data[PWM_INDEX] = value
    peripheral.writeCharacteristic(17, bytes(data), True)

@app.route('/control', methods=['POST'])
def control_device():
    data = request.json
    if 'mac_addr' not in data or 'pwm_value' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    mac_addr = data['mac_addr']
    pwm_value = data['pwm_value']

    if not (0 <= pwm_value <= 100):
        return jsonify({'error': 'PWM value must be between 0 and 100'}), 400

    try:
        peripheral = connect(mac_addr)
        write_pwm(peripheral, pwm_value)
        peripheral.disconnect()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
