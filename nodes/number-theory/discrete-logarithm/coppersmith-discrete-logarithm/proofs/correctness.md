---
title: Correctness of Coppersmith's algorithm
proves: [correctness, termination]
status: full
---

Let $f = x^n + f_1$ be irreducible over $\mathbb{F}_2$, so $K = \mathbb{F}_2[x]/(f)$ is the field with $2^n$ elements and $K^*$ is cyclic of order $N = 2^n - 1$. Let $g \in K^*$ have order $r$ and let $h \in K^*$. Let $\gamma$ be the generator of line L3 and $L(y) \in \mathbb{Z}/N\mathbb{Z}$ the logarithm of $y \in K^*$ to base $\gamma$, so $L(y_1 y_2) = L(y_1) + L(y_2)$. A polynomial $a \in \mathbb{F}_2[x]$ with $f \nmid a$ has a nonzero image in $K$, and we write $L(a)$ for the logarithm of that image. Let $\ell = \prod q^e$ over the prime powers $q^e \parallel N$ with $q \mid r$; then $r \mid \ell \mid N$, and $\ell$ is odd since $N$ is odd. For termination we treat the exponents $m$ of lines L9 and L13 as independent and uniform on $\{0, \dots, N - 1\}$.

**Lemma 1 (membership and the trivial target).** Line L1 returns NONE exactly when $h \notin \langle g \rangle$, and line L2 is correct.

*Proof.* $K^*$ is cyclic, so its only subgroup of order $r$ is $\{y : y^r = 1\}$, which is $\langle g \rangle$. If $h = 1$, then $x = 0$. $\square$

From now on $h = g^{x^*}$ with $0 \le x^* < r$, unique because $g$ has order $r$, and $h \ne 1$, so $r \ge 2$.

**Lemma 2 (the Frobenius identity).** For all $A, B \in \mathbb{F}_2[x]$ and $C = A x^l + B$, with $2^k l \ge n$, the polynomial $D = A(x^{2^k}) \, x^{2^k l - n} f_1 + B(x^{2^k})$ satisfies $C^{2^k} \equiv D \pmod f$.

*Proof.* In a commutative ring of characteristic $2$, $(u + v)^2 = u^2 + v^2$, and by induction $(u + v)^{2^k} = u^{2^k} + v^{2^k}$ and $(uv)^{2^k} = u^{2^k} v^{2^k}$. For $a = \sum a_i x^i$ with $a_i \in \{0, 1\}$, this gives $a^{2^k} = \sum a_i x^{2^k i} = a(x^{2^k})$. So $C^{2^k} = A(x^{2^k}) \, x^{2^k l} + B(x^{2^k})$. Since $f = x^n + f_1$, we have $x^n \equiv f_1 \pmod f$, and $x^{2^k l} = x^{2^k l - n} x^n \equiv x^{2^k l - n} f_1$. $\square$

**Lemma 3 (relations).** Every pair $(e, k')$ in $R$ satisfies $\sum_{s \in S} e_s L(s) \equiv k' \pmod N$.

*Proof.* Every $s \in S$ has degree at most $b \le n - 1$, so $f \nmid s$ and $L(s)$ is defined. A row from line L7 comes from a pair with $f \nmid C$, $C = \prod s^{c_s}$ and $D = \prod s^{d_s}$ in $\mathbb{F}_2[x]$. By Lemma 2, $D \equiv C^{2^k} \pmod f$, which is nonzero in $K$ since $C$ is. Applying $L$ gives $\sum_s d_s L(s) = 2^k \sum_s c_s L(s)$, that is, $\sum_s (2^k c_s - d_s) L(s) \equiv 0$, which is the row $(2^k c - d, 0)$. Line L4 takes $l = \lceil n / 2^k \rceil$, so $2^k l \ge n$ and Lemma 2 applies. A row from line L9 has $\gamma^m \equiv \prod s^{e_s}$, and applying $L$ gives $m \equiv \sum_s e_s L(s)$. $\square$

**Lemma 4 (SOLVE).** Let $M = q^e$ with $q$ prime and $M \mid N$. If SOLVE$(R, q, M)$ returns a vector $\lambda$, then $\lambda_s \equiv L(s) \pmod M$ for every $s \in S$.

*Proof.* By Lemma 3, the vector $X = (L(s) \bmod M)_s$ satisfies every row modulo $M$, because $M \mid N$. Lines L19 and L20 swap two rows, multiply a row by a unit modulo $M$ (an entry not divisible by $q$ is coprime to $M$), or subtract a multiple of one row from another. Each operation is invertible, so the set of solutions modulo $M$ is unchanged, and $X$ is still a solution afterwards. After column $j$ has been processed, row $j$ has a $1$ in column $j$ and every other row has $0$ there, and later steps keep this, since they add multiples of rows whose entry in column $j$ is $0$. When all columns are processed, row $j$ reads $X_j \equiv$ (right side of row $j$) $\pmod M$, so the returned $\lambda_j$ equals $X_j$. $\square$

**Lemma 5 (scale).** After line L11, $\lambda_s \equiv L(s) \pmod \ell$ for every $s \in S$.

*Proof.* Line L11 is passed only when every SOLVE succeeded, so by Lemma 4, $\lambda^{(q)}_s \equiv L(s) \pmod{q^e}$ for each $q^e \parallel \ell$. These moduli are pairwise coprime, and the Chinese remainder theorem gives a unique residue modulo $\ell$ with these reductions, which is $L(s) \bmod \ell$. $\square$

**Lemma 6 (medium polynomials).** If line L14 assigns a value to $L(G_i)$, the value is the true $L(G_i) \bmod \ell$.

*Proof.* Every $G_i$ has degree at most $\min(n - 1, 2b) < n$, so $f \nmid G_i$ and $L(G_i)$ is defined. Line L14 accepts $(A, B)$ only if $f \nmid C$, $C = G_i^a \prod s^{c_s}$ with $\gcd(a, \ell) = 1$, and $D = \prod s^{d'_s}$. By Lemma 2 and the argument of Lemma 3, $2^k (a L(G_i) + \sum_s c_s L(s)) \equiv \sum_s d'_s L(s) \pmod N$, and so modulo $\ell$. Since $\ell$ is odd, $2^k$ is a unit modulo $\ell$, and $a$ is a unit by the test. Solving, $L(G_i) \equiv (2^{-k} \sum_s d'_s L(s) - \sum_s c_s L(s)) \, a^{-1} \pmod \ell$, and by Lemma 5 the $\lambda_s$ may replace the $L(s)$. $\square$

**Lemma 7 (individual logarithms).** For $y \in \{g, h\}$, the value of line L16 is the true $L(y) \bmod \ell$.

*Proof.* Line L15 is passed only when $z = y \gamma^m \bmod f$ equals $\prod s^{d_s} \prod G_i^{a_i}$ in $\mathbb{F}_2[x]$ and every $G_i$ got a value. Then $L(y) + m \equiv \sum_s d_s L(s) + \sum_i a_i L(G_i) \pmod N$. Reducing modulo $\ell$ and using Lemmas 5 and 6 gives line L16. $\square$

**Lemma 8 (conversion).** With $c = \ell / r$, the residue $L(g) \bmod \ell$ is $c u$ for an integer $u$ coprime to $r$, the residue $L(h) \bmod \ell$ is divisible by $c$, and $(L(h)/c) \, u^{-1} \equiv x^* \pmod r$.

*Proof.* Since $g$ has order $r$ and $\gamma$ has order $N$, $\gcd(L(g), N) = N / r$. For each prime $q \mid r$ with $q^a \parallel r$ and $q^e \parallel N$, the $q$-adic valuation of $L(g)$, taken as an integer in $[0, N - 1]$, is exactly $e - a$, which is also the valuation of $c$ at $q$; and $c$ has no other prime factors, since $\ell$ has only primes dividing $r$. Reducing modulo $\ell$ does not change the valuation at $q$ when it is below $e$, so $L(g) \bmod \ell = c u$ with $u$ prime to every $q \mid r$, that is, coprime to $r$. Next, $h = g^{x^*}$ gives $L(h) \equiv x^* c u \pmod \ell$, which is divisible by $c$, and dividing by $c$ gives $L(h) / c \equiv x^* u \pmod{\ell / c}$, that is, modulo $r$. Multiplying by $u^{-1}$ modulo $r$ gives $x^*$. $\square$

**Correctness.** By Lemmas 7 and 8, line L18 returns $x^* \bmod r = x^*$. With Lemma 1, the algorithm returns $x^*$ if $h \in \langle g \rangle$ and NONE otherwise.

**Termination.** The loop of lines L5 to L7 runs over a finite set of pairs. For the loop of lines L8 to L11, fix $s \in S$. Each trial has $\gamma^m = s$ with probability $1/N$, and then line L9 appends the row with $e_s = 1$, all other entries $0$, and right side $L(s)$. With probability $1$, every $s \in S$ eventually contributes such a row, and $R$ eventually has at least $|S| + 10$ rows. Once the rows include the unit vectors for all $s$, every SOLVE succeeds. Indeed, the row that started as the unit vector for column $j$ has entry $0$ in every earlier column, so it is never chosen as a pivot for an earlier column and is never changed by the clearing steps, which subtract a multiple of a pivot row only from rows with a nonzero entry in the pivot column. A swap at column $j' < j$ moves only rows at positions at least $j'$, so this row stays at a position at least $j$ until column $j$ is processed, and then its entry $1$ is a unit pivot. The implementation retries SOLVE after each new row of line L9, so a successful attempt occurs. For the loop of lines L13 to L15, each trial has $z = 1$ with probability $1/N$; then $z$ is the empty product, there are no $G_i$, and line L15 is passed. Each search of line L14 is over a finite set. Hence the algorithm stops with probability $1$. $\blacksquare$
