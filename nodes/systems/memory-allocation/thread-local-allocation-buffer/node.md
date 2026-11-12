---
tag: K3R0NV
kind: concept
slug: thread-local-allocation-buffer
name: Thread-local allocation buffer
aliases:
- TLAB
area: systems/memory-allocation
level: advanced
summary: "A chunk of the shared young space that one thread owns, so that it can allocate objects by bumping a private pointer with no atomic instruction. HotSpot sizes and refills them adaptively."
prereqs: [bump-pointer-allocation, generational-garbage-collection]
see_also: [copying-collection, mutator-and-collector, arena-allocation, tcmalloc, mimalloc, compare-and-swap, internal-fragmentation, immix-collector]
sources:
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, CRC Press, 2011
    locator: Chapter 7, Allocation (sequential allocation, and the section on allocation in concurrent systems with local allocation buffers)
  - url: https://github.com/openjdk/jdk/blob/master/src/hotspot/share/gc/shared/threadLocalAllocBuffer.cpp
    title: "OpenJDK, HotSpot source file threadLocalAllocBuffer.cpp"
    locator: startup_initialization (the target number of refills), initial_desired_size, resize, initial_refill_waste_limit, retire and insert_filler
  - url: https://github.com/openjdk/jdk/blob/master/src/hotspot/share/gc/shared/tlab_globals.hpp
    title: "OpenJDK, HotSpot source file tlab_globals.hpp"
    locator: the flags UseTLAB, ResizeTLAB, MinTLABSize, TLABSize, TLABAllocationWeight, TLABWasteTargetPercent (1), TLABRefillWasteFraction (64) and TLABWasteIncrement (4)
---

A thread-local allocation buffer (TLAB) is a block of the shared allocation space of a garbage-collected heap that is handed to one thread for its private use. The thread allocates small objects inside its TLAB with [bump-pointer allocation](/bump-pointer-allocation/): compare, add, store, and no atomic instruction, because no other thread allocates there. Only when the buffer runs out does the thread take the slow path and get a new TLAB from the shared space with an atomic operation. The HotSpot Java virtual machine carves its TLABs from eden, the young space of its [generational collectors](/generational-garbage-collection/), and adapts the size of each thread's TLAB to how fast the thread allocates.

## In plain words

Many cooks share one big pantry. If every cook walked to the pantry and signed a book for each egg, they would wait in line all day. So each cook takes a full tray of supplies to their own station and works from it alone. Only when the tray is empty does the cook go back to the pantry, sign once, and take a new tray.

The tray must have the right size. A tray that is too small means many trips. A tray that is too big means much food sits unused at the stations when the kitchen is cleaned. The kitchen watches how fast each cook works and sizes the next tray to match.

## The idea

**Fast path.** A TLAB is a range $[\mathit{start}, \mathit{end})$ with a private pointer $\mathit{top}$. To allocate $s$ words:

1. if $\mathit{top} + s \le \mathit{end}$, return $\mathit{top}$ and set $\mathit{top} \leftarrow \mathit{top} + s$;
2. otherwise take the slow path.

No other thread reads or writes $\mathit{top}$, so step 1 needs no [compare-and-swap](/compare-and-swap/) and no lock. The shared eden has its own top pointer, and only the slow path moves it, with an atomic operation, by a whole TLAB at a time.

**Slow path and the refill waste limit.** When an object does not fit, the thread must choose. It can throw away the rest of its TLAB and get a new one, or it can keep the TLAB and put this one object directly in the shared eden. HotSpot decides with a per-thread refill waste limit $w$:

- If the free space left in the TLAB, $\mathit{end} - \mathit{top}$, is larger than $w$, the TLAB still has too much room to waste. The object goes directly into shared eden with an atomic bump, and $w$ grows by TLABWasteIncrement (default 4 words), so that a run of large objects does not keep the TLAB alive forever.
- Otherwise the TLAB is retired: its unused tail is filled with a dummy filler object, so that the heap stays parsable as a sequence of objects, and the thread gets a new TLAB. The limit $w$ is reset to its initial value.

The initial value of $w$ is the desired TLAB size divided by TLABRefillWasteFraction, whose default is 64. So a retired TLAB wastes at most about 1/64 of its size.

**Adaptive size.** At startup HotSpot sets the target number of refills per eden cycle to
$$R = \frac{100}{2 \cdot \mathrm{TLABWasteTargetPercent}},$$
which is 50 with the default TLABWasteTargetPercent of 1. The reasoning: when a collection happens, each thread's current TLAB is on average half used, so its expected waste is half a TLAB. If a thread fills $R$ TLABs per cycle, that half TLAB is $1/(2R)$ of what it allocated, which is the target percentage. At each collection, HotSpot updates for each thread an average of the fraction $f$ of eden that the thread allocated (weighted by TLABAllocationWeight, default 35), and sets the next desired size to
$$\text{desired size} = \frac{f \cdot \text{eden capacity}}{R},$$
clamped between a minimum (MinTLABSize, 2 KB by default) and a maximum.

**Cost of the scheme.** TLABs move the allocation cost from a shared atomic per object to a shared atomic per TLAB. The price is [internal fragmentation](/internal-fragmentation/) of eden: the filler at the end of each retired TLAB, and the unused part of each thread's current TLAB when a collection starts. Both are bounded by the two waste fractions above.

## Examples

**The refill decision.** Take a desired TLAB size of 8192 words (64 KB with 8-byte words). The initial limit is $8192 / 64 = 128$ words.

| Event | Free in TLAB | Request | Limit before | Decision | Limit after |
|---|---|---|---|---|---|
| 1 | 300 | 400 | 128 | 300 > 128: put the object in shared eden | 132 |
| 2 | 300 | 350 | 132 | 300 > 132: put the object in shared eden | 136 |
| 3 | 300 | 40 | 136 | fits: bump to 260 free | 136 |
| 4 | 100 | 200 | 136 | 100 ≤ 136: fill 100 words, get a new TLAB | 128 |

After event 4, the new TLAB has 8192 free words, and the request of 200 words is served from it.

**The adaptive size.** Eden has 8,388,608 words (64 MB). A thread did a quarter of all allocation in the last cycles, so $f = 0.25$. With $R = 50$, the desired size is $0.25 \times 8{,}388{,}608 / 50 \approx 41{,}943$ words, about 328 KB. A thread that allocates rarely gets a much smaller TLAB, so it does not hold a large part of eden unused.

**Without TLABs.** Every allocation by every thread would do a compare-and-swap on the shared eden top. On many cores this one cache line moves between processors on each allocation, and allocation stops scaling.

## Where it is used

- **HotSpot.** All of its collectors that allocate in a contiguous young space use TLABs, from the serial and parallel collectors to the [Garbage-First](/garbage-first-collector/) collector. The [Z](/z-garbage-collector/) and [Shenandoah](/shenandoah-collector/) collectors also give threads local buffers in their regions.
- **Other managed runtimes.** Thread-local buffers are the standard way for a runtime with a [copying collector](/copying-collection/) to allocate in parallel; the GC Handbook, Chapter 7, describes them as local allocation buffers. [Immix](/immix-collector/) gives each thread its own block to fill.
- **Collectors themselves.** Parallel collectors copy survivors into per-thread promotion buffers, the same idea applied to the collector instead of the [mutator](/mutator-and-collector/).
- **Allocators for C and C++.** [tcmalloc](/tcmalloc/) and [mimalloc](/mimalloc/) also give each thread or CPU a private cache, but they hand out blocks from free lists by size class, not by bumping a pointer through a contiguous region, because a C heap cannot rely on a collector to clean up behind it. A TLAB is closer to an [arena](/arena-allocation/) that a garbage collector empties.

## References
