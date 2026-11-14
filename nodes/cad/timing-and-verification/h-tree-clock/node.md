---
tag: EFPFNF
kind: definition
slug: h-tree-clock
name: H-tree clock network
aliases:
- H-tree clock distribution
area: cad/timing-and-verification
level: intro
summary: A recursive H-shaped clock tree that gives equal path lengths to sinks on a regular grid, but is wasteful for sinks placed unevenly.
prereqs: [complete-binary-tree, elmore-delay]
see_also: [clock-tree-synthesis, method-of-means-and-medians, tsay-zero-skew, deferred-merge-embedding, rc-tree, rectilinear-minimum-spanning-tree, rectilinear-steiner-tree-problem, setup-and-hold-constraints]
sources:
  - paper: "H. B. Bakoglu, J. T. Walker and J. D. Meindl, A symmetric clock-distribution tree and optimized high-speed interconnections for reduced clock skew in ULSI and WSI circuits, Proceedings of the IEEE International Conference on Computer Design (ICCD), 118 to 122, 1986"
    locator: the symmetric H-shaped clock distribution tree
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 2011
    locator: Chapter 7, Specialized Routing, Section 7.5.1, on H-trees and other clock tree constructions
  - book: isbn:9780849372421
    title: Charles J. Alpert, Dinesh P. Mehta and Sachin S. Sapatnekar (editors), Handbook of Algorithms for Physical Design Automation, CRC Press, 2008
    locator: Chapter 42, Clock Network Design, Basics
---

An H-tree is a clock routing structure: a wire tree that starts at the centre of a square and splits again and again in the shape of the letter H, so that its $4^k$ ends lie at the centres of a regular grid of cells. Every path from the centre to an end has the same length and passes through copies of the same subtrees, so with equal loads at the ends the [Elmore delay](/elmore-delay/) to every end is the same and the skew is zero. It works well when the sinks, or local buffers that drive them, sit on a regular grid, and it wastes wire when the sinks are placed unevenly. Bakoglu, Walker and Meindl described it as a clock distribution tree in 1986.

## Definition

**H-tree of order 1.** In a square of side $D$ with centre $o$, the H-tree of order 1 is the union of three segments: a horizontal bar of length $D / 2$ centred at $o$, and two vertical bars of length $D / 2$ centred at its ends. Its four *ends* are the ends of the vertical bars, which are the centres of the four quadrants of the square. The clock enters at $o$.

**H-tree of order $k$.** For $k \ge 2$, the H-tree of order $k$ is the H-tree of order 1 in the square, together with an H-tree of order $k - 1$ in each of the four quadrants of side $D / 2$, whose centre is an end of the first H. Its ends are the $4^k$ centres of the cells of side $D / 2^k$ that tile the square.

As a graph, the H-tree of order $k$ is a [complete binary tree](/complete-binary-tree/) of depth $2k$ rooted at $o$: each H splits once along its horizontal bar and once more along each vertical bar. An *H-tree clock network* routes the clock along this tree from a driver at $o$ to the sinks at its ends, usually with buffers at some of the branch points. When the sinks do not sit at the ends, each sink is joined to an end by a short local wire.

**Lengths.** For the H-tree of order $k$ in a square of side $D$,
$$ \text{wire length} = \sum_{i = 1}^{k} 4^{i - 1} \cdot \frac{3}{2} \cdot \frac{D}{2^{i - 1}} = \frac{3}{2} D \,(2^k - 1), \qquad \text{path length to each end} = \sum_{i = 1}^{k} \frac{D}{2^i} = D \,(1 - 2^{-k}). $$
The H of level $i$ has a horizontal bar and two vertical bars of length $D / 2^i$ each, and a path uses half of one bar of each kind, $D / 2^{i + 1}$ twice.

**Zero skew.** The four quadrant subtrees of an H-tree are translates of each other, and the two halves of each bar carry the same downstream subtrees. Under the Elmore delay of the [RC tree model](/rc-tree/), with the same wire width at each level and equal loads at the ends, the delay to an end is a sum over the edges of its path of the edge resistance times the downstream capacitance, and these terms are the same for all ends. So all $4^k$ ends get the same delay. This is exact in the model; on silicon, process variation and unequal loads still cause skew.

## Examples and non-examples

**Example: 16 sinks on a grid.** In a square of side $D = 8$, the H-tree of order 2 has its ends at the 16 points $(x, y)$ with $x, y \in \{1, 3, 5, 7\}$. The first H has bars of length 4, so 12 units of wire; each of the four H's of level 2 has bars of length 2, so 6 units each. The total is $12 + 24 = 36 = \frac{3}{2} \cdot 8 \cdot (2^2 - 1)$. Every path from the centre $(4, 4)$ has length $2 + 2 + 1 + 1 = 6 = 8 (1 - 1/4)$, so the skew is zero.

**Example: the price of equal paths.** For $N = 4^k$ sinks at the cell centres with spacing $s = D / 2^k$, a comb, one row of wire with a column of wire through each column of sinks, connects them with $(N - 1) s$ wire, the length of a [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) of the grid. The H-tree uses $\frac{3}{2} \sqrt N (\sqrt N - 1) s$, so the ratio is $\frac{3}{2} \sqrt N / (\sqrt N + 1)$, which is $1.2$ for 16 sinks and tends to $1.5$. The comb pays for this with skew: driven at one end of its row, its paths range from 0 to $2 (\sqrt N - 1) s$, almost $2 D$.

**Non-example: sinks in one corner.** Take the square of side 8 and four sinks at $(6, 6)$, $(6, 7)$, $(7, 6)$ and $(7, 7)$, with the clock at $(4, 4)$. The H-tree of order 1 has ends at $(2, 2)$, $(2, 6)$, $(6, 2)$ and $(6, 6)$. Joining each sink to its own end with local wires of lengths 0, 5, 5 and 10 gives paths of length 4, 9, 9 and 14, a skew of 10, and 32 units of wire. A small H-tree of order 1 in the square of side 2 centred at $(6.5, 6.5)$, with bars of length 1 and 3 units of wire, fed by 5 units of wire from $(4, 4)$, gives every sink a path of length 6, zero skew and 8 units of wire. The H-tree follows the shape of the chip, not the positions of the sinks.

**Non-example: a grid that is not a power of 4.** For a $3 \times 3$ grid of sinks, or a chip that is not square, no H-tree has its ends at the sinks. Some ends get no sink or two sinks, and the local wires differ in length, so in general the skew is no longer zero. Trees that follow the sinks, such as the [method of means and medians](/method-of-means-and-medians/), or exact methods such as [Tsay's zero-skew algorithm](/tsay-zero-skew/) with [deferred-merge embedding](/deferred-merge-embedding/), handle such sets.

**Non-example: an H-shaped tree with unequal loads.** An H-tree of order 2 in which one end drives a load of 2 units of capacitance and the other 15 ends drive 1 unit has equal path lengths but not equal Elmore delays, since the downstream capacitance differs between the halves of a bar. Equal length is not equal delay.

## Related definitions

- **[Clock tree synthesis](/clock-tree-synthesis/).** The problem of building a clock tree to a given set of sinks with low skew, latency and power. The H-tree is its oldest regular answer.
- **Clock skew.** The difference between the arrival times of the clock at two registers; the [setup and hold constraints](/setup-and-hold-constraints/) say how much of it a pair of registers can take.
- **Zero-skew tree.** A clock tree in which the delays from the root to all sinks are equal under a stated delay model. The H-tree is one on a regular grid; [Tsay's algorithm](/tsay-zero-skew/) builds one for any sinks and topology.
- **[Method of means and medians](/method-of-means-and-medians/).** A recursive clock router that splits the sinks at their median and joins the centres of mass. On the cell centres of a $2^k \times 2^k$ grid it gives the H-tree.
- **Clock mesh and spine.** Other clock networks: a grid of wires shorted together, or a few long trunks with short branches. They trade more wire and power for less sensitivity to variation.
- **H-tree layout.** The same recursive H embeds a complete binary tree with $n$ leaves in a grid of area $O(n)$, a classical result of VLSI layout theory.
- **[Rectilinear Steiner tree](/rectilinear-steiner-tree-problem/).** The shortest rectilinear tree that connects the sinks, with no condition on the paths. It is the wire length lower bound that an H-tree gives up for equal paths.

## References
