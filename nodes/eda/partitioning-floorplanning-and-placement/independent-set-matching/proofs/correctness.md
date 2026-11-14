---
title: For cells that share no net, the wirelength is separable, so the assignment gives the best permutation, keeps the placement legal and never increases HPWL
proves: [correctness, termination, running time]
status: full
---

Fix one step, with the set $S = \{c_1, \ldots, c_k\}$ of line L3 and the slots $s_1, \ldots, s_k$ of line L5, where $c_a$ is at $s_a$ before the step. For a permutation $\sigma$ of $\{1, \ldots, k\}$, let $\mathrm{WL}(\sigma)$ be the wirelength when each $c_a$ is at $s_{\sigma(a)}$ and every other cell is where it was. The identity is $\iota$.

**Lemma 1 (the set is independent and of one width).** Every cell of $S$ has the width $W_{c_0}$, and no net contains two cells of $S$.

*Proof.* Line L3 takes only cells of width $W_{c_0}$. It appends a cell $c$ only if no net of $c$ is a net of a cell already in $S$. So for two cells of $S$, the later one shares no net with the earlier one. $\square$

**Lemma 2 (separable cost).** Let $N_S$ be the nets with a pin on a cell of $S$, and $\mathrm{WL}_0 = \sum_{e \notin N_S} w_e \mathrm{HPWL}(e)$. For every permutation $\sigma$,

$$ \mathrm{WL}(\sigma) = \mathrm{WL}_0 + \sum_{a=1}^{k} \mathrm{cost}(c_a, s_{\sigma(a)}). $$

*Proof.* A net $e \notin N_S$ has no pin on a cell of $S$, so no pin moves, and its term is the same for every $\sigma$; together these terms give $\mathrm{WL}_0$. By Lemma 1, each net $e \in N_S$ has a pin on exactly one cell $c_a$ of $S$, and its other pins are on cells outside $S$ or on pads, which do not move. So under $\sigma$ the HPWL of $e$ equals its HPWL with $c_a$ at $s_{\sigma(a)}$ and all other cells where they were. Summing over the nets of $c_a$ gives $\mathrm{cost}(c_a, s_{\sigma(a)})$, and each net of $N_S$ is counted once, for its one cell of $S$. $\square$

**Theorem 1 (best permutation, no increase).** After line L8, the wirelength is $\min_\sigma \mathrm{WL}(\sigma) \le \mathrm{WL}(\iota)$, the wirelength before the step.

*Proof.* Line L6 fills $\mathrm{cost}[a][b] = \mathrm{cost}(c_a, s_b)$. By Lemma 2, $\mathrm{WL}(\sigma) = \mathrm{WL}_0 + \sum_a \mathrm{cost}[a][\sigma(a)]$, and $\mathrm{WL}_0$ does not depend on $\sigma$. The Hungarian algorithm returns a permutation of least $\sum_a \mathrm{cost}[a][\sigma(a)]$ (see the [Hungarian algorithm](/hungarian-algorithm/) for its proof), so it returns a $\sigma$ of least $\mathrm{WL}(\sigma)$. The identity is a permutation, so the least value is at most $\mathrm{WL}(\iota)$. $\blacksquare$

**Theorem 2 (legal).** If the placement is legal before a step, it is legal after it.

*Proof.* By Lemma 1 all cells of $S$ have the same width $W$. The slot $s_b$ is the left edge and row of $c_b$ before the step, so it is the interval $[x, x + W)$ of sites in a row, inside the row and free of every cell outside $S$. After the step the cells of $S$ occupy the same $k$ intervals, one cell in each, because $\sigma$ is a bijection. The cells outside $S$ do not move. So the set of occupied intervals is the same as before, and no two cells overlap. $\blacksquare$

**Theorem 3 (termination and running time).** With $P$ passes the algorithm stops after $P n$ steps. One step costs $O(n D + k^2 D + k^3)$ time, where $D$ bounds the number of pins on the nets of one cell (so also the number of its nets).

*Proof.* The loops of lines L1 and L2 run $P$ and $n$ times. Line L3 looks at each cell of the window once, at most $n$ cells, and keeps the nets of $S$ in a hash set, so each test costs the number of nets of the cell, at most $D$, in expected $O(1)$ time per net. Line L6 computes $k^2$ values; each needs the HPWL of the nets of one cell, $O(D)$ pin positions, so $O(k^2 D)$ in total. The Hungarian algorithm with potentials runs in $O(k^3)$ time, and line L8 in $O(k)$. $\blacksquare$
