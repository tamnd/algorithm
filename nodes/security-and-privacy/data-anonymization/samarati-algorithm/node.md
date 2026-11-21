---
tag: FM4D27
kind: algorithm
slug: samarati-algorithm
name: Samarati's algorithm
aliases:
- binary search over the generalization lattice
area: security-and-privacy/data-anonymization
level: core
summary: Binary searches the heights of the full-domain generalization lattice for the lowest height with a k-anonymous node within a suppression limit.
model: word-ram
complexity:
  vars: {n: the number of rows, d: the number of quasi-identifier attributes, g: the number of vectors of the lattice, h: the height of the top vector}
  time: {worst: O(n d g log h)}
  space: {extra: O(n d + g d)}
history:
  year: 2001
  people: [Pierangela Samarati]
  note: "Samarati defined minimal generalization over the lattice of generalization vectors and gave the binary search on the height in IEEE TKDE in 2001, after a 1998 report with Sweeney."
prereqs: [generalization-and-suppression, binary-search]
see_also: [datafly, incognito, mondrian-anonymization, k-anonymity, k-anonymity-np-hardness, join-semilattice]
sources:
  - paper: doi:10.1109/69.971193
    title: "Pierangela Samarati, Protecting respondents' identities in microdata release, IEEE Transactions on Knowledge and Data Engineering 13(6), 2001"
    locator: "pp. 1010 to 1027, generalization hierarchies, the lattice of distance vectors, k-minimal generalization with suppression, and the binary search on the height"
  - url: "https://spdp.di.unimi.it/papers/k-Anonymity.pdf"
    title: "Valentina Ciriani, Sabrina De Capitani di Vimercati, Sara Foresti and Pierangela Samarati, k-Anonymity, in Secure Data Management in Decentralized Systems, Springer, Advances in Information Security, 2007"
    locator: "Section 4.1, the algorithm of Samarati, with the race and ZIP example and its two 2-minimal generalizations"
  - paper: doi:10.1142/S021848850200165X
    title: "Latanya Sweeney, Achieving k-anonymity privacy protection using generalization and suppression, International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems 10(5), 2002"
    locator: "pp. 571 to 588, minimal generalization and the comparison with Datafly"
  - paper: doi:10.1145/1066157.1066164
    title: "Kristen LeFevre, David J. DeWitt and Raghu Ramakrishnan, Incognito, efficient full-domain k-anonymity, Proceedings of ACM SIGMOD 2005"
    locator: "pp. 49 to 60, the comparison with the binary search of Samarati in the experiments"
---

Samarati's algorithm finds a full-domain generalization of a table that is [k-anonymous](/k-anonymity/) after the removal of at most MaxSup rows, and that generalizes as little as possible. It searches the lattice of generalization vectors, where the height of a vector is the total number of generalization steps. The number of removed rows can only fall when a vector goes up, so the algorithm does a [binary search](/binary-search/) on the height. The result has the least height, and no vector strictly below it works, so it is a k-minimal generalization in the sense of Samarati (2001).

## In plain words

Each quasi-identifier attribute can be written at several levels of detail, from the raw value to a single star. Choose a level for each attribute, and add up the levels: that is the height of the choice. A low height keeps much detail. At each height there are several choices. Test them: a choice works if, after the table is coarsened, at most MaxSup rows are in groups of fewer than $k$ equal rows. Those rows are deleted.

If some choice works at a height, then some choice works at each greater height, because coarser values only make groups bigger. So the heights split into a low part where nothing works and a high part where something works. Binary search finds the boundary. Then return the first working choice at that height.

## The problem

The input is a table $T$ of $n$ rows with $d$ quasi-identifier attributes, a tree hierarchy for each attribute $a$ with levels $0, \ldots, h_a$ (see [generalization and suppression](/generalization-and-suppression/)), an integer $k \ge 1$ and a limit MaxSup $\ge 0$. A vector $v$ with $0 \le v_a \le h_a$ *satisfies* if, in $T$ generalized by $v$, at most MaxSup rows are in classes of fewer than $k$ rows. The output is a satisfying vector of least height $|v| = \sum_a v_a$, or NIL if no vector satisfies. The top vector is $\top = (h_1, \ldots, h_d)$ with height $h$, and the lattice has $g = \prod_a (h_a + 1)$ vectors. $k$ and MaxSup are policy choices.

## The algorithm

```pseudo id=main
SAMARATI(T, H, k, MaxSup)
L1  if not SATISFIES(T, top, k, MaxSup) then return NIL
L2  low ← 0, high ← height(top)
L3  sol ← top
L4  while low < high do
L5      try ← ⌊(low + high) / 2⌋
L6      found ← NIL
L7      for each vector v with height(v) = try, in lexicographic order do
L8          if SATISFIES(T, v, k, MaxSup) then found ← v; exit the loop
L9      if found ≠ NIL then sol ← found, high ← try
L10     else low ← try + 1
L11 return sol

SATISFIES(T, v, k, MaxSup)
L12 count the rows of each tuple of T generalized by v, in a hash table
L13 s ← the number of rows whose tuple has a count < k
L14 return s ≤ MaxSup
```

Line L1 tests the top vector first. If even the top fails, no vector can satisfy. Lines L4 to L10 keep the least satisfying height in $[low, high]$, and sol is always a satisfying vector at height $high$. The release is the table generalized by sol without the $s$ rows of line L13.

Samarati (2001) adds a matrix of distance vectors between the tuples of $T$, which lets the test skip vectors that cannot work. It is an optimization and does not change the answer.

## Example

Take the 9 rows of Ciriani et al. (2007): asian 94142, asian 94141, three rows of asian 94139, black 94138, black 94139, white 94139 and white 94141. Race has levels R0 and R1 (person), and ZIP has levels Z0 (5 digits), Z1 (9414\* or 9413\*) and Z2 (941\*\*), so $h = 3$. Let $k = 2$ and MaxSup = 2.

| step | low | high | try | vectors tested at try | rows to suppress | sol |
|---|---|---|---|---|---|---|
| L1 | | | | (1, 2) | 0 | |
| start | 0 | 3 | | | | (1, 2) |
| 1 | 0 | 3 | 1 | (0, 1) | 2: white 9413\*, white 9414\* | (0, 1) |
| 2 | 0 | 1 | 0 | (0, 0) | 6 | (0, 1) |
| end | 1 | 1 | | | | (0, 1) |

The result is (0, 1): keep the race and cut the ZIP to 4 digits, and suppress the two white rows. The vector (1, 0) also has height 1 and suppresses 2 rows, so it is also 2-minimal. The algorithm returns (0, 1) only because it comes first in lexicographic order. With MaxSup = 0, the answer is (0, 2), and with MaxSup = 9 it is (0, 0).

## Correctness

The proof rests on monotonicity. With tree hierarchies, if $v \le w$ then each class of $T$ at $w$ is a union of classes at $v$, so a row that is not suppressed at $v$ is not suppressed at $w$. So if a vector of height $t < h$ satisfies, raising one of its levels gives a satisfying vector of height $t + 1$. The predicate "some vector of height $t$ satisfies" is false below the least height $t^*$ and true from $t^*$ to $h$. The loop of line L4 keeps the invariant $low \le t^* \le high$, with sol the first satisfying vector at height $high$. Each step halves the range, and at the end $low = high = t^*$. No satisfying vector lies strictly below sol, because it would have a smaller height. The full proof is in proofs/correctness.md.

## Complexity

Let $n$ be the number of rows, $d$ the number of attributes, $g$ the number of vectors and $h$ the height of the top vector. The model is the [word RAM](/word-ram/), with expected $O(1)$ time per hash table operation.

- One call of SATISFIES generalizes $n$ rows of $d$ values and counts them: $O(n d)$ expected time.
- The loop of line L4 runs at most $\lceil \lg(h + 1) \rceil$ times. Each round tests at most the number of vectors of one height, which is less than $g$.
- In total, $O(n d g \log h)$ expected time in the worst case. The space is $O(n d)$ for the generalized table and $O(g d)$ for the list of vectors of one height.

In practice $g$ is the main factor. For 4 attributes with hierarchies of heights 2, 3, 3 and 4, $g = 3 \cdot 4 \cdot 4 \cdot 5 = 240$, but each round tests only the vectors of one height. Finding a vector with the fewest suppressed columns, in place of the least height, is NP-hard for $k \ge 3$ even with hierarchies of two levels, the value and a star ([NP-hardness of optimal k-anonymity](/k-anonymity-np-hardness/)).

## Properties

- **Least height, k-minimal.** The result has the least height among the satisfying vectors, and no satisfying vector is strictly below it. It need not be the vector of least loss for other measures, such as precision or discernibility.
- **Deterministic.** The order of line L7 fixes the result among the vectors of the least height.
- **One level per attribute.** Each value of an attribute is generalized to the same level, which keeps the columns uniform for analysis.
- **Tuple suppression.** Whole rows are removed, up to MaxSup. A larger MaxSup gives a lower vector.

## Variants and improvements

- **Preference criteria.** Ciriani et al. (2007) list rules for the choice among several k-minimal vectors: the least absolute distance (height), the least relative distance, the largest distribution of the values, and the least suppression.
- **All minimal vectors.** [Incognito](/incognito/) finds every k-anonymous vector with a bottom-up search and a priori pruning, and was faster than the binary search in the experiments of LeFevre et al. (2005).
- **Greedy search.** [Datafly](/datafly/) raises one attribute at a time and may stop above the least height.
- **Multidimensional generalization.** [Mondrian](/mondrian-anonymization/) gives boxes of values instead of one level per attribute, and loses less detail.

## When to use it

Use it when the release must use one level of detail per attribute, the hierarchies are given, and the lattice is small enough to enumerate the vectors of a height. It gives a provable answer to "the least total generalization". If all minimal vectors are needed, to choose by another measure, use Incognito. If the quasi-identifier is numeric and many-valued, Mondrian usually keeps more detail.

## Pitfalls

- **A ceiling in line L5.** With $try = \lceil (low + high)/2 \rceil$, the case $high = low + 1$ gives $try = high$, and if it is found, line L9 sets $high$ to the same value. The loop never ends. Use the floor.
- **Skipping line L1.** Without it, sol starts at the top vector and is returned when nothing satisfies, so the caller gets a vector that is not k-anonymous within MaxSup.
- **Counting classes in line L13.** MaxSup bounds the number of rows removed, not the number of classes. Counting the classes of fewer than $k$ rows removes too many rows.
- **A hierarchy that is not a tree.** Then monotonicity fails, and lines L9 and L10 can discard the part of the range that holds the answer.

## Implementations

## History

Samarati and Sweeney described k-anonymity with generalization and suppression in a 1998 report. Samarati (2001) gave the formal model: domain generalization hierarchies, the lattice of distance vectors, the minimal generalization with a suppression threshold, and the binary search on the height. Sweeney (2002) gave the precision measure and the greedy Datafly. LeFevre, DeWitt and Ramakrishnan (2005) used the binary search as a baseline for Incognito.

## References
