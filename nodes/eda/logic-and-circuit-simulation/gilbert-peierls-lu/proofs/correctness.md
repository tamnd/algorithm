---
title: Gilbert-Peierls LU computes P A = L U, finds each column pattern by search, and runs in time proportional to arithmetic
proves: [correctness]
status: full
---

We use the notation of the page. $A$ is $n \times n$. After step $k - 1$ the columns $1, \ldots, k - 1$ of $L$ and $U$ exist, and $\pi(j)$ is the row of $A$ chosen as pivot $j$. A row $i$ is *pivotal* after step $k - 1$ when $i = \pi(j)$ for some $j < k$. The graph $G_k$ has the rows of $A$ as nodes and an edge $\pi(j) \to r$ for each $j < k$ and each $r$ with $L(r, j) \ne 0$. We count an entry as nonzero when it is stored, so all statements are about structural patterns: an entry is structurally nonzero when it is stored by the algorithm, even if its value cancels to zero.

**Lemma 1 (the column solve).** Let $b = A(:, k)$. Lines L3 to L6 compute the vector $x$ with $x_{\pi(j)} = U(j, k)$ for $j < k$ and, for a row $r$ that is not pivotal, $x_r = b_r - \sum_{j < k} L(r, j)\, U(j, k)$, provided that the rows are visited in an order where $\pi(j)$ comes before every $r$ with $L(r, j) \ne 0$.

*Proof.* This is forward substitution with the unit lower triangular matrix whose columns are $L(:, 1), \ldots, L(:, k - 1)$, written column by column: when row $\pi(j)$ is visited, $x_{\pi(j)}$ already has all its updates, because each update to it comes from some $\pi(j')$ with $L(\pi(j), j') \ne 0$, and the visiting order puts $\pi(j')$ first. Line L6 then subtracts $L(r, j)\, x_{\pi(j)}$ from every $x_r$. By induction over the visiting order, $x_{\pi(j)} = b_{\pi(j)} - \sum_{j' < j} L(\pi(j), j') x_{\pi(j')}$, which is the definition of $U(j, k)$ in the factorization $PA = LU$ restricted to the first $k$ columns, and the non-pivotal rows hold the stated sums. $\square$

**Lemma 2 (the pattern is a reach set).** Let $B$ be the set of nonzero rows of $A(:, k)$. In exact structural terms, $x_r \ne 0$ if and only if $r$ is reachable in $G_k$ from some node of $B$.

*Proof.* If $r \in B$, then $x_r$ starts nonzero. If $r \notin B$, then $x_r$ starts at zero and changes only at line L6, from some pivotal $i = \pi(j)$ with $L(r, j) \ne 0$ and $x_i \ne 0$, that is, along an edge $i \to r$ of $G_k$ from a node with $x_i \ne 0$. By induction on the visiting order, every nonzero $x_r$ is reachable from $B$. Conversely, if $r$ is reachable from $B$ by the path $s = i_0 \to i_1 \to \cdots \to i_t = r$, then each $x_{i_m}$ receives a structural update from $x_{i_{m-1}}$, so by induction on $m$ each is structurally nonzero. $\square$

**Lemma 3 (the order is topological).** The graph $G_k$ has no cycle, and the reverse postorder of a depth-first search of $G_k$ from $B$ visits $\pi(j)$ before every $r$ with $L(r, j) \ne 0$.

*Proof.* An edge $\pi(j) \to r$ has $L(r, j) \ne 0$, so $r$ is not pivotal at step $j$: either $r$ never becomes pivotal before step $k$, or $r = \pi(j')$ with $j' > j$. So along each edge the pivot step strictly grows, and a node that is not pivotal has no outgoing edge. There is no cycle. In a depth-first search of a graph with no cycle, each edge $i \to r$ has $r$ finished before $i$; so $i$ comes before $r$ in the reverse postorder. This is the standard proof of [topological sort](/topological-sort/) by [depth-first search](/depth-first-search/). $\square$

**Theorem 1 (correctness).** If every step finds a nonzero pivot, the algorithm returns a row order $\pi$, a unit lower triangular $L$ and an upper triangular $U$ with $PA = LU$, where row $k$ of $PA$ is row $\pi(k)$ of $A$, and every multiplier has $|L(r, k)| \le 1$. If $A$ is nonsingular, in exact arithmetic every step finds a nonzero pivot.

*Proof.* By Lemmas 2 and 3 the rows of line L2 contain every row where $x$ is nonzero, in an order valid for Lemma 1. So line L8 sets $U(j, k) = x_{\pi(j)}$ for $j < k$ and $U(k, k) = x_p$ with $p = \pi(k)$, and $L(r, k) = x_r / x_p$ for the other non-pivotal rows. For a non-pivotal row $r$, Lemma 1 gives $A(r, k) = \sum_{j < k} L(r, j) U(j, k) + x_r = \sum_{j \le k} L(r, j) U(j, k)$, with $L(p, k) = 1$. For a pivotal row $\pi(j)$ the same identity holds by the definition of $U(j, k)$. Together these are column $k$ of $PA = LU$. Line L7 takes the largest $|x_r|$, so $|L(r, k)| \le 1$.

If all non-pivotal $x_r$ are zero at step $k$, then $A(:, k)$ is a combination of the first $k - 1$ columns of $L$ with coefficients $U(1{:}k{-}1, k)$. The first $k - 1$ columns of $A$ span the same space as these columns of $L$, because the leading $k - 1$ columns of $U$ form a nonsingular triangle. So the first $k$ columns of $A$ are dependent and $A$ is singular. $\square$

**Theorem 2 (time proportional to arithmetic).** Let $f_k$ be the number of multiply and subtract operations of line L6 in step $k$, and $f = \sum_k f_k$. The depth-first search of step $k$ visits at most $|B| + f_k$ nodes and traverses exactly $f_k$ edges. The whole factorization runs in $O(n + \mathrm{nnz}(A) + f)$ time.

*Proof.* The search traverses each out-edge of each visited pivotal node once. The out-edges of $\pi(j)$ are the nonzeros of $L(:, j)$, and line L6 does one operation for each of them for each visited pivotal node, so the edge count equals $f_k$. Each visited node is either a start node in $B$ or is reached by a traversed edge, so the node count is at most $|B| + f_k$. Lines L3, L7 and L8 cost $O(1)$ per visited node, and the divisions are at most the visited nodes. With a mark array that is reset only for the visited nodes, nothing costs time proportional to $n$ inside a step. Summing over $k$, $\sum_k |B| = \mathrm{nnz}(A)$, which gives $O(n + \mathrm{nnz}(A) + f)$. $\square$

The count $f$ is the same arithmetic that a column-oriented dense code would do with the same pivots if it skipped all zero operands. So the theorem says that the sparse overhead (the search and the bookkeeping) is never more than a constant times the useful arithmetic plus the size of the input.

**Theorem 3 (the pattern equals symbolic elimination).** The stored patterns of $L$ and $U$ are the patterns that symbolic Gaussian elimination without pivoting produces on $PA$, where symbolic elimination makes position $(i, j)$ nonzero when it is nonzero in $PA$ or when $(i, t)$ and $(t, j)$ are nonzero for some $t < \min(i, j)$.

*Proof.* Renumber the rows by $P$. Then Lemma 2 says that $(i, k)$ is in the pattern of column $k$ of $L + U$ if and only if $(i, k)$ is nonzero in $PA$ or there is a $t < k$ with $(i, t)$ in the pattern of $L$, $t < i$, and $(t, k)$ in the pattern of column $k$ of $U$. This is the same recurrence as symbolic elimination, column by column, with the same base case. Both define the smallest set closed under the rule, so they agree. $\square$

What is proved here is exact for exact arithmetic and for the structural patterns. In floating point the pivot choice of line L7 can differ from the exact one when two candidates have nearly equal size, and the stability of partial pivoting is the usual worst case bound $2^{n-1}$ on the [growth factor](/growth-factor/), which is rarely approached in practice; that last point is an empirical observation, not a theorem.
