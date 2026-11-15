---
tag: NAXKG5
kind: model
slug: boolean-retrieval-model
name: Boolean retrieval model
aliases:
- exact-match retrieval
area: information-retrieval-and-ai-reasoning/ranking-models
level: intro
summary: A query is a Boolean expression of terms, and a document is returned when it satisfies the expression, with no ranking.
prereqs: [term-document-incidence-matrix, posting-list]
see_also: [posting-list-intersection, merge-based-list-intersection, inverted-index, ranked-retrieval, vector-space-model, conjunctive-normal-form, phrase-query, precision-and-recall]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 1 (Boolean retrieval, the inverted index, Section 1.3 on the processing of Boolean queries and the order of terms by increasing document frequency, Section 1.4 on extended Boolean and ranked retrieval)
  - book: isbn:9780321416919
    title: Ricardo Baeza-Yates and Berthier Ribeiro-Neto, Modern Information Retrieval, second edition, Addison-Wesley, 2011
    locator: Chapter 3 (modeling, the Boolean model and its comparison with the vector and probabilistic models)
  - paper: doi:10.1145/182.358466
    title: Gerard Salton, Edward A. Fox and Harry Wu, Extended Boolean information retrieval, Communications of the ACM 26(11), 1022 to 1036, 1983
    locator: the p-norm model, which goes from strict Boolean matching at p equal to infinity to a vector inner product at p equal to 1
---

In the Boolean retrieval model a query is an expression of terms joined by AND, OR and NOT, and the answer is the set of documents that satisfy it. Each document counts only as the set of its terms, which is one column of the [term-document incidence matrix](/term-document-incidence-matrix/). An engine evaluates the query with set operations on the [posting lists](/posting-list/) of an [inverted index](/inverted-index/), mostly by [intersection](/posting-list-intersection/). A document either matches or does not match, so the model gives no order among the documents it returns.

## The machine

**Documents and queries.** Let $D = \{d_1, \ldots, d_N\}$ be a collection and $V$ its vocabulary. Each document $d$ is reduced to its set of terms $T(d) \subseteq V$, so the number of occurrences and the order of words are lost. A query is a formula built from terms by the grammar

$$q ::= t \mid q \text{ AND } q \mid q \text{ OR } q \mid \text{NOT } q, \qquad t \in V.$$

**Meaning.** The answer $M(q) \subseteq D$ is defined by induction on the formula:

$$M(t) = \{d : t \in T(d)\}, \quad M(q_1 \text{ AND } q_2) = M(q_1) \cap M(q_2), \quad M(q_1 \text{ OR } q_2) = M(q_1) \cup M(q_2), \quad M(\text{NOT } q) = D \setminus M(q).$$

Read as logic, each term $t$ is a propositional variable that is true for $d$ when $t \in T(d)$, and $d$ is in $M(q)$ when the formula is true for $d$. The answer is a set, and an engine returns it in some fixed order, such as document id or date, which the model does not define.

**Evaluation on an index.** $M(t)$ is the posting list of $t$, sorted by document id. AND is a merge [intersection](/merge-based-list-intersection/) of two sorted lists, OR is a merge union, and $q_1$ AND NOT $q_2$ is a merge difference. Each step of a merge costs one comparison and reads one posting. A bare NOT $q$ needs the list of all $N$ ids, so engines accept NOT only inside an AND. For a conjunction of $m$ terms, a good order intersects the lists in order of increasing document frequency $\mathrm{df}(t)$, so that each intermediate result is at most the size of the shortest list (Manning, Raghavan and Schuetze, Section 1.3).

**Example.** In the toy collection of the information retrieval pages, $N = 8$, tokens are the lower-case words split on spaces, and there is no stemming. Six posting lists:

| term | $\mathrm{df}$ | posting list |
|---|---|---|
| sorted | 4 | 1, 2, 4, 8 |
| array | 3 | 1, 2, 8 |
| search | 2 | 1, 7 |
| posting | 3 | 3, 4, 5 |
| list | 2 | 3, 4 |
| merge | 2 | 2, 5 |

- sorted AND array gives $\{1, 2, 4, 8\} \cap \{1, 2, 8\} = \{1, 2, 8\}$.
- sorted AND array AND search starts with the shortest list, search $= \{1, 7\}$. Its intersection with array gives $\{1\}$, and the intersection with sorted keeps $\{1\}$.
- sorted AND NOT array gives $\{1, 2, 4, 8\} \setminus \{1, 2, 8\} = \{4\}$.
- posting OR merge gives $\{2, 3, 4, 5\}$.
- posting AND list AND merge gives the empty set, although $d_5$ is "skip pointers speed up the merge of two posting lists". The token "lists" is not the term "list". With a [stemmer](/stemming/) that maps both words to "list", the answer is $\{5\}$.

The query sorted AND array returns $d_1$, $d_2$ and $d_8$ with no order among them, while a ranking model such as [BM25](/bm25/) puts $d_1$ first because it also contains "search".

## What it counts

- **Answer set.** The output is a set. Its quality is measured by the [precision and recall](/precision-and-recall/) of that set against the relevance judgments, not by measures of a ranked list.
- **Postings read.** The main cost of evaluation is the number of postings read and compared. A merge of lists of lengths $n_1$ and $n_2$ reads at most $n_1 + n_2$ postings. [Skip pointers](/skip-pointers/) let a merge jump over runs of postings, and with galloping search an intersection of lists of lengths $m \le n$ takes $O(m \log_2(n/m) + m)$ comparisons.
- **Size of the answer.** The model gives no control over $|M(q)|$. Adding a term with AND can only shrink the answer, and adding a term with OR can only grow it. On a large collection the user must often rewrite a query many times to get an answer that is neither empty nor too large.

## Relation to other models

- **Incidence matrix.** On the term-document incidence matrix, AND, OR and NOT are the bitwise operations on the rows of the terms, and the answer is the set of columns with a 1. This is the dense form of the same model.
- **Vector space model.** The [vector space model](/vector-space-model/) gives each document a score and ranks all documents, so a document that misses one query term can still rank high. The *extended Boolean* model of Salton, Fox and Wu (1983) joins the two: an AND or OR of weighted terms has a $p$-norm score. At $p = \infty$ the score is the strict Boolean answer, and at $p = 1$ it is proportional to an inner product of weights.
- **Coordination level matching.** Counting how many query terms a document contains, and ranking by that count, is the simplest bridge from Boolean matching to ranking. The [binary independence model](/binary-independence-model/) with equal term weights gives this order.
- **Boolean filter with ranking.** Many engines first apply a Boolean condition, often an AND of the query terms or a set of required fields, and then rank the documents that pass with a score such as BM25. Dynamic pruning methods such as [WAND](/wand/) evaluate the ranked part.
- **Positions.** A [phrase query](/phrase-query/) or a proximity condition is not a Boolean expression of terms, because it depends on the order of words. It needs a [positional index](/positional-index/).
- **Propositional logic.** Every query is a propositional formula, and every propositional formula over the terms is a query. It can be rewritten in [conjunctive normal form](/conjunctive-normal-form/), an AND of ORs, which some professional search systems used as their query form.

## Known results in the model

- **Every set condition is a query.** AND, OR and NOT are functionally complete, so every condition on which terms a document contains, and on which it does not contain, is expressed by some query.
- **Query satisfiability and equivalence.** Every truth assignment of the terms is the term set of some possible document. So a query has a nonempty answer on some collection exactly when its formula is satisfiable, which is NP-complete to decide. Two queries give the same answer on every collection exactly when their formulas are equivalent, which is coNP-complete.
- **Evaluation cost.** With posting lists, an AND of $m$ terms costs $O(\sum_t \mathrm{df}(t))$ by merging, and processing the terms in order of increasing $\mathrm{df}$ keeps every intermediate list no longer than the shortest one. See [posting-list intersection](/posting-list-intersection/) for the adaptive bounds.
- **Use in practice.** Boolean search with extensions such as proximity operators and truncation was the main form of commercial and library search before ranked retrieval. It is still used for legal, patent and systematic medical searches, where users want a precise and repeatable answer set (Manning, Raghavan and Schuetze, Chapter 1).

## References
