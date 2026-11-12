---
tag: CVZ3Q6
kind: technique
slug: read-barrier
name: Read barrier
aliases:
- load barrier
- GC read barrier
area: systems/garbage-collection
level: advanced
summary: "Code added to each pointer load, so that a mutator that runs during a moving collection only uses the current copy of each object."
prereqs: [mutator-and-collector, copying-collection]
see_also: [write-barrier, baker-real-time-collector, c4-collector, shenandoah-collector, z-garbage-collector, concurrent-garbage-collection, tagged-pointers, page-fault]
sources:
  - paper: doi:10.1145/359460.359470
    title: Henry G. Baker, List processing in real time on a serial computer, Communications of the ACM 21(4), 280-294, 1978
    locator: the incremental copying collector in which a fetch of a pointer into from-space first copies the object, so that the mutator sees only to-space
  - paper: doi:10.1145/800055.802042
    title: Rodney A. Brooks, Trading data space for reduced time and code space in real-time garbage collection on stock hardware, LISP and Functional Programming 1984, 256-262
    locator: the indirection word in each object, through which every access goes, so that the barrier has no test
  - paper: doi:10.1145/53990.53992
    title: Andrew W. Appel, John R. Ellis and Kai Li, Real-time concurrent collection on stock multiprocessors, PLDI 1988, 11-20
    locator: the use of page protection on unscanned to-space pages as a read barrier, with the trap handler that scans the page
  - paper: doi:10.1145/1064979.1064988
    title: Cliff Click, Gil Tene and Michael Wolf, The pauseless GC algorithm, VEE 2005, 46-56
    locator: the read barrier on every pointer load that checks a mark bit in the pointer and whether the target page is being relocated, and fixes the loaded slot
  - paper: doi:10.1145/1029873.1029891
    title: Stephen M. Blackburn and Antony L. Hosking, Barriers, friend or foe?, ISMM 2004, 143-151
    locator: the measured cost of conditional and unconditional read barriers, compared with write barriers
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Section 11.8 (Read and write barriers) and Chapter 17 (Concurrent copying and compaction)
---

A read barrier is a small piece of code that runs with every load of a pointer from the heap. It is the price of moving objects while the mutator runs. When a collector copies objects in steps, or at the same time as the mutator, an object can exist in two places for a while. The barrier makes sure that the mutator uses the right one. [Baker's](/baker-real-time-collector/) barrier copies the target of a from-space pointer when the mutator loads it, so that the mutator only holds to-space pointers. Brooks's barrier reads through an indirection word that each object carries, so that every access reaches the current copy. Newer collectors test bits in the pointer and fix the loaded slot in place. Loads are far more frequent than stores, so a read barrier costs more than a [write barrier](/write-barrier/), and much work goes into making its fast path short.

## In plain words

A moving collector copies objects to new places, to pack them together. If the program runs while this happens, it can hold the old address of an object that has already moved. It could then read old data, or write data that gets lost.

So each time the program reads a pointer from memory, it runs a few extra steps. The steps check whether the pointer is out of date. If it is, they find the new place, or move the object now, and give the program the new address. Some designs also fix the pointer in memory, so that the next read of it is fast.

## When it applies

- **The collector moves objects while the mutator runs.** Incremental copying, concurrent copying and concurrent compaction all need it, in some form. A stop-the-world copying collector does not, because the mutator never sees a half-moved heap.
- **Short pauses matter more than throughput.** The barrier slows down every pointer load, but it lets the pauses shrink to the time to scan the roots, or less.
- **The runtime controls every load.** The compiler must insert the barrier at each load of a reference from the heap, including in the runtime and in intrinsics.
- **An alternative is the operating system.** With page protection, unscanned pages trap on the first access and the trap handler scans the page. There is no code at each load, but each trap is expensive and the grain is a page.

## The template

Two classic barriers. The first keeps the *to-space invariant*: the mutator holds only to-space pointers. The second keeps every object reachable through its *forwarding word*, which points to the object itself or to its copy.

```pseudo id=main
READ-BAKER(o, i)                     ▷ the to-space invariant
L1  v ← o.f[i]
L2  if collecting and v is in from-space then
L3      v ← EVACUATE(v)              ▷ copy v, or follow its forwarding address
L4      o.f[i] ← v                   ▷ heal the slot
L5  return v

READ-BROOKS(o, i)                    ▷ an unconditional indirection
L6  return o.fwd.f[i]
WRITE-BROOKS(o, i, v)
L7  o.fwd.f[i] ← v

COPY-BROOKS(o)                       ▷ the collector moves o
L8  c ← a copy of o.fwd; c.fwd ← c; o.fwd ← c
```

**Walk-through.** In Baker's scheme, the collection starts with a flip that copies the root targets. The mutator then loads pointers only through lines L1 to L5: a from-space pointer is replaced by the address of the copy, and the copy is made at once if it does not exist yet. Line L4 heals the slot, so that the next load of it takes the fast path. In Brooks's scheme, each object has an extra word $fwd$. Every load and every store goes through it (lines L6 and L7), with no test. To move an object, the collector copies it and redirects the forwarding word of the old copy (line L8). Old pointers stay valid until a later phase rewrites them to the new copies.

### Example

Object $a$ is a root and $a.f_0$ points to $b$; $b$ is not a root. A Baker collection flips: $a$ is copied to $a'$ in to-space, and $a'.f_0$ still holds the from-space address of $b$, because $a'$ has not been scanned. The mutator now loads $a'.f_0$. Line L2 sees a from-space pointer, line L3 copies $b$ to $b'$, line L4 stores $b'$ into $a'.f_0$, and the mutator gets $b'$. When the scanner later reaches $a'$, the slot already holds a to-space pointer.

In a Brooks heap, suppose the collector copies $a$ to $a'$ and sets $a.fwd \gets a'$, while the mutator still holds $a$. The mutator stores $a.f_0 \gets b$. Line L7 writes into $a'$, the copy that survives. A store that skips the indirection would write into $a$, which the collector frees at the end, and the store would be lost. The tests run this scenario both ways, and random interleavings of mutator steps and collector steps for both barriers, against a heap with no collector.

### Correctness

**Baker.** Invariant: during a collection, every root holds nil or a to-space pointer. The flip establishes it. A load returns a to-space pointer by lines L2 to L5, and a store copies a value that the mutator holds, so it cannot bring a from-space pointer into a root. Objects allocated during the collection are in to-space. Each to-space copy is scanned once and its from-space fields are replaced by their copies. So at the end, when the scan queue is empty, no to-space object and no root points into from-space, and from-space can be freed.

**Brooks.** Invariant: for each object, $o.fwd$ is the only copy that holds current data. A store writes $o.fwd$ (line L7), a load reads it (line L6), and the copy at line L8 takes its contents from $o.fwd$ and becomes the new $o.fwd$ in one step. Pointer comparison must also compare $a.fwd$ with $b.fwd$, not $a$ with $b$.

### Cost

A read barrier adds $O(1)$ work to every pointer load. Brooks's barrier is one extra load on every access, and one extra word per object. Baker's barrier is a test and a rarely taken branch, but the slow path can copy an object, so the time of a single load is not bounded by a small constant unless objects are small or copied in parts. Blackburn and Hosking measured conditional read barriers to cost more than the common write barriers, and the cost differs much between processors. Self-healing makes the slow path run at most once per slot per collection.

## Classic examples

- **Baker (1978).** Incremental copying with a to-space invariant, for real-time Lisp: the [Baker real-time collector](/baker-real-time-collector/).
- **Brooks (1984).** An indirection word in each object, read on every access, so that the barrier has no branch.
- **Appel, Ellis and Li (1988).** The read barrier is page protection: to-space pages that are not yet scanned are protected, and the first access traps into a handler that scans the page.
- **Pauseless and C4.** Every pointer load checks a bit in the pointer and whether the target page is being moved, and fixes the loaded slot. The [C4 collector](/c4-collector/) calls this a loaded value barrier.
- **Shenandoah.** The [Shenandoah collector](/shenandoah-collector/) first used Brooks forwarding words, and later moved to a barrier on loaded references that copies the target if needed.
- **ZGC.** The [Z garbage collector](/z-garbage-collector/) keeps metadata bits in each pointer (colored pointers), and its load barrier tests them and heals the slot when the color is out of date.

## Variations

- **Conditional or unconditional.** Brooks's indirection has no branch but always costs a load; a test of the pointer costs a compare and a branch, and is cheap when the branch is almost never taken.
- **To-space invariant or not.** Baker's barrier never lets the mutator see from-space. Replicating collectors do the opposite: the mutator works on from-space, and a write barrier logs the changes so that the replica can catch up.
- **Bits in the pointer.** Unused high bits of a [tagged pointer](/tagged-pointers/) can say whether a pointer is up to date for this phase, so that the barrier test needs no load from the object.
- **Self-healing.** Write the fixed pointer back to the slot it came from, so that the slow path runs at most once per slot.
- **Hardware support.** Lisp machines checked tags on loads in hardware. Virtual memory protection is a coarse form of the same idea.

## Pitfalls

- **Pointer comparison.** With an indirection or a heap where two copies exist, $a = b$ can be false for the same object. Compare after the barrier.
- **Loads that bypass the barrier.** Loads in the runtime, in native code, or from a register that held the old value before a flip, all see stale pointers.
- **Races on the copy.** With several threads, two threads can try to copy the same object at the same time, and a thread can write to the old copy while the collector copies it. A [compare-and-swap](/compare-and-swap/) on the forwarding word decides the winner.
- **Unbounded slow paths.** A barrier that copies a large array on a load makes that load slow. Real-time collectors copy large objects lazily, or in parts.
- **Assuming the cost is small.** Loads are frequent. Measure the barrier on the target processor before choosing a design.

## Exercises

1. In Baker's scheme, show that a store $o.f_i \gets v$ needs no barrier, given the to-space invariant.
2. Explain why Brooks's scheme needs a final phase that rewrites the pointers to the old copies before their memory is freed, and what goes wrong if it is skipped.
3. A colored-pointer barrier has a fast path of a load, a test of the pointer bits and a branch. Estimate its cost per million loads if the slow path takes 50 times as long and runs on 0.1% of loads.

## References
