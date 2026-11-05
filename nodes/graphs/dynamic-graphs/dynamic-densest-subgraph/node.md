---
tag: CYJ390
kind: problem
slug: dynamic-densest-subgraph
name: Dynamic densest subgraph
aliases:
- dynamic densest subgraph problem
area: graphs/dynamic-graphs
level: research
summary: Maintain an approximately densest subgraph under edge updates.
prereqs: [dynamic-graph, k-core-decomposition, degeneracy, arboricity]
see_also: [dynamic-k-core-decomposition, k-core, max-flow-problem, amortized-update-time, dynamic-matching, dynamic-graph-coloring]
sources:
  - paper: doi:10.1007/3-540-44436-x_10
    title: Moses Charikar, Greedy approximation algorithms for finding dense components in a graph, Proceedings of APPROX 2000, Lecture Notes in Computer Science 1913, 84 to 95
    locator: the greedy peeling algorithm and its factor 2 bound, and the linear program for the densest subgraph
  - paper: doi:10.1145/2746539.2746592
    title: Sayan Bhattacharya, Monika Henzinger, Danupon Nanongkai and Charalampos E. Tsourakakis, Space- and time-efficient algorithm for maintaining dense subgraphs on one-pass dynamic streams, Proceedings of STOC 2015, 173 to 182
    locator: the main theorem ((4 + eps)-approximation, polylogarithmic amortized time per update, with high probability)
  - paper: doi:10.1145/3357713.3384327
    title: Saurabh Sawlani and Junxing Wang, Near-optimal fully dynamic densest subgraph, Proceedings of STOC 2020, 181 to 193
    locator: the main theorem ((1 + eps)-approximation in poly(log n, 1/eps) worst-case time per update) and the orientation view of the dual
  - paper: doi:10.1145/2736277.2741638
    title: Alessandro Epasto, Silvio Lattanzi and Mauro Sozio, Efficient densest subgraph computation in evolving graphs, Proceedings of WWW 2015, 300 to 310
    locator: the main theorem ((2 + eps)-approximation with adversarial insertions and random deletions)
  - paper: doi:10.1007/978-3-662-43951-7_45
    title: Tsvi Kopelowitz, Robert Krauthgamer, Ely Porat and Shay Solomon, Orienting fully dynamic graphs with worst-case time bounds, Proceedings of ICALP 2014, Lecture Notes in Computer Science 8573, 532 to 543
    locator: the main theorem (low out-degree orientations of graphs with bounded arboricity, worst-case update time)
---

The dynamic densest subgraph problem asks to keep a vertex set $S$ of nearly maximum density $|E(S)|/|S|$ in an undirected [dynamic graph](/dynamic-graph/) under edge insertions and deletions. The static problem is solvable exactly in polynomial time with [maximum flow](/max-flow-problem/), and a simple peeling order gives a factor 2. Exact dynamic maintenance is costly, so the dynamic results keep an approximation. The best known fully dynamic algorithm keeps a $(1 + \varepsilon)$-approximation in polylogarithmic worst-case time per update.

## In plain words

In a social network, look for a group of people with many friendships among themselves, compared with the size of the group. A good score is the number of friendships inside the group divided by the number of people in it. Friendships start and end all the time, and you want a group with a near-best score after each change.

Finding the very best group again after each change is slow. But a group whose score is almost the best is enough for most uses, and such a group can be kept with a small amount of work per change. A useful view is to give each friendship to one of its two people, so that nobody gets too many. The most loaded people then point to a dense group.

## Definition

**Input.** An undirected graph $G = (V, E)$ on $n$ vertices and an online sequence of $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ edge updates, with queries.

**Density.** For a nonempty $S \subseteq V$, let $E(S)$ be the set of edges with both ends in $S$, and let $\rho(S) = |E(S)|/|S|$. The **maximum density** is $\rho^* = \max_{S \ne \emptyset} \rho(S)$. Some papers use the average degree $2|E(S)|/|S|$; it differs by a factor 2.

**Queries.** $\mathrm{value}()$ returns an estimate $\tilde\rho$ with $\rho^*/\alpha \le \tilde\rho \le \rho^*$. A stronger query $\mathrm{set}()$ returns a set $S$ with $\rho(S) \ge \rho^*/\alpha$. The number $\alpha \ge 1$ is the approximation factor.

**Cost.** Update time per edge update, worst case or [amortized](/amortized-update-time/), and the time to report the set, usually $O(|S|)$. Updates are insertions only, deletions only, or both (fully dynamic).

**Orientation dual.** An orientation gives each edge a direction. The smallest possible maximum out-degree over all orientations of $G$ is $\lceil \rho^* \rceil$, and in the fractional form, where each edge splits one unit of load between its ends, the smallest maximum load is exactly $\rho^*$. This is the linear programming dual of the densest subgraph problem, and the dynamic algorithms work on it.

## Variants

- **Insertions only, deletions only, fully dynamic.** Each has its own results, listed below.
- **Random deletions.** Insertions are chosen by an adversary, but each deletion removes an edge chosen uniformly at random; this is the model of Epasto, Lattanzi and Sozio (2015).
- **Value only or set.** Some algorithms only keep the value $\tilde\rho$; reporting a set needs more care.
- **Weighted.** Edge or vertex weights, with $\rho(S)$ the weight inside $S$ over the weight of $S$.
- **Directed.** Density $|E(S, T)|/\sqrt{|S|\,|T|}$ over pairs of sets; Sawlani and Wang reduce it to the vertex-weighted problem.
- **Streams.** Keep the answer in small space while edges arrive and leave in one pass; the paper of Bhattacharya, Henzinger, Nanongkai and Tsourakakis handles this setting too.
- **Densest at least $k$ vertices.** This variant, and the variant with exactly $k$ vertices, is NP-hard already in the static case.

## Examples

Start with the complete graph on $\{0, 1, 2, 3\}$ and the path $3, 4, 5, 6$, so $n = 7$ and $m = 9$. The table gives $\rho^*$, a densest set, and the value of Charikar's greedy peeling after each update. Peeling removes a vertex of smallest degree, again and again, and returns the densest of the sets it passes through.

| update | edges | $\rho^*$ | a densest set | peeling value |
|---|---|---|---|---|
| start | 9 | 3/2 | $\{0, 1, 2, 3\}$ | 3/2 |
| insert 46 | 10 | 3/2 | $\{0, 1, 2, 3\}$ | 3/2 |
| insert 35 | 11 | 11/7 | all of $V$ | 11/7 |
| insert 36 | 12 | 12/7 | all of $V$ | 12/7 |
| delete 01 | 11 | 11/7 | all of $V$ | 11/7 |
| delete 12 | 10 | 3/2 | $\{3, 4, 5, 6\}$ | 3/2 |

The densest set jumps from the clique to the whole vertex set after one insertion, so the answer is not stable: a single update can change the densest set completely. After the last update two different sets have density 3/2: the set $\{3, 4, 5, 6\}$ with 6 edges, and the set $\{0, 2, 3, 4, 5, 6\}$ with 9 edges, which peeling finds. At the row with 12 edges, $\rho^* = 12/7$, so every orientation has a vertex of out-degree at least $\lceil 12/7 \rceil = 2$, and an orientation with maximum out-degree 2 exists.

## Known algorithms

**Static.** Goldberg's reduction to a sequence of minimum cuts finds $\rho^*$ exactly with [maximum flow](/max-flow-problem/). Charikar's peeling, the same order as in the [k-core decomposition](/k-core-decomposition/), gives a factor 2 in $O(n + m)$ time. In a densest set $S^*$, each vertex has degree at least $\rho^*$ inside $S^*$, since removing a vertex of smaller degree would raise the density. Look at the step when peeling first removes a vertex of $S^*$: all of $S^*$ is still present, so every vertex left has degree at least $\rho^*$, and the current set has density at least $\rho^*/2$. The maximum core number lies between $\rho^*$ and $2\rho^*$.

**Dynamic.**

| setting | algorithm | factor | update time | case |
|---|---|---|---|---|
| any | recompute with peeling | 2 | $O(n + m)$ | worst, deterministic |
| any | recompute with flow | 1 | a max-flow computation | worst, deterministic |
| insertions, random deletions | Epasto, Lattanzi and Sozio (2015) | $2 + \varepsilon$ | polylogarithmic | amortized, expected |
| fully dynamic | Bhattacharya, Henzinger, Nanongkai and Tsourakakis (2015) | $4 + \varepsilon$ | polylogarithmic | amortized, with high probability, randomized |
| fully dynamic | Sawlani and Wang (2020) | $1 + \varepsilon$ | $\mathrm{poly}(\log n, 1/\varepsilon)$ | worst |

**Orientation method.** Sawlani and Wang keep an orientation in which each edge gives its load to an end whose load is not much larger than the load of the other end. If this local condition holds, the maximum load is within a factor $1 + \varepsilon$ of $\rho^*$, and the vertices whose load is close to the maximum contain a near-densest set. An update changes one load and may break the condition at one vertex. The fix reverses edges along a short path of decreasing loads, like an augmenting path. Earlier dynamic orientation algorithms, such as that of Kopelowitz, Krauthgamer, Porat and Solomon (2014), keep out-degrees small for graphs of bounded [arboricity](/arboricity/) with a similar path-flipping rule.

## Bounds

**Upper bounds.** A $(1 + \varepsilon)$-approximation in $\mathrm{poly}(\log n, 1/\varepsilon)$ worst-case time per update, fully dynamic.

**Lower bounds.** A structure that reports a set must spend time proportional to its size, and the example shows that one update can change the densest set from 4 to 7 vertices. Apart from this, we do not state a lower bound: all fast dynamic results are approximate, and we do not know of a published conditional lower bound for exact maintenance.

## Reductions

- **To orientations.** By LP duality, $\rho^*$ is the smallest maximum load of a fractional orientation, so a dynamic low out-degree orientation gives an estimate of $\rho^*$.
- **To core numbers.** The maximum core number $k_{\max}$ satisfies $\rho^* \le k_{\max} \le 2\rho^*$, so an approximate [dynamic k-core decomposition](/dynamic-k-core-decomposition/) gives a factor about 2.
- **Arboricity and degeneracy.** By the Nash-Williams formula, the [arboricity](/arboricity/) is the maximum of $\lceil |E(S)|/(|S| - 1) \rceil$ over sets with $|S| \ge 2$, so it lies between $\rho^*$ and $\lceil 2\rho^* \rceil$. The [degeneracy](/degeneracy/) is the maximum core number. So the three quantities agree up to a factor 2.

## Applications

- **Community and fraud detection.** Dense groups in social or transaction graphs that change over time.
- **Link spam.** Groups of web pages that link to each other much more than usual.
- **Subroutine.** Low out-degree orientations, which are the dual, speed up dynamic [matching](/dynamic-matching/), [coloring](/dynamic-graph-coloring/) and adjacency queries on sparse graphs.

## References
