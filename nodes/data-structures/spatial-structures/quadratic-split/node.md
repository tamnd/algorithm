---
tag: 4EXTW1
kind: algorithm
slug: quadratic-split
name: Quadratic split
aliases:
- Guttman quadratic split
area: data-structures/spatial-structures
level: advanced
summary: Guttman's split that picks the pair of entries wasting the most area as seeds, then assigns the rest greedily.
model: word-ram
complexity:
  vars: {n: the number of entries to split (M + 1 for an overflowing node of capacity M), d: the number of dimensions}
  time: {worst: O(d n^2)}
  space: {extra: O(n)}
history:
  year: 1984
  people: [Antonin Guttman]
  note: Guttman gave the quadratic split with the R-tree, between an exhaustive split that is exponential in the node size and a linear split that is faster and worse.
prereqs: [r-tree, minimum-bounding-rectangle]
see_also: [r-tree-node-splitting, r-star-tree, r-tree, overlap-and-dead-space, x-tree, str-packing]
sources:
  - paper: doi:10.1145/602259.602266
    title: Antonin Guttman, R-trees, a dynamic index structure for spatial searching, Proceedings of ACM SIGMOD 1984, pp. 47 to 57
    locator: Section 3.5 (node splitting, the exhaustive algorithm, the quadratic-cost algorithm with PickSeeds and PickNext, and the linear-cost algorithm) and Section 4 (performance tests of the three splits)
  - paper: doi:10.1145/93597.98741
    title: Norbert Beckmann, Hans-Peter Kriegel, Ralf Schneider and Bernhard Seeger, The R*-tree, an efficient and robust access method for points and rectangles, Proceedings of ACM SIGMOD 1990
    locator: Section 3 (the analysis of Guttman's splits, the tendency of the quadratic split to make one large and one small group, and the effect of the minimum fill)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the section on the R-tree and its node splitting rules
---

The quadratic split divides the $M + 1$ entries of an overflowing [R-tree](/r-tree/) node into two groups of at least $m$ entries each, so that the two bounding rectangles have a small total area. It first picks as *seeds* the two entries that would waste the most area if they were put together, puts them in different groups, and then adds the other entries one by one, each time taking the entry with the strongest preference for one group. It runs in $O(M^2)$ time, which is small for nodes of tens of entries, and gives splits close to the best of the exponential search in practice. Antonin Guttman gave it in 1984 as the default split of the R-tree.

## In plain words

You have too many boxes in one bag and must put them into two bags. You want the two bags to be as small as possible.

First, find the two boxes that fit worst together: the pair for which one bag around both would hold the most empty space. Put one in each bag. Then, again and again, look at the boxes that are left and take the one that cares most which bag it goes into: the box for which one bag would grow much less than the other. Put it in the bag that grows less.

Each bag must end with at least $m$ boxes. When one bag needs all the remaining boxes to reach $m$, give them all to it.

## The problem

Given $n \ge 2$ closed rectangles $E_1, \ldots, E_n$ in $\mathbb{R}^d$ (in the R-tree, $n = M + 1$) and a minimum fill $m$ with $1 \le m \le n/2$, find a partition into two groups $G_1, G_2$ with $|G_1|, |G_2| \ge m$ that makes
$$\operatorname{area}(\operatorname{MBR}(G_1)) + \operatorname{area}(\operatorname{MBR}(G_2))$$
small, where $\operatorname{MBR}(G)$ is the smallest box that contains the rectangles of $G$. Guttman chose the total area as the measure, because a query point falls into a node in proportion to its area. Finding the best partition is the [R-tree node splitting](/r-tree-node-splitting/) problem; the quadratic split is a heuristic for it, not an exact algorithm.

The *waste* of a pair is $w(E_i, E_j) = \operatorname{area}(\operatorname{MBR}(E_i, E_j)) - \operatorname{area}(E_i) - \operatorname{area}(E_j)$, the area of the box around both that neither covers, up to their overlap. The *enlargement* of a group $G$ by an entry $E$ is $\operatorname{area}(\operatorname{MBR}(G \cup \{E\})) - \operatorname{area}(\operatorname{MBR}(G))$.

## The algorithm

```pseudo id=main
QUADRATIC-SPLIT(E1, ..., En, m)
L1  for each pair i < j: compute the waste w(Ei, Ej)        ▷ PICK-SEEDS
L2  take the pair (i, j) of largest waste; G1 ← {Ei}, G2 ← {Ej}
L3  while some entries are not assigned:
L4      if a group needs all the remaining entries to reach m then assign them all to it; stop
L5      for each remaining entry E: d1 ← enlargement of G1 by E; d2 ← enlargement of G2 by E   ▷ PICK-NEXT
L6      take the entry E with the largest |d1 − d2|
L7      add E to the group with the smaller enlargement; on a tie, to the group of smaller area, then to the one with fewer entries
L8  return G1, G2
```

Line L1 is the quadratic part: it compares all $\binom{n}{2}$ pairs. A pair with a large waste is a pair whose box would be mostly empty, so it is a bad idea to put the two in one node; the seeds start two groups that are far apart. Line L6 takes the entry whose choice matters most, so that the entries that clearly belong to one group are placed while that group is still small, and the hard cases come last. Line L4 keeps the minimum fill: it stops the greedy step as soon as one group can reach $m$ only by taking all that is left.

Guttman's *linear split* replaces both steps by cheaper ones: the seeds are the pair with the largest separation along some axis, normalized by the width of the whole set, and the remaining entries are taken in any order. It runs in $O(dn)$ time and gives somewhat worse splits.

## Example

Take $m = 2$ and the five rectangles of an overflowing node with $M = 4$, written as $[x_1, x_2] \times [y_1, y_2]$: a $= [0, 2] \times [0, 2]$, b $= [1, 3] \times [5, 7]$, c $= [6, 8] \times [0, 1]$, d $= [7, 9] \times [6, 9]$ and e $= [2, 3] \times [1, 3]$. Their areas are 4, 4, 2, 6 and 2.

**Seeds.** The wastes are

| pair | waste | pair | waste |
|---|---|---|---|
| a, b | 13 | b, d | 22 |
| a, c | 10 | b, e | 6 |
| a, d | 71 | c, d | 19 |
| a, e | 3 | c, e | 14 |
| b, c | 43 | d, e | 48 |

The largest is a and d: the box $[0, 9] \times [0, 9]$ has area 81, and $81 - 4 - 6 = 71$. So $G_1 = \{a\}$ with box area 4, and $G_2 = \{d\}$ with box area 6.

**Round 1.** The remaining entries are b, c and e.

| entry | $d_1$ (join a) | $d_2$ (join d) | $\lvert d_1 - d_2 \rvert$ |
|---|---|---|---|
| b | $21 - 4 = 17$ | $32 - 6 = 26$ | 9 |
| c | $16 - 4 = 12$ | $27 - 6 = 21$ | 9 |
| e | $9 - 4 = 5$ | $56 - 6 = 50$ | 45 |

e has the strongest preference and goes to $G_1$, whose box becomes $[0, 3] \times [0, 3]$, area 9.

**Round 2.** For b, $d_1 = 21 - 9 = 12$ and $d_2 = 26$; for c, $d_1 = 24 - 9 = 15$ and $d_2 = 21$. b has the larger difference, 14 against 6, and goes to $G_1$, whose box becomes $[0, 3] \times [0, 7]$, area 21.

**Round 3.** One entry, c, is left, and $G_2$ has 1 entry, so it needs c to reach $m = 2$: line L4 puts c in $G_2$. The result is $G_1 = \{a, e, b\}$ with box $[0, 3] \times [0, 7]$ and $G_2 = \{d, c\}$ with box $[6, 9] \times [0, 9]$, total area $21 + 27 = 48$.

**A case where it is not optimal.** Take $m = 2$ and A $= [4, 6] \times [0, 1]$, B $= [7, 8] \times [7, 9]$, C $= [0, 3] \times [4, 6]$ and D $= [1, 2] \times [5, 6]$, where D lies inside C. The largest waste is 32, for both the pair A, B and the pair B, C, and the first pair found is A and B, so they become the seeds. Then C goes with A ($d_1 = 34$, $d_2 = 38$), and D must go with B to fill it. The total area is $36 + 28 = 64$. The best split is $\{A, B\}$ and $\{C, D\}$, with total area $36 + 6 = 42$: it puts the two seeds together, which the quadratic split never does.

## Correctness

The output is a valid split: each entry is put in exactly one group, both groups start with one seed, and the test of line L4 ensures that each group ends with at least $m$ entries. The argument is a count: as long as neither group has triggered line L4, each group $G$ has $|G| + r > m$, where $r$ is the number of remaining entries, and one step lowers $|G| + r$ by at most 1; so the sum is at least $m$ when line L4 fires or when $r = 0$. The seeds are a pair of largest waste by lines L1 and L2. The quadratic split makes no claim of optimality, and the example above shows that it is not optimal. The full proof is in the proofs folder.

## Complexity

The model is the word RAM, with a rectangle in $d$ dimensions as $2d$ numbers, so the area of a box costs $O(d)$.

- **Seeds.** $\binom{n}{2}$ pairs, $O(d)$ each: $O(d n^2)$.
- **Assignment.** At most $n - 2$ rounds, each of which computes two enlargements for each remaining entry: $O(d n)$ per round, $O(d n^2)$ in total.
- **Total.** $O(d n^2)$ time, and $O(n)$ extra space for the groups and the list of remaining entries. For $n = M + 1$, this is $O(d M^2)$ per split.

In an R-tree, a split happens on at most one node per level of an insertion, so the split adds $O(d M^2 \log_m n)$ to an insertion in the worst case, and much less on average, since most insertions do not split.

## Properties

- **Deterministic.** With a fixed order of the entries and fixed rules for ties, the result depends only on the input.
- **Seeds never share a group.** The two seeds start different groups and stay there. This is the reason for the bad case above.
- **Uneven groups.** Once one group has a large box, most entries prefer it, since its enlargement is small. So the quadratic split tends to make one large group and one group of the minimum size $m$. Beckmann and others observed this and made it one of the reasons for the [R*-tree](/r-star-tree/) split.
- **Only area.** It does not look at overlap between the two boxes or at their margins, which the R*-tree split uses.

## Variants and improvements

- **Linear split.** Guttman's $O(dn)$ split: seeds by the largest normalized separation along any axis, and the other entries in any order. Ang and Tan later proposed a different linear split that assigns entries by their distance to the sides of the node.
- **Exhaustive split.** Try all $2^{n-1}$ partitions with enough entries in each group and keep the best. It is exact for the measure, and only usable for small $n$.
- **R*-tree split.** Sort along each axis, choose the axis with the smallest sum of margins, and on it the distribution with the least overlap. It runs in $O(d n \log n)$ time and gives better trees. See the [R*-tree](/r-star-tree/).
- **Other measures.** The same greedy method works with the margin (the perimeter) or the overlap in place of the area, or with a weight on balance.
- **Split history.** The [X-tree](/x-tree/) keeps the history of splits and may refuse a split with too much overlap, making a larger node instead.

## When to use it

Use the quadratic split in a dynamic R-tree when nodes hold up to some tens of entries and simplicity matters, for example in an in-memory R-tree of a game or a small library. Use the R*-tree split when queries matter more than insertion time, which is the case in most databases. For data that is loaded once, use [STR packing](/str-packing/) or another bulk load, which builds full nodes and needs no splits.

## Pitfalls

- **Forgetting the minimum fill.** Without line L4, the greedy step can put all entries in one group, and the other node has one entry, which breaks the R-tree invariant.
- **Negative waste.** If two rectangles overlap, the waste can be negative, as for C and D above, where it is $-1$. Do not use the absolute value: the seeds are the pair with the largest signed waste.
- **Degenerate rectangles.** Points and segments have area 0. Then many enlargements are 0 and all ties go to the first group, which makes a bad split. Use a tie rule that looks at the margin or at the group size, or use a small positive size for points.
- **Recomputing boxes.** The group boxes must be updated after each assignment, as in line L7. Using the seed boxes for all rounds gives a different and worse split.
- **Cost of area in high dimensions.** Volumes in high dimensions become very small or very large and lose meaning; the split then behaves badly. Use the margin or a structure made for high dimensions, such as the [X-tree](/x-tree/).

## Implementations

## History

Antonin Guttman gave three node splits in his 1984 R-tree paper: an exhaustive split, the quadratic split and the linear split, and found in tests that the linear split was nearly as good as the quadratic one for searches while much faster to insert. Later studies, among them those of Greene in 1989 and of Beckmann, Kriegel, Schneider and Seeger in 1990, found that the quadratic split gives clearly better trees than the linear one, and proposed the split of the R*-tree, which most systems now use. The quadratic split is still the default in several R-tree libraries.

## References
