---
title: Kannan's algorithm terminates and returns an HKZ-reduced basis of the same lattice
proves: [correctness, termination]
status: full
---

**Setting.** The input is $n \ge 1$ linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of the lattice $L$. We write $b_i^*$ for the Gram-Schmidt vectors, $N_i = \|b_i^*\|^2$, $\mu_{ij} = \langle b_i, b_j^* \rangle / N_j$ for $j < i$, and $\pi_k$ for the orthogonal projection onto $\operatorname{span}(b_1, \ldots, b_{k-1})^\perp$, so that $\pi_k(L) = \pi_k(L(b_k, \ldots, b_n))$ is a lattice of rank $n - k + 1$ with basis $\pi_k(b_k), \ldots, \pi_k(b_n)$ and Gram-Schmidt norms $N_k, \ldots, N_n$. Line numbers refer to the pseudocode on the page; indices are $1, \ldots, n$ here, while the implementation counts from 0. The basis is **HKZ-reduced** when it is size-reduced, $|\mu_{ij}| \le 1/2$, and

$$N_k = \lambda_1(\pi_k(L))^2 \qquad \text{for } k = 1, \ldots, n. \tag{1}$$

We say that the basis is **HKZ from $k$** when (1) holds for $k, k+1, \ldots, n$. This depends only on $b_1, \ldots, b_{k-1}$ (through $\pi_k$) and on the projections $\pi_k(b_k), \ldots, \pi_k(b_n)$.

Let $s$ be a common denominator of the input entries. All operations below are integer row operations, so the rows stay in $\frac1s \mathbb{Z}^m$ and $s^{2j} D_j$, with $D_j = N_1 \cdots N_j$, is a positive integer.

**Lemma 1 (row operations).** Each of the following keeps $L$ and the rows $b_1, \ldots, b_{k-1}$, hence keeps $\pi_k$ and the lattice $\pi_k(L)$:

1. adding an integer multiple of an earlier row to a row at position $\ge k$;
2. swapping two adjacent rows at positions $\ge k$;
3. replacing $b_k, \ldots, b_n$ by an integer unimodular combination of them.

Operation 1 does not change any $b_i^*$.

*Proof.* All three are unimodular operations on the rows that do not touch positions below $k$. Adding a multiple of an earlier row to $b_i$ keeps $\operatorname{span}(b_1, \ldots, b_{i-1})$ and the component of $b_i$ orthogonal to it, so no Gram-Schmidt vector changes. $\square$

**Lemma 2 (line L4).** The LLL step on positions $k, \ldots, n$ terminates; it uses only operations 1 and 2 of Lemma 1.

*Proof.* Size reduction is operation 1 and keeps every $D_j$. A swap of positions $j - 1, j$ with $j - 1 \ge k$ is done only when $N_j + \mu_{j,j-1}^2 N_{j-1} < \tfrac34 N_{j-1}$; the left side is the new $N_{j-1}$, so $D_{j-1}$ decreases and the other $D_i$ are Gram determinants of the same sets of rows. The positive integer $\sum_j s^{2j} D_j$ therefore decreases at each swap, and between two swaps the position rises at most $n$ times. $\square$

**Lemma 3 (line L7 is exact).** The enumeration returns a nonzero $x \in \mathbb{Z}^{n-k+1}$ such that $\pi_k(\sum_i x_i b_{k+i})$ is a shortest nonzero vector of $\pi_k(L)$, together with its squared length.

*Proof.* By the Gram-Schmidt decomposition, $\|\pi_k(\sum_{j \ge 0} x_j b_{k+j})\|^2 = \sum_j (x_j - c_j)^2 N_{k+j}$ with $c_j = -\sum_{i > j} x_i \mu_{k+i,k+j}$, and this is 0 only for $x = 0$. The search starts with the value $N_k$ of $x = (1, 0, \ldots, 0)$ and fixes the coordinates from the last to the first. At each level it skips only values $x_j$ whose partial sum already exceeds the current best: below the start of its scan by the choice $\lfloor c_j \rfloor - \lfloor \sqrt{\lfloor q \rfloor} \rfloor - 1$ with $q = \max(\mathit{best} - \rho, 0)/N_{k+j}$, since then $c_j - x_j > \sqrt q$; while rising from below $c_j$; and above $c_j$ once a value fails, since all further values are further from $c_j$. The best value only decreases, so a skipped value stays useless. Every level scans a bounded interval, so the search ends, and it returns the minimum over all nonzero $x$. This is the same search as in [BKZ](/bkz-algorithm/), where the proof is written out in full. $\square$

**Lemma 4 (line L8).** If the enumeration finds a squared length smaller than $N_k$, then $\gcd(x) = 1$, and the gcd sweep replaces $b_k, \ldots, b_n$ by a unimodular combination whose first vector is $v = \sum_i x_i b_{k+i}$. Afterwards $N_k = \lambda_1(\pi_k(L))^2$.

*Proof.* If $g = \gcd(x) > 1$, then $x / g$ would give a vector of squared length smaller by the factor $g^2$, which contradicts Lemma 3. The sweep runs from the end of the block to its front and, for two adjacent rows $u, w$ with current coefficients $y_j, y_{j+1}$ not both 0, uses $g = \gcd(y_j, y_{j+1}) = s y_j + t y_{j+1}$ to replace them by $\frac{y_j}{g} u + \frac{y_{j+1}}{g} w$ and $-t u + s w$. This $2 \times 2$ matrix has determinant 1 and keeps $\sum_j y_j b_{k+j}$ with $y_j \leftarrow g$, $y_{j+1} \leftarrow 0$. At the end the coefficients are $(1, 0, \ldots, 0)$, so the new $b_k$ is $v$. This is operation 3 of Lemma 1, so $\pi_k$ is unchanged and the new $b_k^* = \pi_k(v)$ is a shortest nonzero vector of $\pi_k(L)$. $\square$

**Calls.** The stack starts with the single task $(1, \mathrm{start})$. When a task $(k, \mathrm{start})$ is popped with the rest of the stack equal to $\sigma$, call the run from that moment until the stack is again equal to $\sigma$ the **call at $k$**. Every task pushed while it runs has index at least $k$ and lies above $\sigma$.

**Lemma 5 (one call).** For every $k$, a call at $k$ terminates. It does not change $b_1, \ldots, b_{k-1}$ or $L$, and when it ends the basis is HKZ from $k$.

*Proof.* By downward induction on $k$.

*Case $k = n$.* Line L3 discards the task. The lattice $\pi_n(L) = \mathbb{Z} b_n^*$ has $\lambda_1^2 = N_n$, so the basis is HKZ from $n$.

*Case $k < n$.* Line L4 terminates by Lemma 2 and pushes $(k, \mathrm{check})$ and then $(k + 1, \mathrm{start})$, which is popped next. By induction the call at $k + 1$ terminates, keeps $b_1, \ldots, b_k$, and leaves the basis HKZ from $k + 1$; then $(k, \mathrm{check})$ is on top and is popped. From now on, every time $(k, \mathrm{check})$ is popped, the basis is HKZ from $k + 1$, which we use as an invariant.

Line L5 is operation 1 on $b_{k+1}$; it keeps all $b_i^*$ and the projection $\pi_{k+1}(b_{k+1})$, so the basis stays HKZ from $k + 1$, and afterwards $|\mu_{k+1,k}| \le 1/2$.

If $N_k > 4 N_{k+1}$ on line L6, the swap is operation 2 and makes the new $N_k$ equal to $N_{k+1} + \mu_{k+1,k}^2 N_k \le N_{k+1} + \tfrac14 N_k < \tfrac12 N_k$. The tasks $(k, \mathrm{check})$ and $(k + 1, \mathrm{start})$ are pushed; the call at $k + 1$ restores the invariant and does not change $b_k$, so $N_k$ keeps its new value. Thus each swap at this level halves $N_k$ at least, while $N_k \ge \lambda_1(\pi_k(L))^2 > 0$ always holds, because $b_k^*$ is a nonzero vector of $\pi_k(L)$, a lattice that does not change during the call by Lemma 1. So line L6 swaps at most $\log_2\!\big(N_k / \lambda_1(\pi_k(L))^2\big) + 1$ times, with $N_k$ its value at the first check.

When line L6 does not swap, line L7 computes $\lambda_1(\pi_k(L))^2$ by Lemma 3. If it is smaller than $N_k$, line L8 makes $N_k = \lambda_1(\pi_k(L))^2$ (Lemma 4) and pushes $(k + 1, \mathrm{start})$. The call at $k + 1$ does not change $b_1, \ldots, b_k$, so (1) still holds at $k$, and it makes the basis HKZ from $k + 1$; then the stack is $\sigma$ again and the call at $k$ ends, HKZ from $k$. If instead the enumerated length equals $N_k$, then (1) already holds at $k$, the invariant gives it from $k + 1$ on, nothing is pushed, and the call ends.

Every step of the call is one of the operations of Lemma 1 at positions $\ge k$, so $b_1, \ldots, b_{k-1}$ and $L$ do not change. $\square$

**Theorem.** The algorithm terminates and returns an HKZ-reduced basis of $L$. Its first row is a shortest nonzero vector of $L$.

*Proof.* The whole loop of lines L2 to L8 is the call at 1, with $\sigma$ empty, so by Lemma 5 it terminates and leaves a basis of $L$ that satisfies (1) for every $k$. Line L9 is a sequence of operations 1 of Lemma 1; it makes $|\mu_{ij}| \le 1/2$ for all $j < i$ and changes no Gram-Schmidt vector, so (1) still holds and the basis is HKZ-reduced. Since $b_1 = b_1^*$, (1) at $k = 1$ says $\|b_1\| = \lambda_1(L)$. $\blacksquare$
