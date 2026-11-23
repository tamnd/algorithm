---
tag: 3DDM7T
kind: theorem
slug: parallel-composition-theorem
name: Parallel composition theorem
aliases:
- parallel composition
area: security-and-privacy/differential-privacy
level: core
summary: "Mechanisms run on disjoint parts of the data, with parts fixed before the data is seen, cost only the largest epsilon in total under add/remove neighbors, and at most twice it under replace."
history:
  year: 2009
  people: [Frank McSherry]
  note: "McSherry stated parallel composition in the paper on the PINQ system, where it lets a query on each group of a partition cost only once."
prereqs: [sequential-composition-theorem]
see_also: [sequential-composition-theorem, advanced-composition-theorem, laplace-mechanism, global-sensitivity, binary-tree-mechanism, group-privacy-theorem, post-processing-theorem]
sources:
  - paper: doi:10.1145/1559845.1559850
    title: "Frank McSherry, Privacy integrated queries: an extensible platform for privacy-preserving data analysis, SIGMOD 2009, pages 19 to 30"
    locator: "the section on sequential and parallel composition (the Partition operator of PINQ)"
  - paper: doi:10.1145/1810891.1810916
    title: "Frank McSherry, Privacy integrated queries: an extensible platform for privacy-preserving data analysis, Communications of the ACM 53(9), pages 89 to 97, 2010"
    locator: "the journal version, with the same composition rules"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), pages 211 to 407, 2014"
    locator: "Section 3.5 (composition theorems), which the proof below extends to disjoint inputs"
---

The parallel composition theorem says that queries on disjoint parts of a dataset do not add up their privacy costs. If the records are split into parts by a rule that does not look at the data, and mechanism $j$ reads only part $j$ and is $\varepsilon_j$-differentially private, then all outputs together are $(\max_j \varepsilon_j)$-DP under add/remove neighbors. The reason is that one person's record sits in one part only, so only one mechanism sees a change. A histogram with noise on each bin is the standard use: it costs the $\varepsilon$ of one bin, not the sum over the bins that the [basic composition theorem](/sequential-composition-theorem/) would give. Two conditions matter. The partition must be fixed before the data is seen, and the neighbor relation must be add/remove; under replace the cost can double.

## Statement

A dataset $x$ is a finite multiset of records from a universe $\mathcal U$. Under the add/remove relation, $x \sim x'$ when one of them is the other plus one record. Under the replace relation, $x \sim x'$ when they have the same size and differ in one record.

Let $\pi : \mathcal U \to \{1, \ldots, k\}$ be a fixed function, chosen without access to the data. It splits each dataset into parts $x_j = \{r \in x : \pi(r) = j\}$. For $j = 1, \ldots, k$, let $M_j(x_j; y_1, \ldots, y_{j-1})$ read part $j$ and the earlier outputs. The composed mechanism outputs $(Y_1, \ldots, Y_k)$ with $Y_j \sim M_j(x_j; Y_1, \ldots, Y_{j-1})$. Composition may be adaptive, as on the [basic composition](/sequential-composition-theorem/) page.

**Theorem (parallel composition).** Suppose that for each $j$ and each prefix, $M_j$ is $(\varepsilon_j, \delta_j)$-DP for the add/remove relation on its own part (this includes the empty part).

1. Under add/remove neighbors, the composed mechanism is $(\max_j \varepsilon_j, \max_j \delta_j)$-DP.
2. Under replace neighbors, if each $M_j$ is also $(\varepsilon_j, \delta_j)$-DP for replace on its own part, the composed mechanism is $(\varepsilon^*, \delta^*)$-DP with $\varepsilon^* = \max\left(\max_j \varepsilon_j, \max_{a \ne b} (\varepsilon_a + \varepsilon_b)\right) \le 2 \max_j \varepsilon_j$ and $\delta^* \le 2 \max_j \delta_j$.

## In plain words

Sort the people into groups by a rule you fix in advance, for example by their age band. Ask one private question about each group. Each person is in one group only, so only one answer can depend on them. The total privacy cost for each person is the cost of the one question about their group, and not the sum over all groups.

The rule for the groups must not depend on the data. If it does, one new person can move many others from group to group, and the argument breaks.

If a change of one person can also move that person from one group to another, two answers change. Then the cost can be up to twice as large.

## Proof

Fix a pair of neighbors. The proof of [basic composition](/sequential-composition-theorem/) uses the privacy inequality of each step only for this one pair. So it is enough to find, for each step $j$, numbers $(\varepsilon'_j, \delta'_j)$ such that $M_j(x_j; \text{prefix})$ and $M_j(x'_j; \text{prefix})$ meet the inequality with these numbers for every prefix. Then the composed outputs meet it with $(\sum_j \varepsilon'_j, \sum_j \delta'_j)$.

**Add/remove.** Say $x' = x \cup \{r\}$, and let $j^* = \pi(r)$. Because $\pi$ does not depend on the data, every other record stays in its part. So $x'_j = x_j$ for $j \ne j^*$, and $x'_{j^*} = x_{j^*} \cup \{r\}$. For $j \ne j^*$ the two inputs are equal, so for each prefix the two output laws are equal, and $(\varepsilon'_j, \delta'_j) = (0, 0)$. For $j = j^*$ the two parts are add/remove neighbors, so $(\varepsilon'_{j^*}, \delta'_{j^*}) = (\varepsilon_{j^*}, \delta_{j^*})$. The sum is $(\varepsilon_{j^*}, \delta_{j^*})$, which is at most $(\max_j \varepsilon_j, \max_j \delta_j)$. The case $x = x' \cup \{r\}$ is the same with the roles swapped.

**Replace.** Say $x'$ is $x$ with the record $r$ replaced by $r'$. Let $a = \pi(r)$ and $b = \pi(r')$. If $a = b$, only part $a$ changes, by a replace, and the sum is $(\varepsilon_a, \delta_a)$. If $a \ne b$, part $a$ loses $r$ and part $b$ gains $r'$. Each of these two parts changes by one add/remove step, and the other parts do not change. The sum is $(\varepsilon_a + \varepsilon_b, \delta_a + \delta_b)$. Both cases are at most $(\varepsilon^*, \delta^*)$. $\blacksquare$

## Consequences

- **Histograms and contingency tables.** Let the parts be the bins, and let $M_j$ release the count of bin $j$ plus Laplace noise of scale $1/\varepsilon$ (the [Laplace mechanism](/laplace-mechanism/) on a count). With 5 bins and $\varepsilon = 0.5$, each bin gets noise of scale 2. The whole histogram is $0.5$-DP under add/remove, while basic composition would only give $2.5$. Under replace the same release is $1.0$-DP, which matches the [global sensitivity](/global-sensitivity/) $\Delta_1 = 2$ of a histogram under replace.
- **Trees of counts.** In the [binary tree mechanism](/binary-tree-mechanism/), the nodes on one level cover disjoint time ranges, so each level costs the $\varepsilon$ of one node. The levels are then combined by sequential composition.
- **Query systems.** PINQ has a Partition operator that splits the data by a key list given in advance and charges the budget once for all parts.
- **Data-dependent splits need their own budget.** A split that is chosen from the data, for example at a private median, must be paid for first. Then the parts are fixed, and the theorem applies to the queries after that point, by sequential composition of the two stages.

## Tightness

**The maximum is reached.** In the histogram above, adding a record to bin $j$ raises its count by 1. At an output $y$ with $y_j$ above both counts, the density ratio of the Laplace noise is exactly $e^{\varepsilon}$. So the release is not $\varepsilon'$-DP for any $\varepsilon' < \varepsilon$, and the bound $\max_j \varepsilon_j$ is exact.

**The factor 2 under replace is reached.** Replace a record of bin $a$ by a record of bin $b \ne a$. Count $a$ goes down by 1 and count $b$ goes up by 1. At an output with $y_a$ below and $y_b$ above all counts, the ratio is $e^{\varepsilon} \cdot e^{\varepsilon} = e^{2\varepsilon}$.

**A partition that reads the data fails.** Let the universe be $\{0, 1\}$. If $x$ holds at least one record with value 1, put all records in part 1; else put all records in part 2. Release each part's size plus noise of scale $1/\varepsilon$. Each step is $\varepsilon$-DP on its own part. Now take $x$ with $n$ records of value 0 and $x' = x \cup \{1\}$. The true pair of sizes moves from $(0, n)$ to $(n + 1, 0)$. The privacy loss at some outputs is $(2n + 1)\varepsilon$, which grows with $n$. So no bound in terms of $\varepsilon$ alone holds.

## History

McSherry (2009) introduced parallel composition, together with sequential composition, in the paper on PINQ, a query language with a built-in privacy budget. The journal version appeared in Communications of the ACM in 2010. The theorem was implicit earlier in the analysis of histograms, where a record changes one cell only. The need for a data-independent split and the factor 2 under replace neighbors are standard points in the later literature, because the papers of that time used different neighbor relations.

## References
