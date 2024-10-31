
export OPAL_PREFIX=/opt/amazon/openmpi

ARG_TCP="--mca pml ^cm --mca btl tcp,self --mca btl_tcp_if_exclude lo,docker0"

mpirun -tag-output -np 8 $ARG_TCP python3 ./python/mscclpp_benchmark/allreduce_bench.py

