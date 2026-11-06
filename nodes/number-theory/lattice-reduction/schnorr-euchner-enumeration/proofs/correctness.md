---
title: Schnorr-Euchner enumeration returns a shortest nonzero vector after a bounded number of nodes
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The input is a list of linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$. We write $b_i^*$ for their Gram-Schmidt vectors, $B_i = \|b_i^*\|^2 > 0$, $\mu_{ij} = \langle b_i, b_j^* \rangle / B_j$ for $j < i$, and $\pi_k$ for the orthogonal projection onto $\operatorname{span}(b_1, \ldots, b_{k-1})^\perp$. For integers $x_1, \ldots, x_n$, let $c_k(x) = -\sum_{j > k} x_j \mu_{jk}$ and $\ell_k(x) = \sum_{i \ge k} (x_i - c_i(x))^2 B_i$, with $\ell_{n+1} = 0$. Both depend only on $x_k, \ldots, x_n$ (and $c_k$ only on $x_{k+1}, \ldots, x_n$). The line numbers refer to the `main` block of the page.

**Lemma 1 (the identity).** For $v = \sum_i x_i b_i$, $\|\pi_k(v)\|^2 = \ell_k(x)$; in particular $\|v\|^2 = \ell_1(x)$.

*Proof.* Substitute $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$:
$$v = \sum_i x_i b_i^* + \sum_i \sum_{j < i} x_i \mu_{ij} b_j^* = \sum_k \Big( x_k + \sum_{j > k} x_j \mu_{jk} \Big) b_k^* = \sum_k (x_k - c_k(x)) b_k^*.$$
The projection $\pi_k$ keeps the terms with index at least $k$ and removes the others, and the $b_i^*$ are pairwise orthogonal, so $\|\pi_k(v)\|^2 = \sum_{i \ge k} (x_i - c_i)^2 B_i$. $\square$

**Lemma 2 (the order at one level).** Fix $x_{k+1}, \ldots, x_n$, so $c = c_k$ is fixed. The values produced at level $k$, starting from $\lceil c \rfloor$ at line L7 (or $0$ at line L3) and continuing by line L12, are distinct integers in order of nondecreasing $|x_k - c|$, and so of nondecreasing $\ell_k$. In the symmetric case (all of $x_{k+1}, \ldots, x_n$ zero, so $c = 0$) they are $0, 1, 2, \ldots$, which is every integer $z \ge 0$ in order of nondecreasing $|z - c|$.

*Proof.* Let $z_0 = \lceil c \rfloor$, so $|c - z_0| \le 1/2$, and let $s = +1$ if $c \ge z_0$ and $s = -1$ otherwise. Then $c$ lies between $z_0$ and $z_0 + s/2$. The sequence is $z_0, z_0 + s, z_0 - s, z_0 + 2s, z_0 - 2s, \ldots$. Write $d = |c - z_0| \le 1/2$. The distances are $d, 1 - d, 1 + d, 2 - d, 2 + d, \ldots$, that is $j - d$ and $j + d$ for the values $z_0 + js$ and $z_0 - js$; since $0 \le d \le 1/2$, $j + d \le (j + 1) - d$, so the sequence of distances is nondecreasing. It lists every integer once. Finally $\ell_k = \ell_{k+1} + (x_k - c)^2 B_k$ with $B_k > 0$ and $\ell_{k+1}$ fixed. In the symmetric case line L12 adds 1 each time and $c = 0$. $\square$

**Lemma 3 (the invariant of the result).** At every moment, the pair (best, $R^2$) satisfies best $\ne 0$ and $\|\sum_i \text{best}_i b_i\|^2 = R^2$. Moreover $R^2$ never increases.

*Proof.* At line L2, best $= e_1$ and $R^2 = B_1 = \|b_1\|^2$. Line L9 is the only line that changes them; it runs at a leaf with $x \ne 0$ and $\ell_1 < R^2$, and sets best $= x$ and $R^2 = \ell_1(x) = \|\sum_i x_i b_i\|^2$ by Lemma 1, which is smaller than before. $\square$

**Lemma 4 (the shape of the search).** The loop is a depth-first search of the tree whose nodes at level $k$ are the tuples $(x_k, \ldots, x_n)$ it produces. At a node of level $k > 1$ that passes the test at line L6, the search descends to level $k - 1$, tries values there in the order of Lemma 2 (with $x_k, \ldots, x_n$ fixed), processing the subtree of each value that passes, and returns to level $k$ exactly when a value at level $k - 1$ fails. At level 1, a passing value is a leaf, after which the next value is tried.

*Proof.* Line L7 descends and sets the first value; line L5 evaluates the node. If it passes and $k > 1$, line L7 descends again. If it passes at $k = 1$, lines L8 and L9 handle the leaf and line L12 moves to the next value at the same level. If it fails, line L10 goes up one level and line L12 moves to the next value there. The variables $x_j$ for $j$ above the current level are not changed while the search is below them, so they stay fixed during a subtree. $\square$

**Theorem 1 (termination).** The loop terminates.

*Proof.* At a fixed level with fixed higher coordinates, the values $x_k$ tried are distinct (Lemma 2), so $|x_k - c_k| \to \infty$ along them and $\ell_k \ge (x_k - c_k)^2 B_k \to \infty$; since $R^2 \le B_1$ by Lemma 3, a failing value comes after finitely many values. So each node has finitely many children that pass, plus one that fails. The depth is $n$. By König's lemma for this finitely branching tree of finite depth, the tree is finite, and the depth-first search of Lemma 4 visits each node once; it ends when the level $n$ fails and $k$ becomes $n + 1$ at line L11. $\square$

**Theorem 2 (correctness).** The returned best is a nonzero vector of minimal length: $\|\sum_i \text{best}_i b_i\| = \lambda_1(L)$.

*Proof.* By Lemma 3, the output is a nonzero lattice vector of squared length $R_f^2$, the final radius. Suppose a nonzero $u = \sum_i y_i b_i$ had $\|u\|^2 < R_f^2$. Let $t$ be the largest index with $y_t \ne 0$; replacing $u$ by $-u$ we may assume $y_t > 0$. By Lemma 1, $\ell_k(y) = \|\pi_k(u)\|^2 \le \|u\|^2 < R_f^2 \le R^2$ for every $k$ and every moment, by Lemma 3.

We show by induction on $k = n, n - 1, \ldots, 1$ that the search visits the node $(y_k, \ldots, y_n)$ and that this node passes. At level $n$, the values are tried in the order of Lemma 2 (symmetric case, $0, 1, 2, \ldots$, and $y_n \ge 0$ because either $t = n$ and $y_n > 0$ or $y_n = 0$). Level $n$ is left only after a value $z$ fails, that is $\ell_n(z) \ge R^2 > \ell_n(y)$; so $|z - c_n| > |y_n - c_n|$, and by the nondecreasing order $y_n$ was tried before $z$. When it was tried it passed, since $\ell_n(y) < R^2$. The step from $k$ to $k - 1$ is the same: after the node $(y_k, \ldots, y_n)$ passes, by Lemma 4 the search tries values at level $k - 1$ with $x_k, \ldots, x_n = y_k, \ldots, y_n$ until one fails. If $k - 1 < t$, the higher coordinates are not all zero, so the full zig-zag order of Lemma 2 is used and contains $y_{k-1}$; if $k - 1 \ge t$, the symmetric order $0, 1, 2, \ldots$ is used, and $y_{k-1} \ge 0$ (it is $0$ above $t$ and positive at $t$). In both cases the failing value has $\ell_{k-1} \ge R^2 > \ell_{k-1}(y)$, so it comes after $y_{k-1}$, which was tried and passed.

So the leaf $y$ is reached and passes, with $y \ne 0$, and line L9 sets $R^2 = \|u\|^2 < R_f^2$. Since $R^2$ never increases, the final radius is at most $\|u\|^2$, a contradiction. $\square$

**Theorem 3 (CVP).** With the centers $c_k = \tau_k - \sum_{j > k} x_j \mu_{jk}$, where $\tau_k = \langle t, b_k^* \rangle / B_k$, without the symmetry rule and the test $x \ne 0$, and started from Babai's vector $x^B$ with $R^2 = \ell_1(x^B)$, the search returns $x$ minimizing $\|t - \sum_i x_i b_i\|$.

*Proof.* Write $t = t_\perp + \sum_k \tau_k b_k^*$ with $t_\perp$ orthogonal to $\operatorname{span}(L)$. As in Lemma 1, $t - \sum_i x_i b_i = t_\perp + \sum_k (c_k - x_k) b_k^*$, so $\|t - v\|^2 = \|t_\perp\|^2 + \ell_1(x)$ and the partial sums $\ell_k$ are nondecreasing as $k$ decreases. Lemmas 2 to 4 and Theorem 1 hold unchanged, using the full zig-zag order at every level. If some $y$ had $\ell_1(y) < R_f^2$, the induction of Theorem 2 (without the sign normalization) shows that its leaf is reached and passes, and line L9 would lower $R^2$ below $R_f^2$; so the result, which is $x^B$ or a later leaf, minimizes $\ell_1$, hence the distance. $\square$

**Theorem 4 (the number of nodes).** The number $N$ of executions of line L5 satisfies
$$N \le 1 + 2 P, \qquad P \le \sum_{k=1}^n \prod_{i=k}^n \Big( 2 \sqrt{B_1 / B_i} + 1 \Big),$$
where $P$ is the number of passing nodes. If the basis is $\delta$-LLL-reduced with $1/4 < \delta \le 1$ and $\alpha = 1 / (\delta - 1/4)$, then $N \le 1 + 2 n \, 3^n \alpha^{n(n-1)/4}$, and the total cost is $O(n^2 m + n N)$ arithmetic operations.

*Proof.* Every node either passes or fails. By Lemma 4, a failing node at level $k < n$ ends the trial of values below a passing node of level $k + 1$, and each passing node of level $k + 1 \ge 2$ has exactly one failing child; at level $n$ exactly one node fails, the last one. So the number of failing nodes is at most $P + 1$, and $N \le 2P + 1$.

A passing node $(x_k, \ldots, x_n)$ has $\ell_k(x) < R^2 \le B_1$, by Lemma 3. Given $x_{k+1}, \ldots, x_n$, the number of integers $x_k$ with $(x_k - c_k)^2 B_k < B_1$ is at most $2 \sqrt{B_1 / B_k} + 1$, as they lie in an open interval of length $2 \sqrt{B_1 / B_k}$. Multiplying over the levels $i = n, \ldots, k$ bounds the passing nodes at level $k$ by $\prod_{i \ge k} (2 \sqrt{B_1 / B_i} + 1)$, and summing over $k$ bounds $P$.

For a $\delta$-LLL-reduced basis, $B_1 \le \alpha^{i-1} B_i$ (consequence (a) on [LLL-reduced basis](/lll-reduction/)), so each factor is at most $2 \alpha^{(i-1)/2} + 1 \le 3 \alpha^{(i-1)/2}$, as $\alpha \ge 1$. The product over $i = k, \ldots, n$ is at most $3^n \alpha^{\sum_{i=1}^n (i-1)/2} = 3^n \alpha^{n(n-1)/4}$, and there are $n$ values of $k$.

For the cost: line L1 takes $O(n^2 m)$ operations; at each node line L5 takes $O(1)$ operations, the center at line L7 takes $O(n)$, and lines L9 and L12 take $O(n)$ (copying best, testing $x \ne 0$ and the symmetric case, which an implementation can also maintain in $O(1)$ by tracking the highest nonzero index). So the search takes $O(n N)$. $\square$
