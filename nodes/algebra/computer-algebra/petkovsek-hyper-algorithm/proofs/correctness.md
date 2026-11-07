---
title: Hyper returns exactly the hypergeometric solutions
proves: [correctness, termination]
status: full
---

Let $K$ be a field of characteristic $0$ and $L = \sum_{i=0}^{r} p_i(n) S^i$ with $p_i \in K[n]$, $r \ge 1$, $p_0 \ne 0$ and $p_r \ne 0$. A hypergeometric term $t$ is eventually nonzero with $t(n + 1) = R(n)\, t(n)$ for a rational $R \in K(n)$ and all large $n$.

**Lemma 1 (Gosper-Petkovšek form).** Every nonzero $R \in K(n)$ can be written $R = Z \frac{a(n)}{b(n)} \frac{c(n + 1)}{c(n)}$ with $Z \in K \setminus \{0\}$, monic $a, b, c \in K[n]$, $\gcd(a(n), b(n + h)) = 1$ for all integers $h \ge 0$, $\gcd(a(n), c(n)) = 1$ and $\gcd(b(n), c(n + 1)) = 1$. This is the lemma of Petkovšek (1992) and of A = B, Chapter 5. Its proof uses only gcds over $K$ and the integer roots of a resultant, so $a, b, c$ and $Z$ lie in $K$.

**Lemma 2 (the key identity).** For $R$ in the form of Lemma 1 and $P_i = p_i(n) \prod_{j=0}^{i-1} a(n + j) \prod_{j=i}^{r-1} b(n + j)$,

$$c(n) \prod_{j=0}^{r-1} b(n + j) \cdot \sum_{i=0}^{r} p_i(n) \prod_{k=0}^{i-1} R(n + k) = \sum_{i=0}^{r} Z^i P_i(n)\, c(n + i).$$

*Proof.* $\prod_{k<i} R(n + k) = Z^i \prod_{k<i} \frac{a(n + k)}{b(n + k)} \cdot \frac{c(n + i)}{c(n)}$, because the factors $c(n + k + 1)/c(n + k)$ telescope. Multiplying by $c(n) \prod_{j<r} b(n + j)$ cancels $c(n)$ and $\prod_{k<i} b(n + k)$, and leaves $\prod_{j=i}^{r-1} b(n + j)$. $\square$

If $t$ has ratio $R$, then $(L t)(n) = t(n) \sum_i p_i(n) \prod_{k<i} R(n + k)$. So for eventually nonzero $t$, $L t = 0$ holds if and only if the rational function $\sum_i p_i \prod_{k<i} R(n + k)$ is zero, if and only if the right side of Lemma 2 is the zero polynomial.

**Termination.** $p_0$ and $p_r(n - r + 1)$ have finitely many monic factors. For each pair, $\sum \alpha_i Z^i$ is a nonzero polynomial, because $\alpha_i \ne 0$ for some $i$ by the choice of $m$, so it has at most $r$ roots. Line L6 solves one finite linear system, by Lemma 4. So the algorithm stops.

**Soundness.** Let a ratio $R = Z a(n) c(n + 1)/(b(n) c(n))$ be output, with $c \ne 0$ from line L6. Then $\sum_i Z^i P_i(n) c(n + i) = 0$, and Lemma 2 holds for this $R$ even if the gcd conditions fail, since its proof used none of them. Since $c(n) \prod_j b(n + j)$ is a nonzero polynomial, $\sum_i p_i \prod_{k<i} R(n + k) = 0$ as a rational function. Define $t(n_0) = 1$ and $t(n + 1) = R(n) t(n)$ for $n \ge n_0$, where $n_0$ exceeds every integer root of the numerator and denominator of $R$. Then $t$ is a hypergeometric solution.

**Lemma 3 (the necessary conditions).** If $t$ is a hypergeometric solution with ratio $R$ in the form of Lemma 1, with $\deg c = \delta$, then $a(n) \mid p_0(n)$, $b(n) \mid p_r(n - r + 1)$, $\sum_i \alpha_i Z^i = 0$ for the $\alpha_i$ of line L4, and $c$ solves $\sum_i Z^i P_i(n) c(n + i) = 0$.

*Proof.* The last claim is Lemma 2 with $L t = 0$. In $\sum_i Z^i P_i(n) c(n + i) = 0$, each term with $i \ge 1$ contains the factor $a(n)$. So $a(n)$ divides $P_0(n) c(n) = p_0(n) \prod_{j=0}^{r-1} b(n + j)\, c(n)$. By Lemma 1, $a(n)$ is coprime to each $b(n + j)$ with $j \ge 0$ and to $c(n)$, so $a(n) \mid p_0(n)$. Each term with $i \le r - 1$ contains the factor $b(n + r - 1)$, so it divides $P_r(n) c(n + r) = p_r(n) \prod_{j=0}^{r-1} a(n + j)\, c(n + r)$. Here $\gcd(b(n + r - 1), a(n + j)) = 1$ for $0 \le j \le r - 1$: substituting $n \mapsto n - j$, it is $\gcd(a(n), b(n + h))$ with $h = r - 1 - j \ge 0$. And $\gcd(b(n + r - 1), c(n + r)) = 1$ is the shift of $\gcd(b(n), c(n + 1)) = 1$. So $b(n + r - 1) \mid p_r(n)$, that is, $b(n) \mid p_r(n - r + 1)$. Finally, $c$ is monic of degree $\delta$, so $c(n + i)$ has leading term $n^\delta$ for every $i$, and the coefficient of $n^{m + \delta}$ in the sum is $\sum_i Z^i \alpha_i$, which must be $0$. $Z \ne 0$ because $R \ne 0$. $\square$

**Lemma 4 (degree bound).** Let $Q_0, \ldots, Q_r \in K[n]$, not all zero, and $R_k = \sum_{i \ge k} \binom{i}{k} Q_i$. Let $b^\ast = \max \{ \deg R_k - k : R_k \ne 0 \}$ and $\varphi(\delta) = \sum_{k : \deg R_k - k = b^\ast} \operatorname{lc}(R_k)\, \delta(\delta - 1) \cdots (\delta - k + 1)$. Every nonzero polynomial solution $c$ of $\sum_i Q_i(n) c(n + i) = 0$ has a degree $\delta$ with $\varphi(\delta) = 0$.

*Proof.* Some $R_k$ is nonzero: the map from $(Q_i)$ to $(R_k)$ is triangular with $1$ on the diagonal, so it is invertible. With $E c(n) = c(n + 1)$ and $\Delta = E - 1$, the binomial theorem $E^i = \sum_k \binom{i}{k} \Delta^k$ gives $\sum_i Q_i E^i = \sum_k R_k \Delta^k$. For $c$ of degree $\delta$, $\Delta^k c$ has degree $\delta - k$ and leading coefficient $\delta(\delta - 1) \cdots (\delta - k + 1) \operatorname{lc}(c)$ when $k \le \delta$, and is $0$ when $k > \delta$, where the product also vanishes. So $R_k \Delta^k c$ has degree at most $\deg R_k + \delta - k \le b^\ast + \delta$, and the coefficient of $n^{b^\ast + \delta}$ in the sum is $\operatorname{lc}(c)\, \varphi(\delta)$, which must be $0$. The polynomial $\varphi$ is nonzero, since the falling factorials of distinct degrees $k$ are linearly independent and their coefficients $\operatorname{lc}(R_k)$ are nonzero. $\square$

So with $D$ the largest nonnegative integer root of $\varphi$, the solutions of degree at most $D$ are all the polynomial solutions, and they are the kernel of a linear map on the coefficient vectors $(c_0, \ldots, c_D)$. Line L6 computes a basis $c_1, \ldots, c_s$ of this kernel.

**Completeness.** Let $t$ be a hypergeometric solution with ratio $R \in K(n)$, and write $R$ in the form of Lemma 1. By Lemma 3 the pair $(a, b)$ is tried at line L2 and $Z$ is found at line L5, provided the factorizations of $p_0$ and $p_r(n - r + 1)$ and the roots are taken over $K$. Also by Lemma 3, $c = \sum_j \lambda_j c_j$ for the basis of line L6. Choose $n_0$ beyond all integer roots of $a$, $b$, $c$ and the $c_j$, and let $A(n) = \prod_{k=n_0}^{n-1} a(k)/b(k)$. Then for $n \ge n_0$, $t(n) = \kappa\, Z^n A(n)\, c(n)$ for a constant $\kappa$, and the output solution $h_j$ with ratio $Z a(n) c_j(n + 1)/(b(n) c_j(n))$ is $h_j(n) = \kappa_j Z^n A(n) c_j(n)$ with $\kappa_j \ne 0$. Hence $t = \sum_j (\kappa \lambda_j / \kappa_j)\, h_j$ for $n \ge n_0$. Reducing the ratio to lowest terms at line L7 does not change the sequence $h_j$ for $n \ge n_0$. $\blacksquare$
