---
tag: 6R5NQC
kind: definition
slug: epsilon-nash-equilibrium
name: Epsilon-Nash equilibrium
aliases:
- approximate Nash equilibrium
- epsilon-equilibrium
area: algorithmic-game-theory/strategic-games
level: core
summary: A mixed profile in which no player can gain more than epsilon by a unilateral deviation; with payoffs in [0, 1] it is the target of most algorithms for Nash equilibria.
prereqs: [nash-equilibrium, mixed-strategy]
see_also: [lipton-markakis-mehta-algorithm, dmp-half-approximate-nash, rubinstein-approximate-nash-lower-bound, ppad-completeness-of-nash, nash-equilibrium-computation, correlated-equilibrium, no-regret-dynamics, bimatrix-game]
sources:
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (epsilon-Nash equilibrium) and Chapter 4 (computing approximate equilibria)
  - paper: "Richard J. Lipton, Evangelos Markakis and Aranyak Mehta, Playing large games using simple strategies, Proceedings of the 4th ACM Conference on Electronic Commerce (EC 2003), 36-41"
    title: Playing large games using simple strategies
    locator: the sampling argument and the quasi-polynomial algorithm for constant epsilon
  - paper: "Constantinos Daskalakis, Aranyak Mehta and Christos Papadimitriou, A note on approximate Nash equilibria, Theoretical Computer Science 410(17) (2009), 1581-1588"
    title: A note on approximate Nash equilibria
    locator: the simple 1/2-approximation for bimatrix games with payoffs in [0, 1]
  - paper: "Haralampos Tsaknakis and Paul G. Spirakis, An optimization approach for approximate Nash equilibria, Internet Mathematics 5(4) (2008), 365-382"
    title: An optimization approach for approximate Nash equilibria
    locator: the descent method that reaches a 0.3393-approximation
  - paper: doi:10.1145/3606697
    title: "Argyrios Deligkas, Michail Fasoulakis and Evangelos Markakis, A polynomial-time algorithm for 1/3-approximate Nash equilibria in bimatrix games, ACM Transactions on Algorithms 19(4) (2023); conference version ESA 2022"
    locator: the (1/3 + delta)-approximation in polynomial time, the best refereed bound for the additive notion as of 2026
  - paper: doi:10.1137/23M1549237
    title: "Argyrios Deligkas, Michail Fasoulakis and Evangelos Markakis, A polynomial-time algorithm for 1/2-well-supported Nash equilibria in bimatrix games, SIAM Journal on Computing (2023); arXiv 2207.07007"
    locator: the (1/2 + delta)-well-supported equilibrium in polynomial time
  - paper: "Aviad Rubinstein, Settling the complexity of computing approximate two-player Nash equilibria, Proceedings of the 57th IEEE Symposium on Foundations of Computer Science (FOCS 2016), 258-265"
    title: Settling the complexity of computing approximate two-player Nash equilibria
    locator: the quasi-polynomial lower bound for a constant epsilon under the exponential time hypothesis for PPAD
  - paper: doi:10.1145/1516512.1516516
    title: "Xi Chen, Xiaotie Deng and Shang-Hua Teng, Settling the complexity of computing two-player Nash equilibria, Journal of the ACM 56(3) (2009)"
    locator: PPAD-completeness for epsilon = 1/poly(n)
---

An $\varepsilon$-Nash equilibrium is a profile of [mixed strategies](/mixed-strategy/) in which no player can raise their payoff by more than $\varepsilon$ by changing their own strategy. It relaxes the [Nash equilibrium](/nash-equilibrium/), which is the case $\varepsilon = 0$, and it is what algorithms compute in practice: exact equilibria can be irrational in games with three or more players, and finding an exact equilibrium is PPAD-complete even for two players. The additive form below has meaning only for a fixed payoff scale, which here is $[0, 1]$.

## Definition

Let $G = (N, (S_i), (u_i))$ be a finite [normal-form game](/normal-form-game/) whose players maximize, with all payoffs in $[0, 1]$, and let $\varepsilon \ge 0$.

**Additive form.** A mixed profile $\sigma$ is an *$\varepsilon$-Nash equilibrium* if

$$u_i(\sigma) \ge u_i(s_i', \sigma_{-i}) - \varepsilon \quad \text{for every player } i \text{ and every } s_i' \in S_i.$$

Pure deviations are enough. By linearity, $u_i(\sigma_i', \sigma_{-i})$ is an average of the values $u_i(s_i', \sigma_{-i})$, so no mixed deviation gains more than the best pure one, and a mixed strategy is a best response if and only if its support lies inside the set of pure best responses. So $\sigma$ is an $\varepsilon$-Nash equilibrium if and only if the *largest gain* $\max_i \big(\max_{s_i'} u_i(s_i', \sigma_{-i}) - u_i(\sigma)\big)$ is at most $\varepsilon$, which takes $\sum_i |S_i|$ deviation payoffs to check.

**Well-supported form.** $\sigma$ is an *$\varepsilon$-well-supported Nash equilibrium* if every pure strategy in the support of every $\sigma_i$ is within $\varepsilon$ of a best response:

$$\sigma_i(s_i) > 0 \implies u_i(s_i, \sigma_{-i}) \ge \max_{s_i'} u_i(s_i', \sigma_{-i}) - \varepsilon.$$

Then $u_i(\sigma)$, an average of such values, is within $\varepsilon$ of the best response payoff, so an $\varepsilon$-well-supported equilibrium is an $\varepsilon$-Nash equilibrium. The converse fails, as the second example shows.

**Multiplicative form.** For positive payoffs, $\sigma$ is an $\varepsilon$-*relative* (multiplicative) equilibrium if $u_i(\sigma) \ge (1 - \varepsilon) \max_{s_i'} u_i(s_i', \sigma_{-i})$ for every $i$. It does not depend on the scale of the payoffs, but it is a different notion, and bounds for one form do not carry over to the other. Each result below says which form it uses; all of them use the additive form unless stated.

**Scale.** If every $u_i$ is multiplied by $c > 0$, an $\varepsilon$-Nash equilibrium becomes a $c\varepsilon$-Nash equilibrium. This is why the additive $\varepsilon$ needs the normalization: a game with payoffs in $[0, M]$ is first divided by $M$.

## Examples and non-examples

Each table lists the payoff of the row player first. All games here are scaled to $[0, 1]$.

**A near miss in matching pennies.** Let the row player win 1 if the coins match and 0 otherwise, and the column player the reverse. Let the row player be uniform and the column player play Heads with probability $1/2 + t$. The column player is indifferent, since the row player is uniform. The row player gets $1/2$, but Heads gets $1/2 + t$. So the profile is a $t$-Nash equilibrium and not a $t'$-Nash equilibrium for any $t' < t$; with $t = 1/10$ the largest gain is exactly $1/10$.

**An $\varepsilon$-equilibrium that is not well supported.** Take the [prisoner's dilemma](/prisoners-dilemma/) with payoffs divided by 5:

| | C | D |
| --- | --- | --- |
| C | 3/5, 3/5 | 0, 1 |
| D | 1, 0 | 1/5, 1/5 |

Let the column player defect and the row player cooperate with probability $p$. Against D, cooperation gets 0 and defection gets $1/5$, so the row player gets $(1 - p)/5$ and gains $p/5$ by defecting for sure. With $p = 1/20$ the profile is a $1/100$-Nash equilibrium. It is not a $1/100$-well-supported one, because C is in the support and is $1/5$ worse than the best response.

**The simple 1/2-approximation.** In a [bimatrix game](/bimatrix-game/) $(A, B)$ with entries in $[0, 1]$, pick any row $i$, let $j$ be a best column against row $i$, and let $k$ be a best row against column $j$. Let the row player mix rows $i$ and $k$ with probability $1/2$ each, and let the column player play $j$. The row player gets at least $A_{kj}/2$ and can get at most $A_{kj}$ against $j$, so the gain is at most $1/2$. The column player gets at least $B_{ij}/2$, and any column $j'$ gets $B_{ij'}/2 + B_{kj'}/2 \le B_{ij}/2 + 1/2$, so the gain is at most $1/2$. This is the [algorithm of Daskalakis, Mehta and Papadimitriou](/dmp-half-approximate-nash/); it reads one row and one column of the matrices. On the game with $A = \begin{pmatrix} 1 & 0 & 1/2 \\ 0 & 1 & 1/2 \\ 1/2 & 1/2 & 0 \end{pmatrix}$ and $B = \begin{pmatrix} 0 & 1 & 1/2 \\ 1 & 0 & 0 \\ 1/2 & 0 & 1 \end{pmatrix}$ and $i = 1$, the best column is $j = 2$ and the best row against it is $k = 2$; the row player mixes rows 1 and 2, and the largest gain is exactly $1/2$, so the bound is tight for this method.

**Non-example: close in payoff, far in strategy.** Let the row player have T with payoff $1 - \varepsilon$ and B with payoff 1, and let the column player have one strategy. T is an $\varepsilon$-Nash equilibrium, but the only Nash equilibrium plays B, at distance 1 in the probability of T. An $\varepsilon$-Nash equilibrium need not be near any exact one. Finding a profile that is near an exact equilibrium is a different and, for three or more players, harder problem (Etessami and Yannakakis 2010).

## Related definitions

- **Results for two players, additive form, payoffs in $[0, 1]$.** For every constant $\varepsilon > 0$, an $\varepsilon$-Nash equilibrium exists in which each player mixes uniformly over a multiset of $O(\log n/\varepsilon^2)$ pure strategies, where the game is $n \times n$, so trying all of them takes $n^{O(\log n/\varepsilon^2)}$ time ([Lipton-Markakis-Mehta algorithm](/lipton-markakis-mehta-algorithm/), 2003). Under the exponential time hypothesis for PPAD, quasi-polynomial time $n^{\log^{1 - o(1)} n}$ is necessary for some constant $\varepsilon$ ([Rubinstein 2016](/rubinstein-approximate-nash-lower-bound/)). For $\varepsilon = 1/\mathrm{poly}(n)$ the problem is PPAD-complete (Chen, Deng and Teng 2009; [PPAD-completeness of Nash](/ppad-completeness-of-nash/)).
- **Polynomial-time ratios.** The best $\varepsilon$ reached in polynomial time has gone from $1/2$ (Daskalakis, Mehta and Papadimitriou) to $0.3393$ (Tsaknakis and Spirakis 2008) and to $1/3 + \delta$ for every constant $\delta > 0$ (Deligkas, Fasoulakis and Markakis, ESA 2022 and ACM Transactions on Algorithms 2023). An arXiv preprint of Li and Li (arXiv 2610.05317, 4 October 2026, not refereed) claims about $0.30954 + \delta$. The smallest constant reachable in polynomial time is an open problem as of November 2026; by Rubinstein's result it cannot be every constant unless the exponential time hypothesis for PPAD fails.
- **Well-supported ratios.** For $\varepsilon$-well-supported equilibria the best polynomial-time ratio is $1/2 + \delta$ (Deligkas, Fasoulakis and Markakis, SIAM Journal on Computing 2023), and the best possible ratio is also open as of November 2026.
- **The hierarchy.** For $\varepsilon = 0$ the inclusions pure Nash $\subseteq$ mixed Nash $\subseteq$ correlated $\subseteq$ coarse correlated equilibria hold, and each is strict: matching pennies has no pure equilibrium; in chicken, with (D, D) = (0, 0), (D, C) = (7, 2), (C, D) = (2, 7) and (C, C) = (6, 6), the uniform distribution on (D, C), (C, D) and (C, C) is a correlated equilibrium and not a product distribution; in rock-paper-scissors the uniform distribution on the 6 profiles where the players differ is a coarse correlated equilibrium and not a correlated one. The same inclusions hold for each fixed $\varepsilon$, with the $\varepsilon$-relaxed versions of each set.
- **Approximate correlated equilibria.** The same relaxation applied to the inequalities of a [correlated](/correlated-equilibrium/) or [coarse correlated equilibrium](/coarse-correlated-equilibrium/) gives the sets that [no-regret dynamics](/no-regret-dynamics/) reach. Those are easy to compute; the approximate Nash equilibrium is not, as far as is known.
- **Pure $\varepsilon$-equilibria.** A pure profile in which no player gains more than $\varepsilon$; it may not exist, as in matching pennies with $\varepsilon < 1$.

## References
