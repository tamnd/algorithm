---
tag: MAS7EM
kind: technique
slug: prefix-filtering
name: Prefix filtering
aliases:
- prefix filter
area: searching/similarity-search
level: advanced
summary: Only sets sharing a token in their rarest-token prefix can reach a threshold, so only those pairs are checked.
prereqs: [jaccard-similarity, inverted-index]
see_also: [set-similarity-join, ppjoin, allpairs, all-pairs-similarity-search, string-similarity-join, q-gram-filtering, shingling, minhash]
sources:
  - paper: doi:10.1109/ICDE.2006.9
    title: Surajit Chaudhuri, Venkatesh Ganti and Raghav Kaushik, A primitive operator for similarity joins in data cleaning, Proceedings of the 22nd International Conference on Data Engineering (ICDE), 2006
    locator: the SSJoin operator and the prefix filter (if two sets of sizes at most l overlap in at least α elements, their prefixes of length l − α + 1 in a fixed global order intersect)
  - paper: doi:10.1145/1242572.1242591
    title: Roberto J. Bayardo, Yiming Ma and Ramakrishnan Srikant, Scaling up all pairs similarity search, Proceedings of the 16th International World Wide Web Conference (WWW), 2007
    locator: pages 131 to 140 (the All-Pairs algorithm, which indexes only a prefix of each vector, ordered by frequency, and processes the vectors in order of size)
  - paper: doi:10.1145/1367497.1367516
    title: Chuan Xiao, Wei Wang, Xuemin Lin and Jeffrey Xu Yu, Efficient similarity joins for near duplicate detection, Proceedings of the 17th International World Wide Web Conference (WWW), 2008
    locator: Section 3 (the prefix filtering principle for Jaccard, cosine and overlap thresholds, the prefix length |x| − ⌈t|x|⌉ + 1, and the size filter)
---

Prefix filtering is the technique of sorting the elements of every set in one fixed global order, keeping only a short *prefix* of each sorted set, and comparing only pairs of sets whose prefixes share an element. If two sets must overlap in at least $\alpha$ elements, then their prefixes of length $|x| - \alpha + 1$ and $|y| - \alpha + 1$ share an element, so no pair above the threshold is missed. For a [Jaccard](/jaccard-similarity/) threshold $t$ the prefix of a set $x$ has $|x| - \lceil t|x| \rceil + 1$ elements, a small part of $x$ when $t$ is high. With the global order chosen from the rarest to the most frequent element, the prefixes contain rare elements, the lists of an [inverted index](/inverted-index/) on them are short, and few candidate pairs remain. Chaudhuri, Ganti and Kaushik introduced it in 2006, and it is the base of [All-Pairs](/allpairs/), [PPJoin](/ppjoin/) and most exact algorithms for the [set similarity join](/set-similarity-join/).

## In plain words

You have a pile of sets, such as the words of many documents, and you want all pairs that share most of their words. Comparing every pair is too slow. Here is a way to skip most pairs safely.

Put every set in the same fixed order, with rare words first. Now take two sets that share, say, at least 8 words, and look at the first shared word in this order. All the other shared words come after it in both sets, so it cannot be near the end of either set: at least 7 words follow it. So the first few words of each set, all but the last 7, already contain a shared word. Only pairs whose first few words overlap can be similar. Since the first words are rare ones, few pairs pass this test.

## When it applies

- The objects are sets, or multisets, or sparse vectors with nonnegative weights.
- The question is a join or a search with a **high threshold** on a similarity that implies a minimum overlap: overlap, [Jaccard](/jaccard-similarity/), [cosine](/cosine-similarity/), dice. The higher the threshold, the shorter the prefixes.
- The answer must be **exact**: every pair above the threshold, as opposed to the probabilistic answer of [MinHash](/minhash/) with [LSH](/locality-sensitive-hashing/).
- The element frequencies are skewed, as for words and [shingles](/shingling/), so that the rare elements in the prefixes have short lists.

## The template

Fix a total order $\prec$ on the universe of elements, and write each set $x$ as the list of its elements sorted by $\prec$. For $1 \le p \le |x|$, the **$p$-prefix** of $x$ is the list of its first $p$ elements.

**Lemma (prefix filtering).** Let $x$ and $y$ be sets with $|x \cap y| \ge \alpha \ge 1$. Then the $(|x| - \alpha + 1)$-prefix of $x$ and the $(|y| - \alpha + 1)$-prefix of $y$ share an element.

*Proof.* Let $w$ be the least element of $x \cap y$ in the order $\prec$. The other $|x \cap y| - 1 \ge \alpha - 1$ common elements are greater than $w$, so in the sorted list of $x$ at least $\alpha - 1$ elements follow $w$, and $w$ is at position at most $|x| - \alpha + 1$. The same holds for $y$. So $w$ lies in both prefixes. $\square$

**Thresholds.** If $J(x, y) = |x \cap y| / |x \cup y| \ge t$ and $|y| \le |x|$, then $|x \cap y| \ge t\,|x \cup y| \ge t\,|x|$, so the lemma applies with $\alpha = \lceil t|x| \rceil$; since $\alpha \ge \lceil t|y| \rceil$, the prefix of length $p(y) = |y| - \lceil t|y| \rceil + 1$ is at least as long as the one the lemma needs. Also $|y| \ge |x \cap y| \ge t|x|$, the **size filter**. For the cosine of binary vectors, $|x \cap y| \ge t\sqrt{|x|\,|y|}$ gives $\alpha \ge \lceil t^2 |x| \rceil$ in the same way.

```pseudo id=main
SELF-JOIN(R, t)                              ▷ all pairs of sets of R with Jaccard similarity at least t
L1  ≺ ← the elements in order of increasing frequency in R; sort each set by ≺
L2  sort R by size
L3  I ← an empty inverted index from elements to lists of sets
L4  for each x in R, in order of size do
L5      C ← ∅
L6      for each element w in the p(x)-prefix of x, with p(x) = |x| − ⌈t|x|⌉ + 1, do
L7          for each y in I[w] with |y| ≥ t|x| do C ← C ∪ {y}      ▷ hole: more filters
L8          append x to I[w]
L9      for each y in C do
L10         if J(x, y) ≥ t then output (y, x)                   ▷ verification
```

Each pair is found when its larger set (in the order of line L2) is processed. Line L7 applies the size filter; it is where [PPJoin](/ppjoin/) adds the positional filter and PPJoin+ the suffix filter. Line L10 computes the exact similarity, in $O(|x| + |y|)$ time by merging the sorted lists.

### Example

Let $t = 0.6$ and $R = \{r_1, \ldots, r_6\}$ with $r_1 = \{A, B, C, D, E\}$, $r_2 = \{A, B, C, D, F\}$, $r_3 = \{B, C, D, E, F, G\}$, $r_4 = \{A, G, H\}$, $r_5 = \{C, D, E, F, H\}$ and $r_6 = \{A, B, C, D, E, G\}$. The frequencies are $H$: 2, $F$ and $G$: 3, $A$, $B$ and $E$: 4, $C$ and $D$: 5, so the order is $H \prec F \prec G \prec A \prec B \prec E \prec C \prec D$, with ties broken by name. A set of size 3 has a prefix of $3 - 2 + 1 = 2$ elements, one of size 5 has $5 - 3 + 1 = 3$, and one of size 6 has $6 - 4 + 1 = 3$.

| set, in order | sorted | prefix | candidates | similarities |
|---|---|---|---|---|
| $r_4$ | H G A | H G | none | |
| $r_1$ | A B E C D | A B E | none | |
| $r_2$ | F A B C D | F A B | $r_1$ | $J(r_1, r_2) = 0.6667$, output |
| $r_5$ | H F E C D | H F E | $r_1$, $r_2$, $r_4$ | 0.4286, 0.4286, 0.1429 |
| $r_3$ | F G B E C D | F G B | $r_1$, $r_2$, $r_5$ | 0.5714 each |
| $r_6$ | G A B E C D | G A B | $r_1$, $r_2$, $r_3$ | 0.8333 and 0.7143 output, 0.5714 |

The join outputs $(r_1, r_2)$, $(r_1, r_6)$ and $(r_3, r_6)$, which are all the pairs with $J \ge 0.6$, after verifying 10 candidate pairs of the 15. The elements $C$ and $D$, in five sets each, never enter a prefix, and their lists stay empty.

**Cost.** Lines L1 and L2 take $O(N \log N)$ time for $N = \sum |x|$. The probing costs the total length of the lists read in line L7, and the verification $O(|x| + |y|)$ per candidate. In the worst case every pair is a candidate, for example when all sets share one rare element, and the join costs $\Theta(n^2)$ verifications, the same as the scan; the gain is on skewed data with a high threshold.

## Classic examples

- **SSJoin.** Chaudhuri, Ganti and Kaushik defined a set similarity join operator for data cleaning in a database engine, with the prefix filter as a relational plan.
- **[All-Pairs](/allpairs/).** Bayardo, Ma and Srikant index only a prefix of each vector, process vectors by size, and apply the size filter, for cosine thresholds on weighted vectors.
- **[PPJoin](/ppjoin/).** Xiao, Wang, Lin and Yu add the positional filter, an upper bound on the overlap from the positions of the shared prefix element, and PPJoin+ adds a suffix filter.
- **[String similarity join](/string-similarity-join/).** Strings become sets of $q$-grams; an edit distance threshold $k$ gives a minimum overlap by the [q-gram lemma](/q-gram-lemma/), and the prefix of $qk + 1$ $q$-grams in a global order is enough (Ed-Join).
- **Near-duplicate detection.** With documents as sets of [shingles](/shingling/) and a high Jaccard threshold, the join finds all near-duplicate pairs exactly.

## Variations

- **Global order.** Any total order is correct; increasing frequency makes the lists of the prefix elements short. A random order, by a hash, needs no counting pass but gives longer lists.
- **Index prefix shorter than the probe prefix.** If sets are processed by increasing size, $x$ only needs to be found by larger sets, which need an overlap of at least $\lceil \frac{2t}{1+t} |x| \rceil$ with it; so $x$ can be indexed with the shorter prefix $|x| - \lceil \frac{2t}{1+t}|x| \rceil + 1$ while it still probes with $p(x)$.
- **Weighted sets.** For weighted overlap or cosine, the prefix is the shortest list of first elements whose remaining weight is below the needed overlap.
- **R-S join.** For two collections, index one and probe with the other, or index both with a common order.
- **Top-$k$ join.** Lower the threshold as the $k$ best pairs are found; prefixes grow as the threshold falls.

## Pitfalls

- **Different orders for different sets.** The lemma needs one global order for all sets. Sorting each set by its own frequencies, or by a hash with a different seed per set, breaks it.
- **Rounding of the prefix length.** The overlap bound is $\lceil t|x| \rceil$, a ceiling. Floating point can turn $t|x| = 3$ into $3.0000000000000004$, whose ceiling 4 gives a prefix one element too short and loses pairs; compute with a small tolerance or with rational numbers.
- **Duplicates inside a set.** Multisets need distinct tokens, for example by numbering the repeats ($w_1$, $w_2$), before the lemma applies.
- **Low thresholds.** For $t = 0.2$ the prefix is 80% of the set, and the filter saves little; use [MinHash](/minhash/) or [LSH](/locality-sensitive-hashing/) when an approximate answer is enough.
- **Counting the same pair twice.** Probing with all of $x$'s prefix may find $y$ through several elements; $C$ must be a set.

## Exercises

1. Show that the bound of the lemma is tight: for every $\alpha \ge 1$ and sizes $|x|, |y| \ge \alpha$, give two sets with $|x \cap y| = \alpha$ whose $(|x| - \alpha)$-prefix and $(|y| - \alpha)$-prefix are disjoint.
2. For the cosine similarity of binary vectors, $|x \cap y| / \sqrt{|x|\,|y|} \ge t$, derive the prefix length and the size filter.
3. In the example, find the candidate pairs if the order breaks ties by reverse name instead, and check that the output is the same.

## References
