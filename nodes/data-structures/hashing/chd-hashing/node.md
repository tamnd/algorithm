---
tag: X3MZCW
kind: algorithm
slug: chd-hashing
name: CHD perfect hashing
aliases:
- compress hash and displace
- hash, displace, and compress
area: data-structures/hashing
level: research
summary: Practical minimal perfect hashing that uses displacement tables and about 2 bits per key.
solves: [static-dictionary-problem]
model: word-ram
complexity:
  vars: {n: the number of keys}
  time: {expected: O(n)}
  space: {extra: O(n)}
properties: {deterministic: false}
prereqs: [fks-perfect-hashing, minimal-perfect-hashing, hash-function]
see_also: [perfect-hash-function, minimal-perfect-hash-function, perfect-hashing, bloomier-filter, xor-filter, elias-fano-encoding, rank-select-dictionary, uniform-hashing-assumption]
sources:
  - paper: doi:10.1007/978-3-642-04128-0_61
    title: Djamal Belazzougui, Fabiano C. Botelho and Martin Dietzfelbinger, Hash, displace, and compress, Algorithms, ESA 2009, LNCS 5757
    locator: pages 682 to 693 (the algorithm, its analysis with fully random hash functions, and the space figures)
  - paper: doi:10.1007/3-540-48447-7_5
    title: Rasmus Pagh, Hash and displace, efficient evaluation of minimal perfect hash functions, Algorithms and Data Structures, WADS 1999, LNCS 1663
    locator: pages 49 to 54 (the hash and displace scheme that CHD changes)
  - paper: doi:10.1145/828.1884
    title: Michael L. Fredman, János Komlós and Endre Szemerédi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3), 1984
    locator: pages 538 to 544 (the two-level idea, buckets that get their own function)
---

CHD builds a [minimal perfect hash function](/minimal-perfect-hash-function/) for a fixed set of $n$ keys: a function that maps the keys one to one onto $\{0, \ldots, n - 1\}$, evaluated in $O(1)$ time and stored in a few bits for each key. It splits the keys into small buckets with one hash function, and then, from the largest bucket to the smallest, chooses for each bucket the first pair of displacements that sends all its keys to free slots. The table of chosen indices is the whole function, and since most indices are small, it compresses well. Belazzougui, Botelho and Dietzfelbinger published it in 2009 as "hash, displace, and compress", a change of the hash and displace method of Pagh.

## In plain words

We want to give each of $n$ known keys its own number from 0 to $n - 1$, without storing the keys. First, a hash function sorts the keys into many small groups, about five keys in each. Then we handle the groups one at a time, largest first. For a group, we try a list of simple ways to move its keys around the table, in a fixed order, and keep the first way that puts each key of the group in an empty slot, with no two keys in the same slot. We remember only the position of that way in the list. To find the number of a key later, compute its group, read the remembered position, and apply that way to the key. Large groups go first, while the table is still nearly empty and easy to fill.

## The problem

The input is a set $S$ of $n$ distinct keys from a universe $U$ and a table size $m \ge n$. The output is a function $\phi : U \to \{0, \ldots, m - 1\}$ that is one to one on $S$, a [perfect hash function](/perfect-hash-function/). When $m = n$, it is a bijection from $S$ onto $\{0, \ldots, n - 1\}$, a minimal one. The function need not say whether a key is in $S$: a key outside $S$ gets some slot. To answer membership, store each key, or a value for it, in slot $\phi(x)$ of an array, as for the [static dictionary problem](/static-dictionary-problem/). The goals are a small description of $\phi$, $O(1)$ evaluation time and a fast build.

## The algorithm

Let $r = \lceil n / \lambda \rceil$ be the number of buckets, where $\lambda$ is the average bucket size, a small constant; the Python version uses $\lambda = 5$ by default. Use three hash functions: $g : U \to [r]$ chooses the bucket, and $f_1, f_2 : U \to [m]$ give each key a start and a step. A **displacement index** $\ell \in \{0, \ldots, m^2 - 1\}$ stands for the pair $(d_0, d_1) = (\lfloor \ell / m \rfloor, \ell \bmod m)$, and sends the key $x$ to the slot

$$s_\ell(x) = (f_1(x) + d_0 \, f_2(x) + d_1) \bmod m.$$

The order of the pairs, $d_1$ fastest, is the choice of this page.

```pseudo id=main
CHD-BUILD(S, m, r)
L1  repeat
L2      pick g, f_1, f_2 at random
L3      B_i ← {x ∈ S : g(x) = i} for each i ∈ [r]
L4      mark all m slots free; ok ← true
L5      for each bucket i, in order of |B_i| from largest to smallest do
L6          ℓ ← 0
L7          while ℓ < m² and the slots s_ℓ(x), x ∈ B_i, are not distinct and free do ℓ ← ℓ + 1
L8          if ℓ = m² then ok ← false; break
L9          σ[i] ← ℓ; mark the slots s_ℓ(x), x ∈ B_i, as used
L10 until ok
L11 return (g, f_1, f_2, σ)

CHD-EVAL(x)
L12 i ← g(x); (d_0, d_1) ← (⌊σ[i] / m⌋, σ[i] mod m)
L13 return (f_1(x) + d_0 · f_2(x) + d_1) mod m
```

Lines L5 to L9 are a greedy placement. Line L7 tries the indices $0, 1, 2, \ldots$ until all keys of the bucket land on distinct free slots, and line L9 fixes them there for good. An empty bucket takes $\ell = 0$. If no index works for some bucket, line L8 gives up, and line L10 restarts with new hash functions. A bucket of one key always fits while the table has a free slot $t$, by the index $\ell = (t - f_1(x)) \bmod m$, which has $d_0 = 0$. For a bucket of two keys or more, the step $f_2$ matters: two keys with the same $f_1$ collide for $d_0 = 0$, but not for $d_0 \ne 0$ when their $f_2$ values differ.

The **compress** part is the storage of $\sigma$. The early buckets meet a nearly empty table and take small indices, and the late buckets have one key and also need few trials until the table is nearly full. So most values of $\sigma$ are small, and a code with fewer bits for small numbers stores them compactly. The paper stores $\sigma$ with a compressed code that keeps $O(1)$ access to each entry; the Python version stores a plain list, and reports the size of an Elias gamma code of the indices as a measure.

## Example

Take $m = n = 10$, the keys $S = \{10, 22, 37, 40, 52, 60, 70, 72, 75, 88\}$, and $r = 4$ buckets ($\lambda = 3$). The hash functions are those that the Python version draws with `random.Random(1)` and $p = 101$; here we only need their values.

| bucket $i$ | keys of $B_i$ | $f_1$ values | $f_2$ values |
|---|---|---|---|
| 1 | 22, 37, 60, 70, 88 | 4, 2, 5, 9, 6 | 1, 7, 4, 0, 2 |
| 3 | 52, 72, 75 | 4, 0, 4 | 9, 0, 6 |
| 0 | 40 | 8 | 1 |
| 2 | 10 | 0 | 7 |

Line L5 takes the buckets in this order, largest first.

1. **Bucket 1.** For $\ell = 0$, the pair is $(0, 0)$ and the slots are the $f_1$ values 4, 2, 5, 9 and 6. They are distinct and free, so $\sigma[1] = 0$.
2. **Bucket 3.** The keys 52 and 75 have the same $f_1 = 4$, so every pair with $d_0 = 0$ fails. For $d_0 = 1$ the slots are $(3 + d_1, d_1, d_1) \bmod 10$, and 72 and 75 always collide. For $d_0 = 2$ the slots are $(2 + d_1, d_1, 6 + d_1) \bmod 10$. With $d_1 = 0$ they are 2, 0 and 6, and slot 2 is used. With $d_1 = 1$ they are 3, 1 and 7, all free. So $\sigma[3] = 2 \cdot 10 + 1 = 21$.
3. **Bucket 0.** The key 40 goes to slot $f_1 = 8$, which is free, so $\sigma[0] = 0$.
4. **Bucket 2.** The key 10 goes to slot $f_1 = 0$, the last free slot, so $\sigma[2] = 0$.

The result is $\sigma = [0, 0, 0, 21]$, and the ten keys fill the ten slots: 10 to 0, 72 to 1, 37 to 2, 52 to 3, 22 to 4, 60 to 5, 88 to 6, 75 to 7, 40 to 8 and 70 to 9. To evaluate the function at 75, compute $g(75) = 3$, read $\sigma[3] = 21$, decode $(d_0, d_1) = (2, 1)$, and return $(4 + 2 \cdot 6 + 1) \bmod 10 = 7$.

## Correctness

**Claim.** If CHD-BUILD returns, then CHD-EVAL is one to one on $S$ and maps into $[m]$, so it is a perfect hash function, and a minimal one when $m = n$.

The reason is an invariant of the loop of lines L5 to L9: after a bucket is placed, the used slots are exactly the slots $s_{\sigma[g(x)]}(x)$ of the keys of the buckets placed so far, and these slots are distinct. Line L9 adds the slots of the new bucket only when line L7 found them distinct and free. When the loop ends with ok true, every bucket is placed, and CHD-EVAL computes exactly $s_{\sigma[g(x)]}(x)$ for each key. When $m = n$, the $n$ distinct slots fill all of $[m]$. The build ends with probability 1 when the hash functions are fully random, because then each attempt succeeds with positive probability. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

The details are in [the complexity proof](proofs/complexity.md).

**Evaluation: $O(1)$ worst case.** CHD-EVAL computes three hash values, reads one entry of $\sigma$ and does a few arithmetic steps. With the compressed $\sigma$ of the paper, the read of one entry also takes $O(1)$ time.

**Space.** The plain form stores $r = \lceil n/\lambda \rceil$ indices, each less than $m^2$, and the seeds of the hash functions: $O(n)$ words. The paper shows that, with fully random hash functions, the compressed form uses a number of bits close to the lower bound for perfect hash functions; its abstract gives about 1.4 bits for each key for $m = 1.23n$, and about 1.98 bits for each key for $m = 1.01n$.

**Build time.** One trial of line L7 costs $O(|B_i|)$ time, and the bucket sizes sum to $n$, so the build costs $O(n + m)$ plus $O(\lambda)$ times the total number of trials. The paper proves, with fully random hash functions and a table with $m \ge (1 + \varepsilon) n$ for a constant $\varepsilon > 0$, that the expected total number of trials is $O(n)$, so the expected build time is $O(n)$. This step is given as a sketch in the complexity proof. For $m = n$, the last buckets meet a nearly full table, and the number of trials can be much larger. A minimal function can instead be built with $m$ a little larger than $n$, and then the used slots are mapped onto $[n]$, as in the variants below.

| quantity | bound | assumption |
|---|---|---|
| evaluation | $O(1)$ | worst case |
| build | $O(n)$ expected | fully random hash functions, $m \ge (1 + \varepsilon) n$ |
| plain space | $O(n)$ words | worst case |
| compressed space | about 2 bits for each key | the parameters of the paper |

## Properties

- **Static.** The set is fixed; adding a key means building again.
- **No membership.** The function gives some slot to every key, in $S$ or not. To reject keys outside $S$, store the keys, or short fingerprints of them, in the slots.
- **Las Vegas build.** The result is always perfect; only the build time is random.
- **Order of the buckets.** Placing large buckets first is what makes the method fast: a bucket of $k$ keys in a table with a fraction $\beta$ of free slots fits a random pair with probability about $\beta^k$, so large buckets must come while $\beta$ is close to 1.

## Variants and improvements

- **Hash and displace.** Pagh's scheme uses one displacement for each bucket, the slot $(f(x) + d_{g(x)}) \bmod m$, and was the starting point of CHD. CHD uses a pair $(d_0, d_1)$ and a single index for it, so the stored numbers are small, and it compresses them.
- **Non-minimal tables.** With $m = n / \alpha$ for a load $\alpha < 1$, the build is faster and the index table smaller. A minimal function then follows by mapping the used slots of $[m]$ onto $[n]$, for example with a [rank and select dictionary](/rank-select-dictionary/) on the bit vector of used slots.
- **$k$-perfect hashing.** The paper also builds functions where at most $k$ keys share a slot, for example when a slot is a block of memory with room for $k$ keys.
- **Other compact functions.** The [Bloomier filter](/bloomier-filter/) and the [XOR filter](/xor-filter/) build static functions by peeling a random hypergraph; later minimal perfect hash methods also use the bucket-and-search idea of CHD.

## When to use it

Use CHD to map a large fixed set of keys, such as the words of a dictionary or the URLs of a crawl, to dense numbers in a few bits for each key, when the keys themselves are kept elsewhere or not at all. If the set changes, use a [hash table](/hash-table/). If the space of the function does not matter and the keys are stored anyway, the two-level table of [FKS perfect hashing](/fks-perfect-hashing/) is simpler to analyze.

## Pitfalls

- **Equal pairs in a bucket.** Two keys of the same bucket with the same $f_1$ and the same $f_2$ collide for every pair $(d_0, d_1)$. Line L8 must detect this and restart with new hash functions, or the build never ends.
- **$m = n$ exactly.** With no spare slots, the last buckets with two or more keys can need many trials, or none may work. Use a load a little below 1, or put the buckets of one key last, as the order by size does.
- **Weak hash functions.** The analysis assumes fully random $g$, $f_1$ and $f_2$. With a weak family, keys can fall into a few large buckets and the build slows down. The paper notes that this assumption can be justified, as in earlier work; the Python version uses polynomials of degree 2 modulo a prime, for which the analysis is not proved.
- **Treating the output as a membership test.** A key outside $S$ gets a slot of a key in $S$. Check a stored key or fingerprint.

## Implementations

The Python version takes integer keys less than a prime $p$, and builds $g$, $f_1$ and $f_2$ from polynomials of degree 2 modulo $p$, reduced to $[r]$ and $[m]$. It uses $m = n$ by default. Its pseudocode line ids match the markers in the code.

## History

Fredman, Komlós and Szemerédi showed in 1984 how to give each bucket of a first-level hash its own function. Pagh's hash and displace of 1999 replaced the second-level functions by one displacement for each bucket, and placed the buckets in order of size. Belazzougui, Botelho and Dietzfelbinger presented CHD at the European Symposium on Algorithms in 2009, with displacement pairs, the compression of their indices, and an analysis that gives linear expected build time and a space close to the lower bound. An implementation is part of the CMPH library of Botelho and others.

## References
