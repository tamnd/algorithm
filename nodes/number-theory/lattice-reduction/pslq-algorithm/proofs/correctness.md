---
title: Exact PSLQ returns an integer relation after at most (n - 1) ln X / ln tau^2 iterations
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The input is $x \in \mathbb{Q}^n$, $n \ge 2$, $x \ne 0$, and $\gamma^2 > 4/3$; let $\tau^2 = 4 \gamma^2 / (4 + \gamma^2)$, so that $1 / \tau^2 = 1 / \gamma^2 + 1/4$ and $1 < \tau^2 < 4$. We write $a_i$ for the rows of $A$, $P_x$ for the orthogonal projection onto $x^\perp$, $p_i = a_i P_x = a_i - (\langle a_i, x \rangle / \langle x, x \rangle) x$, and $\mu_{ij}$, $B_j = \|p_j^*\|^2$ for the Gram-Schmidt data of $p_1, \ldots, p_n$, with $d_k = B_1 \cdots B_k$ the Gram determinant of $p_1, \ldots, p_k$. The line numbers refer to the `main` block of the page.

**Lemma 1 (the integer invariants).** At every moment $A$ is an integer matrix with $\det A = \pm 1$, $B = A^{-1}$, and $y = x B$, so $x = y A = \sum_i y_i a_i$.

*Proof.* Line L1 sets $A = B = I$ and $y = x$. Line L7 exchanges rows $r, r+1$ of $A$ and columns $r, r+1$ of $B$, which keeps $B = A^{-1}$ and permutes the entries of $y = x B$. Line L11 multiplies $A$ on the left by $I - t E_{ij}$, and line L12 multiplies $B$ on the right by its inverse $I + t E_{ij}$, which adds $t$ times column $i$ to column $j$; then $y = x B$ changes by $y_j \leftarrow y_j + t y_i$. Both matrices are integer with determinant $\pm 1$. $\square$

**Lemma 2 (the Gram-Schmidt data).** At every moment, the stored $\mu_{ij}$ ($j \le n - 1$) and $B_j$ are the Gram-Schmidt data of the rows $p_i$, and $B_n = 0$. After HERMITE-REDUCE, $|\mu_{ij}| \le 1/2$ for all $j < i$.

*Proof.* Line L2 computes them from the Gram matrix $\langle p_i, p_j \rangle = \langle a_i, a_j \rangle - \langle a_i, x \rangle \langle a_j, x \rangle / \langle x, x \rangle$, which for $A = I$ is $I - x^{\mathsf T} x / \langle x, x \rangle$. Since $p_1, \ldots, p_n$ lie in $x^\perp$, of dimension $n - 1$, and $p_1, \ldots, p_{n-1}$ are independent while all $y_j \ne 0$ (Lemma 3), these span $x^\perp$ and $p_n^* = 0$.

The projection $P_x$ is linear, so the row operation $a_i \leftarrow a_i - t a_j$ is $p_i \leftarrow p_i - t p_j$, and the swap of $a_r, a_{r+1}$ is the swap of $p_r, p_{r+1}$. Line L11 is the update of a size reduction step, exactly as in Lemma 2 of the [LLL proof](/lll-algorithm/) (the vector $p_i^*$ does not change, and $\mu_{ik} \leftarrow \mu_{ik} - t \mu_{jk}$ for $k < j$, $\mu_{ij} \leftarrow \mu_{ij} - t$). Line L8 is the swap update of Lemma 3 there, which needs only $B_r' = B_{r+1} + \mu_{r+1,r}^2 B_r \ne 0$; this holds by Lemma 3 below, as the new $p_1, \ldots, p_{n-1}$ are independent. For $r = n - 1$, with $p_n^* = 0$, the derivation gives $c_{n-1}^* = \mu p_{n-1}^*$, so $B_{n-1}' = \mu^2 B_{n-1}$, and $c_n^* = p_{n-1}^* - \frac{1}{\mu} c_{n-1}^* = 0$, matching $B_n' = B_{n-1} B_n / B_{n-1}' = 0$.

In HERMITE-REDUCE, for a fixed $i$ the steps with $j = i - 1, \ldots, 1$ change $\mu_{ik}$ only for $k \le j$; so after the step at $j$, $|\mu_{ij}| \le 1/2$, and later steps (smaller $j$) do not change it. Rows other than $i$ are not changed by the steps of row $i$. $\square$

**Lemma 3 (independence while no relation is found).** If all $y_j \ne 0$, then for every $j$ the $n - 1$ vectors $p_i$, $i \ne j$, are linearly independent. In particular $p_1, \ldots, p_{n-1}$ are independent and $B_1, \ldots, B_{n-1} > 0$.

*Proof.* Suppose $\sum_{i \ne j} c_i p_i = 0$ with the $c_i$ not all zero. Then $\sum_{i \ne j} c_i a_i = \lambda x$ for some $\lambda$, and $\lambda \ne 0$ because the $a_i$ are independent. So $x$ lies in the span of the $a_i$, $i \ne j$. But $x = \sum_i y_i a_i$ is the unique expansion in the basis $A$, and $y_j \ne 0$: a contradiction. $\square$

The checks at lines L1 and L5 guarantee that all $y_j \ne 0$ whenever lines L2, L6 to L8 run; the swap at line L7 only permutes $y$, so the condition still holds when line L8 runs.

**Lemma 4 (the Gram determinants).** For $k \le n - 1$, $d_k = \det \operatorname{Gram}(a_1, \ldots, a_k, x) / \langle x, x \rangle$. If $x$ is an integer vector and all $y_j \ne 0$, then $d_k \ge 1 / \langle x, x \rangle$.

*Proof.* Subtracting $(\langle a_i, x \rangle / \langle x, x \rangle) x$ from each $a_i$ is an elementary operation on the list $a_1, \ldots, a_k, x$ that does not change its Gram determinant, and it gives $p_1, \ldots, p_k, x$, whose Gram matrix is block diagonal because $p_i \perp x$. So $\det \operatorname{Gram}(a_1, \ldots, a_k, x) = d_k \langle x, x \rangle$. For integer $A$ and $x$ the left side is an integer, and it is positive since $d_k > 0$ by Lemma 3; hence it is at least 1. $\square$

**Lemma 5 (one iteration).** Let $D = \prod_{k=1}^{n-1} d_k = \prod_{j=1}^{n-1} B_j^{n-j}$. Initially $D \le 1$ and every $B_j \le 1$. Each iteration multiplies $D$ by at most $1 / \tau^2$ and does not increase $\max_{j \le n-1} B_j$.

*Proof.* For $A = I$, the Schur complement gives $\det \operatorname{Gram}(e_1, \ldots, e_k, x) = \langle x, x \rangle - \sum_{i \le k} x_i^2$, so by Lemma 4, $d_k = \sum_{i > k} x_i^2 / \sum_i x_i^2 \le 1$, and $B_j = d_j / d_{j-1} \le 1$ since the $d_k$ decrease. HERMITE-REDUCE does not change any $B_j$.

Consider the swap at $r$, after a HERMITE-REDUCE, so $\mu = \mu_{r+1,r}$ has $|\mu| \le 1/2$ by Lemma 2. If $r \le n - 2$, the choice at line L6 gives $\gamma^{2r} B_r \ge \gamma^{2(r+1)} B_{r+1}$, that is $B_{r+1} \le B_r / \gamma^2$, so
$$B_r' = B_{r+1} + \mu^2 B_r \le B_r \Big( \frac{1}{\gamma^2} + \frac14 \Big) = \frac{B_r}{\tau^2}.$$
If $r = n - 1$, then $B_n = 0$ and $B_{n-1}' = \mu^2 B_{n-1} \le B_{n-1} / 4 < B_{n-1} / \tau^2$. In both cases the first $k$ rows are the same set for every $k \ne r$, so $d_k$ is unchanged for $k \ne r$, and $d_r' = d_{r-1} B_r' \le d_r / \tau^2$; since $r \le n - 1$, the factor $d_r$ occurs in $D$, and $D' \le D / \tau^2$. For the maximum: $B_r' \le B_r$, and for $r \le n - 2$, $B_{r+1}' = B_r B_{r+1} / B_r' \le B_r$ because $B_r' \ge B_{r+1}$; for $r = n - 1$, $B_n' = 0$. The other $B_j$ do not change. $\square$

**Theorem 1 (correctness).** If the algorithm returns a vector $m$, then $m \in \mathbb{Z}^n$, $m \ne 0$ and $\langle m, x \rangle = 0$.

*Proof.* It returns $e_j$ at line L1 when $x_j = 0$, or column $j$ of $B$ at line L5 when $y_j = 0$. In the second case $m$ is a column of the invertible integer matrix $B$, so $m \ne 0$, and $\langle x, m \rangle = (x B)_j = y_j = 0$ by Lemma 1. $\square$

**Theorem 2 (the lower bound).** At every moment when all $y_j \ne 0$, every integer relation $m$ of $x$ satisfies $\|m\|^2 \ge 1 / \max_{j \le n-1} B_j$. This bound never decreases during the run.

*Proof.* Since $\langle m, x \rangle = 0$, $m \in x^\perp$, and $\langle p_i, m \rangle = \langle a_i P_x, m \rangle = \langle a_i, m \rangle$, the $i$th entry of the integer vector $z = A m^{\mathsf T}$; $z \ne 0$ since $A$ is invertible. By Lemma 3 the vectors $p_1^*, \ldots, p_{n-1}^*$ are a nonzero orthogonal basis of $x^\perp$, so some $\langle p_k^*, m \rangle \ne 0$; let $k$ be the least such index. Then $z_k = \langle p_k, m \rangle = \langle p_k^*, m \rangle + \sum_{j < k} \mu_{kj} \langle p_j^*, m \rangle = \langle p_k^*, m \rangle \ne 0$, so $1 \le |z_k| \le \|p_k^*\| \|m\|$, and $\|m\|^2 \ge 1 / B_k \ge 1 / \max_j B_j$. The bound never decreases by Lemma 5. $\square$

**Theorem 3 (termination).** Let $\hat x$ be the primitive integer vector on the line of $x$ and $X = \|\hat x\|^2$. The number $I$ of iterations satisfies $\tau^{2I} \le X^{n-1}$, so $I \le (n - 1) \ln X / \ln \tau^2$, and the algorithm returns a relation.

*Proof.* Replacing $x$ by $\hat x = c x$ with $c \ne 0$ changes neither $P_x$ nor which entries of $y = x B$ are zero, so every step is the same; we may assume $x = \hat x$. If $X = 1$, $x = \pm e_j$ has a zero entry and line L1 returns (as $n \ge 2$). Otherwise consider the state just after the swap of the $t$th iteration. All $y_j$ were nonzero at line L5 of that iteration, and the swap only permuted them, so by Lemma 4 every $d_k \ge 1 / X$ and $D \ge X^{-(n-1)}$. By Lemma 5, $D \le \tau^{-2t}$. Hence $\tau^{2t} \le X^{n-1}$ for every iteration $t$ that is performed. Since $\tau^2 > 1$, only finitely many iterations happen; the loop can only end at line L5, with a relation by Theorem 1. $\square$

**Theorem 4 (cost).** The algorithm takes $O(n^3 (I + 1)) = O(n^4 \log X)$ arithmetic operations, using $O(n^2)$ space.

*Proof.* Line L2 computes the Gram matrix of the $p_i$ in $O(n^2)$ operations for $A = I$ and the Gram-Schmidt data in $O(n^3)$. Line L6 takes $O(n)$ operations, line L7 $O(n)$, and line L8 $O(n)$. HERMITE-REDUCE makes at most $n(n-1)/2$ steps, each with $O(n)$ operations on $\mu$, on a row of $A$ and on a column of $B$, so $O(n^3)$. There are $I$ iterations, each with one HERMITE-REDUCE, plus the call at line L3 and the checks at line L5 of $O(n)$ each, giving $O(n^3 (I + 1))$, and $I = O(n \log X)$ by Theorem 3. The stored data are $A$, $B$, $\mu$, $y$ and the $B_j$, which are $O(n^2)$ numbers. $\square$
