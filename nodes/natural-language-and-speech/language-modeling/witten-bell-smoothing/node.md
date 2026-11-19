---
tag: FME53F
kind: algorithm
slug: witten-bell-smoothing
name: Witten-Bell smoothing
aliases:
- Witten-Bell discounting
- Witten-Bell interpolation
area: natural-language-and-speech/language-modeling
level: core
summary: "Interpolate each n-gram estimate with the lower order, giving the lower order the weight T(h)/(c(h) + T(h)), where T(h) is the number of distinct words seen after the history h."
model: word-ram
complexity:
  vars: {n: the order of the model, N: the number of training tokens}
  time: {worst: "Θ(n N)"}
  space: {extra: "Θ(n N)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1991
  people: [Ian H. Witten, Timothy C. Bell]
  note: Witten and Bell studied how to estimate the chance of a novel symbol in adaptive text compression. Language modeling took over the estimate T/(c + T) as a smoothing method named after them.
prereqs: [n-gram-language-model, maximum-likelihood-estimation]
see_also: [jelinek-mercer-smoothing, deleted-interpolation, kneser-ney-smoothing, katz-backoff, absolute-discounting, good-turing-estimation, prediction-by-partial-matching, perplexity]
sources:
  - paper: doi:10.1109/18.87000
    title: Ian H. Witten and Timothy C. Bell, The zero-frequency problem, estimating the probabilities of novel events in adaptive text compression, IEEE Transactions on Information Theory 37(4), 1991, pages 1085 to 1094
    locator: the escape estimate based on the number of distinct symbols seen in a context, and its comparison with other escape methods
  - paper: doi:10.1006/csla.1999.0128
    title: Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Computer Speech and Language 13(4), 1999, pages 359 to 394
    locator: Witten-Bell smoothing as interpolation with the weight N_1+(h .)/(N_1+(h .) + c(h)), and its measured performance
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: chapter N-gram Language Models (draft of January 2026), smoothing and interpolation
---

Witten-Bell smoothing is a way to fill the zeros of an [n-gram language model](/n-gram-language-model/). For each history $h$ (the words before the one we predict), it mixes the counts seen after $h$ with the estimate of the shorter history, and it sets the mix from one number: $T(h)$, how many different words were seen after $h$. A history followed by many different words gets a large share from the lower order, because a new word after it is likely; a history that is always followed by the same word keeps almost all of its own estimate. Unlike [Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/) and [deleted interpolation](/deleted-interpolation/), it fits no weights on held-out data, and unlike [Kneser-Ney smoothing](/kneser-ney-smoothing/) it subtracts no fixed discount.

## In plain words

Read a text and watch what comes after one word, say "the". Each time a word follows "the" that has never followed it before, count one surprise. The number of surprises, over the number of times "the" was followed by anything plus the surprises, is a good guess for the chance that the next word after "the" is again a surprise.

Witten-Bell gives exactly that share of the probability to a simpler model that ignores "the", and keeps the rest for the words already seen after "the", in proportion to their counts. The simpler model is built the same way, from a shorter context, down to the case where every word is equally likely.

## The problem

The training text is a list of sentences over a vocabulary $V$ that holds every predicted token: the words, the end marker `</s>` and the unknown word `<unk>`. Each sentence is padded with $n - 1$ start markers `<s>` on the left and one `</s>` on the right. For a history $h$ of up to $n - 1$ tokens, $c(h w)$ is the number of times $h$ is followed by $w$, $c(h) = \sum_w c(h w)$, and $T(h) = N_{1+}(h \,\cdot)$ is the number of distinct $w$ with $c(h w) > 0$. Write $h'$ for $h$ without its first token, and $\epsilon$ for the empty history, so that $c(\epsilon) = N$ is the number of predicted tokens. The task is a conditional distribution $P(w \mid h)$ over $V$ for every history, with no zeros.

## The algorithm

The interpolated Witten-Bell estimate is

$$P_{WB}(w \mid h) = \frac{c(h w) + T(h) \, P_{WB}(w \mid h')}{c(h) + T(h)} \quad \text{if } c(h) > 0,$$

and $P_{WB}(w \mid h) = P_{WB}(w \mid h')$ if $c(h) = 0$. Below the unigrams sits the uniform distribution $1/|V|$. In the form of [Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/), the weight of the maximum likelihood estimate is $\lambda(h) = c(h) / (c(h) + T(h))$, and the lower order gets $1 - \lambda(h) = T(h) / (c(h) + T(h))$.

```pseudo id=main
P-WB(w, h)                              ▷ c, T counted once on the training text
L1  if h = ε then lower ← 1 / |V| else lower ← P-WB(w, h')
L2  if c(h) = 0 then return lower
L3  λ ← c(h) / (c(h) + T(h))
L4  return λ c(h w) / c(h) + (1 - λ) lower
```

Line L1 gets the estimate of the shorter history. Line L2 skips a history that never occurred, so the whole mass goes down one order. Line L3 is the Witten-Bell weight. Line L4 mixes the two estimates. A model of order $n$ calls P-WB with the last $n - 1$ tokens before $w$.

## Example

Train a bigram model ($n = 2$) on the three sentences "a b", "a c" and "b c", with $V = \{a, b, c, \langle /s \rangle\}$. The padded sentences give $N = 9$ predicted tokens: a, b and c twice each and `</s>` three times. Every token of $V$ occurs, so $T(\epsilon) = 4$.

The unigram level mixes the counts with the uniform $1/4$: $P(a) = (2 + 4 \cdot \tfrac14)/(9 + 4) = 3/13$, the same for b and c, and $P(\langle /s \rangle) = (3 + 1)/13 = 4/13$.

| history $h$ | followers and counts | $c(h)$ | $T(h)$ | $P(\langle /s \rangle \mid h)$ | $P(a \mid h)$ | $P(b \mid h)$ | $P(c \mid h)$ |
|---|---|---|---|---|---|---|---|
| `<s>` | a 2, b 1 | 3 | 2 | 8/65 | 32/65 | 19/65 | 6/65 |
| a | b 1, c 1 | 2 | 2 | 2/13 | 3/26 | 19/52 | 19/52 |
| b | c 1, `</s>` 1 | 2 | 2 | 21/52 | 3/26 | 3/26 | 19/52 |
| c | `</s>` 2 | 2 | 1 | 10/13 | 1/13 | 1/13 | 1/13 |

For example, $P(b \mid a) = (1 + 2 \cdot \tfrac{3}{13})/(2 + 2) = 19/52$, and $P(\langle /s \rangle \mid c) = (2 + 1 \cdot \tfrac{4}{13})/(2 + 1) = 10/13$. After c only `</s>` was seen, so $T(c) = 1$ and the history c gives its own estimate the weight $\lambda = 2/3$. After a two different words were seen in two tokens, so a gives half its mass to the unigram level. Each row sums to 1. The sentence "a b c" gets $\tfrac{32}{65} \cdot \tfrac{19}{52} \cdot \tfrac{19}{52} \cdot \tfrac{10}{13} = 1444/28561$.

If `<unk>` is added to $V$, the uniform level becomes $1/5$, $T(\epsilon)$ stays 4, and `<unk>` gets $P(\langle \text{unk} \rangle) = (4/5)/13 = 4/65$ and $P(\langle \text{unk} \rangle \mid a) = 2/65$.

## Correctness

**Every row is a distribution.** By induction on the length of $h$. The uniform level sums to 1. If $c(h) = 0$ the row is the row of $h'$. If $c(h) > 0$, sum line L4 over $w \in V$: $\lambda \sum_w c(h w)/c(h) + (1 - \lambda) \sum_w P_{WB}(w \mid h') = \lambda + (1 - \lambda) = 1$. The first sum is 1 because every token seen after $h$ is in $V$.

**No zeros.** The uniform level is positive. If $c(h) > 0$ then $T(h) \ge 1$, so $1 - \lambda > 0$ and line L4 is positive whenever the lower order is. So $P_{WB}(w \mid h) > 0$ for every $w \in V$ and every history.

**The meaning of the weight.** Read the text after $h$ token by token. The number of tokens that are the first of their type is $T(h)$, out of $c(h)$ tokens. Then $T(h) / (c(h) + T(h))$ is the escape estimate of Witten and Bell for the chance that the next token after $h$ is new, and line L4 gives that share to the lower order.

## Complexity

One pass over the padded training text with a [hash table](/hash-table/) or a [trie](/trie/) counts $c(h w)$, $c(h)$ and $T(h)$ for every order: $\Theta(n N)$ expected time, and $\Theta(n N)$ space in the worst case, since each token adds at most one new n-gram per order. $T(h)$ is counted when an n-gram is seen for the first time. One query P-WB$(w, h)$ makes $n$ calls, so it takes $\Theta(n)$ expected time; a full row takes $\Theta(n |V|)$. With exact fractions, as in the implementation, the denominators grow with $n$; in practice the model stores floating point log probabilities.

## Properties

- **No free parameters.** Everything comes from the counts. There is no held-out set and no discount to tune.
- **Adaptive to the history.** A history with a fixed follower (like "San" before "Francisco") gets little from the lower order; a history with many followers (like "the") gets much.
- **Interpolated.** Every n-gram, seen or not, gets some mass from the lower order, so seen n-grams are discounted by a share of the lower order and unseen ones are not all equal.
- **Recursive and exact.** The recursion has depth $n$, and with fractions the rows sum to 1 exactly.
- **Strong discount for small counts.** A history seen once gives half its mass to the lower order, since $c(h) = T(h) = 1$.

## Variants and improvements

- **The backoff form.** Use $c(h w)/(c(h) + T(h))$ for the seen words and share $T(h)/(c(h) + T(h))$ among the unseen words in proportion to the lower order, normalized as in [Katz backoff](/katz-backoff/).
- **A scaled weight.** Replace $T(h)$ by $\beta T(h)$ with a constant $\beta$ tuned on held-out data.
- **Escape methods in compression.** In [prediction by partial matching](/prediction-by-partial-matching/) the same estimate decides when to escape from a long context to a shorter one. There, the lower order often excludes the symbols already seen in the longer context.
- **Kneser-Ney.** [Kneser-Ney smoothing](/kneser-ney-smoothing/) also uses $T(h)$, but as the number of discounts of a fixed size $D$, and it uses continuation counts at the lower orders. Chen and Goodman (1999) found it better than Witten-Bell.

## When to use it

Use it when you need a smoothed n-gram model with no tuning and no held-out data, for example for small or quickly changing text, for a character model, or as a baseline. It is simple to implement, it never gives a zero, and it adapts to the diversity of each history. For a model of words trained on a large corpus, [modified Kneser-Ney smoothing](/modified-kneser-ney-smoothing/) usually gives a lower [perplexity](/perplexity/).

## Pitfalls

- **$T(h)$ counts types, not tokens.** It is the number of different words after $h$, not the number of times $h$ was followed by something.
- **The vocabulary of the base level.** The uniform level divides by $|V|$, which must hold `</s>` and `<unk>`. If $V$ is only the words seen in training, an unseen word in the test text gets no probability.
- **`<s>` is not predicted.** It is part of histories only. It must not be in $V$, and it is not counted in $N$.
- **Unseen histories.** If $c(h) = 0$, the formula has $0/0$. The rule is to use the lower order directly.
- **Mixing up the two forms.** The interpolated and the backoff forms give different numbers. Say which one a result uses.

## Implementations

## History

Witten and Bell (1991) studied the zero-frequency problem in adaptive text compression: a coder that predicts the next symbol from its context must give some probability to a symbol never seen in that context. They compared several estimates of this escape probability, among them the one based on the number of distinct symbols seen in the context. Language modeling took the estimate over as Witten-Bell smoothing, and Chen and Goodman (1999) described it as a form of Jelinek-Mercer interpolation with the weight $T(h)/(c(h) + T(h))$ and compared it with the other classical methods.

## References
