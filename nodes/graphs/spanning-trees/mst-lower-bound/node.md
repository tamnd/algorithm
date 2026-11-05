---
tag: 3S9CGS
kind: theorem
slug: mst-lower-bound
name: Minimum spanning tree lower bound
aliases:
- Omega(m) lower bound for MST
area: graphs/spanning-trees
level: advanced
summary: Any MST algorithm must read every edge, giving an Omega(m) lower bound.
prereqs: [minimum-spanning-tree, adversary-argument, decision-tree-model, cut-property, bridge]
see_also: [mst-verification, pettie-ramachandran-mst, karger-klein-tarjan-mst, chazelle-mst, max-finding-lower-bound, trivial-lower-bound, euclidean-minimum-spanning-tree, comparison-model]
sources:
  - paper: doi:10.1145/505241.505243
    title: Seth Pettie and Vijaya Ramachandran, An optimal minimum spanning tree algorithm, Journal of the ACM 49(1) (2002), 16-34
    locator: the introduction (the decision-tree complexity of the MST problem, between the trivial Ω(m) and O(m α(m, n)))
  - paper: doi:10.1145/201019.201022
    title: David R. Karger, Philip N. Klein and Robert E. Tarjan, A randomized linear-time algorithm to find minimum spanning trees, Journal of the ACM 42(2) (1995), 321-328
    locator: the main theorem, expected O(m) time, which meets the lower bound
  - paper: doi:10.1145/355541.355562
    title: Bernard Chazelle, A minimum spanning tree algorithm with inverse-Ackermann type complexity, Journal of the ACM 47(6) (2000), 1028-1047
    locator: the main theorem, the best deterministic upper bound O(m α(m, n))
---

The minimum spanning tree lower bound says that each correct MST algorithm must look at the weight of every edge that is not a [bridge](/bridge/) or a self-loop, on every input. In the [comparison model](/comparison-model/), where each step compares two weights, this gives at least $(m - b)/2$ comparisons for a graph with $m$ edges of which $b$ are bridges or self-loops, so $\Omega(m)$ for graphs without bridges. The bound is met in expectation by the randomized Karger-Klein-Tarjan algorithm, and it is the best general lower bound known, so the deterministic complexity of the MST problem lies between $\Omega(m)$ and $O(m\,\alpha(m, n))$.

## Statement

Let $G = (V, E)$ be a finite, connected, undirected graph with $m$ edges. Parallel edges are allowed. Let $b$ be the number of edges of $G$ that are bridges or self-loops. Consider a deterministic algorithm that knows $G$ and gets access to the weights $w : E \to \mathbb{R}$ only through queries, where each query depends on the weights of at most $q$ edges. Examples are a comparison $w(e) < w(f)$ (with $q = 2$) and a read of one weight (with $q = 1$). The algorithm must output a [minimum spanning tree](/minimum-spanning-tree/) of $(G, w)$ for every $w$. Weights may tie.

**Theorem.** For every weight function $w$, the run of the algorithm on $w$ makes at least one query that involves $e$, for each edge $e$ that is not a bridge or a self-loop. So it makes at least $(m - b)/q$ queries on every input. For a [2-edge-connected](/two-edge-connected-graph/) graph without self-loops, $b = 0$ and the bound is $m/q$.

The same bound holds for each Las Vegas randomized algorithm, on every run, and for the [MST verification](/mst-verification/) problem on each input where the given tree is an MST.

## In plain words

Suppose an algorithm never looks at the price of some road. Then it cannot know whether that road is very cheap or very expensive. If the road is very cheap, every best network must use it. If it is very expensive, no best network can use it, unless the road is the only way to reach some place. The algorithm gives the same answer in both cases, so it is wrong in one of them. So a correct algorithm must look at every road that has an alternative, and the work grows at least with the number of roads.

## Proof

Fix $w$ and the run of the algorithm on $w$. Let $T$ be its output, which is an MST of $(G, w)$. Let $e$ be an edge that is not a bridge and not a self-loop, and suppose that no query of the run involves $e$. Let $M$ be a number larger than $|w(f)|$ for every edge $f$.

Define $w'$ equal to $w$ on every edge except $e$. Each query of the run does not involve $e$, so it has the same answer under $w'$ as under $w$. The algorithm is deterministic, so its run on $w'$ asks the same queries, gets the same answers, and outputs the same $T$. Two cases show that $T$ is not an MST of $(G, w')$, which contradicts the correctness of the algorithm.

*Case $e \in T$.* Put $w'(e) = M$. The edge $e$ is not a bridge, so $G - e$ is connected. Removing $e$ from $T$ splits $T$ into two trees with vertex sets $S$ and $V \setminus S$, and some edge $f \ne e$ of $G$ crosses this cut, since $G - e$ is connected. Then $T - e + f$ is a spanning tree, and $w'(T - e + f) = w'(T) - M + w(f) < w'(T)$. So $T$ is not an MST of $w'$.

*Case $e \notin T$.* Put $w'(e) = -M$. The edge $e = uv$ is not a self-loop, so $u \ne v$, and the path from $u$ to $v$ in $T$ has some edge $f$. Then $T - f + e$ is a spanning tree, and $w'(T - f + e) = w'(T) - w(f) - M < w'(T)$. So $T$ is not an MST of $w'$.

Each case gives a contradiction, so some query of the run involves $e$. Each query involves at most $q$ edges and each of the $m - b$ edges must be involved in one, so the run makes at least $(m - b)/q$ queries.

For a Las Vegas algorithm, fix the random bits. The algorithm is then deterministic and must be correct for each $w$ with these bits, so the argument applies to each run. For MST verification, the input is $(G, w, T)$ and the answer is yes. If some edge $e$ that is not a bridge or a self-loop is not involved in any query, the same $w'$ makes $T$ fail to be an MST, but the run and the answer yes stay the same. $\blacksquare$

## Consequences

- **The MST problem takes $\Omega(m)$ time** in each model where a step touches $O(1)$ weights: the comparison model, the [decision tree model](/decision-tree-model/) with comparisons of two weights, and the [word RAM](/word-ram/) with one weight per word. On graphs with $m \ge 2n$ the bound is $\Omega(n + m)$ even after removing bridges, since a connected graph has at most $n - 1$ bridges.
- **Linear-time algorithms are optimal.** The [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/) runs in expected $O(m)$ time and the Fredman-Willard algorithm for integer weights on the word RAM runs in $O(m)$ worst-case time, so both meet the bound. Prim's algorithm with a [Fibonacci heap](/fibonacci-heap/) meets it on graphs with $m = \Omega(n \log n)$.
- **MST verification takes $\Theta(m)$ time.** The theorem gives $\Omega(m)$, and linear-time verification algorithms exist ([MST verification](/mst-verification/)).
- **Only the order of the weights matters,** and the proof uses only the extreme values $M$ and $-M$. So the same bound holds for integer weights and for distinct weights: put $w'(e)$ just above the largest or just below the smallest weight.

## Tightness

**Bridges and self-loops.** They need no query. A bridge is in every spanning tree and a self-loop is in none. When $G$ is itself a tree, every edge is a bridge, and the algorithm can output $E$ with no query at all. So the term $b$ cannot be dropped.

**The constant.** The bound $(m - b)/2$ comparisons is not always tight. On the cycle $C_n$, an MST is the cycle minus a heaviest edge, and [finding a maximum](/max-finding-lower-bound/) of $n$ values needs $n - 1$ comparisons, while the theorem gives $n/2$.

**The general gap.** No lower bound larger than $\Omega(m)$ is known for MST in the comparison model, and the best deterministic upper bound is Chazelle's $O(m\,\alpha(m, n))$. The algorithm of Pettie and Ramachandran runs within a constant factor of the optimal decision tree depth, so its running time is optimal, but that depth is known only to lie between these two bounds.

**Implicit graphs.** In the [algebraic decision tree](/algebraic-decision-tree/) model, the [Euclidean MST](/euclidean-minimum-spanning-tree/) of $n$ points needs $\Omega(n \log n)$ steps, by a reduction from sorting. That bound is in terms of $n$ for a complete graph with $\binom{n}{2}$ implicit edges, and it does not improve the bound for explicit graphs.

## History

The argument is an [adversary argument](/adversary-argument/) of the simplest kind, and papers on MST algorithms state it as the trivial lower bound. The question whether a deterministic algorithm can reach $O(m)$ is open. Karger, Klein and Tarjan reached expected linear time in 1995, Chazelle reached $O(m\,\alpha(m, n))$ in 2000, and Pettie and Ramachandran gave an algorithm of optimal but unknown complexity in 2002.

## References
