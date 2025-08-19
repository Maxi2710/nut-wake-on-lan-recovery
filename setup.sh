#!/bin/bash

#Exit script if a command fails
set -e

echo -e "\e[32mInstalling required packeges...\e[0m"
sudo apt update
sudo apt install nut-client python3 python3-yaml

echo -e "\e[32mCreating directories...\e[0m"
sudo mkdir /usr/local/bin/nut-wakeonlan/
sudo mkdir /etc/nut/wakeonlan/

echo -e "\e[32mMoving files to the correct location...\e[0m"
sudo mv main.py /usr/local/bin/nut-wakeonlan/main.py
sudo mv nut-wakeonlan.service /etc/systemd/system/nut-wakeonlan.service
sudo mv config.yml /etc/nut/wakeonlan/config.yml

echo -e "\e[32mMaking 'main.py' executable...\e[0m"
sudo chmod +x /usr/local/bin/nut-wakeonlan/main.py

echo -e "\e[32mReloading systemd...\e[0m"
sudo systemctl daemon-reload

echo -e "\e[32mEnabeling and starting service...\e[0m"
sudo systemctl enable nut-wakeonlan.service
sudo systemctl start nut-wakeonlan.service

echo -e "\e[32mSetup complete!\e[0m"

echo -e "\e[32mRemoving repository folder...\e[0m"
cd ..
sudo rm -rf nut-wake-on-lan-recovery
