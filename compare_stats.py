import re

stats = [
    "simTicks",
    "simInsts",
    "simOps",
    "hostSeconds",
    "hostInstRate",
    "system.cpu.ipc",

    "system.ruby.network.packets_injected",
    "system.ruby.network.packets_received",

    "system.ruby.network.flits_injected",
    "system.ruby.network.flits_received",

    "system.ruby.network.average_packet_latency",
    "system.ruby.network.average_hops",

    "system.ruby.l1_cntrl0.L1Dcache.demandHits",
    "system.ruby.l1_cntrl0.L1Dcache.demandMisses",

    "system.ruby.l2_cntrl0.L2cache.demandHits",
    "system.ruby.l2_cntrl0.L2cache.demandMisses",
]

def extract(filename):
    data = {}

    with open(filename) as f:
        for line in f:
            if line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            key = parts[0]

            if key in stats:
                data[key] = parts[1]

    return data

moesi = extract("results/moesi/stats.txt")
adaptive = extract("results/adaptive/stats.txt")

print("="*90)
print("{:<55} {:>15} {:>15}".format("Statistic","MOESI","Adaptive"))
print("="*90)

for s in stats:
    print("{:<55} {:>15} {:>15}".format(
        s,
        moesi.get(s,"-"),
        adaptive.get(s,"-")
    ))
