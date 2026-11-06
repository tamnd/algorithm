---
title: Correctness of Pollard's p-1 algorithm
proves: [correctness, termination]
status: full
---

Let $N \ge 3$, $B \ge 1$ and $2 \le a < N$. Write $M(B) = \operatorname{lcm}(1, 2, \dots, B)$.

**Lemma 1.** $M(B) = \prod_{q \le B} q^{e_q}$, where $q$ runs over the primes at most $B$ and $e_q$ is the largest integer with $q^{e_q} \le B$.

*Proof.* Let $P$ be the product on the right. For each $k \le B$ and each prime power $q^j \parallel k$, we have $q \le q^j \le k \le B$ and $j \le e_q$, so $k \mid P$. So $P$ is a common multiple of $1, \dots, B$. Conversely each factor $q^{e_q} \le B$ is one of the numbers $1, \dots, B$, so $q^{e_q}$ divides every common multiple, and these factors are pairwise coprime, so $P$ divides every common multiple. Hence $P$ is the least common multiple. $\square$

**Invariant.** Let $q_1 < q_2 < \cdots < q_m$ be the primes at most $B$. After $i$ passes of the loop of lines L2 to L4, $c \equiv a^{q_1^{e_1} \cdots q_i^{e_i}} \pmod N$.

*Proof.* Before the loop, $c = a$, which is the empty product case $i = 0$. If the claim holds after $i$ passes, line L3 computes $e = e_{i+1}$ and line L4 replaces $c$ by $c^{q_{i+1}^{e_{i+1}}} \bmod N$, which is congruent to $a^{q_1^{e_1} \cdots q_{i+1}^{e_{i+1}}}$. $\square$

**Termination.** The loop runs once for each of the $m = \pi(B)$ primes, line L3 is a finite loop because $q \ge 2$, and line L4 is a modular exponentiation with a finite exponent. So the algorithm stops.

**The output.** By the invariant and Lemma 1, $c \equiv a^{M(B)} \pmod N$ after the loop, so line L5 returns $g = \gcd(a^{M(B)} - 1, N)$, which is a positive divisor of $N$ (if $c = 1$, then $c - 1 = 0$ and $g = N$).

**Theorem.** (a) Let $p$ be a prime factor of $N$ with $p \nmid a$, and suppose that every prime power that divides $p - 1$ is at most $B$. Then $p \mid g$.

(b) Let $r^k$ be the exact power of a prime $r$ that divides $N$. If $a^{M(B)} \not\equiv 1 \pmod{r^k}$, then $r^k \nmid g$, so $g < N$.

(c) If the hypotheses of (a) and (b) both hold, then $1 < g < N$ and $g$ is a proper factor of $N$.

*Proof.* (a) Every prime power $q^j \parallel p - 1$ has $q^j \le B$, so $j \le e_q$ and $q^j \mid M(B)$ by Lemma 1. These prime powers are pairwise coprime, so $p - 1 \mid M(B)$. By Fermat's little theorem, $a^{p - 1} \equiv 1 \pmod p$, so $a^{M(B)} \equiv 1 \pmod p$, and $p$ divides $a^{M(B)} - 1$ and $N$, so $p \mid g$.

(b) If $r^k \mid g$, then $r^k \mid a^{M(B)} - 1$, against the hypothesis. Since $r^k \mid N$ and $r^k \nmid g$, $g \ne N$.

(c) By (a), $g \ge p > 1$, and by (b), $g < N$. $\blacksquare$
