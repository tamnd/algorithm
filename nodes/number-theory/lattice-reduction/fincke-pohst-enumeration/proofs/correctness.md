---
title: Fincke-Pohst enumeration lists exactly the lattice vectors in the ball, and its search tree has at most the product of the Gram-Schmidt ratios as nodes per level
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The input is $n \ge 1$ linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$, a target $t \in \mathbb{Q}^m$ and a rational $R \ge 0$. We write $b_i^*$ for the Gram-Schmidt vectors, $N_i = \|b_i^*\|^2 > 0$, $\mu_{ij} = \langle b_i, b_j^* \rangle / N_j$, $\tau_j = \langle t, b_j^* \rangle / N_j$, and $o = t - \sum_j \tau_j b_j^*$, the component of $t$ orthogonal to the span. Indices are $1, \ldots, n$ here; the implementation counts from 0. For an integer vector $x$ define, for $1 \le i \le n$,

$$c_i(x) = \tau_i - \sum_{j > i} x_j \mu_{ji}, \qquad \rho_i(x) = \|o\|^2 + \sum_{j \ge i} (x_j - c_j(x))^2 N_j, \qquad \rho_{n+1} = \|o\|^2.$$

Note that $c_i$ and $\rho_i$ depend only on $x_i, \ldots, x_n$ (and $c_i$ only on $x_{i+1}, \ldots, x_n$).

**Lemma 1 (the distance splits).** For every $x \in \mathbb{Z}^n$, $\|t - x B\|^2 = \rho_1(x)$.

*Proof.* Since $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$,

$$x B = \sum_i x_i b_i = \sum_j \Big(x_j + \sum_{i > j} x_i \mu_{ij}\Big) b_j^*,$$

so $t - x B = o + \sum_j (c_j(x) - x_j) b_j^*$. The vectors $o, b_1^*, \ldots, b_n^*$ are pairwise orthogonal, and Pythagoras gives the claim. $\square$

**Lemma 2 (pruning is safe).** $\rho_{n+1} \le \rho_n(x) \le \cdots \le \rho_1(x)$. So if $\|t - x B\|^2 \le R$, then $\rho_i(x) \le R$ for every $i$.

*Proof.* Each step adds a nonnegative term $(x_i - c_i)^2 N_i$. $\square$

Call a tuple $(x_i, \ldots, x_n)$ of integers **feasible** if $\rho_i \le R$, and call it a node of level $i$. By Lemma 2, every prefix $(x_j, \ldots, x_n)$, $j \ge i$, of a feasible tuple is feasible.

**Lemma 3 (the candidates for one coordinate form an interval).** Fix a feasible $(x_{i+1}, \ldots, x_n)$, or the empty tuple when $i = n$ and $\|o\|^2 \le R$. The integers $x_i$ that make $(x_i, \ldots, x_n)$ feasible are exactly the integers in the interval $|x_i - c_i| \le \sqrt{(R - \rho_{i+1}) / N_i}$, and there are at most $2 \sqrt{R / N_i} + 1$ of them.

*Proof.* Feasibility means $(x_i - c_i)^2 N_i \le R - \rho_{i+1}$, and $c_i$ does not depend on $x_i$. An interval of length $2 \sqrt{(R - \rho_{i+1})/N_i} \le 2 \sqrt{R / N_i}$ contains at most that many plus one integers. $\square$

**Lemma 4 (the loop is a depth-first traversal).** The loop at lines L4 to L10 visits the feasible tuples in the following order. When it enters level $i$ with `new` set (line L5), it computes $c_i$ and sets $x_i$ to the smallest feasible value, using the exact search for the smallest integer with $(x - c_i)^2 \le q$. Line L6 moves to the next integer. Line L7 leaves level $i$ as soon as $x_i$ leaves the interval of Lemma 3, and lines L8 to L10 record $\rho_i$ and descend, or output $x$ at level 1.

*Proof.* By Lemma 3 the feasible $x_i$ form a run of consecutive integers, so starting at the smallest and incrementing until the first infeasible value visits exactly that run, in increasing order. Returning to level $i + 1$ with `new` cleared resumes the run at that level with the next value. Each visit of a feasible $x_i$ at level $i > 1$ descends to level $i - 1$ with `new` set, which recomputes $c_{i-1}$ from the current $x_i, \ldots, x_n$. Hence, by induction from level $n$ down, every feasible tuple is visited exactly once, prefixes in lexicographic order of $(x_n, \ldots, x_i)$. $\square$

**Correctness.** If $\|o\|^2 > R$, no lattice vector is within the radius by Lemma 1 and Lemma 2, and line L2 correctly returns the empty list. Otherwise, by Lemma 4, line L9 outputs exactly the feasible tuples of level 1, each once and in lexicographic order of $(x_n, \ldots, x_1)$, and by Lemma 1 these are exactly the $x \in \mathbb{Z}^n$ with $\|t - x B\|^2 \le R$.

**Lemma 5 (the size of the tree).** The number of nodes of level $k$ is at most $\prod_{i = k}^n (2 \sqrt{R / N_i} + 1)$.

*Proof.* By induction on $k$ from $n$ down. Every node of level $k < n$ extends a node of level $k + 1$, its prefix, and by Lemma 3 a node of level $k + 1$ has at most $2 \sqrt{R / N_k} + 1$ extensions. $\square$

**Termination and cost.** Let $T$ be the total number of nodes. Every pass through the loop either accepts a value at line L8, which creates a node, or goes up at line L7. Going up from level $i$ happens once for each node of level $i + 1$, and once for the root when $i = n$, so the loop runs at most $2T + 1$ times and terminates. Computing $c_i$ costs $O(n)$ arithmetic operations, the search for the first integer of the interval costs $O(1)$ operations plus one integer square root, and the other lines cost $O(1)$. Gram-Schmidt at line L1 costs $O(n^2 m)$. The total is $O(n^2 m + n T)$ arithmetic operations, with $T \le \sum_{k=1}^n \prod_{i=k}^n (2 \sqrt{R / N_i} + 1)$ by Lemma 5.

**Corollary (LLL preprocessing).** If the basis is LLL-reduced with $\delta = 3/4$ and $R = \|b_1\|^2$, then $N_i \ge 2^{-(i-1)} N_1$, so $R / N_i \le 2^{i - 1}$ and $T \le n \prod_{i=1}^n (2^{(i+1)/2} + 1) = 2^{O(n^2)}$.

*Proof.* The Lovász condition with size reduction gives $N_{i+1} \ge N_i / 2$. Insert $\sqrt{R / N_i} \le 2^{(i-1)/2}$ into Lemma 5. $\square$

**Theorem.** On every valid input the algorithm outputs exactly the integer vectors $x$ with $\|t - x B\|^2 \le R$, each once, in lexicographic order of $(x_n, \ldots, x_1)$, and it uses $O(n^2 m + n T)$ arithmetic operations, where the number $T$ of tree nodes satisfies the bound of Lemma 5. $\blacksquare$
