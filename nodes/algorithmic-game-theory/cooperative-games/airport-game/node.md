---
tag: E48NA8
kind: model
slug: airport-game
name: Airport game
aliases:
- Littlechild-Owen airport problem
area: algorithmic-game-theory/cooperative-games
level: core
summary: A cost game in which planes need runways of different lengths. Its Shapley value splits each runway segment equally among those that use it.
prereqs: [transferable-utility-game, shapley-value]
see_also: [convex-game, shapley-convex-games-theorem, core-of-a-cooperative-game, nucleolus, cost-sharing-mechanism, minimum-cost-spanning-tree-game, bankruptcy-problem, shapley-network-design-game]
sources:
  - paper: doi:10.1287/mnsc.20.3.370
    title: "S. C. Littlechild and G. Owen, A simple expression for the Shapley value in a special case, Management Science 20(3) (1973), 370-372"
    locator: the cost game of the runway, and the Shapley value as the sum of the equal shares of the segments
  - paper: doi:10.2307/3003493
    title: "S. C. Littlechild and G. F. Thompson, Aircraft landing fees: a game theory approach, Bell Journal of Economics 8(1) (1977), starting at page 186"
    locator: landing fees at Birmingham airport computed by the Shapley value and the nucleolus of the airport game
  - paper: doi:10.1515/9781400881970-018
    title: "Lloyd S. Shapley, A value for n-person games, in H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press, 1953, 307-317"
    locator: the value and its additivity, which gives the segment formula
---

The airport game is a cost-sharing game. Several planes use one runway, and each plane needs a runway of a certain length. The runway must be long enough for the largest plane, and the question is how to split its cost. Littlechild and Owen (1973) showed that the [Shapley value](/shapley-value/) of this game has a simple form: cut the runway into segments at the lengths that the planes need, split the cost of each segment equally among the planes that use it, and add up the shares. The game is concave, so these shares are also in the [core](/core-of-a-cooperative-game/): no group of planes pays more than the runway it would need on its own.

## The machine

**Players.** $N = \{1, \ldots, n\}$. Each player is one plane, or one landing in the applied version. Player $i$ needs a runway that costs $c_i \ge 0$ to build. Number the players so that $0 \le c_1 \le c_2 \le \cdots \le c_n$, and set $c_0 = 0$.

**Costs.** The game is a cost game $(N, c)$ with

$$c(S) = \max_{i \in S} c_i \text{ for } S \ne \emptyset, \qquad c(\emptyset) = 0.$$

A runway that serves the coalition $S$ must serve its largest plane, and a runway for a large plane serves every smaller plane at no extra cost. The players minimize their cost shares. The standing assumptions are those of a TU cost game: the cost can be shared in any way, the full runway for $N$ is built, and each player pays a share $x_i$ with $\sum_i x_i = c(N) = c_n$.

**Segments.** The runway for $N$ splits into the segments $k = 1, \ldots, n$, where segment $k$ costs $c_k - c_{k-1}$ and is used by the players $k, k+1, \ldots, n$, the planes that need at least $c_k$. For $k = 1, \ldots, n$, let $g_k$ be the cost game with $g_k(S) = 1$ if $S$ contains a player of $\{k, \ldots, n\}$ and $g_k(S) = 0$ if not. Then

$$c = \sum_{k=1}^{n} (c_k - c_{k-1})\, g_k,$$

because for $S$ with largest player $m$, the games $g_1, \ldots, g_m$ give 1 and the others give 0, and the sum telescopes to $c_m$.

## What it counts

The model measures the cost share $x_i$ of each player, the landing fee. The usual targets are:

- **The Shapley value** $\varphi(c)$, the expected marginal cost of a player when the players arrive in a random order. A plane adds cost only when it is the largest one so far, and then it pays for the extension of the runway.
- **The core** of the cost game: the vectors with $\sum_{i \in N} x_i = c(N)$ and $\sum_{i \in S} x_i \le c(S)$ for every $S$. A share vector outside the core gives some group of planes a reason to build its own runway.
- **The nucleolus**, which Littlechild and Thompson (1977) computed next to the Shapley value for real fee data.

## Relation to other models

- **[TU games](/transferable-utility-game/).** The airport game is a TU game in cost form. All the inequalities of the core and the other solution concepts are reversed with respect to profit games.
- **[Convex games](/convex-game/).** The cost function is submodular: $c(S \cup T) + c(S \cap T) \le c(S) + c(T)$, since the maximum over $S \cup T$ is the maximum over $S$ or over $T$, and the maximum over $S \cap T$ is at most the other one. So the cost game is concave, and the profit game $v(S) = \sum_{i \in S} c_i - c(S)$ of the savings is convex.
- **Tree cost games.** If the planes sit at the nodes of a rooted tree and a coalition pays for the edges on the paths from the root to its members, the same argument splits each edge equally among the players below it. The airport game is the case where the tree is a path. The [minimum cost spanning tree game](/minimum-cost-spanning-tree-game/) is a related cost game in which the network is not fixed in advance.
- **[Shapley network design game](/shapley-network-design-game/).** There the cost of each edge is split equally among its users, which is the Shapley value of the game $g_k$ for one edge, but the users choose their paths strategically.
- **[Bankruptcy problems](/bankruptcy-problem/)** have the same kind of input, a list of numbers sorted by size, but they divide a fixed amount among claims instead of a cost among needs.

## Known results in the model

**Theorem (Littlechild and Owen 1973).** With $c_1 \le \cdots \le c_n$ and $c_0 = 0$, the Shapley value of the airport game is

$$\varphi_i(c) = \sum_{k=1}^{i} \frac{c_k - c_{k-1}}{n - k + 1}.$$

*Proof.* In the game $g_k$, the players $1, \ldots, k-1$ are null, and the players $k, \ldots, n$ are symmetric. Efficiency gives each of the $n - k + 1$ users the share $1/(n-k+1)$ of $g_k(N) = 1$, so $\varphi_i(g_k) = 1/(n-k+1)$ if $i \ge k$ and 0 if not. The Shapley value is linear ([uniqueness theorem](/shapley-uniqueness-theorem/)), and $c = \sum_k (c_k - c_{k-1})\, g_k$, so $\varphi_i(c) = \sum_{k \le i} (c_k - c_{k-1})/(n-k+1)$. $\square$

**Example.** Three planes need runways that cost $c = (1, 3, 6)$. Segment 1 costs 1 and has 3 users, segment 2 costs 2 and has 2 users, segment 3 costs 3 and has 1 user. So

$$\varphi = \left(\tfrac{1}{3},\ \tfrac{1}{3} + 1,\ \tfrac{1}{3} + 1 + 3\right) = \left(\tfrac{1}{3}, \tfrac{4}{3}, \tfrac{13}{3}\right),$$

which sums to $c(N) = 6$. The same numbers come from the six orders: the largest plane always pays for the segments that no earlier plane needed. All six core inequalities hold: $\tfrac{1}{3} \le 1$, $\tfrac{4}{3} \le 3$, $\tfrac{13}{3} \le 6$, $\tfrac{5}{3} \le 3$, $\tfrac{14}{3} \le 6$ and $\tfrac{17}{3} \le 6$. Equal division $(2, 2, 2)$ is not in the core, since player 1 would pay 2 for a runway it could build for 1.

**The Shapley value is in the core.** The cost game is concave, so by [Shapley's theorem on convex games](/shapley-convex-games-theorem/), applied to the convex savings game, the core is nonempty and contains the Shapley value. A direct proof: let $m$ be the largest player of $S$. Then $\sum_{i \in S} \varphi_i = \sum_{k} (c_k - c_{k-1})\, |S \cap \{k, \ldots, n\}| / (n-k+1)$. The terms with $k > m$ are 0, and for $k \le m$ the fraction is at most 1, so the sum is at most $\sum_{k \le m} (c_k - c_{k-1}) = c_m = c(S)$.

**Computation.** Sort the costs in $O(n \log n)$ time, then compute all shares with one prefix sum in $O(n)$ time. If many players share each cost level, as with the landings of one aircraft type, only the levels and the counts of players per level are needed. Littlechild and Thompson (1977) used this to compute fees for the landings at Birmingham airport by the Shapley value and by the nucleolus.

**Monotone shares.** A larger plane never pays less: $\varphi_{i+1} - \varphi_i = (c_{i+1} - c_i)/(n - i) \ge 0$. Planes with equal needs pay equal shares, and the smallest plane pays only its share of the first segment.

## References
