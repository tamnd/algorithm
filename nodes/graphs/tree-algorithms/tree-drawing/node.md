---
tag: FAQ0ZT
kind: problem
slug: tree-drawing
name: Tree drawing
aliases:
- Drawing trees
area: graphs/tree-algorithms
level: core
summary: Placing the nodes of a tree in the plane so that hierarchy is clear, with compact width and no crossing edges.
prereqs: [rooted-tree, graph-drawing]
see_also: [reingold-tilford-layout, graph-drawing, planar-straight-line-drawing, force-directed-layout, tree-center, dendrogram, np-hard, preorder-traversal]
sources:
  - book: isbn:9780133016154
    title: Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999
    locator: Chapter 3 (Divide and conquer), layered drawings of rooted trees, radial drawings, HV drawings and upward drawings of binary trees, with their area bounds
  - paper: Edward M. Reingold and John S. Tilford, Tidier drawings of trees, IEEE Transactions on Software Engineering SE-7(2), 223 to 228 (1981)
    locator: the aesthetic rules for layered drawings of trees and the linear-time contour method
  - paper: Kenneth J. Supowit and Edward M. Reingold, The complexity of drawing trees nicely, Acta Informatica 18, 377 to 392 (1983)
    locator: the narrowest drawing under the aesthetic rules, NP-hard on an integer grid and solvable by linear programming with real coordinates
---

Tree drawing is the problem of placing the vertices of a [tree](/tree/) at points of the plane, and its edges as curves, so that the drawing is easy to read: no edges cross, the hierarchy of a [rooted tree](/rooted-tree/) is visible, and the drawing is small. Every tree has a planar straight-line drawing, so the question is never whether a drawing exists but which rules it obeys and how much area it needs. The most used version, the layered drawing of an ordered rooted tree, is solved in $\Theta(n)$ time by the [Reingold-Tilford layout](/reingold-tilford-layout/); finding the narrowest such drawing on an integer grid is [NP-hard](/np-hard/).

## In plain words

You have a tree, such as a family tree or the folders on a disk, and you want to draw it on a page. Each item becomes a dot, and each link becomes a line. A good picture puts the top item at the top and each generation on its own row. Lines do not cross. Children stay in their order. A parent sits above the middle of its children. Two dots on a row are not too close. The same shape is drawn the same way each time it occurs. And the picture is not wider than it needs to be.

Some of these wishes can be met fast, for every tree. Making the picture as narrow as possible while keeping all the others turns out to be very hard. Other styles, such as rings around a centre, trade some wishes for a smaller or rounder picture.

## Definition

**Input.** A tree with the vertices $0, \ldots, n-1$, $n \ge 1$. In the main version it is rooted, not weighted, and ordered: the children of each vertex are given as a list from left to right, as on the [rooted tree](/rooted-tree/) page. The numbers name the vertices and have no effect on the drawing. A free tree is first rooted, often at its [centre](/tree-center/).

**Output.** A drawing $\Gamma$: a point $\Gamma(v)$ for each vertex, and for each edge a curve between the points of its ends. A *straight-line* drawing uses segments; a *grid* drawing puts the points at integer coordinates.

**Constraints.** A drawing can be asked to be:

- *planar*: no two edges meet except at a shared end;
- *upward*: each child is strictly below its parent;
- *layered*: the $y$ value of each vertex is minus its depth;
- *order-preserving*: the children of each vertex appear from left to right in their given order;
- *separated*: two vertices on one horizontal line are at least $\delta > 0$ apart.

**Aesthetic rules of the tidy layered drawing.** On top of layered, planar, order-preserving and separated, the parent is centred over its children, and isomorphic subtrees are drawn the same up to a shift.

**Goal.** Among the drawings that meet the constraints, find one of small *area* (the area of the bounding box of a grid drawing), *width* or *height*, or one with a good *aspect ratio*.

## Variants

- **Tidy layered drawing.** The version above with the greedy rule that each subtree sits as far left as it can. The [Reingold-Tilford layout](/reingold-tilford-layout/) solves it in $\Theta(n)$ time.
- **Least width.** The same rules, with the width as small as possible. With real coordinates this is a linear program; with integer coordinates it is NP-hard.
- **Radial drawings.** The root is at the centre, and the vertices of depth $i$ are on a circle of radius $i$, each subtree in a sector. This suits free trees and wide trees.
- **HV drawings.** For binary trees, each child is directly to the right of its parent or directly below it, so all edges are horizontal or vertical.
- **Upward grid drawings of small area.** Planar, upward, straight-line grid drawings of binary trees, with the area as small as possible, and possibly without the layered rule or the order rule.
- **H-tree.** A complete binary tree drawn on a grid with edges along grid lines, in the shape of nested letters H, with area linear in $n$. It is used in chip layout.
- **Dendrograms.** Leaves on one line, inner vertices at a height given by a weight such as a merge distance, as in a [dendrogram](/dendrogram/) of a clustering.
- **Space-filling drawings.** Each vertex becomes a region nested in the region of its parent, as in a treemap, with no edges drawn.

## Examples

Take the tree rooted at $0$ with $p = [-1, 0, 0, 1, 1, 2, 4, 4]$ and children in increasing order. The Reingold-Tilford layout with $\delta = 2$, shifted so that the smallest $x$ is $0$, gives the following positions.

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $x$ | 5/2 | 1 | 4 | 0 | 2 | 4 | 1 | 3 |
| depth | 0 | 1 | 1 | 2 | 2 | 2 | 3 | 3 |

The drawing is $4$ wide and $3$ high. Level 2 holds three vertices, so a layered drawing with $\delta = 2$ needs width at least $4$, and this one has the least width.

The small cases:

- **Single vertex.** A point; width and height $0$.
- **Path** $0, \ldots, n-1$ rooted at $0$. The layered drawing is a vertical line of height $n - 1$ and width $0$. A drawing that is not layered can fold the path into a square of area $O(n)$.
- **Star** with centre $0$ and $n - 1$ leaves. The layered drawing has height $1$ and width $(n - 2)\delta$. A radial drawing puts the leaves on a circle.

## Known algorithms

| algorithm | drawing | time | size |
|---|---|---|---|
| [Reingold-Tilford layout](/reingold-tilford-layout/) | tidy layered, binary trees and, with extensions, any ordered tree | $\Theta(n)$ | height $h$; width not always least |
| Walker's method with the linear-time fix of Buchheim, Jünger and Leipert | tidy layered, any degree, small subtrees spread evenly | $\Theta(n)$ | as above |
| Level-by-level placement (Wetherell and Shannon) | layered, each level packed from the left | $\Theta(n)$ | narrow, but a subtree can change shape |
| Linear programming over the tidy constraints | layered, least width with real coordinates | polynomial | least width |
| Radial layout from [subtree sizes](/subtree-sizes/) or leaf counts | radial | $\Theta(n)$ | each subtree in a sector |
| [Force-directed layout](/force-directed-layout/) | free placement | many iterations | no guarantee |

## Bounds

- **Existence.** Every tree has a planar straight-line grid drawing, and the layered drawing of the [Reingold-Tilford layout](/reingold-tilford-layout/) is one. So the decision question is trivial; only the size is a question.
- **Layered size.** A layered drawing has height equal to the height $h$ of the tree, and width at least $(w - 1)\delta$, where $w$ is the largest number of vertices on one level. For a complete binary tree with $n$ vertices this gives area $\Theta(n \log n)$, while the H-tree, which is not layered, needs only $\Theta(n)$.
- **Least width.** Under the tidy rules, the narrowest drawing with real coordinates is the solution of a linear program, so it takes polynomial time. With integer coordinates it is NP-hard (Supowit and Reingold).
- **Time.** Each drawing must give a point to each vertex, so $\Omega(n)$ time, and the tidy layered drawing takes $\Theta(n)$.

## Reductions

- **Free trees to rooted trees.** Rooting a free tree at a vertex of its [centre](/tree-center/) gives the rooted tree of least height, and so the layered or radial drawing of least height.
- **Tidy drawing to contours.** The tidy layered drawing of a vertex depends only on the leftmost and rightmost positions on each level of its child subtrees, so the problem reduces to merging these contours bottom-up.
- **Least width to linear programming.** The tidy rules are linear equations and inequalities in the $x$ values, and the width is a linear objective, so the real version is a [linear program](/linear-programming-problem/).
- **Tree drawing as graph drawing.** A tree is a planar graph, so the general methods of [graph drawing](/graph-drawing/) and [planar straight-line drawing](/planar-straight-line-drawing/) apply, but they ignore the hierarchy.

## Applications

- **Software.** Syntax trees in compilers, call trees in profilers, folder trees in file browsers, class hierarchies.
- **Data and decisions.** Decision trees, game trees, search trees in teaching, organization charts.
- **Biology.** Phylogenetic trees and family trees, often as [dendrograms](/dendrogram/) or radial drawings.
- **Hardware.** H-tree layouts of clock networks and of binary tree circuits on chips.

## References
