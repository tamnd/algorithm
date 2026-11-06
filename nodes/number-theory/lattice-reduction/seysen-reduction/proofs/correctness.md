---
title: Seysen's algorithm returns a Seysen-reduced basis of the same lattice after at most S_0 det(G) updates
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The input is a list of linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$, the matrix $B$ with these rows, $G = B B^{\mathsf T}$, $H = G^{-1}$ and $D = H B$ with rows $d_1, \ldots, d_n$. We write $E_{ji}$ for the matrix with a single 1 in row $j$ and column $i$, and $\lceil x \rfloor = \lfloor x + 1/2 \rfloor$. The line numbers refer to the `main` block of the page.

**Lemma 1 (the dual basis).** $D B^{\mathsf T} = I$, that is $\langle d_k, b_l \rangle = 1$ if $k = l$ and $0$ otherwise, and $D D^{\mathsf T} = H$. The rows of $D$ are the only vectors in the row space of $B$ with the first property.

*Proof.* $D B^{\mathsf T} = H B B^{\mathsf T} = H G = I$ and $D D^{\mathsf T} = H G H = H$. If $d$ lies in the row space, $d = y B$, and $\langle d, b_l \rangle = (y G)_l$; so prescribing these values fixes $y$, as $G$ is invertible. $\square$

**Lemma 2 (one update).** Let $i \ne j$, $\lambda \in \mathbb{Z}$, and $T = I + \lambda E_{ji}$, so that $B' = T B$ replaces $b_j$ by $b_j + \lambda b_i$. Then $B'$ is a basis of the same lattice, its Gram matrix is $G' = T G T^{\mathsf T}$, its dual basis is $D' = T^{-\mathsf T} D$, which replaces $d_i$ by $d_i - \lambda d_j$, and the dual Gram matrix is $H' = T^{-\mathsf T} H T^{-1}$. Line L9 computes $G'$ and $H'$.

*Proof.* $T$ is an integer matrix with $\det T = 1$ and integer inverse $T^{-1} = I - \lambda E_{ji}$ (as $E_{ji}^2 = 0$), so $B$ and $B'$ generate the same lattice. $G' = T B B^{\mathsf T} T^{\mathsf T}$. The rows of $T^{-\mathsf T} D$ lie in the row space and satisfy $T^{-\mathsf T} D B^{\mathsf T} T^{\mathsf T} = T^{-\mathsf T} T^{\mathsf T} = I$, so by Lemma 1 they are the dual basis of $B'$; $T^{-\mathsf T} = I - \lambda E_{ij}$ subtracts $\lambda$ times row $j$ from row $i$. Multiplying $G$ on the left by $T$ adds $\lambda$ times row $i$ to row $j$, and on the right by $T^{\mathsf T}$ adds $\lambda$ times column $i$ to column $j$; likewise for $H$ with $-\lambda$ and the roles of $i$ and $j$ exchanged. These are the four operations of line L9. $\square$

**Lemma 3 (the change of S).** With $S = \sum_k G_{kk} H_{kk}$, the update of Lemma 2 changes $S$ by

$$\Delta S = 2 G_{ii} H_{jj} \big( \lambda^2 - 2 \lambda \lambda^* \big), \qquad \lambda^* = \frac12 \left( \frac{H_{ij}}{H_{jj}} - \frac{G_{ij}}{G_{ii}} \right).$$

*Proof.* Only $b_j$ and $d_i$ change, so only the terms $k = i$ and $k = j$ change, and in them $\|b_i\|^2 = G_{ii}$ and $\|d_j\|^2 = H_{jj}$ stay fixed. Now $\|b_j + \lambda b_i\|^2 = G_{jj} + 2 \lambda G_{ij} + \lambda^2 G_{ii}$ and $\|d_i - \lambda d_j\|^2 = H_{ii} - 2 \lambda H_{ij} + \lambda^2 H_{jj}$. Hence

$$\Delta S = H_{jj} (2 \lambda G_{ij} + \lambda^2 G_{ii}) + G_{ii} (\lambda^2 H_{jj} - 2 \lambda H_{ij}) = 2 G_{ii} H_{jj} \lambda^2 - 2 \lambda (G_{ii} H_{ij} - H_{jj} G_{ij}),$$

and $G_{ii} H_{ij} - H_{jj} G_{ij} = 2 G_{ii} H_{jj} \lambda^*$. $\square$

**Lemma 4 (the best integer).** Let $f(\lambda) = \lambda^2 - 2 \lambda \lambda^* = (\lambda - \lambda^*)^2 - (\lambda^*)^2$. If $|\lambda^*| \le 1/2$ then $f(\lambda) \ge 0$ for all integers $\lambda$. If $|\lambda^*| > 1/2$ then $f(\lceil \lambda^* \rfloor) < 0$, and $\lceil \lambda^* \rfloor$ minimizes $f$ over the integers.

*Proof.* $f(\lambda) < 0$ means $|\lambda - \lambda^*| < |\lambda^*|$. If $|\lambda^*| \le 1/2$, every integer $\lambda \ne 0$ has $|\lambda - \lambda^*| \ge |\lambda| - |\lambda^*| \ge 1 - 1/2 \ge |\lambda^*|$, and $f(0) = 0$. If $|\lambda^*| > 1/2$, then $|\lceil \lambda^* \rfloor - \lambda^*| \le 1/2 < |\lambda^*|$. The nearest integer to $\lambda^*$ minimizes $(\lambda - \lambda^*)^2$. $\square$

**Theorem 1 (correctness).** If the algorithm returns, the output is a basis of the input lattice and it is Seysen-reduced: for all $i \ne j$ and all integers $\lambda$, replacing $b_j$ by $b_j + \lambda b_i$ does not lower $S$. Equivalently $|\lambda_{ij}^*| \le 1/2$ for all ordered pairs.

*Proof.* By Lemma 2, by induction over the updates, the rows stay a basis of $L$ and $G$, $H$ are the Gram matrices of the current basis and its dual. Line L7 tests $f(\lceil \lambda^* \rfloor) < 0$, which by Lemma 3 is $\Delta S < 0$, as $G_{ii} H_{jj} > 0$. The algorithm returns after a pass in which no test succeeds, and during that pass the matrices did not change, so at the end every pair has $f(\lceil \lambda_{ij}^* \rfloor) \ge 0$. By Lemma 4 this gives $|\lambda_{ij}^*| \le 1/2$, and then $f(\lambda) \ge 0$ for all integers $\lambda$, that is $\Delta S \ge 0$ for every update. $\square$

**Theorem 2 (termination and the number of updates).** Let the input rows be integer vectors, $S_0$ the initial measure and $S_{\text{end}}$ the final one. Then the number of updates satisfies $K \le (S_0 - S_{\text{end}}) \det(G) \le S_0 \det(G) \le n X^n$, where $X$ bounds the squared lengths of the input rows. For a rational input, scaling all rows by a common denominator changes neither the tests nor $S$, so the same bound holds for the scaled basis.

*Proof.* $\det G' = \det(T)^2 \det G = \det G$, so $\Delta := \det G$ is a fixed positive integer. Since $H = \operatorname{adj}(G) / \Delta$, we have $S \Delta = \sum_k G_{kk} \operatorname{adj}(G)_{kk}$, an integer, at every moment, as $G$ stays an integer matrix by Lemma 2. Each update lowers $S$ strictly (Lemma 3 and line L7), so it lowers $S \Delta$ by at least 1; hence $K \le (S_0 - S_{\text{end}}) \Delta$. Finally $\operatorname{adj}(G)_{kk}$ is the Gram determinant of the rows other than $b_k$, at most $\prod_{l \ne k} G_{ll} \le X^{n-1}$ by Hadamard's inequality, and $G_{kk} \le X$, so $S_0 \Delta \le n X^n$. Scaling the rows by $q$ multiplies $G$ by $q^2$ and $H$ by $q^{-2}$, which leaves $\lambda^*$ and $S$ unchanged. $\square$

**Theorem 3 (cost).** The algorithm takes $O(n^3 + n^2 m + (n^2 + m) K)$ arithmetic operations. For an integer input, every number it stores is an integer or a rational with denominator dividing $\det G$, of $O(n \log X)$ digits, assuming $X \ge 2$.

*Proof.* Line L1 computes $G$ with $O(n^2 m)$ operations and $H$ by Gauss-Jordan elimination with $O(n^3)$. A pass runs line L5 to L7 for $n(n-1)$ pairs at $O(1)$ each. An update costs $O(m)$ at line L8 and $O(n)$ at line L9. Every pass but the last makes at least one update, so there are at most $K + 1$ passes, and the total is $O(n^2 m + n^3 + n^2 (K + 1) + (n + m) K)$.

For the sizes: at every moment $S \Delta \le S_0 \Delta \le n X^n$. Both $G_{kk}$ and $\operatorname{adj}(G)_{kk} = \Delta H_{kk}$ are positive integers (Gram determinants of integer vectors), and their product is at most $S \Delta$, so each is at most $n X^n$. By Cauchy-Schwarz for the positive definite matrices $G$ and $\operatorname{adj}(G)$, $|G_{kl}| \le \sqrt{G_{kk} G_{ll}}$ and the same for $\operatorname{adj}(G)$. The basis entries satisfy $|b_{jt}| \le \|b_j\| \le (n X^n)^{1/2}$. So all these integers have $O(\log n + n \log X) = O(n \log X)$ digits, and the entries of $H$ are such integers over $\Delta \le X^n$. The values $\lambda^*$ and $\lambda$ are computed from them, and $|\lambda| \le |\lambda^*| + 1/2$ is bounded by the same sizes. The intermediate values of the Gauss-Jordan elimination are ratios of minors of $G$, of the same size by Hadamard's inequality. $\square$
