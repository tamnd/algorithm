---
title: Every Rabin-Williams signature made by the signer verifies
proves: [correctness]
status: full
---

We use the notation of the page: $N = pq$ with primes $p \equiv 3 \pmod 8$ and $q \equiv 7 \pmod 8$, and $h = H(M)$ with $\gcd(h, N) = 1$. For an odd prime $r$ and $a$ not divisible by $r$, $\left(\frac{a}{r}\right) \in \{1, -1\}$ is the Legendre symbol; Euler's criterion gives $a^{(r-1)/2} \equiv \left(\frac{a}{r}\right) \pmod r$, and the symbol is multiplicative in $a$.

**Lemma 1 (signs of $-1$ and $2$).** $\left(\frac{-1}{p}\right) = \left(\frac{-1}{q}\right) = -1$, $\left(\frac{2}{p}\right) = -1$ and $\left(\frac{2}{q}\right) = 1$.

*Proof.* $p \equiv q \equiv 3 \pmod 4$, so $(p - 1)/2$ and $(q - 1)/2$ are odd and $(-1)^{(r-1)/2} = -1$ for $r \in \{p, q\}$. By the second supplement to quadratic reciprocity, $\left(\frac{2}{r}\right) = 1$ if $r \equiv \pm 1 \pmod 8$ and $-1$ if $r \equiv \pm 3 \pmod 8$; $p \equiv 3$ and $q \equiv 7 \equiv -1$. $\square$

**Lemma 2 (the tweaks).** There is exactly one pair $(e, f) \in \{1, -1\} \times \{1, 2\}$ such that $h' = h (e f)^{-1} \bmod N$ is a square modulo $p$ and modulo $q$, and line L2 finds it.

*Proof.* $h'$ is a square modulo $r$ if and only if $\left(\frac{h}{r}\right) \left(\frac{e}{r}\right) \left(\frac{f}{r}\right) = 1$, since the symbol of an inverse equals the symbol of the element. By Lemma 1, $\left(\frac{e}{p}\right) = \left(\frac{e}{q}\right) = e$, $\left(\frac{f}{q}\right) = 1$ for both values of $f$, and $\left(\frac{f}{p}\right)$ is $1$ for $f = 1$ and $-1$ for $f = 2$. The condition modulo $q$ is $\left(\frac{h}{q}\right) e = 1$, which fixes $e = \left(\frac{h}{q}\right)$. The condition modulo $p$ is then $\left(\frac{h}{p}\right) e \left(\frac{f}{p}\right) = 1$, which fixes $f = 1$ if $\left(\frac{h}{p}\right) e = 1$ and $f = 2$ otherwise. These are the choices of line L2, and each step had exactly one solution. $\square$

**Lemma 3 (square roots modulo a prime $r \equiv 3 \pmod 4$).** If $a$ is a nonzero square modulo $r$, then $t = a^{(r+1)/4} \bmod r$ satisfies $t^2 \equiv a$, and the square roots of $a$ modulo $r$ are exactly $t$ and $r - t$.

*Proof.* $(r + 1)/4$ is an integer because $r \equiv 3 \pmod 4$. $t^2 = a^{(r+1)/2} = a \cdot a^{(r-1)/2} \equiv a \cdot 1$ by Euler's criterion. The polynomial $X^2 - a$ has at most two roots in the field $\mathbb{Z}_r$, and $t \not\equiv -t$ because $r$ is odd and $t \not\equiv 0$. $\square$

**Theorem (correctness).** For every message $M$ with $\gcd(H(M), N) = 1$, the triple $(e, f, s)$ returned by line L7 passes lines L8 to L10.

*Proof.* Line L2 returns $e \in \{1, -1\}$ and $f \in \{1, 2\}$, and line L6 returns $s \in [0, N)$, so line L8 passes. By Lemma 2, $h' = h (e f)^{-1}$ from line L3 is a square modulo $p$ and modulo $q$, and it is nonzero modulo both because $\gcd(h, N) = 1$. By Lemma 3, the values $s_p$ and $s_q$ of line L4 satisfy $s_p^2 \equiv h' \pmod p$ and $s_q^2 \equiv h' \pmod q$, and line L5 replaces them by $p - s_p$ or $q - s_q$, which have the same squares. Line L6 gives $s$ with $s \equiv s_p \pmod p$ and $s \equiv s_q \pmod q$, so $s^2 \equiv h' \pmod p$ and $\pmod q$, and by the [Chinese remainder theorem](/chinese-remainder-theorem/) $s^2 \equiv h' \pmod N$. Then $e f s^2 \equiv e f h (e f)^{-1} = h \pmod N$. Line L9 computes the same $h$ as line L1, so line L10 returns valid. $\blacksquare$

**Two roots factor $N$.** Let $s_1^2 \equiv s_2^2 \pmod N$ with $s_1 \not\equiv \pm s_2 \pmod N$. Then $N$ divides $(s_1 - s_2)(s_1 + s_2)$ but neither factor. As $N = pq$, one prime divides $s_1 - s_2$ and the other divides $s_1 + s_2$, and $\gcd(s_1 - s_2, N)$ is $p$ or $q$. By Lemma 3 and the Chinese remainder theorem, each $h'$ has exactly four roots modulo $N$, which form two pairs $\{s, N - s\}$; two roots from different pairs factor $N$. $\blacksquare$
