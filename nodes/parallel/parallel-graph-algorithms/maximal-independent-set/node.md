---
tag: J9ZM07
kind: problem
slug: maximal-independent-set
name: Maximal independent set
aliases:
- MIS
area: parallel/parallel-graph-algorithms
level: core
summary: Find an independent vertex set to which no further vertex can be added; not necessarily maximum.
prereqs: [independent-set, work-span-model]
see_also: [luby-mis, maximum-independent-set, distributed-mis, maximal-matching, israeli-itai, jones-plassmann, ruling-set, kmw-lower-bound]
sources:
  - paper: doi:10.1137/0215074
    title: Michael Luby, A simple parallel algorithm for the maximal independent set problem, SIAM Journal on Computing 15(4), 1986
    locator: pp. 1036 to 1053 (the randomized algorithm, the pairwise independent derandomization, and applications such as maximal matching); section numbers to be checked
  - paper: doi:10.1145/4221.4226
    title: Richard M. Karp and Avi Wigderson, A fast parallel algorithm for the maximal independent set problem, Journal of the ACM 32(4), 1985
    locator: pp. 762 to 773 (the first NC algorithm for MIS); DOI and pages to be checked
  - paper: doi:10.1016/0196-6774(86)90019-2
    title: Noga Alon, László Babai and Alon Itai, A fast and simple randomized parallel algorithm for the maximal independent set problem, Journal of Algorithms 7(4), 1986
    locator: pp. 567 to 583 (the randomized algorithm and its derandomization with small sample spaces)
  - paper: doi:10.1016/S0019-9958(85)80041-3
    title: Stephen A. Cook, A taxonomy of problems with fast parallel algorithms, Information and Control 64, 1985
    locator: pp. 2 to 22 (the lexicographically first maximal independent set is P-complete); DOI and pages to be checked
  - paper: doi:10.1145/2312005.2312058
    title: Guy E. Blelloch, Jeremy T. Fineman and Julian Shun, Greedy sequential maximal independent set and matching are parallel on average, SPAA 2012
    locator: the dependence length of random-order greedy MIS, O(log^2 n) with high probability, and the linear-work algorithms built on it
---

A maximal independent set (MIS) of a graph is a set of vertices, no two of them adjacent, such that every other vertex has a neighbour in the set. A greedy scan finds one in linear time, so the problem is easy sequentially; the question is how to find one in parallel. It is the basic symmetry-breaking problem of parallel and distributed computing: [maximal matching](/maximal-matching/) and $(\Delta + 1)$-coloring reduce to it, and it is solved in $O(\log n)$ rounds by [Luby's algorithm](/luby-mis/).

## In plain words

A group of people sit in a room, and some pairs of them are rivals. You want to pick a team in which no two members are rivals. You also want the team to be full: everybody left out must have a rival in the team, so that nobody else can join.

Such a team is easy to build one person at a time: take anybody who has no rival in the team yet, and repeat. The hard part is to build it fast when every person must decide at the same moment, using only what the neighbours say. If two rivals both decide to join, the team breaks; if both wait for the other, nobody joins. Random numbers are the usual way to break the tie.

The team does not have to be the largest possible. Any full team will do.

## Definition

Let $G = (V, E)$ be an undirected graph with $n$ vertices, $m$ edges and largest degree $\Delta$. A set $I \subseteq V$ is independent if no edge has both ends in $I$. It is a maximal independent set if, in addition, every vertex $v \notin I$ has a neighbour in $I$. Equivalently, $I$ is independent and dominating.

- **Input:** an undirected graph $G$.
- **Output:** a set $I \subseteq V$ that is a maximal independent set of $G$.

Every graph has a maximal independent set, and the graph with no edges has only one, $V$ itself. A [maximum independent set](/maximum-independent-set/), one of largest size, is maximal, but a maximal one can be much smaller: in a star with $k$ leaves, the center alone is maximal and the $k$ leaves are maximum. Finding a maximum independent set is NP-hard; finding a maximal one is not.

Work and span are counted in the [work-span model](/work-span-model/); rounds are counted in the synchronous model in which each vertex reads its neighbours in one round.

## Variants

- **Lexicographically first MIS.** Given an order of the vertices, the greedy MIS takes each vertex in order if no earlier neighbour was taken. Its output is fixed by the order. For an order given as part of the input, this problem is P-complete (Cook 1985).
- **Random-order greedy MIS.** For a uniformly random order, the greedy MIS can be computed in parallel: Blelloch, Fineman and Shun (2012) show that its dependence length is $O(\log^2 n)$ with high probability, and Fischer and Noever (2018) improve this to $\Theta(\log n)$.
- **Distributed MIS.** In the LOCAL and CONGEST models, every vertex is a processor and the cost is the number of rounds; see [distributed MIS](/distributed-mis/).
- **Ruling sets.** An $(\alpha, \beta)$-[ruling set](/ruling-set/) relaxes maximality: members are at distance at least $\alpha$ from each other, and every vertex is within distance $\beta$ of a member. An MIS is a $(2, 1)$-ruling set.
- **Maximal matching.** A maximal set of edges, no two sharing an end, is an MIS of the line graph of $G$.

## Examples

**A path.** On the path $0 - 1 - 2 - 3 - 4$, the sets $\{0, 2, 4\}$, $\{1, 3\}$ and $\{0, 3\}$ are maximal independent sets. The first is also maximum. The set $\{0, 2\}$ is independent but not maximal, because 4 has no neighbour in it.

**A star.** With center 0 and leaves 1 to $k$, the only maximal independent sets are $\{0\}$ and $\{1, \ldots, k\}$.

**A complete graph.** On $K_n$, every single vertex is a maximal independent set, and there are no others.

**A small maximal set.** On the cycle $0 - 1 - 2 - 3 - 4 - 5 - 0$, the set $\{0, 3\}$ is independent, and every vertex outside it is adjacent to 0 or 3: 1 and 5 to 0, 2 and 4 to 3. So $\{0, 3\}$ is maximal, of size 2, while $\{0, 2, 4\}$ has size 3. A greedy scan that takes 0 and then 3 stops there.

## Known algorithms

| algorithm | model | work | rounds or span | kind |
|---|---|---|---|---|
| sequential greedy | RAM | $O(n + m)$ | $n$ steps | deterministic |
| Karp and Wigderson (1985) | PRAM | polynomial | $O(\log^4 n)$ time | deterministic, first NC algorithm |
| [Luby](/luby-mis/) (1986), Alon, Babai and Itai (1986) | CRCW PRAM, work-span | $O(n + m)$ expected | $O(\log n)$ rounds w.h.p. | randomized |
| Luby (1986), pairwise independent form | PRAM | polynomial | $O(\log^2 n)$ time | deterministic |
| random-order greedy (Blelloch, Fineman, Shun 2012) | work-span | $O(n + m)$ expected | polylogarithmic span w.h.p. | randomized, same output as greedy |

The sequential greedy algorithm is optimal in work. Luby's algorithm in the form in which each vertex draws a random value and joins when its value is a local minimum removes at least half of the edges in expectation in each round, so the total expected work is $O(n + m)$ and the number of rounds is $O(\log n)$ with high probability; the proof is on the [Luby page](/luby-mis/). [Jones-Plassmann coloring](/jones-plassmann/) applies the same local-minimum rule to coloring.

## Bounds

- **Work.** Every algorithm must read the graph, so $\Omega(n + m)$ work is needed, and the greedy scan and Luby's algorithm (in expectation) meet it.
- **Parallel time.** The problem is in NC: Karp and Wigderson gave the first deterministic NC algorithm, and Luby's derandomization gives $O(\log^2 n)$ time with a polynomial number of processors. The randomized algorithms take $O(\log n)$ time with high probability. No polylogarithmic lower bound on the parallel time is known in the PRAM model.
- **Fixed order.** The lexicographically first MIS is P-complete, so it has no NC algorithm unless $\mathrm{P} = \mathrm{NC}$. The difficulty is in the fixed order, not in maximality.
- **Distributed rounds.** In the LOCAL model, Kuhn, Moscibroda and Wattenhofer prove a lower bound of $\Omega\big(\min\big(\sqrt{\log n / \log \log n}, \log \Delta / \log \log \Delta\big)\big)$ rounds for MIS; see the [KMW lower bound](/kmw-lower-bound/).

## Reductions

- **Maximal matching to MIS.** A maximal matching of $G$ is an MIS of its line graph $L(G)$, which has $m$ vertices and $O(m \Delta)$ edges. [Israeli and Itai](/israeli-itai/) solve maximal matching directly, without building $L(G)$.
- **$(\Delta + 1)$-coloring to MIS.** Build the graph $H$ on the pairs $(v, c)$ with $v \in V$ and $c \in \{1, \ldots, \Delta + 1\}$. Join $(v, c)$ to $(v, c')$ for $c \ne c'$, and $(u, c)$ to $(v, c)$ for every edge $\{u, v\}$. An MIS $I$ of $H$ holds at most one pair for each $v$, because the pairs of $v$ form a clique. It holds at least one: $v$ has at most $\Delta$ neighbours, so some color $c$ is used by no neighbour in $I$, and the pair $(v, c)$ is then either in $I$ or blocked by another pair of $v$ in $I$. So $I$ gives each vertex one color, and neighbours get different colors.
- **Vertex cover.** The ends of a maximal matching form a vertex cover at most twice the minimum. So an MIS algorithm for line graphs gives a parallel 2-approximation of vertex cover.

## Applications

- **Symmetry breaking.** An MIS picks a set of local leaders with no two adjacent, which is the first step of many parallel and distributed algorithms: clustering, coloring, and matching.
- **Graph coloring.** Removing one MIS after another colors the graph, one color for each MIS; [Jones-Plassmann](/jones-plassmann/) uses the same random priorities to get a greedy coloring.
- **Coarsening.** Algebraic multigrid and graph partitioners choose coarse vertices as an independent set of a graph built from the matrix or the graph, so that every fine vertex is next to a coarse one.
- **Scheduling.** Tasks that conflict share an edge; an MIS is a set of tasks that can run at once, and no other task can be added.

## References
