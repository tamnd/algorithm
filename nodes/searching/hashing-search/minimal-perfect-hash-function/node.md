---
tag: 4XPV55
kind: definition
slug: minimal-perfect-hash-function
name: Minimal perfect hash function
aliases:
- MPHF
area: searching/hashing-search
level: core
summary: Perfect hash function whose range is exactly the key set size.
prereqs: [perfect-hash-function, hash-function, static-dictionary-problem]
see_also: [minimal-perfect-hashing, perfect-hashing, chd-hashing, fks-perfect-hashing, bloomier-filter, rank-select-dictionary, static-dictionary-lower-bound, direct-address-table]
sources:
  - paper: doi:10.1007/3-540-44693-1_28
    title: Torben Hagerup and Torsten Tholey, Efficient minimal perfect hashing in nearly minimal space, STACS 2001, Lecture Notes in Computer Science 2010
    locator: pages 317 to 326 (the space bound n log e + log log u plus or minus O(log n) bits for a minimal perfect hash function)
  - paper: doi:10.1007/978-3-642-04128-0_61
    title: Djamal Belazzougui, Fabiano C. Botelho and Martin Dietzfelbinger, Hash, displace, and compress, ESA 2009, Lecture Notes in Computer Science 5757
    locator: pages 682 to 693, Section 2 (the lower bound of about n / ln 2 bits)
  - url: https://arxiv.org/abs/2506.06536
    title: Hans-Peter Lehmann, Thomas Mueller, Rasmus Pagh, Giulio Ermanno Pibiri, Peter Sanders, Sebastiano Vigna and Stefan Walzer, Modern minimal perfect hashing, a survey
    locator: the definitions of minimal, order-preserving and monotone minimal perfect hash functions, and the space lower bounds
---

A minimal perfect hash function for a set $S$ of $n$ keys is a [perfect hash function](/perfect-hash-function/) with exactly $n$ slots: it maps the keys of $S$ one to one onto $\{0, 1, \ldots, n - 1\}$. It numbers the keys of a fixed set without gaps, so an array of exactly $n$ entries indexed by it holds one record per key. Any such function needs about $n \lg e \approx 1.443\,n$ bits in the worst case when the universe is large, and one that must also give each key a prescribed number needs about $n \lg n$ bits. The methods that build these functions, such as hash-and-displace and hypergraph peeling, are on the [minimal perfect hashing](/minimal-perfect-hashing/) page; this page fixes the definitions and their limits.

## Definition

Let $U$ be a universe with $|U| = u$, and let $S \subseteq U$ with $|S| = n \ge 1$. Write $[n] = \{0, \ldots, n - 1\}$.

**Minimal perfect hash function.** A function $h : U \to [n]$ is a *minimal perfect hash function* (MPHF) for $S$ if its restriction to $S$ is a bijection from $S$ onto $[n]$. Equivalently, it is a perfect hash function for $S$ with $m = n$ slots, so its load is 1. Its values outside $S$ are arbitrary.

**Order-preserving.** Given a bijection $\sigma : S \to [n]$ fixed in advance, an MPHF $h$ is *order-preserving for $\sigma$* if $h(x) = \sigma(x)$ for each $x \in S$. The function then stores an arbitrary numbering of the keys, chosen by the user.

**Monotone.** If $U$ is totally ordered, an MPHF is *monotone* if it is order-preserving for the rank map, that is $x < y$ implies $h(x) < h(y)$ for all $x, y \in S$. It maps each key of $S$ to its rank in $S$, so it is the [rank](/rank-select-dictionary/) query of $S$ restricted to keys that are in $S$.

**The costs.** An MPHF is judged by three numbers: the bits that describe it, the time to evaluate $h(x)$, and the time to build it from $S$. The target is $O(1)$ evaluation time on the [word RAM](/word-ram/), linear build time, and a number of bits close to the lower bounds below.

**Space bounds.** Let $\mathcal{F}$ be a set of functions from $U$ to $[n]$ that contains an MPHF for each $S$ of size $n$, and let $\mathcal{F}_\sigma$ contain an order-preserving MPHF for each pair $(S, \sigma)$. A scheme that describes its function with $b$ bits for every input can describe at most $2^b$ functions, so $b \ge \lg |\mathcal{F}|$ and $b \ge \lg |\mathcal{F}_\sigma|$.

1. **(Minimal.)** $|\mathcal{F}| \ge \binom{u}{n} (n/u)^n$, which is $n \lg e - O(\log n)$ bits when $u \ge n^2$.
2. **(Order-preserving.)** $|\mathcal{F}_\sigma| \ge n! \binom{u}{n} (n/u)^n$, which is at least $n \lg n + n \lg(1 - n/u)$ bits, so $n \lg n - 2$ bits when $u \ge n^2$ and $n \ge 2$.

*Proof.* Fix $h$, and let $u_j = |h^{-1}(j)|$ for $j \in [n]$, so $\sum_j u_j = u$. The function $h$ is an MPHF for $S$ exactly when $S$ takes one key from each set $h^{-1}(j)$. So $h$ serves $\prod_j u_j$ sets, and by the inequality of arithmetic and geometric means $\prod_j u_j \le (u/n)^n$. For the order-preserving case, $h$ determines $\sigma$ on each set that it serves, so it serves at most $(u/n)^n$ of the $n! \binom{u}{n}$ pairs $(S, \sigma)$. Covering all sets, or all pairs, gives the two bounds on the sizes. For the bits, $\binom{u}{n} n! = u (u - 1) \cdots (u - n + 1) \ge u^n (1 - n/u)^n$, so $\lg |\mathcal{F}_\sigma| \ge n \lg n + n \lg(1 - n/u)$, and $\lg |\mathcal{F}| \ge n \lg n - \lg n! + n \lg(1 - n/u) = n \lg e - O(\log n) + n \lg (1 - n/u)$ by Stirling's formula. When $u \ge n^2$, $n \lg(1 - n/u) \ge n \lg(1 - 1/n) \ge -2$ for $n \ge 2$. $\square$

The minimal bound is proved with sharper constants on the [minimal perfect hashing](/minimal-perfect-hashing/) page, and Hagerup and Tholey give its exact form $n \lg e + \lg \lg u \pm O(\log n)$. The order-preserving bound shows that such a function cannot be much smaller than a plain table of the $n$ numbers $\sigma(x)$, which takes $n \lceil \lg n \rceil$ bits once the keys are mapped to $[n]$ by any MPHF.

## Examples and non-examples

**A small MPHF.** Let $S = \{3, 8, 12, 17\}$. The function $h(x) = (x \bmod 11) \bmod 4$ maps 3, 8, 12 and 17 to 3, 0, 1 and 2, a bijection onto $[4]$, so it is an MPHF for $S$. It is not monotone, since $3 < 8$ but $h(3) = 3 > h(8) = 0$. For the key $5 \notin S$ it gives $h(5) = 1$, the slot of 12: an MPHF alone cannot tell that 5 is absent.

**A monotone MPHF.** For the same $S$, a table of the sorted keys $(3, 8, 12, 17)$ with a [binary search](/binary-search/) returns the ranks 0, 1, 2 and 3, so it is a monotone MPHF. It stores the keys, so it uses $\Theta(n \log u)$ bits and $O(\log n)$ time; the point of the definition is to do much better than this.

**How rare a random MPHF is.** A uniformly random function from $S$ to $[n]$ is a bijection with probability $n!/n^n$. For $n = 4, 8, 16$ this is about $1/10.7$, $1/416$ and $1/881\,658$. The brute-force methods split the keys into groups of a few keys and try seeds of a hash function on each group until one is a bijection, so a group of $k$ keys needs about $k^k/k!$ tries on average and a seed of about $\lg(k^k/k!)$ bits: 3.42 bits for $k = 4$, 8.70 bits for $k = 8$ and 19.75 bits for $k = 16$. Per key this is 0.86, 1.09 and 1.23 bits, rising toward $\lg e \approx 1.443$ as $k$ grows, which is the bound of Part 1 for that group size.

**The order-preserving bound in numbers.** For $n = 8$ and $u = 2^{32}$, Part 2 gives $\lg |\mathcal{F}_\sigma| \approx 24.0$ bits, which is $n \lg n = 24$, while Part 1 gives about 8.70 bits. Fixing the numbering in advance costs almost three times the space here, and the ratio grows like $\lg n / \lg e$.

**Non-example: a perfect function with spare slots.** The function $x \bmod 6$ maps $S = \{3, 8, 12, 17\}$ to 3, 2, 0 and 5. It is perfect but not minimal: the slots 1 and 4 are empty. A [rank structure](/rank-select-dictionary/) on the bit vector of used slots turns it into an MPHF, as shown on the [minimal perfect hashing](/minimal-perfect-hashing/) page.

**Non-example: the direct-address table.** When $S = U = \{0, \ldots, n - 1\}$, the identity is an MPHF, and the [direct-address table](/direct-address-table/) uses it. For any other $S$ the identity has a range larger than $n$ and is not minimal.

## Related definitions

- [Perfect hash function](/perfect-hash-function/): the general definition with $m \ge n$ slots, and the space bound for each load.
- [Minimal perfect hashing](/minimal-perfect-hashing/): the methods that build MPHFs in about 1.5 to 3 bits per key, and their uses.
- [CHD hashing](/chd-hashing/) and [FKS perfect hashing](/fks-perfect-hashing/): two constructions of perfect hash functions that can be made minimal.
- [Bloomier filter](/bloomier-filter/): a retrieval structure that stores a value per key of $S$ without the keys; an order-preserving MPHF is a retrieval structure for the values $\sigma(x)$.
- [Rank-select dictionary](/rank-select-dictionary/): the rank query, which a monotone MPHF answers for keys of $S$.
- [Static dictionary lower bound](/static-dictionary-lower-bound/): the limits for structures that must also reject keys outside $S$.

## References
