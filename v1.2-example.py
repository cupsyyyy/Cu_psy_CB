import serial
import time
import threading
import os
from serial.tools import list_ports

# Fallback COM port (used if auto-detection fails)
fallback_com_port = "COM3" # <---- UPDATE THIS TO YOUR COM PORT

baud_change_command = bytearray([0xDE, 0xAD, 0x05, 0x00, 0xA5, 0x00, 0x09, 0x3D, 0x00])
makcu = None
makcu_lock = threading.Lock()
is_connected = False
current_com_port = None
current_baud_rate = None
listener_thread = None
log_messages = []
LOG_LIMIT = 20

button_map = {
    0: 'Left Mouse Button',
    1: 'Right Mouse Button',
    2: 'Middle Mouse Button',
    3: 'Side Mouse 4 Button',
    4: 'Side Mouse 5 Button'
}
RED, GREEN, RESET = "\033[91m", "\033[92m", "\033[0m"

def log(message):
    global log_messages
    timestamp = time.strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}"
    log_messages.append(entry)
    if len(log_messages) > LOG_LIMIT:
        log_messages.pop(0)
    print(entry, flush=True)

def print_debug_output(button_states):
    print("\033[H\033[J", end="")  # Clear screen
    debug_output = f"Port: {current_com_port or 'None'} | Baud Rate: {current_baud_rate or 'None'} | Connected: {is_connected}\n\n"
    debug_output += "---== Log ==---\n"
    debug_output += "\n".join(log_messages) + "\n"
    debug_output += "\n---== Button States ==---\n"
    for bit, name in button_map.items():
        state = button_states.get(bit, False)
        color = GREEN if state else RED
        state_str = "Pressed" if state else "Unpressed"
        debug_output += f"{name}: {color}{state_str}{RESET}\n"
    debug_output += "---== Button States ==---"
    print(debug_output)

def open_serial_port(port, baud_rate):
    try:
        log(f"Trying to open {port} at {baud_rate} baud.")
        return serial.Serial(port, baud_rate, timeout=0.05)
    except serial.SerialException as e:
        log(f"Failed to open {port} at {baud_rate} baud. Error: {str(e)}")
        if isinstance(e.__cause__, PermissionError):
            log("PermissionError: Port may already be in use by another application.")
        return None

def change_baud_rate_to_4M():
    global makcu, current_baud_rate, is_connected
    if makcu and makcu.is_open:
        log("Sending baud rate switch command to 4M.")
        makcu.write(baud_change_command)
        makcu.flush()
        makcu.close()
        time.sleep(0.1)
        makcu = open_serial_port(makcu.name, 4000000)
        if makcu:
            current_baud_rate = 4000000
            is_connected = True
            log("Switched to 4M baud successfully.")
        else:
            is_connected = False
            log("Failed to reopen port at 4M baud.")

def connect_to_com_port(port):
    global makcu, is_connected, current_com_port, current_baud_rate
    if not is_connected:
        makcu = open_serial_port(port, 115200)
        if makcu:
            current_com_port, current_baud_rate = port, 115200
            log(f"Connected to {port} at 115200.")
            change_baud_rate_to_4M()
        else:
            log(f"Initial connection to {port} at 115200 failed.")

def close_com_port():
    global makcu, is_connected
    if makcu and makcu.is_open:
        makcu.close()
        is_connected = False
        log("Closed COM port.")

def listen_makcu():
    last_value = None
    button_states = {i: False for i in button_map}
    log("Started listening thread for button states.")

    ignore_sequence = False
    ignore_counter = 0

    while is_connected:
        try:
            byte = makcu.read(1)
            if byte:
                # \r marks the end of the event, so im using this to skip the end, very lazy lol
                if byte == b'\r':
                    ignore_sequence = True
                    ignore_counter = 5
                    continue

                if ignore_sequence:
                    ignore_counter -= 1
                    if ignore_counter == 0:
                        ignore_sequence = False
                    continue

                value = byte[0]
                if value != last_value:
                    byte_str = str(byte)
                    if 'b\'\\x00' in byte_str:
                        button_states = {i: False for i in button_map}
                    elif 'b\'\\x' in byte_str or 'b\'\\n' in byte_str:
                        for bit, name in button_map.items():
                            is_pressed = bool(value & (1 << bit))
                            if is_pressed != button_states[bit]:
                                button_states[bit] = is_pressed
                    print_debug_output(button_states)
                    last_value = value
        except serial.SerialException as e:
            if "ClearCommError failed" in str(e):
                pass
            else:
                log(f"Serial error during listening: {e}")
                break

def find_com_port():
    log("Searching for CH343 device...")
    for port in serial.tools.list_ports.comports():
        if "USB-Enhanced-SERIAL CH343" in port.description:
            log(f"Device found: {port.device}")
            return port.device
    log("Device not found.")
    return None

def main():
    global current_com_port
    current_com_port = find_com_port()
    
    if not current_com_port and fallback_com_port:
        log(f"Falling back to port: {fallback_com_port}")
        current_com_port = fallback_com_port

    if current_com_port:
        connect_to_com_port(current_com_port)
        if is_connected:
            with makcu_lock:
                log("Sending init command: km.buttons(1)")
                makcu.write(b"km.buttons(1)\r")
                makcu.flush()

            global listener_thread
            listener_thread = threading.Thread(target=listen_makcu)
            listener_thread.daemon = True
            listener_thread.start()

            while True:
                time.sleep(1)
        else:
            log("Failed to connect to the device.")
            print_debug_output({i: False for i in button_map})
    else:
        log("No COM port available. Cannot proceed.")
        print_debug_output({i: False for i in button_map})

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("KeyboardInterrupt: Closing COM Port.")
        close_com_port()
        if listener_thread:
            listener_thread.join()
        log("Program terminated gracefully.")
        print_debug_output({i: False for i in button_map})