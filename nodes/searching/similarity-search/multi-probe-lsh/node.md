---
tag: 9SW2DV
kind: algorithm
slug: multi-probe-lsh
name: Multi-probe LSH
area: searching/similarity-search
level: advanced
summary: Probes several nearby buckets per hash table so fewer tables are needed for the same recall.
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, M: the number of hash functions per table, L: the number of tables, T: the number of extra probes per table, E: the number of sets extracted from the heap per table, C: the number of candidates}
  time: {build: Θ(n L M d), query: O(L (M d + M log M + E (M + log E)) + C d)}
  space: {index: Θ(n L + L M d)}
properties: {deterministic: false, online: false}
history:
  year: 2007
  people: [Qin Lv, William Josephson, Zhe Wang, Moses Charikar, Kai Li]
  note: Lv, Josephson, Wang, Charikar and Li proposed the query-directed probing sequence for p-stable LSH at VLDB 2007.
prereqs: [e2lsh, locality-sensitive-hashing, priority-queue]
see_also: [e2lsh, locality-sensitive-hashing, lsh-amplification, lsh-forest, p-stable-distribution, approximate-nearest-neighbor, nearest-neighbor-search, random-hyperplane-lsh]
sources:
  - paper: "Qin Lv, William Josephson, Zhe Wang, Moses Charikar and Kai Li, Multi-probe LSH: efficient indexing for high-dimensional similarity search, Proceedings of the 33rd International Conference on Very Large Data Bases (VLDB 2007)"
    locator: pages 950 to 961 (Section 4, the perturbation vectors, the step-wise and query-directed probing sequences, the score, and the generation by shift and expand with a heap; Section 6, the experiments on image and audio features)
  - paper: doi:10.1145/997817.997857
    title: Mayur Datar, Nicole Immorlica, Piotr Indyk and Vahab S. Mirrokni, Locality-sensitive hashing scheme based on p-stable distributions, Proceedings of the 20th Annual Symposium on Computational Geometry (SoCG 2004)
    locator: pages 253 to 262 (the hash family h(v) = floor((a·v + b)/w) and its collision probability)
  - paper: "Rina Panigrahy, Entropy based nearest neighbor search in high dimensions, Proceedings of the 17th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2006)"
    locator: pages 1186 to 1195 (probing the buckets of random points near the query, with O(1) tables or near-linear space)
---

Multi-probe LSH is a way to query an [E2LSH](/e2lsh/) index that looks in several buckets of each hash table instead of one. Besides the bucket of the query, it probes the buckets whose keys differ from it by $\pm 1$ in a few coordinates, in order of a score that measures how close the query lies to the corresponding slot boundaries. A near neighbor that missed the query's bucket by a small margin is found in a neighboring one. The index is unchanged; only the query differs. Each probe can only add candidates, so the success probability is at least that of E2LSH with the same tables. Lv, Josephson, Wang, Charikar and Li proposed it in 2007 to cut the number of tables, and so the memory, of LSH. They reported 14 to 18 times fewer tables than basic LSH for the same recall. There is no worst-case bound on the number of probes needed.

## In plain words

Plain LSH cuts the space into cells by random rulers and stores each point in its cell. A query looks only in its own cell. A close neighbor sitting just across a cell wall is missed. To catch it anyway, plain LSH builds many independent sets of cells, which costs a lot of memory.

Multi-probe LSH builds fewer sets and looks in more cells of each. For every ruler it notes how far the query is from the wall on each side. A wall that is very near is likely to have cut off a neighbor, so the cell across that wall is checked first. Then the next most likely cell, and so on, for a fixed number of looks. A small priority list makes these cells come out in the right order without listing them all.

## The problem

Given $n$ points in $\mathbb{R}^d$ and a query $q$, find a point close to $q$ in the [Euclidean distance](/euclidean-distance/): the [approximate nearest neighbor](/approximate-nearest-neighbor/) problem, or its version with a radius $r$ and a factor $c > 1$. The index is that of E2LSH: $L$ tables, each with a key $g_t(v) = (h_{t,1}(v), \ldots, h_{t,M}(v))$ of $M$ functions $h(v) = \lfloor (a \cdot v + b)/w \rfloor$, with $a$ a standard Gaussian vector and $b$ uniform in $[0, w)$. The goal is to reach a given recall with fewer tables than E2LSH needs.

## The algorithm

For a hash function $h_j$ and the query $q$, let $f_j(q) = a_j \cdot q + b_j$, so that $h_j(q) = \lfloor f_j(q)/w \rfloor$, and let $x_j(-1) = f_j(q) - w\,h_j(q)$ and $x_j(+1) = w - x_j(-1)$ be the distances from $f_j(q)$ to the left and right ends of its slot. A *perturbation vector* is a $\Delta \in \{-1, 0, 1\}^M$, $\Delta \ne 0$, and it names the bucket $g(q) + \Delta$. Its **score** is

$$\mathrm{score}(\Delta) = \sum_{j : \Delta_j \ne 0} x_j(\Delta_j)^2.$$

A point $p$ with $\|p - q\| = u$ has $f_j(p) - f_j(q)$ distributed as $N(0, u^2)$, so it lands across the wall at gap $x$ with probability that decreases with $x$, roughly like $e^{-x^2 / 2u^2}$; a small score marks a likely bucket. To list the vectors in order of score, sort the $2M$ gaps as $z_1 \le z_2 \le \cdots \le z_{2M}$, each $z_i$ standing for a pair $(j, \delta)$. A set $A \subseteq \{1, \ldots, 2M\}$ stands for the vector with $\Delta_j = \delta$ for each pair of $A$; it is *valid* if it does not hold both pairs of the same $j$. With $\max A = m$, the operations are $\mathrm{shift}(A) = A \setminus \{m\} \cup \{m + 1\}$ and $\mathrm{expand}(A) = A \cup \{m + 1\}$.

```pseudo id=main
BUILD(P, M, L, w)
L1  for t ← 1 to L do draw a[t][1..M] Gaussian in ℝ^d and b[t][1..M] uniform in [0, w)
L2  for each p in P and t ← 1 to L do insert p in table T_t under the key g_t(p)

QUERY(q, T)                                 ▷ T extra probes per table
L3  C ← ∅
L4  for t ← 1 to L do
L5      for j ← 1 to M do compute f_j(q), h_j(q), x_j(−1) and x_j(+1)
L6      C ← C ∪ T_t[g_t(q)]                   ▷ the home bucket, as in E2LSH
L7      for each of the first T vectors Δ of PERTURBATIONS(x) do C ← C ∪ T_t[g_t(q) + Δ]
L8  return the point of C nearest to q, or none if C = ∅

PERTURBATIONS(x)                            ▷ yields the vectors Δ in order of score
L9  sort the 2M pairs (j, δ) by x_j(δ) into z_1 ≤ … ≤ z_2M
L10 H ← a min-heap holding the set {1}, keyed by score
L11 repeat: A ← EXTRACT-MIN(H)
L12     if max A < 2M then insert shift(A) and expand(A) into H
L13     if A is valid then yield the vector of A
```

Lines L1 and L2 are the E2LSH index. Line L5 costs $Md$ for the projections. Line L6 probes the home bucket, so the candidates always include those of E2LSH. Line L7 asks for vectors one at a time; the generator stops when the query stops asking. The score of $\mathrm{shift}(A)$ is the score of $A$ minus $z_m^2$ plus $z_{m+1}^2$, and that of $\mathrm{expand}(A)$ is the score of $A$ plus $z_{m+1}^2$, so each costs $O(1)$ to compute from its parent. Invalid sets are not yielded but must still be expanded, since their descendants can be valid.

## Example

Take one table, $M = 2$ and $w = 4$, and, to keep the numbers readable, the axis directions $a_1 = (1, 0)$, $a_2 = (0, 1)$ with $b_1 = 0.5$, $b_2 = 1$, so the buckets are the cells of a grid. The query $q = (3.2, 2.5)$ has $f_1 = 3.7$ and $f_2 = 3.5$, both in slot 0, so $g(q) = (0, 0)$ and

$$x_1(-1) = 3.7, \quad x_1(+1) = 0.3, \quad x_2(-1) = 3.5, \quad x_2(+1) = 0.5.$$

The sorted gaps are $0.3, 0.5, 3.5, 3.7$, for the pairs $(1, +1), (2, +1), (2, -1), (1, -1)$. The heap yields

| order | set | $\Delta$ | score |
|---|---|---|---|
| 1 | {1} | (+1, 0) | 0.09 |
| 2 | {2} | (0, +1) | 0.25 |
| 3 | {1, 2} | (+1, +1) | 0.34 |
| 4 | {3} | (0, −1) | 12.25 |
| 5 | {1, 3} | (+1, −1) | 12.34 |
| 6 | {4} | (−1, 0) | 13.69 |
| 7 | {2, 4} | (−1, +1) | 13.94 |
| 8 | {3, 4} | (−1, −1) | 25.94 |

The heap also pops the sets {2, 3}, {1, 2, 3}, {1, 4} and {1, 2, 4}, with scores 12.5, 12.59, 13.78 and 14.03, but each holds both pairs of one coordinate, so they are skipped. Every one of the 8 nonzero vectors of $\{-1, 0, 1\}^2$ appears once.

Let the data be $(1, 1)$, $(4.3, 2)$, $(2.5, 4.5)$, $(6, 6)$, $(-2, 5)$, $(9, 1)$, $(0, -3)$ and $(3, 0)$. The home bucket $(0, 0)$ holds $(1, 1)$ and $(3, 0)$, at distances 2.6627 and 2.5080 from $q$, and E2LSH with this one table answers $(3, 0)$. The first probe, bucket $(1, 0)$, adds $(4.3, 2)$ at distance 1.2083, the true nearest neighbor, which lies 0.6 beyond the right wall of the query's slot in the first coordinate. With $T = 4$ probes the candidates are 6 of the 8 points.

## Correctness

The probing sequence and the query satisfy three exact statements, proved in [the correctness proof](proofs/correctness.md).

1. **The sequence.** PERTURBATIONS yields each nonzero $\Delta \in \{-1, 0, 1\}^M$ exactly once, in nondecreasing order of score. The reason is that every nonempty $A \subseteq \{1, \ldots, 2M\}$ other than $\{1\}$ has exactly one parent, $A \setminus \{m\}$ if $m - 1 \in A$ and $A \setminus \{m\} \cup \{m - 1\}$ otherwise, where $m = \max A$, and a child never scores less than its parent.
2. **The answer.** QUERY returns the nearest point of $q$ among the points in the $L(T + 1)$ probed buckets, and these buckets include the $L$ home buckets of E2LSH.
3. **The success probability.** For any point $p$ with $\|p - q\| = u$, over the random choice of the functions, $\Pr[p \in C] \ge 1 - (1 - p(u)^M)^L$, where $p(u)$ is the E2LSH collision probability of one function. So every guarantee of [E2LSH](/e2lsh/) with $M$ and $L$ holds for multi-probe LSH with the same $M$ and $L$, for every $T \ge 0$. With $T = 3^M - 1$, every point whose key differs from $g_t(q)$ by at most 1 in each coordinate, for some $t$, is a candidate.

The gain of extra probes is empirical. For data where a near neighbor tends to fall in an adjacent bucket, a few probes per table raise the recall as much as many more tables would, but no bound in the literature guarantees how many probes replace one table.

## Complexity

In the real RAM, with $O(d)$ time for an inner product:

- **Build.** $L M$ projections per point, $\Theta(nLMd)$ time, and $\Theta(nL)$ space for the tables plus $\Theta(LMd)$ for the functions.
- **Query.** Per table, $Md$ for the projections and $O(M \log M)$ for the sort. Let $E \ge T$ be the number of sets extracted from the heap before the $T$-th valid one; invalid sets are extracted too. Each extraction costs $O(\log E)$, since the heap grows by at most 2 per extraction, plus $O(M)$ to test validity and form the key. Then $Cd$ for the distances to the $C$ distinct candidates. The total is $O(L(Md + M\log M + E(M + \log E)) + Cd)$. In the example, $E = 12$ for $T = 8$.

With $T = 0$ this is E2LSH. For the $T$ in use, small next to $3^M$, the probing cost per table is small next to the distance computations.

## Properties

- **Randomized.** The functions are random; the probing order is deterministic given the functions and the query.
- **Same index as E2LSH.** Any E2LSH index can be queried with multi-probing, and $T$ can change from query to query.
- **Monotone in $T$.** More probes give a superset of candidates, never a worse answer.

## Variants and improvements

- **Step-wise probing.** Probe all vectors with one nonzero coordinate, then all with two, and so on. It ignores the position of the query in its slots, and Lv et al. found it needs more probes than the query-directed order.
- **Expected scores.** Replace the gaps $x_j(\delta)$ by their expected values given their rank among the $2M$ gaps, $E[z_i^2]$, so that one probing sequence of sets can be computed once and reused for all queries; only the sort of line L9 stays per query.
- **A global order.** Merge the probing sequences of the $L$ tables in a single heap and spend a total budget of probes where the scores are smallest.
- **Entropy-based LSH (Panigrahy).** Hash random points near the query, at the distance of the expected neighbor, and probe their buckets. It achieves near-linear space with $O(1)$ tables in theory, but needs many probes; multi-probe LSH computes the likely buckets directly instead of sampling them.
- **Other families.** The same idea applies to bit-sampling and [random hyperplane](/random-hyperplane-lsh/) hashes: flip the bits whose projections lie closest to zero first. [LSH forests](/lsh-forest/) reach a related effect by shortening the keys instead of perturbing them.

## When to use it

Use multi-probe LSH when an E2LSH index needs too many tables to fit in memory for the recall you need: build a few tables and raise $T$ until the recall is enough. For very high recall at large scale, graph indexes such as [HNSW](/hnsw/) often answer faster, and when exact answers are needed in low dimension, a [k-d tree](/kd-tree/) is simpler.

## Pitfalls

- **Expecting a guarantee from the probes.** The theory of E2LSH covers only the home buckets; the parameters $M$ and $L$ must still be chosen for the target with $T = 0$ if a proven success probability is needed.
- **Too large a $T$.** Each table has only $3^M - 1$ perturbations, and probes far from the query mostly return far points. Beyond a few hundred probes, the candidates grow faster than the recall.
- **Width and $M$ chosen for E2LSH.** With multi-probing, a larger $M$, which gives smaller buckets, is usually better, since misses are recovered by probes. Tune $M$, $w$ and $T$ together on sample queries.
- **Forgetting invalid sets.** Skipping the shift and expansion of an invalid set loses valid descendants: in the example, the valid set $\{2, 4\}$ is the shift of the invalid set $\{2, 3\}$, and nothing else generates it.
- **Duplicates across tables.** The same point appears in many probed buckets; keep the candidates in a set, so that each distance is computed once.

## Implementations

## History

Datar, Immorlica, Indyk and Mirrokni introduced the p-stable hash family in 2004. Panigrahy proposed in 2006 to query an LSH index at random points near the query, to save tables. Qin Lv, William Josephson, Zhe Wang, Moses Charikar and Kai Li presented multi-probe LSH at VLDB 2007, with the query-directed probing sequence and its generation by shift and expand, and experiments on image and audio features.

## References
