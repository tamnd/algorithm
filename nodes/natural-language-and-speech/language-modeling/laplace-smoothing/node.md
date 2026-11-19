---
tag: 8JPVRM
kind: technique
slug: laplace-smoothing
name: Laplace smoothing
aliases:
- add-one smoothing
- add-k smoothing
- Lidstone smoothing
- additive smoothing
area: natural-language-and-speech/language-modeling
level: intro
summary: Add one, or a constant k, to every count before normalizing, so no event gets zero probability. Simple, but with a large vocabulary it takes too much mass from seen events.
prereqs: [maximum-likelihood-estimation, n-gram-language-model]
see_also: [good-turing-estimation, witten-bell-smoothing, absolute-discounting, dirichlet-prior-smoothing, conjugate-prior, naive-bayes-classifier, motif-information-content, greedy-motif-search]
sources:
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999
    locator: Chapter 6, Section 6.2 (statistical estimators, with Laplace's law, Lidstone's law and the Jeffreys-Perks law)
  - paper: "William A. Gale and Kenneth W. Church, What's wrong with adding one?, in N. Oostdijk and P. de Haan (eds.), Corpus-Based Research into Language, Rodopi, Amsterdam, 1994"
    title: Gale and Church 1994
    locator: the comparison of add-one estimates of English bigram counts with held-out counts
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: chapter N-gram Language Models (draft of January 2026), Laplace smoothing and add-k smoothing
---

Laplace smoothing turns counts into probabilities by adding a small constant to every count first, so that an event never seen in the sample still gets a probability above zero. With the constant 1 it is called add-one smoothing; with a general constant $k > 0$ it is add-k or Lidstone smoothing. It is used wherever a table of counts must give probabilities for events that may be missing from it: next-word tables in an [n-gram language model](/n-gram-language-model/), word counts in a [naive Bayes classifier](/naive-bayes-classifier/), and base counts in DNA motif profiles, where the added counts are called pseudocounts (see [greedy motif search](/greedy-motif-search/) and [motif information content](/motif-information-content/)). It is the easiest smoothing to state and to prove correct, and with a large vocabulary it is one of the least accurate.

## In plain words

You count what you saw and divide by the total. Anything you did not see then gets a chance of zero, and one such zero can make a whole sentence impossible.

The fix is to pretend that you saw every possible outcome a few extra times, the same number of times for each. Add that number to every count, also the counts that are zero, and divide by the new total. Outcomes you saw keep most of their share, and outcomes you did not see get a small equal share.

The cost is that every unseen outcome gets the same extra share. When there are many more possible outcomes than observations, the unseen ones together take most of the total.

## When it applies

It applies to a table of counts $c(h w)$ for a fixed, finite set $V$ of outcomes and a set of contexts $h$, where each row must become a distribution on $V$. In a language model, $h$ is the history and $V$ is the vocabulary of predicted tokens, which holds the end marker `</s>` and the unknown-word token `<unk>` but not the start marker `<s>`. The set $V$ must be fixed before counting, since $|V|$ enters every probability.

It works well when $|V|$ is small compared with the number of observations per context: a few classes, four DNA bases, the letters of an alphabet, or the features of a text classifier where only the ratio of two probabilities matters. It works badly for word n-grams, where $|V|$ is in the tens of thousands and most contexts are seen only a few times.

## The template

Fix $k > 0$. For a context $h$ with total count $c(h) = \sum_{w \in V} c(h w)$,

$$P_k(w \mid h) = \frac{c(h w) + k}{c(h) + k |V|}.$$

Every value is positive, and the row sums to $(c(h) + k|V|)/(c(h) + k|V|) = 1$. The names of the special cases are:

| $k$ | name |
|---|---|
| $1$ | Laplace, or add-one |
| $1/2$ | Jeffreys-Perks, or expected likelihood estimation |
| any $k > 0$ | Lidstone, or add-k |

The estimate is a weighted mean of the maximum likelihood estimate and the uniform distribution:

$$P_k(w \mid h) = \mu \, \frac{c(h w)}{c(h)} + (1 - \mu) \, \frac{1}{|V|}, \qquad \mu = \frac{c(h)}{c(h) + k |V|},$$

so it is a fixed form of interpolation, with a weight that depends only on $c(h)$. A context never seen, with $c(h) = 0$, gets the uniform distribution. The count that the estimate acts as if it saw, the adjusted count, is

$$c^*(h w) = P_k(w \mid h) \, c(h) = (c(h w) + k) \, \mu .$$

In Bayesian terms, $P_k(\cdot \mid h)$ is the posterior mean of the row when the prior on the row is a symmetric Dirichlet distribution with parameter $k$ for each outcome (see [conjugate prior](/conjugate-prior/) and [Bayes' theorem](/bayes-theorem/)). The case $k = 1$ is a uniform prior on the simplex.

## Classic examples

**Laplace's rule of succession.** With two outcomes and $k = 1$, an event that happened $s$ times in $n$ trials gets the probability $(s + 1)/(n + 2)$ for the next trial. Laplace used it for the chance that the sun rises tomorrow, given that it has risen every day on record.

**A base after a DNA context.** In a model of DNA with $V = \{A, C, G, T\}$, the context CG is seen 5 times, followed by A twice and by G three times. The maximum likelihood estimate gives C and T the probability 0. Add-one smoothing divides by $5 + 4 = 9$:

| base $w$ | count | $P_1(w \mid \mathrm{CG})$ |
|---|---|---|
| A | 2 | 3/9 |
| C | 0 | 1/9 |
| G | 3 | 4/9 |
| T | 0 | 1/9 |

Here $|V|$ is small, so the seen bases keep $7/9$ of the mass.

**A word bigram row.** In a word model with $|V| = 50\,000$, a history seen 10 times and followed by 3 different words has 49 997 unseen followers. Add-one smoothing gives each of them $1/50\,010$, and all of them together $49\,997/50\,010$, more than 99.9% of the row. A follower seen 5 times gets $6/50\,010$, against $5/10$ from the counts. Gale and Church (1994) compared add-one estimates of English bigram counts with the counts in held-out text and found them far worse than the alternatives, mostly for this reason.

**Text classification.** A [naive Bayes classifier](/naive-bayes-classifier/) multiplies $P(w \mid \text{class})$ over the words of a document. A single word never seen in the training documents of a class would make that class impossible. Add-one smoothing over the word list prevents this, and since the decision compares classes, the overall shrinkage matters less than in a language model.

## Variations

- **Tuned $k$.** Choose $k$ on held-out text, for example by minimizing the [perplexity](/perplexity/). For word models the best $k$ is often much smaller than 1, but the result is usually still worse than [Good-Turing estimation](/good-turing-estimation/), [Witten-Bell smoothing](/witten-bell-smoothing/) or [absolute discounting](/absolute-discounting/).
- **Non-uniform pseudocounts.** Add $k \, q(w)$ for a distribution $q$ on $V$, so that $P(w \mid h) = (c(h w) + k|V| q(w))/(c(h) + k|V|)$ with $q$ a lower-order model. This is the form of [Dirichlet prior smoothing](/dirichlet-prior-smoothing/) in retrieval, where $q$ is the collection model; a fixed weight in place of $\mu$ gives [Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/).
- **Pseudocounts in profiles.** Motif finders add a pseudocount to each base in each column of a profile, so that a base never seen in a column does not make a candidate motif impossible.
- **Add to the unigrams only.** Many n-gram systems smooth only the unigram level by adding $k$, and handle the higher orders with discounting or interpolation.

## Pitfalls

- **Too much mass to unseen events.** With $|V| \gg c(h)$, the unseen words take most of every row, as in the bigram example. The perplexity of a word model with add-one smoothing is usually much worse than with any discounting method.
- **The same share for every unseen event.** An unseen word gets $k/(c(h) + k|V|)$ whether it is common or rare in general. A lower-order model, as in interpolation or backoff, gives better shares.
- **The vocabulary must be fixed.** $|V|$ must count every token that can be predicted, with `</s>` and `<unk>`. Values computed with different $V$ are not comparable, and a value of $|V|$ that misses a token gives rows that do not sum to 1.
- **Do not add to $c(h)$ only.** The denominator must grow by $k|V|$, the sum of the added counts, not by $k$.
- **Raw counts after smoothing.** The adjusted counts $c^*$ of seen events are lower than the counts, often much lower. Report probabilities, or adjusted counts, not the sum of the two.

## Exercises

1. Show that $P_k(\cdot \mid h)$ sums to 1 over $V$ and that it equals the uniform distribution when $c(h) = 0$.
2. For the CG context above, compute the add-k estimates with $k = 1/2$, and check that they sum to 1.
3. In the word bigram example, find the value of $k$ for which the unseen words get half of the row.
4. Show that $P_k(w \mid h) \to c(h w)/c(h)$ as $k \to 0$ for $c(h) > 0$, and $P_k(w \mid h) \to 1/|V|$ as $k \to \infty$.
5. Show that the posterior mean of a Dirichlet distribution with parameters $c(h w) + k$ is $P_k(w \mid h)$.

## References
