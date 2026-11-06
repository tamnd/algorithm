---
title: BKZ with an exact block oracle terminates and returns a BKZ-reduced basis of the same lattice
proves: [correctness, termination]
status: full
---

**Setting.** The input is $n \ge 1$ linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$, a block size $\beta \ge 2$ and a parameter $\delta$ with $1/4 < \delta \le 1$. We write $b_i^*$ for the Gram-Schmidt vectors, $N_i = \|b_i^*\|^2$, $\mu_{ij} = \langle b_i, b_j^* \rangle / N_j$ for $j < i$, and $\pi_k$ for the orthogonal projection onto $\operatorname{span}(b_1, \ldots, b_{k-1})^\perp$. For $1 \le k \le n$ let $h(k) = \min(k + \beta - 1, n)$ and let

$$L_{[k]} = \pi_k\big(L(b_k, \ldots, b_{h(k)})\big)$$

be the projected block lattice, with basis $\pi_k(b_k), \ldots, \pi_k(b_{h(k)})$. Indices are $1, \ldots, n$ here; the implementation counts from 0. Write $D_j = N_1 \cdots N_j$, the Gram determinant of $b_1, \ldots, b_j$.

A basis is **BKZ-reduced** with block size $\beta$ and parameter $\delta$ if it is LLL-reduced with parameter $\delta$ (size-reduced, $|\mu_{ij}| \le 1/2$, and $N_{k+1} + \mu_{k+1,k}^2 N_k \ge \delta N_k$) and

$$\delta N_k \le \lambda_1(L_{[k]})^2 \qquad \text{for } k = 1, \ldots, n. \tag{1}$$

For $k = n$ the block lattice is $\mathbb{Z} b_n^*$, so (1) holds for every basis; only $k \le n - 1$ needs checking.

**Lemma 1 (the block coordinates).** For a coefficient vector $x \in \mathbb{Z}^d$, $d = h - k + 1$, write $v = \sum_{j=0}^{d-1} x_j b_{k+j}$. Then

$$\|\pi_k(v)\|^2 = \sum_{j=0}^{d-1} (x_j - c_j)^2 N_{k+j}, \qquad c_j = -\sum_{i = j+1}^{d-1} x_i \mu_{k+i, k+j},$$

and $\pi_k(v) = 0$ only for $x = 0$.

*Proof.* Each $b_{k+i} = b_{k+i}^* + \sum_{l < k+i} \mu_{k+i, l} b_l^*$, and $\pi_k$ removes the terms with $l < k$. Collecting the coefficient of $b_{k+j}^*$ gives $x_j + \sum_{i > j} x_i \mu_{k+i,k+j} = x_j - c_j$. The $b_l^*$ are pairwise orthogonal, so the squared length is the weighted sum. If it is 0, then $x_{d-1} = c_{d-1} = 0$, then $x_{d-2} = c_{d-2} = 0$, and so on down to $x_0 = 0$. $\square$

**Lemma 2 (the block oracle is exact).** On line L4, the enumeration returns a nonzero $x \in \mathbb{Z}^d$ with $\|\pi_k(\sum_j x_j b_{k+j})\|^2 = \lambda_1(L_{[k]})^2$, and the value it returns is this squared length.

*Proof.* The search keeps a value $\mathit{best}$, initially $N_k$, the squared length for $x = (1, 0, \ldots, 0)$, so $\mathit{best}$ is always the squared length of some nonzero vector of $L_{[k]}$ and never increases. It fixes $x_{d-1}, x_{d-2}, \ldots, x_0$ in this order. With $x_{j+1}, \ldots, x_{d-1}$ fixed, let $\rho_{j+1} = \sum_{i > j} (x_i - c_i)^2 N_{k+i}$; by Lemma 1 every completion has squared length at least $\rho_{j+1} + (x_j - c_j)^2 N_{k+j}$. Call $x_j$ *feasible* when this partial value is at most $\mathit{best}$.

At a new level the scan starts at $x_j = \lfloor c_j \rfloor - \lfloor \sqrt{\lfloor q \rfloor} \rfloor - 1$ with $q = \max(\mathit{best} - \rho_{j+1}, 0) / N_{k+j}$. Every integer $x \le$ this start has $c_j - x \ge \lfloor \sqrt{\lfloor q \rfloor} \rfloor + 1 > \sqrt q$, because $(\lfloor \sqrt{\lfloor q \rfloor} \rfloor + 1)^2$ is an integer above $\lfloor q \rfloor$, so it is at least $\lfloor q \rfloor + 1 > q$. Hence $(x - c_j)^2 N_{k+j} > \mathit{best} - \rho_{j+1}$, and no value below the start is feasible. The scan then raises $x_j$ by 1 while $x_j$ is infeasible and $x_j \le c_j$. If it stops at an infeasible $x_j > c_j$, every larger integer is further from $c_j$ and also infeasible, so the level is finished. Otherwise $x_j$ is feasible, and the search descends; when it comes back, it continues with $x_j + 1$. Because $\mathit{best}$ only decreases, a value that was infeasible when it was skipped stays infeasible. So every feasible prefix is visited, and every leaf with squared length at most the final $\mathit{best}$ is reached; at a leaf $j = 0$, the search replaces $\mathit{best}$ when the value is smaller and $x \ne 0$.

Every level scans a bounded interval of integers, of length at most $2 \sqrt{N_k / N_{k+j}} + 3$, so the search ends. At the end, $\mathit{best}$ is at most the squared length of every nonzero $x$, and it is attained by the stored $x$. $\square$

**Lemma 3 (the inserted vector is primitive).** If line L5 succeeds, the coefficient vector $x$ has $\gcd(x_0, \ldots, x_{d-1}) = 1$.

*Proof.* The map $x \mapsto \pi_k(\sum_j x_j b_{k+j})$ is linear and injective by Lemma 1. If $g = \gcd(x) > 1$, then $x / g$ is a nonzero integer vector whose image has squared length $\|\pi_k(v)\|^2 / g^2 < \|\pi_k(v)\|^2$, which contradicts the minimality from Lemma 2. $\square$

**Lemma 4 (the insertion).** On line L6, with $\gcd(x) = 1$, the procedure replaces $b_k, \ldots, b_h$ by vectors $b_k', \ldots, b_h'$ that generate the same lattice as $b_k, \ldots, b_h$, with $b_k' = \sum_j x_j b_{k+j}$. The rows outside positions $k, \ldots, h$ do not change.

*Proof.* The procedure runs $j = d-2, \ldots, 0$ and keeps a coefficient vector $y$, initially $x$, with the invariant that $\sum_j y_j b_{k+j}$ (with the current rows) equals the original $v = \sum_j x_j b_{k+j}$ and that $y_{j+1}, \ldots, y_{d-1}$ are 0 after step $j$. At step $j$, if $y_j = y_{j+1} = 0$ nothing happens. Otherwise let $g = \gcd(y_j, y_{j+1}) > 0$ and $s y_j + t y_{j+1} = g$, and put $p = y_j / g$, $q = y_{j+1} / g$. The rows $u = b_{k+j}$, $w = b_{k+j+1}$ become $u' = p u + q w$ and $w' = -t u + s w$. The matrix $\begin{pmatrix} p & q \\ -t & s \end{pmatrix}$ has determinant $(s y_j + t y_{j+1}) / g = 1$, so the two rows generate the same lattice as before, and $y_j u + y_{j+1} w = g u' + 0 \cdot w'$, so the invariant holds with $y_j \leftarrow g$, $y_{j+1} \leftarrow 0$. After step $j$, $y_j$ is the gcd of $x_j, \ldots, x_{d-1}$, up to the case where all of them are 0. After step 0, $y = (\gcd(x), 0, \ldots, 0) = (1, 0, \ldots, 0)$, so $b_k' = v$. Each step is unimodular on two adjacent rows of the block. $\square$

**Lemma 5 (the LLL subroutine).** Lines L1 and L7 terminate and return an LLL-reduced basis of the same lattice, and each swap they make strictly decreases one $D_j$ and keeps the others.

*Proof.* The subroutine is LLL with size reduction against all earlier rows. Size reduction subtracts integer multiples of earlier rows, which is unimodular and keeps every $b_i^*$. A swap of $b_{k-1}$ and $b_k$ is a permutation. By the standard invariant, the rows before the current index are LLL-reduced, so when the index passes $n$ the basis is LLL-reduced. A swap happens when $N_k + \mu_{k,k-1}^2 N_{k-1} < \delta N_{k-1}$; the left side is the new $N_{k-1}$, so $D_{k-1}$ drops by a factor less than $\delta \le 1$, and $D_j$ for $j \ne k - 1$ is the Gram determinant of the same set of rows, so it is unchanged. Let $s$ be a common denominator of the input entries; all rows stay in $\frac1s \mathbb{Z}^m$, so $s^{2j} D_j$ is a positive integer. The positive integer $\sum_j s^{2j} D_j$ decreases at each swap, and between swaps the index rises at most $n - 1$ times, so the subroutine ends. $\square$

**Lemma 6 (the loop invariant).** At each test of line L2:

1. the current basis generates the input lattice and is LLL-reduced;
2. the last $z$ steps made no insertion, the basis has not changed during them, and condition (1) holds for the $z$ indices they examined, which are $z$ consecutive values of $k$ in the cyclic order $1, 2, \ldots, n-1, 1, \ldots$

*Proof.* Before the first test, line L1 makes the basis LLL-reduced (Lemma 5) and $z = 0$. Consider one step at index $k$. If line L5 fails, line L4 computed $\lambda_1(L_{[k]})^2$ exactly (Lemma 2) and found it at least $\delta N_k$, which is (1) for $k$; the basis is unchanged, $z$ grows by 1, and the next index is the cyclic successor of $k$, so part 2 holds. If line L5 succeeds, lines L6 and L7 replace the basis by another basis of the same lattice (Lemmas 3, 4 and 5) that is LLL-reduced, and $z$ becomes 0, so part 2 holds trivially. $\square$

**Lemma 7 (termination).** The loop ends after at most $(I + 1)(n - 1)$ steps, where $I$ is the number of insertions, and $I$ is finite.

*Proof.* Consider an insertion at index $k$. Rows $b_1, \ldots, b_{k-1}$ do not change, so $D_1, \ldots, D_{k-1}$ do not change. The new $b_k^*$ is $\pi_k(v)$, so the new $N_k$ is the value from line L4, which is less than $\delta N_k \le N_k$; hence $D_k$ strictly decreases. The swaps of the following LLL call each strictly decrease one $D_j$ and keep the others. So the tuple $T = (s^2 D_1, s^4 D_2, \ldots, s^{2n} D_n)$ of positive integers strictly decreases in lexicographic order at each insertion and at each swap, even when $D_{k+1}, \ldots$ grow. The lexicographic order on $n$-tuples of positive integers is a well-order, so there are finitely many insertions. A step without insertion raises $z$ by 1, so at most $n - 2$ such steps lie between two insertions and at most $n - 1$ come after the last one, when $z$ reaches $n - 1$. Each step terminates, by Lemmas 2 and 5. $\square$

**Theorem.** The procedure terminates and returns a BKZ-reduced basis, with block size $\beta$ and parameter $\delta$, of the input lattice.

*Proof.* By Lemma 7 the loop ends, and it ends when $z = n - 1$. By Lemma 6 the basis then generates the input lattice and is LLL-reduced, and the last $n - 1$ steps examined $n - 1$ consecutive indices in a cyclic order of length $n - 1$, which are all of $1, \ldots, n-1$, on the same basis. So (1) holds for $k \le n - 1$, and for $k = n$ it always holds. For $n = 1$ the loop does not run, and the single row is trivially BKZ-reduced. $\blacksquare$
