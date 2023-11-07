'''
Congratulations on beating level 1!

Now that you know how many packets arrive, you would like to differentiate between IPV4 and IPV6 packets.
For this, you will need to actually look inside the packet contents.
'''

from bcc import BPF

# eBPF program code
bpf_program = """
#include <uapi/linux/bpf.h>

#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/ip.h>

/* TODO: Define your shared data structure. What datastructure is appropriate?
 * Hint: https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#maps
 */

int count_packets(struct xdp_md *skb) {

    void* data_end = (void*)(long)skb->data_end;
    void* data = (void*)(long)skb->data;

    struct ethhdr *eth = data;

    /* TODO: Something is missing here. Why is the verifier complaining? There is a hint at the end of this file. */

    if (eth->h_proto == htons(ETH_P_IP)) {
        /* TODO: Count IPV4 packets
    }

    if (eth->h_proto == htons(ETH_P_IPV6)) {
        /* TODO: Count IPV6 packets
    }

    return XDP_PASS;
}
"""

# Load the BPF program
b = BPF(text=bpf_program, cflags=["-w"])

# Attach the eBPF program to the XDP hook
INTERFACE = "enp0s3"
b.attach_xdp(dev=INTERFACE, fn=b.load_func("count_packets", BPF.XDP))

# Keep the program running to maintain the XDP hook
try:
    ipv4, ipv6 = 0, 0;
    while True:
        # TODO: Extract the counts from your shared datastructure
        pass
except KeyboardInterrupt:
    pass
finally:
    # Detach the eBPF program from the XDP hook when the program exits
    b.remove_xdp(dev=INTERFACE)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Hint: To satisfy the verifier you have to make sure that you don't access memory that is not belonging to your processs.
    #       Write a check to ensure that there is enough data in the packet to safely access and process the ethernet header.
