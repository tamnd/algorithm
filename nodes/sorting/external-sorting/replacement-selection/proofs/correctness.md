---
title: Replacement selection makes sorted runs, each but the last with at least P items
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode, and we write $c = |R|$ for the number of the current run. When $c \ge 1$, let $w$ be the last item written by line L7. All items of $F$ are distinct as triples, because their positions $s$ are distinct.

**Invariant.** At each test of line L4:

1. Each run of $R$ is sorted, and no run is empty.
2. If $c = 0$, each item in $H$ has run number 1. If $c \ge 1$, each item in $H$ has run number $c$ or $c + 1$, and each item with run number $c$ has a key of at least $w$.
3. The items written to $R$, the items in $H$ and the items not yet read are together the items of $F$, each one time.

*Initialization.* Line L2 gives each item in $H$ the run number 1, and $R$ is empty. So the invariant is true.

*Maintenance.* Let $(r, x, s)$ be the minimum of $H$ at line L5.

Case $c = 0$. Then $r = 1$, line L6 appends run 1, and line L7 makes it $(x)$, which is sorted.

Case $c \ge 1$ and $r = c$. By part 2, $x \ge w$, so run $c$ stays sorted when line L7 appends $x$. Line L6 does nothing, because $r = |R|$.

Case $c \ge 1$ and $r = c + 1$. Because the heap orders by run number first, no item in $H$ has run number $c$. Line L6 appends run $c + 1$, and line L7 makes it $(x)$. The current run is now $c + 1$.

In each case, the new current run is $r$ and the new last item is $w = x$. We check part 2 for the new values. Each other item in $H$ has run number $r$ or $r + 1$: in the first two cases because the numbers in $H$ were $c$ or $c+1$ with $r = c$, and in the third case because they were all $c + 1 = r$. Each other item in $H$ with run number $r$ is at least $x$, because $x$ is the minimum among the items with run number $r$. If line L8 reads an item $y$, line L9 gives it the number $r$ only when $y \ge x$, and else $r + 1$. So part 2 stays true. Line L10 or line L11 removes $x$ from $H$, and $x$ is now in $R$, so part 3 stays true. Part 1 holds by the three cases.

*Termination.* Each iteration writes exactly one item to $R$. By part 3, at most $n$ items can be written. So the loop stops after at most $n$ iterations. It stops only when $H$ is empty. Line L11 runs only when no item is left to read, so at that point all items are written, and the loop ran exactly $n$ times.

**Theorem 1.** REPLACEMENT-SELECTION returns sorted, non-empty runs whose items together are the items of $F$, each one time.

*Proof.* At the end, $H$ is empty and no item is left to read. Parts 1 and 3 of the invariant give the claim. $\blacksquare$

**Theorem 2.** Each run except the last has at least $P$ items.

*Proof.* Take a run $c$ that is not the last run. Run $c + 1$ starts at a step where all items in $H$ have run number $c + 1$. First let $c \ge 2$. Run $c$ started at a step where all items in $H$ had run number $c$, and all of them are written to run $c$. If the input was not empty at that step, line L10 kept the heap at $P$ items since line L2, so the heap held $P$ items, and run $c$ has at least $P$ items. If the input was empty at that step, then no item is read after it, so no item gets the run number $c + 1$, and run $c$ is the last run. This is false. Now let $c = 1$. When run 2 starts, $H$ holds at least one item with run number 2. Such an item was read by line L8 at a step that wrote an item to run 1. If the heap held fewer than $P$ items after line L2, the input was empty, no item was read, and there is no run 2. So the heap held $P$ items, all of them with run number 1, and they are all written to run 1. $\blacksquare$

**Theorem 3 (equal keys).** Let $a$ and $b$ be items with equal keys, where $a$ comes before $b$ in $F$. Then the run of $a$ is at most the run of $b$, and if they are in the same run, $a$ comes first in it.

*Proof.* Write $\rho(z)$ for the run number of item $z$. An item that line L2 reads gets $\rho = 1$, and an item that line L8 reads at a step with current run $c$ gets $\rho = c$ or $\rho = c + 1$. The current run never decreases. If $a$ is read by line L2, then $\rho(a) = 1 \le \rho(b)$. Else let $c_a$ and $c_b$ be the current runs at the steps that read $a$ and $b$, with $c_a \le c_b$. If $c_a < c_b$, then $\rho(b) \ge c_b \ge c_a + 1 \ge \rho(a)$. If $c_a = c_b = c$ and $\rho(a) = c + 1$, then the key of $a$ is less than the item $w_a$ just written at that step. The items written to run $c$ are written in sorted order by Theorem 1, so the item $w_b$ written at the step that reads $b$ satisfies $w_b \ge w_a$. The key of $b$ equals the key of $a$, so it is less than $w_b$, and $\rho(b) = c + 1$. In all cases $\rho(a) \le \rho(b)$. If $\rho(a) = \rho(b)$, the heap order by run number, then key, then position puts $a$ before $b$, because $a$ has the smaller position, and both are in the heap or $a$ was already written when $b$ was read. $\blacksquare$
