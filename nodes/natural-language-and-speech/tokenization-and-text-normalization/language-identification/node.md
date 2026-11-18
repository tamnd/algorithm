---
tag: 8PNF27
kind: problem
slug: language-identification
name: Language identification
aliases:
- language detection
- LangID
area: natural-language-and-speech/tokenization-and-text-normalization
level: intro
summary: Decide the natural language in which a text or a short string is written, from a fixed set of candidate languages.
prereqs: [multiclass-classification]
see_also: [naive-bayes-classifier, n-gram-language-model, cross-entropy-loss, cosine-similarity, kmer, aho-corasick, k-nearest-neighbors, logistic-regression]
sources:
  - paper: doi:10.1613/jair.1.11675
    title: Tommi Jauhiainen, Marco Lui, Marcos Zampieri, Timothy Baldwin and Krister Linden, Automatic language identification in texts, a survey, Journal of Artificial Intelligence Research 65, 2019
    locator: pages 675 to 782 (the problem, its variants, features, methods and evaluation)
  - paper: "William B. Cavnar and John M. Trenkle, N-gram-based text categorization, Proceedings of SDAIR-94, the Third Annual Symposium on Document Analysis and Information Retrieval, 1994, pages 161 to 175"
    locator: Section 4 and Table 2 (language classification of 3478 newsgroup articles in eight languages)
  - url: https://aclanthology.org/P12-3005/
    title: Marco Lui and Timothy Baldwin, langid.py, an off-the-shelf language identification tool, ACL 2012 System Demonstrations
    locator: pages 25 to 30; Section 2 (multinomial naive Bayes over byte n-grams with n from 1 to 4, and feature selection by the difference of information gain over languages and over domains)
  - url: https://aclanthology.org/N10-1027/
    title: Timothy Baldwin and Marco Lui, Language identification, the long and the short of the matter, NAACL HLT 2010
    locator: pages 229 to 237 (the effect of document length and of the number of languages on accuracy)
---

Language identification is the problem of deciding which natural language a text is written in, from a fixed set of candidate languages. It is a [multiclass classification](/multiclass-classification/) problem over strings, and the usual features are character or byte $n$-grams, because they need no tokenizer and already show the spelling habits of a language. The [Cavnar-Trenkle method](/cavnar-trenkle-language-identification/) is the classic simple algorithm: it compares ranked lists of frequent $n$-grams. Modern tools use a [naive Bayes classifier](/naive-bayes-classifier/) or a neural network over the same kind of features. A pipeline usually runs language identification first, because the choice of tokenizer, stemmer or model depends on the language.

## In plain words

Every language has its own common letter groups. English text is full of "th", "the" and "ing", French of "le", "es" and "ent", German of "der", "ch" and "sch". A program counts the letter groups in some text of each language. Then, for a new text, it counts the same groups and picks the language whose counts look most alike. Long texts are easy. Short texts, such as a search query or a short message, and closely related languages, such as Danish and Norwegian, are hard.

## Definition

**Input:** a string $x$ of length $n$, a set of $k$ candidate languages $\{\ell_1, \ldots, \ell_k\}$, and training text in each language.

**Output:** one language $\hat\ell$ of the set. A probabilistic method returns $\hat\ell = \arg\max_\ell P(\ell \mid x)$, and it may also return the scores of all languages.

Quality is measured as accuracy, or as precision and recall per language, on test texts of a stated length. The length matters a great deal: accuracy on texts of a few words is much lower than on texts of a few hundred characters, as Baldwin and Lui (2010) and the Cavnar-Trenkle results show. These are measurements.

## Variants

- **Short texts.** Queries, tweets and titles give only a few $n$-grams.
- **Closely related languages and dialects.** Bosnian, Croatian and Serbian, or varieties of Spanish or Arabic, differ in a few words and spellings.
- **Open set.** The text may be in none of the known languages, and the system must say "unknown".
- **Multilingual documents.** One document can hold several languages; the task is to find all of them and their proportions, or to label each segment.
- **Code switching.** Speakers change language inside a sentence, so the label is per word, a [sequence labeling](/sequence-labeling/) task.
- **Script and encoding detection.** When the scripts differ, as for Greek and Russian, the Unicode script of the characters decides. Detecting the character encoding of raw bytes is a related problem.
- **Spoken language identification.** The input is audio, and the features are acoustic and phonetic.

## Examples

Train on about 150 characters each of simple English, French and German sentences, and use profiles of the $L$ most frequent character $n$-grams with $n$ from 1 to 5 and the out-of-place distance of Cavnar and Trenkle. These are the samples of the tests on the Cavnar-Trenkle page.

| text | $L$ | distance en | distance fr | distance de | chosen |
|---|---|---|---|---|---|
| the house | 6 | 15 | 30 | 30 | en |
| the end of the day | 8 | 46 | 40 | 52 | fr (wrong) |
| the end of the day | 11 to 20 | | | | en |

With very short profiles, the few top $n$-grams of English and French overlap, and a short text matches the wrong one. Longer profiles keep more of the evidence and fix the error. This is a measurement on toy data, but it shows the same effect that Cavnar and Trenkle report: on their newsgroup articles, profiles of 300 $n$-grams gave higher accuracy than profiles of 100.

## Known algorithms

- **[Cavnar-Trenkle](/cavnar-trenkle-language-identification/).** Rank the 300 most frequent character $n$-grams ($n$ = 1 to 5) of each language and of the text, and choose the language with the smallest out-of-place distance between the ranks. Cavnar and Trenkle (1994) report 99.8% accuracy for articles over 300 bytes with 300 $n$-grams, a measurement.
- **Naive Bayes over $n$-grams.** Score $\ln P(\ell) + \sum_g c_g(x) \ln P(g \mid \ell)$ over the $n$-gram counts $c_g(x)$ of the text. langid.py (Lui and Baldwin 2012) uses a multinomial naive Bayes model over byte $n$-grams with $n$ from 1 to 4, chooses the features by the difference between their information gain for languages and for domains, and counts them with the [Aho-Corasick](/aho-corasick/) automaton.
- **Per-language language models.** Train a character [n-gram language model](/n-gram-language-model/) per language and choose the one with the lowest [cross-entropy](/cross-entropy-loss/) on the text.
- **Vector space methods.** Represent texts as $n$-gram frequency vectors and choose the language of the nearest centroid or the [nearest neighbors](/k-nearest-neighbors/) under [cosine similarity](/cosine-similarity/).
- **Discriminative and neural classifiers.** [Logistic regression](/logistic-regression/), linear models over hashed $n$-grams, and neural networks, which are the standard for many languages and for short texts.
- **Stop word lists.** Count frequent function words of each language. This works for long texts but fails on short ones.

## Bounds

Extracting the $n$-grams of order at most $m$ from a text of $n$ characters takes $O(nm)$ time, which is $O(n)$ for a fixed maximum order, and every method must read the text, so this is optimal. Scoring $k$ languages costs $O(k)$ times the size of the text profile, or less with sparse features. There is no accuracy bound independent of the data: a short string that is a valid text in two languages cannot be assigned to one of them by any method, and closely related languages are a known hard case (Jauhiainen et al. 2019).

## Reductions

- **To text classification.** Language identification is text categorization with languages as the classes, which is how Cavnar and Trenkle present it; the same algorithm also sorts articles by subject.
- **To language model scoring.** With a uniform prior over languages, the Bayes decision $\arg\max_\ell P(x \mid \ell)$ is the language whose model gives the text the lowest cross-entropy.
- **Rank distances.** The out-of-place measure of Cavnar and Trenkle is a sum of rank differences, which Jauhiainen et al. (2019) note is equivalent to Spearman's measure of disarray, a relative of [Spearman rank correlation](/spearman-rank-correlation/).

## Applications

- **Pipelines.** Choose the tokenizer, the [stemmer](/stemming/), the [lemmatizer](/lemmatization/) or the translation model by language.
- **Corpus building.** Filter web crawls into corpora for one language, the first step of training many language models.
- **Search and indexing.** Index each document with the rules of its language, and restrict results by language.
- **Machine translation and speech.** Detect the source language before [machine translation](/machine-translation/), or choose the recognizer in [speech recognition](/automatic-speech-recognition/).

## References
