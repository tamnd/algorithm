---
tag: 4A6NMB
kind: data-structure
slug: burst-trie
name: Burst trie
area: data-structures/string-structures
level: advanced
summary: Trie whose leaf containers hold small buckets of strings that split (burst) when they grow.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {m: the length of the key, L: the container limit, n: the number of keys}
  time: {worst: O(m + L log L)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [trie, binary-search-tree]
see_also: [trie, hat-trie, burstsort, hybrid-tst, adaptive-radix-tree, splay-tree, move-to-front, ternary-search-tree]
sources:
  - paper: Steffen Heinz, Justin Zobel and Hugh E. Williams, Burst tries, a fast, efficient data structure for string keys, ACM Transactions on Information Systems 20(2), 2002, doi:10.1145/506309.506312
    locator: pages 192 to 223, the access trie and containers, the burst heuristics (ratio, limit and trend), and the experiments on word and URL collections
  - paper: Nikolas Askitis and Ranjan Sinha, HAT-trie, a cache-conscious trie-based data structure for strings, Proceedings of the 30th Australasian Computer Science Conference (ACSC 2007), CRPIT 62
    locator: pages 97 to 105, the burst trie as the starting point and containers replaced by cache-conscious hash tables
---

A burst trie is a [trie](/trie/) whose top levels are ordinary trie nodes, called *access nodes*, and whose leaves are small *containers*, each holding the keys that share the path to it, stored without that path in a simple structure such as a list or a [binary search tree](/binary-search-tree/). A container that becomes too large *bursts*: it is replaced by a new access node, and its keys are spread over new containers by their next symbol. So the trie grows only where many keys share a prefix, and the many sparse parts at the bottom of a plain trie are replaced by small, dense containers. Heinz, Zobel and Williams (2002) introduced it for vocabularies of text collections, where it was faster than the tree structures they compared it with and much smaller than a trie.

## In plain words

A trie spends one node per letter, even deep down where only one or two words remain, and those nodes waste most of their space. A plain list of words wastes no space but is slow to search when it is long.

The burst trie mixes the two. At the top, it is a trie: you follow the first letters of the word through nodes with a slot per letter. When the path reaches a slot that holds a small bag of words instead of a node, you search the bag. Each bag holds the ends of the words that start with the letters you followed. When a bag gets too full, it bursts: it becomes a trie node, and its words are sorted into new, smaller bags by their next letter.

## The abstract type

The burst trie implements the [string symbol table](/string-symbol-table/): get, put, delete, ordered iteration and prefix queries. With sorted containers it is ordered; with containers that keep the most recent key in front, as in the paper, the order is recovered by sorting each container when needed.

## Representation

- An *access node* $x$ has a slot for each symbol of the alphabet, which is empty or holds a child, and a value field $x.val$ for the key that ends exactly at $x$. A child is either an access node or a container.
- A *container* $c$ holds a set of pairs $(t, v)$, where $t$ is a string, possibly empty. In this page and its code, a container is a sorted array of the strings with their values.
- The *path* of a node or a container is the string of symbols on the slots from the root to it.

**Invariant.**

- **(B1) Keys.** The stored keys are: $path(x)$ for each access node $x$ with $x.val \ne$ NIL, and $path(c) \cdot t$ for each container $c$ and each pair $(t, v)$ in $c$. Each key is stored once, with its value.
- **(B2) Size.** Every container holds between 1 and $L$ pairs, where $L$ is the *limit*.
- **(B3) Order.** Each container is sorted by its strings, with no repeats.

A key that ends at the path of a container is stored there with $t = \varepsilon$. So the empty string can sit in any container, and it is found by a search for $\varepsilon$.

## Operations

```pseudo id=main
BURST-GET(T, s)
L1  x ← T.root; d ← 0; while x is an access node:
L2      if d = |s| then return x.val
L3      x ← the slot of x for s[d]; if x is empty then return NIL; d ← d + 1
L4  look up s[d ..] in the container x
L5  return its value, or NIL if it is not there

BURST-PUT(T, s, v)
L6  walk down as in BURST-GET; if the walk ends at an access node x with d = |s| then x.val ← v; return
L7  if the slot of x for s[d] is empty then put a new empty container c in it
L8  t ← s[d+1 ..]; if t is in c then replace its value by v; return
L9  insert (t, v) into c
L10 if |c| > L then replace c in its slot by BURST(c)

BURST(c)
L11 make a new access node y; for each (t, v) in c: if t = ε then y.val ← v else add (t[1 ..], v) to the container in the slot of y for t[0]
L12 for each container c' in a slot of y with |c'| > L: replace c' by BURST(c'); return y
```

**Search.** The walk follows one slot per symbol while it is in access nodes, which costs $O(1)$ per symbol. When it reaches a container, the rest of the key is searched there: by binary search in a sorted array, by a scan in a list, or by a tree search in a BST.

**Burst.** Line L11 splits the pairs of the container by their first symbol, and removes that symbol, which is now on the path. The pair with the empty string becomes the value of the new access node. If all pairs share the same first symbol, the new container in that slot is as large as the old one, and line L12 bursts it again. Each burst moves at most $L + 1$ pairs, so a burst costs $O(L)$ symbol operations per level, apart from the string copies.

**Burst heuristics.** The rule here, burst when the container has more than $L$ pairs, is the *limit* heuristic. Heinz et al. also study the *ratio* heuristic, which bursts when the fraction of searches that end in the container without hitting its first record is high, and the *trend* heuristic, which keeps a counter per container that goes up on unlucky accesses and down on lucky ones. These need the access counts that a list with [move-to-front](/move-to-front/) provides.

**Delete.** Remove the pair from its container, and free the container when it becomes empty. The access nodes are kept, so the trie does not shrink back; rebuilding is cheap if needed.

## Example

Put "she sells sea shells by the sea shore" with values 0 to 7 and the limit $L = 3$.

- she, sells and sea go to the container in slot "s" of the root, as the strings he, ells and ea, kept in sorted order: ea, ells, he.
- shells makes it 4 pairs, more than 3, so the container bursts. The new access node for "s" gets two containers: in slot "e", the strings a and lls (from sea and sells), and in slot "h", the strings e and ells (from she and shells).
- by and the go to new containers in the slots "b" and "t" of the root, with the strings y and he.
- The second sea finds the pair a in the container of "se" and replaces its value with 6.
- shore adds ore to the container of "sh", which now holds e, ells, ore: 3 pairs, not more than the limit.

The burst trie has 2 access nodes (the root and "s") and 4 containers (b, t, se, sh), against 20 nodes in the plain trie of the same keys. A search for shore takes two slots, s and h, and then a binary search for "ore" among 3 strings.

Putting shy adds y to the container of "sh", which bursts into an access node for "sh" with three containers: in slot "e", the strings ε (she) and lls (shells); in slot "o", the string re; and in slot "y", the string ε.

## Correctness

The invariant (B1) says where each key lives, and the search follows it: the walk through access nodes consumes one symbol per node, so at a container $c$ reached with $d$ symbols consumed, $path(c) = s[0 .. d-1]$, and the key $s$ is stored if and only if $s[d ..]$ is in $c$. A burst moves each pair $(t, v)$ to a place whose path plus string is still $path(c) \cdot t$, so it keeps (B1) and restores (B2). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

With sorted array containers and a limit $L$:

| operation | cost |
|---|---|
| get | $O(m)$ slot steps, then a binary search with $O(\log L)$ string comparisons |
| put without burst | as get, plus an insertion that moves $O(L)$ entries |
| a burst | $O(L)$ pair moves per level, plus copying the shortened strings |
| delete | as put |
| ordered walk | $O(n + \text{number of access nodes} \cdot R)$, plus sorting containers if they are not kept sorted |

Each burst creates one access node and moves at most $L + 1$ pairs per level, so the total work of bursts is bounded by the total length of the keys, times $O(1)$ per symbol, for a sequence of insertions.

**Space.** Each container holds at least one key. With insertions only, each access node other than the root was made by a burst of more than $L$ keys that share its path, and the access nodes at one depth have disjoint sets of keys below them, so there are fewer than $n / L$ of them at each depth. In the worst case, keys with long common prefixes, the access nodes form chains, as in a trie. For typical vocabularies the access trie is small, and most memory is in the containers, which store the keys with no per-symbol overhead.

**Cache behaviour.** The access nodes near the root are used by every search and stay in cache. A container is small and is read in a few cache misses, compared with one miss per symbol in a deep trie.

## Variants

- **Container structures.** Heinz et al. compare linked lists with move-to-front, binary search trees and [splay trees](/splay-tree/) as containers.
- **HAT-trie.** The [HAT-trie](/hat-trie/) of Askitis and Sinha (2007) replaces the containers by cache-conscious hash tables that store the strings in contiguous arrays, which removes the pointer chasing of lists and trees.
- **Burstsort.** [Burstsort](/burstsort/) inserts all strings of an array into a burst trie whose containers are unsorted arrays of pointers, and then sorts each container with a small sort while walking the trie in order. It is a cache-efficient string sort.
- **Hybrid TST.** The [hybrid TST](/hybrid-tst/) is the reverse arrangement: a table at the top and ternary search trees below, with no bursting.

## When to use it

Use a burst trie for large sets of strings in main memory, such as the vocabulary of a text collection built while the text is read, when lookups and insertions dominate and the keys share prefixes unevenly. The skew of real text, where a few words are very frequent, suits containers that move the most recent key to the front. When order is not needed, a [hash table](/hash-table/) is simpler; when it is, the burst trie gives order by sorting small containers instead of keeping a tree over all keys.

## Pitfalls

- **Bursting a container whose keys share the next symbol.** All pairs land in one new container, which is still too large. The burst must repeat, as in line L12, or the limit is not enforced.
- **Keys that end at an access node.** After a burst, the key whose remaining string was empty is stored in the access node, not in a container. Searches must check $x.val$ when the key is used up at an access node.
- **The limit.** A small limit makes many access nodes and approaches a trie, with its space cost. A large limit makes container searches slow. The paper chooses it by experiment.
- **Shortening strings.** Each burst removes the first symbol of every string in the container. Copying the strings each time costs time and memory churn; storing an offset into a shared copy avoids it.

## Implementations

The Python class uses dictionaries for the slots of access nodes and sorted lists with binary search as containers, so the ordered walk needs no sorting. It uses the limit heuristic, bursts with a work list instead of recursion, and frees empty containers on delete. The tests replay the example of this page with $L = 3$, check limits as small as 1, and compare random operations and prefix queries against a dictionary.

## History

Heinz, Zobel and Williams introduced the burst trie in 2002, for building and searching the vocabularies of large text collections, and studied the burst heuristics and container structures by experiment. The idea led to burstsort, by Sinha and Zobel, and to the HAT-trie of Askitis and Sinha (2007).

## References
