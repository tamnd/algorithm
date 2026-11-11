---
tag: T5PX1A
kind: problem
slug: sinkless-orientation
name: Sinkless orientation
aliases:
- sinkless orientation problem
area: distributed/distributed-graph-algorithms
level: research
summary: Orient every edge so that no node of degree 3 or more has only incoming edges. It takes Theta(log n) rounds deterministically and Theta(log log n) with randomness.
prereqs: [local-model, locally-checkable-labeling]
see_also: [locally-checkable-labeling, round-elimination, lovasz-local-lemma, distributed-edge-coloring, distributed-maximal-matching, kmw-lower-bound, ring-coloring, linial-coloring-lower-bound]
sources:
  - paper: doi:10.1145/2897518.2897570
    title: Sebastian Brandt, Orr Fischer, Juho Hirvonen, Barbara Keller, Tuomo Lempiäinen, Joel Rybicki, Jukka Suomela and Jara Uitto, A lower bound for the distributed Lovász local lemma, STOC 2016
    locator: pp. 479 to 488 (randomized Omega(log log n) for the LLL, proved through sinkless orientation and sinkless colouring by round elimination)
  - paper: doi:10.1137/17M1117537
    title: Yi-Jun Chang, Tsvi Kopelowitz and Seth Pettie, An exponential separation between randomized and deterministic complexity in the LOCAL model, SIAM Journal on Computing 48(1), 2019
    locator: pp. 122 to 143 (fast deterministic algorithms speed up to O(log* n), so randomized lower bounds give deterministic Omega(log_Delta n); also FOCS 2016, doi:10.1109/FOCS.2016.72, pp. 615 to 624)
  - paper: doi:10.1137/1.9781611974782.166
    title: Mohsen Ghaffari and Hsin-Hao Su, Distributed degree splitting, edge coloring, and orientations, SODA 2017
    locator: pp. 2505 to 2523 (sinkless orientation in O(log_Delta n) deterministic and O(log_Delta log n) randomized rounds on Delta-regular graphs, which matches the lower bounds)
  - paper: doi:10.1145/3293611.3331611
    title: Sebastian Brandt, An automatic speedup theorem for distributed problems, PODC 2019
    locator: pp. 379 to 388 (round elimination as a general and mechanical operation on problems)
  - paper: doi:10.1137/1.9781611977585.ch17
    title: Alkida Balliu, Janne H. Korhonen, Fabian Kuhn, Henrik Lievonen, Dennis Olivetti, Shreyas Pai, Ami Paz, Joel Rybicki, Stefan Schmid, Jan Studený, Jukka Suomela and Jara Uitto, Sinkless orientation made simple, SOSA 2023
    locator: pp. 175 to 191 (self-contained proofs of the deterministic Omega(log n) LOCAL bound and the O(log log n) SLOCAL bound)
---

In sinkless orientation, every edge of a graph must get a direction so that each node of degree at least 3 has at least one outgoing edge. A solution always exists and is easy to find centrally, but in the [LOCAL](/local-model/) model it needs $\Theta(\log n)$ rounds deterministically and $\Theta(\log \log n)$ rounds with randomness. Brandt et al. (2016) proved the randomized lower bound by round elimination, and it was the first problem for which this method gave a tight bound; it is now the standard example of an exponential gap between randomized and deterministic complexity.

Notation on this page: $G = (V, E)$ has $n$ nodes and maximum degree $\Delta$. A node is **constrained** if its degree is at least 3, and **free** otherwise. An orientation is **sinkless** if every constrained node has out-degree at least 1. On $\Delta$-regular graphs, the bounds are written with $\log_\Delta$.

## In plain words

Every road between two towns must become one-way. The rule is that every town with three or more roads must have at least one road leaving it, so that no such town is a dead end for traffic.

A planner with the whole map can always do this. The hard question is how fast towns can agree when each one only talks with its neighbours. A town cannot just pick its own outgoing road, because the neighbour at the other end may pick the same road for itself.

Loops of roads help: a loop can be driven in one direction, and nearby towns can point their roads toward it. When every town has three roads, a loop is never far away, but finding one may need a look as far as the logarithm of the number of towns. With random choices, almost every town is fine at once.

## Definition

**Input.** A graph $G = (V, E)$ in the LOCAL model, with unique identifiers or with random bits.

**Output.** Each edge $\{u, v\}$ is oriented as $u \to v$ or $v \to u$; both ends must agree.

**Condition.** Every node of degree at least 3 has an outgoing edge.

For bounded $\Delta$ the condition can be checked by looking at each node and its edges, so sinkless orientation is a [locally checkable labeling](/locally-checkable-labeling/) problem.

*Claim.* Every finite graph has a sinkless orientation.

*Proof.* Start from any orientation and remove the sinks one at a time. Let $v$ be a constrained sink, and let $S$ be the set of nodes with a directed path to $v$, including $v$. If $S$ contains a free node or a node of out-degree at least 2, call it $w$; reverse a directed path from $w$ to $v$. Then $v$ gains an outgoing edge, $w$ loses one but stays free or keeps one, the inner nodes of the path keep their out-degree, and the number of constrained sinks falls by 1. Otherwise every node of $S$ is constrained, $v$ has out-degree 0 and every other node of $S$ has out-degree exactly 1. An edge with one end in $S$ and its tail outside $S$ cannot exist, by the definition of $S$, and the single outgoing edge of a node of $S$ leads into $S$, since it is the first edge of a path to $v$. So the edges that touch $S$ all lie inside $S$, and there are at most $|S| - 1$ of them. But every node of $S$ has degree at least 3, so there are at least $3|S| / 2$ such edges, a contradiction. $\blacksquare$

The code on this page uses this argument as a centralized reference, and tests that the result is sinkless.

## Variants

- **Minimum degree versus all degrees.** Some papers require an outgoing edge at every node and then assume minimum degree at least 3, or study $\Delta$-regular graphs. Nodes of degree 1 cannot satisfy the condition, and on a cycle, where degree is 2, the problem becomes a consistent direction, which needs $\Omega(n)$ rounds.
- **Sinkless colouring.** With a proper $\Delta$-edge colouring as input, colour every node with one of the $\Delta$ edge colours so that no edge of colour $i$ has both ends coloured $i$. This is equivalent to sinkless orientation in 0 rounds, as shown under Reductions, and it is the form used in the lower bound.
- **Sinkless and sourceless orientation.** Every node needs both an outgoing and an incoming edge. Brandt et al. treat it with the same method.
- **Larger out-degree.** Requiring out-degree at least $k$, or an orientation in which each node's in-degree and out-degree are nearly equal, leads to degree splitting, which Ghaffari and Su use for [edge colouring](/distributed-edge-coloring/).
- **Other models.** In the SLOCAL model, where nodes are processed one at a time and each looks at a small radius, the problem takes only $O(\log \log n)$ locality deterministically; the gap to $\Omega(\log n)$ in deterministic LOCAL separates the two models.

## Examples

- **$K_4$.** Every node has degree 3. Orient the triangle $0 \to 1 \to 2 \to 0$ and the edges at node 3 as $3 \to 0$, $3 \to 1$, $3 \to 2$. Each node has an outgoing edge. Orienting all three edges at node 0 inward makes 0 a sink; the repair reverses one directed path that ends at 0.
- **A tree.** In a tree whose inner nodes have degree 3 and whose leaves have degree 1, orienting every edge away from a root is sinkless, since only the free leaves have no outgoing edge. Orienting every edge toward the root is sinkless too, because the root of a binary tree has degree 2 and is free.
- **A random start.** If each edge of a 3-regular graph is oriented by a fair coin, each node is a sink with probability $2^{-3} = \frac{1}{8}$. The tests on this page measure this rate on random 3-regular graphs.
- **Not local by a fixed rule.** On a $\Delta$-regular graph whose nodes look the same up to a large radius, a rule such as "point the edge to the larger identifier" makes the node of largest identifier in its neighbourhood a sink; any rule must break symmetry over a long distance.

## Known algorithms

- **Deterministic, $O(\log n)$ rounds.** In a graph where every node has degree at least 3, a ball of radius $\lceil \log_2 n \rceil + 1$ around any node contains a cycle, since a tree in which every node has at least 2 children below it has more than $n$ nodes at that depth. A cycle can be oriented in one direction, and nearby nodes can orient a path toward it. Ghaffari and Su (2017) turn this into an $O(\log n)$ algorithm that handles the overlaps between the choices of different nodes, and $O(\log_\Delta n)$ on $\Delta$-regular graphs.
- **Randomized, $O(\log \log n)$ rounds.** In outline: orient at random, or by a slightly better local rule, so that each node fails only with a small probability and the failures are almost independent; fix most failures locally; the nodes left over form components of $\mathrm{poly}(\log n)$ nodes, and the deterministic algorithm finishes them in $O(\log \mathrm{poly}(\log n)) = O(\log \log n)$ rounds. This shattering pattern is from Ghaffari and Su; on $\Delta$-regular graphs it takes $O(\log_\Delta \log n)$ rounds.
- **Centralized.** The path reversal in the proof above, or an Euler tour argument, finds a sinkless orientation in linear time.
- **SLOCAL.** Ghaffari, Harris and Kuhn's derandomization turns the randomized algorithm into a deterministic SLOCAL algorithm with locality $O(\log \log n)$; the SOSA 2023 paper gives a direct proof.

## Bounds

- **Randomized lower bound.** Brandt et al. (2016): any randomized algorithm that succeeds w.h.p. needs $\Omega(\log \log n)$ rounds, already on 3-regular graphs, and $\Omega(\log_\Delta \log n)$ on $\Delta$-regular graphs.
- **Deterministic lower bound.** $\Omega(\log n)$, and $\Omega(\log_\Delta n)$ on $\Delta$-regular graphs. Chang, Kopelowitz and Pettie (2016) show that a deterministic algorithm for such a problem with $o(\log_\Delta n)$ rounds can be sped up to $O(\log^* n)$ rounds; that would contradict the randomized bound, since a deterministic algorithm is also a randomized one.
- **Tightness.** The upper bounds of Ghaffari and Su match both bounds, so the problem is $\Theta(\log n)$ deterministically and $\Theta(\log \log n)$ with randomness, an exponential gap.

**Round elimination, in outline.** Fix a $\Delta$-regular graph with a proper $\Delta$-edge colouring and girth more than $2t + 1$, so every view of radius $t$ is a tree. Suppose an algorithm solves sinkless orientation in $t$ rounds, failing at each node with probability at most $p$. Each node can then simulate it with one less round of information for one of the two problems: from a sinkless orientation algorithm one builds a sinkless colouring algorithm that looks half a round less far, and from that a sinkless orientation algorithm that looks another half round less far. A node picks an edge colour $i$ if, given what it sees, the algorithm orients its edge of colour $i$ outward with high enough probability over the unseen part. The new failure probability is bounded by a function of $p$ and $\Delta$ that is roughly a fixed root of $p$, so the failure grows from $1/n$ toward a constant as rounds are removed. A 0-round algorithm cannot succeed: all nodes see the same thing, so they choose colour $i$ with the same probability $q_i$, and for some $i$, $q_i \ge 1/\Delta$, so an edge of colour $i$ fails with probability at least $1/\Delta^2$. So about $\log_\Delta \log n$ steps are needed before the failure becomes constant, which gives the bound. The key point is that the problem is a fixed point: after one full step it is the same problem again. Brandt (2019) made the step mechanical for any problem in this setting; this description is a sketch, and the papers give the exact functions.

## Reductions

- **Sinkless colouring to orientation, in 0 rounds.** Given a sinkless colouring, a node coloured $i$ orients its edge of colour $i$ outward, and every other edge is oriented by the rule of its other end or by identifiers. Two nodes never claim the same edge, since that edge would have colour $i$ at both ends, which is forbidden. So every node has an outgoing edge.
- **Orientation to sinkless colouring, in 0 rounds.** A node takes the colour of one of its outgoing edges. An edge of colour $i$ with both ends coloured $i$ would be outgoing at both ends, which is impossible.
- **To the Lovász local lemma.** Orient each edge at random. The bad event "$v$ is a sink" has probability $2^{-d}$ on a $d$-regular graph and depends on at most $d$ other bad events. For $d \ge 4$, $e \cdot 2^{-d} \cdot (d + 1) < 1$, so the [symmetric local lemma](/lovasz-local-lemma/) applies, and any distributed LLL algorithm solves sinkless orientation. This is how the lower bound for sinkless orientation becomes a lower bound for the distributed LLL.
- **From degree splitting.** An orientation in which every node has out-degree at least $\lfloor \deg / 2 \rfloor - O(1)$ is sinkless when degrees are large enough, so degree splitting algorithms solve it.

## Applications

- **Lower bounds.** The $\Omega(\log \log n)$ bound for the distributed Lovász local lemma comes from sinkless orientation. The same round elimination method later gave the lower bounds for [maximal matching](/distributed-maximal-matching/), MIS and ruling sets.
- **Gaps between randomized and deterministic complexity.** Sinkless orientation and $\Delta$-colouring of trees are the standard examples where randomness helps exponentially in LOCAL.
- **Edge colouring and degree splitting.** Ghaffari and Su use orientations with balanced degrees to split graphs and then colour the edges of the parts recursively.
- **A test case for theory.** Sinkless orientation has helped to sort out the complexity classes of [LCL problems](/locally-checkable-labeling/) and the relation between LOCAL and SLOCAL.

## References
