from bcc import BPF

# eBPF program code
bpf_program = """
#include <uapi/linux/bpf.h>

BPF_HASH(num_packets, u64);

int count_packets(struct __sk_buff *skb) {
    u64 zero = 0, *count;
    u64 key = 0;
    count = num_packets.lookup_or_try_init(&key, &zero);
    if (count) {
        (*count)++;
    }

    return XDP_PASS;
}
"""

# Load the BPF program
b = BPF(text=bpf_program, cflags=["-w"])

# Attach the eBPF program to the XDP hook
INTERFACE = "enp0s3"  # Replace with your network interface
b.attach_xdp(dev=INTERFACE, fn=b.load_func("count_packets", BPF.XDP))

# Keep the program running to maintain the XDP hook
try:
    while True:
        num_packets = b.get_table("num_packets")
        for k, v in num_packets.items():
            print("Packet count: ", v.value, end='\r')
except KeyboardInterrupt:
    pass
finally:
    # Detach the eBPF program from the XDP hook when the program exits
    b.remove_xdp(dev=INTERFACE)
