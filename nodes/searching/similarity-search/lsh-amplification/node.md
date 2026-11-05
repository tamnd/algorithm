---
tag: VQ354Z
kind: technique
slug: lsh-amplification
name: LSH amplification by banding
aliases:
- AND-OR amplification
- banding
area: searching/similarity-search
level: core
summary: Combine k hashes by AND and L tables by OR to sharpen the gap between near and far collision probabilities.
prereqs: [locality-sensitive-hash-family]
see_also: [locality-sensitive-hashing, minhash, bit-sampling-lsh, e2lsh, multi-probe-lsh, lsh-forest, simhash]
sources:
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Section 3.4 Locality-Sensitive Hashing for Documents (the banding of minhash signatures, the S-curve 1 − (1 − s^r)^b and its threshold near (1/b)^(1/r)) and Section 3.6.3 Amplifying a Locality-Sensitive Family (AND- and OR-constructions)
  - paper: doi:10.4086/toc.2012.v008a014
    title: Sariel Har-Peled, Piotr Indyk and Rajeev Motwani, Approximate nearest neighbor, towards removing the curse of dimensionality, Theory of Computing 8, 2012
    locator: Section 3 (the concatenation of k functions and the L tables, with k = log_{1/p2} n and L = n^ρ / p1)
  - paper: doi:10.1145/1327452.1327494
    title: Alexandr Andoni and Piotr Indyk, Near-optimal hashing algorithms for approximate nearest neighbor in high dimensions, Communications of the ACM 51(1), 2008
    locator: pages 117 to 122 (the LSH algorithm with k concatenated functions and L tables, and its analysis)
---

LSH amplification turns a weak [locality-sensitive hash family](/locality-sensitive-hash-family/), whose collision probabilities $p_1$ for near pairs and $p_2$ for far pairs may be close, into a sharp filter. It concatenates $k$ functions, so that a pair collides only if all $k$ agree (an AND), and it builds $L$ such tables, so that a pair is a candidate if it collides in at least one table (an OR). A pair with collision probability $p$ for one function then becomes a candidate with probability $1 - (1 - p^k)^L$, an S-shaped curve whose step can be put at any threshold. It is the core of [locality-sensitive hashing](/locality-sensitive-hashing/), where the band sizes $k = \lceil \log_{1/p_2} n \rceil$ and $L = \lceil n^\rho / p_1 \rceil$ give a query time near $n^\rho$.

## In plain words

One random hash puts similar items together often, but it also puts many dissimilar items together. To be stricter, ask for many hashes to agree at once. Then dissimilar items almost never match, but similar items also match less often.

To get the similar items back, make many such strict tests, each with its own random hashes, and keep an item if it passes any one of them. A similar item has many chances, so it almost surely passes one. A dissimilar item fails each test with high probability, so it rarely passes any.

With the right number of hashes in each test and the right number of tests, items above a chosen similarity are kept almost always, and items below it are dropped almost always.

## When it applies

- You have a family of random functions in which the probability that two items get the same value grows with their similarity, and no single function separates near from far well enough.
- You can afford a little more memory (one table for each OR term) and more hash evaluations, in exchange for far fewer comparisons of full items.
- The goal is a candidate set: a later step checks each candidate with the true distance, so false positives cost time and false negatives cost recall.
- The similarity threshold is known, or there is a target radius $r$ as in the [$(c, r)$-near neighbor](/c-approximate-nearest-neighbor/) problem.

## The template

The holes are the family $\mathcal{H}$, the band size $k$, the number of bands $L$, and the check of a candidate.

```pseudo id=main
BUILD(P, ℋ, k, L)
L1  for j ← 1 to L do
L2      draw h_{j,1}, …, h_{j,k} from ℋ, all independent
L3      g_j(x) ← (h_{j,1}(x), …, h_{j,k}(x))            ▷ AND of k functions
L4      T_j ← a hash table that maps each key g_j(x) to the list of x ∈ P with that key

CANDIDATES(q)
L5  C ← ∅
L6  for j ← 1 to L do C ← C ∪ T_j[g_j(q)]           ▷ OR over L tables
L7  return the points of C that pass the check, for example δ(q, x) ≤ c r
```

Line L3 makes a key from $k$ values. Two points have the same key in table $j$ only if all $k$ functions agree. Line L6 collects the points that share a key with $q$ in at least one table. Line L7 removes the false positives.

**The amplified probability.** Let one function give a pair $(x, q)$ the collision probability $p$. The $k$ functions of a band are independent, so the pair has the same key in band $j$ with probability $p^k$. The $L$ bands are independent, so the pair is in no band with probability $(1 - p^k)^L$, and

$$P_{k,L}(p) = \Pr[x \in C] = 1 - (1 - p^k)^L.$$

$P_{k,L}$ is increasing in $p$, so a family that is $(r_1, r_2, p_1, p_2)$-sensitive gives the candidate rule probabilities at least $P_{k,L}(p_1)$ for pairs within $r_1$ and at most $P_{k,L}(p_2)$ for pairs at distance $r_2$ or more.

**The AND alone keeps the exponent.** The family of keys $g$ is $(r_1, r_2, p_1^k, p_2^k)$-sensitive, and $\ln(1/p_1^k) / \ln(1/p_2^k) = \ln(1/p_1)/\ln(1/p_2) = \rho$. The AND makes both probabilities small. The OR then lifts the near probability back up with $L \approx 1/p_1^k$ tables, while the expected number of far collisions stays at $L\, n\, p_2^k$.

**The choice for LSH.** With $n$ points, take $k = \lceil \log_{1/p_2} n \rceil$ and $L = \lceil n^\rho / p_1 \rceil$. Then $p_2^k \le 1/n$, so each table holds at most one far point in the bucket of $q$ in expectation, and $L$ tables hold at most $L$. Also $k < \log_{1/p_2} n + 1$, so $p_1^k > p_1 \cdot p_1^{\log_{1/p_2} n} = p_1 n^{-\rho}$, so $L p_1^k \ge 1$ and a near point is missed in all tables with probability at most $(1 - p_1^k)^L \le e^{-L p_1^k} \le 1/e$. The page [locality-sensitive hashing](/locality-sensitive-hashing/) completes this into the full guarantee.

**The threshold of the S-curve.** For $b$ bands of $r$ rows (the notation of Leskovec, Rajaraman and Ullman, with $r = k$ and $b = L$), at $p = (1/b)^{1/r}$ the curve is $1 - (1 - 1/b)^b$, which is near $1 - 1/e \approx 0.63$ for large $b$. So the step of the curve is near $(1/b)^{1/r}$. More rows make the step steeper. More bands move it to the left.

## Classic examples

- **[MinHash](/minhash/) for near-duplicate documents.** Split a signature of $n = br$ minhash values into $b$ bands of $r$ rows. Two documents with [Jaccard similarity](/jaccard-similarity/) $s$ become candidates with probability $1 - (1 - s^r)^b$. With $b = 20$ and $r = 5$ the curve is:

  | $s$ | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 |
  |---|---|---|---|---|---|---|---|---|
  | $1 - (1 - s^5)^{20}$ | 0.0064 | 0.0475 | 0.1860 | 0.4701 | 0.8019 | 0.9748 | 0.9996 | 1.0000 |

  The threshold estimate is $(1/20)^{1/5} \approx 0.549$. With $b = 10$ and $r = 10$ the same 100 values give a step near $(1/10)^{1/10} \approx 0.794$: the curve is $0.0097$ at $s = 0.5$ and $0.6789$ at $s = 0.8$.
- **[Bit sampling](/bit-sampling-lsh/) in the Hamming cube.** For $n = 10^6$ points in $\{0, 1\}^{100}$, $r_1 = 10$ and $r_2 = 20$, so $p_1 = 0.9$, $p_2 = 0.8$ and $\rho \approx 0.4722$. Then $k = \lceil \ln 10^6 / \ln 1.25 \rceil = 62$ and $L = \lceil n^{\rho}/p_1 \rceil = 757$. A pair at distance 10 is a candidate with probability $1 - (1 - 0.9^{62})^{757} \approx 0.981$, and the expected number of far candidates is at most $L\, n\, p_2^{k} \approx 742$, against $10^6$ for a scan.
- **[Locality-sensitive hashing](/locality-sensitive-hashing/)** in general, with any family: [random hyperplanes](/random-hyperplane-lsh/) for the angle, [E2LSH](/e2lsh/) for $\ell_2$.
- **[SimHash](/simhash/) with permuted tables.** To find fingerprints within Hamming distance 3 of 64 bits, split the bits into blocks and use one table for each choice of blocks that must agree exactly. This is an AND inside each table and an OR over the tables, with blocks chosen so that no near pair is missed.

## Variations

- **OR then AND.** Leskovec, Rajaraman and Ullman also compose in the other order, $(1 - (1 - p)^b)^r$, and repeat the two constructions. Each composition pushes $p_1$ toward 1 and $p_2$ toward 0, at the cost of more hash evaluations, but adds no tables.
- **Multi-probe.** [Multi-probe LSH](/multi-probe-lsh/) looks also at the buckets of keys that differ from $g_j(q)$ in a few positions, which acts like more bands without more tables.
- **Variable $k$.** [LSH forest](/lsh-forest/) stores each key as a prefix tree, so a query can use the longest band that still finds enough candidates. This removes the need to fix $k$ in advance.
- **Covering designs.** For the Hamming distance, the bands can be chosen deterministically so that each pair within distance $r$ collides in at least one table, which gives LSH with no false negatives.

## Pitfalls

- **Dependent functions.** Line L2 must draw the $k \cdot L$ functions independently. If the same $k$ functions are reused in two tables, the two tables are copies and the OR adds nothing. If the $k$ functions of one band are dependent (for example, overlapping bits), $p^k$ is wrong.
- **Hashing the tuple badly.** The key of line L3 is a tuple. Storing it as a sum or an XOR of the $k$ values, without care, makes unrelated keys equal and adds false positives. Use the tuple, or a good hash of it.
- **Too large a $k$.** With $k$ so large that $p_1^k L \ll 1$, near points are missed. Check $L p_1^k \ge 1$, or compute $P_{k,L}(p_1)$ for the target recall before you build.
- **Forgetting the check.** The candidates of line L6 include far points. Without line L7 the output is not an answer to the $(c, r)$-near neighbor problem.
- **Counting far collisions with $n$ instead of the bucket.** Each table can return a bucket of many points that share one key. Bound the work by stopping after $O(L)$ candidates, as LSH does, or the worst case is a full scan.

## Exercises

1. With $b$ bands of $r$ rows, show that $P(s) = 1 - (1 - s^r)^b$ is increasing in $s$ on $[0, 1]$, and that $P(0) = 0$ and $P(1) = 1$.
2. A system uses $n = 120$ minhash values and wants pairs with $J \ge 0.7$ found with probability at least $0.95$, and pairs with $J \le 0.3$ kept with probability at most $0.06$. Find all splits $(b, r)$ with $br = 120$ that meet both rules.
3. Show that the AND of $k$ functions does not change $\rho$, but that the OR of $L$ functions with $L \ge 2$ does change it, by computing $\ln(1/P)/\ln(1/Q)$ for $P = 1 - (1 - p_1)^2$ and $Q = 1 - (1 - p_2)^2$ with $p_1 = 0.5$ and $p_2 = 0.25$.

## References
