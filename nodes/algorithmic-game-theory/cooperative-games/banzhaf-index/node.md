---
tag: 88QF85
kind: definition
slug: banzhaf-index
name: Banzhaf power index
aliases:
- Penrose-Banzhaf index
- Banzhaf index
area: algorithmic-game-theory/cooperative-games
level: core
summary: The number of coalitions in which a player is a swing, divided by 2^(n-1) for the raw index or by the total number of swings of all players for the normalized index.
prereqs: [weighted-voting-game, shapley-value]
see_also: [shapley-shubik-index, power-index-dynamic-programming, power-index-hardness, owen-multilinear-extension, fourier-analysis-of-boolean-functions, shapley-uniqueness-theorem, marginal-contribution-nets, apportionment-problem]
sources:
  - paper: "John F. Banzhaf III, Weighted voting doesn't work: a mathematical analysis, Rutgers Law Review 19 (1965), 317-343"
    title: "John F. Banzhaf III, Weighted voting doesn't work: a mathematical analysis, Rutgers Law Review 19 (1965), 317-343"
    locator: the count of the coalitions in which a voter is decisive, and the weighted board of Nassau County with members who have no power
  - paper: doi:10.2307/2981392
    title: "L. S. Penrose, The elementary statistics of majority voting, Journal of the Royal Statistical Society 109(1) (1946), starting at page 53"
    locator: the probability that one vote decides the outcome, and the square root rule for the weights of delegates
  - paper: doi:10.1287/moor.4.2.99
    title: "Pradeep Dubey and Lloyd S. Shapley, Mathematical properties of the Banzhaf power index, Mathematics of Operations Research 4(2) (1979), 99-131"
    locator: the raw and normalized forms of the index, its axioms, and its comparison with the Shapley-Shubik index
  - paper: doi:10.1002/nav.3800220409
    title: "Guillermo Owen, Multilinear extensions and the Banzhaf value, Naval Research Logistics Quarterly 22(4) (1975), 741-750"
    locator: the Banzhaf value of a general TU game as the gradient of the multilinear extension at the center of the cube
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 2, Basic concepts (the Banzhaf index), and Chapter 4, Weighted voting games
---

The Banzhaf power index measures the voting power of a member of a body that decides by a yes or no vote. It counts the coalitions in which the member is a *swing*: the coalition loses without the member and wins with it. The *raw* index divides this count by $2^{n-1}$, the number of coalitions of the other members, and is the probability that the member decides the outcome when all the others vote at random. The *normalized* index divides the count by the total number of swings of all members, so that the indices sum to 1. Penrose (1946) defined the raw form, and Banzhaf (1965) found it again and used it in court cases on weighted voting; it is also called the Penrose-Banzhaf index. It differs from the [Shapley-Shubik index](/shapley-shubik-index/), which counts orders instead of coalitions.

## Definition

Let $v$ be a simple game on $N = \{1, \ldots, n\}$: a monotone TU game with values in $\{0, 1\}$, $v(\emptyset) = 0$ and $v(N) = 1$. A coalition $S$ wins if $v(S) = 1$. The usual input is a [weighted voting game](/weighted-voting-game/) $[q; w_1, \ldots, w_n]$, where $S$ wins if $\sum_{i \in S} w_i \ge q$.

A set $S \subseteq N \setminus \{i\}$ is a *swing* of player $i$ if $S$ loses and $S \cup \{i\}$ wins. Banzhaf states the same thing from the other side: $i$ is critical in the winning coalition $T = S \cup \{i\}$, since its departure turns $T$ into a losing coalition. Let $\eta_i(v)$ be the number of swings of $i$. Then:

- the **raw Banzhaf index** is $\beta'_i(v) = \dfrac{\eta_i(v)}{2^{n-1}}$;
- the **normalized Banzhaf index** is $\beta_i(v) = \dfrac{\eta_i(v)}{\sum_{j \in N} \eta_j(v)}$.

The denominator of the normalized index is positive: in every order of the players, the pivot of that order is a swing for the set before it, so some player has a swing.

The raw index has a probability meaning. Let each player other than $i$ vote yes with probability $1/2$, independently, and let $S$ be the set of yes votes. Each subset of $N \setminus \{i\}$ then has probability $2^{-(n-1)}$, so $\beta'_i(v)$ is the probability that the vote of $i$ decides the outcome. For a general TU game, the same average of the marginal contributions, $\frac{1}{2^{n-1}} \sum_{S \subseteq N \setminus \{i\}} (v(S \cup \{i\}) - v(S))$, is the *Banzhaf value*, and the raw index is its special case for simple games.

**Properties.** Both indices give 0 exactly to the dummies, give equal values to symmetric players, and in a weighted voting game respect the weights: $w_i \ge w_j$ implies $\eta_i \ge \eta_j$. The normalized indices sum to 1, while the raw indices sum to $\sum_i \eta_i / 2^{n-1}$, which is not 1 in general. The raw index has the transfer property $\beta'(v \vee w) + \beta'(v \wedge w) = \beta'(v) + \beta'(w)$; the normalized index does not, because the denominator changes from game to game. Dubey and Shapley (1979) characterize the raw index by symmetry, the null player property, the transfer property and the condition $\sum_i \beta'_i(v) = \sum_i \eta_i(v) / 2^{n-1}$, which takes the place of efficiency.

## Examples and non-examples

**The check game $[51; 50, 49, 1]$.** A coalition wins if it holds player 1 and at least one of players 2 and 3. The swings are:

| player | swings | count |
| --- | --- | --- |
| 1 | $\{2\}$, $\{3\}$, $\{2, 3\}$ | 3 |
| 2 | $\{1\}$ | 1 |
| 3 | $\{1\}$ | 1 |

With $n = 3$ there are $2^2 = 4$ coalitions of the other players. The raw index is $(3/4, 1/4, 1/4)$, which sums to $5/4$, and the normalized index is $(3/5, 1/5, 1/5)$. The [Shapley-Shubik index](/shapley-shubik-index/) of the same game is $(2/3, 1/6, 1/6)$.

**Nassau County.** Banzhaf's best-known example is a county board with the weights 9, 9, 7, 3, 1 and 1 and a majority of 16. Any two of the three large members win, since $9 + 9$, $9 + 7$ and $9 + 7$ are all at least 16. One large member with all three small ones has at most $9 + 5 = 14$. So the three small members are never swings: their indices are 0, although they hold 5 of the 30 votes. Each large member has 16 swings, the raw index $16/32 = 1/2$, and the normalized index $1/3$.

**The Council of the EEC in 1958.** In $[12; 4, 4, 4, 2, 2, 1]$ the swing counts are $(10, 10, 10, 6, 6, 0)$. The raw index is $(5/16, 5/16, 5/16, 3/16, 3/16, 0)$ and the normalized index is $(5/21, 5/21, 5/21, 1/7, 1/7, 0)$. The Shapley-Shubik index is $(7/30, 7/30, 7/30, 3/20, 3/20, 0)$: the large members get a little less under Shapley-Shubik ($7/30 \approx 0.233$ against $5/21 \approx 0.238$) and the middle members a little more.

**The UN Security Council in 1954.** In $[37; 7, 7, 7, 7, 7, 1, 1, 1, 1, 1, 1]$ a permanent member has 57 swings and another member 5. The normalized indices are $57/315 = 19/105 \approx 0.181$ and $5/315 = 1/63 \approx 0.016$, much less extreme than the Shapley-Shubik values $76/385 \approx 0.197$ and $1/462 \approx 0.0022$.

**Majority votes and the square root rule.** In a majority vote among an odd number $m$ of equal voters, a voter is a swing when the others split evenly, so $\beta' = \binom{m-1}{(m-1)/2} / 2^{m-1}$, which is close to $\sqrt{2/(\pi m)}$; for $m = 101$ both are about $0.0796$. A citizen's power in a large electorate thus falls as $1/\sqrt{m}$, not as $1/m$. Penrose (1946) drew the conclusion that, in a council of delegates who each vote as a bloc, the voting weights should be chosen so that the delegates' powers are proportional to the square roots of the populations they represent.

**Non-example: the raw index is not efficient.** In the check game the raw indices sum to $5/4$. Do not read them as shares of a whole. In the Nassau example they sum to $3/2$.

**Non-example: normalizing does not give the Shapley-Shubik index.** Both the normalized Banzhaf index and the Shapley-Shubik index sum to 1, but they weight the swings differently: Banzhaf counts each swing once, and Shapley-Shubik gives a swing of size $s$ the weight $s!\,(n-s-1)!/n!$.

## Related definitions

- **[Shapley-Shubik power index](/shapley-shubik-index/)**: the Shapley value of the simple game, an average over orders instead of coalitions.
- **[Owen's multilinear extension](/owen-multilinear-extension/)**: the raw index is the gradient of the extension at the center $(1/2, \ldots, 1/2)$ of the cube (Owen 1975).
- **Influence**: for a simple game seen as a monotone Boolean function, the raw index of $i$ is the influence of the variable $i$ in [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/), the probability that flipping $x_i$ changes the output on a uniform input.
- **Computation**: [dynamic programming](/power-index-dynamic-programming/) counts the swings of a player in $O(n q)$ operations for a weighted voting game with integer quota $q$, and with binary weights the problem is #P-complete ([hardness of power indices](/power-index-hardness/)). For a [marginal contribution net](/marginal-contribution-nets/), the Banzhaf value takes time linear in the size of the net.
- **[Shapley's uniqueness theorem](/shapley-uniqueness-theorem/)**: it shows why the Banzhaf value cannot be efficient on all TU games, since it is symmetric, additive and gives null players 0 but is not the Shapley value.

## References
