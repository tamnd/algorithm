---
tag: YR5TKX
kind: technique
slug: write-barrier
name: Write barrier
aliases:
- store barrier
- GC write barrier
area: systems/garbage-collection
level: core
summary: "Code that the compiler or runtime adds to each pointer store, so that the collector learns of the stores it must know about: generational, card, incremental, SATB."
prereqs: [mutator-and-collector, gc-roots]
see_also: [read-barrier, remembered-set, card-marking, incremental-update-barrier, snapshot-at-the-beginning, reference-counting, tricolor-marking, generational-garbage-collection]
sources:
  - paper: "Benjamin Zorn, Barrier methods for garbage collection, Technical Report CU-CS-494-90, Department of Computer Science, University of Colorado at Boulder, November 1990"
    locator: the classification of read and write barriers by the action they take, and the estimates of their cost in software and with hardware support
  - paper: doi:10.1145/141936.141946
    title: Antony L. Hosking, J. Eliot B. Moss and Darko Stefanovic, A comparative performance evaluation of write barrier implementations, OOPSLA 1992, 92-109
    locator: the measured cost of sequential store buffers, remembered sets and card marking as generational write barriers
  - paper: doi:10.1145/1029873.1029891
    title: Stephen M. Blackburn and Antony L. Hosking, Barriers, friend or foe?, ISMM 2004, 143-151
    locator: the measurements of several read and write barriers in one virtual machine on several processors, and the fast path and slow path split
  - url: https://bibliography.selflanguage.org/_static/write-barrier.pdf
    title: Urs Hoelzle, A fast write barrier for generational garbage collectors, OOPSLA 1993 Workshop on Garbage Collection and Memory Management
    locator: the two-instruction card marking barrier, and the share of the barrier in the total cost
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Section 11.8 (Read and write barriers), and Chapter 15 on the barriers of concurrent collectors
---

A write barrier is a small piece of code that runs with every store of a pointer into the heap. The compiler or interpreter puts it around the store $o.f_i \gets v$, and it tells the collector about the stores that would otherwise break the collector's invariant. A [generational collector](/generational-garbage-collection/) uses it to record old-to-young pointers in a [remembered set](/remembered-set/) or a [card table](/card-marking/). An incremental or concurrent marker uses it to keep the tri-color invariant: an [incremental update](/incremental-update-barrier/) barrier shades the new value $v$, and a [snapshot-at-the-beginning](/snapshot-at-the-beginning/) barrier shades the overwritten value. [Reference counting](/reference-counting/) uses it to adjust the counts. The name has nothing to do with a memory fence: a write barrier in this sense orders no memory accesses, it adds collector bookkeeping.

## In plain words

The program and the collector share the heap. The collector keeps some notes about the heap, for example which old objects point to new ones, or which objects it has already checked. When the program stores a pointer, those notes can become wrong.

So each time the program stores a pointer, it runs a few extra steps first or after. The steps are short: compare two addresses, set a byte, or add an item to a list. They keep the notes of the collector true, so that the collector never throws away an object that is still in use. Different collectors need different steps, but the place where the steps go is the same: next to each store of a pointer.

## When it applies

- **Part of the heap is collected without a scan of the rest.** A minor collection, a region of [Garbage-First](/garbage-first-collector/), a car of the [train algorithm](/train-algorithm/) or an increment of [Beltway](/generational-collector-beltway/): pointers into the collected part from the rest must be known. The barrier records them.
- **The mutator runs while the collector marks.** In [incremental](/incremental-garbage-collection/) and [concurrent](/concurrent-garbage-collection/) collection, a store can hide a white object behind a black one. The barrier prevents this.
- **The collector counts references.** Every store changes two counts, the one of the new target and the one of the old target.
- **The runtime controls every store.** All stores of pointers must go through the barrier, including those in the runtime, in native code that the runtime calls, and in bulk copies of arrays. A [conservative](/conservative-garbage-collection/) collector for C has no such control, and must use the page protection of the operating system instead.

## The template

The barrier wraps the store. Its *before* part sees the old value $u$ of the slot, and its *after* part sees the new value $v$. The holes are the two actions.

```pseudo id=main
WRITE(o, i, v)                       ▷ replaces each pointer store o.f[i] ← v
L1  u ← o.f[i]                       ▷ read only if the before part needs it
L2  BEFORE(o, i, u, v)
L3  o.f[i] ← v
L4  AFTER(o, i, u, v)

THE ACTIONS OF THE COMMON BARRIERS
L5  generational:        after:  if o is old and v is young then add (o, i) to the remembered set
L6  card marking:        after:  card[address of o.f[i] >> k] ← DIRTY
L7  incremental update:  after:  if marking and v is white then shade v
L8  snapshot (SATB):     before: if marking and u is white then shade u
L9  reference counting:  before: if v ≠ nil then count[v] ← count[v] + 1
L10                      after:  if u ≠ nil then decrement count[u], and free u if it reaches 0
```

**Walk-through.** Line L5 is the filtering barrier of Ungar's generation scavenging: it records only the stores that create old-to-young pointers. Line L6 is the card marking barrier: no test, one shift and one byte store. Line L7 is the barrier of Dijkstra, Lamport and others: a pointer stored into a black object can never point to a white one, because the white target turns gray. Line L8 is Yuasa's deletion barrier: each object that was reachable when the marking started stays found, because a pointer that the mutator deletes is shaded first. Lines L9 and L10 increment before they decrement, so that a store of a pointer into the slot that already holds it does not free the object.

A barrier is split into a *fast path*, inlined at each store, and a *slow path*, a call. For the generational barrier the fast path is the test "old source, young value", and the slow path records the slot; for the SATB barrier the fast path is the test "marking is active", and the slow path appends $u$ to a buffer.

### Example

The lost object problem shows why a concurrent marker needs a barrier. Objects $a$ and $b$ are roots; $b.f_0$ points to $c$. The marker scans $a$ (black), and $b$ is gray, $c$ white. Now the mutator does three things: it loads $c$ from $b.f_0$ into a register, stores $c$ into $a.f_0$, and stores nil into $b.f_0$. Then it drops the register. Now $c$ is reachable only from the black object $a$, which the marker does not scan again.

| barrier | what happens at $a.f_0 \gets c$ | what happens at $b.f_0 \gets$ nil | end of marking |
|---|---|---|---|
| none | nothing | nothing | $c$ is white and is freed, $a.f_0$ dangles |
| incremental update (L7) | $c$ becomes gray | nothing | $c$ is marked |
| snapshot (L8) | nothing | $u = c$ becomes gray | $c$ is marked |

The implementation runs this scenario, and also random interleavings of mutator steps and marking steps for both barriers, and checks that no reachable object is freed. With the snapshot barrier it also checks that every object reachable at the start of the marking survives.

### Correctness

Each use of the barrier has its own invariant, and the barrier is what keeps it on a store.

- **Generational.** Every old-to-young slot is in the remembered set. A store is the only mutator action that changes a slot, and line L5 records the slot when the store makes it old-to-young.
- **Incremental update.** No black object points to a white one (the strong tri-color invariant), for the heap; roots are rescanned at the end. A store into a black object $o$ of a white $v$ would break it, and line L7 makes $v$ gray first.
- **Snapshot.** Every white object that was reachable at the start of the marking is reachable from a gray object through white objects (the weak tri-color invariant). Such a path can only break by a store that overwrites one of its pointers, and line L8 shades the target $u$ of that pointer.
- **Reference counting.** The count of each object equals the number of heap slots that point to it. A store removes one pointer to $u$ and adds one to $v$, and lines L9 and L10 do the same to the counts.

### Cost

The barrier adds $O(1)$ work to each pointer store: in the common case a few instructions on the fast path. Its total cost depends on the store rate of the program, and is usually a few percent of the run time. Hoelzle reported that card marking took between 40% and 100% of the total barrier cost in SELF, and that the whole store check cost 0.5% to 8%. Blackburn and Hosking measured several barriers in the same virtual machine and found the common generational write barriers cheap on average, with a larger spread between processors. The work moves between the barrier and the collector: a filtering barrier does more at each store and leaves less for the collection, and an unconditional card barrier does the opposite.

## Classic examples

- **Generation scavenging (Ungar, 1984)**, with a filtering barrier and an object remembered set: [remembered set](/remembered-set/).
- **Card marking (Sobalvarro 1988, Wilson and Moher 1989, Hoelzle 1993)**, the unconditional byte store: [card marking](/card-marking/).
- **On-the-fly marking (Dijkstra et al., 1978)**, with the incremental update barrier: [incremental update barrier](/incremental-update-barrier/).
- **Yuasa's real-time snapshot collector (1990)**, with the deletion barrier: [snapshot at the beginning](/snapshot-at-the-beginning/). Garbage-First and Shenandoah use SATB barriers for their concurrent marking.
- **Reference counting**, and the deferred form that does not count stores into roots: [reference counting](/reference-counting/), [deferred reference counting](/deferred-reference-counting/).

## Variations

- **Filtering or unconditional.** Test the source and target before recording, or record every store and filter later. The first makes the barrier slower and the collection faster.
- **Boundary barriers.** With generations at fixed address ranges, "old source, young value" is one comparison of addresses. Beltway records a pointer only if its target is collected before its source.
- **Barriers in hardware or the virtual memory system.** Write-protect the old generation and catch the first store to each page in a fault handler, or read the dirty bits of the pages. There is no code at each store, but the grain is a page.
- **Combined barriers.** A concurrent generational collector runs both a generational action and a marking action in one barrier. Garbage-First, for example, has an SATB part before the store and a card part after it.
- **Eliding barriers.** A compiler can drop the barrier on a store into an object that was just allocated in the young generation, or on a store of nil with a generational barrier, when it can prove the action has no effect.

## Pitfalls

- **Stores that bypass the barrier.** Array copies, reflection, unsafe operations, native code and the runtime's own code all store pointers. One missing barrier is enough to free a live object.
- **Barrier and store out of order.** With threads, the collector can see the store before the action, or the action before the store. The order must match what the collector assumes. A card barrier, for example, must make the card dirty visible no later than the end of the collector's handshake.
- **Forgetting the roots.** Stores into registers and stack slots usually have no barrier. An incremental update collector must rescan the roots at the end of marking; a snapshot collector must take the snapshot of the roots at the start.
- **Confusing it with a memory fence.** A hardware memory barrier orders loads and stores between processors. A GC write barrier is bookkeeping code. A concurrent collector can need both.
- **Cost in hot loops.** A barrier on every store of a tight loop can matter. Measure before choosing a heavier barrier for a simpler collector.

## Exercises

1. In the example table, which barrier keeps more floating garbage if the mutator had then also stored nil into $a.f_0$ before the end of the marking?
2. Show that the reference counting barrier frees a live object if line L10 runs before line L9 and $u = v$.
3. Write the barrier for a collector with three generations, which records every pointer from an older generation into a younger one, using one comparison when generations occupy increasing address ranges.

## References
