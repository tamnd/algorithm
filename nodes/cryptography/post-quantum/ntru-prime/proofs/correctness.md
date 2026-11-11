---
title: Streamlined NTRU Prime never fails to decrypt when q is at least 16w + 1
proves: [correctness]
status: full
---

Let $p$ and $q$ be primes, $R = \mathbb{Z}[x]/(x^p - x - 1)$, and $w \ge 1$. Elements of $R$ are written with their unique representative of degree below $p$. For $a \in R$, $\|a\|_\infty$ is the largest absolute value of a coefficient and $\|a\|_1$ the sum of the absolute values. Small and short are as on the page.

**Lemma 1 (products in $R$).** For $a, b \in R$, $\|a b\|_\infty \le 2 \|a\|_\infty \|b\|_1$.

*Proof.* Let $\sum_j c_j x^j$ be the product of $a$ and $b$ in $\mathbb{Z}[x]$, with degree at most $2p - 2$. A monomial $x^j$ with $j < p$ stays as it is, and for $p \le j \le 2p - 2$ the rule $x^p = x + 1$ gives $x^j = x^{j-p+1} + x^{j-p}$, with both exponents below $p$. So the coefficient of $x^i$ in $R$ is
$$c_i + [i \ge 1]\, c_{p+i-1} + [i \le p - 2]\, c_{p+i}.$$
Write $c_j = \sum_k a_{j-k} b_k$ with $a_u = 0$ for $u \notin [0, p)$. Then the coefficient is $\sum_k b_k s_k$ with $s_k = a_{i-k} + [i \ge 1]\, a_{p+i-1-k} + [i \le p-2]\, a_{p+i-k}$. Fix $k \in [0, p)$. If $k \le i$, the index $p + i - k$ is at least $p$, and $p + i - 1 - k$ is below $p$ only if $k = i$; so at most two terms of $s_k$ are nonzero. If $k > i$, the index $i - k$ is negative; so again at most two terms are nonzero. Hence $|s_k| \le 2 \|a\|_\infty$, and the coefficient is at most $\sum_k |b_k| \cdot 2 \|a\|_\infty = 2 \|a\|_\infty \|b\|_1$ in absolute value. $\square$

**Lemma 2 (the rounding error).** For every $t \in R/q$, $c = \mathrm{Round}(t)$ satisfies $c \equiv t + \varepsilon \pmod q$ with $\varepsilon$ small.

*Proof.* Each centered coefficient $t_i$ is an integer, so $t_i / 3$ has fractional part $0$, $1/3$ or $2/3$, and the nearest multiple of 3 is at distance 0 or 1. Set $\varepsilon_i = c_i - t_i \in \{-1, 0, 1\}$. $\square$

**Theorem.** Assume $q \ge 16 w + 1$. Let $(h, (f, v))$ come from lines L1 to L5 and $c$ from lines L6 and L7 for a short $r$. Then line L10 returns $r$.

*Proof.* Since $R/q$ is a field, $3f \ne 0$ is invertible and $h \cdot 3f \equiv g \pmod q$ (line L4). By Lemma 2, $3 f c \equiv 3 f h r + 3 f \varepsilon \equiv g r + 3 f \varepsilon \pmod q$. Let $E = g r + 3 f \varepsilon \in R$, computed over the integers. By Lemma 1 with $\|g\|_\infty \le 1$ and $\|r\|_1 = w$, $\|g r\|_\infty \le 2w$. By Lemma 1 with $\|\varepsilon\|_\infty \le 1$ and $\|f\|_1 = w$, $\|f \varepsilon\|_\infty \le 2w$. So $\|E\|_\infty \le 8w < q/2$, because $q \ge 16w + 1$. Each residue class modulo $q$ has one representative in $[-(q-1)/2, (q-1)/2]$, so line L8 gives $e = E$ exactly.

Modulo 3, $E \equiv g r$, so in $R/3$, $e v \equiv g r g^{-1} = r$ (line L2). Representatives of degree below $p$ are unique, and $r$ has coefficients in $\{-1, 0, 1\}$, which is the centered set modulo 3, so line L9 gives $r' = r$. Since $r$ is short, it has weight $w$, and line L10 returns $r$. $\blacksquare$

**Remarks.** For sntrup761, $16 \cdot 286 + 1 = 4577 \le 4591$, so the theorem applies to every key and every short $r$, with no probability involved. The full KEM decrypts with this core and then encrypts $r'$ again; by the theorem the re-encryption equals $c$ for honest ciphertexts, so the KEM returns the encapsulated key. That last step uses the encodings and hashes of the specification, which the code on this page does not implement.
