---
title: Boehm's knot insertion leaves the curve unchanged
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The old knot vector is $t_0 \le \cdots \le t_{n+p+1}$; in this proof we call it $\tau$, and we call the new knot vector $t$. The B-splines $N^\tau_i = N^\tau_{i,p}$ and $N^t_j = N^t_{j,p}$ come from the [Cox-de Boor recursion](/cox-de-boor-recursion/), with half-open spans and the rule that a term with a zero denominator is $0$. A span $[\tau_\nu, \tau_{\nu+1})$ is *nonempty* if $\tau_\nu < \tau_{\nu+1}$. We use two facts. Local support: $N^\tau_{i,q}(x) = 0$ for $x \notin [\tau_i, \tau_{i+q+1})$. And Marsden's identity on one span, Step 2 of the proof of the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/): with $\psi^\tau_i(y) = \prod_{r=1}^{p} (y - \tau_{i+r})$, for every nonempty span $\nu$ with $p \le \nu \le n$, every $x \in [\tau_\nu, \tau_{\nu+1})$ and every real $y$,

$$\sum_{i=\nu-p}^{\nu} \psi^\tau_i(y) \, N^\tau_i(x) = (y - x)^p. \tag{M}$$

The same holds for $t$ with $\psi^t_j(y) = \prod_{r=1}^{p} (y - t_{j+r})$.

**Claim.** Let $p \ge 1$, $n \ge p$, $\tau_p \le u < \tau_{n+1}$, and let $u$ have multiplicity at most $p$ in $\tau$. Then BOEHM-INSERT returns a sorted knot vector $t$ of length $n + p + 3$ with the same domain $[\tau_p, \tau_{n+1}]$, and points $Q_0, \ldots, Q_{n+1}$ such that

$$\sum_{j=0}^{n+1} Q_j \, N^t_j(x) = \sum_{i=0}^{n} P_i \, N^\tau_i(x) \qquad \text{for } \tau_p \le x < \tau_{n+1}.$$

Every $Q_j$ is a convex combination of $P_{j-1}$ and $P_j$, or equal to one of them.

**Step 1 (what the lines compute).** Line L1 gives the $\mu$ with $\tau_\mu \le u < \tau_{\mu+1}$. Since $\tau_p \le u < \tau_{n+1}$, we have $p \le \mu \le n$, and the span $\mu$ is nonempty. Line L7 gives $t_j = \tau_j$ for $j \le \mu$, $t_{\mu+1} = u$, and $t_j = \tau_{j-1}$ for $j \ge \mu + 2$; this is sorted, because $\tau_\mu \le u < \tau_{\mu+1}$. So $t_p = \tau_p$, because $p \le \mu$, and $t_{n+2} = \tau_{n+1}$, because $n + 2 \ge \mu + 2$; the domain does not change. Define

$$\beta_j = \begin{cases} 1 & j \le \mu - p, \\ (u - \tau_j)/(\tau_{j+p} - \tau_j) & \mu - p + 1 \le j \le \mu, \\ 0 & j \ge \mu + 1. \end{cases}$$

In the middle case $j \le \mu$ and $j + p \ge \mu + 1$, so $\tau_j \le \tau_\mu \le u < \tau_{\mu+1} \le \tau_{j+p}$; the denominator is positive and $0 \le \beta_j \le 1$. Lines L2, L3 to L5 and L6 then give, for $0 \le j \le n + 1$,

$$Q_j = (1 - \beta_j) P_{j-1} + \beta_j P_j, \tag{1}$$

where a term with weight $0$ is absent; so $P_{-1}$ and $P_{n+1}$ are never used. This proves the last sentence of the claim.

**Step 2 (the Marsden coefficients go to the Marsden coefficients).** For every real $y$ and $0 \le j \le n + 1$,

$$(1 - \beta_j) \, \psi^\tau_{j-1}(y) + \beta_j \, \psi^\tau_j(y) = \psi^t_j(y), \tag{2}$$

with the same convention for absent terms. For $j \le \mu - p$ the knots $t_{j+1}, \ldots, t_{j+p}$ are $\tau_{j+1}, \ldots, \tau_{j+p}$, because $j + p \le \mu$, so $\psi^t_j = \psi^\tau_j$. For $j \ge \mu + 1$ they are $\tau_j, \ldots, \tau_{j+p-1}$, because $j + 1 \ge \mu + 2$, so $\psi^t_j = \psi^\tau_{j-1}$. For $\mu - p + 1 \le j \le \mu$ they are $\tau_{j+1}, \ldots, \tau_\mu$, then $u$, then $\tau_{\mu+1}, \ldots, \tau_{j+p-1}$, so $\psi^t_j(y) = (y - u) \, \pi(y)$ with $\pi(y) = \prod_{r=1}^{p-1} (y - \tau_{j+r})$. On the left side, $\psi^\tau_{j-1}(y) = (y - \tau_j) \pi(y)$ and $\psi^\tau_j(y) = \pi(y) (y - \tau_{j+p})$, so the left side is

$$\pi(y) \bigl( y - \tau_j - \beta_j (\tau_{j+p} - \tau_j) \bigr) = \pi(y) \, (y - u),$$

because $\beta_j (\tau_{j+p} - \tau_j) = u - \tau_j$. This proves (2).

**Step 3 (locality).** Let $\nu$ be a nonempty span of $t$ in the domain, so $p \le \nu \le n + 1$ and $t_\nu < t_{\nu+1}$. Put $\nu' = \nu$ if $\nu \le \mu$ and $\nu' = \nu - 1$ if $\nu \ge \mu + 1$. From the form of $t$ in Step 1: for $\nu < \mu$ the span is $[\tau_\nu, \tau_{\nu+1})$; for $\nu = \mu$ it is $[\tau_\mu, u)$; for $\nu = \mu + 1$ it is $[u, \tau_{\mu+1})$; for $\nu \ge \mu + 2$ it is $[\tau_{\nu-1}, \tau_\nu)$. In all cases $I = [t_\nu, t_{\nu+1})$ lies in the nonempty span $\nu'$ of $\tau$, and $p \le \nu' \le n$.

We show that for $\nu - p \le j \le \nu$ the point $Q_j$ uses only $P_i$ with $\nu' - p \le i \le \nu'$. By (1), $Q_j$ uses $P_{j-1}$ only if $\beta_j < 1$, so only if $j \ge \mu - p + 1$, and it uses $P_j$ only if $\beta_j > 0$, so only if $j \le \mu$. If $\nu \le \mu$, then $\nu' = \nu$ and $j \le \nu$; for $j = \nu - p \le \mu - p$ only $P_{\nu-p}$ is used, and for larger $j$ the indices $j - 1, j$ lie in $[\nu - p, \nu]$. If $\nu \ge \mu + 1$, then $\nu' = \nu - 1$ and $j - 1 \ge \nu - p - 1 = \nu' - p$; for $j = \nu \ge \mu + 1$ only $P_{\nu-1}$ is used, and for smaller $j$ the indices $j - 1, j$ lie in $[\nu' - p, \nu']$.

**Step 4 (equality on one span of t).** Fix $\nu$, $\nu'$ and $I$ as in Step 3, and work with one coordinate of the points, so the $P_i$ are numbers. For $z = (z_{\nu'-p}, \ldots, z_{\nu'}) \in \mathbb{R}^{p+1}$ let $Q_j(z)$ be given by (1) with $z$ in place of $P$; by Step 3 this is defined for $\nu - p \le j \le \nu$. Define two linear maps from $\mathbb{R}^{p+1}$ to functions on $I$:

$$F(z) = \sum_{i=\nu'-p}^{\nu'} z_i \, N^\tau_i, \qquad G(z) = \sum_{j=\nu-p}^{\nu} Q_j(z) \, N^t_j.$$

For a real $y$ let $z(y) = (\psi^\tau_{\nu'-p}(y), \ldots, \psi^\tau_{\nu'}(y))$. By (M) for $\tau$ on the span $\nu'$, $F(z(y)) = (y - x)^p$ on $I$. By (2), $Q_j(z(y)) = \psi^t_j(y)$, so by (M) for $t$ on the span $\nu$, $G(z(y)) = (y - x)^p$ on $I$ too.

Choose distinct reals $y_0, \ldots, y_p$. The vectors $z(y_0), \ldots, z(y_p)$ are linearly independent. If $\sum_k \lambda_k z(y_k) = 0$, then $\sum_k \lambda_k (y_k - x)^p = F(0) = 0$ for all $x \in I$, an interval, so this polynomial in $x$ is zero. Its coefficient of $x^{p-r}$ is $(-1)^{p-r} \binom{p}{r} \sum_k \lambda_k y_k^r$, so $\sum_k \lambda_k y_k^r = 0$ for $0 \le r \le p$. This is a Vandermonde system with distinct $y_k$, so all $\lambda_k = 0$. Hence the $z(y_k)$ are a basis of $\mathbb{R}^{p+1}$. The linear maps $F$ and $G$ agree on a basis, so $F = G$.

**Step 5 (the whole domain).** Let $\tau_p \le x < \tau_{n+1}$. Since $t$ has the same domain, $x$ lies in a nonempty span $\nu$ of $t$ with $p \le \nu \le n + 1$. By local support for $t$, the right side of the claim at $x$ is $\sum_{j=\nu-p}^{\nu} Q_j N^t_j(x) = G(P_{\nu'-p}, \ldots, P_{\nu'})(x)$; Step 3 shows that the $Q_j$ of the algorithm are the $Q_j(z)$ for this $z$. By local support for $\tau$, the left side at $x$ is $\sum_{i=\nu'-p}^{\nu'} P_i N^\tau_i(x) = F(P_{\nu'-p}, \ldots, P_{\nu'})(x)$, because $x$ lies in the span $\nu'$ of $\tau$. Step 4 gives equality, coordinate by coordinate. At the right end $x = \tau_{n+1}$, both curves are defined by the limit from the left, and these limits are equal because the two sides agree on the last nonempty span. $\blacksquare$

**Remarks.** The proof did not use the bound on the multiplicity of $u$. That bound keeps every knot of $t$ at multiplicity at most $p + 1$, so that the B-splines on $t$ are linearly independent on the domain by the Curry-Schoenberg theorem, and then the $Q_j$ are the only control points on $t$ that give the curve. The cost is one search, $p$ weights and $p$ combinations of points in $\mathbb{R}^d$, and the copies of lines L2, L6 and L7: $O(\log n + p d)$ arithmetic and $O((n + p) d)$ in total.
