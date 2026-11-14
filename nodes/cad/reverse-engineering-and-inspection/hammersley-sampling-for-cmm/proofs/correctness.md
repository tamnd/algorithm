---
title: The radical inverse, the net property of the base-2 Hammersley set, its star discrepancy bound (m + 1)/N for N = 2^m, the size of empty disks, and why a sample never overstates the minimum zone
proves: [correctness, termination]
status: full
---

**Setup.** For an integer base $b \ge 2$ and an integer $i \ge 0$ with base-$b$ digits $i = \sum_{j \ge 0} a_j b^j$, $0 \le a_j < b$, the radical inverse is
$$ \varphi_b(i) = \sum_{j \ge 0} a_j \, b^{-j-1} . $$
The $N$-point Hammersley set in dimension $k$ is $P_N = \{ (i/N, \varphi_{b_1}(i), \dots, \varphi_{b_{k-1}}(i)) : 0 \le i < N \}$ with $b_1, b_2, \dots$ the first primes. For a set $P$ of $N$ points in $[0, 1)^k$, the star discrepancy is
$$ D^*_N(P) = \sup_{y \in [0, 1]^k} \Bigl\lvert \frac{\#\{x \in P : x \in [0, y)\}}{N} - \prod_{j} y_j \Bigr\rvert , $$
where $[0, y)$ is the box $[0, y_1) \times \dots \times [0, y_k)$.

**Lemma 1 (the radical inverse).** The code returns $\varphi_b(i)$, and it stops after $\lfloor \log_b i \rfloor + 1$ steps for $i \ge 1$. If $i < b^m$, then $\varphi_b(i) = r/b^m$, where $r$ is the integer whose $m$ base-$b$ digits are those of $i$ in reverse order. So $\varphi_b$ maps $\{0, \dots, b^m - 1\}$ one to one onto $\{0, 1/b^m, \dots, (b^m - 1)/b^m\}$, and $0 \le \varphi_b(i) < 1$ for all $i$.

*Proof.* The loop takes the digits $a_0, a_1, \dots$ of $i$ from the least significant one by `divmod`, and keeps $\mathrm{num}/\mathrm{den}$ with $\mathrm{num} = a_0 b^{t-1} + a_1 b^{t-2} + \dots + a_{t-1}$ and $\mathrm{den} = b^t$ after $t$ steps, which is $\sum_{j < t} a_j b^{-j-1}$. It stops when the quotient is $0$, after the number of digits of $i$. If $i < b^m$, pad its digits to length $m$; then $b^m \varphi_b(i) = \sum_{j < m} a_j b^{m-1-j}$, which is the integer with the digits in reverse order. Reversal of $m$ digits is a bijection of $\{0, \dots, b^m - 1\}$, and $r \le b^m - 1$ gives $\varphi_b(i) < 1$. $\square$

**Lemma 2 (the net property).** Let $N = 2^m$ and $k = 2$ with base $2$. For every $j$ with $0 \le j \le m$ and all integers $0 \le a < 2^j$, $0 \le c < 2^{m-j}$, the box
$$ E = \bigl[ a 2^{-j}, (a+1) 2^{-j} \bigr) \times \bigl[ c 2^{-(m-j)}, (c+1) 2^{-(m-j)} \bigr) $$
of area $2^{-m}$ holds exactly one point of $P_N$.

*Proof.* Write $i$ with $m$ binary digits. The first coordinate $i/2^m$ lies in $[a 2^{-j}, (a+1) 2^{-j})$ exactly when the $j$ leading digits of $i$ form the number $a$. By Lemma 1, $\varphi_2(i) = \sum_{t < m} a_t 2^{-t-1}$, so its first $m - j$ binary digits after the point are $a_0, \dots, a_{m-j-1}$, the $m - j$ trailing digits of $i$; and $\varphi_2(i)$ lies in $[c 2^{-(m-j)}, (c+1) 2^{-(m-j)})$ exactly when those digits, read in this order, form $c$. The leading $j$ digits and the trailing $m - j$ digits are disjoint and together are all $m$ digits, so exactly one $i < 2^m$ meets both conditions. $\square$

A set with this property is a $(0, m, 2)$-net in base $2$ in Niederreiter's terms.

**Theorem 3 (discrepancy for N = 2^m).** For $N = 2^m$, the base-2 Hammersley set has $D^*_N(P_N) \le (m + 1)/N$.

*Proof.* Fix $y = (x, z) \in [0, 1]^2$ and let $A$ be the number of points in $[0, x) \times [0, z)$. Write $x = \sum_{j \ge 1} x_j 2^{-j}$ in binary, and let $s_j = \sum_{t < j} x_t 2^{-t}$. Then $[0, x)$ is the disjoint union of the intervals $I_j = [s_j, s_j + 2^{-j})$ for the $j \le m$ with $x_j = 1$, and a rest $I_\infty = [s_{m+1}, x)$ of length less than $2^{-m}$. Each $I_j$ has the form $[a 2^{-j}, (a+1) 2^{-j})$.

Consider one strip $I_j \times [0, z)$ with $j \le m$. Split $[0, z)$ into $q = \lfloor z 2^{m-j} \rfloor$ intervals of length $2^{-(m-j)}$ and a rest $R$ of length less than $2^{-(m-j)}$. Each of the $q$ boxes is a box $E$ of Lemma 2, so it holds one point and has area $2^{-m}$: count and $N$ times area agree there. The rest $I_j \times R$ lies inside one box $E$ (or is empty when $z = 1$ and $R$ is empty), so it holds $0$ or $1$ point and has area in $[0, 2^{-m})$; there the count and $N$ times the area differ by less than $1$. The strip $I_\infty \times [0, z)$ lies inside a column $[a 2^{-m}, (a+1) 2^{-m}) \times [0, 1)$, a box $E$ with $j = m$, so the same holds for it.

Add over the at most $m$ strips $I_j$ and the strip $I_\infty$: $\lvert A - N x z \rvert < m + 1$. Divide by $N$ and take the supremum over $y$. $\square$

The exact values for $m = 0, \dots, 6$ are $1, \frac34, \frac12, \frac5{16}, \frac{11}{64}, \frac{25}{256}, \frac{55}{1024}$, so $N D^*_N$ is $1, 1.5, 2, 2.5, 2.75, 3.125, 3.4375$, below $m + 1$. They are computed by the brute force of Lemma 4 in the tests.

**The general bound (cited).** Niederreiter (1992, Theorem 3.8) proves that the $N$-point Hammersley set in dimension $k \ge 2$ with pairwise coprime bases $b_1, \dots, b_{k-1}$ has
$$ D^*_N(P_N) < \frac{k}{N} + \frac{1}{N} \prod_{t=1}^{k-1} \Bigl( \frac{b_t - 1}{2 \log b_t} \log N + \frac{b_t + 1}{2} \Bigr) = O\Bigl( \frac{(\log N)^{k-1}}{N} \Bigr), $$
with the leading constant $\prod_t (b_t - 1)/(2 \log b_t)$. For $k = 2$ and $b_1 = 2$ it reads $D^*_N < \frac{7}{2N} + \frac{\log N}{2 N \log 2}$, for every $N$, not only powers of $2$. At $N = 2^m$ this is $(m/2 + 7/2)/N$, which is sharper than Theorem 3 for $m \ge 6$. This file does not prove the general bound; the tests check it against the exact discrepancy for $N \le 48$ in two dimensions and for small $N$ in three.

**Lemma 4 (the brute force is exact).** For $N$ points in $[0, 1)^2$, let $X$ be the set of first coordinates together with $1$, and $Z$ likewise. Then
$$ D^*_N = \max_{x \in X, \; z \in Z} \max\Bigl( xz - \frac{A^{\circ}(x, z)}{N}, \; \frac{\bar A(x, z)}{N} - xz \Bigr), $$
where $A^{\circ}$ counts the points with $p < x, q < z$ and $\bar A$ the points with $p \le x, q \le z$.

*Proof.* If $x = 0$ or $z = 0$, the box is empty and has area $0$. Otherwise let $x' < x''$ be consecutive values of $X \cup \{0\}$ with $x \in (x', x'']$, and $z', z''$ likewise. No coordinate lies strictly between $x'$ and $x''$, so a point has $p < x$ exactly when $p < x''$, and exactly when $p \le x'$; the same holds for $z$. So on the cell the count $A$ of $[0, x) \times [0, z)$ is constant and equals both $A^{\circ}(x'', z'')$ and $\bar A(x', z')$. On the cell, $xz - A/N$ is largest at $(x'', z'')$, which is a candidate of the first kind. And $A/N - xz$ has the supremum $\bar A(x', z')/N - x' z'$, approached as $(x, z) \to (x', z')$ from above; if $x' = 0$ or $z' = 0$ and $0$ is not a coordinate, this value is $0$, and otherwise $(x', z')$ is a candidate of the second kind. Every candidate value is attained or approached by local discrepancies, so the maximum equals the supremum. $\square$

**Lemma 5 (empty disks).** If an open disk of radius $\rho$ inside $[0, 1)^2$ holds no point of $P$, then $\rho \le \sqrt{2 D^*_N(P)}$.

*Proof.* For a box $B = [u, u') \times [v, v')$, the count of $B$ is $A(u', v') - A(u, v') - A(u', v) + A(u, v)$ in terms of the counts of anchored boxes, and the area is the same signed sum of the four products. Each of the four terms has an error of at most $N D^*_N$, so the count of $B$ differs from $N$ times its area by at most $4 N D^*_N$. The disk contains half-open squares of side $s$ for every $s < \sqrt 2 \rho$, which are empty, so $s^2 \le 4 D^*_N$ for all such $s$, and $2 \rho^2 \le 4 D^*_N$. $\square$

So the Hammersley set leaves no hole larger than $\sqrt{2(m+1)/N}$ for $N = 2^m$. This is weaker than the centered $\sqrt N \times \sqrt N$ grid, whose largest empty disk has the radius $1/\sqrt{2N}$. Low discrepancy is a statement about averages over boxes, not about the worst gap.

**Lemma 6 (a sample never overstates the minimum zone).** Let $S$ be the surface of a part and $Q \subset S$ the sampled points. For every form tolerance whose zone is a region that must hold the points, the minimum zone width of $Q$ is at most that of $S$.

*Proof.* Every zone that holds $S$ holds $Q$, so the minimum over the zones that hold $Q$ is over a larger set. $\square$

So a sample can only underestimate the minimum zone form error, and the gap is the error of the sampling. By Lemma 5, a parameter point at distance at least $\rho$ from the edge of the domain has a sample at a distance of at most $\rho = \sqrt{2 D^*_N}$. So when the deviation from the nominal surface is Lipschitz in the parameters with the constant $\lambda$, the sample underestimates the deviation of a peak away from the edge by at most $\lambda \rho$.

**Least-squares references (cited).** The least-squares plane of points spread over a patch depends on the mean and covariance of the points, which are averages of polynomials of the coordinates. For a parameterization $S(u, v)$ with constant area element, these averages are quadrature sums of integrals over the patch, and the [Koksma-Hlawka inequality](/koksma-hlawka-inequality/) bounds their errors by $V(f) D^*_N$, with $V$ the variation of the integrand in the sense of Hardy and Krause. This is why a low discrepancy helps the least-squares fit, while Lemma 5 is what matters for the minimum zone.

**Lemma 7 (the mapped points).** On a rectangle $[x_0, x_0 + w) \times [y_0, y_0 + h)$, the affine map $(u, v) \mapsto (x_0 + u w, y_0 + v h)$ sends each anchored box of the unit square to an anchored box of the rectangle with the same fraction of the area, so the mapped points have the same star discrepancy relative to the rectangle. On a patch $S(u, v)$, the points are even in the parameters, and even on the surface only when the area element $\lvert S_u \times S_v \rvert$ is constant.

*Proof.* The map is a bijection of boxes to boxes that multiplies all areas by $w h$ and keeps the counts. For a patch, the area of the image of a region $U$ is $\int_U \lvert S_u \times S_v \rvert \, du \, dv$, which is a constant times the area of $U$ for every $U$ exactly when the area element is constant. $\square$

**Termination.** The main loop runs $N$ times, and each radical inverse stops by Lemma 1. The brute-force discrepancy loops over at most $(N + 1)^2$ corners.
