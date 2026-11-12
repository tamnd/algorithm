---
tag: M9NMG9
kind: technique
slug: teacher-forcing
name: Teacher forcing
aliases:
- teacher-forced training
area: machine-learning/neural-network-training
level: advanced
summary: "Train a sequence model by feeding it the true previous output at each step instead of its own prediction; fast and exact for likelihood, but it causes exposure bias."
prereqs: [backpropagation-through-time, maximum-likelihood-estimation]
see_also: [imitation-learning, dagger, beam-search, cross-entropy-loss, reinforce, hidden-markov-model, exploding-gradient-problem]
sources:
  - paper: doi:10.1162/neco.1989.1.2.270
    title: "Ronald J. Williams and David Zipser, A learning algorithm for continually running fully recurrent neural networks, Neural Computation 1(2), 1989"
    locator: pp. 270 to 280; the section on teacher-forced real-time recurrent learning
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 10.2.1 (teacher forcing and networks with output recurrence, Figure 10.6)
  - paper: "Samy Bengio, Oriol Vinyals, Navdeep Jaitly and Noam Shazeer, Scheduled sampling for sequence prediction with recurrent neural networks, Advances in Neural Information Processing Systems 28 (NIPS 2015), arXiv:1506.03099"
    locator: Section 2 (the train and test mismatch) and Section 2.4 (the decay schedules for the probability of using the true token)
  - paper: "Marc'Aurelio Ranzato, Sumit Chopra, Michael Auli and Wojciech Zaremba, Sequence level training with recurrent neural networks, ICLR 2016, arXiv:1511.06732"
    locator: Section 1 and Section 3 (the term exposure bias)
  - paper: "Stéphane Ross, Geoffrey J. Gordon and J. Andrew Bagnell, A reduction of imitation learning and structured prediction to no-regret online learning, AISTATS 2011, PMLR 15"
    locator: pp. 627 to 635; Section 2 (the error of a policy trained on expert states grows as T^2 times the one-step error)
  - paper: "Alex Lamb, Anirudh Goyal, Ying Zhang, Saizheng Zhang, Aaron Courville and Yoshua Bengio, Professor forcing: a new algorithm for training recurrent networks, Advances in Neural Information Processing Systems 29 (NIPS 2016), arXiv:1610.09038"
    locator: Section 3 (matching the hidden state dynamics of teacher-forced and free-running mode)
---

Teacher forcing is a way to train a model that produces a sequence one item at a time, where each output becomes the next input. During training, the model gets the true previous item $y_{t-1}$ from the data at step $t$, not the item $\hat y_{t-1}$ it produced itself. For a model of $p_\theta(y_t \mid y_{<t}, x)$ this is exactly maximum likelihood training, and the steps can be computed in parallel. The cost is exposure bias: at test time the model must continue from its own outputs, a situation it never saw in training, and its errors can compound.

## In plain words

Think of a student who learns to write a sentence one word at a time. With teacher forcing, after each word the teacher shows the correct word, and the student guesses the next one from the correct text so far. The student learns fast, because one bad guess does not spoil the rest of the lesson.

At the exam there is no teacher. The student must continue from their own words. If one word is wrong, the next guess starts from a text the student has never practised on, and the mistakes can pile up. This gap between practice and exam is called exposure bias.

## When it applies

The technique applies to any model whose output at step $t - 1$ is an input at step $t$: recurrent language models, the decoders of translation and speech models, attention decoders, and models of time series that predict the next value. A recurrent network of this type computes

$$h_t = F_\theta(h_{t-1}, z_{t-1}, x), \qquad p_\theta(y_t \mid \cdot) = G_\theta(h_t),$$

where $z_{t-1}$ is the item fed back from step $t - 1$ and $x$ is an optional input, such as the source sentence in translation. There are two modes:

- **Free running.** $z_{t-1} = \hat y_{t-1}$, the model's own output, sampled or chosen by [beam search](/beam-search/). This is how the model is used.
- **Teacher forcing.** $z_{t-1} = y_{t-1}$, the true item from the training data. This is how the model is trained.

Reasons to train this way:

- **It is the likelihood.** By the chain rule of probability, $\log p_\theta(y \mid x) = \sum_t \log p_\theta(y_t \mid y_{<t}, x)$. So the teacher-forced loss is the exact negative log likelihood, and minimizing it is [maximum likelihood estimation](/maximum-likelihood-estimation/) of the sequence model. Each term is a [cross-entropy loss](/cross-entropy-loss/) whose inputs are known before training starts.
- **Short gradient paths.** The outputs are not fed back, so no gradient flows through the chain $\hat y_{t-1} \to h_t$. In a network whose only recurrence goes through the output, the steps become independent, and training needs no [backpropagation through time](/backpropagation-through-time/) at all. With a hidden-to-hidden recurrence, BPTT still runs through $h_t$, but not through the sampled outputs, which are not differentiable.
- **Parallel training.** All the inputs $y_{<t}$ are known, so models without a hidden recurrence, such as convolutional or attention decoders with a causal mask, compute the losses of all $T$ positions at once.
- **Stable early training.** A model with random weights produces random outputs. In free-running mode the later steps would see only noise and get no useful signal.

## The template

```pseudo id=template
TEACHER-FORCED-LOSS(θ, x, y_1..y_T)
1  h ← INIT(θ, x);  z ← ⟨start⟩;  L ← 0
2  for t ← 1 to T do
3      h ← F_θ(h, z, x)
4      L ← L − log G_θ(h)[y_t]              ▷ cross-entropy at step t
5      z ← y_t                              ▷ teacher forcing; free running would use a sample of G_θ(h)
6  return L                                ▷ minimize with BPTT and a gradient method
```

Line 5 is the whole technique. At test time, the same loop runs with $z$ set to the model's own choice, and line 4 is not computed.

## Classic examples

**Compounding error in a linear model.** A scalar autoregressive model predicts $\hat y_t = w\, z_{t-1}$. The true sequence is $y_0 = 1$, $y_t = 0.95\, y_{t-1}$, and training has ended with $w = 1.0$, an error of $0.05$ in the coefficient. Compare the error at step $t$ in the two modes:

| $t$ | true $y_t = 0.95^t$ | teacher forced: $\lvert w\, y_{t-1} - y_t \rvert$ | free running: $\lvert w^t - y_t \rvert$ |
|---|---|---|---|
| 1 | 0.950000 | 0.050000 | 0.050000 |
| 2 | 0.902500 | 0.047500 | 0.097500 |
| 5 | 0.773781 | 0.040725 | 0.226219 |
| 10 | 0.598737 | 0.031512 | 0.401263 |
| 20 | 0.358486 | 0.018868 | 0.641514 |

The teacher-forced error, which is what training measures, stays at $0.05\, y_{t-1}$ and even shrinks. The free-running error adds up, because each step starts from the last wrong value. The training loss says that the model is good, but its prediction 20 steps ahead is off by 0.64.

**Language models.** A recurrent or attention language model is trained with teacher forcing on text, with the input sequence equal to the target sequence shifted by one position. In generation, a model that makes one unlikely choice can drift into text unlike its training data, and then repeat itself or degrade.

**Exposure bias in imitation learning.** Ranzato, Chopra, Auli and Zaremba (2016) named the mismatch exposure bias: in training, the model sees only prefixes from the data, and at test time prefixes from its own distribution. The same problem is known in [imitation learning](/imitation-learning/), where a policy trained on the states an expert visits sees other states once it makes a mistake. Ross, Gordon and Bagnell (2011) showed that if such a policy errs with probability $\varepsilon$ per step on the expert's states, its expected number of errors over $T$ steps can be of order $T^2 \varepsilon$ instead of $T \varepsilon$, because one mistake can put it in states where the later steps go wrong. [DAgger](/dagger/) removes the quadratic term by training on the states the learned policy visits.

For a probabilistic sequence model the picture is less sharp. If the model distribution equals the data distribution, teacher forcing is consistent and there is no bias. Exposure bias matters when the model is misspecified or undertrained, and when decoding is greedy or uses beam search.

## Variations

- **Scheduled sampling** (Bengio, Vinyals, Jaitly and Shazeer 2015). At each step of training, feed the true item with probability $\epsilon_i$ and the model's own sample with probability $1 - \epsilon_i$, where $i$ is the training iteration. The schedule starts at $\epsilon_i = 1$, pure teacher forcing, and decays: linearly, exponentially as $k^i$ with $k < 1$, or as an inverse sigmoid $k / (k + \exp(i / k))$ with $k \ge 1$. This exposes the model gradually to its own errors. The sampled inputs are treated as constants, so the gradient ignores how they depend on $\theta$, and the objective is no longer the likelihood: its optimum is not the data distribution in general.
- **Professor forcing** (Lamb et al. 2016). Train a discriminator to tell the hidden states of teacher-forced runs from those of free-running runs, and train the generator so that the two look the same.
- **Sequence level training.** Train on a loss of the whole generated sequence, such as BLEU, with [REINFORCE](/reinforce/) or other policy gradient methods, often started from a teacher-forced model (Ranzato et al. 2016).
- **Partial teacher forcing for continuous outputs.** For time series, mix the true and the predicted value, $z_{t-1} = \alpha y_{t-1} + (1 - \alpha) \hat y_{t-1}$, or force only every $k$-th step. This keeps the gradient paths short but trains on longer free-running stretches.
- **Teacher forcing in RTRL.** Williams and Zipser (1989) used the term for continually running recurrent networks trained by real-time recurrent learning: the units that have targets are set to the target values in the feedback, and the derivatives of these units with respect to the weights are set to zero.

## Pitfalls

- **Measuring only the teacher-forced loss.** A low validation loss with teacher forcing does not mean good generated sequences. Evaluate the model in free-running mode, as it is used.
- **Leaking the target.** The input at step $t$ must be $y_{t-1}$, shifted by one. Feeding $y_t$ lets the model copy the answer and gives a near-zero loss. In attention models the causal mask must hide all positions $\ge t$.
- **Gradients through samples.** Sampled tokens are not differentiable. In scheduled sampling the sampled input is used as a constant; a framework that tries to differentiate through argmax or sampling gives zero or undefined gradients.
- **Changing the schedule too fast.** Scheduled sampling with a fast decay gives early training the noisy free-running inputs that teacher forcing exists to avoid.
- **Continuous dynamics.** For a model of a dynamical system, teacher forcing can fit the one-step map well and still give rollouts that drift away from the data, as in the example. If the learned map is unstable, the rollouts can also grow without bound. Check multi-step predictions.

## Exercises

1. In the linear example, show that the free-running error at step $t$ is $\lvert 1 - 0.95^t \rvert$ and that it tends to 1, while the teacher-forced error tends to 0.
2. A model $\hat y_t = w\, y_{t-1}$ is trained with teacher forcing on noisy data $y_t = a\, y_{t-1} + \eta_t$. Show that the teacher-forced squared loss is minimized by the least squares estimate $w = \sum_t y_t y_{t-1} / \sum_t y_{t-1}^2$, and that its gradient needs no backpropagation through time.
3. Show that the teacher-forced cross-entropy of a sequence equals $-\log p_\theta(y_1, \ldots, y_T \mid x)$ for an autoregressive model.
4. In a network with both a hidden recurrence and an output recurrence, which gradient paths does teacher forcing cut, and which remain?

## References
