---
tag: 7RPTK2
kind: problem
slug: string-similarity-join
name: String similarity join
aliases:
- approximate string join
area: strings/approximate-matching
level: research
summary: Find all pairs of strings, one from each of two collections, that are within a similarity threshold.
prereqs: [edit-distance, q-gram-lemma]
see_also: [set-similarity-join, approximate-dictionary-lookup, q-gram-filtering, prefix-filtering, pigeonhole-filtering, edit-distance-hardness, all-pairs-similarity-search, minhash]
sources:
  - paper: "Luis Gravano, Panagiotis G. Ipeirotis, H. V. Jagadish, Nick Koudas, S. Muthukrishnan and Divesh Srivastava, Approximate string joins in a database (almost) for free, Proceedings of the 27th International Conference on Very Large Data Bases (VLDB), 2001"
    locator: the count, position and length filters on positional q-grams, written as SQL queries, followed by an exact check of the edit distance
  - paper: doi:10.1109/ICDE.2006.9
    title: Surajit Chaudhuri, Venkatesh Ganti and Raghav Kaushik, A primitive operator for similarity joins in data cleaning, Proceedings of the 22nd International Conference on Data Engineering (ICDE), 2006
    locator: the SSJoin operator, the reduction of an edit distance threshold to an overlap of q-gram sets, and the prefix filter
  - paper: "Chuan Xiao, Wei Wang and Xuemin Lin, Ed-Join: an efficient algorithm for similarity joins with edit distance constraints, Proceedings of the VLDB Endowment 1(1), 2008"
    locator: the prefix of qk + 1 q-grams for an edit distance threshold k, and the location-based and content-based mismatch filters that shorten it
  - paper: "Guoliang Li, Dong Deng, Jiannan Wang and Jianhua Feng, Pass-Join: a partition-based method for similarity joins, Proceedings of the VLDB Endowment 5(3), 2011"
    locator: the partition of each string into k + 1 segments and the selection of the substrings of the other string that are compared with them
  - paper: "Yu Jiang, Guoliang Li, Jianhua Feng and Wen-Syan Li, String similarity joins: an experimental evaluation, Proceedings of the VLDB Endowment 7(8), 2014"
    locator: the survey and the experimental comparison of the join algorithms for edit distance and for token-based similarity
  - paper: doi:10.1137/15M1053128
    title: Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing, 2018
    locator: the vector gadgets, whose edit distance takes one value for orthogonal vectors and a larger one otherwise
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005
    locator: pages 357 to 365 (the reduction from CNF satisfiability to orthogonal vectors)
---

The string similarity join takes two collections of strings $R$ and $S$ and a threshold, and asks for all pairs $(r, s) \in R \times S$ that are similar enough, most often with [edit distance](/edit-distance/) at most $k$. It is the batch form of [approximate dictionary lookup](/approximate-dictionary-lookup/): every string of $R$ is a query against $S$. Practical algorithms use cheap filters, such as length, [q-gram counts](/q-gram-filtering/), [prefixes](/prefix-filtering/) and [partitions](/pigeonhole-filtering/), to cut the $|R| \cdot |S|$ pairs down to a short list of candidates, and check only those exactly. In the worst case no strongly subquadratic algorithm is known, and under SETH none exists.

## In plain words

Two lists of names come from two sources, and some names appear in both with small typing errors. The task is to list every pair of names, one from each list, that differ by at most a few edits.

Comparing every name with every name is correct but slow, since the number of pairs is the product of the list sizes. So the algorithms first throw away pairs that cannot be close: names whose lengths differ too much, or names that share too few short pieces of text. They index the short pieces of one list, so that each name of the other list meets only the names that share a piece with it. Only the pairs that pass every filter get the exact, slower comparison.

## Definition

Let $\Sigma$ be an alphabet and $\mathrm{ed}$ the Levenshtein distance: insertions, deletions and substitutions of single symbols, each of cost 1, with no transpositions. The input is two finite lists of strings $R = (r_1, \ldots, r_{|R|})$ and $S = (s_1, \ldots, s_{|S|})$ over $\Sigma$ and an integer $k \ge 0$. The output is the set of index pairs

$$ J_k(R, S) = \{\, (i, j) : 1 \le i \le |R|,\ 1 \le j \le |S|,\ \mathrm{ed}(r_i, s_j) \le k \,\}, $$

in any order. Pairs are reported as indices, so equal strings at two indices give two pairs. The **self-join** of one list $R$ reports the pairs $(i, j)$ with $i < j$ and $\mathrm{ed}(r_i, r_j) \le k$. With $k = 0$ the join is an equality join, which hashing solves in time linear in the input and output. Empty strings are allowed: $\mathrm{ed}(\varepsilon, s) = |s|$.

The q-gram filters below number the positions of a string from 0. A **q-gram** of $x$ is the substring $x[p \ldots p+q)$ for $0 \le p \le |x| - q$, and $Q(x)$ is the multiset of these $|x| - q + 1$ q-grams, empty when $|x| < q$.

## Variants

- **Normalized threshold.** Report pairs with $\mathrm{ed}(r, s) \le \tau \max(|r|, |s|)$ for a fraction $\tau$, so long strings may have more errors. For a pair this is a threshold $k = \lfloor \tau \max(|r|, |s|) \rfloor$ that depends on the lengths.
- **Token-based similarity.** Split each string into words or q-grams and compare the sets by Jaccard, cosine or overlap similarity. This is the [set similarity join](/set-similarity-join/).
- **Hamming join.** All strings have the same length, and the distance is the [Hamming distance](/hamming-distance/). It applies to fixed-length codes and binary fingerprints.
- **Top-k join.** Report the $K$ pairs with the smallest distance, with no threshold given.
- **Approximate join.** Allow the output to miss pairs with some probability, as with [MinHash](/minhash/) signatures for Jaccard similarity, in return for less work.
- **Distributed join.** Split $R$ and $S$ over many machines so that each pair that can be in the output meets on one machine.

## Examples

Let $R = (\texttt{kitten}, \texttt{sitting}, \texttt{mitten}, \texttt{smith})$ and $S = (\texttt{sitten}, \texttt{knitting}, \texttt{smitten}, \texttt{bitten}, \texttt{smyth})$. The edit distances are:

| | sitten | knitting | smitten | bitten | smyth |
|---|---|---|---|---|---|
| kitten | 1 | 3 | 2 | 1 | 5 |
| sitting | 2 | 2 | 3 | 3 | 5 |
| mitten | 1 | 4 | 1 | 1 | 5 |
| smith | 4 | 6 | 3 | 5 | 1 |

For $k = 1$ the join has 6 pairs: (kitten, sitten), (kitten, bitten), (mitten, sitten), (mitten, smitten), (mitten, bitten) and (smith, smyth). For $k = 2$ it has 9 pairs: these 6 and (kitten, smitten), (sitting, sitten) and (sitting, knitting).

**Filters for $k = 1$ and $q = 2$.** The length filter keeps a pair only if the lengths differ by at most 1. The count filter keeps it only if the strings share at least $\max(|r|, |s|) - q + 1 - kq = \max(|r|, |s|) - 3$ q-grams, counted with multiplicity. Of the 20 pairs, 8 pass both filters: the 6 pairs of the output and two **false candidates**, (kitten, smitten) and (sitting, knitting), each at distance 2. For example, kitten and smitten share the 4 q-grams it, tt, te and en, which is exactly the required $7 - 3 = 4$. The exact check removes the two false candidates. A filter never removes a pair of the output.

## Known algorithms

All exact algorithms below use the same three steps: generate candidate pairs with filters that keep every output pair, check each candidate with an edit distance computation that stops once the distance exceeds $k$, and report the pairs that pass. The check of one pair takes $O(k \min(|r|, |s|))$ time with a band of $2k + 1$ diagonals of the [Wagner-Fischer](/wagner-fischer-algorithm/) table, as in [Ukkonen's cutoff](/ukkonen-cutoff-algorithm/), or $O(|r| + |s| + k^2)$ time with the diagonal method of [Landau and Vishkin](/landau-vishkin-algorithm/).

| method | filter | where |
|---|---|---|
| nested loops | none, all $\lvert R \rvert \cdot \lvert S \rvert$ pairs | baseline |
| length filter | $\bigl\lvert \lvert r \rvert - \lvert s \rvert \bigr\rvert \le k$ | sort or group by length |
| q-gram count filter | at least $\max(\lvert r \rvert, \lvert s \rvert) - q + 1 - kq$ common q-grams | Gravano and others, 2001, in SQL |
| prefix filter | a common q-gram among the first $qk + 1$ of each string in a global order | Chaudhuri, Ganti and Kaushik, 2006; Ed-Join, 2008 |
| mismatch filters | shorter prefixes from the positions and content of the q-grams | Ed-Join, Xiao, Wang and Lin, 2008 |
| partition filter | one of $k + 1$ segments of $s$ occurs in $r$ | Pass-Join, Li, Deng, Wang and Feng, 2011 |
| tries | shared prefixes of the strings, with an active set of trie nodes | trie-based joins, for short strings |

**The filters are safe.** Let $\mathrm{ed}(r, s) \le k$.

- *Length.* Each operation changes the length by at most 1, so $\bigl| |r| - |s| \bigr| \le k$.
- *Count.* By the [q-gram lemma](/q-gram-lemma/), the multiset intersection $C = Q(r) \cap Q(s)$ has $|C| \ge |r| - q + 1 - kq$, and by symmetry $|C| \ge |s| - q + 1 - kq$.
- *Prefix.* Fix a total order on $\Sigma^q$, sort $Q(r)$ and $Q(s)$ by it, and assume $|r| - q + 1 - kq \ge 1$, so that $|C| \ge 1$. Let $x$ be the smallest element of $C$. A q-gram $v < x$ that occurs in $r$ does not occur in $s$, since otherwise $v \in C$. So all q-grams of $Q(r)$ before the first copy of $x$ are outside $C$, and there are at most $|Q(r)| - |C| \le kq$ of them. So $x$ is among the first $kq + 1$ q-grams of $r$, and in the same way among the first $kq + 1$ of $s$. An inverted index on these prefixes finds the candidates. A string too short for the assumption must be compared without this filter.
- *Partition.* Cut $s$ into $k + 1$ nonempty segments. A script of at most $k$ operations changes at most $k$ of them, so one segment of $s$ occurs unchanged in $r$, by the [pigeonhole principle](/pigeonhole-filtering/). Pass-Join also bounds where in $r$ the segment can start, and indexes the segments of the shorter strings.

Ordering the q-grams by increasing frequency puts rare q-grams in the prefixes, which keeps the inverted lists short. The filters reduce the candidates in practice, but none of them gives a worst-case bound better than the nested loops. Jiang, Li, Feng and Li compare these algorithms experimentally on real data sets.

## Bounds

- **Output.** If all strings are equal, the output has $|R| \cdot |S|$ pairs, so every algorithm takes $\Omega(|R| \cdot |S|)$ time in the worst case when it must list the output.
- **Upper bound.** Nested loops with a banded check take $O(|R| \cdot |S| \cdot k \ell)$ time, where $\ell$ is the largest length.
- **Conditional lower bound.** Even the decision version, "is the output empty", has no algorithm in time $O(n^{2-\delta} \ell^{c})$ for $|R| = |S| = n$ and constants $\delta > 0$ and $c$, unless the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) fails. This holds for the Levenshtein distance over an alphabet of $O(\ell)$ symbols, and for the Hamming distance over a binary alphabet. The proof is the reduction from orthogonal vectors below. So a fast join must depend on the data, for example on a small $k$, on short strings or on few candidate pairs.

## Reductions

- **From orthogonal vectors, Hamming.** Let $A$ and $B$ be lists of $n$ vectors in $\{0, 1\}^d$, an instance of [orthogonal vectors](/orthogonal-vectors/). Map each coordinate of a vector of $A$ by $0 \mapsto \texttt{000}$ and $1 \mapsto \texttt{011}$, and each coordinate of a vector of $B$ by $0 \mapsto \texttt{001}$ and $1 \mapsto \texttt{100}$. The two blocks of a coordinate differ in 3 places when both bits are 1, and in 1 place otherwise. So the images of $a$ and $b$ have Hamming distance $d + 2\, a \cdot b$, and the join with threshold $k = d$ is nonempty if and only if some pair is orthogonal. The strings have length $3d$.
- **From orthogonal vectors, edit distance.** Backurs and Indyk build strings $G_1(a)$ and $G_2(\hat b)$ of length $O(d)$ with $\mathrm{ed}(G_1(a), G_2(\hat b)) = 10(d + 1) + \min(a \cdot b, 1)$; see the [edit distance hardness theorem](/edit-distance-hardness/). So the join of $(G_1(a))_{a \in A}$ and $(G_2(\hat b))_{b \in B}$ with $k = 10(d + 1)$ is nonempty if and only if some pair is orthogonal. With the reduction from CNF satisfiability to orthogonal vectors, either reduction gives the conditional lower bound above.
- **To dictionary lookup.** Build an index on $S$ for [approximate dictionary lookup](/approximate-dictionary-lookup/), such as a [trie](/trie/) or a [BK-tree](/bk-tree/), and query it with each string of $R$.
- **To set similarity join.** The count and prefix filters turn the edit distance threshold into a lower bound on the overlap of q-gram multisets, so the candidate step is a [set similarity join](/set-similarity-join/) with an overlap threshold that depends on the lengths. The exact check stays necessary, since a large overlap does not imply a small edit distance.

## Applications

- **Data cleaning and record linkage.** Find the same customer, product or address in two databases where the names have typing errors and different spellings.
- **Duplicate detection.** A self-join of one table finds near-duplicate records before they are merged.
- **Query logs and spelling.** Group misspelled search queries with their correct forms.
- **Biological sequences.** Group short reads or barcodes that differ by a few sequencing errors.

## References
