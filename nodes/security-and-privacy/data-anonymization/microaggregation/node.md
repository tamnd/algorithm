---
tag: CKSR6M
kind: technique
slug: microaggregation
name: Microaggregation
aliases:
- microaggregation masking
area: security-and-privacy/data-anonymization
level: core
summary: Groups numerical records into clusters of at least k and replaces each value by its cluster mean, with least loss of information.
prereqs: [k-anonymity, clustering-problem]
see_also: [mdav, generalization-and-suppression, data-swapping, post-randomization-method, k-means, ward-method, l-diversity, t-closeness]
sources:
  - book: isbn:9781119978152
    title: "Anco Hundepool, Josep Domingo-Ferrer, Luisa Franconi, Sarah Giessing, Eric Schulte Nordholt, Keith Spicer and Peter-Paul de Wolf, Statistical Disclosure Control, Wiley, 2012"
    locator: "Chapter 3, Microdata, pp. 23 to 130, the perturbative masking methods for continuous data and the measures of information loss"
  - paper: doi:10.1109/69.979982
    title: "Josep Domingo-Ferrer and Josep Maria Mateo-Sanz, Practical data-oriented microaggregation for statistical disclosure control, IEEE Transactions on Knowledge and Data Engineering 14(1), 2002"
    locator: "pp. 189 to 201, the optimal k-partition problem, the bound of 2k - 1 on the group size, and the multivariate heuristics"
  - paper: "Anna Oganian and Josep Domingo-Ferrer, On the complexity of optimal microaggregation for statistical disclosure control, Statistical Journal of the United Nations Economic Commission for Europe 18(4), 2001"
    locator: "pp. 345 to 353, the proof that optimal multivariate microaggregation is NP-hard"
  - paper: "Stephen Lee Hansen and Sumitra Mukherjee, A polynomial algorithm for optimal univariate microaggregation, IEEE Transactions on Knowledge and Data Engineering 15(4), 2003"
    locator: "pp. 1043 to 1044, the reduction of optimal univariate microaggregation to a shortest path in a graph on the sorted values"
  - paper: doi:10.1007/s10618-005-0007-5
    title: "Josep Domingo-Ferrer and Vicenc Torra, Ordinal, continuous and heterogeneous k-anonymity through microaggregation, Data Mining and Knowledge Discovery 11(2), 2005"
    locator: "pp. 195 to 212, k-anonymity by joint microaggregation of the quasi-identifiers, the MDAV-generic heuristic, and the aggregation of ordinal and nominal values"
---

Microaggregation is a masking method for numerical microdata, the tables of one row per person or per firm that a statistical office releases. It puts the records into groups of at least $k$ similar records and replaces the values of each record by the mean of its group. If the values that a [quasi-identifier](/quasi-identifier/) uses are aggregated together, every released record has at least $k - 1$ others with the same values, so the release is [k-anonymous](/k-anonymity/). The cost is a loss of detail, which is measured by the within-group sum of squared errors. The best partition is NP-hard to find for more than one attribute, so in practice a heuristic such as [MDAV](/mdav/) builds it.

## In plain words

A survey office wants to publish the income and the age of each firm, but a very large firm is easy to recognize from its numbers. So the office makes small groups of firms that have close values, for example three firms in each group. In each group it writes the average income and the average age for every firm of the group. A reader now sees each value at least three times and cannot tell which firm of a group is which.

The averages of the whole table stay the same. The spread of the values goes down a little. Small groups of close records lose the least detail. The hard part is to choose the groups, because there are very many ways to cut a table into groups.

## When it applies

- The attributes to protect are numerical, or ordinal with a median, and the analyst cares about means, totals and regressions more than about single values.
- The release is a table of records, not a table of counts. For tables of counts and magnitudes see the [cell suppression problem](/cell-suppression-problem/) and [controlled tabular adjustment](/controlled-tabular-adjustment/).
- The goal is k-anonymity, or a lower risk of linkage with a smaller loss than [generalization and suppression](/generalization-and-suppression/) gives on numbers. Microaggregation keeps a numerical scale, while generalization turns a value into an interval.
- The protection is not differential privacy. The group means depend on each record, and the method gives no bound on what one record changes. See [differential privacy](/differential-privacy-definition/) for that guarantee.

## The template

Let $X$ be $n$ records with $d$ numerical attributes, and $k \ge 1$ the least group size. The value of $k$ is a policy choice. A *k-partition* of $X$ is a partition into groups of at least $k$ records. Its loss is the within-group sum of squared errors,

$$\mathrm{SSE} = \sum_{g} \sum_{x \in g} \lVert x - \bar{x}_g \rVert^2,$$

where $\bar{x}_g$ is the mean of group $g$. The usual relative measure is $\mathrm{SSE}/\mathrm{SST}$, where $\mathrm{SST}$ is the sum of squared distances to the mean of all of $X$.

```pseudo id=main
MICROAGGREGATE(X, k)
L1  X ← SCALE(X)                         ▷ hole: put the attributes on one scale, for example z-scores
L2  P ← PARTITION(X, k)                  ▷ hole: a k-partition with groups of k to 2k - 1 records
L3  for each group g of P do
L4      a ← AGGREGATE(g)                 ▷ hole: the mean; the median or the mode for ordinal or nominal values
L5      for each record x of g do
L6          replace the values of x by a  ▷ in the original units, not the scaled ones
L7  return X with the replaced values
```

The holes are SCALE, PARTITION and AGGREGATE. The choice of PARTITION decides the loss:

- **An optimal partition.** It minimizes the SSE. Domingo-Ferrer and Mateo-Sanz (2002) show that an optimal k-partition has groups of $k$ to $2k - 1$ records. The reason is a theorem on sums of squares: for a group $g$ split into $A$ and $B$, $\mathrm{SSE}(g) = \mathrm{SSE}(A) + \mathrm{SSE}(B) + \frac{|A||B|}{|g|} \lVert \bar{x}_A - \bar{x}_B \rVert^2$. The last term is at least 0, so a split never adds loss, and a group of $2k$ or more records can be split into two groups of at least $k$.
- **One attribute.** In an optimal partition of sorted values, each group is a run of consecutive values. So the optimum is a [shortest path](/shortest-path/) from node 0 to node $n$ in the graph with an arc from $i$ to $j$ for $k \le j - i \le 2k - 1$, weighted by the SSE of values $i + 1$ to $j$ (Hansen and Mukherjee 2003). The graph has $O(n k)$ arcs, and with prefix sums each weight takes $O(1)$ time.
- **Several attributes.** Optimal multivariate microaggregation is NP-hard (Oganian and Domingo-Ferrer 2001). The methods in use are heuristics: MDAV, variants of Ward's clustering with a least group size, and projections to one dimension followed by the univariate optimum. Their loss is a measured quantity on test data, not a proved bound.

**Example (one attribute).** Take the values 1, 2, 4, 9, 10, 12, 19, 20 and $k = 2$. Let $D_j$ be the least SSE of the first $j$ values. The arcs have length 2 or 3, and

| j | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| $D_j$ | 1/2 | 14/3 | 13 | 31/6 | 28/3 | 89/3 | 59/6 |

The path is $0 \to 3 \to 6 \to 8$, so the groups are $\{1, 2, 4\}$, $\{9, 10, 12\}$ and $\{19, 20\}$, with SSE $59/6 \approx 9.83$. The SST is $2927/8 \approx 365.9$, so the relative loss is about 2.7 percent. The released values are $7/3$ three times, $31/3$ three times and $39/2$ two times. The sum of the values, 77, does not change.

## Classic examples

- **[MDAV](/mdav/).** The standard multivariate heuristic. It builds groups of $k$ around the record farthest from the centroid and then around the record farthest from that one, in $O(n^2 d / k)$ distance work.
- **The univariate optimum.** The [shortest path](/shortest-path/) method above, used on one attribute or on the first [principal component](/principal-component-analysis/) of several.
- **Ward's method with a least group size.** Domingo-Ferrer and Mateo-Sanz (2002) adapt [Ward's hierarchical clustering](/ward-method/), which merges the two clusters with the least growth of SSE, to groups of at least $k$.
- **Individual ranking.** Each attribute is microaggregated alone with the univariate method. The loss is low, but the result is not k-anonymous (see Pitfalls).
- **[k-means](/k-means/) is a near relative.** It minimizes the same SSE for a fixed number of clusters, with no least size, so its clusters can hold one record and give no protection.

## Variations

- **Fixed and variable group size.** Fixed-size heuristics such as MDAV make groups of exactly $k$, except one group. Variable-size heuristics let a group grow up to $2k - 1$ when the data has a natural cluster of that size, and often have a lower SSE.
- **Ordinal and nominal data.** Domingo-Ferrer and Torra (2005) aggregate an ordinal attribute by the median and a nominal attribute by the mode, with a distance for each type.
- **Joint and partial microaggregation.** For k-anonymity, all quasi-identifiers are aggregated together. Attributes outside the quasi-identifier are left as they are, so the analyst keeps their full detail.
- **Microaggregation for t-closeness.** The partition can also bound the distance between the sensitive values of a group and those of the whole table, as in [t-closeness](/t-closeness/). This needs larger groups.

## Pitfalls

- **Individual ranking is not k-anonymous.** Take the records (1, 1), (2, 3), (3, 2), (4, 4) and $k = 2$. The first attribute gives the groups of records $\{1, 2\}$ and $\{3, 4\}$, the second gives $\{1, 3\}$ and $\{2, 4\}$. The released records are (1.5, 1.5), (1.5, 3.5), (3.5, 1.5) and (3.5, 3.5): each one is unique.
- **No scaling at line L1.** With income in euros and age in years, the distance is almost only income. Groups are then close in income and far apart in age, and the loss of age is large.
- **Attribute disclosure.** If all records of a group have about the same sensitive value, a reader who knows that a person is in the group learns the value. The group sizes say nothing about this. See [l-diversity](/l-diversity/) and [t-closeness](/t-closeness/).
- **The variance goes down.** The masked data has the between-group variance only: the total sum of squares falls by the SSE. Estimates of variances and of correlations are biased toward 0 unless the analyst corrects them.
- **An outlier in the last group.** A heuristic that fills groups in turn can put a far record in the last group with records far from it. Its value then moves far, and the SSE grows. The MDAV page has an example.
- **Groups larger than 2k - 1 at line L2.** They are never needed. By the split identity above, such a group can be cut in two with no more loss.

## Exercises

1. Prove the split identity of the template: for a set $g = A \cup B$ with $A \cap B = \emptyset$, $\mathrm{SSE}(g) = \mathrm{SSE}(A) + \mathrm{SSE}(B) + \frac{|A||B|}{|g|} \lVert \bar{x}_A - \bar{x}_B \rVert^2$.
2. Show that for one attribute, some optimal k-partition has groups that are runs of consecutive sorted values. Hint: if $a < b < c$ with $a$ and $c$ in one group and $b$ in another, swap $b$ with $a$ or with $c$.
3. Compute the optimal 3-partition of 1, 2, 4, 9, 10, 12, 19, 20 by the shortest path method. With 8 values, only the group sizes 3 and 5, 4 and 4, or 5 and 3 are possible. Compare the loss with that of the 2-partition.
4. Find a table of 4 records with 2 attributes where individual ranking with $k = 2$ gives a 2-anonymous release, and one where it does not.

## References
