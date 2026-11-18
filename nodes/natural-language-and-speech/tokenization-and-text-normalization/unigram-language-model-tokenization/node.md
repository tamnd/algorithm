---
tag: 9PE3NB
kind: algorithm
slug: unigram-language-model-tokenization
name: Unigram language model tokenization
aliases:
- unigram tokenizer
- Kudo unigram segmentation
area: natural-language-and-speech/tokenization-and-text-normalization
level: advanced
summary: Kudo's subword method. Fit a unigram model over pieces by EM, prune pieces that least lower the likelihood, and segment by Viterbi.
solves: [text-tokenization]
model: word-ram
complexity:
  vars: {n: the length of the word in characters, m: the length of the longest piece, N: the total length of the corpus in characters, V: the vocabulary size (number of pieces)}
  time: {encode: O(n m), em_step: O(N m), exact_losses: O(V N m)}
  space: {encode: O(n), model: O(V m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Taku Kudo]
  note: Kudo proposed the unigram model of pieces with EM training and loss-based pruning, as the segmenter behind subword regularization. It is one of the two models of the SentencePiece library.
prereqs: [subword-tokenization, viterbi-algorithm, forward-backward-algorithm, expectation-maximization]
see_also: [subword-regularization, byte-pair-encoding, wordpiece, bpe-dropout, word-lattice, maximum-likelihood-estimation, language-model, optimal-tokenization-hardness]
sources:
  - paper: doi:10.18653/v1/P18-1007
    title: Taku Kudo, Subword regularization, Improving neural network translation models with multiple subword candidates, ACL 2018, pages 66 to 75
    locator: Section 3.2, Unigram language model (Equations 6 and 7, the EM objective and the four-step vocabulary algorithm with eta = 80, page 68), the seed vocabulary paragraph (page 69), and Section 3.3, Subword sampling
  - paper: doi:10.18653/v1/D18-2012
    title: Taku Kudo and John Richardson, SentencePiece, A simple and language independent subword tokenizer and detokenizer for neural text processing, EMNLP 2018 System Demonstrations
    locator: the library that ships the unigram model as one of its two segmentation algorithms
---

Unigram language model tokenization splits a word into subword pieces by giving each piece of a fixed vocabulary a probability and choosing the split whose pieces have the largest product of probabilities. Taku Kudo introduced it in 2018, together with a training method: start from a large set of candidate pieces, fit the probabilities by [expectation maximization](/expectation-maximization/), and drop the pieces whose loss hurts the model least, until the vocabulary has the size wanted. Unlike [byte-pair encoding](/byte-pair-encoding/), the model gives a probability to every split, which is what [subword regularization](/subword-regularization/) samples from.

## In plain words

Every piece in the vocabulary has a score that says how common it is. To cut a word, look at every way to write it as a row of known pieces, multiply the scores along each row, and keep the row with the best total. A table filled from left to right finds that row without listing every row.

To learn the scores, start with a large pile of candidate pieces. Guess the scores, then count how often each piece would be used if the words were cut with the current scores, weighting each possible cut by how likely it is. Turn the counts into new scores and repeat. Then throw away the pieces the corpus can best do without, keep every single letter so that every word can still be cut, and repeat until the pile is small enough.

## The problem

The input of training is a corpus of words with their counts and a target size $T$. The output is a vocabulary of pieces (nonempty strings) and a probability $p(w)$ for each piece $w$, with $\sum_w p(w) = 1$. The input of encoding is a word $x$ of $n$ characters, and the output is a segmentation of $x$: a list of pieces whose concatenation is $x$.

The model is a [unigram language model](/language-model/) of pieces: the pieces of a segmentation $s$ are independent, so (Kudo's Equation 6)

$$P(s) = \prod_{w \in s} p(w), \qquad P(x) = \sum_{s} P(s),$$

where the sum runs over all segmentations $s$ of $x$. Encoding returns $\arg\max_s P(s)$ (Equation 7). Training maximizes the corpus log likelihood $L = \sum_x f_x \log P(x)$, where $f_x$ is the count of the word $x$; all logs on this page are natural logs. Positions in a word are fenceposts $0, \ldots, n$, and the piece $x[i{:}j]$ covers the characters between positions $i$ and $j$. The pieces $x[i{:}j]$ of the vocabulary are the edges of a [word lattice](/word-lattice/) on these positions, and a segmentation is a path from $0$ to $n$.

## The algorithm

Encoding is the [Viterbi algorithm](/viterbi-algorithm/) on the lattice, in the VITERBI semiring (log probabilities, plus = max, times = +):

```pseudo id=viterbi
VITERBI(x, p)
V1  best[j] ← -∞ for j = 0..n
V2  best[0] ← 0
V3  for j ← 1 to n
V4      for i ← max(0, j - m) to j - 1
V5          if x[i:j] is a piece and best[i] > -∞
V6              if best[i] + log p(x[i:j]) > best[j] then best[j] ← that value; back[j] ← i
V7  follow back[] from n to 0, collecting the pieces x[back[j]:j]
V8  return best[n] and the pieces in left-to-right order
```

One EM step uses the [forward-backward algorithm](/forward-backward-algorithm/) on the same lattice, in the LOG semiring (log probabilities, plus = log-add, times = +). The forward value $\alpha[j]$ is the log of the total probability of the segmentations of $x[{:}j]$, and the backward value $\beta[i]$ is that of $x[i{:}]$. The piece $x[i{:}j] = w$ is used with posterior probability $\exp(\alpha[i] + \log p(w) + \beta[j] - \log P(x))$.

```pseudo id=em
EM-STEP(corpus, p)
E1  C[w] ← 0 for every piece w
E2  for each word x with count f in the corpus
E3      for each piece w, with E[c_w] the expected uses of w in x (forward-backward)
E4          C[w] ← C[w] + f · E[c_w]
E5  Z ← the sum of C[w] over the pieces
E6  return the model p'(w) = C[w] / Z
```

Training follows the four steps of Kudo's Section 3.2. The loss of a piece $w$ is $L(p) - L(p_{-w})$, where $p_{-w}$ is $p$ without $w$, renormalized.

```pseudo id=main
TRAIN-UNIGRAM(corpus, T, eta)
T1  seed ← every character, plus the most frequent substrings of the words
T2  p ← the relative frequencies of the seed pieces
T3  loop
T4      run a few EM steps on p
T5      give each character of probability 0 the smallest positive probability, drop other pieces of probability 0, and renormalize
T6      if p has at most T pieces, or only characters, then return p
T7      loss(w) ← L(p) - L(p without w), for each piece w of length 2 or more
T8      k ← max(T, ⌊eta · |p|⌋) - (the number of characters)
T9      keep the k pieces of largest loss
T10     p ← the characters and the kept pieces
T11     renormalize p
```

Kudo gives $\eta = 80$ percent of the pieces per round as an example value, and keeps the single characters to avoid unknown words. Line T5 is a choice of this page: plain EM can give a character probability 0 when longer pieces always cover it, and such a character would no longer help a new word. The seed of line T1 comes from frequent substrings; Kudo suggests the [enhanced suffix array](/enhanced-suffix-array/) to list them in linear time, and does not let a piece cross a word boundary. The code here counts the substrings up to a fixed length directly.

## Example

Take the model h 0.1, u 0.1, g 0.1, s 0.15, hu 0.1, ug 0.15, hug 0.2, gs 0.05 and ugs 0.05, and the word "hugs". Every split of "hugs" except the whole word is possible, which gives 7 segmentations:

| segmentation | probability | posterior |
|---|---|---|
| hug s | 0.03 | 0.6757 |
| h ugs | 0.005 | 0.1126 |
| hu gs | 0.005 | 0.1126 |
| h ug s | 0.00225 | 0.0507 |
| hu g s | 0.0015 | 0.0338 |
| h u gs | 0.0005 | 0.0113 |
| h u g s | 0.00015 | 0.0034 |

The total is $P(\text{hugs}) = 0.0444$, so $\log P = -3.1145$. The forward values at positions 0 to 4 are 1, 0.1, 0.11, 0.226 and 0.0444, and the backward values are 0.0444, 0.079, 0.065, 0.15 and 1 (shown as probabilities, not logs). Viterbi returns hug, s with probability 0.03. The expected number of uses of hug is $0.03 / 0.0444 = 0.6757$, and that of s is 0.7635, because s is in four of the seven segmentations.

For training, take the corpus hug 10, pug 5, pun 12, bun 4 and hugs 5. The seed holds the 7 characters and the 12 longer substrings, 19 pieces in all. The corpus log likelihood is $-110.31$ for the seed frequencies, and $-68.21$, $-55.62$ and $-54.54$ after one, two and three EM steps. With $T = 10$ training ends with the pieces hug, pun, pug and s and the 6 other characters. A new word "pugs" is then encoded as pug, s, and "bugs" as b, u, g, s.

## Correctness

The lattice paths from 0 to $n$ are exactly the segmentations, and the weight of a path is the probability of its segmentation. By induction on $j$, VITERBI finds the best path to each position, and the forward and backward passes find the total weight to and from each position; their product at an edge, over $P(x)$, is the posterior use of that edge. An EM step never lowers $L$, by Jensen's inequality and Gibbs' inequality. Training stops, because each round removes at least one piece, and it keeps every character. These are theorems, proved in proofs/correctness.md. The pruning rule is a heuristic: it does not promise the vocabulary of size $T$ with the largest likelihood.

## Complexity

Let $m$ be the length of the longest piece and $V$ the vocabulary size. With the pieces in a [trie](/trie/), the edges that start at one position are found in $O(m)$ steps, so the lattice of a word has $O(n m)$ edges, and Viterbi, forward and backward each take $O(n m)$ time in the word-RAM model, with $O(n)$ space for the tables. The code here looks up each substring in a hash table, which adds a factor $m$ for hashing. One EM step over a corpus of total length $N$ takes $O(N m)$ time, plus $O(V)$ to normalize. The exact losses of line T7 need one likelihood per piece, $O(V N m)$ in all, so a trainer for a large corpus needs a cheaper estimate of the loss.

## Properties

- **A probability for every segmentation.** The model scores all segmentations, so it gives the best one, the $k$ best, or a random one, from the same lattice.
- **Characters always kept.** Every word over the alphabet of the training corpus has a segmentation.
- **Top-down training.** BPE and [WordPiece](/wordpiece/) grow a vocabulary by merges; the unigram method shrinks a large seed.
- **No context.** The pieces are independent given the word, which is a strong assumption (a heuristic) that makes the lattice algorithms exact.

## Variants and improvements

- **Sampling.** [Subword regularization](/subword-regularization/) samples a segmentation with probability proportional to $P(s)^a$ for a smoothing value $a$, either from the $l$ best or exactly by forward filtering and backward sampling (Kudo's Section 3.3).
- **n-best decoding.** Kudo's Section 2.2 translates the $n$ best segmentations and keeps the best translation.
- **SentencePiece.** The library of Kudo and Richardson trains the model on raw text with the space as an ordinary symbol, so no word splitter is needed.

## When to use it

Use it when you want a subword vocabulary with probabilities, either to sample segmentations in training or to score them. If one fixed segmentation from a merge table is enough, [byte-pair encoding](/byte-pair-encoding/) is simpler.

## Pitfalls

- **Underflow.** The product of many piece probabilities underflows in floating point. Work with log probabilities and add them with log-add, as the code does through nlslog.
- **Whole words win on small corpora.** Maximum likelihood favors long pieces. In a measurement on the corpus of the example, $T = 12$ keeps all five words and the 7 characters, and $T = 10$ still keeps hug, pun and pug.
- **Negative loss.** Removing a piece renormalizes the others, so the loss of a piece that is almost never used can be slightly negative.
- **Ties.** Two segmentations can have the same probability, as h ugs and hu gs do above. Viterbi then returns the one it meets first.

## Implementations

## History

Kudo (2018) proposed the unigram model of pieces to get many segmentations with probabilities for subword regularization, and compared it with byte-pair encoding, which gives one segmentation. The same year, Kudo and Richardson released SentencePiece, which implements both models.

## References
