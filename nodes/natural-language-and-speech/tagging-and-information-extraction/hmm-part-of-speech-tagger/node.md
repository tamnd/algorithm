---
tag: GZMMN9
kind: algorithm
slug: hmm-part-of-speech-tagger
name: HMM part-of-speech tagger
aliases:
- bigram HMM tagger
- trigram HMM tagger
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Tag words with an HMM whose states are tags: tag n-gram transitions and word emissions come from counts with smoothing, and Viterbi finds the best tag sequence in O(n k^(m+1))."
solves: [part-of-speech-tagging]
model: word-ram
complexity:
  vars: {n: the number of words in the sentence, k: the number of tags, m: the order of the tag model}
  time: {worst: "Θ(n k^(m+1))"}
  space: {extra: "Θ(n k^m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1988
  people: [Kenneth W. Church, Steven J. DeRose, Thorsten Brants]
  note: "Church and DeRose published stochastic taggers with tag n-gram models in 1988. Brants described the trigram tagger TnT, with deleted interpolation and a suffix model, in 2000."
prereqs: [hidden-markov-model, viterbi-algorithm, part-of-speech-tagging]
see_also: [hmm-decoding, deleted-interpolation, universal-pos-tagset, bayesian-hmm-tagging, brill-tagger, maximum-entropy-markov-model, structured-perceptron, out-of-vocabulary-word]
sources:
  - paper: "Kenneth W. Church, A stochastic parts program and noun phrase parser for unrestricted text, Proceedings of the Second Conference on Applied Natural Language Processing (ANLP), 1988, pages 136 to 143"
    title: Church 1988
    locator: the stochastic parts program with lexical and contextual probabilities estimated from the tagged Brown corpus
  - paper: "Steven J. DeRose, Grammatical category disambiguation by statistical optimization, Computational Linguistics 14(1), 1988, pages 31 to 39"
    title: DeRose 1988
    locator: tag disambiguation with tag transition probabilities and dynamic programming
  - paper: "Thorsten Brants, TnT: a statistical part-of-speech tagger, Proceedings of the Sixth Conference on Applied Natural Language Processing (ANLP 2000), pages 224 to 231"
    title: Brants 2000
    locator: "Section 2.1 and equation 1 (the second-order model with start and end tags), Section 2.2 and Figure 1 (deleted interpolation), Section 2.3 (the suffix model), Section 2.4 (capitalization), Section 2.5 (beam search), Table 5 (Penn Treebank results)"
  - book: isbn:9780262133609
    title: "Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999"
    locator: "Chapter 10 (part-of-speech tagging, with Markov model taggers)"
---

An HMM part-of-speech tagger treats the tags of a sentence as the hidden states of a [hidden Markov model](/hidden-markov-model/) and the words as its outputs. It estimates the tag transition and word emission probabilities by counting in a tagged corpus, smooths them, and then finds the most probable tag sequence of a new sentence with the [Viterbi algorithm](/viterbi-algorithm/). The Viterbi page describes the decoder for any HMM, and [hmm-decoding](/hmm-decoding/) states the decoding problem. This page is about the tagger as a whole: the boundary tags, the order of the model, the smoothing of the transitions, the handling of unknown words and the cost of a second-order state space, as in the TnT tagger of Brants (2000).

## In plain words

Each word gets a tag such as noun or verb. The tagger learns two kinds of numbers from a corpus that people have already tagged: how often one tag follows the previous tag or two tags, and how often each tag produces each word. To tag a new sentence, it looks for the one sequence of tags that makes the sentence most likely under these numbers. There are far too many sequences to try one by one, but the best sequence that ends in a given tag at a given word only needs the best sequences that end one word earlier, so the search fills a table from left to right. Rare tag pairs get a share of the probability of shorter contexts, and a word never seen in training gets its tag guesses from its last letters.

## The problem

Input: a tagged training corpus, the tag set $Y$ with $k$ tags, an order $m \ge 1$, and a sentence $x = x_1 \ldots x_n$. Output: a tag sequence $y = y_1 \ldots y_n$ that maximizes the model probability

$$P(x, y) = \prod_{i=1}^{n+1} P(y_i \mid y_{i-m}, \ldots, y_{i-1}) \prod_{i=1}^{n} P(x_i \mid y_i),$$

where $y_{1-m} = \cdots = y_0 = \langle s \rangle$ are start tags and $y_{n+1} = \langle /s \rangle$ is the end tag. With $m = 1$ this is the bigram tagger, $P(x, y) = \prod_{i=1}^{n+1} P(y_i \mid y_{i-1}) \prod_{i=1}^{n} P(x_i \mid y_i)$. With $m = 2$ it is the trigram tagger of TnT, whose equation 1 has exactly this form with the end transition $P(t_{T+1} \mid t_T)$ at the end. Since $P(x)$ does not depend on $y$, the same $y$ also maximizes $P(y \mid x)$. Logs are natural logs.

## The algorithm

Training counts the predicted events. A sentence of $n$ tokens has $n + 1$ of them: the tags $y_1, \ldots, y_n$ and the end tag, each with its history of $m$ earlier symbols. Let $f(g)$ be the count of a tag $n$-gram $g$ whose last symbol is predicted, $f_h(c)$ the number of predicted events whose history ends with the context $c$, and $N$ the number of predicted events. The maximum likelihood estimates are $\hat P(t \mid c) = f(c\,t) / f_h(c)$ and $\hat P(t) = f(t) / N$, with $0/0 = 0$. TnT smooths by linear interpolation:

$$P(t \mid h) = \lambda_0 \hat P(t) + \lambda_1 \hat P(t \mid y_{i-1}) + \cdots + \lambda_m \hat P(t \mid y_{i-m}, \ldots, y_{i-1}).$$

The weights come from deleted interpolation (Brants 2000, Figure 1). Start with all $\lambda_j = 0$. For each $(m+1)$-gram $g$ with count $c = f(g) > 0$, compute the estimate of each order with this one event removed: $(f(g_j) - 1) / (f_h(c_j) - 1)$ for the last $j + 1$ symbols $g_j$ of $g$ with context $c_j$, and $(f(t) - 1) / (N - 1)$ for order 0, with a zero denominator giving 0. Add $c$ to the weight of the order with the largest value, then divide all weights by their sum. Brants gives no tie rule; the code gives a tie to the higher order.

Known words use $P(w \mid t) = f(w, t) / f(t)$. An unknown word uses the suffix model (Brants 2000, Section 2.3, after Samuelsson 1993). From the tokens of rare words (frequency at most 10), estimate $\hat P(t \mid \ell)$ for each suffix $\ell$ of up to 10 letters. Then smooth from the empty suffix to the longest suffix of the word that was seen: $P(t \mid \ell_i) = (\hat P(t \mid \ell_i) + \theta P(t \mid \ell_{i-1})) / (1 + \theta)$, where $\ell_i$ is the suffix of length $i$. The emission score is $P(t \mid \ell) / P(t)$, which is $P(\ell \mid t)$ up to the factor $P(\ell)$ that is the same for all tags.

```pseudo id=main
HMM-TAG(corpus, x_1 .. x_n, m)                 ▷ m = 1 bigram, m = 2 trigram (TnT)
L1  count the tag n-grams of lengths 1 .. m+1 over the predicted events, with m start tags <s> and one end tag </s> per sentence
L2  λ_0 .. λ_m ← DELETED-INTERPOLATION(counts)
L3  P(t | h) ← Σ_{j=0..m} λ_j P^(t | last j tags of h)
L4  P(w | t) ← f(w, t) / f(t) if w is known, else P(t | suffix of w) / P(t)
L5  δ_0(<s> .. <s>) ← 0                        ▷ a state is the tuple of the last m tags
L6  for i ← 1 to n do
L7      for each tag t and state g: h ← (g without its first tag, t); δ_i(h) ← max over g of δ_{i-1}(g) + log P(t | g) + log P(x_i | t); ψ_i(h) ← the first maximizing g
L8  h_n ← the first state that maximizes δ_n(h) + log P(</s> | h)
L9  for i ← n downto 1 do y_i ← the last tag of h_i; h_{i-1} ← ψ_i(h_i)
L10 return y_1 .. y_n
```

The decoder works in log space with log 0 = -inf, because a product of a few hundred probabilities underflows in double precision. The test file has a sentence of 400 words whose plain product is 0.0, while its log score is about -834.4. The smallest positive double is about $e^{-745}$. Sums in log space use the log_add form of the [log-sum-exp trick](/log-sum-exp-trick/); the Viterbi recursion itself needs only max and +.

## Example

Take a corpus of five tagged sentences, with D for determiner, J for adjective, N for noun and V for verb: "the/D dog/N runs/V", "the/D old/J dog/N runs/V", "dogs/N run/V", "the/D runs/N" and "old/J dogs/N walk/V". The bigram tagger ($m = 1$) has $N = 19$ predicted events. The tag counts are D 3, J 2, N 5, V 4 and `</s>` 5, and the history counts are `<s>` 5, D 3, J 2, N 5 and V 4. Deleted interpolation looks at the nine bigrams:

| bigram | count | bigram estimate | unigram estimate | winner |
|---|---|---|---|---|
| (`<s>`, D) | 3 | 2/4 | 2/18 | λ_1 |
| (D, N) | 2 | 1/2 | 4/18 | λ_1 |
| (N, V) | 4 | 3/4 | 3/18 | λ_1 |
| (V, `</s>`) | 4 | 3/3 | 4/18 | λ_1 |
| (J, N) | 2 | 1/1 | 4/18 | λ_1 |
| (D, J) | 1 | 0/2 | 1/18 | λ_0 |
| (`<s>`, N) | 1 | 0/4 | 4/18 | λ_0 |
| (N, `</s>`) | 1 | 0/4 | 4/18 | λ_0 |
| (`<s>`, J) | 1 | 0/4 | 1/18 | λ_0 |

So $\lambda_0 = 4/19$ and $\lambda_1 = 15/19$. For example $P(N \mid D) = \frac{4}{19} \cdot \frac{5}{19} + \frac{15}{19} \cdot \frac{2}{3} = 210/361$, $P(V \mid D) = \frac{4}{19} \cdot \frac{4}{19} = 16/361$, $P(D \mid \langle s \rangle) = 183/361$, $P(\langle /s \rangle \mid N) = 77/361$ and $P(\langle /s \rangle \mid V) = 305/361$.

Now tag "the runs". The word "runs" is a verb twice and a noun once, so $P(\text{runs} \mid V) = 2/4$ and $P(\text{runs} \mid N) = 1/5$. Only D emits "the", so $\delta_1(D) = \log(183/361)$. At word 2 only N and V emit "runs":

- $\delta_2(N) = \delta_1(D) + \log(210/361) + \log(1/5)$, so $e^{\delta_2(N)} \approx 0.0590$;
- $\delta_2(V) = \delta_1(D) + \log(16/361) + \log(1/2)$, so $e^{\delta_2(V)} \approx 0.0112$.

With the end transition, D N scores about $0.0590 \cdot 77/361 \approx 0.01258$ and D V about $0.0112 \cdot 305/361 \approx 0.00949$. The tagger returns D N. The emission alone prefers V, but "the" is rarely followed by a verb, and the context wins. On "the dog runs" the same model returns D N V. The test file checks these sequences against a search over all $k^n$ tag sequences.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has two parts. First, after position $i$ the table holds, for each state of $m$ tags, the largest log probability of a tag prefix that ends in that state; this holds because the score of the next step depends only on the previous state, the new tag and the word (the optimal substructure of [DAG dynamic programming](/dag-dynamic-programming/)). The end transition and the [traceback](/traceback/) then give a sequence of maximal $P(x, y)$. Second, the deleted interpolation weights are nonnegative and sum to 1, so each transition row is a convex combination of distributions when all its contexts were seen in training. A row whose context was never seen loses the mass of that order: TnT defines an estimate with a zero denominator as 0, so the model is deficient on such histories. This does not affect the correctness of the search, only the meaning of the scores.

## Complexity

Decoding has $k^m$ states at each position and $k$ predecessors of each state that can differ in the first tag, so the time is $\Theta(n k^{m+1})$: $\Theta(n k^2)$ for the bigram tagger and $\Theta(n k^3)$ for the trigram tagger. The back pointers take $\Theta(n k^m)$ space. Training reads the corpus once, so it is linear in its size times $m$ for the $n$-gram counts. Deleted interpolation looks at each distinct $(m+1)$-gram once. The suffix model adds up to 10 trie or table lookups per unknown word and $O(k)$ work for each suffix length. For the 45 tags of the Penn Treebank, $k^3 = 91125$ per word for a full trigram search; this is why TnT adds a beam.

## Properties

- Exact decoding: the Viterbi search finds a maximum of $P(x, y)$ under the model (a theorem, proved above). The tagger is not exact in any stronger sense: its accuracy is a measurement.
- Generative: it models $P(x, y)$ and so can use untagged text through the [Baum-Welch algorithm](/baum-welch-algorithm/), but it cannot use overlapping features of the word such as its suffix and its capitalization at the same time, except through special models such as the suffix model.
- Measured accuracy: TnT reports 96.7% on the Penn Treebank (97.0% on known tokens and 85.5% on unknown tokens, with 2.9% unknown tokens) and 96.7% on the German NEGRA corpus, each averaged over ten 90/10 splits (Brants 2000, Tables 2 and 5).
- The tie rule of the code is the first maximizer in a fixed order, so the output is deterministic.

## Variants and improvements

- Order. The bigram tagger is the HMM tagger of most textbooks. TnT uses $m = 2$; Brants reports that the second-order model with careful smoothing matches the maximum entropy tagger of Ratnaparkhi (1996).
- Context-dependent weights. One set of $\lambda$ per frequency class of the history is a common alternative. Brants reports that the groupings he tried were at best equal to one context-free set of weights, and some were worse (Section 2.2).
- Other smoothing. [Laplace smoothing](/laplace-smoothing/), [Kneser-Ney smoothing](/kneser-ney-smoothing/) and backoff can replace interpolation; the [deleted interpolation](/deleted-interpolation/) page covers the general method with held-out data.
- Capitalization. TnT adds a flag for a capitalized word to each tag in the context, which doubles the tag set (Section 2.4).
- Beam search. TnT drops each state whose score is below the best score divided by $\theta = 1000$; Brants reports about twice the speed with no change in accuracy (Section 2.5). The search is then no longer exact.
- Unsupervised training. With no tagged corpus, the [Baum-Welch algorithm](/baum-welch-algorithm/) can fit the HMM from text and a tag dictionary; the [Bayesian HMM tagger](/bayesian-hmm-tagging/) puts priors on the tables and samples instead.
- Discriminative taggers. The [maximum entropy Markov model](/maximum-entropy-markov-model/), the [structured perceptron](/structured-perceptron/) and the [conditional random field](/conditional-random-field/) keep the Viterbi search but score rich, overlapping features.

## When to use it

Use an HMM tagger when you need a fast, simple and well-understood baseline that trains by counting in seconds, or when you want a generative model that can also use untagged text. A trigram HMM with good smoothing and suffix handling is close to the discriminative feature-based taggers of the late 1990s. For the best accuracy today, use a discriminative model with word features or a neural encoder such as the [BiLSTM-CRF](/bilstm-crf/).

## Pitfalls

- Underflow: multiply probabilities in log space. A product of a few hundred probabilities is 0.0 in double precision.
- Missing end transition: without $P(\langle /s \rangle \mid h)$ the model prefers sequences that end in tags that rarely end a sentence.
- Zero transition and emission probabilities: an unsmoothed bigram that never occurred makes every sequence through it impossible. The unigram term of the interpolation keeps every tag reachable as long as $\lambda_0 > 0$.
- Unseen histories: with the TnT rule $0/0 = 0$, the transition row of an unseen history sums to less than 1. This is harmless for tagging but wrong if the scores are used as probabilities.
- The weight $\theta$ of the suffix model: Brants's text says the standard deviation of the tag probabilities, while equation 10 as printed has no square root. The code takes the square root. Check which one an implementation uses before you compare numbers.
- Second-order cost: with $k$ near 50, the state space has $k^2$ states per word. Restrict the tags of known words to those seen in training, as the code does through the zero emissions, or use a beam.

## Implementations

## History

Early taggers used hand-written rules. In 1988 Church published a stochastic parts program and DeRose a statistical tag disambiguator, both with tag sequence probabilities estimated from tagged text and a dynamic programming search. Brants (2000) gave a careful account of the details that most earlier papers left out: the start and end tags, context-independent deleted interpolation, the suffix model of Samuelsson (1993) for unknown words, a capitalization flag and a beam. He cites an independent comparison of seven taggers (Zavrel and Daelemans 1999) in which TnT had the highest accuracy and was also the fastest.

## References
