import torch
import torch.distributed as dist

# initialize
dist.init_process_group(backend='nccl')
my_rank = dist.get_rank()
world_size = dist.get_world_size()
torch.cuda.set_device(my_rank % torch.cuda.device_count())
my_device = torch.cuda.current_device()
root_rank = 7

from mscclpp_op import (
    MscclppAllReduce1,
    MscclppAllReduce2,
    MscclppAllReduce3,
    MscclppAllReduce4,
    MscclppAllReduce5,
    MscclppAllReduce6,
)
# from nccl_op import NcclAllReduce
import mscclpp.comm as mscclpp_comm
import ipaddress
import netifaces as ni

def is_valid(ip):
    """
    Check if the IP address is valid for connecting to other devices.
    This excludes loopback (127.0.0.1) and link-local (169.254.x.x) addresses.
    """
    ip_obj = ipaddress.ip_address(ip)
    return not (ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast)

def get_netinterface_info():
    """
    Returns the name of the first network interface with a valid IP address that it finds.
    """
    interfaces = ni.interfaces()
    for interface in interfaces:
        addresses = ni.ifaddresses(interface)
        if ni.AF_INET in addresses:
            for addr in addresses[ni.AF_INET]:
                ip_address = addr["addr"]
                if is_valid(ip_address):
                    print(f"Selected Interface: {interface}, IP Address: {ip_address}")
                    return interface, ip_address
    return None, None

# create a MscclppGroup
network_interface, my_ip = get_netinterface_info()
my_ip_tensor = torch.tensor([int(octet) for octet in my_ip.split('.')], device=my_device, dtype=torch.int32)
dist.broadcast(my_ip_tensor, src=root_rank)
root_ip = '.'.join(map(str, my_ip_tensor.tolist()))
ifIpPortTrio = network_interface + ":" + root_ip + ":50000"  # some random port
mscclpp_group = mscclpp_comm.CommGroup(
    interfaceIpPortTrio=ifIpPortTrio, rank=my_rank, size=world_size
)

print(f"Hello from {my_rank}\n")
