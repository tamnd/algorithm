---
title: Karp's formula gives the minimum cycle mean, and the walk at the minimizing vertex holds an optimal cycle
proves: [correctness, termination]
status: full
---

Let $G = (V, A)$ be a finite directed graph with $n \ge 1$ vertices, arcs of real weight $w$, parallel arcs and self-loops allowed. For $k \ge 0$ and $v \in V$ let $D_k(v)$ be the least weight of a walk with exactly $k$ arcs that ends at $v$ (and starts anywhere), with $D_0(v) = 0$ and $D_k(v) = \infty$ if there is no such walk.

**Termination and the table.** Lines L2 to L5 run $n$ rounds over a finite arc list, and line L11 moves from $(k, v)$ to $(k - 1, u)$, so it stops after at most $n$ steps. By induction on $k$, lines L3 to L5 set $D[k][v] = \min_{(u, v) = a} D[k-1][u] + w(a)$, which is $D_k(v)$: a walk of $k$ arcs to $v$ is a walk of $k - 1$ arcs to some $u$ followed by an arc $(u, v)$. The pointer $P[k][v]$ is the last arc of a walk that attains $D_k(v)$, so following the pointers from $(n, t)$ traces such a walk backwards.

**Fact 1 (decomposition).** A closed walk splits into simple cycles, so its mean is a weighted average of their means and is at least $\lambda^*$, the least mean of a simple cycle. A walk with $n$ or more arcs visits at least $n + 1$ vertex positions, so some vertex repeats and it contains a closed sub-walk. Hence $G$ has a cycle if and only if $D_n(v) < \infty$ for some $v$, and line L10 is correct.

From here on, $G$ has a cycle, and $\lambda^*$ is the least mean of a cycle.

**Fact 2 (shift).** Replace $w$ by $w' = w - c$ for a constant $c$. Every walk with $k$ arcs loses $kc$, so $D'_k(v) = D_k(v) - kc$, and $(D'_n(v) - D'_k(v))/(n - k) = (D_n(v) - D_k(v))/(n - k) - c$. Every cycle mean drops by $c$. So the formula and $\lambda^*$ both drop by $c$, the choice of $t$ at line L9 and the pointers do not change, and it suffices to prove the claims for $w' = w - \lambda^*$. Assume from now on that $\lambda^* = 0$: every cycle has weight at least 0, and some cycle has weight 0.

**Lemma 3.** For every $v$ with $D_n(v) < \infty$, $\max_{0 \le k < n,\ D_k(v) < \infty} (D_n(v) - D_k(v))/(n - k) \ge 0$.

*Proof.* Let $W$ be a walk of $n$ arcs to $v$ of weight $D_n(v)$. By Fact 1 it contains a closed sub-walk; removing it leaves a walk to $v$ with fewer arcs and weight at most $D_n(v)$, since the removed part has weight at least 0. Repeat until no vertex repeats: the result is a walk with $k < n$ arcs to $v$ and weight at most $D_n(v)$. So $D_k(v) \le D_n(v)$ for this $k$, and that term of the max is at least 0. $\square$

**Lemma 4.** Some $v$ has $D_n(v) \le D_k(v)$ for every $k < n$ with $D_k(v) < \infty$, so its max is at most 0.

*Proof.* Let $\delta(v) = \min_{k \ge 0} D_k(v)$. It is finite: walks of length 0 have weight 0, and, as no cycle is negative, removing closed sub-walks as in Lemma 3 shows that the minimum over all lengths is attained by some walk with fewer than $n$ arcs. So $\delta(v) = \min_{0 \le k < n} D_k(v)$. Let $C$ be a cycle of weight 0 with vertices $c_0, c_1, \ldots, c_{L-1}$ in order. For each $j$, $\delta(c_{j+1}) \le \delta(c_j) + w(c_j, c_{j+1})$ (indices mod $L$), and the sum of these inequalities around $C$ is an equality because $w(C) = 0$; so each one is an equality.

Choose $c_0$ with $\delta(c_0)$ attained by a walk $Q$ with $k_0 < n$ arcs. Follow $C$ from $c_0$ for $n - k_0$ arcs, ending at some $c_j$. The walk $Q$ followed by these arcs has $n$ arcs and, by the equalities, weight $\delta(c_j)$. So $D_n(c_j) \le \delta(c_j) \le D_k(c_j)$ for every $k$. $\square$

**Theorem 5 (Karp's formula).** $\lambda^* = \min_{v : D_n(v) < \infty} \max_{0 \le k < n,\ D_k(v) < \infty} (D_n(v) - D_k(v))/(n - k)$, so line L9 ends with $\lambda = \lambda^*$.

*Proof.* With $\lambda^* = 0$: every max is at least 0 by Lemma 3, and some max is at most 0 by Lemma 4, so the min is 0. The general case follows by Fact 2. $\square$

**Theorem 6 (the cycle).** The cycle $C$ returned by line L11 has mean $\lambda^*$.

*Proof.* With $\lambda^* = 0$, the vertex $t$ chosen at line L9 has max equal to 0, so $D_n(t) \le D_k(t)$ for every $k < n$ with $D_k(t) < \infty$. Line L11 traces a walk $W$ of $n$ arcs to $t$ of weight $D_n(t)$, and $C$ is a closed sub-walk of $W$ between two visits of the same vertex, with no vertex repeated inside it, so $C$ is a simple cycle with $L \ge 1$ arcs. Removing $C$ from $W$ leaves a walk of $n - L$ arcs to $t$ of weight $D_n(t) - w(C)$, so $D_{n-L}(t) \le D_n(t) - w(C)$, which is finite, and $w(C) \le D_n(t) - D_{n-L}(t) \le 0$. Also $w(C) \ge 0$, so $w(C) = 0$, the mean of $C$ is $\lambda^*$. By Fact 2 this holds for the original weights. $\blacksquare$
