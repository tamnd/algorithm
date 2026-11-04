---
tag: SJRBA7
kind: data-structure
slug: trie
name: Trie
aliases:
- prefix tree
- digital tree
- retrieval tree
area: data-structures/string-structures
level: intro
summary: Rooted tree in which each edge is labelled by a symbol and each root-to-node path spells a string.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {n: the number of keys, m: the length of the query key, N: the total length of the keys, R: the alphabet size}
  time: {worst: Θ(m)}
  space: {extra: O(R N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [asymptotic-notation, alphabet, dictionary]
see_also: [prefix-matching, longest-prefix-match, radix-tree, ternary-search-tree, double-array-trie, suffix-trie, aho-corasick, hash-table]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.2 (Tries), the R-way trie TrieST, the propositions on its cost and space, and the StringST API
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.3 (Digital searching), Algorithm T (trie search) and the history at the end of the section
  - paper: doi:10.1145/367390.367400
    title: Edward Fredkin, Trie memory, Communications of the ACM 3(9), 1960
    locator: pages 490 to 499
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 12, Problem 12-2 (Radix trees), a binary trie used to sort bit strings
---

A trie is a rooted tree that stores a set of strings: each edge carries one symbol of an [alphabet](/alphabet/), the edges out of a node carry distinct symbols, and a key is stored at the node that the path from the root spells. It implements the [string symbol table](/string-symbol-table/), a [dictionary](/dictionary/) with string keys. A search for a key of length $m$ follows at most $m$ edges, whatever the number of keys, and the same walk answers [prefix matching](/prefix-matching/) and [longest prefix](/longest-prefix-match/) queries that a hash table cannot answer. The cost is space: with an array of $R$ links in each node, a trie can use up to $R$ links for each symbol of the keys.

## In plain words

Look up "shore" in a paper dictionary. You open the part for "s", then the part for "sh" inside it, then "sho", and so on. Each letter takes you into a smaller part of the book.

A trie stores the words in the same way. The top node is the empty word. From each node there is at most one branch for each letter. To find a word, start at the top and follow the branch for each letter in turn. If a branch is missing, the word is not there. If you reach the end of the word, you check whether that node marks the end of a stored word. Words with the same beginning share the same first nodes, so "she", "shells" and "shore" share the nodes for "s" and "sh". The time of a search depends only on the length of the word you look for.

## The abstract type

A trie implements the [string symbol table](/string-symbol-table/): a finite map from strings over an alphabet $\Sigma$ of size $R$ to values, with `put(T, s, v)`, `get(T, s)`, `delete(T, s)` and `size(T)`. Because the tree follows the symbols of the keys, it also answers the string queries of that type: `keys_with_prefix(T, p)` ([prefix matching](/prefix-matching/)), `longest_prefix_of(T, s)` (the [longest prefix match](/longest-prefix-match/)), `keys_that_match(T, q)` with a wildcard ([wildcard matching](/wildcard-matching-in-trie/)), and a walk of all keys in lexicographic order.

## Representation

Each node $x$ has a field $x.val$, which is a value or NIL, and a map $x.next$ from symbols to child nodes. The two common maps are an array of $R$ links indexed by the symbol (the R-way trie of Sedgewick and Wayne), and a hash map or sorted list of the children that exist. The trie $T$ has a root node $T.root$ and a count $T.n$.

For a node $x$, let $str(x)$ be the string of symbols on the path from the root to $x$. So $str(T.root) = \varepsilon$, the empty string.

**Invariant.**

- **(T1) Keys.** A string $s$ is a key with value $v$ if and only if there is a node $x$ with $str(x) = s$ and $x.val = v \ne$ NIL.
- **(T2) No dead branch.** Each node other than the root has a value, or has at least one child.
- **(T3) Count.** $T.n$ is the number of nodes with a value.

By (T1) and because the edges out of a node carry distinct symbols, each string is $str(x)$ for at most one node $x$. By (T2), each node is on the path of some key. So the nodes other than the root are in one-to-one correspondence with the distinct nonempty prefixes of the keys, and a trie of keys of total length $N$ has at most $N + 1$ nodes. The shape of the trie depends only on the set of keys, not on the order of the inserts.

## Operations

The main block uses the array or map $x.next$ as a function: $x.next[c]$ is NIL when $x$ has no child for $c$. The string $s$ has symbols $s[0], \ldots, s[m-1]$.

```pseudo id=main
TRIE-GET(T, s)
L1  x ← T.root
L2  for i ← 0 to |s| − 1 do
L3      x ← x.next[s[i]]
L4      if x = NIL then return NIL
L5  return x.val

TRIE-PUT(T, s, v)                       ▷ v ≠ NIL
L6  x ← T.root
L7  for i ← 0 to |s| − 1 do
L8      if x.next[s[i]] = NIL then x.next[s[i]] ← a new node with no value and no children
L9      x ← x.next[s[i]]
L10 if x.val = NIL then T.n ← T.n + 1
L11 x.val ← v

TRIE-DELETE(T, s)
L12 path ← [T.root]; x ← T.root
L13 for i ← 0 to |s| − 1 do
L14     x ← x.next[s[i]]
L15     if x = NIL then return             ▷ s is not a key
L16     append x to path
L17 if x.val = NIL then return
L18 x.val ← NIL; T.n ← T.n − 1
L19 for i ← |s| down to 1 do              ▷ path[i] is the node of s[0 .. i − 1]
L20     if path[i].val ≠ NIL or path[i] has a child then return
L21     remove the link path[i − 1].next[s[i − 1]]

KEYS-WITH-PREFIX(T, p)
L22 x ← the node reached from T.root by the symbols of p, or NIL
L23 if x = NIL then return the empty list
L24 out ← empty list; stack ← [(x, p)]
L25 while stack is not empty do
L26     (y, t) ← pop(stack)
L27     if y.val ≠ NIL then append t to out
L28     for each symbol c of y.next, in decreasing order do push (y.next[c], t·c)
L29 return out

LONGEST-PREFIX-OF(T, s)
L30 x ← T.root; best ← −1
L31 for i ← 0 to |s| do
L32     if x.val ≠ NIL then best ← i
L33     if i = |s| then break
L34     x ← x.next[s[i]]
L35     if x = NIL then break
L36 if best < 0 then return NIL else return s[0 .. best − 1]
```

**Get.** Lines L1 to L5 follow the edge for each symbol. The walk stops at a missing edge (a miss) or at the node $x$ with $str(x) = s$, whose value is the answer. A node without a value is a miss too: "she" can be a node only because "shells" is a key.

**Put.** Lines L6 to L9 walk the same path and create each missing node on the way. Line L10 counts a new key, and line L11 sets or replaces the value.

**Delete.** Lines L12 to L16 record the path. Line L18 removes the value. Then lines L19 to L21 go back up and cut each node that now has no value and no child, so (T2) holds again. The loop stops at the first node that is still needed.

**Prefix and ordered walk.** KEYS-WITH-PREFIX goes down to the node of $p$ and then lists its subtree in preorder. Pushing the children in decreasing order makes them pop in increasing order, so the output is in lexicographic order. With $p = \varepsilon$ it lists all keys in order. The [prefix matching](/prefix-matching/) page gives the cost analysis and the other methods.

**Longest prefix.** LONGEST-PREFIX-OF walks down $s$ and remembers the last depth $i$ where a node has a value. This is the query that IP routing does on address bits.

## Example

Put the keys of Sedgewick and Wayne, "she sells sea shells by the sea shore", with the values 0 to 7 in this order. The key "sea" comes twice, so its value 2 is replaced by 6. The trie has 7 keys and 20 nodes: the root and one node for each of the 19 distinct nonempty prefixes. A value is shown after the symbol of its node.

```
(root)
├── b
│   └── y 4
├── s
│   ├── e
│   │   ├── a 6
│   │   └── l
│   │       └── l
│   │           └── s 1
│   └── h
│       ├── e 0
│       │   └── l
│       │       └── l
│       │           └── s 3
│       └── o
│           └── r
│               └── e 7
└── t
    └── h
        └── e 5
```

| operation | path walked | result |
|---|---|---|
| get("shells") | s, h, e, l, l, s | 3 |
| get("shell") | s, h, e, l, l | NIL: the node exists but has no value |
| get("shy") | s, h, then no edge y | NIL |
| keys_with_prefix("sh") | s, h, then the subtree | she, shells, shore |
| keys_with_prefix("") | the whole tree | by, sea, sells, she, shells, shore, the |
| longest_prefix_of("shellsort") | s, h, e, l, l, s, then no edge o | shells |
| longest_prefix_of("shelter") | s, h, e, l, then no edge t | she |
| delete("shells") | s, h, e, l, l, s | the nodes s, l, l under "she" are cut; 17 nodes remain |

## Correctness

Each operation keeps (T1) to (T3) and returns the answer that the string symbol table defines. The key facts: a walk by the symbols of $s$ reaches the node $x$ with $str(x) = s$ if such a node exists, because each node has at most one child for each symbol; PUT changes the value of exactly one node and adds only nodes on the path of $s$, which then has a value at its end; DELETE cuts a node only when it has no value and no child, so it cuts no other key, and it cuts from the bottom up, so each remaining node still has a key below it. The preorder walk lists the keys of the subtree of the node of $p$, which by (T1) are exactly the keys that start with $p$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/), where a symbol fits in a word. Let $m = |s|$, and let $d$ be the length of the longest prefix of $s$ that is a path of the trie.

| operation | array of $R$ links | hash map of children | sorted array or BST of children |
|---|---|---|---|
| get, search miss | $\Theta(d + 1)$ worst | $\Theta(d + 1)$ expected | $O((d + 1) \log R)$ worst |
| put | $\Theta(m)$ worst, plus $\Theta(R)$ for each new node | $\Theta(m)$ expected | $O(m \log R)$ worst, plus the shift of a sorted array |
| delete | $\Theta(m)$ worst, plus $\Theta(R)$ to test "has a child" with no counter | $\Theta(m)$ expected | $O(m \log R)$ |
| keys with prefix $p$, $k$ keys found in a subtree of $t$ nodes | $\Theta(\lvert p \rvert + tR)$ | $\Theta(\lvert p \rvert + t)$ expected | $\Theta(\lvert p \rvert + t)$ |
| longest prefix of $s$ | $\Theta(d + 1)$ | $\Theta(d + 1)$ expected | $O((d + 1) \log R)$ |
| space | $\Theta(R)$ words for each node | $\Theta(1)$ expected words for each edge | $\Theta(1)$ words for each edge |

**Search cost does not depend on $n$.** GET does $d + 1 \le m + 1$ steps of $O(1)$ time with arrays. A search hit does exactly $m$ steps. A [balanced BST](/balanced-binary-search-tree/) with string keys needs $O(\log n)$ string comparisons, and each comparison can read up to $m$ symbols.

**Nodes and links.** By the invariant, the number of nodes is $1 + |\{\text{distinct nonempty prefixes of the keys}\}| \le 1 + N$. In the R-way trie each node has $R$ links, so the space is between about $Rn$ links, when the keys share long prefixes, and $R(N + 1)$ links. Sedgewick and Wayne state these bounds in Section 5.2 as about $RN$ to $RNw$ links for $N$ keys of average length $w$, in their notation. With $R = 256$ and many short keys, most links are NIL, which is the reason for the [ternary search tree](/ternary-search-tree/) and the [radix tree](/radix-tree/).

**Random keys.** For a trie of $n$ random keys over an alphabet of size $R$, a search miss looks at about $\log_R n$ nodes on average (Sedgewick and Wayne, Section 5.2). The miss stops when the path leaves the trie, which happens after the first few symbols, and long keys do not slow it down.

**Prefix walk.** The subtree of the node of $p$ has $t$ nodes and holds $k$ keys, and $k \le t$. With map children, the walk does $O(1)$ work for each node, so the output cost is $O(t)$, and $t$ is at most $k$ times the longest key length below $p$. The [radix tree](/radix-tree/) removes nodes with one child and brings the walk down to $O(k)$ nodes.

## Variants

- **Radix tree (Patricia).** The [radix tree](/radix-tree/) merges each chain of nodes with one child into one edge labelled by a string, so it has at most $2n - 1$ nodes. PATRICIA, on bits, is the binary version.
- **Ternary search tree.** A [ternary search tree](/ternary-search-tree/) stores the children of a trie node as a BST, with three links in each node. The [hybrid TST](/hybrid-tst/) uses an $R^2$ table at the root.
- **Compact array layouts.** The [double-array trie](/double-array-trie/) stores all transitions in two integer arrays, and the [LOUDS trie](/louds-trie/) stores the shape in about two bits for each node.
- **Cache-conscious tries.** The [burst trie](/burst-trie/), the [HAT-trie](/hat-trie/) and the [adaptive radix tree](/adaptive-radix-tree/) keep small groups of keys in buckets or choose the node layout by the number of children.
- **Suffix trie.** The trie of all suffixes of a text, the [suffix trie](/suffix-trie/), answers substring queries. Its compact form is the [suffix tree](/suffix-tree/).
- **Persistent trie.** A [persistent trie](/persistent-trie/) copies only the path of each update, so old versions stay readable.
- **Aho-Corasick automaton.** The [Aho-Corasick](/aho-corasick/) automaton is a trie of patterns with failure links, for multiple pattern matching.

## When to use it

Use a trie when the keys are strings and you need prefix queries, longest prefix queries or ordered walks, and when the keys share prefixes, as words of a language do. Use a [hash table](/hash-table/) for plain get and put: it also reads each key one time and uses much less space than an R-way trie. Use a [ternary search tree](/ternary-search-tree/) or a [radix tree](/radix-tree/) when the alphabet is large, for example bytes or Unicode, and the R-way array would waste memory.

## Pitfalls

- **A prefix is not a key.** A walk that ends on a node is not a hit: "shell" reaches a node in the example but is not a key. Line L5 returns the value of the node, which can be NIL.
- **Deleting without pruning.** Setting $x.val$ to NIL and stopping leaves dead branches. Then (T2) fails, the node count is no longer the number of prefixes, and a test "does some key start with $p$?" that checks only for the node of $p$ gives wrong answers. Lines L19 to L21 prune.
- **R links in each node.** An R-way trie with $R = 65536$ for UTF-16 symbols needs 64 thousand links for each node. Use a map of children, a TST, or work on bytes with $R = 256$.
- **Key that is a prefix of another key.** Code that stores keys only at leaves (as some textbook versions do) cannot hold both "she" and "shells". Either keep a value field in each node, as here, or end each key with a terminal symbol that is not in the alphabet.
- **Recursion depth.** A recursive walk uses stack space proportional to the longest key. Keys of millions of symbols, such as DNA reads, overflow the stack in Python. The main block uses a loop and an explicit stack.

## Implementations

The Python class uses a dictionary of children in each node, so it works for any hashable symbols, and it keeps a child count implicitly through the length of the dictionary. All operations are loops with an explicit stack.

## History

Knuth (Section 6.3) credits the idea of searching by the digits or letters of the key to René de la Briandais, who described it in 1959, and the name to Edward Fredkin, who in 1960 took "trie" from the middle of the word "retrieval". Fredkin's paper "Trie memory" of 1960 describes the structure as a memory for storing and retrieving information by its symbols. Donald R. Morrison's PATRICIA of 1968 is the compact binary form.

## References
