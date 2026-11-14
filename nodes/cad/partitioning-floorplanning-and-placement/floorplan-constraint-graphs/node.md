---
tag: 3CZSKW
kind: definition
slug: floorplan-constraint-graphs
name: Horizontal and vertical constraint graphs
aliases:
- floorplan constraint graphs
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Two DAGs on the blocks whose edges say one block is left of or below another, so longest paths give the least width and height of a packing.
prereqs: [floorplanning, directed-acyclic-graph, dag-longest-path]
see_also: [sequence-pair, b-star-tree-floorplan, o-tree-floorplan, difference-constraints, mosaic-floorplan, slicing-floorplan, transitive-reduction, critical-path]
sources:
  - paper: doi:10.1109/43.552084
    title: Hiroshi Murata, Kunihiro Fujiyoshi, Shigetoshi Nakatake and Yoji Kajitani, VLSI module placement based on rectangle-packing by the sequence-pair, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(12), 1518 to 1524, 1996
    locator: the horizontal and vertical constraint graphs of a sequence pair and the packing by longest paths in them
  - paper: "Jai-Ming Lin and Yao-Wen Chang, TCG: a transitive closure graph-based representation for non-slicing floorplans, Proceedings of the 38th Design Automation Conference, 764 to 769, 2001"
    locator: the representation by a pair of transitively closed constraint graphs in which each pair of blocks is related in exactly one graph
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 22.2 (single-source shortest paths in directed acyclic graphs, and longest paths by negated weights) and Section 22.4 (difference constraints and shortest paths)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (constraint graphs of floorplans and sequence pairs; general locator)
---

The horizontal and vertical constraint graphs of a set of rectangular blocks are two directed acyclic graphs on the blocks. An edge $a \to b$ in the horizontal graph $G_h$ says that block $a$ must lie to the left of block $b$, and an edge $a \to b$ in the vertical graph $G_v$ says that $a$ must lie below $b$. They are the common decoding step of [floorplanning](/floorplanning/) in chip design: a [sequence pair](/sequence-pair/), a [B*-tree](/b-star-tree-floorplan/) or an [O-tree](/o-tree-floorplan/) fixes the relations, and the [longest paths](/dag-longest-path/) in the two graphs give the least $x$ and $y$ coordinates that obey them. When every pair of blocks is joined by a path in one of the two graphs, the result has no overlap, and its width and height are the lengths of the longest paths through each graph.

## Definition

**Blocks and placements.** There are $n$ blocks $1, \ldots, n$. Block $i$ has a width $w_i > 0$ and a height $h_i > 0$. A placement gives each block a lower-left corner $(x_i, y_i)$, and block $i$ then covers the rectangle $[x_i, x_i + w_i] \times [y_i, y_i + h_i]$. Two blocks overlap when the interiors of their rectangles meet. A placement is a packing when no two blocks overlap. In a placement, $a$ is *left of* $b$ when $x_a + w_a \le x_b$, and $a$ is *below* $b$ when $y_a + h_a \le y_b$. The interiors of two rectangles meet exactly when the interiors of both their $x$-intervals and their $y$-intervals meet, so a placement is a packing if and only if for each pair $\{a, b\}$ at least one of four relations holds: $a$ left of $b$, $b$ left of $a$, $a$ below $b$ or $b$ below $a$.

**Constraint graphs.** A horizontal constraint graph is a weighted directed graph $G_h$ on the vertex set $\{s, 1, \ldots, n, t\}$. Each edge $a \to b$ between two blocks has the weight $w_a$ and means "$a$ is left of $b$". The source $s$ has an edge of weight $0$ to every block, and every block $i$ has an edge of weight $w_i$ to the sink $t$. A vertical constraint graph $G_v$ is the same with the heights $h_a$ as weights and "below" as the meaning. A placement *satisfies* the pair $(G_h, G_v)$ when $x_b \ge x_a + w_a$ for each edge $a \to b$ of $G_h$ between blocks, $y_b \ge y_a + h_a$ for each such edge of $G_v$, and all coordinates are at least $0$. These are [difference constraints](/difference-constraints/). The pair is *complete* when for every two blocks $a \ne b$ there is a directed path from one to the other in $G_h$ or in $G_v$.

**Longest-path placement.** When both graphs are acyclic, let $L_h(v)$ be the length of a longest path from $s$ to $v$ in $G_h$, and $L_v(v)$ the same in $G_v$. The longest-path placement is $x_i = L_h(i)$ and $y_i = L_v(i)$. Its width is $W = L_h(t) = \max_i (x_i + w_i)$ and its height is $H = L_v(t)$. A longest $s$ to $t$ path is a critical path: the blocks on it decide the width or the height.

**Facts.** Each one follows from the definitions in a few lines.

1. *Feasibility.* Some placement satisfies the pair if and only if both graphs are acyclic. If $G_h$ has a cycle $a_1 \to a_2 \to \cdots \to a_k \to a_1$, adding the constraints along it gives $x_{a_1} \ge x_{a_1} + w_{a_1} + \cdots + w_{a_k}$, which is false since the widths are positive. If both graphs are acyclic, the longest-path placement satisfies each edge, because a longest path to $b$ is at least as long as a longest path to $a$ followed by the edge $a \to b$.
2. *Least placement.* Every placement that satisfies the pair has $x_i \ge L_h(i)$ and $y_i \ge L_v(i)$ for each block. Along a longest path $s \to a_1 \to \cdots \to a_k = i$, the constraints give $x_{a_1} \ge 0$ and $x_{a_{j+1}} \ge x_{a_j} + w_{a_j}$, so $x_i$ is at least the length of the path. So the longest-path placement has the least width and the least height, at the same time, among all placements that satisfy the pair.
3. *No overlap.* If the pair is complete and acyclic, the longest-path placement is a packing. A path $a \leadsto b$ in $G_h$ starts with an edge of weight $w_a$, and all other weights are positive, so fact 2 applied to the path gives $x_b \ge x_a + w_a$: $a$ is left of $b$. A path in $G_v$ puts one block below the other in the same way.
4. *Every packing has a pair.* For a packing, put an edge $a \to b$ in $G_h$ whenever $a$ is left of $b$, and in $G_v$ whenever $a$ is below $b$. Both graphs are acyclic, because $x$ (or $y$) grows strictly along each edge. The pair is complete, because each pair of blocks has one of the four relations. The packing satisfies its own pair, so by fact 2 the longest-path placement of the pair is a packing that is no wider and no taller. It is the packing pushed as far left and down as its relations allow. So an optimal packing for area is always the longest-path placement of some complete acyclic pair.
5. *Only reachability counts.* Adding an edge $a \to c$ when a path $a \leadsto c$ already exists does not change any $L_h$ value, because that path is at least $w_a$ long. Removing such an edge does not change them either. So a pair can be replaced by its [transitive reduction](/transitive-reduction/) or by its [transitive closure](/transitive-closure/), and what matters are the two strict partial orders "left of" and "below" that the graphs generate.
6. *Cost.* With $m$ edges, a [topological sort](/topological-sort/) and one pass give all of $L_h$ in $O(n + m)$ time on the word RAM. A complete pair has at least one path for each of the $n(n-1)/2$ pairs of blocks, and when each pair is a direct edge there are $\Theta(n^2)$ edges, so decoding a sequence pair this way costs $O(n^2)$. The weighted [longest common subsequence](/longest-common-subsequence/) method of Tang, Tian and Wong finds the same longest paths in $O(n \log n)$ time without building the graphs.

**Extra constraints.** Design rules often add constraints that are not of the form "left of". A lower bound $x_a \ge c$ is an edge $s \to a$ of weight $c$. An upper bound $x_b - x_a \le d$, for example to keep two blocks close, is an edge $b \to a$ of weight $-d$. Such edges can close cycles. The least solution then exists if and only if no cycle has positive total weight, and the [Bellman-Ford algorithm](/bellman-ford/) finds it, or reports the positive cycle, in $O(n m)$ time. A fixed outline $W^\ast \times H^\ast$ is met if and only if $L_h(t) \le W^\ast$ and $L_v(t) \le H^\ast$.

## Examples and non-examples

**A complete pair.** Take four blocks with sizes $A$: $3 \times 2$, $B$: $2 \times 3$, $C$: $4 \times 2$ and $D$: $4 \times 1$ (width times height). Let $G_h$ have the edges $A \to B$ and $C \to B$, and let $G_v$ have the edges $A \to C$, $C \to D$ and $B \to D$. The six pairs are joined as follows: $AB$ and $CB$ in $G_h$, and $AC$, $CD$, $BD$ and $AD$ (by the path $A \to C \to D$) in $G_v$. So the pair is complete. The longest paths give:

| block | size | $x = L_h$ | $y = L_v$ | rectangle |
|---|---|---|---|---|
| $A$ | $3 \times 2$ | $0$ | $0$ | $[0, 3] \times [0, 2]$ |
| $B$ | $2 \times 3$ | $\max(0 + 3, 0 + 4) = 4$ | $0$ | $[4, 6] \times [0, 3]$ |
| $C$ | $4 \times 2$ | $0$ | $0 + 2 = 2$ | $[0, 4] \times [2, 4]$ |
| $D$ | $4 \times 1$ | $0$ | $\max(2 + 2, 0 + 3) = 4$ | $[0, 4] \times [4, 5]$ |

The width is $L_h(t) = 4 + 2 = 6$, on the critical path $s \to C \to B \to t$, and the height is $L_v(t) = 4 + 1 = 5$, on $s \to A \to C \to D \to t$. The area is $30$, and the blocks cover $6 + 6 + 8 + 4 = 24$ of it. By fact 2, no placement that keeps these five relations is narrower than $6$ or lower than $5$.

**Non-example: a missing relation.** Remove the edge $C \to B$. Now no path joins $B$ and $C$ in either graph, so the pair is not complete. The longest paths give $x_B = 3$, and $B$ becomes $[3, 5] \times [0, 3]$, which overlaps $C = [0, 4] \times [2, 4]$ in the square $[3, 4] \times [2, 3]$. Satisfying the constraints is not enough: without completeness, nothing keeps two blocks apart.

**Non-example: a cycle.** Add the edge $B \to A$ to $G_h$. The cycle $A \to B \to A$ asks for $x_B \ge x_A + 3$ and $x_A \ge x_B + 2$, so no placement satisfies the pair.

**Redundant relations are allowed.** Add the edge $A \to B$ to $G_v$ as well, so that $A$ is both left of and below $B$. The pair is still complete and acyclic, and the placement is still a packing, but now $y_B = 2$, $y_D = \max(4, 2 + 3) = 5$ and the height grows to $6$. A pair that relates a pair of blocks in both graphs is legal, but it can cost area. Representations such as the sequence pair and TCG put each pair of blocks in exactly one graph.

**A slicing structure.** For a [slicing floorplan](/slicing-floorplan/), a vertical cut puts every block of the left part left of every block of the right part, and a horizontal cut does the same for below and above. So the transitive closure of $G_h$ is built from the slicing tree by series composition at the vertical cuts and by disjoint union at the horizontal cuts: it is a series-parallel order.

## Related definitions

- **[Sequence pair](/sequence-pair/).** Two orders of the blocks that define a complete pair in which each pair of blocks has exactly one relation. Its edges go forward in one of the two orders, so both graphs are acyclic.
- **[B*-tree](/b-star-tree-floorplan/) and [O-tree](/o-tree-floorplan/).** Trees that fix the $x$ coordinate of each block from its parent and find each $y$ coordinate with a contour, so they build neither graph.
- **TCG (transitive closure graph).** Lin and Chang (2001) store the pair itself, both graphs transitively closed, with each pair of blocks in exactly one of them. A move edits edges and then repairs the closure.
- **[Difference constraints](/difference-constraints/) and [DAG longest paths](/dag-longest-path/).** The constraint system and the algorithm that solves it; the critical path is the same notion as in [critical path](/critical-path/) scheduling.
- **[Mosaic floorplan](/mosaic-floorplan/).** A dissection of the chip into rooms. Its graphs can be taken on adjacent rooms only, an edge for each pair of rooms that touch across a segment.
- **[Floorplanning](/floorplanning/).** The optimization problem in which these graphs evaluate one candidate.

## References
