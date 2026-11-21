---
tag: NJPQYV
kind: technique
slug: generalization-and-suppression
name: Generalization and suppression
aliases:
- value generalization hierarchy
area: security-and-privacy/data-anonymization
level: intro
summary: "Coarsens quasi-identifier values along a hierarchy, such as zip 02139 to 021**, and deletes outlier records, until a privacy model holds."
prereqs: [k-anonymity]
see_also: [samarati-algorithm, datafly, incognito, mondrian-anonymization, k-anonymity-approximation, microaggregation, l-diversity, cell-suppression-problem]
sources:
  - paper: doi:10.1109/69.971193
    title: "Pierangela Samarati, Protecting respondents' identities in microdata release, IEEE Transactions on Knowledge and Data Engineering 13(6), 2001"
    locator: "pp. 1010 to 1027, domain generalization hierarchies, the lattice of generalization vectors, tuple suppression and minimal generalization"
  - paper: doi:10.1142/S021848850200165X
    title: "Latanya Sweeney, Achieving k-anonymity privacy protection using generalization and suppression, International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems 10(5), 2002"
    locator: "pp. 571 to 588, generalization and suppression, the precision metric, and the algorithms MinGen and Datafly"
  - url: "https://spdp.di.unimi.it/papers/k-Anonymity.pdf"
    title: "Valentina Ciriani, Sabrina De Capitani di Vimercati, Sara Foresti and Pierangela Samarati, k-Anonymity, in Secure Data Management in Decentralized Systems, Springer, Advances in Information Security, 2007"
    locator: "Section 3, the taxonomy of generalization and suppression by the level at which each is applied"
  - paper: doi:10.1109/ICDE.2005.42
    title: Roberto J. Bayardo and Rakesh Agrawal, Data privacy through optimal k-anonymization, Proceedings of the 21st International Conference on Data Engineering (ICDE 2005)
    locator: "pp. 217 to 228, the discernibility metric and the search for an optimal k-anonymization over a set-enumeration tree"
  - paper: doi:10.1145/1749603.1749605
    title: "Benjamin C. M. Fung, Ke Wang, Rui Chen and Philip S. Yu, Privacy-preserving data publishing, a survey of recent developments, ACM Computing Surveys 42(4), 2010"
    locator: the sections on anonymization operations and information metrics
---

Generalization and suppression is the standard way to turn a table into a [k-anonymous](/k-anonymity/) one. Generalization replaces each [quasi-identifier](/quasi-identifier/) value by a coarser value from a hierarchy, such as the ZIP code 02139 by 021\*\* or the age 34 by 30 to 39. Suppression removes what is left over: a few outlier rows, or single cells. The values stay true, only less precise, which is why the technique was preferred to adding noise in early medical and census releases. The algorithms that use it differ in what they generalize together and in how they search for a good generalization.

## In plain words

Think of the ZIP code as an address that you can write with less and less detail: the full code, then four digits and a star, then three digits and two stars, then only a star. Do the same for the age and the date of birth. A row is safe when at least $k$ rows look the same at the chosen detail. Use less detail until almost all rows are safe. Delete the few rows that are still unusual, instead of making the whole table coarse for their sake.

The work is to find the least loss of detail that makes the table safe. Many choices are possible, and the best one is hard to find in general.

## When it applies

- The release is a table of records, one per person, with a known [quasi-identifier](/quasi-identifier/) of a few attributes.
- Each quasi-identifier attribute has a meaningful hierarchy: ZIP codes by prefix, dates by month and year, ages by intervals, categories by a taxonomy. The data holder writes these hierarchies; they are part of the policy, as is $k$.
- The users of the data accept values that are true but coarse, and a small number of deleted rows.
- The privacy goal is a syntactic model such as [k-anonymity](/k-anonymity/) or [l-diversity](/l-diversity/). For a guarantee against any outside knowledge, use [differential privacy](/differential-privacy-definition/) instead.

## The template

A hierarchy for attribute $a$ has levels $0, 1, \ldots, h_a$. Level 0 is the raw value, and $H_a[l]$ maps a raw value to its value at level $l$. In a *tree hierarchy* each value at level $l$ has one parent at level $l + 1$ and level $h_a$ is the root, often written \*. In *full-domain* generalization one vector $v = (v_1, \ldots, v_d)$ gives the level of each attribute for the whole table. The vectors with $0 \le v_a \le h_a$ form a lattice under the order $v \le w$ when $v_a \le w_a$ for each $a$. It has $g = \prod_a (h_a + 1)$ vectors, and the height of $v$ is $\sum_a v_a$.

```pseudo id=main
ANONYMIZE(T, ⟨hierarchies⟩, ⟨privacy test⟩, ⟨search⟩, ⟨loss⟩, MaxSup)
L1  best ← NIL
L2  for each candidate v that ⟨search⟩ proposes over the lattice of ⟨hierarchies⟩ do
L3      R ← GENERALIZE-AND-SUPPRESS(T, v, ⟨privacy test⟩, MaxSup)
L4      if R ≠ FAIL and (best = NIL or ⟨loss⟩(R) < ⟨loss⟩(best)) then best ← R
L5      if ⟨search⟩ can stop now then exit the loop
L6  return best

GENERALIZE-AND-SUPPRESS(T, v, ⟨privacy test⟩, MaxSup)
L7  for each row t of T do t' ← (H_1[v_1](t.A_1), ..., H_d[v_d](t.A_d)) with the other attributes of t
L8  put the rows t' in classes by their quasi-identifier values, with a hash table
L9  S ← the rows of the classes that fail ⟨privacy test⟩           ▷ k-anonymity: class size < k
L10 if |S| > MaxSup then return FAIL
L11 return the generalized rows without the rows of S, in a random order
```

The holes are the hierarchies, the privacy test of a class, the order in which ⟨search⟩ proposes vectors and when it stops, and the ⟨loss⟩ that compares two releases. The core step, lines L7 to L11, takes $O(n d)$ expected time for $n$ rows on the [word RAM](/word-ram/). Line L11 shuffles the rows, so that the row order of two releases does not match them up.

**Why it is correct for k-anonymity.** Line L9 puts a row in $S$ exactly when its class has fewer than $k$ rows. Removing all the rows of a class does not change the other classes, so each class that is left has at least $k$ rows. This holds for every vector and every search.

**Monotonicity.** With tree hierarchies, if $v \le w$ then each class at $w$ is a union of classes at $v$. So the number of rows that line L9 removes for k-anonymity can only go down when $v$ goes up. This is the property that lets [Samarati's algorithm](/samarati-algorithm/) do a binary search on the height and lets [Incognito](/incognito/) prune the lattice.

**An example lattice.** The 9 rows of Ciriani et al. (2007) have the attributes race and ZIP: asian 94142, asian 94141, three rows of asian 94139, black 94138, black 94139, white 94139 and white 94141. Race has the levels R0 (the value) and R1 (person). ZIP has the levels Z0 (5 digits), Z1 (9414\* or 9413\*) and Z2 (941\*\*). The table gives the number of rows that line L9 removes for $k = 2$.

| vector (race, ZIP) | height | classes of fewer than 2 rows | rows removed |
|---|---|---|---|
| (0, 0) | 0 | 6 single rows | 6 |
| (0, 1) | 1 | white 9413\*, white 9414\* | 2 |
| (1, 0) | 1 | person 94142, person 94138 | 2 |
| (0, 2) | 2 | none | 0 |
| (1, 1) | 2 | none | 0 |
| (1, 2) | 3 | none | 0 |

With MaxSup = 2, both vectors of height 1 work, and neither of them is below the other. Both are minimal generalizations, so the minimal answer is not unique, and the choice between them is a matter of the ⟨loss⟩.

## Classic examples

- [Samarati's algorithm](/samarati-algorithm/): full-domain generalization with tuple suppression. ⟨search⟩ is a binary search on the height, and ⟨loss⟩ is the height.
- [Datafly](/datafly/): full-domain generalization with tuple suppression. ⟨search⟩ is greedy: raise the level of the attribute with the most distinct values, until at most $k$ rows are left to suppress.
- [Incognito](/incognito/): full-domain generalization. ⟨search⟩ visits the lattices of the subsets of the attributes from small to large, as in a priori frequent item set mining, and finds every k-anonymous vector.
- [Mondrian](/mondrian-anonymization/): multidimensional generalization. Instead of one vector for the table, it cuts the space of quasi-identifier values into boxes of at least $k$ rows, and each box is released as its ranges.
- [The O(k) approximation](/k-anonymity-approximation/): cell suppression only. Each cluster of rows hides the columns where its rows differ.

## Variations

- **The level of the recoding.** Ciriani et al. (2007) classify the methods by the level at which they generalize (attribute or cell) and suppress (tuple, attribute or cell). Full-domain generalization, also called global recoding, uses one level per attribute. Local recoding generalizes each cell on its own; it loses less detail, but the same value can appear at different levels in one column, which makes analysis harder.
- **Subtree and sibling generalization.** A value can be generalized together with only its subtree of the hierarchy, not the whole level.
- **Multidimensional recoding.** Generalize tuples of values together, as boxes, which is what [Mondrian](/mondrian-anonymization/) does.
- **The loss measure.** The height of $v$; the precision of Sweeney (2002), which averages the level of each cell divided by the height of its hierarchy; the discernibility metric of Bayardo and Agrawal (2005), which charges each row the size of its class and each removed row the size of the table; and the average class size divided by $k$. They rank releases differently. None of them measures the value of the data for a given analysis, so they are heuristics for utility.
- **Exact search.** Bayardo and Agrawal (2005) search a set-enumeration tree with pruning and find a release of least discernibility cost on real data sets. The problem stays NP-hard in general ([NP-hardness of optimal k-anonymity](/k-anonymity-np-hardness/)).
- **Other privacy tests.** Line L9 can test [l-diversity](/l-diversity/) or [t-closeness](/t-closeness/) on the sensitive values of each class. The same search works if the test is monotone under generalization.

## Pitfalls

- **A hierarchy that is not a tree.** If the intervals of a level overlap or a value has two parents, monotonicity fails, and the binary search of Samarati and the pruning of Incognito can miss the answer.
- **Suppressed rows are not random.** Line L9 removes the rows with rare values, such as the oldest people or rare races. An analysis of the release is then biased. Report the number of suppressed rows and the rule.
- **A small quasi-identifier.** The release is safe only against a join on the attributes that the data holder chose. An attribute that is left out, but known to an adversary, can undo the protection.
- **The row order.** Rows released in the order of the original table can be matched across two releases by their position. Line L11 shuffles them.
- **Many attributes.** With many quasi-identifier attributes, most rows are far apart, and k-anonymity needs so much generalization that little detail is left. This is a known limit of the technique on wide or sparse data.

## Exercises

1. Show that the lattice of full-domain generalization vectors has $g = \prod_a (h_a + 1)$ vectors and $h + 1$ heights, where $h = \sum_a h_a$.
2. Prove the monotonicity of the number of removed rows for tree hierarchies. Then give a hierarchy for one attribute, with two overlapping intervals at one level, where it fails.
3. In the example lattice above, find all minimal vectors for $k = 2$ with MaxSup = 0, and for $k = 3$ with MaxSup = 2.
4. Show that the discernibility cost of a k-anonymous release of $n$ rows without suppression is at least $n k$, and say when it is equal to $n k$.

## References
