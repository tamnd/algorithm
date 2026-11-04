---
tag: 5G5MVH
kind: data-structure
slug: sequential-search-symbol-table
name: Sequential search symbol table
area: data-structures/linear-structures
level: intro
summary: Symbol table stored as an unordered linked list of key-value pairs, searched by scanning from the head.
implements: [dictionary]
prereqs: [singly-linked-list, dictionary, asymptotic-notation]
see_also: [binary-search-symbol-table, ordered-symbol-table, hash-table, separate-chaining, self-organizing-list, linear-search, move-to-front-heuristic]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1 (Symbol Tables), Algorithm 3.1 (SequentialSearchST) and Proposition A
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1 (Sequential searching), Algorithm S
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2 (Linked lists), the procedures LIST-SEARCH and LIST-PREPEND
---

A sequential search symbol table stores a map from keys to values as an unordered [singly linked list](/singly-linked-list/) of key-value pairs. To find a key, it compares the key with each node from the head; to insert a new key, it adds a node at the head. It implements the [dictionary](/dictionary/) abstract type with only an equality test on keys, and each search or insertion makes up to $n$ compares on $n$ keys. It is the simplest symbol table, the baseline for the [binary search symbol table](/binary-search-symbol-table/) and the [hash table](/hash-table/), and the list that each chain of [separate chaining](/separate-chaining/) uses.

## In plain words

Write each word and its meaning on a card, and keep the cards in one stack in no special order. To look up a word, go through the cards from the top, one by one, until you find it or run out of cards. To add a new word, first look for it. If it is already there, change its meaning on the card. If it is not there, put a new card on top.

This needs nothing from the words except that you can tell whether two of them are the same. The price is speed: with a thousand cards, a word that is not there costs a thousand looks.

## The abstract type

The table implements the [dictionary](/dictionary/) type, which Sedgewick and Wayne call a symbol table, for keys that can be tested for equality:

- `get(T, k)`: the value of $k$, or nil when $k$ is not in $T$;
- `put(T, k, v)`: map $k$ to $v$, replacing the old value of $k$;
- `delete(T, k)`: remove $k$ and its value, if present;
- `contains(T, k)`, `size(T)` and `keys(T)`, the keys in some order.

## Representation

The fields are $T.first$, a pointer to the first node or nil, and $T.n$, the number of nodes. Each node has the fields $key$, $value$ and $next$.

**Invariant.**

- (I1) Following $next$ from $T.first$ reaches nil after exactly $T.n$ nodes.
- (I2) The keys of the nodes are distinct.
- (I3) The set of pairs $(key, value)$ of the nodes is the map that the table stores.

The order of the nodes carries no information. With the PUT below it is the reverse of the order in which the keys were first inserted.

## Operations

```pseudo id=main
GET(T, k)
L1  x ← T.first
L2  while x ≠ nil do
L3      if x.key = k then return x.value      ▷ search hit
L4      x ← x.next
L5  return nil                                ▷ search miss

PUT(T, k, v)
L6  x ← T.first
L7  while x ≠ nil do
L8      if x.key = k then x.value ← v, return  ▷ the key is present: update
L9      x ← x.next
L10 T.first ← a new node (k, v, next = T.first), T.n ← T.n + 1
```

GET walks the list from the first node and compares $k$ with the key of each node. It stops at the first node with key $k$, which by (I2) is the only one, or at the end of the list. PUT runs the same search. On a hit it replaces the value in place. On a miss it knows that $k$ is absent, so line L10 puts a new node in front of the old first node in $\Theta(1)$ time. A hit at position $i$ costs $i$ compares; a miss costs $T.n$ compares.

```pseudo id=delete
DELETE(T, k)
D1  prev ← nil, x ← T.first
D2  while x ≠ nil and x.key ≠ k do prev ← x, x ← x.next
D3  if x = nil then return
D4  if prev = nil then T.first ← x.next else prev.next ← x.next
D5  T.n ← T.n − 1
```

DELETE keeps a pointer to the node before $x$, because in a singly linked list the predecessor is the only node that points to $x$. Line D4 makes it skip $x$. The cost is the same as for the search.

## Example

Insert the keys of S E A R C H E X A M P L E, each with its index in this string as the value, into an empty table. The table shows the key compares of each PUT, their running total, and the list after the PUT, from the first node.

| put | compares | total | list |
|---|---|---|---|
| S 0 | 0 | 0 | S0 |
| E 1 | 1 | 1 | E1 S0 |
| A 2 | 2 | 3 | A2 E1 S0 |
| R 3 | 3 | 6 | R3 A2 E1 S0 |
| C 4 | 4 | 10 | C4 R3 A2 E1 S0 |
| H 5 | 5 | 15 | H5 C4 R3 A2 E1 S0 |
| E 6 | 5 | 20 | H5 C4 R3 A2 E6 S0 |
| X 7 | 6 | 26 | X7 H5 C4 R3 A2 E6 S0 |
| A 8 | 5 | 31 | X7 H5 C4 R3 A8 E6 S0 |
| M 9 | 7 | 38 | M9 X7 H5 C4 R3 A8 E6 S0 |
| P 10 | 8 | 46 | P10 M9 X7 H5 C4 R3 A8 E6 S0 |
| L 11 | 9 | 55 | L11 P10 M9 X7 H5 C4 R3 A8 E6 S0 |
| E 12 | 9 | 64 | L11 P10 M9 X7 H5 C4 R3 A8 E12 S0 |

The second E is a hit at position 5, so it costs 5 compares and changes the value in place. The ten distinct keys alone cost $0 + 1 + \cdots + 9 = 45$ compares. After the last PUT, GET(R) costs 7 compares and returns 3, and GET(Z) costs 10 compares and returns nil.

## Correctness

GET returns the value of $k$ when $k$ is in the table and nil otherwise, and PUT and DELETE keep (I1) to (I3) for the new map. The proof is a [loop invariant](/loop-invariant/) for the scan: when line L2 tests $x$, no node before $x$ has key $k$. So a hit returns the only node with key $k$, and a miss proves that $k$ is absent, which is what line L10 needs to keep the keys distinct. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The cost measure is the number of key compares, the model of Sedgewick and Wayne; every other step of a loop round costs $O(1)$ on the [word RAM](/word-ram/), so the time is within a constant factor of the compares plus 1. Let $n = T.n$.

- **Search.** A hit at position $i$ makes $i$ compares, a miss makes $n$. So GET makes at most $n$ compares, and $n$ for each miss.
- **Insert.** PUT of a new key makes $n$ compares and then $\Theta(1)$ work. PUT of a present key at position $i$ makes $i$ compares.
- **Building the table.** Inserting $N$ distinct keys into an empty table makes $0 + 1 + \cdots + (N - 1) = N(N - 1)/2 \sim N^2/2$ compares, because the $j$-th insertion searches a list of $j - 1$ nodes.
- **Average hit.** If each of the $n$ keys is equally likely to be searched, the expected cost of a hit is $\frac{1}{n}\sum_{i=1}^{n} i = (n + 1)/2$ compares.
- **Space.** $\Theta(n)$: one node with two references and a next pointer per key.

| operation | compares, worst case | compares, typical |
|---|---|---|
| get, hit | $n$ | $(n + 1)/2$ for a uniformly random key |
| get, miss | $n$ | $n$ |
| put, new key | $n$ | $n$ |
| put, present key | $n$ | $(n + 1)/2$ |
| delete | $n$ | $(n + 1)/2$ for a present key |
| build from $N$ distinct keys | $N(N - 1)/2$ | |

**A lower bound with equality tests only.** If a structure can learn about keys only by testing two of them for equality, then a search miss among $n$ stored keys needs $n$ compares in the worst case. Suppose a search for $k$ ends with "absent" after it has compared $k$ with fewer than $n$ stored keys. Some stored key $y$ was not compared with $k$. Every test that was made has the same answer if $k$ is replaced by $y$, so the search for $y$ takes the same path and also answers "absent", which is wrong. So the scan is optimal for keys that have no order and no hash function. With an order, a sorted array gives $O(\log n)$ compares for a search; with a hash function, a hash table gives $O(1)$ expected time.

## Variants

- **Ordered symbol table.** With comparable keys, a sorted array and binary search give the [binary search symbol table](/binary-search-symbol-table/), with $O(\log n)$ compares for a search but $\Theta(n)$ moves for an insertion. It implements the [ordered symbol table](/ordered-symbol-table/) operations, such as min and rank.
- **Self-organizing order.** Move each found node to the front, as a [self-organizing list](/self-organizing-list/) does. Under requests with locality, the average cost drops a lot, and with [move to front](/move-to-front-heuristic/) it is never more than twice the best possible.
- **Unordered array.** Store the pairs in a [dynamic array](/dynamic-array/) and scan it. The costs are the same, and the scan is faster on real caches. Delete moves the last pair into the hole.
- **Hash table chains.** A [hash table](/hash-table/) with [separate chaining](/separate-chaining/) keeps $m$ such lists and sends each key to one of them by a hash function, which divides the expected cost by about $m$.
- **A sentinel.** Put $k$ in an extra last node before the scan, so the loop needs only the test $x.key = k$ and not the test $x \ne nil$; Knuth's Algorithm Q in Section 6.1 does this for an array. See [sentinel node](/sentinel-node/).

## When to use it

Use a sequential search symbol table when the table is small (tens of keys), when keys can only be tested for equality, or as the chain of a hash table, where each list has few keys. It is easy to get right and has no overhead. Do not use it for large tables: building a table of a million distinct keys costs about $5 \cdot 10^{11}$ compares. For comparable keys use a balanced search tree; for hashable keys use a hash table.

## Pitfalls

- **Inserting without searching.** Adding the node of line L10 without the search of lines L6 to L9 makes a second node for a present key, which breaks (I2). Later GET calls return the newer value, but DELETE removes only one of the nodes, so the old value comes back.
- **Deleting with one pointer.** A scan that keeps only $x$ cannot unlink $x$ in a singly linked list. Keep $prev$ as in line D2, and handle the first node by line D4.
- **Size out of step.** Increase $T.n$ only on the miss of line L10, not on every PUT, and decrease it only when line D4 removes a node.
- **Equality of the wrong kind.** In Java or Python, testing keys by identity (`==` on references, or `is`) instead of by value makes two equal strings different keys. Use `equals` or `==` on values.
- **Modifying while iterating.** Deleting the current node during a loop over the keys loses the rest of the list if the loop reads $x.next$ after the unlink frees $x$. Save $x.next$ first.

## Implementations

## History

Sequential search is the oldest search method, and Knuth opens Chapter 6 with it as Algorithm S, together with the sentinel version Algorithm Q. Sedgewick and Wayne use the linked-list form, SequentialSearchST, as the first symbol table of their Chapter 3, and they prove in Proposition A that it needs $\sim N^2/2$ compares to insert $N$ distinct keys; this motivates the binary search, tree and hash table versions that follow.

## References
