---
tag: 0M80MN
kind: problem
slug: relation-extraction
name: Relation extraction
aliases:
- relation classification
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Find pairs of entity mentions in a text and the semantic relation that holds between them, such as born in or employed by."
prereqs: [named-entity-recognition, classification]
see_also: [dipre, distant-supervision, entity-linking, hearst-patterns, dependency-parsing, kernel-trick, shortest-path, span-f1-score]
sources:
  - paper: "Iris Hendrickx, Su Nam Kim, Zornitsa Kozareva, Preslav Nakov, Diarmuid Ó Séaghdha, Sebastian Padó, Marco Pennacchiotti, Lorenza Romano and Stan Szpakowicz, SemEval-2010 Task 8: multi-way classification of semantic relations between pairs of nominals, Proceedings of SemEval 2010"
    title: Hendrickx et al. 2010
    locator: the nine relation types with direction plus Other, the data and the official macro-averaged F1
  - paper: "Dmitry Zelenko, Chinatsu Aone and Anthony Richardella, Kernel methods for relation extraction, Journal of Machine Learning Research 3, 2003"
    title: Zelenko et al. 2003
    locator: kernels over shallow parse trees for relation classification
  - paper: "Razvan C. Bunescu and Raymond J. Mooney, A shortest path dependency kernel for relation extraction, Proceedings of HLT-EMNLP 2005"
    title: Bunescu and Mooney 2005
    locator: the kernel on the shortest dependency path between the two entities
  - paper: "Mike Mintz, Steven Bills, Rion Snow and Dan Jurafsky, Distant supervision for relation extraction without labeled data, Proceedings of ACL-IJCNLP 2009"
    title: Mintz et al. 2009
    locator: training a relation classifier from Freebase facts matched to sentences
---

Relation extraction finds facts of the form "entity A stands in relation R to entity B" in text. From "Marie Curie was born in Warsaw" it extracts born_in(Marie Curie, Warsaw). It works on top of [named entity recognition](/named-entity-recognition/), which finds the entities, and it feeds knowledge bases, often through [entity linking](/entity-linking/), which says which real entities the names denote. The core form is a classification problem: given a sentence and two marked entity mentions, say which relation from a fixed list holds between them, or none. Methods range from hand-written patterns, through bootstrapping from seeds such as [DIPRE](/dipre/), to trained classifiers, [distant supervision](/distant-supervision/) and pretrained neural encoders.

## In plain words

Take a sentence with two names marked in it, for example a person and a city. Decide whether the sentence says something about how they are related, and what: the person was born there, lives there, works there, or nothing. The list of possible relations is fixed in advance. Most pairs of names in a sentence have no relation from the list, so "none" is the most common answer. The words between the two names, and the grammar that connects them, are the strongest clues: "born in", "the mayor of", "founded by". The order matters too: "A acquired B" is not "B acquired A".

## Definition

**Input.** A sentence (or a document) of tokens $x_1, \ldots, x_n$; entity mentions given as typed spans $(i, j, t)$ in fencepost indices, so that $(i, j)$ covers tokens $i + 1, \ldots, j$; and a set $\mathcal{R}$ of relation types.

**Output.** For each ordered pair $(a, b)$ of entity mentions, a relation $r \in \mathcal{R} \cup \{\mathrm{none}\}$. Relations are directed: $r(a, b)$ and $r(b, a)$ are different facts, unless $r$ is symmetric.

**Relation classification** is the form where one pair is given per example and only the label is predicted. **End-to-end relation extraction** finds the mentions and the relations together.

**Score.** Precision, recall and F1 over the predicted relation instances other than none. A prediction is correct only if both arguments, their order and the relation type are right. Some data sets average F1 over relation types (macro), others over instances (micro); the SemEval-2010 Task 8 score is the macro F1 over its nine relation types, with direction taken into account (Hendrickx et al. 2010).

## Variants

- Sentence-level classification: one pair per example, as in SemEval-2010 Task 8, which has nine directed relation types such as Cause-Effect and Component-Whole, plus Other.
- Mention-level extraction with entity types: relations between typed mentions, as in the ACE data, with types such as part-whole and employment.
- Document-level extraction: the two entities may appear in different sentences, and the fact may need several sentences.
- Knowledge base population: facts about given entities, collected over a large corpus, where one correct sentence per fact suffices.
- Open information extraction: no fixed list of relations; the relation is the phrase that links the arguments, such as (Curie, "was born in", Warsaw).
- n-ary relations and events: facts with more than two arguments, such as a drug, a gene and a mutation, or an attack with its time and place.

## Examples

"Marie Curie was born in Warsaw and worked in Paris." With the mentions Marie Curie (PER), Warsaw (LOC) and Paris (LOC), the ordered pairs give born_in(Curie, Warsaw), employed_in(Curie, Paris), and none for (Warsaw, Paris) and for every reversed pair.

Direction: "Google acquired YouTube" gives acquired(Google, YouTube), and a system that predicts acquired(YouTube, Google) is wrong.

A hard negative: "Obama never visited Lagos" contains a person and a place and the word "visited", but the sentence denies the relation.

## Known algorithms

- Hand-written patterns: lexical and syntactic patterns such as "X, the CEO of Y", as in the [Hearst patterns](/hearst-patterns/) for the is-a relation. High precision, low recall.
- Bootstrapping from seeds: [DIPRE](/dipre/) and Snowball alternate between learning patterns from known pairs and finding new pairs with the patterns.
- Feature-based classifiers: [logistic regression](/logistic-regression/) or a [support vector machine](/support-vector-machine/) on features such as the words between the mentions, their entity types and the path between them in the dependency tree.
- Kernel methods: compare two examples by a kernel on their parse trees (Zelenko et al. 2003) or on the [shortest path](/shortest-path/) between the two entities in the dependency graph (Bunescu and Mooney 2005), and train a support vector machine with the [kernel trick](/kernel-trick/).
- [Distant supervision](/distant-supervision/): label sentences automatically by matching the entity pairs of a knowledge base, then train a classifier on the noisy labels (Mintz et al. 2009).
- Neural classifiers: encode the sentence with marks around the two entities, by a convolutional or recurrent network, or by a pretrained [transformer](/transformer/) such as [BERT](/bert/), and classify the pair from the representations of the marks or the entities.

## Bounds

- A sentence with $k$ entity mentions has $k (k - 1)$ ordered pairs, so classifying every pair takes $O(k^2)$ classifier calls (a theorem, by counting). Restricting pairs by entity type, or by distance, lowers the count in practice.
- With a transformer encoder of cost $O(n^2 d)$ for $n$ tokens and width $d$, one encoding of the sentence can serve all pairs if the pair classifier reads only the entity representations; marking the entities in the input instead needs one encoding per pair.
- Finding the dependency path between two mentions costs $O(n)$ by [breadth-first search](/breadth-first-search/) on the tree.

## Reductions

- Relation classification is [multiclass classification](/multiclass-classification/) of a (sentence, pair) example into $|\mathcal{R}| + 1$ classes, or $2 |\mathcal{R}| + 1$ when each direction is a class.
- End-to-end extraction reduces to [named entity recognition](/named-entity-recognition/) followed by relation classification of all pairs; joint models avoid the errors that the pipeline passes on.
- Knowledge base population combines relation extraction with [entity linking](/entity-linking/), so that facts attach to the right entities.
- [Distant supervision](/distant-supervision/) reduces the need for labels to a knowledge base and an entity linker, at the price of noisy labels.

## Applications

- Building and updating knowledge bases from news, the web or scientific papers.
- Biomedical text mining: interactions between proteins, drugs and genes.
- Question answering: the answer to "Where was Curie born?" is the second argument of a born_in fact.
- Business intelligence: acquisitions, executives and products from news.

## References
