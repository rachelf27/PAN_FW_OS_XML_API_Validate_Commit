"""
Summary
-------
Check the status of ALL jobs of single Palo Alto Network device.

Approach
--------
The script requests the IP address and credentials of the Palo Alto Network device. 
It then issues a "show jobs all" command to the firewall, which prompts the firewall to display all job logs. 
The script processes these logs to extract the status of each job. 
Finally, the job statuses are output to a .csv file, offering a comprehensive view of the device's job history and statuses.

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
    Prints the final status and result of each job for the specified firewall IP.
Write to a file(CSV): 
    Appends the firewall IP, job ID, and status of each job to 'check_all_jobs_status.csv'.
"""

import pan.xapi
import getpass
import csv
import xml.etree.ElementTree as ET

#Prompt for firewall credentials
firewall_ip = input("Enter firewall IP: ")
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

# Connect to the firewall
conn = pan.xapi.PanXapi(
    api_username=username,
    api_password=password,
    hostname=firewall_ip,
)

try:
    # Check job statuses and retrieve the XML response
    conn.op("show jobs all", cmd_xml=True)
    xml_response = conn.xml_result()

    # If it generated an XML response
    if xml_response:
        # Parse the XML response
        # Note: This XML response sends junk, to get around that, wrap the XML content in a root element
        xml_response = "<root>" + xml_response + "</root>"
        root = ET.fromstring(xml_response)
        # To convert the memory address of 'root' element object, convert it back to a string
        xml_str = ET.tostring(root, encoding="unicode")
        # Print the entire XML content to the terminal. Remove this if unnecessary.
        print(xml_str)

        # To extract and print the job statuses, loop 'all' the job elements and write them to a Dictionary: Key(job_id), Value(status)
        job_entries = root.findall(".//job")
        job_statuses = {}
        for job in job_entries:
            job_id = job.find("id").text if job.find("id") is not None else "N/A"
            status = (
                job.find("status").text if job.find("status") is not None else "N/A"
            )
            job_statuses[job_id] = status 
        for job_id in job_statuses:
            print(f"Job ID: {job_id}, Status: {job_statuses[job_id]}, Firewall_ID: {firewall_ip}")
    else:
        print("XML response is empty or malformed.")

    # Write firewall IP and job statuses to CSV file
    with open("check_all_jobs_status.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(
            [
                "Firewall_IP",
                "Job ID",
                "Status"
            ]
        # Write the dictionary content
        for job_id, status in job_statuses.items():
            writer.writerow([job_id, status, firewall_ip])
    print("Results 'for all jobs' saved for:", firewall_ip)

except pan.xapi.PanXapiError as e:
    print("An error occurred:", e)
except ET.ParseError as e:
    print("An XML parsing error occurred:", e)
