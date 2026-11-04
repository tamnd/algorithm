---
tag: EHFR24
kind: data-structure
slug: counting-bloom-filter
name: Counting Bloom filter
aliases:
- counting Bloom filter
area: data-structures/probabilistic-structures
level: core
summary: Bloom filter with small counters in place of bits, allowing deletions.
model: word-ram
complexity:
  vars: {n: the number of stored keys, m: the number of counters, k: the number of hash functions, c: the bits per counter}
  time: {worst: Θ(k)}
  space: {extra: Θ(m c)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [bloom-filter, binomial-coefficient-bounds, union-bound]
see_also: [spectral-bloom-filter, cuckoo-filter, quotient-filter, count-min-sketch, approximate-membership, bloom-filter-optimal-hash-count]
sources:
  - paper: doi:10.1109/90.851975
    title: Li Fan, Pei Cao, Jussara Almeida and Andrei Z. Broder, Summary cache, a scalable wide-area Web cache sharing protocol, IEEE/ACM Transactions on Networking 8(3), 2000
    locator: pages 281 to 293, Section V (counting Bloom filters, 4-bit counters and the bound on counter overflow)
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2.4 (counting Bloom filters and the overflow probability)
---

A counting Bloom filter replaces each bit of a [Bloom filter](/bloom-filter/) by a small counter, so that keys can be deleted as well as inserted. INSERT$(x)$ adds 1 to the $k$ counters at the positions of $x$, DELETE$(x)$ subtracts 1 from them, and QUERY$(x)$ answers "maybe present" when all $k$ counters are nonzero. With 4-bit counters and the usual number of hash functions, the chance that any counter overflows is about $1.37 \cdot 10^{-15}$ times the number of counters, so the filter costs four times the memory of a Bloom filter with the same false positive rate. Fan, Cao, Almeida and Broder introduced it in 2000 for the summary cache protocol of Web proxies.

## In plain words

A Bloom filter turns switches on and can never turn them off, because a switch can be shared by several stored words. A counting Bloom filter puts a small counter in each place in its place. Storing a word adds one to each of its counters, and removing the word takes one away again.

A counter is zero only when no stored word uses it. So a lookup still says "surely absent" when it finds a zero, and "maybe present" when all its counters are above zero, exactly as before.

The counters are small, often four bits, so they can count only to fifteen. This is almost always enough. If a counter does reach its top value, it stays there for ever. That place can no longer go back to zero, but no stored word is ever lost.

## The abstract type

The filter solves the dynamic version of the [approximate membership problem](/approximate-membership/) for a multiset $S$ of keys. INSERT$(x)$ adds one copy of $x$ to $S$. DELETE$(x)$ removes one copy of $x$, and is allowed only when $x$ has a copy in $S$. QUERY$(x)$ returns true for each $x$ in $S$, and returns true for an $x$ not in $S$ only with a small probability. The filter cannot check the precondition of DELETE: it does not store the keys.

## Representation

The filter is an array $C[0 \ldots m-1]$ of counters of $c$ bits each, with the largest value $c_{\max} = 2^c - 1$, and $k$ [hash functions](/hash-function/) $h_1, \ldots, h_k$ from the universe to $\{0, \ldots, m - 1\}$. For a position $j$ let $N_j$ be the number of pairs (copy of $x$ in $S$, $i$) with $h_i(x) = j$. A key whose positions repeat counts once for each repeat.

**Invariant (C).** For each position $j$, either $C[j] = N_j$ and counter $j$ has never reached $c_{\max}$, or $C[j] = c_{\max}$.

So a counter below the top value is exact, and a counter at the top value is *stuck*: no operation changes it again. In both cases $C[j] = 0$ implies $N_j = 0$.

## Operations

```pseudo id=main
CREATE(m, k, c)
L1  C ← an array of m counters of c bits, all 0
L2  choose hash functions h_1, ..., h_k : U → {0, ..., m − 1}

INSERT(C, x)
L3  for i ← 1 to k do
L4      if C[h_i(x)] < c_max then C[h_i(x)] ← C[h_i(x)] + 1     ▷ a full counter sticks

DELETE(C, x)                                               ▷ precondition: x is in S
L5  for i ← 1 to k do
L6      if C[h_i(x)] < c_max then C[h_i(x)] ← C[h_i(x)] − 1     ▷ a stuck counter stays

QUERY(C, x)
L7  for i ← 1 to k do
L8      if C[h_i(x)] = 0 then return false                 ▷ x is not in S
L9  return true                                            ▷ x is in S, or a false positive
```

**Insert.** Lines L3 and L4 add 1 to each counter of $x$. A counter that holds $c_{\max}$ is not changed, so it never wraps around to 0.

**Delete.** Lines L5 and L6 subtract 1 from each counter of $x$, except a stuck counter. A stuck counter may hold fewer than $c_{\max}$ real entries, so it cannot know when it should leave the top value. Leaving it at $c_{\max}$ costs at most some false positives at that position.

**Query.** Lines L7 to L9 are the query of a Bloom filter, with "counter is 0" in place of "bit is 0".

**Conversion.** The array of the bits $[C[j] > 0]$ is exactly the Bloom filter of the distinct keys in $S$ when no counter is stuck. A server can keep a counting filter and send the much smaller Bloom filter to its clients, which is how the summary cache protocol uses it.

## Example

Let $m = 10$, $k = 3$ and $c = 4$, with these positions.

| key | $h_1$ | $h_2$ | $h_3$ |
|---|---|---|---|
| a | 0 | 3 | 7 |
| b | 3 | 5 | 9 |
| c | 1 | 5 | 7 |
| d | 0 | 1 | 9 |

| after | $C[0 \ldots 9]$ |
|---|---|
| insert a | 1 0 0 1 0 0 0 1 0 0 |
| insert b | 1 0 0 2 0 1 0 1 0 1 |
| insert c | 1 1 0 2 0 2 0 2 0 1 |
| delete b | 1 1 0 1 0 1 0 2 0 0 |

Before the delete, QUERY(d) finds counters 0, 1 and 9 all nonzero and returns true, a false positive. After the delete, counter 9 is 0 again, so QUERY(b) and QUERY(d) both return false. QUERY(a) and QUERY(c) still return true: counters 3 and 5 went from 2 to 1, not to 0, because a and c also use them. A plain Bloom filter would have to clear bits 3, 5 and 9 to delete b, and then QUERY(a) and QUERY(c) would wrongly return false.

## Correctness

Invariant (C) holds after each operation: an insert or delete of $x$ changes $N_j$ by the number of $i$ with $h_i(x) = j$, and lines L4 and L6 change $C[j]$ by the same amount unless the counter is stuck. A counter that reaches $c_{\max}$ is never written again. So $C[j] = 0$ implies that no copy in $S$ uses position $j$, and QUERY returns true for each key in $S$. The precondition of DELETE is needed: without it, $N_j$ could become negative in the analysis, and a counter that a stored key needs could fall to 0. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory probes |
|---|---|---|
| create | $\Theta(m)$ counter writes | none |
| insert, delete | $k$ hash evaluations | $k$ reads and writes |
| query | at most $k$ hash evaluations | at most $k$ |
| space | $m c$ bits | |

**False positive rate.** When no counter is stuck, the zero pattern of $C$ is the bit array of a Bloom filter of the distinct keys of $S$. So the rate is that of a Bloom filter with $m$ bits and $n$ keys, about $(1 - e^{-kn/m})^k$, and the best $k$ is $(m/n)\ln 2$ as in the [optimal hash count theorem](/bloom-filter-optimal-hash-count/). The filter uses $c$ times as many bits as the Bloom filter with the same rate.

**Overflow.** Let $n$ distinct keys be stored once each, with ideal hashing and $k \le (m/n)\ln 2$. Then
$$ \Pr[\text{some counter reaches } i] \le m \left(\frac{e \ln 2}{i}\right)^i. $$
The proof uses the bound $\binom{kn}{i} \le (ekn/i)^i$ from the [binomial coefficient bounds](/binomial-coefficient-bounds/) and the [union bound](/union-bound/) over the $m$ counters, and is in [the complexity proof](proofs/complexity.md).

| counter value $i$ | 8 | 12 | 15 | 16 |
|---|---|---|---|---|
| $(e \ln 2/i)^i$ | $9.5 \cdot 10^{-6}$ | $2.3 \cdot 10^{-10}$ | $3.1 \cdot 10^{-14}$ | $1.37 \cdot 10^{-15}$ |

A 4-bit counter is stuck only if it reaches 15. Even with $m = 10^9$ counters this has probability below $10^{-4}$. Fan et al. (2000) gave the bound $1.37 \cdot 10^{-15} \cdot m$ for a count of 16.

## Variants

- **Spectral Bloom filter.** Read the minimum of the $k$ counters as an estimate of the multiplicity of $x$. See the [spectral Bloom filter](/spectral-bloom-filter/), and the [count-min sketch](/count-min-sketch/), which has one counter row for each hash function.
- **Wider counters.** With $c = 8$ or more, overflow never happens in practice, at twice the memory of $c = 4$.
- **Fingerprint filters.** A [cuckoo filter](/cuckoo-filter/) or a [quotient filter](/quotient-filter/) supports deletes in about $\log_2(1/\varepsilon) + 3$ bits per key, much less than $4 \cdot 1.44 \log_2(1/\varepsilon)$, and the counting quotient filter of Pandey et al. also counts multiplicities.
- **Stream filters.** The [stable Bloom filter](/stable-bloom-filter/) decrements random counters to forget old keys of a stream, and so allows false negatives.

## When to use it

Use a counting Bloom filter when a set changes by inserts and deletes, all deletes are of keys that are really present, and a plain Bloom filter must be derived from it, as in the summary cache protocol. It is also simple to make concurrent, because each counter is updated on its own. For a filter that is kept only in memory and needs deletes, a [cuckoo filter](/cuckoo-filter/) usually needs less than a third of the space for the same rate.

## Pitfalls

- **Deleting an absent key.** If $x$ was never inserted but QUERY$(x)$ returns true, DELETE$(x)$ decrements counters that other keys need, and a later query can give a false negative. Delete only keys that are known to be present, for example because an exact table elsewhere holds them.
- **Wrap-around.** A counter that is incremented past $c_{\max}$ without a check becomes 0, and gives false negatives for each key that uses it. Line L4 makes the counter stick.
- **Decrementing a stuck counter.** A stuck counter may have lost track of its count. Decrementing it can bring it to 0 while keys still use it. Line L6 leaves it at $c_{\max}$.
- **Repeated inserts.** The overflow bound is for distinct keys inserted once. A key inserted 20 times saturates its 4-bit counters at once. Keep a set, not a multiset, if this can happen, or use wider counters.
- **Sizing by the Bloom filter.** The rate depends on the number of nonzero counters, so $m$ must be sized for the largest number of keys present at one time, not for the total number of inserts.

## Implementations

The Python class follows the main block with BLAKE2b and double hashing, and adds a count of the stuck counters.

## History

Fan, Cao, Almeida and Broder (2000) introduced counting Bloom filters in the summary cache protocol, in which each Web proxy keeps a summary of its cache and sends a Bloom filter of it to the other proxies. They proposed 4-bit counters and gave the overflow bound. Broder and Mitzenmacher's survey (2004) presents the structure and its analysis. Later work, such as the [spectral Bloom filter](/spectral-bloom-filter/) of Cohen and Matias (2003), used the counters to estimate multiplicities.

## References
