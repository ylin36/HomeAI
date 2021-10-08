## Current system Spec
Runs against windows 11 with WSL2, cuda11. 
Inference done against RTX3080
Outputs to VCXSRV since wls2 doesn't have gui

## get ip addresses of ubuntu host
using wsl type in 'ip addr' to get ip address of the ubuntu host

## open firewall
advanced settings in windows defender firewall
inbound rules, new rule for port.

## to add forward
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=172.30.90.228

## to remove
netsh interface portproxy delete v4tov4 listenport=5000 listenaddress=0.0.0.0

## python in wsl
code .
install wsl plugin
install python plugin

## opencv no ui work around
install https://sourceforge.net/projects/vcxsrv/
launch from program files xlaunch.exe.
-1
start no client
Disable access control

Set environment variable
export DISPLAY=<windows_ip>:0