---
title: The sieve of Atkin returns exactly the primes up to n
proves: [correctness]
status: full
---

We use the three theorems of Atkin and Bernstein (Theorems 6.1, 6.2 and 6.3 of *Prime sieves using binary quadratic forms*), which hold for every squarefree positive integer $m$:

- (A) if $m \equiv 1 \pmod 4$: $m$ is prime $\iff$ $N_1(m) = \#\{(x, y) : x, y > 0,\ 4x^2 + y^2 = m\}$ is odd;
- (B) if $m \equiv 1 \pmod 6$: $m$ is prime $\iff$ $N_2(m) = \#\{(x, y) : x, y > 0,\ 3x^2 + y^2 = m\}$ is odd;
- (C) if $m \equiv 11 \pmod{12}$: $m$ is prime $\iff$ $N_3(m) = \#\{(x, y) : x > y > 0,\ 3x^2 - y^2 = m\}$ is odd.

Their proofs count ideals of norm $m$ in $\mathbb{Z}[i]$, $\mathbb{Z}[\omega]$ and $\mathbb{Z}[\sqrt 3]$: there are 2 for a prime and a multiple of 4 for a product of at least two distinct primes. Here we prove that the algorithm is correct given (A), (B) and (C).

If $n < 2$ there is no prime up to $n$, and line L1 returns the empty list. Assume $n \ge 2$.

**Classes.** An integer $m$ is coprime to 6 if and only if $m \bmod 12 \in \{1, 5, 7, 11\}$. For such $m$ define its count $N(m) = N_1(m)$ if $m \bmod 12 \in \{1, 5\}$, $N(m) = N_2(m)$ if $m \bmod 12 = 7$, and $N(m) = N_3(m)$ if $m \bmod 12 = 11$. In the first case $m \equiv 1 \pmod 4$, in the second $m \equiv 1 \pmod 6$, in the third $m \equiv 11 \pmod{12}$, so by (A), (B) and (C):

(\*) for every squarefree $m$ coprime to 6, $m$ is prime if and only if $N(m)$ is odd.

**After lines L3 to L5.** Line L2 sets all flags to false. Line L3 visits every pair $x, y \ge 1$ with $4x^2 + y^2 \le n$ exactly once, and flips $F[m]$ for $m = 4x^2 + y^2$ when $m \bmod 12 \in \{1, 5\}$. So the number of flips it makes at a given $m \le n$ is $N_1(m)$ if $m \bmod 12 \in \{1, 5\}$ and 0 otherwise. In the same way line L4 flips $m$ exactly $N_2(m)$ times if $m \bmod 12 = 7$ and never otherwise, and line L5 flips $m$ exactly $N_3(m)$ times if $m \bmod 12 = 11$ and never otherwise. (In line L5, for fixed $x$ the value $3x^2 - y^2$ decreases in $y$, so the pairs with $y < x$ and value at most $n$ are those with $y$ from $x - 1$ down to the first $y$ whose value exceeds $n$, exclusive. If some $y < x$ qualifies, then so does $y = x - 1$, the smallest value, and $3x^2 - (x - 1)^2 = 2x^2 + 2x - 1 \le n$; this is the bound on $x$.) A flag that starts false and is flipped $t$ times is true if and only if $t$ is odd. Hence, after line L5, for $0 \le m \le n$:

(\*\*) $F[m]$ is true if and only if $m$ is coprime to 6 and $N(m)$ is odd.

In particular $F[m]$ is false for $m \in \{0, 1, 2, 3, 4\}$: $0, 2, 3, 4$ are not coprime to 6, and $N(1) = N_1(1) = 0$, since $4x^2 + y^2 \ge 5$ for $x, y \ge 1$.

**Lines L6 and L7.** We show by induction on $r = 5, 6, \ldots, \lfloor \sqrt n \rfloor$ that when line L7 tests $F[r]$, the flag is true if and only if $r$ is prime. Lines L6 and L7 only ever set flags to false.

Suppose that for every $5 \le s < r$ the test of $F[s]$ was true exactly when $s$ was prime; then every multiple of $q^2$ up to $n$ has been cleared for each prime $5 \le q < r$. Consider $F[r]$.

- If $r$ is prime ($r \ge 5$), then $r$ is coprime to 6 and squarefree, and $N(r)$ is odd by (\*); so $F[r]$ was true after line L5 by (\*\*). It was not cleared since: a clearing at $r$ would need $q^2 \mid r$ for some $q < r$, which a prime does not allow. So $F[r]$ is true.
- If $r$ is not coprime to 6, $F[r]$ was false after line L5 and stays false.
- If $r$ is coprime to 6 and squarefree but composite, $N(r)$ is even by (\*), so $F[r]$ is false by (\*\*).
- If $r$ is coprime to 6 and not squarefree, some prime $q$ has $q^2 \mid r$; $q \ne 2, 3$, so $q \ge 5$, and $q < r$. By the induction hypothesis $F[q]$ was true when tested, so line L7 cleared all multiples of $q^2$ up to $n$, including $r$.

So the claim holds for $r$. Consequently, after the loop of line L6, the flags cleared by lines L6 and L7 are exactly the multiples of $p^2$ up to $n$ for the primes $5 \le p \le \sqrt n$.

**Line L8.** Let $5 \le m \le n$. If $m$ is prime, it is coprime to 6 and squarefree, so $F[m]$ is true after line L5 by (\*) and (\*\*), and no $p^2$ with $p$ prime divides it, so it is not cleared: $m$ is output. If $m$ is not prime, either $m$ is not coprime to 6, and $F[m]$ was never true; or $m$ is coprime to 6 and squarefree, and $N(m)$ is even, so $F[m]$ was never true; or $m$ is coprime to 6 and not squarefree, so $p^2 \mid m$ for a prime $p \ge 5$ with $p^2 \le m \le n$, hence $p \le \lfloor \sqrt n \rfloor$, and $m$ was cleared in line L7. So the numbers $m \ge 5$ output are exactly the primes in $[5, n]$, in increasing order, and line L8 puts the primes 2 and 3 that are at most $n$ before them. The output is the increasing list of all primes up to $n$. $\blacksquare$
