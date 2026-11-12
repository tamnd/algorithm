---
tag: 08MB4F
kind: algorithm
slug: wake-sleep-algorithm
name: Wake-sleep algorithm
aliases:
- Helmholtz machine training
- wake-sleep
- wake-sleep learning
area: machine-learning/probabilistic-inference
level: research
summary: "Trains a generative model and a recognition model in turn: the wake phase fits the generative model to data inferred by recognition, the sleep phase fits recognition to dreams."
solves: [maximum-likelihood-estimation, marginal-inference]
model: real-ram
complexity:
  vars: {T: the number of steps, P: the number of weights in both models}
  time: {worst: "O(T P)"}
  space: {extra: "O(P)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 1995
  people: [Geoffrey E. Hinton, Peter Dayan, Brendan J. Frey, Radford M. Neal, Richard S. Zemel]
  note: "Hinton, Dayan, Frey and Neal (Science, 1995) gave the algorithm; Dayan, Hinton, Neal and Zemel (Neural Computation, 1995) named the Helmholtz machine and related it to free energy."
prereqs: [evidence-lower-bound, variational-inference]
see_also: [variational-autoencoder, expectation-maximization, contrastive-divergence, black-box-variational-inference, importance-sampling, shannon-entropy, cross-entropy-loss, autoencoder]
sources:
  - paper: "Geoffrey E. Hinton, Peter Dayan, Brendan J. Frey and Radford M. Neal, The wake-sleep algorithm for unsupervised neural networks, Science 268(5214), 1995"
    title: Hinton, Dayan, Frey and Neal 1995
    locator: "the wake and sleep phases, their local delta rules, and the description-length view"
  - paper: "Peter Dayan, Geoffrey E. Hinton, Radford M. Neal and Richard S. Zemel, The Helmholtz machine, Neural Computation 7(5), 1995"
    title: Dayan, Hinton, Neal and Zemel 1995
    locator: "the Helmholtz machine, its free energy bound, and the training of the recognition model"
  - paper: "Jorg Bornschein and Yoshua Bengio, Reweighted wake-sleep, International Conference on Learning Representations (ICLR), 2015"
    title: Bornschein and Bengio 2015
    locator: "the importance-weighted wake and sleep updates, and the wake update of the recognition model"
  - paper: "Diederik P. Kingma and Max Welling, Auto-encoding variational Bayes, International Conference on Learning Representations (ICLR), 2014"
    title: Kingma and Welling 2014
    locator: "joint training of a generative and a recognition model on one bound with the reparameterization gradient"
---

The wake-sleep algorithm trains a *Helmholtz machine*: a top-down generative model $p_\theta(h, v)$ of hidden causes $h$ and data $v$, and a bottom-up recognition model $q_\phi(h \mid v)$ that guesses the causes of a data vector. In the *wake* phase, it takes a data vector, samples causes from the recognition model, and changes $\theta$ to make that pair more probable under the generative model. In the *sleep* phase, it samples a "dream" $(h, v)$ from the generative model and changes $\phi$ to make the recognition model recover $h$ from $v$. With binary stochastic units, both updates are local delta rules. The wake phase follows the gradient of the [evidence lower bound](/evidence-lower-bound/) in $\theta$. The sleep phase minimizes $\mathrm{KL}(p \,\|\, q)$ on dreams, not the $\mathrm{KL}(q \,\|\, p)$ on data that the bound needs, so the algorithm does not optimize one bound. The [variational autoencoder](/variational-autoencoder/) keeps the same two models but trains both on the bound.

## In plain words

There are two networks. One draws: from a few hidden switches it makes a picture. The other looks: from a picture it guesses which switches were on.

While awake, the system sees real pictures. The looking network guesses the switches, and the drawing network learns to make that picture from those switches. While asleep, the drawing network makes up its own pictures, and it knows which switches it used. The looking network learns to guess those switches from the made-up pictures. Each network learns from the other's output, and each change uses only nearby signals. The looking network learns from dreams, not from real data, so the two steps do not improve one shared score. In practice the drawing network still gets better at the data.

## The problem

**The model.** A sigmoid belief network with $H$ hidden and $V$ visible binary units (more layers work the same way). The generative model is $p_\theta(h_j = 1) = \sigma(b_j)$ and $p_\theta(v_i = 1 \mid h) = \sigma(c_i + \sum_j W_{ij} h_j)$, with $\sigma(z) = 1/(1 + e^{-z})$. The recognition model is factorial: $q_\phi(h_j = 1 \mid v) = \sigma(d_j + \sum_i R_{ji} v_i)$.

**The goal.** Maximize the average log likelihood $\frac{1}{N} \sum_n \log p_\theta(v_n)$ of the data, where $p_\theta(v) = \sum_h p_\theta(h, v)$ is a sum over $2^H$ states. For large $H$ this sum, and the posterior $p_\theta(h \mid v)$, are intractable, so learning uses $q_\phi$ instead.

**The bound.** For every $v$, $\log p_\theta(v) \ge \mathcal{L}(\theta, \phi; v) = \mathbb{E}_{q_\phi}[\log p_\theta(v, h) - \log q_\phi(h \mid v)]$, with the gap $\mathrm{KL}(q_\phi(\cdot \mid v) \,\|\, p_\theta(\cdot \mid v))$. The Kullback-Leibler divergence is defined on the [ELBO](/evidence-lower-bound/) page; it is a [cross-entropy](/cross-entropy-loss/) minus an [entropy](/shannon-entropy/).

## The algorithm

```pseudo id=main
WAKE-SLEEP(data, η, T)
L1  initialize θ (generative) and φ (recognition) with small random weights
L2  for t = 1 .. T
L3      wake: take a data vector v; sample h ~ q_φ(h | v)
L4          θ ← θ + η ∇_θ log p_θ(v, h)        (delta rules)
L5      sleep: sample a dream h ~ p_θ(h)
L6          sample v ~ p_θ(v | h)
L7          φ ← φ + η ∇_φ log q_φ(h | v)        (delta rules)
L8  return θ, φ
```

With $\hat v_i = \sigma(c_i + \sum_k W_{ik} h_k)$ and $\hat h_j = q_\phi(h_j = 1 \mid v)$, the updates are

$$\Delta b_j = \eta (h_j - \sigma(b_j)), \quad \Delta c_i = \eta (v_i - \hat v_i), \quad \Delta W_{ij} = \eta (v_i - \hat v_i) h_j,$$

$$\Delta d_j = \eta (h_j - \hat h_j), \quad \Delta R_{ji} = \eta (h_j - \hat h_j) v_i.$$

Each weight changes by the product of the activity at one end and a prediction error at the other end. In a deeper network, each layer predicts the layer below in the wake phase and the layer above in the sleep phase.

## Example

**Two bars.** Four pixels; each data vector shows the left pair, the right pair, both or none: $1100$, $0011$, $1111$, $0000$, equally often. A model with two hidden units can fit this exactly in the limit of large weights, and the best average log likelihood is $-\log 4 = -1.3863$.

Run wake-sleep with $H = 2$, $\eta = 0.05$, weights started from $\mathcal{N}(0, 0.1^2)$, and a data vector drawn uniformly at each step (seed 0). The average log likelihood, by enumeration of the four hidden states, is

| steps | log likelihood | average ELBO |
|---|---|---|
| 0 | $-2.7761$ | |
| 1000 | $-2.7624$ | $-2.8014$ |
| 5000 | $-2.1729$ | $-2.2668$ |
| 20000 | $-1.4544$ | $-1.4802$ |

At the end, hidden unit 1 drives the left pair with weights $8.53$ and hidden unit 2 drives the right pair with weights $9.07$; the cross weights are below $1$ in size. So each hidden unit has learned one bar. Five more seeds end between $-1.4388$ and $-1.4279$.

**The sleep phase is not ELBO ascent.** Fix a generative model that does not fit the data: $b = 0$, $c_i = -1.5$, and both hidden units drive pixels 1 and 2 with weight $3$. Its average log likelihood on the two bars is $-3.0161$. Either hidden unit alone explains pixels 1 and 2, so the true posterior has explaining away. Exact gradient ascent from $\phi = 0$ on the sleep objective reaches recognition weights $1.72$ and biases $-2.54$, where the average ELBO is $-3.0847$. Exact ascent on the ELBO itself reaches weights $2.08$ and biases $-3.11$, with ELBO $-3.0701$.

## Correctness

- **Delta rules are gradients.** For a unit with $P(1) = \sigma(z)$, the derivative of the log probability of its value $y$ in $z$ is $y - \sigma(z)$. So the wake update is $\nabla_\theta \log p_\theta(v, h)$ and the sleep update is $\nabla_\phi \log q_\phi(h \mid v)$.
- **The wake phase climbs the ELBO in $\theta$.** Its expected value, for $h \sim q_\phi(\cdot \mid v)$, is $\nabla_\theta \mathcal{L}(\theta, \phi; v)$, because the entropy of $q$ does not depend on $\theta$. This is the M-step of generalized [expectation maximization](/expectation-maximization/) done by stochastic gradient, with $q$ in place of the exact posterior.
- **The sleep phase minimizes $\mathrm{KL}(p \| q)$ on dreams.** Its expected value is the gradient of $\mathbb{E}_{p_\theta(h, v)} \log q_\phi(h \mid v)$, which equals $-\mathbb{E}_{p_\theta(v)}\, \mathrm{KL}(p_\theta(\cdot \mid v) \| q_\phi(\cdot \mid v))$ up to a constant. The ELBO in $\phi$ needs $\mathrm{KL}(q \| p)$ averaged over the data instead. The two have different optima, as in the example.
- **Exact recognition gives the likelihood gradient.** If $q_\phi = p_\theta(\cdot \mid v)$, the expected wake update is $\nabla_\theta \log p_\theta(v)$.
- **No convergence guarantee.** The pair of updates is not gradient ascent on the ELBO, so neither the bound nor the likelihood need increase.

The proofs are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model, with one random bit counted as $O(1)$.

- **One step.** Sampling and the update cost $O(P)$ in each phase, where $P$ is the number of weights, $O(H V)$ for one hidden layer.
- **Total.** $O(T P)$ for $T$ steps.
- **Memory.** $O(P)$; the algorithm is online and keeps no data statistics.
- **Evaluation.** The log likelihood itself costs $O(2^H H V)$ per data vector by enumeration; training never needs it.

## Properties

- **Local learning rules.** Each weight uses only the two units it connects, which was a main reason for the interest in neuroscience.
- **Two objectives.** The wake phase ascends the ELBO; the sleep phase descends a different divergence on model samples.
- **Mass covering recognition.** Since the sleep phase minimizes $\mathrm{KL}(p \| q)$, a factorial $q$ tends to spread over all modes of the posterior, as in [expectation propagation](/expectation-propagation/), rather than pick one.
- **Works with discrete units.** No gradient passes through samples, so binary units are fine, unlike the reparameterization gradient of the variational autoencoder.
- **Stochastic and online.** One data vector and one dream per step.

## Variants and improvements

- **Reweighted wake-sleep.** Bornschein and Bengio (2015) draw several samples from $q$, weight them by importance weights $p_\theta(v, h)/q_\phi(h \mid v)$, and add a *wake* update for $\phi$ on real data. This gives better models and a likelihood-based objective in the limit of many samples.
- **Variational autoencoder.** Train both models on the ELBO, with the reparameterization gradient for continuous $h$; this optimizes one bound.
- **Black-box and score-function gradients.** Train $\phi$ on the ELBO with score-function estimators and control variates, as in [black-box variational inference](/black-box-variational-inference/), to keep discrete units.
- **Deep belief net fine-tuning.** Hinton, Osindero and Teh used an up-down variant of wake-sleep to fine-tune deep belief networks.

## When to use it

Use wake-sleep for directed models with discrete hidden units where you want simple, local, online updates, or as a model of learning in the brain. For best likelihoods today, prefer reweighted wake-sleep, the variational autoencoder for continuous latents, or score-function ELBO training for discrete latents.

## Pitfalls

- **Expecting a bound to rise.** Neither the ELBO nor the likelihood is guaranteed to increase.
- **Early dreams are poor.** At the start the generative model dreams nonsense, and the recognition model learns from it; the two models can lock into a poor solution.
- **Factorial recognition and explaining away.** A factorial $q$ cannot represent the correlations that explaining away creates, which biases the wake updates.
- **Learning rates.** Too large a rate makes the weights grow quickly and the units saturate.

## Implementations

## History

Hinton and Zemel had used description length and free energy to train autoencoders in 1994. In 1995, Hinton, Dayan, Frey and Neal presented the wake-sleep algorithm in *Science*, and Dayan, Hinton, Neal and Zemel described the Helmholtz machine, named after Helmholtz's view of perception as inference, in *Neural Computation*. The algorithm interested both machine learning and neuroscience, since both phases use local rules. It was later used to fine-tune deep belief networks (Hinton, Osindero and Teh, 2006). In 2014, the variational autoencoder trained the same pair of models on one bound, and in 2015 Bornschein and Bengio introduced reweighted wake-sleep.

## References
