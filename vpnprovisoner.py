import os
import time
import digitalocean, random
# import pyperclip

regions = ['nyc1','nyc3','ams3','sfo3','sgp1','lon1','fra1','tor1','blr1']
server = random.choice(regions)

# DigitalOcean Key
dokey = "insertkey"

# Set up droplet
manager = digitalocean.Manager(token=dokey)
keys = manager.get_all_sshkeys()
droplet = digitalocean.Droplet(token=dokey,
                               name='VPN',
                               region=server, # New York 2
                               image='ubuntu-20-04-x64', # Ubuntu 20.04 x64
                               size_slug='s-1vcpu-1gb',  # 1GB RAM, 1 vCPU
                               ssh_keys=keys,
                               backups=False)
droplet.create()

while True:
    my_droplets = manager.get_all_droplets()
    print(my_droplets)
    #need to loop this until ip != None
    ip = my_droplets[0].ip_address
    if type(ip) == str:
        break
    time.sleep(5)
    print("Waiting for droplet to respond...")
print("Droplet Created!")

# pyperclip.copy("ssh root@" + ip)

# Set up VPN
import paramiko
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
while True:
    try:
        ssh.connect(ip, 22, "root")
        break
    except:
        print("Waiting for SSH...")
        time.sleep(5)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh\nchmod +x openvpn-install.sh\nexport AUTO_INSTALL=y\n./openvpn-install.sh\n")
print("Setting up VPN...")

# Download OVPN
os.chdir(os.path.expanduser("~"))
from scp import SCPClient
while True:
    try:
        with SCPClient(ssh.get_transport()) as scp:
            scp.get('~/client.ovpn')
        break
    except:
        print("OVPN not ready...")
        time.sleep(5)
ssh.close()
print("OVPN file downloaded!")

# Fix OVPN file with IP address
import re
textfile = open("client.ovpn", 'r')
filetext = textfile.read()
textfile.close()
clean = re.sub("remote (.+?) 1194", "remote " + ip + " 1194", filetext, flags=re.S)
with open("client.ovpn", "w") as text_file:
    text_file.write(clean)
print("OVPN file cleaned!")

input("Press Enter to destroy...")

droplet.shutdown()
print("Droplet Shut down")
droplet.destroy()
# while True:
#     my_droplets = manager.get_all_droplets()
#     if len(my_droplets) != 0:
#         for i in my_droplets:
#             i.destroy()
print("Droplet destroyed!")
