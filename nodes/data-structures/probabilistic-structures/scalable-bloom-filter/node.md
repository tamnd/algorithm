---
tag: Q55J7F
kind: data-structure
slug: scalable-bloom-filter
name: Scalable Bloom filter
aliases:
- dynamic Bloom filter
area: data-structures/probabilistic-structures
level: advanced
summary: Chain of Bloom filters added as the set grows, keeping the false positive rate bounded.
model: word-ram
complexity:
  vars: {n: the number of inserted keys, l: the number of slices, k: the number of hash functions of the last slice}
  time: {worst: Θ(l k)}
  space: {extra: Θ(n k)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [bloom-filter, bloom-filter-optimal-hash-count, union-bound, geometric-series]
see_also: [false-positive-rate, approximate-membership, counting-bloom-filter, stable-bloom-filter, quotient-filter, cuckoo-filter]
sources:
  - paper: doi:10.1016/j.ipl.2006.10.007
    title: Paulo Sergio Almeida, Carlos Baquero, Nuno Preguica and David Hutchison, Scalable Bloom filters, Information Processing Letters 101(6), 2007
    locator: pages 255 to 261 (slices with growing size and a geometric series of error rates, partitioned slices with fill ratio one half)
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2 (the false positive rate of a Bloom filter and of the partitioned form)
---

A scalable Bloom filter is a [Bloom filter](/bloom-filter/) that does not need to know the number of keys in advance. It is a list of Bloom filters, the *slices*. New keys go into the last slice, and when that slice holds as many keys as it was planned for, a new slice is added that is $s$ times larger and has a false positive rate $r$ times smaller. A query asks every slice. The rates $\varepsilon_0, \varepsilon_0 r, \varepsilon_0 r^2, \ldots$ form a geometric series, so the [union bound](/union-bound/) keeps the total rate below $\varepsilon_0/(1 - r)$ however many keys arrive. The cost is a query time that grows with the number of slices, and about $\log_2(1/r)/\ln 2$ more bits per key for each new slice. Almeida, Baquero, Preguiça and Hutchison introduced it in 2007.

## In plain words

A Bloom filter must be given its size before the first key arrives. If more keys come than planned, it fills up and starts to say "maybe present" for almost every key.

A scalable Bloom filter solves this by starting small. When the current filter is full, it starts a new, larger one and puts all new keys there. The old filters are kept, so a lookup asks all of them and says "maybe present" if any one says so.

Each filter adds its own chance of a wrong "maybe". To keep the sum small, each new filter is made more careful than the one before: it uses more hash functions, so its own chance of error is a fixed fraction of the previous one. The chances then add up to a total that stays below a fixed limit for ever.

## The abstract type

The filter solves the incremental [approximate membership problem](/approximate-membership/) with no bound on the size of the set. INSERT$(x)$ adds $x$ to the set $S$, and QUERY$(x)$ returns true for each $x \in S$, and returns true for an $x \notin S$ with probability at most $\varepsilon = \varepsilon_0/(1 - r)$, at every size of $S$. There is no delete.

## Representation

The parameters are the part size $b_0 \ge 2$ of the first slice, the first rate $\varepsilon_0$, the tightening ratio $r \in (0, 1)$, and the growth factor $s \ge 1$. The filter is a list of slices $F_0, \ldots, F_{l-1}$. Slice $i$ is a *partitioned* Bloom filter:

- $k_i = \lceil \log_2(1/(\varepsilon_0 r^i)) \rceil$ parts $P_{i,1}, \ldots, P_{i,k_i}$ of $b_i = b_0 s^i$ bits each;
- one [hash function](/hash-function/) $h_{i,j}$ for each part, from the universe to $\{0, \ldots, b_i - 1\}$;
- a count $c(F_i)$ of the keys inserted into it, and the capacity $\kappa_i = \lfloor (b_i - 1)\ln 2 \rfloor$.

A key sets one bit in each part, so the parts are independent Bloom filters with one hash function each. The capacity is the largest count at which the expected fraction of 1 bits of each part is at most one half, which is the point where a Bloom filter with this many hash functions has its [best rate](/bloom-filter-optimal-hash-count/).

**Invariant (S).** Every slice except the last holds exactly $\kappa_i$ keys, the last slice holds between 1 and $\kappa_{l-1}$ keys, and the bit $P_{i,j}[p]$ is 1 exactly when some key inserted into slice $i$ has $h_{i,j}(x) = p$.

## Operations

```pseudo id=main
CREATE(b_0, ε_0, r, s)
L1  F ← an empty list of slices

ADD-SLICE(F)
L2  i ← the number of slices;  k_i ← ⌈log_2(1 / (ε_0 r^i))⌉;  b_i ← b_0 s^i
L3  append a slice with k_i parts of b_i bits, all 0, count 0, capacity ⌊(b_i − 1) ln 2⌋

INSERT(F, x)
L4  if F is empty or the last slice holds its capacity then ADD-SLICE(F)
L5  for j ← 1 to k of the last slice i do set P_{i,j}[h_{i,j}(x)] ← 1
L6  add 1 to the count of the last slice

QUERY(F, x)
L7  for each slice i do
L8      if P_{i,j}[h_{i,j}(x)] = 1 for every j ≤ k_i then return true
L9  return false
```

**Insert.** Line L4 starts a new slice when the last one is full, and lines L5 and L6 put the key into the last slice only. The older slices never change again.

**Query.** Lines L7 to L9 return true if any slice accepts $x$. The slices can be asked in any order; asking the largest slice first is faster on average when most queries are for keys that are present, since the last slices hold most of the keys.

**Why the rate tightens.** If every slice had the same rate $\varepsilon_0$, the total rate would grow with the number of slices and so with the logarithm of $n$. With rates $\varepsilon_0 r^i$ the sum is bounded by $\varepsilon_0/(1 - r)$, a [geometric series](/geometric-series/). Each new slice needs about $\log_2(1/r)$ more hash functions than the one before.

## Example

Let $b_0 = 4$, $\varepsilon_0 = 1/4$, $r = 1/2$ and $s = 2$. Slice 0 has $k_0 = 2$ parts of 4 bits and capacity $\lfloor 3 \ln 2 \rfloor = 2$. Slice 1 has $k_1 = 3$ parts of 8 bits and capacity $\lfloor 7 \ln 2 \rfloor = 4$. The positions are as follows, one for each part.

| key | slice 0 | slice 1 |
|---|---|---|
| a | 1, 2 | |
| b | 1, 3 | |
| c | 2, 0 | 0, 5, 2 |
| d | 3, 1 | 3, 5, 7 |
| e | 0, 0 | 6, 1, 2 |
| x | 1, 0 | 3, 5, 2 |
| y | 0, 2 | 0, 1, 1 |

Insert a, b, c, d and e in this order. The keys a and b fill slice 0, whose parts then have 1 bits at $\{1\}$ and $\{2, 3\}$. The insert of c finds slice 0 at its capacity, so line L4 adds slice 1, and c, d and e go there. Its three parts then have 1 bits at $\{0, 3, 6\}$, $\{1, 5\}$ and $\{2, 7\}$.

Every stored key is found. QUERY(x) fails in slice 0, because bit 0 of the second part is 0, but slice 1 has bits 3, 5 and 2 of its parts set, so it returns true: a false positive, made of bits of d, c and again c. QUERY(y) fails in slice 0 at bit 0 of the first part, and in slice 1 at bit 1 of the third part, so it returns false. The bound on the rate with two slices is $1/4 + 1/8 = 0.375$, and it never exceeds $1/2$.

## Correctness

No bit is ever cleared, and line L5 sets the $k_i$ bits of $x$ in the slice that takes it, so line L8 finds them for that slice and QUERY$(x)$ returns true for each inserted key. For an absent key, the parts of a slice are filled by independent hash functions, so the probability that slice $i$ accepts it is the product of the expected fill fractions of its parts, which is at most $2^{-k_i} \le \varepsilon_0 r^i$ by the choice of the capacity. The union bound over the slices gives at most $\varepsilon_0/(1 - r)$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| insert | $k_{l-1}$ hash evaluations and bit writes, plus $\Theta(k_{l-1} b_{l-1})$ to allocate a new slice |
| query | at most $\sum_{i < l} k_i = \Theta(l k)$ hash evaluations and bit reads |
| space | $\sum_{i < l} k_i b_i$ bits |

**Number of slices.** Slice $i$ holds about $b_0 s^i \ln 2$ keys. For $s \ge 2$, after $n$ inserts there are $l = \log_s(n/b_0) + O(1)$ slices, so a query costs $O(\log n \cdot (\log(1/\varepsilon_0) + \log n))$ time in the worst case. With $s = 1$ the slices do not grow and $l$ is linear in $n$, so this choice is only for small growth.

**Space.** For $s \ge 2$, the last slice holds a constant fraction of the keys and has the most hash functions, so the space is $\Theta(n k)$ bits with $k = k_{l-1}$, that is about $k_{l-1}/\ln 2$ bits per key when the slices are full. Compared with a Bloom filter of rate $\varepsilon$ sized in advance, the filter pays twice: once for the factor $1 - r$ in $\varepsilon_0 = \varepsilon(1 - r)$, which costs $\log_2(1/(1 - r))$ hash functions, and once for the $\log_2(1/r)$ more hash functions of each later slice. For $\varepsilon = 0.01$, $b_0 = 1000$, $s = 2$ and 11 full slices with 1.42 million keys, this gives these bits per key, against 9.59 for a single Bloom filter sized for the final $n$.

| $r$ | 0.5 | 0.8 | 0.9 |
|---|---|---|---|
| $\varepsilon_0$ | 0.005 | 0.002 | 0.001 |
| $k$ of the last slice | 18 | 13 | 12 |
| bits per key | 24.5 | 17.9 | 17.2 |

So the ratio $r$ should be close to 1, and the space grows only slowly with $n$, by about $0.22$ bits per key for each doubling when $r = 0.9$.

## Variants

- **Skip present keys.** An insert can first run QUERY$(x)$ and do nothing if it returns true. This saves room for repeated keys and is common in libraries. It makes the set of keys of a slice depend on the hash values, and the proof on this page does not cover that form.
- **Unpartitioned slices.** Each slice can be a plain Bloom filter of $k_i b_i$ bits with $k_i$ hash functions over the whole array. Its rate is about the same, but the exact rate is then slightly above the product formula, see the [false positive rate](/false-positive-rate/).
- **Growth factor.** Almeida et al. suggest a small $s$ such as 2 when the set grows slowly, and a larger $s$ such as 4 when it grows fast, since a larger $s$ gives fewer slices and so faster queries.
- **Other growing filters.** A [quotient filter](/quotient-filter/) or a [cuckoo filter](/cuckoo-filter/) can be resized or chained in the same way. A filter that must forget old keys instead of growing is the [stable Bloom filter](/stable-bloom-filter/).

## When to use it

Use a scalable Bloom filter when the number of keys is not known in advance, can vary by orders of magnitude, and the rate must stay below a fixed bound, for example in a crawler that records the URLs it has seen or in a store that keeps a filter for each data file of unknown size. If an upper bound on $n$ is known, a single Bloom filter sized for it uses less space and has faster queries.

## Pitfalls

- **The same rate in every slice.** With $r = 1$ the total rate grows with the number of slices, which is the error the structure is meant to prevent.
- **Asking only the last slice.** Keys stay in the slice that took them. A query must ask every slice, or it gives false negatives.
- **Correlated hash functions.** The positions in the parts of a slice must be independent. Double hashing $h_1 + j h_2 \bmod b$ with a part size $b$ that is a power of 2 gives only a few hundred distinct position lists for small $b$, and in a test of the Python code it made the rate of the first slice about four times too large. The Python code takes an independent 64-bit word of BLAKE2b for each part.
- **Repeated keys.** Without the skip of the variant above, a key inserted twice takes two places of the capacity. The bound on the rate still holds, but the space grows faster.
- **No deletes.** Bits are shared, as in every Bloom filter. A [counting Bloom filter](/counting-bloom-filter/) can be used for the slices if deletes are needed, with four times the space.

## Implementations

The Python class follows the main block. Each slice stores its parts as byte arrays, and the class also gives the current bound $\varepsilon_0 (1 + r + \cdots + r^{l-1})$ and the total number of bits.

## History

Almeida, Baquero, Preguiça and Hutchison (2007) proposed scalable Bloom filters, with the geometric series of rates, partitioned slices filled to one half, and growth by a factor $s$. They gave the bound $\varepsilon_0/(1 - r)$ and measured the space for several values of $r$ and $s$. The partitioned form of a Bloom filter, with one part for each hash function, is older, and the survey of Broder and Mitzenmacher (2004) discusses it.

## References
