---
tag: BASG89
kind: problem
slug: sample-complexity-of-revenue-maximization
name: Sample complexity of revenue maximization
aliases:
- Cole-Roughgarden sample complexity
area: algorithmic-game-theory/auctions
level: research
summary: "How many samples from the value distributions are needed to choose an auction that earns at least a 1 - epsilon fraction of the optimal expected revenue."
prereqs: [myerson-optimal-auction, regular-distribution, pac-learning]
see_also: [bulow-klemperer-theorem, reserve-price, empirical-risk-minimization, dkw-inequality, empirical-distribution-function, ironing, virtual-valuation, vc-dimension]
sources:
  - paper: doi:10.1145/2591796.2591867
    title: "Richard Cole and Tim Roughgarden, The sample complexity of revenue maximization, Proceedings of the 46th ACM Symposium on Theory of Computing (STOC 2014), 243-252"
    locator: the model of learning a near-optimal single-item auction from samples, the upper bound polynomial in n and 1/epsilon for regular distributions, and the lower bound of order n/epsilon
  - paper: doi:10.1137/16M1065719
    title: "Zhiyi Huang, Yishay Mansour and Tim Roughgarden, Making the most of your samples, SIAM Journal on Computing 47(3) (2018), 651-674"
    locator: Table 1 (one buyer), Theorems 3.2 and 4.12 (MHR), Theorem 4.8 (regular), Theorems 3.7 and 4.7 (support [1, H]), and the results for a single sample
  - paper: doi:10.1145/3313276.3316325
    title: "Chenghao Guo, Zhiyi Huang and Xinzhi Zhang, Settling the sample complexity of single-parameter revenue maximization, Proceedings of the 51st ACM Symposium on Theory of Computing (STOC 2019), 662-673"
    locator: the bounds for n bidders, tight up to polylogarithmic factors, for regular, MHR, [1, H] and [0, 1] values, and the method that runs Myerson's auction on a dominated empirical distribution
  - paper: doi:10.1016/j.geb.2014.03.011
    title: "Peerapong Dhangwatnotai, Tim Roughgarden and Qiqi Yan, Revenue maximization with a single sample, Games and Economic Behavior 91 (2015), 318-333"
    locator: the price equal to one sample, which earns half of the optimal revenue from one buyer with a regular distribution
---

[Myerson's optimal auction](/myerson-optimal-auction/) needs the value distribution of every bidder. A real seller does not know the distributions, but it can see past bids or values. The sample complexity of revenue maximization asks how many such samples a seller needs to choose an auction whose expected revenue is within a factor $1 - \varepsilon$ of the optimal revenue for the true distributions. The answer depends on the number $n$ of bidders, on $\varepsilon$, and on the class of distributions. For some classes no finite number of samples is enough, and for the standard classes the answer is now known up to logarithmic factors.

## In plain words

A seller who knew how much each buyer is likely to pay could set the best reserve prices. Instead, the seller has a record of what buyers paid or bid before. How long does that record need to be before the seller can set prices almost as well as with perfect knowledge? If values can be extremely spread out, a few rare buyers with huge values can carry most of the revenue, and the seller needs many samples to notice them. If the distributions are well behaved, fewer samples are enough. The question is to find the exact number of samples for each kind of distribution, and the auction that uses them best.

## Definition

There are $n$ bidders with values $v_i$ drawn independently from distributions $D_1, \ldots, D_n$, all from a class $\mathcal{C}$. Write $D = D_1 \times \cdots \times D_n$ and let $\mathrm{OPT}(D)$ be the expected revenue of Myerson's optimal auction for $D$. A learning algorithm receives $N$ independent samples $v^{(1)}, \ldots, v^{(N)}$ from $D$, each a profile of $n$ values, and outputs a single-item auction $M$ that is dominant-strategy incentive compatible. Its expected revenue $\mathrm{Rev}(M, D)$ is taken over fresh values drawn from $D$.

The **sample complexity** $N_{\mathcal{C}}(n, \varepsilon)$ is the least $N$ for which some algorithm satisfies, for every $D \in \mathcal{C}^n$,

$$\mathbb{E}_{\text{samples}}\big[\mathrm{Rev}(M, D)\big] \ge (1 - \varepsilon)\, \mathrm{OPT}(D).$$

The standard classes are:

- **Regular**: the [virtual valuation](/virtual-valuation/) is nondecreasing ([regular distribution](/regular-distribution/)).
- **MHR** (monotone hazard rate): $f(v)/(1 - F(v))$ is nondecreasing. Every MHR distribution is regular.
- **$[1, H]$**: any distribution with support in $[1, H]$.
- **$[0, 1]$ with additive error**: any distribution on $[0, 1]$, with the goal $\mathrm{Rev} \ge \mathrm{OPT} - \varepsilon$ in place of the factor $1 - \varepsilon$.

Without some such restriction the problem has no finite answer: with values on $\{0, h\}$ and the value $h$ of probability $1/h$, a seller who sees $N \ll h$ samples sees only zeros with probability close to 1, while the optimal revenue is 1.

## Variants

- **One buyer.** For $n = 1$ the problem is to learn a near-optimal posted price, the monopoly price of the [reserve price](/reserve-price/) page.
- **Identical or different bidders.** The bidders may share one distribution, or each may have its own.
- **A single sample.** With $N = 1$, the goal is a constant approximation ratio in place of $1 - \varepsilon$.
- **Learning with high probability.** The revenue must be at least $(1 - \varepsilon)\, \mathrm{OPT}$ with probability $1 - \delta$ over the samples, in the style of [PAC learning](/pac-learning/).
- **Richer settings.** Many items, many units, or matroid constraints, where the class of candidate auctions is larger.

## Examples

- **A single sample for one buyer.** Post the price $s$ equal to the one sample. For $U[0, 1]$, the price $s \sim U[0, 1]$ earns $\mathbb{E}[s(1 - s)] = 1/6$, while the optimal price $1/2$ earns $1/4$, a ratio of $2/3$. For the exponential distribution with mean 1, the sample price earns $\mathbb{E}[s e^{-s}] = \int_0^\infty s e^{-2s}\, ds = 1/4$, while the optimal price 1 earns $1/e$, a ratio of $e/4 \approx 0.68$. For every regular distribution the ratio is at least $1/2$.
- **A simple bound for values in $[1, H]$.** Take $N$ samples from one buyer, let $\hat F$ be the [empirical distribution function](/empirical-distribution-function/), and post the price $\hat p$ that maximizes the empirical revenue $p \cdot \hat{\Pr}[v \ge p]$. By the [DKW inequality](/dkw-inequality/), with probability at least $1 - \delta$ every sale probability is estimated within $\eta$ when $N \ge \ln(2/\delta)/(2\eta^2)$. Then every price $p \le H$ has its revenue estimated within $H\eta$, so $\hat p$ loses at most $2H\eta$ against the best price. Since the price 1 always sells, $\mathrm{OPT} \ge 1$, and $\eta = \varepsilon/(2H)$ gives revenue at least $(1 - \varepsilon)\, \mathrm{OPT}$ with $N = 2H^2 \ln(2/\delta)/\varepsilon^2$ samples. The best bound is smaller by a factor of about $H$.
- **Why heavy tails cost samples.** For the two-point distribution above, the price $h$ and the price 0 earn 1 and 0. A seller that has not seen the value $h$ cannot tell the distribution from a point mass at 0. This distribution has no density, so it is outside the regular and MHR classes, but a regular distribution can still put much of its revenue on rare high values, which is why the regular class needs more samples than the MHR class.

## Known algorithms

- **Empirical Myerson.** Estimate each $D_i$ from the samples, iron the estimates, and run Myerson's auction for them. Cole and Roughgarden (2014) showed that a version of this approach needs a number of samples polynomial in $n$ and $1/\varepsilon$ for regular distributions.
- **Myerson on a dominated empirical distribution.** Guo, Huang and Zhang (2019) shift each empirical distribution down by its confidence margin, so that the true distribution stochastically dominates it with high probability, and run Myerson's auction for the shifted distributions. The analysis uses the strong revenue monotonicity of Devanur, Huang and Psomas (2016): the optimal auction for a dominated distribution earns at least its own optimal revenue on the true one. This gives the tight bounds below.
- **Empirical price for one buyer.** Huang, Mansour and Roughgarden (2018) give price-learning algorithms for one buyer that reach their bounds.
- **One sample per bidder.** Dhangwatnotai, Roughgarden and Yan (2015) showed that the price equal to the sample earns half of the optimal revenue from one buyer with a regular distribution.

## Bounds

For one buyer (Huang, Mansour and Roughgarden, Table 1):

| Class | Upper bound | Lower bound |
| --- | --- | --- |
| MHR | $O(\varepsilon^{-3/2} \log \varepsilon^{-1})$ (Theorem 3.2) | $\Omega(\varepsilon^{-3/2})$ (Theorem 4.12) |
| Regular | $O(\varepsilon^{-3} \log \varepsilon^{-1})$ | $\Omega(\varepsilon^{-3})$ (Theorem 4.8) |
| $[1, H]$ | $O(H \varepsilon^{-2} \log(H \varepsilon^{-1}))$ (Theorem 3.7) | $\Omega(H \varepsilon^{-2})$ (Theorem 4.7) |

For $n$ bidders (Guo, Huang and Zhang), with $\tilde\Theta$ hiding polylogarithmic factors:

| Class | Sample complexity |
| --- | --- |
| Regular | $\tilde\Theta(n \varepsilon^{-3})$ |
| MHR | $\tilde\Theta(n \varepsilon^{-2})$ |
| $[1, H]$ | $\tilde\Theta(n H \varepsilon^{-2})$ |
| $[0, 1]$, additive error | $\tilde\Theta(n \varepsilon^{-2})$ |

These settle the earlier gap between the polynomial upper bound and the lower bound of order $n/\varepsilon$ of Cole and Roughgarden.

With a single sample and one buyer: the price equal to the sample is a $1/2$ approximation for regular distributions, and no deterministic pricing rule does better on this class. For MHR distributions, a fixed multiple of the sample earns at least $0.589$ of the optimal revenue, no deterministic rule beats $e/4 \approx 0.68$, and no continuously differentiable rule beats $0.677$ (Huang, Mansour and Roughgarden).

## Reductions

- **To statistical learning.** Choosing an auction from samples is [empirical risk minimization](/empirical-risk-minimization/) over a class of mechanisms, with revenue in place of a loss. For values in a bounded range, uniform convergence bounds, such as those from the [VC dimension](/vc-dimension/) of a class of prices, give sample bounds of the form $\mathrm{poly}(H, 1/\varepsilon)$, as in the DKW example above. The tight bounds need arguments specific to auctions.
- **From extra bidders.** By the [Bulow-Klemperer theorem](/bulow-klemperer-theorem/), for i.i.d. regular values one more bidder in a Vickrey auction is worth at least as much as full knowledge of the distribution. A bidder's value is a sample from the common distribution, which is the link between samples and competition that the single-sample mechanisms use.
- **Lower bounds by distinguishing.** Lower bounds come from pairs of distributions that are hard to tell apart with few samples but have different optimal auctions, so any algorithm loses on one of them.

## Applications

- **Reserve prices in online advertising.** A seller of ad space can set reserve prices from logs of past bids, which is a direct use of revenue learning from samples.
- **Data-driven pricing.** A seller with a history of purchases chooses a posted price or a menu, and the sample bounds say how much history is enough.
- **Prior-independent mechanism design.** A mechanism that must do well without knowing the distribution can treat the bids of some bidders as samples for setting the prices of others, which leads to the same questions.

## References
