---
tag: PX2K2C
kind: data-structure
slug: partitioned-elias-fano
name: Partitioned Elias-Fano index
aliases:
- PEF
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: research
summary: Splits each posting list into chunks chosen by dynamic programming and codes each chunk with Elias-Fano or a bitmap, to fit local density.
model: word-ram
complexity:
  vars: {n: the number of values, m: the number of chunks, u: one more than the largest value, ε: the approximation parameter}
  time: {build_exact: O(n^2), build_approx: O(n log(1/ε) / ε), access: O(log m), next_geq: O(log m + log n)}
  space: {bits: O(n log(u / n) + n + log u), build_extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [elias-fano-encoding, bit-vector]
see_also: [posting-list, postings-gap-encoding, simple-9, pfor-delta, roaring-bitmap, sd-array, dag-shortest-paths, document-identifier-reassignment]
sources:
  - paper: doi:10.1145/2600428.2609615
    title: Giuseppe Ottaviano and Rossano Venturini, Partitioned Elias-Fano indexes, Proceedings of the 37th International ACM SIGIR Conference (SIGIR 2014), pages 273 to 282
    locator: the two-level representation with Elias-Fano, bitmap and run chunks, the exact dynamic program for the partition, and its (1 + ε) approximation on a pruned graph
  - paper: doi:10.1145/2433396.2433409
    title: Sebastiano Vigna, Quasi-succinct indices, Sixth ACM International Conference on Web Search and Data Mining (WSDM 2013), pages 83 to 92
    locator: the Elias-Fano representation of posting lists with skipping, which the partitioned form splits into chunks
  - paper: "Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys, 2021, arXiv 1908.10598"
    title: Techniques for inverted index compression
    locator: the section on Elias-Fano and its partitioned form, with the comparison of index codes in space and speed
---

A partitioned Elias-Fano index stores a strictly increasing list of document ids, a [posting list](/posting-list/), as a sequence of chunks. Each chunk is coded relative to the last value of the chunk before it, in the smallest of three forms: nothing at all for a run of consecutive ids, a bitmap for a dense chunk, or [Elias-Fano](/elias-fano-encoding/) for a sparse one. A small upper level, itself a pair of Elias-Fano lists in the original design, keeps the first index and the last value of each chunk. The cut points are chosen by a dynamic program that minimizes the total size, with a fixed cost for each chunk. Ottaviano and Venturini introduced it in 2014. Plain Elias-Fano, on its own page, uses one width for the whole list and so pays for the average density; this page is about the split into chunks and the choice of the cuts. The page on [Simple-9](/simple-9/) codes the gaps word by word and has no fast skip, and [document identifier reassignment](/document-identifier-reassignment/) changes the ids so that the chunks here get denser.

## In plain words

Elias-Fano is a good way to store a sorted list of numbers, but it picks its settings from the list as a whole. Real lists are not even. In one place the numbers come one after another, and in another place there are big holes. A setting that fits the whole list fits neither place well. So cut the list into pieces and store each piece in the way that fits it. A piece of numbers that come one after another needs no bits at all. A crowded piece is best stored as a row of yes and no bits. A thin piece is stored with Elias-Fano. Each piece costs a few extra bits for its entry in a small table, so too many pieces is also bad. A short computation over all the places to cut finds the best balance.

## The abstract type

The structure stores a static strictly increasing list $X = x_0 < x_1 < \cdots < x_{n-1}$ of nonnegative integers and answers:

- `access(q)`: return $x_q$, for $0 \le q < n$;
- `next_geq(y)`: return the least $q$ with $x_q \ge y$, or $n$ if there is none.

These are the same two queries as [Elias-Fano encoding](/elias-fano-encoding/). In query processing, `next_geq` is the skip that list intersection and dynamic pruning use to jump over ids.

## Representation

A partition is a list of cuts $0 = c_0 < c_1 < \cdots < c_m = n$. Chunk $t$ holds $x_i, \ldots, x_{j-1}$ with $i = c_{t-1}$ and $j = c_t$. Its base is $\beta = 0$ for the first chunk and $\beta = x_{i-1} + 1$ otherwise. Its universe is $U = x_{j-1} - \beta + 1$, and its size is $b = j - i$. It stores the $b$ distinct values $x_k - \beta$, which lie in $[0, U)$.

- **Run.** If $b = U$, the chunk holds every integer from $\beta$ to $x_{j-1}$, and it needs no payload.
- **Bitmap.** A [bit vector](/bit-vector/) of $U$ bits, with bit $x_k - \beta$ set. It is used when $U$ is at most the Elias-Fano size.
- **Elias-Fano.** The low parts and the unary high parts of the values, in $E(b, U) = b\ell + b + \lfloor (U-1)/2^\ell \rfloor + 1$ bits with $\ell = \lfloor \lg(U/b) \rfloor$.

So the payload of a chunk is $0$ for a run and $\min(U, E(b, U))$ otherwise. The upper level keeps the start index $c_{t-1}$ and the last value $x_{c_t - 1}$ of each chunk, with the kind of the chunk and the offset of its payload. In the paper these are Elias-Fano sequences too. The model here charges a fixed $F$ bits for each chunk's entry, and the paper bounds this by about $2 \lg u + \lg n$ bits. The implementation uses $F = 2\lceil \lg(u+1) \rceil + \lceil \lg(n+1) \rceil$ by default.

## Operations

```pseudo id=main
PARTITION(x[0..n-1], F)                      ▷ strictly increasing, x[0] ≥ 0
L1  C[0] ← 0
L2  for j ← 1 to n do
L3      C[j] ← ∞
L4      for i ← 0 to j - 1 do
L5          if C[i] + F + COST(i, j) < C[j] then C[j] ← C[i] + F + COST(i, j), back[j] ← i
L6  return the cuts n, back[n], back[back[n]], ..., 0 in increasing order

BUILD(x, cuts)
L7  for each pair i < j of consecutive cuts do
L8      β ← 0 if i = 0 else x[i - 1] + 1, U ← x[j - 1] - β + 1, b ← j - i
L9      if b = U then kind ← RUN, payload ← empty
L10     else if U ≤ E(b, U) then kind ← BITMAP, payload ← U bits with bit x[k] - β set for i ≤ k < j
L11     else kind ← EF, payload ← ELIAS-FANO(x[i..j-1] - β, U)
L12     append (i, x[j - 1], kind, payload) to the upper level

ACCESS(q)
L13 t ← the last chunk whose start is ≤ q
L14 return β_t + the element of rank q - start_t of chunk t

NEXT-GEQ(y)
L15 t ← the first chunk whose last value is ≥ y, and return n if there is none
L16 return start_t + the rank of the first element ≥ y in chunk t
```

**Partition.** $C[j]$ is the least size of a partition of the prefix $x_0, \ldots, x_{j-1}$. The last chunk of such a partition is $x_i, \ldots, x_{j-1}$ for some $i$, and its cost depends only on $i$ and $j$, because its base is fixed by $x_{i-1}$. So lines L4 and L5 try every $i$. This is a shortest path from 0 to $n$ in the [DAG](/dag-shortest-paths/) on the positions $0, \ldots, n$, with an edge $i \to j$ of weight $F + \text{COST}(i, j)$. Each weight takes $O(1)$ time from $b$ and $U$.

**Build.** Lines L8 to L11 code each chunk in the form with the fewest bits. The bitmap wins on dense chunks, where $U/b$ is small, and Elias-Fano wins on sparse ones.

**Access.** Line L13 is a search in the list of starts. Line L14 reads one element: a run gives $\beta + r$ for rank $r$, a bitmap gives $\beta$ plus the position of its $(r+1)$-th 1, and an Elias-Fano chunk gives $\beta$ plus its own access. With a select index on each bitmap and each high part, the read takes $O(1)$ time.

**Next-geq.** All chunks before $t$ end below $y$, so line L15 skips them in one search of the last values, and chunk $t$ contains the answer. Line L16 then searches inside that one chunk. This is the gain over plain gap codes: the skip touches the upper level and one chunk, not the ids in between.

## Example

Take the list of 20 ids $X = 0, 1, 2, 3, 4, 5, 6, 7, 40, 100, 160, 220, 300, 301, 303, 304, 306, 307, 309, 310$, with $F = 10$ bits for each chunk. It has a run at the start, a sparse middle and a dense end. The optimal cuts are $0, 8, 13, 20$:

| chunk | values | base $\beta$ | $U$ | $b$ | kind | payload bits | the other forms |
|---|---|---|---|---|---|---|---|
| 1 | 0 to 7 | 0 | 8 | 8 | run | 0 | Elias-Fano 16, bitmap 8 |
| 2 | 40, 100, 160, 220, 300 | 8 | 293 | 5 | Elias-Fano | 40 | bitmap 293 |
| 3 | 301 to 310, without 302, 305, 308 | 301 | 10 | 7 | bitmap | 10 | Elias-Fano 17 |

In chunk 2 the stored values are $32, 92, 152, 212, 292$ and $\ell = \lfloor \lg(293/5) \rfloor = 5$. The low parts $0, 28, 24, 20, 4$ take 25 bits, and the high parts $1, 2, 4, 6, 9$ set bits $1, 3, 6, 9, 13$ of a high part of $5 + 9 + 1 = 15$ bits, so the payload is `0000011100110001010000100` then `010100100100010`, 40 bits. Chunk 3 stores $0, 2, 3, 5, 6, 8, 9$ as the bitmap `1011011011`.

The total is $3 \cdot 10 + 0 + 40 + 10 = 80$ bits. One chunk for the whole list costs $10 + 119 = 129$ bits, because a single Elias-Fano code with $\ell = \lfloor \lg(311/20) \rfloor = 3$ pays 3 low bits for every id, also in the run. Chunks of a fixed size cost 113 bits for size 4 and 115 bits for size 5. With the default $F = 23$ of the implementation, the same cuts are optimal and the total is 119 bits.

Queries: `next_geq(150)` finds that chunk 2 is the first chunk whose last value, 300, is at least 150. It then reads 40, 100, 160 in that chunk and returns index 10, and `access(10)` is 160. `next_geq(302)` goes to chunk 3 and returns index 14, the id 303. `next_geq(311)` finds no chunk and returns 20.

## Correctness

The [proof](proofs/correctness.md) shows that each chunk value lies in $[0, U)$ of its chunk, so each of the three codes gives back the chunk. It shows that the size of a partition is a sum of chunk costs that depend only on the two cuts, so the recurrence of lines L4 and L5 finds the least size of each prefix by induction. Finally, it shows that the search on the starts and on the last values finds the right chunk for `access` and `next_geq`. The tests compare the dynamic program with a search over all $2^{n-1}$ partitions for $n \le 12$, check every payload length against the formulas, and compare both queries with a binary search on the plain list.

## Complexity

The exact dynamic program does $n(n+1)/2$ steps of $O(1)$ each, so it takes $O(n^2)$ time and $O(n)$ space. This is too slow for lists of millions of ids. The paper gives a $(1 + \varepsilon)$ approximation instead. It keeps, for each start, only one edge for each cost level, where the levels grow by a factor of $1 + \varepsilon$, and it finds a partition within a factor $(1 + \varepsilon)$ of the best in $O(n \log_{1+\varepsilon}(1/\varepsilon))$ time. For small $\varepsilon$ this is $O(n \log(1/\varepsilon) / \varepsilon)$, which is linear for a fixed $\varepsilon$. The implementation here runs the exact program.

The size is never more than that of a single chunk, which is $F$ plus the Elias-Fano size $n \lceil \lg(u/n) \rceil + 2n$ at most. So the space is $O(n \log(u/n) + n + \log u)$ bits, and on lists with dense regions it is often much less. With search over the upper level, `access` takes $O(\log m)$ time for $m$ chunks plus $O(1)$ in the chunk with select indexes. `next_geq` adds a search inside one chunk, in $O(\log n)$ time at most. With the Elias-Fano upper level of the paper, the chunk search is itself an Elias-Fano `next_geq`. The implementation reads the bits of a chunk one by one, so its in-chunk reads take time linear in the payload.

## Variants

- **Chunks of a fixed size.** Cut every 128 ids, for example, and choose only the code of each chunk. This needs no dynamic program and is simpler, but it misses the run and the dense regions that do not align with the cuts. In the example it costs 113 bits against 80.
- **Approximate partition.** The $(1 + \varepsilon)$ method of the paper, with one edge kept for each cost level. Pibiri and Venturini state that the paper uses two parameters, $\varepsilon_1 = 0.03$ and $\varepsilon_2 = 0.3$.
- **Other chunk codes.** The same partition scheme works with any code whose cost for a chunk is known from its ends, and later work puts other codes in the chunks. Clustered Elias-Fano, by Pibiri and Venturini, shares one reference list among a cluster of similar posting lists.
- **Uniform Elias-Fano with skips.** The [quasi-succinct index](/elias-fano-encoding/) of Vigna stores one Elias-Fano code for each list, with forward pointers into the high part for fast skips. It is the case of a single chunk.

## When to use it

Use it for a static [inverted index](/inverted-index/) that must be both small and fast to intersect, where queries skip a lot with `next_geq`. It gains the most on lists with clusters of close ids, which is common after [document identifier reassignment](/document-identifier-reassignment/) and for sites crawled in URL order. For lists that are read in full, with few skips, a block code such as [PForDelta](/pfor-delta/) may decode faster. For an index that changes all the time, use a dynamic scheme and code each merged partition anew.

## Pitfalls

- **Code each chunk relative to the chunk before it.** If a chunk stores its values against 0, its universe is the whole range up to its last value, and it loses the gain of the partition.
- **Count the upper level.** If $F$ is too small, the program cuts the list into many tiny chunks whose entries cost more than they save. If it is too large, the program gives one chunk. The value of $F$ must model the real cost of the upper level.
- **Compare against the real Elias-Fano size.** The choice between the bitmap and Elias-Fano must use the exact $E(b, U)$, with the floor in $\ell$, not an estimate such as $b(2 + \lg(U/b))$.
- **Do not scan the chunks.** `next_geq` must find the chunk from the upper level. Walking the chunks one by one throws away the skip.
- **The exact program is quadratic.** Use the approximation, or a cap on the chunk length, on long lists.

## Implementations

## History

Elias published the high and low bit representation in 1974, after a memo by Fano. Vigna made it practical for inverted indexes in his quasi-succinct indices of 2013. Ottaviano and Venturini noticed that one Elias-Fano code for a whole list cannot use its local clusters, and in 2014 they split the list into chunks chosen by a dynamic program, with the bitmap and the run as cheaper codes for dense chunks. Their index was smaller than plain Elias-Fano at about the same query speed, and it became a standard point of comparison in later work on index compression.

## References
