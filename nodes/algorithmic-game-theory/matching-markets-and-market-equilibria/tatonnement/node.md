---
tag: ZA6PKF
kind: algorithm
slug: tatonnement
name: Tatonnement
aliases:
- Walrasian tatonnement
- Walrasian auctioneer
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Raises the prices of goods in excess demand and lowers the others. In continuous time it converges under gross substitutes; discrete versions also need small enough steps.
model: real-ram
complexity:
  vars: {n: the number of buyers, m: the number of goods, T: the number of rounds}
  time: {worst: O(T n m)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1874
  people: [Leon Walras, Kenneth Arrow, Leonid Hurwicz, H. D. Block, Herbert Scarf]
  note: Walras described the groping of prices in 1874. Arrow, Block and Hurwicz (1959) proved global stability of the continuous process under gross substitutes, and Scarf (1960) gave markets where it cycles.
prereqs: [competitive-equilibrium, fisher-market]
see_also: [arrow-debreu-market, proportional-response-dynamics, gross-substitutes, kelso-crawford-process, demange-gale-sotomayor-auction, gradient-descent, euler-method, lyapunov-function]
sources:
  - book: "Leon Walras, Elements d'economie politique pure, Corbaz, Lausanne, 1874"
    locator: the theory of exchange (the groping, or tatonnement, by which prices of goods in excess demand rise and the others fall)
  - paper: doi:10.2307/1907515
    title: "Kenneth J. Arrow and Leonid Hurwicz, On the stability of the competitive equilibrium, I, Econometrica 26(4), 522-552 (1958)"
    locator: the whole paper (local and global stability of the continuous process, gross substitutes)
  - paper: doi:10.2307/1907779
    title: "Kenneth J. Arrow, H. D. Block and Leonid Hurwicz, On the stability of the competitive equilibrium, II, Econometrica 27(1), 82-109 (1959)"
    locator: the whole paper (global stability of continuous tatonnement for any number of goods under gross substitutes)
  - paper: doi:10.2307/2556215
    title: "Herbert Scarf, Some examples of global instability of the competitive equilibrium, International Economic Review 1(3), 157-172 (1960)"
    locator: the whole paper (exchange economies with complementary goods in which the continuous process cycles)
  - paper: doi:10.1145/1060590.1060601
    title: "Bruno Codenotti, Benton McCune and Kasturi Varadarajan, Market equilibrium via the excess demand function, Proceedings of the 37th ACM Symposium on Theory of Computing (STOC 2005), 74-83"
    locator: the whole paper (a discrete tatonnement that reaches an approximate equilibrium in polynomial time under weak gross substitutes)
  - paper: doi:10.1145/1374376.1374422
    title: "Richard Cole and Lisa Fleischer, Fast-converging tatonnement algorithms for one-time and ongoing market problems, Proceedings of the 40th ACM Symposium on Theory of Computing (STOC 2008)"
    locator: the whole paper (multiplicative price updates and their rate of convergence)
  - paper: doi:10.1016/j.geb.2019.03.014
    title: "Yun Kuen Cheung, Richard Cole and Nikhil R. Devanur, Tatonnement beyond gross substitutes? Gradient descent to the rescue, Games and Economic Behavior 123 (2020)"
    locator: the whole paper (tatonnement in Fisher markets as gradient descent on a convex function)
---

Tatonnement, French for groping, is the oldest algorithm for finding market prices. An imaginary auctioneer calls out prices, asks every agent what she would buy, and then raises the price of each good that is wanted more than it is supplied and lowers the price of each good that is left over. No trade happens until the prices balance. Walras (1874) used the process to argue that markets find their [competitive equilibrium](/competitive-equilibrium/), and it is the model behind most later price-adjustment algorithms. Its rest points are exactly the equilibria, but it does not always reach them. Arrow, Block and Hurwicz (1959) proved that the continuous-time process converges when goods are gross substitutes, and Scarf (1960) built a market in which it cycles forever. Discrete versions, the ones a computer runs, also need step sizes small enough for the market at hand.

## In plain words

The auctioneer starts with some prices. Each person says how much of each good she wants at these prices. If people want more of a good than there is, its price goes up a bit. If some of it is left over, its price goes down a bit. Then everyone answers again. When every good is used up exactly, the prices are right and trade starts. This works well when goods can replace each other, like tea and coffee: when tea becomes expensive, people buy more coffee. It can fail when goods are used together, like left and right shoes. Then the prices can go round in circles. Steps that are too large can also make prices jump past the right value again and again.

## The problem

There are $m$ divisible goods with supplies $s_j > 0$. The market is given by its *excess demand* $z(p) \in \mathbb{R}^m$: at positive prices $p$, $z_j(p)$ is the total demand for good $j$ minus $s_j$. The algorithm uses $z$ as a black box, one call per round. The usual assumptions are those of a market with locally nonsatiated agents and well-defined demand:

- $z$ is continuous on positive prices and $z_j(p) \ge -s_j$ (demand is never negative);
- $z(\lambda p) = z(p)$ for $\lambda > 0$ (only relative prices matter);
- Walras' law: $p \cdot z(p) = 0$ (every agent spends all her money).

The task is to find $p > 0$ with $z(p) = 0$, or an approximate equilibrium with $|z_j(p)| \le \varepsilon s_j$ for every $j$. In a [Fisher market](/fisher-market/) with $n$ buyers, the demand of each buyer is computed from her budget and utility at $p$, so a round costs $O(nm)$ time for the usual utility classes.

The demand is *gross substitutes* (for divisible goods) if raising the price of one good never lowers the demand for any other good; *strict* gross substitutes asks that it strictly raises it. CES utilities $(\sum_j a_{ij} x_j^\rho)^{1/\rho}$ with $0 < \rho < 1$ give gross substitutes, and Cobb-Douglas utilities ($\rho \to 0$) are the borderline case. The [gross substitutes](/gross-substitutes/) page treats the version of this condition for indivisible items.

## The algorithm

```pseudo id=main
TATONNEMENT(excess demand z, supplies s, start p0 > 0, step λ ∈ (0, 1), rounds T, tolerance ε)
L1  p ← p0
L2  for t = 0, 1, ..., T - 1 do
L3      z ← z(p)
L4      if |z_j| / s_j ≤ ε for every good j then return (p, t, converged)
L5      p_j ← p_j · (1 + λ · min(z_j / s_j, 1)) for every good j
L6  return (p, T, whether |z_j(p)| / s_j ≤ ε for every j)
```

Line L5 is a multiplicative rule of the kind studied by Cole and Fleischer (2008). The relative excess demand is capped at $1$, so one round at most multiplies a price by $1 + \lambda$. Since $z_j / s_j \ge -1$, the factor is at least $1 - \lambda > 0$, so prices stay positive. The classical *additive* rule $p \leftarrow p + \lambda z(p)$ is the [Euler method](/euler-method/) for the differential equation $\dot{p} = z(p)$, the continuous tatonnement of Arrow and Hurwicz. The implementation has both rules, in floating point, and excess demand functions for Cobb-Douglas, CES and linear Fisher markets and for Scarf's economy.

## Example

Take the Fisher check value: budgets $1$ and $1$, one unit of each of two goods, linear utilities $u_1 = (2, 1)$ and $u_2 = (1, 2)$. The equilibrium prices are $(1, 1)$. As long as $p_2 / p_1$ lies strictly between $1/2$ and $2$, buyer 1 spends her budget on good 1 and buyer 2 on good 2, so $z_j = 1/p_j - 1$. With $\lambda = 1/2$ and $p_j \ge 1/2$, line L5 gives $p_j \leftarrow p_j + (1 - p_j)/2$, which halves the distance to $1$. From $p^0 = (0.8, 1.4)$, $p^t = (1 - 0.2 / 2^t, \; 1 + 0.4 / 2^t)$.

| $t$ | $p$ | $z$ |
|---|---|---|
| 0 | $(0.8, 1.4)$ | $(0.25, -0.2857)$ |
| 1 | $(0.9, 1.2)$ | $(0.1111, -0.1667)$ |
| 2 | $(0.95, 1.1)$ | $(0.0526, -0.0909)$ |
| 3 | $(0.975, 1.05)$ | $(0.0256, -0.0476)$ |

With $\varepsilon = 10^{-9}$, line L4 stops after 29 updates. Note that the linear demand is not a function where a buyer is indifferent, for example at $p = (2, 1)$; the implementation raises an error there, and tatonnement as defined here needs a demand function.

*Scarf's economy.* Three agents and three goods; agent $j$ owns one unit of good $j$ and wants goods $j$ and $j + 1$ (indices mod 3) in equal amounts, a Leontief utility. The equilibrium prices are the multiples of $(1, 1, 1)$. Along the continuous process both $\sum_j p_j^2$ and $\prod_j p_j$ stay constant, so from $(1.2, 1.0, 0.8)$ the prices circle the equilibrium forever. The additive rule with $\lambda = 0.1$ is worse: $\sum_j p_j^2$ grows from $3.08$ to about $3.097$ after 100 rounds and $3.528$ after 1000, and prices turn negative after about $10^4$ rounds.

## Correctness

The proof is in `proofs/correctness.md`. It shows:

1. With $0 < \lambda < 1$, prices stay positive, and a price vector is a rest point of line L5 if and only if it is an equilibrium. When line L4 returns, $p$ is an $\varepsilon$-approximate equilibrium.
2. In a Fisher market with Cobb-Douglas utilities, $z_j = c_j / p_j - 1$ with $c_j$ the money spent on good $j$, and once $p_j \ge c_j / 2$ line L5 shrinks $p_j - c_j$ by the factor $1 - \lambda$ each round. The prices converge to the equilibrium $c$ at a geometric rate.
3. The continuous process $\dot{p} = z(p)$ converges to the equilibrium ray under strict gross substitutes (Arrow, Block and Hurwicz 1959). The proof uses the [Lyapunov function](/lyapunov-function/) $\max_j p_j / p^*_j$: the goods with the highest ratio to the equilibrium prices have negative excess demand, so their prices fall.
4. In Scarf's economy, Walras' law gives $\frac{d}{dt} \sum_j p_j^2 = 2 p \cdot z = 0$, and $\sum_j z_j / p_j = 0$ gives $\frac{d}{dt} \sum_j \log p_j = 0$. The orbit from a point off the equilibrium ray never reaches it, and the additive rule increases $\sum_j p_j^2$ by $\lambda^2 \|z\|^2$ in every round.

## Complexity

A round costs one evaluation of $z$ plus $O(m)$ time; in a Fisher market with linear, CES or Cobb-Douglas utilities an evaluation takes $O(nm)$, so $T$ rounds take $O(Tnm)$ time and $O(m)$ extra space. The number of rounds is the hard part. In the Cobb-Douglas case it is $O(\log(1/\varepsilon) / \lambda)$ once prices are within a factor 2 of equilibrium. Codenotti, McCune and Varadarajan (2005) proved that a discrete tatonnement reaches an approximate equilibrium in polynomial time for markets with weak gross substitutes, and Cole and Fleischer (2008) bounded the rate of convergence of multiplicative updates for several classes of markets. Without gross substitutes there is no bound in general: the process may cycle.

## Properties

- **Local information.** Each price moves only according to the excess demand of its own good. No agent reports her utility; the auctioneer only asks for demands.
- **Rest points are equilibria.** With positive prices, $p$ is fixed by line L5 exactly when $z(p) = 0$.
- **Scale invariant.** Since $z$ is homogeneous of degree $0$, multiplying $p^0$ by a constant multiplies every iterate by it.
- **Not monotone.** Unlike the [DGS auction](/demange-gale-sotomayor-auction/), prices can go up and down.
- **Float arithmetic.** The output is approximate. To get an exact equilibrium of a linear market, use a combinatorial method such as the [DPSV algorithm](/dpsv-algorithm/).

## Variants and improvements

- **Continuous time.** $\dot{p}_j = z_j(p)$, or $\dot{p}_j = h_j(z_j(p))$ for sign-preserving functions $h_j$. Arrow and Hurwicz (1958) and Arrow, Block and Hurwicz (1959) proved global stability under gross substitutes.
- **Gradient view.** For Fisher markets, Cheung, Cole and Devanur (2020) showed that a multiplicative tatonnement is a generalized [gradient descent](/gradient-descent/) on a convex function of the prices. This gives convergence for some markets beyond gross substitutes. [Proportional response dynamics](/proportional-response-dynamics/) is a related method that updates bids instead of prices, as mirror descent on a convex program.
- **Ascending auctions.** With indivisible items and money, the [Kelso-Crawford process](/kelso-crawford-process/) and the [DGS auction](/demange-gale-sotomayor-auction/) only raise prices, in discrete steps, and stop at an exact Walrasian equilibrium.
- **Global methods.** For markets without gross substitutes, the [Scarf algorithm](/scarf-algorithm/) finds approximate equilibria by simplicial path following, at the cost of an exponential worst case.

## When to use it

Use it as a model of how prices react in a decentralized market, and as an algorithm when the demand has gross substitutes and only demand queries are available, for example in a simulation where agents are black boxes. For exact equilibria of linear Fisher markets use the [Eisenberg-Gale program](/eisenberg-gale-program/) or a combinatorial algorithm. For markets with complements, use a method with a convergence guarantee for that class, or expect cycles.

## Pitfalls

- A step $\lambda$ that is too large in line L5 makes prices overshoot. In the tests, CES Fisher markets with $\rho = 3/4$ converge with $\lambda = 0.2$, but one of them fails to converge in 5000 rounds with $\lambda = 1/2$. Gross substitutes alone does not make every discrete step size work.
- Without the cap $\min(z_j / s_j, 1)$ in line L5, a good with huge excess demand at a tiny price gets a huge jump, and the next round may overshoot by a large factor.
- The additive rule $p \leftarrow p + \lambda z$ can make prices negative. In Scarf's economy it does so after enough rounds, and even before that it spirals outward.
- The stopping test in line L4 must be relative to the supplies $s_j$. An absolute test on $z_j$ means different things for goods with supplies of very different size.
- Line L3 needs a demand function. With linear utilities the demand is a set at prices where a buyer is indifferent, and these are exactly the equilibrium prices of many markets; the excess demand there must be chosen, and a naive choice can make the prices jump around the equilibrium.

## Implementations

## History

Walras (1874) described the groping of prices by which a market finds its equilibrium, with no trade before prices balance. Arrow and Hurwicz (1958) and Arrow, Block and Hurwicz (1959) studied the process as a differential equation and proved that it is globally stable when goods are gross substitutes. Scarf (1960) showed with an economy with complementary goods that the process can cycle forever, so no general stability theorem holds. Computer science returned to tatonnement as a distributed algorithm: Codenotti, McCune and Varadarajan (2005) proved polynomial-time convergence to approximate equilibria for weak gross substitutes, Cole and Fleischer (2008) studied fast multiplicative updates and ongoing markets, and Cheung, Cole and Devanur (2020) explained tatonnement in Fisher markets as gradient descent.

## References
