# **Animal Monitor System setup**

# *Requirements:*
* Raspberry Pi ( 3B or newer is recomended )
* SD card and Reader (32 GB or higher recomended)
* Keyboard
* Mouse
* Monitor



## Installing Raspberry Pi OS
1. Head to the [the Raspberry Pi website](https://www.raspberrypi.org/software/) and follow the steps to install Raspberry Pi Imager for your computer.

2. Connect your SD card to the computer

3. In Raspberry Pi Imager, Choose the 'RASPBERRY PI OS (32-BIT)' operating system and select your SD card then click 'Write'.


## Setting up the OS
1. Take out the SD card from the reader and plug it into the sd slot on the Raspberry Pi.

2. Connect your raspbery PI usb cable, the monitor (HDMI) and the usb keyboard and mouse.  

3. once the pi boots up, follow the setup prompt and choose country and timezone. select a new password for the pi and make sure to remember it.

4. setup your wifi connection on the pi by running the following command on the terminal (icon found in top left):
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

5. Scroll to the end of the file and add the following to the file to configure your network:
```
network={
   ssid="Test Wifi Network"
   psk="SecretPassWord"
}
```
***remember to replace ssid with your network name and psk with your password***

Save and close the file by pressing Ctrl+X followed by Y. At this point the Raspberry Pi should automatically connect to your network.

6. reboot the pi by clicking the pi symbol(raspberry in the top left) and choose shutdown then reboot.


## enable SSH, serial and i2c
1. open the terminal on the pi and run:
```
sudo raspi-config.
```

2. Use the arrows on your keyboard to select Interfacing Options.
3. Select the P2 SSH option on the list.
4. Select <Yes> on the “Would you like the SSH server to be enabled?” prompt.
5. select interface option again and this time turn on i2c and and Serial port the same way as before.
6. select finish once done.
7. run the command:
```
sudo reboot
```


## Seting up GitHub

####Configure git and update packages

1. open the terminal on the pi and run:
```
sudo apt update
```
2. check that git is installed  by runing:
```
git --version
```
if git is not installed, run the following command to install git:
```
sudo apt install git
```

#### Adding git credidentials

3. To add a username:
```
git config -–global user.name “USERNAME”
```
make sure to substitute your github username above instead of USERNAME

4. To add an email:
```
git config -–global user.email “email@example.ca”
```
make sure to substitute your github email above instead of “email@example.ca”

5. Clone the HIFU_AnimalMonitor Repository from github by running the following command:
```
git clone https://github.com/AmineBenaceur/HIFUAnimalMonitor.git
```

6. You will be asked for your username and password again, the pull should finish quickly after.
