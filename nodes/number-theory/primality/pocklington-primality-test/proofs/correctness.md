---
title: Correctness of the Pocklington primality test
proves: [correctness, termination, error]
status: full
---

We prove that POCKLINGTON returns PRIME only for primes, returns COMPOSITE only for composites, always stops, and returns UNKNOWN on a prime with probability at most $t \, 2^{-k}$. The input is an odd $n \ge 5$, a divisor $F = \prod_{j=1}^{t} q_j^{e_j}$ of $n - 1$ with $F^2 > n$ and the $q_j$ distinct primes, and the number $k \ge 1$ of tries for each prime.

**Lemma 1** (order of a prime power). Let $p$ be a prime, $q$ a prime, $e \ge 1$, and $b$ an integer with $b^{q^e} \equiv 1 \pmod p$ and $b^{q^{e-1}} \not\equiv 1 \pmod p$. Then the multiplicative order of $b$ modulo $p$ is $q^e$, and $q^e \mid p - 1$.

*Proof.* Since $b^{q^e} \equiv 1$, $p \nmid b$ and the order $d$ of $b$ divides $q^e$, so $d = q^i$ for some $0 \le i \le e$. If $i < e$, then $d \mid q^{e-1}$ and $b^{q^{e-1}} \equiv 1$, which is false. So $d = q^e$. By Fermat's little theorem $b^{p-1} \equiv 1$, so $d \mid p - 1$. $\square$

**Lemma 2** (Pocklington). Suppose that for each $j$ there is a base $a_j$ with $a_j^{n-1} \equiv 1 \pmod n$ and $\gcd(a_j^{(n-1)/q_j} - 1, n) = 1$. Then every prime factor $p$ of $n$ satisfies $p \equiv 1 \pmod F$, and $n$ is prime.

*Proof.* Fix a prime $p \mid n$ and an index $j$. Put $b = a_j^{(n-1)/q_j^{e_j}}$, an integer power because $q_j^{e_j} \mid F \mid n - 1$. Then $b^{q_j^{e_j}} = a_j^{n-1} \equiv 1 \pmod p$, since $p \mid n$. Also $b^{q_j^{e_j - 1}} = a_j^{(n-1)/q_j}$. If this were $\equiv 1 \pmod p$, then $p$ would divide both $a_j^{(n-1)/q_j} - 1$ and $n$, against the gcd condition. So Lemma 1 gives $q_j^{e_j} \mid p - 1$. The prime powers $q_j^{e_j}$ are pairwise coprime, so their product $F$ divides $p - 1$. Hence $p \ge F + 1 > \sqrt n$.

If $n$ were composite, it would have a prime factor $p \le \sqrt n$, which contradicts $p > \sqrt n$. So $n$ is prime. $\square$

**Correctness of PRIME.** Line L12 is reached only after the loop of line L4 has finished for every prime $q_j$. The loop for $q_j$ ends without a return only by the break of line L10, so a base $a_j = a_{q_j}$ was recorded for which line L7 did not return, that is $a_j^{n-1} \bmod n = 1$, and line L8 gave $g = 1$, that is $\gcd(a_j^{(n-1)/q_j} - 1, n) = 1$. Line L3 has checked $F \mid n - 1$ and $F^2 > n$. Lemma 2 applies, so $n$ is prime. For $n < 5$, line L1 returns PRIME only for $2$ and $3$, which are prime.

**Correctness of COMPOSITE.** Line L1 returns COMPOSITE for $n \in \{0, 1, 4\}$ (and for negative $n$), none of which is prime. Line L2 returns it for an even $n \ge 6$, which has the factor $2$. Line L7 returns it when $a^{n-1} \not\equiv 1 \pmod n$ for some $a \in [2, n-2]$. If $n$ were prime, then $n \nmid a$ and Fermat's little theorem would give $a^{n-1} \equiv 1$; so $n$ is composite. Line L9 returns it with $g = \gcd(\cdot, n)$ and $1 < g < n$; then $g$ is a proper divisor of $n$, so $n$ is composite.

**Termination.** Line L4 runs over $t$ primes and line L5 does at most $k$ tries for each, and every step of a try (two modular powers and a gcd) stops. So the call stops after at most $k t$ tries.

**Error: UNKNOWN on a prime.** Let $n$ be prime. Then lines L7 and L9 never return: $a^{n-1} \equiv 1$ by Fermat's little theorem, and $g = \gcd(c - 1, n)$ with $c = a^{(n-1)/q} \bmod n$ is $1$ or $n$, because $n$ is prime and $c - 1 \in [-1, n - 2]$. Moreover $g = n$ exactly when $c = 1$. The group $\mathbb{Z}_n^*$ is cyclic of order $n - 1$, and $q \mid n - 1$, so the map $x \mapsto x^{(n-1)/q}$ has kernel $K_q$ of size exactly $(n-1)/q$ (the kernel of the power map in a cyclic group of order $m$ with exponent $d \mid m$ has size $d$). The base $1$ lies in $K_q$ and is not in $[2, n-2]$, so at most $(n-1)/q - 1$ of the $n - 3$ bases in $[2, n-2]$ are bad. Since $q \ge 2$ and $n \ge 5$,
$$\frac{(n-1)/q - 1}{n - 3} \le \frac{(n-1)/2 - 1}{n - 3} = \frac{1}{2}.$$
The $k$ bases for $q$ are independent and uniform, so the loop for $q$ fails all $k$ tries with probability at most $2^{-k}$. By the union bound over the $t$ primes of $F$, the call returns UNKNOWN with probability at most $t \, 2^{-k}$, and otherwise it returns PRIME.

**Error: composites.** For a composite $n$, the call never returns PRIME, by the correctness of PRIME. It returns COMPOSITE or UNKNOWN; UNKNOWN is not a wrong answer, only a missing one. So all errors are of one kind: a prime may receive UNKNOWN, with the probability bounded above, and no input ever receives a wrong verdict. $\blacksquare$
