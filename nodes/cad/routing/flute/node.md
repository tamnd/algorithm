---
tag: Q78Z3D
kind: algorithm
slug: flute
name: FLUTE
aliases:
- fast lookup table Steiner tree
area: cad/routing
level: advanced
summary: Chu and Wong's rectilinear Steiner tree method that looks up optimal trees for nets of up to nine pins in precomputed tables and splits larger nets into smaller ones.
solves: [rectilinear-steiner-tree-problem]
model: real-ram
complexity:
  vars: {n: the number of pins, D: the largest degree with a table}
  time: {table_lookup: O(1), worst: O(n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, exact: false}
history:
  year: 2004
  people: [Chris Chu, Yiu-Chung Wong]
  note: Chu presented lookup tables of wirelength vectors for wirelength estimation at ICCAD 2004. Chu and Wong turned it into a Steiner tree algorithm at ISPD 2005, and the journal version with a new net breaking method appeared in 2008.
prereqs: [hanan-theorem, rectilinear-minimum-spanning-tree]
see_also: [rectilinear-steiner-tree-problem, hanan-theorem, iterated-one-steiner, rectilinear-minimum-spanning-tree, half-perimeter-wirelength, pareto-optimality, global-routing, placement-problem]
sources:
  - paper: doi:10.1109/TCAD.2007.907068
    title: Chris Chu and Yiu-Chung Wong, FLUTE, fast lookup table based rectilinear Steiner minimal tree algorithm for VLSI design, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 27(1), 70 to 83, 2008
    locator: the position sequence, the wirelength vectors, the lookup tables up to degree 9, the net breaking and the accuracy parameter
  - paper: doi:10.1109/ICCAD.2004.1382665
    title: Chris Chu, FLUTE, fast lookup table based wirelength estimation technique, Proceedings of ICCAD 2004, 696 to 701
    locator: the first form of the lookup tables, for wirelength estimation
  - paper: doi:10.1145/1055137.1055145
    title: Chris Chu and Yiu-Chung Wong, Fast and accurate rectilinear Steiner minimal tree algorithm for VLSI design, Proceedings of ISPD 2005
    locator: the conference version of the Steiner tree algorithm
  - paper: doi:10.1137/0114025
    title: M. Hanan, On Steiner's problem with rectilinear distance, SIAM Journal on Applied Mathematics 14(2), 255 to 265, 1966
    locator: the theorem that some optimal tree lies on the grid of lines through the pins
---

FLUTE (fast lookup table estimation) is a method of Chris Chu and Yiu-Chung Wong that builds rectilinear Steiner trees for the nets of a chip in electronic design automation (EDA). Most nets have few pins, and for a small net the optimal tree depends only on the order of the pins in $x$ and in $y$ and on the gaps between their coordinates. FLUTE stores, for every such order, a short list of *wirelength vectors*, each a formula for the length of a candidate tree in terms of the gaps, together with the tree. A lookup evaluates these few formulas and takes the shortest, which gives an optimal tree for nets of up to 9 pins in the published tables. Larger nets are broken into smaller ones until the tables apply, so for them the result is a heuristic. The method is used in placement and global routing tools, where millions of nets must be estimated many times.

## In plain words

Take a net of four pins. Sort the pins from left to right, and note their order from bottom to top. This gives one of $4! = 24$ patterns. Two nets with the same pattern are stretched copies of each other.

For each pattern, the best wire can only have a few shapes. The length of each shape is a sum of the gaps between neighboring columns and rows, with some gaps counted twice. So for each pattern we write down a short list of formulas, once, before any chip is seen.

For a real net, find its pattern, put its gaps into the formulas, and take the smallest result. That is the length of the best tree.

A net with many pins has too many patterns for a table. Split it into smaller nets that share a pin, and join their trees.

## The problem

The input is a net, a set $P$ of $n$ pins in the plane. The output is a rectilinear Steiner tree of $P$, a tree of horizontal and vertical wires that joins all pins, possibly through extra Steiner points, of small total length. The optimum is the rectilinear Steiner minimal tree, and finding it is NP-hard for general $n$, see the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/).

Sort the pins by $x$, with ties by $y$, and sort them by $y$, with ties by $x$. The *position sequence* $\pi$ records, for the pin of $x$ rank $i$, its $y$ rank $\pi(i)$. Let $x_1 \le \cdots \le x_n$ and $y_1 \le \cdots \le y_n$ be the sorted coordinates, and let the gaps be $h_i = x_{i+1} - x_i$ and $v_j = y_{j+1} - y_j$. Every pin lies on the $n \times n$ grid of these coordinates. By [Hanan's theorem](/hanan-theorem/) some optimal tree lies on this grid, so its length is

$$\sum_{i=1}^{n-1} a_i h_i + \sum_{j=1}^{n-1} b_j v_j,$$

where $a_i$ and $b_j$ count how many wires cross the column gap $i$ and the row gap $j$. The integer vector $(a, b)$ is the *wirelength vector* of the tree. It depends only on the tree on the grid, and the same grid tree exists for every net with the sequence $\pi$.

## The algorithm

The tables are built once, offline. For each degree $d \le D$ and each position sequence $\pi$ of length $d$, the table holds the wirelength vectors of trees on the grid that can be optimal for some gaps, and for each vector one tree. A vector that is at least another vector in every entry can never be the only best one, since the gaps are not negative, so it can be dropped.

```pseudo id=main
FLUTE(P, D)
L1  if |P| ≤ D then
L2      π ← the position sequence of P;  g ← the gaps (h_1, …, h_{n−1}, v_1, …, v_{n−1})
L3      (a, S) ← the entry of table[π] with the least a · g
L4      return MST(P ∪ S), with the Steiner points S placed at their grid coordinates
L5  best ← none
L6  for each axis in {x, y} do
L7      split P at the pin of median rank on this axis into two nets that share that pin
L8      solve both nets by FLUTE(·, D);  if their total length is less than that of best then best ← this pair
L9  return the union of the two trees of best
```

The implementation on this page builds its own tables for $D = 4$ with the Dreyfus-Wagner recursion of the [Steiner tree problem](/steiner-tree-problem/) in graphs, run on the $d \times d$ grid, where costs are vectors instead of numbers and each set of vectors is cut down to the vectors that no other vector is at most in every entry, its [Pareto](/pareto-optimality/) minima. For degree 4 this gives 40 vectors over the 24 position sequences: 8 sequences have one vector and 16 have two. The published FLUTE tables go to $D = 9$ and come with their own generation method. The net breaking of lines L5 to L9 is a simplified form: FLUTE chooses the breaking pin by a score and has an accuracy parameter that tries more ways to break the net.

## Example

Take the four pins $(0, 0)$, $(2, 4)$, $(3, 1)$ and $(6, 5)$. In order of $x$ their $y$ ranks are $0, 2, 1, 3$, so $\pi = (0, 2, 1, 3)$. The gaps are $h = (2, 1, 3)$ and $v = (1, 3, 1)$. The table for this sequence has two vectors.

| vector $(a; b)$ | meaning | length here |
| --- | --- | --- |
| $(1, 2, 1;\ 1, 1, 1)$ | the middle column gap is crossed twice | $2 + 2 + 3 + 1 + 3 + 1 = 12$ |
| $(1, 1, 1;\ 1, 2, 1)$ | the middle row gap is crossed twice | $2 + 1 + 3 + 1 + 6 + 1 = 14$ |

The first vector wins. Its tree has one Steiner point at the grid point of column 1 and row 1, which is $(2, 1)$, and the edges $(0,0)$ to $(2,1)$ of length 3, $(2,1)$ to $(3,1)$ of 1, $(2,1)$ to $(2,4)$ of 3 and $(2,4)$ to $(6,5)$ of 5, total 12. The half perimeter of the bounding box is $6 + 5 = 11$, and every tree here must pay one gap more, the smaller of $h_2 = 1$ and $v_2 = 3$.

Now stretch the same pattern: the pins $(0, 0)$, $(1, 3)$, $(5, 2)$ and $(6, 5)$ have the same $\pi$, with $h = (1, 4, 1)$ and $v = (2, 1, 2)$. The first vector gives $1 + 8 + 1 + 5 = 15$ and the second gives $6 + 2 + 2 + 2 = 12$, so now the second tree wins, with its Steiner point at $(1, 2)$. The same two formulas cover every net with this pattern.

On the five pins $(0, 0)$, $(4, 1)$, $(1, 4)$, $(5, 5)$ and $(2, 3)$ the implementation breaks the net and returns length 13, the optimum, with Steiner points $(1, 3)$ and $(4, 3)$.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Lengths are linear in the gaps.** Every tree on the grid of a sequence $\pi$ has a length $a \cdot g$ for an integer vector that does not depend on the gaps.
- **The table gives the optimum.** For a net with $n \le D$ pins, the least $a \cdot g$ over the table is the length of a rectilinear Steiner minimal tree. This uses Hanan's theorem and the fact that dropping a vector that another vector is at most in every entry never loses the minimum when $g \ge 0$. Repeated coordinates give zero gaps and are covered by the same formula.
- **The vector recursion is right.** The Dreyfus-Wagner recursion with sets of vectors gives, for every $g \ge 0$ at once, the optimal Steiner tree length in the grid graph, because each step is a sum or a minimum and both commute with the linear map $a \mapsto a \cdot g$.
- **Net breaking gives a tree.** Two trees that share a pin form one tree that spans all pins, and its length is the sum of the two. It is an upper bound, not the optimum.

## Complexity

- **Lookup.** For $n \le D$ the work is two sorts of $n$ pins and one dot product of length $2(n - 1)$ per table entry. For a fixed $D$ this is $O(1)$, and for small nets it is about as fast as a rectilinear minimum spanning tree.
- **Net breaking here.** The simple breaking of this page solves four nets of about half the size at each level, two per axis, so $T(n) = 4T(n/2 + 1) + O(n \log n)$, which is $O(n^2)$. FLUTE breaks nets with its own scores, and its paper reports run times close to those of a fast rectilinear MST code on the ISPD98 circuits.
- **Tables.** A table of degree $d$ has $d!$ position sequences. The size grows fast with $d$, which is one reason why the published tables stop at $d = 9$. The construction here builds the table of one sequence when it is first needed and caches it.

## Properties

- **What is proved.** For nets of at most $D$ pins the result is optimal. For larger nets the result is a valid rectilinear Steiner tree, with no proved bound on its ratio to the optimum.
- **What the authors report.** The 2008 paper says that FLUTE is optimal up to degree 9 in its implementation, and very accurate up to degree 100, and that with the default accuracy it was more accurate than the batched form of [iterated 1-Steiner](/iterated-one-steiner/) and almost as fast as Prim's rectilinear MST on the nets of 18 ISPD98 circuits.
- **What is measured here.** With tables only up to $D = 4$ and the simple breaking, on random nets with coordinates from 0 to 99 (Python `random.Random(2026)`), compared with the brute-force optimum: for 200 nets of 5 pins the mean ratio was 1.0476, the worst 1.3396, and 105 nets were optimal; for 25 nets of 6 pins the mean was 1.0457, the worst 1.20, and 13 were optimal. These are toy inputs, not benchmark results, and they are much worse than FLUTE itself, because real FLUTE looks up nets of 5 to 9 pins in its tables.
- **Deterministic.** Ties in the table go to the first entry, and ties in the breaking go to the $x$ axis.

## Variants and improvements

- **Accuracy parameter.** FLUTE has a parameter that controls how many ways a large net is broken and which result is kept, a tradeoff between time and length set by the user.
- **Wirelength only.** The first form of 2004 was aimed at wirelength estimation, which is what a placement tool needs most of the time. The trees themselves are needed for routing.
- **Larger nets.** Later work extended the method to nets with many pins, with other ways to break the net and to improve the joined trees.
- **Other tools.** Placement tools that want a cheaper estimate use the [half-perimeter wirelength](/half-perimeter-wirelength/), which is exact only for nets of up to 3 pins.

## When to use it

- When the Steiner tree length of millions of small nets is needed over and over, in placement and [global routing](/global-routing/).
- When most nets have fewer than 10 pins, which is common in chips.

For one large net where the length matters more than the time, [iterated 1-Steiner](/iterated-one-steiner/) or an exact solver can do better. When only a bound is needed, the [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) is simpler.

## Pitfalls

- **Ties in coordinates.** Pins that share an $x$ or a $y$ value need a fixed rule for their ranks. The formula still holds with zero gaps, but the code must map the grid points of the tree back to coordinates with the sorted lists, not with the pin index.
- **Steiner points on pins.** With zero gaps, a grid Steiner point can fall on a pin. Remove such points before building the tree.
- **Calling the breaking exact.** The result for a net larger than $D$ is a heuristic. Two halves that are each optimal do not make an optimal whole.
- **Table size.** Building tables for large $d$ is expensive in time and memory, since there are $d!$ sequences. Use symmetry, or ship the precomputed tables.

## Implementations

## History

M. Hanan showed in 1966 that the grid of lines through the pins contains an optimal rectilinear Steiner tree, which makes the set of tree shapes for a net finite and dependent only on the order of the pins. Chris Chu presented FLUTE at ICCAD 2004 as a fast and accurate way to estimate the wirelength of nets in placement, with lookup tables of wirelength vectors for small nets. Chu and Yiu-Chung Wong turned it into a Steiner tree algorithm at ISPD 2005. The journal version of 2008 added a new net breaking method and a parameter that trades time for accuracy. FLUTE became a standard Steiner tree routine inside academic placers and global routers.

## References
