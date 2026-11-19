---
tag: NGSSK3
kind: model
slug: n-gram-language-model
name: N-gram language model
aliases:
- n-gram model
- Markov language model
area: natural-language-and-speech/language-modeling
level: intro
summary: A language model that conditions each token only on the n - 1 tokens before it, with probabilities estimated from counts in a corpus and smoothed to fill the zeros.
prereqs: [language-model, markov-chain, maximum-likelihood-estimation]
see_also: [laplace-smoothing, good-turing-estimation, katz-backoff, kneser-ney-smoothing, perplexity, kmer, interpolated-markov-model, neural-probabilistic-language-model]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part I, the series of approximations to English by letter and word sources of increasing order
  - paper: "C. E. Shannon, Prediction and entropy of printed English, Bell System Technical Journal 30(1), 1951, pages 50 to 64"
    title: Shannon 1951
    locator: the entropy of English letters estimated from n-gram statistics and from human prediction
  - paper: doi:10.1006/csla.1999.0128
    title: Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Computer Speech and Language 13(4), 1999, pages 359 to 394
    locator: the comparison of smoothing methods for n-gram models over several corpora and training sizes
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999
    locator: Chapter 6 (statistical inference, n-gram models over sparse data)
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: chapter N-gram Language Models (draft of January 2026)
---

An n-gram language model predicts each token of a sequence from the $n - 1$ tokens just before it and from nothing else, and it learns these predictions by counting. A bigram model ($n = 2$) predicts each word from the previous word, and a trigram model ($n = 3$) from the previous two. The same model on DNA, with the four bases as tokens, is the k-mer Markov model used in gene finding and sequence analysis (see [k-mer](/kmer/) and [interpolated Markov model](/interpolated-markov-model/)). It is the oldest practical [language model](/language-model/), it is fast to train and to query, and its central problem is that most possible n-grams never occur in the training data, which is what the smoothing methods of this area solve.

## The machine

Fix the order $n \ge 1$ and a vocabulary $V$ of predicted tokens, with the end marker `</s>` and an unknown-word token `<unk>`. Each sentence $w_1, \ldots, w_m$, with $w_m = \langle /s \rangle$, is padded on the left with $n - 1$ start markers `<s>`, written $w_{2-n}, \ldots, w_0$. The **history** of token $w_i$ is the tuple $u_i = w_{i-n+1}, \ldots, w_{i-1}$ of the $n - 1$ tokens before it.

The model is a table that gives, for each history $u$, a distribution $P(\cdot \mid u)$ on $V$. The probability of a sentence is

$$P(w_1, \ldots, w_m) = \prod_{i=1}^{m} P(w_i \mid w_{i-n+1}, \ldots, w_{i-1}).$$

This is the chain rule of a language model with the **Markov assumption** that only the last $n - 1$ tokens matter. The model is a [Markov chain](/markov-chain/) whose states are the histories; the unigram model ($n = 1$) has one state and treats a sentence as a bag of independent tokens.

The **maximum likelihood estimate** from a training corpus is a ratio of counts. Let $c(u\,w)$ be the number of positions where history $u$ is followed by $w$, and $c(u) = \sum_{w \in V} c(u\,w)$. Then

$$P_{\mathrm{ML}}(w \mid u) = \frac{c(u\,w)}{c(u)}.$$

For each $u$ the likelihood $\prod_w P(w \mid u)^{c(u w)}$ is largest at these values, by Gibbs' inequality, and the histories do not share parameters, so this is the joint maximum. It gives probability 0 to every n-gram not seen in training, and it is undefined for a history not seen. A **smoothed** model replaces it with an estimate that is positive on all of $V$.

**A word example.** Train a bigram model on the three sentences "a b", "a c" and "b c". The maximum likelihood rows are:

| history $u$ | $P(\langle /s \rangle \mid u)$ | $P(a \mid u)$ | $P(b \mid u)$ | $P(c \mid u)$ |
|---|---|---|---|---|
| `<s>` | 0 | 2/3 | 1/3 | 0 |
| a | 0 | 0 | 1/2 | 1/2 |
| b | 1/2 | 0 | 0 | 1/2 |
| c | 1 | 0 | 0 | 0 |

So $P(\text{a b}) = \frac23 \cdot \frac12 \cdot \frac12 = \frac16$, $P(\text{a c}) = \frac13$ and $P(\text{b c}) = \frac16$. The model also gives $\frac16$ to "a b c" and $\frac16$ to "b", which it never saw, because it combines bigrams from different sentences. It gives 0 to "c", because no sentence starts with c. These five sentences have total probability 1.

**A DNA example.** A model of order 3 on DNA predicts each base from the two before it. If the context CG occurs 5 times in a genome, followed by A twice and by G three times, then $P_{\mathrm{ML}}(A \mid \mathrm{CG}) = 2/5$, $P_{\mathrm{ML}}(G \mid \mathrm{CG}) = 3/5$, and C and T get 0. [Laplace smoothing](/laplace-smoothing/) with pseudocounts of 1 changes these to $3/9$, $4/9$, $1/9$ and $1/9$.

## What it counts

The model is measured by its fit to held-out text and by its size and speed.

- **Fit.** The standard measure is the [perplexity](/perplexity/) on held-out text, $\exp$ of the mean of $-\ln P(w_i \mid u_i)$ over the predicted tokens. It is infinite for an unsmoothed model as soon as one test n-gram is new.
- **Parameters.** Only the seen n-grams need storage. A corpus of $N$ tokens has at most $N$ distinct n-grams of each order, so a model of order $n$ stores at most $nN$ counts, plus the backoff or interpolation weights per history. The number of possible n-grams, $|V|^n$, is far larger.
- **Time.** Counting takes one pass over the corpus, with $\Theta(nN)$ expected time when the n-grams are kept in a [hash table](/hash-table/) or a [trie](/trie/). Scoring a token takes $O(n)$ lookups for a smoothed model that combines the orders $n, n-1, \ldots, 1$.
- **Data.** The fraction of new n-grams in fresh text from the same source is estimated by $N_1/N$, the share of training tokens whose n-gram was seen exactly once, which is the [Good-Turing](/good-turing-estimation/) estimate of the unseen mass.

## Relation to other models

- **Smoothed n-gram models.** [Laplace smoothing](/laplace-smoothing/) adds a constant to every count. [Good-Turing estimation](/good-turing-estimation/) and [simple Good-Turing](/simple-good-turing/) reestimate the counts from the counts of counts. [Katz backoff](/katz-backoff/) uses discounted counts for seen n-grams and the shorter history for the rest. [Deleted interpolation](/deleted-interpolation/), [Witten-Bell smoothing](/witten-bell-smoothing/) and [absolute discounting](/absolute-discounting/) mix the orders with weights per history. [Kneser-Ney smoothing](/kneser-ney-smoothing/) and [modified Kneser-Ney smoothing](/modified-kneser-ney-smoothing/) add a lower order built from the number of distinct contexts.
- **Large-scale variants.** [Stupid backoff](/stupid-backoff/) drops normalization to scale to web corpora, [entropy-based pruning](/entropy-based-ngram-pruning/) removes n-grams whose loss changes the model least, and a [cache language model](/cache-language-model/) mixes in the counts of the recent text.
- **Biology and compression.** The k-mer Markov models of DNA are n-gram models on bases, and the [interpolated Markov model](/interpolated-markov-model/) of gene finders mixes orders as deleted interpolation does. [Prediction by partial matching](/prediction-by-partial-matching/) in text compression is an n-gram model whose escape probabilities gave rise to Witten-Bell smoothing.
- **Neural models.** The [neural probabilistic language model](/neural-probabilistic-language-model/) keeps the fixed window of $n - 1$ tokens but shares parameters through word vectors, so similar histories get similar predictions. The [recurrent neural network language model](/recurrent-neural-network-language-model/) and the [transformer](/transformer/) drop the fixed window. The [maximum entropy language model](/maximum-entropy-language-model/) uses n-grams as features of a log-linear model.
- **Hidden Markov models.** A [hidden Markov model](/hidden-markov-model/) has a Markov chain on hidden states, with the tokens as emissions. In an n-gram model the states are the visible histories.

## Known results in the model

- **The maximum likelihood estimate is a ratio of counts,** as shown above, and it is the estimate that the unsmoothed model uses.
- **A smoothed model is a distribution on sentences.** If every history gives `</s>` a positive probability, then, since there are finitely many histories, the probabilities of all finite sentences sum to 1 (see [language model](/language-model/)).
- **Shannon's approximations.** Shannon (1948) generated text from letter and word models of increasing order and showed that it looks more like English as the order grows. Shannon (1951) used n-gram statistics of English letters, and the predictions of human readers, to estimate the entropy of printed English.
- **Sparsity grows with the order.** For a fixed corpus, raising $n$ lowers the perplexity on the training text but raises the share of test n-grams that are new, so on held-out text the best order depends on the amount of data and on the smoothing.
- **Comparisons of smoothing.** Chen and Goodman (1999) compared the smoothing methods above over several corpora and training sizes, measured by cross-entropy on held-out text, and found that their modified Kneser-Ney smoothing did best.

## References
