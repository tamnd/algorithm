---
tag: 8KPT1J
kind: algorithm
slug: interval-based-reclamation
name: Interval-based reclamation
aliases: [IBR, 2GEIBR]
area: concurrency/memory-reclamation
level: advanced
summary: Each thread reserves an interval of epochs for its operation. A retired node is freed when its lifetime, from birth epoch to retire epoch, meets no reserved interval.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, R: the retire list length that starts a scan, L: the most retired nodes whose lifetime meets one reserved interval}
  space: {reservations: Θ(n), garbage: O(n (R + n L))}
  steps: {protect_stable_epoch: O(1), scan: O(n + R)}
properties: {robust: true, bounded_garbage: true, per_node_cost: false, needs_store_load_fence: true}
history:
  year: 2018
  people: [Haosen Wen, Joseph Izraelevitz, Wentao Cai, H. Alan Beadle, Michael L. Scott]
  note: Wen and others presented interval-based reclamation at PPoPP 2018, with the two-global-epoch version 2GEIBR and the tagged versions TagIBR and POIBR.
prereqs: [hazard-eras]
see_also: [hazard-pointers, epoch-based-reclamation, hyaline, debra, neutralization-based-reclamation, safe-memory-reclamation]
sources:
  - paper: doi:10.1145/3178487.3178488
    title: Haosen Wen, Joseph Izraelevitz, Wentao Cai, H. Alan Beadle and Michael L. Scott, Interval-based memory reclamation, PPoPP 2018, pages 1-13
    locator: Section 3, the 2GEIBR algorithm with the birth and retire epochs of a node, the lower and upper reservation of a thread, the read that raises the upper end, and the test that frees a node whose lifetime meets no reservation
  - paper: doi:10.1145/3087556.3087588
    title: Pedro Ramalhete and Andreia Correia, Brief announcement, hazard eras, non-blocking memory reclamation, SPAA 2017
    locator: the birth and retire eras of a node and the clock re-check that interval-based reclamation reuses
---

Interval-based reclamation (IBR) is a [safe memory reclamation](/safe-memory-reclamation/) method by Wen, Izraelevitz, Cai, Beadle and Scott. A global epoch moves forward as nodes are allocated. Each node records the epoch of its birth and the epoch of its retirement. Each thread reserves one interval of epochs: the lower end is the epoch at the start of its operation, and each pointer read raises the upper end to the current epoch. A retired node is freed when its lifetime meets no reserved interval. This page implements the two-global-epoch version, 2GEIBR, in which a thread needs only two shared words and a read costs two plain loads while the epoch does not move. A stopped thread holds back only the nodes whose lifetimes meet its interval, so the garbage stays bounded.

## In plain words

A library has a big counter that goes up now and then when new books arrive. Each book has a card with the number when it arrived and the number when it was taken off the shelf.

When you start reading, you write the counter on your badge twice, as "from" and "to". Each time you take a book, you look at the counter. If it moved, you change the "to" number first.

A book that was taken off the shelf goes to the shredder only when no badge has a "from" to "to" range that overlaps its card. Then nobody who started reading while it was on the shelf is still reading.

A reader who falls asleep keeps only the books of their own range.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for lock-free structures such as the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/). [Hazard pointers](/hazard-pointers/) and [hazard eras](/hazard-eras/) bound the garbage, but a thread must say which pointers it holds, one slot each. [Epoch-based reclamation](/epoch-based-reclamation/) needs no slots, but a stalled thread blocks all reclamation. IBR wants the interface of epochs, where a thread only marks the start and end of an operation, with the bound of hazard eras.

The model: $n$ asynchronous processes on a sequentially consistent shared memory with reads, writes, fetch-and-add and [compare-and-swap](/compare-and-swap/). $E$ is the global epoch. Each process has one single-writer reservation $Res[p]$, a pair $[lo, up]$ or nil, that all processes read. Each node $x$ stores its birth epoch $b_x$ and gets a retire epoch $r_x$. Every $F$-th allocation of a process adds 1 to $E$ first. $R$ is the retire list length that starts a scan.

## The algorithm

```pseudo id=main
BEGIN()
L1  e ← E
L2  Res[me] ← [e, e]; lo ← e; up ← e
PROTECT(src)                         ▷ every pointer read in the operation
L3  p ← src
L4  e ← E
L5  if e = up then return p          ▷ the epoch did not move: p is covered
L6  Res[me] ← [lo, e]; up ← e; goto L3
END()
L7  Res[me] ← nil
RETIRE(x)                            ▷ x is unlinked; b_x was read from E at allocation
L8  r_x ← E; rlist ← rlist ∪ {x}; if |rlist| < R then return
L9  res ← { Res[q] ≠ nil : all q }
L10 for each x in rlist: if some [lo', up'] in res has b_x ≤ up' and r_x ≥ lo' then keep x
L11     else remove x from rlist and FREE(x)
```

The re-check at L4 and L5 is the one of hazard eras, applied to the upper end of the interval. If $E$ still equals $up$ after the pointer was read, then $E$ was $up$ when the pointer was read, so the node was born at or before $up$, and it was still linked, so it will be retired at or after $up$. Its lifetime meets $[lo, up]$.

The difference from hazard eras is that the interval only grows during an operation. A node that one PROTECT covered stays covered after later reads, because $lo$ stays and $up$ only goes up. So a thread needs no slot per pointer, and a client written for epochs needs only BEGIN, END and a wrapped read.

The epoch moves at allocations here, as in the paper: each process adds 1 to $E$ at every $F$-th allocation, before it reads the birth epoch. The test uses $F = 1$ for the exhaustive runs and $F = 2$ for the rest.

## Example

A stack that starts empty, two processes, $F = 1$, $R = 1$, $E = 1$. Process $p$ pops once. Process $q$ pushes $a$, pops, pushes $b$ and pops. This is the run that breaks the version that never raises the upper end.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1, L2 | reads $E = 1$, reserves $[1, 1]$ | $Res[p] = [1, 1]$ |
| 2 | $q$ | push | adds 1 to $E$, allocates $a$ with $b_a = 2$, links it | $E = 2$, $top = a$ |
| 3 | $p$ | L3 to L6 | reads $top = a$, reads $E = 2 \ne 1$, reserves $[1, 2]$ | $Res[p] = [1, 2]$ |
| 4 | $p$ | L3 to L5 | reads $top = a$ again, $E = 2$: returns $a$ | |
| 5 | $q$ | pop, L8 to L11 | unlinks $a$, $r_a = 2$; the scan sees $[1, 2]$ and its own $[2, 2]$: keeps $a$ | $top =$ nil |
| 6 | $q$ | push | $E = 3$, $b_b = 3$, links $b$ | $top = b$ |
| 7 | $q$ | pop, L8 to L11 | unlinks $b$, $r_b = 3$; the scan sees $[1, 2]$ and $[3, 3]$: $[2, 2]$ meets $[1, 2]$, so it keeps $a$, and keeps $b$ | |
| 8 | $p$ | pop | reads $a.next$ safely; its CAS fails; it reads $top =$ nil and returns empty | |

Without L6, $p$ keeps $[1, 1]$ at step 3 and uses $a$, whose lifetime $[2, 2]$ does not meet $[1, 1]$. The scan at step 7 frees $a$, and the read at step 8 is a use after free. The test finds this run.

## Correctness

The full proof is in proofs/correctness.md. It assumes that a process accesses a node only in the operation in which PROTECT returned it and only if the node was reachable at that read (the stack reads from the root, and the dequeue checks the head again), retires each node once after its unlink, and does not link a retired node again.

- **Key fact.** When PROTECT returns $x$, the reservation $[lo, up]$ has been in place since before $x$ was read, and $b_x \le up$ and $r_x \ge lo$. The interval only grows until END, so a scan that frees $x$ would read an interval that meets its lifetime and keep it.
- **Safety.** No process accesses a freed node, and no node is freed twice.
- **Bound.** If at most $L$ retired nodes have a lifetime that meets one reserved interval, each list holds at most $R + nL$ nodes. A stopped process with interval $[lo, up]$ holds back only the nodes alive at $lo$ and those born in $[lo, up]$.

The test file checks every interleaving of four small stack runs and one queue run, 60 seeded random runs of each kind with two settings of $R$ and $F$, the use after free above, the use after free with an immediate free, and the garbage under a stall.

## Complexity

| measure | value |
|---|---|
| shared space | two words per process and the epoch; two epochs per node |
| PROTECT, epoch unchanged | 2 reads, no write |
| PROTECT, epoch moved | one more write and fence, then 2 reads |
| BEGIN, END | 2 steps and 1 step |
| RETIRE | 1 step, plus a scan every $R$ retires |
| SCAN | $O(n + R)$ steps |
| unfreed nodes | at most $n (R + nL)$ |

**Garbage under a stall.** The test runs three processes with $R = 6$ and $F = 2$ on a structure with four nodes, with process 0 stopped inside its first pop after it reserved $[1, 1]$, and the others doing 50 or 400 operations. The peak is 11 to 13 over all runs. The stalled interval meets at most the $4 + 3 = 7$ nodes born in epoch 1. The test checks the bound $nR + n(4 + n + 2nF) = 75$, in which the live intervals of the running processes are allowed $n + 2nF$ nodes each; this is a bound for this workload, not a general one. Under [epoch-based reclamation](/epoch-based-reclamation/) the same run keeps all 400 nodes.

## Properties

- Robust: a stopped process holds back only the nodes whose lifetimes meet its interval.
- The interface is that of epochs: BEGIN, END, and a read wrapper. The client does not count its pointers.
- Most reads cost two plain loads; a write and a fence are needed only when the epoch moved.
- PROTECT is lock free; RETIRE and SCAN are wait free.
- Each node carries two extra words for its epochs.
- A long operation grows its interval, so it holds back more nodes than one hazard era would.

## Variants and improvements

- **TagIBR and POIBR.** The paper also has versions that store the birth epoch next to each pointer and update both with a double-width CAS, which makes the reservation follow the pointers more tightly. They are not implemented here.
- **[Hazard eras](/hazard-eras/).** Ramalhete and Correia (2017) publish single eras in $K$ slots per thread instead of one interval.
- **[Hyaline](/hyaline/).** Nikolaev and Ravindran use birth epochs in the same way in Hyaline-S to make reference-counted batches robust.
- **[DEBRA](/debra/) and [NBR](/neutralization-based-reclamation/).** Other ways to make epochs robust, with signals instead of birth epochs.

## When to use it

Use IBR when you have code written for epoch-based reclamation, with clear operation boundaries, and you need a bound on garbage when a thread stalls. It is a good fit for structures with long traversals, such as lists, trees and skip lists, where the per-node writes of hazard pointers are too slow. If operations are very long, the interval of a stalled thread covers many epochs, and the bound becomes weak; then hazard pointers or hazard eras hold back less.

## Pitfalls

**Not raising the upper end.** The wrong code reserves $[e, e]$ at L2 and reads pointers with plain loads, as plain epochs do. A node born after $e$ is then not covered, and a scan frees it while the reader still uses it. The right code checks $E$ at L4 after each pointer read and raises the upper end at L6.

**Lowering the lower end, or clearing the interval in the middle.** The interval must only grow until L7. A thread that writes a new $[e, e]$ in the middle of an operation drops the cover of the nodes it read before.

**Birth epoch read too late.** The birth epoch must be read from $E$ before the node is linked. A birth epoch from after the link lets a scan free a node that a reader with an earlier interval holds.

**An epoch that never moves.** If no process allocates, $E$ stays, and all intervals and lifetimes share one epoch: nothing is freed while any operation runs. Move the epoch at allocation or at retire, at a rate set by $F$.

## Implementations

## History

Haosen Wen, Joseph Izraelevitz, Wentao Cai, H. Alan Beadle and Michael L. Scott presented interval-based reclamation at PPoPP 2018. They built on the birth and retire eras of [hazard eras](/hazard-eras/) by Ramalhete and Correia (2017), and replaced the per-pointer eras by one interval per thread. The paper has three versions, 2GEIBR, TagIBR and POIBR, and compares them with epochs and hazard pointers on lists, hash maps and trees.

## References
