import subprocess
import logging
import json
import os

# Setting up logging
logging.basicConfig(filename='service_manager.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load configuration
CONFIG_FILE = 'service_manager_config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

config = load_config()

def run_command(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def start_service(service_name):
    command = f'sc start {service_name}'
    result = run_command(command)
    logging.info(f'Started service {service_name}: {result}')
    return result

def stop_service(service_name):
    command = f'sc stop {service_name}'
    result = run_command(command)
    logging.info(f'Stopped service {service_name}: {result}')
    return result

def restart_service(service_name):
    stop_command = f'sc stop {service_name}'
    start_command = f'sc start {service_name}'
    stop_output = run_command(stop_command)
    start_output = run_command(start_command)
    result = stop_output + start_output
    logging.info(f'Restarted service {service_name}: {result}')
    return result

def service_status(service_name):
    command = f'sc query {service_name}'
    result = run_command(command)
    logging.info(f'Service status for {service_name}: {result}')
    return result

def list_services():
    command = 'sc query type= service state= all'
    result = run_command(command)
    logging.info('Listed all services')
    return result

def list_services_with_display_names():
    command = 'wmic service get Name,DisplayName'
    result = run_command(command)
    logging.info('Listed all services with display names')
    return result

def manage_service_dependencies(service_name, action):
    # Simplified example for dependencies management
    if action == 'start':
        command = f'sc qc {service_name}'
        output = run_command(command)
        dependencies = []
        for line in output.splitlines():
            if 'DEPENDENCIES' in line:
                dependencies = line.split(':')[1].strip().split()
        for dep in dependencies:
            start_service(dep)
    elif action == 'stop':
        # Stopping dependencies is not a straightforward task and needs careful handling.
        logging.info(f'Stop dependencies for {service_name} is not implemented due to complexity.')

def check_default_service():
    if "default_service" in config:
        print(f"Default service name is: {config['default_service']}")
        change_or_remove = input("Do you want to change or remove the default service? (change/remove/no): ").strip().lower()
        if change_or_remove == 'change':
            change_default_service()
        elif change_or_remove == 'remove':
            remove_default_service()
        elif change_or_remove == 'no':
            return config['default_service']
        else:
            print("Invalid option. Proceeding without changes.")
            return config['default_service']
    else:
        print("No default service is set.")
        return None

def change_default_service():
    new_service_name = input("Enter the new default service name: ").strip()
    config["default_service"] = new_service_name
    save_config(config)
    print(f"Default service updated to {new_service_name}")

def remove_default_service():
    if "default_service" in config:
        del config["default_service"]
        save_config(config)
        print("Default service removed.")
    else:
        print("No default service is set to remove.")

if __name__ == "__main__":
    display_services = input("Do you want to display all service names and display names? (yes/no): ").strip().lower()
    
    if display_services == 'yes':
        print(list_services_with_display_names())
    
    default_service = check_default_service()
    
    if default_service:
        service_name = default_service
    else:
        service_name = input("Enter the service name: ")

    while True:
        print("\nService Manager")
        print("1. Start Service")
        print("2. Stop Service")
        print("3. Restart Service")
        print("4. Service Status")
        print("5. List All Services")
        print("6. Set Default Service")
        print("7. Check Default Service")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            manage_service_dependencies(service_name, 'start')
            result = start_service(service_name)
        elif choice == '2':
            result = stop_service(service_name)
        elif choice == '3':
            result = restart_service(service_name)
        elif choice == '4':
            result = service_status(service_name)
        elif choice == '5':
            result = list_services()
        elif choice == '6':
            service_name = input("Enter the new default service name: ")
            config["default_service"] = service_name
            save_config(config)
            print(f"Default service set to {service_name}")
            continue
        elif choice == '7':
            check_default_service()
            continue
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        if "Access is denied" in result:
            print("Error: Access is denied. Please run the script as an administrator.")
        else:
            print(result)
