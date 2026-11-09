---
tag: 7P1NFC
kind: theorem
slug: minimum-cut-count-bound
name: Bound on the number of minimum cuts
aliases:
- Karger's cut-count bound
- at most n choose 2 minimum cuts
area: randomized/monte-carlo-and-las-vegas
level: advanced
summary: A connected multigraph on n vertices has at most n(n-1)/2 minimum cuts. The proof uses the contraction algorithm, and the cycle shows that the bound is exact.
prereqs: [global-min-cut-problem, karger-min-cut, probabilistic-method]
see_also: [karger-min-cut, karger-stein, global-min-cut-problem, randomized-contractions, stoer-wagner, min-cut-problem, probabilistic-method, error-amplification]
sources:
  - paper: "David R. Karger, Global min-cuts in RNC, and other ramifications of a simple min-cut algorithm, Proceedings of the 4th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1993"
    title: David R. Karger, Global min-cuts in RNC, and other ramifications of a simple min-cut algorithm
    locator: pages 21 to 30 (the contraction algorithm, its success probability, and the bound on the number of minimum cuts)
  - paper: doi:10.1145/234533.234534
    title: David R. Karger and Clifford Stein, A new approach to the minimum cut problem, Journal of the ACM 43(4), 1996
    locator: pages 601 to 640 (the contraction algorithm, the count of minimum and near-minimum cuts, and the recursive contraction algorithm)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 1 (the randomized min-cut algorithm, its success probability 2/(n(n-1)), and the exercise on the number of minimum cuts)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 1, Section 1.1 (a min-cut algorithm, with the probability bound by contraction)
---

A connected multigraph with $n$ vertices has at most $\binom{n}{2} = n(n-1)/2$ minimum cuts. The proof is probabilistic: one run of [Karger's contraction algorithm](/karger-min-cut/) outputs any fixed minimum cut with probability at least $2/(n(n-1))$, and it outputs only one cut, so there can be at most $n(n-1)/2$ of them. The cycle on $n$ vertices has exactly $n(n-1)/2$ minimum cuts, so the bound is exact. It contrasts with minimum $s$-$t$ cuts, whose number can be exponential in $n$.

## Statement

Notation on this page: $G = (V, E)$ is a multigraph with $n = |V| \ge 2$ vertices, parallel edges allowed and no loops. A **cut** is a partition $\{S, V \setminus S\}$ with both sides nonempty; its size $|E(S, V \setminus S)|$ is the number of edges with one end on each side. $\lambda$ is the size of a minimum cut. $\Pr$ is over the random choices of the contraction algorithm.

**Theorem (Karger 1993).** If $G$ is connected, then $G$ has at most $\binom{n}{2}$ minimum cuts.

**Lemma (the contraction bound).** If $G$ is connected and $C$ is a minimum cut of $G$, one run of the contraction algorithm outputs $C$ with probability at least $\binom{n}{2}^{-1} = \frac{2}{n(n-1)}$.

The *contraction algorithm*: while more than two vertices remain, pick an edge uniformly at random among the remaining edges, merge its two ends into one vertex, and delete the loops that this creates; keep parallel edges. When two vertices remain, each stands for a set of original vertices, and these two sets form the output cut.

For a minimum cut, the edge set determines the partition, because both sides of a minimum cut of a connected graph induce connected subgraphs. So counting the minimum cuts as partitions or as edge sets gives the same number.

## In plain words

Squeeze a graph by picking a random link and fusing its two ends, again and again, until only two blobs are left. The links between the two blobs form a cut. A smallest cut has few links compared to the whole graph, so a random pick rarely hits one of them. A smallest cut survives the whole squeeze with a chance of at least one in "number of pairs of vertices".

Every run ends with exactly one cut. If there were more smallest cuts than pairs of vertices, the chances of ending with each of them would add up to more than one, which cannot happen. So a graph has at most as many smallest cuts as it has pairs of vertices. A ring of vertices has exactly that many, because cutting any two links of the ring is a smallest cut.

## Proof

**Proof of the lemma.** Fix a minimum cut $C = \{S, V \setminus S\}$ with edge set $F = E(S, V \setminus S)$, so $|F| = \lambda$. Since $G$ is connected, $\lambda \ge 1$.

*Every cut of a contracted graph is a cut of $G$.* A vertex of a contracted graph stands for a set of original vertices, so a cut of the contracted graph is a cut of $G$ with the same edges. Hence every contracted graph has minimum cut at least $\lambda$.

*Many edges remain.* Suppose $k$ vertices remain, and none of the edges of $F$ has been contracted yet. Each vertex $v$ of the contracted graph has degree at least $\lambda$, because the edges at $v$ form the cut $\{v\}$ against the rest. So the contracted graph has at least $k\lambda/2$ edges. The edges of $F$ are still all present, since an edge is deleted only when it is contracted or becomes a loop, and an edge of $F$ becomes a loop only if its two ends were merged, which needs a path of contracted edges from $S$ to $V \setminus S$, so a contracted edge of $F$. The next step picks an edge of $F$ with probability at most

$$\frac{\lambda}{k\lambda/2} = \frac{2}{k}.$$

*Survival.* The algorithm does $n - 2$ steps, with $k = n, n - 1, \dots, 3$ vertices before each. Let $\mathcal{E}_k$ be the event that the step with $k$ vertices does not contract an edge of $F$. By the bound above, conditioned on the earlier steps,

$$\Pr[\text{no edge of } F \text{ is ever contracted}] \ge \prod_{k=3}^{n} \left(1 - \frac{2}{k}\right) = \prod_{k=3}^{n} \frac{k - 2}{k} = \frac{(n-2)!}{n!/2} = \frac{2}{n(n-1)}.$$

*Survival means output $C$.* If no edge of $F$ is contracted, every contracted edge has both ends on the same side of $C$, so every vertex of every contracted graph stands for a subset of $S$ or a subset of $V \setminus S$. At the end two vertices remain, and their sets cover $V$; since $S$ and $V \setminus S$ are both nonempty, one set is $S$ and the other is $V \setminus S$. So the output is $C$. $\square$

**Proof of the theorem.** Let $C_1, \dots, C_t$ be the distinct minimum cuts. One run outputs exactly one cut, so the events "the output is $C_i$" are disjoint, and

$$1 \ge \sum_{i=1}^{t} \Pr[\text{output} = C_i] \ge t \cdot \frac{2}{n(n-1)}.$$

Hence $t \le n(n-1)/2$. $\blacksquare$

**Where connectivity is used.** If $G$ is not connected, then $\lambda = 0$, the degree bound $k\lambda/2$ says nothing, and the theorem fails: a graph with $c$ components has $2^{c-1} - 1$ cuts of size 0, which is $31 > 15$ for six isolated vertices.

## Consequences

- **Karger's algorithm works.** A single run finds a given minimum cut with probability at least $2/(n(n-1))$. Repeating it $\binom{n}{2} \ln(1/\delta)$ times and keeping the smallest cut fails with probability at most $\delta$, see [Karger's algorithm](/karger-min-cut/) and [error amplification](/error-amplification/). The [Karger-Stein algorithm](/karger-stein/) improves the running time by contracting only to about $n/\sqrt{2}$ vertices before branching.
- **All minimum cuts at once.** Since each minimum cut is output with probability at least $2/(n(n-1))$, about $\binom{n}{2} \ln \binom{n}{2}$ runs output every minimum cut with constant probability, by a union bound over the at most $\binom{n}{2}$ cuts. So all minimum cuts can be listed in randomized polynomial time.
- **Near-minimum cuts.** The same argument, stopped earlier, shows that the number of cuts of size at most $\alpha\lambda$ is $O(n^{2\alpha})$ for each fixed $\alpha \ge 1$ (Karger 1993, Karger and Stein 1996). This count is the basis of cut sparsification and of the analysis of network reliability.
- **A compact representation.** Because there are only $O(n^2)$ minimum cuts, all of them can be stored in polynomial space. A classical result of Dinits, Karzanov and Lomonosov (1976) represents all minimum cuts of a graph by a cactus graph with $O(n)$ nodes; it gives another proof of the bound.
- **A probabilistic counting argument.** The proof is an example of the [probabilistic method](/probabilistic-method/): a random process that hits each object with probability at least $p$ shows that there are at most $1/p$ objects.

## Tightness

**The cycle.** In the cycle $C_n$ with $n \ge 3$, every cut has at least 2 edges, and removing any 2 of the $n$ edges splits the cycle into two paths. So $\lambda = 2$ and the minimum cuts correspond to the $\binom{n}{2}$ pairs of edges. The bound is exact. On the cycle, one contraction run outputs each of the $\binom{n}{2}$ minimum cuts with probability exactly $2/(n(n-1))$; the tests check this by exact computation for $n \le 6$.

**Small graphs.** An exhaustive search over all connected simple graphs on at most 5 vertices (in the tests) and on 6 vertices (in a separate run) finds maximum counts $1, 3, 6, 10, 15$ for $n = 2, \dots, 6$, equal to $\binom{n}{2}$. For $n \ge 3$ the graphs that reach the bound are exactly the labeled cycles: 1, 3, 12 and 60 graphs for $n = 3, 4, 5, 6$. Multigraphs can also reach it, for example a cycle with every edge doubled.

**Minimum $s$-$t$ cuts are not bounded.** Join $s$ and $t$ by $n - 2$ paths of length 2. A minimum $s$-$t$ cut cuts one edge of each path, and either edge will do, so there are $2^{n-2}$ minimum $s$-$t$ cuts; for $n = 7$ that is $32 > 21$. The theorem is about global minimum cuts, and the contraction argument needs that every vertex has degree at least $\lambda$, which fails for $s$-$t$ cuts.

**The lemma is tight.** On the cycle, the probability $2/(n(n-1))$ of the lemma is reached exactly for every minimum cut.

## History

Karger (1993) introduced the random contraction algorithm for the global minimum cut and observed that its analysis bounds the number of minimum cuts by $\binom{n}{2}$, and the number of $\alpha$-approximate minimum cuts by $O(n^{2\alpha})$. Karger and Stein (1996) gave the full journal version, with the recursive contraction algorithm. The bound on the number of minimum cuts was known before through the cactus representation of Dinits, Karzanov and Lomonosov (1976), but the contraction argument made it a one-line consequence of a randomized algorithm, and it is now a standard example in textbooks such as Motwani and Raghavan (1995) and Mitzenmacher and Upfal (2005).

## References
