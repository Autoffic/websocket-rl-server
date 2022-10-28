# websocket-rl-server

## If you intend to use it over lan
On most of the machines, the ports isn't exposed over LAN. Inorder to bypass this, there are two options:

### Firewall
One way is to unblock the port, process may differ in different platforms. On windows, windows firewall is used and on linux some firewall controller is used. Inorder to unblock for this websocket, tcp inbound(and outbound) connection must be allowed.<br>
- [windows](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-firewall/create-an-inbound-port-rule). Also create outbound rule.
- [linux](https://www.ibm.com/docs/es/spectrum-scale/5.1.0?topic=firewall-examples-how-open-ports): Example(OpenSuse): `sudo firewall-cmd --open-port 5000/tcp`

### ssh
Another way is to connect via ssh and link to the server directly in clients. For this purpose, the server must host a ssh server too.<br>
For linking through openssh: `ssh -L {client-port}:{server-ip}:{server-port} user@{server-ip}. <br>
Example: `ssh -L 5000:192.168.0.108:5000 user@192.168.0.108` <br>
This links the server's port 5000 to clients ports 5000 so `localhost:5000` will connect to the server's port.