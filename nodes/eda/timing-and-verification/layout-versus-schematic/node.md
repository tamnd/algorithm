---
tag: V0X7JN
kind: problem
slug: layout-versus-schematic
name: Layout versus schematic
aliases:
- LVS
- layout vs schematic check
area: eda/timing-and-verification
level: core
summary: Decide whether the netlist extracted from a layout is the same circuit as the schematic netlist, a graph isomorphism problem on circuits.
prereqs: [graph-isomorphism-problem, circuit-extraction, bipartite-graph]
see_also: [gemini-netlist-comparison, weisfeiler-leman, gi-completeness, babai-quasipolynomial-algorithm, nauty, subgraph-isomorphism, boolean-equivalence-checking, design-rule-checking]
sources:
  - paper: "Carl Ebeling and Ofer Zajicek, Validating VLSI circuit layout by wirelist comparison, Proceedings of the IEEE International Conference on Computer-Aided Design (ICCAD) 1983, 172 to 173"
    locator: the statement of layout validation as graph isomorphism of the device and net graphs of two wirelists
  - paper: doi:10.1109/ICCAD.1988.122520
    title: Carl Ebeling, GeminiII, a second generation layout validation program, IEEE International Conference on Computer-Aided Design (ICCAD) 1988, Digest of Technical Papers, 322 to 325
    locator: the comparison of netlists with interchangeable pins and the reporting of differences
  - paper: doi:10.1145/2897518.2897542
    title: László Babai, Graph isomorphism in quasipolynomial time, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 684 to 697
    locator: the quasipolynomial upper bound for graph isomorphism, which applies to LVS through the reduction on this page
  - paper: "Daniel Neuen and Pascal Schweitzer, An exponential lower bound for individualization-refinement algorithms for graph isomorphism, Proceedings of the 50th ACM Symposium on Theory of Computing (STOC), 2018"
    locator: the graphs on which every individualization and refinement search, the scheme of practical LVS tools, visits exponentially many nodes
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: the sections on physical verification (general locator)
---

Layout versus schematic, or LVS, asks whether the circuit drawn in a chip layout is the circuit that the designer meant. Its inputs are two netlists: the one that [circuit extraction](/circuit-extraction/) recovered from the layout, and the schematic netlist. LVS decides whether the two are the same up to the names of the nets and the order of the devices, and if they are not, it reports where they differ. It is [graph isomorphism](/graph-isomorphism-problem/) on circuits, and with [design rule checking](/design-rule-checking/) it makes up the physical verification of a chip. This page states the problem and what is known about its complexity. The classic method is [Gemini](/gemini-netlist-comparison/).

## In plain words

The designer draws the circuit twice: once as a schematic, a list of parts and wires, and once as the shapes on the chip. The shapes are turned back into a list of parts and wires by a program. LVS then checks that the two lists describe the same circuit.

The lists use different names and a different order. A wire called "out" in the schematic may be "net 4017" in the layout. So the check has to find a way to pair every part and every wire of one list with one of the other, such that each pair is connected in the same way. If no pairing works, the check must also say where the problem is, for example "this wire touches one transistor too many", so that the designer can fix the layout.

## Definition

**Input.** Two netlists $G$ and $G'$. A netlist has a set of devices and a set of nets. Each device has a type (n-transistor, p-transistor, resistor, and so on), parameters (such as $W$ and $L$), and pins. Each pin has a *pin class* and lies on one net. Pins of one class of a device are interchangeable: the source and the drain of a MOS transistor are one class, the gate another. Some nets carry names that must match, such as the supplies and the ports. Let $n$ be the number of devices, $m$ the number of nets and $P$ the number of pins.

**Equivalence.** $G$ and $G'$ are *equivalent* when there are bijections $\pi$ from the devices of $G$ to those of $G'$ and $\varphi$ from the nets of $G$ to those of $G'$ such that

- $\pi(u)$ has the type of $u$, and its parameters are within the given tolerance of those of $u$;
- for each pin class $c$, $\varphi$ maps the multiset of nets on the pins of class $c$ of $u$ to the multiset of nets on the pins of class $c$ of $\pi(u)$;
- a named net maps to the net with the same name.

**Output.** Yes with the bijections, or no with a report of the differences. The decision part is exact. The report has no standard formal statement: a "smallest set of differences" can be defined as a graph edit distance, but tools give heuristic reports, such as a class of nets with more members on one side.

The netlists are bipartite graphs with one vertex per device and per net and one edge per pin, colored by the pin class. Equivalence without the parameters is isomorphism of these [bipartite graphs](/bipartite-graph/) with colors.

## Variants

- **With netlist reduction.** Before the comparison, parallel devices of one type on the same nets are merged into one with the sum of the widths, and series stacks of transistors may be merged or have their inputs made interchangeable. Then layouts that split a large transistor into fingers still match the schematic.
- **Hierarchical LVS.** Cells that match are compared once and then treated as black boxes with ports.
- **Subcircuit search.** Find all copies of a small netlist inside a large one, a [subgraph isomorphism](/subgraph-isomorphism/) problem. SubGemini solves it with the Gemini labels.
- **Functional equivalence.** Two netlists with different structure can compute the same Boolean function. LVS calls them different. Deciding whether two circuits compute the same function is [Boolean equivalence checking](/boolean-equivalence-checking/), a different problem.

## Examples

**A match.** The schematic of an inverter has an n-transistor with gate IN and source and drain GND and OUT, and a p-transistor with gate IN and source and drain VDD and OUT. The inverter on the [circuit extraction](/circuit-extraction/) page gives an n-transistor with gate A on GND and Y, and a p-transistor with gate A on VDD and Y. The map IN to A, OUT to Y, GND to GND and VDD to VDD, with the n-transistor to the n-transistor and the p-transistor to the p-transistor, keeps the types, the pin classes and the supply names. So the two are equivalent. If the ports are named IN and OUT in the schematic and A and Y in the layout, the tool needs a table that pairs these names.

**A short.** In the second layout of the circuit extraction page the metal of Y touches the metal of A, so the layout netlist has 3 nets and the schematic has 4. A bijection of nets needs equal counts, so the netlists are not equivalent, and the proof is a single count. The report points to the net with too many pins: the merged net has 4 pins (two gates and two drains), and no net of the schematic has 4.

**Local counts are not enough.** Six resistors in one ring, against two rings of three resistors each, have the same number of devices and nets, every net has 2 pins and every resistor has 2 nets. They are not equivalent, since one graph is connected and the other is not, but no count of pins or of neighbors around a single vertex shows it. This is why LVS tools need more than local counts, and why [color refinement](/weisfeiler-leman/) alone cannot decide LVS.

**Swapped inputs.** In a CMOS NAND gate with inputs A and B, exchanging the two inputs in the layout gives an isomorphic netlist with A and B swapped. Without port names LVS accepts it. With the names, it is a mismatch. The [Gemini](/gemini-netlist-comparison/) page traces this case and the ring case, and its tests check them against a brute-force search over all bijections.

## Known algorithms

| Method | Idea | What is known |
| --- | --- | --- |
| [Gemini](/gemini-netlist-comparison/) and GeminiII | refine labels of devices and nets on both netlists at once, then guess to break ties | each refinement is polynomial; a reported count mismatch is a proof of difference; worst case exponential with backtracking |
| [Color refinement](/weisfeiler-leman/) alone | the refinement step without guesses | polynomial; it proves some pairs different but cannot prove equivalence when classes stay larger than one |
| [Individualization and refinement](/individualization-refinement/), for example [nauty](/nauty/) | refinement with a full search tree and pruning by automorphisms | exact; exponential on some graphs (Neuen and Schweitzer 2018) |
| Matching by names | when every net has a name on both sides, sort the devices by their typed pin lists | $O(P \log P)$, exact |
| [Babai's algorithm](/babai-quasipolynomial-algorithm/) | group-theoretic method for general graph isomorphism | quasipolynomial time; a theoretical bound, not used in LVS tools |

## Bounds

**LVS is GI-complete (proved).** LVS without parameters is equivalent, under polynomial-time reductions, to graph isomorphism:

- *From graph isomorphism.* For a graph $H$, make one net per vertex, one resistor per edge with its two pins in one class, and one one-pin device of a type T on each net, so that no net is empty. An isomorphism of graphs gives an equivalence of the netlists. Conversely an equivalence maps nets to nets bijectively, and it maps each resistor to a resistor on the image nets, so the map of nets is a graph isomorphism.
- *To graph isomorphism.* A netlist is a bipartite graph with colored vertices and colored edges, and isomorphism of colored graphs reduces to isomorphism of plain graphs by standard gadgets, as on the [GI-completeness](/gi-completeness/) page.

So LVS is in quasipolynomial time by Babai's theorem, it is in NP, and it is not known to be in P. It is not known to be NP-complete, and it is not expected to be, because graph isomorphism is NP-complete only if the polynomial hierarchy collapses.

**Easy cases (proved).** If every net is named on both sides, $\varphi$ is fixed, and each device is determined up to equivalence by its type and its multiset of (pin class, net) pairs, so sorting these keys decides LVS in $O(P \log P)$ time. If color refinement gives every vertex its own class, the map by classes is the only candidate and it is checked in $O(P)$ time.

**What is measured.** On real circuits, supply names, port names and the mix of device types make the refinement split almost all classes in a few rounds, so Gemini-type tools run in near-linear time. This is an observation from practice, not a theorem.

## Reductions

- **From graph isomorphism**, as above, so a fast general LVS method would be a fast graph isomorphism method.
- **To colored graph isomorphism**, as above.
- **From circuit extraction.** The layout netlist comes from [circuit extraction](/circuit-extraction/). Extraction reads geometry and writes a netlist; LVS reads two netlists and never looks at the geometry. A short or an open in the layout shows up only in LVS, because extraction faithfully reports the circuit that is drawn.
- **To subgraph isomorphism.** Hierarchical LVS and device recognition search for small patterns in a large netlist.

## Applications

- **Sign-off.** A layout goes to manufacturing only if it is LVS-clean against the schematic, together with DRC.
- **Debugging layouts.** The report of differences points to shorts, opens, missing contacts and swapped connections.
- **Checking netlist transformations.** Tools that rewrite netlists, such as layout generators and netlist reducers, use LVS to show that they kept the structure.

## References
