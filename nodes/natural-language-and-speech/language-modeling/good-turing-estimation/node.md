---
tag: 7B0QFN
kind: algorithm
slug: good-turing-estimation
name: Good-Turing estimation
aliases:
- Good-Turing smoothing
- Good-Turing discounting
area: natural-language-and-speech/language-modeling
level: core
summary: "Estimate the total chance of the unseen types as N_1/N and replace each count r by r* = (r+1) N_(r+1) / N_r, where N_r is the number of types seen r times."
model: word-ram
complexity:
  vars: {T: the number of distinct seen types, N: the number of tokens in the sample}
  time: {worst: "Θ(N)"}
  space: {extra: "Θ(T)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1953
  people: [Alan M. Turing, I. J. Good]
  note: Good published the method in Biometrika in 1953 and gave the main idea to Turing, from their wartime work on codebreaking.
prereqs: [maximum-likelihood-estimation]
see_also: [simple-good-turing, katz-backoff, laplace-smoothing, witten-bell-smoothing, absolute-discounting, kneser-ney-smoothing, chao1-estimator, zipfs-law]
sources:
  - paper: doi:10.1093/biomet/40.3-4.237
    title: I. J. Good, The population frequencies of species and the estimation of population parameters, Biometrika 40(3-4), 1953, pages 237 to 264
    locator: the estimate (r+1) N_(r+1) / N_r of the frequency of a species seen r times, the estimate N_1/N of the unseen mass, and the need to smooth the N_r
  - paper: doi:10.1080/09296179508590051
    title: William A. Gale and Geoffrey Sampson, Good-Turing frequency estimation without tears, Journal of Quantitative Linguistics 2(3), 1995, pages 217 to 237
    locator: a plain account of the Turing estimator and of the noise in the counts of counts
  - paper: "Kenneth W. Church and William A. Gale, A comparison of the enhanced Good-Turing and deleted estimation methods for estimating probabilities of English bigrams, Computer Speech and Language 5(1), 1991"
    title: Church and Gale 1991
    locator: Good-Turing estimates of bigram probabilities compared with held-out counts
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999
    locator: Chapter 6, Section 6.2 (statistical estimators, with Good-Turing estimation)
  - paper: doi:10.1006/csla.1999.0128
    title: Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Computer Speech and Language 13(4), 1999, pages 359 to 394
    locator: Good-Turing estimation as the base of Katz smoothing
---

Good-Turing estimation answers a question that comes up whenever we count things in a sample: how much probability should go to the types that we have not seen at all, and how much less should each seen type get than its share in the sample? The answer uses only the counts of counts. If $N_r$ types were seen exactly $r$ times in $N$ tokens, the unseen types together get $N_1 / N$, and a type seen $r$ times gets the adjusted count $r^* = (r+1) N_{r+1} / N_r$ in place of $r$. Unlike [Laplace smoothing](/laplace-smoothing/), it adds nothing by hand: the share of the unseen comes from the data, and in language models it is the discount behind [Katz backoff](/katz-backoff/). The same idea estimates the number of unseen species in ecology, as in the [Chao1 estimator](/chao1-estimator/).

## In plain words

You count the fish of each kind in a net. Some kinds you saw only once. How likely is it that the next fish is of a kind you have never seen? Good-Turing says: about as likely as it was that the last fish caught was of a kind seen only once, because a kind that is new now would have been seen once after one more catch. So the share of the new kinds is the number of kinds seen once divided by the number of fish.

The same thought moves every count down a little. A kind seen once is treated like the kinds seen twice, scaled to how many there are of each. The share given to the new kinds comes out of the shares of the seen ones, so the total stays one.

## The problem

A sample of $N$ tokens is drawn from an unknown distribution over a set of types that may be very large. Type $x$ was seen $c(x) = r$ times. Write $N_r$ for the number of types seen exactly $r$ times, so that $N = \sum_r r N_r$, and $T = \sum_{r \ge 1} N_r$ for the number of seen types. The task is to give each seen type a probability and to give the unseen types, as a group, a total probability $P_0$, so that $P_0 + \sum_x p(x) = 1$.

The [maximum likelihood estimate](/maximum-likelihood-estimation/) $p(x) = r / N$ gives $P_0 = 0$. In text this is far too low: by [Zipf's law](/zipfs-law/) a large part of the types in any sample are seen once, and many more were missed.

## The algorithm

The Turing estimate of the adjusted count is

$$r^* = (r+1) \frac{N_{r+1}}{N_r}, \qquad p(x) = \frac{r^*}{N}, \qquad P_0 = \frac{N_1}{N}.$$

The formula alone fails where $N_{r+1} = 0$: then $r^* = 0$, and in every sample the most frequent type gets probability zero. The usual fix, used here, keeps $r^* = r$ where the formula has no data or where $r$ is above a cut-off $k$, and then scales the seen probabilities so that they sum to $1 - P_0$.

```pseudo id=main
GOOD-TURING(c, k)                    ▷ c(x) ≥ 1 for each seen type x; k = ∞ for no cut-off
L1  N ← Σ_x c(x); N_r ← the number of types x with c(x) = r
L2  P_0 ← N_1 / N                    ▷ the total probability of all unseen types
L3  for each r with N_r > 0 do
L4      if r ≤ k and N_{r+1} > 0 then r* ← (r + 1) N_{r+1} / N_r
L5      else r* ← r
L6  S ← Σ_r N_r r*
L7  for each seen type x do p(x) ← (1 - P_0) r*_{c(x)} / S
L8  return p, P_0
```

Line L2 is the share of the unseen. Lines L3 to L5 give the adjusted counts. Lines L6 and L7 scale the seen probabilities to the mass that is left. If the number $U$ of unseen types is known, for example $U = |V| - T$ for a fixed vocabulary $V$, each unseen type gets $P_0 / U$. If it is not known, $P_0$ stays a single number, as in the [escape probability](/prediction-by-partial-matching/) of a text compressor.

## Example

Take the sample "a a a b b c d e", with $N = 8$. The type a was seen 3 times, b twice, and c, d and e once each. So $N_1 = 3$, $N_2 = 1$, $N_3 = 1$, and $N_4 = 0$.

| $r$ | $N_r$ | $r^*$ by the formula | $r^*$ used | $p$ of one type |
|---|---|---|---|---|
| 0 | | | | $P_0 = 3/8$ for all unseen types |
| 1 | 3 | $2 \cdot 1 / 3 = 2/3$ | $2/3$ | $5/96$ |
| 2 | 1 | $3 \cdot 1 / 1 = 3$ | $3$ | $15/64$ |
| 3 | 1 | $4 \cdot 0 / 1 = 0$ | $3$ | $15/64$ |

The unseen types get $3/8$. Then $S = 3 \cdot \tfrac23 + 3 + 3 = 8$, and each type gets $(5/8) r^* / 8$. The total is $3/8 + 3 \cdot 5/96 + 2 \cdot 15/64 = 1$. The formula alone gives a the probability 0, b the probability $3/8$, and each singleton $1/12$. Both versions show the main weakness of the raw estimate: with so few types the $N_r$ are noisy, and b gets as much as a or more. [Simple Good-Turing](/simple-good-turing/) smooths the $N_r$ before it uses them.

## Correctness

There are two parts.

**The output is a distribution.** Every $r^*$ is positive, $S = \sum_r N_r r^* > 0$, and $\sum_x p(x) = (1 - P_0) \sum_r N_r r^* / S = 1 - P_0$. So $P_0 + \sum_x p(x) = 1$ exactly.

**Why the formula is right.** Draw $N$ tokens independently from a distribution $q$. Let $M_r$ be the total probability of the types seen exactly $r$ times. Then

$$\mathbb{E}[M_r] = \frac{r+1}{N+1} \, \mathbb{E}[N_{r+1}^{(N+1)}],$$

where $N_{r+1}^{(N+1)}$ is the number of types seen $r+1$ times in a sample of $N + 1$ tokens. For $r = 0$, the unseen mass has expectation $\mathbb{E}[N_1^{(N+1)}] / (N+1)$, which $N_1 / N$ estimates. For $r \ge 1$, the $N_r$ types seen $r$ times share $\mathbb{E}[M_r]$, and each gets about $(r+1) N_{r+1} / (N N_r) = r^* / N$. The identity follows from $\binom{N}{r} = \frac{r+1}{N+1} \binom{N+1}{r+1}$ and holds for every $q$, with no assumption on the shape of the distribution.

## Complexity

After the tokens are counted, which takes $\Theta(N)$ expected time with a [hash table](/hash-table/), the table of the $N_r$ takes $\Theta(T)$ time, lines L3 to L6 take time linear in the number of distinct counts, and line L7 takes $\Theta(T)$. The number of distinct counts is at most $\sqrt{2N}$, since distinct counts $r_1 < r_2 < \cdots < r_m$ need $N \ge 1 + 2 + \cdots + m$. The extra space is $\Theta(T)$ for the output. In exact rational arithmetic each step works on numbers of $O(\log N)$ bits before the final scaling.

## Properties

- **Distribution free.** The expectation identity holds for any distribution of the types. The estimator assumes only that the tokens are independent draws.
- **The unseen mass is $N_1 / N$.** It is large when many types are seen once, and zero when no type is seen once.
- **Not monotone.** The raw $r^*$ need not grow with $r$. In the example, b (seen twice) gets as much as a (seen three times).
- **Lost mass.** The formula alone sums to $1 - P_0$ over the seen types only when there is no gap: the seen mass is $\sum_{s \ge 2,\, N_{s-1} > 0} s N_s / N$, so every count $s$ with $N_{s-1} = 0$ drops out. The scaling of line L7 corrects this.
- **Small counts only.** For large $r$ the counts of counts are 0 or 1 and the formula is noise. The ratio $r^*/r$ is close to 1 there anyway, which is why a cut-off $k$, such as Katz's $k = 5$, loses little.

## Variants and improvements

- **[Simple Good-Turing](/simple-good-turing/)** (Gale and Sampson 1995) averages the $N_r$ over the gaps, fits a line to $\log N_r$ against $\log r$, and switches from the raw to the smoothed $r^*$ when the two no longer differ significantly.
- **[Katz backoff](/katz-backoff/)** uses Good-Turing discounts for the counts 1 to $k$ in each order of an [n-gram model](/n-gram-language-model/) and gives the unseen mass to the lower order.
- **The enhanced Good-Turing method** of Church and Gale (1991) splits the bigrams into classes by the counts of their words before it applies the formula.
- **[Absolute discounting](/absolute-discounting/)** and [Kneser-Ney smoothing](/kneser-ney-smoothing/) replace $r - r^*$, which is close to a constant for $r \ge 2$ in text, by a fixed discount $D$.
- **The [Chao1 estimator](/chao1-estimator/)** uses $N_1$ and $N_2$ to estimate how many species were not seen, not how much probability they have.

## When to use it

Use it to estimate the share of new types in a sample from a large or open set: new words in text, new species in a survey, new k-mers in a sequencing run, or new values in a database column. On its own it gives the total for the unseen types and not their split, so a language model still needs a second distribution, such as a lower-order model, to share $P_0$ among the words. For small counts use it with smoothed $N_r$ ([simple Good-Turing](/simple-good-turing/)), or use it only for $r \le k$.

## Pitfalls

- **Gaps in the counts of counts.** If $N_{r+1} = 0$ the formula gives $r^* = 0$. Keep $r^* = r$ there, or smooth the $N_r$, and then renormalize.
- **$P_0$ is a total.** It is the mass of all unseen types together. Dividing it by the number of unseen types needs a closed vocabulary.
- **No singletons.** If $N_1 = 0$ the unseen types get nothing. This happens on data where rare items were removed before counting, for example a vocabulary with a frequency cut-off.
- **All singletons.** If every type is seen once, $P_0 = 1$ and the seen types get nothing. The estimate is right in spirit (the sample says almost nothing about the next token) but it is not useful.
- **Dependent tokens.** The identity assumes independent draws. Words repeat in bursts inside a document, so on text from only a few documents the estimate of the unseen mass can be far off.

## Implementations

## History

I. J. Good published the method in 1953 and wrote that the key idea was due to Alan Turing. The two had worked together on codebreaking during the Second World War. Good's paper also warned that the $N_r$ must be smoothed before they are used for larger $r$. The estimator came to language modeling through speech recognition: Katz (1987) built his backoff model on it, Church and Gale (1991) tested it on English bigrams, and Gale and Sampson (1995) gave the simple smoothing method that most later software uses.

## References
