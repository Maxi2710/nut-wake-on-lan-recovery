# nut-wake-on-lan-recovery
A python daemon that monitors UPS status via NUT, sends Wake-on-LAN packets to clients when power is restored and fully workes with IPv6 and IPv4 <br/>


## Installation (Ubuntu / Debian)
Install git:
```bash
sudo apt install git
```
Clone the repository and run setup.sh:
```bash
sudo git clone https://github.com/Maxi2710/nut-wake-on-lan-recovery.git && cd nut-wake-on-lan-recovery && bash setup.sh
```

---

## Configuration
Edit config file: ```nano /etc/nut/wakeonlan/config.yml``` <br/>
This file consists of two main sections: ```nut``` and ```wol``` 
<br/>


### ```nut``` section
This defines how to connect to your UPS using NUT (Network UPS Tools).
<br/>
- ```ups_name```: The name of you UPS as defined in you NUT configuration.
- ```ip```: The IP address (IPv6 or IPv4) of the NUT server running your UPS deamon.

Example:
```yaml
nut:
  ups_name: "ups"
  ip: "2001:db8::200"
```


### ```wol``` section
This contains a list of clients that should be woken up via Wake-on-LAN after the power is restored.
<br/>
Each entry has the following options:
<br/>
- ```mac```: The MAC address of the client's network interface.
- ```ip_version```: Whether to send the WOL packet via IPv6(```6```) or IPv4(```4```).
- ```interface```: The local network interface used to send the WOL packet (e.g., ```eth0```).
  Node: you can obtain the interface name with ```ip a```
        The interface name is only important if you use IPv6
Example:
```yaml
wol:
  - mac: "b3:44:bd:da:b4:49"
    ip_version: 6
    interface: "eth0"
```
<br/>
## Full Example:
```yaml
nut:
  ups_name: "ups"
  ip: "2001:db8::200"


wol:
  - mac: "b3:44:bd:da:b4:49"
    ip_version: 6
    interface: "eth0"

  - mac: "1c:49:5e:84:62:63"
    ip_version: 6
    interface: "eth0"
```
