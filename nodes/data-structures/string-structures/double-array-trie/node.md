---
tag: 8PV0JP
kind: data-structure
slug: double-array-trie
name: Double-array trie
aliases:
- darts
area: data-structures/string-structures
level: advanced
summary: Compact trie stored in two integer arrays (base and check) with constant-time transitions.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {m: the length of the key, N: the number of trie nodes, R: the alphabet size}
  time: {worst: O(m)}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [trie, array]
see_also: [trie, radix-tree, adaptive-radix-tree, louds-trie, deterministic-finite-automaton, longest-prefix-match, succinct-data-structures, hash-table]
sources:
  - paper: Jun-ichi Aoe, An efficient digital search algorithm by using a double-array structure, IEEE Transactions on Software Engineering 15(9), 1989, doi:10.1109/32.31365
    locator: pages 1066 to 1077, the base and check arrays, retrieval, insertion with relocation of siblings, and deletion
  - paper: Jun-ichi Aoe, Katsushi Morimoto and Takashi Sato, An efficient implementation of trie structures, Software Practice and Experience 22(9), 1992, doi:10.1002/spe.4380220902
    locator: pages 695 to 721, the double array with a separate TAIL array for single-branch suffixes, and its insertion and deletion
---

A double-array trie stores a [trie](/trie/) in two integer arrays, $base$ and $check$, so that each node is one cell index and the child of node $s$ on the symbol with code $a$ is the cell $t = base[s] + a$, which is valid exactly when $check[t] = s$. A transition thus costs two array reads, as in a full table of $R$ pointers per node, while the space is close to one pair of integers per node, as in a list of children, because the children of different nodes are interleaved in the same arrays. Aoe introduced the structure in 1989. It is the standard dictionary structure of morphological analyzers for Japanese and other languages, where static dictionaries with fast prefix searches are needed.

## In plain words

A trie node with a full table of 256 children is fast but mostly empty. A double array lets many nodes share one long table. Each node gets a starting point, its base, and its child for letter number $a$ sits at base plus $a$. The table cells left empty by one node are used by other nodes.

Since cells are shared, a cell must say whose child it is. That is the check array: the cell at base plus $a$ belongs to node $s$ only if its check says $s$. To follow a letter, add the letter's number to the base and look at the check. If it names the current node, you have moved; if not, the word is not there.

## The abstract type

The double-array trie implements the [string symbol table](/string-symbol-table/), and in practice mostly its static, read-only form: build once from a set of keys, then get, list the keys with a prefix, and list the keys that are prefixes of a text (the *common prefix search* of dictionary lookup in text). Aoe's paper also gives insertion and deletion, which move groups of siblings to new places when their cells are needed.

## Representation

Symbols are mapped to codes $1, \ldots, R$, and code 0 is an end-of-key symbol. The arrays $base$ and $check$ have the same length $M$.

- The root is cell 0, with $check[0]$ a reserved mark.
- A cell $t$ is *free* if $check[t] = -1$.
- For a node $s$ of the trie, its children sit in the cells $base[s] + a$ for the codes $a$ of its child symbols, and these cells have $check = s$.
- If the path of $s$ is a key, $s$ has a child on code 0, a *leaf cell* $t = base[s]$, and $base[t]$ stores the value or, as here, a negative number $-(i + 1)$ that indexes the value $i$ in a separate array.

**Invariant.**

- **(D1) Children.** For each node $s$ and each code $a$, the trie node $s$ has a child on $a$ if and only if $t = base[s] + a$ is in range and $check[t] = s$, and then $t$ is that child.
- **(D2) Ownership.** Each cell other than the root is free or is the child of exactly one node, the one named by its check.
- **(D3) Keys.** A key $k$ is stored if and only if the walk on the codes of $k$ from the root reaches a node with a leaf cell, which holds the value of $k$.

(D1) and (D2) together say that the sets of cells $\{base[s] + a\}$ of the children of different nodes are disjoint.

## Operations

```pseudo id=main
DA-NEXT(s, a)                     ▷ the child of s on code a
L1  t ← base[s] + a
L2  if 0 ≤ t < M and check[t] = s then return t
L3  return NIL

DA-GET(k)
L4  s ← 0; for each symbol c of k: s ← DA-NEXT(s, code(c)); if s = NIL then return NIL
L5  t ← DA-NEXT(s, 0)
L6  if t ≠ NIL then return the value of the leaf cell t else return NIL

DA-BUILD(K)
L7  build the ordinary trie of K, with a child on code 0 at each node where a key ends
L8  queue ← [(root of the trie, cell 0)]; while the queue is not empty:
L9      (u, s) ← dequeue; C ← the codes of the children of u
L10     b ← the smallest b ≥ 1 such that the cell b + a is free for every a in C (grow the arrays if needed)
L11     base[s] ← b; for each a in C: check[b + a] ← s
L12     for each a in C: if a = 0 then store the value of u's key in the leaf cell b else enqueue (the child of u on a, cell b + a)
```

**Lookup.** Each symbol costs one DA-NEXT: one addition, two array reads and one comparison, with no search among siblings. The lookup is $O(m)$ for a key of length $m$, with a small constant.

**Build.** The children of a node must be placed together, at offsets given by their codes from one base. Line L10 finds the first base where all of them fit; this is the step that interleaves the nodes. The search for a base is the costly part of building; real builders keep a linked list of free cells and skip bases that cannot work.

**Insertion (Aoe).** To add a child on code $a$ to a node $s$ when the cell $base[s] + a$ is taken by another node $s'$, Aoe's algorithm moves the children of one of the two nodes, the one with fewer children, to a new base where they all fit, updates the checks of the grandchildren that pointed to the moved cells, and then inserts. Deletion frees the cells of the removed nodes.

**Common prefix search.** Walk the symbols of a text from the root, and after each step test the child on code 0. Each success is a dictionary word that starts the text. Morphological analyzers run this at each position of a sentence to find candidate words.

## Example

Store ab, ac, b, bc with values 0 to 3. The codes are a = 1, b = 2, c = 3, and 0 ends a key. Building in breadth-first order gives:

| step | node (path) | child codes | base | cells taken |
|---|---|---|---|---|
| 1 | root, cell 0 | a, b | 1 | 2 (a), 3 (b) |
| 2 | a, cell 2 | b, c | 2 | 4 (ab), 5 (ac) |
| 3 | b, cell 3 | end, c | 6 | 6 (end of b), 9 (bc) |
| 4 | ab, cell 4 | end | 1 | 1 (end of ab) |
| 5 | ac, cell 5 | end | 7 | 7 (end of ac) |
| 6 | bc, cell 9 | end | 8 | 8 (end of bc) |

At step 3, the bases 1 to 5 fail because one of the cells $b$ or $b + 3$ is taken, and 6 is the first base for which cells 6 and 9 are free. At step 4, cell 1, left free by the root, is used. The final arrays have 10 cells:

| cell | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| base | 1 | −1 | 2 | 6 | 1 | 7 | −3 | −2 | −4 | 8 |
| check | root | 4 | 0 | 0 | 2 | 2 | 3 | 5 | 9 | 3 |

The leaf cells hold $-(i + 1)$ for the value index $i$: cell 1 holds −1 for ab, cell 6 holds −3 for b. A lookup of bc goes from cell 0 on b to $1 + 2 = 3$ ($check[3] = 0$), on c to $6 + 3 = 9$ ($check[9] = 3$), and on the end code to $8 + 0 = 8$ ($check[8] = 9$), which holds −4, the value 3. A lookup of a goes to cell 2 and then to $2 + 0 = 2$, whose check is 0, not 2, so a is not a key. The trie has 10 nodes counting the leaf cells, and the arrays have no free cell.

## Correctness

By (D1), DA-NEXT returns exactly the child of $s$ on code $a$, so DA-GET follows the trie path of $k$ and, by (D3), finds the value. The build keeps (D1) and (D2) because line L10 only uses free cells, and each node's base is set once, before its children are placed. The check test is what rules out false transitions: a cell $base[s] + a$ that belongs to another node has a check different from $s$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | cost |
|---|---|
| DA-NEXT | $O(1)$ |
| get, prefix walk, common prefix search over a text prefix of length $m$ | $O(m)$ |
| list the keys below a node | $O(R)$ per node visited, since the children are found by testing every code |
| build, as in the pseudocode | $O(N \cdot M \cdot R)$ in the worst case for the naive base search |
| space | $2M$ integers, with $M \ge N$ cells for $N$ trie nodes, plus the values |

The number of cells $M$ is at least the number of nodes $N$, and the difference is the number of free cells left by the placement. How many cells stay free depends on the order in which nodes are placed and on the base search; builders that place nodes with many children first and keep a free list leave few gaps.

**Compared with other tries.** A trie with arrays of $R$ pointers uses $NR$ cells for $N$ nodes and the same $O(1)$ step. A trie with sorted lists of children uses about $N$ cells but needs a search per step. The double array has the step of the first and nearly the space of the second, at the cost of a slow and complicated update.

## Variants

- **TAIL array.** Aoe, Morimoto and Sato (1992) store each suffix that has no branching, the part of a key below the last branching node, as a string in a separate TAIL array, so that the double array only holds the branching part of the trie. This saves most of the cells for sets of long keys.
- **Automata.** The same base and check layout stores the transition table of any sparse [deterministic finite automaton](/deterministic-finite-automaton/), not only a trie: a state is a cell, and the check names the source state of each transition.
- **Darts and similar libraries.** Darts (double-array trie system) and its successors are widely used static implementations, built from sorted key lists and used by morphological analyzers.
- **Succinct tries.** When memory matters more than speed, a [LOUDS trie](/louds-trie/) or another [succinct](/succinct-data-structures/) encoding uses about 2 bits per node plus the labels, at the cost of slower steps.

## When to use it

Use a double-array trie for a large static dictionary that needs very fast lookups and prefix searches, such as the word list of a tokenizer or a morphological analyzer. If the set changes often, an [adaptive radix tree](/adaptive-radix-tree/) or a [hash table](/hash-table/) is easier to update. If space is the main constraint, use a succinct trie.

## Pitfalls

- **Forgetting the check.** Testing only that $base[s] + a$ is in range, or that the cell is in use, follows edges of other nodes and returns wrong keys. The test $check[t] = s$ is essential.
- **Base 0 and the root.** If $base[s]$ can be 0, the cell $base[s] + 0$ may be the root itself or a cell that collides with a reserved mark. Start bases at 1 and give the root a check that no node index equals.
- **Keys that are prefixes of other keys.** Without an end code, a node cannot tell whether its path is a key. Use code 0 for the end of a key, as here, or a flag in the cell.
- **Slow builds.** The naive search for a base is quadratic in practice for large dictionaries. Keep a free list, place the nodes with the most children first, and remember for each node size the last base that failed.
- **Integer width.** Bases and checks must hold indexes up to $M$; with 32-bit cells the arrays are limited to about $2^{31}$ cells, and negative values used for leaves reduce the range further.

## Implementations

The Python class is static: it builds the plain trie of the keys with dictionaries, then places the nodes in breadth-first order with the naive base search of line L10. It stores value indexes in the leaf cells as negative numbers and offers get, prefix listing and common prefix search. The tests replay the example of this page and compare random key sets and queries against a dictionary.

## History

Aoe introduced the double-array structure in 1989, with retrieval, insertion and deletion. Aoe, Morimoto and Sato (1992) added the TAIL array for single-branch suffixes. Static double arrays became the dictionary format of Japanese morphological analyzers in the 2000s, through libraries such as Darts.

## References
