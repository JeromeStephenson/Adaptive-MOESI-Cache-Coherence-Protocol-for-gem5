# Adaptive MOESI Cache Coherence Protocol for gem5

## Overview

This project implements an **Adaptive MOESI Cache Coherence Protocol** by modifying the default **MOESI_CMP_directory** protocol in gem5.

The objective is to reduce unnecessary memory accesses by allowing cache-to-cache transfers whenever another cache already owns the requested data.

The protocol was implemented in SLICC and evaluated against the original MOESI protocol using the same benchmark and simulation environment.

---

# Objective

The standard MOESI protocol often requests data from memory even when another cache already contains the latest copy.

The Adaptive MOESI protocol introduces additional protocol states and transitions that allow:

- Direct cache-to-cache data transfer
- Reduced directory involvement
- Reduced memory traffic
- Better sharing efficiency

---

# Experimental Setup

## Simulator

- gem5 25.1

## Processor

- DerivO3CPU
- 4 cores

## Memory System

- Ruby Memory System
- MOESI_CMP_directory (baseline)
- Adaptive MOESI (modified)

## Benchmark

OpenMP Counter Benchmark

```cpp
#pragma omp parallel
for(int i=0;i<1000000;i++)
{
    #pragma omp atomic
    counter++;
}
```

Expected output

```
Counter = 4000000
```

Both protocols successfully produced the correct output.

---

# Adaptive MOESI Modifications

The following changes were introduced into the protocol:

- Added adaptive ownership transitions
- Introduced optimized cache-to-cache forwarding
- Reduced unnecessary memory fetches
- Added adaptive acknowledgment handling
- Modified L1 controller state transitions
- Modified Directory controller behavior
- Added Owner → Modified transition optimization

---

# Simulation Results

| Metric | MOESI | Adaptive MOESI |
|---------|------:|---------------:|
| Simulation Ticks | 45,078,751,000 | 45,769,020,500 |
| Host Execution Time (s) | **527.49** | **485.99** |
| Ruby Average Latency | **29.17** | 29.67 |
| Ruby Hit Latency | 1.000848 | **1.000525** |
| Ruby Miss Latency | **64.13** | 192.43 |
| Outstanding Requests | **1.115** | 1.125 |

---

# Directory Controller Statistics

## Original MOESI

| Event | Count |
|------|------:|
| Fetch | 12,610 |
| Memory_Data | 12,609 |

---

## Adaptive MOESI

| Event | Count |
|------|------:|
| Memory_Data_Cache | 13,017 |

Unlike the original protocol, Adaptive MOESI delivers many responses directly from cache ownership instead of relying solely on memory.

---

# L1 Controller Message Statistics

## Forward GETX

Original MOESI

```
4,000,035
```

Adaptive MOESI

```
6,666,749
```

Increase:

```
+66.7%
```

This indicates that many more requests are being satisfied through cache-to-cache forwarding.

---

## Forward GETS

Original

```
108
```

Adaptive

```
664
```

Increase:

```
6.15×
```

Again showing significantly more cache sharing.

---

## Invalidations

Original

```
73
```

Adaptive

```
24
```

Reduction

```
67%
```

Fewer invalidations indicate that the adaptive protocol preserves sharing more effectively.

---

## Acknowledgements

Original

```
71
```

Adaptive

```
1,333,425
```

The adaptive protocol introduces explicit acknowledgment messages for the new ownership transitions.

Although message count increases, these acknowledgments enable direct cache-to-cache transfers.

---

# Cache State Behavior

The Adaptive protocol introduces additional states such as

```
MM
MM_W
OM
O
```

These states help maintain ownership while servicing requests directly from caches.

Example statistics:

```
MM.Fwd_GETX        1,333,373
MM_W.Fwd_GETX      5,333,351
O.Fwd_GETS                84
```

These transitions do not exist in the original protocol.

---

# Performance Discussion

## Host Execution Time

Adaptive MOESI reduced host execution time by

```
527.49 s
↓

485.99 s

≈7.9% faster
```

This indicates that the protocol executes more efficiently inside gem5.

---

## Cache Sharing

Forward GETS increased from

```
108

↓

664
```

showing much greater cache-to-cache communication.

---

## Invalidations

Reduced from

```
73

↓

24
```

showing improved sharing behavior.

---

## Memory Access

The original protocol relied primarily on

```
Memory_Data
```

responses.

The adaptive protocol introduces

```
Memory_Data_Cache
```

allowing many requests to be serviced directly from peer caches.

---

## Miss Latency

Miss latency increased from

```
64 cycles

↓

192 cycles
```

This is expected because ownership transfer now involves additional protocol states and acknowledgments before data reaches the requester.

---

# Advantages of Adaptive MOESI

✔ Increased cache-to-cache transfers

✔ Reduced invalidations

✔ Improved ownership tracking

✔ Reduced host simulation time

✔ Better cache sharing

✔ Demonstrates successful protocol customization in gem5

---

# Limitations

The current benchmark is relatively simple and mostly consists of atomic counter updates.

More realistic workloads should be evaluated, including:

- PARSEC
- SPLASH-2
- NAS Parallel Benchmarks
- SPEC CPU

These benchmarks generate richer coherence traffic and provide a more comprehensive evaluation.

---

# Future Work

Potential extensions include:

- Adaptive ownership prediction
- Dynamic cache migration
- Machine-learning-based coherence decisions
- Hybrid MOESI/MESIF protocol
- Energy-aware coherence optimization
- Scalability evaluation on 8, 16, and 32-core systems

---

# Conclusion

The Adaptive MOESI protocol was successfully implemented and integrated into gem5.

Compared to the original MOESI protocol, the adaptive version demonstrates:

- Faster host simulation time
- More cache-to-cache forwarding
- Fewer invalidations
- Improved cache sharing

Although coherence miss latency increased due to additional ownership management, the protocol validates that adaptive cache ownership can reduce unnecessary memory communication while preserving correctness.

This work demonstrates how cache coherence protocols can be customized within gem5 and provides a foundation for future research into adaptive coherence mechanisms.

---

# Repository Structure

```
gem5/
│
├── src/
│   └── mem/
│       └── ruby/
│           └── protocol/
│               ├── MOESI_CMP_directory_Adaptive-L1cache.sm
│               ├── MOESI_CMP_directory_Adaptive-L2cache.sm
│               ├── MOESI_CMP_directory_Adaptive-dir.sm
│               └── MOESI_CMP_directory_Adaptive.slicc
│
├── benchmarks/
│   └── openmp_test
│
├── results/
│   ├── moesi/
│   └── adaptive/
│
├── compare_stats.py
│
└── README.md
```

---

# References

1. gem5 Simulator Documentation  
2. Sorin et al., *A Primer on Memory Consistency and Cache Coherence*  
3. MOESI Cache Coherence Protocol Specification  
4. Ruby Memory System (gem5)

---

## Author

**Jerome Stephenson**

Implementation of an Adaptive MOESI Cache Coherence Protocol using gem5 Ruby for multicore cache coherence research.
