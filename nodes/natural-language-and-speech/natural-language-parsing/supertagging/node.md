---
tag: C05N44
kind: technique
slug: supertagging
name: Supertagging
aliases:
- almost parsing
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: Assign each word a rich lexical category, such as a CCG category or a TAG elementary tree, by sequence tagging before full parsing.
prereqs: [sequence-labeling, combinatory-categorial-grammar, tree-adjoining-grammar]
see_also: [part-of-speech-tagging, maximum-entropy-markov-model, bilstm-crf, forward-backward-algorithm, viterbi-algorithm, a-star-parsing, cyk-algorithm, beam-search]
sources:
  - paper: "Srinivas Bangalore and Aravind K. Joshi, Supertagging: an approach to almost parsing, Computational Linguistics 25(2), 237-265, 1999"
    title: "Srinivas Bangalore and Aravind K. Joshi, Supertagging: an approach to almost parsing"
    locator: "the elementary trees of lexicalized TAG as supertags, the tagging models, and the lightweight dependency analyzer that combines the chosen trees"
  - paper: "Stephen Clark and James R. Curran, Wide-coverage efficient statistical parsing with CCG and log-linear models, Computational Linguistics 33(4), 493-552, 2007"
    title: "Stephen Clark and James R. Curran, Wide-coverage efficient statistical parsing with CCG and log-linear models"
    locator: "Section 8 (the log-linear supertagger, the tag dictionary and the multitagger, Table 4) and Section 9.1 (adaptive supertagging)"
---

Supertagging gives each word of a sentence a rich lexical category before parsing, using a fast [sequence labeling](/sequence-labeling/) model of the kind used for [part-of-speech tagging](/part-of-speech-tagging/). In a lexicalized grammar such as [CCG](/combinatory-categorial-grammar/) or [lexicalized TAG](/tree-adjoining-grammar/), a word's category already fixes most of the structure around it, so choosing the categories does much of the parser's work, and Bangalore and Joshi called it almost parsing. The grammar pages define the categories; this page is about choosing them, and about how a parser uses a short list of likely categories per word instead of every category the lexicon allows.

## In plain words

A part-of-speech tagger says that "likes" is a verb. A supertagger says much more: "likes" is a verb that wants an object on its right and a subject on its left. With such a tag on every word, there is little left for the parser to decide.

Most words could have many tags, and the parser would have to try them all. A supertagger looks at the words around each word and guesses which few tags are likely. The parser then only tries those.

Sometimes the right tag is not on the short list, and then the parser finds no complete analysis. A good system then asks the tagger for a longer list and tries again.

## When it applies

Supertagging helps when the grammar is lexicalized, so that the lexicon holds most of the information and the combining rules are few and general, and when the lexicon gives common words many categories. Both hold for wide-coverage CCG and LTAG grammars extracted from treebanks: in the tag dictionary of Clark and Curran (2007) the word "is" has 45 CCG categories (measurement). It does not help much for a plain [context-free grammar](/context-free-grammar/), whose preterminals carry little structure.

It needs training data with gold categories for each word, usually from a treebank converted to the grammar, such as CCGbank for CCG.

## The template

Let a sentence have $n$ words, and let the category set have $t$ members.

1. **Category set.** Take the categories from the training data, and keep those seen at least a threshold number of times. Rare categories are dropped, so the parser can never use them.
2. **Tag dictionary.** For a word seen often in training, allow only the categories seen with that word. Rare and unknown words are allowed every category, or in some systems every category seen with their part-of-speech tag.
3. **Tagger.** Train a sequence model that gives, for each word $i$ and allowed category $c$, a probability $p_i(c)$. Older systems use a maximum entropy model over a window of words and part-of-speech tags, with the [forward-backward algorithm](/forward-backward-algorithm/) for the marginals. Newer systems use a bidirectional recurrent network or a transformer with a softmax at each word. A first-order sequence model takes $O(n\,t^2)$ time for the marginals; a model that tags each word independently given the encoder output takes $O(n\,t)$ after the encoder (theorem).
4. **Multitagging.** Keep for word $i$ every category $c$ with $p_i(c) \ge \beta \max_{c'} p_i(c')$, for a cutoff $\beta$ between 0 and 1. A small $\beta$ keeps more categories.
5. **Parsing.** Run the parser, for example [CKY](/cyk-algorithm/) for a binary CCG, with only the kept categories as lexical entries.
6. **Adaptive search.** If the parser finds no analysis that spans the sentence, lower $\beta$ and parse again. Clark and Curran start with a restrictive setting and ask for more categories only when needed (heuristic, with measured speedups).

The cutoff $\beta$ trades accuracy for speed. With $\beta = 0.075$, Clark and Curran's multitagger kept 1.27 categories per word on average and the correct category was on the list for 97.34% of the words; with $\beta = 0.001$ and a looser tag dictionary it kept 3.57 categories per word with 99.17% (measurement, section 00 of CCGbank, Table 4).

## Classic examples

- **LTAG supertagging.** Bangalore and Joshi (1999) treated the elementary trees of a lexicalized TAG as tags, trained n-gram tagging models on them, and combined the chosen trees with a simple dependency analyzer instead of a full TAG parser. They introduced the name supertag and the phrase almost parsing.
- **CCG supertagging.** Clark and Curran (2007) used 425 CCG categories, those seen at least 10 times in sections 02 to 21 of CCGbank, a log-linear tagger over a five-word window with the two previous categories as features, and a tag dictionary for words seen at least 20 times. A single best tag was right for 92.6% of the words with gold part-of-speech tags and 91.5% with automatic ones, but for only 36.8% and 32.5% of whole sentences (measurement). Multitagging and adaptive search made their CKY parser both fast and accurate.
- **Supertag-factored A\* parsing.** If the score of a CCG derivation is the sum of the log probabilities of its supertags, then the best supertag of each word gives an admissible estimate of the outside score, and [A\* parsing](/a-star-parsing/) finds the best derivation while expanding few items (theorem for admissibility; the speed is a measurement). Lewis and Steedman used this design with neural supertaggers.

## Variations

- **Single tagging versus multitagging.** One tag per word is fastest, but whole-sentence accuracy is low, so most sentences would contain an error. Multitagging is the usual choice.
- **Parse first, tag more on failure, or the reverse.** A system can start with a loose $\beta$ for accuracy and tighten it when the chart grows too large, or start tight for speed and loosen it on failure.
- **Neural taggers.** A [BiLSTM-CRF](/bilstm-crf/) or a pretrained transformer encoder gives better supertags than window models, because it sees the whole sentence. Better tags make the parser's job easier still (heuristic).
- **Constructive tagging.** Some taggers predict a category as a sequence of atomic categories and slashes instead of choosing from a fixed list, so they can produce categories that were too rare to keep.
- **Other formalisms.** HPSG parsers supertag lexical types, and dependency parsers sometimes tag each word with its head direction and label first. The idea is the same.

## Pitfalls

- **No recovery from a missing category.** If the correct category is not kept, no parse can be correct. Measure the share of words whose gold category is kept, not just the accuracy of the top tag.
- **Unseen categories.** A category dropped by the frequency threshold can never be assigned. Rare constructions are then always wrong.
- **Tag dictionary blind spots.** A frequent word is limited to the categories seen with it in training, so a valid but unseen use cannot be tagged.
- **Gold part-of-speech tags.** Results with gold part-of-speech tags are higher than in real use, where the tags are predicted.
- **Mismatch with the parser.** The parser's model and the tagger's probabilities are trained separately. A parser that uses only the tagger's list cannot fix the tagger's ranking, and a tight $\beta$ makes the parser's statistics matter less.

## Exercises

1. With $\beta = 1$, the multitagger keeps only the best category of each word, except for ties. Show that lowering $\beta$ never removes a category from a word's list.
2. A tagger gives each word 3 categories, and the parser is CKY over a binary CCG. If each chart cell held at most the categories built from those lists, explain why the work grows with the number of categories per word, and why the number of categories per word is the right measure of the tagger's cost to the parser.
3. A single-tag supertagger has 92% per-word accuracy and errors that are independent across words. Estimate the share of 25-word sentences with no error, and compare it with the 36.8% sentence accuracy that Clark and Curran measured. What does the comparison suggest about how errors are distributed?
4. Show that if the score of a derivation is the sum of the log probabilities of its supertags, the sum over the words outside a span of each word's best supertag score is an upper bound on the outside score of any item over that span.

## References
