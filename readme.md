## get ip addresses of ubuntu host
using wsl type in 'ip addr' to get ip address of the ubuntu host

## open firewall
advanced settings in windows defender firewall
inbound rules, new rule for port.

## to add forward
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=172.30.90.228

## to remove
netsh interface portproxy delete v4tov4 listenport=5000 listenaddress=0.0.0.0
