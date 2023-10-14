#!/bin/bash

# Check if Streamlit is installed
if pip show streamlit &> /dev/null; then
  echo -e "\e[32mstreamlit is installed.\e[0m"
else
  echo -e "\e[31mstreamlit is not installed.\e[0m"
  echo "To install Streamlit, run the following command: pip install streamlit"
fi
if which nmap &> /dev/null; then
  # nmap is installed, display a green prompt
  echo -e "\e[32mnmap is installed.\e[0m"
else
  # nmap is not installed, display a red prompt and installation instructions
  echo -e "\e[31mnmap is not installed."
  
  # Check if the system is using apt or yum package manager and provide instructions
  if [ -n "$(command -v apt-get)" ]; then
    echo "Please install nmap using the following command:"
    echo "sudo apt-get install nmap"
  elif [ -n "$(command -v yum)" ]; then
    echo "Please install nmap using the following command:"
    echo "sudo yum install nmap"
  else
    echo "Please install nmap using the package manager for your system."
  fi
  
  echo -e "\e[0m"
fi


# Check if ftp is installed
if command -v ftp &> /dev/null; then
    # If ftp is installed, print a green prompt
    echo -e "\e[32mftp is installed.\e[0m"
else
    # If ftp is not installed, print a red prompt and ask to install it
    echo -e "\e[31mftp is not installed.\e[0m"
    
    # Check if apt is available and prompt to install using apt
    if command -v apt-get &> /dev/null; then
        echo "You can install ftp using apt:"
        echo "sudo apt-get install ftp"
    # Check if yum is available and prompt to install using yum
    elif command -v yum &> /dev/null; then
        echo "You can install ftp using yum:"
        echo "sudo yum install ftp"
    else
        # If neither apt nor yum is available, provide a general message
        echo "Please install ftp using your package manager."
    fi
fi
if which smbclient &> /dev/null; then
  # smbclient is installed (green prompt)
  echo -e "\e[32msmbclient is installed.\e[0m"
else
  # smbclient is not installed (red prompt)
  echo -e "\e[31msmbclient is not installed.\e[0m"
  
  # Check if the system uses apt (Debian/Ubuntu) or yum (RHEL/CentOS)
  if which apt &> /dev/null; then
    echo "To install smbclient, run: sudo apt install smbclient"
  elif which yum &> /dev/null; then
    echo "To install smbclient, run: sudo yum install smbclient"
  else
    echo "Please install smbclient using your system's package manager."
  fi
fi
# Check if ldapsearch is installed
if command -v ldapsearch &> /dev/null; then
  # ldapsearch is installed, display a green prompt
  echo -e "\e[32mldapsearch is installed.\e[0m"
else
  # ldapsearch is not installed, display a red prompt and provide installation instructions
  echo -e "\e[31mldapsearch is not installed.\e[0m"
  echo "To install ldapsearch, you can use one of the following commands:"
  echo "For Ubuntu/Debian:"
  echo "  sudo apt-get install ldap-utils"
  echo "For CentOS/RHEL:"
  echo "  sudo yum install openldap-clients"
fi
if which rpcclient &> /dev/null; then
  # rpcclient is installed (Green prompt)
  echo -e "\e[32mrpcclient is installed.\e[0m"
else
  # rpcclient is not installed (Red prompt)
  echo -e "\e[31mrpcclient is not installed.\e[0m"
  
  # Check if apt or yum is available and ask to install rpcclient
  if command -v apt &> /dev/null; then
    echo "You can install rpcclient using apt with the following command:"
    echo "sudo apt install samba-common-bin"
  elif command -v yum &> /dev/null; then
    echo "You can install rpcclient using yum with the following command:"
    echo "sudo yum install samba-client"
  else
    echo "Please install rpcclient manually for your system."
  fi
fi
if which faketime &> /dev/null; then
    # faketime is installed, display a green prompt
    echo -e "\e[32mfaketime is installed.\e[0m"
else
    # faketime is not installed, display a red prompt
    echo -e "\e[31mfaketime is not installed.\e[0m"

    # Check if apt or yum package manager is available
    if which apt &> /dev/null; then
        echo "You can install faketime using apt. Run the following command: sudo apt install faketime"
    elif which yum &> /dev/null; then
        echo "You can install faketime using yum. Run the following command: sudo yum install faketime"
    else
        echo "Please install faketime manually using your package manager."
    fi
fi
if command -v bloodhound-python &>/dev/null; then
  # Installed, display green prompt
  echo -e "\e[32mbloodhound-python is installed.\e[0m"
else
  # Not installed, display red prompt
  echo -e "\e[31mbloodhound-python is not installed.\e[0m"

  # Check if apt or yum is available
  if command -v apt &>/dev/null; then
    echo "You can install bloodhound-python using apt with the following command: sudo apt install bloodhound-python"
  elif command -v yum &>/dev/null; then
    echo "You can install bloodhound-python using yum with the following command: sudo yum install bloodhound-python"
  else
    echo "Please install bloodhound-python manually using your package manager."
  fi
fi
if dpkg -l | grep -q 'bloodhound'; then
  echo -e "\e[32mbloodHound is installed.\e[0m"
else
  echo -e "\e[31mbloodHound is not installed.\e[0m"

  # Check if apt or yum package manager is available
  if command -v apt &> /dev/null; then
    echo "You can install BloodHound using apt: sudo apt install bloodhound"
  elif command -v yum &> /dev/null; then
    echo "You can install BloodHound using yum: sudo yum install bloodhound"
  else
    echo "Please install BloodHound using your system's package manager."
  fi
fi
if command -v hashcat &> /dev/null; then
    # Hashcat is installed, display a green prompt
    echo -e "\e[32mhashcat is installed.\e[0m"
else
    # Hashcat is not installed, display a red prompt and ask to install
    echo -e "\e[31mhashcat is not installed.\e[0m"

    # Check the package manager and prompt accordingly
    if command -v apt &> /dev/null; then
        echo "You can install Hashcat using apt: sudo apt install hashcat"
    elif command -v yum &> /dev/null; then
        echo "You can install Hashcat using yum: sudo yum install hashcat"
    else
        echo "Please install Hashcat using your system's package manager."
    fi
fi
if which john &> /dev/null; then
  # 'john' is installed, display a green prompt
  echo -e "\e[32mjohn is installed.\e[0m"
else
  # 'john' is not installed, display a red prompt and suggest installation
  echo -e "\e[31mjohn is not installed.\e[0m"

  # Check which package manager is available
  if command -v apt &> /dev/null; then
    # 'apt' package manager is available, suggest using it
    echo "You can install 'john' with 'apt' using the following command: sudo apt install john"
  elif command -v yum &> /dev/null; then
    # 'yum' package manager is available, suggest using it
    echo "You can install 'john' with 'yum' using the following command: sudo yum install john"
  else
    # Neither 'apt' nor 'yum' is available, so provide a generic message
    echo "Please install 'john' using the appropriate package manager for your system."
  fi
fi
if ! which crackmapexec &> /dev/null; then
  # 'crackmapexec' is not installed, display a red prompt and suggest installation
  echo -e "\e[31m'crackmapexec' is not installed.\e[0m"

  # Check which package manager is available
  if command -v apt &> /dev/null; then
    # 'apt' package manager is available, suggest using it
    echo "You can install 'crackmapexec' with 'apt' using the following command:"
    echo "sudo apt install crackmapexec"
  elif command -v yum &> /dev/null; then
    # 'yum' package manager is available, suggest using it
    echo "You can install 'crackmapexec' with 'yum' using the following command:"
    echo "sudo yum install crackmapexec"
  else
    # Neither 'apt' nor 'yum' is available, so provide a generic message
    echo "Please install 'crackmapexec' using the appropriate package manager for your system."
  fi
else
  # 'crackmapexec' is installed, check its version
  cme_version=$(crackmapexec 2>&1 | grep -oP '[0-9]+\.[0-9]+\.[0-9]+')
  # Check if the version is lower than 5.4.0
  if [[ -z $cme_version || "$(echo "$cme_version 5.4.0" | awk '{print ($1 < $2)}')" == 1 ]]; then
    echo -e "\e[31mcrackmapexec	 version is too low (version $cme_version). Please upgrade to version 5.4.0 or higher.\e[0m"
  else
    echo -e "\e[32mcrackmapexec is installed (version $cme_version).\e[0m"
  fi
fi
check_kerbrute() {
  if command -v kerbrute_linux_amd64 &> /dev/null; then
    echo -e "\e[32m'kerbrute_linux_amd64' is installed.\e[0m"
  else
    echo -e "\e[31m'kerbrute_linux_amd64' is not installed.\e[0m"
    echo "You can install 'kerbrute_linux_amd64' from the following GitHub repository:"
    echo "https://github.com/ropnop/kerbrute"
  fi
}

check_pyLDAPmonitor() {
  if which pyLDAPmonitor.py &> /dev/null; then
    echo -e "\e[32mpyLDAPmonitor.py is installed.\e[0m"
  else
    echo -e "\e[31mpyLDAPmonitor.py is not installed.\e[0m"
    echo "You can install 'pyLDAPmonitor.py' from the following GitHub repository:"
    echo "https://github.com/p0dalirius/LDAPmonitor"
    echo "After installation, make sure to set the example dir to your environment variable"
  fi
}

# Run the function to check 'pyLDAPmonitor.py'
check_pyLDAPmonitor

check_powerview() {
  if which powerview.py &> /dev/null; then
    echo -e "\e[32mpowerview.py is installed.\e[0m"
  else
    echo -e "\e[31mpowerview.py is not installed.\e[0m"
    echo "You can install 'powerview.py' from the following GitHub repository:"
    echo "https://github.com/tevora-threat/SharpView"
    echo "After installation, make sure to set the example dir to your environment variable"
  fi
}

# Run the function to check 'pyLDAPmonitor.py'
check_powerview

echo -e "\e[33mFor impacket installation, please check the github for more details"
