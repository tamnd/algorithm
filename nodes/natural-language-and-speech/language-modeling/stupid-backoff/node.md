---
tag: 0ZTM89
kind: algorithm
slug: stupid-backoff
name: Stupid backoff
aliases:
- Brants stupid backoff
area: natural-language-and-speech/language-modeling
level: advanced
summary: "Unnormalized scores for very large n-gram models: the relative frequency if seen, else 0.4 times the score of the shorter n-gram."
model: word-ram
complexity:
  vars: {n: the order of the model, N: the number of predicted training tokens, V: the vocabulary}
  time: {build: "Θ(n N)", query: "Θ(n)"}
  space: {extra: "Θ(n N)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 2007
  people: [Thorsten Brants, Ashok C. Popat, Peng Xu, Franz J. Och, Jeffrey Dean]
  note: Brants and colleagues at Google used it for n-gram models built from web text with MapReduce, for machine translation.
prereqs: [n-gram-language-model]
see_also: [katz-backoff, kneser-ney-smoothing, n-gram-language-model, perplexity, mapreduce-model, entropy-based-ngram-pruning, bloom-filter, hash-table]
sources:
  - paper: "Thorsten Brants, Ashok C. Popat, Peng Xu, Franz J. Och and Jeffrey Dean, Large language models in machine translation, Proceedings of EMNLP-CoNLL 2007, pages 858 to 867"
    title: Brants, Popat, Xu, Och and Dean 2007
    locator: equations 5 and 6 (the score S and its recursion), footnote 2 (the value 0.4 was set by hand), Section 7.3 (no perplexity for stupid backoff), Section 7.4 (BLEU against Kneser-Ney as the data grows)
---

Stupid backoff is a way to use an [n-gram language model](/n-gram-language-model/) built from far more text than a normal smoothing method can handle. If the n-gram $h w$ was seen, its score is the relative frequency $c(h w)/c(h)$. If not, the score is a fixed factor $\alpha = 0.4$ times the score of $w$ after the shorter history. There is no discount and no normalization, so the scores are not probabilities, and Brants and colleagues write $S$ for them instead of $P$. In exchange, the model needs nothing but raw counts, which are easy to compute and to look up in a distributed system. On very large data it gave machine translation quality close to that of [Kneser-Ney smoothing](/kneser-ney-smoothing/).

## In plain words

To score the next word, look at what followed the same last few words in the training text. If the word appeared there, its score is the fraction of times it came next.

If it never came next, forget the oldest word of the history and look again with the shorter history. Each time you do this, multiply the score by 0.4, as a fixed penalty for having less context. With no history left, the score is just how often the word appears in the whole text.

The scores do not add up to one. That is fine for a translation system that only compares candidate sentences, and it makes the model very cheap to build from huge amounts of text.

## The problem

The training corpus is a list of sentences. Each sentence is padded with $n - 1$ copies of <s> on the left and one </s> on the right; </s> is predicted and counted, <s> is never predicted. Write $c(g)$ for the number of times the m-gram $g$ ($1 \le m \le n$) ends at a predicted token, $N$ for the number of predicted tokens and $V$ for the set of predicted tokens. For a history $h$ write $c(h) = \sum_x c(h x)$, the number of times $h$ is followed by a predicted token, and $h'$ for $h$ without its first token.

The task is to give a score to every word $w$ after every history $h$ of $n - 1$ tokens. The score must be cheap to compute from raw counts held on many machines, it must prefer words seen after longer histories, and it does not have to be a probability. The definition of Brants and colleagues is

$$S(w \mid h) = \begin{cases} \dfrac{c(h w)}{c(h)} & \text{if } c(h w) > 0, \\[1ex] \alpha\, S(w \mid h') & \text{otherwise,} \end{cases} \qquad S(w) = \frac{c(w)}{N},$$

with $\alpha = 0.4$.

## The algorithm

Training is one pass of counting: at each predicted position, add one to the count of every m-gram that ends there, for $m = 1, \ldots, n$, and one to the count of its history. At web scale this is a MapReduce word count over n-grams. A query walks down from the full history until it finds a seen n-gram.

```pseudo id=main
SB-SCORE(w, h)                         ▷ h holds the last m - 1 tokens
L1  if c(h w) > 0 then
L2      return c(h w) / c(h)
L3  if h is empty then return 0        ▷ w was never seen
L4  return α · SB-SCORE(w, h')
```

The implementation keeps $c(h)$ in its own table. Brants and colleagues divide by the raw frequency of the history; the two are equal for every history without <s>, because such a history is always followed by a predicted token, at least </s>.

## Example

Take the three sentences "a b", "a c" and "b c" with $n = 2$ and $\alpha = 2/5$. There are $N = 9$ predicted tokens: a, b and c twice each, and </s> three times, so the unigram scores are 2/9, 2/9, 2/9 and 3/9. After <s>, a was seen twice and b once out of $c(\text{<s>}) = 3$; c and </s> were not seen there, so they back off to $\frac25 \cdot \frac29 = \frac4{45}$ and $\frac25 \cdot \frac39 = \frac2{15}$. The whole model is:

| $h$ | a | b | c | </s> | sum |
|---|---|---|---|---|---|
| <s> | 2/3 | 1/3 | 4/45 | 2/15 | 11/9 |
| a | 4/45 | 1/2 | 1/2 | 2/15 | 11/9 |
| b | 4/45 | 4/45 | 1/2 | 1/2 | 53/45 |
| c | 4/45 | 4/45 | 4/45 | 1 | 19/15 |

Every row sums to more than 1: the seen words alone already sum to 1, and the backed off words add to it. With $n = 3$ on the same text, the history <s> c was never seen; </s> then gets $\frac25 \cdot 1$ and each other word $\frac4{25} \cdot \frac29 = \frac8{225}$, which sums to 38/75, less than 1.

## Correctness

There is no distribution to be correct about, so the proof shows what the scores are. The counting loop gives $c(g)$ and $c(h)$ as defined, because the padding gives every predicted position a full window of $n$ tokens. Lines L1 to L4 compute $S(w \mid h)$ by induction on the length of $h$, and the division at line L2 is safe because $c(h) \ge c(h w) > 0$. Every word of $V$ gets a score in $(0, 1]$. After a seen history the scores sum to at least 1, since the seen words give exactly $\sum_{w} c(h w)/c(h) = 1$. After a history of length $m - 1$ they sum to at most $1 + \alpha + \cdots + \alpha^{m-1}$, which is below $1/(1 - \alpha) = 5/3$ for $\alpha = 0.4$.

## Complexity

Training visits each of the $N$ predicted tokens once and updates $n$ m-gram counts and $n$ history counts, so it takes $\Theta(n N)$ expected operations with [hash tables](/hash-table/), and the tables hold at most $n N$ keys. A query makes at most $n$ lookups of $c(h w)$ and one of $c(h)$, $\Theta(n)$ operations. Each operation hashes a tuple of up to $n$ tokens, so in word operations each bound is a factor $n$ larger. A query needs no data beyond the counts, while a normalized backoff model also stores a weight for every history.

## Properties

- **Not a distribution.** The scores after a history do not sum to 1, and the sum differs from row to row. The model has no [perplexity](/perplexity/).
- **Raw counts only.** There is no discount, no count of counts and no per-history weight to compute, so training is a single counting job.
- **A fixed backoff factor.** One constant $\alpha$ for all orders and all histories; 0.4 was set by hand.
- **Bounded scores.** Every score of a seen word is in $(0, 1]$, and a backed off score is at most $\alpha$.
- **Exact.** All scores are ratios of integer counts times powers of $\alpha$.

## Variants and improvements

- **[Katz backoff](/katz-backoff/)** has the same shape but discounts the seen counts and picks a weight $\alpha(h)$ for each history so that the probabilities sum to 1.
- **Other factors.** $\alpha$ is a parameter; a different value per order, tuned on held-out data, is a simple change.
- **Compact storage.** Very large count tables are often stored with lossy or randomized structures such as a [Bloom filter](/bloom-filter/), and pruned before use, as in [entropy-based pruning](/entropy-based-ngram-pruning/) for normalized models.
- **Normalizing after the fact.** Dividing each row by its sum gives a distribution, but it costs a sum over $V$ for each history and removes the reason to use the method.

## When to use it

Use it when the training text is so large that counting is the only affordable step, and the model is used only to compare candidates, for example as a feature in a machine translation decoder. Brants and colleagues found it about 1 BLEU point below Kneser-Ney on the same smaller data, with the gap closing as the data grew. Do not use it when you need probabilities: for [perplexity](/perplexity/), for speech recognition with a calibrated score, or to mix with other models. Then use [Kneser-Ney](/kneser-ney-smoothing/) or [Katz backoff](/katz-backoff/).

## Pitfalls

- **Reporting perplexity.** The scores are not probabilities, so a perplexity computed from them has no meaning.
- **The wrong denominator.** Dividing by the count of the history as a whole n-gram includes positions where it is not followed by a predicted token, for example the pads at the start of a sentence.
- **Unseen words.** A word not in the training text scores 0 at every order. Map such words to <unk>.
- **Comparing across histories.** Since rows sum to different totals, the score of a word after one history cannot be compared with its score after another as if they were probabilities.
- **Underflow.** The scores of a long sentence multiply to a number below the smallest double. Sum logs instead.

## Implementations

## History

Brants, Popat, Xu, Och and Dean (2007) built n-gram models from up to 1.8 trillion tokens of web text for the Google machine translation system. Kneser-Ney smoothing needs counts of counts and per-history weights, which are expensive at that scale, so they used raw relative frequencies with a fixed backoff factor and called the method stupid backoff. They counted with MapReduce on about 1500 machines in about a day, stored the counts across many servers, and showed that the BLEU score of stupid backoff kept growing with the data, until with the web data it was 0.82 BLEU points above the best Kneser-Ney model on smaller data.

## References
