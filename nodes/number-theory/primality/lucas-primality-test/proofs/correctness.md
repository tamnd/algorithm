---
title: The Lucas test returns true exactly when n is prime
proves: [correctness, termination]
status: full
---

We use the pseudocode LUCAS$(n, q_1, \ldots, q_m)$ of the page. The input is an integer $n \ge 0$ and, for $n \ge 3$, the list of the distinct primes $q_1, \ldots, q_m$ that divide $n - 1$. Write $n - 1 = q_1^{e_1} \cdots q_m^{e_m}$ with each $e_i \ge 1$.

**Lemma 1 (orders).** Let $n \ge 2$, let $a$ be an integer with $a^{n-1} \equiv 1 \pmod n$, and let $r$ be the least $t \ge 1$ with $a^t \equiv 1 \pmod n$. Then $\gcd(a, n) = 1$, $r \mid n - 1$, and $r \mid \varphi(n)$.

*Proof.* $a \cdot a^{n-2} \equiv 1$, so $a$ is a unit modulo $n$. Divide: $n - 1 = cr + t$ with $0 \le t < r$; then $a^t = a^{n-1} (a^r)^{-c} \equiv 1$, so $t = 0$ by the choice of $r$. The units modulo $n$ form a group of order $\varphi(n)$, and $r$ is the order of $a$ in it, so $r \mid \varphi(n)$ by Lagrange's theorem. $\square$

**Lemma 2 (bases imply primality).** Let $n \ge 3$. Suppose that for each $i$ there is an integer $a_i$ with $a_i^{n-1} \equiv 1$ and $a_i^{(n-1)/q_i} \not\equiv 1 \pmod n$. Then $n$ is prime.

*Proof.* Let $r_i$ be the order of $a_i$. By Lemma 1, $r_i \mid n - 1$. If $q_i^{e_i} \nmid r_i$, then, as $r_i \mid n - 1$, the power of $q_i$ in $r_i$ is at most $e_i - 1$, so $r_i \mid (n - 1)/q_i$ and $a_i^{(n-1)/q_i} \equiv 1$, a contradiction. So $q_i^{e_i} \mid r_i$, and by Lemma 1, $q_i^{e_i} \mid \varphi(n)$. The $q_i^{e_i}$ are pairwise coprime, so their product $n - 1$ divides $\varphi(n)$. Since $1 \le \varphi(n) \le n - 1$, this forces $\varphi(n) = n - 1$. Then each of $1, \ldots, n - 1$ is coprime to $n$, so $n$ has no divisor $d$ with $1 < d < n$, and $n$ is prime. $\square$

**Lemma 3 (primes have the bases).** Let $n \ge 3$ be prime, and let $g$ be a primitive root modulo $n$. Then $g^{n-1} \equiv 1$ and $g^{(n-1)/q_i} \not\equiv 1 \pmod n$ for each $i$.

*Proof.* The group of units modulo a prime is cyclic of order $n - 1$, so a primitive root $g$ exists, with order $n - 1$. Then $g^{n-1} \equiv 1$, and since $0 < (n - 1)/q_i < n - 1$, $g^{(n-1)/q_i} \not\equiv 1$. $\square$

**Lemma 4 (each search ends).** Let $n \ge 3$. For each $i$, the loop of lines L4 to L7 ends after at most $p - 1$ bases, where $p$ is the smallest prime factor of $n$ if $n$ is composite, and the least primitive root $g$ of $n$ if $n$ is prime, with $g \le n - 1$.

*Proof.* The loop tries $a = 2, 3, \ldots$ and ends at line L5 or line L6. If $n$ is composite and the loop reaches $a = p$, then $p \mid a^{n-1}$, so $a^{n-1} \not\equiv 1 \pmod n$ (as $p \nmid 1$), and line L5 returns. If $n$ is prime and the loop reaches $a = g$, then by Lemma 3 line L5 does not fire and line L6 exits the loop. In both cases the loop ends no later than at that base, which is at most $n - 1$. $\square$

**Theorem.** For every valid input, LUCAS$(n, q_1, \ldots, q_m)$ ends, and it returns true if and only if $n$ is prime.

*Proof.* *Termination.* Line L1 ends the call for $n < 3$. Otherwise the outer loop has $m$ passes, and each inner loop ends by Lemma 4.

*The case $n < 3$.* Line L1 returns true for $n = 2$, the only prime below 3, and false for $n = 0$ and $n = 1$.

*False is right.* Let $n \ge 3$ be prime. By Lemma 4, every base tried satisfies $2 \le a \le g \le n - 1$, so $\gcd(a, n) = 1$, and $a^{n-1} \equiv 1 \pmod n$ by Fermat's little theorem. So line L5 never returns false for a prime, and line L1 does not either. Hence false is returned only for composite $n$ or $n < 2$.

*True is right.* Line L8 is reached only when, for each $i$, line L6 exited the loop with some base $a_i$. That base passed line L5, so $a_i^{n-1} \equiv 1$, and line L6 gives $a_i^{(n-1)/q_i} \not\equiv 1$. By Lemma 2, $n$ is prime.

*Primes return true.* If $n \ge 3$ is prime, no base ever fails line L5, and by Lemma 4 each search exits through line L6. So the call reaches line L8 and returns true. $\blacksquare$
