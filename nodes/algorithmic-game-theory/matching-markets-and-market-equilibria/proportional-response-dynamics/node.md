---
tag: M8R35N
kind: algorithm
slug: proportional-response-dynamics
name: Proportional response dynamics
aliases:
- proportional response
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: Each buyer splits its budget in proportion to the utility each good gave it last round. It converges to the Fisher market equilibrium.
model: real-ram
complexity:
  vars: {n: the number of buyers, m: the number of goods, T: the number of rounds}
  time: {worst: "O(T n m)"}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2007
  people: [Fang Wu, Li Zhang]
  note: Wu and Zhang introduced the dynamics as a model of tit-for-tat bandwidth trading in peer-to-peer networks. Birnbaum, Devanur and Xiao showed in 2011 that it is mirror descent on a convex program of Shmyrev.
prereqs: [fisher-market, mirror-descent]
see_also: [eisenberg-gale-program, kullback-leibler-divergence, bregman-divergence, tatonnement, dpsv-algorithm, orlin-fisher-market-algorithm, multiplicative-weights-update, proportional-fairness]
sources:
  - paper: doi:10.1145/1250790.1250844
    title: "Fang Wu and Li Zhang, Proportional response dynamics leads to market equilibrium, STOC 2007, 354-363"
    locator: the whole paper (the dynamics and its convergence in an exchange model of bandwidth trading)
  - paper: doi:10.1016/j.tcs.2010.06.021
    title: "Li Zhang, Proportional response dynamics in the Fisher market, Theoretical Computer Science 412(24), 2691-2698 (2011)"
    locator: the whole paper (convergence in Fisher markets with CES utilities)
  - paper: doi:10.1145/1993574.1993594
    title: "Benjamin Birnbaum, Nikhil R. Devanur and Lin Xiao, Distributed algorithms via gradient descent for Fisher markets, EC 2011, 127-136"
    locator: "Section 2.1 (Shmyrev's convex program, Theorem 1), Section 2.2 and Theorem 3 (the rate of generalized gradient descent), Theorem 6 and Lemma 7 (proportional response is gradient descent with the KL divergence)"
---

Proportional response dynamics is a simple, distributed way to reach the equilibrium of a linear [Fisher market](/fisher-market/). In every round, each buyer bids money on goods, each good's price is the total money bid on it, and each buyer gets a share of the good equal to her share of the bids. Then every buyer splits her budget again, in proportion to the utility that each good gave her in the round that just ended. No buyer solves an optimization problem, there is no step size, and every good is sold in every round. Birnbaum, Devanur and Xiao showed that one round is exactly one step of [mirror descent](/mirror-descent/) with the [Kullback-Leibler divergence](/kullback-leibler-divergence/) on a convex potential of Shmyrev, and from this the potential gap is at most $\mathrm{KL}(b^* \| b^0) / T$ after $T$ rounds.

## In plain words

Every buyer has a budget and spreads it as bids over the goods she likes. A good costs whatever money was bid on it, and each bidder gets a piece of it in proportion to her bid. A buyer then looks at what each good gave her: if one good gave her half of her total pleasure, she puts half of her budget on it in the next round. Goods that pay off well get more money, and goods that pay off badly get less. Prices rise on goods that many buyers like and fall on the others. Round after round, the bids settle at the market equilibrium, where every buyer spends only on her best goods.

## The problem

There are $n$ buyers and $m$ goods, with one unit of each good. Buyer $i$ has a budget $e_i > 0$ and utility $u_{ij} \ge 0$ for all of good $j$, linear in the amount. Every buyer likes some good and every good is liked by some buyer. A bid matrix $b$ has $b_{ij} \ge 0$, $b_{ij} = 0$ when $u_{ij} = 0$, and $\sum_j b_{ij} = e_i$ for each buyer. Find bids whose prices $p_j = \sum_i b_{ij}$ are the equilibrium prices: with the allocation $x_{ij} = b_{ij} / p_j$, every buyer spends only on goods of maximum bang per buck $u_{ij} / p_j$.

## The algorithm

```pseudo id=main
PROPORTIONAL-RESPONSE(utilities u, budgets e, rounds T)
L1  b_ij ← e_i / (the number of goods that i likes) for every good j with u_ij > 0, else 0
L2  for t ← 1 to T do
L3      p_j ← Σ_i b_ij for every good j
L4      x_ij ← b_ij / p_j for every buyer i and good j
L5      v_i ← Σ_j u_ij x_ij for every buyer i
L6      b_ij ← e_i u_ij x_ij / v_i for every buyer i and good j
L7  return the bids of all rounds
```

Line L3 clears the market: the price of a good is the money on it. Line L4 shares each good in proportion to the bids, so every good is fully allocated. Line L5 is the utility of each buyer, and line L6 splits her budget in proportion to the parts $u_{ij} x_{ij}$ of that utility. The new bids again add up to $e_i$. A bid that is positive stays positive, so any start with positive bids on all liked goods works; line L1 is only one choice.

The Shmyrev potential of a bid matrix is
$$
\Phi(b) = \sum_j p_j \log p_j - \sum_{i, j} b_{ij} \log u_{ij}, \qquad p_j = \sum_i b_{ij},
$$
where the second sum is over the pairs with $u_{ij} > 0$. It is convex, and its minimizers are exactly the equilibrium bids. Its gradient is $\partial \Phi / \partial b_{ij} = \log p_j + 1 - \log u_{ij}$, and line L6 equals $b^{t+1}_{ij} \propto b^t_{ij} \exp(-\partial \Phi / \partial b_{ij})$, scaled to the budget of buyer $i$. This is mirror descent with step $1$ and the KL divergence, which is the [multiplicative weights](/multiplicative-weights-update/) form of gradient descent.

## Example

Two buyers and two goods, $u_1 = (1, 1)$, $u_2 = (1, 3)$, budgets $e = (1, 2)$. At the equilibrium the prices are $(1, 2)$: buyer 1 has bang per buck $(1, 1/2)$ and spends her $1$ on good 1, and buyer 2 has bang per buck $(1, 3/2)$ and spends her $2$ on good 2. The minimum of $\Phi$ is $2 \log 2 - 2 \log 3 \approx -0.8109$.

| round $t$ | prices $p$ | bids of buyer 1 | bids of buyer 2 | $\Phi(b^t)$ |
|---|---|---|---|---|
| 0 | $(1.5, 1.5)$ | $(0.5, 0.5)$ | $(1, 1)$ | $0.1178$ |
| 1 | $(1, 2)$ | $(0.5, 0.5)$ | $(0.5, 1.5)$ | $-0.2616$ |
| 2 | $(1.0303, 1.9697)$ | $(0.6667, 0.3333)$ | $(0.3636, 1.6364)$ | $-0.4318$ |
| 3 | $(1.0408, 1.9592)$ | $(0.7927, 0.2073)$ | $(0.2481, 1.7519)$ | $-0.5654$ |
| 5 | $(1.0368, 1.9632)$ | $(0.9312, 0.0688)$ | $(0.1056, 1.8944)$ | $-0.7195$ |
| 10 | $(1.0094, 1.9906)$ | $(0.9972, 0.0028)$ | $(0.0122, 1.9878)$ | $-0.8040$ |
| 20 | $(1.0002, 1.9998)$ | $(1.0000, 0.0000)$ | $(0.0002, 1.9998)$ | $-0.8109$ |

In round 0, buyer 1 gets $1/3$ of each good and utility $2/3$, half of it from each good, so she keeps her split. Buyer 2 gets $2/3$ of each good, with utility $2/3$ from good 1 and $2$ from good 2, so she moves to the split $(0.5, 1.5)$. In round 1 the prices are already $(1, 2)$, but the bids are not an equilibrium, because both buyers still bid on a good that is not their best. The prices then move away and come back as the bids concentrate. $\Phi$ goes down in every round.

For the market $u_1 = (2, 1)$, $u_2 = (1, 2)$ with budgets $(1, 1)$, the prices stay at $(1, 1)$ and buyer 1 bids exactly $2^t / (2^t + 1)$ on good 1 in round $t$.

## Correctness

The proof is in `proofs/correctness.md`. The minimizers of $\Phi$ over the bid matrices are the equilibrium bids, by the optimality conditions. Line L6 is the mirror descent step, and $\Phi$ is smooth relative to the KL divergence with constant $1$: the gap $\Phi(a) - \Phi(b) - \nabla \Phi(b) \cdot (a - b)$ is the KL divergence of the price vectors, which is at most the KL divergence of the bids by the log sum inequality. With the three-point identity of the KL divergence, this gives that $\Phi$ never goes up, that $\mathrm{KL}(b^* \| b^t)$ never goes up, and that $\Phi(b^T) - \Phi(b^*) \le \mathrm{KL}(b^* \| b^0) / T$. So the prices converge to the unique equilibrium prices and the bids converge to equilibrium bids.

## Complexity

One round of lines L3 to L6 takes $O(nm)$ time and $O(nm)$ space, so $T$ rounds take $O(Tnm)$ time; only the pairs with $u_{ij} > 0$ matter, so a sparse market costs time linear in the number of such pairs. The number of rounds for a gap of $\varepsilon$ in $\Phi$ is at most $\mathrm{KL}(b^* \| b^0) / \varepsilon$. From the even split of line L1, $\mathrm{KL}(b^* \| b^0) \le \sum_i e_i \log m$. The bound is on the potential, not on the distance to the equilibrium prices, and the prices can approach slowly when a buyer is indifferent at the equilibrium between a good she buys and one she must not buy.

## Properties

- **Distributed.** Each buyer needs only her own utilities and what she received in the last round. Each good needs only the bids on it.
- **No step size and no state.** The next bids depend only on the current bids, and the step of the mirror descent is fixed at $1$.
- **Market clearing in every round.** Every good is sold at the sum of its bids, and every buyer spends her whole budget.
- **Monotone potential.** $\Phi(b^t)$ never goes up, and neither does $\mathrm{KL}(b^* \| b^t)$ for any equilibrium bids $b^*$, which works as a [Lyapunov function](/lyapunov-function/).
- **Rate $1/T$ for linear utilities.** In the market $u_1 = (2, 1)$, $u_2 = (1, 2)$ with budgets $(2, 1)$, the equilibrium prices are $(2, 1)$ and buyer 1 is indifferent between the goods there. The price of good 1 is about $1.9932$ after 100 rounds and $1.9993$ after 1000 rounds, so the error falls only roughly like $1/T$.

## Variants and improvements

- **CES utilities.** Zhang proved convergence in Fisher markets with constant elasticity of substitution utilities, with a fast rate for strictly concave ones.
- **Spending constraint utilities.** Birnbaum, Devanur and Xiao extended both the convex program and the dynamics to spending constraint utilities.
- **Exchange markets.** The original setting of Wu and Zhang is an exchange of bandwidth between peers, where every agent also sells; proportional response is a tit-for-tat rule there.
- **Exact methods.** The [DPSV algorithm](/dpsv-algorithm/) and [Orlin's algorithm](/orlin-fisher-market-algorithm/) compute the equilibrium exactly, and the [Eisenberg-Gale program](/eisenberg-gale-program/) gives it as a convex program in the allocation.
- **Price dynamics.** [Tatonnement](/tatonnement/) moves prices by excess demand instead of moving bids; for linear utilities the demand is not unique, which makes it harder to analyze.

## When to use it

Use it when the buyers are automated agents that update their own bids, such as budgets in ad auctions or bandwidth in a peer-to-peer network, and no central party can solve the market. It is also a very short way to get approximate equilibrium prices of a large linear Fisher market. When exact prices are needed, use an exact combinatorial algorithm or round the result of the dynamics and check it.

## Pitfalls

- Starting line L1 with a zero bid on a good that the buyer likes is a trap: line L6 keeps the bid at zero forever, so the dynamics can converge to the wrong point when the equilibrium needs that bid.
- Dividing by $p_j$ in line L4 for a good that no buyer bids on fails; with positive starting bids on every liked good this cannot happen, because every good is liked by some buyer.
- Dividing in line L6 by anything other than the utility $v_i$ of line L5 for the same allocation, for example by a utility from an older round, breaks the property that the bids of each buyer add up to her budget.
- Stopping when the prices of line L3 look right is wrong: in the example the prices are exactly the equilibrium prices in round 1, but the bids are not.
- Choosing the number of rounds $T$ of line L2 as if the rate were geometric gives too few rounds for linear utilities: when a buyer is indifferent at the equilibrium, the error falls roughly like $1/T$.

## Implementations

## History

Wu and Zhang introduced proportional response in 2007 to model the tit-for-tat rule of peer-to-peer file sharing, where peers trade upload bandwidth, and proved that it converges to the market equilibrium of that exchange. Zhang then studied the dynamics in the Fisher market. Shmyrev found in 2009 a convex program for the linear Fisher market in terms of the bids, related to the dual of the Eisenberg-Gale program. Birnbaum, Devanur and Xiao rediscovered it in 2011, showed that proportional response is generalized gradient descent on it with the KL divergence, and proved the bound of $\mathrm{KL}(b^* \| b^0) / T$.

## References
