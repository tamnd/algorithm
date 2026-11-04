---
tag: 1R4428
kind: concept
slug: minimal-perfect-hashing
name: Minimal perfect hashing
aliases:
- BDZ hashing
- CHD hashing
- MPHF
- minimal perfect hash function
area: data-structures/hashing
level: advanced
summary: Perfect hash function whose range is exactly the key set size.
prereqs: [perfect-hashing]
see_also: [chd-hashing, static-dictionary-problem, fks-perfect-hashing, rank-select-dictionary, bloomier-filter, xor-filter, hypergraph, minimal-perfect-hash-function]
sources:
  - paper: doi:10.1007/978-3-642-04128-0_61
    title: "Djamal Belazzougui, Fabiano C. Botelho and Martin Dietzfelbinger, Hash, Displace, and Compress, ESA 2009, Lecture Notes in Computer Science 5757, 682-693"
    locator: Section 2 (the lower bound of about n / ln 2 bits for a minimal perfect hash function), the algorithm CHD, and Figure 1(d) (2.07 bits per key for lambda = 5, against 2.61 for BPZ)
  - paper: doi:10.1007/978-3-540-73951-7_13
    title: "Fabiano C. Botelho, Rasmus Pagh and Nivio Ziviani, Simple and Space-Efficient Minimal Perfect Hash Functions, WADS 2007, Lecture Notes in Computer Science 4619, 139-150"
    locator: Section 3, the method based on acyclic random 3-hypergraphs with about 1.23 n vertices, giving minimal perfect hash functions of about 2.62 n bits
  - paper: doi:10.1007/3-540-44693-1_28
    title: "Torben Hagerup and Torsten Tholey, Efficient Minimal Perfect Hashing in Nearly Minimal Space, STACS 2001, Lecture Notes in Computer Science 2010, 317-326"
    locator: the space bound n log e + log log u plus or minus O(log n), and a construction with O(1) evaluation time in space (1 + o(1)) times the bound
  - url: https://arxiv.org/abs/2506.06536
    title: "Hans-Peter Lehmann, Thomas Mueller, Rasmus Pagh, Giulio Ermanno Pibiri, Peter Sanders, Sebastiano Vigna and Stefan Walzer, Modern Minimal Perfect Hashing: A Survey, ACM Computing Surveys 58(10) (2026)"
    locator: the space lower bound, the families of methods (hash and displace, retrieval, brute force), and the experimental comparison
---

A minimal perfect hash function for a set $S$ of $n$ keys is a [perfect hash function](/perfect-hashing/) whose range has exactly $n$ values: it maps the keys of $S$ one-to-one onto $\{0, 1, \ldots, n-1\}$. So it numbers the keys without gaps, and an array of $n$ entries indexed by it holds one record per key with no empty slot. The function does not store the keys, and its description can be very small: at least about $n \lg e \approx 1.443\, n$ bits are needed, and practical methods use about 2 to 3 bits per key with $O(1)$ evaluation time. Methods such as [CHD](/chd-hashing/) and the hypergraph method of Botelho, Pagh and Ziviani build one in expected $O(n)$ time.

## In plain words

You have a fixed list of a million words. You want a small formula that turns each word into its own number from 0 to 999 999, with no number used twice and none left over. Then a plain array of a million entries can hold the data of the words, one entry per word.

The formula does not hold the words. It can only answer "which number is this word?" For a word that is not on the list it returns some number, which is meaningless. If you need to know whether a word is on the list, keep the word itself in its entry and compare.

The surprise is how little the formula needs: under two bits per word in theory, and two or three bits per word in practice, whatever the length of the words.

## The idea

**Definition.** Let $S \subseteq U$ with $|S| = n$ and $u = |U|$. A function $h : U \to \{0, \ldots, n-1\}$ is a *minimal perfect hash function* (MPHF) for $S$ if its restriction to $S$ is a bijection onto $\{0, \ldots, n-1\}$. On $U \setminus S$ the values are arbitrary. The costs are the number of bits that describe $h$, the time to evaluate $h(x)$, and the time to build $h$ from $S$.

**Lower bound on the space.** Let $\mathcal{F}$ be a set of functions $U \to \{0, \ldots, n-1\}$ such that every $n$-subset $S \subseteq U$ has an MPHF in $\mathcal{F}$. A scheme that describes its function with $b$ bits for every $S$ can describe at most $2^b$ functions, so $b \ge \lg |\mathcal{F}|$.

*Claim.* $|\mathcal{F}| \ge \binom{u}{n} n^n / u^n$. For $n \ge 2$ and $u \ge n^2$ this gives

$$b \ge n \lg e - \tfrac{1}{2} \lg n - \lg e - 2.$$

*Proof.* Fix $h \in \mathcal{F}$ and let $u_j = |h^{-1}(j)|$, so $\sum_{j=0}^{n-1} u_j = u$. The function $h$ is an MPHF exactly for the sets that take one key from each $h^{-1}(j)$, and there are $\prod_j u_j$ such sets. By the inequality of arithmetic and geometric means, $\prod_j u_j \le (u/n)^n$. All $\binom{u}{n}$ sets must be covered, so $|\mathcal{F}| (u/n)^n \ge \binom{u}{n}$, which is the first claim. For the second, use $\binom{u}{n} \ge (u - n + 1)^n / n!$ and $n! \le e \sqrt{n}\, (n/e)^n$, which holds for $n \ge 1$. Then

$$\lg |\mathcal{F}| \ge n \lg e - \tfrac{1}{2} \lg n - \lg e + n \lg\left(1 - \frac{n-1}{u}\right).$$

If $u \ge n^2$, then $1 - (n-1)/u \ge 1 - 1/n$, and $(1 - 1/n)^n \ge 1/4$ for $n \ge 2$, so the last term is at least $-2$. $\square$

So an MPHF needs $n \lg e - O(\log n) \approx 1.4427\, n$ bits when the universe is large. Hagerup and Tholey state the sharper form $n \lg e + \lg \lg u \pm O(\log n)$, and they give a construction with $O(1)$ evaluation time in space within a factor $1 + o(1)$ of it. Their construction matters for theory; the methods below are the practical ones.

**From a perfect hash function to a minimal one.** Let $g$ be perfect for $S$ with range $\{0, \ldots, m-1\}$ and $m = (1 + \varepsilon) n$. Keep a bit vector $F$ of $m$ bits with $F[i] = 1$ exactly when $i = g(x)$ for some $x \in S$, with a [rank structure](/rank-select-dictionary/). Then $h(x) = \mathrm{rank}_F(g(x))$, the number of ones in $F$ before position $g(x)$, is an MPHF: it is one-to-one on $S$ because $g$ is, and its values on $S$ are exactly $0, \ldots, n-1$. This costs $m + o(m)$ more bits and $O(1)$ more time.

**Hash and displace.** Hash the keys into $r$ small buckets with a first function $b$. Process the buckets from the largest to the smallest. For each bucket $B_j$, find the least index $d$ such that a function $f_d$ from a fixed sequence $f_0, f_1, f_2, \ldots$ maps the keys of $B_j$ to slots that are distinct and still free, and store $D[j] = d$. The function is $h(x) = f_{D[b(x)]}(x)$. Large buckets go first, while many slots are free. The CHD method of Belazzougui, Botelho and Dietzfelbinger is of this kind, with the array $D$ stored in compressed form. With an average of $\lambda = 5$ keys per bucket, its experiments reach 2.07 bits per key for an MPHF.

**Hypergraph peeling.** Use three functions $h_0, h_1, h_2$ into three disjoint ranges that together have $m \approx 1.23 n$ vertices, and view each key $x$ as the hyperedge $\{h_0(x), h_1(x), h_2(x)\}$. If the [hypergraph](/hypergraph/) can be peeled, that is, emptied by removing again and again an edge with a vertex of degree 1, then the edges can be processed in the reverse order of peeling. Each edge then has a vertex that no earlier edge used, and the method sets a 2-bit value $g$ at that vertex so that $i = (g(h_0(x)) + g(h_1(x)) + g(h_2(x))) \bmod 3$ names it. The perfect hash function is $x \mapsto h_i(x)$. Above about $1.23 n$ vertices, a random 3-hypergraph with $n$ edges can be peeled with probability that tends to 1, and below it the probability tends to 0. The function needs $2 \cdot 1.23\, n \approx 2.46\, n$ bits, and the rank step makes it minimal at about $2.62\, n$ bits. This is the method of Botelho, Pagh and Ziviani, and the peeling step is the one of the [XOR filter](/xor-filter/).

**Brute force on small sets.** Split the keys into groups of a few keys and search, for each group, for a seed of a hash function that is a bijection on the group. The expected search grows fast with the group size, but the number of bits for the seed comes close to the lower bound. Methods of this kind come within a few percent of $n \lg e$ bits; the survey of Lehmann and others compares them.

## Examples

**The lower bound for a small case.** For $n = 8$ and $u = 2^{32}$, the bound $\lg\left(\binom{u}{n} n^n / u^n\right)$ is 8.70 bits. The leading term $n \lg e$ is 11.54 bits. The difference is the $-\frac{1}{2} \lg n - \lg e$ part of the bound, which matters only for small $n$.

**Hash and displace by hand.** Take the 8 keys $S = \{12, 25, 31, 47, 58, 63, 77, 90\}$, the bucket function $b(x) = (x \bmod 7) \bmod 3$, and the sequence $f_d(x) = ((d + 1)\, x \bmod 101) \bmod 8$.

| bucket $j$ | keys | least good $d$ | slots $f_d(x)$ |
|---|---|---|---|
| 0 | 31, 63, 77, 90 | 1 | 6, 1, 5, 7 |
| 2 | 12, 47, 58 | 24 | 2, 0, 4 |
| 1 | 25 | 2 | 3 |

Bucket 0 goes first, with 4 keys. With $d = 0$ the keys 31 and 63 both map to 7, so $d = 0$ fails and $d = 1$ succeeds. Bucket 2 must avoid the slots 1, 5, 6 and 7, and the first index that works is $d = 24$. Bucket 1 has one key, and only slot 3 is still free. With $d = 0$ and $d = 1$ the key 25 lands on the used slots 1 and 2, and $d = 2$ gives $75 \bmod 8 = 3$. The function is stored as $D = [1, 2, 24]$, three small numbers. To evaluate $h(47)$: $47 \bmod 7 = 5$ and $5 \bmod 3 = 2$, so $d = D[2] = 24$, and $25 \cdot 47 = 1175$, $1175 \bmod 101 = 64$, $64 \bmod 8 = 0$. The eight keys get the eight values 0 to 7.

**A non-example.** The function $f_1$ alone is not minimal perfect for $S$: $116 \bmod 101 = 15$ gives $f_1(58) = 7$, and $180 \bmod 101 = 79$ gives $f_1(90) = 7$ too. The displacement indices are what separate the buckets.

## Where it is used

- **Static key-value tables.** An MPHF and an array of $n$ values form a static map. With the key stored next to its value, they form a solution of the [static dictionary problem](/static-dictionary-problem/) with one probe into the array.
- **Large read-only indexes.** Search engines, databases and genome indexes store billions of fixed keys, such as URLs or $k$-mers of DNA, and give each key a dense number with a few bits of overhead per key.
- **Compressed static functions.** A retrieval structure, such as a [Bloomier filter](/bloomier-filter/), stores a short value for each key of $S$ without the keys. Several MPHF methods are built from retrieval structures, and the reverse also holds.
- **Filters.** An MPHF plus an array of short fingerprints gives a static [approximate membership](/approximate-membership/) structure.
- **Building blocks.** The FKS scheme of [FKS perfect hashing](/fks-perfect-hashing/) and the method [CHD](/chd-hashing/) are the perfect hashing steps of larger structures.

## References
