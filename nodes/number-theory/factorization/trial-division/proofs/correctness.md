---
title: Trial division returns the prime factorization
proves: [correctness, termination]
status: full
---

Let $N \ge 1$. We write $\prod F$ for the product of the entries of the list $F$ (the empty product is $1$). The trial divisors that line L5 produces are $d_0 = 2$, $d_1 = 3$, $d_2 = 5$, and in general $d_j = 2j + 1$ for $j \ge 1$. Each integer $c \ge 2$ that is not one of them is even and larger than $2$.

**Invariant.** Each time line L2 tests its condition:

> **(T1)** $N = (\prod F) \cdot m$ and $m \ge 1$.
> **(T2)** Each entry of $F$ is a prime less than $d$, and the entries are in non-decreasing order.
> **(T3)** No prime $q < d$ divides $m$.

*Initialization.* Line L1 sets $F$ empty, $m = N$ and $d = 2$. Then (T1) holds because $N \ge 1$, (T2) is empty, and (T3) holds because there is no prime less than $2$.

*The inner loop.* Fix one pass of the outer loop, with divisor $d$. We claim that each time line L3 finds $d \mid m$, $d$ is prime. Let $q$ be a prime factor of $d$. Then $q \mid m$, and by (T3) $q \ge d$. Since $q \le d$, we get $q = d$, so $d$ is prime. Line L4 then appends $d$ and divides $m$ by $d$. This keeps $N = (\prod F) \cdot m$, keeps $m \ge 1$, and keeps $F$ in order, because each earlier entry is less than $d$ by (T2). The inner loop stops after finitely many steps, since $m$ drops by a factor $d \ge 2$ in each step and stays at least $1$. When it stops, $d \nmid m$.

*Maintenance.* Let $d'$ be the next divisor from line L5. (T1) holds by the inner loop. Each entry of $F$ is at most $d < d'$, so (T2) holds. For (T3), let $q < d'$ be a prime. If $q < d$, then $q \nmid m$ by (T3) before the pass, and dividing $m$ cannot add a prime factor. If $q = d$, then $q \nmid m$ because the inner loop ended. If $d < q < d'$, then $q$ is not a trial divisor, so $q$ is even and larger than $2$, which is not a prime. So no such $q$ exists, and (T3) holds for $d'$.

**Termination.** In each pass, $d$ grows by at least $1$, and $m$ does not grow. So after at most $\lfloor \sqrt{N} \rfloor$ passes, $d \cdot d > N \ge m$, and the test of line L2 fails.

**The result.** When line L2 fails, $d^2 > m$. Assume that $m$ is composite. Then $m = ab$ with $1 < a \le b$, so $a \le \sqrt{m} < d$, and a prime factor of $a$ is a prime less than $d$ that divides $m$. This contradicts (T3). So $m = 1$ or $m$ is prime. If $m$ is prime, then $m \ge d$ by (T3), so $m$ is at least each entry of $F$ by (T2), and line L6 appends it at the end in order. In both cases the list $F$ that line L7 returns holds primes in non-decreasing order with $\prod F = N$, by (T1). By the uniqueness of the factorization, this is the prime factorization of $N$. $\blacksquare$
