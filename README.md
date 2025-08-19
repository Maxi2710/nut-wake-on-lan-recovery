# nut-wake-on-lan-recovery
A Python daemon that monitors UPS status via NUT, sends Wake-on-LAN packets to clients when power is restored, and fully works with both IPv6 and IPv4.

---

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

Edit the config file:

```bash
nano /etc/nut/wakeonlan/config.yml
```

This file consists of two main sections: **`nut`** and **`wol`**.


### `nut` section
Defines how to connect to your UPS using NUT (Network UPS Tools).

- `ups_name`: The name of your UPS as defined in your NUT configuration.
- `ip`: The IP address (IPv6 or IPv4) of the NUT server running your UPS daemon.

Example:

```yaml
nut:
  ups_name: "ups"
  ip: "2001:db8::200"
```


### `wol` section
Contains a list of clients that should be woken up via Wake-on-LAN after the power is restored. You can define multiple clients by adding multiple entries under `wol`.

Each entry has the following options:

- `mac`: The MAC address of the client's network interface.
- `ip_version`: Whether to send the WOL packet via IPv6 (`6`) or IPv4 (`4`).
- `interface`: The local network interface used to send the WOL packet (e.g., `eth0`).
> [!NOTE] 
> You can list available interfaces with `ip a`.
> The interface name is only required when using IPv6.

Example:

```yaml
wol:
  - mac: "b3:44:bd:da:b4:49"
    ip_version: 6
    interface: "eth0"
```

---

## Full Example

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

---

## Service Management
After any changes in the `config.yml` it is required to restart the systemd service:
```bash
sudo systemctl restart nut-wakeonlan
```

If installed via `setup.sh`, the daemon should be available as a systemd service. You can control it with the following commands:

```bash
# Start the service
sudo systemctl start nut-wakeonlan

#Restart the service
sudo systemctl restart nut-wakeonlan

# Enable it at boot
sudo systemctl enable nut-wakeonlan

# Check status
systemctl status nut-wakeonlan
```

---

## Troubleshooting & Tips


- **WOL packets not received:**
  - Ensure Wake-on-LAN is enabled in the client's BIOS/UEFI.
  - Check that the correct MAC address is used.
  - For IPv6, make sure the correct interface is specified and the network supports IPv6 multicast.

- **UPS connection issues:**
  - Verify the NUT server IP and UPS name are correct.
  - Make sure the NUT service is running and accessible from the daemon host.

- **Logs:**
  - Check system logs with `journalctl -u nut-wakeonlan` for any errors or status messages.

- **Network interface:**
  - Use `ip a` to list available network interfaces.
  - The interface parameter is mandatory for IPv6 and optional for IPv4.

- **Running manually:**
  - You can run the daemon manually for debugging:
  ```bash
  sudo python3 /usr/local/bin/nut-wakeonlan.py
  ```
