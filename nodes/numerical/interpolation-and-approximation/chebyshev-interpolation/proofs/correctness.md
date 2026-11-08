---
title: Correctness of Chebyshev interpolation
proves: [correctness, aliasing]
status: full
---

Write $x_j = \cos(j\pi/n)$ for $j = 0, \ldots, n$ with $n \ge 1$, and $\theta_j = j\pi/n$, so that $T_k(x_j) = \cos(k\theta_j)$. The sum $\sum''_{j=0}^n g_j$ means $\frac12 g_0 + g_1 + \cdots + g_{n-1} + \frac12 g_n$.

**Claim 1 (a cosine sum).** For an integer $m$, $S(m) = \sum''_{j=0}^n \cos(jm\pi/n)$ equals $n$ if $m$ is a multiple of $2n$ and $0$ otherwise.

*Proof.* If $m = 2nq$, every term is $1$ and the weighted count is $n$. Otherwise put $z = e^{im\pi/n} \ne 1$ and $z^n = (-1)^m$. Then $\sum_{j=0}^{n-1} z^j = (1 - (-1)^m)/(1 - z)$, and $S(m)$ is the real part of $\sum_{j=0}^{n-1} z^j + \frac12((-1)^m - 1)$. If $m$ is even this is $0 + 0$. If $m$ is odd it is $\operatorname{Re}\,\frac{2}{1 - z} - 1$, and $\operatorname{Re}\,\frac{1}{1 - z} = \frac12$ for every $|z| = 1$, $z \ne 1$, so $S(m) = 0$. $\square$

**Claim 2 (discrete orthogonality).** For $0 \le k, m \le n$,
$$\sum''_j T_k(x_j)T_m(x_j) = \begin{cases} 0 & k \ne m, \\ n/2 & k = m \notin \{0, n\}, \\ n & k = m \in \{0, n\}. \end{cases}$$

*Proof.* $\cos k\theta \cos m\theta = \frac12(\cos(k - m)\theta + \cos(k + m)\theta)$, so the sum is $\frac12(S(k - m) + S(k + m))$. For $0 \le k, m \le n$, $k - m$ is a multiple of $2n$ only when $k = m$, and $k + m \in [0, 2n]$ is a multiple of $2n$ only when $k = m = 0$ or $k = m = n$. Claim 1 gives the three cases. $\square$

**Claim 3 (lines L1 to L3 give the interpolant).** Let $v_j = f(\frac{a+b}2 + \frac{b-a}2 x_j)$ be the samples of line L1, and $c_k$ the numbers produced by lines L2 and L3. Then $p_n = \sum_{k=0}^n c_k T_k$ satisfies $p_n(x_j) = v_j$ for all $j$, and it is the unique such polynomial of degree at most $n$.

*Proof.* The $n + 1$ points are distinct, since $\cos$ is strictly decreasing on $[0, \pi]$, so a unique interpolant $q$ of degree at most $n$ exists, and it has an expansion $q = \sum_m d_m T_m$ because $T_0, \ldots, T_n$ form a basis of the polynomials of degree at most $n$. Multiply $q(x_j) = v_j$ by $T_k(x_j)$ and apply $\sum''_j$. By Claim 2, $\sum''_j v_j T_k(x_j) = d_k \cdot n/2$ for $0 < k < n$ and $d_k \cdot n$ for $k \in \{0, n\}$. Line L2 computes $\frac2n\sum''_j v_j \cos(jk\pi/n)$, which is $d_k$ for $0 < k < n$ and $2d_k$ for $k \in \{0, n\}$; line L3 halves the latter. So $c_k = d_k$ for all $k$. $\square$

**Claim 4 (lines L4 to L6 evaluate $p_n$).** Line L4 maps $t \in [a, b]$ to $x \in [-1, 1]$ by the inverse of the map used in line L1, so $p_n(x)$ is the interpolant's value at $t$. With $b_{n+1} = b_{n+2} = 0$ and $b_k = c_k + 2xb_{k+1} - b_{k+2}$ for $k = n, \ldots, 1$, we have $\sum_{k=0}^n c_kT_k(x) = c_0 + xb_1 - b_2$.

*Proof.* Substitute $c_k = b_k - 2xb_{k+1} + b_{k+2}$ for $k \ge 1$:
$$\sum_{k=1}^n c_kT_k = \sum_{k=1}^n b_kT_k - 2x\sum_{k=2}^{n+1} b_kT_{k-1} + \sum_{k=3}^{n+2} b_kT_{k-2}.$$
Collect the coefficient of $b_k$. For $3 \le k \le n$ it is $T_k - 2xT_{k-1} + T_{k-2} = 0$ by the recurrence; the terms with $k = n+1, n+2$ vanish because those $b_k$ are $0$. What remains is $b_1T_1 + b_2(T_2 - 2xT_1) = b_1x - b_2$, using $T_1 = x$ and $T_2 - 2xT_1 = -T_0 = -1$. Adding $c_0T_0 = c_0$ gives the claim. For $n = 1$ the same computation holds with $b_2 = 0$. $\square$

**Claim 5 (aliasing).** For integers $q \ge 0$ and $0 \le k \le n$, $T_{2qn + k}(x_j) = T_{2qn - k}(x_j) = T_k(x_j)$ when $2qn - k \ge 0$. Hence if $f = \sum_{m \ge 0} a_mT_m$ with $\sum|a_m| < \infty$, then $c_k = a_k + \sum_{q \ge 1}(a_{2qn - k} + a_{2qn + k})$ for $0 < k < n$, while $c_0 = a_0 + \sum_{q \ge 1}a_{2qn}$ and $c_n = \sum_{q \ge 0}a_{(2q+1)n}$.

*Proof.* $\cos((2qn \pm k)j\pi/n) = \cos(2qj\pi \pm kj\pi/n) = \cos(kj\pi/n)$. So on the points $f$ agrees with the polynomial obtained by replacing each $T_m$ by the $T_k$ it coincides with; absolute convergence allows the rearrangement. By Claim 3 the coefficients of the interpolant are those of that polynomial. For $0 < k < n$ the indices $m$ with $T_m = T_k$ on the points are exactly $m \equiv \pm k \pmod{2n}$, and for $k = 0$ and $k = n$ the two residues coincide, which gives the stated sums. $\square$

**Claim 6 (termination and cost).** Lines L1 to L3 run fixed loops of $n + 1$ and $(n+1)^2$ iterations, and line L5 runs $n$ iterations, so the algorithm terminates. The adaptive driver doubles $n$ and stops at the first $n$ whose trailing coefficients pass the test, or at the cap, so it runs at most $\log_2(\text{cap}/8) + 1$ stages. $\square$

Claims 3 and 4 together show that the procedure returns the values of the unique polynomial of degree at most $n$ that interpolates $f$ at the mapped Chebyshev points.
