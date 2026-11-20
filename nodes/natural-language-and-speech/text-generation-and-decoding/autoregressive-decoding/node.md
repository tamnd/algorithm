---
tag: RQ9MXS
kind: problem
slug: autoregressive-decoding
name: Autoregressive decoding
aliases:
- decoding from a language model
area: natural-language-and-speech/text-generation-and-decoding
level: intro
summary: "Given a model that gives the next token's distribution from a prefix, find the most probable output or draw a sample, one token at a time. Sampling is easy; the exact mode is hard."
prereqs: [language-model, causal-language-modeling, conditional-probability]
see_also: [greedy-decoding, beam-search, ancestral-sampling, minimum-bayes-risk-decoding, inadequacy-of-the-mode, depth-first-branch-and-bound, speculative-decoding, hmm-decoding]
sources:
  - paper: doi:10.18653/v1/D19-1331
    title: Felix Stahlberg and Bill Byrne, On NMT search errors and model errors, cat got your tongue?, EMNLP-IJCNLP 2019, pages 3356 to 3362
    locator: exact search for the most probable translation by depth-first search with pruning, and the measured share of sentences whose most probable translation is empty
  - paper: doi:10.18653/v1/N18-1205
    title: Yining Chen, Sorcha Gilroy, Andreas Maletti, Jonathan May and Kevin Knight, Recurrent neural networks as weighted language recognizers, NAACL 2018, pages 2261 to 2271
    locator: the complexity of finding the highest weighted string of a recurrent network, undecidable in general and NP-complete for strings of polynomial length
  - paper: doi:10.1016/S0022-0000(02)00009-0
    title: Rune B. Lyngsø and Christian N. S. Pedersen, The consensus string problem and the complexity of comparing hidden Markov models, Journal of Computer and System Sciences 65(3), 2002, pages 545 to 569
    locator: the hardness of finding the most probable string emitted by a hidden Markov model
---

Autoregressive decoding is the problem of producing an output sequence from a model that gives, for every prefix, a distribution over the next token. The model defines $p(y \mid x) = \prod_{t=1}^{|y|} p(y_t \mid y_{<t}, x)$ over sequences that end with an end token `</s>`. Two questions are asked. The search question asks for the mode, $\arg\max_y p(y \mid x)$, which is what translation and speech recognition have usually wanted. The sampling question asks for a random $y$ drawn from $p(\cdot \mid x)$, or from a changed version of it, which is what open text generation usually wants. Sampling is easy: [ancestral sampling](/ancestral-sampling/) draws one token at a time and costs one model call per token. The exact mode is hard: for recurrent networks the general problem is undecidable, and NP-complete for outputs of polynomial length (Chen et al. 2018), so practical systems use [greedy decoding](/greedy-decoding/) or [beam search](/beam-search/), which can miss the mode.

## In plain words

A language model writes text one piece at a time. At each step it says how likely each possible next piece is, given what is already written. Decoding is the choice of the pieces. You can take a random piece by these chances at each step, which gives varied text and is cheap. Or you can try to find the single most likely complete text. That is much harder, because the number of possible texts grows very fast with the length, and the best first piece does not always lead to the best text.

## Definition

**Input.** A vocabulary $V$ that contains `</s>`, a length limit $n$, a context $x$ (a prompt, a source sentence or an audio signal, possibly empty), and a model that, given $x$ and a prefix $y_{<t}$, returns the [conditional probabilities](/conditional-probability/) $p(w \mid y_{<t}, x)$ for all $w \in V$. The model is a black box; one call costs $M$.

**Outputs.** The candidates are the sequences $y$ that end with their first `</s>` and have at most $n$ tokens, and the sequences of exactly $n$ tokens without `</s>`.

- **Mode (MAP decoding).** Find $\arg\max_y p(y \mid x)$, or equivalently the largest $\sum_t \log p(y_t \mid y_{<t}, x)$.
- **Sampling.** Output $y$ with probability $p(y \mid x)$, or with probability proportional to a changed distribution, such as one with a temperature or a truncated vocabulary.

## Variants

- **k best.** Find the $k$ most probable outputs.
- **Samples without replacement.** Draw $k$ distinct outputs, with the law of sampling one at a time without replacement; [stochastic beam search](/stochastic-beam-search/) does this exactly.
- **Constrained.** Find the best output that contains given phrases ([grid beam search](/grid-beam-search/)) or that a grammar accepts ([grammar constrained decoding](/grammar-constrained-decoding/)).
- **Least risk.** Find the output of least expected loss ([minimum Bayes risk decoding](/minimum-bayes-risk-decoding/)). With the 0-1 loss this is the mode.
- **Normalized scores.** Find the output of best score divided by a function of the length ([length normalization](/length-normalization/)).
- **Diverse sets.** Find $k$ outputs that are both probable and different from each other ([diverse beam search](/diverse-beam-search/)).

## Examples

Let $V = \{a, b, \text{</s>}\}$ and $n = 2$. The first step gives $p(a) = 0.6$ and $p(b) = 0.4$. After $a$ the model gives `</s>` $0.4$, $a$ $0.3$ and $b$ $0.3$; after $b$ it gives `</s>` $0.9$ and $0.05$ to each of $a$ and $b$. The output a`</s>` has probability $0.6 \times 0.4 = 0.24$, and b`</s>` has $0.4 \times 0.9 = 0.36$, while the outputs of two tokens without `</s>`, such as ab, have at most $0.6 \times 0.3 = 0.18$. The mode is b`</s>`. Greedy decoding takes $a$ first, because $0.6 > 0.4$, and returns a`</s>`. A beam of width 2 keeps both $a$ and $b$ and finds b`</s>`. Ancestral sampling returns b`</s>` with probability $0.36$.

In real translation models the mode can be very bad: Stahlberg and Byrne 2019 ran exact search on a Transformer model for English to German and measured that the most probable translation was the empty one for more than half of the test sentences (see [inadequacy of the mode](/inadequacy-of-the-mode/)).

## Known algorithms

| method | question | cost in model calls | exact? |
|---|---|---|---|
| ancestral sampling | sample | $n$ | yes |
| greedy decoding | mode | $n$ | no |
| beam search, width $k$ | mode | $n k$ | no |
| depth-first branch and bound | mode | up to $\vert V\vert^n$ | yes |
| stochastic beam search | $k$ samples without replacement | $n k$ | yes |
| MBR over $N$ samples | least risk | $n N$, plus $N^2$ loss calls | for the samples |

Each call returns $|V|$ probabilities, so beam search also does $O(n k |V|)$ work to score the extensions and a [top-k selection](/top-k-selection/) over them per step. [Speculative decoding](/speculative-decoding/) samples exactly with fewer calls of the large model, and a [key-value cache](/key-value-cache/) makes each call of a transformer cost time linear in the prefix length, not quadratic.

Exact search uses [depth-first branch and bound](/depth-first-branch-and-bound/). The log probability of a prefix never increases when a token is added, so a prefix whose log probability is already below that of the best complete output found so far can be pruned. Stahlberg and Byrne 2019 used this to find the exact mode of a neural translation model on a test set. The worst case stays exponential in $n$.

For models with a finite state, the mode is a shortest path. For an [n-gram model](/n-gram-language-model/) of order $m$, the state is the last $m - 1$ tokens, and a [Viterbi](/viterbi-algorithm/) pass over at most $n$ positions finds the most probable output in $O(n |V|^m)$ time.

## Bounds

- The number of candidates is up to $|V|^n$, so exhaustive search is exponential in $n$.
- For recurrent networks, finding the highest weighted string is undecidable in general, and NP-complete when the length is bounded by a polynomial (Chen et al. 2018). These are theorems about the worst case over networks.
- Even for a [hidden Markov model](/hidden-markov-model/), the most probable output string, a sum over all state paths, is NP-hard to find (Lyngsø and Pedersen 2002), while the most probable state path is easy ([HMM decoding](/hmm-decoding/)).
- Ancestral sampling uses one model call per output token. Speculative decoding keeps the exact law and replaces some calls of the large model with calls of a cheaper draft model.

## Reductions

- With the 0-1 loss and the full distribution, MBR decoding is MAP decoding.
- For an HMM, finding the most probable state path is HMM decoding; a neural decoder whose state is the whole prefix makes the state path and the output the same, so its mode is a most probable path in a tree of $|V|^n$ leaves.
- The k best problem with $k = 1$ is MAP decoding, and sampling $k$ outputs without replacement with $k = 1$ is ancestral sampling.

## Applications

Every text generator built on a [language model](/language-model/) or an [encoder-decoder model](/encoder-decoder-model/) solves this problem: [machine translation](/machine-translation/), [speech recognition](/automatic-speech-recognition/) with attention or transducer models, summarization, dialogue and code generation. Translation and speech recognition mostly use beam search for the mode; open text generation mostly samples, with [temperature](/temperature-sampling/), [top-k](/top-k-sampling/) or [nucleus sampling](/nucleus-sampling/).

## References
