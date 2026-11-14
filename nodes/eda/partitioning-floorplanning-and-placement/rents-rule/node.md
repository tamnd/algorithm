---
tag: C7EEZD
kind: concept
slug: rents-rule
name: Rent's rule
aliases:
- Rent exponent
area: eda/partitioning-floorplanning-and-placement
level: core
summary: The empirical law T = t g^p between the number of terminals T and gates g of a block of a circuit, which predicts wire length and cut sizes.
prereqs: [hypergraph, hypergraph-partitioning]
see_also: [hypergraph-partitioning, min-cut-placement, placement-problem, half-perimeter-wirelength, graph-partitioning-problem, planar-separator-theorem, linear-regression]
sources:
  - paper: doi:10.1109/T-C.1971.223159
    title: B. S. Landman and R. L. Russo, On a pin versus block relationship for partitions of logic graphs, IEEE Transactions on Computers C-20(12), 1469 to 1479, 1971
    locator: the statement of the rule, the partitioning experiments on logic graphs, the exponents measured for them (0.57 to 0.75), and Region II, where the rule fails for large blocks
  - paper: "W. E. Donath, Placement and average interconnection lengths of computer logic, IEEE Transactions on Circuits and Systems CAS-26(4), 272 to 277, 1979"
    locator: the estimate of the average wire length of a placement from the Rent exponent, with its three regimes p < 1/2, p = 1/2 and p > 1/2
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 2, Netlist and System Partitioning (the note on Rent's rule in the introduction; general locator)
---

Rent's rule is the observation that, for the blocks of a well-designed digital circuit, the number of terminals $T$ of a block grows as a power of the number of gates $g$ in it, $T = t \, g^p$. Here $t$ is the average number of terminals of one gate and $p$ is the *Rent exponent*, with $0 \le p \le 1$. The rule is empirical, not a theorem: it holds over a range of block sizes for circuits that were built hierarchically and for blocks found by a good partitioner. E. F. Rent wrote it down in internal IBM memos in 1960, and Landman and Russo published it in 1971, with exponents between 0.57 and 0.75 for the logic they studied. Some authors write $T = k G^p$ or $n_P = t \, n_G^r$ for the same law.

## In plain words

Cut a circuit into pieces, and count for each piece how many parts it holds and how many wires leave it. A small piece has few wires going out. A big piece has more, but not in proportion: most wires inside a well-made circuit are short and stay inside the piece. If you plot the numbers on log paper, the points lie close to a straight line. The slope of that line is the Rent exponent.

A slope near 0 means that pieces hardly talk to the rest, like a long chain. A slope of one half is what a flat grid of parts gives. A slope near 1 means that the wires go everywhere, so cutting the circuit never helps. Real logic sits between one half and three quarters. The slope tells a designer how long the wires will be and how many wires each cut will cross.

## The idea

**The quantities.** Take a netlist, a [hypergraph](/hypergraph/) of gates and nets. For a block $B$ of $g$ gates, its terminals are the nets that have a pin in $B$ and a pin outside $B$, plus the primary inputs and outputs of the circuit on gates of $B$. Let $T(B)$ be their number. Partition the netlist again and again, for example by [min-cut bisection](/hypergraph-partitioning/), and record $(g, T)$ for every block. Rent's rule says that

$$ T \approx t \, g^p, \qquad \text{that is,} \qquad \log T \approx \log t + p \log g. $$

The constants $t$ and $p$ are fitted to the points, usually by least squares on the logarithms (see [linear regression](/linear-regression/)), or by the averages of $T$ over the blocks at each level of the partition.

**The exponent depends on the partitioner.** $T(B)$ is a property of the block, not only of the circuit. A poor partition makes $T$ larger at every size and so gives a larger fitted $p$. A Rent exponent is therefore a statement about a circuit and a partitioning method together. Good min-cut partitioners give the smallest values.

**Region I and Region II.** Landman and Russo found that the rule fits for blocks up to a fraction of the whole circuit (Region I). For the few largest blocks, $T$ grows more slowly than the line or even falls (Region II), because the whole circuit has only as many terminals as its package has pins, and a block that is half the circuit cannot have more terminals than the circuit and its other half allow.

**Why a power law: the geometric view.** Suppose the gates sit on a $d$-dimensional grid with wires only between neighbors. A cube of side $k$ holds $g = k^d$ gates, and its terminals are the wires that cross its surface, about $2 d \, k^{d-1} = 2 d \, g^{(d-1)/d}$. So a $d$-dimensional circuit has $p = (d - 1)/d$: $p = 0$ for a chain, $p = 1/2$ for a planar grid and $p = 2/3$ for a 3D grid. An exponent above $1/2$ means that the circuit has more wires leaving a block than a planar grid of the same size would have. In that sense such a circuit does not fit a plane without long wires.

**Consequences for wire length.** Donath (1979) placed a circuit with Rent exponent $p$ on a grid by recursive partitioning and estimated the average length of a wire, in units of the gate pitch, as a function of the number $g$ of gates:

- if $p < 1/2$, the average wire length stays bounded as $g$ grows;
- if $p = 1/2$, it grows as $\log g$;
- if $p > 1/2$, it grows as $g^{p - 1/2}$.

This estimate assumes the rule at all scales and a placement that follows the partition hierarchy. It is a model, and measured wire lengths of real placements depart from it, but it explains why the Rent exponent of a design predicts its wiring demand.

**Not a law of nature.** Random netlists, where each net picks its pins uniformly at random, have $p$ close to 1, because a block of half the gates already cuts a constant fraction of the nets. Highly regular structures such as memories have small $p$. The rule describes the netlists that people design, which are hierarchical and local.

## Examples

**A planar grid of gates.** Put $16 \times 16$ gates on a grid and join each gate to its four neighbors by 2-pin nets. Cut it by alternating vertical and horizontal bisections. An interior block of $k \times k$ gates has $4k$ nets that leave it.

| block | $g$ | $T$ (interior block) | $4 \sqrt{g}$ |
| --- | --- | --- | --- |
| $1 \times 1$ | 1 | 4 | 4 |
| $2 \times 2$ | 4 | 8 | 8 |
| $4 \times 4$ | 16 | 16 | 16 |
| $8 \times 8$ | 64 | 32 | 32 |
| $16 \times 16$ | 256 | 0 | 64 |

The first four rows fit $T = 4 g^{1/2}$ exactly, so $t = 4$ and $p = 1/2$. Blocks on the edge of the grid have fewer terminals: an $8 \times 8$ quarter has only 16. The last row is Region II in its simplest form: the whole circuit has no nets leaving it, unless it has primary inputs and outputs.

**A chain.** Gates $1, \ldots, g$ in a row with a net between each pair of neighbors. Every block of consecutive gates has at most 2 terminals, so $T \le 2 = 2 g^0$ and $p = 0$. A block of gates that are not consecutive has more terminals, which shows how the partition changes the exponent.

**A 3D grid.** A cube of $k \times k \times k$ gates with neighbor nets has $6 k^2 = 6 g^{2/3}$ terminals, so $p = 2/3$, inside the range that Landman and Russo measured for logic.

**Reading a fit.** If the blocks of a design have on average $T = 40$ at $g = 100$ and $T = 160$ at $g = 1600$, then $p = \log(160/40) / \log(1600/100) = \log 4 / \log 16 = 1/2$ and $t = 40 / 100^{1/2} = 4$.

## Where it is used

- **Wire length and interconnect prediction.** Before placement, estimate the distribution and the average of the wire lengths from $t$ and $p$, as in Donath's model, to size the routing resources and to plan the layers.
- **Partitioning and packaging.** Estimate how many pins a chip, a board or a block of an FPGA needs for a given amount of logic, and so how many parts a system must be split into.
- **Evaluating partitioners and placers.** A better [hypergraph partitioner](/hypergraph-partitioning/) yields fewer terminals per block and a lower fitted exponent. In [min-cut placement](/min-cut-placement/) the rule estimates the number of nets that cross the cut lines at each level, and the sum of these numbers is the total [HPWL](/half-perimeter-wirelength/).
- **Synthetic benchmarks.** Generators of artificial netlists choose a target Rent exponent so that the circuits behave like real ones.
- **Relation to graph separators.** For graphs, the [planar separator theorem](/planar-separator-theorem/) gives separators of size $O(\sqrt{n})$, the graph analogue of $p = 1/2$. A family of graphs whose minimum bisections grow like $n^p$ has the same kind of power law, but for Rent's rule this is an empirical fit, not a proved bound.

## References
