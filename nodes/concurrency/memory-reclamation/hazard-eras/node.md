---
tag: D8CRRV
kind: algorithm
slug: hazard-eras
name: Hazard eras
aliases: [hazard eras reclamation]
area: concurrency/memory-reclamation
level: advanced
summary: Like hazard pointers, but a reader publishes the era of a global clock instead of a pointer, and writes again only when the clock moves. A node is freed when no published era lies in its lifetime.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, K: the era slots per process, R: the retire list length that starts a scan, L: the most nodes alive in one era}
  space: {slots: Θ(n K), garbage: O(n (R + n K L))}
  steps: {protect_stable_clock: O(1), scan: O(n K + R)}
properties: {robust: true, bounded_garbage: true, per_node_cost: true, needs_store_load_fence: true}
history:
  year: 2017
  people: [Pedro Ramalhete, Andreia Correia]
  note: Ramalhete and Correia presented hazard eras as a brief announcement at SPAA 2017. Wen and others built interval-based reclamation on the same idea in 2018.
prereqs: [hazard-pointers, epoch-based-reclamation]
see_also: [interval-based-reclamation, hyaline, pass-the-buck, debra, neutralization-based-reclamation, safe-memory-reclamation]
sources:
  - paper: doi:10.1145/3087556.3087588
    title: Pedro Ramalhete and Andreia Correia, Brief announcement, hazard eras, non-blocking memory reclamation, SPAA 2017
    locator: the whole announcement, with the era clock, the birth and retire eras of a node, get_protected with its re-read of the clock, and the test that frees a node when no published era lies in its lifetime
  - paper: doi:10.1145/3178487.3178488
    title: Haosen Wen, Joseph Izraelevitz, Wentao Cai, H. Alan Beadle and Michael L. Scott, Interval-based memory reclamation, PPoPP 2018, pages 1-13
    locator: the related-work account of hazard eras, and Section 3, which extends the era slot to an interval of eras
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: Section 3, the hazard pointer method whose slots, retire lists and scans hazard eras keep
---

Hazard eras are a [safe memory reclamation](/safe-memory-reclamation/) method by Pedro Ramalhete and Andreia Correia that keeps the shape of [hazard pointers](/hazard-pointers/) but publishes time instead of addresses. A global era clock moves forward when nodes are retired. Each node records the era in which it was allocated and the era in which it was retired. Before a process uses a pointer, it publishes the current era in one of its slots; it needs a new write only when the clock has moved since its last one. A retired node is freed when no published era lies between its birth and its retirement. Most reads cost no shared write, and a stopped process can hold back only the nodes that were alive in the few eras it published.

## In plain words

A museum has a big clock that ticks each time an exhibit is removed. Every exhibit has a card with the tick when it arrived and the tick when it was removed.

When you walk in, you write the current tick on your own badge. While the clock does not tick, you can look at anything without writing again. If it ticks, you write the new number before you look further.

An old exhibit goes to the scrap yard only when no badge shows a number between its arrival and its removal. Nobody who could have seen it is still looking.

A visitor who falls asleep keeps only the exhibits of their own few ticks.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for lock-free structures such as the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/). Hazard pointers bound the garbage but need a write and a fence for every node a reader visits. [Epoch-based reclamation](/epoch-based-reclamation/) costs nothing per node but has no bound when a thread stalls. Hazard eras want the bound of the first at close to the cost of the second.

The model: $n$ asynchronous processes on a sequentially consistent shared memory with reads, writes and [compare-and-swap](/compare-and-swap/). $C$ is the era clock. Each process has $K$ single-writer slots $HE[p][0..K-1]$ that all processes read. Each node $x$ stores its birth era $b_x$, set at allocation, and gets a retire era $r_x$. $R$ is the retire list length that starts a scan.

## The algorithm

```pseudo id=main
PROTECT(i, src)                      ▷ prev is the era this process last wrote in slot i
L1  p ← src
L2  e ← C
L3  if e = prev then return p        ▷ the clock did not move: p is covered
L4  HE[me][i] ← e; prev ← e; goto L1
RETIRE(x)                            ▷ x is unlinked; b_x was set from C at allocation
L5  r_x ← C; rlist ← rlist ∪ {x}
L6  CAS(C, r_x, r_x + 1)             ▷ move the clock on
    if |rlist| ≥ R then SCAN()
SCAN()
L7  eras ← { HE[q][j] ≠ nil : all q, j }
L8  for each x in rlist: if some h in eras has b_x ≤ h ≤ r_x then keep x
L9      else remove x from rlist and FREE(x)
CLEAR()                              ▷ at the end of each operation
L10 HE[me][j] ← nil for every j
```

The validation is the same idea as in hazard pointers, applied to the clock instead of the source pointer. If the clock reads the published era $e$ after the pointer $p$ was read, then the clock was $e$ when $p$ was read, so $p$ was born in era $e$ or before, and it was still linked, so it will be retired in era $e$ or later. Its lifetime contains $e$, and every scan that could free it sees $e$ in the slot.

In a traversal, a process can read many nodes in a row with the same era in the slot and no new write: L1 to L3 are plain reads. This is where the method gains over hazard pointers. It writes again only when some process has retired a node in the meantime.

The clock moves at each retire here. The paper leaves the rate open; moving the clock less often makes eras longer, which means fewer writes in PROTECT but more nodes alive in each era and so more garbage held by a stopped process.

## Example

A stack $top \to A \to B$, two processes, $K = 2$, $R = 1$. Both nodes were born in era 1, and $C = 1$. Process $p$ pops once and process $q$ pops twice. This is the run that breaks the version without the check at L3.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1 | reads $top = A$ | |
| 2 | $q$ | L1 to L4, L1 to L3 | publishes era 1, reads $top = A$ again, $C = 1$, returns $A$ | $HE[q][0] = 1$ |
| 3 | $q$ | pop, L5, L6 | CAS $top$ to $B$; $r_A = 1$; CAS $C$ from 1 to 2 | $C = 2$ |
| 4 | $q$ | L7 to L9 | its own slot holds 1, which lies in $[1, 1]$: keeps $A$ | |
| 5 | $q$ | L10 | clears its slots | |
| 6 | $q$ | pop | publishes era 2, pops $B$: $r_B = 2$, $C = 3$; the scan sees eras $\{2\}$, frees $A$, keeps $B$ | $A$ is freed |
| 7 | $p$ | L2 | reads $C = 3$ | |
| 8 | $p$ | L3, L4 | $3 \ne$ nil, so it writes $HE[p][0] = 3$ and goes back to L1 | |
| 9 | $p$ | L1 to L3 | reads $top =$ nil, $C = 3$: the stack is empty | $p$ returns empty |

Without the loop, $p$ would publish era 3 at step 8 and use $A$, whose lifetime $[1, 1]$ does not contain 3; the scan at step 6 was right to free it. The test finds this use after free.

## Correctness

The full proof is in proofs/correctness.md. It assumes the client rules of hazard pointers: access a node only after PROTECT returned it and while the slot is unchanged, retire once after the unlink, and do not link a retired node again.

- **Key fact.** If PROTECT returns $x$ with era $e$, the slot held $e$ since before $x$ was read, and $b_x \le e \le r_x$. A scan that frees $x$ reads the slot after the retire and sees $e$, so it keeps $x$.
- **Safety.** No process accesses a freed node, and no node is freed twice.
- **Bound.** If at most $L$ nodes are alive in one era, each list holds at most $R + nKL$ nodes, and a stopped process holds back at most $KL$ nodes of the others.

The test file checks every interleaving of a small stack run and a small queue run, 60 seeded random runs of each kind with $R = 1$ and with $R = 2nK$, the use after free without the re-check of the clock and with an immediate free, and the garbage under a stall.

## Complexity

| measure | value |
|---|---|
| shared space | $nK$ slots and the clock; two eras per node |
| PROTECT, clock unchanged | 2 reads, no write |
| PROTECT, clock moved | one more write and fence, then 2 reads |
| RETIRE | 2 steps, plus a scan every $R$ retires |
| SCAN | $O(nK + R)$ steps with $nK$ small, or with the eras sorted |
| unfreed nodes | at most $n (R + nKL)$ |

**Garbage under a stall.** The test runs three processes with $K = 2$ and $R = 12$, with process 0 stopped inside its first pop and the others doing 50 or 400 operations. The peak is 23 or 24 over all runs. The proved bound needs $L$; in this workload at most $4 + 3 \cdot 3 = 13$ nodes are alive in one era (the four initial ones, plus one being pushed and one being popped per process), which gives $n(R + nKL) = 270$, and the test checks the tighter $nR + nKL = 114$, in which only the stopped process holds an era for long. Under [epoch-based reclamation](/epoch-based-reclamation/) the same run keeps all 400 nodes.

## Properties

- Robust: a stopped process holds back only the nodes whose lifetimes contain its published eras.
- The bound depends on how many nodes live in one era, unlike hazard pointers, where it depends only on $n$, $K$ and $R$.
- Most reads cost two plain loads; a write and a fence are needed only when the clock moved.
- PROTECT is lock free; RETIRE and SCAN are wait free.
- Each node carries two extra words for its eras.
- The same client discipline as hazard pointers: the code must say which pointers it holds.

## Variants and improvements

- **[Interval-based reclamation](/interval-based-reclamation/).** Wen and others (2018) publish an interval of eras per thread instead of one era per slot. In the two-global-epoch version (2GEIBR), a thread needs only two shared words.
- **Wait-free eras.** Nikolaev and Ravindran (PPoPP 2020, WFE) make PROTECT wait free by letting threads that advance the clock help a reader that keeps failing its check.
- **[Hyaline](/hyaline/).** Nikolaev and Ravindran (2019 and 2021) use the birth era in the same way in Hyaline-S, but count references to batches of retired nodes instead of scanning slots.
- **[Hazard pointers](/hazard-pointers/).** The pointer version: a tighter bound, but a write per node.

## When to use it

Use hazard eras when you need the robustness of hazard pointers but readers traverse long chains of nodes, such as linked lists, skip lists and trees, and the per-node fence of hazard pointers is too slow. The clock must move often enough that few nodes share an era; if the structure allocates many nodes between two retirements, the garbage of a stalled thread can be large.

## Pitfalls

**No re-check of the clock.** The wrong code reads the pointer at L1, writes the era at L4, and returns. The era written may be later than the retirement of the node, so it does not cover it. The right code loops until the clock read at L2 equals the era already in the slot.

**Publishing before the read, without the loop.** Writing the era first and then reading the pointer once also fails: the node read may be born after the published era. The loop at L1 to L4 handles both orders.

**Wrong birth era.** The birth era must be read from $C$ before the node is allocated and stored in it. A birth era set later than the first time the node can be linked lets a scan free a node that a reader with an earlier era holds.

**Clock overflow.** A 32-bit clock that moves on every retire wraps after about four billion retires; then lifetimes compare wrongly. Use a 64-bit clock.

## Implementations

## History

Pedro Ramalhete and Andreia Correia presented hazard eras as a brief announcement at SPAA 2017, as a way to keep the bound of hazard pointers while cutting the cost of the per-node publication. Wen, Izraelevitz, Cai, Beadle and Scott generalized the idea to interval-based reclamation at PPoPP 2018, and Nikolaev and Ravindran built wait-free eras (2020) and Hyaline-S (2019, 2021) on it.

## References
