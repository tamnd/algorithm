---
title: KLU's block triangular form is valid, and factoring only the diagonal blocks solves the system
proves: [correctness]
status: full
---

We use the notation of the page. $A$ is $n \times n$. The *bipartite graph* of $A$ has a row node for each row, a column node for each column, and an edge $(i, j)$ for each structural nonzero $a_{ij}$. A *transversal* is a set of nonzeros, no two in the same row or column; it is a matching of the bipartite graph.

**Lemma 1 (a nonsingular matrix has a full transversal).** If $\det A \ne 0$, then $A$ has a transversal of size $n$.

*Proof.* By the Leibniz formula, $\det A = \sum_\sigma \operatorname{sgn}(\sigma) \prod_i a_{i \sigma(i)}$. If no permutation $\sigma$ has all $a_{i\sigma(i)} \ne 0$, every term is zero and $\det A = 0$. So some $\sigma$ has all its entries nonzero, and $\{(i, \sigma(i))\}$ is a transversal of size $n$. $\square$

**Lemma 2 (the transversal step).** Line L1 returns a transversal of size $n$ when one exists, and reports structural singularity otherwise.

*Proof.* The step processes the columns in turn and searches, by depth-first search, for an alternating path from the new column to an unmatched row: an edge to a row, the matching edge from that row to its column, an edge to another row, and so on. Flipping such a path increases the matching by one. By Berge's theorem, a matching is maximum if and only if it has no augmenting path, see [bipartite matching](/bipartite-matching/). When the search from a column fails, the rows it reached and the columns it reached form a set of $c$ columns whose nonzeros lie in at most $c - 1$ rows, so by Hall's theorem no matching covers all columns. $\square$

Let $Q$ be the column permutation that puts the matched column of row $i$ in place $i$. Then $B = AQ$ has a zero-free diagonal. The *graph of $B$* has a node per index and an edge $i \to t$ for each off-diagonal nonzero $b_{it}$.

**Lemma 3 (the strongly connected components give block upper triangular form).** Order the strongly connected components of the graph of $B$ in reverse of the order in which Tarjan's algorithm emits them, and number the indices block by block. With $R$ the resulting symmetric permutation, $R B R^{\mathsf T}$ is block upper triangular, and each diagonal block has a zero-free diagonal.

*Proof.* Tarjan's algorithm emits a component only after it has emitted every component reachable from it, see [Tarjan's algorithm](/tarjan-scc/). So an edge $i \to t$ with $i$ and $t$ in different components has the component of $t$ emitted before that of $i$, and after the reversal the component of $i$ comes first. A nonzero $b_{it}$ therefore lies in a block row that is at or before its block column: the matrix is block upper triangular. A symmetric permutation moves diagonal entries to diagonal places, so the diagonal stays zero-free. $\square$

The orders inside each block (the fill-reducing order of line L3) are symmetric permutations inside the block, so they keep both properties. Write $T = PAQ'$ for the final matrix, with diagonal blocks $T_{11}, \ldots, T_{mm}$ and blocks $T_{KJ}$ with $K < J$ above them.

**Theorem 1 (only the diagonal blocks need factors).** $\det A = \pm \prod_K \det T_{KK}$. So $A$ is nonsingular if and only if each $T_{KK}$ is nonsingular. In that case, with $y = Q'^{-1} x$ split into the blocks $y_K$ and $c = Pb$ split the same way, the system $Ax = b$ is equivalent to

$$T_{KK}\, y_K = c_K - \sum_{J > K} T_{KJ}\, y_J, \qquad K = m, m - 1, \ldots, 1,$$

which lines L6 to L8 solve in this order.

*Proof.* The determinant of a block upper triangular matrix is the product of the determinants of its diagonal blocks (apply $\det \begin{pmatrix} X & Y \\ 0 & Z \end{pmatrix} = \det X \det Z$ with $X = T_{11}$ and use induction on the number of blocks). The permutations change only the sign. For the system: block row $K$ of $Ty = c$ reads $\sum_{J \ge K} T_{KJ} y_J = c_K$, because the blocks below the diagonal are zero. When block $K$ is processed, all $y_J$ with $J > K$ are already known, so the equation for $y_K$ is the one displayed, with a nonsingular matrix. By induction from $K = m$ down to $K = 1$ all blocks are found. $\square$

**Corollary (fill is confined to the diagonal blocks).** The LU factors that KLU computes are those of the diagonal blocks. The blocks $T_{KJ}$ with $K < J$ are used as they are in the products of line L7, and the zero blocks below the diagonal are never touched. So no fill-in can appear outside the diagonal blocks, and a $1 \times 1$ block needs only a division.

**Theorem 2 (each block is factored correctly).** Each $T_{KK}$ is factored by the Gilbert-Peierls method with threshold pivoting, which returns $P_K T_{KK} = L_K U_K$, and the block solve of line L8 is exact in exact arithmetic.

*Proof.* This is the correctness theorem of [Gilbert-Peierls LU](/gilbert-peierls-lu/) applied to the block. The threshold test only changes which non-pivotal row is chosen among those with $|x_r| \ge u \max |x|$; the proof of that theorem holds for any choice of a nonzero pivot, and the multipliers are bounded by $1/u$ instead of 1. $\square$

**Theorem 3 (refactorization).** If a new matrix $A'$ has the same pattern as $A$ and the reused pivots are nonzero, the refactorization returns factors with $P_K T'_{KK} = L'_K U'_K$.

*Proof.* The block form depends only on the pattern, so it is the same for $A'$. With the pivot rows fixed, the Gilbert-Peierls column solve computes the same quantities as before, with the new values, and a nonzero pivot gives a valid column of $L'_K$ and $U'_K$. Nothing in the proof of Theorem 2 depends on how the pivot row was chosen. $\square$

Not proved here: that the irreducible blocks found are the finest possible block triangular form, and that this form is unique up to the order of independent blocks and the permutations inside blocks. Duff, Erisman and Reid prove these facts in their chapter on reduction to block triangular form; they rest on the [Dulmage-Mendelsohn decomposition](/dulmage-mendelsohn-decomposition/). Also not proved: that the minimum degree order gives little fill. That is an empirical property of the heuristic, measured on circuit matrices by Davis and Palamadai Natarajan.
