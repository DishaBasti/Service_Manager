# Service Manager

A Service Manager is a tool or utility that allows users to manage system services. Services are background processes that perform specific functions and are often critical for the operating system or applications. Unlike regular applications that run in the foreground and have a user interface, services run in the background and typically start when the system boots up.

## Pros over Task Manager

1. Specialized Functionality
2. Automation and Scripting
3. Configuration Management
4. Error Handling

## About the Script

This Python script functions as a Service Manager for Windows systems. It allows users to manage system services via the command line, with capabilities for starting, stopping, restarting, querying the status, and listing services. Additionally, it can set and manage a default service through configuration.

### Components of the Script
1. Logging setup
2. Configuration management
3. Service management functions
4. Default service management

## Workflow

### Initial Setup:

The script may prompt the user to display all services or query the default service settings.
### Service Operations:

Based on user input, the script will execute the relevant commands to manage services.
### Configuration Updates:

Any changes to the default service are saved to the configuration file, affecting subsequent script runs.

## Getting Started

1. Clone the repository
   ```bash
   git clone https://github.com/DishaBasti/Service_Manager.git
   ```

2. Create a 'service_manager.log' file in the same directory.

3. Run cmd as administrator in the directory where the files are present.
   ```
   python service_manager.py
   ```
The service manager is at its service.

