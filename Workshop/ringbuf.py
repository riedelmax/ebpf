'''
CAUTION! An evil kernel critter has eaten almost 
all the skeleton code that was supposed to be in this file.
Instead, he left a bunch of links to the official bcc docs.

This task does provides very little skeleton code.
Your job:
  - print all files that get opened in the kernel
  - use a ring buffer, DO NOT use bpf_trace_printk

Useful docs:
  - open a file relative to a directory file descriptor: https://linux.die.net/man/2/openat
  - open ring buffer: https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#12-open_ring_buffer
  - instrument tracepoint: https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#3-tracepoints
  - read string from user space and make it available in eBPF program: https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#11-bpf_probe_read_user_str

'''

#!/usr/bin/python3

import sys
import time

from bcc import BPF

src = r"""

"""

b = BPF(text=src)

# TODO: Put something here

try:
    while 1:
        b.ring_buffer_consume()
        time.sleep(0.5)
except KeyboardInterrupt:
    sys.exit()