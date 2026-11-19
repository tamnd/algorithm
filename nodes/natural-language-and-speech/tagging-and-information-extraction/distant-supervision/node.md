---
tag: 3VCDM2
kind: technique
slug: distant-supervision
name: Distant supervision
aliases:
- distantly supervised relation extraction
area: natural-language-and-speech/tagging-and-information-extraction
level: advanced
summary: "Label training sentences for relation extraction by matching entity pairs to facts in a knowledge base, accepting noisy labels."
prereqs: [relation-extraction, entity-linking, logistic-regression]
see_also: [dipre, named-entity-recognition, hearst-patterns, yarowsky-algorithm, expectation-maximization, multiclass-classification, scaled-dot-product-attention, softmax-regression]
sources:
  - paper: "Mark Craven and Johan Kumlien, Constructing biological knowledge bases by extracting information from text sources, Proceedings of ISMB 1999"
    title: Craven and Kumlien 1999
    locator: weakly labeled training sentences built by matching known facts from a database to abstracts
  - paper: "Mike Mintz, Steven Bills, Rion Snow and Dan Jurafsky, Distant supervision for relation extraction without labeled data, Proceedings of ACL-IJCNLP 2009"
    title: Mintz et al. 2009
    locator: the distant supervision assumption, the Freebase relations matched to Wikipedia sentences, the features pooled over all sentences of a pair, the random negative pairs, and the held-out and human evaluations
  - paper: "Sebastian Riedel, Limin Yao and Andrew McCallum, Modeling relations and their mentions without labeled text, Proceedings of ECML PKDD 2010"
    title: Riedel, Yao and McCallum 2010
    locator: the at-least-one assumption and the model with a hidden variable per sentence
---

Distant supervision trains a relation classifier without hand-labeled sentences. It takes a knowledge base of facts, such as born_in(Marie Curie, Warsaw), finds the sentences of a large corpus that mention both entities of a fact, and labels them with the relation of the fact. Mintz et al. (2009) gave the name and the standard setup, with Freebase facts and Wikipedia text. The labels are noisy: a sentence can mention Curie and Warsaw without saying that she was born there. Much of the later work is about learning well from such labels, chiefly by treating the sentences of one entity pair as a bag, of which at least one sentence expresses the fact.

## In plain words

You want a program that reads "X was born in Y" and similar sentences and outputs the fact. Labeling thousands of sentences by hand is slow. But you already have a database that lists many people and their birthplaces. So search a large text for sentences that name both a person and their birthplace, and assume each such sentence states the birthplace. Use these sentences as training examples. Many will be wrong: "Curie left Warsaw in 1891" names both but says something else. The trick is that you have so many examples that the right patterns still win, and you can train in a way that expects only some sentences of each pair to be right.

## When it applies

It applies when:

- **a knowledge base covers the relations.** Each relation of interest has many known entity pairs, and the knowledge base names the entities so that they can be matched in text.
- **a large unlabeled corpus mentions the pairs.** The facts appear in text, often more than once per pair, written in varied ways.
- **an entity tagger and linker exist.** The sentences must be matched to the knowledge base entities: [named entity recognition](/named-entity-recognition/) finds the mentions and [entity linking](/entity-linking/) or string matching maps them to entries.
- **some noise is acceptable.** The goal is a classifier or a set of new facts with good precision at the top of a ranking, not perfect labels.

It does not apply to relations that the knowledge base lacks, and it works poorly for relations whose pairs often co-occur for other reasons, such as a person and the country they live in.

## The template

```pseudo id=main
DISTANT-SUPERVISION(knowledge base KB, corpus, relations R)
L1  tag and link the entity mentions of every sentence of the corpus
L2  for each pair (a, b) of linked entities that co-occur in a sentence do
L3      bag(a, b) ← all sentences that mention both a and b
L4      label(a, b) ← the relations r with r(a, b) in KB, or none if the pair has no fact
L5  keep the bags with a relation label, and a sample of the bags labeled none
L6  train a classifier on the bags                 ▷ per sentence, pooled, or at least one per bag
L7  apply the classifier to new pairs and sentences; rank the predicted facts by score
```

The distant supervision assumption of Mintz et al. (2009) is that a sentence that mentions both entities of a fact may express the fact. Their classifier pools the features of all the sentences of a pair into one example, so one example is one pair, not one sentence. The negatives are pairs of entities that appear in no relation of the knowledge base, sampled at random. The at-least-one assumption of Riedel, Yao and McCallum (2010) is weaker: if $r(a, b)$ holds, at least one sentence of the bag expresses it. Then training is multi-instance learning: a hidden variable per sentence says whether it expresses the relation, and the bag label constrains these variables.

With a classifier that gives a sentence score $s_i(r)$ for each sentence $i$ of a bag, three common ways to get a bag score are: the mean of the sentence scores; the maximum (the at-least-one form, used by training on the best sentence of the bag only); and a weighted mean with weights from a softmax over the sentences, called selective attention.

## Classic examples

- **Biology.** Craven and Kumlien (1999) matched facts about proteins and their cell locations from a database to sentences of biomedical abstracts, and called the result weakly labeled data.
- **Freebase and Wikipedia.** Mintz et al. (2009) matched Freebase relations such as place of birth, film director and company founders to sentences of Wikipedia articles, and trained a multiclass [logistic regression](/logistic-regression/) classifier on lexical and dependency features pooled over each pair's sentences. They evaluated on held-out Freebase facts and by human judgment of the top predictions.
- **Freebase and the New York Times.** Riedel, Yao and McCallum (2010) aligned Freebase to New York Times articles, argued that the plain distant supervision assumption fails often on news text, where entity pairs co-occur for many reasons, and trained a model with one hidden variable per sentence. Their data became a standard benchmark for later methods.

A worked case. The knowledge base holds born_in(Curie, Warsaw) and works_in(Curie, Paris). The corpus has three sentences that mention Curie and Warsaw: "Curie was born in Warsaw", "Curie was a student in Warsaw" and "Curie left Warsaw for Paris". The bag of (Curie, Warsaw) is labeled born_in, and only the first sentence expresses it. Labeling each sentence gives one correct and two wrong examples; under the at-least-one assumption, the bag is still correct. The third sentence also enters the bag of (Curie, Paris) with the label works_in, which it does not express either.

## Variations

- **Multi-instance learning.** A bag is positive if at least one sentence is; train by expectation and maximization over the hidden sentence labels, as in [expectation maximization](/expectation-maximization/), or by picking the best sentence in each step.
- **Multi-instance multi-label learning.** A pair can have several relations at once, such as born_in and died_in for the same city; models with one hidden label per sentence and several bag labels handle this.
- **Selective attention.** A neural sentence encoder gives a vector per sentence, and an attention weight per sentence, from a softmax over the bag, decides how much each sentence counts for the bag. The method is the same as in [scaled dot-product attention](/scaled-dot-product-attention/) with one query per relation.
- **Noise models.** Learn a transition matrix from the true label to the observed label, or learn which sentences to drop.
- **Data programming and weak supervision.** Combine many noisy labeling sources, such as patterns and knowledge bases, by a model of their accuracies, instead of one knowledge base.
- **Related ideas.** [DIPRE](/dipre/) and the [Yarowsky algorithm](/yarowsky-algorithm/) start from a few seeds and grow them; distant supervision starts from many facts and does not grow the knowledge base during training.

## Pitfalls

- **False positives.** Sentences that mention both entities but say something else get the relation label. The at-least-one assumption and attention reduce the harm but do not remove it.
- **False negatives.** Knowledge bases are incomplete, so a pair labeled none may in fact stand in the relation. A classifier that finds such a fact is counted wrong.
- **Held-out evaluation.** Scoring against held-out knowledge base facts counts true new facts as errors, so it underestimates precision. Report a human evaluation of the top predictions as well.
- **Entity matching errors.** Wrong links put sentences in the wrong bags. Errors of the entity tagger lose sentences.
- **Popular pairs dominate.** A few pairs with many sentences can make up much of the training data; cap the bag sizes or weight the bags.
- **Overlap between training and test.** The same entity pairs, or the same sentences, can occur in the training and test data of common splits; check for overlap before comparing numbers.

## Exercises

1. A bag has three sentences with probabilities 0.9, 0.2 and 0.1 of expressing born_in. Compute the bag score under the mean, the maximum and a softmax weighting with weights proportional to $e^{s_i}$ where $s_i$ are the probabilities. Which rule is closest to the at-least-one assumption?
2. Explain why sampling negative pairs from entity pairs with no relation in the knowledge base produces false negatives, and estimate their share if the knowledge base lists only half of the true facts of one relation.
3. Design a test set for the relation founded_by that avoids the held-out evaluation problem, and say what it costs.
4. Show with an example that the at-least-one assumption is still wrong for some bags. What does a model trained under it learn from such a bag?
5. For the relation lives_in(person, country), why is distant supervision noisier than for born_in(person, city)? Give a sentence type that causes most of the noise.

## References
