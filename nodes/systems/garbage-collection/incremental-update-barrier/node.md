---
tag: PCHTN8
kind: technique
slug: incremental-update-barrier
name: Incremental update barrier
aliases:
- Dijkstra write barrier
- insertion barrier
- Dijkstra insertion barrier
- Steele write barrier
area: systems/garbage-collection
level: advanced
summary: "A write barrier for incremental marking: when the mutator stores a pointer, shade the new target gray, or make the source gray again. A final remark rescans the roots."
history:
  year: 1975
  people: [Guy L. Steele Jr., Edsger W. Dijkstra, Leslie Lamport]
  note: Steele (CACM, September 1975) made the source of a store gray again. Dijkstra, Lamport, Martin, Scholten and Steffens (CACM, November 1978) shaded the new target. Both keep a black object from hiding a white one.
prereqs: [tricolor-marking, write-barrier, incremental-garbage-collection]
see_also: [snapshot-at-the-beginning, on-the-fly-garbage-collection, concurrent-garbage-collection, card-marking, mark-and-sweep, read-barrier, baker-real-time-collector]
sources:
  - paper: doi:10.1145/359642.359655
    title: "Edsger W. Dijkstra, Leslie Lamport, A. J. Martin, C. S. Scholten and E. F. M. Steffens, On-the-fly garbage collection: an exercise in cooperation, Communications of the ACM 21(11), 966-975, 1978"
    locator: The mutator operation that redirects a pointer and then shades the new target, and the invariant that no black node points to a white node
  - paper: doi:10.1145/361002.361005
    title: "Guy L. Steele Jr., Multiprocessing compactifying garbage collection, Communications of the ACM 18(9), 495-508, 1975"
    locator: The store operation of the mutator, which returns a marked source to the set of nodes to scan again
  - paper: doi:10.1145/113445.113459
    title: "Hans-J. Boehm, Alan J. Demers and Scott Shenker, Mostly parallel garbage collection, PLDI 1991, 157-164"
    locator: Concurrent marking with virtual memory dirty bits, and the final stop-the-world pass over the roots and the dirty pages
  - paper: doi:10.1145/286860.286863
    title: "Pekka P. Pirinen, Barrier techniques for incremental tracing, ISMM 1998, 20-25"
    locator: The classification of barriers by the color of the mutator and the action on a store
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 15 (concurrent garbage collection, the tricolor invariants and the barrier techniques)
  - paper: doi:10.1007/BFb0017182
    title: "Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, 1-42"
    locator: Section 3 (incremental tracing collectors, incremental update and snapshot-at-beginning barriers)
---

An incremental update barrier is a [write barrier](/write-barrier/) that lets a marker run in small steps while the [mutator](/mutator-and-collector/) changes the heap. When the mutator stores a pointer during marking, the barrier makes sure that the marker sees the new edge: the barrier of Dijkstra et al. (1978) shades the new target gray, and the barrier of Steele (1975) makes the source gray again so that it is scanned again. Both keep the strong [tricolor invariant](/tricolor-marking/): no black object points to a white object. The roots are usually not covered by the barrier, so the cycle ends with a short stop-the-world *remark* that rescans the roots before the sweep. The other main barrier is the deletion barrier of [snapshot-at-the-beginning](/snapshot-at-the-beginning/).

## In plain words

The marker colors objects as it goes. White means not yet seen, gray means seen but not yet followed, and black means finished.

The danger is this. The program copies a pointer to an unseen object into a finished object, and then removes the last other path to it. The marker will never look inside the finished object, so it never sees the unseen object, and the sweep frees an object that the program still uses.

The incremental update barrier is a small piece of code that runs on each pointer store. Dijkstra's form makes the stored object gray at once, so the marker will visit it. Steele's form makes the finished object gray again, so the marker will look inside it one more time. Program variables are not watched, so at the end the program stops briefly and the marker scans its variables again.

## When it applies

**Heap model.** The heap holds objects with $k$ pointer fields. The mutator holds its references in $r$ registers (the [roots](/gc-roots/)), and it runs four operations: load a field into a register, store a register into a field, clear a register, and allocate an object. The collector is an incremental [tricolor](/tricolor-marking/) marker with a gray stack $W$, followed by a sweep, as in [mark-and-sweep](/mark-and-sweep/). The two take turns at the granularity of one mutator operation and one mark step, as in [incremental garbage collection](/incremental-garbage-collection/).

**What is measured.** The cost of the barrier on each pointer store, the length of the final remark pause, and the floating garbage: objects that are unreachable at the sweep but survive it.

The technique applies when three things hold:

- the collector marks while the mutator runs, so the reachability graph changes under the marker;
- the store and its barrier act as one step with respect to the marker (true for an incremental collector on one thread; a concurrent collector needs the order that Dijkstra et al. give, see the pitfalls);
- the collector can stop the mutator once at the end to rescan the roots, or the roots are also covered by a barrier.

## The template

```pseudo id=main
WRITE(x, f, y)                         ▷ Dijkstra et al.: shade the new target
L1  x.f ← y
L2  if marking and y ≠ nil and y is white then
L3      make y gray, push y on W

WRITE-STEELE(x, f, y)                  ▷ Steele: make the black source gray again
L4  x.f ← y
L5  if marking and x is black and y ≠ nil and y is white then
L6      make x gray, push x on W

BEGIN-CYCLE()
L7  make every object white, W ← empty
L8  for each root r do SHADE(r)
L9  marking ← true

MARK-STEP()                            ▷ one unit of collector work
L10 if W is not empty then
L11     x ← pop W
L12     for each field y of x do SHADE(y)
L13     make x black
L14 else FINAL-REMARK()

FINAL-REMARK()                         ▷ the mutator is stopped
L15 for each root r do SHADE(r)
L16 while W is not empty do lines L11 to L13
L17 marking ← false
L18 free every white object
```

SHADE$(y)$ makes a white $y$ gray and pushes it on $W$; it does nothing to nil, gray or black. An object is gray exactly when it is on $W$. New objects are allocated white: they have only nil fields, and if they are still reachable at the end, the remark finds them through the roots.

Dijkstra's barrier (lines L1 to L3) runs on every pointer store during marking, whatever the color of $x$. Steele's barrier (lines L4 to L6) acts only when a black object receives a white pointer, and then it sends the whole object back to $W$. Boehm, Demers and Shenker (1991) do the same at page granularity with no barrier code at all: the virtual memory system records which pages were written, and the final pause rescans the marked objects on the dirty pages.

### Why it works

The strong invariant is: no black object has a field that points to a white object. It holds at line L9, since no object is black. Line L13 blackens $x$ only after line L12 shaded all its fields. A store keeps it: with Dijkstra's barrier the new target is not white after line L3, and with Steele's barrier a black source with a white target becomes gray at line L6. Loads, register changes and allocation create no field from a black object. When FINAL-REMARK ends, $W$ is empty, so there is no gray object, every root is black, and by the invariant the black set is closed under fields. So it holds every reachable object, and line L18 frees only garbage. The full proof, and the proof that every object that was garbage at line L7 is freed, are in the proofs section.

### Cost

- **Barrier.** $O(1)$ per pointer store: one color test and at most one push. Loads have no barrier, which is the main reason to prefer a write barrier to a [read barrier](/read-barrier/).
- **Marking.** Each object is pushed at most once per cycle under Dijkstra's barrier, so the mark steps scan at most $L + A$ objects, where $L$ is the number of objects reachable at line L7 and $A$ the number allocated during the cycle. Under Steele's barrier a source can be scanned again each time it receives a white pointer, so the scan work is at most $L + A$ plus one scan per such store.
- **Remark pause.** $O(r)$ to shade the roots plus the scans of line L16. There is no constant bound: everything that is reachable only through the registers can be left for the pause. In the worst case the pause marks the whole live heap again.

## Classic examples

**The lost object.** The heap is $X \to Y \to Z$ (field 0 in each case), register 0 holds $X$, and register 2 stays nil. The mutator runs six operations: load $Y$ into register 1, load $Z$ into register 1, store register 1 into $X$.f1, load $Y$ into register 1, store nil into $Y$.f0, and clear register 1.

| step | who | action | colors of $X, Y, Z$ with no barrier |
|---|---|---|---|
| 0 | collector | BEGIN-CYCLE shades the root $X$ | gray, white, white |
| 1 | collector | MARK-STEP scans $X$ | black, gray, white |
| 2, 3 | mutator | register 1 gets $Y$, then $Z$ | black, gray, white |
| 4 | mutator | $X$.f1 ← $Z$ | black, gray, white |
| 5, 6, 7 | mutator | register 1 gets $Y$, $Y$.f0 ← nil, register 1 cleared | black, gray, white |
| 8 | collector | MARK-STEP scans $Y$, which now has no fields | black, black, white |
| 9 | collector | FINAL-REMARK: the root $X$ is black, $W$ is empty, sweep | $Z$ is freed |

With no barrier, step 4 makes the black $X$ point to the white $Z$, step 6 cuts the gray path $Y \to Z$, and the sweep frees $Z$ while $X$.f1 still points to it. With Dijkstra's barrier, step 4 makes $Z$ gray, step 8 scans $Y$ and step 9 scans $Z$, so $Z$ survives. With Steele's barrier, step 4 makes $X$ gray again, and a later step scans $X$ and finds $Z$.

The program has 6 operations, and the collector needs a state-dependent number of steps. Over all interleavings of the two, there are 207 runs with no barrier, and 9 of them free the reachable $Z$. There are 210 runs with Dijkstra's barrier and 255 with Steele's barrier (Steele's barrier can add scans), and none of them frees a reachable object. On 400 random heaps of 6 objects with random programs of 12 operations and random schedules (seed 7), neither barrier ever frees a reachable object, while the run with no barrier sometimes does.

**A long remark.** The heap is $X \to 1 \to 2 \to 3 \to 4$, a list that hangs off the root $X$. The mutator loads the head 1 into register 1 and then stores nil into $X$.f0. Now the list is reachable only from a register. The marker scans $X$ and finds nothing, so all 4 list objects are scanned inside FINAL-REMARK, with the mutator stopped. A [snapshot-at-the-beginning](/snapshot-at-the-beginning/) barrier shades object 1 when the field is overwritten, and the same 4 scans happen while the mutator runs.

**Systems.** The on-the-fly collector of Dijkstra et al. uses the shading barrier; see [on-the-fly garbage collection](/on-the-fly-garbage-collection/). The mostly parallel collector of Boehm, Demers and Shenker and the CMS collector of the HotSpot JVM use dirty pages or [card marking](/card-marking/) with a final remark; see [concurrent garbage collection](/concurrent-garbage-collection/). The Go runtime used a Dijkstra barrier with a stop-the-world rescan of goroutine stacks until Go 1.8, which changed to a hybrid of the Dijkstra and Yuasa barriers so that stacks need no rescan.

## Variations

- **Dijkstra (shade the target).** Unconditional and simple. It may shade an object that dies before the end of the cycle, which then floats.
- **Steele (gray the source).** Shades less, since the target is reached only if the source is still reachable when it is scanned again. It may rescan a large object many times.
- **Dirty cards or pages.** Boehm, Demers and Shenker and CMS record the written region, not the object. The barrier is one store, and the remark scans the marked objects in dirty cards. A concurrent pre-cleaning pass can scan most dirty cards before the pause to make the pause shorter.
- **Black allocation.** Allocating new objects black removes them from the remark work, but then an object that dies in the cycle cannot be freed in that cycle.
- **Black mutator.** If the roots are scanned first and kept black, a barrier on loads is needed as well; this is the setting of [Baker's collector](/baker-real-time-collector/). The incremental update barrier assumes a gray mutator, whose roots are rescanned at the end.

The incremental update barrier keeps the *strong* invariant and frees objects that die during the cycle. The [snapshot-at-the-beginning](/snapshot-at-the-beginning/) barrier keeps the *weak* invariant, needs no rescan of the roots, and keeps every object that was live when the cycle started. When both collectors sweep at the same point of the same mutator program, the incremental update collector keeps a subset of what the snapshot collector keeps. In the seed 5 runs of the snapshot page, the incremental update collector left 820 floating objects against 980 for the snapshot barrier, over the same 443 runs.

## Pitfalls

- **Shading before the store in a concurrent collector.** If the mutator shades $y$ and then stores it, and it is delayed between the two steps, a whole collection cycle can run in the gap and whiten everything again; the store then happens with no shade. Dijkstra et al. report that an earlier version had this order and that W. H. J. Woodger found this scenario. Store first, then shade.
- **Forgetting the roots.** Stores into registers and stack slots are not barriered in most systems, so the remark at line L15 is required. Without it, an object that is held only in a register at the end is freed.
- **Assuming a short remark.** The remark is short only when little is reachable only from the roots. The long remark example above shows the worst case, which is why CMS adds concurrent pre-cleaning and why later collectors moved to snapshot barriers.
- **Missing stores.** Every pointer store into the heap needs the barrier: array elements, static fields that are not scanned as roots, and stores done by the runtime (for example when an object is cloned).
- **A color test that races.** Shading $y$ only when $x$ is black is enough in the incremental model, where the test, the store and the shade are one step. A concurrent marker can blacken $x$ between the test and the store, so a concurrent collector either shades without the test or makes the test and the store atomic.

## Exercises

1. In the lost-object example, find a schedule where Steele's barrier scans $X$ twice. How many mark steps does that run take?
2. Show that if new objects are allocated black under Dijkstra's barrier, the invariant still holds, and find a run where this keeps an object that the white allocation frees.
3. Give a family of heaps and mutator programs of length 2 where the remark under Dijkstra's barrier scans every one of $n$ objects.
4. Prove that under Dijkstra's barrier each object is pushed on $W$ at most once per cycle, and find a run where Steele's barrier pushes the same object three times.

## References
