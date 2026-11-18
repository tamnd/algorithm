---
tag: TM8W3C
kind: algorithm
slug: morfessor
name: Morfessor
aliases:
- Morfessor baseline
area: natural-language-and-speech/tokenization-and-text-normalization
level: advanced
summary: Unsupervised morphological segmentation of Creutz and Lagus that splits words into morphs by minimizing a two-part MDL code length of lexicon and corpus.
solves: [morphological-analysis]
model: word-ram
complexity:
  vars: {n: the length of the longest word, W: the number of word types, L: the total length of the word types}
  time: {resplit: O(n^3), epoch: O(W n^3)}
  space: {model: O(L)}
properties: {deterministic: false, exact: false, online: false, recursive: true}
history:
  year: 2002
  people: [Mathias Creutz, Krista Lagus]
  note: Creutz and Lagus proposed recursive splitting under a two-part MDL cost for Finnish and English words in 2002. Their 2007 article calls this model the Baseline of the Morfessor family.
prereqs: [minimum-description-length, morphological-analysis, maximum-likelihood-estimation]
see_also: [unigram-language-model-tokenization, byte-pair-encoding, subword-tokenization, two-level-morphology, stemming, local-search, greedy-algorithm, viterbi-algorithm]
sources:
  - paper: doi:10.3115/1118647.1118650
    title: Mathias Creutz and Krista Lagus, Unsupervised discovery of morphemes, Proceedings of the ACL-02 Workshop on Morphological and Phonological Learning, 2002, pages 21 to 30
    locator: Section 2, Method 1, Recursive segmentation and MDL cost; Section 2.1 (the cost, with k = 5 bits per character, page 23) and Section 2.2 (the recursive search, the reprocessing of seen words and the dreaming stage, pages 23 and 24)
  - paper: doi:10.1145/1187415.1187418
    title: Mathias Creutz and Krista Lagus, Unsupervised models for morpheme segmentation and morphology learning, ACM Transactions on Speech and Language Processing 4(1), article 3, 2007
    locator: Section 4.1, the Baseline model
---

Morfessor is a family of methods that learn to split words into morph-like units without any labeled data. Its first member, now called the Baseline, comes from Creutz and Lagus (2002). It searches for a lexicon of morphs and a segmentation of the corpus that make the total description short: the cost of writing down the lexicon plus the cost of the corpus coded with it. The search splits words recursively in two and keeps a split only when it lowers the total cost.

## In plain words

A word list can be stored in two parts: a dictionary of pieces, and each word written as a row of pieces from the dictionary. Long pieces make the rows short but the dictionary big. Single letters make the dictionary tiny but the rows long. Pieces such as "walk", "talk", "ed" and "ing" are a good middle: few pieces, used again and again.

Morfessor looks for this middle. It takes one word, tries it whole and cut in two at every place, and keeps the choice that makes the total smallest. If it cut the word, it does the same to each half. It goes over all the words many times, in random order, until nothing improves. It is a greedy search, so it can get stuck at a choice that a cleverer search would beat.

## The problem

The input is a corpus of word types with counts $f_w$. The output is an analysis: for each word $w$, a list of morphs whose concatenation is $w$. Let $c(m)$ be the number of times the morph $m$ is used in the corpus, weighted by the counts, and $C = \sum_m c(m)$. Following the [minimum description length](/minimum-description-length/) principle, the Baseline minimizes the two-part cost of Creutz and Lagus (2002, Section 2.1), here in nats (natural logs):

$$\mathrm{cost} = \sum_{\text{morph tokens}} -\ln \frac{c(m)}{C} + K \sum_{\text{morph types}} \mathrm{len}(m) = C \ln C - \sum_m c(m) \ln c(m) + K \sum_{\text{morph types}} \mathrm{len}(m).$$

The first part is the code length of the corpus under the [maximum likelihood](/maximum-likelihood-estimation/) unigram model of morphs; the second is the code length of the lexicon, with $K$ per character. Creutz and Lagus use 5 bits per character, enough for 32 lower-case letters, which is $K = 5 \ln 2 = 3.4657$ nats.

## The algorithm

The search reprocesses one word at a time. The split of a string $s$ with count $f$ tries $s$ whole and every cut into two parts:

```pseudo id=resplit
RESPLIT(s, f)
R1  best ← the cost with s added f times; cut ← none
R2  for i ← 1 to len(s) - 1
R3      c ← the cost with s[:i] and s[i:] added f times each
R4      if c < best then best ← c; cut ← i
R5  if cut is none then add s f times and return [s]
R6  left ← RESPLIT(s[:cut], f)
R7  return left followed by RESPLIT(s[cut:], f)
```

The main loop goes over the word types in a random order and repeats until an epoch lowers the cost by less than a tolerance:

```pseudo id=main
MORFESSOR(corpus, rng)
M1  give each word the analysis [w] and count its morphs
M2  repeat
M3      for each word w, in an order shuffled by rng
M4          remove the morphs of the analysis of w (f_w times each)
M5          new ← RESPLIT(w, f_w)
M6          if the cost went up then put the old analysis back, else keep new
M7  until the cost of an epoch drops by less than the tolerance
M8  return the analysis
```

The 2002 search reads word tokens online and reprocesses a word each time it appears, and a "dreaming" stage goes over the words seen so far in random order. The code here runs only the dreaming form, in epochs over the word types. Creutz and Lagus keep the splits in a shared tree, so a chunk split once is split the same way in every word; the code here keeps one list of morphs per word type, which is simpler. Line M6 is a choice of this page: it makes the cost never rise.

A new word is segmented with the learned lexicon by a [Viterbi](/viterbi-algorithm/) pass over its positions, in the TROPICAL semiring (costs $-\ln (c(m)/C)$, plus = min, times = +). A word with no split into known morphs stays whole.

## Example

Take the corpus walk 4, walked 3, walking 3, talk 3, talked 2, talking 2, jump 3, jumped 2 and jumping 2. At the start every word is one morph: $C = 24$ tokens, a data cost of 52.000 nats, and a lexicon of 51 characters, which costs $51 K = 176.753$, so the total is 228.752.

With the seed 0 the first word is walked. Removing it and putting it back whole gives 228.752. The cut walk + ed gives 219.527, because walk is already in the lexicon and only "ed" is new. Every other cut, such as w + alked, adds two new morphs and gives 238.171. So walked becomes walk + ed. The two parts are not split further.

After one epoch the analysis is walk, walk + ed, walk + ing, talk, talk + ed, talk + ing, jump, jump + ed and jump + ing. The lexicon is walk 10, ed 7, ing 7, talk 7 and jump 7: $C = 38$ tokens, a data cost of 60.717 nats, and 17 characters, which cost 58.918, for a total of 119.634. The second epoch changes nothing, and the search stops. A new word "walkjump" is segmented as walk + jump. The word "jumps" stays whole, because "s" is not a morph.

## Correctness

RESPLIT always returns morphs that join back to the word, since it only cuts a string in two and recurses on the halves. The model keeps $C$, $\sum_m c(m) \ln c(m)$ and the lexicon length up to date under each change of a count, so each cost it compares is the exact cost. Each pass over a word either lowers the cost or restores the old analysis, so the cost never rises from epoch to epoch. These are theorems, proved in proofs/correctness.md.

The search is greedy and finds a local optimum, not the global one. With the corpus bb 11 and bbbb 9, the search keeps the morph bb in both words, at a cost of $2K$. Writing both words as single b's costs only $K$, but the search never gets there: splitting bb alone adds b and keeps bb in the lexicon for bbbb, which costs more. That the morphs found are close to linguistic morphemes is a measurement, which Creutz and Lagus report for Finnish and English.

## Complexity

Let $n$ be the length of a word. In the word-RAM model, with the morph counts in a hash table, one cost evaluation changes $O(1)$ counts and costs $O(n)$ time to hash the strings. RESPLIT tries $O(n)$ cuts at each node of its recursion, and the recursion has at most $n$ levels, each over parts of total length at most $n$, so one word costs $O(n^2)$ evaluations and $O(n^3)$ time. An epoch over $W$ word types costs $O(W n^3)$ time. The model takes $O(L)$ space for word types of total length $L$. The number of epochs is not bounded by a formula; in the examples it is small.

## Properties

- **No labels.** Only word counts are needed.
- **Two-part code.** A longer lexicon must pay for itself by shortening the coded corpus, which stops the search from keeping whole words.
- **Order-dependent.** The result depends on the order of the words and on the random seed, as for any greedy [local search](/local-search/).
- **Flat morphs.** The Baseline does not label morphs as stems or affixes.

## Variants and improvements

- **Shared split tree.** The 2002 search keeps every split in one tree of chunks with counts, so the split of a chunk is shared by every word that contains it.
- **Later models.** Creutz and Lagus (2007) describe the Baseline together with the later models of the Morfessor family.
- **Subword vocabularies.** The [unigram language model tokenization](/unigram-language-model-tokenization/) of Kudo uses a similar unigram model of pieces, trained by EM with pruning instead of an MDL cost.

## When to use it

Use it to find morph-like units in a language with rich morphology, such as Finnish or Turkish, when no analyzer or labeled data exists, for example to build a vocabulary for speech recognition. When a rule-based analyzer exists, [two-level morphology](/two-level-morphology/) or another finite-state analyzer gives linguistic analyses with features, which Morfessor does not.

## Pitfalls

- **Local optima.** The greedy split can keep a long morph that a global search would replace, as the bb example shows. Several random orders and more epochs help but do not guarantee the optimum.
- **The value of K.** The cost per lexicon character sets the balance: a large $K$ gives few short morphs and long analyses, and a small $K$ keeps whole words.
- **Not morphemes.** Morphs are strings that compress well, not morphemes with meaning; they can cut across morpheme boundaries.
- **Underflow.** The probability of the corpus is a product of thousands of morph probabilities; compute the cost as a sum of logs, never as a product.

## Implementations

## History

Creutz and Lagus (2002) presented two methods for unsupervised segmentation of words into morphs, tested on Finnish and English. The first, recursive splitting under an MDL cost, became the Morfessor Baseline. Their 2007 article in ACM Transactions on Speech and Language Processing describes the Morfessor family, with the Baseline in Section 4.1.

## References
