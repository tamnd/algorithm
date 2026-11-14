---
tag: VB1R58
kind: concept
slug: universal-switch-block
name: Universal switch block
aliases:
- Chang-Wong-Wong universal switch module
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: An FPGA switch block that can route every set of two-pin connections that its side widths allow, built by Chang, Wong and Wong with the fewest switches, 6W for W tracks a side.
prereqs: [fpga-switch-block, edge-coloring, petersens-theorem]
see_also: [island-style-fpga, routing-resource-graph, minimum-channel-width, sat-based-fpga-routing, chromatic-index, konig-theorem, eulerian-circuit]
sources:
  - paper: doi:10.1145/225871.225886
    title: Yao-Wen Chang, D. F. Wong and C. K. Wong, Universal switch modules for FPGA design, ACM Transactions on Design Automation of Electronic Systems 1(1), 80 to 101, 1996
    locator: the definition of a universal switch module by the dimension constraint, the construction with 6W switches and Fs = 3, the proof that fewer switches cannot be universal, and the proof that the XC4000-type module is not universal
  - paper: "Yao-Wen Chang, D. F. Wong and C. K. Wong, Universal switch-module design for symmetric-array-based FPGAs, Proceedings of the ACM Symposium on Field-Programmable Gate Arrays (FPGA '96), 80 to 86, 1996"
    locator: the conference version of the construction
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 7, Detailed Routing Architecture (switch block patterns compared inside a full routing flow; general locator)
---

A universal switch block is an [FPGA switch block](/fpga-switch-block/) with $W$ tracks on each of its four sides that can route every set of two-pin connections in which no side has more than $W$ connections. Chang, Wong and Wong defined it in 1996, built one with $6W$ switches, and proved that no switch block with fewer switches is universal. The planar pattern of the Xilinx XC4000 family has the same $6W$ switches but is not universal. The concept belongs to the FPGA CAD topic of this sub-area; in content it is a definition with a theorem, which this page states and proves.

## In plain words

At a crossing of two routing channels, each side has a fixed number of tracks. Some nets must turn from one side to another, and some must go straight. Each net uses one switch, and no two nets may use the same track end.

If too many nets want the same side, no switch block can help, because the side runs out of track ends. A universal block is one that never fails for any other reason: whenever every side has room, it finds a track for every net.

The cheap pattern that keeps each net on the same track number fails on a small case: three nets that turn around three sides of the crossing need three different tracks when only two exist. The universal block avoids this by letting some turns swap tracks, and it does so with no more switches than the cheap pattern.

## The idea

### The model

Name the sides $T$, $R$, $B$ and $L$, each with terminals $0$ to $W - 1$. A switch block is a graph $S$ on the $4W$ terminals whose edges join different sides. A *requirement* is a finite list of nets, each a pair $\{a, b\}$ of different sides. Write it as a loopless [multigraph](/multigraph/) $H$ on the vertex set $\{T, R, B, L\}$ with one edge for each net. The *density condition*, which Chang, Wong and Wong call the dimension constraint, is

$$\deg_H(s) \le W \quad \text{for each side } s.$$

A *routing* of $H$ in $S$ gives each net $\{a, b\}$ one switch $\{(a, i), (b, j)\} \in S$, such that no terminal is used by two nets. The block $S$ is **universal** when every $H$ that meets the density condition has a routing in $S$.

The condition is necessary for every block, since a side with more than $W$ nets has too few terminals. So a universal block is one that routes everything that any block could route.

### The lower bound of 6W

**Theorem 1.** Every universal block on four sides with $W$ tracks has at least $6W$ switches.

*Proof.* Fix two sides $a \ne b$. The requirement with $W$ nets $\{a, b\}$ meets the density condition. A routing uses $W$ switches between $a$ and $b$ with pairwise different terminals, so every terminal of $a$ has a switch to side $b$. This holds for each of the three sides $b \ne a$, so every terminal has degree at least 3, and the block has at least $4W \cdot 3 / 2 = 6W$ switches. $\square$

So a universal block with exactly $6W$ switches has $F_s = 3$, and between any two sides its switches form a perfect matching, given by a permutation $\pi_{ab}$ of the tracks.

### The case W = 2

For $W = 2$, a block with $F_s = 3$ is given by one bit $c_{ab}$ for each of the six pairs of sides: $c_{ab} = 0$ means the switches are $(a, i)(b, i)$, and $c_{ab} = 1$ means they are $(a, i)(b, 1 - i)$.

**Lemma 2.** A block with $W = 2$ and $F_s = 3$ is universal if and only if $c$ sums to an odd number on each of the four triangles of side pairs and to an even number on each of the three 4-cycles.

*Proof.* Let $H$ have maximum degree at most 2. Then each connected component of $H$ is a path or a cycle, of length 2, 3 or 4, since there are only four vertices. Components share no side, so they can be routed one at a time.

A routing gives each end of each net a track: if the net $\{a, b\}$ uses track $t$ on side $a$, it uses track $t \oplus c_{ab}$ on side $b$. The routing is legal exactly when the two nets at a side of degree 2 use different tracks there. On a path, choose the track of the first end freely. Each edge then fixes the track at its far end, and at each inner vertex the next net must take the other track, which is always possible. So every path routes. On a cycle of length $\ell$, going once around flips the track $\ell$ times at the vertices and adds $c_{ab}$ on each edge, so the start track comes back to itself if and only if $\ell + \sum_{\text{cycle}} c_{ab}$ is even. A cycle of length 2 has the same pair twice, so its sum is $2 c_{ab}$, which is even. A triangle needs an odd sum, and a 4-cycle needs an even sum.

Conversely, if some triangle or 4-cycle breaks its parity rule, the requirement made of that cycle meets the density condition and has no routing, by the same argument. $\square$

All bits zero is the planar pattern, where every triangle has the sum 0, so it fails on the three nets $T L$, $L B$, $B T$. The choice used on this page is $c_{TR} = c_{BL} = 1$ and the other four bits 0. Each triangle holds exactly one of the edges $TR$ and $BL$, so its sum is 1, and each 4-cycle holds both of them or neither, so its sum is 0 or 2.

### Any W

Let $k = \lfloor W/2 \rfloor$. The block $U_W$ puts a copy of the $W = 2$ block on each pair of tracks $\{2j, 2j + 1\}$ for $0 \le j < k$, with the same pair on all four sides. If $W$ is odd, the last track $W - 1$ gets the six switches $(a, W - 1)(b, W - 1)$. So $U_W$ has $12k + 6(W - 2k) = 6W$ switches.

**Lemma 3.** Let $W$ be odd and $H$ a loopless multigraph on four vertices with maximum degree at most $W$. Then $H$ has a matching that covers every vertex of degree $W$.

*Proof.* Let $D$ be the set of vertices of degree $W$, and write $m_{xy}$ for the number of edges between $x$ and $y$.

- $|D| = 0$: the empty matching.
- $|D| = 1$: the vertex has degree $W \ge 1$, so take one of its edges.
- $|D| = 2$, $D = \{u, v\}$: if $m_{uv} \ge 1$, take that edge. If not, the edges of $u$ and of $v$ all go to the other two vertices $x$ and $y$. If both $u$ and $v$ had neighbors only in $\{x\}$, then $\deg x \ge 2W$, which is too large. So $u$ and $v$ have different neighbors among $x$ and $y$, and the two edges form a matching.
- $|D| = 3$, $D = \{u, v, w\}$, with $z$ the fourth vertex: a matching that covers three vertices has two edges, so it is perfect. Assume no perfect matching exists. The degree sum is even and $3W$ is odd, so $\deg z$ is odd and $z$ has a neighbor, say $u$. Then $m_{vw} = 0$, or $\{uz, vw\}$ is a perfect matching. If $m_{uv} = 0$, then all $W$ edges of $v$ go to $z$, and $\deg z \ge W + m_{uz} > W$. So $m_{uv} \ge 1$, which forces $m_{wz} = 0$, and then all $W$ edges of $w$ go to $u$. Then $m_{uw} \ge 1$ forces $m_{vz} = 0$, and all $W$ edges of $v$ go to $u$. Now $\deg u \ge 2W + 1$, a contradiction.
- $|D| = 4$: $H$ is $W$-regular. From $\deg u + \deg v - \deg w - \deg z = 0$ we get $m_{uv} = m_{wz}$, and in the same way $m_{uw} = m_{vz}$ and $m_{uz} = m_{vw}$. The three numbers $m_{uv}$, $m_{uw}$, $m_{uz}$ sum to $W \ge 1$, so one of them is positive, and that pairing gives a perfect matching. $\square$

**Theorem 4.** $U_W$ is universal for every $W \ge 1$.

*Proof.* Let $H$ meet the density condition. If $W$ is odd, take the matching $M$ of Lemma 3 and route its nets on track $W - 1$: each side is in at most one edge of $M$, so no terminal is used twice. The rest $H' = H - M$ has maximum degree at most $W - 1 = 2k$, since $M$ covers every vertex of degree $W$. If $W$ is even, $H' = H$ and $W = 2k$.

Next split $H'$ into $k$ parts of maximum degree at most 2. Take two copies of $H'$ and, for each vertex $v$, join its two copies by $2k - \deg_{H'}(v)$ parallel edges. The result is a loopless $2k$-regular multigraph. By [Petersen's 2-factor theorem](/petersens-theorem/), whose proof by an [Eulerian circuit](/eulerian-circuit/) and [König's theorem](/konig-theorem/) on a regular bipartite multigraph also holds for multigraphs, its edges split into $k$ 2-factors. Restricted to the first copy, they split the edges of $H'$ into $k$ subgraphs of maximum degree at most 2. Route subgraph $j$ on the track pair $\{2j, 2j + 1\}$ by Lemma 2. Different pairs and the last track use different terminals, so the whole routing is legal. $\square$

With Theorem 1, $U_W$ has the fewest switches that a universal block can have. Chang, Wong and Wong give their own construction and proof. The one above is a short way to reach the same result.

### Limits of the idea

Universality is a property of one switch block. A net in an array passes several blocks, and it must use the same track on the channel segment between two of them. So an array of universal blocks still needs a search for a detailed routing, and the global problem stays hard. The idea also assumes bidirectional switches, one switch per net in the block, and two-pin connections. A net with three or more pins at one block needs more than one switch there.

## Examples

**Three turning nets, W = 2.** The nets are $T L$, $L B$ and $B T$. In $U_2$, the pairs $T L$ and $B T$ keep the track, and $L B$ swaps it. Route $T L$ from $(T, 0)$ to $(L, 0)$. Then $L B$ must start at $(L, 1)$ and swaps to $(B, 0)$. Then $B T$ starts at $(B, 1)$ and ends at $(T, 1)$. Each side uses tracks 0 and 1 once each. The planar pattern fails here, as the proof of Lemma 2 shows.

**A full requirement, W = 3.** Take two nets $T R$, two nets $B L$, one net $T B$ and one net $R L$. Every side has degree 3, so the set $D$ of Lemma 3 holds all four sides, and the pairing $\{TR, BL\}$ has both edges, so $M$ is one net $T R$ and one net $B L$, routed on track 2. The rest is the 4-cycle $T, R, L, B$. Route the second $T R$ from $(T, 0)$ to $(R, 1)$ (a swap), then $R L$ from $(R, 0)$ to $(L, 0)$, then the second $B L$ from $(L, 1)$ to $(B, 0)$ (a swap), and $T B$ from $(B, 1)$ to $(T, 1)$.

**Counts.** For $W = 1$ to 4 there are 10, 56, 214 and 641 requirements that meet the density condition. $U_W$ routes all of them. The planar pattern fails on 0, 4, 24 and 88 of them; for $W = 2$, the four failures are the four triangles.

## Where it is used

- **Architecture of the switch blocks.** The result tells an architect that routability of one block costs no extra switches: the same $6W$ switches as the planar pattern can route every requirement. Chang, Wong and Wong also show that the XC4000-type pattern and the anti-symmetric patterns are not universal, and compare the patterns in experiments with a router.
- **Routing and channel width.** A router on an array with universal blocks never fails inside one block for lack of a switch, only for lack of tracks. The effect on the [minimum channel width](/minimum-channel-width/) of a whole design is measured, not proved. Betz, Rose and Marquardt compare several patterns inside a full flow in Chapter 7.
- **Exact routing.** With the planar pattern, the track choice is a [graph coloring](/graph-coloring/) of the nets; with other patterns it is a constraint problem that [SAT-based FPGA routing](/sat-based-fpga-routing/) solves exactly. The [routing resource graph](/routing-resource-graph/) holds the pattern as edges.
- **Edge coloring.** For the planar pattern, routing one block is an [edge coloring](/edge-coloring/) of $H$ with $W$ colors. A triangle with one edge per side pair has [chromatic index](/chromatic-index/) 3 but maximum degree 2, which is why the planar pattern fails. Universal blocks avoid the need for an edge coloring with $\Delta$ colors.

## References
