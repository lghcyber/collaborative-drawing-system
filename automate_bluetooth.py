import subprocess
import uuid

def run_command(command):
    """Run a shell command and return the output."""
    try:
        print(f"Running command: {' '.join(command)}")  # Debug output for command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Command output: {result.stdout}")  # Debug output for successful command
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing command: {' '.join(command)}")
        print(f"Return code: {e.returncode}")
        print(f"Error message: {e.stderr}")
        return None

def list_bluetooth_devices():
    """List all Bluetooth devices."""
    print("Listing Bluetooth devices...")  # Debug output
    output = run_command(['bluetoothctl', 'devices'])
    if output:
        print("Bluetooth Devices:")
        print(output)

def get_device_mac(device_name):
    """Get the MAC address of a Bluetooth device by its name."""
    print(f"Searching for MAC address of device: {device_name}")  # Debug output
    devices_output = run_command(['bluetoothctl', 'devices'])
    if devices_output:
        for line in devices_output.splitlines():
            if device_name in line:
                # The line format is usually: Device MAC_ADDRESS Device_Name
                parts = line.split()
                if len(parts) >= 2:
                    mac_address = parts[1]
                    print(f"Found MAC address: {mac_address} for device: {device_name}")
                    return mac_address
    print(f"Device {device_name} not found.")  # Debug output
    return None

def connect_bluetooth_device(device_mac):
    """Connect to a Bluetooth device."""
    print(f"Connecting to device {device_mac}...")  # Debug output
    if device_mac:
        run_command(['bluetoothctl', 'connect', device_mac])

def create_virtual_pointer():
    """Create a new virtual pointer with a shorter unique name using xinput."""
    unique_name = "VP_" + str(uuid.uuid4())[:8]  # Use only the first 8 characters of the UUID
    print(f"Creating virtual pointer with name: {unique_name}")  # Debug output

    # Run the command to create a new master device
    run_command(['xinput', 'create-master', unique_name])

    # List devices to find the new master pointer
    devices_output = run_command(['xinput', 'list'])
    if devices_output:
        for line in devices_output.splitlines():
            if unique_name in line and "pointer" in line:
                # Split the line and find the part that contains 'id='
                parts = line.split()
                for part in parts:
                    if 'id=' in part:
                        pointer_id = part.split('=')[1]
                        print(f"Found new pointer ID: {pointer_id} for {unique_name}")
                        return pointer_id, unique_name
    print("Failed to find the new virtual pointer.")  # Debug output
    return None, None

def attach_device_to_pointer(device_name, pointer_id):
    """Attach a device to a new pointer."""
    print(f"Attaching {device_name} to pointer ID {pointer_id}...")  # Debug output
    # Find the device ID
    devices_output = run_command(['xinput', 'list'])
    device_id = None
    if devices_output:
        for line in devices_output.splitlines():
            if device_name in line:
                device_id = line.split()[5].split('=')[1]
                print(f"Found device ID: {device_id} for {device_name}")  # Debug output
                break

    if device_id and pointer_id:
        result = run_command(['xinput', 'reattach', device_id, pointer_id])
        if result is not None:
            print(f"Attached {device_name} to pointer ID {pointer_id}")
        else:
            print(f"Failed to attach {device_name} to pointer ID {pointer_id}")

if __name__ == "__main__":
    device_name = 'Lenovo Bluetooth Mouse'

    list_bluetooth_devices()

    # Get the MAC address dynamically
    device_mac = get_device_mac(device_name)

    if device_mac:
        connect_bluetooth_device(device_mac)

        pointer_id, pointer_name = create_virtual_pointer()

        if pointer_id:
            attach_device_to_pointer(device_name, pointer_id)
        else:
            print("Failed to create a virtual pointer.")
    else:
        print(f"Failed to find MAC address for device: {device_name}")