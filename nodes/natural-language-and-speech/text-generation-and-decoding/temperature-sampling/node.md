---
tag: C3YE2Y
kind: technique
slug: temperature-sampling
name: Temperature sampling
aliases:
- softmax temperature
area: natural-language-and-speech/text-generation-and-decoding
level: intro
summary: "Sample the next token from softmax(z / T). T below 1 sharpens the distribution toward greedy, T above 1 flattens it toward uniform."
prereqs: [language-model, autoregressive-decoding, softmax-regression]
see_also: [top-k-sampling, nucleus-sampling, typical-sampling, greedy-decoding, ancestral-sampling, gumbel-max-trick, shannon-entropy, simulated-annealing]
sources:
  - url: https://arxiv.org/abs/1904.09751
    title: "Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes and Yejin Choi, The curious case of neural text degeneration, ICLR 2020"
    locator: "Section 3.3 (sampling with temperature, Equation 4, with the reference to Ackley, Hinton and Sejnowski 1985) and Table 1 (sampling with t = 0.9 and top-k = 40 with t = 0.7)"
  - url: https://arxiv.org/abs/1909.05858
    title: "Nitish Shirish Keskar, Bryan McCann, Lav R. Varshney, Caiming Xiong and Richard Socher, CTRL, a conditional transformer language model for controllable generation, arXiv 1909.05858, 2019"
    locator: "Section 4.1 (Sampling), Equation 1, with the remarks that T near 0 approximates greedy decoding and a large T flattens the distribution toward uniform"
---

Temperature sampling draws the next token of an autoregressive [language model](/language-model/) from the softmax of the logits divided by a number $T > 0$, the temperature: $q_T(i) = e^{z_i / T} / \sum_j e^{z_j / T}$. With $T = 1$ it is plain [ancestral sampling](/ancestral-sampling/) from the model. A temperature below 1 makes the distribution sharper, so the likely tokens get even more of the mass, and as $T \to 0$ it becomes [greedy decoding](/greedy-decoding/). A temperature above 1 makes it flatter, and as $T \to \infty$ it becomes uniform over the allowed tokens. The order of the tokens never changes; only how strongly the draw follows it. The name comes from the Boltzmann distribution of statistical physics, where the same formula with an energy in place of the logit describes a system at a temperature. The temperature is a heuristic setting, tuned by hand for each use; no value is correct in general.

## In plain words

The model gives every possible next word a score. Temperature is a knob that sets how much you trust those scores when you draw the next word at random. Turn it down and you almost always get the top word, so the text is safe but can be dull and repeat itself. Turn it up and the weaker words get more chances, so the text is more varied but can drift into nonsense. At the middle setting of 1 you draw words with exactly the chances that the model gives.

## When it applies

Temperature applies whenever a token is drawn at random from a softmax over logits: plain sampling, and also [top-k sampling](/top-k-sampling/), [nucleus sampling](/nucleus-sampling/) and [typical sampling](/typical-sampling/), which apply it before they cut the distribution. It does not change [greedy decoding](/greedy-decoding/) or [beam search](/beam-search/) on its own, because dividing all logits by the same positive $T$ keeps their order. The same formula appears outside decoding, for example to soften the outputs of a teacher model in [knowledge distillation](/knowledge-distillation/), and as the acceptance rule of [simulated annealing](/simulated-annealing/).

## The template

The step takes the logits $z$ and a number $u$ drawn uniformly from $[0, 1)$.

```pseudo id=main
TEMPERATURE-SAMPLE(z, T, u)           ▷ z = logits, T > 0, u uniform in [0, 1)
L1  m ← max over i of z[i]            ▷ subtract it so that no exp overflows
L2  for each i do w[i] ← exp((z[i] − m) / T)
L3  Z ← sum of w[i]
L4  r ← u · Z
L5  return the first i with w[1] + ... + w[i] > r
```

Each weight is at most 1 and the largest is exactly 1, so the sum is at least 1 and nothing overflows or divides by 0. A logit of $-\infty$, as used to forbid a token, gets weight 0 and is never drawn. The proof is in [proofs/correctness.md](proofs/correctness.md): the step draws from $q_T$, the entropy of $q_T$ never decreases as $T$ grows, and the limits for $T \to 0$ and $T \to \infty$ are the uniform distributions on the tokens of largest logit and on the allowed tokens.

## Classic examples

**Three logits.** For the logits $z = (2, 1, 0)$:

| $T$ | $q_T$ | entropy (nats) |
|---|---|---|
| 0.25 | (0.98169, 0.01798, 0.00033) | 0.0930 |
| 0.5 | (0.86681, 0.11731, 0.01588) | 0.4411 |
| 1 | (0.66524, 0.24473, 0.09003) | 0.8324 |
| 2 | (0.50648, 0.30720, 0.18632) | 1.0202 |
| 4 | (0.41923, 0.32650, 0.25428) | 1.0781 |
| 100 | (0.33667, 0.33332, 0.33001) | 1.0986 |

The entropy rises from near 0 toward $\log 3 = 1.0986$, the entropy of the uniform distribution on three tokens.

**The power form.** If $p = q_1$ is the distribution at $T = 1$, then $q_T(i) \propto p_i^{1/T}$. At $T = 0.5$, the probabilities are squared and renormalized: $0.66524^2 = 0.44254$, $0.24473^2 = 0.05989$, $0.09003^2 = 0.00811$, with sum $0.51054$, which gives $(0.86681, 0.11731, 0.01588)$ again. So temperature can be applied to probabilities as well as to logits.

**Ties.** For $z = (2, 2, 0)$, a temperature near 0 does not pick one token; it gives $(0.5, 0.5, 0)$. The limit of temperature sampling is greedy decoding only when the largest logit is unique.

**In practice.** Holtzman et al. 2020 compared sampling at $T = 0.9$ and top-k = 40 at $T = 0.7$ with other decoders on GPT-2 Large. Lowering the temperature reduced the incoherent text of pure sampling but brought back some of the repetition of greedy decoding: top-k = 40 at $T = 0.7$ repeated 8.86% of the time, against 0.78% for top-k = 40 at $T = 1$.

## Variations

- **Temperature with truncation.** Apply $T$ to the logits, then top-k, top-p or typical truncation. The kept set of top-k does not depend on $T$; those of top-p and typical sampling do.
- **The Gumbel-max form.** Draw $g_i$ from a standard Gumbel distribution and return the argmax of $z_i / T + g_i$. This draws from $q_T$ too ([Gumbel-max trick](/gumbel-max-trick/)), and it is the basis of [stochastic beam search](/stochastic-beam-search/).
- **Schedules.** Change $T$ during the generation, for example a higher temperature for the first tokens of a story and a lower one later. This is a heuristic with no general result.
- **Entropy targets.** Pick $T$ at each step so that the entropy of $q_T$ hits a target value. Theorem 4 of the proof (the entropy grows with $T$) makes a bisection on $T$ work.
- **Temperature in training.** Divide the logits by $T$ in the loss, as in knowledge distillation, to give more weight to the small probabilities of a teacher.

## Pitfalls

- **Overflow.** Computing $e^{z_i / T}$ directly overflows for a small $T$: with $z = 1000$ and $T = 0.01$ the exponent is $10^5$. Subtract the largest logit first, as in line L1.
- **$T = 0$.** The formula divides by 0. Treat $T = 0$ as greedy decoding with a stated tie rule, not as a temperature.
- **The order of operations.** Temperature then top-p and top-p then temperature give different distributions, because the nucleus depends on the values. Libraries differ; state what you do.
- **High temperature with a large vocabulary.** With tens of thousands of tokens, even $T = 1.5$ moves a lot of mass to the tail, and the output can fall apart within a few tokens. Combine a high temperature with truncation.
- **No single best value.** The best temperature depends on the model, the task and how the output is judged. Values from 0.7 to 1 are common for open-ended text, and 0 (greedy) for tasks with one answer.

## Exercises

1. Show that adding the same constant to all logits does not change $q_T$, and use it to justify line L1.
2. Prove that $q_T(i) \propto p_i^{1/T}$, where $p = q_1$.
3. Show that the entropy of $q_T$ satisfies $dH / d\beta = -\beta \operatorname{Var}_\beta(z)$ with $\beta = 1/T$, and conclude that it does not decrease in $T$.
4. For $z = (2, 1, 0)$, find the temperature at which the most probable token has probability exactly 0.5. (Use bisection, since the probability is monotone in $T$.)
5. Show that the argmax of $z_i / T + g_i$, with independent standard Gumbel $g_i$, has the distribution $q_T$.

## References
