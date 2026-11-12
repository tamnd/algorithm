---
tag: ZQSFAJ
kind: algorithm
slug: contrastive-divergence
name: Contrastive divergence
aliases:
- CD-k
- CD-1
- contrastive divergence learning
- persistent contrastive divergence
- PCD
area: machine-learning/neural-network-training
level: advanced
summary: "Train an RBM by replacing the model expectation in the log likelihood gradient with k Gibbs steps started at the data. Cheap and biased; it is not the gradient of any function."
solves: [maximum-likelihood-estimation]
model: real-ram
complexity:
  vars: {B: the number of examples in a minibatch, k: the number of Gibbs steps, m: the number of visible units, n: the number of hidden units}
  time: {worst: "Θ(B k m n)", best: "Θ(B k m n)"}
  space: {extra: Θ(m n)}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2002
  people: [Geoffrey Hinton]
  note: Hinton introduced contrastive divergence in 2002 to train products of experts, with the restricted Boltzmann machine as the main example. Tieleman added persistent chains in 2008.
prereqs: [gibbs-sampling, maximum-likelihood-estimation, partition-function, markov-random-field]
see_also: [markov-chain, stationary-distribution, mixing-time, total-variation-distance, ising-model, wake-sleep-algorithm, autoencoder, stochastic-approximation]
sources:
  - paper: doi:10.1162/089976602760128018
    title: Geoffrey E. Hinton, Training products of experts by minimizing contrastive divergence, Neural Computation 14(8), 2002
    locator: pp. 1771 to 1800 (the contrastive divergence objective, the update rule for RBMs, and the ignored term)
  - paper: doi:10.1145/1390156.1390290
    title: Tijmen Tieleman, Training restricted Boltzmann machines using approximations to the likelihood gradient, ICML 2008
    locator: pp. 1064 to 1071 (persistent contrastive divergence)
  - url: https://proceedings.mlr.press/v9/sutskever10a.html
    title: Ilya Sutskever and Tijmen Tieleman, On the convergence properties of contrastive divergence, AISTATS 2010, PMLR 9
    locator: pp. 789 to 795 (the CD update is not the gradient of any function, and CD can cycle)
  - url: https://proceedings.mlr.press/r5/carreira-perpinan05a.html
    title: Miguel A. Carreira-Perpiñán and Geoffrey E. Hinton, On contrastive divergence learning, AISTATS 2005
    locator: the bias of CD on small RBMs studied by exact enumeration, and fixed points that differ from maximum likelihood
  - paper: doi:10.1162/neco.2006.18.7.1527
    title: Geoffrey E. Hinton, Simon Osindero and Yee-Whye Teh, A fast learning algorithm for deep belief nets, Neural Computation 18(7), 2006
    locator: greedy layer-wise training of deep belief networks with RBMs trained by CD
  - paper: doi:10.1007/978-3-642-35289-8_32
    title: Geoffrey E. Hinton, A practical guide to training restricted Boltzmann machines, in Neural Networks, Tricks of the Trade, 2nd edition, LNCS 7700, Springer, 2012
    locator: the use of probabilities or samples in each phase, and the monitoring of training
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Chapter 18 (confronting the partition function), Section 18.2 (contrastive divergence and stochastic maximum likelihood)
---

Contrastive divergence (CD-k) is the standard way to train a restricted Boltzmann machine (RBM). The gradient of the log likelihood is a data term minus a model term, and the model term needs samples from the model, which need a long Markov chain. CD-k starts a [Gibbs sampling](/gibbs-sampling/) chain at a training example, runs only $k$ steps (often $k = 1$), and uses the result in place of a model sample. Hinton (2002) introduced it; the update is cheap and works well in practice, but it is biased for finite $k$ and is not the gradient of any objective (Sutskever and Tieleman 2010). Persistent CD (Tieleman 2008) keeps the chains running between updates.

## In plain words

A Boltzmann machine gives each pattern a score, and the probability of a pattern grows with its score. Training raises the scores of the training patterns and lowers the scores of the patterns that the model itself likes. Finding the patterns that the model likes is the hard part: it means running a random process for a long time.

Contrastive divergence cuts this short. It starts the random process at a training pattern and lets it run for one or a few steps. The pattern it gets is close to the data but drifts toward what the model prefers. Training then raises the score of the data and lowers the score of the drifted pattern. This is much faster, but it does not follow the exact direction that maximum likelihood would.

## The problem

**The model.** A restricted Boltzmann machine has binary visible units $v \in \{0, 1\}^m$ and hidden units $h \in \{0, 1\}^n$, connected only between the layers. The parameters are $\theta = (W, a, b)$ with $W \in \mathbb{R}^{m \times n}$, $a \in \mathbb{R}^m$, $b \in \mathbb{R}^n$, and

$$E(v, h) = -a^\top v - b^\top h - v^\top W h, \qquad p(v, h) = \frac{e^{-E(v, h)}}{Z}, \qquad Z = \sum_{v, h} e^{-E(v, h)}.$$

It is a [Markov random field](/markov-random-field/) on a complete bipartite graph. Because there are no links inside a layer, the conditionals factorize:

$$p(h_j = 1 \mid v) = \sigma\big(b_j + \textstyle\sum_i v_i W_{ij}\big), \qquad p(v_i = 1 \mid h) = \sigma\big(a_i + \textstyle\sum_j W_{ij} h_j\big),$$

with $\sigma(x) = 1/(1 + e^{-x})$. Write $q(v) = \sigma(b + W^\top v)$ for the vector of hidden probabilities.

**The goal.** Given a data set $D$ of visible vectors, [maximum likelihood](/maximum-likelihood-estimation/) maximizes $\ell(\theta) = \frac{1}{|D|} \sum_{v \in D} \log p(v)$. Its gradient is

$$\frac{\partial \ell}{\partial W_{ij}} = \langle v_i h_j \rangle_{\text{data}} - \langle v_i h_j \rangle_{\text{model}}, \qquad \frac{\partial \ell}{\partial a_i} = \langle v_i \rangle_{\text{data}} - \langle v_i \rangle_{\text{model}}, \qquad \frac{\partial \ell}{\partial b_j} = \langle h_j \rangle_{\text{data}} - \langle h_j \rangle_{\text{model}},$$

where $\langle \cdot \rangle_{\text{data}}$ averages over $v \in D$ and $h \sim p(h \mid v)$, and $\langle \cdot \rangle_{\text{model}}$ averages over $p(v, h)$. The data term is cheap by the factorization. The model term involves the [partition function](/partition-function/): an exact sum has $2^{\min(m, n)}$ terms, and sampling needs a [Markov chain](/markov-chain/) run to its [stationary distribution](/stationary-distribution/). CD-k is a cheap, biased replacement for the model term.

## The algorithm

```pseudo id=main
CD-k-UPDATE(W, a, b, minibatch V, k, η)
L1   ΔW ← 0, Δa ← 0, Δb ← 0
L2   for each v⁰ in V do
L3       p⁰ ← σ(b + Wᵀ v⁰)                      ▷ positive phase: p(h = 1 | v⁰)
L4       v ← v⁰; sample h ~ Bernoulli(p⁰)
L5       for t ← 1 to k do                         ▷ negative phase: k Gibbs steps
L6           sample v ~ Bernoulli(σ(a + W h))
L7           q ← σ(b + Wᵀ v)
L8           if t < k then sample h ~ Bernoulli(q)
L9       ΔW ← ΔW + v⁰ p⁰ᵀ − v qᵀ
L10      Δa ← Δa + v⁰ − v;  Δb ← Δb + p⁰ − q
L11  W ← W + η ΔW / |V|;  a ← a + η Δa / |V|;  b ← b + η Δb / |V|
```

Line L3 computes the data term exactly for the example. Lines L4 to L8 run $k$ steps of block Gibbs sampling, alternating between the two layers, from the data vector. Line L9 uses the probabilities $p^0$ and $q$ instead of sampled hidden states, which keeps the same expectation and lowers the variance. Line L11 is a step of stochastic gradient ascent with learning rate $\eta$.

**Persistent CD (PCD).** Keep a set of "fantasy" vectors between updates. In the negative phase, start the $k$ Gibbs steps at the fantasy vectors instead of at $v^0$, and store the final states for the next update. If the learning rate is small, the parameters change slowly, the chains stay close to the model distribution, and the negative phase approaches true model samples. This is stochastic maximum likelihood in the sense of [stochastic approximation](/stochastic-approximation/).

## Example

Take $m = 2$ visible units, $n = 1$ hidden unit, $W = (2, -1)^\top$, $a = b = 0$, and one data vector $v = (1, 0)$. Summing out $h$ gives $p(v) \propto e^{a^\top v}(1 + e^{b + v^\top W})$:

| $v$ | (0, 0) | (0, 1) | (1, 0) | (1, 1) |
|---|---|---|---|---|
| $p(v)$ | 0.1292 | 0.0884 | 0.5421 | 0.2403 |

The data term is $q(1, 0) = \sigma(2) = 0.8808$, so the data statistics for $(W_{11}, W_{21}, a_1, a_2, b_1)$ are $(0.8808, 0, 1, 0, 0.8808)$. Subtracting the model statistics gives the exact gradient. The expected CD-k update replaces $p$ with the law $T^k((1, 0), \cdot)$ of the chain after $k$ steps:

| update | $W_{11}$ | $W_{21}$ | $a_1$ | $a_2$ | $b_1$ | largest error |
|---|---|---|---|---|---|---|
| exact gradient | 0.2277 | -0.1994 | 0.2176 | -0.3287 | 0.1393 | 0 |
| expected CD-1 | 0.1807 | -0.1899 | 0.1646 | -0.2965 | 0.1118 | 0.053 |
| expected CD-2 | 0.2184 | -0.1976 | 0.2072 | -0.3223 | 0.1339 | 0.010 |
| expected CD-5 | 0.2276 | -0.1994 | 0.2176 | -0.3286 | 0.1392 | $8.0 \times 10^{-5}$ |
| expected CD-10 | 0.2277 | -0.1994 | 0.2176 | -0.3287 | 0.1393 | $2.4 \times 10^{-8}$ |

Here the chain mixes fast and CD-1 already points in the right direction with about 75 to 95 percent of each entry. With larger weights the chain mixes slowly and the bias of CD-1 is much larger.

## Correctness

By the factorization, line L3 is the exact data term, and after iteration $t$ of the loop the vector $v$ has the law $T^t(v^0, \cdot)$, where $T(v, v') = \sum_h p(h \mid v) p(v' \mid h)$ is the visible Gibbs kernel. So the expected update is the data term minus the statistics under $T^k(v^0, \cdot)$. The kernel has all entries positive and the model marginal $p(v)$ as its stationary distribution, so $T^k(v^0, \cdot) \to p$ geometrically in [total variation](/total-variation-distance/), and the expected CD-k update converges to the exact gradient as $k \to \infty$, with every coordinate within $(1 - c)^k$ for a constant $c > 0$ that depends on the parameters. The full proof is in the proofs folder.

For a fixed $k$ there is no such guarantee. Hinton (2002) motivated CD-k as following the difference $\mathrm{KL}(p_D \Vert p) - \mathrm{KL}(p_k \Vert p)$, where $p_k$ is the law after $k$ steps, but the update drops a term from the derivative of this difference, because $p_k$ depends on $\theta$. Sutskever and Tieleman (2010) showed that the CD update is in general not the gradient of any function: its Jacobian is not symmetric. Carreira-Perpiñán and Hinton (2005) found, by exact computation on small RBMs, that CD-1 converges near but not at the maximum likelihood solution. That CD-k gives good models for practical tasks is an observation.

## Complexity

One Gibbs half-step multiplies a vector by $W$ or $W^\top$, which costs $\Theta(mn)$. For a minibatch of $B$ examples and $k$ steps, the update costs $\Theta(B k m n)$ time and $\Theta(mn)$ extra space for $\Delta W$, plus $\Theta(m + n)$ per chain. PCD costs the same, plus the storage of the fantasy vectors. The exact gradient, by contrast, needs a sum over $2^{\min(m, n)}$ states; the implementation enumerates the $2^m$ visible states to check CD against it.

## Properties

- **Biased for finite $k$.** The bias shrinks as $k$ grows and as the chain mixes faster; it is large when the model has well separated modes.
- **Low variance.** The chain starts at the data, so the negative samples are close to the positive ones, and the difference has a small variance.
- **Not a gradient.** CD can in principle cycle, and there is no objective whose value is guaranteed to rise.
- **Sensitive to the data.** CD-1 only lowers the probability of states one step from the data. Modes of the model far from all data, spurious modes, can survive. PCD explores further and removes them better.
- **The likelihood is not available.** $\log p(v)$ needs $\log Z$, so training is usually monitored by the reconstruction error, which is not the likelihood, or by an estimate of $Z$ by annealed importance sampling.

## Variants and improvements

- **CD-k with larger $k$.** Increase $k$ during training as the weights grow and mixing slows.
- **Persistent CD (stochastic maximum likelihood).** Fantasy chains survive across updates (Tieleman 2008). Fast weights and parallel tempering, which runs chains at several temperatures and swaps states, improve the mixing of these chains.
- **Mean field CD.** Replace samples by their probabilities in all steps. Deterministic, but more biased.
- **Other units.** Gaussian visible units for real data, softmax units for categories, and rectified linear hidden units use the same scheme with other conditionals.
- **Deep belief networks.** Train an RBM with CD, use its hidden probabilities as data for the next RBM, and stack (Hinton, Osindero and Teh 2006).
- **Other energy-based models.** The same short-run idea trains energy-based models with continuous inputs, where Langevin dynamics replaces Gibbs sampling.

## When to use it

Use CD-1 or a small $k$ to train an RBM quickly as a feature learner or for pretraining, where a rough density model is enough. Use PCD when the density matters, for example for sampling or for a likelihood estimate, and keep the learning rate small. For exact maximum likelihood on very small models, enumerate the states. For new work on density models, other methods, such as variational autoencoders, flows or diffusion models, are usually preferred to RBMs.

## Pitfalls

- **Sampling the last hidden layer.** Use the probabilities $q$ in line L9, not sampled states, or the variance rises with no change in expectation. Sample $h$ in line L4, or the reconstruction is too smooth.
- **Trusting the reconstruction error.** It can fall while the likelihood falls too.
- **Large learning rates in PCD.** The fantasy chains lag behind the changing model, and the update becomes biased again.
- **Large weights.** They make the Gibbs chain mix slowly and the bias of CD-k large; [weight decay](/weight-decay/) keeps them small.
- **Mixing up the signs.** The update is gradient ascent on the log likelihood: data term minus model term.

## Implementations

## History

Ackley, Hinton and Sejnowski (1985) gave the learning rule for Boltzmann machines, data statistics minus model statistics, with both phases estimated by long runs of sampling. Smolensky (1986) studied the restricted form under the name harmonium. Hinton (2002) introduced contrastive divergence for products of experts, with the RBM as the main case, and made RBMs practical to train. Carreira-Perpiñán and Hinton (2005) studied its bias by exact enumeration. Hinton, Osindero and Teh (2006) used CD to train deep belief networks layer by layer, which helped start the deep learning revival. Tieleman (2008) introduced persistent CD, and Sutskever and Tieleman (2010) showed that the CD update is not the gradient of any function.

## References
