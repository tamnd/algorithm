---
tag: 1DZJ2C
kind: technique
slug: differentiable-economics
name: Deep learning for auction design
aliases:
- differentiable economics
- RegretNet
area: algorithmic-game-theory/mechanism-design
level: research
summary: Trains neural networks as allocation and payment rules to maximize revenue while penalizing the regret of misreporting.
prereqs: [stochastic-gradient-descent, augmented-lagrangian-method, dominant-strategy-incentive-compatibility]
see_also: [automated-mechanism-design, myerson-optimal-auction, simple-versus-optimal-multi-item, sample-complexity-of-revenue-maximization, backpropagation, softmax-regression, rademacher-complexity, bayesian-incentive-compatibility]
sources:
  - paper: "Paul Dütting, Zhe Feng, Harikrishna Narasimhan, David C. Parkes and Sai Srivatsa Ravindranath, Optimal auctions through deep learning, Proceedings of the 36th International Conference on Machine Learning (ICML 2019), PMLR 97, 1706-1715 (arXiv:1706.03459)"
    locator: the regret-based network, its training by an augmented Lagrangian method, and the single-bidder network that is exactly DSIC
  - paper: doi:10.1145/3630749
    title: "Paul Dütting, Zhe Feng, Harikrishna Narasimhan, David C. Parkes and Sai Srivatsa Ravindranath, Optimal auctions through deep learning: advances in differentiable economics, Journal of the ACM 71(1) (2024), 1-53"
    locator: the generalization bounds for revenue and regret, the bound on regret at a quantile, and the comparison with a linear program on a discretized instance
  - paper: doi:10.1145/3470442
    title: "Paul Dütting, Zhe Feng, Harikrishna Narasimhan, David C. Parkes and Sai Srivatsa Ravindranath, Optimal auctions through deep learning, Communications of the ACM 64(8) (2021), 109-116"
    locator: a short overview of the method and its results
---

Deep learning for auction design, also called differentiable economics, represents the allocation and payment rules of an auction as neural networks and trains them by gradient methods on sampled valuations. The objective is expected revenue, and incentive compatibility enters as a constraint that the expected regret, the most a bidder can gain by misreporting, be zero. Dütting, Feng, Narasimhan, Parkes and Ravindranath (2019) proposed the method for multi-item auctions, where the optimal mechanism is unknown in general, and showed that it recovers known optimal auctions in small cases and finds good mechanisms in larger ones. The price of this flexibility is that incentive compatibility holds only approximately, and the guarantee is measured on samples, not proved.

## In plain words

For one item, the best auction for the seller is known. For several items, it is not, and the best auctions found by hand are strange and hard to compute. This method lets a computer learn an auction from examples. A network reads the bids and says who gets what and who pays what. It is trained to raise the seller's income on many random sets of bids. At the same time, the training searches for lies that help a bidder and punishes the network when such a lie helps. In the end, lies help only a little on the training data. Honest bidding is then nearly, but not exactly, the best plan.

## When it applies

- The setting has several items or several bidders with multi-dimensional values, so that [Myerson's optimal auction](/myerson-optimal-auction/) does not apply and no closed form is known.
- The designer can draw many samples of value profiles from the prior, or has data that stands in for it.
- Approximate incentive compatibility is acceptable: a small expected gain from lying, measured on samples, is tolerable.
- The constraints of the problem can be built into the network or written as differentiable penalties, for example ex post individual rationality, unit demand or budgets.

For small finite type spaces, the exact linear program of [automated mechanism design](/automated-mechanism-design/) is a better choice, because it gives an exactly optimal and exactly incentive compatible mechanism.

## The template

There are $n$ bidders and $m$ items, and bidder $i$ has a valuation $v_i$ drawn from a known prior. A mechanism with parameters $w$ maps bids $b$ to an allocation $g^w(b)$ and payments $p^w(b)$. The utility of bidder $i$ of true value $v_i$ is $u_i^w(v_i; b) = v_i(g_i^w(b)) - p_i^w(b)$. The expected ex post regret of bidder $i$ is

$$\mathrm{rgt}_i(w) = \mathbb{E}_{v}\Big[\max_{v_i'} u_i^w\big(v_i; (v_i', v_{-i})\big) - u_i^w(v_i; v)\Big].$$

A mechanism is DSIC (up to measure-zero events) if and only if $\mathrm{rgt}_i(w) = 0$ for all $i$. The learning problem is to minimize the expected negative revenue $-\mathbb{E}_v[\sum_i p_i^w(v)]$ subject to $\mathrm{rgt}_i(w) = 0$ for all $i$, with the expectations replaced by averages over $L$ samples.

```pseudo id=main
TRAIN-AUCTION-NETWORK(samples, ρ, η, Q)
L1  initialize the network weights w and the multipliers λ_1, ..., λ_n ← 0
L2  for each step t = 1, 2, ...:
L3      draw a minibatch of value profiles v^(1), ..., v^(B)
L4      for each sample and each bidder i: find a misreport v'_i by a few steps of gradient ascent on u_i(v_i; (v'_i, v_-i))
L5      for each bidder i: r_i ← batch average of max(0, u_i(v_i; (v'_i, v_-i)) - u_i(v_i; v))
L6      C ← -(batch average of Σ_i p_i(v)) + Σ_i λ_i r_i + (ρ/2) Σ_i r_i²
L7      w ← w - η ∇_w C    ▷ backpropagation through the networks and the misreports
L8      every Q steps: λ_i ← λ_i + ρ r_i for each bidder i
L9  return the allocation network and the payment network
```

This is an [augmented Lagrangian method](/augmented-lagrangian-method/) with [stochastic gradient](/stochastic-gradient-descent/) steps in $w$ and occasional ascent steps in the multipliers. The inner search on line L4 is itself gradient ascent, and its result is kept from one step to the next for each sample.

**Architecture.** For additive bidders, the allocation network outputs, for each item, a [softmax](/softmax-regression/) over the $n$ bidders and a dummy "no sale" entry, so each item is allocated with total probability at most 1. The payment network outputs $\tilde p_i \in [0, 1]$ through a sigmoid, and the payment is $p_i = \tilde p_i \sum_j g_{ij}\, b_{ij}$, a fraction of the bidder's reported value for its allocation. This makes every truthful bidder's utility nonnegative, so ex post individual rationality holds by construction. For unit-demand bidders, a doubly stochastic allocation is produced by normalizing over bidders and over items and taking the minimum.

**What can be proved.** The paper gives generalization bounds (theorem): with high probability over the samples, the expected revenue and the expected regret of the learned network are close to their sample averages, with a gap that depends on the covering number of the network class and shrinks with the number of samples $L$. It also shows (theorem) that small expected regret implies that the regret at a high quantile is small: at most the expected regret divided by the probability of the tail. Whether the training finds a global optimum is not covered by these results (open).

## Classic examples

**One bidder, two items.** For one additive bidder with two values uniform on $[0, 1]$, the optimal mechanism is known from Manelli and Vincent. For a single bidder, a separate network, which represents the mechanism as a menu of lotteries with prices and lets the bidder choose its best entry, is exactly DSIC by construction, by Rochet's characterization of incentive compatible menus. The authors report (measured) that both this network and the regret-based network come close to the optimal revenue and learn an allocation rule that looks like the optimal one.

**Two bidders, two items.** For two additive bidders with uniform values, no closed-form optimal auction is known. The authors report (measured) that the trained network gets more revenue than strong baselines from earlier work, such as affine maximizer auctions found by search, with small regret on the test samples.

**Comparison with a linear program.** On a discretized instance with two bidders, two items and 11 values per item, the exact LP of automated mechanism design has about $9 \times 10^5$ variables and $3.6 \times 10^6$ constraints. The authors report (measured) that the LP took about 62 hours, against about 3.7 hours for training the network. This is the scale problem that motivates learning.

**Settings without a known optimum.** Later work applied the same template to bidders with budgets, to fairness constraints, to multi-unit and combinatorial settings, and to matching markets, often finding mechanisms with higher revenue than the best known simple designs (measured).

## Variations

- **Exactly DSIC menus.** For one bidder, a menu network gives exact DSIC, since the bidder simply picks its best menu entry. Shen, Tang and Zuo extended menus with a mechanism network and a buyer network. For several bidders, exact DSIC by construction is known only for restricted classes, such as affine maximizers, which give up some revenue.
- **Game formulation.** Rahme, Jelassi and Weinberg replaced the fixed multipliers by a two-player game between the auctioneer and a misreporter network, with fewer hyperparameters.
- **Symmetry.** When the prior is symmetric across bidders or items, permutation-equivariant networks share weights across them and train with fewer samples.
- **Certified regret.** Curry, Chiang, Goldstein and Dickerson computed the exact regret of a trained network with a mixed-integer program at given value profiles, instead of trusting the gradient-ascent estimate.
- **Other objectives.** Welfare, revenue with fairness constraints, or budget balance can be trained the same way, with the matching penalties.

## Pitfalls

- **Regret is underestimated.** The inner search on line L4 is local gradient ascent, so it finds a lower bound on the true best misreport. A network can report tiny regret while a better lie exists. Certification or a strong search with many restarts at test time is needed.
- **Small regret is not incentive compatibility.** Even exact zero regret on the samples gives DSIC only on the samples. Away from them, and with a finite number of samples, the guarantee is only the generalization bound. The regret must be compared with the revenue scale, not read as an absolute number.
- **Revenue gains may come from lies.** A network with positive regret may gain revenue that a truthful mechanism cannot get. Compare revenues at the same, small regret level.
- **Nonconvex training.** The training problem is nonconvex, and results depend on initialization, the penalty schedule $\rho$ and the learning rate. Several runs with different seeds should be compared.
- **Prior mismatch.** The network fits the sampling distribution. It can do badly if real bidders come from a different distribution.
- **Interpretability.** The learned rule is a black box. Checking that it is monotone, or that it treats bidders in a reasonable way, needs extra analysis.

## Exercises

1. Show that if $\mathrm{rgt}_i(w) = 0$ for all $i$ and the prior has full support, then truth telling is a dominant strategy for almost every value profile.
2. Show that the payment $p_i = \tilde p_i \sum_j g_{ij}\, b_{ij}$ with $\tilde p_i \in [0, 1]$ makes every truthful bidder's utility nonnegative.
3. For one bidder and one item with value uniform on $[0, 1]$, the optimal mechanism is the posted price $\frac{1}{2}$. Write a one-entry menu with this price and check that it is DSIC.
4. Explain why gradient ascent on the misreport can get stuck when the allocation is a step function of the bid, and how the softmax helps.
5. Use the bound on regret at a quantile to show that if the expected regret is $10^{-4}$, then the regret is at most $10^{-2}$ with probability at least $0.99$.

## References
