---
tag: RNE0JT
kind: problem
slug: lemmatization
name: Lemmatization
aliases:
- lemmatisation
area: natural-language-and-speech/tokenization-and-text-normalization
level: intro
summary: Map each inflected word form in context to its dictionary form, such as was to be, using morphology and the part of speech.
prereqs: [text-tokenization, part-of-speech-tagging]
see_also: [stemming, porter-stemmer, morphological-analysis, two-level-morphology, finite-state-transducer, sequence-labeling, inverted-index, out-of-vocabulary-word]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 2, Section 2.2.4 (stemming and lemmatization, the lemma as the dictionary form, and the example saw)
  - url: https://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
    title: NLTK, the WordNet corpus reader
    locator: the table MORPHOLOGICAL_SUBSTITUTIONS and the method _morphy (exception lists, suffix rules per part of speech, and the check against the WordNet lemmas)
---

Lemmatization is the problem of mapping each word form of a text to its lemma, the form that a dictionary lists: "was" and "is" to "be", "mice" to "mouse", "better" as an adjective to "good". Its close pair is [stemming](/stemming/): a stemmer cuts suffixes by rules and may give a string that is not a word, while a lemmatizer uses a vocabulary and [morphological analysis](/morphological-analysis/) and returns a real dictionary form. The answer can depend on the context, because the same form can belong to different lemmas: "saw" is the noun "saw" or a form of the verb "see". So lemmatization usually runs after [part-of-speech tagging](/part-of-speech-tagging/).

## In plain words

A dictionary lists "mouse", not "mice", and "see", not "saw". Many tasks want to treat all forms of one word as the same word: a search for "mouse" should also find "mice". A lemmatizer finds the dictionary form of each word. It needs a list of irregular forms, rules for regular endings, and a list of real words to check its result. It also needs to know how the word is used. In "I saw a saw", the first "saw" comes from "see" and the second "saw" is the tool.

## Definition

**Input:** a sentence of tokens $w_1, \ldots, w_n$, often with a part-of-speech tag $p_t$ for each token, and a lexicon of lemmas.

**Output:** a lemma $\lambda_t$ for each token, such that $w_t$ is a form of $\lambda_t$ with the tag $p_t$.

Without context the problem is a relation, not a function: a form can have several (lemma, tag) analyses, and [morphological analysis](/morphological-analysis/) returns all of them. Lemmatization in context selects one. The conventions differ between lexicons and treebanks, for example on whether a participle such as "interesting" used as an adjective has the lemma "interesting" or "interest". So quality is the accuracy against one annotated corpus.

Manning, Raghavan and Schuetze (2008) state the usual difference to stemming: a lemmatizer normally removes only inflectional endings, while a stemmer often also removes derivational affixes, so "organization" is a lemma of its own but can get the same stem as "organize".

## Variants

- **Lemmatization without context.** Given only the form and possibly a tag, return all candidate lemmas, or the most frequent one. Many search systems do this.
- **Lemmatization in context.** Use the sentence to choose among the candidates, usually through the part-of-speech tag.
- **Rich morphology.** In Finnish, Turkish, Czech or Arabic a lemma has hundreds of forms, and the lexicon cannot list them all. Rules or a [finite-state transducer](/finite-state-transducer/) must analyze forms that are not listed.
- **Lemmatization as string transduction.** Learn a model that edits a form into its lemma, for example as a sequence of edit operations chosen by a classifier. This also covers words that are not in the lexicon.
- **Joint tagging and lemmatization.** Predict the tag and the lemma together, because each helps with the other.

## Examples

The WordNet lemmatizer in NLTK follows three steps for a form and a part of speech: look the form up in an exception list of irregular forms; else apply every suffix rule of the part of speech once; then keep the form itself and those results that WordNet lists as lemmas with that part of speech. The noun rules are s to nothing, ses to s, ves to f, xes to x, zes to z, ches to ch, shes to sh, men to man and ies to y. The verb rules are s to nothing, ies to y, es to e, es to nothing, ed to e, ed to nothing, ing to e and ing to nothing.

| form | tag | step that applies | lemma |
|---|---|---|---|
| saw | verb | exception list gives see, and saw is also a verb lemma (to cut) | see or saw |
| saw | noun | the form itself is a noun lemma | saw |
| mice | noun | exception list | mouse |
| flies | noun | ies to y gives fly | fly |
| meeting | noun | the form itself is a noun lemma | meeting |
| meeting | verb | ing to nothing gives meet | meet |
| leaves | noun | s to nothing gives leave, ves to f gives leaf | leave or leaf |

The first and the last rows show that a tag is not always enough: "I saw it" and "they saw wood" both use a verb "saw", and both "leave" (as in "on leave") and "leaf" are nouns. Only the sentence can choose. A stemmer gives one string for each form and ignores the tag, so it cannot separate the two uses of "saw" or of "meeting".

## Known algorithms

- **Lookup tables.** A full list of (form, tag, lemma) entries, as built from a dictionary or a tagged corpus. Lookup with a [hash table](/hash-table/) is fast, but forms that are not in the list get no lemma.
- **Exception lists with suffix rules.** As in the WordNet lemmatizer above: irregular forms by lookup, regular forms by a few rules, and a check against the lexicon.
- **Finite-state morphology.** A [finite-state transducer](/finite-state-transducer/), for example a [two-level](/two-level-morphology/) rule system, maps a surface form to its lemma and tags. One transducer covers the whole lexicon and the rules of spelling change, and it also analyzes forms that were never seen as long as their stem is in the lexicon.
- **Statistical and neural lemmatizers.** Learn to choose edit scripts, or translate the characters of a form into the characters of the lemma, from an annotated corpus, usually with the sentence as context.

## Bounds

With a lookup table or a transducer of fixed size, each token takes time linear in its length, so a text of $n$ characters takes $O(n)$ time, which is optimal because every character must be read. The suffix rule method applies a fixed number of rules per form and checks each result in a hash table, which is also $O(n)$ expected time. No bound on accuracy holds for all data: when two lemmas share a form and a tag, as with "leaves", only the context or knowledge of the world decides.

## Reductions

- **To morphological analysis plus disambiguation.** Produce all analyses of each form with [morphological analysis](/morphological-analysis/), then choose one per token with a tagger, which is [sequence labeling](/sequence-labeling/).
- **From stemming.** Stemming is the cruder problem: map forms to a shared key with no need for the key to be a word. Any lemmatizer gives a stemmer, but the converse does not hold.
- **To string transduction.** With a learned model, lemmatization is a character-level transduction from form to lemma, the same kind of problem as transliteration.

## Applications

- **Search.** Index lemmas in an [inverted index](/inverted-index/) so that a query matches all forms of a word. This matters more for languages with rich morphology than for English.
- **Vocabulary reduction.** Mapping forms to lemmas reduces the number of types and the share of [out-of-vocabulary words](/out-of-vocabulary-word/) for count-based models.
- **Lexicography and corpus linguistics.** Count words by lemma in concordances and frequency lists.
- **Parsing and information extraction.** Dependency treebanks such as those of Universal Dependencies annotate a lemma for each token, and features over lemmas generalize better than features over forms.

## References
