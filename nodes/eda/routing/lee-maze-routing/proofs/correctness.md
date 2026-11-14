---
title: Lee's algorithm labels cells with their distance from the source and backtraces a shortest path, and two bits per cell are enough
proves: [correctness, termination, completeness, running time, akers coding]
status: full
---

Let $G$ be the graph whose vertices are the free cells of the grid, with an edge between two cells that share a side. Let $\delta(v)$ be the number of steps of a shortest path from $s$ to $v$ in $G$, or $\infty$ if there is none. Write $L = \delta(t)$.

**Lemma 1 (queue order).** At every moment the labels of the cells in the queue, from first to last, are non-decreasing, and the last label is at most the first label plus 1.

*Proof.* At the start the queue holds only $s$. Line L3 removes the first cell $u$, with the smallest label $k$, so the remaining labels lie in $\{k, k+1\}$. Line L5 adds cells with label $k + 1$ at the end. Both properties hold again. $\square$

By Lemma 1 the cells leave the queue in order of their labels. Call *phase* $k$ the part of the run in which the cells with label $k$ are removed and processed. A label $k + 1$ is only set in phase $k$.

**Lemma 2 (labels are distances).** For each $k \ge 0$, at the start of phase $k$ the cells with a label at most $k$ are exactly the cells with $\delta(v) \le k$, and each of them has $\mathrm{label}(v) = \delta(v)$. No cell has a label larger than $k$.

*Proof.* By induction on $k$. At the start of phase 0 only $s$ has a label, 0, and $\delta(s) = 0$ while $\delta(v) \ge 1$ for every other cell.

Assume the claim at the start of phase $k$, and let phase $k$ run to its end. The cells labeled in phase $k$ get label $k + 1$, and they are the unlabeled free neighbors of cells with label $k$. Such a cell $v$ is next to a cell with $\delta = k$, so $\delta(v) \le k + 1$. It had no label, so by the assumption $\delta(v) > k$. So $\delta(v) = k + 1 = \mathrm{label}(v)$. Conversely, let $\delta(v) = k + 1$, and let $w$ be the cell before $v$ on a shortest path, with $\delta(w) = k$. By the assumption $w$ has label $k$, so it is processed in phase $k$. At that moment $v$ has no label of at most $k$, so line L4 labels it now, or it was labeled earlier in the same phase with $k + 1$. No cell gets label $k + 2$ in phase $k$. This is the claim for $k + 1$. $\square$

**Lemma 3 (early stop).** When the loop of lines L2 to L5 stops because $t$ is labeled, $\mathrm{label}(t) = L$ and every cell $v$ with $\delta(v) < L$ has $\mathrm{label}(v) = \delta(v)$.

*Proof.* The label of $t$ is set in some phase $k$, and it is $k + 1$. By Lemma 2 applied at the start of phase $k$ and in its proof, $\mathrm{label}(t) = \delta(t) = L$, so $k = L - 1$. At the start of phase $L - 1$, Lemma 2 says that every cell with $\delta(v) \le L - 1$ has its correct label. $\square$

**Lemma 4 (backtrace).** If $t$ is labeled, lines L7 to L10 stop after exactly $L$ steps, and the cells form a path from $t$ to $s$ in $G$.

*Proof.* Let $u \ne s$ be the current cell with $\delta(u) = k \ge 1$. A shortest path from $s$ to $u$ has a cell $w$ before $u$ with $\delta(w) = k - 1 < L$. By Lemma 3, $w$ is labeled, and by Lemma 2 its label is $k - 1$. So line L9 finds a neighbor with label $k - 1$, and the label falls by exactly 1 at each step. After $L$ steps the label is 0, and the only cell with $\delta = 0$ is $s$. Every step goes between neighbors, so the cells form a path. $\square$

**Theorem (correctness and completeness).** If $t$ is reachable from $s$, the algorithm returns a path of length $\delta(t)$, which is a shortest path. Otherwise it returns "no path".

*Proof.* If $t$ is reachable, the queue cannot become empty before $t$ is labeled. Indeed, by Lemma 2 there is a cell with label $k$ for every $k \le \delta(t)$, since a shortest path to $t$ has a cell at each distance, and phase $\delta(t) - 1$ labels $t$. Lemma 4 then gives a path of length $L = \delta(t)$. If $t$ is not reachable, no label is ever given to $t$, since labels follow edges from $s$, so line L6 reports that there is no path. $\square$

**Running time.** Each free cell gets a label at most once, so it enters and leaves the queue at most once. Each removal looks at 4 neighbors. The expansion takes $O(MN)$ time. Each backtrace step looks at 4 neighbors, and there are $L \le MN$ steps. The labels take one entry per cell, $\Theta(MN)$ space. $\square$

**Lemma 5 (Akers coding).** Replace $\mathrm{label}(v)$ by $a(v) = \sigma(\mathrm{label}(v) \bmod 4)$, where $\sigma = (0, 0, 1, 1)$. If the backtrace knows the label $k$ of the current cell modulo 4, the neighbor it needs is the unique kind of labeled neighbor with $a = \sigma((k - 1) \bmod 4)$.

*Proof.* The grid graph is bipartite: a step changes the parity of row plus column. So two neighbors have labels of different parity, and since both labels are distances, they differ by exactly 1. A labeled neighbor of a cell with label $k$ has label $k - 1$ or $k + 1$. These two numbers differ by 2, and $\sigma(j) \ne \sigma(j + 2 \bmod 4)$ for each $j$, because $\sigma$ is 0 on $\{0, 1\}$ and 1 on $\{2, 3\}$. So the bit tells the two kinds apart. The backtrace starts at $t$, whose label is known from the step count of the expansion, and lowers $k$ by 1 at each step. A cell then needs two bits: one for the states "free and unlabeled" or "blocked" and one for $a(v)$, or a code of four states in two bits. $\square$
