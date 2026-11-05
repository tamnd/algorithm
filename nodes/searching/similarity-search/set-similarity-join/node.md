---
tag: EZXWD1
kind: problem
slug: set-similarity-join
name: Set similarity join
aliases:
- similarity join of sets
area: searching/similarity-search
level: advanced
summary: Find all pairs of sets from two collections whose Jaccard or overlap similarity exceeds a threshold.
prereqs: [jaccard-similarity, prefix-filtering]
see_also: [ppjoin, prefix-filtering, allpairs, minhash, string-similarity-join, jaccard-similarity, orthogonal-vectors, similarity-range-query]
sources:
  - paper: doi:10.1109/ICDE.2006.9
    title: Surajit Chaudhuri, Venkatesh Ganti and Raghav Kaushik, A primitive operator for similarity joins in data cleaning, Proceedings of the 22nd International Conference on Data Engineering (ICDE 2006)
    locator: the SSJoin operator, the reduction of string and set similarity predicates to an overlap threshold, and prefix filtering
  - paper: "Arvind Arasu, Venkatesh Ganti and Raghav Kaushik, Efficient exact set-similarity joins, Proceedings of the 32nd International Conference on Very Large Data Bases (VLDB 2006)"
    locator: pages 918 to 929 (PartEnum, signature schemes with a guarantee for the Hamming and Jaccard joins)
  - paper: doi:10.1145/1367497.1367516
    title: Chuan Xiao, Wei Wang, Xuemin Lin and Jeffrey Xu Yu, Efficient similarity joins for near duplicate detection, Proceedings of the 17th International World Wide Web Conference (WWW 2008)
    locator: pages 131 to 140 (Section 2, the problem statement, the overlap thresholds for Jaccard, cosine and overlap similarity; Sections 3 and 4, PPJoin and PPJoin+)
  - paper: "Willi Mann, Nikolaus Augsten and Panagiotis Bouros, An empirical evaluation of set similarity join techniques, Proceedings of the VLDB Endowment 9(9), 2016"
    locator: pages 636 to 647 (an experimental comparison of the prefix filter based algorithms on many data sets)
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005
    locator: pages 357 to 365 (the reduction from CNF satisfiability to orthogonal vectors)
---

The set similarity join takes two collections $R$ and $S$ of finite sets and a threshold $t$, and asks for every pair $(r, s) \in R \times S$ whose similarity is at least $t$, where the similarity is the [Jaccard similarity](/jaccard-similarity/) $|r \cap s| / |r \cup s|$, the [cosine similarity](/cosine-similarity/) of the indicator vectors, or the plain overlap $|r \cap s|$. The *self-join* takes $S = R$ and asks for the unordered pairs of distinct sets. It is the core of near-duplicate detection, data cleaning and record linkage. The scan of all $|R| \cdot |S|$ pairs is the baseline. Exact algorithms based on [prefix filtering](/prefix-filtering/), such as [All-Pairs](/allpairs/) and [PPJoin](/ppjoin/), avoid most pairs on real data but not in the worst case. Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), no algorithm decides in time $O(n^{2 - \varepsilon})$ whether the Jaccard join of $n$ sets with $n$ sets of size $\Theta(\log n)$ at $t = 1/2$ is empty.

## In plain words

You have two lists of sets. A set can be the words of a product title, the shingles of a web page, or the items a customer bought. You want every pair, one set from each list, that is nearly the same: the shared items make up a large part of the two sets together.

Checking every pair works, but with a million sets on each side that is a trillion checks. The useful methods first find, cheaply, a short list of pairs that might be similar, and then check only those. Some do this exactly and never miss a pair. Others use random hashing, are much faster on hard data, and miss a pair now and then with a small chance that you can choose.

## Definition

Let $U$ be a universe of elements, and let $\mathrm{sim}$ be a similarity function on nonempty finite subsets of $U$. Given finite collections $R$ and $S$ of nonempty finite subsets of $U$ and a threshold $t$, the **set similarity join** is

$$R \bowtie_t S = \{\, (r, s) \in R \times S : \mathrm{sim}(r, s) \ge t \,\}.$$

The **self-join** of $R$ is $\{\{r, r'\} : r, r' \in R,\ r \ne r',\ \mathrm{sim}(r, r') \ge t\}$, where $r$ and $r'$ are different members of the collection, which may be equal as sets. The usual similarity functions, for $0 < t \le 1$ except for the overlap, are

| name | $\mathrm{sim}(r, s)$ | equivalent overlap condition |
|---|---|---|
| overlap | $\lvert r \cap s \rvert$ | $\lvert r \cap s \rvert \ge t$ |
| Jaccard | $\lvert r \cap s \rvert / \lvert r \cup s \rvert$ | $\lvert r \cap s \rvert \ge \frac{t}{1+t}(\lvert r \rvert + \lvert s \rvert)$ |
| cosine | $\lvert r \cap s \rvert / \sqrt{\lvert r \rvert \lvert s \rvert}$ | $\lvert r \cap s \rvert \ge t \sqrt{\lvert r \rvert \lvert s \rvert}$ |
| Dice | $2 \lvert r \cap s \rvert / (\lvert r \rvert + \lvert s \rvert)$ | $\lvert r \cap s \rvert \ge \frac{t}{2}(\lvert r \rvert + \lvert s \rvert)$ |

The table shows the observation of Chaudhuri, Ganti and Kaushik: each of these joins is an overlap join with a threshold that depends only on the two sizes. For Jaccard, $o / (|r| + |s| - o) \ge t$ rearranges to $o(1 + t) \ge t(|r| + |s|)$ with $o = |r \cap s|$. The cost of an algorithm is measured in the word RAM, with elements as words, as a function of $n = |R| + |S|$, the total size $N$ of the sets, and the output size $\kappa$.

## Variants

- **Self-join and R-S join.** The self-join is the case $S = R$ without the diagonal. An R-S join reduces to a self-join of $R \cup S$ by tagging each set with its side and dropping pairs from the same side.
- **Top-$k$ join.** Report the $k$ pairs of highest similarity, with no threshold. Prefix filtering still works, with a threshold that rises as better pairs are found.
- **Weighted sets.** Each element has a weight, for example its inverse document frequency, and the overlap is the weight of the intersection. The prefix becomes the shortest initial part whose remaining weight is below the threshold.
- **Containment join.** Report the pairs with $r \subseteq s$, or with $|r \cap s| / |r| \ge t$. The condition is not symmetric, and the size filter works in one direction only.
- **Approximate join.** Report each pair with $\mathrm{sim} \ge t$ with probability at least $1 - \delta$, and few pairs below a lower threshold $t' < t$. [MinHash](/minhash/) with banding solves it for Jaccard.
- **[String similarity join](/string-similarity-join/).** The objects are strings and the predicate is an [edit distance](/edit-distance/) bound. Each string becomes its set of $q$-grams, and the [q-gram filtering](/q-gram-filtering/) count turns the edit bound into an overlap bound, followed by an exact check.

## Examples

**An R-S join.** Let $R = \{r_1, r_2, r_3\}$ with $r_1 = \{a, b, c\}$, $r_2 = \{b, c, d, e\}$, $r_3 = \{a, e\}$, and $S = \{s_1, s_2, s_3\}$ with $s_1 = \{a, b, c, d\}$, $s_2 = \{c, d, e\}$, $s_3 = \{a, f\}$.

| pair | overlap | Jaccard | cosine |
|---|---|---|---|
| $r_1, s_1$ | 3 | 0.75 | 0.8660 |
| $r_1, s_2$ | 1 | 0.2 | 0.3333 |
| $r_1, s_3$ | 1 | 0.25 | 0.4082 |
| $r_2, s_1$ | 3 | 0.6 | 0.75 |
| $r_2, s_2$ | 3 | 0.75 | 0.8660 |
| $r_2, s_3$ | 0 | 0 | 0 |
| $r_3, s_1$ | 1 | 0.2 | 0.3536 |
| $r_3, s_2$ | 1 | 0.25 | 0.4082 |
| $r_3, s_3$ | 1 | 0.3333 | 0.5 |

With Jaccard and $t = 0.5$ the join is $\{(r_1, s_1), (r_2, s_1), (r_2, s_2)\}$, which is also the overlap join with $t = 3$. With the cosine and $t = 0.5$ it gains $(r_3, s_3)$, two small sets with one common element: the cosine is more lenient than Jaccard on sets of different sizes, since $\mathrm{cos} \ge J$ always.

**A self-join.** The six sets $r_1, \ldots, r_6$ of the [prefix filtering](/prefix-filtering/) example, at Jaccard threshold $0.6$, have the self-join $\{r_1, r_2\}, \{r_1, r_6\}, \{r_3, r_6\}$, 3 of the 15 pairs. Prefix filtering verifies 10 pairs to find them, and [PPJoin](/ppjoin/) verifies 6.

**A worst case for filters.** If all $n$ sets contain a common rare element and are otherwise disjoint, every pair shares the first element of its prefix, so prefix filtering makes all $\binom{n}{2}$ pairs candidates, while the output is empty for any $t$ above the similarity of two such sets.

## Known algorithms

| algorithm | idea | exact | worst-case time |
|---|---|---|---|
| nested loops | verify every pair by a merge | yes | $O(\lvert R \rvert \lvert S \rvert\, m)$ for sets of size at most $m$ |
| [prefix filtering](/prefix-filtering/), SSJoin (2006) | an [inverted index](/inverted-index/) on prefixes in a global order; candidates share a prefix element | yes | same, plus $O(N \log N)$ |
| [All-Pairs](/allpairs/) (2007) | process by size, index only a shorter prefix, size filter | yes | same |
| [PPJoin](/ppjoin/) and PPJoin+ (2008) | positional filter on the prefix element, suffix filter | yes | same |
| PartEnum (2006) | partition the dimensions and enumerate signatures; equal signatures for every close pair | yes | depends on the signature count |
| matrix product | the overlaps are the entries of $M M^{\mathsf{T}}$ for the incidence matrix $M$ | yes | $O(n^\omega)$ arithmetic when $\lvert U \rvert \le n$ |
| [MinHash](/minhash/) with banding | $b$ bands of $r$ rows; candidates agree on a whole band | no | $O(N b r + \text{candidates})$ expected |

For the matrix product, let $M$ be the $|R| \times |U|$ 0-1 matrix with $M[r][u] = 1$ when $u \in r$, and $M'$ the same for $S$. Then $(M M'^{\mathsf{T}})[r][s] = |r \cap s|$, and with the sizes this gives every similarity at once, in $O(n^\omega)$ operations on integers of $O(\log n)$ bits when $|U| \le n$, where $\omega < 2.372$ is the exponent of matrix multiplication. It is the best known exact method for dense sets over a small universe; see [Boolean matrix multiplication](/boolean-matrix-multiplication/).

For MinHash with $b$ bands of $r$ rows, a pair of Jaccard similarity $J$ becomes a candidate with probability exactly $1 - (1 - J^r)^b$ under truly random permutations, and each candidate is then verified, so the output has no false positives, and each true pair is missed with probability $(1 - J^r)^b \le (1 - t^r)^b$.

In experiments on real data, the prefix filter based algorithms dominate. Mann, Augsten and Bouros compared them on many data sets and found the differences between All-Pairs, PPJoin and the later variants small and data dependent, with the verification often cheaper than the candidate generation.

## Bounds

**Output size.** The output can have $|R| \cdot |S|$ pairs, for example when all sets are equal, so every algorithm that lists it takes $\Omega(|R| \cdot |S|)$ time in the worst case. Bounds of interest are about deciding emptiness, or are output sensitive.

**Conditional lower bound.** Assume the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/). Then for every $\varepsilon > 0$ there is a constant $c$ such that no algorithm in the word RAM decides, in time $O(n^{2 - \varepsilon})$, whether the Jaccard join at threshold $t = 1/2$ of $n$ sets of size $d$ with $n$ sets of size $2d$ is empty, for $d = c \log n$. The proof is the reduction from [orthogonal vectors](/orthogonal-vectors/) below, together with Williams' theorem that an $O(n^{2 - \varepsilon})$ algorithm for orthogonal vectors in dimension $c \log n$, for every $c$, refutes SETH. The same holds for the overlap join at threshold $d$.

**Exact filters do not help in the worst case.** In the example of a common rare element above, prefix filtering and the positional filter of PPJoin keep all $\binom{n}{2}$ pairs as candidates while the output is empty, so their worst case is that of the scan.

## Reductions

**From orthogonal vectors.** Given $A, B \subseteq \{0, 1\}^d$ with $|A| = |B| = n$, decide whether some $a \in A$ and $b \in B$ have $a \cdot b = 0$. Use the universe $\{1, \ldots, d\} \times \{\alpha, \beta, \gamma\}$, and map

$$a \mapsto \bar a = \{(i, \alpha) : a_i = 0\} \cup \{(i, \beta) : a_i = 1\}, \qquad b \mapsto \bar b = \{(i, \alpha) : 1 \le i \le d\} \cup \{(i, \beta) : b_i = 0\} \cup \{(i, \gamma) : b_i = 1\}.$$

Then $|\bar a| = d$ and $|\bar b| = 2d$. Coordinate $i$ contributes one common element to $\bar a \cap \bar b$ unless $a_i = b_i = 1$, in which case $\bar a$ has $(i, \beta)$ and $\bar b$ has $(i, \alpha)$ and $(i, \gamma)$, and it contributes none. So $|\bar a \cap \bar b| = d - a \cdot b$, and $J(\bar a, \bar b) = (d - a \cdot b) / (2d + a \cdot b)$, which is $1/2$ when $a \cdot b = 0$ and below $1/2$ otherwise. The join of $\{\bar a\}$ and $\{\bar b\}$ at $t = 1/2$ is nonempty if and only if an orthogonal pair exists. The map takes $O(nd)$ time.

**To an overlap join.** By the table of the definition, a Jaccard, cosine or Dice join is an overlap join with a threshold that depends on $(|r|, |s|)$. Grouping the sets by size gives at most $m^2$ overlap joins with constant thresholds, for sets of size at most $m$.

**From the string similarity join.** Two strings within [edit distance](/edit-distance/) $k$ share at least $\max(|x|, |y|) - q + 1 - kq$ of their positional $q$-grams. So the string join reduces to an overlap join on $q$-gram multisets, followed by an exact edit distance check of each candidate.

**To the R-S self-join and back.** An R-S join is a self-join of $R \cup S$ with tagged sides, and a self-join of $R$ is the R-S join of $R$ with itself, with the diagonal and the duplicate orientation removed.

## Applications

- **Near-duplicate documents.** Web pages or news stories as [shingle](/shingling/) sets; the join at a high Jaccard threshold finds copies and mirrors.
- **Data cleaning and record linkage.** Names and addresses as token or $q$-gram sets; the join finds records of the same entity with typing errors. This was the motivation of the SSJoin operator.
- **Collaborative filtering.** Users as sets of items; the join finds users with similar tastes, or items bought by the same users.
- **Query and log analysis.** Queries as sets of clicked results, to find queries with the same intent.
- **Plagiarism detection.** Source files or essays as sets of hashed $k$-grams of tokens.

## References
