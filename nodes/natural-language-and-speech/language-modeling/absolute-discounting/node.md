---
tag: 5979BC
kind: technique
slug: absolute-discounting
name: Absolute discounting
aliases:
- absolute discount smoothing
- interpolated absolute discounting
area: natural-language-and-speech/language-modeling
level: core
summary: "Subtract a fixed discount D from every nonzero n-gram count and give the freed mass to the lower-order model, with D often set to N_1 / (N_1 + 2 N_2)."
prereqs: [n-gram-language-model, good-turing-estimation]
see_also: [kneser-ney-smoothing, modified-kneser-ney-smoothing, katz-backoff, witten-bell-smoothing, deleted-interpolation, simple-good-turing, laplace-smoothing, perplexity]
sources:
  - paper: "Hermann Ney, Ute Essen and Reinhard Kneser, On structuring probabilistic dependences in stochastic language modelling, Computer Speech and Language 8(1), 1994, pages 1 to 38"
    title: Ney, Essen and Kneser 1994
    locator: absolute discounting with interpolation and with backoff, and the estimate of the discount from the counts of counts by leaving one out
  - paper: doi:10.1006/csla.1999.0128
    title: Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Computer Speech and Language 13(4), 1999, pages 359 to 394
    locator: interpolated absolute discounting, the discount D = N_1/(N_1 + 2 N_2), and its relation to Kneser-Ney smoothing
  - paper: "Kenneth W. Church and William A. Gale, A comparison of the enhanced Good-Turing and deleted estimation methods for estimating probabilities of English bigrams, Computer Speech and Language 5(1), 1991"
    title: Church and Gale 1991
    locator: the measurement that held-out counts of English bigrams are close to the training counts minus a constant
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: chapter N-gram Language Models (draft of January 2026), absolute discounting and Kneser-Ney smoothing
---

Absolute discounting is a way to fill the zeros of an [n-gram language model](/n-gram-language-model/) by taking the same small amount $D$, usually less than 1, from the count of every n-gram that was seen and giving the total to the estimate of a shorter history. It rests on a fact found in large text collections: an n-gram seen $r$ times in one half of a corpus is seen about $r - 0.75$ times, on average, in a second half of the same size, nearly the same amount less for every $r \ge 2$. Unlike [Laplace smoothing](/laplace-smoothing/), it takes away a fixed amount, not a share; unlike [Katz backoff](/katz-backoff/), its discount does not depend on $r$; and unlike [Kneser-Ney smoothing](/kneser-ney-smoothing/), which is built on it, it uses the plain lower-order estimate.

## In plain words

A count from a sample is a little too high for the things you saw, because you saw them partly by luck. The surprise is that the excess is about the same for things seen twice and things seen twenty times. So take the same small amount off every count you have. For a word seen after some context, its count drops by, say, three quarters.

The amounts you took away add up. Give that total to a simpler model that looks at less context, and let it share the total among all words, also the words never seen in this context. A context followed by many different words gives away more, because more counts were cut.

## When it applies

It applies to any table of counts of the form "how often $w$ followed $h$" where most counts are small and a simpler model of $w$ exists: word and character n-gram models, models of DNA or protein sequences, and the escape estimates of text compressors. It needs a closed vocabulary $V$ that holds every predicted token, with `</s>` and `<unk>`. The discount $D$ is one number per order, set from the counts of counts or tuned on held-out text.

## The template

For a history $h$ with $c(h) > 0$, write $T(h) = N_{1+}(h \,\cdot)$ for the number of distinct words seen after $h$ and $h'$ for $h$ without its first token. With a discount $0 < D \le 1$, the interpolated form is

$$P_{\mathrm{abs}}(w \mid h) = \frac{\max(c(h w) - D,\, 0)}{c(h)} + \frac{D \, T(h)}{c(h)} \, P_{\mathrm{abs}}(w \mid h'),$$

and $P_{\mathrm{abs}}(w \mid h) = P_{\mathrm{abs}}(w \mid h')$ when $c(h) = 0$. The recursion ends at the unigrams, which are interpolated with the uniform distribution $1/|V|$ in the same way. Each seen n-gram gives up exactly $D$, so the first terms sum to $1 - D T(h)/c(h)$, and the lower order gets exactly the rest. Since $c(h) \ge T(h)$ and $D \le 1$, the weight $D T(h)/c(h)$ lies in $(0, 1]$.

Ney, Essen and Kneser (1994) estimated the discount of each order from the numbers $N_1$ and $N_2$ of n-grams seen once and twice:

$$D = \frac{N_1}{N_1 + 2 N_2}.$$

It comes from leaving one n-gram out at a time and maximizing the likelihood of the left-out n-grams; the formula is an approximation to that optimum that is easy to compute.

The backoff form uses the first term alone for seen words, and gives the freed mass $D T(h)/c(h)$ only to the unseen words, in proportion to the lower order and normalized as in [Katz backoff](/katz-backoff/).

## Classic examples

**A bigram model.** Train on "a b", "a c" and "b c", padded with `<s>` and `</s>`. There are 9 predicted tokens and 7 bigram types: `<s>` a and c `</s>` twice each, and `<s>` b, a b, a c, b c and b `</s>` once each. So $N_1 = 5$, $N_2 = 2$ and $D = 5/9$. For a simple example, let the lower order be the unigram estimate $c(w)/9$: a, b and c get $2/9$ and `</s>` gets $3/9$. After `<s>`, with $c = 3$ and $T = 2$, the freed mass is $(5/9) \cdot 2/3 = 10/27$. The rows give $P(w \mid h)$:

| history $h$ | $w$ = `</s>` | $w$ = a | $w$ = b | $w$ = c |
|---|---|---|---|---|
| `<s>` | 10/81 | 137/243 | 56/243 | 20/243 |
| a | 5/27 | 10/81 | 28/81 | 28/81 |
| b | 11/27 | 10/81 | 10/81 | 28/81 |
| c | 22/27 | 5/81 | 5/81 | 5/81 |

For example, $P(a \mid \langle s \rangle) = (2 - 5/9)/3 + (10/27)(2/9) = 137/243$. The history c was followed only by `</s>`, so it frees only $D \cdot 1/2 = 5/18$ of its mass. Each row sums to 1.

**Kneser-Ney smoothing.** [Kneser-Ney smoothing](/kneser-ney-smoothing/) is interpolated absolute discounting with one change: the lower order counts the number of distinct contexts of a word, not its frequency. On the same corpus with $D = 3/4$, it gives $P(a \mid \langle s \rangle) = 41/84$.

**Good-Turing as a near-constant discount.** For English bigrams, Church and Gale (1991) found that the [Good-Turing](/good-turing-estimation/) adjusted counts satisfy $r - r^* \approx 0.75$ for $r \ge 2$. Absolute discounting uses this constant directly, which avoids the noise of the $N_r$ at large $r$.

## Variations

- **Several discounts.** [Modified Kneser-Ney smoothing](/modified-kneser-ney-smoothing/) uses three discounts, $D_1$, $D_2$ and $D_{3+}$, for the counts 1, 2 and 3 or more, set from $N_1$ to $N_4$. The freed mass is then $(D_1 N_1(h \cdot) + D_2 N_2(h \cdot) + D_{3+} N_{3+}(h \cdot))/c(h)$.
- **Tuned discounts.** Choose $D$ for each order to minimize the [perplexity](/perplexity/) of held-out text, by a line search.
- **Backoff instead of interpolation.** Use the discounted count alone for seen words and normalize the lower order over the unseen words. The two forms give different numbers, so say which one a result uses.
- **Discounts per history count.** Let $D$ depend on a bucket of $c(h)$, in the spirit of [deleted interpolation](/deleted-interpolation/).

## Pitfalls

- **$D$ above 1.** A count of 1 cannot give up more than 1. With $D > 1$ the clipped term $\max(c - D, 0)$ frees less than $D$ per n-gram, and the rows no longer sum to 1. Keep $D \le 1$, or free $\min(c(h w), D)$ per n-gram and use that total.
- **No n-gram seen twice.** If $N_2 = 0$, the formula gives $D = 1$, so the n-grams seen once get nothing from their own count. Check the counts of counts on small data.
- **Unseen histories.** If $c(h) = 0$, the template has $0/0$. Use the lower order directly.
- **The lower order.** The plain lower order gives a word like "Francisco", common but only after "San", a high probability after every history. Kneser-Ney smoothing fixes this with continuation counts.
- **One $D$ per order.** The n-grams of each order have their own $N_1$ and $N_2$, so each order gets its own discount.

## Exercises

1. Show that the row of a history $h$ with $c(h) > 0$ sums to 1 when $0 < D \le 1$ and the lower order is a distribution on $V$.
2. In the example above, compute $P(c \mid a)$ step by step and check the value $28/81$.
3. A model has $N_1 = 2\,000\,000$ bigram types seen once and $N_2 = 600\,000$ seen twice. Compute $D$. How much mass does a history seen 100 times with 40 different followers give to the lower order?
4. Show that $D = N_1/(N_1 + 2N_2)$ always lies in $(0, 1]$ when $N_1 > 0$, and find when it equals 1.
5. Write the backoff form for a bigram model and give the backoff weight $\alpha(h)$ that makes each row sum to 1.

## References
