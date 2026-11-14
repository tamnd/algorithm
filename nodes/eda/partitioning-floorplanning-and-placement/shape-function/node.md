---
tag: CXGS6Q
kind: definition
slug: shape-function
name: Shape function
aliases:
- shape curve
area: eda/partitioning-floorplanning-and-placement
level: core
summary: The staircase curve of allowed width and height pairs of a block, which for a slicing tree is combined bottom up by adding widths or heights.
prereqs: [slicing-floorplan, pareto-front]
see_also: [stockmeyer-floorplan-sizing, normalized-polish-expression, wong-liu-floorplanning, floorplanning, pareto-dominance, convex-function, geometric-programming]
sources:
  - paper: doi:10.1109/DAC.1982.1585510
    title: Ralph H. J. M. Otten, Automatic floorplan design, Proceedings of the 19th Design Automation Conference, 261 to 267, 1982
    locator: shapes of blocks and of slicing structures
  - paper: "Ralph H. J. M. Otten, Efficient floorplan optimization, Proceedings of the IEEE International Conference on Computer Design, 1983"
    locator: shape functions and their addition at the cuts of a slicing tree
  - paper: doi:10.1016/S0019-9958(83)80038-2
    title: Larry Stockmeyer, Optimal orientations of cells in slicing floorplan designs, Information and Control 57(2-3), 91 to 101, 1983
    locator: the merge of lists of non-dominated shapes and the bound on their lengths
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (floorplan sizing with shape functions; general locator)
---

A shape function tells, for each width, the least height of a rectangle that holds a block, so it describes all the shapes that the block can take. A hard block of fixed size that can turn by a quarter turn has a staircase with two steps. A soft block of fixed area has a curve $h = A / w$ between two limits of the aspect ratio. Shape functions are the tool that makes [slicing floorplans](/slicing-floorplan/) easy to size: at a horizontal cut the shape functions of the two parts add up, and at a vertical cut their inverse functions add up. So a pass from the leaves of the slicing tree to the root gives the shape function of the whole chip, and its lowest point of $w \cdot h$ is the least area. The corners of a staircase are the [Pareto front](/pareto-front/) of the shapes, and [Stockmeyer's algorithm](/stockmeyer-floorplan-sizing/) is this pass on lists of corners.

## Definition

**Shape function of a block.** Let $S \subseteq \mathbb{R}_{>0}^2$ be the set of shapes $(w, h)$ that a block can take: each shape is a rectangle of width $w$ and height $h$ that the block fills. A room of width $W$ and height $H$ holds the block if some $(w, h) \in S$ has $w \le W$ and $h \le H$. The shape function of the block is

$$
f(W) = \inf \{\, h : (w, h) \in S,\ w \le W \,\},
$$

with $f(W) = \infty$ when no shape is narrow enough. The function $f$ is nonincreasing, and the set of rooms that hold the block is the region $\{(W, H) : H \ge f(W)\}$ above its graph, which is closed upward and to the right. The *inverse* shape function $g(H) = \inf \{\, w : (w, h) \in S,\ h \le H \,\}$ describes the same region from the other side.

**Staircase and corners.** If $S$ is finite, $f$ is a step function. Its corners are the shapes in $S$ that no other shape in $S$ dominates, that is, the points $(w, h)$ with no other $(w', h')$ with $w' \le w$ and $h' \le h$. Sorted by width, the corners have strictly increasing widths and strictly decreasing heights, and the list of corners stores $f$ exactly.

**Common blocks.**

- A hard block $a \times b$ with $a < b$ that can turn has the two corners $(a, b)$ and $(b, a)$. A square block, or a block that cannot turn, has one corner.
- A soft block of area $A$ whose aspect ratio $h / w$ must lie in $[r_1, r_2]$ has the widths $w$ from $w_1 = \sqrt{A / r_2}$ to $w_2 = \sqrt{A / r_1}$. Its shape function is $\infty$ for $W < w_1$, equal to $A / W$ for $w_1 \le W \le w_2$, and equal to $A / w_2$ for $W > w_2$, since a wider room can hold the widest shape. This function is [convex](/convex-function/) on $[w_1, \infty)$: the slope $-A / W^2$ increases with $W$, and it then jumps up to $0$.

**Combination at a cut.** Let a node of a slicing tree have the children $a$ and $b$ with shape functions $f_a$ and $f_b$ and inverse functions $g_a$ and $g_b$.

- At an $H$ node, $b$ is above $a$. A room of width $W$ holds both exactly when its height is at least $f_a(W) + f_b(W)$, so $f = f_a + f_b$.
- At a $V$ node, $b$ is to the right of $a$. In the same way, a room of height $H$ holds both exactly when its width is at least $g_a(H) + g_b(H)$, so $g = g_a + g_b$.

For the $H$ node, put $a$ at the bottom in its best shape for width $W$ and $b$ on top of it in its best shape for width $W$: the height is $f_a(W) + f_b(W)$. Conversely, in any room of width $W$ the two parts have widths at most $W$, so their heights are at least $f_a(W)$ and $f_b(W)$ because $f_a$ and $f_b$ are nonincreasing. The $V$ case is the same with the two axes swapped.

**Number of corners.** If $f_a$ has $k_1$ corners and $f_b$ has $k_2$ corners, then $f_a + f_b$ has at most $k_1 + k_2 - 1$ corners. The sum changes only at a width where $f_a$ or $f_b$ changes, so each corner of the sum has the width of a corner of $f_a$ or of $f_b$. The sum is finite only from $w_0 = \max(\text{first width of } f_a, \text{first width of } f_b)$ on. If the two first widths differ, the smaller one is below $w_0$ and gives no corner. If they are equal, they give the same width. In both cases at most $k_1 + k_2 - 1$ widths remain. The same holds at a $V$ node with heights in place of widths. By induction, a node with $\ell$ hard blocks below it, each with two corners, has at most $2 \ell - (\ell - 1) = \ell + 1$ corners, and the merge of two sorted corner lists takes time linear in their lengths.

**Convexity is kept.** For soft blocks the shape functions are convex. A sum of convex functions is convex, so an $H$ node keeps convexity. The region above the graph of a convex nonincreasing function is a convex set, so its inverse function is convex too, and a $V$ node, which adds the inverse functions, keeps convexity as well. So a slicing tree of soft blocks has a convex shape function, and the sizing of soft blocks can be done with convex methods such as [geometric programming](/geometric-programming/).

## Examples and non-examples

Take three hard blocks that can turn: $A$ is $2 \times 4$, with corners $(2, 4)$ and $(4, 2)$. $B$ is the square $3 \times 3$, with the one corner $(3, 3)$. $C$ is $1 \times 5$, with corners $(1, 5)$ and $(5, 1)$.

**Side by side.** $A\,B\,V$ adds widths at each height. For $H \ge 4$ the least widths are $2$ and $3$, which gives the corner $(5, 4)$. For $3 \le H < 4$ the block $A$ needs width $4$, which gives $(7, 3)$. Below height $3$ the square does not fit. So the corners are $(5, 4)$ and $(7, 3)$.

**Stacked.** $A\,B\,H$ adds heights at each width. At $W = 3$ the heights are $4$ and $3$, which gives $(3, 7)$, and at $W = 4$ they are $2$ and $3$, which gives $(4, 5)$. So the corners are $(3, 7)$ and $(4, 5)$.

**A whole tree.** The four trees with $A$ and $B$ below and $C$ added at the root give these corner lists:

| expression | corners $(w, h)$ | least area |
|---|---|---|
| $A\,B\,V\,C\,H$ | $(5, 5)$, $(7, 4)$ | $25$ |
| $A\,B\,V\,C\,V$ | $(6, 5)$, $(10, 4)$, $(12, 3)$ | $30$ |
| $A\,B\,H\,C\,V$ | $(4, 7)$, $(5, 5)$ | $25$ |
| $A\,B\,H\,C\,H$ | $(3, 12)$, $(4, 10)$, $(5, 6)$ | $30$ |

None of them is the best slicing floorplan. The expression $A\,C\,H\,B\,V$ first stacks $C$ on $A$: at widths $2$, $4$ and $5$ the heights are $4 + 5 = 9$, $2 + 5 = 7$ and $2 + 1 = 3$, so the corners are $(2, 9)$, $(4, 7)$ and $(5, 3)$, which is $2 + 2 - 1 = 3$ corners, the bound. Then the square goes to the right, and each width grows by $3$: the corners are $(5, 9)$, $(7, 7)$ and $(8, 3)$. The corner $(8, 3)$ has area $24$, the least over all slicing trees of these three blocks. The blocks have area $8 + 9 + 5 = 22$, so the best slicing floorplan leaves $2$ units empty. A node must keep all its corners, not only the one of least area: in $A\,B\,V\,C\,H$ the root uses both corners of $A\,B\,V$, and the corner $(7, 3)$ of area $21$, which is larger than the $20$ of $(5, 4)$, gives the root corner $(7, 4)$ with the least height.

**Non-example: a dominated shape.** A block with the allowed shapes $(3, 3)$ and $(4, 4)$ has the one corner $(3, 3)$. The shape $(4, 4)$ is not on the staircase, because each room that holds it also holds $(3, 3)$.

**Non-example: a floorplan without a cut.** In the pinwheel of five rooms no segment runs from one side of the chip to the other. The least height at width $W$ is then not a sum of the shape functions of two parts, and the combination rules do not apply. For floorplans that are not slicing, the choice of the orientations of the blocks is NP-complete (Stockmeyer 1983).

## Related definitions

- **[Pareto front](/pareto-front/) and [Pareto dominance](/pareto-dominance/).** The corners of a staircase are the Pareto front of the shapes under the order of both coordinates.
- **[Stockmeyer floorplan sizing](/stockmeyer-floorplan-sizing/).** The merge of corner lists up a slicing tree with the time bound $O(n d)$ for depth $d$.
- **[Normalized Polish expression](/normalized-polish-expression/) and [Wong-Liu floorplanning](/wong-liu-floorplanning/).** The annealing search over slicing trees that evaluates each tree by its shape function.
- **[Slicing floorplan](/slicing-floorplan/).** The structure on which the combination rules hold.
- **[Floorplanning](/floorplanning/).** The design problem where the shapes of the blocks are chosen.

## References
