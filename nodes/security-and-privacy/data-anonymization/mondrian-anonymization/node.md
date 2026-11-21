---
tag: EV1MMH
kind: algorithm
slug: mondrian-anonymization
name: Mondrian multidimensional k-anonymity
aliases:
- Mondrian
area: security-and-privacy/data-anonymization
level: core
summary: "Splits the quasi-identifier space recursively, as in a kd-tree, at the most balanced cut of one attribute that leaves at least k records on each side."
model: word-ram
complexity:
  vars: {n: the number of rows, d: the number of quasi-identifier attributes, k: the least size of a region}
  time: {worst: O(d n^2 log n)}
  space: {extra: O(n d)}
history:
  year: 2006
  people: [Kristen LeFevre, David J. DeWitt, Raghu Ramakrishnan]
  note: "LeFevre, DeWitt and Ramakrishnan gave multidimensional recoding for k-anonymity and the greedy Mondrian partitioning at ICDE 2006."
prereqs: [k-anonymity, kd-tree, median-finding]
see_also: [generalization-and-suppression, incognito, samarati-algorithm, datafly, microaggregation, kd-tree, l-diversity, k-anonymity-np-hardness]
sources:
  - paper: doi:10.1109/ICDE.2006.101
    title: "Kristen LeFevre, David J. DeWitt and Raghu Ramakrishnan, Mondrian multidimensional k-anonymity, Proceedings of the 22nd International Conference on Data Engineering (ICDE 2006)"
    locator: "p. 25, strict and relaxed multidimensional partitioning, the NP-hardness of optimal strict partitioning, the bound 2d(k-1)+m on the size of a region, and the greedy median partitioning"
  - paper: doi:10.1145/1066157.1066164
    title: "Kristen LeFevre, David J. DeWitt and Raghu Ramakrishnan, Incognito, efficient full-domain k-anonymity, Proceedings of ACM SIGMOD 2005"
    locator: "pp. 49 to 60, full-domain generalization, which Mondrian is compared with"
  - paper: doi:10.1109/ICDE.2005.42
    title: Roberto J. Bayardo and Rakesh Agrawal, Data privacy through optimal k-anonymization, Proceedings of the 21st International Conference on Data Engineering (ICDE 2005)
    locator: "pp. 217 to 228, the discernibility metric used to compare releases"
  - paper: doi:10.1145/1749603.1749605
    title: "Benjamin C. M. Fung, Ke Wang, Rui Chen and Philip S. Yu, Privacy-preserving data publishing, a survey of recent developments, ACM Computing Surveys 42(4), 2010"
    locator: the section on multidimensional generalization
---

Mondrian makes a table [k-anonymous](/k-anonymity/) by cutting the space of [quasi-identifier](/quasi-identifier/) values into boxes. It starts with one box that holds all rows. It cuts a box in two along one attribute, at a value that leaves at least $k$ rows on each side, and it goes on with both halves until no box has such a cut. Each box is released with the range of each attribute over its rows. This is multidimensional recoding: the same age can go to different ranges for different ZIP codes, so Mondrian usually loses less detail than full-domain [generalization](/generalization-and-suppression/). The cuts are those of a [kd-tree](/kd-tree/) that stops at $k$ rows.

## In plain words

Put each row as a point on a map: age on one axis, ZIP code on the other. Draw a line across the map so that each side has at least $k$ points, and as close to half of them as you can. Pick the axis on which the points of the box are spread most widely, compared with the whole map. Then do the same inside each half, and again, until no line can be drawn that keeps at least $k$ points on each side.

Each final box has at least $k$ points. Release each point as the box it is in, written as a range of ages and a range of ZIP codes.

## The problem

The input is a table $T$ of $n$ rows with $d$ quasi-identifier attributes, each with integer values (or any total order), and an integer $k$ with $1 \le k \le n$. A *cut* of a set $P$ of rows on attribute $a$ at the value $x$ splits $P$ into $\{t \in P : t.a \le x\}$ and $\{t \in P : t.a > x\}$. The cut is *allowable* when both sides have at least $k$ rows. The output is a partition of the rows into regions of at least $k$ rows, none of which has an allowable cut. LeFevre et al. (2006) call this a strict multidimensional partitioning. The value of $k$ is a policy choice.

## The algorithm

```pseudo id=main
MONDRIAN(T, k)
L1  result ← an empty list; stack ← [all rows of T]
L2  while stack is not empty do
L3      P ← pop(stack)
L4      for each attribute a, in decreasing order of the range of a in P divided by its range in T do
L5          x ← the allowable cut on a that maximizes min(|{t ∈ P : t.a ≤ x}|, |{t ∈ P : t.a > x}|), ties to the smaller x; NIL if none
L6          if x ≠ NIL then
L7              push {t ∈ P : t.a > x} and {t ∈ P : t.a ≤ x}; continue at L2
L8      append P to result
L9  return result
```

Ties in line L4 go to the attribute of lower index. Line L5 sorts the values of $a$ in $P$ and tests the cut at each place where two neighbors differ. When the values are distinct, the best cut is at the median, as in the paper. An explicit stack replaces the recursion, because the depth can reach $n/k$.

The release replaces the quasi-identifier values of each row by the box of its region: the pair (least, greatest) of each attribute over the rows of the region.

## Example

Take 10 rows of (age, ZIP): 1 (25, 53711), 2 (25, 53712), 3 (26, 53711), 4 (27, 53710), 5 (29, 53712), 6 (61, 53706), 7 (62, 53706), 8 (63, 53710), 9 (64, 53712), 10 (64, 53711). The full ranges are 39 for age and 6 for ZIP. Let $k = 2$.

| region | normalized ranges (age, ZIP) | cut | parts |
|---|---|---|---|
| 1 to 10 | 1, 1 | age at 29 (5 and 5) | {1..5}, {6..10} |
| {1, 2, 3, 4, 5} | 4/39, 2/6 | ZIP at 53711 (3 and 2) | {1, 3, 4}, {2, 5} |
| {1, 3, 4} | 2/39, 1/6 | none | final |
| {2, 5} | 4/39, 0 | none | final |
| {6, 7, 8, 9, 10} | 3/39, 6/6 | ZIP at 53706 (2 and 3) | {6, 7}, {8, 9, 10} |
| {6, 7} | 1/39, 0 | none | final |
| {8, 9, 10} | 1/39, 2/6 | none | final |

In the first row the two ranges tie, so age goes first. In the fifth row the cuts at 53706 and at 53710 both give a balance of 2, and the smaller value wins. The release is:

| region | age | ZIP |
|---|---|---|
| {1, 3, 4} | 25 to 27 | 53710 to 53711 |
| {2, 5} | 25 to 29 | 53712 |
| {6, 7} | 61 to 62 | 53706 |
| {8, 9, 10} | 63 to 64 | 53710 to 53712 |

The age range 25 to 27 in one region and 25 to 29 in another overlap. Full-domain generalization cannot do that, and it would need wider ranges for the same $k$. With $k = 3$ only the first cut is made, and the regions are rows 1 to 5 and rows 6 to 10.

## Correctness

The invariant of the loop of line L2 is that the sets in the stack and in the result partition the rows, each has at least $k$ rows, and each set in the result has no allowable cut. Line L5 tests every distinct value, so it finds an allowable cut if one exists. Line L7 pushes two nonempty sets of at least $k$ rows, so the loop stops after at most $n - 1$ cuts.

The size of a region is bounded. Let $m$ be the largest number of equal rows of $T$. **Theorem (LeFevre et al. 2006).** A region with no allowable cut has at most $2d(k - 1) + m$ rows. On each attribute, at most $k - 1$ rows are below the median value and at most $k - 1$ are above it, or one of the two cuts next to the median is allowable. So at most $2d(k - 1)$ rows differ from the point of medians on some attribute, and the rest are copies of one point. The full proofs are in proofs/correctness.md.

## Complexity

Let $n$ be the number of rows and $d$ the number of attributes. The model is the [word RAM](/word-ram/), with values that fit in a word.

- Lines L4 and L5 sort the $r$ rows of a region on up to $d$ attributes: $O(d r \log r)$ time.
- If each cut is near the median, as with distinct values, the depth is $O(\log n)$, the regions of one depth have $n$ rows in total, and the time is $O(d n \log^2 n)$. With a linear [median-finding](/median-finding/) step in place of the sort, it is $O(d n \log n)$, which is the bound the paper gives.
- With many equal values, an allowable cut can leave only $k$ rows on one side. Then the depth can be $n / k$, and the time is $O(d n^2 \log n)$ in the worst case.
- The space is $O(n d)$ for the table and the stack.

## Properties

- **k-anonymous.** Each region has at least $k$ rows, and all its rows get the same box. This is a theorem for every input.
- **A bound on the quality.** By the theorem, each region has at most $2d(k - 1) + m$ rows. So the discernibility cost $\sum |R|^2$ of the result is at most $n (2d(k - 1) + m)$. Each k-anonymous partition costs at least $n k$, so the greedy result is within a factor $2d + m/k$ of the least cost for this measure.
- **Not optimal.** LeFevre et al. (2006) show that finding an optimal strict multidimensional partitioning is NP-hard. The greedy rule of line L4 is a heuristic.
- **Deterministic**, with the tie rules of lines L4 and L5.

## Variants and improvements

- **Relaxed partitioning.** The regions may overlap, and the rows with one value may go to different regions. This allows cuts in the middle of a run of equal values, and the bound on region size becomes about $2d(k - 1) + 1$.
- **Categorical attributes.** Cut along the hierarchy of the attribute: a region of the value "person" splits into its children, if each child keeps at least $k$ rows.
- **Other tests.** Replace "at least $k$ rows" in line L5 by a test on the sensitive values, such as [l-diversity](/l-diversity/), as long as the test holds for a union of regions that pass it.
- **Other choices of the attribute.** Choose the attribute by a workload of queries, or by the loss of a later model, in place of the widest range.
- **Clustering.** [Microaggregation](/microaggregation/) also groups at least $k$ rows, but it releases the mean of each group, not its box.

## When to use it

Use Mondrian for numeric or ordered quasi-identifiers with many values, such as age and ZIP code, when the users can work with ranges that differ from row to row. It is fast, simple and usually keeps more detail than full-domain methods. If each column must use one level of detail, for example because analysts expect a uniform coding, use [Samarati's algorithm](/samarati-algorithm/) or [Incognito](/incognito/).

## Pitfalls

- **The median value as the cut in line L5.** With repeated values, the cut at the median value can leave an empty side, while another cut is allowable. Take the values 1, 1, 1, 2, 2, 2, 2, 2 with $k = 3$. The median value is 2, and the cut "at most 2" leaves no row on the right, so a rule that tries only the median stops here. The cut at 1 gives 3 and 5 rows and is allowable. Test every distinct value, or the size bound of the theorem fails.
- **Testing only one side in line L5.** A cut with at least $k$ rows on the left but fewer on the right produces a region of fewer than $k$ rows. Check both sides.
- **Recursion in line L7.** With many equal values the depth can be $n / k$. A recursive version can run out of stack; use an explicit stack.
- **Raw ranges in line L4.** Without the division by the range in $T$, an attribute with large numbers, such as a ZIP code, is always cut first. This is not wrong, but the regions get narrow in one attribute and wide in the others.

## Implementations

## History

LeFevre, DeWitt and Ramakrishnan proposed multidimensional recoding for k-anonymity at ICDE 2006, the year after their full-domain algorithm Incognito. They showed that optimal strict multidimensional partitioning is NP-hard, proved the bound on the size of the regions of a greedy partition, and gave the greedy median algorithm, which they named after the painter Piet Mondrian for the look of its rectangles.

## References
