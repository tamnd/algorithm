---
title: BERLEKAMP returns the irreducible factors of a square-free polynomial
proves: [correctness]
status: full
---

Let $p$ be a prime, $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$, and $f = q_1 \cdots q_r \in \mathbb{F}_p[x]$ monic of degree $n$ with distinct monic irreducible $q_i$. Let $A = \mathbb{F}_p[x]/(f)$, and identify a polynomial $v$ of degree less than $n$ with its coefficient vector and with its class in $A$. The Berlekamp algebra is $B = \{ v \in A : v^p = v \}$.

**Lemma 1 ($B$ is the left null space).** $v^p \bmod f = v Q$, so $B = \{ v : v (Q - I) = 0 \}$.

*Proof.* In characteristic $p$, $(y + z)^p = y^p + z^p$, and $c^p = c$ for $c \in \mathbb{F}_p$ by Fermat's little theorem. So $v^p = \left(\sum_i v_i x^i\right)^p = \sum_i v_i x^{p i}$. Reducing modulo $f$ replaces $x^{p i}$ by row $i$ of $Q$, so $v^p \bmod f = \sum_i v_i Q_i = v Q$. $\square$

**Lemma 2 (structure).** The map $\chi(v) = (v \bmod q_1, \ldots, v \bmod q_r)$ is a bijection from $B$ onto $\mathbb{F}_p^r$, where $\mathbb{F}_p$ is the set of constants in each $K_i = \mathbb{F}_p[x]/(q_i)$. In particular $\dim B = r$.

*Proof.* The $q_i$ are pairwise coprime, so by the Chinese remainder theorem $\chi$ is a ring isomorphism from $A$ onto $\prod_i K_i$, and $v^p = v$ holds in $A$ exactly when it holds in every $K_i$. Each $K_i$ is a field, so $y^p - y$ has at most $p$ roots in $K_i$, and the $p$ constants are roots by Fermat's little theorem. So the solutions in $K_i$ are exactly the constants, and $\chi(B) = \mathbb{F}_p^r$. $\chi$ is $\mathbb{F}_p$-linear, so $\dim B = r$. $\square$

Write $s_i(v) \in \mathbb{F}_p$ for the constant with $v \equiv s_i(v) \pmod{q_i}$.

**Lemma 3 (one gcd step).** Let $h$ be a monic product of some of the $q_i$, and $v \in B$. Then the nonconstant $\gcd(v - s, h)$ for $s \in \mathbb{F}_p$ are the products $\prod \{ q_i \mid h : s_i(v) = s \}$ over the values $s$ that occur, so they form a partition of the factors of $h$.

*Proof.* For $q_i \mid h$, $q_i \mid v - s$ exactly when $s = s_i(v)$. As $h$ is square-free, $\gcd(v - s, h)$ is the product of the $q_i \mid h$ with $q_i \mid v - s$. Each $q_i \mid h$ lies in exactly one of these gcds. $\square$

**Basis.** Line L2 returns $r$ vectors that form a basis of the left null space, which is $B$ by Lemma 1 and has dimension $r$ by Lemma 2. The vector $1$ is in $B$, since row $0$ of $Q$ is $(1, 0, \ldots, 0)$; the elimination returns it first because column $0$ of $(Q - I)^T$ is zero.

**Invariant.** After each pass of the loop at line L4, with the basis vectors $v_2, \ldots, v_j$ used so far, the list of pieces is a list of monic polynomials that partitions $\{ q_1, \ldots, q_r \}$, and two factors $q_a, q_b$ are in the same piece if and only if $s_a(v_t) = s_b(v_t)$ for all $2 \le t \le j$.

*Proof.* Before the loop, the list of pieces is $[f]$, and the condition over an empty set of $t$ is true. In a pass with $v_j$, Lemma 3 replaces each piece $h$ by its parts with equal $s_i(v_j)$, which refines the partition exactly by the new condition. A piece of degree $1$ that the implementation keeps unchanged has one factor, so it satisfies the condition trivially. $\square$

**The loop stops with irreducible pieces.** If the loop runs through all $j \le r$, then two factors $q_a \ne q_b$ in the same piece would have $s_a(v_t) = s_b(v_t)$ for all $t$, including $t = 1$, where $v_1 = 1$. Since the $v_t$ span $B$, $s_a(v) = s_b(v)$ for every $v \in B$. But by Lemma 2 there is $v \in B$ with $\chi(v) = e_a$, the vector with $1$ at $a$ and $0$ elsewhere, which has $s_a(v) = 1 \ne 0 = s_b(v)$. So every piece has one factor. If the loop stops early because there are $r$ pieces, then the partition into $r$ nonempty parts of a set of size $r$ also has one factor per piece. The loop has at most $r - 1$ passes, and each pass computes finitely many gcds, so it stops, and line L10 returns $q_1, \ldots, q_r$. $\blacksquare$
