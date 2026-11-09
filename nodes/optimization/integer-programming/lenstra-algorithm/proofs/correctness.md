---
title: Lenstra's algorithm finds an integer point exactly when one exists
proves: [correctness]
status: full
---

**Statement.** Let $P = \{x \in \mathbb{R}^n : A x \le b\}$ be a bounded rational polyhedron. Then LENSTRA$(A, b)$ terminates. It returns a point of $P \cap \mathbb{Z}^n$ if this set is not empty, and NONE otherwise. At each call that reaches line L10, the set $K$ has at most $n^2 2^{n/2} + 1$ elements.

The proof uses induction on $n$. For $n = 0$, the polyhedron is $\mathbb{R}^0 = \{()\}$ if $0 \le b$ and empty otherwise, and line L1 returns the right answer. Let $n \ge 1$ and assume the statement for $n - 1$.

**Lemma 1 (slices).** Let $d \in \mathbb{Z}^n$ have entries with greatest common divisor 1, and let $W$ be an integer matrix with $\det W = \pm 1$ and $d^\top W = e_1^\top$. For each integer $k$, the map $z \mapsto W(k, z)$ is a bijection from $\{z \in \mathbb{Z}^{n-1} : A' z \le b - k a'\}$ onto $\{x \in P \cap \mathbb{Z}^n : d^\top x = k\}$, where $a'$ is the first column of $A W$ and $A'$ is $A W$ without its first column.

*Proof.* Since $W$ is unimodular, $W^{-1}$ is an integer matrix too, so $x \mapsto W^{-1} x$ is a bijection of $\mathbb{Z}^n$. For $x = W u$ we have $d^\top x = e_1^\top u = u_1$ and $A x = A W u = u_1 a' + A' (u_2, \dots, u_n)$. So $x$ is an integer point of $P$ with $d^\top x = k$ exactly when $u = (k, z)$ with $z \in \mathbb{Z}^{n-1}$ and $A' z \le b - k a'$. $\square$

The polyhedron $\{z : A' z \le b - k a'\}$ is the image of a bounded set under a linear map, so it is bounded, and the induction hypothesis applies to it. By Lemma 1, SLICE$(A, b, d, K)$ returns an integer point of $P$ if some integer point $x$ of $P$ has $d^\top x \in K$, and NONE otherwise.

**Lemma 2 (flat case).** If line L3 runs, every integer point of $P$ satisfies $d^\top x = \delta$.

*Proof.* $P$ is the convex hull of $V$, because it is a bounded polyhedron. The vector $d$ is orthogonal to all differences of points of $V$, so $d^\top v = \delta$ for all $v \in V$, and then $d^\top x = \delta$ for all $x \in P$. If $\delta \notin \mathbb{Z}$, no integer point $x$ has $d^\top x = \delta$, since $d$ is an integer vector. $\square$

So line L3 returns the right answer, by Lemma 1 with $K = \{\delta\}$. Line L8 returns a point of $P \cap \mathbb{Z}^n$. At line L10, every integer point $x$ of $P$ has $d^\top x \in \mathbb{Z}$ (we show below that $d$ is an integer vector) and $\min_V d^\top v \le d^\top x \le \max_V d^\top v$, because a linear function on a polytope takes its extreme values at vertices. So $d^\top x \in K$, and line L10 returns the right answer by Lemma 1. Line L2 returns NONE only if $P$ is empty. This proves the correctness part. Termination follows because each call in dimension $n$ makes finitely many calls in dimension $n - 1$.

It remains to prove the bound on $|K|$. Assume that the call reaches line L10. Then $P$ has a nonempty interior, $S$ has vertices $v_0, \dots, v_n$ and positive volume, and $y \notin P$.

**Lemma 3 (the regular simplex).** Let $\|x\|_Q^2 = x^\top Q x$ with $Q = T^\top G T$ as in line L5. In this norm $S$ is a regular simplex with edge 1. Its barycenter $c$ is at distance $r = 1/\sqrt{2n(n+1)}$ from each facet, and at distance $\sqrt{n/(2(n+1))} = n r$ from each vertex.

*Proof.* The map $x \mapsto T(x - v_0)$ sends $v_0, v_1, \dots, v_n$ to $0, e_1, \dots, e_n$. For $i \ne j$ we have $\|e_i\|_G^2 = 1$ and $\|e_i - e_j\|_G^2 = 1 + 1 - 2 \cdot \frac12 = 1$, so all edges have length 1. In a regular simplex of edge 1 in dimension $n$, the distance from the barycenter to a vertex is $R = \sqrt{n/(2(n+1))}$ and the distance to a facet is $R / n$, because the barycenter divides each median in the ratio $n : 1$. With $R / n = 1/\sqrt{2n(n+1)} = r$ we get $R = n r$. $\square$

So the ball $B_Q(c, r) = \{x : \|x - c\|_Q \le r\}$ lies in $S \subseteq P$.

**Lemma 4 (maximum volume).** $P \subseteq B_Q(c, n^2 r)$.

*Proof.* Let $p \in P$ and write $p = \sum_{i} \lambda_i v_i$ with $\sum_i \lambda_i = 1$ (barycentric coordinates with respect to $S$). If we replace $v_i$ by $p$ in $S$, the volume is multiplied by $|\lambda_i|$. As a function of $p$ with the other vertices fixed, this volume is the absolute value of an affine function, so it is convex, and its maximum over the polytope $P$ is taken at a point of $V$. By the choice of $S$ in line L4, this maximum is at most the volume of $S$, so $|\lambda_i| \le 1$ for all $i$. Let $\mu_i = (1 - \lambda_i)/n$. Then $\mu_i \ge 0$ because $\lambda_i \le 1$, and $\sum_i \mu_i = (n + 1 - 1)/n = 1$. So $q = \sum_i \mu_i v_i \in S$, and
$$c - n(q - c) = (n + 1) c - \sum_i (1 - \lambda_i) v_i = \sum_i v_i - \sum_i v_i + \sum_i \lambda_i v_i = p,$$
using $(n+1) c = \sum_i v_i$. Since $q \in S$, Lemma 3 gives $\|q - c\|_Q \le n r$, so $\|p - c\|_Q = n \|q - c\|_Q \le n^2 r$. $\square$

**Lemma 5 (the LLL basis).** Let $b_1, \dots, b_n$ be the LLL-reduced basis of line L6, with Gram-Schmidt vectors $b_i^*$ in the inner product of $Q$. Then $\|b_n^*\|_Q > 2 r / 2^{n/2}$.

*Proof.* The LLL conditions with $\delta = 3/4$ give $\|b_{i+1}^*\|_Q^2 \ge \frac12 \|b_i^*\|_Q^2$, so $\|b_i^*\|_Q^2 \le 2^{n-i} \|b_n^*\|_Q^2$ (LLL 1982, Proposition 1.6 and its proof). The nearest plane point satisfies $\|y - c\|_Q^2 \le \frac14 \sum_i \|b_i^*\|_Q^2$ (Babai 1986). Since $y \notin P$ and $B_Q(c, r) \subseteq P$, we have $\|y - c\|_Q > r$. So
$$r^2 < \tfrac14 \sum_{i=1}^n 2^{n-i} \|b_n^*\|_Q^2 < \tfrac14 \, 2^n \|b_n^*\|_Q^2,$$
which gives $\|b_n^*\|_Q > 2 r / 2^{n/2}$. $\square$

**Lemma 6 (the direction).** Let $B$ have the columns $b_1, \dots, b_n$ and let $d^\top$ be the last row of $B^{-1}$. Then $d \in \mathbb{Z}^n$ and $|d^\top w| \le \|w\|_Q / \|b_n^*\|_Q$ for all $w \in \mathbb{R}^n$.

*Proof.* $B$ is an integer matrix with $\det B = \pm 1$, so $B^{-1}$ is an integer matrix and $d$ is an integer vector. Write $w = \sum_i \alpha_i b_i$; then $d^\top w = \alpha_n$, because $B^{-1} w = \alpha$. In the Gram-Schmidt basis, $w = \sum_i \beta_i b_i^*$ with $\beta_n = \alpha_n$, since each $b_i$ with $i < n$ lies in the span of $b_1^*, \dots, b_{n-1}^*$ and $b_n = b_n^* + (\text{a vector in that span})$. The vectors $b_i^*$ are orthogonal in the inner product of $Q$, so $\|w\|_Q \ge |\beta_n| \, \|b_n^*\|_Q = |d^\top w| \, \|b_n^*\|_Q$. $\square$

**The bound on $|K|$.** For $p, p' \in P$, Lemma 4 gives $\|p - p'\|_Q \le 2 n^2 r$. By Lemmas 5 and 6,
$$d^\top p - d^\top p' \le \frac{2 n^2 r}{\|b_n^*\|_Q} < \frac{2 n^2 r \, 2^{n/2}}{2 r} = n^2 2^{n/2}.$$
So the interval $[\min_V d^\top v, \max_V d^\top v]$ has length less than $n^2 2^{n/2}$, and it contains at most $n^2 2^{n/2} + 1$ integers. $\blacksquare$

**Optimization.** In `lenstra_maximize`, the binary search keeps two invariants: `x` is an integer point of $P$ with $c^\top x = $ `low`, and no integer point of $P$ has $c^\top x > $ `top`. The first holds after the first call and after each successful call. The second holds at the start because $c^\top x \le \max_V c^\top v$ on $P$ and $c^\top x$ is an integer, and after each NONE answer for $c^\top x \ge$ `mid`. The gap `top` $-$ `low` decreases in each step, so the search ends with `low` $=$ `top`, and `x` is optimal.
