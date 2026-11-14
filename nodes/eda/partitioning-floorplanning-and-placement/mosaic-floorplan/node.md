---
tag: MWJ26C
kind: definition
slug: mosaic-floorplan
name: Mosaic floorplan
aliases:
- rectangular dissection floorplan
area: eda/partitioning-floorplanning-and-placement
level: advanced
summary: A dissection of the chip into rectangles with no empty rooms and no crossing segments, counted up to sliding of segments.
prereqs: [slicing-floorplan, floorplan-constraint-graphs, euler-formula]
see_also: [mosaic-floorplan-baxter-theorem, sequence-pair, b-star-tree-floorplan, o-tree-floorplan, normalized-polish-expression, planar-graph, floorplanning]
sources:
  - paper: "Bo Yao, Hongyu Chen, Chung-Kuan Cheng and Ronald L. Graham, Floorplan representations: complexity and connections, ACM Transactions on Design Automation of Electronic Systems 8(1), 55 to 80, 2003"
    locator: the definition of mosaic floorplans and their equivalence by sliding of segments, the number of inner segments, and the counts of mosaic and slicing floorplans
  - paper: doi:10.1109/ICCAD.2000.896442
    title: Xianlong Hong, Gang Huang, Yici Cai, Jiangchun Gu, Sheqin Dong, Chung-Kuan Cheng and Jun Gu, Corner block list, an effective and efficient topological representation of non-slicing floorplan, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 8 to 12, 2000
    locator: mosaic floorplans without empty rooms and their corner block list
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (slicing and non-slicing floorplans; general locator)
---

A mosaic floorplan is a division of the chip rectangle into rectangular rooms, one room for each block, in which no four rooms meet at a point, and in which only the topology counts: two divisions are the same mosaic floorplan when one becomes the other by sliding segments without changing which room is next to which segment. It is the wider class that contains all [slicing floorplans](/slicing-floorplan/) and also the pinwheel, which no sequence of cuts can make. Its value is that it is a finite, combinatorial object: with $n$ rooms there are exactly $n - 1$ inner segments, the number of floorplans is the Baxter number, and a floorplanner can search over them with representations such as the corner block list or twin binary trees and then compute the sizes with longest paths.

## Definition

**Dissection.** Let $R$ be an axis-parallel rectangle. A dissection of $R$ into $n$ rooms is a set of $n$ axis-parallel rectangles with disjoint interiors whose union is $R$. A *segment* of the dissection is a maximal straight piece of the union of the room boundaries that lies inside $R$ and is not part of the boundary of $R$.

**Mosaic floorplan.** A dissection is a mosaic floorplan if no point of $R$ is a corner of four rooms. Then each end of a segment is a *T-junction*: it lies inside another segment or on a side of $R$, which goes on past it on both sides. Two mosaic floorplans are *equivalent* if there is a one to one map of the rooms and a one to one map of the segments that keeps the direction of each segment and the relations "room $r$ touches segment $s$ from the left", "from the right", "from below" and "from above". A mosaic floorplan is an equivalence class. In each class the rooms can be drawn with any sizes that the relations allow, so the class stores only the topology, and the sizes are found later.

**Number of segments.** A mosaic floorplan with $n$ rooms has exactly $n - 1$ segments. Take it as a plane graph: the vertices are the four corners of $R$ and the ends of the segments, and the edges are the pieces between consecutive vertices on the segments and on the sides of $R$. Let $s$ be the number of segments.

- Two ends of segments never meet at one point. Two ends from opposite sides of a line make four rooms meet. If a vertical segment ends at the end point $p$ of a horizontal segment, then the horizontal line goes on past $p$ on both sides, so the horizontal segment does not end at $p$. So there are $2 s + 4$ vertices.
- There are $s + 4$ lines, the segments and the four sides. A line with $t$ T-junctions inside it has $t + 1$ edges, and each of the $2 s$ ends lies inside exactly one line. So there are $(s + 4) + 2 s = 3 s + 4$ edges.
- The faces are the $n$ rooms and the outer face.

The [Euler formula](/euler-formula/) $V - E + F = 2$ gives $(2 s + 4) - (3 s + 4) + (n + 1) = 2$, so $s = n - 1$. The same count also bounds the pairs of rooms that touch along a piece of an edge: each inner edge has one room on each side, and there are at most $3 s + 4 - 4 = 3 n - 3$ inner edges, so fewer than $3 n$ pairs of rooms are neighbors.

**Counting.** The numbers of mosaic floorplans with $n$ rooms, and of the slicing ones among them, are:

| rooms $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| mosaic floorplans | 1 | 2 | 6 | 22 | 92 | 422 | 2074 |
| slicing floorplans | 1 | 2 | 6 | 22 | 90 | 394 | 1806 |

The first row is the sequence of Baxter numbers, which is the [Baxter number theorem](/mosaic-floorplan-baxter-theorem/), and the second row is the sequence of large Schröder numbers. The ratios of consecutive terms tend to $8$ and to $3 + 2 \sqrt{2} \approx 5.83$, so for large $n$ almost all mosaic floorplans are not slicing.

**Sizes from the topology.** Give each room a block of width $w_r$ and height $h_r$. The relations of a mosaic floorplan give two [constraint graphs](/floorplan-constraint-graphs/): an edge $a \to b$ in the horizontal graph when $a$ touches a vertical segment from the left and $b$ touches the same segment from the right, and in the same way for the vertical graph and the horizontal segments. In every drawing of the floorplan in which each room holds its block, an edge $a \to b$ of the horizontal graph forces $x_b \ge x_a + w_a$. So the longest path to $b$ in the horizontal graph is a lower bound on $x_b$, and the longest paths in the two graphs are lower bounds on the width and the height of the chip.

## Examples and non-examples

**Few rooms.** With two rooms there are two mosaic floorplans, one vertical segment or one horizontal segment. With three rooms there are six, the same as the six slicing floorplans: three columns, three rows, and a full segment with a second segment that ends on it from one of its two sides.

**Four rooms in a grid.** The $2 \times 2$ grid of four equal squares has a point where four rooms meet, so it is not a mosaic floorplan. It stands for two mosaic floorplans. Move the two horizontal pieces apart: the vertical segment becomes whole, and the horizontal pieces are two segments that end on it from the left and from the right. Move the two vertical pieces apart instead: the horizontal segment becomes whole. These two are not equivalent, since in the first one the four rooms touch one vertical segment and in the second one they touch one horizontal segment.

**Sliding gives the same floorplan.** Take a vertical segment from the bottom to the top of $R$ and, on its left, a horizontal segment from the left side of $R$ to it. Moving the horizontal segment up or down, or the vertical segment left or right, changes the sizes of the three rooms but not the relations, so all these drawings are one mosaic floorplan.

**The pinwheel.** The $3 \times 3$ square with the rooms $[0, 1] \times [0, 2]$, $[1, 3] \times [0, 1]$, $[2, 3] \times [1, 3]$, $[0, 2] \times [2, 3]$ and $[1, 2] \times [1, 2]$ is a mosaic floorplan with $5$ rooms and $4 = 5 - 1$ segments. Each segment ends on a side of $R$ at one end and on the next segment at the other end, so none runs from side to side, and the floorplan is not slicing. Its mirror image turns the other way. These two are the $92 - 90 = 2$ mosaic floorplans with five rooms that are not slicing.

**Non-example: a packing with empty space.** A placement of blocks found from a [sequence pair](/sequence-pair/), a [B*-tree](/b-star-tree-floorplan/) or an [O-tree](/o-tree-floorplan/) usually leaves empty space between the blocks, so it is not a dissection. These representations describe packings, a different class of objects, and different packings can give the same mosaic floorplan after the empty space is given to the rooms.

**Non-example: an L-shaped room.** A division of $R$ in which one part is an L shape is not a dissection into rooms, since each room must be a rectangle.

## Related definitions

- **[Slicing floorplan](/slicing-floorplan/).** The mosaic floorplans that can be made by cuts from side to side, counted by the large Schröder numbers.
- **[Baxter number theorem](/mosaic-floorplan-baxter-theorem/).** The count of mosaic floorplans by the Baxter numbers, with the bijection to twin binary trees.
- **Corner block list.** The representation of Hong and others (2000): it removes the room at one corner again and again and records the direction of the removal and the number of T-junctions, so it describes each mosaic floorplan by a word of length $O(n)$.
- **[Floorplan constraint graphs](/floorplan-constraint-graphs/).** The horizontal and vertical graphs that turn the relations into coordinates.
- **[Sequence pair](/sequence-pair/), [B*-tree](/b-star-tree-floorplan/) and [O-tree](/o-tree-floorplan/).** Representations of packings with empty space, a larger set of objects than the mosaic floorplans.
- **[Planar graph](/planar-graph/).** A mosaic floorplan is a plane graph whose inner faces are rectangles, and the count of its segments comes from the Euler formula.

## References
