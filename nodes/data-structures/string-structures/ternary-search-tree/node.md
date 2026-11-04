---
tag: BVWSE3
kind: data-structure
slug: ternary-search-tree
name: Ternary search tree
aliases:
- TST
area: data-structures/string-structures
level: core
summary: Trie node with three children (less, equal, greater) that stores one character per node.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {n: the number of keys, m: the length of the query key, R: the alphabet size, N: the total length of the keys}
  time: {worst: O(m R)}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [trie, binary-search-tree]
see_also: [trie, hybrid-tst, radix-tree, multikey-quicksort, prefix-matching, wildcard-matching-in-trie, string-symbol-table, binary-search-tree]
sources:
  - paper: Jon L. Bentley and Robert Sedgewick, Fast algorithms for sorting and searching strings, Proceedings of the 8th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1997)
    locator: pages 360 to 369, ternary search trees, their relation to multikey quicksort, and the partial-match and near-neighbor searches
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.2 (Tries), the subsection on ternary search tries (class TST), the propositions on their space and search cost, and the table of string symbol table costs
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.3 (Digital searching), the representation of trie nodes as binary trees
---

A ternary search tree (TST) is a [trie](/trie/) in which the children of each trie node are kept in a [binary search tree](/binary-search-tree/) ordered by their symbol: each node holds one symbol and three links, to the nodes with a smaller symbol, to the next symbol of the key (the middle link), and to the nodes with a larger symbol. It implements the [string symbol table](/string-symbol-table/) in space proportional to the total length of the keys, whatever the size of the alphabet. A search reads each symbol of the key once on the middle links and pays extra comparisons only for the left and right steps. Bentley and Sedgewick (1997) showed that it is to [multikey quicksort](/multikey-quicksort/) what a binary search tree is to quicksort.

## In plain words

A trie node with an array of 256 links wastes memory when only two or three letters follow. A ternary search tree keeps only the letters that are used.

Each node holds one letter and three arrows. To search, compare the next letter of your word with the letter in the node. If your letter is smaller, take the left arrow. If it is larger, take the right arrow. If it is equal, this letter is done: take the middle arrow and go on with the next letter of your word. The left and right arrows form a small search tree of the letters that can come at this point. The middle arrows spell out the word.

## The abstract type

A TST implements the [string symbol table](/string-symbol-table/) for nonempty keys: `put`, `get`, `delete`, `keys_with_prefix` ([prefix matching](/prefix-matching/)), `longest_prefix_of`, `keys_that_match` ([wildcard matching](/wildcard-matching-in-trie/)) and the ordered walk. Bentley and Sedgewick also give a near-neighbor search, which lists the keys within a given Hamming distance of a query.

## Representation

Each node $x$ has a symbol $x.c$, a value $x.val$ (or NIL), and three links $x.left$, $x.mid$ and $x.right$. The tree has a root link $T.root$ and a count $T.n$.

The nodes that can be reached from one node by left and right links only form a *sibling tree*: the root and its left and right descendants form the first one, and the middle link of a node leads to the root of the next one. Define the string of a node: if $x$ is in the sibling tree whose entry is the root, $str(x) = x.c$; if $x$ is in the sibling tree that $y.mid$ points to, $str(x) = str(y) \cdot x.c$.

**Invariant.**

- **(S1) BST order.** In each sibling tree, the symbols are distinct and satisfy the [binary search tree property](/binary-search-tree-property/): each symbol in the left subtree of $x$ within the sibling tree is smaller than $x.c$, and each one in the right subtree is larger.
- **(S2) Keys.** A nonempty string $s$ is a key with value $v$ if and only if some node $x$ has $str(x) = s$ and $x.val = v \ne$ NIL.
- **(S3) No dead node.** Each node has a value or a middle child.
- **(S4) Count.** $T.n$ is the number of nodes with a value.

Under (S1), the nodes of one sibling tree have strings that differ in the last symbol only. So each nonempty string is $str(x)$ for at most one node, and the TST nodes are in one-to-one correspondence with the nodes of the trie of the same keys, other than its root. A TST of keys of total length $N$ has at most $N$ nodes, each with three links.

## Operations

```pseudo id=main
TST-GET(T, s)                                ▷ s is nonempty
L1  x ← T.root; d ← 0
L2  while x ≠ NIL do
L3      if s[d] < x.c then x ← x.left
L4      elseif s[d] > x.c then x ← x.right
L5      elseif d < |s| − 1 then x ← x.mid; d ← d + 1
L6      else return x.val
L7  return NIL

TST-PUT(T, s, v)                             ▷ s is nonempty, v ≠ NIL
L8  if T.root = NIL then T.root ← a new node with symbol s[0]; x ← T.root; d ← 0
L9  loop
L10     if s[d] < x.c then (create x.left with symbol s[d] if it is NIL); x ← x.left
L11     elseif s[d] > x.c then (create x.right with symbol s[d] if it is NIL); x ← x.right
L12     elseif d < |s| − 1 then d ← d + 1; (create x.mid with symbol s[d] if it is NIL); x ← x.mid
L13     else if x.val = NIL then T.n ← T.n + 1
L14         x.val ← v; return

TST-DELETE(T, s)
L15 walk as in TST-GET and record the path of nodes, with the link used to reach each one
L16 if the walk did not end at a node x with x.val ≠ NIL then return
L17 x.val ← NIL; T.n ← T.n − 1
L18 for each node y of the path, from x back to the root do
L19     if y.val ≠ NIL or y.mid ≠ NIL then return
L20     delete y from its sibling tree as in a BST delete, and store the new subtree in the link that pointed to y

KEYS-WITH-PREFIX(T, p)
L21 out ← empty list; if p = ε then start at T.root with prefix ε, else find the node x of p as in TST-GET (return out if none), append p if x.val ≠ NIL, and start at x.mid with prefix p
L22 walk the subtree in order: for each node y, first its left subtree, then y, then its right subtree
L23     at y with prefix t: if y.val ≠ NIL then append t · y.c to out
L24     then walk y.mid with prefix t · y.c
L25 return out
```

**Get.** Lines L1 to L7 run a BST search for the symbol $s[d]$ in the current sibling tree. When it finds the symbol, it moves to the next sibling tree through the middle link and to the next symbol, until the last symbol. A search miss ends at a NIL link.

**Put.** The same walk creates each missing node on its way: a new left or right node when the symbol is not in the sibling tree, and a new middle node when a symbol is matched and the key goes on. At the last symbol, lines L13 and L14 set the value.

**Delete.** After the value is removed, a node with no value and no middle child is dead. Line L20 removes it from its sibling tree with the [BST delete](/bst-deletion/): a node with at most one child is replaced by that child, and a node with two children by the smallest node of its right subtree. Removing a node that was the target of a middle link can make its parent dead too, so the loop goes up.

**Prefix walk.** The keys with prefix $p$ are $p$ itself and the keys in the tree below $x.mid$. The walk of lines L22 to L24 lists them in order, because in each sibling tree it visits the smaller symbols first, and at a node it reports $str(y)$ before the longer keys below $y.mid$.

**Longest prefix and wildcards.** The longest prefix walk is TST-GET that remembers the last matched node with a value. For a pattern with dots, the walk goes into the left, middle and right links when the pattern symbol is a dot, and follows the BST search otherwise.

## Example

Put the keys "she sells sea shells by the sea shore" with the values 0 to 7, in this order. The first key fixes the root symbol "s". The tree has 19 nodes, one for each nonempty prefix of the keys. In the drawing, `L:`, `M:` and `R:` show the link from the parent.

```
s
├── L: b
│   └── M: y 4
├── M: h
│   ├── L: e
│   │   └── M: l
│   │       ├── L: a 6
│   │       └── M: l
│   │           └── M: s 1
│   └── M: e 0
│       ├── M: l
│       │   └── M: l
│       │       └── M: s 3
│       └── R: o
│           └── M: r
│               └── M: e 7
└── R: t
    └── M: h
        └── M: e 5
```

| query | nodes compared | result |
|---|---|---|
| get("shore") | s, h, e, o, r, e | 7: the step from "e" to "o" is a right step |
| get("sea") | s, h, e, l, a | 6: "e" is left of "h", and "a" is left of "l" |
| get("by") | s, b, y | 4 |
| get("shy") | s, h, e, o | NIL: "y" is larger than "e" and "o", and the right link of "o" is NIL |
| keys_with_prefix("sh") | the node "h", then the walk below its middle link | she, shells, shore |
| keys_that_match(".he") | all three branches at the first symbol | she, the |
| delete("shells") | the nodes "s", "l", "l" below "she" become dead and are cut | 16 nodes remain |

A search for a key of length 5 compared 5 nodes for "sea" and 6 for "shore": one comparison for each symbol, plus one for each left or right step.

## Correctness

Each operation keeps (S1) to (S4). Inside one sibling tree, GET and PUT are a BST search and a BST insert on symbols, so (S1) holds, and when they match a symbol they move to the sibling tree of the next symbol. So the walk reaches the node $x$ with $str(x) = s$ if it exists, and PUT creates exactly the missing nodes on the path of $s$, as in the trie. DELETE removes only nodes with no value and no middle child; such a node carries no key and has no node below its middle link, and the BST delete keeps (S1) in its sibling tree. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $m = \lvert s \rvert$. A search does one comparison for each symbol matched (a middle step) and one for each left or right step, so its cost is $m + (\text{left and right steps})$.

| operation | worst case | random keys (expected) |
|---|---|---|
| get, put, delete | $O(m R)$; $O(m \log R)$ if each sibling tree is balanced | a miss uses about $\ln n$ symbol comparisons |
| keys with prefix $p$, a subtree of $t$ nodes | $O(mR + t)$ | |
| longest prefix of $s$ | $O(mR)$ | |
| space | 3 links, a symbol and a value for each of at most $N$ nodes | |

**Worst case.** A sibling tree holds at most $R$ symbols, so a BST search in it takes at most $R$ steps, and a search crosses at most $m$ sibling trees. If the symbols of a sibling tree are inserted in sorted order, the tree is a chain, so $O(mR)$ is reached.

**Random keys.** Sedgewick and Wayne (Section 5.2) state that a search miss in a TST built from $n$ random string keys uses about $\ln n$ symbol comparisons on average, and that a search hit or an insert uses one comparison for each symbol of the key, plus the left and right steps. A miss usually stops after a few symbols, so the left and right steps dominate its cost.

**Space.** The R-way trie needs $R$ links for each node, while the TST needs 3. For $R = 256$ and keys with few shared prefixes, this is a factor of about 85 less memory for links.

## Variants

- **Hybrid TST.** The [hybrid TST](/hybrid-tst/) replaces the top of the tree by an $R^2$ table indexed by the first two symbols, which removes most of the left and right steps near the root.
- **Balanced sibling trees.** Each sibling tree can be a red-black tree or a treap, which gives $O(m \log R)$ in the worst case. In practice, inserting the keys in random order is enough.
- **TST with terminal symbols.** Bentley and Sedgewick end each key with a terminal symbol (the byte 0 in C), so that the empty key and keys that are prefixes of others need no value field in the middle of a path.
- **Partial match and near neighbors.** The [wildcard matching](/wildcard-matching-in-trie/) walk and the search for keys within Hamming distance $k$ follow several links when the pattern allows it.
- **Multikey quicksort.** Sorting by three-way partition on the symbol at depth $d$ builds the TST of the keys implicitly; see [multikey quicksort](/multikey-quicksort/).

## When to use it

Use a TST when the keys are strings over a large alphabet, such as bytes or Unicode, and you need prefix, longest prefix or wildcard queries in little memory. Bentley and Sedgewick report that TSTs are competitive with hashing in practice, in particular for search misses, because a miss stops after a few symbols, while a hash function reads the whole key. Use an R-way [trie](/trie/) when $R$ is small (DNA, bits) and speed matters more than space. Use a [radix tree](/radix-tree/) when the keys are long with few shared prefixes, since a TST still has one node for each symbol of each unshared suffix.

## Pitfalls

- **The empty key.** A TST stores the value of a key at the node of its last symbol, so the empty string has no node. Reject it (as the Python class does), or keep its value in a separate field.
- **Sorted inserts.** Inserting the keys in sorted order makes each sibling tree a chain, and a search then pays up to $R$ comparisons for each symbol. Shuffle the keys before building a static TST.
- **Matching a symbol at the last position.** In line L5, the move to the middle link happens only when $d < \lvert s \rvert - 1$. Moving on the last symbol and then testing the value of the next node reads the wrong node, and fails at the end of the tree.
- **Deleting by clearing the value only.** Lazy deletion leaves dead nodes, which waste space and make "is there a key with prefix $p$?" return a wrong yes. Lines L18 to L20 prune, but the BST delete of line L20 must keep the order of the sibling tree.
- **Recursion depth.** The recursive code of the textbooks recurses once for each symbol and each left or right step. With long keys this overflows the stack of Python; the class uses loops and an explicit stack.

## Implementations

The Python class follows the main block with loops. The prefix walk and the wildcard walk use an explicit stack with a state flag to do the in-order visit. Keys must be nonempty strings.

## History

Bentley and Sedgewick presented ternary search trees at SODA in 1997, together with multikey quicksort, and showed that the two are the same recursion: a TST is built by the partitions that multikey quicksort makes. The idea of keeping the children of a trie node in a linked structure, instead of an array, is older: Knuth (Section 6.3) discusses it for the tries of de la Briandais. Sedgewick and Wayne make TSTs one of the two main string symbol tables of their Section 5.2.

## References
