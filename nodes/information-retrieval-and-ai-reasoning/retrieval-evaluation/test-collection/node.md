---
tag: T1GF7G
kind: definition
slug: test-collection
name: Test collection
aliases:
- relevance judgment collection
- qrels
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: intro
summary: A document set, a set of topics and judgments of which documents are relevant to each topic, used to score systems.
prereqs: [precision-and-recall]
see_also: [cranfield-paradigm, pooling, precision-at-k, mean-average-precision, normalized-discounted-cumulative-gain, bpref, interleaved-evaluation, click-model]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8, Section 8.1 (the three parts of a test collection), Section 8.2 (standard test collections, from Cranfield to TREC) and Section 8.5 (assessing relevance)
  - book: isbn:9780262220736
    title: Ellen M. Voorhees and Donna K. Harman (editors), TREC, Experiment and Evaluation in Information Retrieval, MIT Press, 2005
    locator: Chapter 2, Donna K. Harman, The TREC test collections (documents, topics with title, description and narrative, and judgments)
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: file get_trec_results.c (the rank field is ignored and ranks come from sorting by the score field), file form_res_rels.c (tied scores are ordered by document number in reverse lexical order) and file trec_eval.c (option -c, missing queries contribute 0)
  - paper: doi:10.1561/1500000009
    title: Mark Sanderson, Test collection based evaluation of information retrieval systems, Foundations and Trends in Information Retrieval 4(4), 2010, pp. 247-375
    locator: the sections on the history and the construction of test collections
---

A test collection is a fixed set of documents, a set of topics that state information needs, and relevance judgments that say which documents are relevant to which topic. It turns the question "is this search system good?" into a computation: run the system on every topic, compare each ranking with the judgments by a metric, and average over the topics. Because the three parts do not change, two systems, or one system before and after a change, can be scored on the same data and the result can be repeated. The [Cranfield paradigm](/cranfield-paradigm/) is the method built on this object.

## Definition

A **test collection** is a triple $(D, Q, J)$.

- $D$ is a finite set of documents, each with a unique id.
- $Q$ is a finite set of topics. A topic states an information need. A TREC topic has a short title, used as the query in most experiments, a one-sentence description and a narrative that tells the assessor what counts as relevant.
- $J$ is a set of judgments, each a triple $(q, d, g)$ with $q \in Q$, $d \in D$ and a grade $g \in \{0, 1, 2, \ldots\}$, with at most one judgment per pair $(q, d)$. Grade 0 means judged not relevant. A binary collection uses only the grades 0 and 1.

A pair $(q, d)$ with no judgment is **unjudged**. Most metrics treat an unjudged document as not relevant, that is, as grade 0; [bpref](/bpref/) is a metric that removes unjudged documents instead. For a topic $q$, $R_q$ is the number of documents $d$ with a judgment $(q, d, g)$, $g \ge 1$. A document is relevant when its grade is at least the relevance threshold, which is 1 in this area and in the default of trec_eval.

The judgments are **complete** for $q$ when every document of $D$ is judged for $q$. Complete judgments are possible only for small collections. Large collections use [pooling](/pooling/): only the top documents of a set of systems are judged, and the rest stay unjudged.

**Scoring a system.** A *run* gives, for each topic $q$, a ranking of documents of $D$, with a score per document. A metric maps a ranking and the judgments of one topic to a number, and the score of the run is a mean of these numbers over the topics. Three rules must be fixed for the result to be repeatable.

- **Order of tied scores.** This area orders by score descending, then by document id ascending. trec_eval sorts the results by score and orders tied scores by document number in reverse lexical order (file form_res_rels.c). It ignores the rank column of the run file. Two programs that follow different rules can give different values from one run file.
- **Topics with $R_q = 0$.** For [average precision](/mean-average-precision/), [R-precision](/r-precision/), [nDCG](/normalized-discounted-cumulative-gain/) and bpref the value is undefined. In this area the metric returns None and the topic is left out of the mean.
- **Which topics count.** trec_eval scores only the topics that are in the judgments file. A topic there with no relevant document gets 0 for most measures and counts in the mean. A topic that is in the judgments file but missing from the run is left out unless the option -c is given, and then it counts as 0.

## Examples and non-examples

### The toy collection of this area

$D$ has 8 documents.

| Id | Text |
|---|---|
| d1 | binary search finds a key in a sorted array |
| d2 | merge sort merges two sorted runs into one sorted array |
| d3 | an inverted index maps each term to a posting list |
| d4 | a posting list is a sorted list of document ids |
| d5 | skip pointers speed up the merge of two posting lists |
| d6 | a hash table finds a key in constant expected time |
| d7 | search engines rank documents by a score for the query |
| d8 | the sorted array of ids is compressed with gap encoding |

$Q$ has 4 topics, and $J$ has graded judgments with 2 for highly relevant and 1 for relevant. Every pair not listed is grade 0, so the judgments are complete.

| Topic | Query | Relevant documents (grade) | $R_q$ |
|---|---|---|---|
| q1 | sorted array search | d1 (2), d2 (1), d8 (1) | 3 |
| q2 | posting list merge | d5 (2), d4 (1), d3 (1) | 3 |
| q3 | rank documents | d7 (2) | 1 |
| q4 | quantum circuit | none | 0 |

The judgments for q1 to q3 in the TREC format, one judgment per line with the fields topic, iteration (not used), document id and grade:

```text
q1 0 d1 2
q1 0 d2 1
q1 0 d8 1
q2 0 d5 2
q2 0 d4 1
q2 0 d3 1
q3 0 d7 2
```

A fixed run for q1 in the TREC results format, with the fields topic, the literal Q0, document id, rank, score and run name:

```text
q1 Q0 d1 1 2.0 A
q1 Q0 d6 2 2.0 A
q1 Q0 d8 3 1.5 A
q1 Q0 d2 4 1.0 A
q1 Q0 d4 5 1.0 A
```

With the tie rule of this area the ranking is 1, 6, 8, 2, 4, and its [precision at](/precision-at-k/) rank 1 is 1. trec_eval ignores the rank column and reads 6, 1, 8, 4, 2, because "d6" comes after "d1" and "d4" after "d2" in lexical order. Its precision at rank 1 is then 0, from the same file.

Topic q4 shows the edge case. No document is relevant, so average precision and nDCG are undefined and the topic is left out of their means here. Since the judgment lines above list only grades of at least 1, q4 is not in that file at all, and trec_eval does not score it. If the file also had a line such as `q4 0 d6 0`, trec_eval would score q4 and give it 0.

### Cranfield and TREC

The Cranfield II collection is small enough for complete judgments: Manning, Raghavan and Schuetze (Section 8.2) give 1398 abstracts of aerodynamics papers and 225 queries, with every pair judged. The TREC collections have hundreds of thousands to millions of documents, 50 topics per track and year in the ad hoc tracks, and judgments made by pooling (Harman, Chapter 2 of the TREC book).

### Non-examples

- A query log with clicks. It has documents and queries, but no judgments. Clicks depend on the rank at which a result was shown, so they are not a judgment of relevance; see [click models](/click-model/) and [position bias](/position-bias/). Logs serve for online evaluation such as [interleaving](/interleaved-evaluation/).
- A set of queries with no judgments. A system can be run on them but not scored.
- Judgments of search results made against a document set that keeps changing, such as the live web. A new system may return documents that did not exist when the judgments were made, so its score is not comparable to the old ones.
- A labelled data set for a classifier. It has one label per item, not one label per pair of a topic and a document, and it is scored by measures of a [confusion matrix](/confusion-matrix/), not of a ranking.

## Related definitions

- The [Cranfield paradigm](/cranfield-paradigm/) is the experimental method that uses a test collection, and states the assumptions under which its scores mean something.
- [Pooling](/pooling/) builds the judgments of a large test collection. [Bpref](/bpref/), [inferred average precision](/inferred-average-precision/) and [minimal test collections](/minimal-test-collection/) are ways to work with judgments that are incomplete.
- [Precision and recall](/precision-and-recall/) are the basic set measures. The ranked metrics of this area are [precision at k](/precision-at-k/), [R-precision](/r-precision/), [average precision](/mean-average-precision/), the [interpolated precision-recall curve](/interpolated-precision-recall-curve/), [mean reciprocal rank](/mean-reciprocal-rank/) and [nDCG](/normalized-discounted-cumulative-gain/).
- A difference between two systems on a test collection is a mean over its topics. Whether it would hold on other topics is a question for a paired test over the topics, such as the [sign test](/sign-test/) or a [permutation test](/permutation-test/).

## References
