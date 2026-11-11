---
tag: B1T5JR
kind: problem
slug: distributed-weighted-matching
name: Distributed weighted matching approximation
aliases:
- distributed maximum weight matching approximation
area: distributed/distributed-graph-algorithms
level: research
summary: Find a matching of large total weight by local communication. Ratio 1/2 - eps takes O(log Delta / log log Delta) randomized rounds; 1 - eps takes poly(1/eps, log n) deterministic rounds.
prereqs: [local-model, maximum-weight-matching, distributed-maximal-matching, locally-dominant-matching]
see_also: [kmw-lower-bound, israeli-itai, fractional-matching, maximum-matching, distributed-minimum-vertex-cover, distributed-edge-coloring, distributed-mis, network-decomposition]
sources:
  - paper: doi:10.1007/978-3-540-30186-8_24
    title: Mirjam Wattenhofer and Roger Wattenhofer, Distributed weighted matching, DISC 2004, LNCS 3274
    locator: pp. 335 to 348 (a randomized algorithm with ratio 1/5 in O(log^2 n) rounds, and ratio 1/4 in a constant number of rounds on trees)
  - url: https://arxiv.org/abs/cs/0410047
    title: Jaap-Henk Hoepman, Simple distributed weighted matchings, 2004
    locator: the distributed locally heaviest edge algorithm with ratio 1/2, where each node sends a request along its heaviest remaining edge
  - paper: doi:10.1145/2786753
    title: Zvi Lotker, Boaz Patt-Shamir and Seth Pettie, Improved distributed approximate matching, Journal of the ACM 62(5), 2015
    locator: Article 38, pp. 1 to 17 (CONGEST; ratio 1 - eps for unweighted graphs in O(log n) rounds for constant eps, and ratio 1/2 - eps for weighted graphs in O(log(1/eps) log n) rounds, both randomized; also SPAA 2008, doi:10.1145/1378533.1378558, pp. 129 to 136)
  - url: https://arxiv.org/abs/1708.00276
    title: Reuven Bar-Yehuda, Keren Censor-Hillel, Mohsen Ghaffari and Gregory Schwartzman, Distributed approximation of maximum independent set and maximum matching, PODC 2017
    locator: pp. 165 to 174 (local ratio; ratio 1/2 for weighted matching in CONGEST, and ratio 1/(2 + eps) in O(log Delta / log log Delta) rounds, randomized)
  - paper: doi:10.1007/s00446-018-0344-4
    title: Manuela Fischer, Improved deterministic distributed matching via rounding, Distributed Computing 33(3-4), 2020
    locator: deterministic ratio 1/(2 + eps) for weighted matching in O(log^2 Delta log(1/eps) + log* n) rounds, by rounding fractional matchings
  - url: https://arxiv.org/abs/2111.10577
    title: Salwa Faour, Marc Fuchs and Fabian Kuhn, Distributed CONGEST approximation of weighted vertex covers and matchings, OPODIS 2021, LIPIcs 217
    locator: 17:1 to 17:20 (deterministic ratio 1 - eps in 2^O(1/eps) polylog(Delta W) log* n CONGEST rounds)
  - paper: doi:10.1145/3583668.3594570
    title: Shang-En Huang and Hsin-Hao Su, (1 - eps)-approximate maximum weighted matching in poly(1/eps, log n) time in the distributed and parallel settings, PODC 2023
    locator: pp. 44 to 54 (deterministic ratio 1 - eps in poly(1/eps, log n) CONGEST rounds)
---

In the distributed weighted matching problem, the nodes of a weighted network must agree on a matching, a set of edges with no common end, whose total weight is close to the maximum. The exact maximum needs information from far away, so distributed algorithms approximate it. The simple rule that takes edges which are heaviest at both ends gives ratio $\tfrac12$ but can need $n/2$ rounds; ratio $\tfrac12 - \varepsilon$ is possible in $O(\log \Delta / \log \log \Delta)$ rounds, which matches the [KMW lower bound](/kmw-lower-bound/), and ratio $1 - \varepsilon$ in $\mathrm{poly}(1/\varepsilon, \log n)$ rounds.

Notation on this page: $G = (V, E, w)$ has $n$ nodes, $m$ edges, maximum degree $\Delta$ and positive edge weights $w(e)$. $W$ is the ratio of the largest to the smallest weight. $M^*$ is a [maximum weight matching](/maximum-weight-matching/) and $\mathrm{OPT} = w(M^*)$. An algorithm has ratio $\alpha \le 1$ if $w(M) \ge \alpha \cdot \mathrm{OPT}$; many papers write $1/\alpha$ instead, for example a "$(2 + \varepsilon)$-approximation". The model is [LOCAL](/local-model/) or [CONGEST](/congest-model/) as stated.

## In plain words

People in a town want to form pairs to work together, and each possible pair has a value. A person can only talk with the people they know. The town wants pairs with a large total value.

The best plan can depend on people very far away, so nobody can find it quickly. A simple rule is that two people pair up when each is the other's best remaining choice. This gives at least half of the best total, but in a long chain of people with rising values it can take a very long time.

A faster way is to sort the possible pairs into a few groups of about equal value and handle the groups from the most valuable down. Inside a group, any quick method for making pairs is good enough. Better methods also look for short chains of swaps that increase the total.

## Definition

**Input.** A graph $G$ with positive edge weights, in the LOCAL or CONGEST model, with unique identifiers. Each node knows the weights of its edges.

**Output.** Each node outputs its partner, or none; the partners must agree, so the output is a matching $M$.

**Goal.** Make $w(M)$ large: ratio $\alpha$ means $w(M) \ge \alpha \cdot \mathrm{OPT}$, always or in expectation.

**Distributed view.** The cost is the number of rounds, and in CONGEST each message has $O(\log n)$ bits, so a weight must fit in a message. The [locally dominant matching](/locally-dominant-matching/) page treats the same ½ rule as a parallel algorithm and counts work and span; here the question is how far information must travel. A chain of edges with increasing weights costs the parallel algorithm span but not much work, and it costs the distributed algorithm rounds.

**Exact solutions need many rounds.** Take a path with an even number of edges and all weights 1, except one end edge of weight $1 + \delta$. The two best matchings take every other edge, and the optimum is the one that contains the heavy edge. A node in the middle must know which end is heavy, so an exact algorithm needs $\Omega(n)$ rounds.

## Variants

- **Unweighted, maximum cardinality.** All weights are 1. A [maximal matching](/distributed-maximal-matching/) has ratio $\tfrac12$, and ratio $1 - \varepsilon$ needs short augmenting paths.
- **Fractional matching.** Each edge gets $x_e \ge 0$ with $\sum_{e \ni v} x_e \le 1$ at each node. This is a packing LP, and it is the first step of the rounding algorithms. See [fractional matching](/fractional-matching/).
- **Bipartite graphs.** Augmenting paths are simpler, and several algorithms start with this case.
- **$b$-matching.** Node $v$ may have up to $b(v)$ partners.
- **Vertex weights.** The weight of an edge is the sum of the weights of its ends.

## Examples

- **Rising weights on a path.** On the path $0, 1, \dots, n - 1$ with $w(\{i, i + 1\}) = i + 1$, only the last remaining edge is heaviest at both ends, so the locally heaviest rule adds one edge per round. In the tests of the code below, with $n = 256$, it takes 128 rounds, while the weight-class algorithm with $\varepsilon = 1$ takes 33 to 42 rounds.
- **Ratio $\tfrac12$ is tight for maximal matchings.** On the path with weights $1, 1 + \delta, 1$, the locally heaviest rule takes the middle edge, while the two outer edges weigh 2.
- **Random small graphs.** On 40 random graphs with 8 nodes and weights between 1 and 100, both algorithms of the code got on average about 98% of the optimum found by exhaustive search, and at worst 79%. The ratio bounds are worst-case bounds.

## Known algorithms

**Locally heaviest edges (ratio ½).** An edge joins when it is the heaviest remaining edge at both of its ends; ties are broken by identifiers. The result is the greedy matching in order of decreasing weight, with ratio $\tfrac12$; the proof is on the [locally dominant matching](/locally-dominant-matching/) page. Hoepman (2004) gave it as a distributed algorithm in which each node sends a request along its heaviest remaining edge. Each round needs only $O(1)$ messages per edge, but the number of rounds is the length of the longest chain of edges with increasing weights, up to $n/2$.

**Weight classes (ratio $\tfrac{1}{2(1 + \varepsilon)}$).** Put edge $e$ in class $\lfloor \log_{1 + \varepsilon} w(e) \rfloor$. For each class from the heaviest down, compute a maximal matching of the class edges whose ends are both still free, for example with [Israeli-Itai](/israeli-itai/) or Luby's algorithm on the line graph.

*Claim.* The result is a maximal matching $M$ with $w(M) \ge \mathrm{OPT} / (2(1 + \varepsilon))$.

*Proof.* Take $f \in M^*$. If $f \in M$, charge $w(f)$ to $f$ at either end. If not, consider the moment when the class of $f$ was handled. After it, $f$ had a matched end, since otherwise the maximal matching of that class would have added $f$. That end was matched by an edge $e \in M$ of the same class or a heavier class, so $w(f) \le (1 + \varepsilon) w(e)$; charge $w(f)$ to $e$ at the shared end. The edges of $M^*$ have no common end, so each edge of $M$ receives at most one charge at each of its two ends. So $w(M^*) \le 2(1 + \varepsilon) w(M)$. Maximality holds because every edge was free or covered when its class was handled. $\blacksquare$

The number of rounds is $O(\log_{1 + \varepsilon} W)$ times the rounds of a maximal matching, so $O(\varepsilon^{-1} \log W \log n)$ with randomness. The algorithms below avoid the factor $\log W$.

**Earlier randomized results.** Wattenhofer and Wattenhofer (2004) gave ratio $\tfrac15$ in $O(\log^2 n)$ rounds, and ratio $\tfrac14$ in a constant number of rounds on trees. Lotker, Patt-Shamir and Pettie (SPAA 2008, JACM 2015) gave ratio $\tfrac12 - \varepsilon$ in $O(\log(1/\varepsilon) \log n)$ rounds in CONGEST, and ratio $1 - \varepsilon$ for unweighted graphs in $O(\log n)$ rounds for constant $\varepsilon$.

**Local ratio (ratio ½ and ½ - ε).** Bar-Yehuda, Censor-Hillel, Ghaffari and Schwartzman (2017) use the local ratio method for weighted independent set on the line graph, with an MIS algorithm as a subroutine. This gives ratio $\tfrac12$ in CONGEST in $O(\mathrm{MIS} \cdot \log W)$ rounds, where $\mathrm{MIS}$ is the round complexity of MIS, and with a parameter-tuned version of Ghaffari's MIS algorithm, ratio $\tfrac{1}{2 + \varepsilon}$ in $O(\log \Delta / \log \log \Delta)$ rounds, randomized.

**Deterministic rounding.** Fischer (2020) computes a near-optimal fractional matching and rounds it step by step, which gives ratio $\tfrac{1}{2 + \varepsilon}$ deterministically in $O(\log^2 \Delta \log(1/\varepsilon) + \log^* n)$ rounds.

**Ratio $1 - \varepsilon$.** A matching with no short augmentation that increases the weight is close to optimal, so these algorithms repeatedly find many disjoint short augmentations in parallel. Faour, Fuchs and Kuhn (2021) did this deterministically in CONGEST in $2^{O(1/\varepsilon)} \cdot \mathrm{poly}(\log(\Delta W)) \cdot \log^* n$ rounds, and Huang and Su (2023) removed the exponential dependence on $1/\varepsilon$: their deterministic CONGEST algorithm takes $\mathrm{poly}(1/\varepsilon, \log n)$ rounds, and it also gives a PRAM algorithm with $\mathrm{poly}(1/\varepsilon, \log n)$ span.

| Algorithm | Ratio | Rounds | Randomized |
|---|---|---|---|
| Locally heaviest edges (Hoepman 2004) | $\tfrac12$ | up to $n/2$ | no |
| Weight classes plus maximal matching | $\tfrac{1}{2(1 + \varepsilon)}$ | $O(\varepsilon^{-1} \log W \log n)$ | yes |
| Wattenhofer and Wattenhofer (2004) | $\tfrac15$ | $O(\log^2 n)$ | yes |
| Lotker, Patt-Shamir and Pettie (2008, 2015) | $\tfrac12 - \varepsilon$ | $O(\log(1/\varepsilon) \log n)$ | yes |
| Bar-Yehuda et al. (2017) | $\tfrac{1}{2 + \varepsilon}$ | $O(\log \Delta / \log \log \Delta)$ | yes |
| Fischer (2020) | $\tfrac{1}{2 + \varepsilon}$ | $O(\log^2 \Delta \log(1/\varepsilon) + \log^* n)$ | no |
| Faour, Fuchs and Kuhn (2021) | $1 - \varepsilon$ | $2^{O(1/\varepsilon)} \mathrm{poly}(\log(\Delta W)) \log^* n$ | no |
| Huang and Su (2023) | $1 - \varepsilon$ | $\mathrm{poly}(1/\varepsilon, \log n)$ | no |

## Bounds

- **KMW lower bound.** Any constant or polylogarithmic ratio for maximum matching, even for fractional matching in unweighted graphs, needs $\Omega(\log \Delta / \log \log \Delta)$ and $\Omega(\sqrt{\log n / \log \log n})$ rounds, for randomized algorithms too. So the algorithm of Bar-Yehuda et al. is optimal in terms of $\Delta$ for constant $\varepsilon$.
- **Exact optimum.** $\Omega(n)$ rounds on a path, as in the definition.
- **Rounds of the ½ rule.** The locally heaviest rule takes as many rounds as the longest chain of increasing weights, which is $\Theta(n)$ on the rising path. Weight classes or random keys are needed for a bound in terms of $\log n$.

## Reductions

- **Weighted to unweighted.** The weight-class proof above turns any maximal matching algorithm into a weighted algorithm with ratio $\tfrac{1}{2(1 + \varepsilon)}$, at the cost of a factor $O(\log_{1 + \varepsilon} W)$ in rounds. Lotker, Patt-Shamir and Pettie use a finer reduction that keeps a ratio of $\tfrac12 - \varepsilon$ without the factor $\log W$.
- **To independent set on the line graph.** A matching is an independent set of $L(G)$, so weighted matching is maximum weight independent set on the line graph. The line graph has no induced claw, which is why local ratio gives $\tfrac12$ there.
- **Duality with vertex cover.** The LP dual of fractional matching is fractional vertex cover, and the algorithms that round fractional matchings also give approximate covers; see [distributed minimum vertex cover](/distributed-minimum-vertex-cover/).
- **From edge colouring.** A $(2\Delta - 1)$-[edge colouring](/distributed-edge-coloring/) gives a maximal matching in $2\Delta - 1$ more rounds, and so a weight-class step.

## Applications

- **Pairing in networks.** Assigning partners for data exchange, load balancing between pairs of machines, and link scheduling, where the weight is the value of the pair.
- **Coarsening.** Multilevel graph partitioning merges matched pairs; in a distributed graph system the matching must be computed by local rounds.
- **A step in other algorithms.** Approximate matchings are used in algorithms for $b$-matching, for vertex cover, and in augmenting path methods for maximum cardinality matching.

## References
