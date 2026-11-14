---
tag: 0W4EWY
kind: problem
slug: clock-tree-synthesis
name: Clock tree synthesis
aliases:
- CTS
- clock routing
area: eda/timing-and-verification
level: core
summary: Build a buffered tree from the clock source to all registers with low skew, latency and power, under slew limits.
prereqs: [setup-and-hold-constraints, elmore-delay, rectilinear-steiner-tree-problem]
see_also: [h-tree-clock, method-of-means-and-medians, tsay-zero-skew, deferred-merge-embedding, van-ginneken-buffer-insertion, clock-skew-scheduling, rectilinear-steiner-arborescence, np-hard]
sources:
  - paper: doi:10.1137/0132071
    title: "M. R. Garey and D. S. Johnson, The rectilinear Steiner tree problem is NP-complete, SIAM Journal on Applied Mathematics 32(4), 1977"
    locator: the NP-completeness of the rectilinear Steiner tree problem, which the clock problem contains when the skew is free
  - paper: "Ting-Hai Chao, Yu-Chin Hsu, Jan-Ming Ho, Kenneth D. Boese and Andrew B. Kahng, Zero skew clock routing with minimum wirelength, IEEE Transactions on Circuits and Systems II 39(11), 799 to 814, 1992"
    locator: the zero-skew clock routing problem for a given topology and its exact solution under linear delay
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 2011
    locator: Chapter 7, Specialized Routing, Sections 7.4 and 7.5, on the clock routing problem, skew, and clock tree constructions
  - book: isbn:9780849372421
    title: Charles J. Alpert, Dinesh P. Mehta and Sachin S. Sapatnekar (editors), Handbook of Algorithms for Physical Design Automation, CRC Press, 2008
    locator: Chapter 42, Clock Network Design, Basics
---

Clock tree synthesis is a routing problem: connect the clock source to every register, or *sink*, of a synchronous circuit by a tree of wires and buffers, so that the clock reaches all sinks at nearly the same time. The difference between the latest and the earliest arrival is the *skew*, and the [setup and hold constraints](/setup-and-hold-constraints/) of every register pair must hold with it. The tree should also have a short source-to-sink delay, little wire and buffer capacitance, since the clock net switches every cycle and often takes a large part of the power, and sharp signal edges, which a limit on the slew sets. With the skew left free and wire length as the cost, it is the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/), so it is [NP-hard](/np-hard/); with a fixed tree shape and zero skew under linear delay, it has an exact linear-time solution.

## In plain words

Every register on a chip waits for the clock to tell it when to take in new data. If the clock reaches some registers earlier than others, data can arrive too early or too late, and the chip fails or must run slower.

The clock comes from one point and must reach thousands or millions of registers. The wires that carry it form a tree. The task is to draw this tree so that the clock reaches every register at almost the same time, without too long a wait, with as little wire as possible, and with amplifiers along the way so that the signal stays sharp.

A shortest tree reaches near registers early and far registers late. Making all paths take the same time costs extra wire. Clock tree synthesis is the search for a good balance.

## Definition

**Input.** A set of sinks $s_1, \dots, s_n$ with points $p_i$ in the plane and load capacitances $c_i > 0$, and a source point $p_0$, or no source point when the root may go anywhere. The wire resistance $r$ and capacitance $c$ per unit length. A library of buffers, each with an input capacitance, a drive resistance and an intrinsic delay. A delay model, usually the [Elmore delay](/elmore-delay/) of the [RC tree model](/rc-tree/) with buffers as in [van Ginneken buffer insertion](/van-ginneken-buffer-insertion/). A skew bound $B \ge 0$ and a slew limit.

**Decision.** A rooted tree whose leaves are the sinks and whose root is at $p_0$ (the *topology*), a point for each internal node (the *embedding*), a wire length for each edge of at least the rectilinear distance of its ends, since a wire may make a detour to add delay, and a set of buffers at nodes of the tree.

**Delay and skew.** Let $t_i$ be the delay from the source to sink $s_i$ in the delay model. The *latency* is $\max_i t_i$ and the *skew* is $\max_i t_i - \min_i t_i$.

**Output.** A tree with skew at most $B$ and every slew within the limit that minimizes the cost: total wire length, or the total switched capacitance of wires and buffers, which is proportional to the clock power. Latency is a second objective or a further bound.

The case $B = 0$ is the *zero-skew* problem. In the *linear delay* or path length model, $t_i$ is the wire length of the path to $s_i$ and there are no buffers; it is the usual model for the geometry of a clock tree.

## Variants

- **Zero skew or bounded skew.** Zero skew asks for equal delays to all sinks. A bound $B > 0$ allows a cheaper tree; Cong, Kahng, Koh and Tsao gave the bounded-skew form of [deferred-merge embedding](/deferred-merge-embedding/).
- **Given topology or free topology.** With the topology fixed, only the embedding is chosen. Most methods build a topology first, for example by recursive splits or by greedy matching of nearby subtrees, and then embed it.
- **Prescribed or useful skew.** Each sink gets its own target delay instead of a common one. The targets come from [clock skew scheduling](/clock-skew-scheduling/), which shifts the clock at each register to give more time to its slowest paths.
- **Local skew.** Only pairs of registers joined by a timing path need equal clock arrival, so the bound applies to those pairs, not to all sinks.
- **Buffered clock trees.** Buffers are needed on large trees to meet the slew limit. The choice of buffer places and sizes joins the routing problem.
- **Clock gating.** Parts of the tree are switched off when their registers are idle, which saves power and adds gates to the tree.
- **Variation and corners.** The skew must stay small at several process, voltage and temperature corners, or in a statistical sense. Meshes and cross links lower the sensitivity at the cost of more wire and power.
- **Regular structures.** The [H-tree](/h-tree-clock/) fixes topology and embedding in advance for a square region, and local trees join it to the sinks.

## Examples

**Wire against skew.** Take the source at $(0, 0)$, sink $a$ at $(2, 0)$ and sink $b$ at $(0, 6)$, under linear delay. Every tree splits at some point $q$: a wire of length $t$ from the source to $q$, then wires of lengths $\ell_a$ and $\ell_b$ from $q$ to the sinks. The path lengths are $t_a = t + \ell_a$ and $t_b = t + \ell_b$, and the wire length is $W = t + \ell_a + \ell_b$.

- *Least wire.* The shortest tree is the star at the source, $W = 8$, with paths 2 and 6, so the skew is 4. Every tree of length 8 is a shortest path from $a$ to $b$ through the source, so all of them have skew 4.
- *Skew at most $B$, for $0 \le B \le 4$.* The path to $b$ has $t_b \ge 6$, so $t_a \ge 6 - B$ and $W = t_a + t_b - t \ge 12 - B - t$. Also $\ell_a + \ell_b \ge 8$, the distance from $a$ to $b$, so $W \ge t + 8$. The larger of the two bounds is least at $t = (4 - B) / 2$, which gives $W \ge 10 - B / 2$. The tree with $q = (0, (4 - B) / 2)$ meets this bound: $\ell_b = 6 - t$, $\ell_a = 2 + t$, paths $6 - B$ and 6.
- *Zero skew.* For $B = 0$ the least wire is 10, with the split at $(0, 2)$, a wire of length 4 from there to each sink, and both paths of length 6. The set of points at path length 4 from both sinks is the segment from $(0, 2)$ to $(2, 4)$, the merging segment of deferred-merge embedding, and $(0, 2)$ is its point nearest the source.

So each unit of skew given up saves half a unit of wire here, and zero skew costs 25 percent more wire than the Steiner tree. Under the Elmore delay the numbers change, since the load of each branch enters the delay, but the trade-off is the same.

## Known algorithms

- **[H-tree](/h-tree-clock/).** A fixed recursive H for sinks on a regular grid. Zero skew under the Elmore delay when the loads are equal; wasteful for uneven sinks.
- **[Method of means and medians](/method-of-means-and-medians/)** (Jackson, Srinivasan and Kuh, 1990). Splits the sinks at the median, alternating the direction, and joins the centres of mass. It builds a topology in $O(n \log n)$ time, with small but not zero skew.
- **Recursive geometric matching** (Kahng, Cong and Robins, 1991). Builds the topology bottom up by a matching of nearby subtrees at each level.
- **[Tsay's zero-skew algorithm](/tsay-zero-skew/)** (1991). For a given topology, places each tapping point from a closed formula so that the Elmore skew is exactly zero, with wire detours when needed.
- **[Deferred-merge embedding](/deferred-merge-embedding/)** (Chao, Hsu, Ho, Boese and Kahng, 1992, and Edahiro). Keeps a merging segment for each subtree and embeds top down. For a given topology it is proved to use the least wire under linear delay, and it gives exact zero Elmore skew. With greedy merging it also builds the topology.
- **Buffering.** [Van Ginneken buffer insertion](/van-ginneken-buffer-insertion/) and its variants place buffers on a routed tree; clock tools insert buffers level by level to keep the slew within the limit and balance the levels.

## Bounds

- **NP-hard with a free topology.** If $B$ is so large that it never binds, for example $B = \infty$, and the cost is wire length, any tree is feasible and the problem is to find a shortest rectilinear tree that connects the source and the sinks. This is the rectilinear Steiner tree problem, which Garey and Johnson (1977) proved NP-complete in the decision form. So minimum-wire clock routing with a skew bound and a free topology is NP-hard in general.
- **Zero skew with a free topology.** This page cites no hardness result for this case. The Steiner reduction does not apply, since the zero-skew condition changes the feasible trees.
- **Polynomial with a given topology.** Under linear delay, deferred-merge embedding finds a zero-skew tree of least wire for a given binary topology in $O(n)$ time; this is proved (Chao et al., 1992). Under the Elmore delay, a zero-skew embedding of every topology exists and Tsay's method finds one in $O(n)$ time, but least wire is not proved.
- **Lower bounds.** Every clock tree is at least as long as the rectilinear Steiner minimal tree of the source and the sinks, and under linear delay its latency is at least the largest rectilinear distance from the source to a sink. In the example the latency bound 6 is met for every $B$, but the Steiner bound 8 is met only when $B \ge 4$.

## Reductions

- **From the rectilinear Steiner tree problem.** With the skew bound removed, minimum-wire clock routing is the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/) on the source and the sinks; this gives the NP-hardness above.
- **Shortest path trees.** If the skew is free but every sink must be reached from the source by a path of the shortest possible length, the problem is the [rectilinear Steiner arborescence](/rectilinear-steiner-arborescence/) problem. This form bounds the delay to each sink, not only the latency.
- **Prescribed skew to zero skew.** A target delay $d_i$ at each sink is the same as zero skew after adding a delay offset at the sink, which methods based on merging segments handle by starting each sink with delay $-d_i$ instead of 0.
- **To clock skew scheduling.** The choice of target delays that best helps the timing of the circuit is a system of difference constraints, solved in [clock skew scheduling](/clock-skew-scheduling/); clock tree synthesis then realizes the targets.

## Applications

- **Physical design flows.** Clock tree synthesis runs after placement and before signal routing in every flow for synchronous chips, and its result sets the clock arrival times that static timing analysis uses after it.
- **Power.** The clock tree switches every cycle, so its capacitance is a large share of the dynamic power of a chip; low-capacitance trees and clock gating reduce it.
- **High-performance processors.** Large processors use a global grid or H-tree driven from the centre with local trees to the registers, to keep the skew small under variation.
- **Field-programmable gate arrays.** The clock networks are fixed H-trees or spines in the silicon, and the tools choose which branches to use.

## References
