---
title: Set operations on grid cells are the regularized set operations, and CLASSIFY, AREA and OCTREE are exact
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. For an integer triple $c$ write $\bar c = \prod_j [c_j, c_j + 1]$ for the closed cell and $\mathring c = \prod_j (c_j, c_j + 1)$ for the open cell. For a finite set $V$ of triples, $[V] = \bigcup_{c \in V} \bar c$. Let $G$ be the union of the grid planes $x_j = t$ with $t$ an integer. Two facts about cells are used throughout. (a) A point not in $G$ lies in exactly one open cell and in no other closed cell. (b) An open cell $\mathring c$ meets the closed cell $\bar d$ only if $d = c$, and every point of $\bar c$ is a limit of points of $\mathring c$.

**Lemma 1 ($[V]$ is an r-set).** For finite $V$, $[V]$ is bounded, closed and regular, $[V] = \operatorname{cl}(\operatorname{int}[V])$, and semianalytic.

*Proof.* A finite union of closed bounded boxes is closed and bounded, and it is a finite Boolean combination of the halfspaces $x_j \ge t$, so it is semianalytic. Each box is regular, $\bar c = \operatorname{cl} \mathring c$, so $[V] = \bigcup_c \operatorname{cl} \mathring c = \operatorname{cl} \bigcup_c \mathring c \subseteq \operatorname{cl}(\operatorname{int}[V]) \subseteq [V]$, where the last step uses that $[V]$ is closed. $\square$

**Lemma 2 (BOOLEAN).** For op one of or, and, and-not, let $\otimes$ be the matching set operation and $\otimes^*$ its regularized form, $X \otimes^* Y = \operatorname{cl}(\operatorname{int}(X \otimes Y))$. Then line L6 returns $U = \{c : \mathrm{op}(c \in V, c \in W)\}$ and $[U] = [V] \otimes^* [W]$.

*Proof.* Line L6 tests every cell of $V \cup W$; a cell in neither set fails op for all three choices, so the result is $U$. Let $X = [V] \otimes [W]$. For a point $x \notin G$ in the open cell $\mathring c$, fact (a) gives $x \in [V]$ exactly when $c \in V$, and the same for $W$, so $x \in X$ exactly when $c \in U$. So $X \setminus G = \bigcup_{c \in U} \mathring c$. This set is open, so it lies in $\operatorname{int} X$, and its closure $[U]$ lies in $\operatorname{cl}(\operatorname{int} X)$. Conversely, $\operatorname{int} X$ is open and $G$ is closed with empty interior, so $\operatorname{int} X \setminus G$ is dense in $\operatorname{int} X$. It lies in $X \setminus G \subseteq [U]$, which is closed, so $\operatorname{cl}(\operatorname{int} X) \subseteq [U]$. $\square$

**Lemma 3 (CLASSIFY).** Line L1 makes $R = R_1 \times R_2 \times R_3$ the set of cells $c$ with $p \in \bar c$, and CLASSIFY returns IN if $p \in \operatorname{int}[V]$, ON if $p \in \partial [V]$ and OUT if $p \notin [V]$.

*Proof.* The point $p$ is in $\bar c$ exactly when $c_j \le p_j \le c_j + 1$ for each $j$, that is when $c_j = \lfloor p_j \rfloor$, or $p_j$ is an integer and $c_j = p_j - 1$. This is L1. The cells that do not contain $p$ are closed, and only finitely many of them lie within distance 1 of $p$, so there is a ball $B$ around $p$ that meets no cell outside $R$. Every point of space lies in some closed cell, so $B \subseteq \bigcup_{c \in R} \bar c$. If $k = 0$, no cell of $V$ contains $p$, and $p \notin [V]$. If every cell of $R$ is in $V$, then $B \subseteq [V]$ and $p \in \operatorname{int}[V]$. Otherwise some $c \in R$ is in $V$ and some $d \in R$ is not. Then $p \in \bar c \subseteq [V]$. By fact (b), $p$ is a limit of points of $\mathring d$, and $\mathring d$ is disjoint from every cell of $V$, so $p$ is a limit of points outside $[V]$ and is on the boundary. Lines L3 to L5 return these three answers. $\square$

**Lemma 4 (VOLUME and AREA).** The volume of $[V]$ is $|V|$, and the area of $\partial [V]$ is the number of pairs $(c, d)$ with $c \in V$, $d \notin V$ and $d$ a face neighbour of $c$.

*Proof.* The open cells are disjoint and the rest of $[V]$ lies in $G$, which has volume 0, so the volume is $|V|$. By Lemma 3, a point $p$ that is in $G$ on exactly one grid plane lies in exactly two cells $c$ and $d$, face neighbours with the common square $\sigma$ in that plane, and $p \in \partial[V]$ exactly when one of them is in $V$ and the other is not. The points on two or more grid planes lie on the grid lines, which have area 0, and the points off $G$ are not on the boundary. So $\partial[V]$ is, up to a set of area 0, the union of the unit squares $\sigma$ between such pairs. Each such square has area 1 and is counted once, from the side of the cell in $V$. $\square$

**Lemma 5 (OCTREE).** For a set $C$ of cells inside the cube $Q$ of side $s = 2^d$ at $corner$, OCTREE($C$, $corner$, $s$) stops, and it returns a tree whose FULL leaves cover exactly the cells of $C$, in which no internal node has eight children that are all EMPTY or all FULL. The joint walk of two such trees returns the tree of the same kind for $C_1 \otimes C_2$.

*Proof.* By induction on $d$. Lines L7 and L8 return a correct leaf when $C$ is empty or is every cell of $Q$; when $d = 0$ the cube has one cell, so one of the two holds. Otherwise $C$ is mixed, and L9 splits it among the eight subcubes of side $2^{d-1}$, each cell going to the one subcube that contains it; the induction hypothesis gives correct children, and the node is mixed, so it is not one leaf. The depth falls by one per call, so the recursion stops. For the walk, a leaf of value $v$ on a cube stands for the same cells as eight leaves of value $v$ on its subcubes, so expanding a leaf does not change the set, and op applied to two leaves is op applied to every cell of their cube. By induction the eight results are correct, and replacing eight equal leaves by one keeps the set and the reduced form. A reduced tree is unique for its set, since L7 and L8 decide each node from the set alone, so the walk returns the same tree as OCTREE of the result. $\square$

**Lemma 6 (the error of SAMPLE).** Let $S$ be a closed set and $V = \{c : \text{the centre of } c \text{ is in } S\}$. If $\bar c$ does not meet $\partial S$, then $c \in V$ exactly when $\bar c \subseteq S$. So $S \mathbin{\triangle} [V]$ lies in the union of the cells that meet $\partial S$.

*Proof.* Space is the disjoint union of $\operatorname{int} S$, $\partial S$ and the open set outside $S$. If $\bar c$ misses $\partial S$, then it is the union of its two disjoint relatively open parts in $\operatorname{int} S$ and outside $S$. A cube is connected, so one part is empty, and the centre decides which one. A point of $S \mathbin{\triangle} [V]$ in a cell $\bar c$ that misses $\partial S$ would contradict this. $\square$

**Lemma 7 (the area on a convex solid).** If $S$ is convex, then every grid line parallel to an axis meets the cells of $V$ in one run, so AREA($V$) is twice the number of such lines that meet $V$.

*Proof.* The centres on one line that lie in $S$ are the centres in the segment where the line meets $S$, a convex set, so they are consecutive. A run gives exactly two boundary squares across that line, one at each end, and every boundary square is the end of a run on the line through the two cells beside it. $\square$

For a ball of radius $r$ in unit cells, the lines parallel to one axis that meet $V$ number $\pi r^2 + O(r)$: a line through a point of the disk at distance at most $r - 1$ from the centre meets a chord longer than 2, so it holds a centre, and the lattice points of a disk of radius $r$ number $\pi r^2 + O(r)$. So AREA($V$) $= 6 \pi r^2 + O(r)$, while the sphere has area $4 \pi r^2$.

**Theorem.** BOOLEAN returns the voxel sets of the regularized union, intersection and difference; CLASSIFY, VOLUME and AREA return the class of a point, the volume and the boundary area of $[V]$; OCTREE and the joint walk return the reduced octree of their set. Each operation stops: BOOLEAN, CLASSIFY and AREA after a finite loop over at most $|V| + |W|$ cells, 8 cells and $6|V|$ pairs, OCTREE after $d + 1$ levels of calls.

*Proof.* Lemmas 1 to 5 give the results, and the loops and the recursion are bounded as stated. $\square$

The tests check Lemma 2 and Lemma 3 together against ordinary point membership: at a point $p$ of the half-integer grid, each point $p + s/4$ with $s \in \{-1, +1\}^3$ lies in one open cell, so by the proof of Lemma 2 the ordinary result there agrees with the regularized one, and by Lemma 3 $p$ is IN, ON or OUT as these eight points are all, some or none in it. They check Lemma 4 by counting the square centres that CLASSIFY puts ON, Lemmas 6 and 7 on a sampled ball, and Lemma 5 by round trips and Booleans on random octrees. $\blacksquare$
