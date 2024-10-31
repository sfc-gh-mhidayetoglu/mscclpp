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

# create a MscclppGroup
network_interface, my_ip = get_netinterface_info()
root_ip = torch.tensor(my_ip, device=my_device)
dist.broadcast(root_ip, src=root_rank)
root_ip = root_ip.item()
ifIpPortTrio = network_interface + ":" + root_ip + ":50000"  # some random port
mscclpp_group = mscclpp_comm.CommGroup(
    interfaceIpPortTrio=ifIpPortTrio, rank=my_rank, size=world_size
)

print(f"Hello from {my_rank}\n")
