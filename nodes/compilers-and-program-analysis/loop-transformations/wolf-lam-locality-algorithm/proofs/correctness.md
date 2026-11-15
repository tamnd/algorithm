---
title: The reuse spaces are exact, the chosen transformation keeps every dependence, and the search finds the cheapest legal set of loops
proves: [correctness]
status: full
---

## Setting

The nest has depth $k$ and a box of iterations $P \subset \mathbb{Z}^k$. $D$ is a finite set of nonzero distance vectors, each lexicographically positive. Every dependence of the nest goes from an iteration $i$ to the iteration $i + d$ with $d \in D$, or stays inside one iteration; the body of one iteration runs as a unit, with its statements in text order. An access $A[H i + c]$ touches, at iteration $i$, the element of array $A$ with subscripts $H i + c$, where $H$ is an integer matrix with $k$ columns and $c$ is an integer vector. Arrays are stored in row-major order, so the elements whose subscripts differ only in the last place lie next to each other in memory. $H_S$ is $H$ with its last row set to $0$.

For a set $I$ of loops, line L4 looks for a signed permutation matrix $Q$, whose rows are $\pm e_j$, that lists the loops outside $I$ first and the loops of $I$ last, and for a lower unitriangular integer matrix $S$ of size $m = |I|$. It then sets

$$T = \begin{pmatrix} 1 & 0 \\ 0 & S \end{pmatrix} Q .$$

For $y = T x$ we write $y = (o, b)$, with $o$ the first $k - m$ entries (the *outer part*) and $b$ the last $m$ entries (the *band part*). Line L9 runs the iterations in the order of the key

$$\kappa(i) = \bigl(o,\ \lfloor b_1 / B \rfloor, \dots, \lfloor b_m / B \rfloor,\ b\bigr) \quad\text{where } (o, b) = T i,$$

compared lexicographically, with the floor entries left out when $m \le 1$. This is the order of a nest that runs the outer loops, then the tile loops, then the loops inside one tile.

## Part 1: the reuse spaces

**Lemma 1 (self-temporal reuse).** One access touches the same element at iterations $i$ and $i + r$ if and only if $r \in \ker H$.

*Proof.* $H(i + r) + c = H i + c$ if and only if $H r = 0$. $\square$

**Lemma 2 (self-spatial reuse).** One access touches the same row of the array, that is, elements whose subscripts agree in all places but the last, at iterations $i$ and $i + r$ if and only if $r \in \ker H_S$.

*Proof.* The subscripts at $i + r$ and at $i$ differ by $H r$. They agree in all places but the last exactly when every row of $H$ except the last gives $0$ on $r$, which is $H_S r = 0$. $\square$

Only elements of one row lie next to each other in row-major order, so only they can share a cache line; that is why the spatial space uses $H_S$. Since $\ker H \subseteq \ker H_S$, temporal reuse is a special case of spatial reuse.

**Lemma 3 (group reuse).** Let two accesses have the same array and the same $H$ and offsets $c_1, c_2$. Access 1 at iteration $i$ and access 2 at iteration $i'$ touch the same element if and only if $H (i' - i) = c_1 - c_2$. For a subspace $L$, the relation $c_1 \sim c_2 \iff c_1 - c_2 \in H L$ is an equivalence relation on the offsets.

*Proof.* $H i + c_1 = H i' + c_2$ is the same as $H(i' - i) = c_1 - c_2$. The image $H L$ is a subspace, so it contains $0$, it is closed under negation, and it is closed under addition: these give reflexivity, symmetry and transitivity. $\square$

Because $\sim$ is already transitive, the union of all pairs with $c_1 \sim c_2$, which the implementation forms, gives exactly its classes. The number of classes is $g_T$; the same with $H_S$ and the offsets with their last entry set to $0$ is $g_S$.

The test $c_1 - c_2 \in H L$ is over the rational numbers. When every row of $H$ is a unit vector, that is, every subscript is a loop index plus a constant, and $L$ is spanned by unit vectors, a rational solution $r$ can be replaced by an integer one: the entries of $H r$ are entries of $r$, so we can set each needed entry of $r$ to the integer entry of $c_1 - c_2$. Then the rational classes are the classes of real reuse between integer iterations.

## Part 2: the localized space of the transformed nest

**Lemma 4.** Two iterations with the same outer part $o$ differ by a vector of $\operatorname{span}\{e_j : j \in I\}$.

*Proof.* The first $k - m$ rows of $T$ are the first $k - m$ rows of $Q$, which are $\pm e_j$ for the loops $j \notin I$. So $o$ lists the entries $\pm i_j$, $j \notin I$. If two iterations have the same $o$, their difference is $0$ at every $j \notin I$. $\square$

So the iterations inside one tile, and for large tiles inside one run of the band, differ only along the loops of $I$, whatever the skew $S$ is. This is the localized space $L$ of line L6.

## Part 3: legality of the chosen transformation

**Lemma 5 (unimodular).** $\det T = \pm 1$.

*Proof.* $\det Q = \pm 1$ for a signed permutation matrix, and $S$ is unitriangular with determinant $1$. $\square$

So $i \mapsto T i$ is a bijection of $\mathbb{Z}^k$, and the keys $\kappa(i)$ of distinct iterations are distinct.

**Lemma 6 (the band is fully permutable).** If line L4 accepts $(Q, S)$, then for every $d \in D$, with $(o, b) = T d$: either $o$ is lexicographically positive, or $o = 0$, every $b_l \ge 0$, and $b \ne 0$.

*Proof.* Line L4 accepts $Q$ only when the outer part of $Q d$ is lexicographically nonnegative for every $d$, and, for every $d$ whose outer part is $0$, the band part $u$ of $Q d$ is lexicographically positive. The outer part of $T d$ is the outer part of $Q d$. If it is not $0$, it is lexicographically positive.

Now let it be $0$, and let $u$ be the band part of $Q d$. The skew is computed one loop at a time: $b_1 = u_1$ and $b_l = u_l + f_l (b_1 + \dots + b_{l-1})$ for $l \ge 2$, where $f_l = \max(0, \max(-u_l))$ over all $d$ with outer part $0$. We show by induction on $l$ that $b_1, \dots, b_l \ge 0$, and that $b_1 = \dots = b_l = 0$ implies $u_1 = \dots = u_l = 0$.

For $l = 1$: $u$ is lexicographically positive, so $u_1 \ge 0$, and $b_1 = u_1$.

For $l \ge 2$, let $\sigma = b_1 + \dots + b_{l-1} \ge 0$. If $\sigma \ge 1$, then $b_l = u_l + f_l \sigma \ge u_l + f_l \ge 0$, because $f_l \ge 0$ and $f_l \ge -u_l$. If $\sigma = 0$, then $b_1 = \dots = b_{l-1} = 0$, so $u_1 = \dots = u_{l-1} = 0$ by induction; then $u_l$ is the first entry of $u$ that can be nonzero, so $u_l \ge 0$ because $u$ is lexicographically positive, and $b_l = u_l \ge 0$. In both cases the second claim also holds at $l$.

At $l = m$, if $b = 0$ then $u = 0$, which is false since $u$ is lexicographically positive. So $b \ne 0$. $\square$

The matrix $S$ that line L4 builds has the rows $s_l = e_l + f_l (s_1 + \dots + s_{l-1})$, so that $s_l \cdot u = u_l + f_l (b_1 + \dots + b_{l-1})$; that is the recurrence above.

**Lemma 7 (the tiled order keeps every dependence).** For every dependence from $i$ to $j = i + d$, $d \in D$, $\kappa(i) < \kappa(j)$.

*Proof.* Let $(o, b) = T i$ and $(o', b') = T j = T i + T d$. By Lemma 6, either the outer part of $T d$ is lexicographically positive, and then $o' > o$ and $\kappa(j) > \kappa(i)$ in the first part of the key; or $o' = o$ and $b' = b + \delta$ with $\delta \ge 0$ in every entry and $\delta \ne 0$. In the second case, $\lfloor b'_l / B \rfloor \ge \lfloor b_l / B \rfloor$ for every $l$, because the floor is monotone. If some tile entry is larger, the first such entry decides, and $\kappa(j) > \kappa(i)$. If all tile entries are equal, the keys agree up to $b$ and $b'$, and $b' - b = \delta$ is nonnegative and nonzero, so its first nonzero entry is positive and $b' > b$. When $m \le 1$ there are no tile entries and the same argument applies directly. When $m = 0$ the band part is empty, so the second case cannot happen and the outer part decides. $\square$

**Theorem 1 (same result).** The nest that runs the iterations of $P$ in increasing $\kappa$ gives the same final state as the original nest.

*Proof.* By Lemma 5 the keys are distinct, so the order is a total order on $P$ and runs each iteration once. A dependence inside one iteration keeps its order because the body runs as a unit. By Lemma 7, every dependence between two iterations keeps its order. By Theorem 1 of the loop transformation legality page, an order that keeps every dependence pair gives the same final state. $\square$

## Part 4: the search

**Lemma 8 (completeness of line L4).** For a set $I$, line L4 finds $(Q, S)$ if and only if some signed permutation $Q$ that lists the loops of $I$ last makes $Q d$ lexicographically positive for every $d \in D$.

*Proof.* If L4 accepts $Q$, then for every $d$ the outer part of $Q d$ is lexicographically nonnegative, and if it is $0$, the band part is lexicographically positive. In both cases $Q d$ is lexicographically positive. Conversely, if $Q d$ is lexicographically positive for every $d$, then its outer part is lexicographically nonnegative, and when that part is $0$, its band part is lexicographically positive. L4 tries every signed order of the outer loops and every signed order of the band, so it meets this $Q$ or an earlier one that passes the same test; the skew then always exists by Lemma 6. $\square$

**Theorem 2 (cheapest legal set).** Let $\mathcal{F}$ be the sets $I$ for which some signed permutation with the loops of $I$ last is legal. The algorithm returns a set $I^* \in \mathcal{F}$ whose cost in line L7 is the minimum over $\mathcal{F}$, and among sets of equal cost the first in the order of line L3.

*Proof.* $\mathcal{F}$ is not empty: the identity is legal for $I = \emptyset$, because every $d \in D$ is lexicographically positive. Line L3 enumerates every subset of the loops. By Lemma 8, line L5 skips exactly the subsets outside $\mathcal{F}$. Line L8 replaces the best only on a strictly smaller cost, so after the loop the best is the first subset of minimum cost. $\square$

## What the result does not promise

The cost of line L7 is an estimate of the memory accesses per iteration, not a miss count. It does not see the tile size, the size of the cache, or conflicts between arrays in the cache. A tile that is too large for the cache can lose all the reuse that the model counts; the page shows a case with more misses than the original order.

The search covers transformations of the form "signed permutation, then skew of the band". A general unimodular matrix can make a localized space that is not spanned by loop axes. Wolf and Lam also search only over sets of loops, because in practice the reuse spaces are spanned by loop axes. Their SRP heuristic does not try every signed permutation; Lemma 8 holds for the exhaustive search of this implementation.
