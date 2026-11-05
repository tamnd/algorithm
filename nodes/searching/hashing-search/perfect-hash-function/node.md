---
tag: PHWQBJ
kind: definition
slug: perfect-hash-function
name: Perfect hash function
area: searching/hashing-search
level: core
summary: Injective hash function on a fixed key set, so lookups need no collision handling.
prereqs: [hash-function, hash-collision, static-dictionary-problem]
see_also: [perfect-hashing, minimal-perfect-hash-function, fks-perfect-hashing, chd-hashing, birthday-paradox, universal-hash-family, direct-address-table, static-dictionary-lower-bound]
sources:
  - paper: doi:10.1145/828.1884
    title: Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3) (1984)
    locator: pages 538 to 544 (a perfect hash function for n keys with O(n) space and constant evaluation time)
  - paper: doi:10.1137/0605009
    title: Michael L. Fredman and Janos Komlos, On the size of separating systems and families of perfect hash functions, SIAM Journal on Algebraic and Discrete Methods 5(1) (1984)
    locator: pages 61 to 68 (lower bounds on the number of functions in a family that contains a perfect hash function for every set of a given size)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 11 (Hash tables), the treatment of perfect hashing with two levels of universal hashing
---

A perfect hash function for a set $S$ of keys is a [hash function](/hash-function/) that maps the keys of $S$ to distinct slots, so a table built with it has no [collisions](/hash-collision/) on $S$ and a search reads exactly one slot. Perfection is a property of a function together with a fixed key set: no function into $m < |U|$ slots is perfect for every set, so the function is computed after the keys are known, which makes it a tool for the [static dictionary problem](/static-dictionary-problem/). When the number of slots equals the number of keys, the function is a [minimal perfect hash function](/minimal-perfect-hash-function/). This page gives the definitions, the chance that a random function is perfect, and the counting bound on how many bits any perfect hash function needs.

## Definition

Let $U$ be a universe of keys with $|U| = u$, let $S \subseteq U$ with $|S| = n$, and let $m \ge 1$. Write $[m] = \{0, \ldots, m - 1\}$.

**Perfect hash function.** A function $h : U \to [m]$ is *perfect for $S$* if its restriction to $S$ is injective: $h(x) \ne h(y)$ for all distinct $x, y \in S$. This requires $m \ge n$. The ratio $n/m$ is its *load*.

**Minimal and order-preserving.** A perfect hash function with $m = n$ is *minimal*: it is a bijection from $S$ onto $[n]$. It is *order-preserving* if it is minimal and maps the keys of $S$ in increasing order to $0, 1, \ldots, n - 1$, so that it computes the rank of each key.

**Values outside $S$.** The definition says nothing about keys outside $S$. A perfect hash function may map such a key to any slot, so a table that must answer "not present" stores the key of each slot and compares. A function that only maps $S$ correctly, with no stored keys, answers membership only for keys known to be in $S$.

**Perfect family.** A family $\mathcal{H}$ of functions from $U$ to $[m]$ is *$(u, m, n)$-perfect* if for each $S \subseteq U$ with $|S| = n$ some $h \in \mathcal{H}$ is perfect for $S$. A perfect hash function is then stored as the index of one member of the family, which takes $\lceil \lg |\mathcal{H}| \rceil$ bits.

**Two basic facts.**

1. **(A random function.)** If $h$ is a uniformly random function from $U$ to $[m]$, then for each fixed $S$ of size $n$,
$$\Pr[h \text{ is perfect for } S] = \frac{m (m - 1) \cdots (m - n + 1)}{m^n} = \prod_{i=0}^{n-1} \left(1 - \frac{i}{m}\right) \le e^{-n(n-1)/(2m)}.$$
*Proof.* The values $h(x)$ for $x \in S$ are independent and uniform, and the number of injective lists of $n$ values out of $m$ is $m(m-1)\cdots(m-n+1)$. The bound uses $1 - t \le e^{-t}$ and $\sum_{i < n} i = n(n-1)/2$. $\square$

With a [universal family](/universal-hash-family/) instead, the expected number of colliding pairs is at most $\binom{n}{2}/m$, so for $m \ge n^2$ the function is perfect with probability more than $1/2$, by Markov's inequality. This is the second level of [FKS perfect hashing](/fks-perfect-hashing/).

2. **(Counting bound.)** Every $(u, m, n)$-perfect family has
$$|\mathcal{H}| \ge \frac{\binom{u}{n}}{\binom{m}{n} (u/m)^n}.$$
*Proof.* Fix $h$, and let $c_j$ be the number of keys of $U$ with $h(x) = j$. A set $S$ on which $h$ is perfect picks one key from each of $n$ distinct slots, so $h$ is perfect for $e_n(c_0, \ldots, c_{m-1}) = \sum_{j_1 < \cdots < j_n} c_{j_1} \cdots c_{j_n}$ sets. Under the condition $\sum_j c_j = u$, this symmetric sum is largest when all $c_j$ are equal to $u/m$ (by Maclaurin's inequality, $e_n(c) \le \binom{m}{n} (u/m)^n$). So each function is perfect for at most $\binom{m}{n}(u/m)^n$ of the $\binom{u}{n}$ sets, and the family needs at least the ratio. $\square$

Taking $\lg$ of the bound gives the number of bits that any program for a perfect hash function needs in the worst case over $S$. For $u$ much larger than $m$, it is about $\lg (m^n / (m(m-1)\cdots(m-n+1)))$, the $\lg$ of the inverse of the probability in Fact 1. With $m = \beta n$ for a constant $\beta \ge 1$, this is about
$$n \lg e \left(1 + (\beta - 1) \ln\left(1 - \frac{1}{\beta}\right)\right) \text{ bits},$$
which is $n \lg e \approx 1.443\,n$ bits for $\beta = 1$, about $0.443\,n$ bits for $\beta = 2$ and about $0.198\,n$ bits for $\beta = 4$. The counting argument is due to Mehlhorn (1982). Fredman and Komlos sharpened the lower bounds on perfect families.

## Examples and non-examples

**A minimal perfect function found by search.** Let $S = \{3, 8, 12, 17\}$ and $m = 4$. The function $x \bmod 4$ maps $S$ to $3, 0, 0, 1$ and is not perfect. The function $h(x) = (x \bmod 11) \bmod 4$ maps $S$ to $3, 0, 1, 2$, so it is a minimal perfect hash function for $S$. It is not order-preserving, since $3 \mapsto 3$ but $8 \mapsto 0$. With $m = 6$, already $x \bmod 6$ maps $S$ to $3, 2, 0, 5$ and is perfect, at load $2/3$.

**The birthday numbers.** For $n = 23$ keys and $m = 365$ slots, a random function is perfect with probability $\prod_{i<23}(1 - i/365) \approx 0.4927$, the [birthday paradox](/birthday-paradox/). For $n = 10$ and $m = 100$ it is about $0.628$. For $n = m = 10$ it is $10!/10^{10} \approx 3.6 \cdot 10^{-4}$: a random function is almost never minimal perfect, which is why constructions of minimal perfect functions search a structured family instead. For $n = 1000$ and $m = n^2$, the probability is about $0.607$, close to the estimate $e^{-n(n-1)/(2m)} \approx 0.607$.

**A small perfect family.** Let $u = 6$, $n = 3$ and $m = 3$. The counting bound gives $|\mathcal{H}| \ge \binom{6}{3}/(\binom{3}{3} \cdot 2^3) = 20/8 = 2.5$, so any family that has a minimal perfect function for each of the 20 three-key subsets of a six-key universe has at least 3 functions.

**The identity on a small universe.** If $m \ge u$, the identity map, or any injection of $U$ into $[m]$, is perfect for every $S$. This is the [direct-address table](/direct-address-table/), and it is the only case in which one fixed function is perfect for all sets.

**Non-example: a fixed function and an unknown set.** If $m < u$, every fixed $h$ maps two keys $x \ne y$ of $U$ to the same slot, by the [pigeonhole principle](/pigeonhole-principle/), so $h$ is not perfect for any set that contains both. A perfect hash function must therefore depend on $S$.

**Non-example: a perfect function that is too expensive.** A table that lists the keys of $S$ in sorted order with their slots is a perfect function, but evaluating it needs a [binary search](/binary-search/) in $\Theta(\log n)$ time. The useful perfect hash functions take $O(1)$ time to evaluate on the [word RAM](/word-ram/), and the constructions aim at $O(1)$ time and few bits together.

## Related definitions

- [Minimal perfect hash function](/minimal-perfect-hash-function/): the case $m = n$, with its own space bound of about $1.44$ bits per key.
- [Perfect hashing](/perfect-hashing/): the concept page for the methods that build perfect hash functions and the tables that use them.
- [FKS perfect hashing](/fks-perfect-hashing/): the two-level scheme of Fredman, Komlos and Szemeredi with $O(n)$ space and $O(1)$ worst-case search.
- [CHD hashing](/chd-hashing/): a practical construction that compresses the per-bucket displacements to about 2 bits per key.
- [Static dictionary problem](/static-dictionary-problem/) and [static dictionary lower bound](/static-dictionary-lower-bound/): the problem that perfect hash functions solve, and the limits on its space and time.
- [Hash collision](/hash-collision/): the event that a perfect hash function rules out on $S$.

## References
