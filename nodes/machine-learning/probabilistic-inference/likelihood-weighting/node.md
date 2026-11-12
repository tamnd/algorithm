---
tag: S0B2H9
kind: algorithm
slug: likelihood-weighting
name: Likelihood weighting
aliases:
- likelihood weighted sampling
area: machine-learning/probabilistic-inference
level: core
summary: "Sample a Bayesian network with the evidence clamped, and weight each sample by the product of P(e_i | parents) over the observed variables."
model: real-ram
complexity:
  vars: {m: the number of variables, p: the largest number of parents, c: the largest number of values of a variable, s: the number of samples}
  time: {worst: "O(s m (p + c))"}
  space: {extra: "O(m + c)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1990
  people: [Robert Fung, Kuo-Chu Chang, Ross Shachter, Mark Peot]
  note: Fung and Chang, and Shachter and Peot, published likelihood weighting in the proceedings of the fifth Conference on Uncertainty in Artificial Intelligence, 1990.
prereqs: [ancestral-sampling, importance-sampling, bayesian-network]
see_also: [rejection-sampling, gibbs-sampling, marginal-inference, particle-filter, sequential-monte-carlo, probabilistic-programming, annealed-importance-sampling, variable-elimination]
sources:
  - paper: "Robert Fung and Kuo-Chu Chang, Weighing and integrating evidence for stochastic simulation in Bayesian networks, in Uncertainty in Artificial Intelligence 5, North-Holland, 1990"
    title: Fung and Chang 1990
    locator: the weighting of each sample by the likelihood of the evidence
  - paper: "Ross D. Shachter and Mark A. Peot, Simulation approaches to general probabilistic inference on belief networks, in Uncertainty in Artificial Intelligence 5, North-Holland, 1990"
    title: Shachter and Peot 1990
    locator: likelihood weighting and its relation to importance sampling
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009
    locator: "Section 12.2 (likelihood weighting, importance sampling, the mutilated network as the proposal, normalized importance sampling)"
  - book: isbn:9780136042594
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, third edition, 2010
    locator: "Section 14.5.1 (likelihood weighting, Figure 14.15, on the sprinkler network)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 11.1.4 (importance sampling, with likelihood weighted sampling for directed graphs)"
  - paper: "Max Henrion, Propagating uncertainty in Bayesian networks by probabilistic logic sampling, in J. F. Lemmer and L. N. Kanal (eds.), Uncertainty in Artificial Intelligence 2, North-Holland, 1988"
    title: Henrion 1988
    locator: logic sampling, the rejection scheme that likelihood weighting replaces
---

Likelihood weighting estimates a posterior $P(Q \mid E = e)$ in a [Bayesian network](/bayesian-network/) by sampling. It runs [ancestral sampling](/ancestral-sampling/), but it sets each observed variable to its observed value instead of drawing it, and it multiplies the weight of the sample by $P(e_i \mid \text{parents})$ at that variable. It is [importance sampling](/importance-sampling/) whose proposal is the *mutilated network*, the network with the edges into the observed variables cut. The weighted average is self-normalized, so it is biased for a finite sample but consistent; the mean weight is an unbiased estimate of $P(e)$.

## In plain words

Plain forward sampling of a network makes random examples and throws away the ones that do not match what you observed. When the observation is rare, almost every example is thrown away.

Likelihood weighting never throws an example away. When it reaches an observed variable, it does not roll the dice: it writes down the observed value. To make up for this, it gives the example a score. The score is the chance that the network would have produced the observed value by itself, at that point of the story. If there are several observed variables, the scores multiply.

At the end, each example votes for its answer with its score. Examples that explain the observations well count a lot, and examples that explain them badly count little or nothing.

## The problem

The model is a Bayesian network on discrete variables $X_1, \ldots, X_m$, with the joint $P(x) = \prod_i P(x_i \mid x_{\mathrm{Pa}(i)})$. The observed variables are $E \subseteq \{X_1, \ldots, X_m\}$ with the values $e$, and $Q$ is a query variable that is not observed. The task is to estimate the posterior marginal $P(Q = q \mid e)$ for each value $q$, a [marginal inference](/marginal-inference/) query, and the evidence probability $P(e)$.

## The algorithm

```pseudo id=main
LIKELIHOOD-WEIGHTING(G, P, Q, e, s)
L1  π ← a topological order of the variables of G
L2  W[q] ← 0 for each value q of Q
L3  repeat s times
L4      w ← 1
L5      for each variable X in the order π do
L6          u ← the values already set for the parents Pa(X)
L7          if X is observed then x[X] ← e[X]; w ← w · P(X = e[X] | Pa(X) = u)
L8          else x[X] ← a draw from the row P(X | Pa(X) = u)
L9      W[x[Q]] ← W[x[Q]] + w
L10 return W / (the sum of W) as the posterior, and (the sum of W) / s as the estimate of P(e)
```

Lines L4 to L8 make one weighted sample. A sample with $w = 0$ is allowed; it adds nothing.

### Why it is importance sampling

Let $Z$ be the variables that are not observed. Lines L5 to L8 draw $z$ from the distribution

$$q(z) = \prod_{X_i \notin E} P\big(x_i \mid x_{\mathrm{Pa}(i)}\big), \qquad x = (z, e),$$

which is ancestral sampling in the mutilated network: each observed variable is a constant, with no parents. The weight of line L7 is

$$w(z) = \prod_{X_i \in E} P\big(e_i \mid x_{\mathrm{Pa}(i)}\big) = \frac{P(z, e)}{q(z)},$$

the ratio of the target to the proposal that [importance sampling](/importance-sampling/) needs. So $\mathbb{E}_q[w] = \sum_z P(z, e) = P(e)$, and $\mathbb{E}_q\big[w \cdot [x_Q = q]\big] = P(Q = q, e)$. Line L10 divides one estimate by the other.

## Example

Use the sprinkler network of the [ancestral sampling](/ancestral-sampling/) page: $P(C = 1) = 0.5$; $P(S = 1 \mid C) = 0.5, 0.1$ for $C = 0, 1$; $P(R = 1 \mid C) = 0.2, 0.8$; $P(W = 1 \mid S, R) = 0, 0.9, 0.9, 0.99$ for $(S, R) = (0,0), (0,1), (1,0), (1,1)$. The evidence is $C = 1$ and $W = 1$, and the query is $R$. The exact answer, from the sum of the joint, is $P(e) = 1863/5000 = 0.3726$ and $P(R = 1 \mid e) = 202/207 \approx 0.9758$.

Each sample fixes $C = 1$, so $w$ starts at $P(C = 1) = 0.5$. Then $S$ is drawn from $P(S \mid C = 1)$, with $P(S = 0) = 0.9$, and $R$ from $P(R \mid C = 1)$, with $P(R = 0) = 0.2$. Then $W = 1$ is fixed, and $w$ is multiplied by $P(W = 1 \mid S, R)$. Three samples, with two uniform numbers each:

| $u$ for $S$, $R$ | $S$ | $R$ | $w$ |
|---|---|---|---|
| 0.30, 0.95 | 0 | 1 | $0.5 \cdot 0.9 = 0.45$ |
| 0.95, 0.30 | 1 | 1 | $0.5 \cdot 0.99 = 0.495$ |
| 0.40, 0.10 | 0 | 0 | $0.5 \cdot 0 = 0$ |

The third sample has $S = R = 0$, which cannot make the grass wet, so it gets weight 0. From these three, $W[1] = 0.945$, $W[0] = 0$, the posterior estimate of $R = 1$ is 1, and the estimate of $P(e)$ is $0.945 / 3 = 0.315$. With $s = 10000$ samples and the seed 1, the estimates are $0.9728$ for $P(R = 1 \mid e)$ and $0.3704$ for $P(e)$, and the effective sample size is about 8141.

**The bias for small samples.** With only the evidence $W = 1$, the posterior is $P(R = 1 \mid W = 1) = 509/719 \approx 0.7079$. For $s = 1$ the weight cancels in line L10, so the estimate is $[R = 1]$ for a draw from $q$, and its mean is $q(R = 1) = 0.5$. For $s = 2$ the exact mean of the estimate is $0.6459$. It tends to $0.7079$ as $s$ grows.

## Correctness

Let $\hat P_s(e) = \frac{1}{s} \sum_{t=1}^{s} w_t$ and $\hat N_s(q) = \frac{1}{s} \sum_t w_t [x_{t,Q} = q]$. The identity $q(z) w(z) = P(z, e)$ gives $\mathbb{E}[\hat P_s(e)] = P(e)$ and $\mathbb{E}[\hat N_s(q)] = P(q, e)$ exactly, for every $s$. The returned posterior is the ratio $\hat N_s(q) / \hat P_s(e)$. If $P(e) > 0$, the strong law of large numbers makes both averages converge almost surely, so the ratio converges almost surely to $P(q, e) / P(e) = P(q \mid e)$. The ratio of two unbiased estimates is not unbiased in general, as the example shows, so the posterior estimate is biased but consistent. The full proof, with the support condition, is in the proofs file.

## Complexity

- **Time.** One sample costs $O(p + c)$ per variable, as in ancestral sampling: an observed variable costs a lookup and a product, and a free one a draw. So $s$ samples cost $O(s m (p + c))$ in the worst case, plus $O(m p)$ for the topological order.
- **Space.** $O(m)$ for one sample and $O(c)$ for the totals $W$, beside the tables.
- **Samples needed.** No sample is rejected, but the estimate can still need many samples. Its quality depends on the spread of the weights. A common measure is Kish's effective sample size $(\sum_t w_t)^2 / \sum_t w_t^2$, which is at most $s$. By the delta method, the variance of the self-normalized estimate is about $\frac{1}{s} \mathbb{E}_q\big[w^2 ([x_Q = q] - \mu)^2\big] / P(e)^2$ with $\mu = P(q \mid e)$, which is large when $P(e)$ is small and the weights are uneven.

## Properties

- **Unbiased for $P(e)$.** The mean weight has the expected value $P(e)$ for every sample size.
- **Biased but consistent for posteriors.** See the example and the proof.
- **No rejection.** Every sample is kept, though some get weight 0.
- **Evidence acts only downstream.** The observed value is not used when the ancestors of an observed variable are drawn. Evidence at the leaves therefore does not guide the sampling at all; it only changes the weights.
- **Independent samples.** The samples are i.i.d. draws from $q$, unlike the dependent samples of [Gibbs sampling](/gibbs-sampling/).

## Variants and improvements

- **No evidence.** With $E = \varnothing$, every weight is 1 and the method is [ancestral sampling](/ancestral-sampling/).
- **Better proposals.** Importance sampling with a proposal that also uses the evidence on the descendants, for example one learned from earlier samples, reduces the spread of the weights (Koller and Friedman, Section 12.2).
- **Resampling.** Draw new samples from the weighted set in proportion to $w$. Applied step by step to a dynamic model, likelihood weighting with resampling is the [particle filter](/particle-filter/), a case of [sequential Monte Carlo](/sequential-monte-carlo/).
- **Annealing.** When $P(z \mid e)$ is far from $q$, [annealed importance sampling](/annealed-importance-sampling/) moves the samples through intermediate distributions with MCMC.
- **Programs.** In a [probabilistic program](/probabilistic-programming/), an observe statement multiplies the weight by the likelihood of the observed value. This is likelihood weighting on the program.

## When to use it

Use likelihood weighting for posterior queries in a Bayesian network that is too large for [variable elimination](/variable-elimination/), when the evidence is not very unlikely and most observed variables are near the roots. It is simple, it has no burn-in, and its samples are independent, so the error is easy to estimate. When the evidence is at the leaves and unlikely, the weights become very uneven; then Gibbs sampling or a better proposal works better.

## Pitfalls

- **Clamping without the weight.** Fixing the observed values and averaging without weights estimates the answer for the mutilated network, not the posterior.
- **Weight underflow.** A product of many small factors underflows. Keep $\log w$ and normalize with the log-sum-exp trick.
- **Zero total weight.** If every sample has $w = 0$, line L10 divides by zero. Report no estimate.
- **Trusting the sample count.** A few large weights can carry the whole estimate. Report the effective sample size, not only $s$.
- **Unbiased claims.** The posterior estimate is biased for each finite $s$. Only the unnormalized estimate of $P(e)$ is unbiased.

## Implementations

## History

Logic sampling, the [ancestral sampling](/ancestral-sampling/) with rejection of Henrion (1988), threw away the samples that disagree with the evidence. Fung and Chang, and independently Shachter and Peot, replaced the rejection with a weight equal to the likelihood of the evidence. Both papers appeared in the proceedings of the fifth Conference on Uncertainty in Artificial Intelligence (1990).

## References
