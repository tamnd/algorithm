---
title: The totient sieve computes phi(m) for every m up to n
proves: [correctness]
status: full
---

For $1 \le m \le n$ and an integer $t \ge 2$ let

$$F_t(m) = m \prod_{q \text{ prime},\ q < t,\ q \mid m} \frac{q - 1}{q}.$$

So $F_2(m) = m$, and $F_t(m) = \varphi(m)$ as soon as $t$ exceeds every prime factor of $m$, by the product formula $\varphi(m) = m \prod_{q \mid m} (1 - 1/q)$.

**Lemma 1.** $F_t(m)$ is an integer. If $p \ge t$ is a prime that divides $m$, then $p$ divides $F_t(m)$.

*Proof.* Let $Q$ be the product of the distinct primes $q < t$ that divide $m$. Then $Q \mid m$ and $F_t(m) = (m / Q) \prod_{q \mid Q} (q - 1)$, an integer. If $p \ge t$ is prime and $p \mid m$, then $p \nmid Q$, so $p$ divides $m / Q$ and therefore $F_t(m)$. $\square$

**Invariant.** Each time the loop of line L2 reaches a value $p$ (with $2 \le p \le n + 1$, where $p = n + 1$ means the loop has ended), for every $1 \le m \le n$:

> **(I)** $\varphi[m] = F_p(m)$.

*Initialization.* Line L1 sets $\varphi[m] = m = F_2(m)$.

*The test of line L3.* Let $2 \le p \le n$ and assume (I). If $p$ is prime, no prime $q < p$ divides $p$, so $\varphi[p] = F_p(p) = p$. If $p$ is composite, it has a prime factor $q < p$, and $F_p(p) \le p (q - 1)/q < p$. So line L3 succeeds exactly when $p$ is prime.

*Maintenance.* If $p$ is composite, no entry changes, and $F_{p+1}(m) = F_p(m)$ for all $m$, because the prime condition $q < p + 1$ adds only $q = p$, which is not prime. If $p$ is prime, lines L4 and L5 visit exactly the multiples $m$ of $p$ with $m \le n$, each once. For such $m$, Lemma 1 (with $t = p$) says that $p$ divides $\varphi[m] = F_p(m)$, so line L5 computes exactly

$$F_p(m) - \frac{F_p(m)}{p} = F_p(m) \cdot \frac{p - 1}{p} = F_{p+1}(m).$$

For $m$ not divisible by $p$, the entry does not change, and $F_{p+1}(m) = F_p(m)$. So (I) holds for $p + 1$.

*Termination.* The outer loop runs $n - 1$ times, and each inner loop at most $n/p$ times.

*Conclusion.* When the loop ends, $p = n + 1$. Every prime factor of $m \le n$ is at most $n < n + 1$, so $\varphi[m] = F_{n+1}(m) = \varphi(m)$ for every $1 \le m \le n$. Line L1 sets $\varphi[0] = 0$, and no later line writes to index 0. $\blacksquare$

**The number of updates.** For each prime $p \le n$, line L5 runs once for each of the $\lfloor n/p \rfloor$ multiples of $p$ in $[1, n]$. Since $n/p - 1 < \lfloor n/p \rfloor \le n/p$ and $\pi(n) \le n$, the total is $n \sum_{p \le n} 1/p + O(n)$, and Mertens' theorem gives $n \ln \ln n + O(n)$.
