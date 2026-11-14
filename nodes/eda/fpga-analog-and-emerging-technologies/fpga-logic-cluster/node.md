---
tag: K4MEET
kind: definition
slug: fpga-logic-cluster
name: FPGA logic cluster
aliases:
- configurable logic block
- CLB
area: eda/fpga-analog-and-emerging-technologies
level: intro
summary: A logic block of several basic logic elements, each a K-input LUT with an optional flip-flop, joined by local routing that is faster than the global routing.
prereqs: [island-style-fpga, lut-mapping]
see_also: [fpga-packing, t-vpack, aapack, k-feasible-cut, routing-resource-graph, technology-mapping]
sources:
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 6, Cluster-Based Logic Blocks (the basic logic element, the cluster with N elements and I inputs, the full local crossbar and the choice of I); Chapter 3, Section 3.1 Logic Block Packing
  - paper: doi:10.1145/296399.296426
    title: Alexander Marquardt, Vaughn Betz and Jonathan Rose, Using cluster-based logic blocks and timing-driven packing to improve FPGA speed and density, Proceedings of the ACM/SIGDA International Symposium on Field Programmable Gate Arrays (FPGA '99), 37 to 46, 1999
    locator: the definition of the cluster and of its parameters N, K and I, and the legality conditions used by the packer
  - paper: "Elias Ahmed and Jonathan Rose, The effect of LUT and cluster size on deep-submicron FPGA performance and density, IEEE Transactions on Very Large Scale Integration (VLSI) Systems 12(3), 288 to 298, 2004"
    locator: the measured area and delay as functions of K and N (general locator)
---

An FPGA logic cluster is the logic block of an [island-style FPGA](/island-style-fpga/) that holds several basic logic elements and a local routing network that joins them. A basic logic element is one $K$-input lookup table (LUT) with an optional flip-flop. The local routing is faster than the general routing of the array, so a connection inside a cluster is cheap and fast. The definition belongs to the FPGA CAD topic of this sub-area: it fixes what [FPGA packing](/fpga-packing/) must fill.

## Definition

A **basic logic element** with LUT size $K$ has one $K$-input LUT, which can compute any Boolean function of its $K$ inputs, one D flip-flop whose data input is the LUT output, and a two-input multiplexer that drives the output of the element with either the LUT output or the flip-flop output. A configuration bit sets the multiplexer. So an element computes one LUT function and outputs it either at once or one clock cycle later.

A **logic cluster** with parameters $(K, N, I)$ has:

- $N$ basic logic elements with LUT size $K$;
- $I$ input pins, which carry signals from the general routing into the cluster;
- $N$ output pins, one for the output of each element;
- one or more clock pins for the flip-flops;
- local routing that can drive each of the $N K$ LUT inputs from any of the $I$ input pins or from any of the $N$ outputs of the elements. In the cluster of Betz, Rose and Marquardt this is a full crossbar: a multiplexer with $I + N$ inputs in front of each LUT input.

All three numbers are parameters of the architecture. The definition fixes nothing more about their values.

**Legal contents.** Let $C$ be a set of elements of a mapped netlist, each with its input nets and its output net. The *external input nets* of $C$ are the nets that some element of $C$ uses as an input and that no element of $C$ drives. With a full crossbar, $C$ fits in one cluster if and only if

$$|C| \le N \quad\text{and}\quad |\mathrm{ext}(C)| \le I,$$

plus a limit on the number of distinct clocks. The proof is short. Each external net enters on its own input pin, so the second condition is necessary, and the first is the number of element positions. Conversely, if both hold, put the elements in any positions and give each external net its own pin. The crossbar can drive every LUT input from that pin or from the output of the element that drives it inside $C$, since a full crossbar can connect any of its inputs to any LUT input at the same time. An output of an element leaves the cluster on its own output pin, so outputs never limit the contents.

## Examples and non-examples

- **A hand-sized cluster.** Take $K = 3$, $N = 2$, $I = 4$ and three elements: $a$ with inputs $x, y, z$ and output $A$; $b$ with inputs $A, y, w$ and output $B$; $c$ with inputs $u, v, w$ and output $C$. The set $\{a, b\}$ has the external nets $x, y, z, w$, since $A$ is driven inside, so it fits. The set $\{b, c\}$ has the external nets $A, y, w, u, v$, five of them, so it does not fit, even though it has only two elements. The set $\{a, b, c\}$ has three elements and does not fit either.
- **The Betz, Rose and Marquardt cluster.** With $K = 4$ and $N = 4$, their rule $I = K(N + 1)/2$ gives $I = 10$. The crossbar then has $N K = 16$ multiplexers with $I + N = 14$ inputs each.
- **The VTR 7.0 flagship cluster.** $N = 10$ elements with fracturable 6-LUTs (one 6-LUT or two 5-LUTs with shared inputs) and $I = 40$ inputs. This is a typical value of a named architecture, not part of the definition.
- **Commercial names.** Vendors call a cluster a configurable logic block, a slice or a logic array block, and their elements add carry chains and more flip-flops. The definition above is the academic form.
- **Non-example: a block with a sparse crossbar.** If the local routing is not a full crossbar, the two conditions above are still necessary but no longer enough: a set may meet them and still fail to route inside the cluster. Such clusters need a packer that routes, such as [AAPack](/aapack/).
- **Non-example: a memory or multiplier block.** These are hard blocks of a heterogeneous array. They are not clusters of LUTs, and packing fills them by other rules.
- **Non-example: a LUT alone.** A $K$-input LUT without its flip-flop and output multiplexer is the part that [LUT mapping](/lut-mapping/) produces, not an element. A cluster with $N = 1$, $I = K$ is one element in a block and is a valid, if small, cluster.

## Related definitions

- **K-feasible cut.** A LUT can implement a node of the netlist exactly when the node has a [K-feasible cut](/k-feasible-cut/); [LUT mapping](/lut-mapping/) covers the netlist with such cuts and gives the LUTs that become elements.
- **Packing.** [FPGA packing](/fpga-packing/) is the problem of grouping elements into legal clusters, and [T-VPack](/t-vpack/) and [AAPack](/aapack/) are two packers.
- **Choice of the parameters.** Betz, Rose and Marquardt measured that $I = K(N + 1)/2$ inputs let about 98% of the elements be used (Chapter 6). Ahmed and Rose measured area and delay over $K$ and $N$ and found the best area-delay product for $K$ from 4 to 6 and $N$ from 3 to 10. Both are measured results for their circuits and process.
- **Routing graph.** Inside a cluster, the crossbar is part of the [routing resource graph](/routing-resource-graph/) when a tool models it in detail, and a single node with pin classes when it does not.

## References
