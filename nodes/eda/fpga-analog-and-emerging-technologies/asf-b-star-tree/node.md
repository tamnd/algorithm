---
tag: TQF55M
kind: data-structure
slug: asf-b-star-tree
name: ASF-B*-tree
aliases:
- automatically symmetric-feasible B*-tree
- symmetry island B*-tree
area: eda/fpga-analog-and-emerging-technologies
level: research
summary: A B*-tree over the representatives of one symmetric set whose every packing is mirror-symmetric about the axis, used in analog placement by Lin and Lin and by Lin, Chang and Lin.
model: word-ram
complexity:
  vars: {n: the number of representatives (pairs plus self-symmetric cells)}
  time: {pack: O(n), rotate: O(1), swap: O(n), delete: O(n), insert: O(n)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2007
  people: [Po-Hung Lin, Shyh-Chang Lin, Yao-Wen Chang]
  note: Lin and Lin gave the automatically symmetric-feasible B*-tree at DAC 2007, and Lin, Chang and Lin built a hierarchical analog placer on it in IEEE Transactions on CAD in 2009.
prereqs: [b-star-tree-floorplan, analog-symmetry-constraint, preorder-traversal, binary-tree]
see_also: [symmetric-feasible-sequence-pair, sequence-pair, common-centroid-layout, simulated-annealing-placement, skyline-problem, catalan-numbers, floorplanning]
sources:
  - paper: "Po-Hung Lin and Shyh-Chang Lin, Analog placement based on novel symmetry-island formulation, Proceedings of the 44th Design Automation Conference, 465 to 470, 2007"
    title: P.-H. Lin and S.-C. Lin, Analog placement based on novel symmetry-island formulation, DAC 2007, pages 465 to 470
    locator: the definition of the ASF-B*-tree (one representative per pair and per self-symmetric cell, the self-symmetric ones on the rightmost branch), its packing and mirroring, and the symmetry-island theorem
  - paper: doi:10.1109/TCAD.2009.2017433
    title: Po-Hung Lin, Yao-Wen Chang and Shyh-Chang Lin, Analog placement based on symmetry-island formulation, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 28(6), 791 to 804, 2009
    locator: the journal version, with the hierarchical B*-tree that holds each symmetry island as one node, and the experiments
  - paper: doi:10.1145/337292.337541
    title: Yun-Chih Chang, Yao-Wen Chang, Guang-Ming Wu and Shu-Wei Wu, B*-trees, a new representation for non-slicing floorplans, Proceedings of the 37th Design Automation Conference, 458 to 463, 2000
    locator: the B*-tree, its packing, and the theorem that every placement compact to the left and down is the packing of a B*-tree
  - paper: doi:10.1109/43.851988
    title: Florin Balasa and Koen Lampaert, Symmetry within the sequence-pair representation in the context of placement for analog design, IEEE Transactions on Computer-Aided Design 19(7), 721 to 731, 2000
    locator: symmetric placement with sequence pairs, the approach that the ASF-B*-tree is compared with
---

An ASF-B*-tree (automatically symmetric-feasible B*-tree) is a [B*-tree](/b-star-tree-floorplan/) over half of a symmetric set of an analog circuit: the right cell of each matched pair, and the right half of each cell that must sit on the axis. Its topic is analog sizing and layout, one of the five topics of this sub-area. The tree packs this half, and the other half is its mirror image, so every packing is symmetric by construction, as the [symmetry constraint](/analog-symmetry-constraint/) asks. Lin and Lin gave it in 2007 to keep a symmetric set together as one block, a *symmetry island*, in an annealing placer.

## In plain words

Some blocks of an analog circuit come in matched pairs that must be mirror images about one vertical line, and some must sit on that line.

Draw only the right half. Keep the right block of each pair, and the right half of each block that sits on the line. Pack these pieces with a B*-tree, the usual tree for packing blocks: a left child goes to the right of its parent, and a right child goes on top of it. Then copy the drawing in a mirror to the left of the line.

The blocks that must sit on the line are kept on the chain from the root through right children. Those are exactly the pieces that touch the line. With that one rule, every tree the search can make gives a symmetric picture with no overlap, so the search never wastes time on broken trees.

## The abstract type

A symmetric set with a vertical axis has pairs, each of two cells of equal size, and self-symmetric cells. The structure holds a placement of the group, and supports:

- PACK: the placement of all cells of the group, mirror-symmetric about $x = 0$, with its width and height.
- ROTATE$(b)$: turn a pair (both cells) or a self-symmetric cell by 90 degrees.
- SWAP$(a, b)$: exchange two representatives in the tree.
- DELETE$(b)$ and INSERT$(b, p, \text{side})$: move a representative to another place in the tree.

Every sequence of these operations leaves a tree whose packing is symmetric. In a placer the group is then one block of a larger [floorplan](/floorplanning/), and its packing gives the shape of that block.

## Representation

The tree has one node per *representative*. The representative of a pair is its right cell, of size $w \times h$. The representative of a self-symmetric cell of size $w \times h$ is its right half, of size $\frac{w}{2} \times h$. Each node has a left child, a right child and a size. The packing rules are those of the B*-tree: the root has $x = 0$, the left child $c$ of $b$ has $x_c = x_b + w_b$, and the right child has $x_c = x_b$.

The *rightmost branch* is the root and its chain of right children. The tree is an ASF-B*-tree when every self-symmetric representative is on the rightmost branch. The axis is the line $x = 0$, and the nodes of the rightmost branch are exactly the representatives with $x = 0$. A pair representative may also be on the rightmost branch: then its two cells touch at the axis.

## Operations

```pseudo id=main
PACK(T)                                  ▷ T is an ASF-B*-tree of representatives
L1  for each node b of T in preorder do
L2      x_b ← 0 if b is the root; x_p + w_p if b is the left child of p; x_p if b is the right child of p
L3      y_b ← the highest top among the placed nodes whose x-range meets [x_b, x_b + w_b), or 0
L4      record the representative at (x_b, y_b)
L5  for each pair representative b: place its partner at (−x_b − w_b, y_b)
L6  for each self-symmetric b, x_b = 0: place the whole cell at (−w, y_b), width 2w, where w is the width of the half
L7  return the placement, the width 2 · max (x_b + w_b) and the height max (y_b + h_b)
```

Line L3 is the contour of the B*-tree page, which takes amortized $O(1)$ time per node. The implementation searches all placed nodes, in $O(n)$ time per node, which is simpler to check.

The moves keep the ASF rule:

- ROTATE$(b)$ swaps the width and height of the cell. For a self-symmetric cell of size $w \times h$, the half becomes $\frac{h}{2} \times w$.
- SWAP$(a, b)$ exchanges two labels, unless this would move a self-symmetric label off the rightmost branch.
- DELETE$(b)$ is the B*-tree deletion: while $b$ has two children, exchange it with its left child; then replace $b$ by its only child.
- INSERT$(b, p, \text{side})$ makes $b$ the left or right child of $p$, and the old child becomes the child of $b$ on the same side. A self-symmetric $b$ may only become the root (with the old root as its right child) or the right child of a node on the rightmost branch.

## Example

Take a pair $a$ of size $2 \times 1$, a pair $b$ of size $1 \times 2$, and a self-symmetric cell $s$ of size $2 \times 2$ (width by height). The representatives are $a$ ($2 \times 1$), $b$ ($1 \times 2$), and the half of $s$ ($1 \times 2$). The tree has the root $s$, the left child $b$ of $s$, and the right child $a$ of $s$. The self-symmetric $s$ is the root, so it is on the rightmost branch. The preorder is $s, b, a$.

| node | rule | $x$ | $y$ | right half | mirror |
|---|---|---|---|---|---|
| $s$ | root | 0 | 0 | $[0, 1] \times [0, 2]$ | $[-1, 0] \times [0, 2]$ |
| $b$ | left of $s$ | 1 | 0 | $[1, 2] \times [0, 2]$ | $[-2, -1] \times [0, 2]$ |
| $a$ | right of $s$ | 0 | 2 | $[0, 2] \times [2, 3]$ | $[-2, 0] \times [2, 3]$ |

The cell $s$ is $[-1, 1] \times [0, 2]$, centered on the axis. The two cells of $b$ flank it, and the two cells of $a$ lie on top. The group fills $[-2, 2] \times [0, 3]$, with area 12, which is the total area of the cells, so there is no gap. The tests confirm that 12 is the least area of any symmetric placement of this group.

A tree with the root $b$ and $s$ as the left child of $b$ is not an ASF-B*-tree: $s$ would be at $x = 1$, and its two halves would land at $[1, 2]$ and $[-2, -1]$, which is not one cell.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness.md).

By the B*-tree rules, a right child has the $x$ of its parent, and a left child is further right. So every representative has $x \ge 0$, and $x = 0$ exactly on the rightmost branch. The ASF rule thus puts every self-symmetric half on the axis, where it joins its mirror into one centered cell. The two cells of a pair have the same $y$ and mirror $x$-ranges by line L5.

No two cells overlap. The representatives do not overlap, because line L3 puts each one above the placed nodes that share its $x$-range. Their mirrors do not overlap for the same reason. A representative lies in $x \ge 0$ and a mirror in $x \le 0$, so they meet at most along the axis.

No placement of least area is lost. Take any symmetric placement, keep its right half, and compact it down and to the left. The self-symmetric halves stay at $x = 0$. By the theorem of Chang, Chang, Wu and Wu, the compact placement is the packing of a B*-tree, and its self-symmetric halves are at $x = 0$, so they are on the rightmost branch. So some ASF-B*-tree is as good. The tests check this on three groups by a search over a grid.

Lin, Chang and Lin also state that the packing is a symmetry island, one connected region. With the plain packing of lines L1 to L4, this does not hold for every tree. The proof file gives a tree whose packing puts a cell of a pair in a corner where it touches no other cell; the tests count 1 such tree out of 18 for the group of the example, and 3 out of 80 for a group of two pairs and two self-symmetric cells. A placer that needs one connected island must check it or pack the group in a way that keeps it.

## Complexity

| operation | time | extra space |
|---|---|---|
| PACK with the contour | $O(n)$ amortized | $O(n)$ |
| PACK by a search over placed nodes (the implementation) | $\Theta(n^2)$ | $O(n)$ |
| ROTATE | $O(1)$ | none |
| SWAP | $O(1)$ with parent links, plus $O(n)$ to test the rightmost branch | none |
| DELETE, INSERT | $O(1)$ to relink, plus the swaps down a path and the test of the rightmost branch | none |

With $k$ pairs and $m$ self-symmetric cells, the tree has $n = k + m$ nodes, half of the $2k + m$ cells of the group. So the search space is that of B*-trees on $n$ nodes, cut further by the ASF rule. For one group with two pairs and one self-symmetric cell, 18 of the 30 labeled trees are ASF-B*-trees, and with two pairs and two self-symmetric cells, 80 of 336.

## Variants

- **Hierarchical B*-tree.** Lin, Chang and Lin treat each symmetry island as one node of a top-level B*-tree that also holds the free cells, and annealing perturbs both levels.
- **Horizontal axis.** Exchange the roles of $x$ and $y$: the representatives are the upper cells, and the self-symmetric halves are kept on the leftmost branch (the root and its chain of left children), whose nodes all have $y = 0$.
- **Sequence pairs.** [Symmetric-feasible sequence pairs](/symmetric-feasible-sequence-pair/) keep symmetry with a condition on the two orders and a packing that solves the symmetry equations. They allow free cells between the cells of a group, which a mirrored half-tree does not.
- **Common centroid.** Devices that must also cancel gradients in both directions use a [common-centroid layout](/common-centroid-layout/), which a mirror placement does not give.

## When to use it

Use it in an annealing placer for analog circuits when each symmetric set should stay together in one region, which shortens the wires between matched devices and makes their surroundings alike. Use symmetric-feasible sequence pairs instead when other cells may sit between the cells of a group.

## Pitfalls

- **A self-symmetric half off the axis.** If a move puts a self-symmetric half as a left child, its two halves come apart, as in the example above. Every move must keep the ASF rule, or the packing must reject the tree.
- **Odd widths.** The half of a self-symmetric cell of odd width has a half-unit width. Keep the coordinates in half units, or double all coordinates, until the group is placed.
- **Rotating a pair.** Rotate both cells of a pair together, and rotate a self-symmetric cell as a whole: its half is $\frac{h}{2} \times w$ after the turn, not $h \times \frac{w}{2}$.
- **Assuming a connected island.** The plain packing can leave a cell of a pair in a corner, apart from the rest of the group, as shown above. Check connectivity if the placer counts on it.

## Implementations

## History

Chang, Chang, Wu and Wu gave the B*-tree in 2000. Balasa and Lampaert had given symmetric placement with sequence pairs in the same year. Lin and Lin gave the ASF-B*-tree at DAC 2007, to place each symmetric set as one island. Lin, Chang and Lin put the islands into a hierarchical B*-tree in IEEE Transactions on CAD in 2009.

## References
