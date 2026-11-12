---
title: With a tax of k units per allocation, the paced collector never runs out of cells
proves: [correctness, complexity]
status: full
---

We use the heap model and the procedures of the page: $H$ cells, at most $L$ reachable cells at each moment, the trigger $F$, and $k$ units of work per allocation. Let $m = \lceil (L + H)/k \rceil$.

**Lemma 1 (safety).** No cell that is reachable is ever put on the free list.

*Proof.* The mark phase is snapshot-at-the-beginning marking: line L7 shades the roots at the start, line L18 shades the old target of each overwritten field, and lines L5 and L6 mark the cells allocated during the mark phase. By the theorem of [snapshot-at-the-beginning](/snapshot-at-the-beginning/), when $W$ becomes empty at line L12, every cell that was reachable when line L7 ran, and every cell allocated since, is marked. During the sweep, a cell allocated at an address $x \ge s$ is marked at line L5, so the sweep does not free it; a cell allocated at $x < s$ has already been passed. A cell that is unmarked when the sweep reaches it was unreachable at line L7 and was not allocated since, so it is unreachable now and forever (a mutator gets references only from cells that it reaches, or by allocation). Line L15 frees only such cells. $\square$

**Lemma 2 (work of one cycle).** One cycle does at most $L + H$ units of work.

*Proof.* A unit is one scan at line L11 or one swept cell at line L16. A cell is pushed on $W$ only when its mark goes from clear to set, so it is scanned at most once. The cells allocated during the mark phase are marked without a push. So the scanned cells are cells that were shaded by line L7 or line L18 and were not allocated in the cycle. Each of them was reachable at some moment of the cycle and existed at line L7; by the argument of Lemma 1 it was reachable at line L7. So there are at most $L$ scans. The sweep visits each of the $H$ cells once. Lines L12 and L17 do no unit of work. $\square$

**Lemma 3 (allocations per cycle).** A cycle ends during at most $m$ allocations after it starts, counting the allocation that starts it.

*Proof.* Each allocation during the cycle runs COLLECT-WORK$(k)$, which does $k$ units unless the cycle ends inside it. By Lemma 2, after $m$ calls at least $mk \ge L + H$ units would be done, which is more than a cycle needs. $\square$

**Theorem.** Assume the heap starts empty, $F \ge m$ and $H \ge L + 2m$. Then no allocation fails at line L3, and every allocation does at most $k$ units of collector work.

*Proof.* The bound on work is the loop condition of line L9. For the first claim, we show that each cycle starts with at least $m$ free cells. A cycle starts at line L1, when the collector is idle and at most $F$ cells are free. Outside a cycle, the free list shrinks by one cell per allocation. So either the count went down to exactly $F \ge m$ at the previous allocation, or the previous cycle ended with fewer than $F$ free cells and the new cycle starts at the next allocation.

In the second case we count the free cells at the end of the previous cycle. The cells in use then are the survivors of the cycle. By Lemma 1 and the snapshot theorem, every cell that is not freed was reachable at the start of that cycle (at most $L$ cells) or was allocated during it (at most $m$ cells, by Lemma 3). So at least $H - L - m \ge m$ cells are free. The first cycle starts with at least $\min(H, F) \ge m$ free cells, since $H \ge L + 2m \ge m$.

During a cycle, cells leave the free list only by allocation, one per allocation, and by Lemma 3 there are at most $m$ allocations before the cycle ends. A cycle that starts with at least $m$ free cells therefore finds a free cell at each of them. After the cycle the collector is idle, and the argument repeats. $\blacksquare$

**The pause.** Each allocation does at most $k$ units, and the start of a cycle shades the $r$ roots in one pause of $r$ steps. So the longest pause is $\max(r, k)$ steps plus the constant work of the allocation and the barrier, independent of $H$ and $L$.

**The condition is sufficient, not necessary.** The proof does not use the cells that the sweep returns during the cycle, so a smaller $k$ often works in practice.
