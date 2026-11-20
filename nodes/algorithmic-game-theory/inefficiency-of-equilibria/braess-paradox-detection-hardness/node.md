---
tag: B6G3NJ
kind: theorem
slug: braess-paradox-detection-hardness
name: "Hardness of detecting Braess's paradox"
aliases:
- Roughgarden network design hardness
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: Finding the subnetwork with the best equilibrium latency is NP-hard to approximate within a factor below 4/3 for linear latencies.
prereqs: [braess-paradox, wardrop-equilibrium, np-complete]
see_also: [roughgarden-tardos-four-thirds-bound, pigou-bound, marginal-cost-tolls, vertex-disjoint-paths, parameterized-disjoint-paths, approximation-ratio, selfish-routing-model, price-of-anarchy]
sources:
  - paper: doi:10.1016/j.jcss.2005.05.009
    title: "Tim Roughgarden, On the severity of Braess's Paradox: designing networks for selfish users is hard, Journal of Computer and System Sciences 72(5) (2006), 922-953; FOCS 2001, 472-481"
    locator: "Section 3 (linear latencies: the trivial algorithm is a 4/3-approximation, and the reduction from two directed disjoint paths), Section 4 (general latencies, the bound floor(n/2)) and Section 5 (polynomial latencies); numbering as in the author's 2004 preprint"
  - paper: "Steven Fortune, John Hopcroft and James Wyllie, The directed subgraph homeomorphism problem, Theoretical Computer Science 10(2) (1980), 111-121"
    locator: the NP-completeness of two vertex-disjoint paths in a directed graph
  - paper: "Henry Lin, Tim Roughgarden, Eva Tardos and Asher Walkover, Stronger bounds on Braess's paradox and the maximum latency of selfish routing, SIAM Journal on Discrete Mathematics 25(4) (2011)"
    locator: bounds on the size of the paradox in multicommodity networks
  - paper: "Igal Milchtaich, Network topology and the efficiency of equilibrium, Games and Economic Behavior 57(2) (2006)"
    locator: the undirected two-terminal networks in which the paradox cannot occur are the series-parallel ones
---

[Braess's paradox](/braess-paradox/) shows that removing an edge can lower the latency of a Wardrop equilibrium. This page is about the algorithmic question that follows: given a network, which edges should a designer remove to get the best equilibrium? Roughgarden proved in 2001 that for linear latencies the answer "remove nothing" is already within a factor $4/3$ of the best, and that no polynomial-time algorithm does better unless P = NP. The paradox itself, with its numbers $2$ and $3/2$, is on the page [Braess's paradox](/braess-paradox/).

## Statement

Take a single-commodity instance $(G, r, \ell)$ of the [selfish routing model](/selfish-routing-model/): a directed graph $G$ with source $s$ and sink $t$, a traffic rate $r > 0$, and continuous nondecreasing latencies $\ell_e \ge 0$. The equilibrium notion is the [Wardrop equilibrium](/wardrop-equilibrium/) of the nonatomic game, which always exists. In an equilibrium all used paths have the same latency, and this common latency is the same in every equilibrium; call it $L(G)$. The cost of the equilibrium is $r\, L(G)$. For a subgraph $H$ of $G$ that contains an $s$-$t$ path, $L(H)$ is the common latency of the equilibria of $(H, r, \ell)$.

**Network design problem.** Given $(G, r, \ell)$, find a subgraph $H$ that minimizes $L(H)$.

The trivial algorithm returns $H = G$.

**Theorem 1 (Roughgarden; the trivial algorithm).** If every latency is affine, $\ell_e(x) = a_e x + b_e$ with $a_e, b_e \ge 0$, then $L(G) \le \frac{4}{3} L(H)$ for every subgraph $H$. So the trivial algorithm is a $4/3$-approximation.

**Theorem 2 (Roughgarden; hardness).** For every $\varepsilon > 0$ there is no polynomial-time $(4/3 - \varepsilon)$-approximation algorithm for the network design problem with affine latencies, unless P = NP.

**Theorem 3 (Roughgarden; other latencies).** With arbitrary continuous nondecreasing latencies, the trivial algorithm is a $\lfloor n/2 \rfloor$-approximation on graphs with $n$ vertices, and nothing better is possible in polynomial time unless P = NP. For polynomial latencies of degree at most $p$ with nonnegative coefficients, the same holds with the factor $\Theta(p / \ln p)$.

## In plain words

Sometimes closing a road makes traffic faster, because selfish drivers stop crowding onto a shortcut. A planner may want to find the best roads to close. For roads whose delay grows in a straight line with traffic, closing roads never helps by more than a quarter of the travel time, so leaving the network alone is already close to the best choice. But to do better than that, the planner must solve a hard puzzle about two routes that cannot share any crossing. No fast method for that puzzle is known, so in practice no fast method beats the plan of closing nothing.

## Proof

**Proof of Theorem 1.** Let $f$ be an equilibrium of $G$ and $h$ an equilibrium of $H$. The flow $h$ is also a feasible flow in $G$. Every $s$-$t$ path of $G$ has latency at least $L(G)$ under $f$, and $h$ sends $r$ units on such paths, so

$$r\, L(G) \le \sum_{e} \ell_e(f_e)\, h_e.$$

For each edge, $(a_e f_e + b_e) h_e \le (a_e h_e + b_e) h_e + \frac{1}{4} a_e f_e^2$, because $a_e f_e h_e \le a_e h_e^2 + \frac{1}{4} a_e f_e^2$ is $a_e (h_e - f_e/2)^2 \ge 0$. The right side is at most $\ell_e(h_e) h_e + \frac{1}{4} \ell_e(f_e) f_e$. Summing over the edges,

$$r\, L(G) \le \sum_e \ell_e(h_e)\, h_e + \frac{1}{4} \sum_e \ell_e(f_e)\, f_e = r\, L(H) + \frac{1}{4}\, r\, L(G).$$

So $\frac{3}{4} L(G) \le L(H)$. $\blacksquare$

This is the same inequality as in the [Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/), with the optimal flow replaced by the equilibrium of the subgraph.

**Proof of Theorem 2.** The reduction is from the two directed disjoint paths problem: given a directed graph $G$ and vertices $s_1, t_1, s_2, t_2$, are there an $s_1$-$t_1$ path and an $s_2$-$t_2$ path with no vertex in common? Fortune, Hopcroft and Wyllie (1980) proved it [NP-complete](/np-complete/) ([vertex-disjoint paths](/vertex-disjoint-paths/)).

Build $G'$ from $G$: give every edge of $G$ latency 0, add vertices $s$ and $t$, and add four edges

| edge | latency |
|---|---|
| $(s, s_1)$ | 1 |
| $(s, s_2)$ | $x$ |
| $(t_1, t)$ | $x$ |
| $(t_2, t)$ | 1 |

Set $r = 1$. Every $s$-$t$ path uses one edge out of $s$ and one edge into $t$. Write $z$ for the flow on $(s, s_2)$ and $y$ for the flow on $(t_1, t)$. A path of type $s_1 \to t_1$ costs $1 + y$, of type $s_2 \to t_2$ costs $z + 1$, of type $s_2 \to t_1$ costs $z + y$, and of type $s_1 \to t_2$ costs 2.

*Yes-instance.* Let $H$ be the two disjoint paths and the four new edges. $H$ has exactly two $s$-$t$ paths, and the split $1/2, 1/2$ gives each a latency $1 + 1/2 = 3/2$. So $L(H) = 3/2$.

*No-instance.* Let $H$ be any subgraph of $G'$. Suppose first that $H$ contains an $s_2$-$t_1$ path. Let $a$, $b$ and $c$ be the flow on paths of types $s_1 \to t_1$, $s_2 \to t_2$ and $s_2 \to t_1$, and suppose $L(H) < 2$, so type $s_1 \to t_2$ is unused and $a + b + c = 1$. Then $z + y = (b + c) + (a + c) = 1 + c$.

- If $c > 0$, then $L(H) = z + y = 1 + c$. If also $a > 0$, then $L(H) = 1 + y = 1 + a + c$, so $a = 0$, a contradiction; in the same way $b = 0$. So $c = 1$ and $L(H) = 2$, a contradiction.
- If $c = 0$, the unused path of type $s_2 \to t_1$ costs $z + y = 1$, but a used path costs $1 + y$ or $z + 1$, which is more than 1 because $a > 0$ or $b > 0$. This breaks the equilibrium condition.

So $L(H) \ge 2$. If $H$ has no $s_2$-$t_1$ path, then $H$ cannot have both an $s_1$-$t_1$ path and an $s_2$-$t_2$ path: they would share a vertex $v$, since the instance is a no-instance, and $s_2 \to v \to t_1$ would be a path. So every path of $H$ uses $(s, s_1)$, or every path uses $(t_2, t)$. In the first case the paths cost $1 + y$ (type $s_1 \to t_1$) or 2 (type $s_1 \to t_2$). If $1 + y < 2$, all flow is on type $s_1 \to t_1$, so $y = 1$, a contradiction. So $L(H) = 2$, and the second case is the same.

A $(4/3 - \varepsilon)$-approximation algorithm would return a subgraph with $L < \frac{4}{3} \cdot \frac{3}{2} = 2$ on a yes-instance, and every subgraph has $L \ge 2$ on a no-instance. So it would decide the two disjoint paths problem. $\blacksquare$

**Theorem 3** uses larger gadgets of the same kind. The full proofs are in Sections 4 and 5 of the paper.

### Example

Let $G$ have the edges $s_1 \to t_1$, $s_2 \to t_2$ and $s_2 \to t_1$. The disjoint paths exist, and $G'$ is exactly Braess's network: the paths $s s_1 t_1 t$ and $s s_2 t_2 t$ cost $1 + x$ each, and the path $s s_2 t_1 t$ uses the two $x$ edges. All traffic takes $s s_2 t_1 t$, at latency $1 + 1 = 2$, and the other paths also cost 2. Removing $s_2 \to t_1$ gives $L = 3/2$.

Now let $G$ have a middle vertex $v$ and the edges $s_1 \to v$, $v \to t_1$, $s_2 \to v$ and $v \to t_2$. Every $s_1$-$t_1$ path and every $s_2$-$t_2$ path meet at $v$, so this is a no-instance. In $G'$, the equilibrium sends everything along $s \to s_2 \to v \to t_1 \to t$ at latency 2, and by the proof no subgraph does better.

## Consequences

- **Detection is hard.** Call an instance paradox-free if no subgraph has a smaller equilibrium latency than $G$. Roughgarden derived from the same reduction that it is NP-hard to tell paradox-free instances from instances with the paradox, so there is no efficient general test for Braess's paradox in a network.
- **Design for selfish users.** A designer who wants a good equilibrium cannot, in general, find the best edges to remove. The best general strategy, for linear latencies, is to remove nothing.
- **Tolls compared with removal.** Cole, Dodis and Roughgarden later proved that with linear latencies the best tolls help no more than the best edge removal when tolls count in the cost ([marginal cost tolls](/marginal-cost-tolls/)).
- **The paradox is bounded.** Theorem 1 says that for linear latencies, removing edges lowers the equilibrium latency by at most a factor $4/3$. Braess's network reaches this factor, so the bound is exact.

## Tightness

- Braess's network shows that the factor $4/3$ in Theorem 1 is reached: $L(G) = 2$ and $L(H) = 3/2$.
- Theorem 2 shows that the factor of the trivial algorithm cannot be improved by any polynomial-time algorithm unless P = NP. The same holds for the factors in Theorem 3.
- The factor $\lfloor n/2 \rfloor$ for general latencies is reached by a family of graphs that generalize Braess's network, given in the same paper.

## History

Braess described the paradox in 1968. Roughgarden posed the network design question for selfish users and proved Theorems 1 to 3 at FOCS 2001, in a paper that grew into the 2006 journal article. Milchtaich (2006) characterized the undirected two-terminal topologies in which the paradox cannot happen, for any latencies: they are the series-parallel networks. Lin, Roughgarden, Tardos and Walkover studied the size of the paradox in multicommodity networks, where it can be much larger. Later work by Cenciarelli, Gorla and Salvo (Algorithmica, 2019) studied which directed topologies admit the paradox.

## References
