---
tag: X591T6
kind: data-structure
slug: extendible-hashing
name: Extendible hashing
aliases:
- directory-based hashing
area: data-structures/hashing
level: advanced
summary: Disk-oriented hashing with a directory that doubles, splitting only overflowing buckets.
implements: [dictionary]
model: word-ram
complexity:
  vars: {n: the number of keys, b: the capacity of a bucket, d: the global depth}
  time: {worst: O(b + 2^d)}
  space: {extra: Θ(2^d + n)}
prereqs: [hash-table, hash-function, dictionary, load-factor]
see_also: [linear-hashing, dynamic-hashing, b-tree, trie, rehashing, external-memory-model]
sources:
  - url: https://en.wikipedia.org/wiki/Extendible_hashing
    title: Wikipedia, Extendible hashing
    locator: the sections on the example and on the implementation
  - paper: doi:10.1145/320083.320092
    title: Ronald Fagin, Jürg Nievergelt, Nicholas Pippenger and H. Raymond Strong, Extendible hashing, a fast access method for dynamic files, ACM Transactions on Database Systems 4(3), 1979
    locator: pages 315 to 344 (the directory, the global and local depths, splitting and merging)
  - paper: doi:10.1007/bf00264279
    title: Philippe Flajolet, On the performance evaluation of extendible hashing and trie searching, Acta Informatica 20, 1983
    locator: Acta Informatica 20(4), pages 345 to 369 (the asymptotic size of the directory)
---

Extendible hashing is a [hash table](/hash-table/) for data on disk that keeps a directory of $2^d$ pointers to buckets of at most $b$ keys, and finds the bucket of a key $k$ from the low $d$ bits of its hash value $h(k)$. When a bucket overflows, only that bucket splits in two, and the directory doubles only when the bucket that splits is pointed to by a single directory entry. A search reads one directory entry and one bucket, so it costs at most two disk accesses, and one if the directory is in memory. Fagin, Nievergelt, Pippenger and Strong introduced it in 1979, as a [dictionary](/dictionary/) for files that grow and shrink without a full [rehash](/rehashing/).

## In plain words

Think of a set of drawers, each with room for a few cards, and a small index on the wall. To find a card, you look at the last few bits of its hash number. The index says which drawer holds the cards that end with these bits.

When a drawer is full, you do not rebuild everything. You take one new drawer and split the cards of the full drawer between the two, by one more bit of the hash number. If the index is too coarse to tell the two drawers apart, you make the index twice as long, with each old line written twice. Most drawers are not touched by the split. So the table grows one drawer at a time, and a search still reads one line of the index and one drawer.

## The abstract type

Extendible hashing implements the [dictionary](/dictionary/) abstract type: `insert(T, k, v)`, `search(T, k)`, `delete(T, k)` and `size(T)` on a finite map with distinct keys. It needs an equality test and a hash function $h$ that gives $W$-bit values, for example $W = 64$. It does not support ordered queries.

## Representation

The fields are the global depth $d \ge 0$, the directory $\text{dir}[0 \ldots 2^d - 1]$ of pointers to buckets, the bucket capacity $b \ge 1$, and the count $n$. Each bucket $B$ holds a list of pairs and a local depth $\ell(B)$. We write $\text{low}_j(x) = x \bmod 2^j$ for the low $j$ bits of $x$, and "bit $j$ of $x$" for $\lfloor x / 2^j \rfloor \bmod 2$.

**Invariant.**

- **(E1) Directory.** For each bucket $B$ there is a pattern $p(B)$ of $\ell(B) \le d$ bits such that $\text{dir}[i] = B$ exactly for the $2^{d - \ell(B)}$ indices $i$ with $\text{low}_{\ell(B)}(i) = p(B)$.
- **(E2) Placement.** Each pair $(k, v)$ in a bucket $B$ has $\text{low}_{\ell(B)}(h(k)) = p(B)$.
- **(E3) Distinct keys.** No key occurs in two pairs.
- **(E4) Count.** $n$ is the total number of pairs.
- **(E5) Capacity.** Each bucket $B$ has at most $b$ pairs, unless $\ell(B) = W$.

By (E1) and (E2), a pair with key $k$ can only be in the bucket $\text{dir}[\text{low}_d(h(k))]$. If the pair is in bucket $B$, then by (E2) $p(B) = \text{low}_{\ell(B)}(h(k)) = \text{low}_{\ell(B)}(i)$ for $i = \text{low}_d(h(k))$, because $\ell(B) \le d$. So by (E1), $\text{dir}[i] = B$.

## Operations

```pseudo id=main
EH-SEARCH(T, k)
L1  B ← T.dir[h(k) mod 2^T.d]
L2  if B holds a pair (k, v) then return v
L3  return NIL

EH-INSERT(T, k, v)
L4  B ← T.dir[h(k) mod 2^T.d]
L5  if B holds a pair with key k then replace its value by v; return
L6  while |B| = b and ℓ(B) < W do
L7      if ℓ(B) = T.d then T.dir[i + 2^T.d] ← T.dir[i] for 0 ≤ i < 2^T.d; T.d ← T.d + 1
L8      B′ ← a new empty bucket; ℓ(B) ← ℓ(B) + 1; ℓ(B′) ← ℓ(B)
L9      move each pair (k′, v′) of B with bit ℓ(B) − 1 of h(k′) equal to 1 into B′
L10     for each i < 2^T.d with T.dir[i] = B and bit ℓ(B) − 1 of i equal to 1 do T.dir[i] ← B′
L11     B ← T.dir[h(k) mod 2^T.d]
L12 add (k, v) to B; T.n ← T.n + 1

EH-DELETE(T, k)
L13 B ← T.dir[h(k) mod 2^T.d]
L14 if B holds a pair with key k then remove it; T.n ← T.n − 1
```

**Search.** Line L1 reads one directory entry, and line L2 scans one bucket of at most $b$ pairs. The cost is $O(b)$, and on disk it is two block reads.

**Insert.** Lines L4 and L5 handle a key that is present. If the bucket $B$ of $k$ is full, the loop of lines L6 to L11 splits it. Line L7 doubles the directory when $\ell(B) = d$, because then only one entry points to $B$ and the split needs one more bit. The new half of the directory is a copy of the old half, so each bucket keeps its pattern and has twice as many entries. Lines L8 to L10 split $B$ on bit $\ell(B)$ of the old local depth: the pairs and the directory entries with that bit equal to 1 go to $B'$. Line L11 finds the bucket of $k$ again. If all pairs went to the same side, that bucket is still full and the loop splits again. Line L12 adds the pair. A split costs $O(b + 2^d)$ with a scan of the directory, and a doubling costs $O(2^d)$.

**Delete.** Lines L13 and L14 remove the pair from its bucket. This version does not merge buckets. The paper of Fagin and others also merges a bucket with its buddy, the bucket whose pattern differs only in the last bit, when the two fit in one bucket, and halves the directory when each bucket has $\ell(B) < d$.

## Example

Take $b = 2$, $h(k) = k$, and start with $d = 0$ and one empty bucket A with $\ell = 0$. Insert 4, 12, 7, 9, 2, 16 and 6. The directory column lists the bucket of each index $0, 1, \ldots, 2^d - 1$.

| insert | binary | what happens | $d$ | directory | buckets |
|---|---|---|---|---|---|
| 4 | 00100 | into A | 0 | A | A($\ell$=0): 4 |
| 12 | 01100 | into A | 0 | A | A(0): 4 12 |
| 7 | 00111 | A full, $\ell = d$: double, split A on bit 0 into A and B | 1 | A B | A(1): 4 12, B(1): 7 |
| 9 | 01001 | into B | 1 | A B | A(1): 4 12, B(1): 7 9 |
| 2 | 00010 | A full, $\ell = d$: double, split A on bit 1, new C is empty, 2 goes to C | 2 | A B C B | A(2): 4 12, B(1): 7 9, C(2): 2 |
| 16 | 10000 | A full, $\ell = d$: double, split A on bit 2, 4 and 12 go to the new D | 3 | A B C B D B C B | A(3): 16, B(1): 7 9, C(2): 2, D(3): 4 12 |
| 6 | 00110 | into C | 3 | A B C B D B C B | A(3): 16, B(1): 7 9, C(2): 2 6, D(3): 4 12 |

Bucket B has local depth 1, so $2^{3-1} = 4$ entries point to it: the odd indices 1, 3, 5 and 7. The split for key 2 puts no key in the new bucket C, since 4 and 12 both have bit 1 equal to 0. A search for 12 reads $\text{dir}[12 \bmod 8] = \text{dir}[4] = D$ and finds 12. A search for 5 reads $\text{dir}[5] = B$ and returns NIL.

## Correctness

Each operation keeps (E1) to (E5) and returns what the dictionary asks for. A search is correct because, by (E1) and (E2), the only bucket that can hold key $k$ is $\text{dir}[\text{low}_d(h(k))]$. Doubling the directory keeps (E1), because a bucket with pattern $p$ of $\ell \le d$ bits is pointed to by all $i < 2^{d+1}$ with $\text{low}_\ell(i) = p$ after the copy. A split of $B$ with pattern $p$ and depth $\ell$ gives $B$ the pattern $p$ and $B'$ the pattern $p + 2^\ell$, both of depth $\ell + 1$, and moves both the pairs and the directory entries by the same bit, which keeps (E1) and (E2). The loop ends because each round raises $\ell(B)$ for the bucket that it splits, and $\ell(B) \le W$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Search and delete.** One directory entry and one bucket, so $O(b)$ time in the worst case, and two block reads on disk (one if the directory stays in memory). This holds for any keys.

**Insert.** Without a split, $O(b)$. Each round of the loop costs $O(b)$ for the split and $O(2^{d'})$ for the doubling and the scan of line L10, where $d'$ is the global depth in that round. The loop runs at most $W$ times, and the depths $d'$ of the rounds do not decrease, so the sum of the $2^{d'}$ terms is at most $W \cdot 2^{d}$, where $d$ is the global depth after the insert. So an insert costs $O(W(b + 2^d))$ in the worst case. In the table below, $W$ is a constant, so this is $O(b + 2^d)$.

**Space.** There are at most $2^d$ buckets, since each one has a directory entry, and $n$ pairs, so the space is $\Theta(2^d + n)$. The directory is the weak point. Flajolet proved that, for $n$ keys with independent uniform hash values, the expected directory size is of order $n^{1 + 1/b} / b$, which grows faster than $n$. For $b$ in the hundreds, as on disk, the extra factor $n^{1/b}$ is small. The buckets are about $\ln 2 \approx 69$ percent full on average for uniform hash values.

| operation | worst case | notes |
|---|---|---|
| search | $O(b)$ | 1 directory entry, 1 bucket |
| delete | $O(b)$ | without merging |
| insert | $O(b + 2^d)$ | a doubling copies the directory |
| space | $\Theta(2^d + n)$ | the expected directory size is of order $n^{1+1/b}/b$ for uniform hash values |

## Variants

- **Bits from the top.** The paper of Fagin and others indexes the directory by the leading $d$ bits of $h(k)$, so that the directory is a [trie](/trie/) on the hash values cut at depth $d$. The low bits, used here, give the same structure.
- **Merging on delete.** Merge a bucket with its buddy when they fit in one bucket, and halve the directory when no bucket has local depth $d$.
- **Linear hashing.** [Linear hashing](/linear-hashing/), by Litwin, has no directory. It splits the buckets in a fixed round-robin order and uses overflow chains.
- **B-trees.** A [B-tree](/b-tree/) is the other standard index on disk. It keeps the keys in order, at the cost of $O(\log_b n)$ block reads for a search.

## When to use it

Use extendible hashing for an index on disk or in a key-value store when the number of keys changes a lot over time and each search must read only a few blocks. It grows without a full rehash, and each split touches one bucket. Do not use it when the hash values can be chosen by an adversary or have many equal low bits, because the directory then doubles many times for a few keys. Use a [B-tree](/b-tree/) when you need range queries. In memory, an ordinary [hash table](/hash-table/) with doubling is simpler and faster.

## Pitfalls

- **Doubling for every split.** Line L7 must double the directory only when $\ell(B) = d$. If it doubles on each split, the directory grows with each overflow and wastes space.
- **Splitting only once.** If the loop of lines L6 to L11 is an `if`, then after a split where all pairs go to one side, line L12 adds a pair to a full bucket and breaks (E5). The insert of 2 in the example shows this case.
- **Equal hash values.** If more than $b$ keys have the same $W$-bit hash value, splits can never separate them. Without the test $\ell(B) < W$ of line L6, the insert loops forever, and even with it the directory grows to $2^W$ entries. In Python, `hash(-1)` and `hash(-2)` are both $-2$, so with $b = 1$ these two keys alone force this case. Use a hash function with few collisions, bound the depth, and allow an overflow bucket, as (E5) does.
- **Updating only one directory entry.** After a split of a bucket with $\ell(B) < d$, several directory entries point to it. Line L10 must move every entry with the new bit equal to 1 to $B'$, not only the entry of $k$, or (E1) breaks and later searches go to the wrong bucket.
- **Using the wrong bit.** The split uses bit $\ell(B) - 1$ after line L8 increments $\ell(B)$, that is, the old local depth. Using bit $\ell(B)$ instead moves the wrong pairs.

## Implementations

The Python version uses the low bits of a hash value of $W = 64$ bits. It takes the hash function as a parameter, so the tests can use $h(k) = k$ as in the example.

## History

Ronald Fagin, Jürg Nievergelt, Nicholas Pippenger and H. Raymond Strong published extendible hashing in ACM Transactions on Database Systems in 1979, with the directory, the local and global depths, splits, merges and a performance analysis. Philippe Flajolet gave the exact asymptotic analysis of the directory size in 1983, through the connection with tries.

## References
