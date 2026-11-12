---
title: Gang scheduling with an Ousterhout matrix runs every gang all at once, never puts two threads on one processor, and serves every row in turn
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page with $P$ processors. A gang $g$ has $1 \le \mathit{size}_g \le P$ threads and $\mathit{work}_g \ge 1$ slots of work. PLACE puts the threads $0, \ldots, \mathit{size}_g - 1$ of $g$ into distinct free cells of one row.

**Claim 1 (the matrix).** At all times, each cell holds at most one thread; each gang in the matrix lies in exactly one row, in $\mathit{size}_g$ distinct columns, with each of its threads exactly once; and no row is empty.

*Proof.* PLACE writes only into free cells of one row, and distinct threads into distinct columns. A gang is written once (at its arrival) and erased once (at line L8, when its work reaches 0). Line L8 drops a row exactly when its last gang leaves. No other line changes the matrix. $\square$

**Theorem 1 (the gang rule).** In each slot, for each gang $g$, either every thread of $g$ runs, each on the processor of its column, or no thread of $g$ runs. No processor runs two threads.

*Proof.* Line L6 copies the whole row $r$. By Claim 1, a gang of row $r$ has all its threads in that row, and a gang of another row has none. Line L7 adds a gang $h$ only if all its columns are idle in the slot so far, and then it adds all of them; after that those columns are no longer idle, so a later gang cannot use them. So every gang that runs runs whole, and each processor gets at most one thread: from row $r$ (one per cell by Claim 1) or from one gang added by line L7. $\square$

**Theorem 2 (progress and the bounded wait).** Each slot in which the matrix is not empty runs at least one gang. If all gangs arrive at time 0 and $R$ is the number of rows after placement, then every gang runs in each block of $R$ consecutive slots, from slot 0 to its finish.

*Proof.* Rows are never empty (Claim 1), so line L6 runs at least one gang. For the bound: no row is added after time 0, so the number of rows is at most $R$ at all times. Let the rows that exist at a slot be $\rho_0, \ldots, \rho_{k-1}$ in order, with $k \le R$. Line L9 moves the turn to the first remaining row after the row that ran, and line L5 wraps it to row 0 after the last row. So the turns visit the rows in cyclic order, and a row that survives is visited again after at most $k - 1 \le R - 1$ turns of other rows. A gang that has not finished is in a row that survives. So the gap between two runs of a gang, or between slot 0 and its first run, is at most $R$ slots. Line L7 only adds runs. $\square$

**Termination.** Let $U = \sum_g \mathit{work}_g$ over the gangs that have arrived and not finished. Each slot after the last arrival either has an empty matrix, which means that every gang has finished and the loop ends, or runs a gang and lowers $U$ by at least 1. So the loop of line L2 ends at most $U$ slots after the last arrival. $\blacksquare$
