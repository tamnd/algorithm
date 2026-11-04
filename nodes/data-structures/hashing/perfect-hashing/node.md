---
tag: 5SAP5S
kind: concept
slug: perfect-hashing
name: Perfect hashing
aliases:
- perfect hash function
- static dictionary with O(1) worst-case lookup
- static perfect hashing
area: data-structures/hashing
level: advanced
summary: Hash function with no collisions on a fixed key set, giving worst-case O(1) lookup.
prereqs: [static-dictionary-problem, universal-hash-family, hash-function]
see_also: [minimal-perfect-hashing, fks-perfect-hashing, dynamic-perfect-hashing, chd-hashing, cuckoo-hashing, birthday-paradox, perfect-hash-function, hash-collision]
sources:
  - paper: doi:10.1145/828.1884
    title: "Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a Sparse Table with O(1) Worst Case Access Time, Journal of the ACM 31(3) (1984), 538-544"
    locator: the quadratic-space lemma and the two-level scheme in linear space
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 11.5, Perfect hashing (the two-level scheme with universal hashing at each level)
  - paper: doi:10.1007/978-3-642-04128-0_61
    title: "Djamal Belazzougui, Fabiano C. Botelho and Martin Dietzfelbinger, Hash, Displace, and Compress, ESA 2009, Lecture Notes in Computer Science 5757, 682-693"
    locator: Section 2, the space lower bounds for perfect and minimal perfect hash functions
  - url: https://arxiv.org/abs/2506.06536
    title: "Hans-Peter Lehmann, Thomas Mueller, Rasmus Pagh, Giulio Ermanno Pibiri, Peter Sanders, Sebastiano Vigna and Stefan Walzer, Modern Minimal Perfect Hashing: A Survey, ACM Computing Surveys 58(10) (2026)"
    locator: the definitions, the space lower bound and the overview of construction methods
---

Perfect hashing stores a fixed set $S$ of $n$ keys with a [hash function](/hash-function/) that is one-to-one on $S$, so that no two keys of $S$ collide. A lookup then computes one address and reads one slot, which gives $O(1)$ time in the worst case, not only in expectation. Such a function exists for every set, but a random function into $n$ or even $2n$ slots is almost never one-to-one, so the art is to find one fast and to store it in little space. It solves the [static dictionary problem](/static-dictionary-problem/), and the two-level scheme of Fredman, Komlos and Szemeredi does it in $O(n)$ words with a [universal hash family](/universal-hash-family/).

## In plain words

An ordinary hash table puts each key in a slot chosen by a hash function. Two keys sometimes get the same slot, and the table must then search a short list or try other slots. So a lookup is fast on average, but an unlucky lookup can take long.

If the set of keys never changes, you can do better. You can try hash functions until you find one that gives each key its own slot. Then a lookup goes to exactly one slot and is done. Such a function is a perfect hash function for these keys.

A random function rarely has this property unless the table is very large. The trick is to hash in two steps: first into a few groups, then each small group into its own small table, which is large enough for its few keys.

## The idea

**Definition.** Let $S \subseteq U$ with $|S| = n$, and let $m \ge n$. A function $h : U \to \{0, 1, \ldots, m-1\}$ is a *perfect hash function for $S$* if $h(x) \ne h(y)$ for all $x, y \in S$ with $x \ne y$. It is *minimal* if $m = n$; see [minimal perfect hashing](/minimal-perfect-hashing/). On keys outside $S$ the function may return any value, so a membership query still compares the key with the one stored at its slot.

**Random functions are rarely perfect.** For a fixed $S$ and a function chosen uniformly from all functions $U \to \{0, \ldots, m-1\}$, the values on $S$ are independent and uniform, so

$$\Pr[h \text{ is perfect for } S] = \prod_{i=0}^{n-1} \frac{m - i}{m}.$$

For $m = n$ this is $n!/n^n$, which is about $\sqrt{2 \pi n}\, e^{-n}$ by [Stirling's approximation](/stirling-approximation/). For a fixed ratio $m / n$ it still tends to 0 exponentially fast. This is the [birthday paradox](/birthday-paradox/): collisions appear once $n$ is about $\sqrt{m}$. So one level of hashing needs about $n^2$ slots.

**Lemma 1 (quadratic space).** Let $\mathcal{H}$ be a universal family of functions $U \to \{0, \ldots, m-1\}$, that is, $\Pr_{h \in \mathcal{H}}[h(x) = h(y)] \le 1/m$ for all $x \ne y$. If $m \ge n^2$, then a random $h \in \mathcal{H}$ is perfect for $S$ with probability more than $1/2$.

*Proof.* Let $C$ be the number of pairs $\{x, y\} \subseteq S$ with $x \ne y$ and $h(x) = h(y)$. By [linearity of expectation](/linearity-of-expectation/) over the $\binom{n}{2}$ pairs, $E[C] \le \binom{n}{2} / m \le \frac{n(n-1)}{2 n^2} < \frac{1}{2}$. Since $C$ is a nonnegative integer, the [Markov inequality](/markov-inequality/) gives $\Pr[C \ge 1] \le E[C] < 1/2$. The function is perfect exactly when $C = 0$. $\square$

So with $m = n^2$ the expected number of draws until a perfect function appears is less than 2, and each draw is tested in $O(n)$ time.

**Lemma 2 (two levels in linear space).** Let $h$ be random from a universal family into $m = n$ slots, and let $n_j = |\{x \in S : h(x) = j\}|$. Then $E\left[\sum_j n_j^2\right] < 2n$.

*Proof.* Each key contributes 1 to $\sum_j n_j^2$ with itself, and each colliding pair contributes 2, so $\sum_j n_j^2 = n + 2C$ with $C$ as above. Then $E\left[\sum_j n_j^2\right] = n + 2 E[C] \le n + \frac{n(n-1)}{m} = 2n - 1 < 2n$. $\square$

The two-level scheme uses this. Pick $h$ into $n$ buckets. If $\sum_j n_j^2 \ge 4n$, which has probability less than $1/2$ by the Markov inequality, pick again. Then give bucket $j$ a table of $n_j^2$ slots and, by Lemma 1, a second function $h_j$ that is perfect on the $n_j$ keys of the bucket. The tables have fewer than $4n$ slots in total, a lookup computes $h$ and $h_j$ and reads one slot, and the construction takes $O(n)$ expected time. The details are on the page [FKS perfect hashing](/fks-perfect-hashing/).

**How many bits a perfect hash function needs.** The keys themselves need not be stored to evaluate $h$, so one can ask how many bits the description of $h$ needs. Fix $h$, and let $u_j = |h^{-1}(j)|$ for each slot $j$, with $\sum_j u_j = u = |U|$. The function $h$ is perfect for a set $S$ exactly when $S$ takes at most one key from each $u_j$. So the number of $n$-sets with $h$ perfect is the elementary symmetric sum $\sum_{J} \prod_{j \in J} u_j$ over $n$-subsets $J$ of the slots. By Maclaurin's inequality for the elementary symmetric means, this sum is at most $\binom{m}{n}$ times $(u/m)^n$, the $n$-th power of the mean of the $u_j$, with equality when all $u_j$ are equal. So the count is at most $\binom{m}{n} (u/m)^n$. A program that serves all $\binom{u}{n}$ sets therefore needs at least

$$\frac{\binom{u}{n}}{\binom{m}{n} (u/m)^n}$$

different functions, and so at least the logarithm of this number in bits for some set. When $u$ grows and $n$ and $m$ stay fixed, this bound tends to $\lg \frac{m^n (m-n)!}{m!}$ bits. For large $n$ this is about $1.443$ bits per key for $m = n$, $0.886$ for $m = 1.23 n$, and $0.443$ for $m = 2n$. The bound for $m = n$ is $n \lg e$ up to lower-order terms, and the page on [minimal perfect hashing](/minimal-perfect-hashing/) derives it in full. The FKS scheme stores $\Theta(n)$ words, far more than this bound, because it keeps a second function per bucket.

**Static only.** A perfect function for $S$ is in general not perfect for $S \cup \{x\}$. Adding keys needs a rebuild of a part of the structure, which is what [dynamic perfect hashing](/dynamic-perfect-hashing/) does with amortized and expected bounds.

## Examples

**A one-level search.** Take $S = \{10, 22, 37, 40, 52, 60, 70, 72, 75\}$, $n = 9$, the prime $p = 101$, and the functions $h_{a,b}(x) = ((a x + b) \bmod p) \bmod 9$. The function $h_{17,0}$ maps the keys, in the order given, to $6, 8, 5, 2, 4, 1, 7, 3, 0$. These are nine different values, so $h_{17, 0}$ is a minimal perfect hash function for $S$. A table $T$ with $T[h_{17,0}(x)] = x$ answers each membership query with one probe.

**The chance of success.** For a random function, the product formula gives these probabilities that a set of 10 keys has no collision: $10!/10^{10} \approx 0.00036$ with 10 slots, $0.38$ with 50 slots, and $0.63$ with 100 slots. The last case is the setting of Lemma 1, where a universal family guarantees more than $1/2$.

**Two levels.** With the same $S$, take the first-level function $h(x) = (x \bmod 101) \bmod 9 = x \bmod 9$. The buckets are $\{72\}$ at 0, $\{10, 37\}$ at 1, $\{75\}$ at 3, $\{22, 40\}$ at 4, $\{60\}$ at 6 and $\{52, 70\}$ at 7, and buckets 2, 5 and 8 are empty. So $\sum_j n_j^2 = 1 + 4 + 1 + 4 + 1 + 4 = 15$, which is less than $2n = 18$. Each bucket of 2 keys gets a table of 4 slots. The second-level function $x \bmod 4$ is perfect in all three of them: $10 \mapsto 2$ and $37 \mapsto 1$; $22 \mapsto 2$ and $40 \mapsto 0$; $52 \mapsto 0$ and $70 \mapsto 2$. A lookup of 40 goes to bucket $40 \bmod 9 = 4$, then to slot $40 \bmod 4 = 0$ of the table of bucket 4, and finds 40.

**A non-example.** The function $x \bmod 9$ is not perfect for $S$, because $10$ and $37$ both map to 1. And $h_{17,0}$ is perfect for $S$ but not for $S \cup \{11\}$: $17 \cdot 11 = 187$, $187 \bmod 101 = 86$, and $86 \bmod 9 = 5$, the slot of 37.

## Where it is used

- **Static dictionaries.** [FKS perfect hashing](/fks-perfect-hashing/) gives $O(1)$ worst-case lookups in $O(n)$ words for the [static dictionary problem](/static-dictionary-problem/).
- **Compact functions.** [Minimal perfect hashing](/minimal-perfect-hashing/) and methods such as [CHD](/chd-hashing/) map $n$ keys to $\{0, \ldots, n-1\}$ with a few bits per key, so that an array of values can be indexed without storing the keys.
- **Dynamic sets.** [Dynamic perfect hashing](/dynamic-perfect-hashing/) keeps the FKS structure under insertions and deletions, and [cuckoo hashing](/cuckoo-hashing/) gives a dynamic table with two probes in the worst case per lookup.
- **Keyword recognition.** Compilers and interpreters recognize reserved words with a perfect hash function generated for the fixed list of keywords.
- **Retrieval and filters.** A [Bloomier filter](/bloomier-filter/) and related static structures return a stored value for each key of $S$ by a construction close to perfect hashing.

## References
