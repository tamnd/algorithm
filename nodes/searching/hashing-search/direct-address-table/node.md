---
tag: QBRTYG
kind: data-structure
slug: direct-address-table
name: Direct-address table
aliases:
- direct addressing table
area: searching/hashing-search
level: intro
summary: Array indexed directly by key from a small universe, with O(1) operations and no collisions.
implements: [dictionary]
model: word-ram
complexity:
  vars: {u: the number of possible keys 0 to u - 1, n: the number of stored keys}
  time: {worst: Θ(1)}
  space: {extra: Θ(u)}
prereqs: [array, dictionary, word-ram]
see_also: [hash-table, bit-vector, perfect-hashing, counting-sort, static-dictionary-problem, transposition-table, predecessor-problem, hash-function]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.1 (Direct-address tables) and its exercises (the bit vector, and the dictionary on a huge array that is not initialized)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the opening discussion of searching by key transformation
  - paper: doi:10.1145/176454.176484
    title: Preston Briggs and Linda Torczon, An efficient representation for sparse sets, ACM Letters on Programming Languages and Systems 2(1-4) (1993)
    locator: pages 59 to 69 (the two-array set with constant-time clear, add and delete, and the iteration in time proportional to the size)
---

A direct-address table stores a set of keys from the universe $\{0, 1, \ldots, u - 1\}$ in an [array](/array/) of $u$ slots, and keeps the key $k$, with its value, in slot $k$. It implements the [dictionary](/dictionary/) operations search, insert and delete in $\Theta(1)$ time in the worst case, with no [hash function](/hash-function/) and no collisions. The price is $\Theta(u)$ space, whatever the number $n$ of stored keys, so the table fits only small universes. It is the base case of hashing: a [hash table](/hash-table/) maps a large universe to a small array and then works like a direct-address table with collisions.

## In plain words

Think of a hotel with one mailbox for each room number. A letter for room 214 goes straight into box 214, and to check for mail you open box 214. You never search, and two rooms never share a box.

This works because the room numbers are few and known in advance. If the keys were phone numbers, you would need ten billion boxes to hold the mail of a few hundred people. A direct-address table is that row of boxes. It is the fastest dictionary there is, and it wastes space when the possible keys far outnumber the keys you store. Hashing keeps the speed and fixes the waste by first turning each big key into a small box number.

## The abstract type

The table implements the [dictionary](/dictionary/) abstract type on the key universe $U = \{0, 1, \ldots, u - 1\}$. It keeps a finite map $D$ from keys of $U$ to values and supports:

- `search(T, k)`: return $D(k)$, or NIL if $k$ is not a key;
- `insert(T, k, v)`: set $D(k) = v$, replacing the old value if $k$ is a key;
- `delete(T, k)`: remove $k$ and its value, if $k$ is a key;
- `size(T)`: return the number $n$ of keys.

A key outside $U$ is an error. The table also gives the keys in increasing order by a scan of the array in $\Theta(u)$ time, and the bit-vector form answers the [predecessor](/predecessor-problem/) of a key by a backward scan, in $O(u)$ time in the worst case.

## Representation

The fields are an array $A[0 \ldots u - 1]$ and a counter $n$. Each slot holds the value of its key, or the special value NIL when its key is absent. NIL must differ from every value that a user can store. CLRS stores in slot $k$ a pointer to the element with key $k$; the pointer plays the role of the value here.

**Invariant.**

- **(D1) Map.** $D = \{(k, A[k]) : 0 \le k < u, \ A[k] \ne \text{NIL}\}$.
- **(D2) Count.** $n$ is the number of slots $k$ with $A[k] \ne \text{NIL}$.

Distinct keys and the placement of each key hold by construction: key $k$ can only be in slot $k$, and a slot holds one value.

## Operations

```pseudo id=main
DA-SEARCH(T, k)                       ▷ 0 ≤ k < u
L1  return T.A[k]                      ▷ NIL when k is absent

DA-INSERT(T, k, v)                    ▷ v ≠ NIL
L2  if T.A[k] = NIL then T.n ← T.n + 1
L3  T.A[k] ← v

DA-DELETE(T, k)
L4  if T.A[k] ≠ NIL then T.n ← T.n − 1
L5  T.A[k] ← NIL
```

**Search.** Line L1 reads one slot. By (D1) the slot holds $D(k)$ when $k$ is a key and NIL otherwise.

**Insert.** Line L2 adds one to the count only when the slot was empty, so a second insert of the same key replaces the value without changing $n$. Line L3 writes the value.

**Delete.** Line L4 lowers the count only when the slot was full, so a delete of an absent key does nothing. Line L5 clears the slot.

**Initialization.** Creating the table sets all $u$ slots to NIL, which costs $\Theta(u)$ time. This is the one cost that grows with $u$. When the table is created often and used for few keys, the version below removes it.

### The table without initialization

On a machine that can allocate an array without clearing it, the slots of a new array hold arbitrary garbage. The sparse-set representation of Briggs and Torczon, which CLRS sets as an exercise in Section 11.1, uses three arrays of size $u$ that are never cleared: $\mathit{val}$ for the values, $\mathit{idx}$ for positions, and $\mathit{key}$ as a stack of the stored keys, with a top $t$ that is set to 0 at creation. A key $k$ is present exactly when its slot of $\mathit{idx}$ points into the used part of the stack and the stack points back to $k$.

```pseudo id=sparse
VALID(T, k)
L6  i ← T.idx[k]                       ▷ may be garbage
L7  return 0 ≤ i < T.t and T.key[i] = k

SP-SEARCH(T, k)
L8  if VALID(T, k) then return T.val[k] else return NIL

SP-INSERT(T, k, v)
L9  if not VALID(T, k) then
L10     T.idx[k] ← T.t; T.key[T.t] ← k; T.t ← T.t + 1
L11 T.val[k] ← v

SP-DELETE(T, k)
L12 if VALID(T, k) then
L13     i ← T.idx[k]; j ← T.key[T.t − 1]
L14     T.key[i] ← j; T.idx[j] ← i; T.t ← T.t − 1
```

Garbage in $\mathit{idx}[k]$ cannot fool line L7: if it points into $\mathit{key}[0 \ldots t-1]$, that slot was written by line L10 or L14 with some stored key, and the test $\mathit{key}[i] = k$ fails unless $k$ is stored there. Delete moves the top key into the hole, as in a swap-with-last removal. Each operation takes $\Theta(1)$ time, creation takes $\Theta(1)$, clearing the whole set is $t \leftarrow 0$, and the stored keys can be listed from $\mathit{key}[0 \ldots t-1]$ in $\Theta(n)$ time.

## Example

Let $u = 10$, and start from the empty table with $n = 0$. Apply insert$(3, a)$, insert$(7, b)$, insert$(0, c)$, insert$(3, d)$, delete$(7)$ and delete$(5)$.

| step | slots that are not NIL | $n$ | note |
|---|---|---|---|
| insert(3, a) | $A[3] = a$ | 1 | line L2 counts the new key |
| insert(7, b) | $A[3] = a$, $A[7] = b$ | 2 | |
| insert(0, c) | $A[0] = c$, $A[3] = a$, $A[7] = b$ | 3 | |
| insert(3, d) | $A[0] = c$, $A[3] = d$, $A[7] = b$ | 3 | slot 3 was full, so $n$ stays |
| delete(7) | $A[0] = c$, $A[3] = d$ | 2 | |
| delete(5) | $A[0] = c$, $A[3] = d$ | 2 | slot 5 was NIL, nothing changes |

Then search(3) reads slot 3 and returns $d$, and search(7) returns NIL. Each operation touched one slot.

**The sparse version.** Let $u = 8$ and insert the keys 5, 2 and 7. Then $\mathit{key}[0 \ldots 2] = (5, 2, 7)$, $t = 3$, and $\mathit{idx}[5] = 0$, $\mathit{idx}[2] = 1$, $\mathit{idx}[7] = 2$. The other slots of $\mathit{idx}$ hold garbage. Delete 5: line L13 sets $i = 0$ and $j = \mathit{key}[2] = 7$, and line L14 sets $\mathit{key}[0] = 7$, $\mathit{idx}[7] = 0$ and $t = 2$. Now $\mathit{key}[0 \ldots 1] = (7, 2)$. The slot $\mathit{idx}[5]$ still holds 0, but $\mathit{key}[0] = 7 \ne 5$, so VALID(5) is false, as it must be. If $\mathit{idx}[4]$ holds the garbage value 1, VALID(4) reads $\mathit{key}[1] = 2 \ne 4$ and is false too.

## Correctness

The plain table keeps (D1) and (D2) because each operation changes only slot $k$, writes there a value that matches the dictionary operation, and changes $n$ exactly when the slot changes between NIL and not NIL. For the sparse version the invariant is that $\mathit{key}[0 \ldots t-1]$ holds the stored keys without repetition, that $\mathit{idx}[\mathit{key}[i]] = i$ for each $i < t$, and that $\mathit{val}[k]$ is the value of each stored key $k$. Under it, VALID$(k)$ is true exactly for the stored keys, for every content of the slots that were never written. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Each operation of the plain table reads or writes one slot and the counter, so it takes $\Theta(1)$ time in the worst case on the [word RAM](/word-ram/), where a key of $\lceil \lg u \rceil$ bits fits in a word and indexes the array in one step. There is no amortization and no randomness. The sparse version also takes $\Theta(1)$ worst-case time per operation, including creation and clearing.

**Space.** The plain table uses $u$ slots plus the counter, so $\Theta(u)$ words, independent of $n$. The sparse version uses $3u$ words. With values of $b$ bits the plain table needs $u \cdot b$ bits plus a way to mark NIL. For a pure set the [bit vector](/bit-vector/) needs $u$ bits, one per key.

**The trade-off.** Any representation of an arbitrary subset of $U$ needs at least $\lg 2^u = u$ bits in the worst case, since there are $2^u$ subsets. So the bit vector is optimal when $n$ is a constant fraction of $u$. When $n$ is much smaller than $u$, about $\lg \binom{u}{n} \approx n \lg(u/n)$ bits suffice, and a [hash table](/hash-table/) or a [perfect hash function](/perfect-hash-function/) uses $\Theta(n)$ words instead of $\Theta(u)$.

| operation | plain table | sparse version |
|---|---|---|
| create | $\Theta(u)$ | $\Theta(1)$ |
| search, insert, delete | $\Theta(1)$ worst case | $\Theta(1)$ worst case |
| clear all | $\Theta(u)$ | $\Theta(1)$ |
| list the keys | $\Theta(u)$, in order | $\Theta(n)$, in no order |
| space | $\Theta(u)$ words | $3u$ words |

## Variants

- **Bit vector.** For a set without values, slot $k$ is one bit. A word operation tests or sets 64 keys at a time, which also gives fast union and intersection of two sets. See [bit vector](/bit-vector/).
- **Counting array.** Slot $k$ holds the number of copies of $k$, which gives a multiset. [Counting sort](/counting-sort/) uses it to sort keys from a small universe in $\Theta(n + u)$ time.
- **Keys with an offset or a dense code.** Keys from a range $[a, a + u)$ use slot $k - a$. Keys such as characters, days or small enums map to $\{0, \ldots, u-1\}$ by a fixed code, which is a perfect hash function chosen by hand.
- **Sparse set.** The three-array version above. It is common in compilers for sets of registers or of graph nodes that are cleared often.
- **Two-level tables.** A table of pointers indexed by the high bits of the key, whose entries point to tables indexed by the low bits, creates the second-level tables only for the parts of $U$ that hold keys. This is the idea of a [trie](/trie/) on the bits of the key and of a page table.
- **Hashing.** When $u$ is too large, a [hash table](/hash-table/) maps each key to a slot of an array of $\Theta(n)$ slots. For a fixed key set, [perfect hashing](/perfect-hashing/) removes the collisions and keeps the $O(1)$ worst-case search.

## When to use it

Use a direct-address table when the keys are integers from a range of size $u$ that is not much larger than the number of keys, or small enough that $\Theta(u)$ memory costs nothing: characters of a byte alphabet, ports, small node ids, the squares of a board. It is faster than a hash table because it computes no hash, compares no keys and has no collisions, and it gives worst-case bounds that an adversary cannot break. Prefer a hash table when $u$ is large or unbounded, as for strings or 64-bit integers. Prefer a balanced search tree or a structure for the [predecessor problem](/predecessor-problem/) when you need ordered queries on a large universe.

## Pitfalls

- **NIL that is also a value.** If the table uses 0 or None as NIL and a user stores 0 or None, the key is lost. Use a separate presence bit, or a sentinel that no user can create.
- **Keys outside the range.** A key $k \ge u$ or a negative key indexes past the array. In C this overwrites memory; in Python a negative index silently reads from the end. Check the range.
- **Counting duplicates.** If line L2 adds to $n$ without the test, a second insert of the same key counts twice.
- **Hidden initialization cost.** The table looks $O(1)$ per operation, but each creation costs $\Theta(u)$. A loop that creates a fresh table of size $u$ for each of $q$ small queries costs $\Theta(qu)$; clear only the slots that were written, or use the sparse version.
- **Memory of the sparse version.** Reading uninitialized memory is undefined behaviour in C and C++, and some tools flag it. The trick needs memory that the language lets you read before you write.

## Implementations

The Python file has the plain table and the sparse version. Python lists are always initialized, so the sparse version fills its arrays with random garbage at creation, which lets the tests check that VALID does not depend on the content of unwritten slots.

## History

Knuth, in Section 6.4, starts the discussion of hashing from the case where the keys index a table directly, and treats hashing as a way to use the same idea when the keys come from a large set. CLRS Section 11.1 gives the direct-address table as the first dictionary of its chapter on hash tables. The constant-time initialization of a large array was posed as an exercise by Aho, Hopcroft and Ullman in their 1974 book; Briggs and Torczon developed it into the sparse-set representation in 1993 and measured it in a register allocator.

## References
