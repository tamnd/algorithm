---
title: FWHT computes the Walsh-Hadamard transform, and INVERSE-FWHT inverts it
proves: [correctness, complexity]
status: full
---

Let $R$ be a commutative ring, $n = 2^t$, and $x \in R^n$ the input. For $0 \le i, j < n$ write $i_q$ for the binary digit of $i$ at position $q$, so $\langle i, j \rangle = \sum_q i_q j_q$ and $(H_n)_{ji} = (-1)^{\langle i, j \rangle}$. Write $x'$ for the array as the algorithm changes it. For $0 \le q \le t$, let $i \sim_q j$ mean that $i$ and $j$ agree in every position $r \ge q$, and let $\langle i, j \rangle_{<q} = \sum_{r < q} i_r j_r$.

**Invariant (I).** When line L3 tests $h = 2^q$,

$$x'_j = \sum_{i \sim_q j} (-1)^{\langle i, j \rangle_{<q}} \, x_i \qquad \text{for each } 0 \le j < n.$$

*Initialization.* For $q = 0$, $i \sim_0 j$ means $i = j$, and the empty sum in the exponent is $0$, so (I) says $x'_j = x_j$, which holds before the first pass.

*Maintenance.* Let (I) hold for $h = 2^q < n$. Lines L4 and L5 visit each $j$ with $j_q = 0$ exactly once: the block start $s$ is a multiple of $2h$ and $s \le j < s + h$. Its partner $j + h$ differs from $j$ only in position $q$. The pairs $\{j, j + h\}$ are disjoint, and line L7 reads and writes only the two cells of one pair, so the new values are $x''_j = x'_j + x'_{j+h}$ and $x''_{j+h} = x'_j - x'_{j+h}$, computed from the values of (I).

Fix $j$ with $j_q = 0$ and let $j^+ = j + h$. The set $\{i : i \sim_{q+1} j\}$ is the disjoint union of $\{i \sim_q j\}$ (those with $i_q = 0$) and $\{i \sim_q j^+\}$ (those with $i_q = 1$). For $i \sim_q j^+$, $\langle i, j^+ \rangle_{<q} = \langle i, j \rangle_{<q}$ because $j$ and $j^+$ agree below $q$. Hence

$$x''_j = \sum_{i \sim_{q+1} j} (-1)^{\langle i, j \rangle_{<q}} x_i = \sum_{i \sim_{q+1} j} (-1)^{\langle i, j \rangle_{<q+1}} x_i,$$

since $j_q = 0$ makes the term $i_q j_q$ zero, and

$$x''_{j^+} = \sum_{i \sim_q j,\ i_q = 0} (-1)^{\langle i, j \rangle_{<q}} x_i - \sum_{i \sim_q j^+,\ i_q = 1} (-1)^{\langle i, j \rangle_{<q}} x_i = \sum_{i \sim_{q+1} j^+} (-1)^{\langle i, j^+ \rangle_{<q} + i_q} x_i,$$

and $i_q = i_q j^+_q$ because $j^+_q = 1$, so the exponent is $\langle i, j^+ \rangle_{<q+1}$. Every index is $j$ or $j^+$ for exactly one pair, so (I) holds for $2h$ after line L8.

*Termination.* The loop ends at $h = n$, $q = t$. Then $i \sim_t j$ holds for every pair, and $\langle i, j \rangle_{<t} = \langle i, j \rangle$, so $x'_j = \sum_i (-1)^{\langle i, j \rangle} x_i = (H_n x)_j$.

**Theorem 1.** FWHT$(x)$ replaces $x$ by $H_n x$.

*Proof.* The invariant and its termination. $\square$

**Lemma 2.** $H_n H_n = n I$.

*Proof.* $(H_n H_n)_{jk} = \sum_i (-1)^{\langle i, j \rangle + \langle i, k \rangle} = \sum_i (-1)^{\langle i, j \oplus k \rangle}$, since $j_q + k_q \equiv (j \oplus k)_q \pmod 2$. If $j = k$ every term is $1$ and the sum is $n$. Otherwise pick a position $r$ with $(j \oplus k)_r = 1$. The map $i \mapsto i \oplus 2^r$ is an involution of $\{0, \ldots, n-1\}$ with no fixed points that changes the sign of each term. So the terms split into pairs $\{i, i \oplus 2^r\}$ whose two terms cancel, and the sum is $0$ in each ring. $\square$

**Theorem 2.** If $n$ is a unit of $R$, INVERSE-FWHT$(H_n x)$ returns $x$.

*Proof.* Line L9 computes $H_n H_n x = n x$ by Theorem 1 and Lemma 2, and line L10 divides by $n$. $\blacksquare$

**Theorem 3 (XOR convolution).** For $a, b \in R^n$ let $c_k = \sum_{i \oplus j = k} a_i b_j$. Then $H_n c = H_n a \cdot H_n b$ entrywise.

*Proof.* $(H_n c)_m = \sum_k (-1)^{\langle k, m \rangle} \sum_{i \oplus j = k} a_i b_j = \sum_{i, j} a_i b_j (-1)^{\langle i \oplus j, m \rangle}$, and $(-1)^{\langle i \oplus j, m \rangle} = (-1)^{\langle i, m \rangle} (-1)^{\langle j, m \rangle}$ by the same parity identity. The double sum then factors as $(H_n a)_m (H_n b)_m$. $\square$

**Operation count.** The loop of line L3 runs for $h = 1, 2, \ldots, n/2$, that is $t = \lg n$ times. Each pass visits $n/(2h)$ blocks of $h$ pairs, so $n/2$ pairs, and line L7 does one addition and one subtraction per pair. In total $n \lg n$ additions and subtractions and no multiplications; INVERSE-FWHT adds $n$ divisions.
