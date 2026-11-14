---
tag: 4EE5Y2
kind: problem
slug: fpga-packing
name: FPGA packing
aliases:
- FPGA clustering
- logic block packing
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: Group LUTs and flip-flops into the logic clusters of an FPGA under limits on cluster size and inputs, so that delay and routing demand between clusters are low.
prereqs: [fpga-logic-cluster, lut-mapping]
see_also: [t-vpack, aapack, bin-packing, bin-packing-np-hardness, maximum-matching, island-style-fpga, hypergraph-partitioning, fpga-timing-driven-annealing-placement]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A, problem [SR1] Bin Packing (NP-complete in the strong sense) and problem [GT11] Partition into Triangles
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 3, Section 3.1 Logic Block Packing (the packing step of the CAD flow and its legality rules)
  - paper: doi:10.1145/296399.296426
    title: Alexander Marquardt, Vaughn Betz and Jonathan Rose, Using cluster-based logic blocks and timing-driven packing to improve FPGA speed and density, Proceedings of the ACM/SIGDA International Symposium on Field Programmable Gate Arrays (FPGA '99), 37 to 46, 1999
    locator: the packing problem with the limits N and I and the timing-driven objective
  - paper: doi:10.1145/1950413.1950457
    title: Jason Luu, Jason H. Anderson and Jonathan Rose, Architecture description and packing for logic blocks with hierarchy, modes and complex interconnect, Proceedings of the ACM/SIGDA International Symposium on Field Programmable Gate Arrays (FPGA '11), 227 to 236, 2011
    locator: packing for logic blocks whose legality depends on the local interconnect, not only on counts
---

FPGA packing is the step of the FPGA CAD flow that groups the LUTs and flip-flops of a mapped netlist into the [logic clusters](/fpga-logic-cluster/) of the chip. Each cluster has room for at most $N$ basic logic elements (BLEs) and at most $I$ input nets from outside, and the clusters are then placed and routed as single blocks. The problem asks for few clusters, and for few connections between clusters on the critical paths, since a connection inside a cluster is fast and uses no general routing.

## In plain words

After [LUT mapping](/lut-mapping/), the design is a long list of small logic pieces. The chip does not hold them one by one: it holds them in groups, and each group has a fixed number of seats and a fixed number of input wires.

Packing chooses the groups. Pieces that talk to each other a lot should sit in the same group, because a signal inside a group is fast and needs no long wire. A group must not need more input wires than it has. Fewer groups mean a smaller chip, and fewer slow signals between groups mean a faster design.

## Definition

**Input.**

- A netlist of $n$ BLEs. BLE $b$ has a set of at most $K$ input nets, one output net, and a flag for its flip-flop. A BLE is formed from a LUT and the flip-flop that only it feeds.
- The cluster parameters: the size $N$ and the number of input pins $I$, with $K \le I$.
- For the timing form, a delay model with a delay for a connection inside a cluster and a larger one for a connection between clusters.

**Output.** A partition of the BLEs into clusters $C_1, \ldots, C_m$.

**Constraints.** Each cluster is legal. Let $\mathrm{ext}(C)$ be the set of nets that some member of $C$ reads and no member drives. With the full local crossbar of the [logic cluster](/fpga-logic-cluster/) definition, $C$ is legal if and only if

$$|C| \le N \quad\text{and}\quad |\mathrm{ext}(C)| \le I,$$

and its BLEs use at most the number of clocks that the cluster has. With sparse local routing, a cluster is legal when a routing of its nets exists inside it, which is a stronger condition.

**Objective.** The basic form minimizes $m$, the number of clusters. The timing form minimizes the delay of the longest path when connections between clusters are slow, and the routability form minimizes the number of nets that leave clusters. Real packers mix the three.

**Decision form.** Given the netlist, $N$, $I$ and $m$, decide whether a legal partition into at most $m$ clusters exists.

## Variants

- **Cluster count only.** Minimize $m$ with the two counting limits. This is the form whose hardness is shown below.
- **Timing-driven.** Keep the connections of critical paths inside clusters. [T-VPack](/t-vpack/) targets this form.
- **Routability-driven.** Lower the number of nets that cross between clusters, and leave some pins free so that the clusters are easier to route to.
- **Complex blocks.** Blocks with hierarchy, modes, carry chains, memories and multipliers, where legality is a routing check inside the block. [AAPack](/aapack/) targets this form.
- **Depopulated clusters.** Fill clusters below $N$ on purpose to spread congestion, at the cost of more clusters.

## Examples

**A hand instance.** Take $K = 2$, $N = 2$, $I = 3$ and four BLEs: $a$ reads $x, y$ and drives $A$; $b$ reads $A, z$ and drives $B$; $c$ reads $x, w$ and drives $C$; $d$ reads $C, y$ and drives $D$.

| cluster | external nets | legal |
| --- | --- | --- |
| $\{a, b\}$ | $x, y, z$ | yes |
| $\{c, d\}$ | $x, w, y$ | yes |
| $\{a, c\}$ | $x, y, w$ | yes |
| $\{b, d\}$ | $A, z, C, y$ | no |
| $\{a, d\}$ | $x, y, C$ | yes |
| $\{b, c\}$ | $A, z, x, w$ | no |

Two clusters is the least possible, since $\lceil 4 / 2 \rceil = 2$, and $\{a, b\}, \{c, d\}$ reaches it. It also keeps the connections $a \to b$ and $c \to d$ inside clusters. The pairing $\{a, c\}, \{b, d\}$ is not legal, and the pairing $\{a, d\}, \{b, c\}$ is not either, so the optimum is unique.

**Absorbed nets.** In $\{a, b\}$ the net $A$ is driven inside, so it needs no input pin. Adding a BLE to a cluster can lower the input count, which is why the limit cannot be checked BLE by BLE.

## Known algorithms

- **Greedy growth.** [T-VPack](/t-vpack/) fills one cluster at a time from a critical seed, adding the BLE of highest attraction that fits. Every cluster that it outputs is legal and each closed cluster is full or admits no remaining BLE, but it has no guarantee on the number of clusters; its page has a 4-BLE netlist where it uses 3 clusters and 2 suffice.
- **Greedy growth with a routing check.** [AAPack](/aapack/) grows clusters in the same way and checks each addition by placing the BLE in a slot of the block and routing inside the block. The result is legal for the block's real interconnect, with no guarantee on the count.
- **Partitioning.** A [hypergraph partitioning](/hypergraph-partitioning/) of the netlist into parts of size $N$ lowers the nets between parts, and the parts are then repaired to meet the input limit. This gives no legality by itself.
- **Exact search.** For tiny netlists, a dynamic program over subsets finds the least number of clusters: $\mathrm{best}(S) = 1 + \min \mathrm{best}(S \setminus C)$ over legal $C \subseteq S$ that hold the lowest element of $S$. It takes $O(3^n)$ steps and is the brute force that the tests of the packer pages use.
- **Clusters of two.** For $N = 2$ the problem is a [maximum matching](/maximum-matching/): join two BLEs by an edge when the pair is legal. A partition into $m$ clusters of size at most 2 has $n - m$ pairs, and the pairs are a matching, so the least $m$ is $n$ minus the size of a maximum matching, which [Edmonds' blossom algorithm](/edmonds-blossom/) finds in polynomial time.

## Bounds

- **Size.** $m \ge \lceil n / N \rceil$.
- **Inputs.** If the BLEs read $p$ nets that no BLE drives, each such net uses a pin in every cluster that reads it, so $m \ge \lceil p / I \rceil$.
- **Trivial upper bound.** $m \le n$, with one BLE per cluster, which is legal since $K \le I$.

## Reductions

**Theorem 1 (strong NP-hardness).** The decision form of the cluster count problem is NP-complete in the strong sense when $K$, $N$ and $I$ are part of the input.

*Proof.* It is in NP: a partition is checked in polynomial time. For hardness, reduce from [bin packing](/bin-packing/) in its decision form: item sizes $a_1, \ldots, a_n$, a capacity $B$ with each $a_j \le B$, and a number $m$ of bins. Bin packing is NP-complete in the strong sense (Garey and Johnson, [SR1]; see also [the hardness proof of bin packing](/bin-packing-np-hardness/)), so we may assume that the sizes are written in unary. Build BLE $j$ with $a_j$ input nets of its own, used by no other BLE, and an output net that no BLE reads. Set $K = \max_j a_j$, $N = n$ and $I = B$. No net is shared and no BLE drives a net that another reads, so $|\mathrm{ext}(C)| = \sum_{j \in C} a_j$, and $C$ is legal if and only if its items fit in one bin. So a legal partition into $m$ clusters exists if and only if the items fit into $m$ bins. The netlist has $\sum_j a_j + n$ nets, which is polynomial in the unary size. $\square$

**Theorem 2 (hard already for clusters of three).** The decision form is NP-complete when $N = 3$, with $K$ and $I$ part of the input.

*Proof.* Reduce from partition into triangles (Garey and Johnson, [GT11]): given a graph $H$ with $3q$ vertices, decide whether its vertices split into $q$ triangles. Let $\Delta = \max(3, \text{the largest degree of } H)$. Make one BLE per vertex $v$. It reads one net per edge at $v$, shared with the other end of that edge, plus $\Delta - \deg(v)$ nets of its own, so it reads exactly $\Delta$ nets; its output is read by no BLE. Set $K = \Delta$, $N = 3$ and $I = 3\Delta - 3$. A set of three BLEs with $e$ edges of $H$ among them reads $3\Delta - e$ distinct nets, so it is legal if and only if $e = 3$, that is, it is a triangle. A set of at most two BLEs reads at most $2\Delta \le 3\Delta - 3$ nets and is always legal. A partition into $q$ clusters of size at most 3 covers $3q$ BLEs, so every cluster has exactly three BLEs and is a triangle. Conversely, a partition into triangles gives $q$ legal clusters. $\square$

A brute force over 200 random graphs on 6 vertices (seed 2) agrees with Theorem 2 on every instance, 28 of them with a partition into triangles; this checks the construction, not the theorem. With Theorem 2 and the matching algorithm, the cluster count problem is polynomial for $N \le 2$ and NP-complete for $N = 3$. This page gives no result for fixed $K$, $N$ and $I$ together.

## Applications

- **The FPGA CAD flow.** Packing runs between [LUT mapping](/lut-mapping/) and placement, such as [timing-driven annealing placement](/fpga-timing-driven-annealing-placement/). Its result fixes how many blocks the placer and the router must handle.
- **Architecture studies.** Betz, Rose and Marquardt chose the number of cluster inputs by packing benchmarks at different $I$ and measuring how full the clusters became.
- **Heterogeneous blocks.** Packing also fills memory and multiplier blocks and the carry chains of logic blocks, each with its own legality rules.

## References
