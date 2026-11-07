---
title: Correctness of the multimodular determinant
proves: [correctness, termination]
status: full
---

We prove that MULTIMODULAR-DET returns $\det A$ for every $n \times n$ integer matrix $A$. Notation is as on the main page: $a_i$ is row $i$ of $A$, $H = \lfloor \prod_i \|a_i\|_2 \rfloor$, and the primes $p_1, p_2, \ldots$ of the list are distinct.

**The bound.** By Hadamard's inequality, $|\det A| \le \prod_i \|a_i\|_2$. Since $\det A$ is an integer, $|\det A| \le \lfloor \prod_i \|a_i\|_2 \rfloor = H$. The integer square root of the integer $\prod_i \|a_i\|_2^2$ equals $H$, because $\lfloor \sqrt{N} \rfloor$ is the largest integer whose square is at most $N$.

**Lemma 1.** For every prime $p$, line L5 returns $\det A \bmod p$.

*Proof.* The map $\mathbb{Z} \to \mathbb{Z}/p\mathbb{Z}$ is a ring homomorphism, and $\det A = \sum_\sigma \operatorname{sgn}(\sigma) \prod_i a_{i \sigma(i)}$ is a polynomial with integer coefficients in the entries, so $\det (A \bmod p) = (\det A) \bmod p$. Since $p$ is prime, $\mathbb{Z}/p\mathbb{Z}$ is a field, and Gaussian elimination with row swaps computes the determinant of a matrix over a field: each swap multiplies the determinant by $-1$, adding a multiple of the pivot row to another row does not change it, and the determinant of the final triangular matrix is the product of its diagonal; if no nonzero pivot exists in some column, the columns up to it are dependent and the determinant is $0$. $\square$

**Invariant.** At each test of line L4, $M$ is the product of the primes used so far, and $0 \le r < M$ with $r \equiv \det A \pmod M$.

*Initialization.* Before the first test, $M = 1$ and $r = 0$, and every integer is congruent to $0$ modulo $1$.

*Maintenance.* Let $p$ be the next prime. It differs from the primes in $M$, so $\gcd(M, p) = 1$ and $M^{-1} \bmod p$ exists. Let $d = \det A \bmod p$ by Lemma 1, $t = (d - r) M^{-1} \bmod p$ with $0 \le t \le p - 1$, and $r' = r + M t$. Then $r' \equiv r \equiv \det A \pmod M$, and $r' \equiv r + (d - r) = d \equiv \det A \pmod p$. Since $M$ and $p$ are coprime, $r' \equiv \det A \pmod {M p}$. Finally $0 \le r' \le (M - 1) + M (p - 1) = M p - 1$. So the invariant holds for $M' = M p$ and $r'$.

**Termination.** Each pass multiplies $M$ by a prime, so after $k$ passes $M \ge 2^k$, and the condition $M \le 2H$ fails after at most $\lfloor \log_2 (2H) \rfloor + 1$ passes. The list of primes never runs out because there are infinitely many primes. For $n = 0$, line L1 returns $1$, the determinant of the empty matrix.

**Conclusion.** At the exit $M > 2H$, $0 \le r < M$ and $r \equiv \det A \pmod M$. Let $D = \det A$, so $|D| \le H \le (M - 1)/2$.

- If $D \ge 0$, then $D < M$ and $D \equiv r$, so $r = D$. Also $D \le (M - 1)/2$ gives $D \le \lfloor M/2 \rfloor$, so line L8 leaves $r$ unchanged and returns $D$.
- If $D < 0$, then $D + M$ lies in $[0, M)$ and is congruent to $r$, so $r = D + M \ge M - (M - 1)/2 = (M + 1)/2 > \lfloor M/2 \rfloor$. Line L8 replaces $r$ by $r - M = D$.

In both cases the algorithm returns $\det A$. $\blacksquare$
