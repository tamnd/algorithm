---
tag: M3W0NG
kind: algorithm
slug: kneser-ney-smoothing
name: Kneser-Ney smoothing
aliases:
- interpolated Kneser-Ney
area: natural-language-and-speech/language-modeling
level: core
summary: "Absolute discounting whose lower order model uses continuation counts, the number of distinct contexts a word follows, rather than raw counts."
model: word-ram
complexity:
  vars: {n: the order of the model, N: the number of predicted training tokens, V: the vocabulary}
  time: {build: "Θ(n N)", query: "Θ(n)"}
  space: {extra: "Θ(n N)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1995
  people: [Reinhard Kneser, Hermann Ney, Stanley F. Chen, Joshua Goodman]
  note: Kneser and Ney gave a backoff model with continuation counts at ICASSP 1995. Chen and Goodman gave the interpolated form in 1998 and showed that it does better.
prereqs: [n-gram-language-model, absolute-discounting]
see_also: [modified-kneser-ney-smoothing, absolute-discounting, katz-backoff, witten-bell-smoothing, good-turing-estimation, jelinek-mercer-smoothing, dirichlet-prior-smoothing, perplexity]
sources:
  - paper: doi:10.1109/ICASSP.1995.479394
    title: Reinhard Kneser and Hermann Ney, Improved backing-off for M-gram language modeling, Proceedings of ICASSP 1995, volume 1, pages 181 to 184
    locator: the backoff model whose lower order distribution counts the distinct contexts of a word
  - paper: doi:10.1006/csla.1999.0128
    title: Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Computer Speech and Language 13(4), 1999, pages 359 to 394
    locator: Section 2.6 (absolute discounting and the estimate D = n_1 / (n_1 + 2 n_2)), Section 2.7 on pages 366 to 368 (the marginal constraint and the interpolated form, equations 12 to 14), Section 2.8 (backoff against interpolation), Section 4.1 (the implementation with N_1+ counts at every lower order)
  - paper: "Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Technical Report TR-10-98, Harvard University, 1998"
    title: Chen and Goodman 1998
    locator: the longer report behind the 1999 paper, with the interpolated and modified forms
  - paper: doi:10.1017/S1351324900000218
    title: David J. C. MacKay and Linda C. Bauman Peto, A hierarchical Dirichlet language model, Natural Language Engineering 1(3), 1995, pages 289 to 308
    locator: a Bayesian n-gram model with Dirichlet priors shared across orders
  - paper: "Yee Whye Teh, A hierarchical Bayesian language model based on Pitman-Yor processes, Proceedings of COLING-ACL 2006, pages 985 to 992"
    title: Teh 2006
    locator: interpolated Kneser-Ney as an approximate inference scheme in a hierarchical Pitman-Yor language model
---

Kneser-Ney smoothing is the way most [n-gram language models](/n-gram-language-model/) were built from the late 1990s on. It takes a fixed discount $D$ from every seen n-gram count, as [absolute discounting](/absolute-discounting/) does, and gives the mass it took to a lower order distribution. The new idea is what that lower distribution counts. It does not ask how often a word was seen. It asks after how many different words it was seen, the continuation count $N_{1+}(\cdot\, w)$. A word such as "Francisco" can be frequent and still follow almost only "San", so it should get little probability after a history where the full model has no data. This page gives the interpolated form of Chen and Goodman, which uses the lower order for every word; the 1995 original was a backoff model.

## In plain words

To guess the next word, look first at what followed the same last few words in the training text. Trust those counts, but take a fixed small amount away from each one and put it in a pool.

The pool is shared out by a simpler guess that looks at fewer words. The simple guess is the clever part. It does not ask how often a word appeared. It asks how many different words it appeared after. A word that shows up after many different words is a good guess in a new place. A word that is common only inside one fixed phrase is not.

The pool and the simpler guess together fill the gap, so the chances after every history still add up to one.

## The problem

The training corpus is a list of sentences. Each sentence is padded with $n - 1$ copies of `<s>` on the left and one `</s>` on the right; `</s>` is predicted and counted, `<s>` is never predicted. The vocabulary $V$ is the set of predicted tokens, or a given closed set that contains them. For an order $n$, the task is to give a conditional distribution $P(w \mid h)$ over $V$ for every history $h$ of $n - 1$ tokens, with no zero for a word that was not seen after $h$, and with the counts of the training text used as well as possible.

Write $c(g)$ for the number of times the n-gram $g$ ends at a predicted token, and $N_{1+}(\cdot\, g)$ for the number of distinct tokens $x$ such that $x g$ was seen. The model has one level for each order $m = 1, \ldots, n$. Level $n$ uses $a_n(g) = c(g)$, and each lower level uses $a_m(g) = N_{1+}(\cdot\, g)$. For a history $h$ of length $m - 1$ let

$$T(h) = \sum_x a_m(h x), \qquad N_{1+}(h\, \cdot) = |\{x : a_m(h x) > 0\}|, \qquad h' = h \text{ without its first token}.$$

Interpolated Kneser-Ney is the recursion

$$P_m(w \mid h) = \frac{\max(a_m(h w) - D_m, 0)}{T(h)} + \frac{D_m\, N_{1+}(h\, \cdot)}{T(h)}\, P_{m-1}(w \mid h'),$$

with $P_m(w \mid h) = P_{m-1}(w \mid h')$ when $T(h) = 0$, and $P_0(w) = 1 / |V|$. With $D_1 = 0$, level 1 is the continuation unigram $N_{1+}(\cdot\, w) / N_{1+}(\cdot\, \cdot)$.

## The algorithm

Training counts the n-grams once and derives every lower level from the distinct n-grams above it. A query walks down the levels.

```pseudo id=main
KN-TRAIN(corpus, n)
L1  for each predicted position of each padded sentence: a_n(the n-gram ending there) += 1
L2  for m ← n - 1 downto 1: for each distinct key x g of a_{m+1}: a_m(g) += 1
L3  for m ← 2 to n: D_m ← n_1 / (n_1 + 2 n_2), from the counts of counts of a_m;  D_1 ← 0

KN-PROB(w, h)                         ▷ h holds m - 1 tokens
L4  if m = 1 then lower ← 1 / |V| else lower ← KN-PROB(w, h')
L5  T ← Σ_x a_m(h x)
L6  if T = 0 then return lower        ▷ h was never seen at this level
L7  γ ← D_m · N_{1+}(h ·) / T
L8  return max(a_m(h w) - D_m, 0) / T + γ · lower
```

Line L1 is the only pass over the text. Line L2 turns the distinct $(m+1)$-grams into continuation counts: each distinct $x g$ adds one left context to $g$. Line L3 is the default discount of Ney, Essen and Kneser (1994) that Chen and Goodman use, with $n_r$ the number of keys of level $m$ whose count is $r$. Here it is computed from the counts that level actually uses, so the lower levels take it from their continuation counts; this is a choice of the implementation. The totals $T(h)$ and $N_{1+}(h\, \cdot)$ are stored for every history at training time, so lines L5 and L7 are table lookups.

## Example

Take the three sentences "a b", "a c" and "b c" with $n = 2$, $D_2 = 3/4$ and $D_1 = 0$. The padded text has the 7 bigram types `<s>` a (seen twice), `<s>` b, a b, a c, b c, b `</s>` and c `</s>` (seen twice). Line L2 counts the distinct left contexts:

| $w$ | left contexts | $N_{1+}(\cdot\, w)$ | $P_1(w)$ |
|---|---|---|---|
| a | `<s>` | 1 | 1/7 |
| b | `<s>`, a | 2 | 2/7 |
| c | a, b | 2 | 2/7 |
| `</s>` | b, c | 2 | 2/7 |

After `<s>`, $T = 3$ and $N_{1+}(\text{<s>}\, \cdot) = 2$, so $\gamma = (3/4) \cdot 2 / 3 = 1/2$. Then

$$P(\text{a} \mid \text{<s>}) = \frac{2 - 3/4}{3} + \frac12 \cdot \frac17 = \frac{41}{84}, \qquad P(\text{</s>} \mid \text{c}) = \frac{2 - 3/4}{2} + \frac38 \cdot \frac27 = \frac{41}{56}.$$

The whole model is:

| $h$ | a | b | c | `</s>` |
|---|---|---|---|---|
| `<s>` | 41/84 | 19/84 | 1/7 | 1/7 |
| a | 3/28 | 19/56 | 19/56 | 3/14 |
| b | 3/28 | 3/14 | 19/56 | 19/56 |
| c | 3/56 | 3/28 | 3/28 | 41/56 |

Every row sums to 1. The word a is seen as often as b and c, but always after `<s>`, so after any other history it gets the least. With $n = 3$ on the same text, level 2 counts `<s>` a once, not twice, because both occurrences have the same left context `<s>`.

## Correctness

The proof in the proofs file has three parts. Lines L1 and L2 compute the counts as defined, because every $(m+1)$-gram that ends at a predicted token is the suffix of an n-gram, thanks to the padding. Every conditional distribution sums to 1 when $0 \le D_m \le 1$, by induction on $m$: the seen words of $h$ lose exactly $D_m N_{1+}(h\, \cdot) / T(h)$, which is the weight $\gamma$ of the lower level, and the lower level sums to 1. And in a bigram model the continuation unigram is the only lower distribution for which the model keeps the unigram marginals of the data, $\sum_v P(v) P(w \mid v) = c(w) / N$. This is the constraint that led to the method.

## Complexity

Line L1 visits the $N$ predicted tokens once. Line L2 visits each distinct $(m+1)$-gram once for each level, at most $N$ keys per level, so training takes $\Theta(n N)$ expected n-gram operations with [hash tables](/hash-table/). A query makes one lookup per level, $\Theta(n)$ operations, and a full distribution over $V$ takes $\Theta(n |V|)$. Each operation hashes a tuple of up to $n$ tokens, so in word operations each bound is a factor $n$ larger. The tables hold at most $N$ keys per level, $\Theta(n N)$ space.

## Properties

- **A proper distribution.** Every conditional distribution sums to 1 exactly for $0 \le D_m \le 1$, and every word gets a positive probability when the discounts above level 1 are positive.
- **Marginals.** The lower order is chosen so that the model keeps the lower order marginals of the training text, which is the reason for the continuation counts.
- **Interpolated.** Every word, seen or not, gets a share of the lower level. In the backoff form only the unseen words do.
- **One discount per order.** Counts of 1 and of 100 lose the same $D_m$. [Modified Kneser-Ney](/modified-kneser-ney-smoothing/) uses three discounts.
- **Exact.** All values are ratios of integer counts and rational discounts.

## Variants and improvements

- **Backoff Kneser-Ney**, the 1995 form, uses $(c(h w) - D)/c(h)$ for the seen words and $\alpha(h) P(w \mid h')$ for the rest, with $\alpha(h)$ chosen to make the sum 1.
- **[Modified Kneser-Ney smoothing](/modified-kneser-ney-smoothing/)** uses the discounts $D_1$, $D_2$ and $D_{3+}$ for counts 1, 2 and 3 or more.
- **[Absolute discounting](/absolute-discounting/)** is the same recursion with raw counts at every level.
- **The hierarchical Pitman-Yor language model** of Teh (2006) is a Bayesian model whose approximate inference gives interpolated Kneser-Ney; MacKay and Peto (1995) had built a hierarchical Dirichlet model in the same spirit.
- **[Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/)** and **[Dirichlet prior smoothing](/dirichlet-prior-smoothing/)** are the retrieval versions of linear interpolation with a background model.

## When to use it

Use it as the default smoothing for a count-based n-gram model, for example in a speech recognizer, in a spelling corrector, or as a baseline for a neural model measured by [perplexity](/perplexity/). Use the modified form if you have enough data to estimate three discounts. For very large web corpora where a proper distribution is not needed, [stupid backoff](/stupid-backoff/) is cheaper to build. To make the model smaller, prune it with [entropy-based pruning](/entropy-based-ngram-pruning/).

## Pitfalls

- **Raw counts in the lower levels.** The continuation counts are the point of the method. With $c(w)$ in the lower levels it is absolute discounting.
- **Only the unigram level changed.** Every level below $n$ uses continuation counts, not only level 1.
- **A discount above 1.** Then words seen once lose more than their count, and the sum exceeds 1. The default $n_1 / (n_1 + 2 n_2)$ is always in $(0, 1]$, but it fails when $n_1 = 0$.
- **Sentence starts.** Without the padding, an n-gram at the start of a sentence has no left context, and its continuation count is 0. The padding with `<s>` gives it the context `<s>`.
- **Unseen words.** With $D_1 = 0$ a word that never appeared in training gets 0. Map such words to `<unk>`, or use $D_1 > 0$ so the uniform level gets some mass.
- **Testing with floats.** Check that rows sum to 1 in exact arithmetic; float sums hide small errors in the weights.

## Implementations

## History

Kneser and Ney (1995) proposed a backoff model whose lower order distribution is fitted so that the model keeps the marginals of the data, which gives the counts of distinct contexts. Their paper was about backoff. Chen and Goodman (1998, 1999) gave the interpolated form, derived it from the same constraint, and found that it beats the backoff form in their experiments; they note that Ney and colleagues had observed this independently. In the same work they introduced [modified Kneser-Ney](/modified-kneser-ney-smoothing/). MacKay and Peto (1995) had built a hierarchical Dirichlet language model, and Teh (2006) gave the Bayesian reading of the method: he showed that interpolated Kneser-Ney comes out of approximate inference in a hierarchical Pitman-Yor language model.

## References
