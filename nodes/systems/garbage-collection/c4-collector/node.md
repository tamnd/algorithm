---
tag: G25N97
kind: algorithm
slug: c4-collector
name: C4 collector
aliases:
- Continuously Concurrent Compacting Collector
area: systems/garbage-collection
level: research
summary: "Azul's concurrent, generational, compacting collector. A self-healing loaded value barrier marks and relocates objects while the program runs, with no global pause."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {n: the live objects, p: the pointer fields per object, r: the roots, P: the pages of the heap}
  time: {worst: O(n p + r + P), best: Θ(r + P)}
  space: {extra: O(n + P)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2011
  people: [Gil Tene, Balaji Iyengar, Michael Wolf]
  note: Tene, Iyengar and Wolf described C4 at ISMM 2011 as the collector of Azul's JVM on x86. It extends the Pauseless collector of Click, Tene and Wolf (2005) to two generations, with a loaded value barrier that marks and relocates concurrently and heals each stale field.
prereqs: [concurrent-garbage-collection, read-barrier, copying-collection, tricolor-marking]
see_also: [z-garbage-collector, shenandoah-collector, baker-real-time-collector, garbage-first-collector, generational-garbage-collection, page-fault, compare-and-swap, heap-compaction]
sources:
  - paper: doi:10.1145/1993478.1993491
    title: "Gil Tene, Balaji Iyengar and Michael Wolf, C4: The Continuously Concurrent Compacting Collector, ISMM 2011, 79-88"
    locator: The loaded value barrier, the Mark, Relocate and Remap phases, quick release, the two generations, and the operating system support for fast changes to page mappings
  - paper: doi:10.1145/1064979.1064988
    title: "Cliff Click, Gil Tene and Michael Wolf, The Pauseless GC Algorithm, VEE 2005, 46-56"
    locator: The read barrier with self-healing, the NMT bit, page protection for relocation, and the phases on Azul's own hardware
---

C4, the Continuously Concurrent Compacting Collector, is the collector of the Azul JVM, described by Gil Tene, Balaji Iyengar and Michael Wolf in 2011. It marks, moves and fixes objects while the program runs, and it does so in both a young and an old generation. Its key part is the *loaded value barrier* (LVB), a [read barrier](/read-barrier/) on every pointer that the program loads from the heap. The barrier checks two things: whether the pointer was *marked through* in this cycle, and whether it points into a page that is being moved. If either check fails, the barrier traps, does the work (marks the object, or finds or makes its new copy), and writes the fixed pointer back into the field it came from. This *self-healing* means each stale field traps at most once. C4 grew out of the Pauseless collector (Click, Tene and Wolf, 2005), which ran on Azul's own processors. **This page gives a small model of the mechanism, not the real collector.**

## In plain words

Each pointer carries one extra bit that says "checked in this round". At the start of each round, the collector flips the meaning of the bit, so every old pointer is unchecked again.

When the program reads a pointer out of an object, it looks at that bit, and at whether the pointer leads into an area that is being cleared out. If all is well, it goes on at once. If not, the program stops for a moment and fixes the pointer: it marks the object as in use, or it finds the object's new place, or moves the object itself. Then it puts the fixed pointer back, so the next read is fast.

The collector frees the memory of a cleared area as soon as it is empty, but it keeps the area locked until every old pointer into it has been fixed.

## The problem

**Heap model.** The heap is a row of pages of $S$ slots. A pointer is an integer: an address in the low bits and one *NMT* (not marked through) bit above it. An object has a few pointer fields. Each mutator thread has a few registers and does atomic steps: allocate, load a field, store a register into a field, copy or clear a register. A page can be *protected*: the mutators may not use a pointer into it. The collector is one more thread. A *checkpoint* is a point that every mutator must pass before the collector goes on.

**Goal.** Reclaim the unreachable objects and compact the heap, with no step at which all threads stop together. Keep the invariant that a mutator register holds only pointers that are marked through in this cycle and that point into unprotected pages.

## The algorithm

Let $e$ be the *expected* NMT value of the cycle. A pointer $v$ is *good* if $\textit{nmt}(v) = e$ and the page of $v$ is not protected. The forwarding data of moved objects are kept off the pages, so they outlive the memory of the page.

```pseudo id=main
LOAD(x, f)                                     ▷ a mutator loads x.f; x is a good pointer
L1  v ← x.f
L2  if v ≠ nil and v is not good then v ← TRAP(x, f, v)
L3  return v

TRAP(x, f, v)                                  ▷ the loaded value barrier's slow path
L4  a ← the address of v
L5  if the page of a is protected then
L6      if a has no forwarding entry then b ← a copy of a on a page of this thread; CAS the entry of a from empty to b
L7      a ← the entry of a                                        ▷ the winner's copy
L8  if nmt(v) ≠ e and marking then mark a and push it
L9  CAS x.f from v to a with NMT bit e; return a with NMT bit e   ▷ self-healing

CYCLE()                                        ▷ the collector thread
L10 checkpoint: e ← 1 − e; marking ← true; remap, mark and fix the roots of each thread
L11 while the mark stack is not empty do pop an object o
L12     for each field of o that is not good: remap it, mark its target, write it back with NMT bit e
L13 checkpoint, then: marking ← false; unprotect and free the pages released in the last cycle; drop their forwarding data
L14 relocation set ← the used pages with few live objects; free the used pages with none
L15 protect the pages of the relocation set; checkpoint: relocate the objects that the roots point to, fix the roots
L16 for each page of the relocation set, for each live object a on it with no entry: b ← a copy of a; CAS the entry of a from empty to b
L17     release the memory of the page at once (quick release); keep it protected and keep its forwarding data
```

**Mark.** The flip at line L10 makes every pointer in the heap fail the NMT test. The collector traces the live objects (lines L11 and L12) and fixes the NMT bit of each field it passes. A mutator that loads a pointer that the collector has not reached yet traps on the NMT test and marks the object at line L8. So every pointer that a mutator holds is marked, and the mutators never hide an object from the collector.

**Relocate.** Line L15 protects the chosen pages, and from then on any load of a pointer into them traps at line L5. The collector copies the live objects page by page (line L16). A mutator that traps first copies the object itself (line L6). A compare-and-swap on the forwarding entry picks one copy, and the loser uses the winner's.

**Quick release.** As soon as the live objects of a page have their copies, line L17 gives the memory of the page back. Only the forwarding data stay. So the memory freed by one page can hold the copies from the next page, and a compaction needs little spare memory. The paper calls this *hand-over-hand* compaction.

**Remap.** Pointers to the old copies can still be in the heap after relocation; each one traps on protection and heals when loaded. C4 does not run a separate pass to fix them. The next marking visits every live field anyway, so it fixes them on the way (line L12), and after it the old pages can be unprotected and used again (line L13).

**What the model leaves out.** C4 runs two such collectors, one for the young generation and one for the old, with a [remembered set](/remembered-set/) between them, and they can run at the same time. Its checkpoints let each thread pass on its own, so no step stops all threads; the model takes each checkpoint for all threads in one step. The real system uses virtual memory to protect pages and to remap large ranges fast, with changes to the operating system kernel. There are many collector threads and weak references.

## Example

The page size is 6. Page 0 holds an object $A$ in a register, with a field that points to $B$, and four dead objects. The first marking flips $e$, marks $A$ and $B$, and fixes the NMT bit of $A.f$. Two live objects of six is few, so page 0 is chosen.

1. **Relocate.** Line L15 protects page 0. At the checkpoint, $A$ is copied to a new page because the register points to it; the copy's field still points to $B$ on page 0.
2. **The mutator loads $A.f$.** The NMT bit is right, but page 0 is protected, so the barrier traps. $B$ has no entry, so the mutator copies $B$ to its own page, installs the entry, and writes the new pointer into $A.f$.
3. **The next load of $A.f$** is good and does not trap.
4. **The collector** reaches $B$ at line L16, finds the entry, and goes on. Line L17 releases page 0. Page 0 stays protected.

If the collector had copied $B$ first, $A.f$ would still point into page 0 after the release. The tests run that schedule too. In the next marking, the first load of $A.f$ traps once for both reasons: the NMT bit is old and the page is protected. The trap remaps the pointer through the forwarding data, marks $B$, and heals the field. When that marking ends, page 0 is unprotected and free.

## Correctness

The proof in the proofs section shows the following, and the tests check it after every step of random programs on three mutator threads.

1. **Mutators hold only good pointers.** A register gets a value from a checkpoint, which fixes it, from a new object, from another register, or from line L3, which returns a good value.
2. **One copy wins.** The forwarding entry of each object is written once, by a compare-and-swap, so all threads that move or remap the object agree on the copy.
3. **Marking is complete.** Every pointer that a mutator holds or stores during marking was marked: roots at line L10, loads at line L8. An object allocated in this cycle counts as live. So when the mark stack is empty, every reachable object is marked or new, and line L14 frees no reachable object.
4. **Released pages are safe.** A released page is protected, so any pointer into it traps and is remapped through the forwarding data. The page is unprotected and reused only after a full marking, which has fixed every live field.

Without the barrier, a mutator loads a pointer that is not marked through, or that points into a protected page; the tests find a broken invariant in every one of 40 seeded runs.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above. The bounds are for one cycle.

- **Collector work.** Marking visits each live object and its fields, $O(n p)$; relocation copies at most the live objects of the relocation set, $O(n)$; the checkpoints touch the $r$ roots, and lines L13 and L14 scan the $P$ pages. In total $O(n p + r + P)$, and $\Theta(r + P)$ when nothing is live.
- **Barrier.** On each load of a pointer from the heap, a test of one bit and a test of the page's protection, $O(1)$. A trap costs $O(1)$ plus the size of the object if it copies it. Self-healing bounds the traps by the number of fields that hold stale pointers, once per phase.
- **No global pause.** Each thread does $O(\text{its roots})$ work at a checkpoint, and the other threads go on.
- **Space.** Mark bits for $n$ objects, forwarding data with one entry per moved object, and per-page data: $O(n + P)$. Quick release means the spare memory for copies can be as small as a few pages.

## Properties

- **Concurrent and compacting.** Marking, relocation and remapping all run beside the mutators. The heap never fragments.
- **Generational.** C4 collects a young and an old generation with the same concurrent algorithm, so a high rate of allocation does not force a full-heap cycle each time.
- **A cost on every load.** The barrier runs on every pointer load from the heap. A wave of traps follows each flip and each start of relocation.
- **Floating garbage.** Objects that die during a cycle stay until the next one.
- **Needs help from the operating system.** The fast protection and remapping of pages used changes to the Linux kernel in the system that the paper describes.

## Variants and improvements

- **Pauseless (2005).** The first form, on Azul's Vega processors, had a read barrier instruction in hardware and only one generation. It had the same phases and self-healing.
- **ZGC.** The [Z garbage collector](/z-garbage-collector/) of OpenJDK keeps the same plan: a self-healing load barrier, quick release of relocated pages, and remap folded into the next marking. It keeps its state in color bits of the pointer, not in page protection, and it became generational only in JDK 21.
- **Shenandoah.** [Shenandoah](/shenandoah-collector/) moved objects concurrently first with a forwarding word in each object, and later with a load barrier much like the LVB.
- **Baker's barrier.** [Baker's collector](/baker-real-time-collector/) (1978) also copied an object when the program loaded a pointer to it, but it did not heal the field, and it used two semispaces.

## When to use it

Use it for programs on the JVM with large heaps and strict limits on pause times, such as trading, search and other low-latency services, where a stop of even tens of milliseconds is a problem. The cost is a barrier on every pointer load and a need for spare CPU for the collector threads. For batch work, a parallel stop-the-world collector gives more throughput.

## Pitfalls

- **Trap storms.** Right after a flip, every pointer in the heap is stale. If the mutators touch many fields at once, many of them trap. Self-healing keeps the total to one trap per field.
- **A copy that loses.** A thread that loses the compare-and-swap at line L6 must use the winner's copy, or two threads see two objects.
- **Unprotecting too soon.** A released page may be unprotected and reused only after a full marking has fixed every pointer into it. Before that, a stale field may still point there.
- **Forwarding data on the page.** Quick release only works because the forwarding data are kept off the page. A design that keeps the new address in the old object cannot release the page until every pointer is fixed.
- **Checkpoints, not pauses.** The collector must not go on until every thread has passed the checkpoint; a thread that has not passed it may still hold pointers with the old NMT value.

## Implementations

## History

Baker's [real-time collector](/baker-real-time-collector/) (1978) kept the program away from old copies with a read barrier. Appel, Ellis and Li (1988) used page protection for a concurrent copying collector. Click, Tene and Wolf described the Pauseless collector of Azul Systems in 2005; it ran on Azul's Vega processors, which had a read barrier in hardware. Tene, Iyengar and Wolf then described C4 at ISMM 2011: the same design on x86, with two generations and with changes to the Linux kernel for fast changes to page mappings. It is the collector of Azul's JVM, Zing. Its ideas, the self-healing barrier and the quick release in particular, came back in [ZGC](/z-garbage-collector/) for OpenJDK in 2018.

## References
