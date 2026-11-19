---
tag: 99DA92
kind: algorithm
slug: katz-backoff
name: Katz backoff
aliases:
- Katz smoothing
- Katz back-off model
area: natural-language-and-speech/language-modeling
level: core
summary: "An n-gram model that uses discounted counts for the n-grams it has seen and backs off to the shorter history, scaled by a weight alpha(h), for the ones it has not."
model: word-ram
complexity:
  vars: {n: the order of the model, N: the number of training tokens}
  time: {worst: "Θ(n N)"}
  space: {extra: "Θ(n N)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1987
  people: [Slava M. Katz]
  note: Katz gave the method in a two-page paper in IEEE Transactions on Acoustics, Speech, and Signal Processing, for the language model of a speech recognizer.
prereqs: [n-gram-language-model, good-turing-estimation]
see_also: [simple-good-turing, absolute-discounting, kneser-ney-smoothing, stupid-backoff, witten-bell-smoothing, deleted-interpolation, entropy-based-ngram-pruning, perplexity]
sources:
  - paper: doi:10.1109/TASSP.1987.1165125
    title: Slava M. Katz, Estimation of probabilities from sparse data for the language model component of a speech recognizer, IEEE Transactions on Acoustics, Speech, and Signal Processing 35(3), 1987, pages 400 to 401
    locator: the backoff recursion, the Good-Turing discounts for the counts up to k with their renormalization, and the choice k = 5
  - paper: doi:10.1006/csla.1999.0128
    title: Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Computer Speech and Language 13(4), 1999, pages 359 to 394
    locator: Katz smoothing, its discount ratios d_r, and its performance against the other methods
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999
    locator: Chapter 6, Section 6.3 (combining estimators, with Katz's backing-off)
  - paper: doi:10.1093/biomet/40.3-4.237
    title: I. J. Good, The population frequencies of species and the estimation of population parameters, Biometrika 40(3-4), 1953, pages 237 to 264
    locator: the adjusted count (r+1) N_(r+1) / N_r and the unseen mass N_1 / N
---

Katz backoff turns the counts of an [n-gram language model](/n-gram-language-model/) into probabilities that are never zero. If the n-gram was seen in training, the model uses its count, made a little smaller by a [Good-Turing](/good-turing-estimation/) discount. If it was not seen, the model drops the oldest word of the history and asks the shorter model, and it scales that answer by a weight $\alpha(h)$ so that the probabilities after each history still sum to 1. It is a backoff method: unlike [Witten-Bell smoothing](/witten-bell-smoothing/) or [deleted interpolation](/deleted-interpolation/), it uses the lower order only for the words not seen after the history, and unlike [absolute discounting](/absolute-discounting/) it takes its discounts from the counts of counts.

## In plain words

To guess the next word after "the red", look at what followed "the red" in the training text. If the word you ask about followed it, use how often it did, but trust the count a little less than it says, because small counts are lucky. The small amount you took away from these words is put aside.

If the word never followed "the red", forget "the" and ask how likely the word is after "red" alone, and if needed after nothing at all. Then share the amount put aside among all the words that never followed "the red", in proportion to these simpler guesses. Every word gets a chance, and the chances still add up to one.

## The problem

The training text is a list of sentences, each padded with $n - 1$ start markers `<s>` on the left and one `</s>` on the right. The vocabulary $V$ is the set of predicted tokens, which holds `</s>` and, after rare words are mapped to it, `<unk>`. For a history $h$ of up to $n - 1$ tokens, $c(h w)$ is the number of times $h$ is followed by $w$ and $c(h) = \sum_w c(h w)$. Write $h'$ for $h$ without its first token and $\epsilon$ for the empty history, with $c(\epsilon) = N$. The task is a distribution $P(w \mid h)$ over $V$ for every history, with positive values for the seen n-grams.

## The algorithm

For each order $m \ge 2$, let $N_r$ be the number of m-grams seen exactly $r$ times. Katz keeps the counts above a cut-off $k$ (he used $k = 5$) and discounts the counts $1 \le r \le k$ by the ratio

$$d_r = \frac{r^*/r - \mu}{1 - \mu}, \qquad r^* = (r+1) \frac{N_{r+1}}{N_r}, \qquad \mu = \frac{(k+1) N_{k+1}}{N_1}.$$

These ratios are the Good-Turing ratios $r^*/r$, changed so that the counts above $k$ are not discounted and the total mass taken away is still $N_1$, the Good-Turing mass of the unseen m-grams. For $r > k$, $d_r = 1$. The unigrams use the maximum likelihood estimate $c(w)/N$.

```pseudo id=main
P-KATZ(w, h)                              ▷ c and the d_r counted once on the training text
L1  if h = ε then return c(w) / N
L2  if c(h) = 0 then return P-KATZ(w, h')
L3  if c(h w) > 0 then
L4      return d_{c(h w)} c(h w) / c(h)
L5  β(h) ← 1 - Σ_{v : c(h v) > 0} d_{c(h v)} c(h v) / c(h)    ▷ the mass taken from the seen words
L6  γ(h) ← 1 - Σ_{v : c(h v) > 0} P-KATZ(v, h')              ▷ the lower-order mass of the unseen words
L7  α(h) ← β(h) / γ(h)
L8  return α(h) P-KATZ(w, h')
```

Line L4 is the discounted estimate of a seen n-gram. Lines L5 to L7 compute the backoff weight, which depends only on $h$ and is stored once per history. Line L8 gives an unseen word its lower-order probability, scaled so that the unseen words of $h$ share exactly $\beta(h)$.

## Example

Train a bigram model on the four sentences "a a b", "a b c", "a" and "c a", with $k = 2$. There are $N = 13$ predicted tokens: a 5 times, `</s>` 4 times, b and c twice each. The nine bigram types have the counts `<s>` a 3, a b 2, a `</s>` 2, and 1 for each of `<s>` c, a a, b c, b `</s>`, c a and c `</s>`. So $N_1 = 6$, $N_2 = 2$, $N_3 = 1$, and

$$\mu = \frac{3 \cdot 1}{6} = \frac12, \quad r^*_1 = \frac{2 \cdot 2}{6} = \frac23, \quad r^*_2 = \frac{3 \cdot 1}{2} = \frac32, \quad d_1 = \frac{2/3 - 1/2}{1/2} = \frac13, \quad d_2 = \frac{3/4 - 1/2}{1/2} = \frac12.$$

The discounts take away $6 \cdot 1 \cdot \tfrac23 + 2 \cdot 2 \cdot \tfrac12 = 6 = N_1$ counts in all. After the history a, seen 5 times, the seen words get a $\tfrac13 \cdot \tfrac15 = \tfrac1{15}$, b $\tfrac12 \cdot \tfrac25 = \tfrac15$ and `</s>` $\tfrac15$. So $\beta(a) = 8/15$. The only unseen word is c, with unigram probability $2/13$, so $\gamma(a) = 2/13$, $\alpha(a) = 52/15$ and $P(c \mid a) = 8/15$.

| history $h$ | $c(h)$ | $\alpha(h)$ | $P(\langle /s \rangle \mid h)$ | $P(a \mid h)$ | $P(b \mid h)$ | $P(c \mid h)$ |
|---|---|---|---|---|---|---|
| `<s>` | 4 | 13/36 | 1/9 | 3/4 | 1/18 | 1/12 |
| a | 5 | 52/15 | 1/5 | 1/15 | 1/5 | 8/15 |
| b | 2 | 26/21 | 1/6 | 10/21 | 4/21 | 1/6 |
| c | 2 | 13/6 | 1/6 | 1/6 | 1/3 | 1/3 |

The count 3 of `<s>` a is above $k$, so it is not discounted: $P(a \mid \langle s \rangle) = 3/4$. Each row sums to 1. The sentence "a b" gets $\tfrac34 \cdot \tfrac15 \cdot \tfrac16 = 1/40$. Note that $\alpha(h)$ is not a probability; it can be larger than 1.

## Correctness

**Every row is a distribution.** If some word is unseen after $h$ and $\gamma(h) > 0$, the seen words get $1 - \beta(h)$ by line L5, and the unseen words get $\alpha(h) \sum_{\text{unseen}} P(w \mid h') = \alpha(h) \gamma(h) = \beta(h)$, by induction on the length of $h$ (the lower row sums to 1). So the row sums to 1. If every word of $V$ was seen after $h$, there is nothing to back off to, and the implementation keeps the undiscounted estimates $c(h w)/c(h)$ for that history.

**The discounted mass is $N_1$.** When the ratios are valid, $\sum_{r=1}^{k} N_r \, r (1 - d_r) = N_1$. This is the Good-Turing estimate of the total count of the unseen m-grams, so Katz gives the unseen events the same total as Good-Turing, but takes it only from the counts $1$ to $k$.

## Complexity

One pass over the training text with a [hash table](/hash-table/) or a [trie](/trie/) counts all m-grams for $m \le n$ in $\Theta(n N)$ expected time and $\Theta(n N)$ space. The counts of counts and the $d_r$ take time linear in the number of n-gram types. The weight $\alpha(h)$ sums over the words seen after $h$, so all weights together take time linear in the number of n-gram types times $n$. After that, one query takes $\Theta(n)$ expected time. Models are usually stored in the ARPA format, which holds $\log_{10} P$ for each seen n-gram and $\log_{10} \alpha(h)$ for each history.

## Properties

- **Backoff, not interpolation.** A seen n-gram uses only its own discounted count; the lower order is used only for unseen words.
- **Large counts are trusted.** Counts above $k$ are kept, since the Good-Turing ratio $r^*/r$ is close to 1 there and the $N_r$ are noisy.
- **Same unseen mass as Good-Turing.** The discounts take away exactly $N_1$ counts per order.
- **Not monotone.** The ratios $d_r$ come from the noisy $N_r$, so a larger count can get a larger discount.
- **Can raise unseen words above seen ones.** In the example, the unseen bigram a c gets $8/15$ while the seen a a gets $1/15$, because c is frequent after other histories.

## Variants and improvements

- **Smoothed counts of counts.** Compute the $r^*$ with [simple Good-Turing](/simple-good-turing/) instead of the raw formula.
- **[Absolute discounting](/absolute-discounting/)** with backoff replaces $d_r$ by a fixed discount, $r - D$.
- **[Kneser-Ney smoothing](/kneser-ney-smoothing/)** backs off to a continuation distribution, which counts in how many contexts a word occurs, not how often. Chen and Goodman (1999) found it better than Katz.
- **[Stupid backoff](/stupid-backoff/)** drops the normalization: it backs off with a fixed factor such as 0.4 and gives scores that do not sum to 1, which is enough for very large corpora.
- **Pruning.** [Entropy-based pruning](/entropy-based-ngram-pruning/) removes n-grams from a backoff model and recomputes the $\alpha(h)$.

## When to use it

Use it for a word n-gram model when you want a normalized backoff model in the ARPA format, for example for a speech recognizer or for [lattice rescoring](/lattice-rescoring/). On most data [modified Kneser-Ney smoothing](/modified-kneser-ney-smoothing/) gives a lower [perplexity](/perplexity/), but Katz models are simple and well understood. For small vocabularies, such as characters or DNA, where almost every n-gram is seen, the discounts matter less and a simple interpolated model is enough.

## Pitfalls

- **Invalid discounts.** The formula needs $N_1 > 0$, $\mu < 1$, and every $d_r$ in $(0, 1]$. On small or filtered data this fails. The implementation then leaves that order undiscounted.
- **$k = 1$ deletes the singletons.** With $k = 1$, $r^*_1 = 2 N_2 / N_1 = \mu$, so $d_1 = 0$ and every n-gram seen once gets probability 0 from its own count. Use $k \ge 2$.
- **No unseen words.** If every word of $V$ follows $h$, then $\gamma(h) = 0$ and $\alpha(h)$ is undefined. Keep the undiscounted estimates for such a history.
- **Discounts per order.** The $N_r$ and the $d_r$ are computed separately for each order $m$.
- **`<s>` and `</s>`.** `<s>` is never predicted and is not counted in $N$; `</s>` is predicted and counted. A history that holds only `<s>` is seen once per sentence.

## Implementations

## History

Slava Katz published the method in 1987 in a two-page correspondence in the IEEE Transactions on Acoustics, Speech, and Signal Processing, for the language model of a speech recognizer. He combined two ideas: the Good-Turing estimate of the unseen mass, and the use of a shorter context when the longer one has no data, with a normalization that keeps the model a distribution. The backoff model and its file format became standard in speech recognition toolkits. Chen and Goodman (1999) compared it with the other classical methods and found it behind Kneser-Ney smoothing.

## References
