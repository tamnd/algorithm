---
tag: TT0S6E
kind: definition
slug: fpga-switch-block
name: FPGA switch block
aliases:
- disjoint switch block
- Wilton switch block
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: The programmable switches where a horizontal and a vertical FPGA routing channel cross, given by which track on one side can connect to which tracks on the other sides.
prereqs: [island-style-fpga]
see_also: [universal-switch-block, routing-resource-graph, minimum-channel-width, sat-based-fpga-routing, switchbox-routing, edge-coloring]
sources:
  - paper: doi:10.1145/225871.225886
    title: Yao-Wen Chang, D. F. Wong and C. K. Wong, Universal switch modules for FPGA design, ACM Transactions on Design Automation of Electronic Systems 1(1), 80 to 101, 1996
    locator: the switch module as a graph on the 4W terminals of the four sides, the flexibility Fs, the XC4000-type module and the count of 6W switches for Fs = 3
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 4, Section 4.2 Architecture Parameterization and Generation; Chapter 7, Detailed Routing Architecture (switch block patterns and switch types)
  - paper: "Steven J. E. Wilton, Architectures and Algorithms for Field-Programmable Gate Arrays with Embedded Memories, PhD thesis, University of Toronto, 1997"
    locator: the switch block in which turning connections move a signal to another track (general locator; the year of the thesis is given as 1996 in some citations)
  - paper: doi:10.1145/2617593
    title: Jason Luu and others, VTR 7.0, next generation architecture and CAD system for FPGAs, ACM Transactions on Reconfigurable Technology and Systems 7(2), 2014
    locator: the single-driver routing with Fs = 3 of the flagship architecture (general locator)
---

An FPGA switch block is the set of programmable switches at a point where a horizontal and a vertical routing channel of an [island-style FPGA](/island-style-fpga/) cross. It says which track end on one side of the crossing can be connected to which track ends on the other sides. Its pattern decides which sets of nets can be routed through it, and so it sets much of the routability and the area of the array. The definition belongs to the FPGA CAD topic of this sub-area.

## Definition

Name the four sides of a crossing $T$, $R$, $B$ and $L$ (top, right, bottom, left). Each side has $W$ *terminals*, the ends of the tracks of the channel on that side, numbered $0$ to $W - 1$. A terminal is a pair $(s, i)$ with side $s$ and track $i$.

A **switch block** with channel width $W$ is a graph $S$ on the $4W$ terminals in which every edge joins two terminals on different sides. Each edge is a *switch*: when it is on, the two segments are one wire. A switch block on the border of the array has only the sides that exist, three on an edge and two at a corner.

- The **flexibility** $F_s$ of a terminal is its degree in $S$, the number of terminals it can connect to. When all terminals have the same degree, that degree is the $F_s$ of the block.
- A block with $F_s$ on all $4W$ terminals has $F_s \cdot 4W / 2 = 2 F_s W$ switches.
- With $F_s = 3$, which is the usual choice, a terminal has one switch to each of the three other sides. Then the switches between any two sides form a perfect matching between their terminals, and the block has $6W$ switches. A block of this kind is fully given by six permutations of $\{0, \ldots, W - 1\}$, one for each pair of sides.

A set of nets *routes through* the block when each net that must pass from one side to another gets a path of switches, and no two nets use the same terminal. The model of Chang, Wong and Wong lets a net use one switch, from its entry terminal to its exit terminal.

The definition above is for bidirectional wires, where one switch can pass a signal either way. With single-driver wires, each segment starts at a multiplexer, and the block is a set of multiplexers: the inputs of the multiplexer that drives a segment are the incoming segment ends that the pattern allows. The same patterns are then written as directed edges.

## Examples and non-examples

- **The subset pattern.** Terminal $(s, i)$ connects to $(s', i)$ on each other side $s'$. All six permutations are the identity. With $W = 3$ the block has $6 \cdot 3 = 18$ switches. A net that enters on track $i$ stays on track $i$ in every block, so the tracks split into $W$ separate domains. This is the planar pattern of the Xilinx XC4000 family.
- **A pattern where turns change the track.** Keep the identity for the straight pairs $(T, B)$ and $(L, R)$, and use other permutations for the four turning pairs. Wilton's pattern is of this kind: a net that turns moves to another track, so the tracks no longer split into domains. An illustrative pattern with this property, not Wilton's exact formulas, maps track $i$ to track $(i + 1) \bmod W$ for the turns $(T, R)$ and $(B, L)$ and to track $(W - 1 - i)$ for the turns $(L, T)$ and $(R, B)$. It still has $6W$ switches.
- **The universal pattern.** Chang, Wong and Wong chose the six permutations so that every set of two-pin connections that the side widths allow can be routed. See [universal switch block](/universal-switch-block/).
- **Three nets that the subset pattern cannot route.** With $W = 2$, take three nets that join $T$ to $L$, $L$ to $B$ and $B$ to $T$. Each side has two of them, which fits $W = 2$. In the subset pattern each net uses the same track on both of its sides, so the three nets need three pairwise different tracks, and there are only two. A universal block routes them.
- **A full crossbar.** If every terminal has a switch to every terminal of the other three sides, then $F_s = 3W$ and the block has $6W^2$ switches. It is a switch block, and it routes all that the side widths allow, but its area grows with $W^2$.
- **Non-example: a connection block.** The switches between the pins of a logic block and the tracks of a channel form a connection block, not a switch block. Its flexibility is $F_c$, not $F_s$.
- **Non-example: a switch inside one side.** A switch between two tracks on the same side would join two parallel segments of one channel. The definition does not allow it.
- **Non-example: an ASIC switchbox.** In [switchbox routing](/switchbox-routing/) for standard cells, the wires inside the box are drawn by the router. In an FPGA switch block, only the fixed switches can be used.

## Related definitions

- **Universal switch block.** The [universal switch block](/universal-switch-block/) is the pattern with $6W$ switches that routes every set of two-pin connections allowed by the side widths, and the page proves this.
- **Routing resource graph.** The switches of all blocks become edges of the [routing resource graph](/routing-resource-graph/), on which routers work.
- **Channel width.** The pattern changes the [minimum channel width](/minimum-channel-width/) of a design. Betz, Rose and Marquardt (Chapter 7) measured that patterns where turns change the track need fewer tracks than the subset pattern on their benchmarks.
- **Coloring view.** With the subset pattern, giving tracks to nets is a coloring of a conflict graph, and for one block it is an [edge coloring](/edge-coloring/) of the graph of required side pairs. [SAT-based FPGA routing](/sat-based-fpga-routing/) solves this assignment exactly.

## References
