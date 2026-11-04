---
tag: EA0KDC
kind: data-structure
slug: linear-hashing
name: Linear hashing
aliases:
- Litwin linear hashing
area: data-structures/hashing
level: advanced
summary: Dynamic hash table that grows one bucket at a time, without a full rehash.
implements: [dictionary]
model: word-ram
complexity:
  vars: {n: the number of keys, α: the maximum load factor}
  time: {search: O(1 + α), insert: O(1 + α + 1/α), delete: O(1 + α + 1/α)}
  space: {extra: Θ(n)}
prereqs: [rehashing, separate-chaining, load-factor]
see_also: [extendible-hashing, dynamic-hashing, hash-table, uniform-hashing-assumption, b-tree, external-memory-model, array-doubling, rehashing]
sources:
  - paper: "Witold Litwin, Linear Hashing: A New Tool for File and Table Addressing, Proceedings of the Sixth International Conference on Very Large Data Bases (VLDB), Montreal, 1980, pages 212 to 223"
    title: Witold Litwin, Linear Hashing, A New Tool for File and Table Addressing, VLDB 1980
    locator: the split pointer, the family of functions h_i, splits in linear order, and the controlled and uncontrolled split rules
  - paper: doi:10.1145/42404.42410
    title: "Per-Ake Larson, Dynamic Hash Tables, Communications of the ACM 31(4) (1988), 446-457"
    locator: linear hashing adapted to tables in main memory, with a directory of segments and splits controlled by the load factor
  - paper: "Per-Ake Larson, Linear Hashing with Partial Expansions, Proceedings of the Sixth International Conference on Very Large Data Bases (VLDB), Montreal, 1980, pages 224 to 232"
    title: Per-Ake Larson, Linear Hashing with Partial Expansions, VLDB 1980
    locator: the variant that expands the file in several partial steps for a more even load
---

Linear hashing is a [hash table](/hash-table/) that grows and shrinks by one bucket at a time. It keeps a split pointer $p$ and a level $L$: the table has $N \cdot 2^L + p$ buckets, and a key $k$ lives in bucket $h(k) \bmod N 2^L$, or in bucket $h(k) \bmod N 2^{L+1}$ when the first value is less than $p$. When the [load factor](/load-factor/) passes a limit, the table splits bucket $p$ into $p$ and $p + N 2^L$ and moves $p$ by one. So the cost of growth is spread over the insertions, and no operation moves more than one bucket, while a table that doubles by [rehashing](/rehashing/) moves all keys at once. Witold Litwin introduced it in 1980 for files on disk, where it needs no directory.

## In plain words

A hash table has a row of buckets, and each key goes to the bucket that its hash value picks. When the table gets full, the usual fix is to build a table twice as large and move every key. That pause can be long.

Linear hashing grows a little at a time. It adds one new bucket at the end of the row and splits one old bucket in two: the keys of the old bucket go either back to it or to the new bucket. The old buckets are split in order, whatever bucket is the fullest. A pointer marks the next bucket to split.

To find a key, compute its bucket in the small table. If that bucket was already split, use the table of double size. When every old bucket is split, the table has doubled, and the pointer starts again at the first bucket.

## The abstract type

Linear hashing implements a [dictionary](/dictionary/): a finite map from keys to values with these operations.

- `new()`: the empty map.
- `search(k)`: the value of $k$, or NIL when $k$ has no value.
- `insert(k, v)`: map $k$ to $v$, and replace the old value if $k$ is present.
- `delete(k)`: remove $k$ and its value; report whether $k$ was present.

The keys need equality and a [hash function](/hash-function/) $h$ to the integers. The order of the keys plays no role.

## Representation

The parameters are fixed at `new`: the initial number of buckets $N \ge 1$, the maximum load factor $\alpha_{\max} > 0$, and the minimum load factor $\alpha_{\min}$ with $0 \le \alpha_{\min} \le \alpha_{\max}/2$. The fields are the level $L$, the split pointer $p$, the number of pairs $n$, and an array $\mathit{bucket}[0 \ldots B-1]$ of lists of pairs $(k, v)$. Each list is a chain as in [separate chaining](/separate-chaining/); on disk it is a page with a chain of overflow pages.

Write $M = N \cdot 2^L$ for the size of the small table, and $\mathrm{addr}(k)$ for the value of ADDRESS below: $h(k) \bmod M$ if this value is at least $p$, else $h(k) \bmod 2M$.

**Invariant.** After each operation:

- (I1) $L \ge 0$, $0 \le p < M$, and $B = M + p$. So $M \le B < 2M$.
- (I2) Each pair $(k, v)$ is in the list $\mathit{bucket}[\mathrm{addr}(k)]$.
- (I3) No key appears in two pairs, and $n$ is the number of pairs.
- (I4) $n \le \alpha_{\max} B$.

By (I1), the buckets $0$ to $p - 1$ and $M$ to $M + p - 1$ are the halves of split buckets, and the buckets $p$ to $M - 1$ are not split yet in the current round. Part (I2) is what makes SEARCH correct, and part (I4) bounds the expected length of a list.

## Operations

```pseudo id=main
ADDRESS(k)                                 ▷ the bucket of key k
L1  a ← h(k) mod (N · 2^L)
L2  if a < p then a ← h(k) mod (N · 2^(L+1))
L3  return a

SEARCH(k)
L4  for each pair (k', v) in bucket[ADDRESS(k)] do
L5      if k' = k then return v
L6  return NIL

INSERT(k, v)
L7  a ← ADDRESS(k)
L8  if bucket[a] has a pair (k, v') then replace it by (k, v) and return
L9  append (k, v) to bucket[a]; n ← n + 1
L10 while n > α_max · (N · 2^L + p) do SPLIT()

SPLIT()                                    ▷ split bucket p
L11 append an empty bucket; its index is p + N · 2^L
L12 old ← bucket[p]; bucket[p] ← an empty list
L13 for each pair (k, v) in old do
L14     append (k, v) to bucket[h(k) mod (N · 2^(L+1))]
L15 p ← p + 1
L16 if p = N · 2^L then L ← L + 1; p ← 0
```

ADDRESS picks the small table for an unsplit bucket and the large table for a split one. SEARCH scans one list. INSERT adds the pair to its list, and then splits while the load factor $n / B$ is above $\alpha_{\max}$. SPLIT takes the bucket at the pointer, not the bucket that got the new key. Each key $k$ of bucket $p$ has $h(k) \bmod M = p$, so $h(k) \bmod 2M$ is either $p$ or $p + M$, and line L14 sends it to one of the two halves. When the pointer reaches $M$ at line L16, all $M$ old buckets are split, the table has $2M$ buckets, and a new round starts with the level one higher.

The split rule depends only on $n$ and $B$, not on the hash values. Litwin calls this a controlled split; his first rule, an uncontrolled split, splits bucket $p$ each time an insertion overflows a page.

```pseudo id=delete
DELETE(k)
D1  a ← ADDRESS(k)
D2  if bucket[a] has no pair with key k then return false
D3  remove that pair from bucket[a]; n ← n − 1
D4  while N · 2^L + p > N and n < α_min · (N · 2^L + p) do MERGE()
D5  return true

MERGE()                                    ▷ undo the last split
M1  if p = 0 then L ← L − 1; p ← N · 2^L
M2  p ← p − 1
M3  append all pairs of bucket[p + N · 2^L] to bucket[p]
M4  remove the last bucket
```

MERGE is the exact inverse of SPLIT. If $p = 0$, the last round is undone first: the level drops and the pointer moves to the end of that round. Then the last bucket, which has index $p + M$, joins its partner $p$. The test $B > N$ in line D4 keeps the table at its initial size or more, and it also keeps $L \ge 0$ in line M1.

**Cost.** ADDRESS takes $O(1)$ time. SEARCH, and lines L7 to L9 and D1 to D3, take time proportional to the length of one list. SPLIT and MERGE take time proportional to the length of the lists they move, plus $O(1)$ amortized for the array of buckets.

## Example

Take $N = 2$, $\alpha_{\max} = 1$, $\alpha_{\min} = 1/2$, and $h(k) = k$ for small integer keys. Each row shows the state after the operation.

| operation | $L$ | $p$ | buckets $0, 1, 2, \ldots$ |
|---|---|---|---|
| new | 0 | 0 | [] [] |
| insert 5 | 0 | 0 | [] [5] |
| insert 12 | 0 | 0 | [12] [5] |
| insert 7 | 0 | 1 | [12] [5 7] [] |
| insert 20 | 1 | 0 | [12 20] [5] [] [7] |
| insert 3 | 1 | 1 | [] [5] [] [3 7] [12 20] |
| insert 18 | 1 | 2 | [] [] [18] [3 7] [12 20] [5] |
| insert 9 | 1 | 3 | [] [9] [18] [3 7] [12 20] [5] [] |
| delete 12 | 1 | 3 | [] [9] [18] [3 7] [20] [5] [] |
| delete 20 | 1 | 3 | [] [9] [18] [3 7] [] [5] [] |
| delete 9 | 1 | 3 | [] [] [18] [3 7] [] [5] [] |
| delete 5 | 1 | 2 | [] [] [18] [3 7] [] [] |

After insert 7, $n = 3 > 1 \cdot 2$, so bucket 0 splits: 12 stays, because $12 \bmod 4 = 0$, and bucket 2 is new. After insert 20, which goes to bucket $20 \bmod 2 = 0$, bucket 1 splits: $5 \bmod 4 = 1$ and $7 \bmod 4 = 3$. Now $p = 2 = M$, so the round ends with $L = 1$ and $p = 0$. Insert 3 puts 3 into bucket $3 \bmod 4 = 3$, which already holds 7, but the split goes to bucket 0, the one at the pointer: both 12 and 20 are $4 \bmod 8$, so they move to the new bucket 4 and bucket 0 becomes empty. A search for 20 now computes $20 \bmod 4 = 0 < p = 1$, then $20 \bmod 8 = 4$. The deletions of 12, 20 and 9 leave $n = 4 \ge \frac{1}{2} \cdot 7$, so no merge happens. The deletion of 5 gives $n = 3 < 3.5$, so MERGE moves $p$ from 3 to 2 and joins bucket $2 + 4 = 6$ into bucket 2. Then $n = 3 \ge \frac{1}{2} \cdot 6$, and the loop stops.

## Correctness

The invariant (I1) to (I4) holds for the empty table and each operation keeps it. The key step is that SPLIT changes the address of exactly the keys of bucket $p$: before line L15 these keys have $\mathrm{addr}(k) = h(k) \bmod M = p$, and after it, since now $p_{\text{old}} < p$, they have $\mathrm{addr}(k) = h(k) \bmod 2M$, the bucket that line L14 chose. All other keys keep their address, and line L16 changes nothing about addresses, because with $p = M$ every value $h(k) \bmod M$ is less than $p$ and ADDRESS already used $h(k) \bmod 2M$. MERGE is the inverse. With (I2), SEARCH looks in the only list that can hold $k$. Part (I4) holds after INSERT by the loop of line L10, and after DELETE because $\alpha_{\min} \le \alpha_{\max} / 2$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The bounds below assume that the values $h(k)$ of the stored keys and of the query are independent and uniform modulo $2M$, a form of the [uniform hashing assumption](/uniform-hashing-assumption/), and that the sequence of operations does not depend on the hash values. The proof is in [the complexity proof](proofs/complexity.md).

| operation | time | notes |
|---|---|---|
| new | $\Theta(N)$ | |
| search | $O(1 + \alpha_{\max})$ expected | at most $1 + 2\alpha_{\max}$ expected pairs in the list, since an unsplit bucket gets a fraction $1/M \le 2/B$ of the keys |
| insert | $O(1 + \alpha_{\max} + 1/\alpha_{\max})$ expected amortized | at most $\lceil 1/\alpha_{\max} \rceil$ splits per insertion, each with expected cost $O(1 + \alpha_{\max})$ |
| delete | $O(1 + \alpha_{\max} + 1/\alpha_{\max})$ expected amortized | each merge undoes an earlier split, so the merges are paid by the insertions |
| any operation, worst case | $O(n + B)$ | all keys in one list, or many merges after many deletions |
| space | $\Theta(B + n)$ words | when $\alpha_{\min} > 0$, $B \le \max(N, n/\alpha_{\min} + 1)$, so the space is $O(N + n / \alpha_{\min})$ |

The expected length of a list is not the same for all buckets: an unsplit bucket gets about twice as many keys as a split one. This unevenness is the price of the linear order of splits.

## Variants

- **Uncontrolled splits.** Split bucket $p$ each time an insertion overflows a page on disk, as in Litwin's first rule. This needs no count of the keys, but it gives a lower use of the pages than splits controlled by the load factor.
- **Partial expansions.** Larson's variant doubles the table in several partial steps, each of which spreads the keys of two or more buckets over one more bucket, so that the loads of the buckets are more even.
- **Main-memory tables.** Larson (1988) keeps the buckets in a directory of fixed-size segments, so that growth never copies the bucket array. The array of buckets in this page, which grows like a [dynamic array](/dynamic-array/), is the simplest form.
- **[Extendible hashing](/extendible-hashing/).** It splits the bucket that overflows, not the bucket at a pointer, and it needs a directory of $2^d$ pointers that doubles from time to time.
- **Open addressing in the buckets.** Each bucket can be a small array with [linear probing](/linear-probing/) in place of a chain.

## When to use it

Use linear hashing when a hash table must grow without long pauses, for example in a file on disk, in a database index, or in a server with a bound on the latency of each request. It needs only two integers beyond the buckets, it never moves more than one bucket in one step, and it keeps the load factor between two limits that you choose. When an occasional pause is acceptable, a plain table that doubles by [rehashing](/rehashing/) is simpler, and its lists are more even. When the keys need an order, use a [B-tree](/b-tree/) instead.

## Pitfalls

- **Splitting the full bucket.** Line L12 splits bucket $p$, not the bucket that got the new key. If the code splits the overflowing bucket instead, the address rule of lines L1 and L2 no longer finds the keys.
- **The comparison in line L2.** The test is $a < p$: bucket $p$ itself is not split yet. With $a \le p$, keys of bucket $p$ are looked for in bucket $p + M$, which does not exist yet.
- **Negative hash values.** In C or Java, the remainder of a negative $h(k)$ is negative, and line L1 gives a negative index. Use an unsigned hash value, or reduce with a mathematical modulus.
- **The end of a round.** Forgetting line L16 lets $p$ run past $M$. Then line L11 makes buckets with indices that the address rule never computes, and keys get lost.
- **Merge without undoing the round.** In MERGE, when $p = 0$, line M1 must lower $L$ before line M2. Otherwise $p$ becomes $-1$.
- **Limits too close.** With $\alpha_{\min} > \alpha_{\max} / 2$, a merge can make the load factor exceed $\alpha_{\max}$, and a mix of insertions and deletions near the limit splits and merges the same bucket again and again.

## Implementations

## History

Witold Litwin introduced linear hashing at the VLDB conference of 1980, for files and tables that grow and shrink without a periodic reorganization. In the same proceedings, Per-Ake Larson described linear hashing with partial expansions. Larson's paper "Dynamic Hash Tables" of 1988 adapted the method to tables in main memory.

## References
