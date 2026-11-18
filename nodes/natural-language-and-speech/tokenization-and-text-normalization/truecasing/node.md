---
tag: G4FYFP
kind: problem
slug: truecasing
name: Truecasing
aliases:
- case restoration
- capitalization recovery
area: natural-language-and-speech/tokenization-and-text-normalization
level: advanced
summary: Restore the proper capitalization of text that is all lower case or all upper case, a sequence labeling problem solved for example by a trigram model over case variants with Viterbi decoding.
prereqs: [n-gram-language-model, viterbi-algorithm]
see_also: [unicode-case-folding, sequence-labeling, hidden-markov-model, named-entity-recognition, sentence-boundary-detection, automatic-speech-recognition, machine-translation, out-of-vocabulary-word]
sources:
  - url: https://aclanthology.org/P03-1020/
    title: Lucian Vlad Lita, Abe Ittycheriah, Salim Roukos and Nanda Kambhatla, tRuEcasIng, ACL 2003
    locator: pages 152 to 159; Section 2 (the case classes, the unigram baseline, the trigram truecaser with sentence-level Viterbi decoding, unknown words and mixed case), Section 3 (about 98% agreement on news), Section 4 (named entity recognition and machine translation)
  - url: https://aclanthology.org/P99-1021/
    title: Andrei Mikheev, A knowledge-free method for capitalized word disambiguation, ACL 1999
    locator: pages 159 to 166 (capitalized words in positions where capitalization is expected, such as the first word of a sentence)
  - url: https://aclanthology.org/J06-4003/
    title: Tibor Kiss and Jan Strunk, Unsupervised multilingual sentence boundary detection, Computational Linguistics 32(4), 2006
    locator: pages 485 to 525; Figure 3 (the orthographic heuristic, which decides from case counts whether a word after a period starts a sentence)
---

Truecasing is the problem of giving each word of a text its correct capitalization when the text is all lower case, all upper case, or cased in an unreliable way, so that "he moved to new york" becomes "He moved to New York". It is the inverse of [case folding](/unicode-case-folding/), which removes case on purpose, and it is close to [sentence boundary detection](/sentence-boundary-detection/), because a capital letter after a period can mean a sentence start or a name. The standard formulation is [sequence labeling](/sequence-labeling/): each word gets one of a few case forms, and a model of the context, such as a trigram [language model](/n-gram-language-model/) decoded with the [Viterbi algorithm](/viterbi-algorithm/), chooses the forms for the whole sentence.

## In plain words

Some text has no useful capital letters: speech recognizer output, text messages, headlines in capitals, or old telex text. A reader still knows that "new york" is a place and that "apple" in "apple shares fell" is a company. A program must learn this. The simplest program writes each word in the form it saw most often in correctly cased text. That fails for words such as "new", which is usually lower case but is capitalized in "New York". A better program looks at the words around each word and picks the forms that make the whole sentence most likely.

## Definition

**Input:** a sentence of tokens $w_1, \ldots, w_S$ with no reliable case, and cased training text.

**Output:** a cased form $c_t$ for each token, where $c_t$ lower-cases to $w_t$.

Lita et al. (2003) sort the forms into four classes: all lower case (LC), first letter upper case (UC), all letters upper case (CA), and mixed case (MC), such as "McCartney". For LC, UC and CA the class fixes the form. For MC the system must also choose the exact form, so it keeps a short list of the mixed forms seen in training. Let $M$ be the largest number of candidate forms for one token.

**Quality** is the fraction of tokens whose form agrees with a correctly cased reference text, or [precision and recall](/precision-and-recall/) of the capitalized words. Part of the answer is a convention: titles and headlines capitalize words that the same text writes in lower case inside a sentence.

## Variants

- **Lower-case input.** The output of speech recognition and of some machine translation systems has no case at all.
- **Upper-case input.** Headlines, telex and some old documents are all capitals. The task is the same, but the input loses the case of every letter.
- **Ambiguous positions only.** In normal text, case is unreliable only where capitals are required: the first word of a sentence, after a colon, in quotes and in titles. Mikheev (1999) decides only these positions, and Punkt uses case counts from the rest of the text for the word after a period.
- **Normalization for training.** Machine translation pipelines often use "truecasing" for a lighter task: change only the first word of each sentence to its most frequent form, so that "The" and "the" become one type.
- **Joint restoration.** Restore case together with punctuation and sentence boundaries in speech recognizer output, or together with accents, which Lita et al. note is a similar problem.

## Examples

Take the input "he moved to new york". Suppose the cased training text has "new" 50 times and "New" 10 times, and all 10 times "New" is followed by "York". After "to" it has "new" 6 times and "New" 4 times. The token "york" occurs only as "York".

| method | "he" | "new" | "york" | output |
|---|---|---|---|---|
| most frequent form | he | new (50 to 10) | York | he moved to new York |
| most frequent form, first word capitalized | He | new | York | He moved to new York |
| bigram model over the sentence | He | New | York | He moved to New York |

The unigram method cannot see that "york" follows, which is the failure that Lita et al. describe for "new". The bigram model compares the two paths through "new york". The path "new York" needs the bigram "new York", which has count 0, and the path "New York" has bigram probability $10/10 = 1$ for "York" after "New". The second path wins even though "new" alone is more frequent. This is a toy example, but the effect is the one that the paper reports.

## Known algorithms

- **Most frequent form.** Write each token in the form that was most frequent in training, and capitalize the first word of each sentence. This is the baseline of Lita et al. Its accuracy is at most the fraction of tokens that occur in their most frequent form, about 90% on their news corpus, and about 12% of the vocabulary items occurred in more than one form (measurements).
- **Language model with Viterbi decoding.** Lita et al. (2003) build a trigram model of cased words with interpolated smoothing and find the most likely sequence of forms for the whole sentence with the [Viterbi algorithm](/viterbi-algorithm/). The cased words are the hidden states of a [hidden Markov model](/hidden-markov-model/) and the lower-case words are the observations. Rare training words are replaced by the special tokens UNKNOWN_LC and UNKNOWN_UC, so that a word never seen in training gets the case that its context suggests. They report about 98% agreement with the original news articles (a measurement).
- **Classifiers per token.** Predict the class LC, UC, CA or MC of each token from features of the word and its neighbors, for example with a [conditional random field](/conditional-random-field/) or a neural sequence tagger. This generalizes to unknown words through features such as suffixes.
- **Case counts in the same document.** Mikheev (1999) decides an ambiguous capitalized word from how the same word is cased elsewhere in the document, where its position does not force a capital. The orthographic heuristic of Punkt is a similar rule for the word after a period.

## Bounds

With a hash table for the counts, the most frequent form takes $O(S)$ expected time for a sentence of $S$ tokens, and every method must read all tokens, so $\Omega(S)$ is a lower bound. With an $n$-gram model of order $H$ and at most $M$ forms per token, a Viterbi state is the forms of the last $H - 1$ tokens, so there are at most $M^{H-1}$ states per position and $M$ choices per state, and decoding takes $O(SM^H)$ time. This is within the bound $O(SM^{H+1})$ that Lita et al. state. Because most words have only one form, the number of states is much smaller in practice.

No method can be perfect. The lower-case string is the same for different correct outputs: "apple" can be the fruit or the company, and "us" can be the pronoun or "US". Context decides most of these cases, but some need knowledge of the world.

## Reductions

- **To sequence labeling.** Each token gets one label from its candidate forms, so any sequence labeler applies.
- **To language model decoding.** With a cased language model $P$, the best output is $\arg\max P(c_1 \ldots c_S)$ over all choices of $c_t$ that lower-case to $w_t$. Lower-casing is a deterministic channel, so this is noisy channel decoding with a trivial channel model, as in [noisy channel spelling correction](/noisy-channel-spelling-correction/).
- **To word sense disambiguation.** Lita et al. view the forms of a word as senses with different spellings, so methods that choose a sense from context also choose a case.

## Applications

- **Speech recognition output.** Make the transcript of [automatic speech recognition](/automatic-speech-recognition/) readable, often together with punctuation restoration.
- **Machine translation.** Restore the case of [machine translation](/machine-translation/) output when the system works in lower case. Lita et al. report higher cased BLEU scores with their truecaser than with the unigram baseline.
- **Named entity recognition.** Capital letters are a strong feature for [named entity recognition](/named-entity-recognition/). On lower-case text, Lita et al. measured an overall F-measure improvement of 26.52% when the text was truecased before tagging.
- **Sentence boundary detection.** The case of the word after a period is evidence for a boundary, so truecasing and [sentence boundary detection](/sentence-boundary-detection/) help each other.

## References
