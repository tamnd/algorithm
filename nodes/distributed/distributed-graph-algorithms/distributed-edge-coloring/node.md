---
tag: 2M70EM
kind: problem
slug: distributed-edge-coloring
name: Distributed edge coloring
aliases:
- distributed (2Delta-1)-edge coloring
area: distributed/distributed-graph-algorithms
level: research
summary: Colour the edges so that edges at a node differ, by local communication. 2Delta - 1 colours take O(log n) rounds with randomness and O~(log^2 n) deterministically; fewer colours are harder.
prereqs: [local-model, edge-coloring, line-graph, distributed-vertex-coloring]
see_also: [distributed-maximal-matching, linial-algorithm, ring-coloring, linial-coloring-lower-bound, vizing-theorem, list-coloring, chernoff-bound, network-decomposition]
sources:
  - paper: doi:10.1137/S0097539793250767
    title: Alessandro Panconesi and Aravind Srinivasan, Randomized distributed edge coloring via an extension of the Chernoff-Hoeffding bounds, SIAM Journal on Computing 26(2), 1997
    locator: pp. 350 to 368 (randomized edge colouring with 1.6 Delta + O(log^(1+delta) n) colours w.h.p. in polylogarithmic time, and tail bounds for lambda-correlated random variables; also PODC 1992)
  - paper: doi:10.1007/PL00008932
    title: Alessandro Panconesi and Romeo Rizzi, Some simple distributed algorithms for sparse networks, Distributed Computing 14(2), 2001
    locator: the deterministic (2 Delta - 1)-edge colouring in O(Delta + log* n) rounds
  - paper: doi:10.1109/FOCS.2017.25
    title: Manuela Fischer, Mohsen Ghaffari and Fabian Kuhn, Deterministic distributed edge-coloring via hypergraph maximal matching, FOCS 2017
    locator: pp. 180 to 191 (deterministic (2 Delta - 1)-list edge colouring in O(log^7 Delta log n) rounds, by maximal matching in hypergraphs of rank 3; arXiv 1704.02767)
  - paper: doi:10.1137/1.9781611975031.168
    title: Yi-Jun Chang, Qizheng He, Wenzheng Li, Seth Pettie and Jara Uitto, The complexity of distributed edge coloring with small palettes, SODA 2018
    locator: pp. 2633 to 2652 (the lower bounds Omega(log_Delta n) deterministic and Omega(log_Delta log n) randomized for (2 Delta - 2)-edge colouring, and randomized (1 + eps) Delta-edge colouring through the distributed LLL)
  - paper: doi:10.1145/3564246.3585243
    title: Mohsen Ghaffari and Christoph Grunau, Faster deterministic distributed MIS and approximate matching, STOC 2023
    locator: pp. 1777 to 1790 (deterministic O~(log^2 n) rounds for MIS, which by known reductions extends to maximal matching and (2 Delta - 1)-edge colouring)
---

In the distributed edge colouring problem, the nodes of a network must give each edge a colour so that the edges at any node have different colours. The greedy palette has $2\Delta - 1$ colours: an edge has at most $2\Delta - 2$ adjacent edges, so any order of colouring succeeds, and the problem is the vertex colouring of the [line graph](/line-graph/) with its degree plus one colours. This palette takes $O(\log n)$ rounds with randomness and $\tilde O(\log^2 n)$ rounds deterministically. With $2\Delta - 2$ or fewer colours the problem becomes much harder, and the target of [Vizing's theorem](/vizing-theorem/), $\Delta + 1$ colours, needs other methods.

Notation on this page: $G = (V, E)$ has $n$ nodes, $m$ edges and maximum degree $\Delta$. $L(G)$ is the line graph, whose nodes are the edges of $G$, with two of them adjacent when they share an end; its maximum degree is at most $2\Delta - 2$. A colouring with $k$ colours is a $k$-edge colouring. $\tilde O$ hides factors polynomial in $\log \log n$. The model is [LOCAL](/local-model/) unless stated, and "w.h.p." means with probability at least $1 - n^{-c}$.

## In plain words

Each person in a club has some partners for weekly games, and each pair plays once a week. Every game needs a day, and nobody can play two games on the same day. The club wants to use few days.

If every pair picks its day one at a time, it can always find a free day as long as there are about twice as many days as the largest number of partners of one person. The problem is to do this fast when pairs can only talk with the people they share.

A good method is to let many pairs pick a random free day at the same time. If two games with a shared person picked the same day, both try again later. A fixed share of the games succeeds in each attempt, so all games have days after a small number of attempts.

## Definition

**Input.** A graph $G$ in the LOCAL or [CONGEST](/congest-model/) model, with unique identifiers. Each node knows $\Delta$, or an upper bound.

**Output.** Each edge gets a colour from $\{1, \dots, k\}$, known to both of its ends.

**Condition.** A proper [edge colouring](/edge-coloring/): two edges with a common end have different colours. Each colour class is then a matching.

**Palette.** The problem depends strongly on $k$:

- $k = 2\Delta - 1$ is the greedy threshold. Every partial colouring extends, and the problem is $(\Delta' + 1)$-vertex colouring on $L(G)$ with $\Delta' = 2\Delta - 2$.
- $(1 + \varepsilon)\Delta \le k \le 2\Delta - 2$: a partial colouring can get stuck, and the algorithms need randomness or global arguments.
- $k = \Delta + 1$ is always possible by Vizing's theorem, and $k = \Delta$ is possible for some graphs only, for example for bipartite graphs.

**Distributed view.** The cost is the number of synchronous rounds. Local computation is free, so the question is how far information must travel. This differs from a parallel algorithm for edge colouring, where the cost is work and span. A LOCAL algorithm for $L(G)$ runs on $G$ with a constant factor more rounds, since two adjacent edges share an end that can relay their messages.

## Variants

- **List edge colouring.** Each edge $e$ has its own list of at least $\deg(u) + \deg(v) - 1$ colours, where $e = \{u, v\}$. Greedy still succeeds, and the deterministic algorithm of Fischer, Ghaffari and Kuhn solves this form.
- **Fewer colours.** $(1 + \varepsilon)\Delta$, $\Delta + O(\sqrt{\Delta})$ or $\Delta + 1$ colours, usually for $\Delta$ above some function of $n$.
- **Bipartite graphs.** $\Delta$ colours exist by König's theorem, and the distributed algorithms for few colours often start from the bipartite case.
- **Strong edge colouring and distance-2 versions.** Edges at distance at most 1 must also differ; this is vertex colouring of the square of $L(G)$.
- **CONGEST.** The edge colour needs only $O(\log \Delta)$ bits, so the random trial algorithm below runs with the same round bound.

## Examples

- **Cycles.** For a cycle, $L(C_n) = C_n$, so 3-edge colouring of a cycle is 3-vertex colouring of a cycle: [ring colouring](/ring-coloring/) with $\Theta(\log^* n)$ rounds. Here $\Delta = 2$ and $2\Delta - 1 = 3$; two colours are enough for even cycles but take $\Theta(n)$ rounds.
- **A star.** All $\Delta$ edges meet at the centre, so the centre colours them $1, \dots, \Delta$ in one round. Local structure makes this easy.
- **The complete graph $K_9$.** Here $\Delta = 8$ and the palette has 15 colours; $\chi'(K_9) = 9$. In the tests of the code below, a random trial colours about 33% of the uncoloured edges, and all edges are coloured after 8 trials on average.
- **A bad partial colouring.** On a path $a, b, c, d$ with $\Delta = 2$ and $k = 2$, colouring $\{a, b\}$ with 1 and $\{c, d\}$ with 2 leaves no colour for $\{b, c\}$. With $k = 3$ this cannot happen, which is why the greedy palette is easy.

## Known algorithms

**Random trials.** In each trial, every uncoloured edge becomes active with probability $\tfrac12$ and picks a uniform colour from its palette, the colours that no coloured adjacent edge has; it keeps the colour if no adjacent active edge picked the same one. One end of the edge picks the colour and sends it to the other end, and each end then reports a clash at its side, so a trial takes two rounds.

*Claim.* In each trial, an uncoloured edge is coloured with probability at least $\tfrac14$.

*Proof.* Let $e$ have $d$ uncoloured adjacent edges and palette $P_e$. Each coloured adjacent edge removes at most one colour, so $|P_e| \ge (2\Delta - 1) - (2\Delta - 2 - d) = d + 1$. Given that $e$ is active, an adjacent edge $f$ clashes with it if $f$ is active and picks the colour of $e$. For a fixed $f$, this has probability $\tfrac12 \sum_c \Pr[e \text{ picks } c] \Pr[f \text{ picks } c] \le \tfrac12 \cdot \tfrac{1}{|P_e|} \sum_c \Pr[f \text{ picks } c] \le \tfrac{1}{2 |P_e|}$, since the choices are independent. By the union bound, $e$ clashes with probability at most $\tfrac{d}{2(d + 1)} < \tfrac12$, so $e$ is coloured with probability at least $\tfrac12 \cdot \tfrac12$. $\blacksquare$

So the expected number of uncoloured edges falls by a factor $\tfrac34$ per trial, and after $O(\log m) = O(\log n)$ trials no edge is left w.h.p.

**Deterministic, small degree.** [Linial's algorithm](/linial-algorithm/) on $L(G)$ gives $O(\Delta^2)$ colours in $O(\log^* n)$ rounds, and a colour reduction then gives $2\Delta - 1$ colours, in $O(\Delta^2 + \log^* n)$ rounds in total. Panconesi and Rizzi (2001) gave a simple deterministic algorithm in $O(\Delta + \log^* n)$ rounds. On graphs of constant degree, this is $O(\log^* n)$, which is optimal by the ring.

**Deterministic, polylogarithmic.** Fischer, Ghaffari and Kuhn (2017) gave the first deterministic algorithm with $\mathrm{poly}(\log n)$ rounds for all $\Delta$, $O(\log^7 \Delta \log n)$ rounds, also for list edge colouring: they reduce it to maximal matching in a hypergraph of rank 3 and find that matching by rounding fractional matchings. Ghaffari and Grunau (2023) reached $\tilde O(\log^2 n)$ rounds, through deterministic MIS and known reductions.

**Fewer colours, with randomness.** Panconesi and Srinivasan (1997) used $1.6\Delta + O(\log^{1 + \delta} n)$ colours w.h.p. in polylogarithmic time. Their analysis needed tail bounds for sums of dependent random variables, and they extended the [Chernoff-Hoeffding bounds](/chernoff-bound/) to negatively correlated variables. Dubhashi, Grable and Panconesi (1998) used the nibble method to get $(1 + \varepsilon)\Delta$ colours when $\Delta$ is large compared with $\log n$. Chang, He, Li, Pettie and Uitto (2018) reduced $(1 + \varepsilon)\Delta$-edge colouring to $O(\log \varepsilon^{-1})$ calls to a distributed [Lovász local lemma](/lovasz-local-lemma/) algorithm, with palettes down to $\Delta + \tilde O(\sqrt \Delta)$.

| Algorithm | Colours | Rounds | Randomized |
|---|---|---|---|
| Random trials on $L(G)$ | $2\Delta - 1$ | $O(\log n)$ | yes |
| Linial on $L(G)$ plus colour reduction | $2\Delta - 1$ | $O(\Delta^2 + \log^* n)$ | no |
| Panconesi and Rizzi (2001) | $2\Delta - 1$ | $O(\Delta + \log^* n)$ | no |
| Fischer, Ghaffari and Kuhn (2017) | $2\Delta - 1$, lists | $O(\log^7 \Delta \log n)$ | no |
| Ghaffari and Grunau (2023) | $2\Delta - 1$ | $\tilde O(\log^2 n)$ | no |
| Panconesi and Srinivasan (1997) | $1.6\Delta + O(\log^{1 + \delta} n)$ | $\mathrm{poly}(\log n)$ | yes |
| Dubhashi, Grable and Panconesi (1998) | $(1 + \varepsilon)\Delta$, large $\Delta$ | $O(\log n)$ | yes |
| Chang, He, Li, Pettie and Uitto (2018) | $(1 + \varepsilon)\Delta$ | $O(\log \varepsilon^{-1})$ LLL calls | yes |

## Bounds

- **$\Omega(\log^* n)$ for every palette.** On a cycle, any $O(1)$-edge colouring is an $O(1)$-vertex colouring of the cycle, so [Linial's lower bound](/linial-coloring-lower-bound/) applies.
- **The greedy threshold is sharp.** Chang, He, Li, Pettie and Uitto showed that $(2\Delta - 2)$-edge colouring needs $\Omega(\log_\Delta n)$ rounds deterministically and $\Omega(\log_\Delta \log n)$ rounds with randomness. So for constant $\Delta$, one colour less than greedy changes the complexity from $\Theta(\log^* n)$ to $\Omega(\log n)$.
- **Randomized below $\log n$.** For $2\Delta - 1$ colours, randomness can do better than the $O(\log n)$ of plain random trials: a few random rounds leave only small components, and a deterministic algorithm finishes on them. The resulting bounds are polynomial in $\log \log n$.
- **Easier than maximal matching.** The [KMW lower bound](/kmw-lower-bound/) gives $\Omega(\log \Delta / \log \log \Delta)$ rounds for maximal matching, and later bounds give $\Omega(\min(\Delta, \log n / \log \log n))$ deterministic rounds. These bounds do not carry over to $(2\Delta - 1)$-edge colouring: Balliu, Brandt, Kuhn and Olivetti (2022) colour in $\mathrm{poly}(\log \Delta) + O(\log^* n)$ deterministic rounds, which is far below the matching bound when $\Delta$ is about $\log n / \log \log n$.

## Reductions

- **To vertex colouring.** $(2\Delta - 1)$-edge colouring is $(\Delta' + 1)$-vertex colouring of $L(G)$, so every algorithm on the [distributed vertex colouring](/distributed-vertex-coloring/) page applies, with a constant factor more rounds.
- **To maximal matching.** Given a $(2\Delta - 1)$-edge colouring, process the colours one by one and add every edge of the current colour whose ends are both free. Each colour class is a matching, so the edges of one class do not conflict, and the result is a [maximal matching](/distributed-maximal-matching/) after $2\Delta - 1$ more rounds.
- **From maximal matching.** Take a maximal matching of the uncoloured edges as colour $i$, for $i = 1, 2, \dots$. If an edge $e$ is not chosen, the matching covers an end of $e$, so one of its adjacent uncoloured edges gets coloured. Since $e$ has at most $2\Delta - 2$ adjacent edges, it is coloured within $2\Delta - 1$ steps. So $(2\Delta - 1)$-edge colouring costs at most $2\Delta - 1$ maximal matchings.
- **List edge colouring and hypergraph matching.** Fischer, Ghaffari and Kuhn reduce $(2\Delta - 1)$-list edge colouring to maximal matching in a hypergraph of rank 3, and find that matching deterministically by rounding fractional matchings.

## Applications

- **Scheduling pairwise transfers.** Each colour class is a matching, so the edges of one class can exchange data at the same time without a node taking part in two exchanges. The number of colours is the number of time slots; this is used for link scheduling in wireless networks and for data migration.
- **A subroutine.** Edge colourings give maximal matchings, as above, and are used to split edges into classes in algorithms for orientations and decompositions.
- **A test case for distributed complexity.** The jump at $2\Delta - 2$ colours and the methods for fewer colours, such as the nibble and the distributed LLL, made edge colouring a model problem in the study of [locally checkable labelings](/locally-checkable-labeling/).

## References
