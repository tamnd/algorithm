---
tag: FEM89D
kind: definition
slug: conditional-probability-table
name: Conditional probability table
aliases:
- CPT
- tabular CPD
area: machine-learning/probabilistic-inference
level: intro
summary: "The table of P(X | parents) of one discrete node of a Bayesian network: one distribution per parent setting, (r - 1) q free numbers. Noisy-OR needs only k + 1."
history:
  year: 1988
  people: [Judea Pearl]
  note: Pearl used conditional tables as the local parameters of Bayesian networks, and the noisy-OR model to keep them small, in his 1988 book.
prereqs: [conditional-probability, discrete-probability-distribution]
see_also: [bayesian-network, conditional-independence, graphical-model, factor-graph, conjugate-prior, maximum-likelihood-estimation, naive-bayes-classifier, variable-elimination]
sources:
  - book: isbn:9781558604797
    title: "Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988"
    locator: Chapter 3, Section 3.3 (Bayesian networks specified by conditional probabilities) and Chapter 4, Section 4.3 (the noisy-OR model of disjunctive interaction)
  - book: isbn:9780262013192
    title: "Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009"
    locator: Chapter 5 (local probabilistic models, including tabular CPDs, deterministic and tree CPDs, and the noisy-or model) and Chapter 17 (maximum likelihood and Bayesian estimation of table CPDs)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 8.1.3 (discrete variables, the parameter count of a table and its reduction by the graph)
---

A conditional probability table (CPT) gives the distribution of one discrete variable $X$ for each joint value of a set of parent variables $U$. It has one row for each setting $u$ of the parents, and the row is the distribution $P(X \mid U = u)$. In a [Bayesian network](/bayesian-network/), one CPT per node, together with the graph, fixes the whole joint distribution. A full table grows exponentially with the number of parents, so models such as noisy-OR replace it with a few numbers per parent.

## Definition

Let $X$ take $r$ values and let the parents $U = (U_1, \ldots, U_k)$ take $r_1, \ldots, r_k$ values, so there are $q = \prod_{j=1}^k r_j$ parent settings ($q = 1$ when $k = 0$). A **conditional probability table** for $X$ given $U$ is an array $\theta_{x \mid u}$, indexed by $x \in \operatorname{Val}(X)$ and $u \in \operatorname{Val}(U)$, with

$$
\theta_{x \mid u} \ge 0 \quad \text{and} \quad \sum_{x} \theta_{x \mid u} = 1 \quad \text{for every } u.
$$

It is read as $P(X = x \mid U = u) = \theta_{x \mid u}$. Each row is a point of the probability simplex on $r$ values, so the table has

$$
(r - 1)\,q = (r - 1)\prod_{j=1}^k r_j
$$

free parameters. A Bayesian network on variables $X_1, \ldots, X_m$ with $r_i$ values each and parent sets $\mathrm{pa}(i)$ has $\sum_i (r_i - 1)\prod_{j \in \mathrm{pa}(i)} r_j$ free parameters, against $\prod_i r_i - 1$ for an unrestricted joint table.

**Noisy-OR.** Let $X$ and all parents be binary. Give each parent a strength $\lambda_j \in [0, 1]$ and give the child a leak $\lambda_0 \in [0, 1]$. The noisy-OR table is

$$
P(X = 0 \mid u) = (1 - \lambda_0)\prod_{j :\, u_j = 1} (1 - \lambda_j), \qquad P(X = 1 \mid u) = 1 - P(X = 0 \mid u).
$$

It has $k + 1$ parameters in place of the $2^k$ of a full binary table. The two entries of each row are nonnegative and sum to 1 by construction, so it is a CPT.

*Where it comes from.* Each active parent $j$ independently triggers a hidden cause $Z_j$ with $P(Z_j = 1) = \lambda_j$, a leak cause $Z_0$ fires with probability $\lambda_0$, and $X = Z_0 \lor \bigvee_{j : u_j = 1} Z_j$. Then $X = 0$ exactly when no cause fires, and by independence that has the probability above. The leak covers causes that are not in the model. With $\lambda_0 = 0$, a child with no active parent is off for certain.

## Examples and non-examples

**Wet grass.** The child $W$ (wet grass) has parents $S$ (the sprinkler ran) and $R$ (it rained). A noisy-OR with $\lambda_S = 0.9$, $\lambda_R = 0.8$ and leak $\lambda_0 = 0.01$ gives this table.

| $S$ | $R$ | $P(W = 0 \mid S, R)$ | $P(W = 1 \mid S, R)$ |
|---|---|---|---|
| 0 | 0 | 0.99 | 0.01 |
| 1 | 0 | 0.099 | 0.901 |
| 0 | 1 | 0.198 | 0.802 |
| 1 | 1 | 0.0198 | 0.9802 |

For example, $P(W = 0 \mid 1, 1) = 0.99 \cdot 0.1 \cdot 0.2 = 0.0198$. A full table for $W$ would have four free numbers; this one has three. With 20 binary parents, a full table has $2^{20} = 1048576$ free numbers and a noisy-OR has 21.

**Parameter count of a small network.** For the chain $A \to B \to C$ with $r_A = 2$, $r_B = 3$ and $r_C = 4$, the CPTs have $1$, $2 \cdot 2 = 4$ and $3 \cdot 3 = 9$ free numbers, 14 in total, while the full joint has $2 \cdot 3 \cdot 4 - 1 = 23$.

**A child with three values.** If $X$ has 3 values and two parents with 2 and 4 values, the table has $2 \cdot 4 = 8$ rows of 3 entries and $(3 - 1) \cdot 8 = 16$ free numbers.

**Estimating a table.** From complete data, the [maximum likelihood](/maximum-likelihood-estimation/) estimate of each row is the empirical frequency $\hat\theta_{x \mid u} = N(x, u)/N(u)$, because the likelihood of a Bayesian network splits into one multinomial likelihood per row. With a symmetric Dirichlet($\alpha$) prior on each row (the [conjugate prior](/conjugate-prior/)), the posterior mean is $(N(x, u) + \alpha)/(N(u) + r\alpha)$. For the six pairs $(x, u) = (1, 0), (0, 0), (1, 0), (1, 1), (1, 1), (1, 1)$, the MLE gives the rows $(1/3, 2/3)$ for $u = 0$ and $(0, 1)$ for $u = 1$; with $\alpha = 1$ the second row becomes $(1/5, 4/5)$. A row with $N(u) = 0$ has no MLE; the prior fixes it.

**Non-examples.**

- A table whose rows do not each sum to 1, such as the row $(1/2, 1/3)$, is not a CPT.
- A table of $P(U \mid X)$ is a CPT for the reverse arc. Putting it in the slot of $P(X \mid U)$ gives a different joint distribution.
- A joint table $P(X, U)$, or any nonnegative function of $(X, U)$, is a factor of a [Markov random field](/markov-random-field/) or a [factor graph](/factor-graph/), not a CPT: its rows need not sum to 1.
- A continuous child needs a conditional density, for example a linear Gaussian $X \mid u \sim \mathcal{N}(w^\top u + b, \sigma^2)$, and not a table.

## Related definitions

- **Conditional probability distribution (CPD).** The general term: any rule that gives $P(X \mid U = u)$ for each $u$. A CPT is the tabular CPD.
- **Compact CPDs.** Deterministic CPDs, tree CPDs (which show context-specific independence: $X$ ignores some parent when another parent has some value), noisy-MAX for multi-valued children, and logistic CPDs $P(X = 1 \mid u) = \sigma(w_0 + \sum_j w_j u_j)$ all need fewer than $(r - 1)q$ numbers.
- [Bayesian network](/bayesian-network/): a DAG with one CPD per node. The joint is the product of the CPT entries that match an assignment.
- [Conditional independence](/conditional-independence/): a CPT says nothing about the independences among the parents; the graph does.
- [Factor graph](/factor-graph/): each CPT becomes one factor node joined to the child and its parents.
- [Variable elimination](/variable-elimination/) multiplies and sums CPTs as factors; the size of the largest intermediate table, not the CPT sizes, sets its cost.
- In the [naive Bayes classifier](/naive-bayes-classifier/) each feature has a CPT with the class as its only parent.

## References
