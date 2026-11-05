---
tag: NB9NJR
kind: algorithm
slug: reingold-tilford-layout
name: Reingold-Tilford rooted tree layout
aliases:
- Rooted tree layout
area: graphs/tree-algorithms
level: advanced
summary: Lays out a rooted tree by placing subtrees side by side at minimum separation and centering each parent above its children.
solves: [tree-drawing]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [tree-drawing, rooted-tree, preorder-traversal]
see_also: [graph-drawing, planar-straight-line-drawing, force-directed-layout, binary-tree, subtree-sizes, level-order-traversal, tree-traversal, postorder-traversal]
sources:
  - paper: Edward M. Reingold and John S. Tilford, Tidier drawings of trees, IEEE Transactions on Software Engineering SE-7(2), 223 to 228 (1981)
    locator: the aesthetic rules for drawings of binary trees, the contour and thread method, and the proof of linear time
  - paper: Charles Wetherell and Alfred Shannon, Tidy drawings of trees, IEEE Transactions on Software Engineering SE-5(5), 514 to 520 (1979)
    locator: the first aesthetic rules for layered drawings of trees and linear-time methods that place each level from left to right
  - paper: John Q. Walker II, A node-positioning algorithm for general trees, Software, Practice and Experience 20(7), 685 to 705 (1990)
    locator: the extension to trees with any number of children, with the small subtrees between two large ones spread out evenly
  - paper: Christoph Buchheim, Michael Jünger and Sebastian Leipert, Improving Walker's algorithm to run in linear time, Graph Drawing 2002, Lecture Notes in Computer Science 2528, 344 to 353
    locator: the analysis that shows that Walker's method is not linear as published, and a linear-time version
  - book: isbn:9780133016154
    title: Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999
    locator: Chapter 3 (Divide and conquer), the layered drawing of rooted trees by the method of Reingold and Tilford
---

The Reingold-Tilford algorithm draws a rooted, ordered [tree](/rooted-tree/) in layers: each vertex sits on the line of its depth, the children keep their left-to-right order, each parent is centred over its first and last child, and each subtree is pushed as close as possible to its left neighbours without coming nearer than a fixed separation on any level. It works bottom-up and keeps, for each subtree, only its *contours*, the leftmost and rightmost $x$ on each level. Comparing two contours costs the height of the lower part, and that sum is at most $n$, so the whole layout takes $\Theta(n)$ time. It is the standard solution to the layered case of [tree drawing](/tree-drawing/).

## In plain words

Draw a family tree on paper. Each generation goes on its own line, and the children of a person stay in their order. Start from the bottom. A person with no children is a single dot. For a person with children, take the finished drawings of the children, already made, and slide them next to each other from left to right. Push each new drawing to the left until, on some line, it would come too close to the drawings already placed. Then put the parent on the line above, halfway between the first and the last child.

To check "too close" you do not need the whole drawing of a child. Only its left edge on each line matters for the drawings on its left, and only the right edge for those on its right. These edges are the contours. Keeping only the contours makes the method fast.

## The problem

The input is an ordered rooted tree with the vertices $0, \ldots, n-1$, $n \ge 1$, given by its root and the list of the children of each vertex, from left to right, and a separation $\delta > 0$. The tree is not weighted, and the vertex numbers play no role in the drawing. The output is a point $(x(v), y(v))$ for each vertex, with $y(v)$ the depth, such that:

1. the vertices of one level appear in the order of a [preorder](/preorder-traversal/), and two neighbours on a level are at least $\delta$ apart;
2. each parent is at the midpoint of its first and last child;
3. a subtree is drawn the same way, up to a shift, wherever it occurs;
4. given rules 1 to 3, each child subtree sits as far left as it can, relative to the subtrees of its left siblings.

The edges are straight segments from a parent to its children. The root is at $x = 0$; shift the result if non-negative coordinates are needed. The full statement of the problem and its other versions are on the [tree drawing](/tree-drawing/) page.

## The algorithm

For a subtree $T_v$ drawn with $v$ at $x = 0$, let $\mathrm{lc}_v(i)$ and $\mathrm{rc}_v(i)$ be the smallest and the largest $x$ of a vertex at depth $i$ below $v$, for $0 \le i \le h(v)$, where $h(v)$ is the height of $T_v$. The value $\mathrm{rel}(c)$ is the $x$ of a child $c$ minus the $x$ of its parent.

```pseudo id=main
REINGOLD-TILFORD(children, root, δ)
L1  for each v, in an order that puts each vertex after its children do
L2      if v is a leaf then lc_v ← (0);  rc_v ← (0);  continue
L3      F ← the contours of the first child c_1;  off[c_1] ← 0
L4      for each next child c of v, from left to right do
L5          g ← max over the common levels i of ( rc_F(i) − lc_c(i) )
L6          off[c] ← g + δ
L7          F ← F merged with the contours of c shifted by off[c]   ▷ the taller part gives the lower levels
L8      m ← off[c_k] / 2                         ▷ c_k is the last child
L9      for each child c do rel(c) ← off[c] − m
L10     lc_v ← (0) followed by lc_F − m;  rc_v ← (0) followed by rc_F − m
L11 x(root) ← 0;  y(root) ← 0;  for each v in preorder, each child c of v do x(c) ← x(v) + rel(c)
L12     y(c) ← y(v) + 1
L13 return x, y
```

The forest $F$ holds the children placed so far, with $c_1$ at $x = 0$. Line L5 compares only the levels that both $F$ and $T_c$ have. Line L7 builds the contours of the larger forest: on the common levels, the left contour comes from $F$ and the right contour from $c$; below them, both come from the taller part.

**Linear time.** Store each contour as a list with the deepest level first, together with a shift added to all entries. Then shifting a contour costs $O(1)$, adding level $0$ at line L10 is an append, and line L7 keeps the list of the taller part and rewrites only the common levels in it. So lines L5 and L7 cost $O(1 + \min(h_F, h_c))$, where $h_F$ and $h_c$ are the numbers of levels of the two parts. The original paper keeps the contours as paths in the tree with extra pointers, called threads, from the bottom of a short contour to the next vertex of the taller one, which has the same effect.

## Example

Take the tree rooted at $0$ with $p = [-1, 0, 0, 1, 1, 2, 4, 4]$, children in increasing order, and $\delta = 2$. The order of line L1 is the reverse of the preorder $0, 1, 3, 4, 6, 7, 2, 5$.

| $v$ | children | common levels: $\mathrm{rc}_F$ against $\mathrm{lc}_c$ | $\mathrm{off}$ | $m$ | $\mathrm{rel}$ of the children | $\mathrm{lc}_v$ | $\mathrm{rc}_v$ |
|---|---|---|---|---|---|---|---|
| 5, 7, 6, 3 | none | | | | | $(0)$ | $(0)$ |
| 2 | 5 | | $0$ | $0$ | $5{:}\ 0$ | $(0, 0)$ | $(0, 0)$ |
| 4 | 6, 7 | $(0)$ against $(0)$, $g = 0$ | $0, 2$ | $1$ | $6{:}\ -1$, $7{:}\ 1$ | $(0, -1)$ | $(0, 1)$ |
| 1 | 3, 4 | $(0)$ against $(0)$, $g = 0$ | $0, 2$ | $1$ | $3{:}\ -1$, $4{:}\ 1$ | $(0, -1, 0)$ | $(0, 1, 2)$ |
| 0 | 1, 2 | $(0, 1)$ against $(0, 0)$, $g = 1$ | $0, 3$ | $3/2$ | $1{:}\ -3/2$, $2{:}\ 3/2$ | $(0, -3/2, -5/2, -3/2)$ | $(0, 3/2, 3/2, 1/2)$ |

At the root, the subtree of $2$ must clear the subtree of $1$ on level 1 below them, where $4$ is at $1$ and $5$ is at $0$, so $g = 1$ and the two children are $3$ apart. Lines L11 and L12 give $x = (0, -3/2, 3/2, -5/2, -1/2, 3/2, -3/2, 1/2)$ and $y = (0, 1, 1, 2, 2, 2, 3, 3)$. With every $x$ doubled and shifted by $5$:

```
     0
  1     2
3   4   5
  6   7
```

The vertices $3, 4, 5$ on level 2 are exactly $\delta$ apart, and $2$ sits straight over its only child $5$.

The small cases: a single vertex is drawn at $(0, 0)$. A path $0, 1, \ldots, n-1$ has $x = 0$ for every vertex, and the loop of line L1 does no merge, so a path of $10^5$ vertices costs $\Theta(n)$ with no recursion. A star with $k = n - 1$ leaves puts them at $-(k-1)\delta/2, \ldots, (k-1)\delta/2$, with the centre over the middle.

## Correctness

By induction over the order of line L1, after $v$ is handled, $\mathrm{lc}_v$ and $\mathrm{rc}_v$ are the true contours of $T_v$ drawn by the $\mathrm{rel}$ values. When $c$ is added to $F$, the two drawings can only collide on a common level, and on level $i$ the closest pair is the rightmost vertex of $F$ and the leftmost vertex of $T_c$. So line L5 and line L6 give the least shift that keeps every pair on every level at least $\delta$ apart, and line L7 gives the contours of the union. Line L8 centres $v$, and line L10 adds level $0$. Two neighbours on one level are then at least $\delta$ apart, the left-to-right order is the preorder, and the edges do not cross. The full proof is below.

## Complexity

The time is counted in arithmetic operations on coordinates, in the [word RAM](/word-ram/) model.

- Lines L1 to L4, L8 to L10 and the loop of lines L11 and L12 do $O(1)$ work per vertex or per child, so $O(n)$ in all.
- A merge at lines L5 to L7 costs $O(1 + \min(h_F, h_c))$. On each of the $\min(h_F, h_c)$ common levels, the rightmost vertex of $F$ stops being the rightmost vertex of its level, since $T_c$ lies to its right, and it never becomes rightmost again in a larger subtree. So each vertex pays for at most one level of one merge, and all merges cost $O(n)$.

So the time is $\Theta(n)$ and the extra space is $\Theta(n)$ for the contours and the offsets. With $\delta$ an integer, the coordinates are fractions with a power of 2 in the denominator. The Python version keeps them exact with fractions; a floating-point version, or one that rounds each $m$, does $O(1)$ work per operation.

## Properties

- **Layered and planar.** The $y$ value is the depth, every edge goes down one level, and no two edges cross, because the order on each level is the preorder.
- **Same subtree, same drawing.** The drawing of $T_v$ depends only on $T_v$, so isomorphic ordered subtrees are drawn the same up to a shift.
- **Mirror.** For binary trees, the drawing of the mirror tree is the mirror of the drawing. For trees with three or more children, this fails: small subtrees between two large ones are packed against the left one.
- **Not of least width.** Each subtree is packed in a greedy way. A narrower drawing that obeys rules 1 to 3 can exist, and finding the narrowest one on an integer grid is NP-hard, as stated on the [tree drawing](/tree-drawing/) page.
- **Deterministic and not recursive.** The order of line L1 and the preorder of line L11 come from one explicit stack.

## Variants and improvements

- **Binary trees and threads.** The original method is for [binary trees](/binary-tree/), and it keeps the contours in the tree by threads.
- **Walker's method.** For trees of any degree, Walker spreads the small subtrees between two large ones evenly, which restores the mirror property. As published it takes more than linear time in some cases; Buchheim, Jünger and Leipert gave a linear-time version.
- **Node sizes.** Vertices with boxes of different widths only change the contour values, so the same method draws trees of labels or boxes.
- **Other directions.** Swapping $x$ and $y$ draws the tree from left to right, as in file browsers and outline views.
- **Radial and HV drawings.** Other layouts put the levels on circles, or use only horizontal and vertical edges. They are listed on the [tree drawing](/tree-drawing/) page.

## When to use it

Use it to draw a rooted ordered tree in the familiar top-down way: syntax trees, decision trees, family trees, search trees in teaching, call trees. It needs only the tree and gives a drawing in linear time that is stable, since a subtree keeps its shape. For trees of high degree with very uneven subtrees, Walker's spreading looks better. For free trees with no root, or when the depth is not important, a [force-directed layout](/force-directed-layout/) or a radial layout can fit better.

## Pitfalls

- **Comparing only the top level.** Placing the children by their widths, or by the positions of the children alone, lets deeper levels overlap. The comparison must run over every common level.
- **Rebuilding contours.** Copying the contour lists at every merge can cost $\Theta(n^2)$ in all, for example on a long path with a leaf at each vertex. Keep the list of the taller part and rewrite only the common levels.
- **Shifts.** Each contour is relative to its own root, or to the first child of the forest. Forgetting to add the offset of a child, or the shift $-m$ at line L10, gives drawings that look right on small trees and fail on deep ones.
- **Recursion.** A recursive version needs a call stack as deep as the tree. On a path of $10^5$ vertices, use an explicit order as in line L1.
- **Rounding.** Halving at line L8 makes fractions. Rounding each $m$ to an integer is common, but then a parent is not exactly centred.

## Implementations

## History

Wetherell and Shannon in 1979 stated rules for tidy drawings of trees and gave linear-time methods that place each level from left to right. Reingold and Tilford in 1981 added the rule that a subtree is drawn the same wherever it occurs, which their predecessors' drawings did not keep, and gave the contour method for binary trees with a proof of linear time. Supowit and Reingold showed in 1983 that the narrowest drawing under these rules is NP-hard to find on a grid. Walker extended the method in 1990 to trees of any degree, and Buchheim, Jünger and Leipert in 2002 made his extension run in linear time.

## References
