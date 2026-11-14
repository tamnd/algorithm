---
tag: W4VDCC
kind: problem
slug: minimum-channel-width
name: Minimum channel width
aliases:
- FPGA channel width minimization
- W_min
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: The fewest tracks per routing channel with which a placed FPGA netlist can be routed, the standard measure of how routable a design or an architecture is.
prereqs: [routing-resource-graph, island-style-fpga]
see_also: [negotiated-congestion-routing, sat-based-fpga-routing, binary-search-on-answer, universal-switch-block, channel-density, vertex-disjoint-paths, global-routing, detailed-routing]
sources:
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 4, Sections 4.3 and 4.4 (the routers and the search for the minimum channel width) and Chapter 5, Global Routing Architecture (results given as the minimum channel width)
  - paper: "Yu-Liang Wu, Shuji Tsukiyama and Malgorzata Marek-Sadowska, Graph based analysis of 2-D FPGA routing, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(1), 33 to 44, 1996"
    locator: the NP-completeness of detailed routing of a given global routing with the Xilinx-style switch blocks (general locator)
  - paper: doi:10.1109/TCAD.2002.1004311
    title: Gi-Joon Nam, Karem A. Sakallah and Rob A. Rutenbar, A new FPGA detailed routing approach via search-based Boolean satisfiability, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(6), 674 to 684, 2002
    locator: the proofs of unroutability at a given channel width for a fixed global routing
  - paper: "Steven Fortune, John Hopcroft and James Wyllie, The directed subgraph homeomorphism problem, Theoretical Computer Science 10(2), 111 to 121, 1980"
    locator: vertex-disjoint paths for two pairs of terminals in a directed graph are NP-complete (general locator)
---

The minimum channel width of a placed netlist on an [island-style FPGA](/island-style-fpga/) is the smallest number $W$ of tracks per channel for which all nets of the netlist can be routed. It is the main measure of routability in FPGA research: an architecture or a placement is better when its designs need fewer tracks. The problem belongs to the FPGA CAD topic of this sub-area. The problem asks for one number; the algorithms that compute it, exactly or as an upper bound, are linked below.

## In plain words

An FPGA has a fixed number of wires in each routing channel. A design is placed on the chip, and every signal must then find its own wires from its driver to all its readers.

With many wires per channel, this is easy. With few, the signals fight over the same wires, and at some point no way to connect all of them exists. The minimum channel width is the smallest number of wires per channel at which a way still exists.

Researchers report this number for each design. When a new chip layout or a new placement tool makes the number go down, it is easier to route. Most tools find the number by trying a channel width, routing, and then trying a smaller or a larger one.

## Definition

**Input.**

- An architecture family $\mathcal{A}$: for each $W \ge 1$, a [routing resource graph](/routing-resource-graph/) $G_W = (V_W, E_W)$ with capacity 1 on every node. It is built from fixed parameters (the grid, the blocks and their pins, $F_c$, $F_s$, the segment lengths and the rule for the switch pattern) and the channel width $W$.
- A placed netlist: $m$ nets, net $i$ with a source pin and a set of sink pins at fixed block positions, so that each net has a source $s_i$ and sinks $K_i$ in every $G_W$.

**Output.** The number

$$W_{min} = \min \{ W \ge 1 : R(W) \},$$

where $R(W)$ is the statement that $G_W$ has a legal routing: pairwise vertex-disjoint out-trees, the tree of net $i$ rooted at $s_i$ and holding $K_i$. If no $W$ works, for example because a pin has no switch to any track, $W_{min} = \infty$.

**Constraints.** Every channel has the same width. Every node holds at most one net. The placement is fixed. Nothing is minimized except $W$; wirelength and delay are not part of this problem.

**Decision form.** Given $\mathcal{A}$, the netlist and $W$, decide $R(W)$. This is the routability problem at a fixed width.

**Monotonicity.** Call the family *nested* if, for every $W$, there is an injective map from $V_W$ to $V_{W+1}$ that maps edges to edges and the source and sinks of each net to the same source and sinks. In a nested family $R(W)$ implies $R(W + 1)$, because the image of a legal routing is a legal routing: trees map to trees, and an injective map keeps the node sets disjoint. A generated family need not be nested. The tracks that a pin reaches and the switch pattern are recomputed for each $W$, so adding a track can remove a path. The example below has $R(1)$ true and $R(2)$ false.

## Variants

- **Fixed global routing.** The route of each net through the channels and switch blocks is given, and only the tracks are chosen. This is detailed routing at width $W$. Its minimum is at least the minimum over all routings.
- **Segment mix.** With wires of several lengths, $W$ is the total number of tracks, and the fraction of each length is fixed.
- **Low-stress width.** Delay is often measured at a width above the minimum, so that the router has room to choose fast paths. Betz, Rose and Marquardt measure delays at $W = 1.2 \, W_{min}$.
- **Nonuniform channels.** Different widths for horizontal and vertical channels, or for the channels at the border. The problem then has several numbers to set, not one.
- **Heuristic width.** In practice $W_{min}$ is reported as the smallest $W$ at which a given router succeeds. This is a property of the router as well as of the netlist, and it is only an upper bound on the true value.

## Examples

**One switch block.** Three nets meet at one switch block: $T$ to $L$, $L$ to $B$ and $B$ to $T$. Each side carries two nets, so $W \ge 2$. With the subset pattern, each net keeps its track number through the block, so the three nets need three different tracks, and the width is 3. With the [universal switch block](/universal-switch-block/), $W = 2$ is enough.

**A family that is not nested.** Take the array of two blocks side by side of the [routing resource graph](/routing-resource-graph/) page: $n_x = 2$, $n_y = 1$, one input pin per block, $F_{in} = F_{out} = 1$, and a pattern in which turns change the track (track $t$ goes to $(t + 1) \bmod W$ for two turns and to $W - 1 - t$ for the other two). Net $a$ goes from the output of block 1 to the input of block 2, and net $b$ the other way. An exhaustive search over all pairs of simple paths gives:

| $W$ | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| legal routing exists | yes | no | no | no |

With $W = 1$, every map of the pattern is the identity, and net $a$ goes around the bottom channel while net $b$ uses the top one. With $W = 2$, the pattern is no longer the identity, while each output pin still drives only track 0 and each input pin still reads only track 0. Each net then has 17 routes, and every route of net $a$ shares a node with every route of net $b$. Here $W_{min} = 1$, yet $R(2)$ is false. This is a toy instance, made to show that $R$ need not be monotone; it is not a benchmark result.

## Known algorithms

- **Binary search with a router.** VPR raises $W$ until the router succeeds and then runs a [binary search on the answer](/binary-search-on-answer/) between the last failure and the first success. If the predicate that is searched is monotone, the search returns its least true value after $O(\log W_{min})$ router calls; the proof is the usual one for [binary search](/binary-search/) on a monotone predicate. Two limits apply. If $R$ itself is not monotone, as in the example, the search can return a width above $W_{min}$. And the router is a heuristic, usually [negotiated congestion routing](/negotiated-congestion-routing/): its success at $W$ implies $R(W)$, but its failure does not imply that $R(W)$ is false. So the result $W_h$ satisfies $W_{min} \le W_h$, and nothing more is proved.
- **SAT-based routing.** For a fixed global routing, [SAT-based FPGA routing](/sat-based-fpga-routing/) decides routability at $W$ exactly. A satisfying assignment is a routing, and UNSAT proves that no track assignment exists at that $W$ for that global routing. Searching $W$ upward gives the exact minimum for the fixed global routing, which is still only an upper bound on $W_{min}$ over all routings.
- **Exhaustive search.** For tiny graphs, enumerate the trees of each net and search for a disjoint choice. This is exact and exponential, and it is how the example was solved.

## Bounds

- **Lower bound by a cut.** Let $C$ be a set of channel pieces such that every route of each net of a set $N_C$ must use a track of some piece in $C$. The pieces of $C$ hold $|C| W$ track nodes, and the routes of the nets in $N_C$ use disjoint track nodes, so $W \ge \lceil |N_C| / |C| \rceil$. The density condition at one switch block is the case of one side.
- **Lower bound for a fixed global routing.** If $d$ nets use the same channel piece in the global routing, then $W \ge d$. This is the [channel density](/channel-density/) of the FPGA channel.
- **Upper bounds** come only from a routing that is found. There is no general formula, since $W_{min}$ can be infinite for a bad architecture.

## Reductions

- **From disjoint paths.** The decision form with only two-pin nets is the problem of [vertex-disjoint paths](/vertex-disjoint-paths/) between given pairs in a directed graph, and that problem is NP-complete already for two pairs on general directed graphs (Fortune, Hopcroft and Wyllie 1980). Routing resource graphs are special graphs, so this does not by itself prove hardness for FPGAs.
- **Detailed routing is NP-complete.** For a fixed global routing on an array with the Xilinx-style switch blocks, deciding whether the nets fit on the tracks is NP-complete (Wu, Tsukiyama and Marek-Sadowska 1996). With that switch pattern, each net keeps its track, and the problem is a [graph coloring](/graph-coloring/) of the nets that share a channel piece.
- **To SAT.** The decision form for a fixed global routing reduces to [SAT](/sat/) with one variable per net, piece and track, as on the [SAT-based FPGA routing](/sat-based-fpga-routing/) page.

## Applications

- **Architecture studies.** Betz, Rose and Marquardt compare cluster sizes, segment lengths and switch patterns by the minimum channel width that their benchmarks need (Chapters 5 to 7).
- **Placement quality.** A placer is judged by the width that its placements need after routing, as well as by wirelength and delay.
- **Router quality.** A router that routes the same placement at a smaller width is the stronger router on that instance.
- **Chip sizing.** A vendor picks the channel width of a family so that the target designs route with some slack above the measured width.

## References
