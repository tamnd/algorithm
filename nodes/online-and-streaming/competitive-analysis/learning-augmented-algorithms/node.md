---
tag: W5SKKF
kind: concept
slug: learning-augmented-algorithms
name: Learning-augmented algorithms
aliases:
- algorithms with predictions
- learning-augmented online algorithms
- online algorithms with predictions
area: online-and-streaming/competitive-analysis
level: research
summary: Online algorithms that use a machine-learned prediction. They are near optimal when the prediction is good (consistency) and keep a worst-case bound when it is bad (robustness).
prereqs: [competitive-ratio, online-algorithm, ski-rental-problem]
see_also: [learning-augmented-marking, ski-rental-problem, paging-problem, competitive-ratio, exponential-search, online-bipartite-matching, learned-index, learned-bloom-filter]
sources:
  - paper: doi:10.1145/3447579
    title: "Thodoris Lykouris and Sergei Vassilvitskii, Competitive caching with machine learned advice, Journal of the ACM 68(4), article 24, 2021"
    locator: the model of predictions with an error eta, the notions of consistency and robustness for caching, and the Predictive Marker algorithm with competitive ratio O(1 + min(sqrt(eta / OPT), log k)); the conference version is ICML 2018
  - paper: "Manish Purohit, Zoya Svitkina and Ravi Kumar, Improving online algorithms via ML predictions, Advances in Neural Information Processing Systems 31 (NeurIPS 2018), 9661-9670"
    locator: Section 2 (ski rental with a predicted number of days, the deterministic algorithm with trust parameter lambda, Theorem 2.2 with ratio at most min((1 + lambda) / lambda, (1 + lambda) + eta / ((1 - lambda) OPT)), and the randomized version) and Section 3 (non-clairvoyant scheduling with predicted job sizes)
  - book: isbn:9781108494311
    title: "Tim Roughgarden (editor), Beyond the Worst-Case Analysis of Algorithms, Cambridge University Press, 2021"
    locator: Chapter 30, Michael Mitzenmacher and Sergei Vassilvitskii, Algorithms with predictions (the survey of the model, ski rental, caching, learned Bloom filters and the search with a predicted position)
  - paper: "Alexander Wei and Fred Zhang, Optimal robustness-consistency trade-offs for learning-augmented online algorithms, Advances in Neural Information Processing Systems 33 (NeurIPS 2020)"
    locator: the lower bounds that show the deterministic trade-off of Purohit, Svitkina and Kumar for ski rental is optimal
---

A learning-augmented algorithm, also called an algorithm with predictions, is an [online algorithm](/online-algorithm/) that receives a prediction about the future, for example from a machine-learned model, and uses it without trusting it fully. Its quality has two measures: *consistency*, the [competitive ratio](/competitive-ratio/) when the prediction is exact, and *robustness*, the competitive ratio for every prediction, however wrong. Lykouris and Vassilvitskii (2018) set up the model for caching, with a ratio that grows with the prediction error and never passes $O(\log k)$ (see [learning-augmented marking](/learning-augmented-marking/)), and Purohit, Svitkina and Kumar (2018) gave the standard example for [ski rental](/ski-rental-problem/): a trust parameter $\lambda \in (0, 1]$ gives consistency $1 + \lambda$ and robustness $(1 + \lambda)/\lambda$.

## In plain words

An online algorithm must act before it sees the whole input, so in the worst case it does much worse than a planner who knows the future. But in practice we often have a forecast, such as how long a user will stay or which web page will be asked for next. Forecasts are useful, but they can be wrong.

A learning-augmented algorithm uses the forecast and also keeps a safety net. If the forecast is right, it is almost as good as the planner who knows the future. If the forecast is wrong, it is still not much worse than the best algorithm that uses no forecast. A setting tells it how much to trust the forecast, which trades the gain when the forecast is good against the loss when it is bad.

## The idea

Fix an online problem with an offline optimum $\mathrm{OPT}(\sigma)$ on input $\sigma$. The algorithm gets the input online and a prediction $\hat y$ at the start, or a prediction with each request. An error measure $\eta(\hat y, \sigma) \ge 0$ is $0$ exactly when the prediction is right. For a deterministic algorithm $A$:

- $A$ is **$c$-consistent** if $A(\sigma, \hat y) \le c \cdot \mathrm{OPT}(\sigma)$ whenever $\eta = 0$.
- $A$ is **$r$-robust** if $A(\sigma, \hat y) \le r \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$ and $\hat y$.
- $A$ is **smooth** if its ratio grows slowly and continuously with $\eta$, such as $c + O(\eta/\mathrm{OPT})$.

The aim is consistency close to $1$ and robustness close to the best ratio without predictions. Often a parameter sets the trade-off, and lower bounds show that both cannot be optimal at the same time. Constant additive terms are allowed, as in the usual competitive ratio. For randomized algorithms the same notions use the expected cost.

**Ski rental with a prediction.** Renting skis costs $1$ per day and buying costs $b$, a positive integer. The season lasts $x$ days, which the skier learns only when it ends. If the skier buys at the start of day $d$, the cost is $x$ when $x < d$ and $d - 1 + b$ when $x \ge d$, and $\mathrm{OPT} = \min(x, b)$. Without predictions, buying at day $b$ is optimal among deterministic rules, with ratio $2 - 1/b$. Now a prediction $y$ of $x$ is given, with error $\eta = |x - y|$. Purohit, Svitkina and Kumar fix $\lambda \in (0, 1]$ and use this rule:

- if $y \ge b$, buy at the start of day $\lceil\lambda b\rceil$;
- if $y < b$, buy at the start of day $\lceil b/\lambda\rceil$.

**Claim.** The rule is $(1 + \lambda)$-consistent and $\frac{1 + \lambda}{\lambda}$-robust.

*Robustness.* Let $d$ be the buying day. If $x < d$, the cost is $x$. If $y \ge b$, then $d = \lceil \lambda b\rceil \le b$, so $x < b$ and the cost $x$ equals $\mathrm{OPT}$. If $y < b$, the cost is $x$ and either $x \le b$, so the ratio is $1$, or $b < x \le d - 1 < b/\lambda$, so the ratio is less than $1/\lambda$. If $x \ge d$, the cost is $d - 1 + b$. When $y \ge b$, $d - 1 < \lambda b$ and $\mathrm{OPT} = \min(x, b) \ge \min(\lambda b, b) = \lambda b$, so the ratio is less than $\frac{(1 + \lambda)b}{\lambda b}$. When $y < b$, $d - 1 < b/\lambda$ and $x \ge d \ge b$, so $\mathrm{OPT} = b$ and the ratio is less than $\frac{b/\lambda + b}{b} = \frac{1 + \lambda}{\lambda}$.

*Consistency.* Let $x = y$. If $y \ge b$, then $x \ge b \ge d$, the cost is $d - 1 + b < (1 + \lambda)b$, and $\mathrm{OPT} = b$. If $y < b$, then $x < b \le d$, so the cost is $x = \mathrm{OPT}$. $\square$

For $\lambda = 1$ the rule ignores the prediction in effect and has ratio about $2$; as $\lambda \to 0$ it trusts the prediction fully, with consistency near $1$ and unbounded robustness. The full bound of Purohit, Svitkina and Kumar is $\min\{\frac{1 + \lambda}{\lambda},\ (1 + \lambda) + \frac{\eta}{(1 - \lambda)\mathrm{OPT}}\}$, so the ratio also grows smoothly with $\eta$. Wei and Zhang (2020) showed that this deterministic trade-off is the best possible. A randomized version has better consistency and robustness, close to $\frac{\lambda}{1 - e^{-\lambda}}$ and $\frac{1}{1 - e^{-\lambda}}$ for large $b$.

**A worked case.** Let $b = 10$ and $\lambda = 1/2$.

| days $x$ | prediction $y$ | buying day | cost | $\mathrm{OPT}$ | ratio |
|---|---|---|---|---|---|
| $25$ | $25$ | $5$ | $14$ | $10$ | $1.4$ |
| $25$ | $3$ | $20$ | $29$ | $10$ | $2.9$ |
| $5$ | $30$ | $5$ | $14$ | $5$ | $2.8$ |
| $3$ | $3$ | $20$ | $3$ | $3$ | $1$ |

The two exact predictions give ratios at most $1 + \lambda = 1.5$, and the two wrong ones stay below $(1 + \lambda)/\lambda = 3$.

**General methods.** Common designs are: a trust parameter, as in ski rental; following the prediction while it is consistent with what has been seen, and falling back to a robust algorithm when it fails; and running a prediction-based algorithm and a robust algorithm side by side and switching between them, which loses a constant factor in many problems.

## Examples

- **Caching.** [Predictive Marker](/learning-augmented-marking/) (Lykouris and Vassilvitskii) gets, with each request, a predicted time of the next request to the same page. It is a [marking algorithm](/marking-algorithm/) that evicts the unmarked page predicted to come last, and uses random evictions when the predictions fail. Its ratio is $O(1 + \min(\sqrt{\eta/\mathrm{OPT}}, \log k))$ for the absolute error $\eta$ of the predictions, so it is $O(1)$-consistent and $O(\log k)$-robust for the [paging problem](/paging-problem/). Rohatgi (2020) improved the dependence on $\eta$.
- **Ski rental.** The rule above, and the randomized version.
- **Non-clairvoyant scheduling.** Jobs with unknown sizes run on one machine, to minimize the total completion time. With predicted sizes, Purohit, Svitkina and Kumar mix shortest predicted job first with round robin, and get consistency $\frac{1}{1 - \lambda}$ and robustness $\frac{2}{\lambda}$.
- **Search with a predicted position.** To find a key in a sorted array with a predicted index $p$, run [exponential search](/exponential-search/) outward from $p$ and then binary search. This needs $O(1 + \log \eta)$ comparisons when the key is $\eta$ places from $p$, and never more than $O(\log n)$.
- **Online matching and secretary problems.** Predictions of the value of the best candidate, or of the edge weights, give better ratios than the $1/e$ of the [secretary problem](/secretary-problem/) when they are accurate, and keep a constant ratio when they are not (Antoniadis et al. 2020). See also [online bipartite matching](/online-bipartite-matching/).
- **Data structures.** A [learned index](/learned-index/) predicts the position of a key in a sorted array, and a [learned Bloom filter](/learned-bloom-filter/) puts a classifier in front of a backup filter, which keeps the guarantee of no false negatives.

Non-examples: an algorithm that simply trusts the prediction is consistent but has no useful robustness; and an algorithm that ignores the prediction is robust but no better when the prediction is good. Both are the two ends of the trade-off.

## Where it is used

- **Systems with forecasts.** Caches, schedulers and resource managers that have a model of future requests, such as next-access times or job lengths, and must not fail badly when the model is wrong.
- **Online decision problems.** Rent-or-buy decisions such as ski rental, power management of idle machines, and TCP-style timeouts, where the prediction is the length of the idle period.
- **Data structures.** Indexes, filters and hash tables that use learned models of the key distribution.
- **Theory beyond the worst case.** The model gives a way to explain why algorithms that use history do well in practice, and it has been applied to graph problems, covering problems, online matching, metrical task systems and many others.

## References
