from bcc import BPF

# eBPF program code
bpf_program = """
#include <uapi/linux/bpf.h>

#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/ip.h>

BPF_HASH(num_packets, u64);

int count_packets(struct xdp_md *skb) {

    void* data_end = (void*)(long)skb->data_end;
    void* data = (void*)(long)skb->data;

    struct ethhdr *eth = data;

    if (data + sizeof(struct ethhdr) > data_end) {
        return XDP_PASS;
    }

    if (eth->h_proto == htons(ETH_P_IP)) {
        u64 zero = 0, *count;
        u64 key = 0;
        count = num_packets.lookup_or_try_init(&key, &zero);
        if (count) {
            (*count)++;
        }
    }

    if (eth->h_proto == htons(ETH_P_IPV6)) {
        u64 zero = 0, *count;
        u64 key = 1;
        count = num_packets.lookup_or_try_init(&key, &zero);
        if (count) {
            (*count)++;
        }
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
    ipv4, ipv6 = 0, 0;
    while True:
        num_packets = b.get_table("num_packets")
        for k, v in num_packets.items():
            if k.value == 0: ipv4 = v.value 
            else: ipv6 = v.value
        print("IPV4: ", ipv4, "IPV6: ", ipv6, end='\r')
except KeyboardInterrupt:
    pass
finally:
    # Detach the eBPF program from the XDP hook when the program exits
    b.remove_xdp(dev=INTERFACE)
