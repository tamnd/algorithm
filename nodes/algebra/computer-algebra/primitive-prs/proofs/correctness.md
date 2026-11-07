---
title: The primitive PRS algorithm returns the gcd in R[x]
proves: [correctness]
status: full
---

**Setting.** $R$ is a unique factorization domain with field of fractions $K$. A polynomial in $R[x]$ is primitive when its coefficients have no common prime factor. We use two forms of Gauss's lemma: (G1) a product of primitive polynomials is primitive; (G2) if $p, q \in R[x]$ are primitive and $p = \lambda q$ with $\lambda \in K^*$, then $\lambda$ is a unit of $R$. (G2) follows from (G1) by clearing denominators: write $\lambda = a / b$ with $a, b \in R$ coprime; then $b p = a q$, the content of the left side is $b$ and of the right side is $a$, up to units, so $a$ and $b$ are units.

**Lemma 1.** For $f, g \in R[x]$ not both zero, $\gcd(f, g) = \gcd(\operatorname{cont} f, \operatorname{cont} g) \cdot \gcd(\operatorname{pp} f, \operatorname{pp} g)$ up to a unit. *Proof.* Any common divisor $d$ of $f$ and $g$ splits as $\operatorname{cont}(d) \operatorname{pp}(d)$. By (G1) the content of $f = \operatorname{cont}(f) \operatorname{pp}(f)$ factors by contents, so $\operatorname{cont}(d) \mid \operatorname{cont}(f)$ and $\operatorname{pp}(d) \mid \operatorname{pp}(f)$, and the same for $g$. Conversely the product on the right divides both $f$ and $g$. $\square$

**Lemma 2.** Let $A, B \in R[x]$ with $B \ne 0$ and $\deg A \ge \deg B$. Then $\operatorname{prem}(A, B) = \operatorname{LC}(B)^{e} (A \bmod B)$ with $e = \deg A - \deg B + 1$, where $A \bmod B$ is the remainder in $K[x]$. In particular $\deg \operatorname{prem}(A, B) < \deg B$, and $\gcd_{K[x]}(A, B) = \gcd_{K[x]}(B, \operatorname{prem}(A, B))$. *Proof.* $\operatorname{LC}(B)^e A = Q B + r$ in $R[x]$ with $\deg r < \deg B$, by the pseudo-division algorithm. Divide by $\operatorname{LC}(B)^e \ne 0$: then $A = (Q / \operatorname{LC}(B)^e) B + r / \operatorname{LC}(B)^e$, and by uniqueness of division in $K[x]$, $r / \operatorname{LC}(B)^e = A \bmod B$. A polynomial divides $A$ and $B$ exactly when it divides $B$ and $A - qB$. $\square$

**The algorithm.** Lines L1 to L3 handle the cases where $f$ or $g$ is $0$: $\gcd(0, 0) = 0$ and $\gcd(f, 0) = f$ up to a unit. Otherwise, after line L2, $\deg f \ge \deg g \ge 0$ and $g \ne 0$. By Lemma 1 it is enough to show that the loop returns $\gcd(\operatorname{pp} f, \operatorname{pp} g)$ (times $c$), or $c$ when this gcd is 1.

*Invariant.* At line L5, $A$ and $B$ are primitive, $B \ne 0$, $\deg A \ge \deg B$, and $\gcd_{K[x]}(A, B) = \gcd_{K[x]}(\operatorname{pp} f, \operatorname{pp} g)$ up to a factor in $K^*$.

It holds at the start. In a pass, let $r = \operatorname{prem}(A, B)$. If $r \ne 0$, then the new pair is $(B, \operatorname{pp}(r))$; $\operatorname{pp}(r)$ is primitive, $\operatorname{pp}(r)$ is $r$ times an element of $K^*$, and by Lemma 2 $\deg \operatorname{pp}(r) < \deg B$ and $\gcd_{K[x]}(B, \operatorname{pp}(r)) = \gcd_{K[x]}(B, r) = \gcd_{K[x]}(A, B)$. So the invariant holds again.

*Termination.* $\deg B$ falls strictly in each pass and is at least $0$, so the loop ends after at most $\deg g + 1$ passes.

*Result.* There are two ways to leave the loop.

(i) Line L7: $r = 0$. Then $B$ divides $A$ in $K[x]$, so $\gcd_{K[x]}(A, B) = B$ up to $K^*$. By the invariant, $B = \lambda h$ with $h = \gcd_{R[x]}(\operatorname{pp} f, \operatorname{pp} g)$ and $\lambda \in K^*$; here we use that a gcd in $R[x]$ of two primitive polynomials is primitive and is a gcd in $K[x]$ (it divides both in $K[x]$, and every divisor in $K[x]$ becomes, after making it primitive, a divisor in $R[x]$ by (G1)). Both $B$ and $h$ are primitive, so by (G2) $\lambda$ is a unit of $R$, and $B$ is the gcd in $R[x]$. Line L7 returns $c \cdot B$, which is $\gcd(f, g)$ by Lemma 1.

(ii) Line L9: $\deg B = 0$, so $B$ is a nonzero constant, and it is a unit of $K$. So $\gcd_{K[x]}(\operatorname{pp} f, \operatorname{pp} g) = 1$, and the primitive gcd $h$ in $R[x]$ has degree 0; being primitive, it is a unit of $R$. Line L9 returns $c$, which is $\gcd(f, g)$ by Lemma 1.

Over $\mathbb{Z}$, the content is taken with the sign of the leading coefficient, so every $B$ has a positive leading coefficient, $c > 0$, and the returned gcd is the normalized one. $\blacksquare$
