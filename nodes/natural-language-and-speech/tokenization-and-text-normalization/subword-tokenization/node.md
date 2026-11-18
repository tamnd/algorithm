---
tag: 3VESRT
kind: concept
slug: subword-tokenization
name: Subword tokenization
aliases:
- subword segmentation
- subword units
area: natural-language-and-speech/tokenization-and-text-normalization
level: core
summary: Represent words as sequences of frequent pieces learned from data, so that a fixed vocabulary covers every word and rare words share pieces.
prereqs: [text-tokenization, out-of-vocabulary-word]
see_also: [byte-pair-encoding, wordpiece, unigram-language-model-tokenization, byte-level-bpe, subword-regularization, morfessor, optimal-tokenization-hardness, word-lattice]
sources:
  - paper: doi:10.18653/v1/P16-1162
    title: Rico Sennrich, Barry Haddow and Alexandra Birch, Neural machine translation of rare words with subword units, ACL 2016
    locator: the section on byte pair encoding (the merge learning algorithm over characters, and the toy vocabulary low, lower, newest, widest)
  - paper: doi:10.1109/ICASSP.2012.6289079
    title: Mike Schuster and Kaisuke Nakajima, Japanese and Korean voice search, ICASSP 2012, pages 5149 to 5152
    locator: Section 3, Segmentation and word inventory (page 5150)
  - paper: doi:10.18653/v1/P18-1007
    title: Taku Kudo, Subword regularization, Improving neural network translation models with multiple subword candidates, ACL 2018, pages 66 to 75
    locator: Section 3 (the unigram language model and its training)
  - paper: doi:10.18653/v1/D18-2012
    title: Taku Kudo and John Richardson, SentencePiece, A simple and language independent subword tokenizer and detokenizer for neural text processing, EMNLP 2018 System Demonstrations, pages 66 to 71
    locator: the library that trains BPE and unigram models directly on raw text
  - url: https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
    title: Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei and Ilya Sutskever, Language models are unsupervised multitask learners, OpenAI technical report, 2019
    locator: Section 2.2, Input Representation (BPE over bytes with a base vocabulary of 256)
---

Subword tokenization splits text into pieces that are often smaller than words and larger than characters. The pieces come from a fixed vocabulary that is learned from a training corpus. Frequent words stay whole, and rare words are spelled with several frequent pieces, so the vocabulary has a fixed size and still covers every word. It is a form of [text tokenization](/text-tokenization/), and it is the main remedy for the [out-of-vocabulary word](/out-of-vocabulary-word/) problem in neural models. This page gives the common idea; the pages of the methods give the algorithms.

## In plain words

A model can only read tokens from a list it knows. If the list holds whole words, a new word such as a name or a rare form is unknown to the model. If the list holds single letters, every word is known, but each sentence becomes a very long row of letters, which is slow and hard to learn from.

Subword tokenization takes the middle way. The list holds all single letters, so nothing is ever unknown, plus a few thousand frequent pieces such as "ing", "low" or "est", and frequent whole words. A common word is one token. A rare word is a few pieces that the model has seen many times in other words. The size of the list is a dial: a longer list gives shorter rows of tokens.

## The idea

Let $V$ be the vocabulary size, the number of pieces in the vocabulary. A segmentation of a word $x$ of $n$ characters is a sequence of pieces from the vocabulary whose concatenation is $x$. On this page, positions in a word are fenceposts $0, \ldots, n$ between the characters, and the piece $x[i{:}j]$ covers the characters after position $i$ up to position $j$. The segmentations of $x$ are then the paths from $0$ to $n$ in a [word lattice](/word-lattice/) with one edge $i \to j$ for each piece $x[i{:}j]$ in the vocabulary.

Coverage (theorem). If the vocabulary contains every character of the alphabet, every string over the alphabet has at least one segmentation: the one with one piece per character. [Byte-level BPE](/byte-level-bpe/) uses the 256 byte values as the alphabet, so every text has a segmentation once it is written in [UTF-8](/utf-8/).

The trade-off (theorem for BPE, measurement in general). For a fixed corpus, a larger vocabulary gives fewer tokens. In [byte-pair encoding](/byte-pair-encoding/), each merge adds one piece and replaces each counted occurrence of the merged pair with one token, so the token count of the training corpus falls by exactly the count of the pair. The two ends of the dial are the characters (small $V$, long sequences) and the words (short sequences, but $V$ grows without bound with the corpus, as [Heaps' law](/heaps-law/) describes, and unseen words are not covered).

Methods differ in two choices:

- **How the vocabulary is built.** [BPE](/byte-pair-encoding/) adds the most frequent pair of adjacent pieces, greedily. [WordPiece](/wordpiece/) adds the pair that most raises the likelihood of a [language model](/language-model/). The [unigram language model](/unigram-language-model-tokenization/) starts from a large set of pieces and removes those whose loss lowers the likelihood the least. [Morfessor](/morfessor/) minimizes a two-part code length. Finding the vocabulary that gives the fewest tokens is NP-hard, as [optimal tokenization hardness](/optimal-tokenization-hardness/) shows, so all these builders are heuristics.
- **How a word is segmented.** BPE replays its merges. WordPiece takes the longest matching piece from the left. The unigram model takes the most probable path in the lattice by the [Viterbi algorithm](/viterbi-algorithm/), in the VITERBI semiring (max, times) over piece probabilities. [Subword regularization](/subword-regularization/) and [BPE-dropout](/bpe-dropout/) sample a different segmentation each time during training.

## Examples

**The trade-off on a small corpus (measurement).** Take the corpus of Sennrich, Haddow and Birch (2016): "low" 5 times, "lower" 2 times, "newest" 6 times and "widest" 3 times. It has 16 words, 79 characters and 10 distinct characters. Plain BPE, with ties broken to the smallest pair, can make at most 12 merges. The table gives, after $k$ merges, the vocabulary size $V = 10 + k$ and the number of tokens in the corpus.

| merges k | vocabulary size V | tokens in the corpus |
|---|---|---|
| 0 | 10 | 79 |
| 1 | 11 | 70 |
| 2 | 12 | 61 |
| 3 | 13 | 54 |
| 4 | 14 | 47 |
| 5 | 15 | 41 |
| 6 | 16 | 35 |
| 7 | 17 | 29 |
| 8 | 18 | 26 |
| 9 | 19 | 23 |
| 10 | 20 | 20 |
| 11 | 21 | 18 |
| 12 | 22 | 16 |

The first merges are e + s, es + t, l + o and lo + w, each of which saves 9 or 7 tokens; the last merges save only 2. At 12 merges every word is one token, which is word-level tokenization of this corpus.

**An unseen word.** The word "lowest" is not in the corpus. A word-level vocabulary of the four words cannot represent it. With the 4 merges above it becomes low + est, two pieces that the model has seen in other words. The unseen word "slower" becomes s + low + e + r after 4 merges, s + low + er after 11 and s + lower after 12.

**Probabilistic segmentation.** With the unigram model of the [unigram language model](/unigram-language-model-tokenization/) page, the word "hugs" has 7 segmentations, and the most probable is hug + s. The other segmentations stay available for sampling.

## Where it is used

- **Neural machine translation.** Sennrich, Haddow and Birch (2016) used BPE pieces so that a translation model with a fixed vocabulary could translate rare words and names. See [machine translation](/machine-translation/).
- **Voice search and pretrained encoders.** Schuster and Nakajima (2012) built word pieces for Japanese and Korean voice search. WordPiece is the tokenizer of [BERT](/bert/), and [Fast WordPiece tokenization](/fast-wordpiece-tokenization/) encodes it in linear time.
- **Language models over any text.** Radford et al. (2019) ran BPE on bytes for GPT-2, so that the model gives a probability to every Unicode string.
- **Language-independent tokenizers.** SentencePiece (Kudo and Richardson 2018) trains BPE or unigram models on raw text, with the space treated as an ordinary symbol, so no word splitter for the language is needed.
- **Morphology without supervision.** [Morfessor](/morfessor/) finds pieces that often match morphs, a cheap substitute for [morphological analysis](/morphological-analysis/).
- **Robust training.** [Subword regularization](/subword-regularization/) and [BPE-dropout](/bpe-dropout/) feed the model many segmentations of the same text.

## References

- Rico Sennrich, Barry Haddow and Alexandra Birch. Neural machine translation of rare words with subword units. ACL 2016. doi:10.18653/v1/P16-1162.
- Mike Schuster and Kaisuke Nakajima. Japanese and Korean voice search. ICASSP 2012, pages 5149 to 5152. doi:10.1109/ICASSP.2012.6289079.
- Taku Kudo. Subword regularization: improving neural network translation models with multiple subword candidates. ACL 2018, pages 66 to 75. doi:10.18653/v1/P18-1007.
- Taku Kudo and John Richardson. SentencePiece: a simple and language independent subword tokenizer and detokenizer for neural text processing. EMNLP 2018 System Demonstrations, pages 66 to 71. doi:10.18653/v1/D18-2012.
- Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei and Ilya Sutskever. Language models are unsupervised multitask learners. OpenAI technical report, 2019.
