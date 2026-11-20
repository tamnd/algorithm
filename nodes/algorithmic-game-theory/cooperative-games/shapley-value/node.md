---
tag: 4T207Y
kind: definition
slug: shapley-value
name: Shapley value
aliases:
- Shapley value of a cooperative game
area: algorithmic-game-theory/cooperative-games
level: intro
summary: Pays each player its marginal contribution averaged over all orders in which the players can join the grand coalition.
prereqs: [transferable-utility-game, permutation]
see_also: [shapley-uniqueness-theorem, shapley-value-sampling, shapley-shubik-index, banzhaf-index, owen-multilinear-extension, marginal-contribution-nets, core-of-a-cooperative-game, nucleolus]
sources:
  - paper: doi:10.1515/9781400881970-018
    title: "Lloyd S. Shapley, A value for n-person games, in H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press, 1953, 307-317"
    locator: the axioms of the value, the formula as an average over orders, and the proof that the value is unique
  - paper: doi:10.2307/1951053
    title: "Lloyd S. Shapley and Martin Shubik, A method for evaluating the distribution of power in a committee system, American Political Science Review 48(3) (1954), 787-792"
    locator: the value applied to simple games, with the description by orders and pivots
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Chapter 18, The Shapley value (Section 18.1 the properties, Section 18.3 the definition and the characterization)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 12.2.1, The Shapley value
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 2, Basic concepts (the Shapley value and the Banzhaf index), and Chapter 3, Representations and algorithms
---

The Shapley value is a way to divide the worth $v(N)$ of a [transferable utility game](/transferable-utility-game/) among its players. Each player gets its marginal contribution, averaged over all $n!$ orders in which the players can arrive. Shapley (1953) showed that it is the only rule with four natural properties; that result is the [Shapley uniqueness theorem](/shapley-uniqueness-theorem/). Unlike the [core](/core-of-a-cooperative-game/) and the [nucleolus](/nucleolus/), the Shapley value is defined by a closed formula, it exists for every game, and it does not ask for stability against coalitions. On simple games it is the [Shapley-Shubik power index](/shapley-shubik-index/).

## Definition

A TU game is a pair $(N, v)$ with the players $N = \{1, \ldots, n\}$ and a function $v$ that gives a real number $v(S)$ to each coalition $S \subseteq N$, with $v(\emptyset) = 0$. For a player $i$ and a coalition $S$ with $i \notin S$, the number $v(S \cup \{i\}) - v(S)$ is the *marginal contribution* of $i$ to $S$.

Let $\pi$ be an order of the players, a [permutation](/permutation/) of $N$, and let $P_i^\pi$ be the set of the players that come before $i$ in $\pi$. The *Shapley value* of $i$ is

$$\varphi_i(v) = \frac{1}{n!} \sum_{\pi} \Big( v(P_i^\pi \cup \{i\}) - v(P_i^\pi) \Big),$$

where the sum is over all $n!$ orders. Think of the players as arriving one at a time in the order $\pi$, each one paid the amount that it adds to the worth of the players already there. The Shapley value is the expected payment when the order is uniform at random.

For a fixed $S \subseteq N \setminus \{i\}$ with $|S| = s$, the number of orders with $P_i^\pi = S$ is $s!\,(n-s-1)!$: the players of $S$ come first in any order, then $i$, then the others in any order. So the same value is

$$\varphi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{s!\,(n-s-1)!}{n!} \Big( v(S \cup \{i\}) - v(S) \Big).$$

This *subset formula* has $2^{n-1}$ terms per player, where the order formula has $n!$.

A third form uses the unanimity games. For a nonempty $T \subseteq N$, the game $u_T$ has $u_T(S) = 1$ if $T \subseteq S$ and $u_T(S) = 0$ if not. Every game is a unique sum $v = \sum_{T \ne \emptyset} d_T\, u_T$, with the *Harsanyi dividends* $d_T = \sum_{S \subseteq T} (-1)^{|T| - |S|} v(S)$ (this is [Möbius inversion](/mobius-inversion/) on the subsets of $N$). Then

$$\varphi_i(v) = \sum_{T \ni i} \frac{d_T}{|T|}:$$

each dividend is split equally among the members of its coalition.

The Shapley value has these properties for all games $v$ and $w$ on $N$:

- **Efficiency.** $\sum_{i \in N} \varphi_i(v) = v(N)$. Along each order the marginal contributions telescope to $v(N) - v(\emptyset)$.
- **Symmetry.** If $v(S \cup \{i\}) = v(S \cup \{j\})$ for every $S$ that contains neither $i$ nor $j$, then $\varphi_i(v) = \varphi_j(v)$.
- **Null player.** If $v(S \cup \{i\}) = v(S)$ for every $S$, then $\varphi_i(v) = 0$.
- **Additivity.** $\varphi(v + w) = \varphi(v) + \varphi(w)$.

The [uniqueness theorem](/shapley-uniqueness-theorem/) shows that no other rule has all four. The value is also *individually rational* for superadditive games ($\varphi_i(v) \ge v(\{i\})$, because each marginal contribution of $i$ is at least $v(\{i\})$ there), and it lies in the core of every [convex game](/convex-game/) ([Shapley's theorem on convex games](/shapley-convex-games-theorem/)).

For a cost game $(N, c)$, where $c(S)$ is the cost of serving $S$, the same formula applied to $c$ gives cost shares that sum to $c(N)$. The [airport game](/airport-game/) is the standard example.

**Computation.** With $v$ given as a table or as an oracle, the subset formula costs $2^{n-1}$ marginal contributions per player, and the exact value needs exponentially many values of $v$ in general. For compact inputs the cost depends on the input: it is linear in the size of a [marginal contribution net](/marginal-contribution-nets/), pseudo-polynomial for a [weighted voting game](/weighted-voting-game/) by [dynamic programming](/power-index-dynamic-programming/), and #P-hard for weighted voting games with binary weights ([hardness of power indices](/power-index-hardness/)). [Sampling random orders](/shapley-value-sampling/) gives an unbiased estimate with a Hoeffding error bound.

## Examples and non-examples

**A three-player game.** Let $n = 3$, $v(\{1, 2\}) = 4$, $v(\{1, 3\}) = 2$, $v(N) = 6$, and $v(S) = 0$ for the other coalitions. The marginal contributions in the six orders are:

| order | player 1 | player 2 | player 3 |
| --- | --- | --- | --- |
| 1, 2, 3 | 0 | 4 | 2 |
| 1, 3, 2 | 0 | 4 | 2 |
| 2, 1, 3 | 4 | 0 | 2 |
| 2, 3, 1 | 6 | 0 | 0 |
| 3, 1, 2 | 2 | 4 | 0 |
| 3, 2, 1 | 6 | 0 | 0 |
| sum | 18 | 12 | 6 |

So $\varphi(v) = (3, 2, 1)$, which sums to $v(N) = 6$. Each row sums to 6 too: one order alone already divides $v(N)$, but the rows differ, and only their mean treats the orders alike. The dividends give the same answer faster: $d_{\{1,2\}} = 4$, $d_{\{1,3\}} = 2$ and every other dividend is 0, so $v = 4u_{\{1,2\}} + 2u_{\{1,3\}}$. Player 1 gets $4/2 + 2/2 = 3$, player 2 gets $2$ and player 3 gets $1$.

**The glove game.** Player 1 has a left glove and players 2 and 3 each have a right glove. A pair is worth 1, so $v(S) = \min(|S \cap \{1\}|, |S \cap \{2, 3\}|)$. Player 1 adds 1 in every order except the two in which it comes first, so $\varphi_1 = 4/6 = 2/3$. By symmetry and efficiency, $\varphi_2 = \varphi_3 = 1/6$. This is the same vector as the Shapley-Shubik index of the weighted voting game $[51; 50, 49, 1]$. The core of the glove game is the single point $(1, 0, 0)$: if $x_2 > 0$, then the coalition $\{1, 3\}$ gets less than its worth 1. So the Shapley value is not in the core here. The value rewards the right gloves for their share in the orders, while the core lets the scarce left glove take everything.

**Non-example: equal split.** The rule $\psi_i(v) = v(N)/n$ is efficient, symmetric and additive, but it is not the Shapley value. In the three-player game above it gives $(2, 2, 2)$, and it pays a null player: add a fourth player who adds nothing, and the equal split gives that player $6/4$.

**Non-example: one marginal vector.** The marginal vector of one fixed order, for example $(0, 4, 2)$ for the order $1, 2, 3$, is efficient and additive, and in a convex game it is even in the core. It is not symmetric, so it is not the Shapley value.

**The Banzhaf value is a different average.** The Banzhaf value of $i$ is the plain mean of the $2^{n-1}$ marginal contributions $v(S \cup \{i\}) - v(S)$ over $S \subseteq N \setminus \{i\}$, with no weights. In the three-player game the sums of the marginal contributions are 12, 8 and 4, so the Banzhaf value is $(3, 2, 1)$, the same as the Shapley value. This is a property of the example: every dividend sits on a pair, and a pair's dividend is split in half by both rules. In general the Banzhaf value is not efficient; see the [Banzhaf power index](/banzhaf-index/).

## Related definitions

- **[Shapley-Shubik power index](/shapley-shubik-index/)**: the Shapley value of a simple game, the fraction of orders in which a player is the pivot.
- **[Banzhaf power index](/banzhaf-index/)**: the unweighted mean of the marginal contributions, on simple games.
- **[Owen's multilinear extension](/owen-multilinear-extension/)**: the Shapley value is the integral of its gradient along the diagonal of the cube, and the Banzhaf value is its gradient at the center.
- **[Core](/core-of-a-cooperative-game/)** and **[nucleolus](/nucleolus/)**: solution concepts based on the excesses of coalitions. The core can be empty and the nucleolus is always in the core when the core is nonempty; the Shapley value need not be in the core.
- **[Convex games](/convex-game/)**: the Shapley value is the center of gravity of the marginal vectors, which are the vertices of the core.
- **[Sobol indices](/sobol-indices/)**: the Shapley effects of sensitivity analysis are the Shapley value of a game whose worth is the variance that a set of inputs explains.
- **[Shapley network design game](/shapley-network-design-game/)**: a strategic game in which the cost of each edge is split by the Shapley value of a simple cost game, in equal shares among its users.

## References
