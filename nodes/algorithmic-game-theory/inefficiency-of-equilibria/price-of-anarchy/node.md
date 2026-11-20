---
tag: CAPT9J
kind: definition
slug: price-of-anarchy
name: Price of anarchy
aliases:
- coordination ratio
area: algorithmic-game-theory/inefficiency-of-equilibria
level: intro
summary: The ratio between the cost of the worst equilibrium of a game and the cost of an optimal outcome.
prereqs: [nash-equilibrium]
see_also: [price-of-stability, smoothness-framework, pigou-example, roughgarden-tardos-four-thirds-bound, price-of-anarchy-of-load-balancing, shapley-network-design-game, coarse-correlated-equilibrium, first-price-auction-price-of-anarchy]
sources:
  - paper: doi:10.1007/3-540-49116-3_38
    title: "Elias Koutsoupias and Christos Papadimitriou, Worst-case equilibria, STACS 1999, Lecture Notes in Computer Science 1563, 404-413"
    locator: the coordination ratio of a load balancing game on parallel links
  - paper: doi:10.1145/380752.380883
    title: "Christos Papadimitriou, Algorithms, games, and the internet, STOC 2001, 749-753"
    locator: the name price of anarchy
  - paper: doi:10.1145/506147.506153
    title: "Tim Roughgarden and Eva Tardos, How bad is selfish routing?, Journal of the ACM 49(2) (2002), 236-259"
    locator: the price of anarchy of nonatomic selfish routing
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 17, Tim Roughgarden and Eva Tardos, Introduction to the inefficiency of equilibria (the definition and the first examples, including Example 17.1)
  - book: isbn:9780262182430
    title: Tim Roughgarden, Selfish Routing and the Price of Anarchy, MIT Press, 2005
    locator: Section 2.3 (the price of anarchy)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 11 (selfish routing and the price of anarchy)
---

The price of anarchy measures how much a system loses when its players act selfishly instead of following a central plan. For a game with a cost to minimize, it is the cost of the worst equilibrium divided by the least cost of any outcome. A value of 1 means that every equilibrium is optimal, and a large value means that selfish play can be very costly. A bound on the price of anarchy is a statement about a class of games, such as all [selfish routing](/selfish-routing-model/) networks with affine latencies, and it depends on the equilibrium notion. Koutsoupias and Papadimitriou introduced the measure in 1999 as the *coordination ratio*, and Papadimitriou named it the price of anarchy in 2001.

## Definition

Let $G$ be a game with players $1, \ldots, n$, strategy sets $S_i$ and a social cost $C(s) \ge 0$ for each strategy profile $s$, for example the sum of the players' costs or the largest cost. Fix an equilibrium notion and let $\mathrm{EQ}(G)$ be the set of equilibria of $G$. For a randomized equilibrium $\sigma$, its cost is the expected cost $C(\sigma) = \mathbb{E}_{s \sim \sigma}[C(s)]$. Let $\mathrm{OPT}(G) = \min_s C(s)$.

**Definition.** If $\mathrm{EQ}(G)$ is not empty, the *price of anarchy* of $G$ is

$$\mathrm{PoA}(G) = \sup_{\sigma \in \mathrm{EQ}(G)} \frac{C(\sigma)}{\mathrm{OPT}(G)}.$$

For a class $\mathcal{G}$ of games, $\mathrm{PoA}(\mathcal{G}) = \sup_{G \in \mathcal{G}} \mathrm{PoA}(G)$. If $\mathrm{OPT}(G) = 0$, the ratio is 1 when the equilibrium also costs 0 and $+\infty$ otherwise. Always $\mathrm{PoA} \ge 1$.

**Which equilibria.** The value depends on the notion. Common choices are pure [Nash equilibria](/nash-equilibrium/), mixed Nash equilibria, [correlated equilibria](/correlated-equilibrium/), [coarse correlated equilibria](/coarse-correlated-equilibrium/), [Bayes-Nash equilibria](/bayes-nash-equilibrium/), and Wardrop equilibria in nonatomic games. Since pure $\subseteq$ mixed $\subseteq$ correlated $\subseteq$ coarse correlated, the price of anarchy can only grow along this chain. For pure equilibria the definition needs a game class in which pure equilibria exist, such as [potential games](/potential-game/). A statement of a bound should name the class of games, the social cost, and the equilibrium notion.

**Welfare form.** In a game where the players gain value, such as an auction, let $W$ be the social welfare to maximize. Then

$$\mathrm{PoA}(G) = \frac{\max_s W(s)}{\inf_{\sigma \in \mathrm{EQ}(G)} W(\sigma)} \ge 1.$$

Many papers on auctions state the inverse ratio, a number at most 1. For example, a welfare guarantee of $1 - 1/e \approx 0.632$ is a price of anarchy of $e/(e - 1) \approx 1.582$ in the form above, and $1 - 1/e^2 \approx 0.865$ is $1.157$. Say which form a result uses.

## Examples and non-examples

**Pigou's network.** Two parallel links with latencies 1 and $x$ and one unit of nonatomic traffic. The unique Wardrop equilibrium costs 1, and the optimum costs $3/4$, so the price of anarchy is $4/3$. Over all networks with affine latencies the price of anarchy is exactly $4/3$ ([Pigou's example](/pigou-example/), [Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)). For polynomial latencies of degree at most $d$ it is about $d / \ln d$, and over all continuous nondecreasing latencies it is unbounded ([Pigou bound](/pigou-bound/)).

**Load balancing, pure equilibria.** Two identical machines and jobs of sizes 2, 2, 1 and 1. Each job pays the load of its machine, and the social cost is the makespan. Put both jobs of size 2 on machine 1 and both jobs of size 1 on machine 2. The loads are 4 and 2. A job of size 2 that moves would also see load 4, and a job of size 1 that moves would see 5, so this is a pure Nash equilibrium. The optimum puts a 2 and a 1 on each machine, with makespan 3. So this game has price of anarchy at least $4/3$ ([load balancing price of anarchy](/price-of-anarchy-of-load-balancing/)).

**Load balancing, mixed equilibria.** Two identical machines and two jobs of size 1. If each job picks a machine uniformly at random, each job expects load $1 + 1/2$ on either machine, so neither can gain and this is a mixed equilibrium. The jobs collide with probability $1/2$, so the expected makespan is $\tfrac{1}{2} \cdot 2 + \tfrac{1}{2} \cdot 1 = 3/2$. The optimum is 1. The pure equilibria here are optimal, but the mixed one has ratio $3/2$.

**Fair cost sharing.** $n$ players go from $s$ to $t$ over two parallel edges with costs 1 and $n$, and the players on an edge split its cost equally. If all use the edge of cost $n$, each pays 1, and a player who moves alone to the other edge also pays 1. So this is a pure equilibrium with cost $n$, against the optimum 1. The price of anarchy is $n$, while the best equilibrium, all on the edge of cost 1, is optimal ([Shapley network design game](/shapley-network-design-game/), [price of stability](/price-of-stability/)).

**Prisoner's dilemma.** Let each player pay 1 if both cooperate, 2 if both defect, and 3 against 0 if one defects alone. Defection is dominant, so the only equilibrium is both defecting, with total cost 4. The optimum, both cooperating, costs 2. The price of anarchy is 2 ([prisoner's dilemma](/prisoners-dilemma/)).

**A non-example: the best equilibrium.** In the fair cost sharing game above, the ratio of the cheapest equilibrium to the optimum is 1. That ratio is the price of stability, not the price of anarchy. The price of anarchy uses the worst equilibrium.

**A non-example: no pure equilibrium.** In matching pennies no pure Nash equilibrium exists, so the pure price of anarchy is not defined. The mixed price of anarchy is defined, because every finite game has a mixed equilibrium.

## Related definitions

- **Price of stability.** The best equilibrium over the optimum. It is at most the price of anarchy, and the two are equal when all equilibria have the same cost, as in nonatomic routing ([price of stability](/price-of-stability/)).
- **Robust price of anarchy.** A bound proved by the [smoothness framework](/smoothness-framework/) holds for pure, mixed, correlated and coarse correlated equilibria at once, and for the time-averaged cost of [no-regret dynamics](/no-regret-dynamics/) up to an error that goes to 0.
- **Strong price of anarchy.** The same ratio over strong Nash equilibria, where no coalition can deviate so that all its members gain. Fewer profiles qualify, so the ratio is at most the price of anarchy.
- **Bicriteria bounds.** Instead of a ratio of costs, compare the equilibrium with an optimum for a harder task. In selfish routing, an equilibrium costs at most an optimal flow for twice the traffic ([Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)).
- **Bayes-Nash price of anarchy.** In games of incomplete information, the ratio of expected welfare of the optimum to that of the worst Bayes-Nash equilibrium ([first-price auction price of anarchy](/first-price-auction-price-of-anarchy/)).

## References
