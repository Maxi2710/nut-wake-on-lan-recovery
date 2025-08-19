# nut-wake-on-lan-recovery
A python daemon that monitors UPS status via NUT, sends Wake-on-LAN packets to clients when power is restored and fully workes with IPv6 and IPv4 <br/>


## Installation
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

### ```nut``` section
This defines how to connect to your UPS using NUT (Network UPS Tools). <br/>
- ```ups_name```: The name of you UPS as defined in you NUT configuration.
- ```ip```: The IP address (IPv6 or IPv4) of the NUT server running your UPS deamon.
Example:
```yaml
nut:
  ups_name: "ups"
  ip: "2001:db8::200"
```
