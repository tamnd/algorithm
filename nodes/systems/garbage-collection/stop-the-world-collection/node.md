---
tag: 07EXF5
kind: concept
slug: stop-the-world-collection
name: Stop-the-world collection
aliases:
- stop-the-world pause
- STW
- stop-the-world garbage collection
area: systems/garbage-collection
level: intro
summary: "The collector stops every mutator thread at a safepoint, does its work while the heap cannot change, and then lets the threads go on. The pause grows with the work done."
prereqs: [mutator-and-collector, tracing-garbage-collection]
see_also: [incremental-garbage-collection, concurrent-garbage-collection, parallel-garbage-collection, on-the-fly-garbage-collection, baker-real-time-collector, gc-roots, precise-garbage-collection, gc-space-time-tradeoff]
sources:
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Section 6.2 (pause time) and Section 11.6 (GC safe-points and mutator suspension)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 8, incremental and concurrent garbage collection, on the pauses of collectors that stop the program
  - paper: Perry Cheng and Guy E. Blelloch, A parallel, real-time garbage collector, Proceedings of PLDI 2001, ACM
    locator: the definition of minimum mutator utilization over a window of time
  - paper: Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, Springer, 1992
    locator: the introduction to incremental collection, on the disruptive pauses of collectors that stop the program
---

A stop-the-world collector pauses every thread of the program, the *mutator*, for the whole of a collection. The collector waits until each thread has stopped at a *safepoint*, a place in the code where the collector can find all of its pointers. Then it does its work while the heap cannot change, and lets the threads go on. This is the simplest way to make a [tracing collector](/tracing-garbage-collection/) correct: no pointer moves while the collector looks, so it needs no barriers. The price is the *pause*: its length grows with the work of the collection, which for a large heap can be long. [Incremental](/incremental-garbage-collection/), [concurrent](/concurrent-garbage-collection/) and [on-the-fly](/on-the-fly-garbage-collection/) collectors exist to make the pauses short.

## In plain words

Picture a cleaner in an office. The easy way to clean is to ask everyone to step out, clean, and let them back in. While the room is empty, nothing moves, so the cleaner cannot make a mistake. But nobody works during that time, and a big office takes a long time to clean.

Before the cleaner starts, each worker must reach a good place to stop, for example finish the sentence they are writing, so that the cleaner can see what is on the desk. This waiting is part of the pause too.

## The idea

**The world and the pause.** The *world* is the set of all mutator threads. A stop-the-world collection has three steps:

1. **Stop.** The collector asks every mutator thread to stop, and waits until all have stopped at a safepoint.
2. **Collect.** The collector scans the [roots](/gc-roots/) of every thread and does its work: marking, sweeping, copying or compacting. One thread or many can do this; a [parallel collector](/parallel-garbage-collection/) uses many, but the world is still stopped.
3. **Resume.** The collector lets all threads go on.

The pause that a thread sees is the time from the request to stop until it resumes.

**Safepoints.** A thread cannot stop at an arbitrary instruction, because there the runtime may not know which registers and stack slots hold pointers. A *safepoint* is a point where it does know, through a stack map made by the compiler. The compiler places safepoint checks on loop back edges and at calls and returns, so that a thread reaches one soon. A check reads a flag, or touches a memory page that the runtime makes unreadable when it wants the threads to stop. A thread that runs native code, or is blocked, holds no heap pointers in unknown places, and counts as stopped. The time that the last thread needs to reach a safepoint, the *time to safepoint*, adds to every pause.

**The pause is proportional to the work.** The collector does all its work inside the pause, so the length of the pause is the cost of one collection. With $r$ roots, $L$ live words and a heap of $H$ words:

| collector | work in the pause |
|---|---|
| [copying](/copying-collection/) | $O(r + L)$ |
| [mark-and-sweep](/mark-and-sweep/) with an eager sweep | $O(r + L + H)$ |
| mark-and-sweep with a [lazy sweep](/lazy-sweeping/) | $O(r + L)$; the sweep moves into allocation |
| [mark-compact](/mark-compact/) | $O(r + H)$ |

So the pause grows with the live data or with the heap. A program with gigabytes of live data can see pauses of seconds. The collection cost per allocated word can be made small by a larger heap (see [the space-time tradeoff](/gc-space-time-tradeoff/)), but the length of each pause cannot: a larger heap makes fewer pauses, not shorter ones.

**Why stop the world.** While the world is stopped, the heap is a fixed graph. The collector needs no [read barrier](/read-barrier/) or [write barrier](/write-barrier/) to keep the [tricolor invariants](/tricolor-marking/), objects can move freely, and the code of the mutator pays nothing between collections. Stop-the-world collectors usually have the best *throughput*, the share of time spent in the program.

**Measuring pauses.** The longest pause and the distribution of pauses are the simple measures. A better measure is the *minimum mutator utilization* (Cheng and Blelloch 2001): for a window length $w$, the smallest share of any window of length $w$ in which the mutator runs. A program that stops for 50 ms once a second has a utilization of $0$ for windows up to 50 ms, $0.5$ for windows of 100 ms, and $0.95$ for windows of 1 s.

**The spectrum.** Between stopping the world for all the work and never stopping it, there are many steps:

- *Parallel*: the world stops, and several collector threads share the work, so the pause is shorter but still proportional to the work.
- *Incremental*: the collector does a little work at a time, in many short pauses, and barriers keep the invariants in between.
- *Mostly concurrent*: the collector runs beside the mutator, and stops the world only for short phases, such as the scan of the roots at the start and the end of marking.
- *On-the-fly*: the collector never stops all threads at once; it stops them one at a time with handshakes.

## Examples

**A copying collection.** Suppose a copying collector copies about 1 GB of live data per second on one thread. A live set of 200 MB then gives a pause of about 0.2 s, whatever the size of the heap. With 4 collector threads and perfect sharing, the pause is about 0.05 s. To make it shorter still, the collector must do some of the work while the program runs.

**Time to safepoint.** One thread runs a long loop with no safepoint check in it, for example a counted loop that the compiler has proved short. When a collection is requested, all other threads stop at once, but they all wait for this one. The pause that every thread sees then includes the length of that loop. This is why compilers put safepoint checks in long loops.

**A short pause in a concurrent collector.** A mostly concurrent marking collector stops the world briefly to scan the roots and start marking, marks the heap while the program runs, and stops the world again briefly to finish marking. Both pauses do work in proportion to the roots, not to the heap.

## Where it is used

- **Simple and batch runtimes.** Many language runtimes start with a stop-the-world mark-and-sweep or copying collector, and keep it when throughput matters more than pauses, as in batch jobs.
- **Throughput collectors.** The serial and parallel collectors of the HotSpot Java virtual machine stop the world for every collection.
- **Young generation collections.** In most [generational collectors](/generational-garbage-collection/), the young generation is copied in a stop-the-world pause, which is short because few young objects survive. The [Garbage-First collector](/garbage-first-collector/) also copies its regions in pauses, and marks concurrently.
- **Phases of concurrent collectors.** Concurrent collectors such as the [Shenandoah](/shenandoah-collector/) and [Z](/z-garbage-collector/) collectors keep short stop-the-world phases, mainly to scan the roots.
- **The baseline.** Incremental and concurrent collectors are judged by how much shorter their pauses are, and how much throughput they give up, compared with a stop-the-world collector.

## References
