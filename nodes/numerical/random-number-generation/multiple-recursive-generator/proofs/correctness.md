---
title: An MRG with a primitive characteristic polynomial has period m^k - 1 from every non-zero seed
proves: [correctness]
status: full
---

Let $m$ be a prime, $k \ge 1$, $a_1, \ldots, a_k \in \mathbb{Z}_m$ with $a_k \ne 0$, and $P(z) = z^k - a_1 z^{k-1} - \cdots - a_k$. MRG-NEXT maps the state $s = (x_1, \ldots, x_k)$, newest first, to $M s$ where $M$ is the companion matrix of the page: line L2 computes the first coordinate $\sum_j a_j x_j$, and lines L3 and L4 shift the others down. All arithmetic is in the field $\mathbb{F} = \mathbb{Z}_m$, and $V = \mathbb{F}^k$.

**Lemma 1.** The characteristic polynomial of $M$ is $P$, and $M$ is invertible.

*Proof.* Expanding $\det(zI - M)$ along the first row, the standard computation for a companion matrix, gives $\det(zI - M) = z^k - a_1 z^{k-1} - \cdots - a_k = P(z)$. Setting $z = 0$ gives $\det(-M) = P(0) = -a_k$, so $\det M = \pm a_k \ne 0$. $\square$

**Lemma 2.** Every non-zero $s$ has period exactly $m^k - 1$ under $M$ if and only if $M$ has order $m^k - 1$, if and only if $P$ is primitive modulo $m$ (irreducible, with $z$ of order $m^k - 1$ modulo $P$).

*Proof.* Let $N = m^k - 1$ and let $A = \mathbb{F}[M]$, a commutative ring of dimension at most $k$ over $\mathbb{F}$ by the Cayley-Hamilton theorem, so $|A| \le m^k$.

*Periods and order.* If every non-zero $s$ has period $N$, then $M^N s = s$ for all $s$, so $M^N = I$, and no smaller positive power is $I$. Conversely, suppose $M$ has order $N$. Then $I, M, \ldots, M^{N-1}$ are $N$ distinct invertible elements of $A$, and $0 \in A$, so $A$ has exactly $m^k$ elements, all non-zero ones invertible, and $A$ is a field. For $s \ne 0$ with period $\rho$, $(M^\rho - I) s = 0$, so $M^\rho - I \in A$ is not invertible, hence $M^\rho = I$ and $N \mid \rho$. With $\rho \le N$, $\rho = N$.

*Order and primitivity.* If $M$ has order $N$, $A$ is a field with $m^k$ elements, isomorphic to $\mathbb{F}[z]/(\mu)$ with $\mu$ the minimal polynomial of $M$, so $\mu$ is irreducible of degree $k$. Since $\mu \mid P$ and both are monic of degree $k$, $\mu = P$, and $z$ has order $N$ modulo $P$, so $P$ is primitive. Conversely, if $P$ is primitive, it is irreducible, so $\mu = P$, $A \cong \mathbb{F}[z]/(P)$ with $M \mapsto z$, and $M$ has order $N$. $\square$

**Lemma 3 (Knuth's test).** Let $r = (m^k - 1)/(m - 1)$ and $g = (-1)^{k-1} a_k$. $P$ is primitive if and only if (i) $g$ is a primitive root modulo $m$, (ii) $z^r \equiv g \pmod P$, and (iii) $z^{r/q} \bmod P$ is not a constant for every prime $q \mid r$.

*Proof.* Suppose $P$ is primitive, so $K = \mathbb{F}[z]/(P)$ is a field with $m^k$ elements and $\alpha = z$ generates $K^*$. The norm of $\alpha$ to $\mathbb{F}$ is $\alpha^{1 + m + \cdots + m^{k-1}} = \alpha^r$, and it equals the product of the roots of $P$, which is $(-1)^k$ times the constant term $-a_k$, that is $g$. So (ii) holds. The elements of $K$ fixed by $x \mapsto x^m$ are exactly $\mathbb{F}$, and $\beta = \alpha^e$ lies in $\mathbb{F}$ if and only if $\beta^{m - 1} = 1$, if and only if $N \mid e(m-1)$, if and only if $r \mid e$. So $\alpha^{r/q} \notin \mathbb{F}$ for a prime $q \mid r$, which is (iii). The order of $g = \alpha^r$ is $N / r = m - 1$, which is (i).

Conversely, assume (i) to (iii). Since $P(0) = -a_k \ne 0$, $z$ is invertible modulo $P$. Let $E$ be the set of integers $e$ for which $z^e$ is congruent to a constant modulo $P$. The constants that occur are non-zero, because $z^e$ is invertible, and products and inverses of non-zero constants are constants, so $E$ is a subgroup of $\mathbb{Z}$, namely $E = d_0 \mathbb{Z}$ for some $d_0 > 0$. By (ii), $r \in E$, so $d_0 \mid r$. If $d_0 < r$, some prime $q$ divides $r / d_0$, so $d_0 \mid r / q$ and $r/q \in E$, contradicting (iii). Hence $d_0 = r$. Let $d$ be the order of $z$ modulo $P$. Since $z^d = 1$ is a constant, $d \in E$, so $d = r t$ for some $t \ge 1$, and $1 = z^{rt} = g^t$. By (i), $g$ has order $m - 1$, so $(m - 1) \mid t$ and $d \ge r (m-1) = N$. Also $z^N = (z^r)^{m-1} = g^{m-1} = 1$, so $d = N$. Finally, the residues $1, z, \ldots, z^{N-1}$ are $N = m^k - 1$ distinct invertible residues modulo $P$, so every non-zero residue is invertible, $\mathbb{F}[z]/(P)$ is a field, and $P$ is irreducible. With $z$ of order $N$, $P$ is primitive. $\square$

**Theorem.** If $P$ is primitive modulo the prime $m$, then for every seed $s_0 \ne 0$, the sequence of MRG-NEXT has period exactly $m^k - 1$, and the states $s_1, \ldots, s_{m^k - 1}$ are all the non-zero vectors of $V$. Each non-zero value of $x_n$ occurs $m^{k-1}$ times per period and 0 occurs $m^{k-1} - 1$ times.

*Proof.* By Lemma 1, $M$ is invertible with characteristic polynomial $P$; by Lemma 2, every non-zero state has period $N = m^k - 1$. The orbit of $s_0$ is $N$ distinct non-zero vectors, which is all of $V \setminus \{0\}$. The output $x_n$ is the first coordinate of the state $s_n$. Among the non-zero vectors, those with first coordinate $v \ne 0$ number $m^{k-1}$, and those with first coordinate 0 number $m^{k-1} - 1$. $\blacksquare$
