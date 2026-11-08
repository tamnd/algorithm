---
title: For a Blum integer, squaring permutes the quadratic residues, the BBS state sequence is purely periodic with period ord_t(2) dividing lambda(lambda(n)), and the trapdoor computes the previous state
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $n = p q$ with distinct primes $p \equiv q \equiv 3 \pmod 4$, let $\mathbb{Z}_n^*$ be the units modulo $n$, and $\mathrm{QR}_n = \{ y^2 \bmod n : y \in \mathbb{Z}_n^* \}$. Write $p = 2p' + 1$ and $q = 2q' + 1$, with $p'$ and $q'$ odd. The security of the output is not proved here; it is cited on the page. This page proves what the algorithm computes.

**Lemma 1.** $x_0 = s^2 \bmod n \in \mathrm{QR}_n$, and line L3 keeps $x$ in $\mathrm{QR}_n$, with $x_i = x_0^{2^i} \bmod n$.

*Proof.* $\gcd(s, n) = 1$ gives $s \in \mathbb{Z}_n^*$, so $x_0 \in \mathrm{QR}_n$. If $x = y^2$ then $x^2 = (y^2)^2$ is again a square of a unit. The formula follows by induction: $x_{i+1} = (x_0^{2^i})^2 = x_0^{2^{i+1}}$. $\square$

**Lemma 2 (residues modulo $p$).** For a prime $p \equiv 3 \pmod 4$, $-1$ is a non-residue modulo $p$. If $x$ is a nonzero residue modulo $p$, then $r = x^{(p+1)/4} \bmod p$ is a residue with $r^2 \equiv x$, and it is the only square root of $x$ that is a residue.

*Proof.* By Euler's criterion, $(-1)^{(p-1)/2} = (-1)^{p'} = -1$ since $p'$ is odd, so $-1$ is a non-residue. Also $x^{(p-1)/2} \equiv 1$, hence $r^2 = x^{(p+1)/2} = x \cdot x^{(p-1)/2} \equiv x$. As a power of the residue $x$, $r$ is a residue. The square roots of $x$ are $r$ and $-r$, and $-r = (-1) \cdot r$ is a product of a non-residue and a residue, hence a non-residue. $\square$

**Lemma 3 (squaring is a permutation of $\mathrm{QR}_n$).** The map $f(x) = x^2 \bmod n$ is a bijection of $\mathrm{QR}_n$, and $|\mathrm{QR}_n| = p' q'$ is odd.

*Proof.* By the CRT, $\mathbb{Z}_n^* \cong \mathbb{Z}_p^* \times \mathbb{Z}_q^*$, and $y$ is a square modulo $n$ if and only if it is a square modulo $p$ and modulo $q$. So $|\mathrm{QR}_n| = \frac{p-1}{2} \cdot \frac{q-1}{2} = p' q'$, which is odd. $f$ maps $\mathrm{QR}_n$ into itself by Lemma 1. For $x \in \mathrm{QR}_n$, Lemma 2 gives a residue square root $r_p$ modulo $p$ and $r_q$ modulo $q$; the CRT combination $y$ is a residue modulo both, so $y \in \mathrm{QR}_n$ and $f(y) = x$. So $f$ is onto the finite set $\mathrm{QR}_n$, hence a bijection. $\square$

**Theorem 1 (period).** Let $t$ be the multiplicative order of $x_0$ modulo $n$. Then $t$ is odd, the sequence $x_0, x_1, \ldots$ is purely periodic, and its period is $\rho = \operatorname{ord}_t(2)$, the order of 2 modulo $t$ (with $\rho = 1$ when $t = 1$). Moreover $\rho$ divides $\lambda(\lambda(n))$, where $\lambda$ is Carmichael's function.

*Proof.* $\mathrm{QR}_n$ is a subgroup of $\mathbb{Z}_n^*$ of odd order $p' q'$ (Lemma 3), and $x_0 \in \mathrm{QR}_n$, so by Lagrange $t \mid p' q'$ and $t$ is odd. Hence $\gcd(2, t) = 1$ and $\operatorname{ord}_t(2)$ is defined. By Lemma 1, for $i \ge 0$ and $\rho \ge 1$, $x_{i+\rho} = x_i$ if and only if $x_0^{2^i (2^\rho - 1)} = 1$, if and only if $t \mid 2^i (2^\rho - 1)$, if and only if $t \mid 2^\rho - 1$ (as $t$ is odd). This condition does not depend on $i$, so the sequence is purely periodic, and its least period is the least $\rho \ge 1$ with $2^\rho \equiv 1 \pmod t$, which is $\operatorname{ord}_t(2)$.

For the divisibility: every element of $\mathrm{QR}_n$ has order dividing the exponent of $\mathrm{QR}_n \cong \mathrm{QR}_p \times \mathrm{QR}_q$, a product of cyclic groups of orders $p'$ and $q'$, so $t \mid m'$ with $m' = \operatorname{lcm}(p', q')$. Now $\operatorname{ord}_t(2) \mid \lambda(t)$, and $t \mid m'$ implies $\lambda(t) \mid \lambda(m')$ (the exponent of the quotient group $\mathbb{Z}_t^*$ of $\mathbb{Z}_{m'}^*$ divides that of $\mathbb{Z}_{m'}^*$). Finally $\lambda(n) = \operatorname{lcm}(2p', 2q') = 2 m'$ with $m'$ odd, so $\lambda(\lambda(n)) = \operatorname{lcm}(\lambda(2), \lambda(m')) = \lambda(m')$. Hence $\rho \mid \lambda(\lambda(n))$. $\square$

**Proposition 2 (trapdoor computations).** Given $p$ and $q$: (a) $x_i = x_0^{e} \bmod n$ with $e = 2^i \bmod \lambda(n)$; (b) for $i \ge 1$, $x_{i-1}$ is the CRT combination of $x_i^{(p+1)/4} \bmod p$ and $x_i^{(q+1)/4} \bmod q$.

*Proof.* (a) $x_0^{\lambda(n)} = 1$ for every unit, so exponents may be reduced modulo $\lambda(n)$. (b) $x_{i-1} \in \mathrm{QR}_n$ and $f(x_{i-1}) = x_i$. By Lemma 2 the CRT combination $y$ described is in $\mathrm{QR}_n$ with $y^2 \equiv x_i$; by Lemma 3, $f$ is injective on $\mathrm{QR}_n$, so $y = x_{i-1}$. $\square$

**Output.** Line L4 returns $x_i \bmod 2$, the least significant bit of the representative $x_i \in \{0, \ldots, n-1\}$; with $j$ bits per step it returns $x_i \bmod 2^j$. Line L5 returns $b_1, \ldots, b_k$, the predicate applied to $x_1, \ldots, x_k$. $\blacksquare$
