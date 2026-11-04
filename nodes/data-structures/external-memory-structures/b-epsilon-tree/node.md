---
tag: NA7JW5
kind: data-structure
slug: b-epsilon-tree
name: B^ε-tree
aliases:
- B-epsilon tree
- fractal tree index
- buffered B-tree
area: data-structures/external-memory-structures
level: advanced
summary: Write-optimized tree that buffers updates in internal nodes and flushes them in batches.
implements: [dictionary, ordered-set]
model: external-memory-model
prereqs: [b-plus-tree, external-memory-model, amortized-cost]
see_also: [buffer-tree, write-optimized-structure, log-structured-merge-tree, b-tree, external-searching, external-memory-priority-queue]
sources:
  - paper: "Gerth Stolting Brodal and Rolf Fagerberg, Lower bounds for external memory dictionaries, Proceedings of the 14th ACM-SIAM Symposium on Discrete Algorithms (SODA 2003)"
    locator: pp. 546 to 554 (the B^ε-tree as the upper bound and the lower bound on the trade-off between updates and queries)
  - paper: "Michael A. Bender, Martin Farach-Colton, William Jannen, Rob Johnson, Bradley C. Kuszmaul, Donald E. Porter, Jun Yuan and Yang Zhan, An introduction to Bε-trees and write-optimization, ;login: The USENIX Magazine 40(5) (2015)"
    locator: pp. 22 to 28 (the structure, the flush rule, the costs of inserts, point and range queries, and upserts)
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 11 (multiway trees, buffer trees and the trade-off for dynamic dictionaries)
---

The B^ε-tree is a [B+ tree](/b-plus-tree/) whose internal nodes give part of their block to a *buffer* of pending updates. A node of $B$ items holds about $B^\varepsilon$ pivots, for a parameter $0 < \varepsilon \le 1$, and the rest of the block holds messages such as "insert $k$" or "delete $k$". An update is put into the root buffer, and when a buffer is full, the largest group of messages that go to one child moves down to that child in one write. So each I/O moves many messages, and an update costs $O\big(\frac{\log_B N}{\varepsilon B^{1-\varepsilon}}\big)$ amortized I/Os, while a search still costs $O\big(\frac{\log_B N}{\varepsilon}\big)$, because it reads the buffers on its path and gets its answer at once. With $\varepsilon = 1/2$, inserts are about $\sqrt{B}$ times cheaper than in a [B-tree](/b-tree/), and searches cost about twice as much. Brodal and Fagerberg proved that this trade-off between updates and queries is the best possible. It is the main [write-optimized structure](/write-optimized-structure/) besides the [LSM tree](/log-structured-merge-tree/), and it is used as the *fractal tree index* in TokuDB and in the file system BetrFS.

## In plain words

A B-tree writes each new key all the way down to its leaf at once, which costs a few disk reads and a write for one small key. A B^ε-tree is lazy. It puts the new key in a box at the top. When the box is full, it looks for the child that gets the most keys from the box and sends that whole bundle down in one trip. Each trip carries many keys, so the cost per key is small.

To find a key, you walk down as usual, but you look into each box on the way. A box higher up holds newer news, so the first note about your key that you meet is the right answer.

## The abstract type

A [dictionary](/dictionary/) on keys with values, which is also an [ordered set](/ordered-set/):

- `put(k, v)` sets the value of $k$ to $v$, inserting $k$ if it is absent.
- `delete(k)` removes $k$ if it is present.
- `get(k)` returns the value of $k$, or "absent".
- `range(a, b)` lists the keys between $a$ and $b$ in order.

Unlike the [buffer tree](/buffer-tree/), queries are answered at once. Many systems add *upserts*, messages such as "add 1 to the value of $k$" that need not read the old value.

## Representation

There are three parameters: the fan-out $F$, which is about $B^\varepsilon$; the buffer capacity $C$, which is about $B - F$; and the leaf capacity $L$, which is about $B$. The code of this page takes $C = L = B$.

- A **leaf** holds at most $L$ keys in order, with their values.
- An **internal node** holds $f \le F$ children, $f - 1$ increasing pivots as in a [B+ tree](/b-plus-tree/), and a buffer of at most $C$ messages. A message is `PUT(v)` or `DEL` on a key. The buffer keeps at most one message per key: a newer message on the same key replaces the older one.
- Each internal node, together with its buffer, fits in $O(1)$ blocks.

**Invariants.**

- **(E1)** The pivots give the search order, all leaves are at one depth, and each internal node has between 2 and $F$ children.
- **(E2)** Each message in the buffer of $x$ is on a key in the range of $x$.
- **(E3)** On each key, the message in the buffer of a node is newer than any message on that key in a buffer or leaf below it.
- **(E4)** No buffer holds more than $C$ messages between operations.

By (E3), the true state of a key is given by the highest message on its root-to-leaf path, or, if there is none, by the leaf.

## Operations

```pseudo id=main
GET(T, k)
L1  x ← T.root
L2  while x is an internal node do
L3      if x.buf has a message on k then return its value, or "absent" if it is DEL
L4      x ← the child of x whose range holds k
L5  return the value of k in the leaf x, or "absent"

UPSERT(T, k, msg)                   ▷ msg is PUT(v) or DEL
L6  if T.root is a leaf then apply msg to it
L7  else put msg on k into T.root.buf, replacing an older message on k; if |T.root.buf| > C then FLUSH(T.root)
L8  while T.root has more than L keys or F children do make a new root above it and SPLIT the old root

FLUSH(x)
L9  while |x.buf| > C do
L10     c ← the child of x that receives the most messages from x.buf
L11     move those messages to c: if c is a leaf, apply them; else put them into c.buf, replacing older ones
L12     if c is internal and |c.buf| > C then FLUSH(c)
L13     if c has more than L keys or F children then SPLIT(c), which adds a pivot and a child to x

SPLIT(c)                            ▷ c is a child of p
L14 cut c into two halves, by its keys if a leaf, by its children if internal, with the buffer split by the middle pivot; put the middle pivot into p; repeat on a half that is still too big
```

**Why a flush moves many messages.** When line L10 runs, the buffer has more than $C$ messages and at most $F$ children receive them, so the largest group has more than $C/F$ messages. Moving them costs $O(1)$ I/Os: read the child and write it back. With $C = \Theta(B)$ and $F = B^\varepsilon$, that is $\Omega(B^{1-\varepsilon})$ messages per I/O.

**Range queries.** Read the leaves in the range, as in a B+ tree, and also the buffers of their ancestors, and apply the messages of the buffers to what the leaves say. This costs $O\big(\frac{\log_B N}{\varepsilon} + \frac{K}{B}\big)$ I/Os for $K$ answers.

**Deletes.** A delete is a message, a *tombstone*, which removes the key when it reaches the leaf. The code of this page lets leaves become small and rebuilds the whole tree after about as many deletes as keys; real systems merge small nodes, as a B-tree does.

## Example

Take $B = 4$, so $C = L = 4$, and $F = 3$. An internal node is written $\langle$pivots | buffer$\rangle$ followed by its children, and $+k$ and $-k$ are a put and a delete of $k$.

1. Put $10, 20, 30, 40$. The root is a leaf $[10\ 20\ 30\ 40]$. Put $50$: the leaf has 5 keys, more than $L$, and splits under a new root: $\langle 30 \mid\ \rangle([10\ 20]\ [30\ 40\ 50])$.
2. Put $60, 70, 80, 90$. They stay in the root buffer: $\langle 30 \mid +60\ +70\ +80\ +90\rangle$.
3. Put $15$. The buffer has 5 messages. Four go to the right child and one to the left, so FLUSH moves $+60, +70, +80, +90$ in one step. The leaf gets 7 keys and splits: $\langle 30\ 60 \mid +15\rangle([10\ 20]\ [30\ 40\ 50]\ [60\ 70\ 80\ 90])$.
4. Put $25, 35, 45$ and delete $20$. The buffer has $+15, +25, +35, +45, -20$. The first child gets 3 of them, the most, so they move: the leaf becomes $[10\ 15\ 25]$, and $+35, +45$ stay in the root.
5. Put $55$, delete $70$: the root buffer is $+35\ +45\ +55\ -70$. Now `get(70)` meets $-70$ in the root and returns "absent", although 70 is still in its leaf, and `get(45)` returns the value in the buffer, with no leaf read.
6. Put $5$. The middle child gets $+35, +45, +55$, the most. Its leaf gets 6 keys and splits into $[30\ 35\ 40]$ and $[45\ 50\ 55]$. The root now has 4 children, more than $F$, so it splits under a new root, and its buffer is split by the pivot 45: $\langle 45 \mid\ \rangle(\langle 30 \mid +5\rangle([10\ 15\ 25]\ [30\ 35\ 40])\ \langle 60 \mid -70\rangle([45\ 50\ 55]\ [60\ 70\ 80\ 90]))$.

## Correctness

A search is right because of (E3): on the path to the leaf of $k$, the first message on $k$ is the newest update of $k$, and if there is none, the leaf holds the result of all updates of $k$. An update is placed at the top, so it is the newest, and replacing an older message on the same key in one buffer is right because for `PUT` and `DEL` only the last one matters. A flush moves a whole group of messages from a node to a child, and every message on those keys below is older, so (E3) still holds; at a leaf, the messages are applied, which gives the leaf the newest state of each key. Splits move keys and messages with their ranges and do not change any path order. The full proof is below.

## Complexity

Let $h$ be the height. Every internal node other than the root has at least about $F/2$ children, so $h = O(\log_F \frac{N}{B}) = O\big(\frac{\log_B N}{\varepsilon}\big)$.

- **Search.** One node per level: $O(h) = O\big(\frac{\log_B N}{\varepsilon}\big)$ I/Os.
- **Update.** A message moves down one level in a flush step that costs $O(1)$ I/Os and moves more than $C/F$ messages. So it pays $O(F/C)$ per level, $O(hF/C)$ in all. Splits add $O(1)$ I/Os per new node, and a new node needs $\Omega(B)$ keys at the leaves or $\Omega(F)$ splits below it, so they cost less. With $C = \Theta(B)$ and $F = B^\varepsilon$, the update cost is $O\big(\frac{\log_B N}{\varepsilon B^{1-\varepsilon}}\big)$ amortized.

| $\varepsilon$ | update, amortized | search |
|---|---|---|
| 1 (a B-tree) | $O(\log_B N)$ | $O(\log_B N)$ |
| 1/2 | $O\big(\frac{\log_B N}{\sqrt{B}}\big)$ | $O(\log_B N)$ |
| $\to 0$, with $F = 2$ | $O\big(\frac{\log_2 N}{B}\big)$ | $O(\log_2 N)$ |

For $B = 1024$ and $\varepsilon = 1/2$, the fan-out is 32, a search reads about twice as many nodes as in a B-tree, and an update costs about $1/16$ of a B-tree update.

**Optimality.** Brodal and Fagerberg proved that for any external dictionary in a comparison model, if updates cost $O\big(\frac{\log_B N}{\varepsilon B^{1-\varepsilon}}\big)$ amortized, searches need $\Omega\big(\frac{\log_B N}{\varepsilon}\big)$, so the B^ε-tree is on the optimal trade-off curve for all $\varepsilon$ between about $1/\log B$ and 1. The B-tree is the end point $\varepsilon = 1$.

## Variants

- **Fractal tree index.** The commercial form used in TokuDB and TokuMX, with large nodes of megabytes, compression and upsert messages.
- **BetrFS.** A file system built on B^ε-trees, which uses upserts for small writes and range messages for deletes of whole directories.
- **Buffered repository tree.** Buchsbaum and others use a tree of this kind with fan-out 2 and buffers of $B$ items for external graph search.
- **Size-tiered buffers.** Some variants keep messages in each buffer as sorted runs, which makes flushes cheaper in CPU time.
- **The buffer tree.** With fan-out $M/B$ and buffers of $M$, one gets the [buffer tree](/buffer-tree/), which has cheaper updates but answers queries only in batches.

## When to use it

Use a B^ε-tree for an index on disk or flash that receives many more small updates than a B-tree can write, and that must still answer point and range queries at once: databases with heavy insert loads, key-value stores, and file system metadata. It reads less than an [LSM tree](/log-structured-merge-tree/) for range queries, because one tree holds everything. For a read-mostly workload, a [B+ tree](/b-plus-tree/) is simpler and searches a little faster.

## Pitfalls

- **Flushing the wrong child.** Moving the messages of an arbitrary child, or of all children, loses the $C/F$ messages per I/O that the bound needs. Pick the child with the most messages.
- **Searching only the leaves.** A search that skips the buffers misses recent updates and deletes.
- **Order of messages.** If two messages on one key can be in one buffer, as with upserts, keep them in time order and apply them in order.
- **Tombstones.** A delete does not free space until it reaches a leaf. Workloads with many deletes need rebalancing or periodic rebuilds.
- **Choosing $\varepsilon$ too small.** With $F = 2$, updates are cheapest but searches read $\log_2 N$ nodes, which is slower than a B-tree for queries.

## Implementations

## History

Brodal and Fagerberg introduced the B^ε-tree at SODA 2003 as the upper bound that matches their lower bound for the trade-off between updates and queries in external dictionaries. Buffered trees of the same kind had appeared earlier, such as the buffered repository tree of Buchsbaum, Goldwasser, Venkatasubramanian and Westbrook (SODA 2000). Bender, Farach-Colton and Kuszmaul developed the structure into the fractal tree index of Tokutek, used in TokuDB. The file system BetrFS of Jannen and others (FAST 2015) applied it to file systems, and the 2015 article of Bender and others in ;login: gives a short introduction.

## References
