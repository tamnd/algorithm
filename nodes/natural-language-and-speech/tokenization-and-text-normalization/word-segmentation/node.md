---
tag: QD9J8H
kind: problem
slug: word-segmentation
name: Word segmentation
aliases:
- Chinese word segmentation
area: natural-language-and-speech/tokenization-and-text-normalization
level: intro
summary: Insert word boundaries into text written without spaces, as in Chinese, Japanese or Thai, or into a string of characters such as a URL.
prereqs: [text-tokenization, dictionary-problem]
see_also: [text-segmentation, dag-shortest-paths, viterbi-algorithm, unigram-language-model-tokenization, sequence-labeling, conditional-random-field, trie, morfessor]
sources:
  - url: https://aclanthology.org/J96-3004/
    title: Richard Sproat, Chilin Shih, William Gale and Nancy Chang, A stochastic finite-state word-segmentation algorithm for Chinese, Computational Linguistics 22(3), 1996
    locator: pages 377 to 404 (segmentation as a weighted finite-state problem, unknown words, and the agreement of human judges)
  - url: https://aclanthology.org/C92-1019/
    title: Keh-Jiann Chen and Shing-Huan Liu, Word identification for Mandarin Chinese sentences, COLING 1992
    locator: Section 3.1 (maximal matching over chunks of three words and the rules that break ties)
  - book: isbn:9780596157111
    title: Toby Segaran and Jeff Hammerbacher (editors), Beautiful Data, O'Reilly, 2009
    locator: Chapter 14, Peter Norvig, Natural language corpus data, pages 219 to 242 (word segmentation by dynamic programming over a unigram model)
---

Word segmentation is the problem of putting word boundaries into a string that has none, such as text in Chinese, Japanese or Thai, a hashtag, a domain name, or the output of a speech recognizer that emits characters. It is the part of [tokenization](/text-tokenization/) that is hard when a script does not separate words with spaces. The best-known algorithm is [maximum matching](/maximum-matching-segmentation/), which greedily takes the longest dictionary word at each position; the optimal version under a word model is a dynamic program over prefixes, the same recurrence as the [word break problem](/text-segmentation/). Unlike [subword tokenization](/subword-tokenization/), the goal here is the words that a reader would see, not units chosen for a vocabulary.

## In plain words

You get a string such as "thetabledownthere" and must say where the words are. Many splits use only real words: "the table down there" and "theta bled own there" are both possible. So you need a way to choose. One way is a list of words and a rule, such as "always take the longest word that fits". A better way gives each word a probability and picks the split whose words, taken together, are most likely. A computer can find that best split without trying every split, because the best split of the whole string always ends with a best split of some shorter start of it.

## Definition

**Input:** a string $s = s_1 \ldots s_n$ and a word model, either a dictionary $D$ of words or a probability $P(w)$ for each word $w$.

**Output:** boundaries $0 = b_0 < b_1 < \dots < b_k = n$. Here and below, the span $(i, j)$ covers the 1-based characters $i+1$ to $j$, so the words are $s(b_{t-1}, b_t)$ for $t = 1, \dots, k$.

The objective depends on the variant:

- **Dictionary segmentation.** Every word is in $D$. The decision question is whether such a split exists; an algorithm may also be asked for the split with the fewest words.
- **Most likely segmentation.** Maximize $\prod_t P(s(b_{t-1}, b_t))$ under a unigram model, or the probability under an $n$-gram model of the words. With natural logarithms this is the sum $\sum_t \ln P(w_t)$.
- **Segmentation with unknown words.** Real text has words that are in no dictionary, such as names. The model must give some probability to words that it has never seen, see [out-of-vocabulary word](/out-of-vocabulary-word/).

There is no single right answer for natural language. Segmentation standards for the same language differ, for example on whether a compound or a name with a title is one word, and Sproat et al. (1996) found that native speakers also disagree. So a system is scored against one standard, with precision and recall of the words.

## Variants

- **Character tagging.** Label each character with its place in a word, for example B (begin), M (middle), E (end) and S (single). A [sequence labeling](/sequence-labeling/) model such as a [conditional random field](/conditional-random-field/) then predicts the tags. This handles unknown words better than a dictionary.
- **Lattice segmentation.** Keep all dictionary splits as a lattice of words and let a later stage, such as a [part-of-speech tagger](/part-of-speech-tagging/) or a speech recognizer, choose. Japanese morphological analyzers do segmentation and tagging together in this way.
- **Compound splitting.** In German or Dutch, long compounds are written as one word, and machine translation or search may split them into their parts.
- **Unsupervised segmentation.** With no dictionary, a model learns the words from unsegmented text, as in [Morfessor](/morfessor/) for morphemes.
- **Hashtags, URLs and identifiers.** Split "nowhiring" or a domain name into English words, usually with word frequencies from the web.

## Examples

Take the string "thetabledownthere" ($n = 17$) and unigram counts from a small corpus: the 30, a 6, there 5, down 4, table 3, own 2, here 2, and theta, bled, tab, led 1 each, 56 tokens in all, with $P(w) = $ count / 56. Three splits use only these words: "the table down there", "the tab led own there" and "theta bled own there". The table shows the best log probability of each reachable prefix and the last word of its best split.

| prefix length $j$ | prefix | best $\ln P$ | last word | starts at |
|---|---|---|---|---|
| 3 | the | -0.624 | the | 0 |
| 5 | theta | -4.025 | theta | 0 |
| 6 | thetab | -4.650 | tab | 3 |
| 8 | thetable | -3.551 | table | 3 |
| 9 | thetabled | -8.051 | bled | 5 |
| 12 | thetabledown | -6.190 | down | 8 |
| 15 | thetabledownthe | -6.814 | the | 12 |
| 17 | thetabledownthere | -8.606 | there | 12 |

At $j = 9$ the two candidates are "bled" after "theta" ($-4.025 - 4.025 = -8.051$) and "led" after "thetab" ($-4.650 - 4.025 = -8.675$), so "bled" wins. At $j = 12$ the word "down" after "thetable" gives $-6.190$, which beats "own" after "thetabled". Following the last words back from $j = 17$ gives "the table down there", with $\ln P = -8.606$. Greedy longest match from the left takes "theta" first and ends with "theta bled own there", with $\ln P = -13.799$.

A second example is the string "nowhere": "nowhere" and "now here" are both English. Only context, or a model of word sequences, can choose.

## Known algorithms

- **[Maximum matching](/maximum-matching-segmentation/).** Forward, backward or bidirectional longest match against a dictionary, $O(nL)$ time for longest word length $L$ with a [trie](/trie/). It is fast and needs only a word list, but it is not optimal under any probability model. Chen and Liu (1992) refine it by looking at chunks of three words and breaking ties by rules.
- **Dynamic programming over prefixes.** For the unigram model, $\mathrm{best}[j] = \max_{j - L \le i < j} \mathrm{best}[i] + \ln P(s(i, j))$. This is the [Viterbi algorithm](/viterbi-algorithm/) on a chain of positions, and Norvig (2009) gives a short program for English. With a bigram model the state is the position and the last word.
- **Weighted finite-state transducers.** Sproat et al. (1996) compose a dictionary transducer with weights from $-\ln P$ and take the best path, which also allows models for names and other unknown words.
- **Character taggers.** Conditional random fields over the B, M, E, S tags, and later neural taggers, are the standard for languages without spaces when labeled data exist.

## Bounds

A string of length $n$ has $2^{n-1}$ ways to place boundaries, so trying all splits is exponential. The dynamic program does $O(nL)$ dictionary lookups, where $L$ is the length of the longest word; with a trie walked from each start, each lookup step costs $O(1)$ and the total is $O(nL)$. Every algorithm must read the whole string, so $\Omega(n)$ time is needed. A bigram model makes the state a position together with the last word, which has at most $L$ choices, so the cost rises to $O(nL^2)$ transitions.

## Reductions

- **To shortest paths.** Make a node for each position $0, \dots, n$ and an edge from $i$ to $j$ for each dictionary word $s(i, j)$, with weight $-\ln P(s(i, j))$. A most likely segmentation is a shortest path from 0 to $n$ in this acyclic graph, see [shortest paths in a DAG](/dag-shortest-paths/). With all weights 1, the shortest path gives the fewest words.
- **To sequence labeling.** A segmentation is the same as one B, M, E or S tag per character, so any sequence labeler solves the problem.
- **From word break.** The decision version with a dictionary is the [word break problem](/text-segmentation/).

## Applications

- **Search engines** for Chinese, Japanese and Thai index words or character $n$-grams, and the choice changes [precision and recall](/precision-and-recall/).
- **Machine translation** and parsing need words, or at least consistent units, as input.
- **Speech recognition** for these languages scores word sequences with a language model, so the training text must be segmented.
- **Hashtags, URLs and code identifiers** are split into words for search, sentiment analysis and spelling correction.

## References
