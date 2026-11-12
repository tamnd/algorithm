---
tag: TPVW7Y
kind: algorithm
slug: z-garbage-collector
name: Z garbage collector
aliases:
- ZGC
area: systems/garbage-collection
level: research
summary: "A concurrent compacting collector of the HotSpot JVM. Color bits in each pointer and a self-healing load barrier let it mark and move objects while the program runs."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {n: the live objects, p: the pointer fields per object, r: the roots, P: the pages of the heap}
  time: {worst: O(n p + r + P), best: Θ(r + P)}
  space: {extra: O(n + P)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2018
  people: [Per Lidén, Stefan Karlsson]
  note: ZGC came into OpenJDK 11 as an experimental collector through JEP 333. It marks and compacts while the program runs, with a load barrier on pointers that carry color bits, and keeps its pauses short and nearly independent of the heap size.
prereqs: [concurrent-garbage-collection, read-barrier, copying-collection, tricolor-marking]
see_also: [c4-collector, shenandoah-collector, garbage-first-collector, baker-real-time-collector, tagged-pointers, compare-and-swap, heap-compaction, generational-garbage-collection]
sources:
  - url: https://openjdk.org/jeps/333
    title: "JEP 333: ZGC: A Scalable Low-Latency Garbage Collector (Experimental)"
    locator: The goals, colored pointers, load barriers and the first platform (Linux on x64), for JDK 11
  - url: https://openjdk.org/jeps/377
    title: "JEP 377: ZGC: A Scalable Low-Latency Garbage Collector (Production)"
    locator: ZGC becomes a product feature in JDK 15
  - url: https://openjdk.org/jeps/439
    title: "JEP 439: Generational ZGC"
    locator: The young and old generations, store barriers, and the new pointer layout, for JDK 21
  - paper: doi:10.1145/3538532
    title: "Albert Mingkun Yang and Tobias Wrigstad, Deep Dive into ZGC: A Modern Garbage Collector in OpenJDK, ACM Transactions on Programming Languages and Systems 44(4), 2022, 1-34"
---

The Z garbage collector, or ZGC, is a collector of the HotSpot JVM by Per Lidén and Stefan Karlsson. It came into JDK 11 in 2018 as an experimental feature (JEP 333). It marks the live objects and moves them while the program runs, so its pauses do only small, fixed work. Each pointer carries a few *color* bits beside the address. Every time the program loads a pointer from the heap, a [read barrier](/read-barrier/) tests the color. A pointer with a *bad* color goes to a slow path: the barrier marks the object, or finds or makes its new copy, and writes the good pointer back to the field it came from. This *self-healing* means each stale field takes the slow path at most once per cycle. ZGC is close to the [C4](/c4-collector/) collector of Azul, which also uses a self-healing load barrier. **This page gives a small model of the mechanism, not the real collector.**

## In plain words

Each pointer has a small colored tag. The collector says which color is good at each time. When the program reads a pointer out of an object, it first looks at the tag. If the tag is good, it goes on at once.

If the tag is bad, the program does a little of the collector's work. It marks the object as in use, or, if the object is about to move, it finds the new copy, or makes one itself. Then it puts the fixed pointer back where it found it, so the next read is fast.

Meanwhile, the collector finds the objects in use, picks pages with little live data, and copies their objects out. It frees a page as soon as it is empty. It keeps a small table of the old and new places until the next round has fixed every old pointer.

## The problem

**Heap model.** The heap is a row of pages of $S$ slots. A pointer is an integer: an address in the low bits and one color bit above it, Marked0, Marked1 or Remapped. Every color of an address names the same memory. In the real system this is *multi-mapping*: the heap is mapped at three virtual addresses, one for each color. An object has a few pointer fields. Each mutator thread has a few registers and does atomic steps: allocate, load a field, store a register into a field, copy or clear a register. The collector is one more thread. A pause is a step taken when every mutator is between operations.

**Goal.** Reclaim the unreachable objects and compact the heap, while the mutators run. Keep the *to-space invariant*: a mutator register never holds a pointer with a bad color, or a pointer into a page that is being moved or has been released. Each pause does an amount of work that does not grow with the heap.

## The algorithm

The good color is Marked0 or Marked1 during marking, in turn from cycle to cycle, and Remapped during relocation and until the next marking. The other colors are *bad*. Every page that is moved has a *forwarding table* from old addresses to new ones.

```pseudo id=main
LOAD(x, f)                                     ▷ a mutator loads x.f; x is a good pointer
L1  v ← x.f
L2  if v ≠ nil and the color of v is bad then v ← SLOW-PATH(x, f, v)
L3  return v

SLOW-PATH(x, f, v)
L4  a ← the address of v; if a has a forwarding entry then a ← the entry
L5  if marking then mark a and push it on the mark stack
L6  else if a is on a page of the relocation set and has no forwarding entry then
L7      b ← a copy of a on a page of this thread
L8      CAS the entry of a from empty to b; a ← the entry of a       ▷ the winner's copy
L9  CAS x.f from v to a with the good color; return a with the good color   ▷ self-healing

CYCLE()                                        ▷ the collector thread
L10 pause: good ← the marked color not used in the last cycle; remap, mark and recolor the roots
L11 while the mark stack is not empty do pop an object o                     ▷ concurrent
L12     for each field of o with a bad color: remap it, mark its target, write it back with the good color
L13 pause, then: free the pages released in the last cycle and drop their forwarding tables
L14 relocation set ← the used pages with few live objects; free the used pages with none
L15 pause: good ← Remapped; relocate the objects that the roots point to, and recolor the roots
L16 for each page of the relocation set do                                  ▷ concurrent
L17     for each live object a on it with no entry: b ← a copy of a; CAS the entry of a from empty to b
L18     release the memory of the page; keep its forwarding table
```

**Marking and remapping in one pass.** The marking of line L12 sees every live field. A field that still points to an object moved in the last cycle has a bad color (Remapped is bad during marking), so line L12 or line L4 also replaces it by the new address. When marking ends, no live field holds an old address, and line L13 can drop the old forwarding tables. This is why ZGC needs two marked colors: in a marking, a pointer with the color of the last marking is not yet marked in this one.

**Who moves an object.** Both the collector (line L17) and a mutator (line L7) may copy the same object. The compare-and-swap on the forwarding entry picks one copy; the loser drops its copy and uses the winner's. So all threads agree on the one new address of each object.

**Quick release.** A page is released as soon as its live objects have copies (line L18). Only the forwarding table stays, and it is small. So the memory of the relocation set can be used again during the same cycle. ZGC keeps its forwarding tables outside the heap.

**What the model leaves out.** In the real system, the roots of thread stacks are processed concurrently since JDK 16 (JEP 376), there are weak, soft and phantom references, there are small, medium and large pages, and many collector threads do the work. The model has one collector thread and one slot per field, and treats a pause as one step.

## Example

The page size is 6. Page 0 holds an object $A$ in register 0, with a field that points to $B$, and four dead objects. Marking finds $A$ and $B$: two live objects of six, so page 0 goes into the relocation set.

1. **Mark start.** The good color becomes Marked0. Register 0 becomes $0$ colored Marked0.
2. **Marking.** $A.f$ holds $1$ colored Remapped, a bad color now. Line L12 marks $B$ and writes back $1$ colored Marked0.
3. **Relocate start.** The good color becomes Remapped. The pause copies $A$, which the root points to, to address 6 on a new page, and register 0 becomes $6$ colored Remapped. The copy has the same field: $1$ colored Marked0.
4. **The mutator loads $A.f$.** Line L2 sees Marked0, a bad color. Line L6 finds that page 0 is in the relocation set and that $B$ has no entry. The mutator copies $B$ to address 12, installs the entry $1 \to 12$, and writes $12$ colored Remapped back into $A.f$.
5. **The next load of $A.f$** sees Remapped and takes the fast path.
6. **The collector** reaches $B$ at line L17, finds the entry, and does not copy it again. It releases page 0. The table $\{0 \to 6, 1 \to 12\}$ stays until the next marking ends.

The tests run this schedule, and also the two races: the collector copies first and the mutator's CAS fails, or the other way round. A third test lets a mutator copy $B$ and then stop until the collector has ended the whole relocation; its late CAS finds the entry and it uses the collector's copy.

## Correctness

The proof in the proofs section shows the following, and the tests check it after every step of random programs on three mutator threads.

1. **To-space invariant.** A register gets a value only from a pause, which gives it the good color and a new address, from line L3, which returns a good value (lines L2 and L9), or from another register. During relocation, a good pointer never points into the relocation set: lines L7 and L17 copy only to pages outside it, and line L15 recolors only after moving the root's object.
2. **One copy wins.** The forwarding entry of an object is written once, by a compare-and-swap. Every thread that moves the object then uses the entry, so all pointers to it end at the same copy.
3. **Marking is complete.** Every pointer that a mutator holds or stores during marking has been marked: roots at line L10, loads at line L5. An object allocated in this cycle counts as live. So, as in [snapshot](/snapshot-at-the-beginning/) marking with an extra rule, an object that is reachable at mark end is marked, and line L14 frees no reachable object.
4. **No pointer to a released page is used.** A released page is read only through its forwarding table, and the table is dropped only after a full marking has fixed every live field.

Without the load barrier, a mutator loads a pointer with a bad color, or a pointer into a page that is about to move; the tests find a broken invariant in every one of 40 seeded runs.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above. The bounds are for one cycle.

- **Collector work.** Marking visits each live object and each of its fields: $O(n p)$. Relocation copies at most the live objects of the relocation set, $O(n)$. The pauses touch the $r$ roots, and lines L13 and L14 scan the $P$ pages. In total $O(n p + r + P)$, and $\Theta(r + P)$ when nothing is live.
- **Pauses.** Each pause is $O(r)$ in the model, and does not depend on the size of the heap. Since JDK 16, the real system scans thread stacks concurrently too, so its pauses are well under a millisecond in common cases.
- **Barrier.** The fast path is a test and a branch, $O(1)$, on each load of a pointer from the heap. A slow path costs $O(1)$, plus the size of the object if it copies it. Self-healing means each field takes the slow path at most once per phase.
- **Space.** Mark bits for $n$ objects, forwarding tables with one entry per moved object, and per-page data: $O(n + P)$.

## Properties

- **Concurrent and compacting.** Both marking and moving run beside the mutators. The heap never fragments, and there is no long compaction pause.
- **Pauses that do not grow with the heap.** The pauses do fixed work, so their length does not depend on the size of the heap or of the live data.
- **A cost on every load.** The price is a barrier on each pointer load from the heap, and a slow path the first time a stale field is read after a phase change. Throughput is often a little lower than that of a stop-the-world collector.
- **Not generational, in its first form.** Until JDK 21, ZGC marked the whole heap in each cycle. Programs that allocate fast need a large heap so that a cycle can finish before memory runs out.
- **Floating garbage.** Objects that die during a cycle stay until the next one.

## Variants and improvements

- **Generational ZGC (JDK 21, JEP 439).** It adds a young and an old generation, each collected by the same concurrent algorithm. It adds store barriers to keep track of pointers from old to young objects. As far as we know from JEP 439, it also drops multi-mapping: the color bits are checked and removed by the load barrier, with no extra virtual mappings. Later JDK releases made the generational mode the default and then removed the old mode; the exact releases are not checked here.
- **C4.** The [C4](/c4-collector/) collector of Azul, and its forerunner Pauseless, use a similar self-healing load barrier with one bit (not-marked-through) and page protection to trap pointers into pages that are being moved. C4 was generational before ZGC was.
- **Shenandoah.** [Shenandoah](/shenandoah-collector/) also moves objects concurrently, first with a forwarding word in each object and later with a load barrier that keeps a to-space invariant much like this one.
- **Colors without multi-mapping.** Since the address bits of a pointer are masked before use, the colors can be kept in bits that the hardware ignores, such as the top byte on some 64-bit processors. See [tagged pointers](/tagged-pointers/).

## When to use it

Use it for programs that need short pauses on large heaps: services with tight response-time goals, and heaps from a few gigabytes up to many terabytes. Prefer [G1](/garbage-first-collector/) when the best throughput for a pause target near tens of milliseconds is the aim, and a parallel stop-the-world collector for batch work. On small heaps, the cost of the barriers and the extra memory may not pay off.

## Pitfalls

- **Allocation stalls.** If the mutators allocate faster than a cycle can free memory, a thread must wait for the collector. This is not a pause of all threads, but it is a delay. Give the heap room to spare.
- **A copy that loses.** A thread that loses the compare-and-swap at line L8 must use the winner's copy, and its own copy is garbage. A model that installs its own copy anyway lets two threads see two objects.
- **Forwarding tables dropped too soon.** A table may be dropped only after a full marking has fixed every live field. If it is dropped at the end of relocation, a stale field points into memory that may be in use again.
- **The race at the end of relocation.** A mutator may copy an object, stop, and resume after the collector has finished the page. Its compare-and-swap must still see the entry. A version of line L8 that looks only in the table of the current relocation fails this case; the tests keep the schedule.
- **Virtual memory use.** Multi-mapping made the process seem to use three times the memory of the heap in some tools.
- **Raw pointers in native code.** Code outside the JVM must not keep a colored pointer or read a field without the barrier.

## Implementations

## History

Baker's [real-time copying collector](/baker-real-time-collector/) (1978) kept a to-space invariant with a read barrier, but on stock hardware such a barrier was thought too costly. Click, Tene and Wolf described the Pauseless collector of Azul in 2005, which used a self-healing read barrier with hardware support, and Tene, Iyengar and Wolf described its successor C4 in 2011. Per Lidén and Stefan Karlsson of Oracle brought ZGC to OpenJDK in JDK 11 (2018) as an experimental collector for Linux on x64 (JEP 333), using colored pointers and multi-mapping to make the barrier a single test. It became a product feature in JDK 15 (JEP 377). Concurrent thread-stack processing came in JDK 16 (JEP 376). Generational ZGC came in JDK 21 (JEP 439). Yang and Wrigstad gave a detailed account of its design in 2022.

## References
