---
tag: 5DBV1J
kind: technique
slug: scheduled-sampling
name: Scheduled sampling
aliases:
- curriculum sampling for sequence prediction
area: natural-language-and-speech/text-generation-and-decoding
level: advanced
summary: During training feed the model its own predicted token instead of the gold one with a probability that grows on a schedule.
prereqs: [teacher-forcing, exposure-bias, autoregressive-decoding]
see_also: [exposure-bias, teacher-forcing, dagger, imitation-learning, minimum-risk-training, reinforce, dynamic-oracle, backpropagation-through-time]
sources:
  - url: https://proceedings.neurips.cc/paper/2015/hash/e995f98d56967d946471af29d7bf99f1-Abstract.html
    title: "Samy Bengio, Oriol Vinyals, Navdeep Jaitly and Noam Shazeer, Scheduled sampling for sequence prediction with recurrent neural networks, NIPS 2015, pages 1171 to 1179"
    locator: "the description of the method (the coin flip at each time step with probability epsilon_i of using the true previous token, the linear, exponential and inverse sigmoid decay schedules, and no gradient through the sampled token) and Table 1 (image captioning on MSCOCO)"
  - url: https://arxiv.org/abs/1506.03099
    title: "Samy Bengio, Oriol Vinyals, Navdeep Jaitly and Noam Shazeer, Scheduled sampling for sequence prediction with recurrent neural networks, arXiv 1506.03099"
    locator: "the same paper, with the remark that the method was part of the winning entry of the 2015 MSCOCO image captioning challenge"
  - url: https://arxiv.org/abs/1511.05101
    title: "Ferenc Huszár, How (not) to train your generative model, scheduled sampling, likelihood, adversary?, arXiv 1511.05101, 2015"
    locator: "the analysis showing that the scheduled sampling objective is improper and leads to an inconsistent learning algorithm"
---

Scheduled sampling is a way to train an [autoregressive](/autoregressive-decoding/) sequence model that aims to reduce [exposure bias](/exposure-bias/). Plain [teacher forcing](/teacher-forcing/) always feeds the model the gold previous token $y^*_{t-1}$ when it predicts $y_t$. Scheduled sampling, from Bengio, Vinyals, Jaitly and Shazeer 2015, flips a coin at each position: with probability $\varepsilon_i$ it feeds the gold token, and otherwise a token sampled from the model's own prediction at the previous position. The loss is still the [cross-entropy](/cross-entropy-loss/) of the gold token at each position. The probability $\varepsilon_i$ starts near 1 and decays with the training iteration $i$, so the model first learns from gold prefixes and later from prefixes that look more like the ones it will see when it generates. It is a heuristic: it improved image captioning in the original paper, but Huszár 2015 showed that its objective is improper, so its optimum need not be the true distribution.

## In plain words

When a model learns to write, it normally always sees the correct text so far and guesses the next word. When it writes on its own, it sees its own text, mistakes included. Scheduled sampling closes this gap slowly. At the start of training the model sees the correct text. As training goes on, it more and more often sees its own guess in place of a correct word, so it learns to continue from its own mistakes. The change must be slow: a model that sees only its own early, poor guesses learns almost nothing.

## When it applies

Use it when a model is trained with teacher forcing and then runs freely at test time, and the outputs suffer from errors that grow along the sequence: captioning, translation, speech recognition and other sequence prediction. Training becomes slower, since the model's own predictions must be computed before they can be fed back. It needs a decay schedule and its parameters, chosen on held-out data. It is not a fix for errors that do not come from bad prefixes, and if a model already recovers well from its own mistakes, it may not help.

## The template

Let $\varepsilon_i$ be the probability of a gold input at training iteration $i$. The model predicts $y_t$ from the input $x$ and the previous token fed to it, in a recurrent network through its hidden state.

```pseudo id=main
SCHEDULED-SAMPLING-STEP(model, x, y*, i)
L1  ε ← the schedule value ε_i
L2  prev ← the start token;  loss ← 0
L3  for t ← 1 to |y*| do
L4      p ← the next-token distribution of the model given x and the tokens fed so far, ending with prev
L5      loss ← loss − log p(y*_t)
L6      with probability ε: prev ← y*_t;  else prev ← a token drawn from p   ▷ no gradient through the draw
L7  take a gradient step on loss
```

Bengio et al. used three decay schedules, with $k$ and $c$ set for the task:

- linear: $\varepsilon_i = \max(\varepsilon, k - c\,i)$, with a floor $\varepsilon$ and $0 \le \varepsilon < 1$;
- exponential: $\varepsilon_i = k^i$, with $k < 1$;
- inverse sigmoid: $\varepsilon_i = k / (k + \exp(i / k))$, with $k \ge 1$.

The coin flip is made for each token, not once for a whole sequence; the paper reports that flipping once per sequence did worse. The gradient does not flow through the sampled token, which keeps the training a sum of per-token cross-entropies, like teacher forcing.

## Classic examples

**Three schedules.** With the linear schedule $k = 1$, $c = 1/20000$ and floor 0, the exponential schedule $k = 0.9998$, and the inverse sigmoid with $k = 2000$, the probability of a gold input is:

| iteration $i$ | linear | exponential | inverse sigmoid |
|---|---|---|---|
| 0 | 1 | 1 | 0.9995 |
| 5000 | 0.75 | 0.3678 | 0.9939 |
| 10000 | 0.5 | 0.1353 | 0.9309 |
| 15000 | 0.25 | 0.0498 | 0.5252 |
| 20000 | 0 | 0.0183 | 0.0832 |

The inverse sigmoid stays near 1 for a long time, crosses 0.5 near $i = k \ln k \approx 15200$, and then falls fast. The exponential schedule leaves teacher forcing early.

**Image captioning.** Bengio et al. 2015 reported on MSCOCO:

| training | BLEU-4 | METEOR | CIDEr |
|---|---|---|---|
| teacher forcing (baseline) | 28.8 | 24.2 | 89.5 |
| always sampling | 11.2 | 15.7 | 49.7 |
| scheduled sampling | 30.6 | 24.3 | 92.1 |
| uniform scheduled sampling | 29.2 | 24.2 | 90.9 |
| scheduled sampling, ensemble of 5 | 32.3 | 25.4 | 98.7 |

"Always sampling" feeds the model's own tokens from the start, and fails. "Uniform" uses a fixed probability in place of a decaying one, and gains less. The method was part of the winning entry of the 2015 MSCOCO captioning challenge. The paper also reports experiments on constituency parsing and speech recognition.

## Variations

- **The schedule.** Linear, exponential or inverse sigmoid decay, or a decay tied to the training loss.
- **Sample or argmax.** Feed a token drawn from the model's distribution, or its most probable token.
- **Soft inputs.** Feed the average of the token embeddings weighted by the model's probabilities, which lets the gradient flow but feeds an input the model never sees at test time.
- **Two passes for parallel models.** A [transformer](/transformer/) trains all positions at once with teacher forcing. One way to apply scheduled sampling is to run a first pass with gold inputs to get the model's predictions, then a second pass with the mixed inputs.
- **Related methods.** [DAgger](/dagger/) and [dynamic oracles](/dynamic-oracle/) also train on states from the learned model, but with the correct action for each such state. Sequence-level training such as [REINFORCE](/reinforce/) with a reward or [minimum risk training](/minimum-risk-training/) trains the model on its own full outputs.

## Pitfalls

- **The gold token after a model token.** After the model feeds itself a wrong token, the target is still the gold token at that position, which may no longer be the right continuation of the actual prefix. For example, if the model wrote "a big" in place of "the big", the target is still "big", which is fine; but if it skipped a word, every later target is shifted. This is one reason the objective is improper.
- **An improper objective.** Huszár 2015 showed that the scheduled sampling objective is not minimized by the true distribution in general, so with enough data and capacity it does not converge to the right model. Teacher forcing, which is maximum likelihood, does not have this flaw.
- **Too fast a decay.** If the gold inputs disappear before the model is good, it trains on noise, as the always-sampling row shows.
- **Slower training.** Feeding back its own tokens makes the positions depend on each other, which removes the parallel training over positions of teacher forcing.
- **No gradient through the choice.** The model is not told how its earlier choices affected later losses; it only learns to continue from them.

## Exercises

1. For the inverse sigmoid schedule, show that $\varepsilon_i = 1/2$ exactly when $i = k \ln k$.
2. Choose $k$ for the exponential schedule so that $\varepsilon_i = 0.5$ at $i = 10000$.
3. With $\varepsilon = 1$ at every iteration, show that SCHEDULED-SAMPLING-STEP is teacher forcing.
4. Give a two-token example in which the model that minimizes the expected scheduled sampling loss with a fixed $\varepsilon < 1$ is not the data distribution.
5. Explain why the coin flip per token and the coin flip per sequence feed the model different kinds of prefixes.

## References
