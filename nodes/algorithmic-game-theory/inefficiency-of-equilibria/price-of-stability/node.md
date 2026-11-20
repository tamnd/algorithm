---
tag: 1N61PD
kind: definition
slug: price-of-stability
name: Price of stability
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: The ratio between the cost of the best equilibrium of a game and the cost of an optimal outcome.
prereqs: [price-of-anarchy, nash-equilibrium]
see_also: [harmonic-price-of-stability, shapley-network-design-game, potential-game, rosenthal-potential-theorem, atomic-linear-congestion-price-of-anarchy, beckmann-potential, load-balancing-game, pure-nash-equilibrium]
sources:
  - paper: doi:10.1137/070680096
    title: "Elliot Anshelevich, Anirban Dasgupta, Jon Kleinberg, Eva Tardos, Tom Wexler and Tim Roughgarden, The price of stability for network design with fair cost allocation, SIAM Journal on Computing 38(4) (2008), 1602-1623"
    locator: the price of stability of fair cost sharing network design, the H(n) upper bound by the potential function and the matching example in directed networks
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 17, Tim Roughgarden and Eva Tardos, Introduction to the inefficiency of equilibria, Section 17.1 (the price of anarchy and the price of stability), and Chapter 18, Tim Roughgarden, Routing games, Section 18.3.1 (the two coincide in nonatomic instances)
  - paper: doi:10.1007/11561071_8
    title: "George Christodoulou and Elias Koutsoupias, On the price of anarchy and stability of correlated equilibria of linear congestion games, ESA 2005, Lecture Notes in Computer Science 3669, 59-70"
    locator: the bounds on the price of stability of pure equilibria in linear congestion games
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 15 (best-case and strong Nash equilibria, the price of stability of network cost-sharing games)
---

The price of stability is the cost of the best equilibrium of a game divided by the least cost of any outcome. The [price of anarchy](/price-of-anarchy/) asks how bad the worst equilibrium can be. The price of stability asks how good a stable outcome can be. It fits a setting where a designer may propose an outcome to the players, but the outcome must be an equilibrium, or they will not keep it. Then the price of stability is the cost of asking for stability. Anshelevich, Dasgupta, Kleinberg, Tardos, Wexler and Roughgarden used it for network design with fair cost sharing, where the worst equilibrium can cost $n$ times the optimum but the best one costs at most $H(n) = 1 + 1/2 + \cdots + 1/n$ times it.

## Definition

Let $G$ be a game with social cost $C(s) \ge 0$ on strategy profiles, an equilibrium notion with set of equilibria $\mathrm{EQ}(G)$, and $\mathrm{OPT}(G) = \min_s C(s)$, as for the [price of anarchy](/price-of-anarchy/). For a randomized equilibrium $\sigma$, $C(\sigma)$ is its expected cost.

**Definition.** If $\mathrm{EQ}(G)$ is not empty, the *price of stability* of $G$ is

$$\mathrm{PoS}(G) = \inf_{\sigma \in \mathrm{EQ}(G)} \frac{C(\sigma)}{\mathrm{OPT}(G)}.$$

For a class $\mathcal{G}$ of games, $\mathrm{PoS}(\mathcal{G}) = \sup_{G \in \mathcal{G}} \mathrm{PoS}(G)$: the best equilibrium in each game, the worst game in the class. If $\mathrm{OPT}(G) = 0$, the ratio is 1 when some equilibrium costs 0 and $+\infty$ otherwise.

Always $1 \le \mathrm{PoS}(G) \le \mathrm{PoA}(G)$, and the two are equal when all equilibria have the same cost. If the game has finitely many equilibria, the price of stability is 1 exactly when some optimal outcome is an equilibrium.

**Welfare form.** For a welfare $W$ to maximize, $\mathrm{PoS}(G) = \max_s W(s) / \sup_{\sigma \in \mathrm{EQ}(G)} W(\sigma) \ge 1$.

**Which equilibria.** Most results are for pure Nash equilibria, so the class must have them. [Potential games](/potential-game/) do, and they come with a method. The notion matters in the other direction from the price of anarchy: a larger set of equilibria, such as mixed or correlated, can only lower the price of stability. State the class, the social cost and the equilibrium notion.

**The potential function method.** Let $\Phi$ be an exact potential of a finite game, and suppose $C(s) \le A \, \Phi(s)$ and $\Phi(s) \le B \, C(s)$ for all profiles $s$. Let $s'$ minimize $\Phi$. A unilateral move that lowers a player's cost lowers $\Phi$ by the same amount, so $s'$ is a pure Nash equilibrium. Then

$$C(s') \le A \, \Phi(s') \le A \, \Phi(s^*) \le A B \, C(s^*)$$

for an optimal profile $s^*$, so $\mathrm{PoS} \le AB$. The same bound holds for the equilibrium that best-response dynamics reach from $s^*$, since each step lowers $\Phi$.

## Examples and non-examples

**Fair cost sharing on two parallel edges.** $n$ players go from $s$ to $t$ over edges of cost 1 and $n$, and the players on an edge split its cost equally. All players on the edge of cost $n$ is an equilibrium: each pays 1, and a lone move to the other edge also costs 1. All players on the edge of cost 1 is an equilibrium too, and it is optimal. So $\mathrm{PoA} = n$ and $\mathrm{PoS} = 1$ ([Shapley network design game](/shapley-network-design-game/)).

**An optimum that is not stable.** Take a directed network with sink $t$, two players with sources $s_1$ and $s_2$, own edges $s_1 \to t$ of cost 1 and $s_2 \to t$ of cost $1/2$, edges $s_1 \to v$ and $s_2 \to v$ of cost 0, and a shared edge $v \to t$ of cost $1 + \varepsilon$. The optimum sends both players through $v$, with cost $1 + \varepsilon$. It is not an equilibrium: player 2 pays $(1 + \varepsilon)/2 > 1/2$ there and leaves. Then player 1 alone pays $1 + \varepsilon > 1$ and leaves too. With both on their own edges, neither gains by a move, because the shared edge alone costs $1 + \varepsilon$. If player 1 uses $v$ alone, it pays $1 + \varepsilon > 1$, and if player 2 uses $v$ alone, it pays $1 + \varepsilon > 1/2$. So the only equilibrium costs $3/2$, and $\mathrm{PoS} = (3/2)/(1 + \varepsilon)$, which tends to $3/2 = H(2)$. With $n$ players and own edges of cost $1/i$ for player $i$, a similar argument gives $H(n)$.

**The upper bound $H(n)$.** In fair cost sharing, Rosenthal's potential is $\Phi(s) = \sum_e c_e H(n_e)$, where $n_e$ is the number of players on edge $e$ ([Rosenthal potential theorem](/rosenthal-potential-theorem/)). The cost is $C(s) = \sum_{e : n_e \ge 1} c_e$. Since $1 \le H(n_e) \le H(n)$ on used edges, $C \le \Phi \le H(n)\, C$, so the potential method gives $\mathrm{PoS} \le H(n)$. The example above shows that $H(n)$ is tight in directed networks ([harmonic price of stability](/harmonic-price-of-stability/)).

**Nonatomic routing.** In a [selfish routing](/selfish-routing-model/) instance all Wardrop equilibria have the same cost ([Beckmann potential](/beckmann-potential/)), so $\mathrm{PoS} = \mathrm{PoA}$. In Pigou's network both are $4/3$.

**Atomic linear congestion games.** For pure equilibria the price of anarchy is $5/2$ ([atomic linear congestion bound](/atomic-linear-congestion-price-of-anarchy/)). The price of stability is smaller: Christodoulou and Koutsoupias (2005) showed that it is at least $1 + 1/\sqrt{3} \approx 1.577$ and at most $1.6$.

**Load balancing.** On identical machines, take the schedule whose machine loads, sorted in decreasing order, form the lexicographically smallest vector. Its largest load is least, so it is optimal. A job that gains by a move would make the sorted vector smaller, so no job gains, and it is a pure equilibrium. So $\mathrm{PoS} = 1$. The pure price of anarchy of two machines is $4/3$, for example with jobs 2, 2, 1, 1 ([load balancing game](/load-balancing-game/)).

**A non-example: the prisoner's dilemma.** The only equilibrium is mutual defection. Since there is one equilibrium, the price of stability equals the price of anarchy, and it says nothing new. The price of stability is useful only when a game has several equilibria of different cost.

## Related definitions

- **Price of anarchy.** The worst equilibrium over the optimum ([price of anarchy](/price-of-anarchy/)). A bound on it holds for any equilibrium the players reach, while a bound on the price of stability needs some way to pick the good one.
- **Strong price of anarchy.** The worst strong Nash equilibrium over the optimum. Strong equilibria resist deviations by coalitions. In fair cost sharing every strong equilibrium costs at most $H(n)$ times the optimum, when one exists (Twenty Lectures, Lecture 15).
- **Undirected networks.** For fair cost sharing in undirected networks $H(n)$ is an upper bound, but it is not known to be tight. The exact value is an open problem. For a common sink, Jian Li proved an upper bound $O(\log n / \log \log n)$, and the known lower bounds are constants.
- **Potential minimizers.** In a potential game the minimizer of the potential is one stable outcome that a designer can compute or reach by best responses. Its cost gives the potential method bound, even when other equilibria are worse.

## References
