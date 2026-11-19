---
title: The Gale-Church dynamic program returns a cheapest monotone bead alignment
proves: [correctness]
status: full
---

Fix the sentence lengths $x_1, \ldots, x_I$ and $y_1, \ldots, y_J$, the bead types $T = \{(1,1), (1,0), (0,1), (2,1), (1,2), (2,2)\}$ and the bead cost $\mathrm{cost}(l_1, l_2, p, q)$ of lines L12 to L14. Every value of cost is a real number: the prior is positive, and $\ln(2(1 - \Phi(|\delta|)))$ is finite for every real $\delta$ (the implementation uses an asymptotic form where erfc underflows).

A *path* to the cell $(i, j)$ is a sequence of cells $(0, 0) = (i_0, j_0), (i_1, j_1), \ldots, (i_k, j_k) = (i, j)$ with $(i_r - i_{r-1}, j_r - j_{r-1}) \in T$ for each $r$. Step $r$ is the bead that joins the sentences $x_{i_{r-1}+1} \ldots x_{i_r}$ with $y_{j_{r-1}+1} \ldots y_{j_r}$. A path to $(I, J)$ is exactly a monotone alignment in which each sentence is in one bead: the beads cover the positions $1 \ldots I$ and $1 \ldots J$ in order and without overlap, because the indices only grow and every step moves by its bead size. The cost of a path is the sum of the costs of its steps, with $L(i_{r-1}, i_r) = x_{i_{r-1}+1} + \cdots + x_{i_r}$ and the same for $y$. Let $M(i, j)$ be the minimum cost of a path to $(i, j)$, or $+\infty$ if there is no path.

Every step of $T$ has $p + q \ge 1$, so a path to $(i, j)$ has at most $i + j$ steps and the set of paths to a cell is finite. The minimum exists when the set is not empty.

**Lemma 1 (recurrence).** $M(0, 0) = 0$, and for $(i, j) \ne (0, 0)$,

$$M(i, j) = \min_{(p, q) \in T,\ p \le i,\ q \le j} \bigl( M(i - p, j - q) + \mathrm{cost}(L(i-p, i), L'(j-q, j), p, q) \bigr),$$

with $\min \emptyset = +\infty$ and $+\infty + c = +\infty$.

*Proof.* The only path to $(0, 0)$ is the empty one, of cost 0: a non-empty path ends at a cell with $i + j \ge 1$. For $(i, j) \ne (0, 0)$, a path to $(i, j)$ is non-empty, and its last step is some $(p, q) \in T$ with $p \le i$ and $q \le j$. Removing the last step leaves a path to $(i - p, j - q)$, and its cost drops by the cost of that bead, which depends only on $(i, j)$ and $(p, q)$. Conversely, appending the step $(p, q)$ to any path to $(i - p, j - q)$ gives a path to $(i, j)$. So the paths to $(i, j)$ with last step $(p, q)$ are in bijection with the paths to $(i - p, j - q)$, and their costs differ by the same constant. The minimum over all paths is the minimum over $(p, q)$ of the minimum over each class. $\square$

**Lemma 2 (the table).** When the loops of lines L2 and L3 end, $D(i, j) = M(i, j)$ for every cell, and if $M(i, j) < \infty$ and $(i, j) \ne (0, 0)$, then $B(i, j) = (p, q)$ is a bead type that reaches the minimum of Lemma 1.

*Proof.* The loops visit the cells in row-major order. For each $(p, q) \in T$, the cell $(i - p, j - q)$ comes before $(i, j)$ in this order: either $p \ge 1$ and its row is smaller, or $p = 0$, $q = 1$ and it is the cell before in the same row. We use induction over the order of the visits. Line L1 sets $D(0, 0) = 0 = M(0, 0)$, and line L4 never changes it. At a cell $(i, j) \ne (0, 0)$, by the induction hypothesis every predecessor already holds $M(i - p, j - q)$ and is not changed later, because each cell is written only on its own visit. Line L6 computes each candidate of Lemma 1 for the predecessors with a finite value; the others give $+\infty$ and are skipped, which does not change a minimum. Line L7 keeps the smallest candidate seen so far, starting from $+\infty$, and stores its bead type. After line L5 has run through $T$, $D(i, j)$ is the minimum of Lemma 1, which is $M(i, j)$, and $B(i, j)$ is a bead type that reaches it: the first one in the order of $T$, because line L7 replaces only on a strict decrease. $\square$

**Theorem.** For all $I, J \ge 0$, GALE-CHURCH returns a list of beads that is a monotone alignment of the two texts, of cost $M(I, J)$, the minimum over all monotone alignments with the six bead types, and returns $D(I, J) = M(I, J)$.

*Proof.* A path to $(I, J)$ always exists, for example $I$ beads of type 1-0 and then $J$ beads of type 0-1. So $M(I, J) < \infty$. By induction along the paths, every cell on a path of finite cost has a finite value. The traceback of lines L8 to L10 starts at $(I, J)$. We claim that while $(i, j) \ne (0, 0)$ is the current cell, $D(i, j) = M(i, j) < \infty$ and the beads output so far, read in reverse, have cost $M(I, J) - M(i, j)$. This holds at the start. If it holds at $(i, j)$, Lemma 2 gives $(p, q) = B(i, j)$ with $M(i, j) = M(i - p, j - q) + c$, where $c$ is the cost of the bead just output. So $M(i - p, j - q) = M(i, j) - c < \infty$, and the beads output now have cost $M(I, J) - M(i - p, j - q)$. Each step lowers $i + j$ by at least 1, so the loop ends, and it ends at $(0, 0)$ because $i$ and $j$ never become negative ($p \le i$ and $q \le j$ by line L5). At the end the beads have cost $M(I, J) - M(0, 0) = M(I, J)$. Read in reverse, the cells visited form a path from $(0, 0)$ to $(I, J)$, so by the remark on paths the beads are a monotone alignment. Line L11 returns them and $D(I, J)$. $\square$

**Remark (the tie rule).** If two bead types give the same value at a cell, line L7 keeps the first one in the order 1-1, 1-0, 0-1, 2-1, 1-2, 2-2. The theorem does not depend on this choice. The tests compare the cost of the output with the minimum over all paths listed one by one, and they check that the output is a path.

**Remark (complexity).** Each of the $(I + 1)(J + 1)$ cells looks at most at 6 predecessors, and with prefix sums each candidate costs $O(1)$ operations, so lines L1 to L7 take $O(I J)$ time. The table and the back pointers take $O(I J)$ space, and the traceback has at most $I + J$ steps.
