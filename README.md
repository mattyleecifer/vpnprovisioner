# vpnprovisioner

I don't really use VPNs that much and I don't want to pay some company $5 a month in case I need one. I needed a way to quickly provision a VPN so I could use it whenever I needed it and only pay for the exact time I'm using it. 

This script creates a basic DigitalOcean droplet, runs a script to install OpenVPN, and then downloads the OVPN file into your home directory. You can then import the file into OpenVPN and connect. After you're done, press enter and the script will close and destroy the droplet.

You will have to have an ssh key set up with DigitalOcean before you use this, or you can edit the script so it takes a username and password.



