---
title: Correctness of the Pollard-Strassen algorithm
proves: [correctness, termination]
status: full
---

Let $N \ge 2$, let $B$ be the least integer with $B^4 \ge N$, and write $R = \mathbb{Z}/N\mathbb{Z}$. For $j = 0, 1, \dots, B - 1$ let $I_j = \{jB + 1, \dots, jB + B\}$. The blocks are disjoint and their union is $\{1, 2, \dots, B^2\}$. Let $p$ be the least prime factor of $N$.

**Termination.** Lines L2 and L3 run a fixed number of polynomial operations, each a finite loop. Lines L4 to L6 are loops over at most $B$ blocks of $B$ elements. So the algorithm stops.

**Lemma 1 (division by a monic polynomial).** Let $g \in R[x]$ be monic of degree $d \ge 1$. For every $a \in R[x]$ there are unique $q, r \in R[x]$ with $a = qg + r$ and $\deg r < d$.

*Proof.* Existence, by induction on $\deg a$. If $\deg a < d$, take $q = 0$, $r = a$. Otherwise let $c$ be the leading coefficient of $a$ and $e = \deg a$. Then $a - c x^{e - d} g$ has degree less than $e$, because $g$ is monic, and the induction hypothesis applies to it. Uniqueness: if $qg + r = q'g + r'$, then $(q - q')g = r' - r$. If $q \ne q'$, the left side has degree $\deg(q - q') + d \ge d$, because the leading coefficient of $g$ is $1$ and so the leading coefficient of $(q - q')g$ is that of $q - q'$, which is not zero. The right side has degree less than $d$. So $q = q'$ and $r = r'$. $\square$

Write $a \bmod g$ for this $r$. The map $a \mapsto a \bmod g$ is $R$-linear, and $a \bmod g = 0$ exactly when $g \mid a$.

**Lemma 2 (remainders and evaluation).** (a) For $a \in R$, $f \bmod (x - a) = f(a)$. (b) If $g$ and $h$ are monic and $h \mid g$, then $(f \bmod g) \bmod h = f \bmod h$.

*Proof.* (a) Write $f = q(x - a) + r$ with $r$ a constant, by Lemma 1. Substitute $x = a$: $f(a) = r$. (b) Write $f = qg + r$ with $r = f \bmod g$, and $g = sh$. Then $f = (qs)h + r$, so $f \bmod h = (qs h) \bmod h + r \bmod h = r \bmod h$, by linearity. $\square$

**Lemma 3 (the remainder tree).** Let $T$ be the subproduct tree of the monic polynomials $x - a_0, \dots, x - a_{k-1}$: each inner node is the product of its children, and each node is monic and divides its parent. Put $f \bmod (\text{root})$ at the root, and at each child the remainder of its parent's value modulo the child. Then the value at the leaf $x - a_j$ is $f(a_j)$.

*Proof.* By induction down the tree, the value at each node $g$ is $f \bmod g$. This holds at the root. If it holds at a parent $P$ with a child $Q$, then $Q \mid P$, and the value at $Q$ is $(f \bmod P) \bmod Q = f \bmod Q$, by Lemma 2(b). At a leaf $x - a_j$, Lemma 2(a) gives $f(a_j)$. A node that is copied to the next level because it has no partner has itself as its only child, and $(f \bmod Q) \bmod Q = f \bmod Q$. $\square$

**Lemma 4 (the implementation of division).** For monic $g$ of degree $d$ and $a$ of formal degree $m \ge d$, the implementation computes $a \bmod g$ correctly.

*Proof.* Write $\tilde u(x) = x^{e} u(1/x)$ for the reversal of a polynomial $u$ of formal degree $e$. From $a = qg + r$ with $\deg q \le m - d$ and $\deg r < d$, reversal gives $\tilde a = \tilde q \tilde g + x^{m - d + 1} \tilde r'$ for some polynomial $\tilde r'$. The constant term of $\tilde g$ is $1$, because $g$ is monic, so $\tilde g$ is invertible modulo $x^{m - d + 1}$ and $\tilde q \equiv \tilde a \tilde g^{-1} \pmod{x^{m - d + 1}}$. Since $\deg \tilde q \le m - d$, this congruence determines $\tilde q$, hence $q$, and $r = a - qg$.

The inverse comes from Newton's iteration: if $g h \equiv 1 \pmod{x^t}$ and $h' = h(2 - gh)$, then $1 - gh' = (1 - gh)^2 \equiv 0 \pmod{x^{2t}}$. Starting from $h = 1$, which is correct modulo $x$, the iteration doubles the precision until it reaches $m - d + 1$. The schoolbook branch is the existence step of Lemma 1 applied coefficient by coefficient from the top.

Polynomial products use either the schoolbook sum or Kronecker substitution. In the latter, the coefficients $a_i, b_j \in [0, N)$ are written as digits in base $2^{8w}$, where $2^{8w} > \min(\ell_a, \ell_b) N^2$ for the lengths $\ell_a, \ell_b$. Each coefficient $c_k = \sum_{i + j = k} a_i b_j$ of the integer product of the polynomials is a sum of at most $\min(\ell_a, \ell_b)$ terms below $N^2$, so $0 \le c_k < 2^{8w}$. Hence the product of the packed integers has the digits $c_k$ with no carries, and unpacking and reducing modulo $N$ gives the product in $R[x]$. $\square$

**Lemma 5 (the block values).** For each $j$, $v_j \equiv \prod_{k \in I_j} k \pmod N$.

*Proof.* In $\mathbb{Z}[x]$, $(x + 1)(x + 2) \cdots (x + B)$ evaluated at $x = jB$ is $\prod_{i = 1}^{B} (jB + i) = \prod_{k \in I_j} k$. Reduction modulo $N$ is a ring homomorphism $\mathbb{Z}[x] \to R[x]$ that commutes with evaluation, so the polynomial $f$ of line L2 satisfies $f(jB) = \prod_{k \in I_j} k \bmod N$. Line L3 computes $f(jB)$ by Lemmas 3 and 4. $\square$

**Lemma 6 (a gcd above 1).** $\gcd(v_j, N) > 1$ if and only if some $k \in I_j$ has $\gcd(k, N) > 1$.

*Proof.* By Lemma 5, $\gcd(v_j, N) = \gcd(\prod_{k \in I_j} k, N)$, since $v_j$ and the product differ by a multiple of $N$. If a prime $\ell$ divides $N$ and the product, then $\ell$ divides some factor $k$, so $\gcd(k, N) > 1$. Conversely, if $\ell$ divides $N$ and some $k \in I_j$, it divides the product. $\square$

**Lemma 7 (nothing below $p$).** Every integer $k$ with $1 \le k < p$ has $\gcd(k, N) = 1$.

*Proof.* If $\gcd(k, N) > 1$, then some prime $\ell$ divides both, so $\ell \le k < p$ and $\ell \mid N$, against the choice of $p$ as the least prime factor. For $k = 1$ the gcd is $1$. $\square$

**Theorem.** The algorithm returns $p$.

*Proof.* Case 1: $p \le B^2$. Let $J$ be the index with $p \in I_J$. Then $\gcd(p, N) = p > 1$, so $\gcd(v_J, N) > 1$ by Lemma 6. For $j < J$, every $k \in I_j$ satisfies $k \le jB + B \le JB < p$, so $\gcd(k, N) = 1$ by Lemma 7, and $\gcd(v_j, N) = 1$ by Lemma 6. So the loop of line L4 reaches line L6 first at $j = J$. There, every $d \in I_J$ with $2 \le d < p$ is not a divisor of $N$: a divisor $d \ge 2$ of $N$ has a prime factor that divides $N$ and is at most $d$, so $d \ge p$. And $p \in I_J$ divides $N$. So line L6 returns $p$.

Case 2: $p > B^2$. Then $p > B^2 \ge \sqrt N$. If $N$ were composite, then $N = p \cdot (N/p)$ with $N/p \ge p$, so $p \le \sqrt N$, a contradiction. So $N$ is prime and $p = N$. Every $k \le B^2$ satisfies $k < p$, so by Lemmas 6 and 7 no block has a gcd above $1$, and line L7 returns $N = p$.

In both cases the output is the least prime factor of $N$.

For the full factorization, each pass of the driver divides out every power of the least prime factor $p$ of what is left. All prime factors of the cofactor $m$ are then larger than $p$. If $1 < m < p^2$, then $m$ cannot have two prime factors, each above $p$, so $m$ is prime. The cofactor decreases at every pass, so the driver stops, and the primes collected multiply to the input. $\blacksquare$
