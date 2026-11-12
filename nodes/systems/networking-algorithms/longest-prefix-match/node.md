---
tag: X7VXG1
kind: problem
slug: longest-prefix-match
name: Longest prefix match
aliases:
- IP lookup
- LPM
- longest matching prefix
area: systems/networking-algorithms
level: core
summary: "Given a table of address prefixes and a destination address, find the longest prefix in the table that matches the address. It is the per-packet lookup of IP forwarding."
prereqs: [trie, hash-table, binary-search]
see_also: [tree-bitmap, packet-classification, routing-problem, bgp, radix-tree, bloom-filter, predecessor-problem, interval-stabbing-query]
sources:
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 11, Prefix-Match Lookups (Sections 11.4 unibit tries, 11.5 multibit tries, 11.7 Lulea-compressed tries, 11.8 tree bitmap, 11.9 binary search on ranges, 11.10 binary search on prefix lengths)
  - url: "https://www.rfc-editor.org/rfc/rfc4632"
    title: "Vince Fuller and Tony Li, RFC 4632, Classless Inter-domain Routing (CIDR): The Internet Address Assignment and Aggregation Plan, 2006"
    locator: Sections 3.1 and 5.1 (prefix notation and the longest-match rule); it obsoletes RFC 1519 of 1993
  - paper: doi:10.1145/263105.263136
    title: Marcel Waldvogel, George Varghese, Jon Turner and Bernhard Plattner, Scalable high speed IP routing lookups, ACM SIGCOMM 1997
    locator: pages 25 to 36 (binary search on prefix lengths, markers and precomputed best matching prefixes)
  - paper: doi:10.1145/296502.296503
    title: V. Srinivasan and George Varghese, Fast address lookups using controlled prefix expansion, ACM Transactions on Computer Systems 17(1), 1999
    locator: pages 1 to 40 (controlled prefix expansion and the choice of strides by dynamic programming)
  - paper: doi:10.1145/263105.263133
    title: Mikael Degermark, Andrej Brodnik, Svante Carlsson and Stephen Pink, Small forwarding tables for fast routing lookups, ACM SIGCOMM 1997
    locator: pages 3 to 14 (the Lulea scheme)
  - paper: doi:10.1145/321479.321481
    title: "Donald R. Morrison, PATRICIA: Practical Algorithm To Retrieve Information Coded in Alphanumeric, Journal of the ACM 15(4), 1968"
    locator: pages 514 to 534
  - paper: "Keith Sklower, A tree-based packet routing table for Berkeley Unix, Proceedings of the Winter 1991 USENIX Conference"
    locator: the whole paper (the Patricia-based routing table of BSD Unix)
  - paper: doi:10.1145/863955.863979
    title: Sarang Dharmapurikar, Praveen Krishnamurthy and David E. Taylor, Longest prefix matching using Bloom filters, ACM SIGCOMM 2003
    locator: pages 201 to 212
---

Longest prefix match is the lookup that an IP router does for each packet: given a table of address prefixes, each with a next hop, and a destination address, return the longest prefix in the table that matches the address. Since classless addressing (CIDR, RFC 1519 in 1993 and RFC 4632 in 2006), prefixes of any length overlap, so an exact-match [hash table](/hash-table/) does not answer the question by itself. The baseline method walks a binary [trie](/trie/) over the address bits and reads up to $W + 1$ nodes for a $W$-bit address. Binary search on prefix lengths needs only $\lceil \log_2(L+1) \rceil$ hash probes for $L$ distinct lengths, at most 6 for IPv4. The table itself comes from the [routing protocols](/routing-problem/), such as [link-state routing](/link-state-routing/) and [BGP](/bgp/).

## In plain words

A post office sorts letters with a list of rules. One rule says "all letters to this country go to bin 1". Another rule says "letters to this city in that country go to bin 7". A third says "letters to this one street go to bin 9". A letter to that street matches all three rules. The post office uses the most specific rule, the one that names the most of the address.

A router does the same thing with numbers. Each rule names the first few bits of an address. For each packet the router must find the rule that matches the most leading bits, and it must do this many millions of times each second. The hard part is speed: the router can read memory only a few times for each packet.

## Definition

**Model.** Addresses are $W$-bit integers: $W = 32$ for IPv4 and $W = 128$ for IPv6. A *prefix* is a pair $(p, \ell)$ with $0 \le \ell \le W$ and $0 \le p < 2^\ell$. It is written as the $\ell$ bits of $p$ followed by a star, for example `101*`. It *matches* an address $a$ if the top $\ell$ bits of $a$ equal $p$, that is, $\lfloor a / 2^{W - \ell} \rfloor = p$. The prefix `*` of length 0 matches every address and is the default route. In CIDR notation, `192.0.2.0/24` is the prefix of length 24 whose bits are the first 24 bits of `192.0.2.0`.

**Input.** A forwarding table $T$ of $n$ distinct prefixes, each with a next hop, and a query address $a$.

**Output.** The next hop of the prefix $(p, \ell) \in T$ that matches $a$ and has the largest $\ell$, or "no route" if no prefix matches. Two distinct prefixes of the same length cannot both match one address, so the answer is unique.

**Cost.** The cost that matters in a router is the number of memory accesses per lookup, because a lookup must finish in the time of one minimum-size packet. Next come the memory size, which decides if the table fits in fast memory, and the cost of an insert or a delete when a route changes. The variables are $n$ (prefixes), $W$ (address width) and $L$ (distinct prefix lengths in $T$, so $L \le W + 1$).

**The geometric view.** A prefix $(p, \ell)$ is the interval $[p \cdot 2^{W-\ell}, (p+1) \cdot 2^{W-\ell} - 1]$ of addresses. Two such intervals are nested or disjoint. The longest matching prefix is the shortest interval in $T$ that contains $a$. This is a one-dimensional [interval stabbing query](/interval-stabbing-query/) on a nested family.

## Variants

- **Static or dynamic.** A static table is built once. A dynamic table must also support insert and delete, because BGP changes routes many times each second. Leaf pushing and heavy compression make updates slow; the [tree bitmap](/tree-bitmap/) keeps them fast.
- **IPv4 and IPv6.** The width $W$ grows from 32 to 128 bits. Methods whose cost grows with $W$ (unibit tries) suffer most; methods that grow with $\log W$ (binary search on lengths) suffer least.
- **All matching prefixes.** Return every prefix that matches, not only the longest. A trie walk returns them in order of length.
- **Several tables.** A router with virtual routing tables keeps one table for each customer and looks up the pair (table, address).
- **More than one field.** Matching on source and destination prefixes and on ports at the same time is [packet classification](/packet-classification/). Longest prefix match is its one-field case, with "longest" as the priority rule.
- **Strings.** The same question over strings of an alphabet (the longest key in a set that is a prefix of a query) is answered by a [trie](/trie/) or a [radix tree](/radix-tree/). It is different from [prefix matching](/prefix-matching/) of strings, which lists the keys that *start with* the query.

## Examples

**A small table.** Take $W = 8$ and the table A = `*`, B = `1*`, C = `101*`, D = `10110*`, E = `1011011*`.

| address | matching prefixes | answer |
|---|---|---|
| 10110110 | A, B, C, D, E | E |
| 10110001 | A, B, C, D | D |
| 10100000 | A, B, C | C |
| 11000000 | A, B | B |
| 01111111 | A | A |

**The binary trie walk.** For the address 10110110, the walk reads the root and then one node for each bit: 1, 10, 101, 1011, 10110, 101101, 1011011. The node for 10110110 does not exist, so the walk stops after 8 nodes. It saw prefixes at depths 0, 1, 3, 5 and 7, and the last one, E, is the answer.

**Binary search on prefix lengths.** The distinct lengths are $[0, 1, 3, 5, 7]$, one hash table for each. For 10110110 the search probes length 3 (key 101: a prefix, so go longer), then length 5 (key 10110: a prefix, go longer), then length 7 (key 1011011: E). That is 3 probes instead of 8 node reads.

**Why markers are needed.** Take the table A = `*`, B = `0*`, C = `11*`, D = `1111*`, E = `0001111*`, with lengths $[0, 1, 2, 4, 7]$. The search for an address that starts with 0001111 first probes length 2 with the key 00. No prefix is 00, so a plain search would go to shorter lengths and never find E. The build step therefore puts a *marker* 00 at length 2 and a marker 0001 at length 4, on the search path towards length 7. Each marker stores its best matching prefix, here B. For the address 00010000 the search probes 00 (marker, best so far B), 0001 (marker, best so far B), then 0001000 (no entry) and stops with the answer B after 3 probes. It never has to go back.

**A random IPv4 table.** With seed 1, a table of 1000 random prefixes with lengths uniform in 1 to 32, a default route, and one longer nested prefix added below each prefix of length at most 24, has 1723 prefixes. Its binary trie has 12919 nodes. Binary search on prefix lengths uses 33 hash tables and adds 2335 markers. Over 10000 addresses, each drawn inside a random prefix of the table, the trie read 20.35 nodes on average and the binary search did 5.11 probes on average and 6 at most, and the two methods returned the same answer as a scan of all prefixes.

## Known algorithms

**Linear scan.** Compare the address with each prefix and keep the longest match. This is $\Theta(n)$ per lookup and is the reference for tests.

**Binary trie.** Store each prefix at the node of a binary trie that its bits spell, and walk down the bits of the address. The last marked node on the path is the answer.

```pseudo id=main
LPM-TRIE(root, a)                          ▷ a is a W-bit address
L1  v ← root, d ← 0
L2  best ← none
L3  while v ≠ nil do
L4      if v holds a prefix then
L5          best ← the prefix at v          ▷ the first d bits of a
L6      if d = W then break
L7      v ← the child of v for bit d of a, d ← d + 1
L8  return best
```

The walk is correct because the nodes on the path are exactly the prefixes of $a$ of lengths $0, 1, \ldots$ that have a node, so each matching prefix of $T$ is on the path, and the last one seen is the longest. The walk reads at most $W + 1$ nodes. The trie has at most $nW + 1$ nodes. Insert and delete walk one path and take $O(W)$ time.

**Path compression.** A Patricia tree (Morrison, 1968) removes the nodes with one child, so it has $O(n)$ nodes. It was used for the BSD routing table by Sklower in 1991. It does not lower the worst case of $W$ node reads, and the BSD version had to back up the path when the bits skipped at a compressed edge did not match the address. The [radix tree](/radix-tree/) page covers path compression for strings.

**Multibit tries and controlled prefix expansion.** Read $k$ bits at a time, so a lookup reads at most $\lceil W/k \rceil$ nodes. A node of stride $k$ is an array of $2^k$ entries. A prefix whose length is not a node boundary is *expanded*: a prefix of length $\ell$ becomes the $2^{\ell' - \ell}$ prefixes of the next allowed length $\ell'$, and a longer original prefix wins over an expanded shorter one. Srinivasan and Varghese (1999) choose the strides of each level by dynamic programming to use the least memory for a given number of levels.

**Compressed multibit tries.** The Lulea scheme (Degermark, Brodnik, Carlsson and Pink, 1997) uses three levels of strides 16, 8 and 8, pushes all prefixes to the leaves, and compresses each node with a bitmap of where the answer changes, plus small tables of codewords and base indices. The table becomes small enough for the cache of a processor, but an update can force a rebuild of large parts. The [tree bitmap](/tree-bitmap/) (Eatherton, Varghese and Dittia, 2004) keeps two bitmaps for each node and no leaf pushing, so an update changes only one node and its child array.

**Binary search on prefix lengths.** Waldvogel, Varghese, Turner and Plattner (1997) keep one hash table for each distinct length and binary search over the sorted lengths $\ell_0 < \ell_1 < \cdots < \ell_{L-1}$. A hit at length $\ell_m$ means that a longer match may exist, so the search goes right; a miss means that none exists, so it goes left. This needs two additions to the table:

- a *marker* at each length $\ell_m$ where the search towards a longer prefix $P$ goes right; the marker is the first $\ell_m$ bits of $P$;
- in each entry, prefix or marker, the precomputed *best matching prefix* (bmp) of its own bit string.

```pseudo id=bsl
LPM-LENGTHS(H[0 .. L − 1], ℓ[0 .. L − 1], a)   ▷ H[m] is the hash table of length ℓ[m]
L1  lo ← 0, hi ← L − 1, best ← none
L2  while lo ≤ hi do
L3      m ← ⌊(lo + hi) / 2⌋
L4      e ← H[m].get(the first ℓ[m] bits of a)
L5      if e ≠ nil then best ← e.bmp, lo ← m + 1
L6      else hi ← m − 1
L7  return best
```

*Why it is correct.* Let $a$ be the address and let the answer be the prefix $Q$ of length $\ell_q$, or none. We show this invariant of line L2: the answer is $best$, or a prefix with its length index in $[lo, hi]$ that is longer than $best$. At the start it holds because each length index is in $[0, L-1]$. On a hit at index $m$, the entry for the first $\ell_m$ bits of $a$ has as bmp the longest prefix of $T$ of length at most $\ell_m$ that matches those bits, which is the longest prefix of $T$ of length at most $\ell_m$ that matches $a$. So the answer is that bmp or a prefix longer than $\ell_m$, and the invariant holds with $lo = m + 1$. On a miss at index $m$, suppose a prefix $P$ of length index $j \in (m, hi]$ matches $a$. Each earlier step kept $j$ inside $[lo, hi]$, so the steps so far are the same steps that the build did on the search path towards $j$; at index $m$ that path goes right, since $j > m$, so the build put the first $\ell_m$ bits of $P$ into $H[m]$. These bits equal the first $\ell_m$ bits of $a$, so the probe hits, which is a contradiction. So no prefix with index in $(m, hi]$ matches, and the invariant holds with $hi = m - 1$. When $lo > hi$, the answer is $best$.

*Cost.* The loop halves the range $[lo, hi]$, so it makes at most $\lfloor \log_2 L \rfloor + 1 = \lceil \log_2 (L+1) \rceil$ probes: 6 for IPv4 ($L \le 33$) and 8 for IPv6 ($L \le 129$). A prefix adds at most one marker for each right step of its search path, so at most $\lfloor \log_2 L \rfloor$ markers, and the space is $O(n \log W)$ entries. Each probe is an expected $O(1)$ hash lookup. An update is the weak point: a new prefix can change the bmp of many markers below it.

**Binary search on ranges.** By the geometric view, the $2n$ endpoints of the prefix intervals cut the address space into at most $2n + 1$ pieces, and each piece has one fixed answer. A [predecessor](/predecessor-problem/) search on the endpoints, for example a binary search or a B-tree with a wide fan-out, then answers the lookup in $O(\log n)$ comparisons (Varghese, Section 11.9).

**TCAM.** A ternary content-addressable memory stores each prefix as a word of 0, 1 and "don't care" bits and compares the address with all words in parallel. A priority encoder returns the first matching word, so the words are kept in order of decreasing length. One lookup takes one memory cycle, but a TCAM costs much more power and chip area per bit than SRAM, and an insert may have to move many words to keep the order.

**Bloom filters.** Dharmapurikar, Krishnamurthy and Taylor (2003) keep one [Bloom filter](/bloom-filter/) for each prefix length in fast on-chip memory and query all of them in parallel. Then they probe the off-chip hash tables only for the lengths whose filter says yes, from the longest down. A false positive costs one extra probe and never a wrong answer.

### Pitfalls

- **First match is not longest match.** A list of prefixes scanned in insert order returns the first match. A table scan must keep the longest, or the list must be sorted by decreasing length.
- **Markers without a bmp.** If a marker does not store its best matching prefix, a hit on a marker followed by misses ends with no answer, and the search must back up. The bmp removes the back-tracking.
- **The default route.** The prefix of length 0 matches every address. Code that shifts by $W - \ell$ must handle $\ell = 0$, where the shift is by the full width; in C a shift of a 32-bit word by 32 is undefined.
- **Equal prefixes of different lengths.** `10*` and `100*` are different prefixes. A key must hold the length, or each length must have its own table.

## Bounds

| method | memory accesses per lookup | space | update |
|---|---|---|---|
| linear scan | $\Theta(n)$ | $\Theta(n)$ | $O(1)$ |
| binary trie | at most $W + 1$ nodes | $O(nW)$ nodes | $O(W)$ |
| Patricia tree | at most $W + 1$ nodes | $O(n)$ nodes | $O(W)$ |
| multibit trie, stride $k$ | $\lceil W/k \rceil$ nodes | up to $O(n 2^k W / k)$ entries with expansion | rebuild of the expanded entries |
| binary search on lengths | $\lceil \log_2 (L+1) \rceil$ hash probes, expected $O(1)$ each | $O(n \log W)$ entries | can touch many markers |
| binary search on ranges | $O(\log n)$ comparisons | $O(n)$ | can touch many pieces |
| TCAM | 1 parallel search | $n$ ternary words | can move many words |

All bounds are worst case except the hash probes, which are expected. The trie bounds are tight: a table with the prefixes of lengths $0, 1, \ldots, W$ of one address makes the walk read $W + 1$ nodes. Through the reduction to predecessor search, the word-RAM upper bounds for [predecessor search](/predecessor-problem/) also apply to longest prefix match.

## Reductions

- **To interval stabbing.** Each prefix is an interval of addresses, and the intervals form a nested family. The longest match is the shortest interval that contains the address, which is an [interval stabbing query](/interval-stabbing-query/) with "shortest" as the priority.
- **To predecessor search.** Sort the $2n$ interval endpoints and store with each elementary piece its answer. Then a lookup is one [predecessor](/predecessor-problem/) query.
- **From longest prefix match to packet classification.** A classifier with only a destination prefix field and priority by length is a forwarding table, so longest prefix match is the one-field case of [packet classification](/packet-classification/). Tuple space search, restricted to one field, becomes binary search over the lengths without the markers, that is, one probe per length.

## Applications

- **IP forwarding.** Every IPv4 and IPv6 router does a longest prefix match on the destination address of each packet. The [routing problem](/routing-problem/) and its protocols, [link-state routing](/link-state-routing/) inside a network and [BGP](/bgp/) between networks, build the routing table; the router copies the best routes into a forwarding table for this lookup.
- **Classification fields.** Source and destination prefix fields in firewalls and in [packet classification](/packet-classification/) need a longest prefix match on each field.
- **Software routers and switches.** Software forwarding paths use multibit tries such as the [tree bitmap](/tree-bitmap/), and the Open vSwitch classifier uses [tuple space search](/tuple-space-search/).

## References
