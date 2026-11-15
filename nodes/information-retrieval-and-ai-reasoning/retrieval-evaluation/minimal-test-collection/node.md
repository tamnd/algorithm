---
tag: 19JM8C
kind: algorithm
slug: minimal-test-collection
name: Minimal test collection
aliases:
- Carterette-Allan-Sitaraman method
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: research
summary: Judges pooled documents one at a time, each chosen for how much it can tighten bounds on the difference in average precision, and stops once the sign of that difference is fixed.
model: word-ram
complexity:
  vars: {m: the number of documents in either ranking}
  time: {worst: O(m^3)}
  space: {extra: O(m^2)}
properties: {deterministic: true, recursive: false}
prereqs: [mean-average-precision, pooling]
see_also: [test-collection, inferred-average-precision, bpref, cranfield-paradigm, interleaved-evaluation]
sources:
  - paper: doi:10.1145/1148170.1148219
    title: Ben Carterette, James Allan and Ramesh Sitaraman, Minimal test collections for retrieval evaluation, SIGIR 2006, pp. 268-275
    locator: Section 3 (the difference in AP as a sum over pairs and the stopping condition), Section 3.1 (the weights and the rule that judges the document with the largest of p times the weight for relevant and 1 - p times the weight for not relevant, p = 0.5), Section 3.2 (a stop with 95% confidence), Section 3.3 (MAP), Section 4.5 (cost and many systems), the appendix (Algorithm 1 and Theorem 1), and the Robust 2005 experiments
---

A minimal test collection is a set of relevance judgments that is just large enough to decide which of two retrieval systems has the higher [average precision](/mean-average-precision/) on a query. Carterette, Allan and Sitaraman introduced the method in 2006. It writes the difference in average precision as a sum over pairs of documents, keeps a lower and an upper bound on that sum over all relevance values of the documents not yet judged, and asks the assessor to judge the document that can move a bound the most. When the lower bound is above 0 or the upper bound is below 0, the sign of the difference is known, and the rest of the [pool](/pooling/) need not be judged.

## In plain words

You want to know which of two search engines is better on a query, and judging each result costs time. You do not need the exact scores of the engines, only which one is higher.

Look at the results that the two engines rank in different places. A result that one engine puts near the top and the other puts low can change the comparison a lot, so judge it first. A result that both engines rank in the same place can change the comparison only a little, so it is judged late or never.

After each judgment, work out the best and the worst case for the comparison over every way the remaining results could turn out. When even the worst case says that one engine is better, stop.

## The problem

The input is two rankings $A$ and $B$ for one query, and an assessor who returns $x_d = 1$ if document $d$ is relevant and 0 if not. Let $P$ be the $m$ documents in $A$ or $B$, and $R$ the number of relevant documents in the collection. The output is the sign of $\mathrm{AP}(A) - \mathrm{AP}(B)$ and the list of documents judged, with the guarantee that the sign is the same for every relevance of the documents not judged. The goal is to judge few documents.

For a document $i$ at rank $r_A(i)$ of $A$, let $a_{ii} = 1 / r_A(i)$, and for two documents of $A$ let $a_{ij} = 1 / \max(r_A(i), r_A(j))$; let $a_{ij} = 0$ when one of them is not in $A$. Define $b_{ij}$ for $B$ in the same way, and $c_{ij} = a_{ij} - b_{ij}$. Then

$$R \, (\mathrm{AP}(A) - \mathrm{AP}(B)) = D = \sum_{i \le j} c_{ij} x_i x_j,$$

because a relevant document $i$ adds its precision at its rank, and that precision counts each relevant document $j$ ranked at or above $i$ with weight $1 / r(i)$. Relevant documents outside $P$ change $R$ but not the sign of $D$.

## The algorithm

Let $S$ be the documents judged relevant, $N$ those judged not relevant, and $T$ those not judged. A pair with a document in $N$ adds 0 to $D$, and a pair inside $S$ adds $c_{ij}$. Every other pair lies in the set $F$ of pairs that are still open; it adds $0$ or $c_{ij}$. So with $K = \sum_{i, j \in S} c_{ij}$,

$$\mathrm{lo} = K + \sum_{F} \min(0, c_{ij}) \le D \le K + \sum_{F} \max(0, c_{ij}) = \mathrm{hi}.$$

For $i \in T$, let $w^R_i$ and $w^N_i$ be the rise of lo if $i$ is judged relevant or not relevant, and $v^R_i$ and $v^N_i$ the fall of hi in the same two cases.

```pseudo id=main
MINIMAL-TEST-COLLECTION(A, B, judge, p)
L1  c_ij ← a_ij - b_ij for all documents i ≤ j of A ∪ B
L2  S ← ∅, N ← ∅, T ← the documents of A ∪ B
L3  loop
L4      lo, hi ← the bounds on D given S, N and T
L5      if lo > 0 return A, S ∪ N; if hi < 0 return B, S ∪ N; if lo = hi return tie, S ∪ N
L6      if the budget is used return undecided, S ∪ N
L7      for each i ∈ T do
L8          s_i ← max(p·w^R_i, (1 - p)·w^N_i, p·v^R_i, (1 - p)·v^N_i)
L9      i* ← the i ∈ T with the largest s_i, ties to the smallest id
L10     if judge(i*) = 1 then move i* from T to S else move i* from T to N
```

The weights have short forms. Judging $i$ relevant closes the pairs of $i$ with $S$ and with itself, so $w^R_i = \sum_{j \in S \cup \{i\}} \max(0, c_{ij})$ and $v^R_i = \sum_{j \in S \cup \{i\}} \max(0, -c_{ij})$. Judging $i$ not relevant sets all its open pairs to 0, so $w^N_i = \sum_{j \in S \cup T} \max(0, -c_{ij})$ and $v^N_i = \sum_{j \in S \cup T} \max(0, c_{ij})$. Carterette, Allan and Sitaraman state the rule of line L8 for one direction: to show that $A$ is better, judge the document with the largest $\max(p \, w^R_i, (1 - p) \, w^N_i)$, with $p = 0.5$ when nothing is known about the document. The sign is not known in advance, so line L8 here takes the maximum over both directions.

## Example

Take query q1 "sorted array search" of the toy collection of this area, with documents 1, 2 and 8 relevant, and the scores of its run: documents 1 and 6 tie at 2.0, document 8 has 1.5, and documents 2 and 4 tie at 1.0. Breaking the ties in two ways gives two rankings: $A = (1, 6, 8, 2, 4)$ by increasing id, and $B = (6, 1, 8, 4, 2)$ by decreasing id, which is the order trec_eval uses for ties. Their average precisions are $29/36 = 0.8056$ and $53/90 = 0.5889$. The nonzero coefficients are $c_{11} = 1/2$, $c_{66} = -1/2$, $c_{22} = c_{26} = c_{28} = c_{12} = 1/20$, and $c_{44} = c_{46} = c_{48} = c_{14} = -1/20$. Document 8 is at rank 3 in both, so $c_{88} = 0$, and the pair $(1, 6)$ has $c_{16} = 1/2 - 1/2 = 0$.

| step | S | N | lo | hi | $s_1$ | $s_2$ | $s_4$ | $s_6$ | $s_8$ | judged |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | -7/10 | 7/10 | 11/40 | 1/10 | 1/10 | 11/40 | 1/40 | 1: relevant |
| 2 | 1 | | -1/5 | 7/10 | | 1/10 | 1/10 | 11/40 | 1/40 | 6: not relevant |
| 3 | 1 | 6 | 7/20 | 13/20 | | | | | | stop: A |

In step 1, documents 1 and 6 tie, and the smaller id wins. After two judgments $\mathrm{lo} = 7/20 > 0$, so $A$ is better whatever documents 2, 4 and 8 turn out to be. The true value is $D = 3 \, (29/36 - 53/90) = 13/20$, which here equals hi. Two of the five pooled documents were enough: the comparison depends only on the order of the tied documents, and documents 1 and 6 are the ones whose order differs the most.

## Correctness

The proof is in `proofs/correctness.md`. The identity $D = R \, (\mathrm{AP}(A) - \mathrm{AP}(B))$ holds for every relevance vector, and every open pair lies between $\min(0, c_{ij})$ and $\max(0, c_{ij})$, so $\mathrm{lo} \le D \le \mathrm{hi}$ for every completion of the judgments. If $\mathrm{lo} > 0$, then $D > 0$ in every completion, so some document is relevant, $R > 0$ and $A$ has the higher average precision; the case $\mathrm{hi} < 0$ is the same, and $\mathrm{lo} = \mathrm{hi}$ means $D = 0$ in every completion. Each pass judges one new document, and when none is left $\mathrm{lo} = \mathrm{hi}$, so the loop stops after at most $m$ judgments. The rule of line L8 only changes how many judgments are made, not what the stop guarantees. The tests check the sign returned against a brute force over all relevance values of the documents not judged.

## Complexity

- **Time.** Line L1 builds $O(m^2)$ coefficients. Each pass reads every pair once in line L4 and one row of coefficients per document in line L8, so it takes $O(m^2)$ time, and at most $m$ passes take $O(m^3)$. The paper gives $O(S^2 n^2)$ for $S$ systems and $n$ documents, since the weights are taken over all pairs of systems.
- **Space.** The coefficients take $O(m^2)$ space. Only pairs of documents that both rankings retrieve near each other have large values, so a sparse table helps in practice.
- **Judgments.** At most $m$, and often far fewer. In the paper's experiments on the Robust 2005 track, 2200 judgments in about 2.5 hours ranked the systems with high confidence, while the NIST pool for the same track took 37,798 judgments and 280.5 hours.

## Properties

- **Sound.** When the loop returns a sign, no relevance of the documents not judged can change it, and documents outside the pool cannot change it either.
- **Sufficient, not necessary.** The bounds take the worst value of each open pair on its own. Let $A = (3, 2, 4, 1)$ and $B = (3, 4, 1, 2)$, with documents 2 and 4 judged relevant and 1 not relevant. Then $\mathrm{lo} = 0$ and $\mathrm{hi} = 5/12$, but $D$ is $1/6$ or $1/4$ for the two values of document 3, so the sign is already fixed and the loop judges one more document.
- **Monotone.** All four weights are at least 0, so each judgment keeps lo or raises it and keeps hi or lowers it.
- **Equal ranks cancel.** A document at the same rank in both rankings has $c_{ii} = 0$, and a pair has $c_{ij} = 0$ when the same one of its two documents is the lower one in both rankings, at the same rank. In the example, document 8 is at rank 3 in both, and its only nonzero coefficients come from documents 2 and 4 below it, so its score stays at $1/40$.
- **Optimal in one sense.** The appendix of the paper proves an optimality result for the choice rule when all $p$ are equal, and the authors say that it covers only part of the method. The number of judgments that the loop makes is not shown to be the minimum.

## Variants and improvements

- **Tighter bounds.** Group all the open pairs of a document $i$ with $S$ and with itself into one linear coefficient $\ell_i = c_{ii} + \sum_{j \in S} c_{ij}$, and bound $\ell_i x_i$ by $\min(0, \ell_i)$ and $\max(0, \ell_i)$. This is never looser, because $\min(0, u + v) \ge \min(0, u) + \min(0, v)$. In the example above it gives $\ell_3 = 0 + 1/4 - 1/6 = 1/12$ and $\mathrm{lo} = 1/6 > 0$, so the loop stops one judgment earlier. The pairs inside $T$ still need their own bounds.
- **A stop with confidence.** Treat each unknown $x_d$ as a coin with probability $p_d$, and stop when the probability that $D > 0$ is high under a normal approximation; the paper uses 95%. This stops much earlier than the sound rule, at the cost of a small chance of error.
- **Mean average precision and many systems.** Sum the forms over queries to compare MAP, and take each document's weight as the largest over all pairs of systems to rank many systems at once. The paper also uses the expected value of AP, with $p_d = 1/2$ for documents not judged, to give each system a score.
- **Other measures.** A measure that is linear in the relevance values, such as [precision at k](/precision-at-k/) or discounted cumulative gain with binary gains, has only terms $c_{ii} x_i$, and the same bounds apply with no pairs.

## When to use it

Use it when the question is which of a few systems is better and the judging budget is small, for example when a lab compares new runs on new topics. It is not a way to estimate the value of AP itself, and the judgments it collects are chosen for the systems being compared, so they are not a fair sample for scoring a new system later. For an estimate of AP from a random sample of judgments, use [inferred average precision](/inferred-average-precision/).

## Pitfalls

- **Treating documents not judged as not relevant.** Line L4 must bound $D$ over every completion. If it puts $x_d = 0$ for $d \in T$, as trec_eval does for a missing judgment, it computes one value of $D$ and can stop with the wrong sign.
- **Dropping the pairs inside T.** In line L4 the pairs with both documents not judged are open too. A bound that keeps only the pairs with one document in $S$ misses terms such as $c_{46}$ in the example and is not sound.
- **Rounding at the stop.** When two rankings differ only by documents that cancel, $D$ is exactly 0, but floating point sums can give a tiny positive lo and line L5 then declares a winner. Use exact fractions, as the code does, or a tolerance.
- **One direction only.** If line L8 uses only $w^R$ and $w^N$, the loop keeps trying to show that $A$ is better even when $B$ is, and judges documents that cannot lower hi. It still stops, but later.
- **Reading the judgments as a test collection.** The documents in $S \cup N$ were chosen by the two rankings, so a third system scored on them gets a biased value of AP.

## Implementations

## History

Carterette, Allan and Sitaraman presented minimal test collections at SIGIR 2006. They connected evaluation with the building of the test collection: instead of judging a fixed [pool](/pooling/) and then computing measures, the measure to compare decides which documents to judge. On the Robust 2005 track they ranked the systems with a small fraction of the judgments that NIST had made, and after 1000 judgments, about one hour of work, the ranking had 90% confidence. The method was later used, with sampling methods such as [inferred average precision](/inferred-average-precision/), in TREC tracks with many queries and few judgments per query.

## References
