winAD-APT
========



winAD-APT was created  by phrism, putting some common windows AD exploit together and made this framework to make AD pentesting more easily.

winAD-APT is "windows active directory auto pentesting framework", it is made by python streamlit so it has a web ui for users to easily use command to pentest a windows environment .winAD-APT is actually a comand integrated auto run tool, in which you can just input your target ip,domain or credentials and click a button to get a pentesting result.

What can winAD-apt DO?
----------------------------

 * Nmap scan and parameter customize
 * Information gather for a target
 * Lateral penetration for the next step
 * Permission Sploit for priviledge escalation
 * hashcat and john to crack a password
 * All the history command for storage 
 * view and edit files on system and take note easily
 * still developing





Setup
=====

There are two steps for you to install and run this framework, actually all you need to do is make sure all the command can be runned.
#### step1

Impacket plays an irreplaceable role in winowos AD pentest, in this framework, you need to install the main forge of impacket [fortra/impacket](https://github.com/fortra/impacket) from [https://github.com/fortra/impacket](https://github.com/fortra/impacket),   [GetUserSPNs.py](https://github.com/ShutdownRepo/impacket/blob/master/examples/GetUserSPNs.py) from [https://github.com/ShutdownRepo/impacket/](https://github.com/ShutdownRepo/impacket/), and [decledit.py](https://github.com/ThePorgs/impacket/blob/master/examples/dacledit.py) from [https://github.com/ThePorgs/impacket](https://github.com/ThePorgs/impacket), all the impacket python script should be put into your environment variable so you can use them anywhere on your system, you can just change you /etc/profile to achieve this.

#### step2

Apart from impacket, there are other software or tool you should install, you can just run the check script to figure it out;

    chmod +x check.sh; ./check.sh


Screenshot
==========
![RUNOOB 1](https://github.com/phrism/WinAD-APT/tree/main/screenshot/1.png)
![RUNOOB 2](https://github.com/phrism/WinAD-APT/tree/main/screenshot/2.png)
![RUNOOB 3](https://github.com/phrism/WinAD-APT/tree/main/screenshot/3.png)
![RUNOOB 4](https://github.com/phrism/WinAD-APT/tree/main/screenshot/4.png)
![RUNOOB 5](https://github.com/phrism/WinAD-APT/tree/main/screenshot/5.png)



