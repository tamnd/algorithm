---
tag: Z7R55A
kind: problem
slug: static-dictionary-problem
name: Static dictionary problem
aliases:
- static membership problem
area: data-structures/hashing
level: advanced
summary: Preprocess a fixed key set so that lookups are fast, with no updates.
prereqs: [dictionary-problem]
see_also: [perfect-hashing, minimal-perfect-hashing, fks-perfect-hashing, static-dictionary-lower-bound, cell-probe-model, bloomier-filter, approximate-membership, predecessor-problem]
sources:
  - paper: doi:10.1145/828.1884
    title: "Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a Sparse Table with O(1) Worst Case Access Time, Journal of the ACM 31(3) (1984), 538-544"
    locator: the two-level scheme with O(n) cells, O(1) worst-case probes and expected O(n) construction time
  - paper: doi:10.1145/322261.322274
    title: "Andrew Chi-Chih Yao, Should Tables Be Sorted?, Journal of the ACM 28(3) (1981), 615-628"
    locator: the cell-probe model, the lower bound of ceil(lg(n+1)) probes for implicit tables over a large universe, and the two-probe search with one extra cell
  - paper: doi:10.1137/S0097539700369909
    title: "Rasmus Pagh, Low Redundancy in Static Dictionaries with Constant Query Time, SIAM Journal on Computing 31(2) (2001), 353-363"
    locator: static membership with O(1) query time in space close to log2 C(u, n) bits
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 11.5, Perfect hashing
---

The static dictionary problem asks for a data structure that stores a fixed set $S$ of $n$ keys from a universe $U = \{0, 1, \ldots, u-1\}$ and answers membership queries "is $x \in S$?", and often also returns a value stored with $x$. The set is given once, before the first query, and never changes. This is the [dictionary problem](/dictionary-problem/) without insertions and deletions. With no updates to support, the structure can spend its preprocessing time to find a layout with $O(1)$ worst-case query time in $O(n)$ words, which [perfect hashing](/perfect-hashing/) achieves.

## In plain words

You have a list of words that never changes, for example the keywords of a programming language. Later, someone asks you about one word at a time, and you must say fast whether the word is on the list.

Because the list is fixed, you can prepare it once, as carefully as you like. You can sort it and use binary search. You can also build a special table in which each listed word has its own slot, chosen so that no two words share a slot. Then one look at one slot answers each question. The problem asks how fast the answers can be, how little memory the table can use, and how long the preparation takes.

## Definition

**Input to the preprocessing.** A set $S \subseteq U = \{0, 1, \ldots, u-1\}$ with $|S| = n$. In the retrieval form, each $x \in S$ also has a value $v(x)$.

**Output of the preprocessing.** A data structure $D_S$ in memory.

**Query.** Given $x \in U$, answer $\mathrm{member}(x) = [x \in S]$. In the retrieval form, also return $v(x)$ when $x \in S$.

**Costs.** The query time $t$ (in the worst case over $x$, or in expectation over the coins of the preprocessing), the space $s$ of $D_S$ in words or in bits, and the preprocessing time. The usual machine is the [word RAM](/word-ram/) with words of $w \ge \lg u$ bits, so that one key fits in one word. For lower bounds, the [cell-probe model](/cell-probe-model/) charges only the number of memory cells that a query reads.

**The space bound.** Let $B = \lceil \lg \binom{u}{n} \rceil$. Any structure that answers membership correctly uses at least $B$ bits for some set $S$. The proof is a count: if two different sets $S \ne S'$ gave the same memory contents, then a query for a key in $S \setminus S'$ (or in $S' \setminus S$) would get the same answer for both sets, and one of the two answers is wrong. So the map $S \mapsto D_S$ is one-to-one on the $\binom{u}{n}$ sets, and some set needs at least $\lg \binom{u}{n}$ bits.

## Variants

- **Membership.** Return only $[x \in S]$. The structure must hold enough of the keys to reject each $x \notin S$.
- **Retrieval (static function).** Return $v(x)$ for $x \in S$, and any value for $x \notin S$. The structure need not store the keys, so it can use about $n$ times the length of a value, which is much less than $B$ when $u$ is large. A [Bloomier filter](/bloomier-filter/) solves this variant.
- **Approximate membership.** Answer "yes" for every $x \in S$, and "yes" for $x \notin S$ only with a small probability $\varepsilon$. This is the [approximate membership](/approximate-membership/) problem of the [Bloom filter](/bloom-filter/) and the [XOR filter](/xor-filter/). It needs about $n \lg(1/\varepsilon)$ bits.
- **Implicit tables.** The memory is exactly $n$ cells that hold the keys of $S$ in some order, and nothing else. This is the model of Yao's lower bound.
- **Predecessor.** Return the largest key of $S$ that is at most $x$. This is the [predecessor problem](/predecessor-problem/). It is harder: hashing alone does not solve it.
- **Small universe.** When $u$ is at most a small multiple of $w n$, a [bit vector](/bit-set/) of $u$ bits answers each query with one probe.

## Examples

Take $u = 64$ and $S = \{3, 10, 19, 26, 41, 55\}$, so $n = 6$.

- **Space.** $B = \lceil \lg \binom{64}{6} \rceil = \lceil 26.16 \rceil = 27$ bits. A list of the keys with 6 bits each uses 36 bits, and a bit vector uses 64 bits.
- **Sorted array.** Store $(3, 10, 19, 26, 41, 55)$. Binary search answers each query with at most $\lceil \lg 7 \rceil = 3$ probes.
- **A perfect hash table.** The function $h(x) = ((x + 12) \bmod 67) \bmod 6$ maps the six keys to six different slots: $h(3) = 3$, $h(10) = 4$, $h(19) = 1$, $h(26) = 2$, $h(41) = 5$ and $h(55) = 0$. So the table $T = [55, 19, 26, 3, 10, 41]$ and the two numbers 67 and 12 form a static dictionary. The query $x = 41$ computes $h(41) = 53 \bmod 6 = 5$ and finds $T[5] = 41$, so the answer is yes. The query $x = 20$ computes $h(20) = 32 \bmod 6 = 2$ and finds $T[2] = 26 \ne 20$, so the answer is no. Each query reads one cell of $T$.
- **The cost of the search.** Of the $66 \cdot 67 = 4422$ functions $((a x + b) \bmod 67) \bmod 6$ with $1 \le a \le 66$ and $0 \le b \le 66$, only 56 are one-to-one on $S$, about 1.3 percent. With 36 slots instead of 6, about 84 percent of them are one-to-one. This gap is the reason why [FKS perfect hashing](/fks-perfect-hashing/) uses two levels of tables instead of one search for a single function into $n$ slots.

## Known algorithms

| method | query time | space | preprocessing |
|---|---|---|---|
| sorted array and [binary search](/binary-search/) | $O(\log n)$ worst case | $n$ words | $O(n \log n)$ to sort |
| [bit vector](/bit-set/) | $O(1)$ worst case | $u$ bits | $O(u / w + n)$ |
| [hash table](/hash-table/) with [separate chaining](/separate-chaining/) or [linear probing](/linear-probing/) | $O(1)$ expected | $O(n)$ words | $O(n)$ expected |
| [FKS perfect hashing](/fks-perfect-hashing/) | $O(1)$ worst case | $O(n)$ words | $O(n)$ expected |
| [cuckoo hashing](/cuckoo-hashing/) built once | $O(1)$ worst case, two probes | $O(n)$ words | $O(n)$ expected |
| [minimal perfect hashing](/minimal-perfect-hashing/) plus the key array | $O(1)$ worst case | $n$ words plus about 2 to 3 bits per key | $O(n)$ expected |
| succinct dictionaries (Brodnik and Munro, Pagh) | $O(1)$ worst case | $B$ bits plus lower-order terms | see Pagh (2001) |

The hash-based rows assume a random choice of the hash function from a [universal hash family](/universal-hash-family/) or a stronger one. Their expected bounds are over this choice, not over the keys.

## Bounds

- **Query time on the word RAM.** FKS gives $O(1)$ in the worst case with $O(n)$ words, so the query time is $\Theta(1)$. A lower bound of one probe holds for every structure that must reject some $x \notin S$, because without a probe the answer cannot depend on $S$.
- **Space.** $B = \lceil \lg \binom{u}{n} \rceil$ bits, by the count in the Definition. Since $\binom{u}{n} \le (e u / n)^n$, this is at most $n \lg(e u / n) + 1$ bits, which is less than the $n \lg u$ bits of a plain list of the keys when $n \ge 3$. Pagh (2001) answers queries in $O(1)$ time with space $B$ plus lower-order terms.
- **Implicit tables.** Yao (1981) proved in the cell-probe model that if the memory is exactly $n$ cells that hold the keys, and the universe is large enough, every scheme needs $\lceil \lg(n+1) \rceil$ probes in the worst case. So a sorted table with binary search is optimal in that model. See [the lower bound for static dictionaries](/static-dictionary-lower-bound/). Yao also showed that one extra cell in a sorted table allows a search with two probes, so the lower bound depends on the strict space limit.
- **Comparison model.** If the query may only compare $x$ with stored keys, binary search is optimal with $\lceil \lg(n+1) \rceil$ comparisons in the worst case; see the [lower bound for sorted search](/sorted-search-lower-bound/). Hashing escapes this bound because it uses the bits of $x$ as an address.

## Reductions

- **To the dynamic problem.** Insert the $n$ keys into a structure for the [dictionary problem](/dictionary-problem/), then only query it. So each bound for the dynamic problem is a bound for the static one. The converse fails: the static problem has worst-case $O(1)$ query time in linear space with a simple structure, and the dynamic one needs more care, see [dynamic perfect hashing](/dynamic-perfect-hashing/).
- **From a minimal perfect hash function.** Given a [minimal perfect hash function](/minimal-perfect-hashing/) $h : U \to \{0, \ldots, n-1\}$ that is one-to-one on $S$, store each $x \in S$ at $T[h(x)]$. A query $x$ answers yes if and only if $T[h(x)] = x$. This adds $n$ words to the size of $h$ and one probe to its evaluation time.
- **From the predecessor problem.** A predecessor query for $x$ returns $x$ itself if and only if $x \in S$. So a static predecessor structure answers membership with the same cost. The converse fails: the [predecessor lower bound](/predecessor-lower-bound/) shows that predecessor needs more than constant time in linear space for some parameters.
- **To approximate membership.** Store a fingerprint of $\lceil \lg(1/\varepsilon) \rceil$ bits of each key at $T[h(x)]$, in place of the key. A query compares fingerprints. A key $x \notin S$ passes with probability about $\varepsilon$ when the fingerprint function is random.

## Applications

- **Keyword tables.** A compiler or an interpreter checks whether an identifier is a reserved word. The set of reserved words is fixed when the program is written, so tools build a perfect hash function for it in advance.
- **Read-only indexes.** A search engine, a database of a fixed release, or a genome index maps each key of a large static set to its record. Space is the main cost, so [minimal perfect hashing](/minimal-perfect-hashing/) and succinct structures are used.
- **Lookup tables in programs.** A fixed table of Unicode properties, of country codes or of opcodes is a static dictionary. A sorted array is simple and small; a perfect hash table is faster when the table is large and the queries are many.
- **Two-level hashing as a building block.** Dynamic structures rebuild a static dictionary from time to time; [dynamic perfect hashing](/dynamic-perfect-hashing/) uses the FKS static structure in each part.

## References
