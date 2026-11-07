---
title: FAST-MULTIPOINT-EVAL returns f(u_0), ..., f(u_{n-1}) in O(M(n) log n) operations
proves: [correctness]
status: full
---

Let $R$ be a commutative ring with $1$, $f \in R[x]$, $n \ge 1$, and $u_0, \ldots, u_{n-1} \in R$. For a node $(j, k)$ of the subproduct tree, let $S_{j,k}$ be the set of indices $i$ of the leaves below it, so that $m_{j,k} = \prod_{i \in S_{j,k}} (x - u_i)$.

**Lemma 1 (the tree).** For each level $j$, the sets $S_{j,0}, S_{j,1}, \ldots$ are consecutive blocks that partition $\{0, \ldots, n-1\}$ in order. For each node, $m_{j,k} = \prod_{i \in S_{j,k}} (x - u_i)$ is monic of degree $|S_{j,k}|$. If $j \ge 1$, then $S_{j,k} = S_{j-1,2k} \cup S_{j-1,2k+1}$, where the second set is empty if node $2k + 1$ does not exist at level $j - 1$. The top level $h = \lceil \log_2 n \rceil$ has one node, with $S_{h,0} = \{0, \ldots, n - 1\}$.

*Proof.* At level $0$ the blocks are the single indices, and $m_{0,i} = x - u_i$. If the claim holds at level $j - 1$ with $c$ nodes, then level $j$ has $\lceil c/2 \rceil$ nodes, node $k$ is the product of nodes $2k$ and $2k + 1$, or a copy of node $2k$ if $2k + 1 = c$, and the union of two consecutive blocks is a block. A product of monic polynomials is monic and its degree is the sum of the degrees. The number of nodes $\lceil n / 2^j \rceil$ is $1$ exactly when $j \ge \lceil \log_2 n \rceil$. $\square$

**Lemma 2 (remainders keep values).** Let $m$ be monic, let $g \in R[x]$, and let $u \in R$ with $m(u) = 0$. Then $(g \bmod m)(u) = g(u)$.

*Proof.* Division by a monic polynomial is defined over any commutative ring: $g = qm + (g \bmod m)$. Evaluation at $u$ is a ring homomorphism, so $g(u) = q(u) m(u) + (g \bmod m)(u) = (g \bmod m)(u)$. $\square$

**Theorem (correctness).** FAST-MULTIPOINT-EVAL returns the list $f(u_0), \ldots, f(u_{n-1})$.

*Proof.* If $n = 0$, line L1 returns the empty list. Let $n \ge 1$. We show by downward induction on $j$ the invariant: after the remainders for level $j$ are computed, the list $r$ has one entry $r_{j,k}$ per node of level $j$, with $\deg r_{j,k} < \deg m_{j,k}$ and $r_{j,k}(u_i) = f(u_i)$ for all $i \in S_{j,k}$.

*Level $h$.* Line L3 sets $r_{h,0} = f \bmod m_{h,0}$, which has degree less than $\deg m_{h,0} = n$. Each $u_i$ is a root of $m_{h,0}$, so $r_{h,0}(u_i) = f(u_i)$ by Lemma 2.

*From level $j + 1$ to level $j$.* Line L7 sets $r_{j,k} = r_{j+1,\lfloor k/2 \rfloor} \bmod m_{j,k}$, which has degree less than $\deg m_{j,k}$. By Lemma 1, $S_{j,k} \subseteq S_{j+1, \lfloor k/2 \rfloor}$. For $i \in S_{j,k}$, $u_i$ is a root of $m_{j,k}$, so by Lemma 2 and the invariant at level $j + 1$, $r_{j,k}(u_i) = r_{j+1,\lfloor k/2 \rfloor}(u_i) = f(u_i)$.

*Level $0$.* Node $k$ is $x - u_k$ with $S_{0,k} = \{k\}$, and $r_{0,k}$ has degree less than $1$, so it is a constant $c$ (the zero polynomial gives $c = 0$). By the invariant, $c = r_{0,k}(u_k) = f(u_k)$. Line L9 returns these constants in the order of the leaves, which is the order of the points. $\square$

**Theorem (cost).** Assume that multiplying a polynomial with $a$ coefficients by one with at most $a$ coefficients costs at most $M(a)$ ring operations, that $M(a)/a$ is nondecreasing, and that $M(2a) \le 4M(a)$. If $\deg f < n$, then FAST-MULTIPOINT-EVAL uses at most $11 M(n) \lceil \log_2 n \rceil + O(n \log n)$ ring operations.

*Proof.* From $M(a)/a$ nondecreasing, $M$ is nondecreasing and superadditive: $M(a) + M(b) \le M(a + b)$, because $M(a) \le \frac{a}{a+b} M(a+b)$ and $M(b) \le \frac{b}{a+b} M(a+b)$. Hence $\sum_v M(a_v) \le M(\sum_v a_v)$ for any finite family.

*The tree.* A node $v$ of level $j \ge 1$ with $D_v = \deg m_v$ that is a product costs at most $M(D_v + 1)$, since both factors have at most $D_v + 1$ coefficients. A node that is copied costs nothing. At level $j \ge 1$ there are $\lceil n/2^j \rceil \le n$ nodes, and $\sum_v D_v = n$ by Lemma 1, so $\sum_v (D_v + 1) \le 2n$ and the level costs at most $M(2n) \le 4M(n)$. There are $h = \lceil \log_2 n \rceil$ levels above the leaves.

*The descent.* At line L3, $\deg f < n = \deg m_{h,0}$, so $f \bmod m_{h,0} = f$ costs $O(n)$. Consider a node $v$ of level $j + 1$ with $\deg m_v = D$ and the remainder $r_v$ of degree less than $D$. If $v$ is a copy of one child, that child's remainder is $r_v$ itself, because $\deg r_v < D$ and the child is $m_v$; this costs $O(D)$. Otherwise its children have degrees $d_1 + d_2 = D$ with $d_1, d_2 \ge 1$. Dividing $r_v$ by the child of degree $d_1$ is either trivial, if $\deg r_v < d_1$, or a division with a quotient of $k = \deg r_v - d_1 + 1 \le d_2$ coefficients. By the cost theorem for fast division, it costs at most $4M(k) + M(d_1) + 2\lceil \log_2 k \rceil M(k)/k + O(D)$. Since $2 \lceil \log_2 k \rceil \le 2k$ for $k \ge 1$ and $M$ is nondecreasing, this is at most $6M(d_2) + M(d_1) + O(D)$. In the same way, the other child costs at most $6M(d_1) + M(d_2) + O(D)$. Together, $7(M(d_1) + M(d_2)) + O(D) \le 7M(D) + O(D)$. Summing over the nodes of level $j + 1$, whose degrees sum to $n$, a level of the descent costs at most $7M(n) + O(n)$. Line L9 costs $O(n)$.

Adding $4M(n) + 7M(n) + O(n)$ over $h = \lceil \log_2 n \rceil$ levels gives the bound. $\blacksquare$
