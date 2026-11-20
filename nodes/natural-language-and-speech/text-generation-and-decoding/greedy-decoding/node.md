---
tag: 61Q9XF
kind: algorithm
slug: greedy-decoding
name: Greedy decoding
aliases:
- argmax decoding
area: natural-language-and-speech/text-generation-and-decoding
level: intro
summary: At each step emit the single most probable next token, until an end token. Fast, but its output can be far less probable than the most probable sequence.
solves: [autoregressive-decoding]
model: word-ram
complexity:
  vars: {n: the number of output tokens, V: "the vocabulary size |V|", C: the cost of one call of the model}
  time: {worst: "O(n (C + V))"}
  space: {extra: "O(n + V)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
prereqs: [language-model, autoregressive-decoding]
see_also: [beam-search, temperature-sampling, top-k-sampling, length-normalization, inadequacy-of-the-mode, key-value-cache, speculative-decoding, greedy-algorithm]
sources:
  - paper: doi:10.18653/v1/D19-1331
    title: Felix Stahlberg and Bill Byrne, On NMT search errors and model errors, cat got your tongue?, EMNLP-IJCNLP 2019, pages 3356 to 3362
    locator: the comparison of greedy search and beam search with exact search on a trained translation model
  - paper: doi:10.18653/v1/2020.emnlp-main.170
    title: Clara Meister, Ryan Cotterell and Tim Vieira, If beam search is the answer, what was the question?, EMNLP 2020, pages 2173 to 2185
    locator: the definition of decoding as the search for the most probable output, and beam search with width 1 as greedy search
---

Greedy decoding turns an autoregressive [language model](/language-model/) into a generator: at each step it appends the single most probable next token, and it stops when it emits the end token `</s>`. It makes one call of the model per output token, so it is the cheapest search for a likely output. It is a heuristic for the [autoregressive decoding](/autoregressive-decoding/) problem: the product of locally best choices can be much less probable than the most probable whole sequence, and the page gives a model where the ratio is as small as you like.

## In plain words

The model reads the words so far and gives a score to every word that can come next. Greedy decoding takes the word with the best score, adds it to the text, and asks again. It stops when the model chooses the end mark. It never goes back. So a first word that looks good can lead into a text that is bad as a whole, and the decoder cannot fix that.

## The problem

A model gives, for every prefix $y_{<t} = y_1 \ldots y_{t-1}$, a distribution $p(\cdot \mid y_{<t})$ over a vocabulary $V$ that contains `</s>`. For a conditional model the input $x$ is fixed and is left out of the notation. An output is a sequence $y = y_1 \ldots y_n$ that ends with `</s>` and has no `</s>` before it. Its probability is the product of the conditionals,

$$\log p(y) = \sum_{t=1}^{n} \log p(y_t \mid y_{<t}).$$

All logs are natural logs. The decoding problem asks for $\arg\max_y p(y)$ among the outputs of at most $N$ tokens. Greedy decoding does not solve that problem exactly. It returns the output that the greedy rule defines: $y_t = \arg\max_w p(w \mid y_{<t})$ at every step, with a fixed tie rule.

## The algorithm

The model is a function that takes a prefix and returns $\log p(w \mid \text{prefix})$ for every $w \in V$. The limit $N$ stops a model that never chooses `</s>`.

```pseudo id=main
GREEDY-DECODE(model, N)              ▷ model(y) = log p(· | y), N = the most tokens to emit
    y ← empty sequence
L1  s ← 0
L2  for t ← 1 to N do
L3      ℓ ← model(y)                  ▷ one call, |V| log probabilities
L4      w ← argmax over v of ℓ[v]     ▷ ties: the first token in the order of V
L5      append w to y,  s ← s + ℓ[w]
L6      if w = "</s>" then return (y, s)
L7  return (y, s)                     ▷ no "</s>" within N tokens: an unfinished output
```

The score $s$ is a sum of logs. A product of a few hundred probabilities underflows to 0 in double precision, and the sum does not.

## Example

Take the model M1 over $V = \{a, b, \text{</s>}\}$:

| prefix | $p(a)$ | $p(b)$ | $p(\text{</s>})$ |
|---|---|---|---|
| empty | 0.5 | 0.4 | 0.1 |
| a | 0.4 | 0.3 | 0.3 |
| b | 0.05 | 0.05 | 0.9 |
| any longer prefix | 0 | 0 | 1 |

It has seven outputs: `</s>` (0.1), a`</s>` (0.15), aa`</s>` (0.2), ab`</s>` (0.15), b`</s>` (0.36), ba`</s>` (0.02) and bb`</s>` (0.02). They sum to 1.

Greedy decoding chooses a (0.5 against 0.4), then a again (0.4), then `</s>` (1). It returns aa`</s>` with probability $0.5 \cdot 0.4 \cdot 1 = 0.2$, or $\log 0.2 = -1.609$. The most probable output is b`</s>`, with $0.4 \cdot 0.9 = 0.36$. The first step chose a because a has more mass in total, but that mass is spread over three continuations, while the mass of b is nearly all on one. A [beam search](/beam-search/) of width 2 keeps a and b after step 1. At step 2 the two best of the six extensions are b`</s>` ($\log 0.36 = -1.022$, finished) and aa ($-1.609$), so it finds b`</s>`.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows three things. The decoder stops after at most $N$ calls. The output satisfies the greedy rule at every step and its score is its exact log probability. And no constant bounds the ratio between the probability of the mode and the probability of the greedy output (a theorem): with $p(a) = 1/2 + \delta$ and $p(b) = 1/2 - \delta$ at the first step, an output b`</s>` of probability $1/2 - \delta$, and $L$ uniform steps over 4 tokens after a, the greedy output has probability $(1/2 + \delta) 4^{-L}$. The test checks $\delta = 0.01$ and $L = 6$, where the ratio is below 0.001.

So greedy decoding is a heuristic for the mode. The tests compare it with exhaustive search over all outputs of up to 5 tokens on 200 random models with 4 tokens: the greedy output never scores more than the best, and it is worse than the best on some models.

## Complexity

Each step makes one call of the model, of cost $C$, and one pass over $|V|$ scores for the argmax. For an output of $n \le N$ tokens the time is $O(n (C + |V|))$ in the word RAM, with each score as one word. For a [transformer](/transformer/) the call is the main cost. Without a cache, step $t$ runs the network on all $t$ tokens; with a [key-value cache](/key-value-cache/) it runs it on the new token only. The extra space is the output and one row of $|V|$ scores, $O(n + |V|)$, plus the cache if there is one.

Exhaustive search over outputs of at most $N$ tokens makes $\sum_{t < N} (|V| - 1)^t$ calls, which grows exponentially in $N$.

## Properties

- **Deterministic.** The same model and the same tie rule give the same output.
- **Not exact.** The output can be far less probable than the mode (the theorem above).
- **Online.** It emits each token when it chooses it, so a streaming interface can show the text as it grows.
- **Beam search of width 1.** Greedy decoding is the special case $k = 1$ of [beam search](/beam-search/), and the limit of [temperature sampling](/temperature-sampling/) as the temperature goes to 0.
- **Repetition.** With trained models, greedy output often falls into loops that repeat a phrase. This is a measured behavior of trained models, not a property of the algorithm; [repetition penalty](/repetition-penalty/) and sampling are common fixes.

## Variants and improvements

- **Beam search.** Keep the $k$ best prefixes in place of one ([beam search](/beam-search/)). It costs about $k$ times as much and finds more probable outputs, but it is still not exact.
- **Sampling.** Draw the next token from $p$ or from a truncated $p$ ([temperature sampling](/temperature-sampling/), [top-k sampling](/top-k-sampling/), [nucleus sampling](/nucleus-sampling/)) to get varied text.
- **Contrastive search.** Score the top candidates by probability minus a similarity penalty against the context ([contrastive search](/contrastive-search/)).
- **Speculative decoding.** A small model proposes several tokens and the large model checks them in one call. With greedy acceptance the output is the same as greedy decoding of the large model, in fewer large calls ([speculative decoding](/speculative-decoding/)).
- **Constrained greedy decoding.** Mask the tokens that a grammar does not allow before the argmax ([grammar-constrained decoding](/grammar-constrained-decoding/)).

## When to use it

Use greedy decoding when a single short answer is needed and latency matters, for example a classification label, a short extraction, or a first baseline. It is also the usual choice for code and math answers where the model is confident at most steps. Use beam search for translation and speech recognition, where a more probable output is usually a better one, and sampling for open-ended text, where the most probable text is often dull or repetitive.

## Pitfalls

- **No end token.** A model can loop without choosing `</s>`. Always pass a limit $N$, and treat an output without `</s>` as unfinished.
- **Ties.** Two tokens with the same score give different outputs under different tie rules. Fix the rule (here, the first token in the order of $V$) if outputs must be reproducible. On a GPU, small differences in the order of floating-point sums can change which token is the largest.
- **Products of probabilities.** Multiplying probabilities underflows on long outputs. Add log probabilities.
- **A greedy output is not the mode.** Do not call the greedy output "the most likely output" of the model; the example above shows the difference.

## Implementations

The code takes the log probabilities of the model as given, as a function of the prefix, and implements the decoder around them; it does not run or train a network.

## History

Greedy search is the oldest and simplest way to decode a sequence model and has no single inventor. In neural translation it became the baseline against which beam search is measured. Stahlberg and Byrne 2019 ran exact search on a trained translation model and measured how far greedy and beam search are from the mode (see [inadequacy of the mode](/inadequacy-of-the-mode/)).

## References
