---
tag: 86Z2YD
kind: definition
slug: wardrop-equilibrium
name: Wardrop equilibrium
aliases:
- user equilibrium
- Wardrop's first principle
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: A flow in a nonatomic routing game in which every used path of a commodity has the least latency among its paths.
prereqs: [selfish-routing-model, nash-equilibrium]
see_also: [system-optimal-flow, beckmann-potential, pigou-example, braess-paradox, price-of-anarchy, atomic-congestion-game, shortest-path, dijkstra]
sources:
  - paper: doi:10.1680/ipeds.1952.11259
    title: "J. G. Wardrop, Some theoretical aspects of road traffic research, Proceedings of the Institution of Civil Engineers 1(3) (1952), 325-362"
    locator: the first principle (equal journey times on all used routes, no larger than on any unused route) and the second principle (least average journey time)
  - book: "Martin Beckmann, C. B. McGuire and Christopher B. Winsten, Studies in the Economics of Transportation, Yale University Press, 1956"
    locator: Part I (the equilibrium conditions of a road network and their existence and uniqueness)
  - paper: doi:10.1016/0191-2615(79)90022-5
    title: "M. J. Smith, The existence, uniqueness and stability of traffic equilibria, Transportation Research Part B 13(4) (1979), 295-304"
    locator: the variational inequality form of the equilibrium
  - paper: doi:10.6028/jres.073b.010
    title: "Stella C. Dafermos and Frederick T. Sparrow, The traffic assignment problem for a general network, Journal of Research of the National Bureau of Standards, Section B 73B(2) (1969), 91-118"
    locator: the user-optimized and system-optimized flows on a general network
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 18, Tim Roughgarden, Routing games, Definition 18.1 (nonatomic equilibrium flow), Theorem 18.8 (existence and uniqueness) and Proposition 18.20 (variational inequality characterization)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 11 (equilibrium flows and the variational inequality in the proof of the price of anarchy bound)
---

A Wardrop equilibrium is a flow in the [selfish routing model](/selfish-routing-model/) in which, for each commodity, every path that carries traffic has the least latency among all paths of that commodity. It is the [Nash equilibrium](/nash-equilibrium/) of a game with a continuum of travelers, where no single traveler can change the latencies. Wardrop stated it in 1952 as the first of two principles of route choice. The second principle, least total travel time, defines the [system optimal flow](/system-optimal-flow/), and the two flows differ in general ([Pigou's example](/pigou-example/)).

## Definition

Use the notation of the [selfish routing model](/selfish-routing-model/): an instance $(G, r, \ell)$ with commodities $i = 1, \ldots, k$, path sets $\mathcal{P}_i$, continuous nondecreasing latencies $\ell_e \ge 0$, edge flows $f_e$ and path latencies $\ell_P(f) = \sum_{e \in P} \ell_e(f_e)$.

**Definition.** A feasible flow $f$ is a *Wardrop equilibrium* if for every commodity $i$ and every pair of paths $P, P' \in \mathcal{P}_i$,

$$f_P > 0 \implies \ell_P(f) \le \ell_{P'}(f).$$

Let $L_i(f) = \min_{P \in \mathcal{P}_i} \ell_P(f)$ be the shortest path latency of commodity $i$ for the lengths $\ell_e(f_e)$. The definition says that $f_P > 0$ implies $\ell_P(f) = L_i(f)$. So all used paths of a commodity have the same latency, and unused paths have a latency at least as large. Then the cost of the flow is

$$C(f) = \sum_{i=1}^{k} \sum_{P \in \mathcal{P}_i} f_P \, \ell_P(f) = \sum_{i=1}^{k} L_i(f) \sum_{P \in \mathcal{P}_i} f_P = \sum_{i=1}^{k} r_i \, L_i(f).$$

The latency is a cost that each traveler minimizes. One traveler has measure 0, so a switch from $P$ to $P'$ leaves $f$ unchanged and changes the traveler's cost from $\ell_P(f)$ to $\ell_{P'}(f)$. So the definition says exactly that no traveler gains by a switch.

**Equivalent forms.** For a feasible flow $f$ the following three statements are equivalent.

1. $f$ is a Wardrop equilibrium.
2. (*Variational inequality*, Smith 1979.) $\sum_{e} \ell_e(f_e) \, f_e \le \sum_{e} \ell_e(f_e) \, g_e$ for every feasible flow $g$.
3. $f$ minimizes the Beckmann potential $\Phi(g) = \sum_e \int_0^{g_e} \ell_e(x)\,dx$ over the feasible flows ([Beckmann potential](/beckmann-potential/) proves this).

*Proof of 1 if and only if 2.* Fix $f$ and let $H(g) = \sum_e \ell_e(f_e) g_e$. This is the cost of $g$ when each edge latency is frozen at its value under $f$. Expanding $g_e = \sum_{P \ni e} g_P$ gives $H(g) = \sum_P \ell_P(f) g_P$. Each path of commodity $i$ has $\ell_P(f) \ge L_i(f)$, so $H(g) \ge \sum_i r_i L_i(f)$ for every feasible $g$. If $f$ is an equilibrium, $H(f) = \sum_i r_i L_i(f)$, so $H(f) \le H(g)$, which is statement 2. If $f$ is not an equilibrium, some path $P \in \mathcal{P}_i$ has $f_P > 0$ and $\ell_P(f) > \ell_{P'}(f)$ for some $P' \in \mathcal{P}_i$. Let $g$ move all the flow $f_P$ from $P$ to $P'$. Then $H(g) - H(f) = f_P \big(\ell_{P'}(f) - \ell_P(f)\big) < 0$, and statement 2 fails. $\square$

**Existence and uniqueness.** Every instance has a Wardrop equilibrium, and any two equilibria $f$ and $\tilde f$ have $\ell_e(f_e) = \ell_e(\tilde f_e)$ on every edge, so the same $L_i$ and the same cost (Beckmann, McGuire and Winsten 1956; NRTV Theorem 18.8). If every $\ell_e$ is strictly increasing, the edge flows are unique too. The path flows need not be unique.

**How to test a flow.** Compute, for each commodity, the shortest path distances $d_i(v)$ from $s_i$ with the edge lengths $\ell_e(f_e) \ge 0$, for example with [Dijkstra's algorithm](/dijkstra/). In edge form, $f$ is an equilibrium if and only if every edge $e = (u, v)$ with $f^i_e > 0$ is *tight* for commodity $i$: $d_i(v) = d_i(u) + \ell_e(f_e)$. A path made of tight edges has length $d_i(t_i)$, and a path with a slack edge is longer, so this is the definition again. The test takes $k$ shortest path computations, $O(k (|E| + |V| \log |V|))$ time with a binary heap, after the $|E|$ latencies are evaluated.

## Examples and non-examples

**Pigou's network.** Two parallel links from $s$ to $t$ with $\ell_1(x) = 1$ and $\ell_2(x) = x$, and rate 1. The flow $(f_1, f_2) = (0, 1)$ is an equilibrium: the used link has latency 1, and the other link also has latency 1. Its cost is 1. The flow $(1/2, 1/2)$ is *not* an equilibrium: link 1 carries flow at latency 1, and link 2 has latency $1/2$. Yet $(1/2, 1/2)$ has the least cost, $3/4$ ([Pigou's example](/pigou-example/)).

**Three parallel links.** Let $\ell_1(x) = x$, $\ell_2(x) = x + 1$, $\ell_3(x) = 2x + 1$ and $r = 3$. At an equilibrium with common latency $L \ge 1$ on the three links, the flows are $L$, $L - 1$ and $(L - 1)/2$. Their sum is 3 when $L = 9/5$. So the equilibrium is $(9/5, 4/5, 2/5)$. Each link has latency $9/5$, and the cost is $3 \cdot 9/5 = 27/5$. With $r = 1$ instead, the equilibrium is $(1, 0, 0)$: links 2 and 3 are unused, and their latency $1$ equals the latency of link 1. An unused path may tie with the used ones.

**Braess's network with the shortcut.** Vertices $s, v, w, t$, edges $s \to v$ and $w \to t$ with latency $x$, edges $v \to t$ and $s \to w$ with latency 1, the edge $v \to w$ with latency 0, and rate 1. Send all traffic on $s \to v \to w \to t$. Then the three paths have latencies $1 + 0 + 1 = 2$, $1 + 1 = 2$ and $1 + 1 = 2$. All are equal, so the flow is an equilibrium, with cost 2. It is the only one. Write $a = f_{sv}$ and $b = f_{wt}$. The path $s \to v \to t$ has latency $a + 1$, the path $s \to w \to t$ has $1 + b$, and the zigzag path has $a + b$. If $s \to v \to t$ carries flow at an equilibrium, then $a + 1 \le a + b$, so $b = 1$, and all traffic uses $w \to t$, which this path does not use. That is a contradiction, and the same argument applies to $s \to w \to t$ ([Braess's paradox](/braess-paradox/)).

**Edge latencies are unique, path flows are not.** Let $s \to v$ have two parallel edges $a, b$ and $v \to t$ two parallel edges $c, d$, all with latency $x$, and rate 1. The paths are $ac, ad, bc, bd$. Every equilibrium has $f_a = f_b = f_c = f_d = 1/2$, but both $(f_{ac}, f_{ad}, f_{bc}, f_{bd}) = (1/2, 0, 0, 1/2)$ and $(1/4, 1/4, 1/4, 1/4)$ are equilibria, each with latency 1 on every path.

**A non-example: equal latencies on the used paths only.** In the three-link network with $r = 3$, the flow $(2, 1, 0)$ gives the used links 1 and 2 the same latency 2. It is not an equilibrium, because the unused link 3 has latency $\ell_3(0) = 1 < 2$. The test must compare the used paths with all paths of the commodity, not only with each other.

## Related definitions

- **System optimal flow.** Wardrop's second principle: the average journey time is least. It is a [system optimal flow](/system-optimal-flow/), and it is a Wardrop equilibrium for the marginal cost latencies $\ell_e(x) + x \ell_e'(x)$ when $x \ell_e(x)$ is convex. Dafermos and Sparrow (1969) called the two flows *user-optimized* and *system-optimized*.
- **Price of anarchy.** The ratio of the equilibrium cost to the optimal cost. Since all equilibria have the same cost, it is a number of the instance, and it is at most $4/3$ for affine latencies ([price of anarchy](/price-of-anarchy/), [Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)).
- **Approximate equilibrium.** For $\varepsilon \ge 0$, a flow is an $\varepsilon$-approximate equilibrium if every used path has $\ell_P(f) \le L_i(f) + \varepsilon$ (additive) or $\ell_P(f) \le (1 + \varepsilon) L_i(f)$ (multiplicative). Say which one a result uses. Iterative methods and learning dynamics reach these, not exact equilibria.
- **Atomic equilibrium.** In an [atomic congestion game](/atomic-congestion-game/) a player compares its path with other paths after its own unit moves. Pure equilibria exist there by [Rosenthal's potential](/rosenthal-potential-theorem/), but they need not have the same cost.
- **Variable demand.** If the rate $r_i$ falls when $L_i$ grows, an equilibrium also asks that $r_i$ equals the demand at the latency $L_i$. Beckmann, McGuire and Winsten treated this case with the same potential method.
- **Equilibria with perception errors.** In stochastic route choice models of transport, travelers see the latencies with random errors, and used paths need not be shortest. These flows are not Wardrop equilibria.

## References
