---
tag: JK6NEV
kind: algorithm
slug: datafly
name: Datafly
aliases:
- Datafly algorithm
area: security-and-privacy/data-anonymization
level: core
summary: Greedily generalizes the quasi-identifier attribute with the most distinct values until few records violate k-anonymity, then suppresses those.
model: word-ram
complexity:
  vars: {n: the number of rows, d: the number of quasi-identifier attributes, h: the sum of the hierarchy heights}
  time: {worst: O(h n d)}
  space: {extra: O(n d)}
history:
  year: 1997
  people: [Latanya Sweeney]
  note: "Sweeney described the Datafly system for medical data in 1997, and gave the core Datafly algorithm with its analysis in 2002."
prereqs: [generalization-and-suppression, greedy-algorithm]
see_also: [samarati-algorithm, incognito, mondrian-anonymization, k-anonymity, quasi-identifier, k-anonymity-approximation]
sources:
  - url: "https://pubmed.ncbi.nlm.nih.gov/9357587/"
    title: "Latanya Sweeney, Guaranteeing anonymity when sharing medical data, the Datafly system, Proceedings of the AMIA Annual Fall Symposium, 1997"
    locator: "pp. 51 to 55, the Datafly system and its generalization of the attributes with the most distinct values"
  - paper: doi:10.1142/S021848850200165X
    title: "Latanya Sweeney, Achieving k-anonymity privacy protection using generalization and suppression, International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems 10(5), 2002"
    locator: "pp. 571 to 588, Figure 8, the core Datafly algorithm, and the discussion of why its result need not be minimal"
  - url: "https://spdp.di.unimi.it/papers/k-Anonymity.pdf"
    title: "Valentina Ciriani, Sabrina De Capitani di Vimercati, Sara Foresti and Pierangela Samarati, k-Anonymity, in Secure Data Management in Decentralized Systems, Springer, Advances in Information Security, 2007"
    locator: "Section 4, the summary of the greedy algorithm of Sweeney among the algorithms for k-anonymity"
  - paper: doi:10.1145/1066157.1066164
    title: "Kristen LeFevre, David J. DeWitt and Raghu Ramakrishnan, Incognito, efficient full-domain k-anonymity, Proceedings of ACM SIGMOD 2005"
    locator: "pp. 49 to 60, the discussion of greedy full-domain algorithms that do not find a minimal generalization"
---

Datafly is the greedy algorithm of Sweeney for [k-anonymity](/k-anonymity/) by full-domain [generalization and suppression](/generalization-and-suppression/). It starts from the raw table. While more than $k$ rows are in classes of fewer than $k$ rows, it raises by one level the [quasi-identifier](/quasi-identifier/) attribute that has the most distinct values. Then it suppresses the rows that are still in small classes. The release is always k-anonymous, and the algorithm is fast, but the result is not always a minimal generalization: it is a [greedy](/greedy-algorithm/) heuristic for the choice of the levels.

## In plain words

The attribute with the most different values is the one that makes rows look different from each other, such as a full date of birth. So coarsen it first: write the date as year and month. Look again at the table. If many rows are still alone or in very small groups, coarsen the attribute that now has the most different values. Stop when only a few rows, at most $k$, are still in small groups. Delete those rows and release the rest.

Each step is a good local move, but it does not look ahead. It can coarsen an attribute that did not need it.

## The problem

The input is a table $T$ of $n$ rows with $d$ quasi-identifier attributes, a tree hierarchy for each attribute $a$ with levels $0, \ldots, h_a$, where level $h_a$ maps all values to one value, and an integer $k \ge 1$. The output is a vector $v$ with $0 \le v_a \le h_a$ and a set $s$ of at most $k$ rows such that $T$ generalized by $v$, without the rows of $s$, is k-anonymous. Let $h = \sum_a h_a$. The value of $k$ is a policy choice.

## The algorithm

```pseudo id=main
DATAFLY(T, H, k)
L1  v ← (0, ..., 0)
L2  loop
L3      T' ← T generalized by v
L4      s ← the rows of T' whose tuple occurs fewer than k times in T'
L5      if |s| ≤ k then exit the loop
L6      a ← the attribute with the most distinct values in T', ties to the lowest index
L7      v_a ← v_a + 1
L8  return (v, s)
```

The release is $T'$ without the rows of $s$, in a random order. Line L4 counts the tuples with a hash table.

Sweeney's Figure 8 has a further step. Her version replaces the values of the suppressed rows by stars and keeps the rows, so these rows form a class of their own, and a last step makes that class k-anonymous too. The version here removes the suppressed rows, so that step is not needed. The stop test of line L5 bounds the number of removed rows by $k$.

## Example

Take the 9 rows of Ciriani et al. (2007), with race, date of birth (yy/mm/dd), sex and ZIP:

| row | race | birth | sex | ZIP |
|---|---|---|---|---|
| 1 | asian | 64/04/12 | F | 94142 |
| 2 | asian | 64/09/13 | F | 94141 |
| 3 | asian | 64/04/15 | F | 94139 |
| 4 | asian | 63/03/13 | M | 94139 |
| 5 | asian | 63/03/18 | M | 94139 |
| 6 | black | 64/09/27 | F | 94138 |
| 7 | black | 64/09/27 | F | 94139 |
| 8 | white | 64/09/27 | F | 94139 |
| 9 | white | 64/09/27 | F | 94141 |

The hierarchies are: race to person; birth to yy/mm, to yy, to \*; sex to \*; ZIP to 4 digits and a star, to 3 digits, to \*. Let $k = 2$.

| v (race, birth, sex, ZIP) | distinct values | rows in small classes | action |
|---|---|---|---|
| (0, 0, 0, 0) | 3, 6, 2, 4 | 9 | raise birth |
| (0, 1, 0, 0) | 3, 3, 2, 4 | 7 | raise ZIP |
| (0, 1, 0, 1) | 3, 3, 2, 2 | 5 | raise race (tie with birth, lower index) |
| (1, 1, 0, 1) | 1, 3, 2, 2 | 2 | stop, suppress rows 1 and 3 |

The release has the classes $\{2, 9\}$ = (person, 64/09, F, 9414\*), $\{4, 5\}$ = (person, 63/03, M, 9413\*) and $\{6, 7, 8\}$ = (person, 64/09, F, 9413\*). With $k = 3$ the run goes on to (1, 2, 0, 1) and suppresses rows 4 and 5.

The vector (0, 1, 0, 2), of the same height 3, keeps the race and leaves only 1 row to suppress. Datafly does not find it, because at the third step it raised race and not ZIP.

## Correctness

If the loop goes on, some attribute has at least 2 distinct values in $T'$. Otherwise all rows of $T'$ are equal, and $|s|$ is 0 (when $n \ge k$) or $n < k$, so line L5 stops. Line L6 then picks an attribute with at least 2 values, which is not at its top level, because the top level has one value. So line L7 keeps $v_a \le h_a$, and the height grows by one in each round. The loop stops after at most $h + 1$ rounds. At the stop, each row outside $s$ is in a class of at least $k$ rows of $T'$, and all rows of that class are outside $s$, so the release is k-anonymous. The full proof is in proofs/correctness.md.

## Complexity

Let $n$ be the number of rows, $d$ the number of attributes and $h$ the sum of the hierarchy heights. The model is the [word RAM](/word-ram/) with hashing.

- One round generalizes the $n$ rows (line L3), counts the tuples (line L4) and counts the distinct values per attribute (line L6): $O(n d)$ expected time.
- There are at most $h + 1$ rounds, so the time is $O(h n d)$ expected, and the space is $O(n d)$.

This is much less than the $O(n d g \log h)$ of [Samarati's algorithm](/samarati-algorithm/), where $g$ is the size of the lattice, because Datafly follows one path up the lattice.

## Properties

- **Always k-anonymous.** This is a theorem, for each input.
- **Not minimal.** The result is a heuristic choice. Sweeney (2002) says that Datafly can generalize more than needed. A small case: attribute A with values 0 to 3 and levels (value, value div 2, \*), attribute B with values 0 to 2 and levels (value, \*), and the rows (3, 0), (2, 2), (1, 0), (2, 1), (0, 0), (0, 0) with $k = 2$. Datafly returns (1, 1). The lower vector (0, 1) leaves only rows 1 and 3 to suppress, which is at most $k$.
- **At most k suppressed rows.** The limit on suppression is tied to $k$ and is not a separate parameter, as MaxSup is in Samarati's algorithm.
- **Deterministic**, with the tie rule of line L6.

## Variants and improvements

- **The Datafly system.** Sweeney (1997) describes a whole system for the release of medical records, with more inputs and choices than the core algorithm. The core algorithm here is the part that Sweeney (2002) analyzes.
- **Other greedy rules.** Choose the attribute that most reduces the number of rows in small classes, or that loses the least precision per step. These are also heuristics.
- **Exact searches.** [Samarati's algorithm](/samarati-algorithm/) finds a vector of least height, and [Incognito](/incognito/) finds all k-anonymous vectors.
- **Multidimensional cuts.** [Mondrian](/mondrian-anonymization/) is also greedy, but it cuts boxes of the value space and loses less detail on numeric data.

## When to use it

Use Datafly when the lattice is too large to search, a fast and always k-anonymous answer is enough, and some extra generalization is acceptable. It is also a good baseline for the exact algorithms. If the least generalization matters, use Samarati's algorithm or Incognito on the same hierarchies.

## Pitfalls

- **A table with at most k rows.** If $n \le k$, then $|s| \le n \le k$ at once, and line L5 stops at the raw table with every row in $s$. Nothing is released. Check $n > k$ first.
- **Distinct values of the raw table in line L6.** The counts must come from the current table $T'$. With the counts of the raw table, the same attribute stays the largest, and line L7 raises it to its top before it looks at any other.
- **Keeping the suppressed rows with stars in line L8.** If the rows of $s$ are released with all quasi-identifier values replaced by stars, they form one class of $|s|$ rows, and $|s|$ can be less than $k$. Remove them, or add the last step of Sweeney's Figure 8.
- **A top level with more than one value.** Then line L7 can push $v_a$ past $h_a$. Each hierarchy must end in a single value.

## Implementations

## History

Sweeney built the Datafly system for the release of medical records and described it at the AMIA symposium in 1997. In 2002 she gave the core Datafly algorithm, together with the exact but slow MinGen, and showed that Datafly can generalize more than a minimal generalization. Later work, such as Incognito (2005), compared exact full-domain search with such greedy methods.

## References
