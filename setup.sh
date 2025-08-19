sudo apt install python3
sudo apt install python3-yaml
mkdir /usr/local/bin/nut-wakeonlan/
mkdir /etc/nut/wakeonlan/
mv main.py /usr/local/bin/nut-wakeonlan/main.py
mv nut-wakeonlan.service /etc/systemd/system/nut-wakeonlan.service
