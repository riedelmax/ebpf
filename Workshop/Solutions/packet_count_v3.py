from bcc import BPF

# eBPF program code
bpf_program = """
#include <uapi/linux/bpf.h>

#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/ip.h>

struct tcphdr {
    __be16 source;
    __be16 dest;
};

int count_packets(struct xdp_md *skb) {

    void* data_end = (void*)(long)skb->data_end;
    void* data = (void*)(long)skb->data;

    struct ethhdr *eth = data;

    if (data + sizeof(struct ethhdr) > data_end) {
        return XDP_PASS;
    }

    if (eth->h_proto == htons(ETH_P_IP)) {
        struct iphdr *ip = (struct iphdr *)(eth + 1);

        /* TODO: Again with the verifier complaining! But you know what to do, right? */
        if (data + sizeof(struct ethhdr) + sizeof(struct iphdr) > data_end) {
            return XDP_PASS;
        }

        /* TODO: How can you access the protocol? Hint: Check the definition of the iphdr struct. */
        if (ip->protocol == IPPROTO_TCP) {
            struct tcphdr *tcph = (struct tcphdr *)(ip + 1);

            if (data + sizeof(struct ethhdr) + sizeof(struct iphdr) + sizeof(struct tcphdr) > data_end) {
                return XDP_PASS;
            }

            uint16_t src_port = ntohs(tcph->source);
            uint16_t dest_port = ntohs(tcph->dest);

            bpf_trace_printk("src_port=%u dest_port=%u", src_port, dest_port);
        }
    }

    return XDP_PASS;
}
"""

# Load the BPF program
b = BPF(text=bpf_program, cflags=["-w"])

# Attach the eBPF program to the XDP hook
INTERFACE = "eth0"  # Replace with your network interface
b.attach_xdp(dev=INTERFACE, fn=b.load_func("count_packets", BPF.XDP))

# Keep the program running to maintain the XDP hook

try:
    b.trace_print()
except KeyboardInterrupt:
    pass
finally:
    # Detach the eBPF program from the XDP hook when the program exits
    b.remove_xdp(dev=INTERFACE)
