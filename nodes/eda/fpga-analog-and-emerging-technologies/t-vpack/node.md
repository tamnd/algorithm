---
tag: R2R827
kind: algorithm
slug: t-vpack
name: T-VPack
aliases:
- VPack
- timing-driven packing
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: Marquardt, Betz and Rose's greedy packer that grows each cluster by adding the block with the most shared nets and most timing criticality until the cluster is full.
solves: [fpga-packing]
model: word-ram
complexity:
  vars: {n: the number of BLEs, N: the cluster size, K: the LUT size}
  time: {criticality: O(n K), packing: O(n^2 N K)}
  space: {total: O(n K)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1999
  people: [Alexander Marquardt, Vaughn Betz, Jonathan Rose]
  note: Betz and Rose's earlier packer of 1997 grew clusters by shared nets alone. Marquardt, Betz and Rose added a timing term to the attraction and a timing-based seed, and the packer became the packing step of VPR.
prereqs: [fpga-packing, fpga-logic-cluster, static-timing-analysis]
see_also: [aapack, greedy-algorithm, bin-packing, lut-mapping, fpga-timing-driven-annealing-placement, island-style-fpga, critical-path-method, routing-resource-graph]
sources:
  - paper: doi:10.1145/296399.296426
    title: Alexander Marquardt, Vaughn Betz and Jonathan Rose, Using cluster-based logic blocks and timing-driven packing to improve FPGA speed and density, Proceedings of the ACM/SIGDA International Symposium on Field Programmable Gate Arrays (FPGA '99), 37 to 46, 1999
    locator: the section on the timing-driven packing algorithm (the seed choice, the attraction function with its weight on criticality and the normalized count of shared nets, and the legality checks) and the experimental results against the packer without timing
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 3, Section 3.1 Logic Block Packing (forming BLEs from LUTs and flip-flops, and the greedy growth of clusters)
  - paper: "Vaughn Betz and Jonathan Rose, Cluster-based logic blocks for FPGAs, area-efficiency vs. input sharing and size, Proceedings of the IEEE Custom Integrated Circuits Conference (CICC), 1997"
    locator: the earlier packer that grows clusters by the number of shared nets (general locator)
---

T-VPack is a greedy algorithm for [FPGA packing](/fpga-packing/): it puts the basic logic elements (BLEs) of a mapped netlist into [logic clusters](/fpga-logic-cluster/) of at most $N$ BLEs and $I$ external inputs. It fills one cluster at a time, starting from the most timing-critical BLE that is left and adding, at each step, the BLE that fits and has the highest attraction, a mix of its criticality to the cluster and the number of nets it shares with it. The algorithm belongs to the FPGA CAD topic of this sub-area and is the packer of the VPR flow of Marquardt, Betz and Rose.

## In plain words

After LUT mapping, a design is a list of small logic pieces, each a lookup table with an optional flip-flop. The chip groups these pieces into clusters, and a wire inside a cluster is much faster and cheaper than a wire between clusters.

T-VPack fills the clusters one by one. It starts a new cluster with the piece that sits on the slowest path of the design. Then it keeps adding the piece that is most attracted to the cluster: a piece that talks to the cluster over a slow path, or that shares many signals with it. It adds a piece only if the cluster still has room and enough input pins.

When the cluster is full, or no remaining piece fits, it closes the cluster and starts the next one.

## The problem

**Input.** A list of $n$ BLEs. Each BLE has at most $K$ input nets, one output net, and a flag that says whether its flip-flop is used. Cluster parameters $N$ and $I$ with $K \le I$, and a weight $\lambda \in [0, 1]$.

**Output.** A partition of the BLEs into clusters $C$, each legal: $|C| \le N$ and $|\mathrm{ext}(C)| \le I$, where $\mathrm{ext}(C)$ is the set of nets that a member reads and no member drives. This is the legality rule of a cluster with a full crossbar.

**Goal.** Few clusters, and few critical connections between clusters. T-VPack does not minimize either one exactly.

## The algorithm

Before line L1, a [static timing analysis](/static-timing-analysis/) with unit delays gives each connection $(u, v)$ from a BLE $u$ to a reader $v$ a criticality $\mathrm{crit}(u, v) = 1 - \mathrm{slack}(u, v) / D$, where $D$ is the delay of the longest timing path. Each LUT has delay 1, connections have delay 0, and a flip-flop starts a new path. A BLE's criticality is the largest criticality of its connections. For a BLE $b$ and a cluster $C$:

- $\mathrm{Crit}(b, C)$ is the largest criticality of a connection between $b$ and a member of $C$, or 0;
- $\mathrm{Nets}(b)$ is the set of nets that $b$ reads or drives, and $\mathrm{Nets}(C)$ the union over its members;
- $\mathrm{attraction}(b, C) = \lambda \, \mathrm{Crit}(b, C) + (1 - \lambda) \, |\mathrm{Nets}(b) \cap \mathrm{Nets}(C)| / G$, with $G = K + 1$, the most nets that one BLE can touch.

```pseudo id=main
T-VPACK(B, N, I, K, λ)
L1  while some BLE is unclustered:
L2      seed ← the unclustered BLE of highest criticality (ties: more inputs, then lower index); C ← {seed}
L3      while |C| < N:
L4          for each unclustered BLE b:
L5              if |ext(C ∪ {b})| > I then skip b
L6              compute attraction(b, C)
L7          if every b was skipped then leave this loop
L8          add the kept b of highest attraction to C (ties: more inputs, then lower index)
L9      output C
```

A BLE that shares no net with the cluster has attraction 0, so line L8 then adds the BLE with the most inputs that fits. The paper fills a cluster in the same way when no connected BLE fits.

The implementation also has the step before packing that forms BLEs: a LUT and the flip-flop that its output feeds are merged into one BLE when the flip-flop is the only reader of that output. A flip-flop that cannot be merged gets a BLE of its own, whose LUT passes the data input through.

## Example

Take $K = 2$, $N = 2$, $I = 3$, $\lambda = 3/4$, and four BLEs: $a$ reads $x, y$ and drives $A$; $b$ reads $A, z$ and drives $B$; $c$ reads $w, x$ and drives $C$; $d$ reads $C, y$ and drives $D$. None is registered. The longest timing paths are $a \to b$ and $c \to d$, with $D = 2$, so both connections have criticality 1, and every BLE has criticality 1.

1. All four BLEs tie on criticality and on inputs, so the seed is $a$, and $C = \{a\}$ with $\mathrm{Nets}(C) = \{x, y, A\}$.
2. Line L5: $\mathrm{ext}(\{a, b\}) = \{x, y, z\}$, $\mathrm{ext}(\{a, c\}) = \{w, x, y\}$, $\mathrm{ext}(\{a, d\}) = \{x, y, C\}$, so all three fit.
3. Line L6: $b$ gets $\tfrac34 \cdot 1 + \tfrac14 \cdot \tfrac13 = \tfrac56$, since the connection $a \to b$ has criticality 1 and $b$ shares the net $A$. $c$ shares only $x$ and gets $\tfrac14 \cdot \tfrac13 = \tfrac1{12}$, and $d$ shares only $y$ and gets $\tfrac1{12}$.
4. Line L8 adds $b$. The cluster $\{a, b\}$ is full.
5. The next seed is $c$. $\mathrm{ext}(\{c, d\}) = \{w, x, y\}$ fits, and $d$ joins.

The result is $\{a, b\}$ and $\{c, d\}$: two clusters, which is the least possible for four BLEs with $N = 2$, and both critical connections are inside a cluster. The other pairing that keeps the critical connections apart, $\{a, c\}$ and $\{b, d\}$, is not even legal, since $\mathrm{ext}(\{b, d\}) = \{A, z, C, y\}$ has four nets.

## Correctness

The [full proof](proofs/correctness.md) shows the following.

- **Legality.** Each cluster that T-VPack outputs has at most $N$ BLEs and at most $I$ external input nets, and every BLE is in exactly one cluster. The seed is legal because a BLE has at most $K \le I$ inputs, and line L5 and line L3 keep both limits at each addition.
- **Termination.** Each outer pass clusters at least its seed, and each inner pass adds a BLE or ends the cluster.
- **Maximality.** A closed cluster is full, or no BLE that was unclustered at that moment fits into it.
- **Criticality.** The unit-delay analysis returns $\mathrm{crit}(u, v) = \ell(u, v) / D$, where $\ell(u, v)$ is the delay of the longest timing path through the connection.

What is not proved is the number of clusters. T-VPack is a heuristic, and it can use more clusters than needed.

## Complexity

The timing analysis is two passes over the connections, $O(n K)$. In the implementation, each addition at line L8 scans all unclustered BLEs, and each candidate costs $O(N K)$ for the external inputs and $O(N)$ for $\mathrm{Crit}$. There are at most $n$ additions and $n$ closed clusters, so packing takes $O(n^2 N K)$ time. The space is $O(n K)$ for the netlist and the criticalities.

VPR keeps, for the open cluster, only the BLEs that share a net with it, with their attraction updated when a BLE joins, so a step does not look at the whole netlist. Its running time is close to linear in practice; this is a measured property of the tool, not a bound proved here.

## Properties

- **Not optimal.** Take $K = 2$, $N = 2$, $I = 2$ and four BLEs: $o_0$ reads $i_0$; $o_1$ reads $o_0$; $o_2$ reads $i_0$ and $o_0$; $o_3$ reads $o_1$ (each BLE is named after its output). The connections $o_0 \to o_1$ and $o_1 \to o_3$ have criticality 1 and $o_0 \to o_2$ has $2/3$. T-VPack seeds with $o_0$ and adds $o_1$ (attraction $5/6$ against $2/3$ for $o_2$). Then $o_3$ seeds the next cluster, and $\{o_3, o_2\}$ needs the three inputs $o_1, i_0, o_0$, so $o_2$ ends alone: 3 clusters. The partition $\{o_0, o_2\}$, $\{o_1, o_3\}$ is legal with 2. With $\lambda = 0$ the packer finds that partition, so the timing term costs a cluster here.
- **Deterministic.** All ties are broken by fixed rules, so the same input gives the same clusters.
- **Greedy and final.** A BLE never leaves its cluster. The method makes one pass and has no local search.
- **The weight.** $\lambda = 1$ packs for delay only and $\lambda = 0$ for shared nets only. Marquardt, Betz and Rose report that a large weight on timing gives faster circuits at almost the same cluster count; that is a measured result on their benchmarks.

## Variants and improvements

- **Without timing.** The earlier packer of Betz and Rose (1997) is the case $\lambda = 0$, with the seed chosen by the most used inputs instead of by criticality.
- **Ties by timing.** The paper breaks ties among equally critical BLEs with more timing measures. This page breaks them by inputs and index.
- **Clock limits.** A real cluster has a few clock pins, so the check of line L5 also counts the distinct clocks.
- **Hill climbing.** A BLE that drives a net that the cluster reads removes that net from $\mathrm{ext}(C)$. So a packer can let the input count go above $I$ for a while, in the hope that a later BLE absorbs nets, and undo the steps if it does not.
- **Complex blocks.** [AAPack](/aapack/) keeps the greedy growth and the attraction, but checks each candidate by placing it in a slot and routing it inside the cluster, which handles sparse local routing, modes and hard blocks.
- **Placement-aware packing.** Later packers use the placement, or a quick estimate of it, to choose the BLEs of a cluster.

## When to use it

Use T-VPack, or its successor in VTR, to pack a LUT netlist into homogeneous clusters with a full crossbar, where the two counting conditions are the whole legality rule. It is fast and simple, and the timing term keeps critical paths inside clusters. For clusters whose local routing is sparse, or for blocks with modes, use [AAPack](/aapack/), because the input count no longer tells whether a cluster can be routed. When the cluster count matters more than speed, lower $\lambda$.

## Pitfalls

- **Counting inputs per BLE.** The limit is on distinct external nets of the cluster. A net that two members read takes one pin, and a net that a member drives takes none.
- **Forgetting nets that leave.** An output that is read outside the cluster leaves on its own output pin. It does not count against $I$ but it does go into $\mathrm{Nets}(C)$.
- **Stale criticality.** The criticalities are computed once, before packing, with a delay model that does not know which connections end up inside clusters. A packer that updates them as it goes pays for more timing analyses.
- **A BLE wider than the cluster.** If $K > I$, a BLE with $K$ distinct inputs fits nowhere. The implementation raises an error.
- **Combinational loops.** The timing analysis needs every cycle to pass through a flip-flop.

## Implementations

## History

Betz and Rose (1997) built a greedy packer that seeds a cluster with the BLE of the most used inputs and grows it by shared nets, and used it to study the cluster size and the number of inputs. Marquardt, Betz and Rose (1999) added the timing-driven seed and the attraction that mixes criticality with shared nets, and reported faster circuits at about the same area. Their packer was the packing step of VPR for many years, and its greedy structure carried over to AAPack in the VTR flow.

## References
