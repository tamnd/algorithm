---
title: The incremental cost change is exact, the final packing is legal, and the annealing stops after a fixed number of temperatures
proves: [correctness, termination, running time]
status: full
---

Let $C = 2 \sum_e w_e \operatorname{HPWL}(e) + \mu \cdot \text{overlap}$, where overlap $= \sum_{\text{sites}} \max(0, o_s - 1)$ and $o_s$ is the number of cells on site $s$.

**Lemma 1 (the change of the overlap).** Removing a cell from a site with count $o_s$ lowers the overlap by 1 if $o_s \ge 2$ and leaves it if $o_s = 1$. Adding a cell to a site with count $o_s$ raises the overlap by 1 if $o_s \ge 1$ and leaves it if $o_s = 0$.

*Proof.* The term of the site is $\max(0, o_s - 1)$. It changes from $o_s - 1$ to $o_s - 2$ when $o_s \ge 2$ falls by 1, and stays 0 when $o_s = 1$ falls to 0. The case of adding is the same in reverse. $\square$

**Lemma 2 (line L6 is exact).** For a move of a set $Q$ of one or two cells, the value $\Delta$ of line L6 equals $C$ after the move minus $C$ before it.

*Proof.* A net with no cell of $Q$ has the same pins before and after, so its HPWL does not change. Line L6 sums the doubled HPWL of all nets that contain a cell of $Q$, before and after, so the difference of the sums is the change of the wire term. For the overlap, line L6 first removes every cell of $Q$ from the counts, then sets the new positions, then adds every cell of $Q$. Each step changes the overlap as Lemma 1 says, and the implementation adds exactly those changes. Removing all cells of $Q$ first matters for a swap, where one cell takes sites that the other leaves. The sum of the steps is the total change of the overlap. Undoing the move applies the old positions in the same way, so it restores the counts and $C$. $\square$

**Corollary (the acceptance rule).** A move is kept with probability 1 if $\Delta \le 0$ and with probability $e^{-\Delta / T}$ if $\Delta > 0$, because `random()` is uniform on $[0, 1)$ and line L7 undoes the move exactly when `random()` $\ge e^{-\Delta/T}$. So at each temperature the annealing is the Metropolis chain for $C$ restricted to the moves of the window. If $T$ is so small that $e^{-\Delta / T} = 0$ for every $\Delta \ge 1$, no uphill move is kept, and since all values of $C$ are integers, $C$ never rises.

**Lemma 3 (moving cells out of overfull rows).** If line L9 returns, every row holds cells of total width at most $S$.

*Proof.* The procedure keeps the load of each row equal to the total width of its cells. It handles the rows in order. While a row $k$ has load above $S$, it moves one of its cells to a row $q$ whose load plus the width of the cell is at most $S$, or it stops with an error. A row that receives a cell still has load at most $S$, so a row once at most $S$ stays so, and each pass lowers the load of row $k$. When the loop over the rows ends, every row is at most $S$. $\square$

When all cells have width 1 and $n \le K S$, the error never happens: a row with load above $S$ exists only if another row has load below $S$, and a unit cell fits there.

**Lemma 4 (packing a row).** Let cells with integer widths and total width at most $S$ be packed: in order of their targets, each goes to the site nearest its target, clamped to $[0, S - W_i]$, but not left of the end of the previous cell; then, from the right, each cell is moved left to end at or before the start of the next cell, with the first limit $S$. Then every cell is inside $[0, S)$ and no two overlap.

*Proof.* Number the cells $1, \ldots, m$ in the order. After the first pass, $p_j \ge p_{j-1} + W_{j-1}$, so $p_j \ge \sum_{l < j} W_l$. The second pass sets $p'_m = \min(p_m, S - W_m)$ and $p'_j = \min(p_j, p'_{j+1} - W_j)$. By induction from $j = m$ down, $p'_j \ge \sum_{l < j} W_l$: the first term of each minimum satisfies it, $S - W_m \ge \sum_{l < m} W_l$ because the cells fit, and $p'_{j+1} - W_j \ge \sum_{l \le j} W_l - W_j$. So every $p'_j \ge 0$, and the second pass gives $p'_j + W_j \le p'_{j+1}$ and $p'_m + W_m \le S$. All values are integers, so the cells are on sites. $\square$

**Theorem 1 (legality).** If SA-PLACE returns, its placement is legal, and its HPWL is at least the optimum of the placement problem.

*Proof.* By Lemma 3 every row holds at most $S$ sites of cells, and by Lemma 4 each row is packed legally. Cells of different rows do not overlap. A legal placement is feasible for the placement problem, so its HPWL is at least the least HPWL of all legal placements. $\blacksquare$

**Theorem 2 (termination and running time).** With $0 < \alpha < 1$ and $T_0, T_{\text{end}} > 0$, the loop of line L2 runs $L = \max(0, \lceil \log(T_{\text{end}} / T_0) / \log \alpha \rceil)$ times, and SA-PLACE runs in $O(L M n D + n (n + K) + K S + P)$ time, where $D$ bounds the pins on the nets of a cell plus its width.

*Proof.* After $j$ temperatures $T = \alpha^j T_0$, which is at most $T_{\text{end}}$ exactly when $j \ge \log(T_{\text{end}} / T_0) / \log \alpha$. Each temperature makes $M n$ proposals. A proposal costs $O(1)$; line L6 scans the nets of at most two cells and the sites under them, $O(D)$; line L7 costs the same to undo. Line L1 costs $O(K S + n W_{\max} + P)$. In line L9, each cell leaves an overfull row at most once, since it never moves to a row above $S$, and each such step scans the cells and rows, $O(n + K)$; the sorts of the packing cost $O(n \log n)$. $\blacksquare$
