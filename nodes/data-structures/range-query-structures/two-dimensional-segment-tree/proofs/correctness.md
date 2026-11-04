---
title: The two-dimensional segment tree keeps the rectangle products and returns rectangle queries
proves: [correctness, termination]
status: full
---

Let $(S, \oplus, e)$ be a commutative monoid. For a finite set $Z$ of cells of $M$ write $\Pi(Z) = \bigoplus_{(i, j) \in Z} M[i][j]$, which is well defined by associativity and commutativity, with $\Pi(\emptyset) = e$, and $\Pi(Z_1 \cup Z_2) = \Pi(Z_1) \oplus \Pi(Z_2)$ for disjoint $Z_1, Z_2$. For an outer node $v_x$ with rows $X(v_x) = [l_x, r_x]$ and an inner node $v_y$ with columns $Y(v_y) = [l_y, r_y]$, the invariant is

$$\text{(T)} \qquad t[v_x][v_y] = \Pi\bigl(X(v_x) \times Y(v_y)\bigr).$$

We use the facts about the shape of a one-dimensional segment tree from the [segment tree](/segment-tree/) page: the children of a node with range $[lo, hi]$, $lo < hi$, have the ranges $[lo, mid]$ and $[mid + 1, hi]$, which split it; a node with $lo = hi$ is a leaf; and the recursion depth is at most $\lceil \lg n \rceil + 1$.

**Termination.** Every recursive call of BUILD-X, BUILD-Y, QUERY-X, QUERY-Y, UPDATE-X and UPDATE-Y is on a child range, which is strictly shorter than the range of the caller, and no call recurses on a range of length 1. So each call tree is finite.

**Lemma 1 (build).** After BUILD-X$(1, 0, n - 1)$, (T) holds for every outer node $v_x$ and every inner node $v_y$.

*Proof.* By induction on the outer recursion: assume that (T) holds for all cells of the outer children of $v_x$ when line L7 runs, which line L6 ensures by the hypothesis, since it builds them first; outer leaves have no children. We show that BUILD-Y on $v_x$ makes (T) true for each $v_y$, by induction on the inner recursion. At an inner leaf, $Y(v_y) = \{l_y\}$. If $v_x$ is an outer leaf, $X(v_x) = \{l_x\}$ and line L2 stores $M[l_x][l_y] = \Pi(\{(l_x, l_y)\})$. Otherwise, $X(v_x)$ is the disjoint union of $X(2v_x)$ and $X(2v_x + 1)$, and by the outer hypothesis line L2 stores $\Pi(X(2v_x) \times \{l_y\}) \oplus \Pi(X(2v_x + 1) \times \{l_y\}) = \Pi(X(v_x) \times \{l_y\})$. At an inner node that is not a leaf, line L4 builds both inner children first, so by the inner hypothesis line L5 stores $\Pi(X(v_x) \times Y(2v_y)) \oplus \Pi(X(v_x) \times Y(2v_y + 1)) = \Pi(X(v_x) \times Y(v_y))$, since $Y(2v_y)$ and $Y(2v_y + 1)$ split $Y(v_y)$. $\square$

**Lemma 2 (inner query).** If (T) holds for $v_x$, then QUERY-Y$(v_x, v_y, l_y, r_y, c_1, c_2)$, with $[l_y, r_y] = Y(v_y)$, returns $\Pi\bigl(X(v_x) \times ([l_y, r_y] \cap [c_1, c_2])\bigr)$.

*Proof.* By induction on $r_y - l_y$. If the two ranges are disjoint, line L8 returns $e$, the product of the empty set. If $[l_y, r_y] \subseteq [c_1, c_2]$, line L9 returns $t[v_x][v_y]$, which is right by (T). Otherwise $l_y < r_y$, since a range of length 1 that meets $[c_1, c_2]$ lies inside it. Then $[l_y, r_y] \cap [c_1, c_2]$ is the disjoint union of its intersections with $[l_y, m_y]$ and $[m_y + 1, r_y]$, and line L10 returns the product of the two results, which are right by the hypothesis. $\square$

**Lemma 3 (outer query).** If (T) holds everywhere, then QUERY-X$(v_x, l_x, r_x, r_1, r_2, c_1, c_2)$, with $[l_x, r_x] = X(v_x)$, returns $\Pi\bigl(([l_x, r_x] \cap [r_1, r_2]) \times [c_1, c_2]\bigr)$ for $0 \le c_1 \le c_2 \le m - 1$.

*Proof.* By induction on $r_x - l_x$, as in Lemma 2. Line L11 returns $e$ for disjoint rows. Line L12 returns, by Lemma 2 at the inner root with $Y(1) = [0, m - 1]$, the value $\Pi(X(v_x) \times [c_1, c_2])$, which is right when $X(v_x) \subseteq [r_1, r_2]$. Otherwise the rows split between the two children, and line L13 combines the two correct parts, which are products over disjoint sets of cells. $\square$

**Lemma 4 (update).** Let (T) hold for a matrix $M$, let $M'$ differ from $M$ only at $(r, c)$, and let the stored matrix be $M'$ when UPDATE-X$(1, 0, n - 1, r, c)$ is called. After the call, (T) holds for $M'$.

*Proof.* A cell $(v_x, v_y)$ has a different right side in (T) for $M$ and for $M'$ only if $r \in X(v_x)$ and $c \in Y(v_y)$. The outer nodes with $r \in X(v_x)$ are the nodes on the root-to-leaf path $P_x$ of row $r$, and the inner nodes with $c \in Y(v_y)$ are the nodes on the path $P_y$ of column $c$. So only the cells of $P_x \times P_y$ need a new value.

The recursion of UPDATE-X visits exactly the nodes of $P_x$, and for each of them it calls UPDATE-Y only after the call on its child in $P_x$ has returned (line L19 before line L20). We show by induction from the outer leaf upward that, when UPDATE-Y on $v_x \in P_x$ returns, all cells $(v_x, v_y)$ satisfy (T) for $M'$. Cells with $v_y \notin P_y$ did not change and were right. UPDATE-Y visits the nodes of $P_y$ from the root down to the leaf and recomputes them on the way back. At the inner leaf, line L15 reads $M'$ if $v_x$ is an outer leaf, or the cells $(2v_x, v_y)$ and $(2v_x + 1, v_y)$ otherwise: one child is in $P_x$ and right for $M'$ by the outer hypothesis, and the other child's rows do not hold $r$, so its cells were right and unchanged. As in Lemma 1, the new value is right. Each inner node of $P_y$ above the leaf is recomputed at line L18 from its two inner children, of which the one in $P_y$ was just made right and the other one did not change. So all cells of $v_x$ are right for $M'$. At the outer root this gives (T) everywhere. $\square$

**Theorem.** After BUILD-X on $M$ and any sequence of updates, each done by setting one entry and calling UPDATE-X, a call QUERY-X$(1, 0, n - 1, r_1, r_2, c_1, c_2)$ with $0 \le r_1 \le r_2 \le n - 1$ and $0 \le c_1 \le c_2 \le m - 1$ returns $\bigoplus_{r_1 \le i \le r_2} \bigoplus_{c_1 \le j \le c_2} M[i][j]$ for the current matrix.

*Proof.* By Lemma 1 and Lemma 4, (T) holds for the current matrix. By Lemma 3 at the outer root, with $X(1) = [0, n - 1]$, the query returns $\Pi([r_1, r_2] \times [c_1, c_2])$. All calls end by the termination argument. $\blacksquare$
