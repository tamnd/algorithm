---
title: The subresultant algorithm returns the gcd in Z[x]
proves: [correctness]
status: full
---

Let $R$ be a unique factorization domain with fraction field $K$; the case of the page is $R = \mathbb{Z}$, $K = \mathbb{Q}$. Gcds in $R[x]$ are taken with a normal leading coefficient (positive over $\mathbb{Z}$). For $a, b \in K[x]$ let $D_K(a, b)$ be the set of common divisors of $a$ and $b$ in $K[x]$.

**Lemma 1 (pseudo-remainder).** If $A, B \in R[x]$, $B \ne 0$ and $\deg A \ge \deg B$, then $\operatorname{prem}(A, B) = \operatorname{lc}(B)^{\delta + 1} (A \operatorname{rem} B)$ in $K[x]$, where $\delta = \deg A - \deg B$. This is proved on the page [pseudo-division](/pseudo-division/), from the uniqueness of division with remainder in $K[x]$.

**Lemma 2 (exactness).** In every pass of the loop, $\gamma h^{\delta}$ divides every coefficient of $R$ in line L9, and the division in line L10 is exact. Moreover $\gamma \ne 0$ and $h \ne 0$.

*Source.* This is the fundamental theorem of subresultants: up to sign, each new $B$ of line L9 is a subresultant of $\operatorname{pp}(f)$ and $\operatorname{pp}(g)$, a polynomial whose coefficients are determinants of matrices with entries in $R$, and each $h$ is, up to sign, a leading coefficient of a subresultant (Brown and Traub, 1971; von zur Gathen and Gerhard, Section 11.2; Cohen, Section 3.3). The leading coefficients are nonzero because they are leading coefficients of nonzero polynomials, and a product and an exact quotient of nonzero elements of a domain are nonzero. The implementation checks every division and raises an error if one leaves a remainder.

**The case $g = 0$.** After line L1, $\deg f \ge \deg g$, so $g = 0$ is the only case in which line L2 returns. Then $\gcd(f, 0) = f$, normalized, which is the output. If also $f = 0$, the output is $0$.

**Invariant.** Assume $g \ne 0$. Before each test of line L4 (each pass of the loop):

1. $A, B \in R[x]$, $B \ne 0$ and $\deg A \ge \deg B$;
2. $D_K(A, B) = D_K(f, g)$.

*Initialization.* After line L3, $A = \operatorname{pp}(f)$ and $B = \operatorname{pp}(g)$. They differ from $f$ and $g$ by nonzero constants, which are units of $K$, so part 2 holds. Part 1 holds by line L1 and since $g \ne 0$.

*Maintenance.* Suppose the loop does not return at lines L7 or L8, so $R = \operatorname{prem}(A, B) \ne 0$ and $\deg R \ge 1$. By Lemma 1, $R = u \cdot (A \operatorname{rem} B)$ with $u = \operatorname{lc}(B)^{\delta + 1} \ne 0$. By Lemma 2, the new $B$ is $R / (\gamma h^{\delta}) \in R[x]$, a nonzero constant of $K$ times $A \operatorname{rem} B$. A polynomial divides $A$ and $B$ exactly when it divides $B$ and $A - (A \operatorname{quo} B) B = A \operatorname{rem} B$, so $D_K(\text{new } A, \text{new } B) = D_K(B, A \operatorname{rem} B) = D_K(A, B)$. Also $\deg(\text{new } B) = \deg(A \operatorname{rem} B) < \deg B = \deg(\text{new } A)$, which gives part 1.

**Termination.** Each pass that does not return makes $\deg B$ strictly smaller, and $\deg B \ge 1$ in every pass after the first that continues, since line L8 returns when $\deg R = 0$. So the loop returns after at most $\deg g + 1$ passes.

**The output.** Let $G = \gcd(f, g)$ in $R[x]$, and let $c = \gcd(\operatorname{cont} f, \operatorname{cont} g)$. We use two facts that follow from [Gauss's lemma](/gauss-lemma/), which states that a product of primitive polynomials is primitive.

*(a) If $p, a \in R[x]$, $p$ is primitive and $p$ divides $a$ in $K[x]$, then $p$ divides $a$ in $R[x]$.* Write $a = p\, q$ with $q \in K[x]$, and $q = \lambda q_0$ with $\lambda \in K$ and $q_0 \in R[x]$ primitive. Then $p q_0$ is primitive, and $a = \lambda\, p q_0$, so $\lambda = \operatorname{cont}(a)$ up to a unit, which lies in $R$. Hence $q \in R[x]$.

*(b) If $P$ is primitive and $P$ is a gcd of $f$ and $g$ in $K[x]$, then $c P$ is a gcd of $f$ and $g$ in $R[x]$.* By (a), $P$ divides $\operatorname{pp}(f)$ and $\operatorname{pp}(g)$ in $R[x]$, so $c P$ divides $f$ and $g$. If $d \in R[x]$ divides $f$ and $g$, then $\operatorname{cont}(d)$ divides $\operatorname{cont} f$ and $\operatorname{cont} g$, by Gauss's lemma applied to $f = d \cdot (f / d)$, so it divides $c$. And $\operatorname{pp}(d)$ divides $f$ and $g$ in $K[x]$, so it divides $P$ in $K[x]$, and by (a) in $R[x]$. Hence $d = \operatorname{cont}(d) \operatorname{pp}(d)$ divides $c P$.

*Line L7.* $R = 0$, so by Lemma 1, $A \operatorname{rem} B = 0$ and $B$ divides $A$ in $K[x]$. Then $D_K(A, B)$ is the set of divisors of $B$, and by the invariant $B$ is a gcd of $f$ and $g$ in $K[x]$. So is its primitive part $P = \operatorname{pp}(B)$, normalized, and by (b) the output $c P$ is $G$.

*Line L8.* $R$ is a nonzero constant, so $A \operatorname{rem} B$ is a nonzero constant, and $D_K(B, A \operatorname{rem} B)$ contains only constants. As above, $D_K(f, g)$ is the set of nonzero constants, so $1$ is a gcd in $K[x]$, and by (b) with $P = 1$ the output $c$ is $G$. $\blacksquare$
