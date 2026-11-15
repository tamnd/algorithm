---
tag: 5BD152
kind: concept
slug: cranfield-paradigm
name: Cranfield paradigm
aliases:
- Cranfield evaluation methodology
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: intro
summary: Evaluates retrieval systems offline on a fixed set of documents, queries and relevance judgments, so systems can be compared and repeated.
prereqs: [test-collection]
see_also: [pooling, interleaved-evaluation, precision-at-k, mean-average-precision, normalized-discounted-cumulative-gain, sign-test, permutation-test]
sources:
  - paper: doi:10.1108/eb050097
    title: Cyril W. Cleverdon, The Cranfield tests on index language devices, Aslib Proceedings 19(6), 1967, pp. 173-194
    locator: abstract and conclusions (the specificity of index terms matters most; single-word terms did better than concept terms and a controlled vocabulary)
  - paper: doi:10.1007/3-540-45691-0_34
    title: Ellen M. Voorhees, The philosophy of information retrieval evaluation, in Evaluation of Cross-Language Information Retrieval Systems, CLEF 2001, LNCS 2406, 2002, pp. 355-370
    locator: the sections on the Cranfield paradigm and its assumptions (relevance approximated by topical similarity, one set of judgments standing for the user population, complete judgments) and on the appropriate uses of test collections
  - book: isbn:9780262220736
    title: Ellen M. Voorhees and Donna K. Harman (editors), TREC, Experiment and Evaluation in Information Retrieval, MIT Press, 2005
    locator: Chapter 1, The Text REtrieval Conference, and Chapter 3, Chris Buckley and Ellen M. Voorhees, Retrieval system evaluation, pp. 53-75
  - paper: doi:10.1561/1500000009
    title: Mark Sanderson, Test collection based evaluation of information retrieval systems, Foundations and Trends in Information Retrieval 4(4), 2010, pp. 247-375
    locator: the sections on the Cranfield tests and on the assumptions of test collection evaluation
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8, Sections 8.1 and 8.2
---

The Cranfield paradigm evaluates a retrieval system without users. It runs the system on a fixed [test collection](/test-collection/) of documents, topics and relevance judgments, and turns the agreement between each ranking and the judgments into a score. It is named after the experiments that Cyril Cleverdon ran at Cranfield in the 1960s, and it is the method of TREC, CLEF and NTCIR. Its scores can be repeated and compared, at the price of a few strong assumptions about what relevance is.

## In plain words

To learn whether one search system is better than another, you could watch real people use both. That is slow, costly and hard to repeat. The Cranfield method puts a fixed test in place of the people. The test is a set of documents, a set of questions, and a list that says which documents answer which question. Each system answers every question, its results are checked against the list, and the matches become a score. The test does not change, so anyone can repeat it and get the same score. The price is a set of simple beliefs: that the people who made the list speak for all users, that a document is useful on its own, whatever else is shown, and that the list misses few useful documents.

## The idea

**The parts.** An experiment in the Cranfield style fixes five things.

1. A test collection $(D, Q, J)$: documents, topics and judgments.
2. The systems to compare, each of which produces a run, a ranking of $D$ for every topic in $Q$.
3. A metric that scores one ranking against the judgments of one topic, such as [precision at k](/precision-at-k/), [average precision](/mean-average-precision/) or [nDCG](/normalized-discounted-cumulative-gain/), with its rules for tied scores and for topics with no relevant document.
4. An aggregate over topics, usually the arithmetic mean.
5. A test of whether the difference between two systems is larger than the variation over topics, such as the [sign test](/sign-test/), the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) or a [permutation test](/permutation-test/).

The collection and the rules are shared, so a result can be checked by anyone with the same data, and a later system can be scored on the same terms as an earlier one.

**The assumptions.** Voorhees (2002) lists the assumptions that make a Cranfield score stand for the quality of a system for its users.

- Relevance can be approximated by topical similarity. It follows that all relevant documents are equally useful, that the relevance of a document does not depend on the other documents in the ranking, and that the information need does not change while the user reads.
- One set of judgments stands for the whole population of users.
- The judgments are complete: every relevant document is known.

None of them holds exactly. Different assessors disagree on many documents. A second document that repeats the first is less useful, which [alpha-nDCG](/alpha-ndcg/) tries to capture. Large collections are judged by [pooling](/pooling/), so many relevant documents are never found.

**What follows from them.** Voorhees (2002) argues that a test collection is suited to comparing systems on the same collection, and much less to absolute claims such as "this system finds 60% of the relevant documents". This splits the claims made with the paradigm into two kinds.

- Proved, for a fixed collection and fixed rules: the score of a run is a deterministic function of the run file, so it can be repeated. Properties of a metric, such as "average precision is 1 exactly when all relevant documents come first", are proved on the metric pages and hold for every ranking.
- Measured: that the order of systems stays much the same when the assessors change, when judgments are removed, or when the pool is built without one of the systems. These are results of experiments on particular collections (Sanderson 2010 surveys them), and they can fail for a new kind of system.

## Examples

### Two runs on one topic

On the toy collection of this area, topic q1 "sorted array search" has the relevant documents d1 (grade 2), d2 and d8 (grade 1), so $R = 3$. Run A ranks 1, 6, 8, 2, 4, and run B ranks 1, 2, 8, 7, 4.

| Metric | Run A | Run B |
|---|---|---|
| Precision at 3 | 2/3 | 1 |
| Average precision | 29/36 = 0.8056 | 1 |
| Reciprocal rank | 1 | 1 |
| nDCG at 5, gain equal to the grade | 0.9360 | 1 |

B is better on three metrics, and the two runs tie on reciprocal rank, because both put a relevant document first. The comparison uses one topic, so no test can say whether B would stay better on other topics; a real comparison uses 50 topics or more and a paired test.

Run A comes from scores that tie d1 with d6 and d2 with d4. With the tie rule of this area, score descending and then document id ascending, it is the ranking above. trec_eval breaks the ties the other way, reads 6, 1, 8, 4, 2, and reports an average precision of $53/90 \approx 0.5889$ for the same file. A Cranfield result is repeatable only when such rules are fixed and reported.

### The Cranfield tests

Cleverdon's second Cranfield project compared index languages, the ways of describing a document by terms for retrieval. The documents were papers on aeronautics, and the judgments were made for every pair of query and document. Cleverdon (1967) reports that the specificity of the index terms mattered most, and that single words taken from the documents did better than terms built from concepts or taken from a controlled vocabulary. This was a surprise at the time, and it supported indexing by the words of the text.

### TREC

TREC, run by NIST since 1992, applies the paradigm each year to large collections. NIST releases the documents and the topics, the groups submit runs, NIST pools the top documents of the runs and has assessors judge them, and all groups receive the judgments and the scores (Voorhees and Harman 2005, Chapter 1). The judgments are then reused to score systems that were not in the pool, which is where the assumption of complete judgments matters most.

### A contrast with online evaluation

[Interleaved evaluation](/interleaved-evaluation/) shows real users a merge of two rankings and counts which ranking gets more clicks. It needs no judgments and measures real behaviour, but it needs live traffic, and its result cannot be repeated on a later day with the same users. The two are complementary: a Cranfield experiment is cheap to repeat and is used to choose between many candidates, and an online test checks the few that remain.

## Where it is used

- The shared evaluation campaigns TREC, CLEF and NTCIR, and the research papers that reuse their collections.
- Test collections built for one company or product, where editors judge results for a sample of real queries.
- The evaluation of [learning to rank](/learning-to-rank/) methods, whose data sets are test collections with graded judgments, usually scored by nDCG.
- The retrieval part of [retrieval-augmented generation](/retrieval-augmented-generation/), where passages are judged for questions and scored by recall or [mean reciprocal rank](/mean-reciprocal-rank/).
- Work on cheaper judgments, such as [pooling](/pooling/), [bpref](/bpref/), [inferred average precision](/inferred-average-precision/) and [minimal test collections](/minimal-test-collection/), which all keep the paradigm and relax the assumption of complete judgments.

## References
