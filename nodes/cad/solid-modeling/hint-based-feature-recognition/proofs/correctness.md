---
title: The features found from hints cover exactly the reachable part of the removal area, the undercut runs cover the rest, and the stock minus all of them is the part
proves: [correctness, termination]
status: full
---

We use the notation and the pseudocode of the page. $P$ is a closed region bounded by a simple rectilinear polygon with integer vertices, so $P$ is regular and $P = \overline{\operatorname{int} P}$. Let $x_0 < \dots < x_a$ and $y_0 < \dots < y_b$ be the distinct vertex coordinates, and let $W = [x_0, x_a] \times [y_0, y_b]$ be the bounding box (line L1). The grid $G$ is the union of the lines $x = x_i$ and $y = y_j$ inside $W$. The open cell $(i, j)$ is $C_{ij} = (x_i, x_{i+1}) \times (y_j, y_{j+1})$, with $0 \le i < a$ and $0 \le j < b$. The removal area is $D = W -^* P = \overline{\operatorname{int}(W \setminus P)}$. For a set $S$ of cells, $|S|$ is the closure of the union of its open cells. A *block* is a set of cells $[i_0, i_1) \times [j_0, j_1)$, and $|B|$ is a closed rectangle.

The sides of $W$ are top, bottom, left and right, with normals $(0,1)$, $(0,-1)$, $(-1,0)$ and $(1,0)$. For a cell $c$ and a side $s$, the *strip* of $c$ to $s$ is the block of cells from $c$ to the side $s$ in the direction of the normal of $s$. For example, the strip of $(i, j)$ to the top is $[i, i+1) \times [j, b)$.

**Lemma 1 (cells are pure).** Each open cell lies in $\operatorname{int} P$ or in $\mathbb{R}^2 \setminus P$. Let $S_P$ and $S_D$ be the two kinds. Then $P = |S_P|$ and $D = |S_D|$, and line L1 puts in $D$ exactly the cells of $S_D$.

*Proof.* This is Lemmas 1 and 2 of the proof for [volume decomposition](/volume-decomposition-feature-recognition/), with the same grid and the same centre test. Every edge of the polygon lies on a grid line, so an open cell misses $\partial P$ and, being connected, lies on one side of it. The closure claims follow because $G$ is closed with empty interior, so removing it from an open set does not change the closure. $\square$

**Reachability.** A point $p$ of an open cell $C \subseteq D$ is *reachable from side* $s$ if the segment from $p$ to the side $s$ of $W$, in the direction of the normal of $s$, misses $\operatorname{int} P$. A cell is reachable from $s$ if its points are.

**Lemma 2.** A cell of $S_D$ is reachable from $s$ if and only if every cell of its strip to $s$ is in $S_D$. Then all its points are reachable from $s$.

*Proof.* The segment from $p$ to side $s$ passes through the open cells of the strip, and between consecutive ones it crosses a grid line at a single point. If a cell of the strip is in $S_P$, the segment meets that open cell, which lies in $\operatorname{int} P$. If all cells of the strip are in $S_D$, the segment meets no point of $\operatorname{int} P$ inside those open cells, which lie outside $P$. A point $q$ where it crosses a grid line between two such cells is not in $\operatorname{int} P$ either, since every neighbourhood of $q$ meets those open cells, which lie outside $P$. The condition depends only on the cell, so it holds for all points of the cell at once. $\square$

**Lemma 3 (every row and column holds a cell of $P$).** For every $i$ there is a $j$ with $(i, j) \in S_P$, and for every $j$ there is an $i$ with $(i, j) \in S_P$.

*Proof.* The interior of the region bounded by a simple polygon is connected and open, so its projection to the $x$-axis is an open interval $I$. The projection is continuous and $P = \overline{\operatorname{int} P}$, so the projection of $P$, which is $[x_0, x_a]$ because $W$ is the bounding box, lies in $\overline{I}$. Hence $I = (x_0, x_a)$. Pick $x^*$ in $(x_i, x_{i+1}) \subseteq I$ and a point $(x^*, y^*)$ of $\operatorname{int} P$. Since $\operatorname{int} P$ is open, we can move $y^*$ slightly so that it lies on no grid line, while keeping the point in $\operatorname{int} P$ and $x^*$ fixed. The point then lies in an open cell of column $i$, which meets $\operatorname{int} P$ and so is in $S_P$ by Lemma 1. Rows are the same with the axes swapped. $\square$

**Lemma 4 (completion).** Let $(c, s)$ be a hint of line L2. If some cell of the strip of $c$ to $s$ is in $S_P$, line L3 drops the hint. Otherwise lines L3 and L4 return a block $B$ with these properties.
(a) Every cell of $B$ is in $S_D$, and $B$ contains the strip of $c$ to $s$.
(b) $B$ reaches the side $s$: for $s$ the top, $B = [i_0, i_1) \times [j, b)$ where $j$ is the row of $c$.
(c) Every cell of $B$ is reachable from $s$.

*Proof.* Line L3 tests the strip with the prefix sums, which count the cells of $S_D$ in a block exactly, so it drops the hint exactly when the strip holds a cell of $S_P$. Take $s$ the top; the other sides are the same after a rotation. The block starts as the strip $[i, i+1) \times [j, b)$. Line L4 adds the column $i_0 - 1$ or $i_1$ over the rows $[j, b)$ only when all its cells are in $S_D$. So (a) and (b) hold by induction over the growth steps. For (c), the strip to the top of a cell $(i', j')$ of $B$ is $[i', i'+1) \times [j', b)$, which lies in $B$ because $j' \ge j$. All its cells are in $S_D$ by (a), so the cell is reachable by Lemma 2. Each loop of line L4 adds a column inside the grid each time, so it stops after at most $a$ steps. $\square$

**Lemma 5 (every reachable cell is covered).** Let $c \in S_D$ be reachable from $s$. Then some block that line L5 records for side $s$ contains $c$.

*Proof.* Take $s$ the top and $c = (i, j)$. By Lemma 3, column $i$ holds a cell of $S_P$. By Lemma 2 the cells $(i, j), \dots, (i, b-1)$ are all in $S_D$, so every cell of $S_P$ in column $i$ lies below row $j$. Let $(i, k)$ with $k < j$ be the highest one. Then the cells $(i, k+1), \dots, (i, j)$ are in $S_D$. The cell $d = (i, k+1)$ is in $S_D$, and its neighbour opposite the top, $(i, k)$, is in $S_P$, so $(d, \text{top})$ is a hint of line L2. Its strip $[i, i+1) \times [k+1, b)$ consists of cells of $S_D$: those up to row $j$ by the choice of $k$, and those above by the reachability of $c$. So line L3 keeps the hint, and by Lemma 4(a) its block contains the strip, which contains $c$. $\square$

**Lemma 6 (open sides).** A block recorded in line L5 for side $s$ has $s$ among its open sides. No block of cells of $S_D$ has two opposite open sides. So each recorded block has one open side or two adjacent ones, and line L7 calls it a slot or a step.

*Proof.* The first claim is Lemma 4(b). A block with the left and right sides open spans all columns, so any of its rows consists of cells of $S_D$ only, against Lemma 3. Top and bottom are the same. So at most two sides are open, and two open sides are adjacent. $\square$

**Lemma 7 (undercut runs).** Let $U$ be the set of cells of $S_D$ covered by no block of line L5. Each run that line L6 records consists of cells of $S_D$, contains a cell of $U$, and has no open side. Every cell of $U$ lies in a recorded run.

*Proof.* Line L6 takes, in each row, the maximal runs of consecutive cells of $S_D$ and records those that contain a cell of $U$. A cell $u \in U$ lies in exactly one maximal run of its row, which is then recorded. By Lemma 5, $u$ is reachable from no side. If the run of $u$ contained the first or last cell of the row, it would contain the strip of $u$ to the left or the right, and $u$ would be reachable by Lemma 2. If the run lay in row $0$ or row $b-1$, the strip of $u$ to the bottom or the top would be $u$ alone, and $u$ would again be reachable. So the run has no open side. $\square$

**Theorem.** Let $F$ be the blocks of line L5 and $R$ the runs of line L6. Then:
1. every block of $F \cup R$ consists of cells of $S_D$, so $|B| \subseteq D$;
2. the union of $|B|$ over $F \cup R$ is $D$;
3. $W -^* \bigcup_{B \in F \cup R} |B| = P$;
4. a point of an open cell of $S_D$ lies in a block of $F$ if and only if its cell is reachable from some side;
5. the blocks of $F$ are reached from the sides that line L5 records, which are among their open sides, and the runs of $R$ have no open side.

*Proof.* Part 1 is Lemma 4(a) and Lemma 7. For part 2, the blocks of $F$ cover every cell of $S_D$ outside $U$ by the definition of $U$, and the runs of $R$ cover $U$ by Lemma 7. So the union of the closed blocks is a finite union of closed sets. It contains every open cell of $S_D$ and so its closure $|S_D| = D$, and by part 1 it lies in $D$.

For part 3, write $D = |S_D|$. The open cells of $S_P$ are open and disjoint from every open cell of $S_D$, so they miss the closure $D$ and lie in $\operatorname{int}(W \setminus D)$. Taking closures, $P = |S_P| \subseteq W -^* D$. Conversely, $\operatorname{int}(W \setminus D)$ is an open set that misses every open cell of $S_D$, so it lies in $|S_P| \cup G$. An open set $V \subseteq P \cup G$ satisfies $\overline{V} = \overline{V \setminus G} \subseteq P$, so $W -^* D \subseteq P$.

For part 4, a cell in a block of $F$ is reachable by Lemma 4(c), and a reachable cell lies in a block of $F$ by Lemma 5. A point of an open cell lies in a closed block exactly when its cell belongs to the block. Part 5 is Lemma 6 and Lemma 7. $\square$

**Termination.** The grid is finite and line L2 yields at most four hints per cell. Each completion stops by Lemma 4. The marking of covered cells and the row scan of line L6 visit finitely many cells. So the method stops.

**Cost of the marking.** For the side top, the block of a kept hint in row $j$ is the maximal run of columns $[i_0, i_1)$ around the hint's column for which the block $[i_0, i_1) \times [j, b)$ consists of cells of $S_D$. Two such runs for the same $j$ are equal or disjoint, because the union of two overlapping runs would also qualify. So the distinct top blocks with lower row $j$ hold at most $a(b - j)$ cells together. Summing over $j$ and the four sides gives $O(a b (a + b))$ marked cells, which is $O(n^3)$ for $n$ vertices.

**What is not claimed.** The features are not a minimum set and may overlap. The model is the plane, the bounding box as stock, and tool motion along the four axes only. In 3D, with other stock or other tool directions, Lemmas 3 and 5 can fail, as the page's pitfalls say. The 3D method of Vandenbrande and Requicha has heuristic hint patterns and tests, and no such theorem is claimed for it here.
