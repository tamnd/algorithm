---
tag: JCNE9N
kind: technique
slug: separate-chaining
name: Separate chaining
aliases:
- chaining
- open hashing
area: data-structures/hashing
level: intro
summary: Each slot holds a list of all keys that hash to it.
prereqs: [hash-table, hash-function, linked-list, load-factor]
see_also: [open-addressing, linear-probing, universal-hashing, uniform-hashing-assumption, chaining-analysis, coalesced-hashing, rehashing, balls-into-bins]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.2, Hash tables (collision resolution by chaining and its analysis), and Section 11.3 (random and universal hashing)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Hashing (chaining, and the history of hashing at the end of the section)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4, Hash Tables (hashing with separate chaining, SeparateChainingHashST)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 5.2, Balls into bins (the maximum load)
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2) (1979)
    locator: pages 143 to 154
  - paper: "Yossi Azar, Andrei Z. Broder, Anna R. Karlin and Eli Upfal, Balanced allocations, SIAM Journal on Computing 29(1) (1999)"
    locator: the main theorem on the maximum load with d choices
  - url: https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/HashMap.java
    title: OpenJDK source, java.util.HashMap
    locator: the implementation notes and the constants DEFAULT_LOAD_FACTOR, TREEIFY_THRESHOLD and MIN_TREEIFY_CAPACITY
---

Separate chaining is the way of resolving [collisions](/hash-collision/) in a [hash table](/hash-table/) in which slot $j$ of the table holds a [linked list](/linked-list/) (a *chain*) of all stored keys $k$ with $h(k) = j$. To search, insert or delete a key, the table computes its [hash value](/hash-function/) and then works only on that one chain. With $n$ keys in $m$ slots and a hash function that spreads the keys evenly, a chain has $\alpha = n/m$ keys on average, so each operation takes $\Theta(1 + \alpha)$ expected time, where $\alpha$ is the [load factor](/load-factor/). Unlike [open addressing](/open-addressing/), chaining never runs out of room: $\alpha$ can be larger than 1, and deletion is direct.

## In plain words

Think of a wall of numbered mail boxes. Each letter has a name on it, and a fixed rule turns the name into a box number. When two names give the same box, both letters go into that box. To find a letter, you compute its box from the name and look through that box only.

A hash table with chaining works the same way. The table is an array of short lists. A key goes into the list that its hash value selects. If the rule spreads the keys well, each list stays short, so a search looks at only a few keys, however many keys the table holds in total.

## When it applies

- You need a [dictionary](/dictionary-problem/): insert, search and delete by key, with no order on the keys.
- You can compute a hash value for each key, and you can compare two keys for equality.
- The number of keys is not known in advance, or it changes a lot. Chaining degrades smoothly when the table gets full, while open addressing fails when $\alpha$ reaches 1.
- Deletions are frequent. Chaining removes a node from its list, with no [tombstones](/lazy-deletion/).
- The stored items are large or must not move in memory. A node stays at the same address when the table grows, so a pointer to an item stays valid.

## The template

The table has an array $T[0 \ldots m-1]$ of chains, a count $n$ of keys and a hash function $h$ from keys to $\{0, \ldots, m-1\}$. The holes are marked.

```pseudo id=main
CHAINED-INSERT(T, k, v)
L1  j ← h(k)                                   ▷ hole: the hash function
L2  for each node x in T[j] do
L3      if x.key = k then x.value ← v, return      ▷ hole: the policy for an equal key
L4  insert a new node (k, v) at the head of T[j]   ▷ hole: the chain structure
L5  n ← n + 1
L6  if n > α_max · m then REHASH(T, 2m)            ▷ hole: the growth rule

CHAINED-SEARCH(T, k)
L7  for each node x in T[h(k)] do
L8      if x.key = k then return x.value
L9  return NIL

CHAINED-DELETE(T, k)
L10 for each node x in T[h(k)] do
L11     if x.key = k then unlink x from T[h(k)], n ← n − 1, return
```

**The hash function (L1).** The analysis below needs a function that spreads the keys evenly. A fixed function such as the [division method](/division-method/) works on most real inputs. A function drawn at random from a [universal family](/universal-hashing/) gives the expected bounds for every input.

**The policy for an equal key (L3).** A map replaces the value. A multiset skips the loop of lines L2 and L3 and always inserts, which makes an insertion $O(1)$ in the worst case.

**The chain structure (L4).** A singly linked list is the classic choice. Insertion at the head costs $O(1)$. A doubly linked list lets the table delete a node in $O(1)$ time when the caller already holds a pointer to it. A small dynamic array per slot uses less memory and is faster to scan, because its keys are next to each other in memory.

**The growth rule (L6).** Without growth, $\alpha$ grows with $n$, and so does the cost of each operation. [Rehashing](/rehashing/) to a table of twice the size when $\alpha$ passes a bound $\alpha_{\max}$ keeps $\alpha \le \alpha_{\max}$ and costs $O(1)$ amortized time per insertion.

### Cost under random hashing

Assume [simple uniform hashing](/uniform-hashing-assumption/): each key hashes to each slot with probability $1/m$, independently of the other keys. Let $\alpha = n/m$. The cost of an operation is 1 for the hash computation plus the number of keys it compares with.

**Unsuccessful search.** A key $k$ that is not in the table is compared with each key of chain $T[h(k)]$. For each stored key $x$, let $I_x$ be the [indicator](/indicator-random-variable/) of the event $h(x) = h(k)$. Then $\Pr[I_x = 1] = 1/m$. By [linearity of expectation](/linearity-of-expectation/), the expected length of the chain is $\sum_x \mathrm{E}[I_x] = n/m = \alpha$. So the expected cost is $1 + \alpha$.

**Successful search.** Let $x_1, \ldots, x_n$ be the keys in the order of insertion, and let the key that we search be $x_i$ with probability $1/n$ for each $i$. Line L4 puts a new node at the head, so the search for $x_i$ compares with $x_i$ and with each $x_j$, $j > i$, with $h(x_j) = h(x_i)$. The expected number of comparisons is

$$\frac{1}{n} \sum_{i=1}^{n} \Bigl(1 + \sum_{j=i+1}^{n} \frac{1}{m}\Bigr) = 1 + \frac{1}{nm} \sum_{i=1}^{n} (n - i) = 1 + \frac{n-1}{2m} = 1 + \frac{\alpha}{2} - \frac{\alpha}{2n}.$$

So the expected cost is $\Theta(1 + \alpha)$ for both kinds of search, and for a deletion. If $\alpha = O(1)$, each operation takes $O(1)$ expected time. The [chaining analysis](/chaining-analysis/) page states these results as a theorem.

**Worst case.** If all $n$ keys hash to one slot, a search takes $\Theta(n)$ time. Under simple uniform hashing with $n = m$, the longest chain has $\Theta(\log n / \log \log n)$ keys with high probability. This is the maximum load of [balls into bins](/balls-into-bins/).

**Space.** The table uses $m$ head pointers and one node per key, so $\Theta(n + m)$ words. Each node pays for one pointer in addition to the key and the value.

### Example

Insert the keys $12, 44, 13, 88, 23, 94, 11, 39, 20, 16, 5$ into a table with $m = 11$ and $h(k) = k \bmod 11$. Each new key goes to the head of its chain.

| slot | chain (head first) |
|---|---|
| 0 | 11, 88, 44 |
| 1 | 23, 12 |
| 2 | 13 |
| 3 | |
| 4 | |
| 5 | 5, 16 |
| 6 | 39, 94 |
| 7 | |
| 8 | |
| 9 | 20 |
| 10 | |

Here $n = 11$ and $\alpha = 1$. Five slots are empty, and the longest chain has 3 keys. A search for 44 compares with 11, 88 and 44, so 3 comparisons. A search for 33 hashes to slot 0 and fails after 3 comparisons. A search for 7 hashes to the empty slot 7 and fails after 0 comparisons. The successful searches for the 11 keys need 17 comparisons in total, or about $1.55$ on average. The expected value under simple uniform hashing is $1 + 10/22 \approx 1.45$, and the expected number of empty slots is $11 (10/11)^{11} \approx 3.86$.

## Classic examples

Chaining is the oldest collision rule. Knuth's history of hashing, at the end of Section 6.4, credits H. P. Luhn of IBM with the idea of hashing, in an internal memorandum of January 1953 that resolved collisions by chaining.

- **The textbook [hash table](/hash-table/).** CLRS, Knuth and Sedgewick and Wayne all use chaining as the first collision rule. Sedgewick and Wayne's `SeparateChainingHashST` keeps an array of linked lists, one per slot.
- **Java `HashMap`.** Each slot is a linked list, and the table doubles when $\alpha$ passes the default bound $0.75$. Since Java 8, when an insertion meets a chain that already has 8 nodes, the chain becomes a balanced tree if the table has at least 64 slots, and the table grows instead if it is smaller. This bounds the worst case by $O(\log n)$ for keys that can be compared.
- **[Universal hashing](/universal-hashing/).** The first analysis of a randomly chosen hash function is for chaining. It shows that the expected length of a chain is at most $\alpha$ or $1 + \alpha$ for every fixed input.
- **[FKS perfect hashing](/fks-perfect-hashing/).** The first level is chaining with $m = n$. Each chain of $b$ keys is then replaced by a table of $b^2$ slots with no collisions.
- **[Linear hashing](/linear-hashing/) and [extendible hashing](/extendible-hashing/).** These file structures keep a bucket per address and an overflow chain for each bucket that is full.
- **[Hash join](/hash-join/).** The build phase puts the rows of the smaller relation into a chained table keyed by the join attribute. A key can have many rows, so a chain is a natural place for them.

## Variations

- **Sorted chains.** Keep each chain in key order. An unsuccessful search can stop at the first key larger than the target, so it compares with about half of the chain on average. Insertion must then find its place in the chain.
- **Move to front.** After a successful search, move the found node to the head of its chain. This is the [move-to-front heuristic](/move-to-front-heuristic/) applied to each chain, and it helps when a few keys get most of the searches.
- **Chains as trees.** Replace a long chain by a [balanced search tree](/red-black-tree/), as Java does. Then each operation is $O(\log n)$ in the worst case, even for an adversarial input.
- **Coalesced chains.** [Coalesced hashing](/coalesced-hashing/) stores the nodes in the table itself and links them by slot index. It is a mix of chaining and open addressing.
- **Two choices.** Hash each key with two functions, and insert it into the shorter of the two chains. A search looks at both chains. With $n = m$, the longest chain then has $\ln \ln n / \ln 2 + O(1)$ keys with high probability, by the [power of two choices](/power-of-two-choices/).
- **Concurrent tables.** Each chain, or each group of chains, has its own lock. This is [lock striping](/lock-striping/), and it is the base of many [concurrent hash tables](/concurrent-hash-table/).

## Pitfalls

- **No growth rule.** With a fixed $m$, the cost grows linearly with $n$. A table of 1 000 slots that holds 1 000 000 keys has chains of about 1 000 keys.
- **A poor hash function.** With $h(k) = k \bmod m$ and $m = 2^p$, the hash value is the low $p$ bits of the key. Keys that are all multiples of $2^p$, such as aligned addresses, all go into slot 0. Choose $m$ prime for the division method, or mix the bits of the key before the reduction.
- **Deletion from a singly linked list.** To unlink a node, line L11 needs the node before it. Keep a pointer to the previous node during the scan, or use a doubly linked list.
- **Inserting duplicates by mistake.** For a map, line L4 must run only after the scan of lines L2 and L3 finds no equal key. Otherwise the same key is in the chain twice, and a later delete removes only one copy.
- **An adversary that knows the hash function.** If an attacker can choose keys with the same hash value, every request costs $\Theta(n)$ time. This is an [algorithmic complexity attack](/algorithmic-complexity-attack/). Use a hash function with a random seed, or tree chains.
- **Memory per node.** Each node costs one or two pointers and often a separate memory allocation. For small keys, an open-addressing table such as [linear probing](/linear-probing/) is often faster, because a scan of a chain causes one cache miss per node.

## Exercises

1. Insert the keys $5, 28, 19, 15, 20, 33, 12, 17, 10$ into a chained table with $m = 9$ and $h(k) = k \bmod 9$, inserting at the head. Draw the chains, and count the comparisons of a search for each key.
2. Show that with sorted chains, under simple uniform hashing, the expected cost of an unsuccessful search is still $\Theta(1 + \alpha)$.
3. Under simple uniform hashing with $n$ keys and $m$ slots, show that the expected number of empty slots is $m(1 - 1/m)^n$, and that this is about $m e^{-\alpha}$.
4. A chained table inserts at the tail instead of the head. Compute the expected number of comparisons of a successful search under the same assumptions as above.
5. Show that under simple uniform hashing the expected number of pairs of stored keys that share a slot is $n(n-1)/(2m)$. For which $m$ is this at most $n/2$?

## References
