---
title: The sieve of Eratosthenes returns exactly the primes up to n
proves: [correctness]
status: full
---

For $n < 2$ there is no prime $p \le n$, and line L1 returns the empty list. From now on $n \ge 2$. For an integer $m \ge 2$ let $\mathrm{lpf}(m)$ be its smallest prime factor. We use two facts.

**Fact 1.** If $m \ge 2$ is composite, then $\mathrm{lpf}(m)^2 \le m$. Indeed $m = q k$ with $q = \mathrm{lpf}(m)$ and $k \ge 2$. Each prime factor of $k$ divides $m$, so it is at least $q$, and therefore $k \ge q$ and $m = qk \ge q^2$.

**Fact 2.** If $m \ge 2$ is composite and $q = \mathrm{lpf}(m)$, then $m = q k$ with $k \ge q$. This is the same argument.

**Invariant.** Each time line L4 tests a value $p$, the following holds for every $m$ with $2 \le m \le n$:

> **(I)** $P[m]$ is false if and only if $m$ is composite and $\mathrm{lpf}(m) < p$.

*Initialization.* Line L3 sets $p = 2$. Line L2 sets every $P[m]$ with $m \ge 2$ to true, and no $m$ has $\mathrm{lpf}(m) < 2$. So (I) holds.

*Line L5 tests primality.* Suppose line L4 lets $p$ through, so $p^2 \le n$ and $2 \le p \le n$. If $p$ is composite, then by Fact 1, $\mathrm{lpf}(p) \le \sqrt p < p$, so by (I), $P[p]$ is false. If $p$ is prime, then $p$ is not composite, so by (I), $P[p]$ is true. Hence the test of line L5 succeeds exactly when $p$ is prime.

*Maintenance.* We show that (I) holds for $p + 1$ after line L8.

- If $p$ is composite, lines L6 and L7 do not run and no flag changes. No integer $m$ has $\mathrm{lpf}(m) = p$, since $\mathrm{lpf}(m)$ is prime. So "$m$ composite and $\mathrm{lpf}(m) < p$" is the same as "$m$ composite and $\mathrm{lpf}(m) < p + 1$", and (I) holds for $p + 1$.
- If $p$ is prime, lines L6 and L7 set $P[m]$ to false for exactly the numbers $m = p k$ with $k \ge p$ and $m \le n$. Each such $m$ is composite, because $k \ge p \ge 2$, and $\mathrm{lpf}(m) \le p$. Conversely, let $m \le n$ be composite with $\mathrm{lpf}(m) = p$. By Fact 2, $m = p k$ with $k \ge p$, so the loop clears $P[m]$. No flag is set back to true. So after the loop, $P[m]$ is false exactly when $m$ is composite with $\mathrm{lpf}(m) < p$ (cleared before, by (I)) or composite with $\mathrm{lpf}(m) = p$ (cleared now). This is (I) for $p + 1$.

*Termination.* The value $p$ grows by one in each pass of the loop, so the test $p \cdot p \le n$ of line L4 fails after at most $\sqrt n$ passes. Each loop of line L6 is finite, since $m$ grows by $p \ge 2$ and stops above $n$.

*Conclusion.* When line L4 fails, $p^2 > n$, so $p > \sqrt n$. Let $2 \le m \le n$. If $m$ is prime, it is not composite, so by (I), $P[m]$ is true. If $m$ is composite, then by Fact 1, $\mathrm{lpf}(m) \le \sqrt m \le \sqrt n < p$, so by (I), $P[m]$ is false. So $P[m]$ is true exactly for the primes $m$ in $[2, n]$, and line L9 returns all primes up to $n$ in increasing order. $\blacksquare$

**The count of writes.** For a prime $p$ with $p^2 \le n$, the loop of line L6 visits $m = p k$ for $k = p, p + 1, \ldots, \lfloor n/p \rfloor$, which is $\lfloor n/p \rfloor - p + 1$ values. Summed over these primes, this is the formula for $W(n)$ in the complexity section. The lower bound uses $\lfloor n/p \rfloor - p + 1 \ge n/p - p$ and $\sum_{p \le \sqrt n} p \le \sqrt n \cdot \sqrt n = n$, so $W(n) \ge n \sum_{p \le \sqrt n} 1/p - n$, and Mertens' theorem makes this $n \ln \ln n - O(n)$.
