---
tag: YZVC9W
kind: model
slug: rhetorical-structure-theory
name: Rhetorical structure theory
aliases:
- RST
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: A theory of discourse that builds a tree over text spans joined by relations such as elaboration or contrast between nucleus and satellite.
prereqs: [parse-tree, constituency-parsing]
see_also: [centering-theory, coreference-resolution, automatic-summarization, text-segmentation, catalan-numbers, cyk-algorithm, shift-reduce-parsing, parseval-measures]
sources:
  - paper: "William C. Mann and Sandra A. Thompson, Rhetorical Structure Theory: Toward a functional theory of text organization, Text 8(3), 243-281, 1988"
    title: "William C. Mann and Sandra A. Thompson, Rhetorical Structure Theory: Toward a functional theory of text organization"
    locator: "the definitions of relations by constraints on the nucleus, the satellite and their combination and by their effect, the schemas, and the constraints on schema applications"
  - url: https://aclanthology.org/W01-1605/
    title: "Lynn Carlson, Daniel Marcu and Mary Ellen Okurowski, Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory, Proceedings of the Second SIGdial Workshop on Discourse and Dialogue, 2001"
    locator: "the RST Discourse Treebank of 385 Wall Street Journal documents, its segmentation into elementary discourse units, its relation set and its agreement study"
---

Rhetorical structure theory (RST), introduced by Mann and Thompson in 1988, describes how the parts of a text work together. It splits the text into small units, roughly clauses, and builds a tree over them in which neighboring spans are joined by relations such as Elaboration, Evidence, Contrast or Cause. Most relations are unequal: one span, the nucleus, carries the main point, and the other, the satellite, supports it, so that the nuclei passed up the tree give the gist of the text. RST trees are the target of discourse parsing, which works much like [constituency parsing](/constituency-parsing/) with the units in place of words.

## The machine

**Units.** A text is a sequence $e_1, \ldots, e_m$ of elementary discourse units (EDUs), usually clauses, found by a separate segmentation step. Spans are fenceposts over units: the span $(i, j)$ covers the units $e_{i+1}, \ldots, e_j$.

**Relations.** A relation is defined by constraints on the nucleus, constraints on the satellite, constraints on how they combine, and its intended effect on the reader. Evidence, for example, holds when the reader may not yet believe the nucleus, the satellite is something the reader believes or will find credible, and reading the satellite raises the reader's belief in the nucleus. A relation is either

- **mononuclear**, with one nucleus and one satellite, such as Elaboration, Evidence, Background, Circumstance, Concession, Condition, Purpose and Justify, or
- **multinuclear**, with two or more nuclei of equal weight, such as Contrast, Sequence, Joint and List.

**Trees.** A schema application joins adjacent spans under one relation. Mann and Thompson require that the schema applications together cover the whole text (completeness), that every span except the whole text is part of a larger span (connectedness), that each schema application covers a different set of spans (uniqueness), and that the spans of each application are adjacent (adjacency). The result is a tree over contiguous spans whose leaves are the units. Each internal node is labeled with a relation, and each child is marked as a nucleus or a satellite. Most annotation schemes and parsers use binary trees, writing a relation over several spans as a chain of binary ones.

**Nuclearity.** The promotion set of a node is its own unit if it is a leaf, and otherwise the union of the promotion sets of its nuclear children. The promotion set of the root lists the units that the tree marks as most central.

**An example.** The text

> [The new parser is fast.]$_1$ [It uses a supertagger,]$_2$ [which removes most categories before parsing.]$_3$ [However, it fails on long sentences.]$_4$

has the tree

```
Contrast (multinuclear) over (0, 4)
├── Evidence over (0, 3)
│   ├── nucleus: unit 1                        span (0, 1)
│   └── satellite: Elaboration over (1, 3)
│       ├── nucleus: unit 2                    span (1, 2)
│       └── satellite: unit 3                  span (2, 3)
└── nucleus: unit 4                            span (3, 4)
```

Units 2 and 3 together are the evidence that the parser is fast, unit 3 elaborates unit 2, and the whole first part contrasts with unit 4. The promotion set of the root is $\{1, 4\}$: "The new parser is fast. However, it fails on long sentences." is a fair two-sentence summary.

## What it counts

**Number of trees (theorem).** The number of binary trees with ordered leaves over $m$ units is the Catalan number $C_{m-1} = \frac{1}{m}\binom{2m-2}{m-1}$; see [Catalan numbers](/catalan-numbers/). Each internal node also chooses a relation and a nuclearity pattern, so the number of labeled trees is $C_{m-1}$ times $R^{m-1}$ for $R$ choices of relation and nuclearity per node. A parser must not enumerate them.

**Discourse parsing.** The task takes a text, segments it into units and builds the labeled tree. Two algorithm families are standard.

- **Chart parsing (theorem for the cost).** If the score of a tree is a sum of scores of its labeled nodes, each a function of the span, the split point and the label, then the [CKY algorithm](/cyk-algorithm/) over units finds the best tree in $O(m^3 R)$ time and $O(m^2)$ space, exactly as for a grammar in Chomsky normal form with the units as words.
- **Shift-reduce parsing.** A [shift-reduce](/shift-reduce-parsing/) parser keeps a stack of subtrees, shifts the next unit or reduces the top two subtrees under a labeled relation, and builds a binary tree with $2m - 1$ actions, so it runs in $O(m)$ steps given a classifier of constant cost (theorem for the step count). It is greedy or uses a beam, so it can miss the best tree (heuristic).

**Evaluation (measurement).** Parsers are scored by an F1 over the internal nodes of the tree, in the manner of [PARSEVAL](/parseval-measures/): on spans alone, on spans with nuclearity, on spans with relations, and on all three. Results depend a lot on whether gold or predicted units are used.

**Corpus size (measurement).** The RST Discourse Treebank of Carlson, Marcu and Okurowski (2001) annotates 385 Wall Street Journal documents, with 21,789 units, using a relation set that is larger than the original one of Mann and Thompson and grouped into classes.

## Relation to other models

- **Constituency trees.** An RST tree is a constituency tree over units instead of words, with nuclearity in place of heads. Parsers and metrics carry over, as above.
- **Dependency form.** Following the nuclei, each unit can be attached to the head unit of the span it supports, which turns an RST tree into a dependency tree over units. Several RST trees give the same dependency tree.
- **Shallow discourse models.** The Penn Discourse Treebank marks only discourse connectives, such as "however", and their two arguments, with no tree over the text. It is easier to annotate and covers implicit relations between adjacent sentences, but it does not give a structure for the whole text.
- **Graph-based models.** Segmented discourse representation theory and other graph models allow a unit to attach to more than one span, or to spans that are not adjacent. Some studies found that real texts need such structures, which a tree cannot show (heuristic).
- **Entity-based coherence.** [Centering theory](/centering-theory/) and [coreference](/coreference-resolution/) model coherence by which entities a text keeps talking about. RST models it by the relations between propositions. The two views are complementary.
- **Text segmentation.** [Text segmentation](/text-segmentation/) splits a text into topical blocks without relations. RST segmentation into units is much finer, roughly one unit per clause.

## Known results in the model

- **Summaries from nuclearity (heuristic).** Marcu and others ranked units by how high they are promoted in the tree and used the top-ranked units as an extractive summary. This works when the tree is right, and it ties the quality of [automatic summarization](/automatic-summarization/) to the quality of discourse parsing.
- **Agreement (measurement).** Annotators agree more on spans than on nuclearity, and more on nuclearity than on relations, which is why the evaluation reports the three levels separately. The RST Discourse Treebank paper reports such an agreement study.
- **Text generation.** RST began in work on text generation, where a planner chooses relations and orders the units, and it is still used to plan the structure of generated texts.
- **Learned parsers (measurement).** Neural discourse parsers with pretrained encoders are much better at spans and nuclearity than at fine relation labels, and the labels remain the hardest part.

## References
