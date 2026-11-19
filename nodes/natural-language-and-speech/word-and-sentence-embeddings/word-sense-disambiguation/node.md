---
tag: QH9THN
kind: problem
slug: word-sense-disambiguation
name: Word sense disambiguation
aliases:
- WSD
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Choose the intended sense of an ambiguous word in context from a fixed inventory of senses, such as the WordNet synsets of the word.
see_also: [lesk-algorithm, yarowsky-algorithm, resnik-similarity, naive-bayes-classifier, personalized-pagerank, entity-linking, machine-translation, distributional-hypothesis]
sources:
  - paper: doi:10.1145/1459352.1459355
    title: Roberto Navigli, Word sense disambiguation, a survey, ACM Computing Surveys 41(2), 2009, article 10
    locator: the definition of the task, the lexical sample and all-words settings, the sense inventories, the evaluation measures and baselines, and the survey of supervised, unsupervised and knowledge-based methods
  - paper: "Adam Kilgarriff and Joseph Rosenzweig, Framework and results for English SENSEVAL, Computers and the Humanities 34(1-2), 2000"
    title: Kilgarriff and Rosenzweig 2000
    locator: the design of the first SENSEVAL evaluation, its scoring, and its baselines
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: Appendix Word Senses and WordNet, the sections on word sense disambiguation, its evaluation and the most frequent sense baseline
---

Word sense disambiguation (WSD) asks which sense an ambiguous word has at one place in a text, with the senses taken from a fixed inventory such as the synsets of WordNet or the entries of a dictionary. "Bank" in "they sat on the bank of the river" is the sloping land, and in "I went to the bank to deposit my money" it is the financial institution. Each occurrence is a classification with a small set of labels that depends on the word. The problem has no single right algorithm, since the answer is the sense a human reader means. Methods are compared by their accuracy against texts that people have labeled with senses. A strong baseline that needs no context at all is the most frequent sense of the word, and many methods do not beat it by much.

## In plain words

Many words have more than one meaning. A dictionary lists them as senses: "plant" can be a living thing or a factory. When the word appears in a sentence, a reader knows at once which sense is meant. A program does not.

The task is to pick, for each use of a word, one sense from the dictionary's list. The clues are the other words around it, the topic of the document, and how common each sense is. Some methods learn from examples that people have labeled. Some use only the dictionary. Some start from a few sure clues and learn more. A simple trick works surprisingly well: always pick the sense that is used most often. Any real method has to do better than that.

## Definition

**Input.** A sense inventory that gives each word $w$ a finite set $S(w)$ of senses, a text $t_1, \ldots, t_n$, and a set of target positions $i$ with $|S(t_i)| \ge 1$. Supervised settings also give a training text with a sense on each target.

**Output.** For each target position $i$, a sense $\hat{s}_i \in S(t_i)$, or no answer.

**Measure.** The text has gold senses $s_i$ from human annotators. If a system answers $a$ of the $T$ targets and $k$ of the answers are right, its precision is $k / a$, its recall is $k / T$, and with an answer for every target both are the accuracy $k / T$ (see [precision and recall](/precision-and-recall/)). When annotators may give several senses, an answer counts as right if it is one of them.

**What "right" means.** The gold sense is the one the annotators chose. Fine-grained inventories such as WordNet split senses so finely that annotators often disagree, and the agreement between annotators is a practical upper bound on the accuracy that can be measured. This bound and every reported accuracy are measurements on one data set, not properties of the problem.

## Variants

- **Lexical sample.** A few chosen words, each with many labeled occurrences. This allows one classifier per word.
- **All words.** Every content word of a running text is a target. Most words have few or no training examples, so the methods must back off to the inventory.
- **Coarse senses.** Groups of fine senses as labels, which raises both the agreement of annotators and the accuracy of systems.
- **Word sense induction.** No inventory. The occurrences of a word are clustered, and each cluster is a sense, which follows the [distributional hypothesis](/distributional-hypothesis/).
- **Translations as senses.** The senses of a word are its translations into another language, which a parallel corpus labels for free.
- **Entity linking.** The senses are the entries of a knowledge base and the words are names, as in [entity linking](/entity-linking/).

## Examples

**Bank.** With the three senses financial institution, sloping land beside water, and a row of similar objects, the context "the fishermen pulled their boats onto the bank when the river rose" has the second sense, and "a bank of switches" the third. The [Lesk algorithm](/lesk-algorithm/) page works through these contexts with a written inventory.

**Plant.** The living sense and the factory sense of "plant", with the seeds "plant life" and "manufacturing plant", is the example of the [Yarowsky algorithm](/yarowsky-algorithm/).

**The most frequent sense.** Suppose that in labeled text "bank" has the financial sense 70 times out of 100, the land sense 25 times and the row sense 5 times. A system that always answers the financial sense has accuracy 0.70 on text with the same distribution, and needs no context. A system that uses context must beat 0.70 to be worth its cost on this word.

**A hard case.** In "the bank was closed" nothing in the sentence decides between the senses. A wider context, or the sense of other occurrences of "bank" in the same document, may decide it.

## Known algorithms

- **Most frequent sense.** Answer the first sense of a frequency-ordered inventory. $O(1)$ per target. It needs labeled text to order the senses.
- **Dictionary overlap.** The [Lesk algorithm](/lesk-algorithm/) picks the sense whose gloss shares the most words with the context, in $O(n + r g)$ expected time for $n$ context words and $r$ senses of $g$ words.
- **Supervised classifiers.** One classifier per word over features of the context, such as [naive Bayes](/naive-bayes-classifier/), decision lists or a [support vector machine](/support-vector-machine/), trained on labeled occurrences.
- **Bootstrapping.** The [Yarowsky algorithm](/yarowsky-algorithm/) grows a decision list from a few seed collocations, with one sense per discourse.
- **Graph methods.** Run [personalized PageRank](/personalized-pagerank/) over the graph of the inventory, with the senses of the context words as the start, and choose the sense of each target with the highest score.
- **Similarity in a taxonomy.** Choose the senses that are most similar to the senses of the nearby words, with a measure such as [Resnik similarity](/resnik-similarity/).
- **Contextual embeddings.** Embed each labeled occurrence with a model such as [BERT](/bert/), average the vectors of each sense, and give a new occurrence the sense of the nearest average.

## Bounds

For one target, any method that reads the context and scores each sense once costs at least the size of the input, $\Omega(n + r)$, and the methods above reach $O(n + r g)$ or the cost of one pass of the classifier. The joint form, which chooses the senses of all $m$ targets of a text together to maximize a sum of scores for pairs of senses, has $\prod_i |S(t_i)|$ candidate assignments. With arbitrary pair scores it is NP-hard, by the reduction below from maximum cut. If only adjacent targets have pair scores, it is a chain, and a [Viterbi](/viterbi-algorithm/) style program solves it in $O(m r^2)$ for at most $r$ senses per target.

The accuracy has no bound that holds in general. The agreement between annotators bounds what a test set can show, and the most frequent sense is the usual lower reference point. Both are measurements.

## Reductions

- **To classification.** The lexical sample task is one multi-class classification problem per word, with the senses of the word as the classes.
- **To sequence labeling.** The all-words task is a [sequence labeling](/sequence-labeling/) problem in which the label set changes with the word at each position.
- **Joint choice and MAP inference.** Choosing all senses at once to maximize the sum of per-target scores and pair scores is [MAP inference](/map-inference/) in a pairwise [Markov random field](/markov-random-field/), with one node per target.
- **From maximum cut.** Given a graph, make each vertex a target with two senses and give each edge the pair score 1 when the two senses differ and 0 otherwise. The best joint choice has the value of a [maximum cut](/maximum-cut/), so the joint choice with arbitrary pair scores is NP-hard.

## Applications

- **Machine translation.** The sense decides the translation: "bank" as land and "bank" as an institution have different words in most languages, which is why [machine translation](/machine-translation/) systems learn to disambiguate, often without an explicit sense inventory.
- **Information retrieval.** A query for "bank" as an institution should not return pages about rivers. Gains from explicit WSD in retrieval have been small in experiments, which is a measurement.
- **Lexicography.** Labeled occurrences show how the senses of a word are used and how frequent each is.
- **Building lexical resources.** Linking the words of a text or of a definition to senses is a step in building and connecting taxonomies such as WordNet.

## References
