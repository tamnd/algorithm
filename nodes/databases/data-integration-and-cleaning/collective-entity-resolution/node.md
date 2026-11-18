---
tag: YRGXXR
kind: technique
slug: collective-entity-resolution
name: Collective entity resolution
aliases:
- relational entity resolution
area: databases/data-integration-and-cleaning
level: advanced
summary: "Resolve references jointly: the links between records, such as shared co-authors, add evidence, and each merge changes the evidence for the pairs that are left."
prereqs: [entity-resolution, agglomerative-clustering]
see_also: [correlation-clustering, r-swoosh, entity-resolution-blocking, priority-queue, jaccard-similarity, factor-graph, conditional-random-field, gibbs-sampling]
sources:
  - paper: "Indrajit Bhattacharya and Lise Getoor, Collective entity resolution in relational data, ACM Transactions on Knowledge Discovery from Data 1(1), 2007, article 5"
    locator: the combined similarity of attributes and relations with the weight alpha, the greedy agglomerative clustering with a priority queue and the update of the neighbours after each merge, the bootstrapping, and the experiments on bibliographic data
  - paper: "Xin Dong, Alon Halevy and Jayant Madhavan, Reference reconciliation in complex information spaces, Proceedings of the ACM SIGMOD International Conference on Management of Data, 2005"
    locator: the dependency graph of reference pairs, in which a reconciliation decision is propagated to the pairs that depend on it
---

Collective entity resolution decides which references are the same entity *together*, not one pair at a time. Besides the attributes of two references, such as their names, it uses their *relations*: the co-authors of an author name, or the people at the same address. A pair of author names becomes more likely the same person when their co-authors were already found to be the same people. So each merge changes the evidence for other pairs, and the method repeats until no pair is strong enough. [Correlation clustering](/correlation-clustering/) also finds a partition that agrees with pairwise evidence, but its signs or scores are fixed before it starts. In collective resolution the relational part of a score depends on the current clusters. [R-Swoosh](/r-swoosh/) compares merged records again, but only through their own values, not through other records.

## In plain words

Two papers list an author as "W. Wang" and "Wei Wang". The names alone do not tell you whether they are one person. But if both papers also have "A. Ansari" as a co-author, and you already believe that both Ansaris are one person, then the two Wangs are probably one person too. Once you join them, that decision helps with the next pair. You keep joining the pair with the strongest evidence, and after each join you recompute the evidence of the pairs that are linked to it. A wrong join can also spread, so the rule for joining must be strict.

## When it applies

- The references come with relations to other references: co-authors on papers, people in one household, products in one order.
- Attributes alone are ambiguous, for example many authors share short names.
- The relations are themselves references that need resolving, so the decisions depend on each other.

If the records have no links, or the attributes alone decide well, pairwise methods are simpler and cheaper.

## The template

The greedy agglomerative form of Bhattacharya and Getoor:

```pseudo id=main
CollectiveER(references, relations, α, θ)
L1  C ← the initial clusters (bootstrap: merge references that match exactly and are not ambiguous)
L2  Q ← a priority queue of candidate pairs of clusters, from blocking, keyed by sim
L3  while Q is not empty and the top pair has sim ≥ θ do
L4      (c_i, c_j) ← the top pair of Q;  replace c_i and c_j by c = c_i ∪ c_j
L5      update in Q every pair that has c_i or c_j, now with c
L6      for each cluster c_k related to c do update the sims of the pairs of c_k in Q
L7  return C
```

The similarity of two clusters is
$$\mathrm{sim}(c_i, c_j) = (1 - \alpha)\, \mathrm{sim}_A(c_i, c_j) + \alpha\, \mathrm{sim}_R(c_i, c_j), \qquad 0 \le \alpha \le 1,$$
where $\mathrm{sim}_A$ compares the attributes, for example the names, and $\mathrm{sim}_R$ compares the sets of clusters that the two clusters are related to, for example with the [Jaccard similarity](/jaccard-similarity/) of their co-author clusters. Line L6 is the collective step: a merge changes the related clusters of other clusters, so their $\mathrm{sim}_R$ changes. With $\alpha = 0$ the method is plain [agglomerative clustering](/agglomerative-clustering/) on the attributes. The weight $\alpha$ and the threshold $\theta$ are heuristics, set on labelled data. The queue is a [priority queue](/priority-queue/) with updates.

## Classic examples

**Author names.** Three papers: P1 by "W. Wang" (r1) and "A. Ansari" (r2), P2 by "Wei Wang" (r3) and "A. Ansari" (r4), and P3 by "W. Wong" (r5) and "C. Chen" (r6). The true entities are {r1, r3}, {r2, r4}, {r5} and {r6}. Take $\mathrm{sim}_A$(r1, r3) = 0.6, $\mathrm{sim}_A$(r1, r5) = 0.8 and $\mathrm{sim}_A$(r3, r5) = 0.5, with $\alpha = 0.5$ and $\theta = 0.6$.

- *Attributes only.* r1 and r5 (0.8) and r1 and r3 (0.6) pass the threshold, so all three are one cluster, which is wrong.
- *Collectively.* The bootstrap merges r2 and r4 into one cluster $a$. Now r1 and r3 both have the co-author cluster $\{a\}$, so $\mathrm{sim}_R = 1$ and $\mathrm{sim} = 0.5 \cdot 0.6 + 0.5 \cdot 1 = 0.8$. For r1 and r5 the co-author clusters $\{a\}$ and $\{r6\}$ share nothing, so $\mathrm{sim} = 0.5 \cdot 0.8 = 0.4$, and for r3 and r5 it is $0.25$. Only r1 and r3 are merged. After that merge, the new cluster and r5 have no shared co-author, so their similarity stays below $\theta$. The result is the true one.

**Bibliographic data.** Bhattacharya and Getoor measured the method on citation data sets with author references and found that the relational part raised the F1 score over attribute-only clustering on those data sets. This is a measurement, not a guarantee.

**Personal information.** Dong, Halevy and Madhavan reconcile people, e-mail addresses and papers in a personal information space. Each pair of references is a node of a dependency graph, and a decision on one pair raises or lowers the similarity of the pairs that depend on it.

## Variations

- **Dependency graphs.** Keep a graph of reference pairs and propagate each decision to the pairs that depend on it, as Dong et al. do, with merged references enriching each other.
- **Probabilistic models.** Put all match decisions into one model, such as a [conditional random field](/conditional-random-field/) or a [factor graph](/factor-graph/), and infer them jointly, for example with [Gibbs sampling](/gibbs-sampling/).
- **Clustering with fixed scores.** Compute the scores once, then find a partition with [correlation clustering](/correlation-clustering/). This is consistent but not collective in the sense above.
- **Blocking first.** Run [blocking](/entity-resolution-blocking/) so that the queue holds only pairs that share a block, which keeps the queue small.

## Pitfalls

- **Errors spread.** A wrong merge creates relational evidence for more wrong merges. Use a strict $\theta$, and a bootstrap that merges only names that are not ambiguous.
- **Order matters.** The greedy order is a heuristic. Two runs with different ties can give different clusters.
- **Update cost.** One merge can change the scores of many pairs through line L6. On dense relations this costs much more than one pass of pairwise scoring.
- **Popular neighbours.** A very common related entity, such as a large lab or a common co-author, makes many references look related. Weight related clusters by how rare they are.
- **Tuning on the test data.** $\alpha$ and $\theta$ fitted on the data that is then measured give scores that are too high.

## Exercises

1. In the example, show that r1 and r3 pass $\theta = 0.6$ for every $\alpha$, find the values of $\alpha$ at which r1 and r5 also pass, and say which range of $\alpha$ gives the true clusters.
2. Show that with $\alpha = 0$ the template returns single-linkage clusters at threshold $\theta$ when $\mathrm{sim}_A$ of two clusters is the largest similarity of their members.
3. Give an example in which one wrong bootstrap merge causes a second wrong merge through $\mathrm{sim}_R$.
4. Explain why the result of the template can depend on the order of ties in the priority queue, while the components of a fixed match graph cannot.

## References
