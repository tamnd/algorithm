---
tag: HZ5P9K
kind: data-structure
slug: hat-trie
name: HAT-trie
aliases:
- hybrid array-hash trie
area: data-structures/string-structures
level: research
summary: Cache-conscious trie whose leaves are hash-table-backed array buckets.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {m: the length of the key, L: the container limit, N: the total length of the keys}
  time: {worst: O(m L)}
  space: {extra: O(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [burst-trie, hash-table, trie]
see_also: [burst-trie, trie, hash-table, adaptive-radix-tree, string-symbol-table, locality-of-reference, double-array-trie, ternary-search-tree]
sources:
  - paper: Nikolas Askitis and Ranjan Sinha, HAT-trie, a cache-conscious trie-based data structure for strings, Proceedings of the 30th Australasian Computer Science Conference (ACSC 2007), CRPIT 62
    locator: pages 97 to 105, the trie of pointer arrays with array hash tables as containers, pure and hybrid containers, the burst and split of containers, and the experiments against burst tries and hash tables
  - paper: Nikolas Askitis and Justin Zobel, Cache-conscious collision resolution in string hash tables, String Processing and Information Retrieval (SPIRE 2005), LNCS 3772, doi:10.1007/11575832_11
    locator: pages 91 to 102, the array hash table, in which each slot is one contiguous array of length-prefixed strings instead of a linked list
  - paper: Nikolas Askitis and Ranjan Sinha, Engineering scalable, cache and space efficient tries for strings, The VLDB Journal 19(5), 2010, doi:10.1007/s00778-010-0183-9
    locator: pages 633 to 660, the HAT-trie variants, their space use and their performance on large string sets
---

A HAT-trie is a [burst trie](/burst-trie/) whose containers are cache-conscious hash tables. The top of the structure is a [trie](/trie/) of nodes that are arrays of pointers, one per symbol; the leaves are *array hash tables*, in which every slot is a single contiguous array of strings rather than a linked list. A container that grows past a limit $L$ is burst into a trie node or split into two containers. Askitis and Sinha (2007) designed it to combine the speed of a [hash table](/hash-table/) with the prefix structure of a trie: a search reads a few trie nodes and then one slot array, and the keys can still be listed in sorted order by sorting each small container when it is visited.

## In plain words

A trie keeps keys in order but jumps around memory, one node per symbol. A hash table jumps once but loses the order, and a chained hash table jumps again for every link of its chains.

A HAT-trie uses a trie only for the first few symbols of the keys, where it is dense and cheap. Below that, the keys that share a prefix go into a small hash table, and each slot of that table is one block of memory holding its strings one after another. So a search follows a few pointers, hashes the rest of the key, and scans one block. When a small table gets too full, it is replaced by a trie node with new tables below it, or cut into two tables that each cover part of the symbols.

## The abstract type

The HAT-trie implements a [string symbol table](/string-symbol-table/): insert a key with a value, look up a key, and list the keys in sorted order. Prefix queries go through the trie part and then filter the containers below. Deletion is possible but is not part of the original description, and this page does not cover it.

## Representation

- A **trie node** has an array of $R$ pointers, one per symbol, and a value slot for the key that ends at the node. Each pointer leads to a trie node or to a container.
- A **container** is an array hash table with a fixed number of slots; each slot is one array of (string, value) entries, and the container holds at most $L$ entries.
- A **pure** container is the target of exactly one pointer, by symbol $c$, and stores its strings without the symbol $c$.
- A **hybrid** container is the target of a range of consecutive pointers $lo, \ldots, hi - 1$ of one node, and stores its strings with their first symbol, which lies in $[lo, hi)$.

**Invariant.** (H1) The key of a trie node at depth $d$ with string $u$ is $u$ if its value is set. (H2) An entry $t$ in a pure container under the pointer $c$ of the node $u$ stands for the key $u c t$; an entry $t$ in a hybrid container under $u$ stands for $u t$, and $t$ is nonempty with $t[0]$ in its range. (H3) Every container holds at most $L$ entries, each in the slot given by its hash. (H4) Each key is stored once.

## Operations

```pseudo id=main
DESCEND(s)
L1  x ← root;  d ← 0
L2  while d < |s|:
L3      y ← x.child[s[d]];  if y is not a trie node: break;  x ← y;  d ← d + 1
GET(s)
L4  DESCEND(s);  if d = |s|: return x.value;  else return FIND(y, s[d + 1 …] if y is pure else s[d …])
FIND(y, t)
L5  scan the slot array of hash(t) in y for t
PUT(s, v)
L6  DESCEND(s);  if d = |s|: x.value ← v;  return
L7  insert t (as in GET) into the slot array of hash(t) in y, or update it
L8  if y holds more than L entries: BURST(x, y)
BURST(x, y)
L9  if y is pure, under symbol c: replace it by a new trie node z with one hybrid container over all symbols; the empty string goes to z.value and the other strings into the container
L10 if y is hybrid: split its range into two parts with about half of the entries each (if all its strings start with one symbol c, cut out the range [c, c + 1))
L11 a hybrid container whose range is one symbol c becomes pure: remove the first symbol of each string
L12 repeat lines L9 to L11 for every new container that holds more than L entries
```

Line L9 is the burst of a burst trie: one level of the trie is added, and the strings lose one symbol in the next container that becomes pure. Line L10 is new in the HAT-trie: a hybrid container is split like a node of a [B-tree](/b-tree/), without adding a trie node, so that sparse parts of the alphabet share one container.

## Example

Take the limit $L = 3$. The root starts with one hybrid container for all symbols. The keys cab, cat and car fill it. Inserting cart makes 4 entries, all starting with c, and the bursts go down two levels:

| step | container | entries | action |
|---|---|---|---|
| 1 | root, hybrid, all symbols | cab, cat, car, cart | all start with c: cut out c |
| 2 | root, hybrid, c only | the same | becomes pure: ab, at, ar, art |
| 3 | root, pure under c | ab, at, ar, art | burst: new node c, entries into its hybrid |
| 4 | node c, hybrid, all symbols | ab, at, ar, art | all start with a: cut out a |
| 5 | node c, hybrid, a only | the same | becomes pure: b, t, r, rt |
| 6 | node c, pure under a | b, t, r, rt | burst: new node ca, entries into its hybrid |
| 7 | node ca, hybrid, all symbols | b, t, r, rt | split by count: b to one part, r, rt, t to the other |

Then dog and do go into the root container for the symbols from d on. Inserting cats puts ts into the container of node ca that holds r, rt and t; it has 4 entries, and the eighth burst splits it at s into r, rt and t, ts. The final structure has the trie nodes root, c and ca, and the keys are read back in order as cab, car, cart, cat, cats, do, dog by sorting each container when the traversal reaches it.

## Correctness

DESCEND consumes one symbol for each trie node, and by (H2) the container reached holds the key under exactly one string, which GET hashes and finds by (H3). Each step of BURST moves entries between containers or into a node value while keeping the key each entry stands for, so (H2) and (H4) hold, and the work list ends because each burst of a pure container shortens the stored strings. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

A lookup visits at most $m$ trie nodes, hashes the rest of the key, and scans one slot array, whose entries are compared in $O(m)$ time each; with at most $L$ entries in the container, the worst case is $O(m L)$. With a good hash function and enough slots, the expected slot length is a constant, and the lookup takes $O(m)$ expected time.

An insertion that causes no burst costs the same. A burst moves and rehashes the at most $L + 1$ entries of each container it processes, and one insertion can process several containers in a cascade, as in the example. The space is $O(N)$ for the stored strings, plus $R$ pointers per trie node.

## Variants

- **Burst trie.** The original structure of Heinz, Zobel and Williams, with linked lists or trees as containers and only pure containers; see the [burst trie](/burst-trie/).
- **Pure-only HAT-trie.** Askitis and Sinha describe a version with only pure containers, which is simpler but uses more trie nodes and more small containers.
- **Array hash table alone.** Without the trie part, the containers are the array hash table of Askitis and Zobel (2005), a fast unordered string set.
- **Slot layout.** In the original, each slot is an array of length-prefixed strings stored inline, which avoids one pointer per string; the Python version keeps a list of pairs, which has the same logic but not the memory layout.

## When to use it

Use a HAT-trie for a large in-memory set of strings, such as a vocabulary or a set of URLs, when lookups should be as fast as in a hash table and sorted or prefix iteration is still needed sometimes. If order is never needed, an array hash table alone is simpler. If the keys share long prefixes or need range scans often, a [radix tree](/radix-tree/) or an [adaptive radix tree](/adaptive-radix-tree/) keeps order at all times.

## Pitfalls

- **Sorted output is not free.** Each container must be sorted when it is listed, which costs $O(L \log L)$ comparisons per container visited.
- **The first symbol in hybrid containers.** A hybrid container stores the first symbol of each string and a pure one does not; mixing them up loses or duplicates keys when a container changes kind.
- **Repeated bursts.** Many keys with a long common prefix make a burst cascade through several levels in one insertion, as in the example; process them with a work list rather than recursion.
- **Splitting by count.** A split point chosen only by symbol range can leave all entries on one side; split by entry counts, and cut out a single symbol when only one occurs.

## Implementations

The Python class keeps trie nodes as pointer arrays over the symbols with codes below $R$, and containers as lists of slot lists with a shift-add-xor hash. PUT follows the pseudocode, and BURST runs on a work list with the three cases of lines L9 to L11. Sorted listing walks the trie and sorts each container. check_invariant verifies (H2) to (H4) and that hybrid containers own their pointer ranges. The tests replay the example, insert a chain of keys a, aa, aaa, and so on that makes deep bursts, and compare 500 random runs with a dictionary.

## History

Heinz, Zobel and Williams (2002) introduced burst tries. Askitis and Zobel (2005) proposed array hash tables, with each slot stored as one contiguous array. Askitis and Sinha (2007) combined the two in the HAT-trie, added hybrid containers that split without a new trie node, and reported speeds close to those of the array hash table while keeping the keys in trie order; they extended the study in 2010.

## References
