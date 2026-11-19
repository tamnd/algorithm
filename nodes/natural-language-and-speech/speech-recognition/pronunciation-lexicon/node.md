---
tag: XPYCJR
kind: definition
slug: pronunciation-lexicon
name: Pronunciation lexicon
aliases:
- pronunciation dictionary
area: natural-language-and-speech/speech-recognition
level: intro
summary: A list that gives each word of the vocabulary one or more phoneme sequences, linking word models to phone models.
prereqs: [automatic-speech-recognition]
see_also: [hclg-decoding-graph, grapheme-to-phoneme-conversion, joint-sequence-g2p, triphone-model, finite-state-transducer, trie, forced-alignment, gmm-hmm-acoustic-model]
sources:
  - paper: "The CMU Pronouncing Dictionary, Carnegie Mellon University, distributed at https://github.com/cmusphinx/cmudict"
    locator: the phone set of 39 ARPAbet symbols with stress marks on the vowels, and the entries for words with more than one pronunciation
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the chapter on the architecture of an HMM-based recognizer, where the dictionary maps words to phone sequences
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall PTR, 2001
    locator: Chapter 9 (acoustic modeling), the choice of the units of speech and the pronunciation of words
---

A pronunciation lexicon lists the words that a speech recognizer or synthesizer knows and gives each word one or more pronunciations, each a sequence of phones from a fixed phone set. It is the link between the words of the [language model](/language-model/) and the phone models of the acoustic model: the HMM of a word is the concatenation of the HMMs of its phones. A lexicon can also give each pronunciation a probability. In the weighted transducer view of a recognizer it is the transducer L of the [HCLG decoding graph](/hclg-decoding-graph/).

## Definition

Fix a vocabulary $V$ of words and a phone set $\Phi$. A pronunciation lexicon is a finite relation $\mathcal{L} \subseteq V \times \Phi^+$: each pair $(w, \rho)$ says that the word $w$ can be pronounced as the non-empty phone sequence $\rho = \phi_1 \ldots \phi_k$. Most words have one pronunciation, and some have several. A weighted lexicon adds a pronunciation probability $P(\rho \mid w)$ for each pair, with $\sum_\rho P(\rho \mid w) = 1$ for every word. An unweighted lexicon is the special case in which every pronunciation of a word has the same weight, or weight 1 in the max form of the search.

With the lexicon, the acoustic model of a word sequence $W = w_1 \ldots w_U$ is

$$p(O \mid W) = \sum_{\rho_1, \ldots, \rho_U} \prod_{u=1}^{U} P(\rho_u \mid w_u) \cdot p(O \mid \rho_1 \ldots \rho_U),$$

where $p(O \mid \rho_1 \ldots \rho_U)$ is the density of the frames under the HMM built from the concatenated phone sequence. Decoders replace the sum by a maximum, together with the maximum over state paths.

As a transducer, L reads phone sequences and writes words. Its paths spell the pronunciations $\rho$ on the input side and the word $w$ on the output side, with weight $-\log P(\rho \mid w)$, and it accepts any sequence of words by a loop back to the start. Words with the same pronunciation (homophones), and pronunciations that are prefixes of other pronunciations, make L impossible to determinize. Recognizers add disambiguation symbols at the end of such pronunciations before the composition with the grammar, and remove them after determinization.

## Examples and non-examples

- **CMUdict entries.** The CMU Pronouncing Dictionary uses 39 phones in the ARPAbet notation: 15 vowels, each with a stress mark of 0, 1 or 2, and 24 consonants. Some of its entries are:

| word | pronunciation |
|---|---|
| a | AH0 |
| a(2) | EY1 |
| again | AH0 G EH1 N |
| again(2) | AH0 G EY1 N |
| address | AE1 D R EH2 S |
| address(2) | AH0 D R EH1 S |

The suffix "(2)" marks a second pronunciation of the same word. The two pronunciations of "address" differ in the first vowel and in the stress, as in the noun and the verb.
- **Pronunciation probabilities.** A weighted lexicon could give "a" the weights $P(\text{AH0} \mid a) = 0.9$ and $P(\text{EY1} \mid a) = 0.1$. These numbers are an illustration. In practice the weights come from counts of each pronunciation in a [forced alignment](/forced-alignment/) of the training data that allows all the variants.
- **Recognizer phone sets.** A recognizer often removes the stress marks of CMUdict, so AH0 and AH1 become one phone AH, and adds models for silence and noise. The lexicon then maps a silence word to the silence phone.
- **Not a lexicon: letter rules alone.** [Grapheme-to-phoneme conversion](/grapheme-to-phoneme-conversion/) predicts pronunciations from the spelling, for words that are not in the lexicon. Its output can extend a lexicon, but a G2P model is a function from all strings and not a finite list.
- **Not a lexicon: a list of word models.** A recognizer with one HMM per whole word, for example for the ten digits, needs no lexicon, because no word shares a phone model with another.
- **Not a lexicon: the output units of a character model.** An end-to-end model that outputs characters or subword units has no lexicon of phones, although a lexicon of the allowed words can still restrict its search.

## Related definitions

- **[HCLG decoding graph](/hclg-decoding-graph/).** The composition $H \circ C \circ L \circ G$ of the HMM transducer H, the context dependency C, the lexicon L and the grammar G. The lexicon is the L.
- **[Triphone model](/triphone-model/).** The context of a phone depends on the neighbors in the pronunciation, and across word boundaries on the pronunciation of the next word.
- **[Grapheme-to-phoneme conversion](/grapheme-to-phoneme-conversion/)** and **[joint-sequence G2P](/joint-sequence-g2p/).** Models that produce pronunciations for words outside the lexicon.
- **[Trie](/trie/).** A trie of the pronunciations, the lexical prefix tree, shares the first phones of words in the search space of a decoder.
- **[Forced alignment](/forced-alignment/).** It uses the lexicon to turn a transcript into a chain of phone models, and it can pick among the pronunciations of each word.
- **[Finite-state transducer](/finite-state-transducer/).** The formal object that the lexicon becomes in a weighted transducer decoder.

## References
