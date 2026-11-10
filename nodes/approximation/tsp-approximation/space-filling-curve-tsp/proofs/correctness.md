---
title: The Hilbert curve tour costs at most (9√2⌈lg n⌉ + √2) OPT
proves: [correctness]
status: full
---

The input is a set $P$ of $n \ge 2$ points in the plane with the Euclidean distance. Scale and move the points so that their bounding square $Q$ is $[0, 1]^2$: the width or the height of $P$ is 1. (If all points are equal, ALG $=$ OPT $= 0$.) The grid has $2^r \times 2^r$ cells with $2^r \ge n$. For $0 \le j \le r$, a *level-$j$ cell* is one of the $4^j$ squares of side $2^{-j}$ in the dyadic subdivision of $Q$. The tour visits the points in the order of the Hilbert positions of their grid cells, and it closes with the edge from the last point to the first. Platzman and Bartholdi (1989) proved an $O(\log n)$ bound for the Sierpinski curve. The proof below is a full proof of the same order of bound for the Hilbert curve, with an explicit constant. The constant is not the best one.

**Fact 1 (the curve is nested).** The Hilbert curve of order $r$ visits the cells of each level-$j$ cell at consecutive positions.

*Proof.* The curve of order $r$ is four curves of order $r - 1$, one in each quadrant, one after the other, each turned or mirrored. By induction on $r$, the cells of each quadrant have consecutive positions, and in each quadrant the cells of each smaller dyadic square have consecutive positions. $\square$

So the points of each level-$j$ cell form one block of consecutive points of the tour path (the tour without its closing edge). Inside a level-$j$ cell, the points of its four children form sub-blocks, one after the other.

For two consecutive points $p, q$ of the path, let $k(p, q)$ be the largest $j \le r$ such that $p$ and $q$ lie in one level-$j$ cell. Both points lie in that cell, so

$$d(p, q) \le \sqrt{2} \cdot 2^{-k(p, q)}. \tag{1}$$

Let $m_j$ be the number of level-$j$ cells that hold a point of $P$.

**Lemma 2 (few edges at each level).** For $0 \le k < r$, at most $m_{k+1} - 1$ path edges have $k(p, q) = k$.

*Proof.* Such an edge joins two points in one level-$k$ cell $C$ and in two different children of $C$. By Fact 1, inside the block of $C$ the points of each child are one sub-block. So the edges of this kind inside $C$ are the steps from one nonempty sub-block to the next, and there are (the number of nonempty children of $C$) minus 1 of them. Add over all nonempty level-$k$ cells: the count is $m_{k+1} - m_k \le m_{k+1} - 1$. $\square$

**Lemma 3 (a lower bound from separated cells).** Let $m = m_{k+1}$ and $s = 2^{-(k + 1)}$, for some $0 \le k < r$. Then $(m - 1) \cdot 2 \sqrt{2} \cdot s \le 9 \sqrt{2} \cdot \text{OPT}$.

*Proof.* First, $\text{OPT} \ge 2$, because a tour goes from the leftmost point to the rightmost point and back (or from the lowest to the highest), and the width or the height is 1.

Give the level-$(k+1)$ cell in column $a$ and row $b$ the color $(a \bmod 3, b \bmod 3)$. There are 9 colors, so some color has $t \ge \lceil m / 9 \rceil$ nonempty cells. Take one point from each of these cells. Two different cells of one color differ by at least 3 in the column or in the row, so two full cells lie between them, and the two points are at distance at least $2s$.

If $t \ge 2$, the shortcut of an optimal tour to the $t$ chosen points has $t$ edges of length at least $2s$, so $\text{OPT} \ge 2 s t \ge 2 s m / 9$. Then $(m - 1) \cdot 2\sqrt{2} \cdot s < 9 \sqrt{2} \cdot 2 s m / 9 \le 9\sqrt{2} \cdot \text{OPT}$.

If $t = 1$, then $m \le 9$, and $s \le 1/2$ because $k \ge 0$. So $(m - 1) \cdot 2 \sqrt{2} \cdot s \le 8 \sqrt{2} \le 4 \sqrt{2} \cdot \text{OPT}$. $\square$

**Theorem.** For $n \ge 2$ points and a grid with $2^r \ge n$, the Hilbert curve tour satisfies

$$\text{ALG} \le \left(9\sqrt{2} \, \lceil \lg n \rceil + \sqrt{2}\right) \cdot \text{OPT}.$$

*Proof.* Let $K = \lceil \lg n \rceil \le r$. Split the tour edges into three groups.

1. *Shallow edges*, with $k(p, q) = k < K$. By (1) and Lemma 2, the edges with $k(p, q) = k$ cost at most $(m_{k+1} - 1) \cdot \sqrt{2} \cdot 2^{-k} = (m_{k+1} - 1) \cdot 2\sqrt{2} \cdot 2^{-(k+1)}$, which is at most $9\sqrt{2} \cdot \text{OPT}$ by Lemma 3. There are $K$ such levels, so the group costs at most $9 \sqrt{2} \, K \cdot \text{OPT}$.
2. *Deep edges*, with $k(p, q) \ge K$. There are at most $n - 1$ of them, and by (1) each costs at most $\sqrt{2} \cdot 2^{-K} \le \sqrt{2} / n$. The group costs less than $\sqrt{2}$.
3. *The closing edge.* Both ends are in $Q$, so it costs at most $\sqrt{2}$.

The last two groups cost less than $2 \sqrt{2} \le \sqrt{2} \cdot \text{OPT}$, because $\text{OPT} \ge 2$. Add the three groups. $\blacksquare$

**Remarks.**

- The proof uses only Fact 1 and the bound (1). So it holds for each order of the cells that visits each dyadic square at consecutive positions, also for the Z-order (Morton) curve. The Z-order curve jumps between cells, but the bound (1) needs only that both points lie in one cell.
- The bound needs $2^r \ge n$. With a coarse grid, many points can share a finest cell, the deep edges are not short, and the second group can be large.
- The order $\log n$ is the right order for the worst case: Bertsimas and Grigni (1989) gave point sets on which the Sierpinski curve tour is $\Omega(\log n)$ times OPT. That result is quoted, not proved, here. The test file measures a row family for the Hilbert curve whose ratio grows by about 0.23 for each doubling of $n$, which is a measured trend and not a proof.
