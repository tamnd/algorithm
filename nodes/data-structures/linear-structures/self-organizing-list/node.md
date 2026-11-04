---
tag: 2WXV0M
kind: data-structure
slug: self-organizing-list
name: Self-organizing list
aliases:
- self-adjusting list
area: data-structures/linear-structures
level: advanced
summary: List that reorders its elements on access to reduce expected search cost.
implements: [dictionary]
prereqs: [singly-linked-list, move-to-front-heuristic]
see_also: [sequential-search-symbol-table, list-update-problem, list-access-problem, frequency-count, competitive-ratio, splay-tree, lru-cache, move-to-front-transform]
sources:
  - paper: doi:10.1145/5505.5507
    title: James H. Hester and Daniel S. Hirschberg, Self-organizing linear search, ACM Computing Surveys 17(3), 1985
    locator: pp. 295 to 311
  - paper: doi:10.1145/359997.360000
    title: Ronald L. Rivest, On self-organizing sequential search heuristics, Communications of the ACM 19(2), 1976
    locator: pp. 63 to 67
  - paper: doi:10.1145/2786.2793
    title: Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2), 1985
    locator: pp. 202 to 208
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1 (Sequential searching), the part on self-organizing files
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1, Exercise 3.1.22 (Self-organizing search)
---

A self-organizing list is a [linked list](/singly-linked-list/) of key-value pairs, searched from the front, that changes its order after each successful search by a fixed rule, so that the keys that are asked for often move toward the front. The three classic rules are move to front, transpose, and frequency count. Each search, insertion and deletion takes $\Theta(n)$ time in the worst case on $n$ keys, but on skewed or local request sequences the average cost is much less. With the [move-to-front rule](/move-to-front-heuristic/), the total cost on every sequence is less than twice that of the best possible way to reorder the list.

## In plain words

Think of a pile of folders on a desk that you search from the top. Each time you look for a folder, you count the folders that you lift, until you find the right one. If you put each folder that you use back on the top, the folders that you use often stay near the top, and most searches are short.

A self-organizing list does this with a list of records in a computer. It always searches from the front. After it finds a record, it moves the record forward by a fixed rule: all the way to the front, one place forward, or to the place that its number of uses gives it. It needs no knowledge of which records are popular. It learns this from the searches themselves.

## The abstract type

A self-organizing list implements the [dictionary](/dictionary/) abstract type, also called a symbol table, for keys that can be tested for equality:

- `get(L, k)`: the value of key $k$, or nil if $k$ is not in $L$; on a hit, the list may change its order;
- `put(L, k, v)`: associate value $v$ with key $k$, replacing an old value;
- `delete(L, k)`: remove $k$ and its value, if present;
- `size(L)` and `keys(L)`.

The order of the keys is internal. A user of the type sees only the map from keys to values, which the reordering does not change.

## Representation

The fields are a pointer $L.head$ to the first node, a number $L.n$ of nodes, and a rule $L.rule$, one of MTF, TRANSPOSE and COUNT. Each node has the fields $key$, $value$, $next$ and, for the rule COUNT, an integer $count$.

**Invariant.**

- (I1) Following $next$ from $L.head$ reaches nil after exactly $L.n$ nodes, so the list has no cycle.
- (I2) The keys of the nodes are distinct, and the pairs $(key, value)$ of the nodes are exactly the pairs of the map.
- (I3) For the rule COUNT: the $count$ fields do not increase from the front to the back, and the count of a node is 1 plus the number of successful accesses to its key since the key was inserted.

## Operations

The main operation finds the node of a key and moves it by the rule. It unlinks the node, chooses the node $p$ after which to put it back (nil means at the front), and links it there.

```pseudo id=main
ACCESS(L, k)                               ▷ the node of k, moved by the rule, or nil
L1  pp ← nil, prev ← nil, cur ← L.head
L2  while cur ≠ nil and cur.key ≠ k do
L3      pp ← prev, prev ← cur, cur ← cur.next
L4  if cur = nil then return nil
L5  if prev = nil then L.head ← cur.next else prev.next ← cur.next      ▷ unlink cur
L6  if L.rule = MTF then p ← nil                                     ▷ to the front
L7  else if L.rule = TRANSPOSE then p ← pp                           ▷ one place forward
L8  else
L9      cur.count ← cur.count + 1, p ← nil, q ← L.head
L10     while q ≠ nil and q.count ≥ cur.count do p ← q, q ← q.next
L11 if p = nil then cur.next ← L.head, L.head ← cur else cur.next ← p.next, p.next ← cur
L12 return cur
```

Lines L1 to L3 scan the list and keep the two nodes before $cur$: $prev$ just before it and $pp$ before $prev$. Line L5 unlinks $cur$. For MTF, the node goes to the front. For TRANSPOSE, it goes back after $pp$, that is, one place before its old place; when it was first or second, $pp$ is nil and it goes to the front. For COUNT, line L9 adds 1 to its count, and line L10 finds the last node whose count is at least the new count; the node goes after it, so it stays behind the nodes with an equal count. Line L11 links the node after $p$. The cost is $\Theta(i)$ for a key at position $i$, and $\Theta(n)$ for a miss.

The other operations use ACCESS.

```pseudo id=put
GET(L, k)
P1  x ← ACCESS(L, k)
P2  if x = nil then return nil else return x.value
PUT(L, k, v)
P3  x ← ACCESS(L, k)
P4  if x ≠ nil then x.value ← v, return
P5  x ← a new node (k, v, count 1), L.n ← L.n + 1
P6  if L.rule = MTF then x.next ← L.head, L.head ← x
P7  else append x at the end of the list          ▷ count 1 is the least count
```

A new key goes to the front under MTF and to the back under the other two rules, where a count of 1 keeps (I3). PUT costs $\Theta(n)$ for a new key, because the miss in line P3 scans the whole list, and line P7 is a second scan (or uses a tail pointer).

```pseudo id=delete
DELETE(L, k)
D1  prev ← nil, cur ← L.head
D2  while cur ≠ nil and cur.key ≠ k do prev ← cur, cur ← cur.next
D3  if cur = nil then return
D4  if prev = nil then L.head ← cur.next else prev.next ← cur.next
D5  L.n ← L.n − 1
```

DELETE does not reorder the other nodes and costs $\Theta(i)$.

## Example

Start with the keys $a, b, c, d, e$ in this order, each with count 1, and get the keys $d, b, d, e, a, d, b$. The table gives the cost (the position of the key) and the order after the move for each rule.

| get | MTF | TRANSPOSE | COUNT (counts) |
|---|---|---|---|
| $d$ | 4: $d a b c e$ | 4: $a b d c e$ | 4: $d a b c e$ (2 1 1 1 1) |
| $b$ | 3: $b d a c e$ | 2: $b a d c e$ | 3: $d b a c e$ (2 2 1 1 1) |
| $d$ | 2: $d b a c e$ | 3: $b d a c e$ | 1: $d b a c e$ (3 2 1 1 1) |
| $e$ | 5: $e d b a c$ | 5: $b d a e c$ | 5: $d b e a c$ (3 2 2 1 1) |
| $a$ | 4: $a e d b c$ | 3: $b a d e c$ | 4: $d b e a c$ (3 2 2 2 1) |
| $d$ | 3: $d a e b c$ | 3: $b d a e c$ | 1: $d b e a c$ (4 2 2 2 1) |
| $b$ | 4: $b d a e c$ | 1: $b d a e c$ | 2: $d b e a c$ (4 3 2 2 1) |
| total | 25 | 21 | 20 |

The list that never changes costs 22 on these requests. In the COUNT column, the access to $a$ raises its count to 2, and line L10 stops after $e$, the last node with count at least 2, so $a$ stays at position 4.

A different sequence shows the weak point of TRANSPOSE. On $e, d, e, d, \ldots$ with ten requests, TRANSPOSE swaps $e$ and $d$ at the end of the list each time and pays $10 \cdot 5 = 50$, while MTF pays $5 + 5 + 8 \cdot 2 = 26$.

## Correctness

Each operation keeps (I1), (I2) and (I3), and GET returns the value of the map. ACCESS removes one node and puts the same node back, so the set of pairs does not change, and (I1) and (I2) hold. Under COUNT, all nodes before the old place of $cur$ have a count at least the old count, so the new count is at most 1 more than theirs, and line L10 puts $cur$ after the last node with a count at least the new one and before the first node with a smaller count. So the counts stay sorted. PUT either changes one value or adds one new key, which was absent by the miss. DELETE removes the node of $k$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n$ be the number of keys and $i$ the position of the requested key. All bounds are on the [word RAM](/word-ram/).

| operation | worst case | notes |
|---|---|---|
| get, hit at position $i$ | $\Theta(i)$ | at most $\Theta(n)$ |
| get, miss | $\Theta(n)$ | the whole list |
| put, existing key at position $i$ | $\Theta(i)$ | |
| put, new key | $\Theta(n)$ | the miss scans the list |
| delete | $\Theta(i)$ | no reordering |
| space | $\Theta(n)$ | one node per key, plus one count under COUNT |

The worst case is the same as for a list that never changes. The rules differ in their cost on sequences of requests.

- **MTF on every sequence.** In the model where an access at position $i$ costs $i$, MTF pays less than twice the cost of every algorithm, online or offline, on every sequence of gets, as proved on the [move-to-front page](/move-to-front-heuristic/). No deterministic online rule can do better than $2 - 2/(n + 1)$ times the optimum.
- **TRANSPOSE and COUNT are not competitive.** Sleator and Tarjan showed that their ratio to the optimum is not bounded by any constant. For TRANSPOSE, the example above has this form: requests that alternate between the last two keys cost $n$ each, while MTF pays at most 2 per request after the first two.
- **Independent requests.** If each request is for key $j$ with a fixed probability $p_j$, the best fixed order sorts the keys by decreasing $p_j$ and has expected cost $E_{\mathrm{OPT}} = \sum_j j\, p_j$ for $p_1 \ge p_2 \ge \cdots$. MTF reaches a long-run expected cost of at most $2E_{\mathrm{OPT}} - 1$. Rivest proved that the long-run expected cost of TRANSPOSE is at most that of MTF. By the strong law of large numbers, the count of each key divided by the number of requests tends to $p_j$, so when the $p_j$ are distinct, COUNT ends in the best fixed order with probability 1.

## Variants

- **Move ahead $k$.** Move the found key $k$ places forward, a rule between TRANSPOSE and MTF.
- **Array form.** Store the pairs in an array and shift the earlier pairs right by one place on a move to the front, as in Exercise 3.1.22 of Sedgewick and Wayne. The costs stay $\Theta(i)$, and the scan is faster on real caches.
- **Move to front in a hash table.** Each chain of a hash table with [separate chaining](/separate-chaining/) can be a self-organizing list, so that the frequent keys of a chain come first.
- **Self-adjusting trees.** A [splay tree](/splay-tree/) applies the same idea to a binary search tree: each accessed key goes to the root. It has amortized $O(\log n)$ cost and a static optimality theorem that is the analogue of the bound for MTF.
- **Caches.** An [LRU cache](/lru-cache/) keeps its keys in MTF order and removes the last one when it is full.

## When to use it

Use a self-organizing list for a small dictionary, up to some tens of keys, when a few keys get most of the requests or the requests come in bursts. Examples are the chains of a hash table, a list of recent identifiers in a compiler, and the symbol list of a [move-to-front transform](/move-to-front-transform/). Use MTF when the requests have locality or are not known in advance; use TRANSPOSE or COUNT only when the requests are close to independent with stable probabilities. For more than a few hundred keys, a [hash table](/hash-table/) or a balanced search tree is faster, because a list scan is linear in the worst case.

## Pitfalls

- **Losing the node before the predecessor.** TRANSPOSE needs $pp$. A scan that keeps only $prev$ must swap the contents of $prev$ and $cur$ instead, which breaks any outside reference to a node. Line L3 must shift the three pointers in the order `pp ← prev, prev ← cur, cur ← cur.next`.
- **A self-loop on the first node.** If line L5 is skipped when $prev = nil$, line L11 makes $cur.next = cur$. Always unlink before relinking.
- **Ties under COUNT.** Writing line L10 with $>$ instead of $\ge$ puts the node in front of the nodes with the same count. This still keeps (I3), but it turns COUNT into a rule that moves a key ahead of keys that were used as often, and the costs of the example change.
- **A new key under COUNT at the front.** Putting a new key with count 1 at the front breaks (I3). Add it at the back, or give it a count equal to the first count.
- **Iteration that reorders.** A loop that calls GET on each key while it walks the list follows pointers that the moves change, and it may skip keys or visit one twice. Iterate with `keys(L)`, which does not reorder.

## Implementations

## History

Self-organizing files were studied in the 1960s and 1970s under the model of independent requests: McCabe analyzed move to front in 1965, and Rivest in 1976 compared move to front with transpose and proved that transpose has the lower long-run cost. Hester and Hirschberg surveyed these rules and their analyses in 1985. In the same year Sleator and Tarjan gave the amortized analysis that compares a rule with every other algorithm on every sequence, and showed that move to front is within a factor of 2 while transpose and frequency count are not within any constant factor. Knuth, Section 6.1, describes the early results.

## References
