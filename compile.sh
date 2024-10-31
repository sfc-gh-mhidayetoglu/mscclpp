unset PIP_INDEX_URL PIP_CERT

# install msccl++
python -m pip install .
# install additional requirements
python3 -m pip install -r ./python/requirements_cuda12.txt
