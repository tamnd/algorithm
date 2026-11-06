---
title: Correctness of the function field sieve
proves: [correctness, termination]
status: full
---

Let $p$ be prime, let $F_1$ and $F_2$ be monic polynomials over $\mathbb{F}_p$, and let $f$ be monic irreducible of degree $n \ge 2$ with $f \mid F_2(F_1(t)) - t$. Then $K = \mathbb{F}_p[t]/(f)$ is the field with $p^n$ elements and $K^*$ is cyclic of order $N = p^n - 1$. Let $g \in K^*$ have order $r$ and let $h \in K^*$. Let $\gamma$ be the generator of line L3 and $L(z) \in \mathbb{Z}/N\mathbb{Z}$ the logarithm of $z \in K^*$ to base $\gamma$, so $L(z_1 z_2) = L(z_1) + L(z_2)$. Let $\varphi_1 : \mathbb{F}_p[x] \to K$ be the ring map with $x \mapsto t$ and $\varphi_2 : \mathbb{F}_p[y] \to K$ the ring map with $y \mapsto F_1(t)$. For $s \in S_1$ write $L(s)$ for $L(\varphi_1 s)$, and for $s \in S_2$ write $L(s)$ for $L(\varphi_2 s)$; the two bases give separate unknowns. Let $\ell = \prod q^e$ over the prime powers $q^e \parallel N$ with $q \mid r$; then $r \mid \ell \mid N$. For termination we treat the exponents $m$ of lines L9 and L13 and the index $j$ of line L9 as independent and uniform.

**Lemma 1 (membership and the trivial target).** Line L1 returns NONE exactly when $h \notin \langle g \rangle$, and line L2 is correct.

*Proof.* $K^*$ is cyclic, so its only subgroup of order $r$ is $\{z : z^r = 1\}$, which is $\langle g \rangle$. If $h = 1$, then $x = 0$. $\square$

From now on $h = g^{x^*}$ with $0 \le x^* < r$, unique because $g$ has order $r$, and $h \ne 1$, so $r \ge 2$.

**Lemma 2 (constants).** Let $\omega = \gamma^{N/(p-1)}$. Then $\omega$ generates $\mathbb{F}_p^* \subset K^*$, and $L(\omega^i) = i N / (p - 1)$.

*Proof.* $\omega$ has order $p - 1$, and $\mathbb{F}_p^*$ is the unique subgroup of $K^*$ of order $p - 1$, so $\omega$ is a constant and generates $\mathbb{F}_p^*$. The formula follows from $\omega^i = \gamma^{i N/(p-1)}$. $\square$

**Lemma 3 (the commutative diagram).** For all $A, B \in \mathbb{F}_p[x]$ and $G = A(x) + B(x) y$, with $\psi_1(G) = A(x) + B(x) F_1(x)$ and $\psi_2(G) = A(F_2(y)) + B(F_2(y)) y$, we have $\varphi_1(\psi_1(G)) = \varphi_2(\psi_2(G))$.

*Proof.* $\varphi_1(\psi_1(G)) = A(t) + B(t) F_1(t)$ in $K$. Since $\varphi_2$ is a ring map, $\varphi_2(\psi_2(G)) = A(F_2(F_1(t))) + B(F_2(F_1(t))) F_1(t)$. Since $f \mid F_2(F_1(t)) - t$, we have $F_2(F_1(t)) = t$ in $K$, and the two sides agree. $\square$

**Lemma 4 (relations).** Every row $(a, -b; k)$ of $R$ satisfies $\sum_{s \in S_1} a_s L(s) - \sum_{s \in S_2} b_s L(s) \equiv k \pmod N$.

*Proof.* Every $s \in S_1$ has degree at most $D \le n - 1$, so $\varphi_1(s) \ne 0$. Every $s \in S_2$ has $\varphi_2(s) \ne 0$ by line L4. So all the $L(s)$ are defined. A row from line L7 comes from $G$ with $f \nmid \psi_1(G)$, so $z = \varphi_1(\psi_1(G)) \ne 0$, and $z = \varphi_2(\psi_2(G))$ by Lemma 3. With $\psi_1(G) = c_1 \prod s^{a_s}$ and $\psi_2(G) = c_2 \prod s^{b_s}$, applying $L$ to the two expressions for $z$ gives $L(c_1) + \sum a_s L(s) = L(c_2) + \sum b_s L(s)$, which is the row, with $L(c_1)$ and $L(c_2)$ given by Lemma 2. A row from line L10 has $\gamma^m \varphi_2(s_j) = c \prod_{s \in S_1} \varphi_1(s)^{a_s}$ in $K$, where the factor $\varphi_2(s_j)$ is absent if $j$ is none. Applying $L$ gives $m + L(s_j) = L(c) + \sum a_s L(s)$, which is the row with $-1$ in column $j$ and right side $m - L(c)$. $\square$

**Lemma 5 (SOLVE).** Let $M = q^e$ with $q$ prime and $M \mid N$. If SOLVE$(R, q, M)$ returns a vector $\lambda$, then $\lambda_s \equiv L(s) \pmod M$ for every unknown $s$.

*Proof.* By Lemma 4, the vector $X = (L(s) \bmod M)_s$ satisfies every row modulo $M$, because $M \mid N$. Lines L19 and L20 swap two rows, multiply a row by a unit modulo $M$ (an entry not divisible by $q$ is coprime to $M$), or subtract a multiple of one row from another. Each operation is invertible, so the set of solutions modulo $M$ is unchanged, and $X$ is still a solution afterwards. After column $j$ has been processed, row $j$ has a $1$ in column $j$ and every other row has $0$ there, and later steps keep this, since they add multiples of rows whose entry in column $j$ is $0$. When all columns are processed, row $j$ reads $X_j \equiv$ (right side of row $j$) $\pmod M$, so the returned $\lambda_j$ equals $X_j$. $\square$

**Lemma 6 (scale).** After line L11, $\lambda_s \equiv L(s) \pmod \ell$ for every unknown $s$.

*Proof.* Line L11 is passed only when every SOLVE succeeded, so by Lemma 5, $\lambda^{(q)}_s \equiv L(s) \pmod{q^e}$ for each $q^e \parallel \ell$. These moduli are pairwise coprime, and the Chinese remainder theorem gives a unique residue modulo $\ell$ with these reductions, which is $L(s) \bmod \ell$. $\square$

**Lemma 7 (medium polynomials).** If line L14 assigns a value to $L(G_i)$, the value is the true $L(\varphi_1 G_i) \bmod \ell$.

*Proof.* Every $G_i$ has degree at most $\min(2D, n - 1) < n$, so $\varphi_1(G_i) \ne 0$ and its logarithm is defined. Line L14 accepts $G$ only if $f \nmid \psi_1(G)$, $\psi_1(G) = G_i^a c_1 \prod_{S_1} s^{a_s}$ with $\gcd(a, \ell) = 1$, and $\psi_2(G) = c_2 \prod_{S_2} s^{b_s}$. By Lemma 3 and the argument of Lemma 4, $a L(G_i) + L(c_1) + \sum a_s L(s) \equiv L(c_2) + \sum b_s L(s) \pmod N$, and so modulo $\ell$. Since $a$ is a unit modulo $\ell$, $L(G_i) \equiv (L(c_2) + \sum b_s L(s) - L(c_1) - \sum a_s L(s)) \, a^{-1} \pmod \ell$, and by Lemma 6 the $\lambda_s$ may replace the $L(s)$. $\square$

**Lemma 8 (individual logarithms).** For $y \in \{g, h\}$, the value of line L16 is the true $L(y) \bmod \ell$.

*Proof.* Line L15 is passed only when $z = y \gamma^m \bmod f$ equals $c \prod_{S_1} s^{d_s} \prod G_i^{u_i}$ in $\mathbb{F}_p[x]$ and every $G_i$ got a value. Applying $\varphi_1$ and $L$ gives $L(y) + m \equiv L(c) + \sum_s d_s L(s) + \sum_i u_i L(G_i) \pmod N$. Reducing modulo $\ell$ and using Lemmas 2, 6 and 7 gives line L16. $\square$

**Lemma 9 (conversion).** With $c = \ell / r$, the residue $L(g) \bmod \ell$ is $c u$ for an integer $u$ coprime to $r$, the residue $L(h) \bmod \ell$ is divisible by $c$, and $(L(h)/c) \, u^{-1} \equiv x^* \pmod r$.

*Proof.* Since $g$ has order $r$ and $\gamma$ has order $N$, $\gcd(L(g), N) = N / r$. For each prime $q \mid r$ with $q^a \parallel r$ and $q^e \parallel N$, the $q$-adic valuation of $L(g)$, taken as an integer in $[0, N - 1]$, is exactly $e - a$, which is also the valuation of $c$ at $q$; and $c$ has no other prime factors, since $\ell$ has only primes dividing $r$. Reducing modulo $\ell$ does not change the valuation at $q$ when it is below $e$, so $L(g) \bmod \ell = c u$ with $u$ prime to every $q \mid r$, that is, coprime to $r$. Next, $h = g^{x^*}$ gives $L(h) \equiv x^* c u \pmod \ell$, which is divisible by $c$, and dividing by $c$ gives $L(h) / c \equiv x^* u \pmod{\ell / c}$, that is, modulo $r$. Multiplying by $u^{-1}$ modulo $r$ gives $x^*$. $\square$

**Correctness.** By Lemmas 8 and 9, line L18 returns $x^* \bmod r = x^*$. With Lemma 1, the algorithm returns $x^*$ if $h \in \langle g \rangle$ and NONE otherwise.

**Termination.** The loop of lines L5 to L7 runs over a finite set of pairs. For the loop of lines L8 to L11, fix an unknown. For $s \in S_1$, each trial has $j$ = none and $\gamma^m = \varphi_1(s)$ with positive probability, and then line L10 appends the row with $1$ in the column of $s$, $0$ elsewhere, and right side $L(s)$. For $s_j \in S_2$, each trial picks this $j$ and has $\gamma^m = \varphi_2(s_j)^{-1}$ with positive probability; then $z = 1$, which is the empty product with $c = 1$, and line L10 appends the row with $-1$ in the column of $s_j$, $0$ elsewhere, and right side $m$. With probability $1$, every unknown eventually gets such a row, and $R$ eventually has at least $t + 10$ rows. Once the rows include these rows for all unknowns, every SOLVE succeeds. Indeed, the row that has its only nonzero entry, $\pm 1$, in column $j$ has entry $0$ in every earlier column, so it is never chosen as a pivot for an earlier column and is never changed by the clearing steps, which subtract a multiple of a pivot row only from rows with a nonzero entry in the pivot column. A swap at column $j' < j$ moves only rows at positions at least $j'$, so this row stays at a position at least $j$ until column $j$ is processed, and then its entry $\pm 1$ is a unit pivot. The implementation retries SOLVE after each new row of line L10, so a successful attempt occurs. For the loop of lines L13 to L15, each trial has $z = 1$ with probability $1/N$; then there are no $G_i$, and line L15 is passed. Each search of line L14 is over a finite set. Hence the algorithm stops with probability $1$. $\blacksquare$
