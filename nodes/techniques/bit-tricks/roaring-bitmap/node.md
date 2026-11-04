---
tag: SA2AHY
kind: data-structure
slug: roaring-bitmap
name: Roaring bitmap
aliases:
- Roaring bitmaps
- compressed bitmap
area: techniques/bit-tricks
level: advanced
summary: A compressed bitmap that stores 16-bit chunks as arrays, bitmaps or runs, depending on density.
prereqs: [bit-set, binary-search, population-count, dictionary-problem]
see_also: [bit-set, bitmap-index, inverted-index, run-length-encoding, elias-fano-encoding, b-tree, exponential-search, bit-packing]
sources:
  - paper: doi:10.1002/spe.2325
    title: Samy Chambi, Daniel Lemire, Owen Kaser and Robert Godin, Better bitmap performance with Roaring bitmaps, Software Practice and Experience 46(5), 2016
    locator: pp. 709 to 719
  - paper: doi:10.1002/spe.2402
    title: Daniel Lemire, Gregory Ssi-Yan-Kai and Owen Kaser, Consistently faster and smaller compressed bitmaps with Roaring, Software Practice and Experience 46(11), 2016
    locator: pp. 1547 to 1569
  - paper: doi:10.1002/spe.2560
    title: Daniel Lemire, Owen Kaser, Nathan Kurz, Luca Deri, Chris O'Hara, François Saint-Jacques and Gregory Ssi-Yan-Kai, Roaring bitmaps, Implementation of an optimized software library, Software Practice and Experience 48(4), 2018
    locator: pp. 867 to 895
---

A Roaring bitmap stores a set of 32-bit unsigned integers by splitting each value into its high 16 bits, the key, and its low 16 bits. The values with the same key go into one container, and each container picks the layout that suits its density: a sorted array of 16-bit values when it holds at most 4096 values, and a plain [bit vector](/bit-set/) of $2^{16}$ bits otherwise. The keys sit in a sorted array, so membership is a [binary search](/binary-search/) followed by a search in one container, and union and intersection merge the two key arrays and combine the containers pair by pair, with whole-word operations where both are bitmaps. Chambi, Lemire, Kaser and Godin introduced the structure in 2016; a later version adds a third layout, a list of runs, for long stretches of consecutive values.

## In plain words

Imagine a set of numbers between 0 and about four billion. A plain bit vector would need half a gigabyte for that range, even for a set with ten members. A sorted list of the members is small for sparse sets but slow to combine with other sets.

Roaring cuts the range into blocks of 65 536 numbers and treats each block on its own. A block with few members keeps them in a short sorted list. A block with many members, more than 4096, keeps one bit for each number of the block. Blocks with no members take no space at all. So each part of the set uses the cheaper layout, and set operations still work fast, block by block.

## The abstract type

A Roaring bitmap implements a dynamic set $S \subseteq \{0, \ldots, 2^{32} - 1\}$, the [dictionary problem](/dictionary-problem/) without values, with these operations:

- `add(S, x)`, `remove(S, x)`, `contains(S, x)`;
- `cardinality(S)`: the number of members;
- iteration over the members in increasing order;
- `union(S, T)` and `intersection(S, T)`, which return new sets; libraries also have difference, symmetric difference, rank and select.

## Representation

For a value $x$ write $h(x) = \lfloor x / 2^{16} \rfloor$ and $\ell(x) = x \bmod 2^{16}$. The chunk of key $k$ is $S_k = \{\, \ell(x) : x \in S, \ h(x) = k \,\}$.

The structure is a sorted array of keys $k_0 < k_1 < \cdots < k_{m-1}$, one for each nonempty chunk, and a parallel array of containers. The container of $k_i$ stores $S_{k_i}$ as one of:

- **Array container.** The values of the chunk as a sorted array of distinct 16-bit integers, used when $\lvert S_k \rvert \le 4096$. It takes $2 \lvert S_k \rvert$ bytes.
- **Bitmap container.** A bit vector of $2^{16}$ bits, as 1024 words of 64 bits, with bit $\ell$ set exactly when $\ell \in S_k$, and a stored count of the ones. It is used when $\lvert S_k \rvert > 4096$ and always takes 8 KB.
- **Run container.** In the version of Lemire, Ssi-Yan-Kai and Kaser, a sorted list of runs, each a pair of 16-bit integers: a start and a length minus one. It is chosen, usually by an explicit optimization step, when it is smaller than the other two layouts.

The threshold 4096 is where the two layouts have the same size: $4096 \cdot 16$ bits $= 2^{16}$ bits $= 8$ KB. So the array container is never larger than a bitmap, and a bitmap container holds more than 4096 values in 8 KB, under 16 bits for each value.

**Invariant.** (I1) The keys are strictly increasing, and each key has exactly one container. (I2) Each container is nonempty. (I3) An array container is strictly increasing, with values below $2^{16}$, and has at most 4096 values. (I4) A bitmap container has exactly 1024 words, its stored count equals the number of ones, and the count is above 4096. (I5) The set represented is $S = \{\, 2^{16} k_i + \ell : \ell \text{ in the container of } k_i \,\}$.

The implementation below has array and bitmap containers; run containers change the conversion rules but not the overall design.

## Operations

```pseudo id=main
ADD(R, x)                                         ▷ 0 ≤ x < 2^32
L1  h ← x >> 16 ; l ← x AND 0xFFFF
L2  i ← position of h in R.keys by binary search; if h is absent, insert h there with an empty array container
L3  C ← R.containers[i]
L4  if C is an array container
L5      if l ∉ C then insert l into C in sorted order
L6      if |C| > 4096 then replace C by a bitmap container with the same values
L7  else set bit l of C, and if it was 0 add 1 to the count of C
CONTAINS(R, x)
L8  i ← index of x >> 16 in R.keys by binary search; if absent return false
L9  return whether x AND 0xFFFF is in R.containers[i]   ▷ binary search in an array, one bit test in a bitmap
REMOVE(R, x)
L10 i ← index of x >> 16 in R.keys; if absent return
L11 delete l = x AND 0xFFFF from C = R.containers[i] if it is there, and update the count of a bitmap
L12 if C is a bitmap container and |C| ≤ 4096 then replace C by an array container with the same values
L13 if |C| = 0 then delete key i and its container
```

Line L2 may create a new key with an empty array container; line L5 then adds a value, so (I2) holds again at the end. Line L6 converts at 4097 values and line L12 converts back at 4096, so the layout always matches (I3) and (I4). Line L13 removes an empty chunk.

Union and intersection merge the sorted key arrays.

```pseudo id=setops
UNION(R, S)
U1  T ← empty; i ← 0; j ← 0
U2  while i < |R.keys| and j < |S.keys|
U3      if R.keys[i] < S.keys[j] then append a copy of key i of R and its container to T; i ← i + 1
U4      else if S.keys[j] < R.keys[i] then append a copy of key j of S and its container to T; j ← j + 1
U5      else append R.keys[i] and OR-CONTAINERS(R.containers[i], S.containers[j]) to T; i ← i + 1; j ← j + 1
U6  append copies of the remaining keys and containers of R and of S
U7  return T
OR-CONTAINERS(A, B)
U8  if both are arrays then merge them; if the result has more than 4096 values, make it a bitmap
U9  else OR the 1024 words of the two bitmaps (an array is first set into a bitmap), count the ones,
U10     and make the result an array if the count is at most 4096
```

INTERSECTION is the same merge, but it keeps only the common keys, combines their containers with AND, and drops empty results. For an array and a bitmap, AND keeps the array values whose bit is set, so the result is an array at once. For two arrays it is a merge, or a galloping search when one array is much shorter. For two bitmaps it is 1024 word ANDs and popcounts, then a conversion if the count is at most 4096.

## Example

Take $S = \{1, 5, 70000, 70001, 196617\}$. Since $70000 = 1 \cdot 65536 + 4464$ and $196617 = 3 \cdot 65536 + 9$, the keys are 0, 1 and 3, with the array containers $[1, 5]$, $[4464, 4465]$ and $[9]$. Key 2 has no members and takes no space.

- `contains(70001)`: $h = 1$, found at index 1; binary search for 4465 in $[4464, 4465]$ finds it.
- `contains(70002)`: $h = 1$; 4466 is not in the array, so the answer is false.
- `remove(196617)`: $h = 3$; the container $[9]$ becomes empty, and key 3 is deleted. The keys are now 0 and 1.

**Conversion.** Add the even numbers $0, 2, \ldots, 8190$, which all have key 0. After 4096 of them the container of key 0 is still an array, of 8 KB. Adding 1 makes 4097 values, and line L6 turns the container into a bitmap of 8 KB with 4097 ones. Removing 0 brings the count back to 4096, and line L12 turns it back into an array.

## Correctness

Each operation keeps (I1) to (I5) and returns what the abstract type asks for. ADD finds or creates the only key equal to $h(x)$, which keeps the keys sorted and unique, and puts $\ell(x)$ into that container; the conversion at line L6 changes the layout but not the set of values, and restores (I3) or (I4). CONTAINS returns true exactly when $\ell(x)$ is in the container of $h(x)$, which by (I5) means $x \in S$. REMOVE takes $\ell(x)$ out of the right container and restores (I2) and (I4) by lines L12 and L13. UNION and INTERSECTION visit the keys of both inputs in increasing order, so the keys of the result are increasing; on a common key, the chunk of $R \cup S$ is the union of the two chunks and the chunk of $R \cap S$ is their intersection, while a key in only one input contributes its whole chunk to the union and nothing to the intersection. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $m$ be the number of containers and $n = \lvert S \rvert$.

| operation | time | notes |
| --- | --- | --- |
| contains | $O(\log m + \log 4096)$ | binary search for the key, then binary search in an array or one bit test |
| add, remove | $O(m + 4096)$ worst case | shifting the key array and an array container; $O(\log m)$ for a bitmap container and an existing key |
| conversion | $O(4096)$ | array to bitmap and back, 1024 words |
| cardinality | $O(m)$ | sum of the stored counts |
| union, intersection | $O(m + m' + \sum \text{container work})$ | per common key, $O(c + c')$ for two arrays, $O(c)$ for an array and a bitmap, 1024 word operations for two bitmaps |
| space | at most $2n$ bytes of values, plus $O(m)$ | arrays take 16 bits for each value, and bitmaps fewer than 16 |

Since a chunk holds at most $2^{16}$ values, each container operation is bounded by a constant, about 1024 word operations; the bounds are in terms of the 16-bit chunk size, not $n$. The space bound holds because an array spends exactly 16 bits for each value and a bitmap holds more than 4096 values in $2^{16}$ bits.

## Variants

- **Run containers.** Lemire, Ssi-Yan-Kai and Kaser add a container of runs, which stores a block of consecutive values in 4 bytes. A run-optimize step converts each container to runs when that is smaller: a container with $r$ runs takes about $4r$ bytes, against $2c$ bytes for an array and 8 KB for a bitmap.
- **64-bit values.** Implementations for 64-bit integers put a map, or a tree such as an adaptive radix tree, from the high 48 bits to 32-bit Roaring bitmaps or directly to containers.
- **Frozen and serialized forms.** The libraries define a portable format, so that a bitmap can be written to disk and used in place by mapping the file into memory.
- **Vectorized operations.** Lemire and coauthors, in the 2018 paper, use vector instructions to intersect arrays and to compute the popcount of the result of bitmap operations.
- **Other compressed bitmaps.** Word-aligned hybrid codes, such as WAH, Concise and EWAH, compress the bit vector with [run-length encoding](/run-length-encoding/) of words. They allow no random access, so membership takes a scan; Chambi and coauthors report that Roaring is often faster and smaller than them.

## When to use it

Use a Roaring bitmap for sets of 32-bit integers that are large and of mixed density, where fast union, intersection and membership matter: the row sets of a [bitmap index](/bitmap-index/), the posting lists of an [inverted index](/inverted-index/), and filters in analytic databases and search engines. For a small universe that is dense, a plain [bit vector](/bit-set/) is simpler and faster. For a static sorted list that is only scanned, [Elias-Fano encoding](/elias-fano-encoding/) is more compact. For sets of arbitrary keys, use a hash set or a [B-tree](/b-tree/).

## Pitfalls

- **Wrong threshold test.** The array holds at most 4096 values. Converting at 4096 instead of 4097, or back at 4097, breaks the space guarantee or the rule that a bitmap has more than 4096 values.
- **Stale counts.** A bitmap container keeps its count. Every path that sets or clears a bit must update it, or the conversions happen at the wrong times.
- **Empty containers.** An intersection can produce empty chunks. They must be dropped, or iteration and the key search see keys without members.
- **Insertion order.** Adding values one by one into many array containers costs a shift for each insertion. For bulk loading, sort the values first or use the bulk constructors of the libraries.
- **Signed integers.** The structure is defined for unsigned values. In Java, where `int` is signed, the libraries order values as unsigned; negative values sort after the positive ones.

## Implementations

## History

Chambi, Lemire, Kaser and Godin introduced Roaring bitmaps in "Better bitmap performance with Roaring bitmaps" (Software Practice and Experience, 2016), with array and bitmap containers and comparisons against the run-length compressed bitmaps WAH and Concise. Lemire, Ssi-Yan-Kai and Kaser added run containers in "Consistently faster and smaller compressed bitmaps with Roaring" (2016). Lemire and coauthors described the optimized C library CRoaring, with vectorized algorithms and a portable format, in 2018.

## References
