---
tag: VWBFM0
kind: algorithm
slug: fks-perfect-hashing
name: FKS perfect hashing
aliases:
- FKS hashing
- Fredman-Komlos-Szemeredi hashing
- Fredman-Komlos-Szemeredi perfect hashing
- two-level perfect hashing
area: data-structures/hashing
level: advanced
summary: Two-level universal hashing that gives O(n) space and worst-case O(1) static lookup.
solves: [static-dictionary-problem]
model: word-ram
complexity:
  vars: {n: the number of keys}
  time: {expected: O(n)}
  space: {extra: Θ(n)}
properties: {deterministic: false}
prereqs: [hash-table, universal-hash-family, perfect-hashing]
see_also: [dynamic-perfect-hashing, chd-hashing, perfect-hash-function, minimal-perfect-hashing, cuckoo-hashing, static-dictionary-lower-bound, universal-hashing]
sources:
  - paper: doi:10.1145/828.1884
    title: Michael L. Fredman, János Komlós and Endre Szemerédi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3), 1984
    locator: pages 538 to 544
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 11.5 (Perfect hashing)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.3 (Hash functions), the part on universal hashing
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 8 (Data structures), the section on hashing and perfect hashing
---

FKS perfect hashing stores a fixed set $S$ of $n$ keys in $\Theta(n)$ words so that a membership query takes $O(1)$ time in the worst case. It is a [hash table](/hash-table/) with two levels: a first hash function from a [universal family](/universal-hash-family/) splits $S$ into $n$ buckets, and each bucket of $n_j$ keys gets its own table of $n_j^2$ slots with a second hash function that has no [collision](/hash-collision/) on the bucket. The functions are found by random trials, and the expected build time is $O(n)$. It solves the [static dictionary problem](/static-dictionary-problem/) and is the base of [perfect hashing](/perfect-hashing/) and of [dynamic perfect hashing](/dynamic-perfect-hashing/).

## In plain words

Suppose you put a set of keys into a table with as many slots as keys. Some slots get several keys. A table with many more slots than keys, about the square of their number, almost never has two keys in one slot, but it is far too big.

FKS uses both facts. First, hash all the keys into a table of the normal size. Most slots get zero, one or two keys, and only a few get more. Then give each slot its own small table, with the square of its number of keys as its size, and a hash function of its own. For a small group of keys, a square-size table is cheap, and a random function puts each key in its own slot with good chance. If a function fails, try another one. A query computes two hash values and looks at one slot.

## The problem

The input is a set $S$ of $n$ distinct keys from the universe $U = \{0, 1, \ldots, p - 1\}$, where $p$ is a prime. The output is a structure that answers the query "is $x \in S$?" for each $x \in U$. This is the [static dictionary problem](/static-dictionary-problem/): the set does not change after the build. Each slot can also hold a value for its key, which gives a static map.

The hash functions come from the family of Carter and Wegman,

$$h_{a,b,m}(x) = ((a x + b) \bmod p) \bmod m, \qquad a \in \{1, \ldots, p - 1\}, \ b \in \{0, \ldots, p - 1\}.$$

For each $m \ge 1$ this family is universal: for each two distinct keys $x \ne y$ of $U$, a random choice of $(a, b)$ gives $h_{a,b,m}(x) = h_{a,b,m}(y)$ with probability at most $1/m$ (CLRS, Section 11.3).

## The algorithm

```pseudo id=main
FKS-BUILD(S)                               ▷ S: n distinct keys of {0, …, p − 1}
L1  m ← max(n, 1)
L2  repeat
L3      pick (a, b) at random; h ← h_{a,b,m}
L4      S_j ← {x ∈ S : h(x) = j} for j = 0, …, m − 1
L5  until Σ_j |S_j|² ≤ 4n
L6  for j ← 0 to m − 1 do
L7      m_j ← |S_j|²; T_j ← an array of m_j slots, all NIL
L8      if m_j > 0 then
L9          repeat pick (a_j, b_j) at random; h_j ← h_{a_j,b_j,m_j}
L10         until h_j(x) ≠ h_j(y) for all x ≠ y in S_j
L11         for each x in S_j do T_j[h_j(x)] ← x

FKS-SEARCH(x)
L12 j ← h(x)
L13 if m_j = 0 then return false
L14 return T_j[h_j(x)] = x
```

Lines L1 to L5 choose the first-level function. A trial is accepted when the sum of the squares of the bucket sizes is at most $4n$, because this sum is the total size of the second level. Lines L6 to L11 build the second level. For each nonempty bucket, line L9 draws a function into $m_j = n_j^2$ slots, and line L10 accepts it only if it is one-to-one on the bucket. Line L11 then stores each key in its own slot. An empty bucket gets no table and no function.

A search computes the bucket $j$ of $x$ (line L12). If the bucket is empty, $x$ is not in $S$ (line L13). Else $x$ can only be in the slot $h_j(x)$ of $T_j$, and line L14 compares it with the key stored there. So a search makes two hash evaluations and one comparison, in each case.

The test of line L10 uses the array $T_j$ itself: write the keys one by one, stop at the first slot that is already full, and clear the written slots before the next trial. So a trial costs $O(n_j)$ time.

## Example

Let $p = 101$ and $S = \{10, 22, 37, 40, 52, 60, 70, 72, 75\}$, so $n = m = 9$. These are the keys of the perfect hashing figure in CLRS, third edition.

| step | choice | result |
|---|---|---|
| L3, L4 | $(a, b) = (3, 42)$, $h(x) = ((3x + 42) \bmod 101) \bmod 9$ | $S_0 = \{10\}$, $S_2 = \{60, 72, 75\}$, $S_5 = \{70\}$, $S_7 = \{22, 37, 40, 52\}$, the other buckets empty |
| L5 | $\sum_j \lvert S_j \rvert^2 = 1 + 9 + 1 + 16 = 27 \le 36$ | accept $h$ |
| $j = 0$ | $m_0 = 1$, $(a_0, b_0) = (1, 0)$ | $T_0 = [10]$ |
| $j = 2$ | $m_2 = 9$, $(a_2, b_2) = (3, 1)$ | 60, 72, 75 go to slots 8, 6, 6: collision, reject |
| $j = 2$ | $(a_2, b_2) = (10, 18)$ | 60, 72, 75 go to slots 3, 4, 7: accept |
| $j = 5$ | $m_5 = 1$, $(a_5, b_5) = (1, 0)$ | $T_5 = [70]$ |
| $j = 7$ | $m_7 = 16$, $(a_7, b_7) = (10, 18)$ | 22, 37, 40, 52 go to slots 4, 5, 14, 1: accept |

The second level has $27$ slots, and the first level has 9 buckets, each with its size $m_j$ and its pair $(a_j, b_j)$.

Searches:

- $x = 75$: $h(75) = 2$ and $h_2(75) = ((750 + 18) \bmod 101) \bmod 9 = 61 \bmod 9 = 7$. $T_2[7] = 75$, so the answer is true.
- $x = 50$: $h(50) = 192 \bmod 101 \bmod 9 = 91 \bmod 9 = 1$. Bucket 1 is empty, so the answer is false.
- $x = 13$: $h(13) = 81 \bmod 9 = 0$, and $T_0[0] = 10 \ne 13$, so the answer is false.

## Correctness

When FKS-BUILD returns, each key $x \in S$ is stored in the slot $T_{h(x)}[h_{h(x)}(x)]$, and no slot holds two keys. The reason is that $x$ is in the bucket $S_{h(x)}$ by line L4, that $h_{h(x)}$ is one-to-one on this bucket by line L10, and that line L11 writes $x$ to that slot. So a search for $x \in S$ finds $x$, and a search for $y \notin S$ reads either an empty bucket or a slot that holds NIL or a key other than $y$, and returns false. Each trial of lines L3 to L5 and of lines L9 and L10 succeeds with probability more than $1/2$, so the build ends with probability 1. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The proofs are in [the complexity proof](proofs/complexity.md). The model is the [word RAM](/word-ram/) with $p < 2^w$, so $h_{a,b,m}(x)$ costs $O(1)$.

**First level.** Let $C$ be the number of pairs of keys of $S$ that collide under $h$. Each of the $\binom{n}{2}$ pairs collides with probability at most $1/m$, so $E[C] \le \binom{n}{2}/n = (n - 1)/2$. Each bucket of size $n_j$ has $\binom{n_j}{2}$ colliding pairs, and $n_j^2 = n_j + 2\binom{n_j}{2}$. Summing over $j$ gives

$$\sum_j n_j^2 = n + 2C, \qquad E\Big[\sum_j n_j^2\Big] \le n + (n - 1) = 2n - 1.$$

By [Markov's inequality](/markov-inequality/), $\Pr[\sum_j n_j^2 > 4n] \le (2n - 1)/(4n) < 1/2$. So each trial of line L5 succeeds with probability more than $1/2$, and the expected number of trials is less than 2. A trial costs $O(n)$, so the first level costs $O(n)$ expected time.

**Second level.** For a bucket of size $n_j \ge 2$ and $m_j = n_j^2$ slots, the expected number of colliding pairs is at most $\binom{n_j}{2}/n_j^2 < 1/2$, so a trial of line L10 succeeds with probability more than $1/2$ by Markov's inequality. The expected number of trials is less than 2, and each costs $O(n_j)$. Allocating the arrays costs $\sum_j m_j \le 4n$. So the second level costs $O(n)$ expected time, and the whole build takes $O(n)$ expected time.

**Space.** Line L5 guarantees $\sum_j m_j \le 4n$ slots in the second level, plus $O(m) = O(n)$ words for the first level. This is $\Theta(n)$ words in the worst case, not only in expectation.

**Search.** Two hash evaluations, two array reads and one comparison: $O(1)$ time in the worst case.

| quantity | bound | case |
|---|---|---|
| build time | $O(n)$ | expected, over the random choices |
| search time | $O(1)$ | worst case |
| space | $\Theta(n)$ words, at most $4n$ second-level slots | worst case |

## Properties

- **Las Vegas.** The answers are always right. Only the build time is random.
- **Static.** The set is fixed at the build. An insert can break line L10 for its bucket and line L5 for the whole table. [Dynamic perfect hashing](/dynamic-perfect-hashing/) handles updates.
- **Not minimal.** The table has more slots than keys. A [minimal perfect hash function](/minimal-perfect-hash-function/) maps the $n$ keys to exactly $n$ slots.
- **Stores the keys.** A search for a key not in $S$ must compare with the stored key in line L14. Without the keys, the structure cannot reject non-members.

## Variants and improvements

- **Smaller constants.** With a threshold $c n$ in line L5 and $m_j = 2 n_j^2$ in line L7, the trade-off between the number of trials and the space changes. CLRS, third edition, uses $m_j = n_j^2$ and the bound $E[\sum_j m_j] < 2n$.
- **Space $n + o(n)$.** Fredman, Komlós and Szemerédi also give a refinement that packs the second-level parameters and tables into $n + o(n)$ words.
- **Updates.** [Dynamic perfect hashing](/dynamic-perfect-hashing/) by Dietzfelbinger and others rebuilds a bucket when it grows, and rebuilds the whole table when $n$ grows too much. It gives $O(1)$ worst-case search and $O(1)$ expected amortized updates.
- **Practical perfect hashing.** [CHD](/chd-hashing/) uses one table of about $n$ slots and a small displacement for each bucket. It needs about 2 bits for each key when it stores only the function.
- **Worst-case $O(1)$ with two probes and updates.** [Cuckoo hashing](/cuckoo-hashing/) checks two slots and supports inserts in expected amortized $O(1)$ time.

## When to use it

Use FKS when the set of keys is fixed, when each query must take $O(1)$ time in the worst case, and when a few words of space for each key are acceptable. Examples are the keyword tables of compilers and read-only lookup tables. If the set changes, use [dynamic perfect hashing](/dynamic-perfect-hashing/) or [cuckoo hashing](/cuckoo-hashing/). If only the expected time matters, an ordinary [hash table](/hash-table/) is simpler. If space matters most, use a [minimal perfect hash function](/minimal-perfect-hashing/) such as [CHD](/chd-hashing/).

## Pitfalls

- **Linear second-level tables.** With $m_j = n_j$ in line L7 instead of $m_j = n_j^2$, the bound on the expected number of colliding pairs in a bucket is $(n_j - 1)/2$ instead of $1/2$. For a fully random function into $n_j$ slots, the chance of no collision is only $n_j!/n_j^{n_j}$, which is $24/256 \approx 0.094$ for $n_j = 4$, so a large bucket can need many trials. Use $m_j = n_j^2$.
- **No first-level check.** Without the test of line L5, a bad $h$ can put $\Theta(n)$ keys in one bucket, and then that bucket needs $\Theta(n^2)$ slots. Keep line L5.
- **Duplicate keys.** If $S$ holds a key twice, the two copies collide under every $h_j$, and the loop of lines L9 and L10 never ends. Remove duplicates first, or reject them.
- **Keys not below $p$.** The family is universal only for keys in $\{0, \ldots, p - 1\}$. Two keys that differ by a multiple of $p$ collide under every function. Choose a prime $p$ larger than every key, such as $2^{61} - 1$ for 60-bit keys.
- **The slot test.** Line L14 must compare the stored key with $x$. A test of "the slot is not NIL" answers true for each non-member that hashes to a full slot, such as $x = 13$ in the example.

## Implementations

The Python version takes a `random.Random` object, so that a test can fix the seed. Its default prime is $p = 2^{61} - 1$.

## History

Fredman, Komlós and Szemerédi presented the scheme at the IEEE Symposium on Foundations of Computer Science in 1982 and published it in the Journal of the ACM in 1984. It answered the question of whether a static set can be stored in linear space with constant worst-case query time. The two-level form with universal hash functions and squared bucket sizes, as on this page, is the version of CLRS, third edition, Section 11.5. Dietzfelbinger, Karlin, Mehlhorn, Meyer auf der Heide, Rohnert and Tarjan extended it to a dynamic dictionary in 1994.

## References
