---
tag: 4TDCX9
kind: technique
slug: snapshot-at-the-beginning
name: Snapshot-at-the-beginning
aliases:
- SATB
- Yuasa deletion barrier
- SATB marking
- snapshot-at-beginning barrier
area: systems/garbage-collection
level: advanced
summary: "Incremental marking with a deletion barrier: before a pointer field is overwritten, shade its old target. Every object live at the start is marked; new objects are black."
history:
  year: 1990
  people: [Taiichi Yuasa]
  note: Yuasa described real-time mark-and-sweep with a barrier that marks the old value of each overwritten pointer field, so that the collector marks the heap as it was when the cycle began.
prereqs: [tricolor-marking, write-barrier, incremental-garbage-collection]
see_also: [incremental-update-barrier, garbage-first-collector, shenandoah-collector, concurrent-garbage-collection, mark-and-sweep, on-the-fly-garbage-collection]
sources:
  - paper: doi:10.1016/0164-1212(90)90084-Y
    title: "Taiichi Yuasa, Real-time garbage collection on general-purpose machines, Journal of Systems and Software 11(3), 181-198, 1990"
    locator: The incremental mark-and-sweep algorithm, the marking of the old value on each pointer store, and the analysis of the real-time bound
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 15 (concurrent garbage collection, the weak tricolor invariant and deletion barriers) and Chapter 16 (concurrent mark-sweep)
  - paper: doi:10.1007/BFb0017182
    title: "Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, 1-42"
    locator: Section 3 (incremental tracing collectors, snapshot-at-beginning algorithms)
  - paper: doi:10.1145/1029873.1029879
    title: "David Detlefs, Christine Flood, Steve Heller and Tony Printezis, Garbage-first garbage collection, ISMM 2004, 37-48"
    locator: The concurrent marking phase, which uses a snapshot-at-the-beginning barrier with per-thread buffers of old values
---

Snapshot-at-the-beginning (SATB) is a way to mark the heap incrementally or concurrently with a *deletion barrier*: before the [mutator](/mutator-and-collector/) overwrites a pointer field during marking, the [write barrier](/write-barrier/) shades the old target of the field gray. Yuasa (1990) used it for real-time [mark-and-sweep](/mark-and-sweep/). The collector then marks every object that was reachable when the cycle began, plus every object allocated during the cycle, which is allocated black. It keeps the weak [tricolor invariant](/tricolor-marking/), needs no rescan of the roots at the end, and pays for this with floating garbage: objects that die during the cycle survive until the next one. The [Garbage-First](/garbage-first-collector/) and [Shenandoah](/shenandoah-collector/) collectors mark this way.

## In plain words

At the start, the collector takes a picture of what the program can reach. It promises to keep everything in that picture, and everything that the program creates while the collection runs.

To keep the promise without a real copy of the heap, it watches pointer writes. Just before the program overwrites a pointer, the barrier looks at the object that the old pointer named and marks it as "to visit". So a pointer can never vanish before the marker has followed it. The program can move a pointer around as much as it likes: the old place is always recorded before it changes.

The price is that the collector keeps some junk. An object that the program drops during the collection was in the picture, so it stays until the next collection.

## When it applies

**Heap model.** The heap holds objects with $k$ pointer fields. The mutator holds its references in $r$ registers (the [roots](/gc-roots/)) and runs four operations: load a field into a register, store a register into a field, clear a register, and allocate. The collector is an incremental [tricolor](/tricolor-marking/) marker with a gray stack $W$, followed by a sweep. One short pause at the start shades the roots. After it, the two take turns at the granularity of one mutator operation and one mark step, as in [incremental garbage collection](/incremental-garbage-collection/).

**What is measured.** The barrier cost on each pointer store, the pauses (one at the start for the roots, and none at the end in this model), the marking work, and the floating garbage.

It applies when:

- the roots can be scanned once, atomically, at the start of the cycle (or per thread with a handshake, as in [on-the-fly collection](/on-the-fly-garbage-collection/));
- every pointer store into the heap goes through the barrier, which reads the old value;
- keeping the objects that die during one cycle is acceptable.

## The template

```pseudo id=main
WRITE(x, f, y)                         ▷ Yuasa: shade the old target, then store
L1  if marking then
L2      z ← x.f                        ▷ the pointer that is about to vanish
L3      if z ≠ nil and z is white then make z gray, push z on W
L4  x.f ← y

ALLOCATE()
L5  x ← a new object with nil fields
L6  if marking then make x black
L7  return x

BEGIN-CYCLE()                          ▷ a short pause: snapshot the roots
L8  make every object white, W ← empty
L9  for each root r do SHADE(r)
L10 marking ← true

MARK-STEP()                            ▷ one unit of collector work
L11 if W is not empty then
L12     x ← pop W
L13     for each field y of x do SHADE(y)
L14     make x black
L15 else marking ← false
L16     free every white object
```

SHADE$(y)$ makes a white $y$ gray and pushes it on $W$. Loads have no barrier, and stores into registers have no barrier. The barrier does nothing outside a cycle, so the mutator pays only a flag test between collections.

In a real collector, line L3 does not push on the shared stack. Each thread appends $z$ to a thread-local *SATB buffer*, and full buffers go to the marker. Garbage-First drains the remaining buffers in a short *remark* pause at the end of marking. That pause processes buffered old values; it does not rescan the roots or the heap.

### Why it works

Call the heap graph at line L8 the *snapshot*, and the set of objects reachable in it $S$. Each field of an object of $S$ has a *snapshot value*. When the marker scans an object at line L13, each field either still holds its snapshot value, which is then shaded, or it was overwritten during the cycle; the first such overwrite read the snapshot value at line L2 and shaded it at line L3. So when an object turns black, all its snapshot targets are non-white. Objects never turn white again during the cycle. When $W$ is empty, the black set contains the roots of the snapshot and is closed under snapshot fields, so it contains $S$. New objects are black. An object that was unreachable at line L8 can never become reachable again, so every object that is reachable at line L16 is in $S$ or new, and is black. This is the weak invariant at work: a black object may point to a white one, as long as some gray object still reaches that white one through snapshot fields. The full proof is in the proofs section.

### Cost

- **Barrier.** $O(1)$ per pointer store during marking: one load of the old value, one color test and at most one push. It is more work than an [incremental update barrier](/incremental-update-barrier/), because it must read the field before it writes it.
- **Marking.** Each object is pushed at most once, so the mark steps scan at most $|S|$ objects. New objects are never scanned.
- **Pauses.** $O(r)$ at the start for the roots. In this model there is no final pause; with per-thread buffers, the final pause is in proportion to the buffered entries.
- **Floating garbage.** Exactly the objects of $S$ and the new objects that are unreachable at the sweep. This is the most that any of the standard barriers keeps.

## Classic examples

**The lost object, and why the barrier saves it.** The heap is $X \to Y \to Z$ (field 0 in each case), and register 0 holds $X$. The collector shades $X$ and scans it, so $X$ is black and $Y$ is gray. The mutator then loads $Z$ into register 1, stores it into $X$.f1, and stores nil into $Y$.f0. With no barrier, the marker scans $Y$, finds nothing, and the sweep frees $Z$, which $X$ still points to. With the deletion barrier, the store into $Y$.f0 first reads the old value $Z$ and shades it, so $Z$ survives. Over all interleavings of this 6-operation program with the collector steps, 9 of the 207 runs with no barrier free the reachable $Z$, and none of the 210 runs with the barrier does.

**Floating garbage.** The heap is $X \to Y$, and register 0 holds $X$. During marking, the mutator stores nil into $X$.f0, then allocates an object into register 1 and clears register 1. Both $Y$ and the new object are garbage at the sweep.

| barrier | $Y$ | the new object | floating objects |
|---|---|---|---|
| snapshot-at-the-beginning | shaded by the deletion, kept | allocated black, kept | 2 |
| incremental update (Dijkstra) | never shaded, freed | allocated white, freed | 0 |

On 500 random heaps of 6 objects with random programs of 12 operations and random schedules (seed 5), there are 443 runs in which both collectors sweep at the same point of the program. Over these runs the snapshot barrier leaves 980 floating objects and the incremental update barrier 820, and in each run the survivors of the incremental update collector are a subset of the survivors of the snapshot collector.

**No rescan.** The heap is the list $X \to 1 \to 2 \to 3 \to 4$ with $X$ in register 0. The mutator loads the head 1 into a register and stores nil into $X$.f0. The deletion barrier shades 1, and the marker scans the 4 list objects while the mutator runs. The incremental update barrier does not see the deletion, so its final remark finds the list through the register and scans all 4 objects with the mutator stopped.

**Systems.** Yuasa's collector was for Lisp on stock hardware. The Garbage-First collector of HotSpot marks concurrently with an SATB barrier and per-thread buffers. Shenandoah uses SATB marking as well. The Go runtime's hybrid barrier, introduced in Go 1.8, combines a Yuasa deletion barrier with a Dijkstra insertion barrier, so that goroutine stacks need not be rescanned.

## Variations

- **Gray allocation.** Allocating white or gray instead of black makes the new objects collectable in the same cycle only if a final rescan of the roots is added, which gives up the main advantage.
- **Logging barriers.** Record the old value in a buffer and shade it later, which keeps the fast path of the barrier short. Only the snapshot value of a field matters, so a barrier may also log only the first overwrite of each field in a cycle.
- **Hybrid barriers.** Shade both the old target and the new target. This is how a collector can scan thread stacks one at a time with no barrier on stack stores, at the cost of more floating garbage.
- **Concurrent use.** With a concurrent marker, the read of the old value and the store must be atomic with respect to other mutators that write the same field, or the barrier must be applied with a read before the write in a way the memory model orders.

The [incremental update barrier](/incremental-update-barrier/) watches insertions instead of deletions. It keeps the strong invariant, can free objects that die in the cycle, and needs a final remark that can take as long as marking the part of the heap that only the roots reach.

## Pitfalls

- **Rescanning the roots is not needed, but scanning them at one moment is.** The proof uses one snapshot of all roots. If the stacks of several threads are scanned at different moments, a reference can pass from a thread that is not yet scanned to one that is scanned, through a field that is then overwritten before the barrier is on. Collectors with per-thread scans, such as the Doligez, Leroy and Gonthier collectors, shade both the old and the new target of each store until every thread has scanned its stack.
- **Allocating white.** A new object allocated white has no snapshot path to it, so nothing shades it, and the sweep frees it even if a black object points to it. Allocate black.
- **Bulk operations.** Array copies, clears and object reuse overwrite many fields at once. Each overwritten pointer must be shaded, or the collector must treat the whole operation with a special barrier.
- **Weak references.** A reference loaded from a [weak reference](/weak-reference/) during marking creates a strong path that the snapshot did not have. The load must shade the referent, or it can be freed while in use.
- **Expecting a prompt free.** An object that dies just after the cycle starts is kept for the whole cycle and freed only in the next one. The heap must have room for this.

## Exercises

1. Show that the deletion barrier keeps no black object pointing to a white object that is unreachable from every gray object, and give a run where the strong invariant fails but the collection is still correct.
2. Find the largest floating garbage that one cycle can leave, in terms of the size of $S$ and the number of allocations.
3. Prove that if only the first overwrite of each field in a cycle runs the barrier, the collector is still correct.
4. Explain why a snapshot of the roots per thread, taken at different moments, can lose an object if stack stores have no barrier, with a schedule of two threads.

## References
