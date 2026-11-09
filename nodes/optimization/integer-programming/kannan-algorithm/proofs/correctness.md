---
title: Kannan's algorithm is correct and branches on at most n^3 hyperplanes
proves: [correctness]
status: full
---

**Statement.** Let $P = \{x \in \mathbb{R}^n : A x \le b\}$ be a bounded rational polyhedron. KANNAN$(A, b)$ terminates and returns a point of $P \cap \mathbb{Z}^n$ if this set is not empty, and NONE otherwise. Each call in dimension $n$ that reaches line L9 has $|K| \le n^3$.

**Correctness.** Use induction on $n$. Line L1 is correct for $n = 0$. Lines L1 to L5 and L10 to L11 are the same as lines L1 to L5 and L11 to L12 of Lenstra's algorithm, so the slice lemma and the flat case lemma of that proof apply without change: for a primitive integer vector $d$ and a unimodular $W$ with $d^\top W = e_1^\top$, the map $z \mapsto W(k, z)$ is a bijection from the integer points of the subproblem onto the integer points $x$ of $P$ with $d^\top x = k$, and the subproblem is a bounded polyhedron in dimension $n - 1$. Line L7 returns a point only if it is in $P$, and it is an integer point.

At line L9 the vector $d$ is a nonzero integer vector of minimum $Q^{-1}$-length. It is primitive: if $d = g d'$ with an integer $g \ge 2$ and $d' \in \mathbb{Z}^n$, then $\|d'\|_{Q^{-1}} = \|d\|_{Q^{-1}} / g < \|d\|_{Q^{-1}}$, which is a contradiction. Every integer point $x \in P$ has $d^\top x \in \mathbb{Z}$, and $\min_V d^\top v \le d^\top x \le \max_V d^\top v$ because $P$ is the convex hull of $V$. So $d^\top x \in K$, and by the slice lemma and the induction hypothesis, SLICE finds an integer point of $P$ when one exists and returns NONE otherwise. Each call makes finitely many calls in dimension $n - 1$, so the recursion terminates.

**The enumeration is exact.** Let $b_1, \dots, b_n$ be a basis of $\mathbb{Z}^n$ with Gram-Schmidt vectors $b_i^*$ and coefficients $\mu_{ji}$ in the inner product of $Q$, and let $t = \sum_i \tau_i b_i^*$. For $x = \sum_j u_j b_j$,
$$\|x - t\|_Q^2 = \sum_{i=1}^n \|b_i^*\|_Q^2 \Big(u_i + \sum_{j > i} \mu_{ji} u_j - \tau_i\Big)^2.$$
All terms are nonnegative, so the sum of the terms with index at least $i$ is at most the total. The search fixes $u_n, u_{n-1}, \dots$ in this order and visits every value of $u_i$ for which the partial sum stays at most the current bound. A vector with $\|x - t\|_Q^2$ less than the current bound has all its partial sums less than the current bound, so the search visits it. The bound only decreases to values of points it has seen, so at the end the best point is a minimizer. The candidate set is finite because each $u_i$ ranges over a bounded interval. This proves that line L6 returns a closest integer point to $c$, and line L8 (with $t = 0$ and the point $0$ excluded) a shortest nonzero vector.

**The bound on $|K|$.** Let $r = 1/\sqrt{2n(n+1)}$. By the rounding lemmas of Lenstra's algorithm, $B_Q(c, r) \subseteq S \subseteq P \subseteq B_Q(c, n^2 r)$.

*Step 1.* Line L9 runs only if $y \notin P$. Since $B_Q(c, r) \subseteq P$, we get $\|y - c\|_Q > r$. Line L6 returns a closest integer point, so every integer point has $Q$-distance more than $r$ from $c$. The covering radius $\mu$ of $\mathbb{Z}^n$ in the norm $\|\cdot\|_Q$ is the largest such distance over all points of $\mathbb{R}^n$, so $\mu > r$.

*Step 2.* Write $Q = L^\top L$ with $L$ invertible. The map $x \mapsto L x$ sends $\mathbb{Z}^n$ with the norm $\|\cdot\|_Q$ onto the lattice $\Lambda = L \mathbb{Z}^n$ with the Euclidean norm. The dual lattice is $\Lambda^* = L^{-\top} \mathbb{Z}^n$, and $\|L^{-\top} d\|^2 = d^\top Q^{-1} d$. So $\lambda_1(\Lambda^*) = \|d\|_{Q^{-1}}$ for the vector $d$ of line L8, and $\mu(\Lambda) = \mu$. Banaszczyk's transference theorem states $\lambda_1(\Lambda^*) \, \mu(\Lambda) \le n/2$. With Step 1, $\|d\|_{Q^{-1}} \le n / (2\mu) < n/(2r)$.

*Step 3.* For $w \in \mathbb{R}^n$, Cauchy-Schwarz gives $|d^\top w| = |(L^{-\top} d)^\top (L w)| \le \|d\|_{Q^{-1}} \|w\|_Q$. For $p, p' \in P$ we have $\|p - p'\|_Q \le 2 n^2 r$. So
$$\max_{V} d^\top v - \min_{V} d^\top v < \frac{n}{2r} \cdot 2 n^2 r = n^3.$$
An interval of length less than the integer $n^3$ contains at most $n^3$ integers, so $|K| \le n^3$. $\blacksquare$

**Optimization.** The binary search in `kannan_maximize` is the same as in Lenstra's algorithm: `x` is always a feasible integer point with $c^\top x$ equal to `low`, no feasible integer point has $c^\top x$ above `top`, and the gap decreases in each step.
