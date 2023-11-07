'''
Welcome Adventurer! You stand at the endge of the linux kernel, ready to plunge into its depths.
During your journey, you will come accross incomplete pieces of code.
Your task is to complete them and unlock a deeper understanding about eBPF and the linux kernel.

Your first task starts here: Count the number of packets arriving over your main network interface.
'''

from bcc import BPF

# eBPF program code
bpf_program = """
#include <uapi/linux/bpf.h>

/* TODO: Define your shared data structure. What datastructure is appropriate?
 * Hint: https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#maps
 */

int count_packets(struct __sk_buff *skb) {
    /* TODO: Access your shared data structure and increment the packet counter. How fit are you with pointers? (= */

    return XDP_PASS;
}
"""

# Load the BPF program
b = BPF(text=bpf_program, cflags=["-w"])

# Attach the eBPF program to the XDP hook
INTERFACE = "TODO" # What was the name of your network interface again?
b.attach_xdp(dev=INTERFACE, fn=b.load_func("count_packets", BPF.XDP))

# Keep the program running to maintain the XDP hook
try:
    while True:
        num_packets = b.get_table("num_packets") # Name your shared data structure num_packets
        for k, v in num_packets.items():
            print("Packet count: ", v.value, end='\r')
except KeyboardInterrupt:
    pass
finally:
    # Detach the eBPF program from the XDP hook when the program exits
    b.remove_xdp(dev=INTERFACE)
