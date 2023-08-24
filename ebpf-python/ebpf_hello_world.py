#!/usr/bin/python3

# BPF compiler Collection (BCC) provides front-ends in Python and Lua.
# For more information see: https://github.com/iovisor/bcc
from bcc import BPF

# Define the actual eBPF program in a python raw string.
# The defined C function prints a static string to the kernel trace pipe.
# For more information see:
# https://github.com/iovisor/bcc/blob/173282d39b98e3e7e6391d1159c5031bb4adb230/src/python/bcc/__init__.py#L1553
program = r"""
int hello(void *ctx) {
    bpf_trace_printk("Hello, World. I am an eBPF Program.");
    return 0;
}
"""

# Create an instance of the BPF class using the eBPF Program defined above.
b = BPF(text=program)

# Get the kernel function name of this syscall.
syscall = b.get_syscall_fnname("execve")
print("Function name of %s in kernel is %s" % ("execve", syscall))

# Instrument the kernel "execve" function to run our BPF defined hello() function each time it is called.
b.attach_kprobe(event=syscall, fn_name="hello")

# Print the contents of the kernel trace pipe.
b.trace_print()