---
tag: GYFF7P
kind: definition
slug: channel-connected-component
name: Channel-connected component
aliases:
- CCC
- DC-connected component
area: eda/logic-and-circuit-simulation
level: advanced
summary: A maximal set of transistors joined through source and drain terminals, the unit that switch-level simulators, timing simulators and transistor-level timers evaluate.
prereqs: [connected-components]
see_also: [switch-level-simulation, timing-simulation, static-timing-analysis, disjoint-set, circuit-extraction, iterated-timing-analysis, strongly-connected-components, topological-sort]
sources:
  - paper: doi:10.1109/TC.1984.1676408
    title: R. E. Bryant, A switch-level model and simulator for MOS digital systems, IEEE Transactions on Computers C-33(2), 160 to 177, 1984
    locator: the switch graph with input nodes and storage nodes, and the partition of the storage nodes into parts joined by transistor channels, which MOSSIM II solves one at a time (general locator)
  - paper: "R. E. Bryant, MOSSIM: a switch-level simulator for MOS LSI, Proceedings of the 18th Design Automation Conference, 786 to 790, 1981"
    title: R. E. Bryant, MOSSIM, a switch-level simulator for MOS LSI, Proceedings of the 18th Design Automation Conference, 786 to 790, 1981
    locator: the switch-level network of nodes and transistors and its evaluation by parts (general locator)
---

A channel-connected component of a transistor network is a maximal set of nodes that are joined through transistor channels, the path from source to drain, together with the transistors on those channels. The supply nodes and the primary inputs do not join anything. Neither does a gate terminal, because no DC current flows into a gate. So current flows between two components only through the supplies and the inputs, and a component sees the rest of the circuit only through the gates of its transistors and through these fixed nodes. That makes the component the natural unit of evaluation for tools that work on transistors. The definition belongs to both halves of the sub-area. In the logic half, a [switch-level simulator](/switch-level-simulation/) solves one component at a time for its node values. In the circuit half, a [timing simulator](/timing-simulation/) or an [iterated timing analysis](/iterated-timing-analysis/) integrates one component at a time, and transistor-level timers compute delays per component. The components are the [connected components](/connected-components/) of a simple graph, so they are found in linear time.

## Definition

**Network.** A transistor network has a set of *fixed nodes*, the supplies $V_{DD}$ and ground and the primary inputs, whose values the environment sets, and a set $N$ of *storage nodes*. Each transistor $\tau$ has a gate $g(\tau)$ and two channel terminals $a(\tau)$ and $b(\tau)$, which are nodes of either kind. Source and drain are not told apart, since a MOS transistor is symmetric.

**Channel graph.** The channel graph $H$ has the vertex set $N$ and one edge $\{a(\tau), b(\tau)\}$ for each transistor whose two channel terminals are both storage nodes. Edges at fixed nodes and gate terminals are not in $H$.

**Channel-connected component.** A channel-connected component, or CCC, is a pair $(K, T_K)$, where $K$ is the vertex set of a connected component of $H$ and $T_K$ is the set of transistors with at least one channel terminal in $K$. The *gate inputs* of the component are the gates $g(\tau)$ for $\tau \in T_K$, and its *fixed terminals* are the fixed nodes among the channel terminals of $T_K$.

**Component graph.** The component graph has one vertex per CCC and an arc from $C$ to $C'$ when a storage node of $C$ is a gate input of $C'$. Arcs follow the gates, from the node that controls a transistor to the component that holds it.

**Partition (exact).** The CCCs partition the storage nodes, and they partition the transistors that touch at least one storage node. *Proof.* The vertex sets of the connected components of $H$ partition $N$. A transistor with one storage terminal belongs to the component of that node. A transistor with two storage terminals is an edge of $H$, so both ends lie in one component, and it belongs to that one only. $\square$ A transistor with both channel terminals fixed, such as a decoupling device between $V_{DD}$ and ground, is in no component; tools treat it apart. The partition depends only on the network, so it is unique.

**Locality (exact in the switch-level model).** In the switch-level model of [switch-level simulation](/switch-level-simulation/), the new values of the nodes of a component depend only on their old charges, on the values of its gate inputs and on the values of its fixed terminals. *Proof.* The value of a storage node comes from paths of conducting transistors that start at the node. Such a path moves along channels, so it stays inside $K$ until it reaches a fixed node, where it ends, because a fixed node holds its value and passes no signal through. Whether a transistor on the path conducts depends only on its gate input. So nothing outside $K$, its gate inputs and its fixed terminals enters the definition. $\square$ In the electrical model the same holds for the DC currents, since a gate draws none, but not for the charging currents: the capacitance between the gate and the channel of a transistor couples its gate node to the nodes of another component. Timing simulators either ignore this coupling or put it into the node capacitances, so for them locality is an approximation.

**Computation.** Run a [disjoint-set](/disjoint-set/) union over the edges of $H$, or a search from each unvisited storage node. Either way the cost is $O(|N| + |T|)$, up to the inverse Ackermann factor for union-find, where $T$ is the set of transistors.

## Examples and non-examples

Each example was checked by the partition routine of the switch-level implementation.

**Examples.**

- *Inverter.* A CMOS inverter with input $x$ and output $y$ has two transistors, from $V_{DD}$ to $y$ and from $y$ to ground. Both edges end at a fixed node, so $H$ has the single vertex $y$ and no edge. The component is $\{y\}$ with both transistors, and its gate input is $x$.
- *Two-input NAND.* The pull-up transistors run from $V_{DD}$ to $y$, and the pull-down stack runs from $y$ to an internal node $m$ and from $m$ to ground. The edge $\{y, m\}$ joins the output and the internal node, so the component is $\{y, m\}$ with all four transistors.
- *A chain of $k$ inverters.* Each stage is its own component, and the component graph is a path of $k$ vertices. A switch-level or timing simulator can solve the components in this order.
- *Inverter, transmission gate, inverter.* The first inverter drives $a$, a transmission gate of two transistors joins $a$ and $b$, and $b$ drives the second inverter with output $c$. The components are $\{a, b\}$ with four transistors and $\{c\}$ with two. The transmission gate merges its two sides into one component, since current can flow both ways through it.
- *A column of static RAM.* Each of three cells has two cross-coupled inverters with nodes $q_i$ and $\bar q_i$, and two access transistors from $q_i$ to the bit line and from $\bar q_i$ to the other bit line. The bit lines join all the cells, and the column has only two components, each with four nodes and nine transistors. Without the access transistors the same six inverters give six components.

**Non-examples.**

- *Shared supplies.* Two inverters with the same $V_{DD}$ and ground are two components. If the supplies were vertices of $H$, every node of a chip would be in one component, and the partition would be useless.
- *A gate connection.* In the inverter chain, the output of stage 1 is the gate of stage 2, and the two stages stay apart. A gate connection gives an arc of the component graph, not a merge.
- *A latch.* Two cross-coupled inverters form two components, each a gate input of the other. The component graph has a cycle, so no order solves each component once. Simulators iterate over the cycle until no value changes, as in the rounds of the switch-level simulator.
- *A logic gate is not always a component.* A complex gate such as an AND-OR-INVERT is one component, but a pass-transistor multiplexer, a precharged bus or a barrel shifter merges many logic functions into one large component. The cost of a switch-level or timing step grows with the size of the component, so a few large components can dominate the run time.

## Related definitions

- **[Switch-level simulation](/switch-level-simulation/).** Solves one CCC at a time for the steady state, and puts on its queue the components whose gate inputs or nodes changed.
- **[Timing simulation](/timing-simulation/) and [iterated timing analysis](/iterated-timing-analysis/).** Update node voltages one component at a time, in the order of the component graph.
- **[Static timing analysis](/static-timing-analysis/).** At the transistor level, a timer computes a delay for each component, from a change at a gate input to a change at an output node, and then works on the component graph as on a gate netlist.
- **[Circuit extraction](/circuit-extraction/).** Produces the transistor network, with node capacitances, from the layout.
- **[Connected components](/connected-components/) and [disjoint-set](/disjoint-set/).** The graph algorithms that compute the partition.
- **[Strongly connected components](/strongly-connected-components/) and [topological sort](/topological-sort/).** Find the loops of the component graph and an order for the rest.

## References
