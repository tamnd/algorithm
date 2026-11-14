---
tag: 9NWMQZ
kind: data-structure
slug: sequence-pair
name: Sequence pair
aliases:
- Murata sequence pair
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Murata and coauthors' pair of block orders that encodes left-of and below relations for any packing, including non-slicing ones, decoded by longest paths.
model: word-ram
complexity:
  vars: {n: the number of blocks}
  time: {worst: O(n log n), average: O(n log n), best: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1995
  people: [Hiroshi Murata, Kunihiro Fujiyoshi, Shigetoshi Nakatake, Yoji Kajitani]
  note: Murata, Fujiyoshi, Nakatake and Kajitani presented the sequence pair at ICCAD 1995, and the journal version appeared in IEEE Transactions on CAD in 1996.
prereqs: [floorplan-constraint-graphs, permutation, dag-longest-path, fenwick-tree]
see_also: [rectangle-packing, floorplanning, longest-common-subsequence, b-star-tree-floorplan, o-tree-floorplan, normalized-polish-expression, wong-liu-floorplanning, mosaic-floorplan]
sources:
  - paper: doi:10.1109/43.552084
    title: Hiroshi Murata, Kunihiro Fujiyoshi, Shigetoshi Nakatake and Yoji Kajitani, VLSI module placement based on rectangle-packing by the sequence-pair, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(12), 1518 to 1524, 1996
    locator: the definition of the sequence pair, the decoding by the horizontal and vertical constraint graphs, the gridding that gives a sequence pair for every packing, and the annealing over sequence pairs
  - paper: "Hiroshi Murata, Kunihiro Fujiyoshi, Shigetoshi Nakatake and Yoji Kajitani, Rectangle-packing-based module placement, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 472 to 479, 1995"
    locator: the conference version
  - paper: doi:10.1145/343647.343713
    title: Xiaoping Tang, Ruiqi Tian and D. F. Wong, Fast evaluation of sequence pair in block placement by longest common subsequence computation, Design, Automation and Test in Europe (DATE), 106 to 111, 2000
    locator: the O(n log n) decoding as a weighted longest common subsequence
  - paper: doi:10.1145/370155.370523
    title: Xiaoping Tang and D. F. Wong, FAST-SP, a fast algorithm for block placement based on sequence pair, Asia and South Pacific Design Automation Conference (ASP-DAC), 521 to 526, 2001
    locator: the O(n log log n) decoding with a faster priority queue
  - paper: doi:10.1109/TVLSI.2003.817546
    title: Saurabh N. Adya and Igor L. Markov, Fixed-outline floorplanning, enabling hierarchical design, IEEE Transactions on VLSI Systems 11(6), 1120 to 1135, 2003
    locator: annealing over sequence pairs with a fixed outline
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (sequence pairs, from a floorplan to a sequence pair and back; general locator)
---

A sequence pair is two orders of the same blocks, written $(\Gamma_+, \Gamma_-)$. For each pair of blocks, the two orders say whether one block is to the left of the other or below it. The packing of a sequence pair puts every block as far to the left and as low as these relations allow. It is computed by longest paths in the two [constraint graphs](/floorplan-constraint-graphs/), or in $O(n \log n)$ time as a weighted [longest common subsequence](/longest-common-subsequence/). Murata, Fujiyoshi, Nakatake and Kajitani introduced it in 1995, and they proved that every packing, slicing or not, has a sequence pair whose packing is not larger. So a search over the $(n!)^2$ pairs, such as an annealing, always contains an optimal [rectangle packing](/rectangle-packing/).

## In plain words

Write the names of the blocks in two lists. If block A comes before block B in both lists, A goes to the left of B. If B comes before A in the first list but A comes before B in the second, A goes below B. Every two blocks are in one of these cases, so every two blocks are kept apart, either side by side or one above the other.

To build the picture, take the blocks in the order of the first list. Push each block to the left until it touches a block that must be on its left, or the wall. Then do the same downward. The result never has two blocks on top of each other.

## The abstract type

The type stores a sequence pair of a set of $n$ blocks. The operations are:

- RELATION$(a, b)$: tell whether $a$ is left of, right of, below or above $b$.
- PACK$(w, h)$: given the width $w_b$ and the height $h_b$ of each block, return the lower-left corner $(x_b, y_b)$ of each block and the width $W$ and the height $H$ of the packing.
- PACK-BY-GRAPHS$(w, h)$: the same packing, by longest paths in the constraint graphs.
- SWAP-IN-PLUS$(a, b)$ and SWAP-IN-BOTH$(a, b)$: the moves of a search.

The rule of this page is: if $a$ comes before $b$ in both $\Gamma_+$ and $\Gamma_-$, then $a$ is left of $b$; if $b$ comes before $a$ in $\Gamma_+$ and $a$ comes before $b$ in $\Gamma_-$, then $a$ is below $b$. Some sources swap the roles of the two orders, or of "below" and "above". The structure is the same.

## Representation

The two orders are arrays, and two more arrays give the position of each block in each order, so RELATION reads two positions. The four cases of the two comparisons are the four relations: before in both is left, after in both is right, after in $\Gamma_+$ and before in $\Gamma_-$ is below, and the last case is above. Each pair of blocks has exactly one relation, so in the packing each pair is separated by a vertical line or by a horizontal line.

The horizontal constraint graph $G_h$ has an edge $a \to b$ of weight $w_a$ when $a$ is left of $b$, and the vertical graph $G_v$ has an edge $a \to b$ of weight $h_a$ when $a$ is below $b$. Every edge of $G_h$ goes forward in $\Gamma_+$, and every edge of $G_v$ goes forward in $\Gamma_-$, so both graphs are DAGs with a known topological order. The packing is $x_b$ = the longest path into $b$ in $G_h$ and $y_b$ = the longest path into $b$ in $G_v$, the least solution of the [difference constraints](/difference-constraints/) of the two graphs.

## Operations

```pseudo id=main
PACK(Γ+, Γ−, w, h)                          ▷ pos−(b): the position of b in Γ−, from 1
L1  F ← a Fenwick tree of prefix maxima over the positions 1..n, all 0
L2  for each block b in the order Γ+ do
L3      x_b ← the maximum of F over the positions 1 .. pos−(b) − 1
L4      raise F at the position pos−(b) to x_b + w_b
L5  F' ← a new Fenwick tree of prefix maxima, all 0
L6  for each block b in the reverse of the order Γ+ do
L7      y_b ← the maximum of F' over the positions 1 .. pos−(b) − 1
L8      raise F' at the position pos−(b) to y_b + h_b
L9  return x, y, W = the maximum of F, H = the maximum of F'
```

When line L3 runs for $b$, the tree holds the blocks that come before $b$ in $\Gamma_+$, and the query keeps those that also come before $b$ in $\Gamma_-$. These are exactly the blocks left of $b$, so $x_b$ is the largest right side among them. Lines L6 to L8 do the same in the reverse order, and select the blocks below $b$. This is the weighted longest common subsequence of Tang, Tian and Wong: $W$ is the largest total width of a sequence of blocks that is common to $\Gamma_+$ and $\Gamma_-$.

```pseudo id=graphs
PACK-BY-GRAPHS(Γ+, Γ−, w, h)
L10 x_b ← 0 and y_b ← 0 for each block b
L11 for each block b in the order Γ+ do
L12     for each a before b in Γ+ with pos−(a) < pos−(b) do x_b ← max(x_b, x_a + w_a)
L13 for each block b in the order Γ− do
L14     for each a before b in Γ− with pos+(a) > pos+(b) do y_b ← max(y_b, y_a + h_a)
L15 return x, y, W = max_b (x_b + w_b), H = max_b (y_b + h_b)
```

```pseudo id=swap
SWAP-IN-PLUS(a, b)
L16 exchange a and b in Γ+, and exchange pos+(a) and pos+(b)

SWAP-IN-BOTH(a, b)
L17 SWAP-IN-PLUS(a, b); exchange a and b in Γ−, and exchange pos−(a) and pos−(b)
```

A swap in $\Gamma_+$ only changes the relation of $a$ and $b$ and of the blocks between them. A swap in both orders exchanges the places of $a$ and $b$ in the packing, when they have the same size. Murata and coauthors used these two moves and the rotation of a block in their annealing.

## Example

A pinwheel of five blocks fills a $3 \times 3$ square: block 1 ($1 \times 2$) at the lower left, block 2 ($2 \times 1$) at the bottom right, block 3 ($1 \times 1$) in the centre, block 4 ($1 \times 2$) at the right, and block 5 ($2 \times 1$) at the top left. No straight cut splits it, so it is not a [slicing floorplan](/slicing-floorplan/) and no [Polish expression](/normalized-polish-expression/) stores it. The sequence pair $\Gamma_+ = (5, 1, 3, 4, 2)$, $\Gamma_- = (1, 2, 3, 5, 4)$ does. The positions in $\Gamma_-$ are $1 \to 1$, $2 \to 2$, $3 \to 3$, $5 \to 4$ and $4 \to 5$.

| pass | block | pos− | values in the tree at positions below pos− | coordinate | the tree is raised at pos− to |
|---|---|---|---|---|---|
| x | 5 | 4 | none | $x_5 = 0$ | 2 |
| x | 1 | 1 | none | $x_1 = 0$ | 1 |
| x | 3 | 3 | 1 (block 1) | $x_3 = 1$ | 2 |
| x | 4 | 5 | 1, 2, 2 (blocks 1, 3, 5) | $x_4 = 2$ | 3 |
| x | 2 | 2 | 1 (block 1) | $x_2 = 1$ | 3 |
| y | 2 | 2 | none | $y_2 = 0$ | 1 |
| y | 4 | 5 | 1 (block 2) | $y_4 = 1$ | 3 |
| y | 3 | 3 | 1 (block 2) | $y_3 = 1$ | 2 |
| y | 1 | 1 | none | $y_1 = 0$ | 2 |
| y | 5 | 4 | 2, 1, 2 (blocks 1, 2, 3) | $y_5 = 2$ | 3 |

The corners are $1: (0, 0)$, $2: (1, 0)$, $3: (1, 1)$, $4: (2, 1)$ and $5: (0, 2)$, and $W = H = 3$. The block area is $2 + 2 + 1 + 2 + 2 = 9$, so the packing has no empty space. RELATION(2, 3) is "below": block 3 comes before block 2 in $\Gamma_+$, and block 2 comes before block 3 in $\Gamma_-$. In the x pass, block 2 does not see blocks 5, 3 and 4, although they come before it in $\Gamma_+$, because they come after it in $\Gamma_-$: they are above block 2, not to its left.

## Correctness

Each pair of blocks gets exactly one of the four relations, because the two comparisons have four outcomes. The edges of $G_h$ go forward in $\Gamma_+$ and those of $G_v$ go forward in $\Gamma_-$, so both graphs are acyclic, and the longest paths are the least coordinates that obey every relation. PACK computes the same values: when it visits $b$ in the order $\Gamma_+$, the Fenwick query over the positions before $b$ in $\Gamma_-$ ranges over exactly the blocks left of $b$. Since every pair is separated in $x$ or in $y$, no two blocks overlap. Any placement that obeys the same relations has coordinates at least as large. Murata and coauthors proved that every placement without overlap obeys the relations of some sequence pair; this is cited with a sketch, and the tests check it for up to four blocks. The full proof of the rest is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | extra space |
|---|---|---|
| RELATION | $O(1)$ | none |
| PACK | $O(n \log n)$ | $O(n)$ |
| PACK-BY-GRAPHS | $\Theta(n^2)$ | $O(n)$, the edges are not stored |
| SWAP-IN-PLUS, SWAP-IN-BOTH | $O(1)$ | none |

The constraint graphs can have $\Theta(n^2)$ edges, for example when $\Gamma_+ = \Gamma_-$ and all blocks are in one row. The original decoding builds them and takes $O(n^2)$ time. Tang, Tian and Wong showed in 2000 that the packing is a weighted longest common subsequence and gave the $O(n \log n)$ method above. Tang and Wong lowered the time to $O(n \log \log n)$ in 2001 with a faster priority queue for integer keys. The bound is on the word RAM with the sizes in words.

There are $(n!)^2$ sequence pairs of $n$ blocks. Many of them give the same packing, so the space is redundant: for example, a row of blocks and a gap-free stack have many pairs each.

## Variants

- **Rotations and soft blocks.** A search adds the rotation of a block as a move, or changes the shape of a soft block. The pair does not change, only the sizes.
- **Fixed outline.** Adya and Markov search over sequence pairs for a packing that fits a given outline, with a cost for the part outside it.
- **Incremental evaluation.** A swap changes the relations of a few blocks, and incremental methods update only the coordinates that change.
- **Other representations.** The [B*-tree](/b-star-tree-floorplan/) and the [O-tree](/o-tree-floorplan/) store only compacted packings, with less redundancy and a linear decoding. The corner block list of Hong and coauthors stores [mosaic floorplans](/mosaic-floorplan/).
- **Constraints.** Pre-placed blocks, alignment and symmetry for analog layout can be written as conditions on the two orders.

## When to use it

Use a sequence pair when the best packing may be non-slicing and a search will change the packing many times, as in annealing floorplanners for macros. Every pair is a legal packing, the moves are simple swaps, and the decoding is fast. For slicing floorplans, a [normalized Polish expression](/normalized-polish-expression/) has no redundancy and allows exact sizing of soft blocks. If the decoding time matters most, a [B*-tree](/b-star-tree-floorplan/) decodes in linear time.

## Pitfalls

- **Mixing up the convention.** The meaning of "before in $\Gamma_+$ and after in $\Gamma_-$" differs between sources. Use one convention in RELATION, in PACK and in the moves.
- **The wrong order for y.** The y pass must visit the blocks in the reverse of $\Gamma_+$. In the order of $\Gamma_+$ the query selects the blocks above, not below.
- **A reused tree.** The Fenwick tree of line L1 must start at 0 for each decoding. A tree left over from the x pass or from the last pair gives wrong maxima.
- **Expecting a compact packing.** Each block is as low as its "below" relations allow. A block that is "below" $b$ in the pair but lies to one side of $b$ in the geometry can still push $b$ up, so $b$ can float with empty space under all of it. In a B*-tree packing, each block rests on the floor or on a block below it.
- **Counting floorplans.** The $(n!)^2$ pairs do not count distinct packings or floorplans. Many pairs give the same packing.

## Implementations

The Python class stores the two orders and their position maps, and implements RELATION, PACK with a Fenwick tree of prefix maxima, PACK-BY-GRAPHS by longest paths in the topological orders, and the two swaps. The tests check the pinwheel, 800 random pairs of up to 12 blocks for equal results of the two decodings and for the absence of overlap with every relation true in the geometry, and, for 3 and 4 blocks, that the best area over all $(n!)^2$ pairs equals the best area of a search over all positions.

## History

Murata, Fujiyoshi, Nakatake and Kajitani presented the sequence pair at ICCAD 1995 and in IEEE Transactions on CAD in 1996, with the gridding proof that every packing has a sequence pair and an annealing over pairs. Tang, Tian and Wong gave the $O(n \log n)$ decoding by weighted longest common subsequences in 2000, and Tang and Wong the $O(n \log \log n)$ decoding FAST-SP in 2001. Adya and Markov used sequence pairs for fixed-outline floorplanning in 2003.

## References
