---
tag: 4A6SZN
kind: data-structure
slug: radix-tree
name: Radix tree
aliases:
- compressed trie
- Patricia tree
- compact prefix tree
area: data-structures/string-structures
level: core
summary: Trie in which every chain of single-child nodes is merged into one edge labelled by a string.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {n: the number of keys, m: the length of the query key}
  time: {worst: Θ(m)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [trie]
see_also: [trie, prefix-matching, longest-prefix-match, adaptive-radix-tree, suffix-tree, ternary-search-tree, string-b-tree, hat-trie]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.3 (Digital searching), Algorithm P (Patricia) and its analysis
  - paper: doi:10.1145/321479.321481
    title: Donald R. Morrison, PATRICIA, Practical Algorithm To Retrieve Information Coded in Alphanumeric, Journal of the ACM 15(4), 1968
    locator: pages 514 to 534
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 12, Problem 12-2 (Radix trees), where the name is used for a binary trie that is not compressed
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 5.2 (the suffix tree as a compacted trie of the suffixes, with edges labelled by substrings)
---

A radix tree is a [trie](/trie/) in which each chain of nodes that have one child and no key is merged into one edge, so that edges are labelled by nonempty strings and each node without a key has at least two children. A tree of $n$ keys then has at most $2n$ nodes, whatever the length of the keys. Search, insert and delete still read the key once, in $\Theta(m)$ time for a key of length $m$, and the [prefix matching](/prefix-matching/) walk costs $O(k)$ nodes for $k$ results. The binary version of Morrison (1968) is PATRICIA, and the radix tree of all suffixes of a text is the [suffix tree](/suffix-tree/).

## In plain words

In a trie, the word "shore" needs a node for each letter, even after the point where no other word shares its path. The nodes for "o", "r" and "e" each have one child and decide nothing.

A radix tree removes these useless nodes. A branch can carry a piece of a word, such as "ore", instead of one letter. A node stays only where two words part ways or where a word ends. To look up a word, you follow the branch that starts with the next letter and check that the whole piece on it matches. When a new word parts from a branch in the middle of its piece, the piece is cut in two and a new node is put at the cut.

## The abstract type

A radix tree implements the [string symbol table](/string-symbol-table/), with the same operations as a trie: `put`, `get`, `delete`, `keys_with_prefix`, `longest_prefix_of` and the ordered walk. It is often used as a static index too, because its small node count makes it a good layout for the keys of a large set.

## Representation

Each node $x$ has a field $x.val$ (a value or NIL) and a map $x.edges$ from symbols to edges. An edge $e$ has a nonempty label string $e.label$ and a child node $e.child$, and it is stored under its first symbol. For a node $x$, $str(x)$ is the concatenation of the labels on the path from the root to $x$. In practice a label is stored as a pointer into a key and a length, not as a copy.

**Invariant.**

- **(R1) Labels.** Each edge label is nonempty, and each edge is stored under the first symbol of its label. So the labels of the edges out of one node start with distinct symbols.
- **(R2) Keys.** A string $s$ is a key with value $v$ if and only if some node $x$ has $str(x) = s$ and $x.val = v \ne$ NIL.
- **(R3) Branching.** Each node other than the root that has no value has at least two children.
- **(R4) Count.** $T.n$ is the number of nodes with a value.

By (R3), a leaf other than the root has a value, so there are at most $n$ leaves. A rooted tree with $L$ leaves has at most $L - 1$ nodes with two or more children. So the nodes without a value, other than the root, number at most $n - 1$, and the tree has at most $1 + n + (n - 1) = 2n$ nodes for $n \ge 1$. The radix tree of a set of keys is unique: its nodes are the root, the keys, and the strings $str$ where two keys first differ, which are the longest common prefixes of pairs of keys.

## Operations

```pseudo id=main
RADIX-GET(T, s)
L1  x ← T.root; i ← 0
L2  while i < |s| do
L3      e ← x.edges[s[i]]                       ▷ NIL if there is no such edge
L4      if e = NIL or e.label is not a prefix of s[i ..] then return NIL
L5      i ← i + |e.label|; x ← e.child
L6  return x.val

RADIX-PUT(T, s, v)                              ▷ v ≠ NIL
L7  x ← T.root; i ← 0
L8  while i < |s| do
L9      e ← x.edges[s[i]]
L10     if e = NIL then add an edge labelled s[i ..] from x to a new leaf with value v; T.n ← T.n + 1; return
L11     j ← the length of the longest common prefix of e.label and s[i ..]   ▷ j ≥ 1
L12     if j < |e.label| then                   ▷ s leaves the edge inside its label: split it
L13         z ← a new node with no value; add to z an edge with label e.label[j ..] to e.child
L14         e.label ← e.label[0 .. j − 1]; e.child ← z
L15     i ← i + j; x ← e.child
L16 if x.val = NIL then T.n ← T.n + 1
L17 x.val ← v

RADIX-DELETE(T, s)
L18 walk as in RADIX-GET and record the path of nodes from the root to the node x of s
L19 if there is no such node or x.val = NIL then return
L20 x.val ← NIL; T.n ← T.n − 1
L21 if x ≠ T.root and x has no edge then remove the edge from its parent p to x; x ← p
L22 if x ≠ T.root and x.val = NIL and x has exactly one edge f then replace the edge e from the parent of x to x by one edge with label e.label · f.label to f.child

KEYS-WITH-PREFIX(T, p)
L23 walk down from the root by the symbols of p; if p ends inside the label of an edge, go to the child of that edge; let x be the node reached and t = str(x), or return the empty list if p leaves the tree
L24 out ← empty list; stack ← [(x, t)]
L25 while stack is not empty do
L26     (y, u) ← pop(stack)
L27     if y.val ≠ NIL then append u to out
L28     for each edge f of y, in decreasing order of first symbol do push (f.child, u · f.label)
L29 return out
```

**Get.** The walk of lines L1 to L5 is the trie walk with whole labels. By (R1), at most one edge can start with $s[i]$, so the walk has no choice. A label that matches only partly (line L4) means that no key and no node starts with $s$.

**Put.** Lines L8 to L15 walk down $s$. If no edge starts with the next symbol, line L10 hangs the rest of $s$ as one new leaf. If $s$ leaves an edge in the middle of its label, lines L12 to L14 cut the edge at the point $j$ where they differ, or where $s$ ends, and put a node there. The loop then goes on from the new node. Each put adds at most two nodes: the cut node and the new leaf.

**Delete.** After the value is removed, at most two nodes can break (R3). A leaf without a value is cut (line L21), and then its parent may be left with one child and no value. A node with one child and no value is merged with its child into one edge (line L22). A node with two or more children stays.

**Prefix walk.** The prefix $p$ can end in the middle of a label. Then every key below that edge starts with $p$, so the walk goes on to the child. The output is in lexicographic order for the same reason as in the trie. The [longest prefix match](/longest-prefix-match/) walk is GET that remembers the last node with a value, as in the [trie](/trie/).

## Example

Put the keys "she sells sea shells by the sea shore" with the values 0 to 7, in this order. The table gives the change of each put and the number of nodes after it.

| put | what happens | nodes |
|---|---|---|
| she 0 | new leaf "she" under the root | 2 |
| sells 1 | the edge "she" and "sells" agree on 1 symbol: cut "she" into "s" and "he", then add the leaf "ells" | 4 |
| sea 2 | below "s", the edge "ells" and "ea" agree on 1 symbol: cut it into "e" and "lls", then add the leaf "a" | 6 |
| shells 3 | follow "s", "he"; add the leaf "lls" below "she" | 7 |
| by 4 | new leaf "by" under the root | 8 |
| the 5 | new leaf "the" under the root | 9 |
| sea 6 | the node of "sea" exists; its value becomes 6 | 9 |
| shore 7 | below "s", the edge "he" and "hore" agree on 1 symbol: cut it into "h" and "e", then add the leaf "ore" | 11 |

```
(root)
├── by 4
├── s
│   ├── e
│   │   ├── a 6
│   │   └── lls 1
│   └── h
│       ├── e 0
│       │   └── lls 3
│       └── ore 7
└── the 5
```

The trie of the same keys has 20 nodes. Here 11 nodes remain, within the bound $2n = 14$.

- **get("shel")** follows "s" and "h", then the edge "e" to the node "she", and then the edge "lls" is not a prefix of "l". The answer is NIL.
- **keys_with_prefix("shel")** ends inside the label "lls" below "she", goes to its child and returns "shells".
- **delete("she")**: the node "she" keeps one child and has no value, so line L22 merges it: the node "sh" gets the edge "ells" to "shells". 10 nodes remain.
- **delete("sea")**: the leaf "sea" is cut (line L21), and its parent "se" has one child left, so line L22 merges "e" and "lls" into "ells". 8 nodes remain.

## Correctness

Each operation keeps (R1) to (R4) and returns what the string symbol table defines. The walk lemma of the trie holds with labels: from a node, at most one edge can be on the path to a given string. A split replaces one edge by two edges with the same concatenated label, so it changes no $str$ of an old node, and the new node gets a second child (line L10) or the value (line L17) in the same put. A merge replaces two edges by one edge with the concatenated label, and removes a node that has no value. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/), with children in a hash map (expected costs) or in an array of $R$ links (worst-case costs plus $\Theta(R)$ space for each node).

| operation | time |
|---|---|
| get, search miss | $O(m)$: each symbol of $s$ is compared at most once, and each step visits a new node |
| put | $O(m)$, plus at most two new nodes |
| delete | $O(m)$, plus at most one cut and one merge |
| keys with prefix $p$, $k$ results | $O(m + k)$ nodes, plus the length of the output strings |
| longest prefix of $s$ | $O(m)$ |
| space | at most $2n$ nodes and $2n - 1$ edges, plus the keys |

**Node count.** The bound of $2n$ nodes was shown under the invariant. It does not depend on the key lengths, which is the point of the structure: a trie of $n$ keys of length $\ell$ that share no prefix has $1 + n\ell$ nodes, while the radix tree has $n + 1$.

**Walk length.** A search visits at most $\min(m, h) + 1$ nodes, where $h$ is the height. The symbol comparisons cost $O(m)$ in total, because each label is compared with a new part of $s$. With labels stored as pointers, a node takes $O(1)$ words, so the space is $\Theta(n)$ words besides the keys.

**Prefix walk.** The subtree below the node of $p$ holds the $k$ results. Its leaves have values, and its nodes without a value have two or more children, so it has fewer than $2k$ nodes. So the walk costs $O(k)$ besides the output.

**Patricia.** Morrison's PATRICIA works on bit strings and stores at each node only the index of the bit to test, not the label. A search tests one bit at each node and compares the key with the one stored key at the end. Knuth (Section 6.3) shows that for $n$ random keys a successful search tests about $\lg n$ bits on average.

## Variants

- **PATRICIA.** The binary version, with bit indexes at the nodes and one full key comparison at the end of each search. It needs to read the key only at the leaf, which helps when keys are on disk.
- **Crit-bit tree.** A PATRICIA tree for byte strings that stores at each node the first byte and bit where the keys of the two subtrees differ.
- **Adaptive radix tree.** The [adaptive radix tree](/adaptive-radix-tree/) uses nodes of 4, 16, 48 or 256 children by need, and is an index of main-memory databases.
- **Suffix tree.** The radix tree of all suffixes of a text with a [sentinel character](/sentinel-character/) is the [suffix tree](/suffix-tree/). Its edges point into the text, so it takes $O(n)$ space for a text of length $n$.
- **String B-tree.** The [string B-tree](/string-b-tree/) puts a PATRICIA tree in each node of a B-tree, for keys on disk.
- **Burst trie and HAT-trie.** The [burst trie](/burst-trie/) and the [HAT-trie](/hat-trie/) end a trie path in a bucket of keys instead of compressing it.

## When to use it

Use a radix tree when the keys are long and share few prefixes, so that a plain trie would have many nodes with one child. File paths, URLs, IP prefixes and identifiers are typical cases. Use a plain trie when the keys are short and dense, because its code is simpler and its nodes have a fixed size. Use a [hash table](/hash-table/) when no prefix or ordered query is needed.

## Pitfalls

- **Forgetting the split.** When a new key leaves an edge in the middle of its label, a put that only adds a leaf at the child of the edge creates a wrong path. Lines L11 to L14 must cut the label first.
- **Partial label match on a search.** Line L4 must check the whole label. A search that checks only the first symbol of each label, as in PATRICIA, must compare the key with the stored key at the end, or it returns false hits.
- **Merging after delete.** A delete that only clears $x.val$ leaves nodes with one child and no value, which breaks (R3) and the $2n$ bound. Lines L21 and L22 cut and merge. The root is never merged, because its $str$ is the empty string and it must stay.
- **A prefix that ends inside a label.** In KEYS-WITH-PREFIX, a walk that stops when $p$ ends inside a label and returns no result misses all keys below that edge. Line L23 goes on to the child.
- **The name.** CLRS (Problem 12-2) uses "radix tree" for a binary trie without compression. Check which meaning a source uses.

## Implementations

The Python class stores each edge as a pair (label, child) in a dictionary keyed by the first symbol of the label. Labels are copies of string pieces, which is simpler but uses more space than pointers into the keys.

## History

Donald R. Morrison published PATRICIA in 1968 in the Journal of the ACM, as a method to search a large text by its keys with one bit test at each node. Knuth (Section 6.3) describes PATRICIA as Algorithm P and analyses it. Weiner's suffix tree of 1973 and McCreight's construction of 1976 use the same compaction of a trie for the suffixes of a text.

## References
