---
tag: RMX04P
kind: concept
slug: out-of-vocabulary-word
name: Out-of-vocabulary word
aliases:
- OOV word
- unknown word problem
area: natural-language-and-speech/tokenization-and-text-normalization
level: intro
summary: A word at test time that is not in the fixed vocabulary of a model. Handled by an UNK token, by smoothing, or by splitting words into subwords.
prereqs: [n-gram-language-model, text-tokenization]
see_also: [subword-tokenization, byte-pair-encoding, heaps-law, zipfs-law, good-turing-estimation, laplace-smoothing, perplexity, subword-information-embeddings]
sources:
  - url: https://aclanthology.org/P16-1162/
    title: Rico Sennrich, Barry Haddow and Alexandra Birch, Neural machine translation of rare words with subword units, ACL 2016
    locator: pages 1715 to 1725 (open-vocabulary translation by splitting rare words into subword units learned by byte-pair encoding)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 5, Section 5.1.1 (Heaps' law, the growth of the vocabulary with the size of the collection)
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, 3rd edition draft
    locator: the chapter on n-gram language models (unknown words and the UNK token)
---

An out-of-vocabulary (OOV) word is a word token in the input of a model, at test or use time, whose type is not in the fixed vocabulary that the model was built with. A word-level model cannot score or produce such a word directly, so every system with a fixed vocabulary needs a plan for it. The three usual plans are to map unknown words to one special token UNK, to reserve probability for unseen words by [smoothing](/laplace-smoothing/), and to remove the problem by [subword tokenization](/subword-tokenization/), which writes every word with smaller known pieces. The OOV rate of a test text is the fraction of its tokens that are OOV.

## In plain words

A model learns its words from training text. Later it meets a word it has never seen: a new name, a rare word, a spelling error, or a number. It has no entry for that word. You can treat all such words as one "unknown" word, you can save a little probability for anything new, or you can cut words into pieces, such as "un", "believ" and "able", that the model knows. New words never stop coming: the more text you read, the more new words you find.

## The idea

Let $W$ be the vocabulary of a model, a set of V word types, for example all types seen at least $c$ times in the training text, or the V most frequent ones. A token $w$ of a new text is OOV if $w \notin W$. The idea rests on three facts.

- **New words keep coming.** By [Heaps' law](/heaps-law/), the number of distinct types in $T$ tokens grows like $kT^b$ with $b$ near one half, so the vocabulary does not converge as a corpus grows. This is a measured law, not a theorem. It follows that a fixed vocabulary has a non-zero OOV rate on new text, and the rate is higher in a new domain.
- **Most types are rare.** By [Zipf's law](/zipfs-law/), a large share of the types in any corpus occur once or twice. Cutting the vocabulary to frequent types removes many types but only a small share of the tokens. This is also a measured law.
- **The unseen mass can be estimated.** The [Good-Turing estimate](/good-turing-estimation/) of the probability that the next token is a type not seen so far is $N_1/N$, the fraction of tokens whose type occurs exactly once. This is an estimator with known properties, not a measurement of one corpus.

The main ways to handle OOV words follow from these facts:

- **UNK token.** Replace OOV tokens by one token UNK, and train its probability by replacing rare training words with UNK too. The model then gives one probability to all unknown words together.
- **Smoothing.** [Add-one smoothing](/laplace-smoothing/), Good-Turing and later methods move probability from seen to unseen events.
- **Word features.** A tagger can guess the tag of an unknown word from its suffix, capital letters and digits, as in the unknown-word models of [HMM part-of-speech taggers](/hmm-part-of-speech-tagger/).
- **Subwords, characters or bytes.** [Byte-pair encoding](/byte-pair-encoding/), [WordPiece](/wordpiece/) and the [unigram model](/unigram-language-model-tokenization/) split a word into known pieces. [Byte-level BPE](/byte-level-bpe/) starts from all 256 byte values, so no input is OOV. Sennrich, Haddow and Birch (2016) used BPE to translate rare and unseen words.
- **Composed representations.** [Subword information embeddings](/subword-information-embeddings/) build a vector for an unseen word from the vectors of its character $n$-grams.

## Examples

**OOV rate.** Train on "the cat sat on the mat" and take $W$ = {the, cat, sat, on, mat}, so V = 5. The test text "the dog sat on the rug" has 6 tokens, of which "dog" and "rug" are OOV, so the OOV rate is 2/6, about 33%.

**Good-Turing.** In the training text, the type "the" occurs twice and "cat", "sat", "on" and "mat" occur once each, so $N_1 = 4$ and $N = 6$. The estimate of the probability that the next token is a new type is $4/6$. In a large corpus $N_1/N$ is much smaller, but by Heaps' law new types keep coming, so it stays above zero.

**Perplexity with UNK.** Perplexities are comparable only between models with the same vocabulary. Take the extreme vocabulary $W$ = {UNK}: every token maps to UNK, the model gives it probability 1, and the [perplexity](/perplexity/) of every text is 1, although the model has learned nothing. A smaller vocabulary in general maps more tokens to UNK and lowers perplexity for this reason alone. So report the OOV rate and the vocabulary with the perplexity, or compare models that write every text with the same units.

## Where it is used

- **Language models.** Word $n$-gram models use UNK and smoothing; neural language models mostly use subword or byte vocabularies, so OOV words become sequences of pieces.
- **Speech recognition.** A word that is not in the pronunciation lexicon cannot be recognized, and the recognizer outputs a similar known word instead, which also hurts the words around it. Systems add subword units or grow the lexicon, see [automatic speech recognition](/automatic-speech-recognition/).
- **Machine translation.** Names and rare words must be copied, transliterated or built from subwords, see [machine translation](/machine-translation/).
- **Tagging and parsing.** Unknown words are harder to tag than known words, so taggers use suffix and shape features for them.
- **Search.** A query term that is not in the index matches nothing, which is one reason for [stemming](/stemming/) and spelling correction, see [noisy channel spelling correction](/noisy-channel-spelling-correction/).

## References
