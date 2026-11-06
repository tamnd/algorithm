---
title: LLL with deep insertions terminates and returns a size-reduced, deep-reduced basis of the same lattice
proves: [correctness, termination]
status: full
---

**Setting.** The input is $n \ge 1$ linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ and a parameter $\delta$ with $1/4 < \delta \le 1$. We write $b_i^*$ for the Gram-Schmidt vectors, $N_i = \|b_i^*\|^2$, $\mu_{kj} = \langle b_k, b_j^* \rangle / N_j$, and $\pi_i$ for the orthogonal projection onto $\operatorname{span}(b_1, \ldots, b_{i-1})^\perp$, so that $\pi_i(b_k) = b_k^* + \sum_{j = i}^{k-1} \mu_{kj} b_j^*$ and

$$\|\pi_i(b_k)\|^2 = N_k + \sum_{j=i}^{k-1} \mu_{kj}^2 N_j.$$

Indices are $1, \ldots, n$ here; the implementation counts from 0. A basis is **deep-reduced** with parameter $\delta$ if it is size-reduced, $|\mu_{kj}| \le 1/2$ for all $j < k$, and $\|\pi_i(b_k)\|^2 \ge \delta N_i$ for all $i < k$.

**Lemma 1 (the lattice is preserved).** Every step replaces the basis by another basis of the same lattice.

*Proof.* Line L3 replaces $b_k$ by $b_k - q b_j$ with $q \in \mathbb{Z}$ and $j < k$, an elementary unimodular operation. Line L6 moves $b_k$ to position $i$ and shifts $b_i, \ldots, b_{k-1}$ up by one, a permutation of the rows. Both are integer matrices with determinant $\pm 1$. $\square$

**Lemma 2 (size reduction).** After line L3, $|\mu_{kj}| \le 1/2$ for every $j < k$, and the Gram-Schmidt vectors are unchanged.

*Proof.* Subtracting $q b_j$ from $b_k$ does not change $\operatorname{span}(b_1, \ldots, b_{k-1})$ or the component of $b_k$ orthogonal to it, so no $b_l^*$ changes. It changes $\mu_{kl}$ by $-q \mu_{jl}$ for $l < j$, by $-q$ for $l = j$, and not at all for $l > j$. The loop runs $j = k-1, \ldots, 1$ and chooses $q$ as the nearest integer to the current $\mu_{kj}$, so afterwards $|\mu_{kj}| \le 1/2$, and later iterations (with smaller $j$) do not touch $\mu_{kj}$ again. $\square$

**Lemma 3 (the running value).** At line L6 with index $i$, the variable $C$ equals $\|\pi_i(b_k)\|^2$.

*Proof.* Line L4 sets $C = \|b_k\|^2 = \|\pi_1(b_k)\|^2$, and line L7 subtracts $\mu_{ki}^2 N_i$, which is the difference $\|\pi_i(b_k)\|^2 - \|\pi_{i+1}(b_k)\|^2$ by the formula above. $\square$

**Lemma 4 (invariant).** Whenever the loop at line L2 tests its condition, the first $k - 1$ vectors form a deep-reduced basis of the lattice they generate.

*Proof.* Initially $k = 2$, and one vector is deep-reduced. Suppose the invariant holds and a pass runs. Line L3 changes only $b_k$. If no insertion happens, then by Lemma 3 $\|\pi_i(b_k)\|^2 \ge \delta N_i$ for every $i < k$, and by Lemma 2 $b_k$ is size-reduced, so the first $k$ vectors are deep-reduced, and line L8 increments $k$. If an insertion at position $i$ happens, the vectors $b_1, \ldots, b_{i-1}$ are unchanged, and so are their Gram-Schmidt data; the new $k$ is $\max(i, 2)$, and the first $\max(i, 2) - 1$ vectors are either $b_1, \ldots, b_{i-1}$ or, when $i = 1$, the single new vector $b_1$. In both cases they are deep-reduced. $\square$

**Lemma 5 (an insertion decreases the Gram determinants lexicographically).** Let $D_j = \prod_{l \le j} N_l$ be the Gram determinant of $b_1, \ldots, b_j$. An insertion at position $i$ leaves $D_1, \ldots, D_{i-1}$ unchanged and replaces $D_i$ by a value less than $\delta D_i \le D_i$. Size reduction changes no $D_j$.

*Proof.* The first $i - 1$ vectors are unchanged. The new $i$-th Gram-Schmidt vector is the component of $b_k$ orthogonal to $b_1, \ldots, b_{i-1}$, which is $\pi_i(b_k)$, and the insertion happens only if $\|\pi_i(b_k)\|^2 < \delta N_i$ (Lemma 3). So the new $D_i$ is $D_{i-1} \|\pi_i(b_k)\|^2 < \delta D_i$. Size reduction changes no $b_l^*$ (Lemma 2). $\square$

**Termination.** Let $s$ be a common denominator of the input entries. Every basis in the run generates the same lattice $L$ (Lemma 1), so every vector has entries in $\frac1s \mathbb{Z}$, and each $D_j$, a Gram determinant of $j$ such vectors, lies in $s^{-2j} \mathbb{Z}_{>0}$. So the tuple $(s^2 D_1, s^4 D_2, \ldots, s^{2n} D_n)$ is a tuple of positive integers, and by Lemma 5 it strictly decreases in the lexicographic order at every insertion. The lexicographic order on $\mathbb{Z}_{>0}^n$ is a well-order, so there are finitely many insertions. Between two insertions, $k$ only increases, so at most $n - 1$ passes occur. Hence the algorithm terminates.

**Correctness.** When the loop exits, $k = n + 1$, and by Lemma 4 the whole basis is deep-reduced; by Lemma 1 it generates the input lattice. Taking $i = k - 1$ in the deep condition gives $N_k + \mu_{k,k-1}^2 N_{k-1} \ge \delta N_{k-1}$, the Lovász condition, so the output is also LLL-reduced with parameter $\delta$, and the LLL bounds apply: with $\alpha = 1/(\delta - 1/4)$, $\|b_1\|^2 \le \alpha^{n-1} \lambda_1^2$.

**Theorem.** For $1/4 < \delta \le 1$, the algorithm terminates on every valid input and returns a basis of the same lattice that is size-reduced and deep-reduced with parameter $\delta$, hence also LLL-reduced. Each pass of the main loop costs $O(n^2 m)$ arithmetic operations when Gram-Schmidt is recomputed, as in the implementation. The number of passes is finite but is not bounded here by a polynomial; no such bound is known for unrestricted deep insertions. $\blacksquare$
