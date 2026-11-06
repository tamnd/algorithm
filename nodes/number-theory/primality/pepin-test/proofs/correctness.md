---
title: Pépin's test returns true exactly when 2^(2^k) + 1 is prime
proves: [correctness, termination]
status: full
---

We use the pseudocode PEPIN$(k)$ of the page, for an integer $k \ge 0$, with $F = F_k = 2^{2^k} + 1$ and $e = 2^k$. So $F - 1 = 2^e$ and $(F - 1)/2 = 2^{e-1}$.

**Termination.** The loop of line L4 runs $e - 1$ times, and each pass does one squaring and one reduction. The reduction ends (Lemma 1). So the call ends.

**Lemma 1 (the reduction).** Let $x \ge 0$ and write $x = h \cdot 2^e + \ell$ with $0 \le \ell < 2^e$. Then $x \equiv \ell - h \pmod F$. If moreover $x \le (F - 1)^2$, then $-F < \ell - h < F$, so $\ell - h$, plus $F$ if it is negative, is $x \bmod F$.

*Proof.* $2^e = F - 1 \equiv -1 \pmod F$, so $h \cdot 2^e + \ell \equiv \ell - h$. If $x \le (F - 1)^2 = 2^{2e}$, then $h = \lfloor x / 2^e \rfloor \le 2^e = F - 1$, so $\ell - h \ge -(F - 1) > -F$. Also $\ell - h \le \ell < 2^e < F$. So $\ell - h$ lies in $(-F, F)$ and is congruent to $x$, and adding $F$ when it is negative gives the residue in $[0, F)$. $\square$

**Lemma 2 (the loop invariant).** For $k \ge 1$, after the $i$-th pass of line L5, $0 \le x < F$ and $x \equiv 3^{2^i} \pmod F$. So after the loop, $x = 3^{(F-1)/2} \bmod F$.

*Proof.* Before the loop, $x = 3 = 3^{2^0}$ and $3 < F$ since $F \ge 5$. If $x \equiv 3^{2^i}$ with $0 \le x < F$, then $x^2 \equiv 3^{2^{i+1}}$ and $x^2 \le (F - 1)^2$, so by Lemma 1 line L5 stores its residue in $[0, F)$. After $e - 1$ passes, $x \equiv 3^{2^{e-1}} = 3^{(F-1)/2}$. $\square$

**Lemma 3 (the congruence implies primality).** Let $k \ge 1$. If $3^{(F-1)/2} \equiv -1 \pmod F$, then $F$ is prime.

*Proof.* Let $q$ be a prime factor of $F$. Reducing modulo $q$ gives $3^{(F-1)/2} \equiv -1 \pmod q$. If $q = 3$, the left side is 0 and the right side is 2 modulo 3, which is impossible; so $q \ne 3$ and 3 is a unit modulo $q$. Squaring gives $3^{F-1} \equiv 1 \pmod q$. Let $d$ be the multiplicative order of 3 modulo $q$. Then $d \mid F - 1 = 2^e$, so $d$ is a power of 2. If $d \mid (F - 1)/2 = 2^{e-1}$, then $3^{(F-1)/2} \equiv 1 \pmod q$, so $1 \equiv -1$ and $q = 2$, but $F$ is odd. Hence $d = 2^e = F - 1$. By Fermat's little theorem, $d \mid q - 1$, so $q \ge F$. As $q \mid F$, $q = F$, and $F$ is prime. $\square$

**Lemma 4 (primality implies the congruence).** Let $k \ge 1$. If $F$ is prime, then $3^{(F-1)/2} \equiv -1 \pmod F$.

*Proof.* As $k \ge 1$, $e \ge 2$, so $4 \mid 2^e$ and $F \equiv 1 \pmod 4$. As $e$ is even, $2^e = 4^{e/2} \equiv 1 \pmod 3$, so $F \equiv 2 \pmod 3$; in particular $F \ne 3$, and $F$ is an odd prime with $3 \nmid F$. By the law of quadratic reciprocity, since $F \equiv 1 \pmod 4$,
$$\left(\frac{3}{F}\right) = \left(\frac{F}{3}\right) = \left(\frac{2}{3}\right) = -1,$$
the last because the squares modulo 3 are 0 and 1. By Euler's criterion, $3^{(F-1)/2} \equiv \left(\frac{3}{F}\right) = -1 \pmod F$. $\square$

**Theorem.** For each integer $k \ge 0$, PEPIN$(k)$ returns true if and only if $F_k$ is prime.

*Proof.* If $k = 0$, then $F_0 = 3$ is prime, and line L1 returns true. Let $k \ge 1$. By Lemma 2, line L6 returns true if and only if $3^{(F-1)/2} \bmod F = F - 1$, that is, $3^{(F-1)/2} \equiv -1 \pmod F$. By Lemmas 3 and 4, this holds if and only if $F$ is prime. $\blacksquare$
