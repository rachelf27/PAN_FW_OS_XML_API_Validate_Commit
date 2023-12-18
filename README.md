# Automating Palo Alto Network's Firewall Statuses
The goal of this project is to automate the task of checking commit statuses on Palo Alto Network's Firewalls using the PAN-OS SDK for Python.

## Automation Use Cases
The scripts in this project will cater to a variety of scenarios within a network of Palo Alto Firewalls managed by Panorama. 
A typical use case involves traversing through multiple firewalls to validate their configurations, especially useful when addressing commit failures. The scripts log the success, failures, and any error messages for each firewall, offering a comprehensive overview of the network's health.

## Technologies Used
The PAN-OS SDK for Python (pan-os-python) is an essential package for interacting with Palo Alto Networks devices, including Next-generation Firewalls and Panorama. It offers an object-oriented approach that reflects the GUI or CLI/API interactions.  
For detailed documentation, visit [PAN-OS Python SDK Documentation](https://pan-os-python.readthedocs.io/_/downloads/en/latest/pdf/).

## Python Version Compatibility
These scripts were developed and tested using Python version 3.9.18. They may not be fully compatible with earlier versions of Python. Users running older Python versions may need to make minor modifications to the code.

### Requirements
1. Access credentials for Palo Alto Network devices.
2. Configuration of Palo Alto Networks Devices SSH access.

### Dependencies
1. `pan-xapi` - Accessing the PAN-OS XML API.
2. `getpass` - Secure password input.
3. `xml.etree.ElementTree` - XML Parsing.
4. `csv` - Writing to CSV files.
5. `time` - Managing time-based operations.

## Getting Started
To begin using these scripts, clone the project and follow the steps below:

1. **Latest Python**: - Install the latest version of Python:  
   [Download Python](https://www.python.org/downloads/)
2. **Install `pan-os-python`**: - Install the Palo Alto Networks PAN-OS SDK for Python:  
	```
    pip3 install pan-os-python
    ```
3. **Set File Permissions**: - Modify file permissions to make them executable:
   ```
   chmod 744 <filename>
   ```

### Usage
To execute the scripts by running:  
  `python <filename>`  