---
title: The PHT-spline space has dimension 4(V_b + V_+), and REFINE builds a basis with partition of unity
proves: [correctness]
status: full
---

We use the notation of the page. The domain is $\Omega = [0, n]^2$. A cell of level $\ell$ is a square $[i h, (i+1) h] \times [j h, (j+1) h]$ with $h = 2^{-\ell}$. The mesh $T_0$ is the set of the $n^2$ cells of level 0. If the finest level of $T_k$ is $K$, then $T_{k+1}$ comes from $T_k$ when we replace some leaves of level $K$ by their four children. The vertices are the corners of the leaves. $S(T)$ is the set of $C^1$ functions on $\Omega$ that are bicubic polynomials on each leaf. The *order* of a point $v$ is the least $m \ge 0$ with $v \in (2^{-m}\mathbb{Z})^2$. The *data* of a function at a vertex are $(f, f_x, f_y, f_{xy})$ there.

**Lemma 1 (the mesh).** Let $T = T_k$.

1. Every vertex has order at most the finest level $K$, and a vertex of order $m$ is a corner only of leaves of level at least $m$.
2. Two leaves whose sides lie on the same line and overlap in a segment of positive length have nested sides.
3. A vertex lies inside a side (not at an end) of at most one leaf. If it lies inside a side of a leaf $C$ of level $\ell$, then its order is greater than $\ell$, the vertex is not on $\partial\Omega$, and each corner of $C$ has order at most $\ell$.

*Proof.* (1) A corner of a cell of level $\ell$ lies in $(2^{-\ell}\mathbb{Z})^2$, so its order is at most $\ell \le K$. If $v$ of order $m$ is a corner of a leaf of level $\ell$, then $m \le \ell$.

(2) The sides are dyadic intervals $[a 2^{-\ell}, (a+1) 2^{-\ell}]$. Two dyadic intervals with overlapping interiors are nested.

(3) Say $v$ lies inside a side of $C$, and the side is vertical; the other case is the same. Then $C$ covers the points next to $v$ on one side of the line, above and below $v$. A leaf $D$ with $v$ as a corner exists, because $v$ is a vertex. $D$ cannot lie on the side of $C$, because leaves do not overlap. So $D$ lies on the other side, and the line is not part of $\partial\Omega$ near $v$. The same argument shows that $v$ is not on $\partial\Omega$ at all: if $v$ were on the boundary, the side of $C$ would have to lie on the boundary, and then no leaf could have $v$ as a corner. Now suppose that $v$ also lies inside a side of a leaf $C' \ne C$. If that side is on the same line, $C'$ lies on the other side, and covers the points next to $v$ there, so no leaf has $v$ as a corner. If that side is horizontal, $C$ and $C'$ overlap in a quadrant next to $v$. Both cases are impossible. Last, the coordinate of $v$ along the side lies strictly between two neighbouring multiples of $2^{-\ell}$, so its order is greater than $\ell$, while the corners of $C$ have order at most $\ell$. $\square$

So the vertices split into the boundary vertices, the *T-junctions* (the interior vertices that lie inside a side of a leaf, which is their unique *host*), and the *crossings* (the other interior vertices). The basis vertices are the boundary vertices and the crossings. The test of CLASSIFY is this definition: $v$ lies inside a vertical side of a cell of level $\ell$ exactly when $2^\ell v_x$ is an integer and $2^\ell v_y$ is not, and the cell is then one of the two cells of level $\ell$ to the left and right of $v$.

**Lemma 2 (data of a spline).** Let $f \in S(T)$.

1. At every vertex $v$, the data of the polynomials of all leaves that contain $v$ are equal. So the data of $f$ at $v$ are well defined.
2. On each leaf $C$, $f$ is the bicubic Hermite interpolant of its data at the four corners of $C$.

*Proof.* (1) Let $A$ and $B$ be leaves on the two sides of a vertical line $x = a$, with a common segment $I$ of positive length. Since $f$ is $C^1$, $p_A(a, y) = p_B(a, y)$ and $\partial_x p_A(a, y) = \partial_x p_B(a, y)$ for $y \in I$. Differentiate in $y$: $\partial_y p_A = \partial_y p_B$ and $\partial_{xy} p_A = \partial_{xy} p_B$ on $I$. These are polynomials, so the equalities also hold at the ends of $I$. The same holds for a horizontal line. The leaves that contain $v$ cover a neighbourhood of $v$ in $\Omega$. When we go around $v$, two consecutive leaves share a segment of positive length that ends at $v$. So all their data at $v$ are equal.

(2) In one variable, cubic Hermite interpolation on an interval reproduces every cubic, because a cubic with zero value and slope at both ends is zero. The bicubic Hermite interpolant is the tensor product of two such operators, so it reproduces every bicubic. $\square$

**Lemma 3 (when cellwise data give a spline).** Let $D$ assign data to every vertex of $T$. Let $g$ be the function that is, on each leaf, the bicubic Hermite interpolant of $D$ at the corners of the leaf. Then $g \in S(T)$ if and only if, for each T-junction $w$ with host $C$, $D(w)$ equals the data at $w$ of the polynomial $g|_C$. Call this condition (T).

*Proof.* If $g \in S(T)$, then (T) holds by Lemma 2. Conversely, assume (T). Let $A$ and $B$ be leaves with a common segment of positive length on a line, say $x = a$. By Lemma 1(2) the sides are nested; say the side $\sigma_B$ of $B$ lies in the side $\sigma_A$ of $A$. Each end $w$ of $\sigma_B$ is a corner of $A$ or lies inside $\sigma_A$. In the second case $w$ is a T-junction with host $A$, by Lemma 1(3). In both cases $D(w)$ equals the data of $p_A$ at $w$: in the first case because $p_A$ interpolates $D$ at its corners, in the second case by (T).

On the line $x = a$, the trace $p_B(a, \cdot)$ on $\sigma_B$ is the cubic Hermite interpolant of the values $f$ and slopes $f_y$ of $D$ at the ends of $\sigma_B$, because the $x$ shapes are 1 or 0 at $x = a$ and their slopes are 0. In the same way, $\partial_x p_B(a, \cdot)$ is the cubic Hermite interpolant of $f_x$ and $f_{xy}$ at the ends. The traces of $p_A$ on $\sigma_B$ are cubics with the same data at the ends, so by Lemma 2(2) in one variable they are equal. So $p_A = p_B$ and $\partial_x p_A = \partial_x p_B$ on $\sigma_B$, and then also $\partial_y p_A = \partial_y p_B$ there. So $g$ and $\nabla g$ are continuous across every common segment of two leaves. Each is a polynomial on each leaf, so each is continuous on $\Omega$, and $g \in S(T)$. $\square$

**Theorem 1 (dimension).** The map that takes $f \in S(T)$ to its data at the basis vertices is a linear bijection onto $(\mathbb{R}^4)^{V_b + V_+}$. So $\dim S(T) = 4(V_b + V_+)$.

*Proof.* By Lemmas 2 and 3, $f \mapsto$ (its data at all vertices) is a linear bijection from $S(T)$ onto the set of $D$ that satisfy (T). Let $E$ be any data at the basis vertices. We define $D$ at the T-junctions in increasing order. For a T-junction $w$ with host $C$, the corners of $C$ have a smaller order than $w$ by Lemma 1(3), so $D$ is already defined at them. Set $D(w)$ to the data at $w$ of the Hermite interpolant of $D$ at the corners of $C$. Then $D$ satisfies (T), and it agrees with $E$. Every $D$ that satisfies (T) and agrees with $E$ is equal to this one, by the same induction. So the restriction to the basis vertices is a bijection from the set of $D$ that satisfy (T). $\square$

**Lemma 4 (one step).** Let $T' = T_{k+1}$ come from $T = T_k$ by splitting a set $R$ of leaves of the finest level $K$. Then:

1. The new vertices are the side midpoints and centres of the cells of $R$. They have order $K + 1$.
2. The host of every T-junction of $T'$ is a leaf of $T$ that is not split. Its corners are vertices of $T$.
3. The old T-junctions stay T-junctions with the same host, and the old basis vertices stay basis vertices. So the set $N$ of line L2 contains only new vertices.

*Proof.* (1) The new leaves are the children of the cells of $R$. Their corners are the corners of the parents and these five points of order $K + 1$. A point of order $K + 1$ is not a vertex of $T$, by Lemma 1(1).

(2) A host of level $K + 1$ would make a T-junction of order greater than $K + 1$, by Lemma 1(3). That is not possible by Lemma 1(1). So the host has level at most $K$ and is a leaf of $T$ that is not split.

(3) An old T-junction $w$ has order at most $K$, so its host has level less than $K$, by Lemma 1(3). The host is not split, so $w$ still lies inside its side. An old basis vertex $v$ does not lie inside a side of an old leaf. It also does not lie inside a side of a new leaf, because that would give $v$ an order greater than $K + 1$. So $v$ is still a basis vertex. $\square$

**Invariant.** For a basis vertex $v$ of level $\ell$ (the step at which it became a basis vertex), let $h = 2^{-\ell}$. Let $h_-$ and $h_+$ be $h$, or $0$ when $v_x = 0$ or $v_x = n$ on that side, and let $H = h_- + h_+$. Let $A_v$ be the $2 \times 2$ matrix with the rows $(h_+/H, -3/H)$ and $(h_-/H, 3/H)$. Define $B_v$ in the same way in $y$. The function $(v, \alpha, \beta)$ has the data $D_v(\alpha, \beta) = (A_\alpha^0 B_\beta^0, A_\alpha^1 B_\beta^0, A_\alpha^0 B_\beta^1, A_\alpha^1 B_\beta^1)$ at $v$, where $A_\alpha^i$ is the entry in row $\alpha$ and column $i$ of $A_v$. The invariant after step $k$ is this. For each stored function, the stored data (zero where nothing is stored) satisfy (T) on $T_k$, they are $D_v(\alpha, \beta)$ at its own vertex $v$, and they are zero at every other basis vertex.

**Theorem 2 (REFINE keeps the invariant).** The invariant holds after every step.

*Proof.* At step 0 there are no T-junctions, and each function stores $D_v(\alpha, \beta)$ at $v$ only. So the invariant holds.

Assume that it holds for $T = T_k$. Let $g \in S(T)$ be an old function. By Theorem 1 and Lemma 3 its stored data are its data at all vertices of $T$. The function $g$ is also in $S(T')$, because a polynomial on a split cell is a polynomial on each child. Its data at the old vertices do not change. Line L4 computes its data at the new vertices from the polynomial of a split cell $P$ that contains the new vertex. If $P$ has zero data at its four corners, the polynomial is zero and line L4 can skip $P$. A new vertex on a side shared by two split cells gets the same data from both cells, by Lemma 2(1). So after line L4 the stored data are the data of $g$ at all vertices of $T'$, and they satisfy (T) on $T'$.

Line L5 sets the data at the vertices of $N$ to zero. Call the result $D'$. Let $w$ be a T-junction of $T'$ with host $C$. By Lemma 4(2) the corners of $C$ are vertices of $T$, so by Lemma 4(3) they are not in $N$. Also $w \notin N$, because $w$ is not a basis vertex. So $D'$ equals the data of $g$ at $w$ and at the corners of $C$, and $D'$ still satisfies (T). At the old basis vertices $D'$ is unchanged, so it is $D_v(\alpha, \beta)$ at its own vertex and zero at the others. At the vertices of $N$ it is zero.

Line L6 stores, for each $v \in N$, the data $D_v(\alpha, \beta)$ at $v$ and zero elsewhere. For a T-junction $w$ with host $C$, the corners of $C$ are old vertices, so they are not $v$, and the polynomial on $C$ is zero. So the stored zero at $w$ satisfies (T). $\square$

**Theorem 3 (basis and partition of unity).** After any sequence of steps, the stored functions form a basis of $S(T)$ and sum to 1.

*Proof.* $\det A_v = 3 h_+/H^2 + 3 h_-/H^2 = 3/H \ne 0$, and the same holds for $B_v$. The four vectors $D_v(\alpha, \beta)$ are the rows of the Kronecker product $A_v \otimes B_v$, with the columns in a fixed order. This product has the determinant $(\det A_v)^2 (\det B_v)^2 \ne 0$. By Theorem 2, the images of the functions under the bijection of Theorem 1 form a block diagonal matrix with these invertible $4 \times 4$ blocks. So the $4(V_b + V_+)$ functions are a basis.

The rows of $A_v$ sum to $(1, 0)$, and so do the rows of $B_v$. So $\sum_{\alpha, \beta} D_v(\alpha, \beta) = (1, 0, 0, 0)$. At a basis vertex $v$, only the four functions of $v$ have nonzero data. So the sum of all the functions has the data $(1, 0, 0, 0)$ at every basis vertex. The constant 1 has the same data. By Theorem 1 the sum is 1. $\square$

**Theorem 4 (COEFFICIENTS).** Let $s \in S(T)$ have the data $E(v) = (f, f_x, f_y, f_{xy})$ at the basis vertex $v$. Let $s_0 = -h_-/3$, $s_1 = h_+/3$, and define $t_0, t_1$ in the same way in $y$. Then $s = \sum c_{v, \alpha, \beta}\, b_{v, \alpha, \beta}$, with $c_{v, \alpha, \beta} = f + s_\alpha f_x + t_\beta f_y + s_\alpha t_\beta f_{xy}$.

*Proof.* Write $E(v)$ as $E_{ij}$, where $i$ and $j$ are the orders of the derivatives in $x$ and $y$. Then $c_{v, \alpha, \beta} = \sum_{i, j} E_{ij} s_\alpha^i t_\beta^j$. We have $\sum_\alpha A_\alpha = (1, 0)$, and

$$\sum_\alpha s_\alpha A_\alpha = \Bigl(-\frac{h_-}{3} \frac{h_+}{H} + \frac{h_+}{3} \frac{h_-}{H},\ \frac{h_-}{3} \frac{3}{H} + \frac{h_+}{3} \frac{3}{H}\Bigr) = (0, 1).$$

So $\sum_\alpha s_\alpha^i A_\alpha^{i'} = \delta_{i i'}$, and the same holds in $y$. The data at $v$ of the sum are

$$\sum_{\alpha, \beta} c_{v, \alpha, \beta} A_\alpha^{i'} B_\beta^{j'} = \sum_{i, j} E_{ij} \Bigl(\sum_\alpha s_\alpha^i A_\alpha^{i'}\Bigr) \Bigl(\sum_\beta t_\beta^j B_\beta^{j'}\Bigr) = E_{i' j'}.$$

At $v$ only the functions of $v$ contribute. So the sum has the data $E$ at all basis vertices, and by Theorem 1 it equals $s$. $\square$

**Remarks.** (1) A new basis vertex $v$ of step $k + 1$ has order $K + 1$. By Lemma 1(1), the leaves with corner $v$ are the four (or two, at the boundary) children around $v$. The new function of line L6 is zero on every other leaf, because its data are zero at all other vertices. On these leaves it has the same data as the tensor product of the $C^1$ cubic B-splines with the local knots $(v - h, v - h, v, v, v + h)$ and $(v - h, v, v, v + h, v + h)$, $h = 2^{-(K+1)}$. Both are in $S(T')$, so they are equal. At step 0 the same argument shows that the basis is the tensor product $C^1$ cubic B-spline basis. (2) By Theorems 2 and 4, an old function $g$ changes in one step to $g - \sum_{v \in N} \sum_{\alpha, \beta} c_{v, \alpha, \beta}(g)\, b_{v, \alpha, \beta}$. Both sides have the same data at all basis vertices of $T'$. This is the modification of Deng and coauthors. (3) The functions are nonnegative. This is proved in the paper of Deng and coauthors, and it is not proved here. The tests check it at sample points.

So EVALUATE, which evaluates the Hermite interpolant of the stored data on the leaf that contains the point, returns the function. REFINE keeps a basis of $S(T)$ with partition of unity, and COEFFICIENTS gives the coordinates of a spline in that basis. $\blacksquare$
