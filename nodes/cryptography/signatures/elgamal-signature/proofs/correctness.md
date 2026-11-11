---
title: ElGamal signatures verify, and a repeated nonce reveals the private key
proves: [correctness]
status: full
---

We use the notation of the page. $p$ is a prime, $g$ generates $\mathbb{Z}_p^*$, so $g$ has order $p - 1$, the private key is $x$ and the public key is $y = g^x \bmod p$.

**Lemma 1 (exponents modulo $p - 1$).** For all integers $u$ and $v$, if $u \equiv v \pmod{p - 1}$ then $g^u \equiv g^v \pmod p$.

*Proof.* Write $u = v + j(p - 1)$. By [Fermat's little theorem](/fermat-little-theorem/), $g^{p-1} \equiv 1 \pmod p$, because $p \nmid g$. So $g^u = g^v (g^{p-1})^j \equiv g^v \pmod p$. For negative exponents the same holds in the group $\mathbb{Z}_p^*$. $\square$

**Theorem 1 (correctness).** For every hash value $h$, the pair $(r, s)$ returned by line L8 passes lines L9 to L11.

*Proof.* Line L4 gives $k$ with $1 \le k \le p - 2$ and $\gcd(k, p - 1) = 1$, so $k^{-1} \bmod (p - 1)$ exists. Line L5 gives $r = g^k \bmod p$; since $g$ is a unit, $r \neq 0$, so $1 \le r \le p - 1$. Line L6 gives $s \equiv k^{-1}(h - xr) \pmod{p - 1}$ with $0 \le s \le p - 2$, and line L7 excludes $s = 0$, so the range test of line L9 passes. Multiply the congruence of line L6 by $k$: $ks \equiv h - xr$, so $h \equiv xr + ks \pmod{p - 1}$. By Lemma 1,

$$g^h \equiv g^{xr + ks} = (g^x)^r (g^k)^s \equiv y^r r^s \pmod p,$$

which is the test of line L11. $\blacksquare$

**Theorem 2 (a repeated nonce).** Let $(r, s_1)$ and $(r, s_2)$ be signatures on hash values $h_1$ and $h_2$ made with the same $k$. Then $k$ is a solution of

$$(s_1 - s_2)\, k \equiv h_1 - h_2 \pmod{p - 1},$$

and $x$ is a solution of $r x \equiv h_1 - k s_1 \pmod{p - 1}$. With $d = \gcd(s_1 - s_2, p - 1)$, the first congruence has exactly $d$ solutions in $[0, p - 1)$; with $d' = \gcd(r, p - 1)$, the second has exactly $d'$ solutions for the right $k$. Checking each candidate against $r = g^k$ and $y = g^x$ finds $k$ and then $x \bmod (p - 1)$, which is the private key.

*Proof.* Line L6 for both signatures gives $k s_1 \equiv h_1 - x r$ and $k s_2 \equiv h_2 - x r \pmod{p - 1}$. Subtracting removes $x r$ and gives the first congruence, and the first equation, rearranged, gives the second. A congruence $a z \equiv c \pmod m$ that has a solution has exactly $\gcd(a, m)$ solutions modulo $m$, and they differ by multiples of $m / \gcd(a, m)$ ([linear congruence](/linear-congruence/)). The true $k$ and the true $x$ are among them, since the congruences were derived from true equations. A wrong candidate $k'$ with $g^{k'} \equiv r = g^k$ would satisfy $k' \equiv k \pmod{p - 1}$, because $g$ has order $p - 1$; so the check of $g^{k'}$ against $r$ keeps only the true $k$. The same argument with $y$ keeps only the true $x$. $\blacksquare$

The number of candidates is small in practice: $p - 1$ is even, so $d$ and $d'$ are at least 2 when $s_1 - s_2$ or $r$ is even, but a large common factor with $p - 1$ is unlikely for random values.
