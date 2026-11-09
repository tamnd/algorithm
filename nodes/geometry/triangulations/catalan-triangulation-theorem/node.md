---
tag: ARZR6M
kind: theorem
slug: catalan-triangulation-theorem
name: Catalan count of convex polygon triangulations
aliases:
- Catalan triangulation count
area: geometry/triangulations
level: intro
summary: A convex n-gon has exactly the Catalan number C(n-2) triangulations.
prereqs: [catalan-numbers, convex-polygon, polygon-triangulation]
see_also: [number-of-triangulations, triangulation-dual-tree, flip-graph, polygon-triangulation-dp, matrix-chain-multiplication, binary-tree]
sources:
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Exercise 6.19, item (a) (triangulations of a convex (n+2)-gon) and the notes on the history of Catalan numbers
  - book: isbn:9781107427747
    title: Richard P. Stanley, Catalan Numbers, Cambridge University Press, 2015
    locator: Chapter 2, item 1 (triangulations of a convex polygon) and Appendix B (the history of the Catalan numbers, by Igor Pak)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Section 7.5 (the generating function of the Catalan numbers)
---

A convex polygon with $n$ corners can be cut into triangles by non-crossing diagonals in exactly $C_{n-2}$ ways, where $C_m = \frac{1}{m+1}\binom{2m}{m}$ is the $m$-th [Catalan number](/catalan-numbers/). A square has 2 triangulations, a pentagon 5, a hexagon 14. Euler counted these in 1751 and guessed the formula; it was the first appearance of the Catalan numbers. The count grows like $4^n$, so brute-force search over triangulations is hopeless beyond small $n$, and optimal triangulations are found by [dynamic programming](/polygon-triangulation-dp/) instead.

## Statement

Let $P$ be a convex polygon with $n \ge 3$ vertices, no three of them collinear. Let $T_n$ be the number of [triangulations](/polygon-triangulation/) of $P$ by diagonals. Then
$$T_n = C_{n-2} = \frac{1}{n-1}\binom{2n-4}{n-2}.$$

The first values are:

| $n$ | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| $T_n$ | 1 | 2 | 5 | 14 | 42 | 132 | 429 | 1430 |

## In plain words

Draw a convex shape with some number of corners, such as a hexagon. Count the ways to cut it into triangles with straight cuts between corners that do not cross. For three corners there is one way, for four there are two, for five there are five, for six there are fourteen. These numbers form a famous sequence that also counts ways to put brackets in a product and shapes of binary trees. Each new corner multiplies the count by close to four.

## Proof

Number the vertices $v_1, \ldots, v_n$ around $P$. In a convex polygon with no three vertices collinear, every segment between two non-adjacent vertices is a diagonal, and two diagonals $v_a v_b$ and $v_c v_d$ cross exactly when their end points alternate around the polygon. So $T_n$ depends only on $n$.

**Recurrence.** Set $T_2 = 1$ (a single edge, with one empty triangulation). In any triangulation, the polygon edge $v_1 v_n$ is a side of exactly one triangle, $v_1 v_k v_n$ for some $2 \le k \le n - 1$. That triangle splits $P$ into the convex polygons $v_1 v_2 \ldots v_k$ with $k$ vertices and $v_k v_{k+1} \ldots v_n$ with $n - k + 1$ vertices (a side with only 2 vertices is just the edge $v_1 v_2$ or $v_{n-1} v_n$). The rest of the triangulation is a triangulation of each part, chosen independently. Conversely, every choice of $k$ and of triangulations of the two parts gives a triangulation of $P$, and different choices give different triangulations (they differ in the triangle on $v_1 v_n$ or in one of the parts). So
$$T_n = \sum_{k=2}^{n-1} T_k \, T_{n-k+1} \qquad (n \ge 3).$$
With $a_m = T_{m+2}$ this reads $a_0 = 1$ and $a_m = \sum_{i=0}^{m-1} a_i \, a_{m-1-i}$ for $m \ge 1$, the Catalan recurrence. For example, $T_6 = T_2 T_5 + T_3 T_4 + T_4 T_3 + T_5 T_2 = 5 + 2 + 2 + 5 = 14$.

**Closed form.** Let $A(x) = \sum_{m \ge 0} a_m x^m$. The recurrence says that the coefficient of $x^m$ in $x A(x)^2$ equals $a_m$ for $m \ge 1$, so $A(x) = 1 + x A(x)^2$. Solving the quadratic, $A(x) = \frac{1 - \sqrt{1 - 4x}}{2x}$; the other root has a pole at $x = 0$, while $A(0) = 1$. By the binomial series, $\sqrt{1 - 4x} = 1 - 2\sum_{m \ge 0} \frac{1}{m+1}\binom{2m}{m} x^{m+1}$, which gives $a_m = \frac{1}{m+1}\binom{2m}{m} = C_m$. The steps are valid as identities of formal power series. With $m = n - 2$, $T_n = C_{n-2} = \frac{1}{n-1}\binom{2n-4}{n-2}$. $\blacksquare$

A bijective proof: root the [dual tree](/triangulation-dual-tree/) at the triangle on $v_1 v_n$. A triangle $v_a v_c v_b$ with $a < c < b$, whose side $v_a v_b$ faces the root, gets a left child across $v_a v_c$ and a right child across $v_c v_b$, when those sides are diagonals. This is a bijection between triangulations of $P$ and binary trees with $n - 2$ nodes, which are counted by $C_{n-2}$.

## Consequences

- **Growth.** By Stirling's formula, $C_m \sim \frac{4^m}{\sqrt{\pi}\, m^{3/2}}$, so $T_n = \Theta(4^n n^{-3/2})$. Enumerating all triangulations is feasible only for small $n$; optimization over all of them needs the $O(n^3)$ [interval dynamic program](/polygon-triangulation-dp/), which is the same recurrence with $\min$ in place of the sum.
- **Simple polygons have at most $C_{n-2}$ triangulations, with equality only for convex ones.** In a simple polygon, two diagonals whose end points alternate around the boundary must cross (each diagonal separates the polygon, and the other diagonal joins the two sides), and two non-alternating diagonals do not cross. So a triangulation of a simple polygon $P$ is a maximal set of pairwise non-alternating index pairs, which is a triangulation of the convex $n$-gon with the same labels. Distinct triangulations map to distinct ones. Equality needs every index pair to be a diagonal, which holds only when $P$ is strictly convex. The two-eared strip in the [two ears theorem](/two-ears-theorem/) has only $2^{n/2 - 2}$ triangulations.
- **Point sets.** Convex position is neither the maximum nor the minimum over $n$ points in general position: some sets have about $8.65^n$ triangulations and the double circle has about $\sqrt{12}^{\,n} \approx 3.46^n$, both up to polynomial factors. See [number of triangulations](/number-of-triangulations/).
- **Associahedron.** The $C_{n-2}$ triangulations are the vertices of the $(n-3)$-dimensional associahedron, whose edges are [flips](/edge-flip/). This [flip graph](/flip-graph/) has diameter $2n - 10$ for $n \ge 13$ ([flip graph diameter theorem](/flip-graph-diameter-theorem/)).
- **Other Catalan families.** The same recurrence counts parenthesizations of a product of $n - 1$ factors (the orders for [matrix chain multiplication](/matrix-chain-multiplication/)), binary trees with $n - 2$ nodes, and Dyck paths of length $2(n - 2)$.

## Tightness

The count is exact. The hypothesis that no three vertices are collinear is needed: if a vertex has an angle of exactly $\pi$, the segment between its neighbors runs along the boundary and is not a diagonal, and the count drops. For the four points $(0,0), (1,0), (2,0), (1,1)$, which form a convex region with a flat vertex at $(1,0)$, there is exactly one triangulation, not $C_2 = 2$. Convexity is needed too, by the second consequence above.

## History

Leonhard Euler posed the problem of counting triangulations of a convex polygon in a 1751 letter to Christian Goldbach and gave the formula from the values for small $n$, without a complete proof. Johann Andreas von Segner found the recurrence in a paper written in 1758. Gabriel Lamé gave a short proof of the closed form in 1838, and Eugène Catalan studied the numbers in the same year, in connection with parenthesizations; they were later named after him. Stanley's book lists more than two hundred families counted by the same numbers.

## References
