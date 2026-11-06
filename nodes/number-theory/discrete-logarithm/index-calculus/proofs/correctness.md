---
title: Correctness of index calculus
proves: [correctness, termination]
status: full
---

Let $p$ be prime, $g \in (\mathbb{Z}/p\mathbb{Z})^*$ of order $n$, and $h \in (\mathbb{Z}/p\mathbb{Z})^*$. Let $\gamma$ be the generator of line L3 and $L(y) \in \mathbb{Z}/(p - 1)\mathbb{Z}$ the logarithm of $y$ to base $\gamma$, so $L(y_1 y_2) = L(y_1) + L(y_2)$. Let $\ell = \prod q^f$ over the prime powers $q^f \parallel p - 1$ with $q \mid n$. Since $n \mid p - 1$, every prime power $q^e \parallel n$ satisfies $e \le f$, so $n \mid \ell$. For termination we treat the exponents $k$ of lines L6 and L11 as independent and uniform on $\{0, \dots, p - 2\}$.

**Lemma 1 (membership and the trivial target).** Line L1 returns NONE exactly when $h \notin \langle g \rangle$, and line L2 is correct.

*Proof.* $(\mathbb{Z}/p\mathbb{Z})^*$ is cyclic, so its only subgroup of order $n$ is $\{y : y^n = 1\}$, which is $\langle g \rangle$. If $h = 1$, then $x = 0$. $\square$

From now on $h = g^{x^*}$ with $0 \le x^* < n$, unique because $g$ has order $n$, and $h \ne 1$, so $n \ge 2$.

**Lemma 2 (relations).** Every pair $(e, k)$ in $R$ satisfies $\sum_{s \in S} e_s L(s) \equiv k \pmod{p - 1}$.

*Proof.* Line L7 appends $(e, k)$ only if $\gamma^k \equiv \prod_s s^{e_s} \pmod p$. Every $s \in S$ is a prime below $p$, so $s \in (\mathbb{Z}/p\mathbb{Z})^*$, and applying $L$ gives $k \equiv \sum_s e_s L(s)$. $\square$

**Lemma 3 (SOLVE).** Let $m = q^f$ with $q$ prime. If SOLVE$(R, q, m)$ returns a vector $\lambda$, then $\lambda_s \equiv L(s) \pmod m$ for every $s \in S$.

*Proof.* By Lemma 2 the vector $X = (L(s) \bmod m)_s$ satisfies every row modulo $m$, because $m \mid p - 1$. Lines L15 and L16 swap two rows, multiply a row by a unit modulo $m$ (an entry not divisible by $q$ is coprime to $m$), or subtract a multiple of one row from another. Each operation is invertible, so the set of solutions modulo $m$ of the system is unchanged, and $X$ is still a solution afterwards. After the column $j$ has been processed, row $j$ has a $1$ in column $j$ and every other row has $0$ there, and later steps keep this, since they add multiples of rows whose entry in column $j$ is $0$. When all columns are processed, row $j$ reads $X_j \equiv \text{(right side of row } j) \pmod m$. So the returned $\lambda_j$ equals $X_j$. $\square$

**Lemma 4 (individual logarithms).** After lines L9 and L12, $\lambda_s \equiv L(s) \pmod \ell$ for every $s$, and $L(y)$ of line L12 is the true $L(y) \bmod \ell$ for $y \in \{g, h\}$.

*Proof.* Line L9 is reached only when every SOLVE succeeded, so by Lemma 3, $\lambda^{(q)} \equiv L(s) \pmod{q^f}$ for each $q^f \parallel \ell$. These moduli are pairwise coprime, and the Chinese remainder theorem gives a unique residue modulo $\ell$ with these reductions, which is $L(s) \bmod \ell$. At line L11, $y \gamma^k \equiv \prod s^{d_s}$, so $L(y) + k \equiv \sum d_s L(s) \pmod{p - 1}$, and reducing modulo $\ell \mid p - 1$ gives line L12. $\square$

**Lemma 5 (conversion).** With $c = \ell / n$, the residue $L(g) \bmod \ell$ is $c u$ for an integer $u$ coprime to $n$, the residue $L(h) \bmod \ell$ is divisible by $c$, and $(L(h)/c) u^{-1} \equiv x^* \pmod n$.

*Proof.* Since $g$ has order $n$ and $\gamma$ has order $p - 1$, $\gcd(L(g), p - 1) = (p - 1)/n$. For each prime $q \mid n$ with $q^e \parallel n$ and $q^f \parallel p - 1$, the $q$-adic valuation of $L(g)$, taken as an integer in $[0, p - 2]$, is exactly $f - e$, which is also the valuation of $c$ at $q$; and $c$ has no other prime factors, since $\ell$ has only primes dividing $n$. Reducing modulo $\ell$ does not change the valuation at $q$ when it is below $f$, so $L(g) \bmod \ell = c u$ with $u$ prime to every $q \mid n$, that is, coprime to $n$. Next, $h = g^{x^*}$ gives $L(h) \equiv x^* L(g) \equiv x^* c u \pmod \ell$, which is divisible by $c$, and dividing by $c$ gives $L(h)/c \equiv x^* u \pmod{\ell / c}$, that is, modulo $n$. Multiplying by $u^{-1}$ modulo $n$ gives $x^*$. $\square$

**Correctness.** By Lemmas 4 and 5, line L14 returns $x^* \bmod n = x^*$. With Lemma 1, the algorithm returns $x^*$ if $h \in \langle g \rangle$ and NONE otherwise.

**Termination.** The descent of line L11 stops with probability $1$: for each trial, $y \gamma^k$ is uniform in $(\mathbb{Z}/p\mathbb{Z})^*$ and equals $1$, which is smooth, with probability $1/(p - 1)$. For the loop of lines L5 to L9, fix $s \in S$. Each trial has $\gamma^k = s$ with probability $1/(p - 1)$, and then line L7 appends the row with $e_s = 1$, all other entries $0$, and right side $L(s)$. With probability $1$, every $s \in S$ eventually contributes such a row. Once the relations include the unit vectors for all $s$, every SOLVE succeeds: before column $j$ is processed, the row that started as the unit vector for column $j$ has been changed only by subtracting multiples of earlier pivot rows, which subtracts multiples of its entries in earlier columns, all $0$, so it still has entry $1$ in column $j$, which is a unit. The attempts at line L8 happen every $5$ new relations, so a successful attempt occurs. Hence the algorithm stops with probability $1$. $\blacksquare$
