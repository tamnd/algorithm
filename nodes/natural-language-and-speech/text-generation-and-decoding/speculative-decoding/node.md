---
tag: K824EJ
kind: algorithm
slug: speculative-decoding
name: Speculative decoding
aliases:
- speculative sampling
area: natural-language-and-speech/text-generation-and-decoding
level: research
summary: A small draft model proposes several tokens. The large model checks them in one pass and accepts each by a rule that keeps its exact distribution.
solves: [autoregressive-decoding]
model: real-ram
complexity:
  vars: {n: the number of output tokens, k: the number of draft tokens per step (gamma on the page), a: the acceptance rate (alpha on the page), V: "the vocabulary size |V|", P: the cost of one parallel call of the target, Q: the cost of one call of the draft}
  time: {worst: "O(n (P + k Q + k V))", expected: "O(n (1 - a) / (1 - a^(k + 1)) (P + k Q + k V))"}
  space: {extra: "O(k V)"}
properties: {deterministic: false, exact: true, online: true, recursive: false}
history:
  year: 2023
  people: [Yaniv Leviathan, Matan Kalman, Yossi Matias, Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre, John Jumper]
  note: Leviathan, Kalman and Matias (ICML 2023) and Chen et al. (arXiv 2302.01318, 2023) found the same acceptance rule independently.
prereqs: [rejection-sampling, autoregressive-decoding, transformer]
see_also: [key-value-cache, greedy-decoding, temperature-sampling, total-variation-distance, knowledge-distillation, roofline-model, ancestral-sampling, non-autoregressive-translation]
sources:
  - url: https://proceedings.mlr.press/v202/leviathan23a.html
    title: Yaniv Leviathan, Matan Kalman and Yossi Matias, Fast inference from transformers via speculative decoding, ICML 2023, PMLR 202, pages 19274 to 19286
    locator: "Algorithm 1 (one step of speculative decoding), Section 3 (the acceptance rate and Equation (1) for the expected number of tokens per run of the target), and Appendix A.1 (the proof that the output follows the target)"
  - url: https://arxiv.org/abs/2302.01318
    title: Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre and John Jumper, Accelerating large language model decoding with speculative sampling, arXiv 2302.01318, 2023
    locator: the modified rejection sampling scheme and its proof
---

Speculative decoding samples from a large autoregressive model, the target $p$, with fewer sequential calls of it. A small draft model $q$ proposes $\gamma$ tokens one by one. The target then scores all $\gamma + 1$ prefixes in one parallel pass, which on a GPU takes about as long as one ordinary step, because a decoding step of a large [transformer](/transformer/) is limited by reading the weights from memory, not by arithmetic. Each draft token $x$ is accepted with probability $\min(1, p(x) / q(x))$; at the first rejection, a token is drawn from the normalized residual $\max(0, p - q)$ and the step ends; if all are accepted, one more token comes from $p$ for free. This is a form of [rejection sampling](/rejection-sampling/), and the page proves that the output has exactly the distribution of sampling from $p$. The speed up depends on how often the draft agrees with the target, and is a measurement.

## In plain words

A big model writes well but slowly, one word at a time. A small model writes fast but worse. Let the small model guess the next few words. Then ask the big model about all of them at once, which costs about as much as asking for one word. Keep the guessed words while the big model agrees with them, by a random rule that is fair to the big model. At the first word it does not accept, the big model picks a replacement, and you start again from there. The text you get is a text the big model could have written by itself, with the same chances, but you asked it fewer times.

## The problem

The target and the draft give, for every prefix $y$, distributions $p(\cdot \mid y)$ and $q(\cdot \mid y)$ over a vocabulary $V$ that contains "</s>". The task is to draw an output $y$ with $P(y) = \prod_t p(y_t \mid y_{<t})$, exactly the law of [ancestral sampling](/ancestral-sampling/) from $p$, with as few sequential calls of $p$ as possible. A call of $p$ on several prefixes of the same sequence counts as one call, because a transformer with a [key-value cache](/key-value-cache/) scores them in one forward pass.

For one position, write $p$ and $q$ for the two distributions of the next token. The acceptance rate is

$$\alpha = \sum_{x \in V} \min(p(x), q(x)) = 1 - \mathrm{TV}(p, q),$$

where TV is the [total variation distance](/total-variation-distance/). It is the probability that a draft token is accepted.

## The algorithm

One step, from a prefix $y$:

```pseudo id=main
SPECULATIVE-STEP(y, p, q, γ)
L1  for i ← 1 to γ do                               ▷ stop early after "</s>"
L2      x_i ~ q(· | y x_1 .. x_{i-1})
L3  compute p(· | y x_1 .. x_{i-1}) for i = 1 .. γ + 1 in one call of the target
L4  for i ← 1 to γ do
L5      draw r uniform on [0, 1)
L6      if r · q(x_i | ·) < p(x_i | ·) then accept x_i and continue      ▷ probability min(1, p/q)
L7      else return x_1 .. x_{i-1} and a token drawn from norm(max(0, p(· | ·) - q(· | ·)))
L8  if x_γ = "</s>" then return x_1 .. x_γ
L9  return x_1 .. x_γ and a token drawn from p(· | y x_1 .. x_γ)
```

The decoder repeats steps from the growing output until it ends with "</s>" or reaches the length limit; near the limit, the step drafts fewer tokens so that it never overshoots. The test in line L6 is written without a division, so a draft probability of 0 needs no special case: a token with $q(x) = 0$ is never drafted. If $p = q$, the residual has mass 0, but then no rejection happens.

## Example

The target $p$ is the model M1 of [greedy decoding](/greedy-decoding/). At the empty prefix the two models are

| token | a | b | </s> |
|---|---|---|---|
| $p$ | 0.5 | 0.4 | 0.1 |
| $q$ | 0.7 | 0.2 | 0.1 |
| $\min(p, q)$ | 0.5 | 0.2 | 0.1 |
| $\max(0, p - q)$ | 0 | 0.2 | 0 |

So $\alpha = 0.8$, and the residual puts all its mass on b. Check the law of the first token:

- a is drafted with probability 0.7 and accepted with probability $0.5 / 0.7$, so it is output with probability 0.5;
- b is drafted with probability 0.2 and always accepted, and every rejection (probability $1 - \alpha = 0.2$) outputs b too, so b comes out with probability 0.4;
- "</s>" is drafted with probability 0.1 and always accepted: 0.1.

That is $p$. The draft offers too much a and too little b, and the rejection step moves exactly the excess of a to b.

If every draft token were accepted with probability $\alpha = 0.8$ independently, a step with $\gamma = 4$ would yield $(1 - 0.8^5) / (1 - 0.8) = 3.3616$ tokens per call of the target on average. The test runs 10000 steps on a pair of models that give the rows of the table at every position, with a third token c in place of "</s>", so that the rate is 0.8 at every position and the acceptances are independent. It measures an acceptance rate near 0.8 and about 3.36 tokens per call. When the two models are equal, every draft token is accepted, and 400 tokens take 100 target calls with $\gamma = 3$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The core is one line: the probability that a step emits $x$ at a given position is

$$q(x) \min\Big(1, \frac{p(x)}{q(x)}\Big) + (1 - \alpha) \frac{\max(0, p(x) - q(x))}{1 - \alpha} = \min(p(x), q(x)) + \max(0, p(x) - q(x)) = p(x).$$

The proof then shows by induction over the positions that each emitted token, given every token before it, has the law $p(\cdot \mid \text{prefix})$, whether it came from an accepted draft, a rejection or the bonus draw of line L9. By the chain rule the output has the law of sampling from $p$. This is a theorem, and the test checks it twice: the exact law of the output, computed with fractions over every path of the algorithm, equals the target law for $\gamma = 0$ to 3, and the frequencies of 20000 sampled outputs agree with it.

The same proof gives the mean number of tokens per step, $(1 - \alpha^{\gamma + 1}) / (1 - \alpha)$, under the assumption that each draft token is accepted with probability $\alpha$ independently; the test checks the exact mean against this formula for $\gamma = 0$ to 5. On real models the rate varies from position to position, so the formula is a model of the speed, not a theorem about it.

## Complexity

A step makes at most $\gamma$ draft calls, one target call, and $O(\gamma |V|)$ work for the tests and the residual. In the worst case every step emits one token, so $n$ tokens take $n$ target calls, no fewer than plain sampling, plus the draft work. With independent acceptances at rate $\alpha$, a step emits $(1 - \alpha^{\gamma + 1}) / (1 - \alpha)$ tokens on average, so the expected number of target calls is about $n (1 - \alpha) / (1 - \alpha^{\gamma + 1})$.

If one draft call costs $c$ times one target call, a step costs $\gamma c + 1$ target calls of time, and the expected speed up in wall time over plain sampling is

$$\frac{1 - \alpha^{\gamma + 1}}{(1 - \alpha)(\gamma c + 1)},$$

under the same assumptions, and assuming that the parallel call on $\gamma + 1$ prefixes takes the time of one call. It grows with $\alpha$ and has a best $\gamma$ for each $\alpha$ and $c$. Leviathan et al. measured speed ups of 2 to 3 times on T5-XXL against the standard implementation, a measurement on their hardware. The total arithmetic grows, because rejected draft tokens are scored and thrown away; the method trades arithmetic for fewer sequential steps, which pays when the target is limited by memory bandwidth (see the [roofline model](/roofline-model/)).

The extra space is the $\gamma + 1$ target distributions and the $\gamma$ draft distributions of one step, $O(\gamma |V|)$, plus the key-value caches of both models.

## Properties

- **Exact** (a theorem). The output has the law of sampling from the target, for any draft model, any $\gamma$ and any acceptance rate.
- **Never wrong, sometimes slow.** A bad draft only lowers $\alpha$; it never biases the output.
- **At least one token per target call.** Every step emits between 1 and $\gamma + 1$ tokens.
- **Greedy mode.** With temperature 0, accept a draft token when it equals the argmax of the target and otherwise emit the argmax. The output is then the output of [greedy decoding](/greedy-decoding/) of the target.
- **Works with any sampler** that changes the distribution per position, such as [temperature sampling](/temperature-sampling/), as long as $p$ and $q$ in the test are the distributions after that change.

## Variants and improvements

- **Draft choices.** A smaller model of the same family, a model trained by [knowledge distillation](/knowledge-distillation/) to match the target (which raises $\alpha$), extra prediction heads on the target itself, or n-gram matches from the prompt.
- **Draft trees.** Propose a tree of continuations and verify all its branches in one pass with a tree-shaped attention mask, to raise the expected accepted length.
- **Adaptive $\gamma$.** Stop drafting when the draft model's confidence drops, since a token it is unsure of is likely to be rejected.
- **Blockwise parallel decoding.** An earlier greedy scheme (Stern, Shazeer and Uszkoreit 2018) predicted several future tokens with extra heads and kept the longest prefix that the model's greedy choices confirmed.
- **Non-autoregressive generation.** [Non-autoregressive translation](/non-autoregressive-translation/) drops the sequential dependency instead, and changes the output distribution; speculative decoding keeps it.

## When to use it

Use speculative decoding to cut the latency of a large model at batch size 1 or small batches, where each step is limited by memory bandwidth, and when a cheap draft with a high acceptance rate exists. At large batch sizes the hardware is already busy with arithmetic, and the extra work of rejected drafts can make the total slower. Measure $\alpha$ on your data before choosing $\gamma$.

## Pitfalls

- **Testing the wrong distributions.** The test must use the same processed distributions (temperature, top-k, penalties) for $p$ and $q$ that the sampler uses. Using raw $p$ with a filtered $q$ breaks exactness.
- **A drifting key-value cache.** After a rejection, the caches of both models hold entries for draft tokens that were thrown away. Truncate them to the accepted length.
- **Floating-point ties.** The residual $\max(0, p - q)$ of two nearly equal distributions is tiny and noisy. If it sums to 0 after rounding, fall back to $p$, as the code does.
- **Speed ups are not universal.** They depend on $\alpha$, $\gamma$, $c$, the batch size and the hardware. Report them as measurements.
- **The draft must cover the target's support.** It need not, for exactness, but tokens with $q(x) = 0$ are only produced by the residual, which lowers $\alpha$.

## Implementations

The code takes the next-token distributions of the target and the draft as given, as functions of the prefix, and implements the drafting, the acceptance test and the residual sampling; it does not run or train a network. One call of the target on $\gamma + 1$ prefixes stands for one parallel forward pass and is counted as one call.

## History

Leviathan, Kalman and Matias, and Chen, Borgeaud, Irving, Lespiau, Sifre and Jumper found the same acceptance rule independently: the first posted in November 2022 and published at ICML 2023, and the second posted in February 2023. Both prove that the rule keeps the target's distribution. Earlier work on blockwise parallel decoding had used a similar draft and verify loop for greedy decoding only. The method is now a standard part of large model serving.

## References
