---
tag: R2ZAVZ
kind: algorithm
slug: modified-kneser-ney-smoothing
name: Modified Kneser-Ney smoothing
aliases:
- Chen-Goodman smoothing
area: natural-language-and-speech/language-modeling
level: advanced
summary: "Kneser-Ney with three discounts, for counts one, two and three or more, set from counts of counts. The best n-gram smoothing in the measurements of Chen and Goodman."
model: word-ram
complexity:
  vars: {n: the order of the model, N: the number of predicted training tokens, V: the vocabulary}
  time: {build: "Θ(n N)", query: "Θ(n)"}
  space: {extra: "Θ(n N)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1998
  people: [Stanley F. Chen, Joshua Goodman]
  note: Chen and Goodman introduced it in their Harvard technical report of 1998 and in the journal paper of 1999, as part of a large comparison of smoothing methods.
prereqs: [kneser-ney-smoothing]
see_also: [kneser-ney-smoothing, absolute-discounting, good-turing-estimation, katz-backoff, witten-bell-smoothing, stupid-backoff, entropy-based-ngram-pruning, perplexity]
sources:
  - paper: doi:10.1006/csla.1999.0128
    title: Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Computer Speech and Language 13(4), 1999, pages 359 to 394
    locator: Section 3 on pages 370 to 371 (the three discounts, gamma, and the estimates of equation 17), Section 4.1 (the variants kneser-ney-mod and kneser-ney-mod-fix), Section 6 on pages 390 to 391 (the discussion of the results)
  - paper: "Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Technical Report TR-10-98, Harvard University, 1998"
    title: Chen and Goodman 1998
    locator: the longer report with the full set of experiments
  - paper: doi:10.1109/ICASSP.1995.479394
    title: Reinhard Kneser and Hermann Ney, Improved backing-off for M-gram language modeling, Proceedings of ICASSP 1995, volume 1, pages 181 to 184
    locator: the continuation counts of the lower order distribution
---

Modified Kneser-Ney smoothing is [Kneser-Ney smoothing](/kneser-ney-smoothing/) with three discounts in place of one. A count of 1 loses $D_1$, a count of 2 loses $D_2$, and a count of 3 or more loses $D_{3+}$. The mass taken goes, as in Kneser-Ney, to a lower order distribution built from continuation counts. Chen and Goodman introduced it in their 1998 and 1999 study of smoothing methods for [n-gram language models](/n-gram-language-model/), and it was the best method in their measurements on their corpora. It became a common default in n-gram toolkits. The three discounts come from the counts of counts with a formula close to the [Good-Turing](/good-turing-estimation/) estimate, or from held-out data.

## In plain words

Kneser-Ney takes the same small amount away from every count. But a word seen once after some words is much more likely to be luck than a word seen ten times. Modified Kneser-Ney takes a different amount away from words seen once, words seen twice, and words seen three or more times.

The amounts are chosen from how many word pairs were seen once, twice, three times and four times in the whole training text. The amount taken away is put in a pool, and the pool is shared out by a simpler guess. That guess counts how many different words each word was seen after, not how often it was seen. The chances after every history still add up to one.

## The problem

The setting is that of [Kneser-Ney smoothing](/kneser-ney-smoothing/). Sentences are padded with $n - 1$ copies of `<s>` and one `</s>`; `</s>` is predicted and counted, `<s>` is never predicted. Level $n$ of the model uses the raw counts $a_n(g) = c(g)$, and each lower level $m$ uses the continuation counts $a_m(g) = N_{1+}(\cdot\, g)$, the number of distinct tokens $x$ such that $x g$ was seen. For a history $h$ of length $m - 1$ let $T(h) = \sum_x a_m(h x)$, and let $N_1(h\, \cdot)$, $N_2(h\, \cdot)$ and $N_{3+}(h\, \cdot)$ be the numbers of words $x$ with $a_m(h x)$ equal to 1, equal to 2, and at least 3.

The discount of a count $k$ is $D(0) = 0$, $D(1) = D_1$, $D(2) = D_2$ and $D(k) = D_{3+}$ for $k \ge 3$, with a separate triple for each level. The model is

$$P_m(w \mid h) = \frac{a_m(h w) - D(a_m(h w))}{T(h)} + \gamma(h)\, P_{m-1}(w \mid h'), \qquad \gamma(h) = \frac{D_1 N_1(h\, \cdot) + D_2 N_2(h\, \cdot) + D_{3+} N_{3+}(h\, \cdot)}{T(h)},$$

with $P_m(w \mid h) = P_{m-1}(w \mid h')$ when $T(h) = 0$, $h'$ the history without its first token, and $P_0(w) = 1/|V|$. Level 1 has zero discounts by default, so it is the continuation unigram.

## The algorithm

Let $n_r$ be the number of keys of a level whose count is $r$. Chen and Goodman (1999, equation 17) estimate

$$Y = \frac{n_1}{n_1 + 2 n_2}, \qquad D_1 = 1 - 2Y \frac{n_2}{n_1}, \qquad D_2 = 2 - 3Y \frac{n_3}{n_2}, \qquad D_{3+} = 3 - 4Y \frac{n_4}{n_3}.$$

```pseudo id=main
MKN-TRAIN(corpus, n)
L1  for each predicted position of each padded sentence: a_n(the n-gram ending there) += 1
L2  for m ← n - 1 downto 1: for each distinct key x g of a_{m+1}: a_m(g) += 1
L3  for m ← 2 to n: (D_1, D_2, D_3+) ← equation 17 on n_1 .. n_4 of a_m; check 0 ≤ D(k) ≤ k

MKN-PROB(w, h)                        ▷ h holds m - 1 tokens
L4  if m = 1 then lower ← 1 / |V| else lower ← MKN-PROB(w, h')
L5  T ← Σ_x a_m(h x)
L6  if T = 0 then return lower
L7  γ ← (D_1 N_1(h ·) + D_2 N_2(h ·) + D_3+ N_3+(h ·)) / T
L8  k ← a_m(h w); return (k - D(k)) / T + γ · lower
```

Lines L1 and L2 are the counting of Kneser-Ney. Line L3 is new. The check in line L3 matters: the estimates can leave the range $[0, k]$ on small data, and then the row would not sum to 1. The totals $T(h)$ and the three numbers $N_1(h\, \cdot)$, $N_2(h\, \cdot)$, $N_{3+}(h\, \cdot)$ are stored for each history at training time, so a query costs one lookup per level.

## Example

Take six sentences: "x y" three times, "x z" twice and "x u" once, with $n = 2$. After the history x the counts are y 3, z 2 and u 1, so $T = 6$ and each count class has one word. The text has 7 bigram types, and the continuation unigram is $1/7$ for each of x, y, z and u and $3/7$ for `</s>`, which follows three words.

With the discounts $D_1 = 1/2$, $D_2 = 1$ and $D_{3+} = 3/2$, $\gamma(\text{x}) = (1/2 + 1 + 3/2) / 6 = 1/2$. Kneser-Ney with $D = 3/4$ has $\gamma(\text{x}) = (3/4) \cdot 3 / 6 = 3/8$. The two rows after x are:

| $w$ | count | modified, $D(k)$ | modified $P(w \mid \text{x})$ | Kneser-Ney $P(w \mid \text{x})$ |
|---|---|---|---|---|
| y | 3 | 3/2 | $1.5/6 + 1/14 = 9/28$ | $2.25/6 + 3/56 = 3/7$ |
| z | 2 | 1 | $1/6 + 1/14 = 5/21$ | $1.25/6 + 3/56 = 11/42$ |
| u | 1 | 1/2 | $0.5/6 + 1/14 = 13/84$ | $0.25/6 + 3/56 = 2/21$ |
| `</s>` | 0 | 0 | $3/14$ | $9/56$ |
| x | 0 | 0 | $1/14$ | $3/56$ |

Both rows sum to 1. Here the modified form takes more from the frequent word and less from the singleton. On real data the estimates come from equation 17. For a trigram model on 300 random sentences over 50 words with Zipf weights, the top level had $n_1, \ldots, n_4 = 605, 75, 16, 8$, which gives $Y = 121/151 \approx 0.80$ and $D_1 \approx 0.80$, $D_2 = 5614/3775 \approx 1.49$ and $D_{3+} = 211/151 \approx 1.40$.

## Correctness

The proofs file shows four things. Every conditional distribution sums to 1 exactly when $0 \le D(k) \le k$ for every $k$: the seen words lose $\sum D(a_m(h w)) / T(h)$, which is exactly $\gamma(h)$ once the words are grouped by count class, and the lower level sums to 1. Every probability is positive when the discounts above level 1 are positive. With $D_1 = D_2 = D_{3+}$ the model is Kneser-Ney. And in equation 17, $D_1 = Y$ always, $D_r = r - Y r^*$ with $r^*$ the Good-Turing adjusted count, and $D_2$ or $D_{3+}$ can be negative on small or odd data, which is why line L3 checks the range.

## Complexity

As for [Kneser-Ney](/kneser-ney-smoothing/): training makes one pass over the $N$ predicted tokens and one pass over the distinct n-grams of each level, $\Theta(n N)$ expected n-gram operations with [hash tables](/hash-table/). Line L3 adds one pass over the counts of each level. A query takes $\Theta(n)$ operations, and a full distribution $\Theta(n |V|)$. The tables take $\Theta(n N)$ space; the three numbers per history add a constant factor.

## Properties

- **A proper distribution** for discounts in range, exactly, in rational arithmetic.
- **Three discounts per level.** The discount depends on the count class. Equation 17 does not force it to grow with the count: in the trigram example above, $D_{3+} < D_2$.
- **Contains Kneser-Ney** as the case of equal discounts.
- **Discounts from data.** The default needs no held-out data. Chen and Goodman's best variant fitted the discounts on held-out data instead.

## Variants and improvements

- **kneser-ney-mod and kneser-ney-mod-fix.** In the experiments of Chen and Goodman, the first optimizes the discounts on held-out data and the second uses equation 17; the second did slightly worse.
- **Backoff form.** The variant kneser-ney-mod-backoff of Chen and Goodman uses the lower level only for unseen words. It did worse than the interpolated form for small counts.
- **Two discounts.** Ney and colleagues (1997) independently suggested two discounts in place of one, as Chen and Goodman report.
- **Pruned models.** Large modified Kneser-Ney models are often made smaller with [entropy-based pruning](/entropy-based-ngram-pruning/), which removes the n-grams whose loss changes the model least.

## When to use it

Use it for a count-based n-gram model when the corpus is large enough that the counts of counts $n_1$ to $n_4$ are stable at every level. It is the usual baseline that later neural language models were compared with, as in Bengio and colleagues (2003). On very small corpora the estimates can fail; use plain Kneser-Ney or fit the discounts on held-out data. For web-scale counts where only a score is needed, [stupid backoff](/stupid-backoff/) is much cheaper to build.

## Pitfalls

- **"The best smoothing".** It was the best of the methods Chen and Goodman measured, on their corpora (Brown, North American Business news, Switchboard and Broadcast News) and their n-gram orders. That is a measurement, not a theorem.
- **Out-of-range discounts.** Equation 17 can give $D_2 < 0$ or $D_{3+} < 0$, for example with $n_1 = n_2 = 1$ and $n_3 = 6$. Clipping the discount without changing $\gamma$ breaks the sum to 1. Check and fall back to explicit values.
- **Division by zero.** $n_2 = 0$ or $n_3 = 0$ makes equation 17 undefined. This happens at low levels of small models, and in corpora where rare n-grams were removed before counting.
- **Counts of counts of the wrong level.** Each level needs its own discounts, from the counts that level uses.
- **Lower levels with raw counts.** As for Kneser-Ney, every level below $n$ uses continuation counts.

## Implementations

## History

Chen and Goodman (1998, 1999) compared the main smoothing methods of the time on several corpora, training set sizes and n-gram orders. They found interpolated [Kneser-Ney](/kneser-ney-smoothing/) the best of the existing methods and proposed this modification, with three discounts per level. In their discussion, the modified form "consistently outperformed all other algorithms" in their experiments, and the largest single factor in its success was the lower order distribution of Kneser and Ney. They credit the estimates of equation 17 to Ries (1997), and note that Ney and colleagues had independently proposed two discounts. Modified Kneser-Ney then became a common default in n-gram toolkits.

## References
