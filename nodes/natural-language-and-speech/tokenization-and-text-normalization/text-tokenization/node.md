---
tag: T9MA31
kind: problem
slug: text-tokenization
name: Tokenization
aliases:
- text tokenization
area: natural-language-and-speech/tokenization-and-text-normalization
level: intro
summary: Split a raw text into a sequence of units such as words, punctuation marks, subwords or bytes that later stages of a pipeline process.
prereqs: [unicode-code-point, regular-expression]
see_also: [penn-treebank-tokenization, subword-tokenization, word-segmentation, sentence-boundary-detection, unicode-text-segmentation, byte-pair-encoding, optimal-tokenization-hardness, maximal-munch]
sources:
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, 3rd edition draft
    locator: the chapter Words and Tokens
  - url: https://www.unicode.org/reports/tr29/
    title: Unicode Standard Annex 29, Unicode Text Segmentation
    locator: Section 4 (word boundaries and the rules WB1 to WB999)
  - paper: arxiv:2412.15210
    title: Philip Whittington, Gregor Bachmann and Tiago Pimentel, Tokenisation is NP-complete, ACL 2025, pages 28133 to 28153
    locator: the two decision problems, direct tokenisation (choose a vocabulary) and bottom-up tokenisation (choose merges), both NP-complete
---

Tokenization is the problem of turning a raw text into a sequence of units, called tokens, that the next stages of a pipeline read: words and punctuation marks for a tagger or a parser, subwords or bytes for a neural language model. It has no single right answer. Each convention defines its own tokens, so tokenization is specified by a rule set or by a vocabulary, and results are comparable only under the same tokenizer. [Penn Treebank tokenization](/penn-treebank-tokenization/) is one rule set for English words, and [subword tokenization](/subword-tokenization/) is the family of methods that split words into pieces from a learned vocabulary. For scripts without spaces, the hard part is [word segmentation](/word-segmentation/).

## In plain words

A program cannot work on a text as one long row of characters. It first cuts the text into pieces. For English, a first idea is to cut at spaces, but then "end." and "end" are different pieces, and "don't" is one piece. So real tokenizers also split off punctuation and follow rules for short forms.

Different tasks want different pieces. A search engine wants words. A modern language model wants pieces from a fixed list of a few thousand to a few hundred thousand entries, so that every possible text can be written with them. Rare words are then cut into smaller known pieces, and in the end into single bytes.

## Definition

**Input:** a text $x = x_1 \ldots x_n$, a string of Unicode code points or of bytes.

**Output:** a sequence of tokens $\tau_1, \ldots, \tau_k$. In the common case each token is a span of the text: there are positions $0 \le i_1 < j_1 \le i_2 < j_2 \le \dots \le i_k < j_k \le n$, the span $(i, j)$ covers the 1-based characters $i+1$ to $j$, and the characters between spans are white space that is dropped. A tokenizer may also normalize a token (lower case, Unicode normalization, the quote marks of the Penn Treebank), or map it to an integer ID in a vocabulary of size V.

A tokenizer is specified in one of three ways:

- **By rules.** An ordered list of patterns or a lexer, as in the Penn Treebank sed script or the word boundary rules of Unicode Annex 29.
- **By a vocabulary and an encoding rule.** A set of strings with V entries and a rule that writes every text with them, such as the merge order of [byte-pair encoding](/byte-pair-encoding/) or longest match in [WordPiece](/wordpiece/).
- **By an objective.** Choose the segmentation into vocabulary items that is most likely under a model, as in the [unigram language model](/unigram-language-model-tokenization/), or that uses the fewest tokens.

## Variants

- **White space tokenization.** Split at runs of white space. Fast and reversible, but it leaves punctuation attached.
- **Rule-based word tokenization.** Separate punctuation and clitics by rules for one language, as in [Penn Treebank tokenization](/penn-treebank-tokenization/) or the [Unicode word boundary rules](/unicode-text-segmentation/).
- **Word segmentation.** For Chinese, Japanese, Thai and strings such as URLs, find the words first, see [word segmentation](/word-segmentation/).
- **Subword tokenization.** Learn a vocabulary of frequent pieces from a corpus: [byte-pair encoding](/byte-pair-encoding/), [WordPiece](/wordpiece/), the [unigram language model](/unigram-language-model-tokenization/), or [byte-level BPE](/byte-level-bpe/), which starts from the bytes of [UTF-8](/utf-8/) so that no text is out of vocabulary.
- **Character and byte tokenization.** Every character or byte is a token. There are no unknown tokens, but sequences are long.
- **Stochastic tokenization.** Sample one of several tokenizations during training, as in [BPE-dropout](/bpe-dropout/) and [subword regularization](/subword-regularization/).
- **Detokenization.** The inverse problem: rebuild the original text from the tokens. It is exact only if the tokenizer keeps white space information.

## Examples

Take the text `Don't stop.` (11 characters).

| tokenizer | tokens |
|---|---|
| white space | `Don't`, `stop.` |
| Penn Treebank | `Do`, `n't`, `stop`, `.` |
| Unicode word boundaries (words only) | `Don't`, `stop`, `.` |
| characters | `D`, `o`, `n`, `'`, `t`, (space), `s`, `t`, `o`, `p`, `.` |

The Unicode rules keep `Don't` together because an apostrophe between two letters is not a word boundary, while the Penn Treebank rule for n't splits it. A subword tokenizer gives tokens that depend on its learned vocabulary: a frequent word is one token, and a rare word becomes several pieces.

## Known algorithms

- **Regular expression rules** applied in order, as in [Penn Treebank tokenization](/penn-treebank-tokenization/), in $O(n)$ time for a fixed rule set.
- **Lexers** built from a [deterministic finite automaton](/deterministic-finite-automaton/) that read the text once and take the longest match at each point, the [maximal munch](/maximal-munch/) rule.
- **Unicode text segmentation**, a fixed set of rules over character properties, see [Unicode text segmentation](/unicode-text-segmentation/).
- **Byte-pair encoding** applies learned merges in order; **WordPiece** takes the longest vocabulary prefix of each word, in linear time with [Fast WordPiece](/fast-wordpiece-tokenization/); the **unigram model** finds the most likely split with the Viterbi algorithm.
- **Dynamic programming over prefixes** finds the split into vocabulary items with the fewest tokens or the highest probability, as in [word break](/text-segmentation/).

## Bounds

For a fixed rule set or a fixed automaton, tokenization takes $O(n)$ time, which is optimal because every character must be read. Given a vocabulary with longest entry length $L$, the split into the fewest vocabulary items is a shortest path over positions and takes $O(nL)$ time with a [trie](/trie/). The hard part is choosing the vocabulary. Whittington, Bachmann and Pimentel (2025) prove that two decision problems are NP-complete: whether some vocabulary of a given size compresses a dataset to at most a given number of tokens, and the same question for a sequence of merges as in BPE. This is a theorem; see [NP-hardness of optimal tokenization](/optimal-tokenization-hardness/). Greedy learners such as BPE are therefore heuristics for this objective.

## Reductions

- **Fewest tokens to shortest paths.** With a fixed vocabulary, make a node per position and an edge $(i, j)$ for each vocabulary item that spells the span $(i, j)$. A shortest path from 0 to $n$ in this acyclic graph is a tokenization with the fewest tokens, see [shortest paths in a DAG](/dag-shortest-paths/).
- **Most likely tokens to Viterbi decoding.** With weights $-\ln P(\text{token})$ the same graph gives the unigram language model tokenization.
- **Word segmentation is a special case** in which the units are the words of a language and the text has no spaces.

## Applications

- **Language models.** The token sequence fixes the vocabulary size V, the length of each input, and how [perplexity](/perplexity/) is counted, so perplexities are comparable only between models with the same tokenizer.
- **Search.** An [inverted index](/inverted-index/) stores terms that a tokenizer produced, often after [stemming](/stemming/) or lemmatization.
- **Treebanks and taggers.** Parsers and [part-of-speech taggers](/part-of-speech-tagging/) trained on a treebank expect its tokens.
- **Text to speech and speech recognition.** Numbers, abbreviations and symbols are first split into tokens and then expanded into words, see [TTS text normalization](/tts-text-normalization/).
- **Counting words.** The number of words of a text, and laws such as [Zipf's law](/zipfs-law/) and [Heaps' law](/heaps-law/), depend on what counts as a token.

## References
