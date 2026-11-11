---
title: Every DSA signature made by the signer verifies
proves: [correctness]
status: full
---

We use the notation of the page. $p$ and $q$ are primes with $q \mid p - 1$, $g$ is an element of order $q$ in $\mathbb{Z}_p^*$, the private key is $x$ with $1 \le x \le q - 1$, the public key is $y = g^x \bmod p$, and $z$ is the message representative of lines L1 and L9.

**Lemma 1 (exponents modulo $q$).** For all integers $u$ and $v$ with $u \equiv v \pmod q$, $g^u \equiv g^v \pmod p$.

*Proof.* $g$ has order $q$, so $g^q \equiv 1 \pmod p$. Write $u = v + jq$; then $g^u = g^v (g^q)^j \equiv g^v$. $\square$

**Lemma 2 (the generator of Appendix A.2.1 has order $q$).** If $g = h^{(p-1)/q} \bmod p$ and $g \ne 1$, then $g$ has order $q$.

*Proof.* $g^q = h^{p-1} \equiv 1 \pmod p$ by [Fermat's little theorem](/fermat-little-theorem/), so the order of $g$ divides $q$. As $q$ is prime, the order is 1 or $q$, and it is not 1 because $g \ne 1$. $\square$

**Theorem (correctness).** For every message $M$, the pair $(r, s)$ returned by line L6 passes lines L7 to L12.

*Proof.* Line L2 gives $1 \le k \le q - 1$, so $k$ is invertible modulo the prime $q$. Line L5 returns only when $r \ne 0$ and $s \ne 0$, and both are reduced modulo $q$, so $0 < r < q$ and $0 < s < q$ and line L7 passes. As $s \ne 0$ and $q$ is prime, $w = s^{-1} \bmod q$ exists (line L8). Line L9 computes the same $z$ as line L1, because it hashes the same message with the same rule.

From line L4, $s \equiv k^{-1}(z + x r) \pmod q$, so $k \equiv s^{-1}(z + x r) \equiv w (z + x r) \pmod q$. With line L10,

$$u_1 + x u_2 \equiv z w + x r w = w (z + x r) \equiv k \pmod q.$$

So, by Lemma 1, line L11 computes

$$g^{u_1} y^{u_2} = g^{u_1} g^{x u_2} = g^{u_1 + x u_2} \equiv g^k \pmod p.$$

The value $(g^{u_1} y^{u_2} \bmod p) \bmod q$ is therefore $(g^k \bmod p) \bmod q = r$ by line L3, and line L12 returns valid. $\blacksquare$

**Why the reduction modulo $q$ is harmless.** Line L3 throws away most of $g^k \bmod p$ and keeps a number below $q$. The verifier never needs the full value, because it recomputes $g^k \bmod p$ itself in line L11 and reduces it in the same way. The argument above needs only that both sides reduce the same element of $\mathbb{Z}_p^*$.

**A repeated nonce.** If two signatures $(r, s_1)$ and $(r, s_2)$ on representatives with $z_1 \not\equiv z_2 \pmod q$ use the same $k$, then $k s_1 \equiv z_1 + x r$ and $k s_2 \equiv z_2 + x r \pmod q$. Subtraction gives $k (s_1 - s_2) \equiv z_1 - z_2 \not\equiv 0$, so $s_1 \not\equiv s_2$, and since $q$ is prime, $k = (z_1 - z_2)(s_1 - s_2)^{-1} \bmod q$ and then $x = (k s_1 - z_1) r^{-1} \bmod q$. Unlike in the ElGamal scheme, each step has exactly one solution, because $q$ is prime. $\blacksquare$
