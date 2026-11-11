---
tag: J09ZRC
kind: theorem
slug: diameter-lower-bound-distributed
name: Distributed diameter lower bound
aliases:
- Omega(n) diameter lower bound in CONGEST
area: distributed/distributed-graph-algorithms
level: research
summary: In CONGEST, the exact diameter needs Ω(n/log n) rounds, even on graphs of constant diameter. The proof reduces two-party set disjointness on n^2 bits to a cut of O(n) links.
prereqs: [distributed-diameter, congest-model, disjointness-problem, communication-complexity, round-complexity]
see_also: [distributed-diameter, distributed-apsp, peleg-rubinovich-lower-bound, disjointness-problem, randomized-communication-complexity, network-diameter-estimation, distributed-shortest-paths, congest-model]
sources:
  - paper: doi:10.1137/1.9781611973099.91
    title: Silvio Frischknecht, Stephan Holzer and Roger Wattenhofer, Networks cannot compute their diameter in sublinear time, SODA 2012
    locator: pages 1150 to 1162, the main theorem Ω(n/log n) for the exact diameter on graphs of constant diameter, and the reduction from set disjointness
  - paper: "Amir Abboud, Keren Censor-Hillel and Seri Khoury, Near-linear lower bounds for distributed distance computations, even in sparse networks, DISC 2016"
    locator: Theorem 1.1 (exact diameter on sparse graphs, Ω(n/log^2 n)), Theorem 1.2 ((3/2 - ε)-approximation of the diameter, Ω(n/log^3 n)), Section 2.1 (the bit gadget); arXiv 1605.05109
  - paper: "Stephan Holzer, David Peleg, Liam Roditty and Roger Wattenhofer, Distributed 3/2-approximation of the diameter, DISC 2014"
    locator: brief announcement, pages 562 to 564, the O((n log n)^(1/2) + D) algorithm
  - paper: "David Peleg, Liam Roditty and Elad Tal, Distributed algorithms for network diameter and girth, ICALP 2012"
    locator: the O(n) algorithm for the exact diameter
  - paper: "Ofer Grossman, Seri Khoury and Ami Paz, Improved hardness of approximation of diameter in the CONGEST model, DISC 2020"
    locator: Ω(n/log n) rounds to tell diameter 3 from diameter 5; doi:10.4230/LIPIcs.DISC.2020.19
---

## Statement

The model is [CONGEST](/congest-model/) with messages of $B$ bits: in each synchronous round, each node sends at most one message of $B$ bits over each of its links. An algorithm computes the diameter if, at the end, some node (or each node) outputs the diameter of the network, which is the largest hop distance between two nodes.

**Theorem (Frischknecht, Holzer and Wattenhofer, SODA 2012).** For each $n$ there are networks with $n$ nodes and constant diameter on which each deterministic or randomized (Monte Carlo, with error probability at most $1/3$) algorithm that computes the diameter needs $\Omega(n/B)$ rounds. With $B = O(\log n)$ this is $\Omega(n/\log n)$ rounds.

The bound holds already for the question "is the diameter 2 or 3?" in the form proved below. The same holds for the original construction, where the question is "is the diameter 4 or 5?". In both forms, the networks are dense: they have $\Theta(n^2)$ links.

**Extension (Abboud, Censor-Hillel and Khoury, DISC 2016).** Each algorithm that computes a $(3/2 - \epsilon)$-approximation of the diameter, for a constant $\epsilon > 0$, needs $\Omega(n/\log^3 n)$ rounds, also on sparse networks. The exact diameter needs $\Omega(n/\log^2 n)$ rounds on networks with $O(n \log n)$ links.

## In plain words

To find the diameter, the network must, in effect, check every pair of nodes. The proof builds a network that is two halves joined by a "waist" of about $n$ links. Each half holds about $n^2$ bits of secret data, written into which links exist inside it. The diameter is 3 if the two secrets share a 1 in the same position, and 2 otherwise.

Two people, one for each half, could solve this "do our sets meet?" question by running the network algorithm and sending each other only the messages that cross the waist. It is known that this question needs about $n^2$ bits of talk between the two people. The waist carries only about $n \log n$ bits in each round, so the algorithm needs about $n/\log n$ rounds.

## Proof

The proof is a reduction from two-party [set disjointness](/disjointness-problem/). The gadget below is a simple form of the construction, with the same parameters as in the paper: $\Theta(n^2)$ bits of input and a cut of $\Theta(n)$ links. The paper's own graphs differ in detail.

**Set disjointness.** Alice holds $x \in \{0, 1\}^K$ and Bob holds $y \in \{0, 1\}^K$. They must decide whether there is an index $t$ with $x_t = y_t = 1$. Each randomized protocol with error at most $1/3$ needs $\Omega(K)$ bits of communication (Kalyanasundaram and Schnitger, 1992; Razborov, 1992). See [randomized communication complexity](/randomized-communication-complexity/).

**The gadget.** Let $k \ge 1$ and $K = k^2$, and index the bits of $x$ and $y$ by pairs $(i, j)$ with $1 \le i, j \le k$. The graph $G_{x, y}$ has $n = 4k + 2$ nodes:

$$L = \{\ell_1, \ldots, \ell_k\}, \quad L' = \{\ell'_1, \ldots, \ell'_k\}, \quad R = \{r_1, \ldots, r_k\}, \quad R' = \{r'_1, \ldots, r'_k\}, \quad c_L, \quad c_R.$$

The links that do not depend on the input:

1. each of $L$, $L'$, $R$ and $R'$ is a clique;
2. $c_L$ is joined to every node of $L \cup L'$, and $c_R$ to every node of $R \cup R'$;
3. the *cut*: $\{\ell_i, r_i\}$ and $\{\ell'_i, r'_i\}$ for each $i$, and $\{c_L, c_R\}$.

The links that encode the input:

4. Alice's side: $\{\ell_i, \ell'_j\}$ is a link if and only if $x_{ij} = 0$;
5. Bob's side: $\{r_i, r'_j\}$ is a link if and only if $y_{ij} = 0$.

The cut has $2k + 1$ links, and the left side $L \cup L' \cup \{c_L\}$ depends only on $x$, the right side only on $y$.

**Lemma.** The diameter of $G_{x, y}$ is 2 if $x$ and $y$ are disjoint, and 3 otherwise.

*Proof.* The graph is not complete, so the diameter is at least 2. Check each kind of pair.

- Two nodes in the same set among $L, L', R, R'$: distance 1 (clique).
- $L$ and $L'$: both are joined to $c_L$, so distance at most 2. The same holds for $R$ and $R'$.
- $c_L$ and any node: $c_L$ is joined to $L \cup L' \cup \{c_R\}$, and $c_R$ is joined to $R \cup R'$, so distance at most 2. The same holds for $c_R$.
- $\ell_i$ and $r_j$: if $i = j$, distance 1. If $i \ne j$, the path $\ell_i, \ell_j, r_j$ has length 2. The same holds for $\ell'_i$ and $r'_j$.
- $\ell_i$ and $r'_j$: the neighbours of $\ell_i$ are $L$, $c_L$, $r_i$, and the $\ell'_{j'}$ with $x_{ij'} = 0$. The neighbours of $r'_j$ are $R'$, $c_R$, $\ell'_j$, and the $r_{i'}$ with $y_{i'j} = 0$. A common neighbour exists if and only if $\ell'_j$ is a neighbour of $\ell_i$ (that is, $x_{ij} = 0$) or $r_i$ is a neighbour of $r'_j$ (that is, $y_{ij} = 0$). Otherwise the distance is 3, by the path $\ell_i, c_L, c_R, r'_j$.
- $\ell'_j$ and $r_i$: by the same check, the distance is 2 if $x_{ij} = 0$ or $y_{ij} = 0$, and 3 otherwise.

So some pair is at distance 3 if and only if some $(i, j)$ has $x_{ij} = y_{ij} = 1$. $\square$

**The simulation.** Let $\mathcal{A}$ be an algorithm that computes the diameter in $r$ rounds on all graphs with $n$ nodes. Alice and Bob run $\mathcal{A}$ on $G_{x, y}$ together. Alice simulates the nodes of the left side and Bob the nodes of the right side. Each of them knows all links of its own side and the fixed cut links. In each round, each simulated node computes its messages from its state. A message over a link inside one side stays with the player who simulates both ends. A message over a cut link is sent to the other player. With shared random bits, a randomized $\mathcal{A}$ is simulated in the same way. After $r$ rounds, some simulated node outputs the diameter. The player who simulates it sends one more bit to the other player, so both know whether the diameter is 2 or 3, and by the lemma whether $x$ and $y$ meet.

**The counting.** In each round, each of the $2k + 1$ cut links carries at most $B$ bits in each direction, so the protocol sends at most $2(2k + 1)B\, r$ bits. Set disjointness on $K = k^2$ bits needs $\Omega(k^2)$ bits, so

$$2(2k + 1)B\, r = \Omega(k^2), \qquad r = \Omega\Big(\frac{k}{B}\Big) = \Omega\Big(\frac{n}{B}\Big).$$

With $B = O(\log n)$ this gives $\Omega(n/\log n)$ rounds. The diameter of every graph in the family is at most 3, so the bound holds even for networks of constant diameter. For an $n$ that is not of the form $4k + 2$, add up to three extra nodes on the left side, each joined to $c_L$ and to all of $L \cup L'$. Each extra node is within distance 2 of every node (through $c_L$, $\ell_i$ or $\ell'_j$), so the lemma still holds. $\blacksquare$

## Consequences

- **APSP is hard.** [Distributed APSP](/distributed-apsp/) gives the diameter in $O(D)$ more rounds, so APSP also needs $\Omega(n/\log n)$ rounds. The same holds for all eccentricities, the radius and the center.
- **Global but not about $D$.** The networks have diameter 3, so an $O(D)$ algorithm, or even an $O(D + \sqrt{n})$ algorithm as for [MST](/distributed-mst/) and [SSSP](/distributed-shortest-paths/), cannot exist. The diameter is harder than MST in CONGEST.
- **Approximation helps.** The $3/2$-approximation of Holzer, Peleg, Roditty and Wattenhofer (DISC 2014) takes $O(\sqrt{n \log n} + D)$ rounds, and a 2-approximation takes $O(D)$ rounds with one BFS. By the extension above, any ratio below $3/2$ again needs near-linear rounds.
- **Only the message size matters.** In the [LOCAL model](/local-model/), the diameter takes $O(D)$ rounds, so the bound is a fact about bandwidth.

## Tightness

The bound is tight up to the $\log n$ factor: the exact diameter takes $O(n)$ rounds by the pipelined BFS of [distributed APSP](/distributed-apsp/) (Holzer and Wattenhofer, PODC 2012; Peleg, Roditty and Tal, ICALP 2012). For approximations, the picture is:

| ratio | rounds | source |
|---|---|---|
| exact | $\Theta(n)$ up to log factors | FHW 2012; HW 2012; PRT 2012 |
| $3/2 - \epsilon$ | $\tilde{\Omega}(n)$ | Abboud, Censor-Hillel and Khoury, 2016 |
| $3/2$ | $O(\sqrt{n \log n} + D)$ | Holzer, Peleg, Roditty and Wattenhofer, 2014 |
| $2$ | $O(D)$ | one BFS |

Grossman, Khoury and Paz (DISC 2020) show that even to tell diameter 3 from diameter 5 needs $\Omega(n/\log n)$ rounds. This does not contradict the $3/2$-approximation, whose estimate for diameter 5 can be 4, and for diameter 3 can be 2 or 3.

The gadget above has $\Theta(n^2)$ links. On sparse networks, the cut must be small, and the bit gadget of Abboud, Censor-Hillel and Khoury replaces the clique sides with $O(\log n)$ cut links and inputs of $\Theta(n)$ bits. This gives $\Omega(n/\log^2 n)$ rounds for the exact diameter on networks with $O(n \log n)$ links.

## History

Before 2012, it was open whether the diameter could be found as fast as a BFS tree. Frischknecht, Holzer and Wattenhofer (SODA 2012) showed that it cannot, with a reduction from set disjointness in the style of the [Peleg-Rubinovich](/peleg-rubinovich-lower-bound/) and Das Sarma et al. bounds, but with a simpler graph: a cut of $\Theta(n)$ links and an input of $\Theta(n^2)$ bits. In the same year, Holzer and Wattenhofer and, independently, Peleg, Roditty and Tal gave $O(n)$ algorithms, so the exact complexity was settled. The approximation thresholds at $3/2$ came from the distributed form of the sequential algorithm of Roditty and Vassilevska Williams (STOC 2013) and from the bit gadget of Abboud, Censor-Hillel and Khoury (2016).

## References
