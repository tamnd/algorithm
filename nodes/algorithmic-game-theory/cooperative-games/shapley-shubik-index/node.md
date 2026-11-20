---
tag: CG9N02
kind: definition
slug: shapley-shubik-index
name: Shapley-Shubik power index
aliases:
- Shapley-Shubik index
area: algorithmic-game-theory/cooperative-games
level: core
summary: The Shapley value of a simple game, the fraction of orders in which a player is pivotal for turning a coalition into a winning one.
prereqs: [shapley-value, weighted-voting-game]
see_also: [banzhaf-index, power-index-dynamic-programming, power-index-hardness, shapley-uniqueness-theorem, shapley-value-sampling, owen-multilinear-extension, core-of-a-cooperative-game, apportionment-problem]
sources:
  - paper: doi:10.2307/1951053
    title: "Lloyd S. Shapley and Martin Shubik, A method for evaluating the distribution of power in a committee system, American Political Science Review 48(3) (1954), 787-792"
    locator: the index as the fraction of orders in which a member is pivotal, with examples from committees and the Security Council
  - paper: doi:10.1007/BF01780630
    title: "Pradeep Dubey, On the uniqueness of the Shapley value, International Journal of Game Theory 4(3) (1975), 131-139"
    locator: the characterization of the index on simple games by the transfer axiom
  - paper: doi:10.1515/9781400881970-018
    title: "Lloyd S. Shapley, A value for n-person games, in H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press, 1953, 307-317"
    locator: the value of a general TU game, of which the index is the special case of simple games
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 2, Basic concepts, and Chapter 4, Weighted voting games (power indices and their complexity)
  - paper: doi:10.3390/g9020029
    title: "Alexander Mayer, Luxembourg in the early days of the EEC: null player or not?, Games 9(2) (2018), article 29"
    locator: the power indices of the Council of the EEC from 1958
---

The Shapley-Shubik power index measures the voting power of each member of a body that decides by a yes or no vote. It is the [Shapley value](/shapley-value/) of the *simple game* of the body: let the members vote yes one at a time in a random order, and give the whole credit to the *pivot*, the member whose yes vote first makes the motion pass. The index of a member is the probability that it is the pivot. Shapley and Shubik (1954) proposed it for committees and legislatures. It differs from the [Banzhaf index](/banzhaf-index/), which counts coalitions instead of orders. For [weighted voting games](/weighted-voting-game/) it can be computed in pseudo-polynomial time by [dynamic programming](/power-index-dynamic-programming/), and it is #P-hard with binary weights ([hardness of power indices](/power-index-hardness/)).

## Definition

A *simple game* on $N = \{1, \ldots, n\}$ is a TU game $v$ with values in $\{0, 1\}$ that is monotone ($S \subseteq T$ implies $v(S) \le v(T)$), with $v(\emptyset) = 0$ and $v(N) = 1$. A coalition $S$ *wins* if $v(S) = 1$ and *loses* otherwise. The main example is a weighted voting game $[q; w_1, \ldots, w_n]$, where $S$ wins if $\sum_{i \in S} w_i \ge q$.

For an order $\pi$ of $N$, let $P_i^\pi$ be the set of the players before $i$. Player $i$ is the *pivot* of $\pi$ if $P_i^\pi$ loses and $P_i^\pi \cup \{i\}$ wins. Each order has exactly one pivot: along the order the coalition grows from $\emptyset$, which loses, to $N$, which wins, and by monotonicity it switches from losing to winning exactly once. The *Shapley-Shubik index* of player $i$ is

$$\varphi_i(v) = \frac{\text{the number of orders } \pi \text{ in which } i \text{ is the pivot}}{n!}.$$

Since the marginal contribution $v(P_i^\pi \cup \{i\}) - v(P_i^\pi)$ is 1 if $i$ is the pivot and 0 if not, this is the Shapley value of $v$. A set $S \subseteq N \setminus \{i\}$ for which $S$ loses and $S \cup \{i\}$ wins is a *swing* of $i$. The subset formula of the Shapley value gives

$$\varphi_i(v) = \sum_{S \text{ a swing of } i} \frac{|S|!\,(n - |S| - 1)!}{n!}.$$

The index has these properties: $\varphi_i(v) \ge 0$; $\sum_i \varphi_i(v) = 1$, since each order has one pivot; a dummy player (one with no swings) has index 0; symmetric players have equal indices; and in a weighted voting game, $w_i \ge w_j$ implies $\varphi_i \ge \varphi_j$, because each swing $S$ of $j$ gives a swing of $i$ of the same size: $S$ itself if $i \notin S$, and $(S \setminus \{i\}) \cup \{j\}$ if $i \in S$, and different swings of $j$ give different swings of $i$.

On simple games the sum of two games is not a simple game, so the additivity axiom of the [uniqueness theorem](/shapley-uniqueness-theorem/) is not available. Dubey (1975) showed that on simple games the index is the only solution with efficiency, symmetry, the null player property and the transfer axiom $\psi(v \vee w) + \psi(v \wedge w) = \psi(v) + \psi(w)$.

## Examples and non-examples

**The check game $[51; 50, 49, 1]$.** Players 1, 2 and 3 have the weights 50, 49 and 1. The six orders and their pivots are:

| order | weights after each arrival | pivot |
| --- | --- | --- |
| 1, 2, 3 | 50, 99 | 2 |
| 1, 3, 2 | 50, 51 | 3 |
| 2, 1, 3 | 49, 99 | 1 |
| 2, 3, 1 | 49, 50, 100 | 1 |
| 3, 1, 2 | 1, 51 | 1 |
| 3, 2, 1 | 1, 50, 100 | 1 |

Player 1 is the pivot in 4 orders and the others in 1 each, so the index is $(2/3, 1/6, 1/6)$. Players 2 and 3 have the same power although their weights are 49 and 1, because each of them forms a winning coalition with player 1 and with nobody else. The swings of player 1 are $\{2\}$, $\{3\}$ and $\{2, 3\}$, and the subset formula gives $\frac{1!\,1!}{3!} + \frac{1!\,1!}{3!} + \frac{2!\,0!}{3!} = \frac{1}{6} + \frac{1}{6} + \frac{1}{3} = \frac{2}{3}$.

**The Council of the EEC in 1958.** The game $[12; 4, 4, 4, 2, 2, 1]$ (France, Germany and Italy 4, Belgium and the Netherlands 2, Luxembourg 1) has the index $(7/30, 7/30, 7/30, 3/20, 3/20, 0)$. Luxembourg is a dummy: the other weights are all even, so no coalition of them has weight 11. Its index is 0 although it holds 1 of the 17 votes.

**The UN Security Council.** A motion needs the votes of all 5 permanent members and a fixed number of the others. With 6 other members and 7 votes needed, as in 1954, the game is $[37; 7, 7, 7, 7, 7, 1, 1, 1, 1, 1, 1]$, and each permanent member has the index $76/385 \approx 0.197$ and each other member $1/462 \approx 0.0022$. With the present 10 other members and 9 votes needed, the game is $[39; 7, 7, 7, 7, 7, 1, \ldots, 1]$, and the indices are $421/2145 \approx 0.196$ and $4/2145 \approx 0.0019$.

**Simple cases.** In a symmetric game, for example $[k; 1, \ldots, 1]$ for any $1 \le k \le n$, every player has $1/n$. A dictator has index 1 and all others 0.

**Non-example: the share of the weight.** The index is not $w_i / w(N)$. In the check game, player 2 holds 49% of the weight and has $1/6$ of the power. Weight shares are only a rough guide, and only in games with many small players.

**Non-example: the normalized Banzhaf index.** The normalized Banzhaf index of the check game is $(3/5, 1/5, 1/5)$, not $(2/3, 1/6, 1/6)$. The Banzhaf index counts every swing once, while the Shapley-Shubik index gives the swings of size $s$ the weight $s!\,(n-s-1)!/n!$, which favors very small and very large swings. The two indices often rank the players the same way, but their numbers differ.

## Related definitions

- **[Banzhaf power index](/banzhaf-index/)**: the number of swings of a player, divided by $2^{n-1}$ (raw) or by the total number of swings (normalized).
- **[Shapley value](/shapley-value/)**: the general form for TU games.
- **[Weighted voting game](/weighted-voting-game/)**: the usual input. Its [core](/core-of-a-cooperative-game/) is nonempty only if there is a veto player, while the index always exists.
- **[Owen's multilinear extension](/owen-multilinear-extension/)**: the index is the integral of the gradient of the extension along the diagonal.
- **Computation**: [dynamic programming](/power-index-dynamic-programming/) in $O(n^2 q)$ operations per player, [sampling](/shapley-value-sampling/) for large games, and [#P-hardness](/power-index-hardness/) for binary weights.

## References
