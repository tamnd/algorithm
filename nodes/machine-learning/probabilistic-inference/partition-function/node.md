---
tag: VFPG8P
kind: concept
slug: partition-function
name: Partition function
aliases:
- log-partition function
area: machine-learning/probabilistic-inference
level: advanced
summary: "Z = sum over all configurations of the product of the factors. It turns factors into a distribution; log Z is convex in the natural parameters, with gradient the mean of the features."
prereqs: [markov-random-field, exponential-family-distribution]
see_also: [partition-function-computation, marginal-inference, ising-model, bethe-free-energy, mean-field-approximation, variational-inference, convex-function, log-sum-exp-trick]
sources:
  - paper: doi:10.1561/2200000001
    title: "Martin J. Wainwright and Michael I. Jordan, Graphical models, exponential families, and variational inference, Foundations and Trends in Machine Learning 1(1-2), 2008, pages 1 to 305"
    locator: "Section 3: the log partition function A of an exponential family is convex, its gradient is the mean parameter and its Hessian the covariance of the sufficient statistics"
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 4 (the partition function of a Markov network) and Chapter 20 (the gradient of the log-likelihood of a log-linear model)"
---

The partition function of a model given by nonnegative factors $\psi_c$ is the sum of their product over all configurations,
$$Z = \sum_x \prod_c \psi_c(x_c).$$
Dividing by $Z$ turns the product into a probability distribution, $P(x) = \frac{1}{Z} \prod_c \psi_c(x_c)$, as in a [Markov random field](/markov-random-field/). The name comes from statistical physics, where $Z = \sum_x e^{-E(x)/T}$ for an energy $E$ and a temperature $T$. For an [exponential family](/exponential-family-distribution/) $P_\theta(x) = \exp(\langle \theta, \phi(x) \rangle - A(\theta))$, the log-partition function $A(\theta) = \log Z(\theta)$ is [convex](/convex-function/), its gradient is the vector of means $\mathbb{E}_\theta[\phi(x)]$, and its Hessian is the covariance of $\phi(x)$ (Wainwright and Jordan 2008, Section 3). Computing $Z$ is a hard problem in general; see [partition function computation](/partition-function-computation/).

## In plain words

A model often gives each configuration a score that says how good it is, not a probability. To turn scores into probabilities, divide each score by the total of all scores. That total is the partition function.

The total is a sum over every configuration, and there are very many of them, so it is hard to compute. But it tells a lot. It is needed to compare two models, and its logarithm changes smoothly with the parameters of the model.

The rate at which the logarithm changes, when you turn up the weight of one feature, is exactly how often that feature is on, on average, under the model. This is why learning such models needs averages under the model.

## The idea

**Definition.** For discrete variables, factors $\psi_c \ge 0$ and $\tilde p(x) = \prod_c \psi_c(x_c)$, the partition function is $Z = \sum_x \tilde p(x)$, and $P(x) = \tilde p(x)/Z$ when $Z > 0$. For continuous variables the sum is an integral. $Z$ depends on the factors, not on $x$: it is a number for each model, or a function of the parameters.

**Special cases.**

- For a [Bayesian network](/bayesian-network/), the factors are conditional tables, and $Z = 1$: sum out the variables from the leaves up, and each table sums to 1.
- With evidence $e$, the sum over the configurations that agree with $e$ is $Z(e)$, and $P(e) = Z(e)/Z$. For a Bayesian network, $Z(e) = P(e)$, the probability of the evidence.
- In physics, $F = -T \log Z$ is the free energy, and the derivatives of $\log Z$ give the mean energy and the specific heat.

**Exponential families.** Write the factors as $\psi_c = \exp(\langle \theta_c, \phi_c(x_c) \rangle)$, with features $\phi$ and natural parameters $\theta$. Then $P_\theta(x) = \exp(\langle \theta, \phi(x) \rangle - A(\theta))$ with $A(\theta) = \log \sum_x \exp(\langle \theta, \phi(x) \rangle)$. Three facts:

1. **Gradient.** $\dfrac{\partial A}{\partial \theta_k} = \dfrac{1}{Z} \sum_x \phi_k(x)\, e^{\langle \theta, \phi(x) \rangle} = \mathbb{E}_\theta[\phi_k(x)]$.
2. **Hessian.** $\dfrac{\partial^2 A}{\partial \theta_j \partial \theta_k} = \mathbb{E}_\theta[\phi_j \phi_k] - \mathbb{E}_\theta[\phi_j]\, \mathbb{E}_\theta[\phi_k] = \mathrm{Cov}_\theta(\phi_j, \phi_k)$. Differentiate fact 1 by the quotient rule.
3. **Convexity.** For any direction $u$, $u^\top \nabla^2 A\, u = \mathrm{Var}_\theta(\langle u, \phi(x) \rangle) \ge 0$, so $A$ is convex. It is strictly convex when no nonzero combination $\langle u, \phi(x) \rangle$ is constant on the support, that is, when the features are not redundant.

So $A$ is a smooth convex function whose gradient maps the natural parameters $\theta$ to the mean parameters $\mu = \mathbb{E}_\theta[\phi]$. Its convex conjugate is the negative entropy, as a function of $\mu$, and
$$A(\theta) = \sup_{\mu} \big( \langle \theta, \mu \rangle - A^*(\mu) \big),$$
where $\mu$ ranges over the means that some distribution can have. This variational form is the base of [mean-field](/mean-field-approximation/) methods, of the [Bethe free energy](/bethe-free-energy/), and of other [variational methods](/variational-inference/): they replace the set of means, or the entropy, by something easier.

## Examples

**Two agreeing spins.** Two binary variables with one feature $\phi(x) = [x_1 = x_2]$ and parameter $\theta = \log 2$, so the factor is 2 when the two agree and 1 when they differ.

| $(x_1, x_2)$ | (0, 0) | (0, 1) | (1, 0) | (1, 1) |
|---|---|---|---|---|
| $\tilde p$ | 2 | 1 | 1 | 2 |

$Z = 6$, and $P(\text{agree}) = 4/6 = 2/3$. Fact 1 says $A'(\theta) = \mathbb{E}[\phi] = 2/3$. Directly: $Z(\theta) = 2 e^\theta + 2$, so $A'(\theta) = 2e^\theta / (2e^\theta + 2) = 4/6$ at $e^\theta = 2$. Fact 2 says $A''(\theta) = \mathrm{Var}(\phi) = (2/3)(1/3) = 2/9$, and the derivative of $e^\theta/(e^\theta + 1)$ is $e^\theta/(e^\theta + 1)^2 = 2/9$.

**The Ising model.** On a graph with spins $x_i \in \{-1, +1\}$, $Z = \sum_x \exp\big(\beta \sum_{ij} x_i x_j + h \sum_i x_i\big)$. The derivative of $\log Z$ with respect to $h$ is the mean total magnetization, and with respect to $\beta$ the mean number of agreeing edges minus disagreeing ones. See the [Ising model](/ising-model/).

**Counting.** With $\psi = 1$ on allowed configurations and 0 elsewhere, $Z$ counts the allowed configurations: for example, the independent sets of a graph (the hard-core model at weight 1), or the satisfying assignments of a formula.

**A Bayesian network.** $P(A)\, P(B \mid A)$ written with one indicator feature per table entry and $e^{\theta} =$ the entry has $Z = 1$.

## Where it is used

- **Learning undirected models.** The log-likelihood of data $x^{(1)}, \ldots, x^{(N)}$ is $\langle \theta, \sum_i \phi(x^{(i)}) \rangle - N A(\theta)$. By fact 1 its gradient is $N(\hat{\mathbb{E}}[\phi] - \mathbb{E}_\theta[\phi])$, the data mean minus the model mean, so each step of learning needs [marginal inference](/marginal-inference/). By fact 3 the log-likelihood is concave, and at the optimum the model means match the data means. [Conditional random fields](/conditional-random-field/) use the same facts with a $Z$ for each input.
- **Model comparison.** The probability of data under a model needs $Z$; ratios of partition functions decide which model fits better.
- **Probability of evidence.** For a Bayesian network, $P(e) = Z(e)$; for a latent variable model it is the [marginal likelihood](/marginal-likelihood/).
- **Statistical physics.** Free energy, phase transitions, and the exact solution of the planar Ising model.
- **Approximate inference.** Variational methods give bounds on $\log Z$: mean field gives a lower bound, and tree-reweighted methods an upper bound. Sampling methods estimate ratios of partition functions.
- **Counting.** Many counting problems, such as perfect matchings and independent sets, are partition functions of simple models, which is why computing $Z$ is #P-hard in general.

## References
