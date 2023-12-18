"""
Summary
-------
Check the status of Firewall commits of single Palo Alto Network device.

Approach
--------
The script begins by submitting a "commit validate" command to the firewall. 
This command forces the firewall to validate its candidate configuration and ensures the job is at the top of the job list and is logged. 
The script then retrieves and analyzes the job logs to receive the commit status. 
Finally, it outputs the status of firewall's commit operation to a .csv file, providing a clear overview of the network's configuration status.

Parameters
----------
`firewall_ip`: str: 
    The IP address of the Palo Alto Network Firewall device.
`username`: str: 
    The username for authentication to access the firewall.
`password`: str: 
    The password for authentication.

Returns
-------
Standard Out: 
    Prints the final status, result, and configuration status of the job for firewall IP.
Write to a file(CSV): 
    Appends the firewall IP, final status, result, and configuration status of the job to 'commit_job_statuses.csv'.
"""

import csv
import time
import pan.xapi
import getpass
import xml.etree.ElementTree as ET

# Function to check the job until the status is "FIN" or the timeout (3 minutes) is reached
def get_job_status(job_id, conn, timeout=180, interval=10):
    start_time = time.time()  # get current time (in seconds) to start
    # Poll until elapsed time is less than timeout
    while time.time() - start_time < timeout:
        try:
            cmd = f"<show><jobs><id>{job_id}</id></jobs></show>"
            conn.op(cmd, cmd_xml=False)
            xml_response = conn.xml_result()
            if xml_response:
                xml_response = "<root>" + xml_response + "</root>"
                root = ET.fromstring(xml_response)
                status_element = root.find("./job/status")
                result_element = root.find("./job/result")
                details_elements = root.findall("./job/details/line")

                # Check if each element exists before accessing its text value
                status = status_element.text if status_element is not None else "N/A"
                result = result_element.text if result_element is not None else "N/A"
                details = " | ".join(
                    [elem.text for elem in details_elements if elem.text is not None]
                )

                if status == "FIN":
                    return status, result, details
            time.sleep(interval)
        except ET.ParseError as e:
            print("An XML parsing error occurred:", e)
            break
    return "N/A", "N/A", "N/A"


# Prompt for firewall credentials
firewall_ip = input("Enter firewall IP: ")
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

try:
    # Connect to the firewall
    conn = pan.xapi.PanXapi(
        api_username=username,
        api_password=password,
        hostname=firewall_ip,
    )

    # Start the job and get the initial response
    conn.op("validate full", cmd_xml=True)
    initial_response = conn.xml_result()
    if initial_response:
        print(
            "\n", "Initial response from Validate Full query:", initial_response, "\n"
        )

        # Wrap the XML response with root element when junk is sent from the response
        xml_response = "<root>" + initial_response + "</root>"
        initial_root = ET.fromstring(xml_response)
        # Extract the job ID from the initial response
        job_id_element = initial_root.find(".//job")
        job_id = job_id_element.text if job_id_element is not None else None

        if job_id:
            print(f"Job started with ID: \033[1m {job_id} \033[0m")
            job_status, job_result, configuration_status = get_job_status(job_id, conn)

            print(f"Final Status of Job {job_id}: \033[1m {job_status} \033[0m")
            print(f"Result of Job {job_id}: \033[1m {job_result} \033[0m")
            print(f"Configuration Status: \033[1m {configuration_status} \033[0m")

            # Write firewall IP and job statuses to CSV file
            with open("commit_status_single_FW.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                # Write the header and results
                writer.writerow(
                    [
                        "Firewall_IP",
                        "Job ID",
                        "Status",
                        "Result",
                        "Configuration Status",
                    ]
                )
                writer.writerow(
                    [firewall_ip, job_id, job_status, job_result, configuration_status]
                )
            print(f"Job Status for the \033[1m {firewall_ip} \033[0m with \033[1m {job_id} \033[0m is written to a CSV.")
        else:
            print("No valid job ID received.")

except pan.xapi.PanXapiError as e:
    print(f"An error occurred with PAN XML API: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print(f"Could not connect to the firewall at {firewall_ip}. Please check your network connection and credentials.")
