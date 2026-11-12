---
tag: 14H9V7
kind: algorithm
slug: ancestral-sampling
name: Ancestral sampling
aliases:
- forward sampling
- logic sampling
- probabilistic logic sampling
area: machine-learning/probabilistic-inference
level: intro
summary: "Draw an exact sample from the joint distribution of a Bayesian network: draw each variable from its CPT, parents before children."
model: real-ram
complexity:
  vars: {m: the number of variables, p: the largest number of parents, c: the largest number of values of a variable, s: the number of samples}
  time: {worst: "O(s m (p + c))"}
  space: {extra: "O(m)"}
properties: {deterministic: false, exact: true, online: false, recursive: false}
history:
  year: 1988
  people: [Max Henrion]
  note: Henrion described probabilistic logic sampling for Bayesian networks in 1988, with rejection of the samples that disagree with the evidence.
prereqs: [bayesian-network, conditional-probability-table, topological-sort, inverse-transform-sampling]
see_also: [likelihood-weighting, rejection-sampling, importance-sampling, gibbs-sampling, marginal-inference, probabilistic-programming, hidden-markov-model]
sources:
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009
    locator: "Section 12.1 (forward sampling: the algorithm, the analysis of the error, and conditional queries by rejection)"
  - book: isbn:9780136042594
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, third edition, 2010
    locator: "Section 14.5.1 (direct sampling methods: PRIOR-SAMPLE and REJECTION-SAMPLING on the sprinkler network of Figure 14.12)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 8.1.2 (generative models and ancestral sampling) and Chapter 11 (sampling methods, logic sampling with evidence)"
  - paper: "Max Henrion, Propagating uncertainty in Bayesian networks by probabilistic logic sampling, in J. F. Lemmer and L. N. Kanal (eds.), Uncertainty in Artificial Intelligence 2, North-Holland, 1988"
    title: Henrion 1988
    locator: the logic sampling scheme and its rejection of samples that disagree with the evidence
---

Ancestral sampling draws one exact sample from the joint distribution of a [Bayesian network](/bayesian-network/). It visits the variables in a [topological order](/topological-sort/), so that the parents of a variable have values before the variable, and it draws each variable from its [conditional probability table](/conditional-probability-table/) given those values. A sample costs one table lookup and one draw per variable. With evidence, the method keeps only the samples that agree with it; this is [rejection sampling](/rejection-sampling/), and its acceptance rate is $P(e)$, which can be exponentially small in the number of observed variables.

## In plain words

A Bayesian network tells a story about how the data come about. Some things happen first, and other things depend on them. To make one random example of the story, you start with the things that depend on nothing. You roll a die for each of them, with the odds that the network gives. Then you go to the things that depend only on what you already know, and you roll for them with the odds that match what you rolled before. You go on until every variable has a value.

Each run gives one complete example, and the examples have exactly the right frequencies. To answer a question about the world when you already know some facts, you can make many examples and throw away the ones that do not match the facts. When the facts are rare, you throw away nearly all of them.

## The problem

The model is a Bayesian network on discrete variables $X_1, \ldots, X_m$ with a directed acyclic graph $G$. Variable $X_i$ has the parents $\mathrm{Pa}(X_i)$ and the table $P(X_i \mid \mathrm{Pa}(X_i))$. The joint distribution is the product

$$P(x_1, \ldots, x_m) = \prod_{i=1}^{m} P\big(x_i \mid x_{\mathrm{Pa}(i)}\big).$$

There are two tasks:

- **Sampling.** Output a random assignment $x$ with $\Pr[\text{output} = x] = P(x)$ for each $x$.
- **A conditional query.** Given evidence $E = e$ on some variables and a query variable $Q$, estimate $P(Q = q \mid E = e)$ for each value $q$. This is a [marginal inference](/marginal-inference/) query.

## The algorithm

The values of $X_i$ are $0, \ldots, c_i - 1$. A draw from a row $(p_0, \ldots, p_{c-1})$ takes a uniform $u \in [0, 1)$ and returns the least $x$ with $u < p_0 + \cdots + p_x$; this is [inverse transform sampling](/inverse-transform-sampling/) on a finite set.

```pseudo id=main
ANCESTRAL-SAMPLE(G, P)
L1  π ← a topological order of the variables of G
L2  for each variable X in the order π do
L3      u ← the values already drawn for the parents Pa(X)
L4      x[X] ← a draw from the row P(X | Pa(X) = u)
L5  return x

REJECTION-QUERY(G, P, Q, e, s)
L6  count[q] ← 0 for each value q of Q
L7  repeat s times
L8      x ← ANCESTRAL-SAMPLE(G, P)
L9      if x agrees with e on each observed variable then count[x[Q]] ← count[x[Q]] + 1
L10 return count / (the sum of count), or "no estimate" if the sum is 0
```

Line L3 needs only values that are already drawn, because each parent comes before its child in $\pi$. The order is computed one time, with Kahn's algorithm, and then reused for all samples.

## Example

The sprinkler network of Russell and Norvig has four binary variables: Cloudy $C$, Sprinkler $S$, Rain $R$ and WetGrass $W$, with the edges $C \to S$, $C \to R$, $S \to W$ and $R \to W$. The tables give the probability of the value 1:

| row | $P(\cdot = 1)$ |
|---|---|
| $C$ | 0.5 |
| $S$ given $C = 0$, $C = 1$ | 0.5, 0.1 |
| $R$ given $C = 0$, $C = 1$ | 0.2, 0.8 |
| $W$ given $(S, R) = (0,0), (0,1), (1,0), (1,1)$ | 0, 0.9, 0.9, 0.99 |

A topological order is $C, S, R, W$. Take the uniform numbers $0.62, 0.35, 0.71, 0.40$:

| step | row used | $P(\cdot = 0)$ | $u$ | value |
|---|---|---|---|---|
| $C$ | $P(C)$ | 0.5 | 0.62 | 1 |
| $S$ | $P(S \mid C = 1)$ | 0.9 | 0.35 | 0 |
| $R$ | $P(R \mid C = 1)$ | 0.2 | 0.71 | 1 |
| $W$ | $P(W \mid S = 0, R = 1)$ | 0.1 | 0.40 | 1 |

The sample is $(C, S, R, W) = (1, 0, 1, 1)$. Its probability is $0.5 \cdot 0.9 \cdot 0.8 \cdot 0.9 = 0.324$, the largest of the 16 joint probabilities. Two states, those with $S = R = 0$ and $W = 1$, have probability 0 and never come out.

For the query $P(R = 1 \mid W = 1)$, exact enumeration gives $P(W = 1) = 0.6471$ and $P(R = 1, W = 1) = 0.4581$, so the answer is $0.4581 / 0.6471 \approx 0.7079$. With $s = 20000$ samples and the seed 7 of the test file, REJECTION-QUERY keeps 12840 samples, near the expected $20000 \cdot 0.6471 = 12942$, and returns $0.7051$. In the same tests, a chi-square statistic of 20000 samples against the exact joint is about $13.2$ on 13 degrees of freedom.

## Correctness

Number the variables in the order $\pi$, so that each parent of $X_i$ has an index less than $i$. The first $j$ variables form an *ancestral set*: no variable outside the set is a parent of a variable in it. For such a set, the marginal is the product of the tables of its members,

$$P(x_1, \ldots, x_j) = \prod_{i=1}^{j} P\big(x_i \mid x_{\mathrm{Pa}(i)}\big),$$

because summing out $x_m$, then $x_{m-1}$, and so on, removes one table at a time: when $x_j$ is summed out, it occurs only in its own table (all its children have larger indices and are gone), and each row of a table sums to 1. The sampler draws $x_j$ from the row given $x_{\mathrm{Pa}(j)}$, so by induction on $j$ the first $j$ draws have exactly this marginal. For $j = m$ this is the joint. For the query, a sample is kept with probability $P(e)$, and a kept sample has the distribution $P(x)\,[x \text{ agrees with } e] / P(e) = P(x \mid e)$. The full proof is in the proofs file.

## Complexity

Let $p$ be the largest number of parents and $c$ the largest number of values.

- The topological order costs $O(m + |E(G)|)$ one time, with $|E(G)| \le m p$.
- One sample costs $O(p)$ to form the parent tuple and $O(c)$ to draw from the row, for each variable, so $O(m (p + c))$ for a sample and $O(s m (p + c))$ for $s$ samples. This is a worst-case bound in the [real RAM](/real-ram/), with unit cost for a uniform draw and a table lookup.
- The extra space is $O(m)$ for one sample, beside the tables, which have $\sum_i c_i \prod_{j \in \mathrm{Pa}(i)} c_j$ entries.

The statistical cost is separate. The samples are independent, so the empirical frequency of an event $A$ with $P(A) = \mu$ has the variance $\mu (1 - \mu) / s$. By the multiplicative [Chernoff bound](/chernoff-bound/), $s \ge 3 \ln(2/\delta) / (\mu \varepsilon^2)$ samples give a relative error at most $\varepsilon$ with probability at least $1 - \delta$ (Koller and Friedman, Section 12.1.2). In REJECTION-QUERY the number of kept samples is Binomial$(s, P(e))$, so the work per kept sample is $1 / P(e)$ samples on average. If $k$ observed variables are each 1 with probability $1/2$, independently, then $P(e) = 2^{-k}$: with $k = 10$ and 4096 samples, about 4 survive.

## Properties

- **Exact.** Each sample has exactly the distribution $P$. This is a sampler with no bias and no burn-in, unlike [Gibbs sampling](/gibbs-sampling/).
- **Independent samples.** The runs share no state except the generator, so the samples are i.i.d.
- **Directed models only.** The method needs the factorization into normalized conditionals. A [Markov random field](/markov-random-field/) has unnormalized potentials and an unknown [partition function](/partition-function/), so there is no order in which each draw is local.
- **Evidence only by rejection.** Ancestral sampling has no way to force an observed value except to throw samples away.

## Variants and improvements

- **Likelihood weighting.** Clamp the observed variables to their values and multiply the sample weight by $P(e_i \mid \mathrm{Pa})$ at each one. No sample is lost. See [likelihood weighting](/likelihood-weighting/).
- **Gibbs sampling and other MCMC.** Start from a state that agrees with the evidence and resample one variable at a time from its full conditional. See [Gibbs sampling](/gibbs-sampling/).
- **Sampling only the ancestors.** For a query on $Q$ with evidence on $E$, only the ancestors of $Q \cup E$ matter. The other variables can be skipped.
- **Generative models.** Sampling a [hidden Markov model](/hidden-markov-model/) state by state, sampling a language model token by token, and running a [probabilistic program](/probabilistic-programming/) forward are all ancestral sampling.

## When to use it

Use ancestral sampling to simulate data from a directed model, to check a model by looking at its samples, and to estimate prior probabilities. Use it with rejection only when the evidence is likely, for example $P(e)$ above about $10^{-2}$. For rare evidence use likelihood weighting, Gibbs sampling, or an exact method such as [variable elimination](/variable-elimination/) when the network is small.

## Pitfalls

- **A child before its parents.** Drawing in the order of the input list, not a topological order, reads parent values that do not exist yet.
- **Clamping without a weight.** Setting $W = 1$ and drawing the other variables as before gives samples from the network with $W$ cut off from its parents, not from $P(\cdot \mid W = 1)$. In the example this estimates $P(R = 1 \mid W = 1)$ as the prior $P(R = 1) = 0.5$, not $0.7079$. The weight that fixes this is likelihood weighting.
- **Rare evidence.** The expected number of samples per kept sample is $1 / P(e)$. A run that keeps no sample has no estimate at all.
- **Rounding in the draw.** The cumulative sum of a row can end slightly below 1. A draw must still return a value of positive probability.
- **A shared generator.** Use one seeded generator object passed in as a parameter, so that runs repeat.

## Implementations

## History

Henrion (1988) introduced probabilistic logic sampling for Bayesian networks: draw each node in the order of the graph and reject the samples that disagree with the evidence. Fung and Chang and, independently, Shachter and Peot (both 1990) replaced the rejection with weights, which is [likelihood weighting](/likelihood-weighting/). Bishop uses the name ancestral sampling, and Koller and Friedman use forward sampling.

## References
