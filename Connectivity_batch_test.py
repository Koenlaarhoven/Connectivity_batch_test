import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import socket


class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


my_platform = '-n' if platform.system().lower() == 'windows' else '-c'

# Display own IP and username
host_self = socket.gethostname()
IP_self = socket.gethostbyname(host_self)
# f"{bcolors.HEADER} starts a color
# f"{bcolors.ENDC}" ends a color
print(f"{bcolors.HEADER}Your Computer Name is : " + host_self)
print("Your Computer IP Address is: " + IP_self+f"{bcolors.ENDC}"+"\n")


# Definition of all the addresses that need to be reached


class hostnames:
    IPs = []
    devices = []
    destinations = []
    sites = []
    instances = []

    def __init__(self, IP, device, destination, site, port=22):
        self.IP = IP
        self.port = port
        self.IPs.append(IP)
        self.device = device
        self.devices.append(device)
        self.destination = destination
        self.destinations.append(destination)
        self.site = site
        self.sites.append(site)
        # track all instances of this class (h1, h2 etc.)
        self.__class__.instances.append(self)

    # Sends a ping through the command line. the number indicates the number of packets
    # Returns True if host (str) responds to a ping request.
    # Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.

    def ping(self):
        host = self.IP
        res_ping = subprocess.call(['ping', my_platform, '1', host])
        if res_ping == 0:
            self.res_ping = res_ping = host + ' ping OK!'
        elif res_ping == 2:
            self.res_ping = res_ping = host + ' no response!'
        else:
            self.res_ping = res_ping = host + ' ping failed!'

    def check_port(self):
        host = self.IP
        port = self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        SSH_status = s.connect_ex((host, port))
        if SSH_status == 0:
            self.res_SSH = ' port ' + str(port) + ' is open!'
        else:
            self.res_SSH = ' port ' + str(port) + ' is closed!'
        s.close()


############################# data #############################################
h1 = hostnames(
    '100.100.100.1', 'APPLICATION1', 'in-Band', 'SITE1')
h2 = hostnames(
    '100.100.100.2', 'APPLICATION2', 'in-Band', 'SITE1')
h3 = hostnames(
    '100.100.111.1', 'MACHINE1', 'APIC in-band', 'SITE2')
h4 = hostnames(
    '100.100.111.2', 'MACHINE2', 'Node 1 in-band', 'SITE2')
h5 = hostnames(
    '100.100.111.3', 'MACHINE3', 'Spine 1 in-band', 'SITE2')
h6 = hostnames(
    '100.100.222.1', 'MACHINE4', 'APIC in-band', 'SITE1')
h7 = hostnames(
    '100.100.222.2', 'MACHINE5', 'Node 1 in-band', 'SITE1')
h8 = hostnames(
    '100.100.222.3', 'MACHINE6', 'Spine 1 in-band', 'SITE1')
################################################################################



for hostname_instance in hostnames.instances:
    # each instance here is h1, h2 etc.
    print(f"{bcolors.OKGREEN}" + hostname_instance.IP + f"{bcolors.ENDC}")
    
    hostname_instance.ping()

    # Checks whether the port of the specified IP is open
    hostname_instance.check_port()

    device = hostname_instance.device
    destination = hostname_instance.destination
    site = hostname_instance.site
    res_ping = hostname_instance.res_ping
    res_SSH = hostname_instance.res_SSH

    print("Device {}  which is {}  on site  {}  results in: \n {}  {}  \n".format(
        device, destination, site, res_ping, res_SSH)'")
