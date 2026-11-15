---
tag: SMAEPR
kind: algorithm
slug: rocchio-algorithm
name: Rocchio algorithm
aliases:
- Rocchio relevance feedback
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Moves the query vector toward the centroid of the relevant documents and away from the centroid of the nonrelevant ones.
solves: [ranked-retrieval]
model: word-ram
complexity:
  vars: {z: the total number of nonzero weights in the query and the judged document vectors}
  time: {worst: O(z)}
  space: {extra: O(z)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1971
  people: [Joseph J. Rocchio]
  note: Rocchio described the update in a chapter of The SMART Retrieval System, edited by Gerard Salton, and tested it on the SMART collections.
prereqs: [relevance-feedback, vector-space-model, cosine-similarity]
see_also: [pseudo-relevance-feedback, relevance-model-rm3, tf-idf, stop-word-removal, precision-and-recall]
sources:
  - paper: "J. J. Rocchio, Relevance feedback in information retrieval, in Gerard Salton (editor), The SMART Retrieval System: Experiments in Automatic Document Processing, Prentice-Hall (1971)"
    locator: the query modification that adds the relevant document vectors and subtracts the nonrelevant ones
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 9, Section 9.1.1 (the Rocchio algorithm, the weights alpha = 1, beta = 0.75 and gamma = 0.15, and the rule that negative term weights are ignored)
  - paper: "Gerard Salton and Chris Buckley, Improving retrieval performance by relevance feedback, Journal of the American Society for Information Science 41(4) (1990), 288-297"
    locator: the comparison of twelve feedback methods on six test collections, evaluated on the residual collection, in which the Ide dec-hi variant did best overall
---

The Rocchio algorithm is the classic method of [relevance feedback](/relevance-feedback/) in the [vector space model](/vector-space-model/). After a first search, the user marks some of the results as relevant and some as not relevant. Rocchio builds a new query vector from the old one by adding a multiple of the centroid (the mean vector) of the relevant documents and subtracting a smaller multiple of the centroid of the nonrelevant ones. The new query then runs again. It gains weight on terms that the relevant documents share, including terms that the user never typed, and loses weight on terms of the nonrelevant ones. Joseph Rocchio described it in 1971 for the SMART system.

## In plain words

A short query often misses good documents because they use other words. After the first search, the user looks at a few results and says which ones are good and which are bad. Each document is a list of word weights. Rocchio takes the average of the good documents and adds it to the query, so the query now also asks for the words that the good documents have in common. It takes the average of the bad documents and subtracts a small part of it, so words that only the bad documents use count less. Words that end up with a negative weight are dropped. The new query then runs again, and documents that look like the good ones move up, even if they do not share a word with the first query.

## The problem

The input is a query vector $q$ over the vocabulary, a set $D_r$ of document vectors that the user judged relevant, a set $D_n$ judged nonrelevant, and three weights $\alpha, \beta, \gamma \ge 0$. The vectors are sparse: each maps terms to weights, for example term frequencies or [tf-idf](/tf-idf/) weights, and most terms have weight 0. The output is a new query vector $q^+$, which is then used to rank the collection by [cosine similarity](/cosine-similarity/). Either set of judged documents may be empty.

## The algorithm

For a nonempty set $D$, the centroid is $c(D) = \frac{1}{|D|} \sum_{d \in D} d$.

```pseudo id=main
ROCCHIO(q, Dr, Dn, α, β, γ)
L1  q' ← α · q
L2  if Dr is not empty: q' ← q' + β · c(Dr)
L3  if Dn is not empty: q' ← q' - γ · c(Dn)
L4  remove every term t with q'(t) ≤ 0
L5  return q'
```

So $q^+ = \max(0, \alpha q + \beta c(D_r) - \gamma c(D_n))$, taken term by term. Line L4 is the usual rule: Manning, Raghavan and Schütze write that negative term weights are ignored, that is, set to 0. A common setting, which their book gives as reasonable, is $\alpha = 1$, $\beta = 0.75$ and $\gamma = 0.15$. The choice $\gamma < \beta$ trusts positive feedback more than negative feedback. These values are conventions that came from experiments, not results of a proof.

## Example

Take query "sorted array search" on the toy collection, with raw term counts as weights, so $q$ has weight 1 on each of its three terms. The first search ranks document 1, "binary search finds a key in a sorted array", first. The user marks document 1 relevant and document 6, "a hash table finds a key in constant expected time", nonrelevant. The table shows the weights after each line, with $\alpha = 1$, $\beta = 0.75$ and $\gamma = 0.15$; the five terms of document 6 that document 1 lacks behave alike, so one column stands for them.

| term | sorted | array | search | a | binary | finds | in | key | hash, table, constant, expected, time |
|---|---|---|---|---|---|---|---|---|---|
| after L1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| after L2 | 1.75 | 1.75 | 1.75 | 1.5 | 0.75 | 0.75 | 0.75 | 0.75 | 0 |
| after L3 | 1.75 | 1.75 | 1.75 | 1.2 | 0.75 | 0.6 | 0.6 | 0.6 | -0.15 |
| after L4 | 1.75 | 1.75 | 1.75 | 1.2 | 0.75 | 0.6 | 0.6 | 0.6 | removed |

The word "a" occurs twice in each of the two documents. The cosine scores of the eight documents before and after feedback are below, to 4 places.

| document | 1 | 2 | 6 | 4 | 8 | 7 | 3 | 5 |
|---|---|---|---|---|---|---|---|---|
| before | 0.5222 | 0.5000 | 0 | 0.1543 | 0.3651 | 0.1826 | 0 | 0 |
| after | 0.8780 | 0.4327 | 0.3461 | 0.3166 | 0.3160 | 0.2663 | 0.1083 | 0 |

The new order is $1, 2, 6, 4, 8, 7, 3, 5$. Document 1 gains, as it should. But document 6, which the user rejected, climbs from a score of 0 to third place. It shares "a", "finds", "key" and "in" with document 1, and these words got positive weight from the relevant document, much more than the small penalty from the nonrelevant one. With the [stop words](/stop-word-removal/) "a" and "in" removed from all vectors, the new query is sorted, array and search at 1.75, binary at 0.75, and finds and key at 0.6. The order becomes $1, 2, 8, 7, 4, 6, 3, 5$, with document 6 sixth at 0.1402, and the scores of document 1 rise from 0.7071 to 0.9084.

## Correctness

Lines L1 to L3 compute $\alpha q + \beta c(D_r) - \gamma c(D_n)$ term by term, and line L4 keeps the positive part; the file proofs/correctness.md proves this, and that scaling all three weights by the same positive number does not change the ranking. It also proves the fact behind the method. If all document vectors have length 1, then among all unit query vectors, the one that maximizes the mean cosine with the relevant documents minus the mean cosine with the nonrelevant ones is the difference of the two centroids, scaled to length 1; the proof writes the objective as a dot product with $c(D_r) - c(D_n)$ and applies the Cauchy-Schwarz inequality. Rocchio's update is this optimal query, plus $\alpha q$ to stay near what the user asked, with $\gamma < \beta$.

The theorem is about the judged documents only. That the new query ranks unjudged relevant documents higher is a measured effect. Salton and Buckley compared twelve feedback methods on six collections and found clear gains for the vector methods, with the Ide dec-hi variant, which subtracts only the highest-ranked nonrelevant document, the best overall in their tests.

## Complexity

Line L1 copies the query, and lines L2 and L3 read each nonzero weight of each judged document once and add it into a hash map. So the update takes $O(z)$ time and $O(z)$ extra space, where $z$ is the total number of nonzero weights in $q$ and the judged vectors. Line L4 scans the result once. The real cost comes after: the new query can have hundreds of terms, and each term is a posting list to read in the second search, so the second search is much slower than the first. Systems often keep only the $m$ terms of largest weight, as the function `top_terms` of the code does.

## Properties

- **Linear.** The new query is a linear combination of the old query and the two centroids, cut at 0. Adding a relevant document that equals the current centroid of $D_r$ does not change $c(D_r)$.
- **Only ratios matter.** Multiplying $\alpha$, $\beta$ and $\gamma$ by the same positive number scales the query and leaves the cosine ranking the same.
- **Expands the query.** Every term of every relevant document gets a positive weight from line L2, so the new query can match documents that share no word with the old one.
- **Order of judgments does not matter.** The centroids are means, so the result depends on the sets $D_r$ and $D_n$, not on the order in which the user judged them.
- **No feedback, no change.** With both sets empty, the result is $\alpha q$, which ranks like $q$.

## Variants and improvements

- **Ide regular and Ide dec-hi.** Ide's variants add the relevant vectors without dividing by $|D_r|$, and dec-hi subtracts only the top-ranked nonrelevant document. Salton and Buckley found dec-hi the best of the methods they tested.
- **Positive feedback only.** Setting $\gamma = 0$ is common, because nonrelevant documents are many and varied, and their centroid says little about what to avoid.
- **Pseudo relevance feedback.** Treat the top $k$ results of the first search as relevant, with no user, and apply the same update. This is [pseudo-relevance feedback](/pseudo-relevance-feedback/); Rocchio with $\gamma = 0$ is one of its standard forms.
- **Language model feedback.** In the language modeling approach, the analogue of Rocchio mixes the query model with a model estimated from the feedback documents, as the [relevance model](/relevance-model-rm3/) does.
- **Term selection.** Keep only the top $m$ terms by weight, or only terms with a high tf-idf in the relevant set, to bound the cost of the second search and reduce noise.

## When to use it

Use Rocchio when you have a vector space retrieval system and some judgments, from users, from clicks, or from a pseudo feedback step, and you want a cheap way to expand the query. It works best when the relevant documents form one cluster in the vector space, so that their centroid is a good representative. It works badly when the relevant documents are of several kinds, such as documents in two languages or about two senses of a word, because their centroid then lies between the clusters and may be close to neither.

## Pitfalls

- **Stop words and common words.** Line L2 gives positive weight to every word of the relevant documents, including "a" and "in". In the example these words lift the rejected document 6 to third place. Remove stop words or use idf weights before the update, not raw counts.
- **Keeping negative weights.** Without line L4, the new query has negative weights, and a document gets a lower score for containing a term of the nonrelevant set. With cosine similarity this can rank a document below one that shares nothing with the query. Drop the negative weights as in line L4, unless you have tested the other choice.
- **Too much feedback weight.** A large $\beta$ relative to $\alpha$ lets the relevant documents replace the user's query. If the judged documents are about a side topic, the new query follows them. Keep $\alpha$ large enough that the original terms stay among the strongest, as sorted, array and search do in the example.
- **Evaluating on the judged documents.** The judged relevant documents rise after feedback almost by construction. Measure the gain on the documents the user has not seen yet, the residual collection, as Salton and Buckley do.
- **Long queries.** The new query holds every term of every relevant document, so the second search reads many posting lists. Cut the query to its top terms.

## Implementations

## History

Rocchio developed the method for the SMART retrieval system that Gerard Salton led, first at Harvard and then at Cornell, and his chapter in the 1971 book on SMART is the usual reference. The update is usually explained by the query that best separates the relevant from the nonrelevant documents, which is the centroid difference of the correctness section. Eleanor Ide studied variants in the same period. In 1990 Salton and Buckley compared the main feedback methods on six collections and showed consistent gains from feedback. The method then became the standard way to expand queries in vector space systems, and the TREC experiments of the 1990s used it in automatic form, with the top results of a first search taken as relevant.

## References
