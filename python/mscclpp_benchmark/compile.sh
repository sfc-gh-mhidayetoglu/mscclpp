#!/bin/bash -x

POD_BASE=dist-training-mhidayetoglu-mscclpp-default0

numnode=$(kubectl -n yak exec $POD_BASE-0 -- cat /etc/volcano/VC_DEFAULT0_NUM)
echo numnode $numnode

for ((i = 0; i < numnode; i++));
do
  echo POD_BASE-$i
  kubectl -n yak exec POD_BASE-$i -- /bin/bash -c "cd /code/users/mhidayetoglu/mscclpp && ./compile.sh"
done

exit

# Define the namespace and pod label selector
NAMESPACE="default"
LABEL_SELECTOR="app=mscclpp"

# Get the list of pods matching the label selector
PODS=$(kubectl get pods -n yak -l $LABEL_SELECTOR -o jsonpath='{.items[*].metadata.name}')

# Loop through each pod and run the compile script
for POD in $PODS; do
    echo "Running compile.sh on pod $POD"
    kubectl exec -n $NAMESPACE $POD -- /bin/bash -c "/code/users/mhidayetoglu/mscclpp/compile.sh"
done