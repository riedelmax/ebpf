# Setup a Lima VM that lets you run eBPF Programs

1. Install Lima using brew  
   `brew install lima`
2. Check installation  
   `lima --version`
3. Read and adapt the VMs config in `ubuntu-lts-ebpf.yaml`
4. Run the VM  
   `limactl start --name=ebpf-lima-vm ./ubuntu-lts-ebpf.yaml`  
   `Proceed with the current configuration`
5. Connect to your VM via ssh on `localhost:2222`. I recommend to use VSCode and the VSCode Remote Extension. Entering `Remote-SSH: Connect to Host...` should bring the VM up.