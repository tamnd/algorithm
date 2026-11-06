---
title: The Möbius sieve computes mu(m) for every m up to n
proves: [correctness]
status: full
---

For $m \ge 2$ let $\mathrm{lp}(m)$ be the least prime factor of $m$. Lines L1 to L6 and the list of primes are exactly the [linear sieve](/linear-sieve/), and lines L3, L7 and L8 write only to $\mu$, which the linear sieve never reads. So the proof of the linear sieve applies without change, and gives these facts for $n \ge 2$:

1. In the round of $i$, after line L3, $\mathrm{lp}[i] = \mathrm{lp}(i)$, and line L3 runs its body exactly when $i$ is prime.
2. Line L6 runs exactly once for each composite $m \le n$, in the round of $i = m / \mathrm{lp}(m)$, with $p = \mathrm{lp}(m) \le \mathrm{lp}(i)$, and for no other index.

**Claim.** For each $m$ with $1 \le m \le n$, the entry $\mu[m]$ is written exactly once after line L1 sets it, and it then gets the value $\mu(m)$. More precisely: $\mu[1]$ is set to 1 in line L1 and never changed; for a prime $m$ the only write is in line L3; for a composite $m$ the only write is in line L7 or line L8 of the round $i = m / \mathrm{lp}(m)$.

*Proof.* Lines L3, L7 and L8 write at $i \ge 2$ or at $p \cdot i \ge 4$, so $\mu[1]$ keeps the value 1 $= \mu(1)$. A prime $m$ is not of the form $p \cdot i$ with $i \ge 2$, so lines L7 and L8 never write it, and by fact 1 line L3 writes $\mu[m] = -1 = \mu(m)$ in the round of $m$. Line L3 never writes a composite, by fact 1. A composite $m$ is written by lines L7 or L8 only together with line L6, so by fact 2 exactly once, in the round of $i = m / \mathrm{lp}(m)$.

It remains to check the value for composite $m$, by strong induction on $m$. Let $p = \mathrm{lp}(m)$ and $i = m / p$, so $2 \le i < m$ and $p \le \mathrm{lp}(i)$. The entry $\mu[i]$ was set before the round of $i$ reaches line L4: in line L1 if $i = 1$ (impossible here), in line L3 of the same round if $i$ is prime, or in the round of $i / \mathrm{lp}(i) < i$ if $i$ is composite. By induction it equals $\mu(i)$, and it does not change later. By fact 1, $\mathrm{lp}[i] = \mathrm{lp}(i)$.

- If $p = \mathrm{lp}(i)$, then $p \mid i$, so $p^2 \mid p i = m$ and $\mu(m) = 0$. Line L7 writes 0.
- If $p < \mathrm{lp}(i)$, then $p$ does not divide $i$, since every prime factor of $i$ is at least $\mathrm{lp}(i)$. So $\gcd(p, i) = 1$, and because $\mu$ is multiplicative, $\mu(m) = \mu(p) \mu(i) = -\mu(i)$. Line L8 writes $-\mu[i] = -\mu(i)$.

In both cases the written value is $\mu(m)$. $\square$

For $n = 0$ the output is $[0]$, and for $n = 1$ it is $[0, 1]$; both are correct, since the loop of line L2 does not run. Index 0 is never written after line L1, so $\mu[0] = 0$. The loops terminate as in the linear sieve. By the claim, the array returned in line L9 holds $\mu(m)$ for every $1 \le m \le n$. $\blacksquare$

**Multiplicativity of $\mu$.** The step $\mu(p i) = \mu(p) \mu(i)$ for $\gcd(p, i) = 1$ follows from the definition: if $i$ is squarefree with $r$ distinct prime factors, then $p i$ is squarefree with $r + 1$, so $\mu(p i) = (-1)^{r+1} = -\mu(i)$; if $i$ has a square factor, so does $p i$, and both values are 0.
