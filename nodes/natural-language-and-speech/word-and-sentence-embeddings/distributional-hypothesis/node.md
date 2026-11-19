---
tag: J8XQ48
kind: concept
slug: distributional-hypothesis
name: Distributional hypothesis
aliases:
- distributional semantics
area: natural-language-and-speech/word-and-sentence-embeddings
level: intro
summary: Words that occur in similar contexts tend to have similar meanings, so the contexts of a word can stand for its meaning.
see_also: [word-context-matrix, positive-pointwise-mutual-information, cosine-similarity, brown-clustering, latent-semantic-analysis, skip-gram-model, glove, word-embedding]
sources:
  - paper: "Zellig S. Harris, Distributional structure, Word 10(2-3), 1954, pages 146 to 162"
    title: Harris 1954
    locator: the argument that difference of meaning correlates with difference of distribution
  - paper: "J. R. Firth, A synopsis of linguistic theory, 1930-1955, in Studies in Linguistic Analysis, Philological Society, Blackwell, Oxford, 1957"
    title: Firth 1957
    locator: the sentence "You shall know a word by the company it keeps"
  - paper: "Peter D. Turney and Patrick Pantel, From frequency to meaning, vector space models of semantics, Journal of Artificial Intelligence Research 37, 2010, pages 141 to 188"
    title: Turney and Pantel 2010
    locator: the statement of the distributional hypothesis and the survey of word-context, term-document and pair-pattern matrices
---

The distributional hypothesis says that words that occur in similar contexts tend to have similar meanings. It turns a question about meaning into a question about counts: list the contexts of each word in a large corpus, and compare the lists. Harris 1954 argued that differences of meaning go with differences of distribution, and Firth 1957 put it as "You shall know a word by the company it keeps". The hypothesis is a heuristic about language, not a theorem, and how well it holds is measured by comparing the similarities it gives with human judgments. Every count-based method on this site, from the [word-context matrix](/word-context-matrix/) to [Brown clustering](/brown-clustering/), and the learned [word embeddings](/word-embedding/) as well, rest on it.

## In plain words

If you do not know the word "tesgüino", but you read that people drink it, that it is made from corn and that too much of it makes you drunk, you can guess that it is some kind of alcoholic drink. You guessed from the words around it.

The hypothesis says that this works in general. Words that appear in the same kinds of places, next to the same kinds of words, tend to mean similar things. "Cat" and "dog" both come after "the" and before "eats" or "sleeps". "Coffee" and "tea" both come after "a cup of". So a computer can collect, for every word, the words that appear near it, and call two words similar when their collections are similar. It needs no dictionary and no meaning, only a lot of text.

## The idea

**Context.** The hypothesis needs a choice of what a context is. The usual choices are the words within a window of $k$ tokens on each side, the words linked to the target by a syntactic dependency, or the document the word occurs in. The counts of these contexts for each word form the rows of a [word-context matrix](/word-context-matrix/).

**Similar distribution.** Two words have a similar distribution when their rows are close, usually by [cosine similarity](/cosine-similarity/) after a reweighting such as [PPMI](/positive-pointwise-mutual-information/). The reweighting matters: raw counts are dominated by frequent contexts such as "the", which occur with almost every noun and say little about any of them.

**What kind of similarity.** The hypothesis gives one number per pair, and that number mixes several relations. Synonyms are close, but so are words of the same category ("milk" and "water"), antonyms ("hot" and "cold" occur in the same frames) and words of the same topic. The context decides which relation dominates. Small windows and syntactic contexts tend to group words that can replace each other, and documents or large windows tend to group words of the same topic. This is an observation from many experiments, a measurement, and not a rule.

**Strong and weak forms.** The weak form is the one above: similar contexts are evidence of similar meaning. A strong form says that the distribution of a word is its meaning, or determines it. The methods on this site need only the weak form.

**Limits.** The hypothesis says nothing about a word seen a few times, since its context counts are noise. It merges the senses of an ambiguous word into one row, so "bank" is partly close to "river" and partly to "money", which is why [word sense disambiguation](/word-sense-disambiguation/) is a separate problem. It also cannot tell true statements from frequent ones: if a corpus often puts two words together, they become similar whatever they mean.

## Examples

**A tiny corpus.** Take the five sentences "the cat drinks milk", "the dog drinks water", "a cat eats fish", "a dog eats meat" and "the child drinks milk", and use the words just before and just after each word as its contexts, within the sentence. Then "cat" and "dog" have the same contexts, {the, a, drinks, eats}, once each, and the cosine of their count rows is 1. The row of "child" is {the, drinks}, which gives a cosine of $2 / (\sqrt{4} \sqrt{2}) = 0.7071$ with "cat". "Milk" and "water" both occur only after "drinks", so their cosine is also 1, and "milk" and "fish" share no context, so their cosine is 0. The method puts the two animals together and the two drinks together, from 20 tokens.

**The effect of the weighting.** In the same corpus, with PMI in bits, "the" with "child" gets 2.32, more than "the" with "cat" (1.32), since "child" occurs once, and after "the". After PPMI the cosine of "cat" and "child" falls from 0.7071 to 0.5207, and the cosine of "cat" and "milk", which share only the context "drinks", falls from 0.5 to 0.1282.

**A word test.** Rubenstein and Goodenough 1965 asked people to rate the similarity of pairs of nouns and found that the ratings correlate with the overlap of the contexts of the nouns. Data sets of human ratings of word pairs remain the standard test of methods built on the hypothesis, and the agreement they report is a measurement.

**A counter-example.** "Good" and "bad" occur in almost the same contexts ("a ___ idea", "very ___"), so a distributional method finds them very similar, while their meanings are opposite. The hypothesis gives relatedness, not sameness of meaning.

## Where it is used

- **Count-based word vectors.** The [word-context matrix](/word-context-matrix/), weighted by [pointwise mutual information](/pointwise-mutual-information/) or [PPMI](/positive-pointwise-mutual-information/), gives one sparse vector per word. [Latent semantic analysis](/latent-semantic-analysis/) reduces a term-document matrix with the [singular value decomposition](/singular-value-decomposition/).
- **Word classes.** [Brown clustering](/brown-clustering/) groups words whose classes predict the next word in the same way.
- **Learned embeddings.** The [skip-gram model](/skip-gram-model/) and [GloVe](/glove/) learn dense vectors from the same counts, and under some assumptions skip-gram with negative sampling factorizes a shifted PMI matrix.
- **Word senses and relations.** Context vectors of single occurrences can be clustered into senses, and the [Yarowsky algorithm](/yarowsky-algorithm/) labels senses by their nearby words. Patterns such as [Hearst patterns](/hearst-patterns/) use specific contexts to find specific relations.
- **Information retrieval.** The term-document matrix of the [vector space model](/vector-space-model/) is the same idea applied to documents: documents with similar words are about similar things.

## References
