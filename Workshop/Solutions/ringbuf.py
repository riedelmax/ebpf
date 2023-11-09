#!/usr/bin/python3

import sys
import time

from bcc import BPF

src = r"""
BPF_RINGBUF_OUTPUT(buffer, 16);

struct event {
    char filename[64];
};

TRACEPOINT_PROBE(syscalls, sys_enter_openat) {
    struct event *event = buffer.ringbuf_reserve(sizeof(struct event));
    if (!event) {
        return 1;
    }
    bpf_probe_read_user_str(event->filename, sizeof(event->filename), args->filename);
    buffer.ringbuf_submit(event, 0);
    return 0;
}
"""

b = BPF(text=src)

def callback(ctx, data, size):
    print(b['buffer'].event(data).filename.decode('utf-8'))

b['buffer'].open_ring_buffer(callback)

print("Printing openat() calls, ctrl-c to exit.")
print("FILENAME")

try:
    while 1:
        b.ring_buffer_consume()
        time.sleep(0.5)
except KeyboardInterrupt:
    sys.exit()