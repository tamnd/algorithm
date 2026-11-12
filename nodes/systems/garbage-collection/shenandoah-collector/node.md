---
tag: 1QJAF8
kind: algorithm
slug: shenandoah-collector
name: Shenandoah collector
aliases:
- Shenandoah GC
area: systems/garbage-collection
level: research
summary: "A concurrent, region-based, compacting collector of OpenJDK. It marks with SATB and moves objects while the program runs, first with Brooks pointers, later with a load barrier."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {n: the live objects, p: the pointer fields per object, r: the roots, R: the regions of the heap}
  time: {worst: O(n p + r + R), best: Θ(r + R)}
  space: {extra: O(n + R)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2016
  people: [Christine H. Flood, Roman Kennke, Andrew Dinn, Andrew Haley, Roland Westrelin]
  note: Flood, Kennke, Dinn, Haley and Westrelin of Red Hat described Shenandoah at PPPJ 2016. It marks concurrently with a snapshot-at-the-beginning barrier and evacuates regions while the program runs, with a Brooks forwarding pointer in each object and a compare-and-swap to install it.
prereqs: [concurrent-garbage-collection, snapshot-at-the-beginning, read-barrier, copying-collection]
see_also: [garbage-first-collector, z-garbage-collector, c4-collector, baker-real-time-collector, write-barrier, compare-and-swap, heap-compaction, remembered-set]
sources:
  - paper: doi:10.1145/2972206.2972210
    title: "Christine H. Flood, Roman Kennke, Andrew Dinn, Andrew Haley and Roland Westrelin, Shenandoah: An open-source concurrent compacting garbage collector for OpenJDK, PPPJ 2016, 1-9"
    locator: The phases, the Brooks forwarding pointer, the read and write barriers, and evacuation with a compare-and-swap
  - url: https://openjdk.org/jeps/189
    title: "JEP 189: Shenandoah: A Low-Pause-Time Garbage Collector (Experimental)"
    locator: Shenandoah comes into OpenJDK in JDK 12
---

Shenandoah is a collector of OpenJDK, built at Red Hat and described by Flood, Kennke, Dinn, Haley and Westrelin in 2016. Like [G1](/garbage-first-collector/), it cuts the heap into regions, marks the live objects with a [snapshot-at-the-beginning](/snapshot-at-the-beginning/) barrier, and then reclaims the regions with the most garbage by copying their live objects out. Unlike G1, it does the copy while the program runs. Each object being moved gets a *forwarding pointer* to its new copy, installed with a [compare-and-swap](/compare-and-swap/), so the collector and a program thread can race to copy it and both end up with the same copy. The first design gave every object an extra word for this, a *Brooks pointer*, and sent every access through it. Since JDK 13, a *load reference barrier* instead fixes each pointer as it is loaded, so the program never sees an old copy. **This page gives a small model of the mechanism, not the real collector.**

## In plain words

The heap is cut into many boxes. First, a helper finds out which objects are still in use, while the program runs. Then it picks the boxes with the most garbage.

Next, the helper copies the objects that are still in use out of those boxes, again while the program runs. Each old object gets a note with the address of its new copy. If the program needs an object that has not moved yet, it moves it itself. Two threads may try to move the same object; only the first note counts, and the other copy is thrown away.

Last, the helper goes over the heap and changes every old address to the new one. A short stop fixes the program's own pointers, and the old boxes are free.

## The problem

**Heap model.** The heap is a row of regions of $S$ slots. An object has a few pointer fields and a forwarding pointer, which is empty until the object is copied. Each mutator thread has a few registers and does atomic steps: allocate, load a field, store a register into a field, copy or clear a register. The collector is one more thread. A pause is a step taken when every mutator is between operations.

**Goal.** Reclaim the unreachable objects and compact the heap, with pauses that do not grow with the heap. No write may be lost: once an object has a copy, every write must go to that copy. With the load reference barrier, keep the stronger *to-space invariant*: no register points into the collection set while it is being moved.

## The algorithm

$\textit{fwd}(a)$ is the forwarding pointer of $a$ if it is set, and $a$ otherwise. The *collection set* is empty except between lines L13 and L16.

```pseudo id=main
EVACUATE(a)                                    ▷ a is in the collection set
L1  if fwd(a) = a then
L2      b ← a copy of a in a region of this thread
L3      CAS the forwarding pointer of a from empty to b      ▷ only the first copy is installed
L4  return fwd(a)                                             ▷ the winner's copy

LOAD(x, f)                                     ▷ a mutator loads x.f
L5  v ← x.f, read through fwd(x) in Brooks mode
L6  if load reference barrier and v is in the collection set then v ← EVACUATE(v); CAS x.f from the old v to the new one
L7  return v

STORE(x, f, y)                                 ▷ a mutator stores y into x.f
L8  if marking and x.f ≠ nil then push x.f on the SATB queue            ▷ pre-write barrier
L9  if Brooks mode then x ← EVACUATE(x) if x is in the collection set, else fwd(x); y ← fwd(y)
L10 x.f ← y

CYCLE()                                        ▷ the collector thread
L11 Init Mark pause: mark the objects that the roots point to
L12 concurrent: take an object from the SATB queue or the mark stack; mark the targets of its fields
L13 Final Mark pause: finish marking; free the regions with no live object; choose the collection set; evacuate the root objects
L14 concurrent: for each marked object a in the collection set do EVACUATE(a)
L15 concurrent, after an Init Update Refs pause: for each live object outside the collection set, set each field v in the collection set to fwd(v)
L16 Final Update Refs pause: set each root v in the collection set to fwd(v); free the regions of the collection set
```

**Marking.** Lines L11, L12 and L8 are [snapshot-at-the-beginning](/snapshot-at-the-beginning/) marking: every object reachable at the start is marked, because a store logs the pointer it overwrites. Objects allocated during the cycle count as live.

**Choosing the regions.** Line L13 frees at once the regions with no live object (Shenandoah calls this *immediate garbage*), and puts in the collection set the regions with little live data. The real heuristics weigh the garbage of each region and the free memory.

**Evacuation and the race.** Both the collector (line L14) and a mutator (lines L6 and L9) call EVACUATE. A copy is made at line L2, and line L3 installs it only if no other copy was installed in between. A thread whose compare-and-swap fails uses the winner's copy at line L4; its own copy is garbage. This is the heart of the design: it lets the mutator move an object it needs without a lock.

**Brooks mode (2016).** Every object has a forwarding word that points to itself until the object moves. Every read goes through it (line L5), so a mutator may hold a pointer to an old copy and still read the current data. Every write first evacuates its target if it is in the collection set (line L9), so no write goes to an old copy after a copy exists. The stored value is also passed through $\textit{fwd}$, so that a pointer to an old copy is not written into a field that line L15 has already fixed.

**Load reference barrier (JDK 13).** A pointer is fixed when it is loaded from the heap (line L6). The mutator never holds a pointer into the collection set, so plain reads and writes are safe, and the stored value needs no barrier. The field is healed, so the next load of it is fast.

**Update references.** After evacuation, line L15 walks the live objects outside the collection set and replaces each pointer to an old copy. Line L16 fixes the roots and frees the old regions. After it, no pointer into them remains.

**What the model leaves out.** The real collector has many threads in each phase, processes weak references and class unloading, has humongous regions, and falls back to a *degenerated* or a full stop-the-world collection when it cannot keep up. Since JDK 13 the forwarding pointer is kept in the object's header word, not in an extra word; in the model it is an attribute of the object in both modes.

## Example

The region size is 6. Region 0 holds an object $A$ in a register, with a field that points to $B$, and four dead objects. Marking finds $A$ and $B$, two live objects of six, so region 0 is the collection set.

1. **Final Mark.** The pause copies $A$, because a root points to it, and sets the root to the copy $A'$. The field $A'.f$ still points to $B$ in region 0.
2. **Load reference barrier.** The mutator loads $A'.f$. Line L6 sees that $B$ is in the collection set. $B$ is not forwarded, so the mutator copies it to its own region, installs the forwarding pointer, and heals $A'.f$ to point to $B'$. The next load of $A'.f$ needs no work.
3. **The collector** reaches $B$ at line L14, sees the forwarding pointer, and goes on.
4. **Brooks mode, the same heap.** The mutator loads $A'.f$ and keeps the old address of $B$ in a register; that is allowed. If the collector has copied $B$ and the mutator then stores into $B$, line L9 turns the target into $B'$, and the write goes to the copy. Without that barrier, the write goes to the old $B$, and it is lost when region 0 is freed; the tests show both cases.

The tests also run the two races with the load reference barrier: the collector installs first and the mutator uses its copy, or the other way round.

## Correctness

The proof in the proofs section shows the following. The tests check it after every step of random programs on three mutator threads, in both modes.

1. **One copy.** A forwarding pointer is set once, by compare-and-swap, and never changes. Every thread that moves or follows the object then uses the same copy.
2. **No lost write.** With the load reference barrier, a register never points into the collection set, so every write goes to a copy outside it. In Brooks mode, a write to an object of the collection set first evacuates it. In both modes, once a copy is installed, the old object is never written again.
3. **Marking is complete.** By the snapshot argument, every object reachable at the end of marking was reachable at its start or was allocated during it, and is marked or counted as live.
4. **No pointer into a freed region.** Evacuation copies every marked object of the collection set. Line L15 fixes every field of every live object, line L16 fixes the roots, and stores during line L15 write only to-space pointers. So when line L16 frees the regions, nothing reachable points into them.

Without the barriers, the tests find a broken run for most seeds: a register that points into the collection set, a write to an old copy, a reachable object that marking missed, or a changed graph.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above. The bounds are for one cycle.

- **Collector work.** Marking visits each live object and its fields, $O(n p)$. Evacuation copies at most the live objects of the collection set, $O(n)$. Updating references visits each live object and its fields again, $O(n p)$. The pauses touch the $r$ roots, and the choice of regions scans the $R$ regions. In total $O(n p + r + R)$, and $\Theta(r + R)$ when nothing is live.
- **Pauses.** Each pause is $O(r)$ in the model, plus $O(R)$ to choose the regions. The real collector also scans thread stacks in the pauses, so a pause grows with the roots but not with the heap.
- **Barriers.** In Brooks mode every read and write pays one extra load of the forwarding word, and writes and stores of pointers pay a test. With the load reference barrier, only loads of pointers from the heap pay a test, $O(1)$. A slow path costs $O(1)$ plus the size of the object if it copies it.
- **Space.** Mark bits and per-region data, $O(n + R)$. In Brooks mode each object, live or dead, also has one extra word.

## Properties

- **Concurrent and compacting.** Marking, evacuation and the update of references all run beside the mutators; the heap does not fragment.
- **Not generational, in its first form.** Each cycle marks the whole heap. A program that allocates fast needs room to spare so that a cycle can finish.
- **Pauses that do not grow with the heap.** The pauses do work in the roots, not in the live data.
- **Floating garbage.** Snapshot marking keeps every object that was live at the start of marking until the next cycle.
- **Two modes, two invariants.** Brooks mode lets the mutator hold old pointers and makes every access pay. The load reference barrier keeps the to-space invariant and makes only pointer loads pay.

## Variants and improvements

- **The load reference barrier (JDK 13).** It replaced the read and write barriers of Brooks mode with one barrier on pointer loads, and soon after the extra forwarding word was dropped: the forwarding pointer of an object that has moved is kept in its header.
- **Update of references in the next marking.** Instead of a separate pass (line L15), a collector can fix old pointers during the next marking, as [ZGC](/z-garbage-collector/) and [C4](/c4-collector/) do. That saves a walk of the heap but keeps the old regions until the next cycle.
- **Generational mode.** A generational mode for Shenandoah has been developed in OpenJDK; its release status is not checked here.
- **Read barriers in other collectors.** [Baker's collector](/baker-real-time-collector/) copied an object when the program loaded a pointer to it, without a compare-and-swap, since it ran on one processor. C4 and ZGC use self-healing load barriers much like the load reference barrier.

## When to use it

Use it for programs on the JVM that need short pauses, of a few milliseconds or less, on heaps from a few gigabytes upward, and that can spare some CPU and memory for the collector. It suits services with strict response times. For batch work, a parallel stop-the-world collector gives more throughput; for a pause target of tens of milliseconds, G1 often does as well with less overhead.

## Pitfalls

- **A copy that loses.** A thread whose compare-and-swap fails at line L3 must use the winner's copy. If it used its own, two threads would see two objects, and a write would be lost.
- **Writes to the old copy.** In Brooks mode, a write that does not go through the write barrier lands in the old copy after the collector has copied the object, and it is lost. The tests show this.
- **Old pointers stored late.** In Brooks mode, a mutator may hold an old pointer during the update of references. If it stores it into a field that line L15 has already fixed, the field points into a region that is about to be freed. The store must pass the value through $\textit{fwd}$.
- **Pointer comparison.** In Brooks mode, two pointers to the same object may differ, one to the old copy and one to the new. A comparison of pointers must compare $\textit{fwd}$ of both.
- **Running out of memory during evacuation.** If no free region is left for copies, the cycle cannot finish concurrently, and the real collector falls back to a longer pause.

## Implementations

## History

Brooks (1984) proposed the forwarding word in each object, so that a read barrier is one extra load, for an incremental copying collector in the line of [Baker](/baker-real-time-collector/) (1978). Red Hat built Shenandoah for OpenJDK, and Flood, Kennke, Dinn, Haley and Westrelin described it at PPPJ 2016. It came into OpenJDK in JDK 12 as an experimental collector (JEP 189). In JDK 13 the load reference barrier replaced the Brooks barriers, and the extra forwarding word was removed. Later releases made it a product feature; the release is not checked here.

## References
