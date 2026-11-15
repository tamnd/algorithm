---
title: The constructed time function puts every dependence between fronts, so the fronts can run in parallel
proves: [correctness]
status: full
---

## Setting

The nest has depth $k$ and iteration space $P = \{i \in \mathbb{Z}^k : A i + b \ge 0\}$, a bounded set. $D$ is a finite set of nonzero distance vectors, each lexicographically positive: for each $d \in D$ there is a level $\ell(d)$ with $d_1 = \dots = d_{\ell(d) - 1} = 0$ and $d_{\ell(d)} > 0$. Every dependence of the nest goes from an iteration $i$ to the iteration $i + d$ for some $d \in D$, or stays inside one iteration. The body of one iteration runs as a unit, with its statements in text order.

The algorithm computes $\pi$ by lines L1 to L7:

$$\pi_k = 1, \qquad \pi_l = \max\Bigl(0,\ \max_{d \in D,\ \ell(d) = l} \Bigl\lceil \frac{1 - \sum_{m > l} \pi_m d_m}{d_l} \Bigr\rceil\Bigr) \quad (l = k - 1, \dots, 1),$$

with the inner maximum taken as $0$ when no $d$ leads at $l$. It then forms the matrix $T$ with the rows $\pi, e_1, \dots, e_{k-1}$ (line L8) and runs the fronts $F_t = \{i \in P : \pi \cdot i = t\}$ in increasing $t$, each front in any order or in parallel (lines L9 to L11).

## Lemma 1: every distance gets a positive time difference

**Claim.** $\pi \cdot d \ge 1$ for every $d \in D$.

*Proof.* Let $l = \ell(d)$. Then $\pi \cdot d = \pi_l d_l + \sum_{m > l} \pi_m d_m$, because the entries before $l$ are $0$.

If $l = k$, then $d = (0, \dots, 0, d_k)$ with $d_k \ge 1$, and $\pi \cdot d = d_k \ge 1$.

If $l < k$, write $r = \sum_{m > l} \pi_m d_m$. The values $\pi_m$ for $m > l$ are fixed before level $l$ is processed, so $r$ is the value that line L5 computes. Line L6 makes $\pi_l \ge \lceil (1 - r)/d_l \rceil \ge (1 - r)/d_l$. Multiplying by $d_l > 0$ gives $\pi_l d_l \ge 1 - r$, so $\pi \cdot d = \pi_l d_l + r \ge 1$. $\square$

So a time function exists whenever every distance is lexicographically positive, which holds for every real dependence. The construction also gives $\pi_l \ge 0$ for all $l$ and $\pi_k = 1$.

## Lemma 2: the matrix is unimodular

**Claim.** $\det T = \pm 1$, and the inverse map is $i_l = y_{l+1}$ for $l < k$ and $i_k = y_1 - \sum_{l < k} \pi_l y_{l+1}$.

*Proof.* Move the first row of $T$ to the bottom. This is a cyclic permutation of the rows and changes the determinant by the factor $(-1)^{k-1}$. The result has the rows $e_1, \dots, e_{k-1}, \pi$, which is lower triangular with diagonal $1, \dots, 1, \pi_k = 1$, so its determinant is $1$. Hence $\det T = (-1)^{k-1}$.

For the inverse: $y = T i$ means $y_1 = \pi \cdot i$ and $y_{l+1} = i_l$ for $l < k$. Then $y_1 = \sum_{l < k} \pi_l y_{l+1} + \pi_k i_k$ with $\pi_k = 1$, which gives the formula for $i_k$. All coefficients are integers, so $i$ is an integer vector exactly when $y$ is. $\square$

So $i \mapsto T i$ is a bijection from $P$ onto $Q = \{y \in \mathbb{Z}^k : A T^{-1} y + b \ge 0\}$, and $i \in F_t$ exactly when $T i \in Q$ has first coordinate $t$.

## Lemma 3: the scan visits each iteration once, front by front

**Claim.** The nest of lines L9 to L11, with bounds from Fourier-Motzkin elimination, visits every point of $Q$ exactly once, in lexicographic order of $y$.

*Proof.* Let $Q_v$ be the real projection of the real polyhedron of $Q$ onto the coordinates $y_1, \dots, y_v$. Fourier-Motzkin elimination of $y_k, \dots, y_{v+1}$ gives a system of inequalities whose real solution set is exactly $Q_v$. The loop at level $v$ runs, for fixed integers $y_1, \dots, y_{v-1}$, over the integers $y_v$ with $(y_1, \dots, y_v) \in Q_v$: its lower bound is the ceiling of the largest lower bound and its upper bound is the floor of the smallest upper bound. Every integer point of $Q$ projects into each $Q_v$, so each of its coordinates is in the range of its loop, and the point is visited. At level $k$ the system is the original one, so a visited point satisfies all constraints of $Q$ and is in $Q$. The loops run each coordinate in increasing order, so the points come in lexicographic order, and no point comes twice. A range can be empty for some outer values, when the real projection has no integer point above them; then the inner loop runs zero times, which loses nothing. $\square$

By Lemma 2, the visited $y$ correspond one to one to the iterations of $P$, and the outer coordinate $y_1 = t$ is constant on each front and increases from front to front.

## Theorem: the fronts keep every dependence, and a front has none inside it

**Claim.** Run the fronts in increasing $t$, and the iterations of each front in any order or at the same time. Then every dependence pair runs in its original order, two iterations of one front never depend on each other, and the final state equals the state of the original nest.

*Proof.* Take a dependence from iteration $i$ to iteration $j \ne i$. Then $j = i + d$ for some $d \in D$, and $\pi \cdot j = \pi \cdot i + \pi \cdot d \ge \pi \cdot i + 1$ by Lemma 1. So $j$ is in a strictly later front than $i$, and the front of $i$ runs to completion first. In particular, no dependence joins two distinct iterations of one front, in either direction. A dependence inside one iteration keeps its order, because the body runs as a unit in text order.

Inside a front, the iterations touch disjoint sets of elements that any of them writes: if two of them touched one element and one wrote it, the one that runs first in the original order would be the source of a dependence to the other, which we just excluded. So any order or interleaving of the iterations of one front gives the same state after the front. By induction over the fronts, the state after each front is the state that the original nest has after running exactly the iterations of the fronts so far, in its own order; this follows from Theorem 1 of the loop transformation legality page, since every dependence pair keeps its order. After the last front, by Lemma 3, every iteration has run once, and the final states agree. $\square$

## What the construction does not promise

The number of fronts is not minimal in general. The construction always sets $\pi_k = 1$, so that $T$ is unimodular with the simple inverse above. For the single distance $(1, -3)$ on the box $1 \le i, j \le 4$ it gives $\pi = (4, 1)$, and all 16 iterations get different times, while $\pi = (1, 0)$, which is also valid, gives 4 fronts of 4 iterations. The correctness proof above holds for any integer $\pi$ with $\pi \cdot d \ge 1$, given a scan of the fronts; only Lemma 2 uses $\pi_k = 1$.
