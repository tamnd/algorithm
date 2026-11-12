---
title: The Oslo algorithm returns the control points of the same curve on the finer knots
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page: the old knots $\tau_0 \le \cdots \le \tau_{n+p+1}$ with coefficients $c_0, \ldots, c_n$, the fine knots $t_0 \le \cdots \le t_{N+p+1}$, and $f = \sum_i c_i N^\tau_i$ with $N^\tau_i = N^\tau_{i,p}$. The B-splines come from the [Cox-de Boor recursion](/cox-de-boor-recursion/) with half-open spans. A span $[\tau_\nu, \tau_{\nu+1})$ is *nonempty* if $\tau_\nu < \tau_{\nu+1}$, and on a nonempty span $\nu$ with $p \le \nu \le n$ we write $\pi_\nu$ for the polynomial that equals $f$ there. We work with one coordinate of the points, so the $c_i$ are numbers; the claim for points follows coordinate by coordinate.

We use three facts from other pages. Local support: $N^\tau_{i,q}(x) = 0$ for $x \notin [\tau_i, \tau_{i+q+1})$. Marsden's identity on one span, Step 2 of the proof of the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/): with $\psi^\tau_{i,q}(y) = \prod_{l=1}^{q} (y - \tau_{i+l})$, for a nonempty span $\nu$ with $p \le \nu \le n$, all $x \in [\tau_\nu, \tau_{\nu+1})$ and all real $y$,

$$\sum_{i=\nu-p}^{\nu} \psi^\tau_{i,p}(y) \, N^\tau_i(x) = (y - x)^p, \tag{M}$$

and the same for $t$. And the smoothness that the Curry-Schoenberg theorem gives as a corollary: under its conditions, every $f$ in the span of the $N^\tau_i$ is $C^{p-m}$ at an interior knot of multiplicity $m \le p$.

**Claim.** Let $p \ge 1$ and $n \ge p$. Assume the conditions that the implementation checks: $t$ contains $\tau$ as a multiset, every new knot lies in the open interval $(\tau_p, \tau_{n+1})$, $\tau_p < \tau_{p+1}$ and $\tau_n < \tau_{n+1}$, and no knot of $t$ has multiplicity above $p + 1$. Then the points $d_0, \ldots, d_N$ of OSLO-REFINE satisfy

$$\sum_{j=0}^{N} d_j \, N^t_j(x) = f(x) \qquad \text{for } \tau_p \le x < \tau_{n+1}.$$

**Step 0 (the domain does not change).** The new knots are larger than $\tau_p$, so the $p + 1$ smallest entries of $t$ are $\tau_0, \ldots, \tau_p$ and $t_p = \tau_p$. In the same way $t_{N+1} = \tau_{n+1}$.

## Step 1. Blossoms

For a polynomial $\pi$ of degree at most $p$ define $B[\pi](x_1, \ldots, x_p)$ by linearity from $B[x^k] = e_k(x_1, \ldots, x_p) / \binom{p}{k}$, where $e_k$ is the elementary symmetric polynomial of degree $k$. Then $B[\pi]$ is symmetric, affine in each argument, linear in $\pi$, and $B[\pi](x, \ldots, x) = \pi(x)$, because $e_k(x, \ldots, x) = \binom{p}{k} x^k$.

(B1) *Uniqueness.* Let $g$ be a function of $x_1, \ldots, x_p$ that is symmetric, affine in each argument, and has $g(x, \ldots, x) = \pi(x)$. A function that is affine in each argument is a sum $\sum_S a_S \prod_{k \in S} x_k$ over subsets $S$ of $\{1, \ldots, p\}$; this follows by induction on $p$, writing $g = g_0 + x_p g_1$ with $g_0, g_1$ affine in each of $x_1, \ldots, x_{p-1}$. Symmetry makes $a_S$ depend only on $|S| = k$, so $g = \sum_k a_k e_k$. On the diagonal this is $\sum_k a_k \binom{p}{k} x^k = \pi(x)$, which fixes every $a_k$. So $g = B[\pi]$.

(B2) *The power.* $(y - x)^p = \sum_k \binom{p}{k} (-1)^k y^{p-k} x^k$, so $B[(y - x)^p](x_1, \ldots, x_p) = \sum_k (-1)^k y^{p-k} e_k = \prod_{k=1}^{p} (y - x_k)$.

(B3) *A zero.* Let $1 \le m \le p$, let $\pi = (x - \xi)^{p-m+1} g(x)$ with $\deg g \le m - 1$, and let the list $x_1, \ldots, x_p$ contain $\xi$ at least $m$ times. Then $B[\pi](x_1, \ldots, x_p) = 0$. By linearity in $g$ it is enough to take $g = (y - x)^{m-1}$, because these polynomials for $m$ distinct $y$ span the polynomials of degree at most $m - 1$ (the Vandermonde argument of Step 2). For this $g$ let

$$h(x_1, \ldots, x_p) = \frac{1}{p!} \sum_{\sigma} \prod_{k=1}^{p-m+1} (x_{\sigma(k)} - \xi) \prod_{k=p-m+2}^{p} (y - x_{\sigma(k)}),$$

the sum over all permutations $\sigma$. It is symmetric, affine in each argument, because each $x_k$ appears in exactly one factor of each product, and on the diagonal it is $\pi(x)$. By (B1), $h = B[\pi]$. In each product the second group has only $m - 1$ arguments, so at least one copy of $\xi$ falls in the first group, and the product is $0$.

## Step 2. The rows compute blossoms

Let $\mu$ be a nonempty span with $p \le \mu \le n$, and let $x_1, \ldots, x_p$ be reals. Run lines L3 to L8 with $x_r$ in place of $t[j + r]$, and let $\alpha$ be the result. Then

$$\sum_{s=0}^{p} \alpha[s] \, c_{\mu-p+s} = B[\pi_\mu](x_1, \ldots, x_p). \tag{1}$$

*Proof.* After round $r$, index the entries of $\alpha$ by $i = \mu - r + s$, so $\alpha^{(r)}_i$ for $\mu - r \le i \le \mu$, and $\alpha^{(0)}_\mu = 1$. Line L7 for the entry $i' = \mu - r + 1 + s$ of round $r - 1$ uses $a = (x_r - \tau_{i'})/(\tau_{i'+r} - \tau_{i'})$, and the denominator is at least $\tau_{\mu+1} - \tau_\mu > 0$, because $i' \le \mu$ and $i' + r \ge \mu + 1$. Line L8 adds $(1 - a) \alpha^{(r-1)}_{i'}$ to the entry $i' - 1$ and $a \, \alpha^{(r-1)}_{i'}$ to the entry $i'$. The downward order of line L6 makes each step read an entry of round $r - 1$ before it is overwritten. We show by induction on $r$ that for every real $y$

$$\sum_{i=\mu-r}^{\mu} \alpha^{(r)}_i \, \psi^\tau_{i,r}(y) = \prod_{k=1}^{r} (y - x_k).$$

For $r = 0$ both sides are $1$. For round $r$, the left side is $\sum_{i'} \alpha^{(r-1)}_{i'} \bigl( (1 - a) \psi^\tau_{i'-1,r}(y) + a \, \psi^\tau_{i',r}(y) \bigr)$. Since $\psi^\tau_{i'-1,r}(y) = (y - \tau_{i'}) \psi^\tau_{i',r-1}(y)$ and $\psi^\tau_{i',r}(y) = \psi^\tau_{i',r-1}(y) (y - \tau_{i'+r})$, the bracket is $\psi^\tau_{i',r-1}(y) \bigl( y - \tau_{i'} - a (\tau_{i'+r} - \tau_{i'}) \bigr) = \psi^\tau_{i',r-1}(y) (y - x_r)$. The induction hypothesis finishes the step.

Now both sides of (1) are linear functions of $z = (c_{\mu-p}, \ldots, c_\mu)$; the right side because $\pi_\mu = \sum_{i=\mu-p}^{\mu} c_i N^\tau_i$ on the span, by local support. For $z(y) = (\psi^\tau_{\mu-p,p}(y), \ldots, \psi^\tau_{\mu,p}(y))$ the left side is $\prod_k (y - x_k)$ by the induction with $r = p$, and $\pi_\mu = (y - x)^p$ by (M), so the right side is $\prod_k (y - x_k)$ by (B2). For distinct $y_0, \ldots, y_p$, the vectors $z(y_k)$ are a basis of $\mathbb{R}^{p+1}$: if $\sum_k \lambda_k z(y_k) = 0$, then $\sum_k \lambda_k (y_k - x)^p = 0$ on the span by (M), so $\sum_k \lambda_k y_k^r = 0$ for $0 \le r \le p$ by comparing coefficients, and the Vandermonde matrix of distinct $y_k$ is nonsingular. Two linear maps that agree on a basis are equal. $\square$

## Step 3. Blossom values are control points

Let $\nu$ be a nonempty span of $t$ with $p \le \nu \le N$, and let $\pi$ have degree at most $p$. Then for $x \in [t_\nu, t_{\nu+1})$

$$\sum_{j=\nu-p}^{\nu} B[\pi](t_{j+1}, \ldots, t_{j+p}) \, N^t_j(x) = \pi(x). \tag{2}$$

Both sides are linear in $\pi$. For $\pi = (y - x)^p$, (B2) gives the coefficients $\prod_{r=1}^{p} (y - t_{j+r}) = \psi^t_{j,p}(y)$, and (M) for $t$ gives (2). These $\pi$ span all polynomials of degree at most $p$. $\square$

## Step 4. Pieces have equal blossoms at the knots between them

Let $a < b$ be nonempty spans of $\tau$ in $[p, n]$, and let the list $x_1, \ldots, x_p$ contain the knots $\tau_{a+1}, \ldots, \tau_b$, counted with multiplicity. Then $B[\pi_a](x_1, \ldots, x_p) = B[\pi_b](x_1, \ldots, x_p)$.

Go from $a$ to $b$ through the nonempty spans between them. Two consecutive ones, $a' < b'$, are separated by one knot value $\xi = \tau_{a'+1} = \cdots = \tau_{b'}$ of multiplicity $m = b' - a'$, and the list contains $\xi$ at least $m$ times; so $m \le p$. The conditions of the claim are those of the Curry-Schoenberg theorem for $\tau$, so $f$ is $C^{p-m}$ at $\xi$. Hence $\pi_{b'} - \pi_{a'}$ has a zero of order at least $p - m + 1$ at $\xi$ and is $(x - \xi)^{p-m+1} g$ with $\deg g \le m - 1$. By (B3) and linearity, $B[\pi_{b'}] = B[\pi_{a'}]$ at the list. $\square$

## Step 5. Conclusion

Let $\tau_p \le x < \tau_{n+1}$. By Step 0, $x$ lies in a nonempty span $\nu$ of $t$ with $p \le \nu \le N$. Every knot of $\tau$ is a knot of $t$, so $[t_\nu, t_{\nu+1})$ lies in one nonempty span $\nu'$ of $\tau$, with $p \le \nu' \le n$ and $\tau_{\nu'} \le t_\nu$, and $f = \pi_{\nu'}$ there.

Fix $j$ with $\nu - p \le j \le \nu$, and let $\mu$ be the index of line L2. The span $\mu$ of $\tau$ is nonempty: if $\tau_p \le t_j < \tau_{n+1}$ then $\tau_\mu \le t_j < \tau_{\mu+1}$; if $t_j < \tau_p$ then $\mu = p$ and $\tau_p < \tau_{p+1}$; and $t_j \ge \tau_{n+1}$ cannot happen, because $t_j \le t_\nu < t_{N+1} = \tau_{n+1}$. By Step 2, $d_j = B[\pi_\mu](t_{j+1}, \ldots, t_{j+p})$.

Next, $\mu \le \nu'$, because $\tau_\mu \le \max(t_j, \tau_p) \le t_\nu < \tau_{\nu'+1}$. Every knot $\tau_l$ with $\mu < l \le \nu'$ satisfies $t_j < \tau_l \le t_\nu$: the upper bound because $\tau_l \le \tau_{\nu'} \le t_\nu$, the lower bound because $\tau_l \ge \tau_{\mu+1} > t_j$ in the first case of line L2 and $\tau_l \ge \tau_{p+1} > \tau_p > t_j$ in the second. Since $\tau$ is contained in $t$ as a multiset, these knots are among the entries of $t$ with values in $(t_j, t_\nu]$, and these entries have indices $j + 1, \ldots, \nu$, because $t_{\nu+1} > t_\nu$. As $\nu \le j + p$, the knots $\tau_{\mu+1}, \ldots, \tau_{\nu'}$ are contained in the list $t_{j+1}, \ldots, t_{j+p}$. Step 4 gives $d_j = B[\pi_{\nu'}](t_{j+1}, \ldots, t_{j+p})$.

So, by local support for $t$ and by (2) with $\pi = \pi_{\nu'}$,

$$\sum_{j=0}^{N} d_j N^t_j(x) = \sum_{j=\nu-p}^{\nu} B[\pi_{\nu'}](t_{j+1}, \ldots, t_{j+p}) \, N^t_j(x) = \pi_{\nu'}(x) = f(x). \qquad \blacksquare$$

## Remarks

*Rows sum to 1.* Every step of line L8 splits an entry into parts with weights $1 - a$ and $a$, so the sum of $\alpha$ stays $1$.

*Rows are nonnegative.* The knot vector $t$ also satisfies the conditions of the Curry-Schoenberg theorem: $t_{p+1} > t_p$ and $t_N < t_{N+1}$ because the new knots lie strictly inside the domain. So the $N^t_j$ are linearly independent on the domain, and the matrix with $N^\tau_i = \sum_j \alpha_{i}(j) N^t_j$ is unique. Inserting the new knots one at a time by [Boehm knot insertion](/boehm-knot-insertion/) gives such a matrix as a product of matrices with entries in $[0, 1]$. So the rows of the Oslo algorithm are that product, and their entries are nonnegative. The intermediate entries of $\alpha$ need not be, when line L2 clamps $\mu$.

*Cost.* For each $j$, line L2 costs $O(\log n)$, lines L4 to L8 cost $p(p + 1)/2$ steps, and line L9 costs $O(p d)$. The total is $O(N (\log n + p^2 + p d))$, with $O(p)$ extra space for $\alpha$.
