---
tag: NRZ4EB
kind: algorithm
slug: xjoin
name: XJoin
aliases:
- XJoin algorithm
area: databases/stream-and-incremental-processing
level: advanced
summary: "A symmetric hash join for unreliable sources that spills partitions to disk and joins them while inputs are blocked."
solves: [relational-join]
model: word-ram
complexity:
  vars: {n: the number of input tuples, M: the memory limit in tuples, T: the number of output tuples, h: the number of stage 2 runs}
  time: {worst: "O(n^2 h^2)", average: "O(n h + T h^2)", best: "O(n + T)"}
  space: {extra: "O(M)"}
properties: {deterministic: true, exact: true, online: true, external: true, in_place: false, recursive: false}
history:
  year: 2000
  people: [Tolga Urhan, Michael J. Franklin]
  note: "Urhan and Franklin designed XJoin for queries over remote sources on a wide-area network, where inputs arrive in bursts and stall."
prereqs: [symmetric-hash-join, grace-hash-join]
see_also: [symmetric-hash-join, hash-join, grace-hash-join, hybrid-hash-join, sliding-window-join, ripple-join, eddies, pipelining-and-materialization]
sources:
  - paper: "Tolga Urhan and Michael J. Franklin, XJoin, a reactively-scheduled pipelined join operator, IEEE Data Engineering Bulletin 23(2), 2000, 27 to 33"
    title: "XJoin: a reactively-scheduled pipelined join operator"
    locator: "the three stages of XJoin, the arrival and departure timestamps, and the history list of stage 2 runs for duplicate avoidance"
  - paper: "Zachary G. Ives, Daniela Florescu, Marc Friedman, Alon Levy and Daniel S. Weld, An adaptive query execution system for data integration, Proceedings of ACM SIGMOD 1999"
    title: An adaptive query execution system for data integration
    locator: "the pipelined hash join of the Tukwila system and its strategies for memory overflow, the closest earlier design (the page numbers are not confirmed here)"
  - paper: "Annita N. Wilschut and Peter M. G. Apers, Dataflow query execution in a parallel main-memory environment, Proceedings of the First International Conference on Parallel and Distributed Information Systems (PDIS), 1991"
    title: Dataflow query execution in a parallel main-memory environment
    locator: the pipelining hash-join that XJoin extends (the page numbers are not confirmed here)
---

XJoin is a pipelined equi-join for inputs that arrive over a network at unpredictable rates and that may not fit in memory. It is a [symmetric hash join](/symmetric-hash-join/) whose two hash tables are split into partitions, as in the [Grace hash join](/grace-hash-join/): when memory is full, a partition moves to disk, and the join of the disk parts is done later, partly while both inputs are blocked and partly at the end. The symmetric hash join has no such memory limit, and a [hash join](/hash-join/) blocks until one input is complete. Timestamps on each tuple make sure that no result pair is emitted twice, although a pair can be met in memory, in a later disk run and again at the end.

## In plain words

You are matching two piles of letters that the post brings in at random times. You keep two trays, each with a few slots, and you match a new letter with the letters in the other tray at once. When the trays are full, you put the contents of the fullest slot into a box in the cellar and write the time on each letter.

When no post comes for a while, you do not wait. You fetch one box from the cellar and match its letters with what is now in the trays. You note the time of this visit on the box. At the end of the day you match everything that is left. Before you write a match down, you check the times on both letters and on the box. They tell you if you have written this match down before.

## The problem

The input is two relations $R$ and $S$ with the set $J$ of common attributes, delivered as a sequence of arrivals from either input. Between arrivals there can be long stalls. The output is the natural join $R \bowtie S$ on $J$ under bag semantics, as on the page [relational join problem](/relational-join/), with NULL keys never matching. Memory holds at most $M$ tuples. The join must emit results as early as it can, never emit a result twice, and emit all results by the end of both inputs.

There are three goals at once. A blocking join gives no early results. A plain symmetric hash join fails when memory is full. A join that spills to disk and joins the disk parts later can meet the same pair twice, once in memory before a spill and once from disk afterwards.

## The algorithm

Both inputs are hashed into $P$ partitions on the join key with one hash function $h$. Each partition of each input has a memory part and a disk part. Each stored tuple carries its arrival time $\mathrm{ATS}$ and its departure time $\mathrm{DTS}$, the time at which it moved to disk, or $\infty$ while it is in memory. Each disk part keeps a *history*: the list of times at which stage 2 used it. One logical clock gives all times.

```pseudo id=main
XJOIN(events, P, M)                    ▷ events: arrivals of R or S tuples, and "blocked" signals
L1  for each input X and partition p: mem[X][p] ← ∅; disk[X][p] ← ∅; hist[X][p] ← ∅; clock ← 0
L2  for each event e, in order do
L3      clock ← clock + 1
L4      if e is the arrival of tuple t on input X then                           ▷ stage 1
L5          if t[J] has no NULL then p ← h(t[J]); t.ATS ← clock; t.DTS ← ∞; add t to mem[X][p]
L6              for each u in mem[Y][p] with u[J] = t[J] do emit (t, u)          ▷ Y is the other input
L7              if memory holds more than M tuples then clock ← clock + 1; move the largest memory part to disk, with DTS ← clock
L8      else if e says that both inputs are blocked then                          ▷ stage 2
L9          choose an input X and a partition p with disk[X][p] not empty; pt ← clock
L10         for each a in disk[X][p] and b in mem[Y][p] with a[J] = b[J] do
L11             if not DONE(a, b) then emit (a, b)
L12         append pt to hist[X][p]
L13 for each p, each a in mem[R][p] ∪ disk[R][p] and b in mem[S][p] ∪ disk[S][p] with a[J] = b[J] do     ▷ stage 3
L14     if not DONE(a, b) then emit (a, b)

DONE(x, y)                             ▷ true if the pair was emitted before
L15 if x.ATS < y.DTS and y.ATS < x.DTS then return true                          ▷ both were in memory together
L16 for each (u, v) in ((x, y), (y, x)) and each pt in the history of the disk part of u do
L17     if u.DTS < pt and v.ATS < pt < v.DTS then return true                    ▷ u on disk and v in memory at pt
    return false
```

**Stage 1** (lines L4 to L7) is the symmetric hash join on the memory parts. **Stage 2** (lines L8 to L12) uses the time in which the join would otherwise wait: it reads one disk part and probes the memory part of the same partition of the other input. **Stage 3** (lines L13 and L14) runs once both inputs have ended, and joins everything, in memory and on disk, that is not yet done.

The test of line L15 is exact for stage 1: two tuples met in memory if and only if their memory intervals $[\mathrm{ATS}, \mathrm{DTS})$ overlap. The test of line L17 is exact for a stage 2 run at time $pt$: that run met exactly the pairs with one tuple already on disk and the other in memory at $pt$. So DONE needs no list of emitted pairs, only two numbers per tuple and one list per disk part.

Two choices are heuristics and do not affect correctness: which memory part goes to disk at line L7 (here the largest, which frees the most memory), and which disk part stage 2 uses at line L9 (here the largest). In the original operator, stage 2 also stops as soon as new input arrives, and it starts only when it is expected to produce enough new results. The code on this page runs one whole disk part for each "blocked" event.

## Example

$R(A, B)$ and $S(B, C)$ join on $B$, with one partition ($P = 1$) and memory for $M = 3$ tuples. All tuples have $B = 10$, so the join has $4 \cdot 3 = 12$ results. $R$ tuples are named by $A$, and $S$ tuples by $C$.

| time | event | what happens | emitted |
|---|---|---|---|
| 1 | $R$: 1 | memory {1} | none |
| 2 | $S$: p | stage 1 meets 1 | (1, p) |
| 3 | $R$: 2 | stage 1 meets p | (2, p) |
| 4, 5 | $R$: 3 | stage 1 meets p; memory holds 4 tuples, so at time 5 the $R$ part {1, 2, 3} moves to disk with DTS 5 | (3, p) |
| 6 | blocked | stage 2: disk {1, 2, 3} against memory {p}. All three pairs pass line L15 (p.ATS = 2 < 5), so they are skipped. History of the $R$ disk part: [6] | none |
| 7 | $S$: q | memory of $R$ is empty | none |
| 8 | blocked | stage 2: disk {1, 2, 3} against memory {p, q}. The pairs with q fail line L15 (q.ATS = 7 > 5) and the entry 6 (7 > 6). History: [6, 8] | (1, q), (2, q), (3, q) |
| 9 | $R$: 4 | stage 1 meets p and q | (4, p), (4, q) |
| 10, 11 | $S$: s | stage 1 meets 4; at time 11 the $S$ part {p, q, s} moves to disk with DTS 11 | (4, s) |
| 12 | end | stage 3: of the 12 pairs, only the pairs of s with 1, 2 and 3 pass no test (s.ATS = 10 is after DTS 5 and after both history entries) | (1, s), (2, s), (3, s) |

Stage 1 emits 6 results, stage 2 emits 3 and stage 3 emits 3, for 12 in total, each once. Six tuples go to disk. Without the tests of DONE, the stage 2 run at time 6 would emit (1, p), (2, p) and (3, p) a second time.

## Correctness

The claim is that each result pair is emitted exactly once, and that every emitted tuple is a result of the inputs that have arrived. The clock gives distinct times to arrivals, moves to disk and stage 2 runs. A tuple is in memory exactly between its $\mathrm{ATS}$ and its $\mathrm{DTS}$ and never comes back from disk, so line L15 is true exactly for the pairs that stage 1 met, and line L17 for an entry $pt$ is true exactly for the pairs that the run at $pt$ met. These values do not change later. So DONE returns true exactly for pairs that were met before, each pair is emitted at its first meeting, and stage 3 emits the pairs that were never met. Memory never holds more than $M$ tuples after an event, because a move frees at least one tuple. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/) model, with $n$ input tuples, $T$ results, $h$ stage 2 runs and expected $O(1)$ hash table operations. A real system would also count the disk part reads in pages, as in the [external memory model](/external-memory-model/).

- **Stage 1** costs expected $O(1 + m)$ per arriving tuple, where $m$ is the number of results it emits, as in the symmetric hash join. A move to disk writes each tuple at most once, so all moves together write at most $n$ tuples.
- **Stage 2** reads one disk part per run, at most $n$ tuples, so all runs read $O(n h)$ tuples. Each pair that a run meets costs one call of DONE.
- **DONE** costs $O(1 + h_p)$, where $h_p \le h$ is the length of the history of the part. A pair can be met at most $h + 2$ times: in stage 1, in stage 2 runs and in stage 3. So the expected total is $O(n h + T h^2)$. With no overflow, nothing goes to disk, every history is empty, and the cost is $O(n + T)$. The worst case, when all keys collide in one bucket, is $O(n^2 h^2)$.
- **Memory** is at most $M$ tuples plus the history lists. Disk holds at most $n$ tuples.

These are worst case bounds over the arrival order, in expectation over the hash function. They are not amortized.

## Properties

- **Pipelined.** Stage 1 emits results as fast as a symmetric hash join while memory lasts.
- **Reactive.** Stage 2 runs only when both inputs are blocked, so the time that a remote source stalls is used to produce results.
- **Exact under bag semantics.** Every result is emitted once, even with duplicate tuples, because DONE is about occurrences, not values.
- **Bounded memory.** At most $M$ tuples in memory after each event. A plain symmetric hash join needs all $n$.
- **Order of results.** The final output does not depend on the heuristics or on the arrival order, but the time at which each result appears does.

## Variants and improvements

- **Tukwila.** Ives et al. (1999) used a symmetric hash join in the Tukwila data integration system and gave strategies for memory overflow that move partitions of one or both inputs to disk. XJoin adds the use of blocked time and the timestamp test.
- **Choice of the part to move and to read.** The policies at lines L7 and L9 are heuristics. Any other policy keeps the output correct, because the proof does not use them, so a system can tune them to its workload.
- **Windows.** On unbounded streams, the [sliding window join](/sliding-window-join/) drops expired tuples instead of moving them to disk.
- **Outside streams.** XJoin is a general pipelined join for any plan with slow or bursty inputs, such as federated and distributed queries. It also gives early results for [online aggregation](/ripple-join/) and adaptive plans such as [eddies](/eddies/).

## When to use it

Use it for an equi-join of two inputs that arrive slowly or in bursts, when the user wants early results and the inputs may not fit in memory. If both inputs are on local disk, a [Grace hash join](/grace-hash-join/) or a [hybrid hash join](/hybrid-hash-join/) does less work. If both inputs fit in memory, a [symmetric hash join](/symmetric-hash-join/) is simpler.

## Pitfalls

- **Duplicates.** A pair met in memory can be met again when its tuples are on disk. A test that checks only the stage (for example, "stage 3 joins only disk with disk") misses pairs or repeats them. Use the timestamps of both tuples and the history of the disk part.
- **Equal times.** The tests need strict inequalities between distinct times. If a move to disk shares its time with the arrival that caused it, a pair met at that arrival can fail line L15. The pseudocode gives the move its own clock tick.
- **Stage 2 too often.** Reading a whole disk part to find few new results wastes I/O. The original operator uses a threshold before it starts stage 2, which is a heuristic.
- **Late data.** XJoin has no windows and no watermarks: it waits for the end of both inputs, so a tuple that arrives late is still joined with everything. It handles delayed input, not out-of-order event times. A windowed stream join must decide separately how long to keep tuples for late data.

## Implementations

## History

Urhan and Franklin designed XJoin for queries over remote sources on a wide-area network, where the delays of a source are not known in advance and a source can stall for a long time. Their Data Engineering Bulletin paper of 2000 gives the three stages and the timestamp method. XJoin builds on the symmetric hash join of Wilschut and Apers (1991) and on the Tukwila work of Ives et al. (1999), which used a symmetric hash join for data integration and dealt with memory overflow.

## References
