import ipaddress
import os
import time
import paramiko

def get_router_ip():           # Getting from the user input of router ip address, checking the input=ipv4
    while True:
        router_ip_address = input('Please enter your router IP address: ')
        try:
            ipaddress.IPv4Network(router_ip_address)
            return router_ip_address
        except ipaddress.AddressValueError:
            print('You must enter a valid IP address')

host = get_router_ip()
username = ""

while not username:         # Valid the correct credential login
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=username, password=password)
    except paramiko.ssh_exception.AuthenticationException:
        print("Invalid credentials, please try again")
        username = ""

stdin, stdout, stderr = client.exec_command('reboot')   # Sending reboot
time.sleep(10)
count = 0

while count < 120:
    device_check = os.system("ping -c 1 " + host)
    if device_check == 0:
        print('Device is up')
        client.close()
        break
    else:
        print('Device is down')
        count += 1
        time.sleep(1)
