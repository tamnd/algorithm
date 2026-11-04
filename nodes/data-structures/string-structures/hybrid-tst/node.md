---
tag: EHWQ99
kind: data-structure
slug: hybrid-tst
name: Hybrid ternary search trie with R^2 root branching
aliases:
- Hybrid TST with R^2 branching at the root
area: data-structures/string-structures
level: core
summary: Ternary search trie variant whose root branches on the first two characters through an R by R table, speeding up searches.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {m: the length of the query key, R: the alphabet size, N: the total length of the keys}
  time: {worst: O(m R)}
  space: {extra: Θ(R^2 + N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [ternary-search-tree, trie]
see_also: [ternary-search-tree, trie, string-symbol-table, prefix-matching, burst-trie, msd-radix-sort, multikey-quicksort, hash-table]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.2 (Tries), the discussion of TSTs with R^2 branching at the root and the table of costs of string symbol table implementations
  - paper: Jon L. Bentley and Robert Sedgewick, Fast algorithms for sorting and searching strings, Proceedings of the 8th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1997)
    locator: pages 360 to 369, ternary search trees and their search cost
  - paper: Julien Clément, Philippe Flajolet and Brigitte Vallée, The analysis of hybrid trie structures, Proceedings of the 9th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1998)
    locator: the analysis of tries whose nodes are arrays, lists or binary search trees, with the ternary search trie as the BST case
---

A hybrid TST with $R^2$ branching at the root is a [ternary search tree](/ternary-search-tree/) whose top two levels are replaced by a table of $R \times R$ entries, indexed by the first two symbols of the key, where $R$ is the size of the [alphabet](/alphabet/). Each entry holds the value of the two-symbol key and a TST for the rest of the keys that start with those two symbols. A search pays one table access for the first two symbols, instead of the left and right steps that a TST takes near its root, which is where most of them happen. Sedgewick and Wayne (Section 5.2) give it as a practical improvement of the TST for large sets of keys.

## In plain words

In a ternary search tree, the first letter of every word is found by a search among up to all the letters of the alphabet, and the second letter again by a search among the letters that follow the first. These two searches at the top are paid by every lookup, and they are the most crowded part of the tree.

The hybrid replaces the top of the tree by a big table with one box for each pair of first letters, such as "sh" or "th". To find a word, you jump straight to the box of its first two letters. Inside the box there is a small ternary search tree that holds only the words that start with those two letters, and the search goes on there. Short words of one or two letters are kept in the table directly.

## The abstract type

The hybrid TST implements the [string symbol table](/string-symbol-table/) with the same operations as the TST: `put`, `get`, `delete`, `keys_with_prefix`, `longest_prefix_of` and the ordered walk of all keys. Unlike the plain TST, it can store the empty key and the keys of length 1 without special cases inside the tree.

## Representation

The alphabet is $\Sigma = \{\sigma_0 < \sigma_1 < \cdots < \sigma_{R-1}\}$, and $\iota(\sigma_a) = a$ is the index of a symbol.

- $T.short$ holds the values of the keys of length 0 and 1: one field for $\varepsilon$ and an array of $R$ values for the one-symbol keys.
- $T.table$ is an array of $R^2$ cells, indexed by $\iota(a) \cdot R + \iota(b)$ for the pair of symbols $ab$. A cell is NIL or holds a value $cell.val$ for the key $ab$ and the root $cell.tst$ of a [ternary search tree](/ternary-search-tree/).
- $T.n$ is the number of keys.

**Invariant.**

- **(H1) Short keys.** A string of length at most 1 is a key with value $v$ if and only if $T.short$ holds $v \ne$ NIL for it.
- **(H2) Cells.** For each pair $ab$, the cell of $ab$ is NIL if and only if no key starts with $ab$. If the cell exists, its value is the value of $ab$ (or NIL if $ab$ is not a key), and its TST holds exactly the pairs $(t, v)$ such that $ab \cdot t$ is a key with value $v$ and $t \ne \varepsilon$.
- **(H3) TSTs.** Each TST of a cell meets the TST invariant: BST order in each sibling tree, no dead node, and keys at the nodes of their last symbol.
- **(H4) Count.** $T.n$ is the number of keys.

## Operations

The procedures TST-GET, TST-PUT and TST-DELETE are those of the [ternary search tree](/ternary-search-tree/), run on the TST of one cell with the key less its first two symbols.

```pseudo id=main
HYBRID-GET(T, s)
L1  if |s| < 2 then return the value of s in T.short
L2  cell ← T.table[ι(s[0]) · R + ι(s[1])]
L3  if cell = NIL then return NIL
L4  if |s| = 2 then return cell.val
L5  return TST-GET(cell.tst, s[2 ..])

HYBRID-PUT(T, s, v)
L6  if |s| < 2 then set the value of s in T.short to v (add 1 to T.n if s was not a key); return
L7  cell ← T.table[ι(s[0]) · R + ι(s[1])]; if cell = NIL then make it a new empty cell
L8  if |s| = 2 then (add 1 to T.n if cell.val = NIL); cell.val ← v; return
L9  TST-PUT(cell.tst, s[2 ..], v) (add 1 to T.n if s[2 ..] was not in the TST)

HYBRID-DELETE(T, s)
L10 if |s| < 2 then clear the value of s in T.short (subtract 1 from T.n if it was a key); return
L11 cell ← T.table[ι(s[0]) · R + ι(s[1])]; if cell = NIL then return
L12 if |s| = 2 then (subtract 1 from T.n if cell.val ≠ NIL); cell.val ← NIL
L13 else TST-DELETE(cell.tst, s[2 ..]) (subtract 1 from T.n if it removed a key)
L14 if cell.val = NIL and cell.tst = NIL then T.table[ι(s[0]) · R + ι(s[1])] ← NIL

HYBRID-KEYS-WITH-PREFIX(T, p)
L15 if p = ε then return [ε if it is a key] followed by HYBRID-KEYS-WITH-PREFIX(T, σ) for σ = σ_0, ..., σ_{R−1}
L16 if |p| = 1 then return [p if it is a key] followed, for b = σ_0, ..., σ_{R−1} with a cell for p·b, by [p·b if cell.val ≠ NIL] and the keys of cell.tst, each with p·b in front
L17 cell ← the cell of p[0] p[1]; if cell = NIL then return the empty list; if |p| = 2 then return [p if cell.val ≠ NIL] followed by the keys of cell.tst with p in front
L18 return the keys of TST-KEYS-WITH-PREFIX(cell.tst, p[2 ..]), each with p[0] p[1] in front
```

**Get and put.** A key of length at least 2 picks its cell in $O(1)$ time from its first two symbols. Lines L5 and L9 then run the TST search on the rest of the key, in a TST that holds only the keys of that cell.

**Delete.** Line L13 runs the pruning delete of the TST, and line L14 frees a cell that no longer holds any key. Without line L14, the test "some key starts with $ab$" by a look at the cell would give wrong answers.

**Prefix walk.** For $\lvert p \rvert \ge 2$, the walk is the TST walk in one cell. For a prefix of length 1, it must visit the $R$ cells of the row of $p$, in order of the second symbol, so the cost has a term $R$. The empty prefix visits all $R^2$ cells.

## Example

Put the keys "she sells sea shells by the sea shore" with the values 0 to 7, over the alphabet of the 26 lowercase letters. The table has $26^2 = 676$ cells, and 4 of them are used.

| cell | value | keys in its TST (the key less its first two letters) | TST nodes |
|---|---|---|---|
| by | 4 | none | 0 |
| se | NIL | a (6), lls (1) | 4 |
| sh | NIL | e (0), ells (3), ore (7) | 7 |
| th | NIL | e (5) | 1 |

The four TSTs have 12 nodes in all, against 19 in the plain TST of the same keys: the nodes of the first two symbols are now table cells.

- **get("shore")** goes to the cell "sh" in one step. Its TST has the root "e" (from "she", the first key put there), so the search for "ore" compares "o" with "e" and goes right, then matches "o", "r" and "e". That is 4 symbol comparisons, against 6 in the plain TST, where the search also passes the root "s" and the node "h", and then makes the same right step.
- **get("by")** reads the value 4 from the cell "by" with no comparison at all. In the plain TST it takes 3 comparisons.
- **keys_with_prefix("s")** visits the 26 cells of row "s" in order. The cells "se" and "sh" give sea, sells, she, shells, shore.
- **delete("by")** clears the value of the cell "by". Its TST is empty, so line L14 frees the cell.

## Correctness

The operations keep (H1) to (H4) because each key goes to exactly one place, fixed by its length and its first two symbols: $T.short$ for length at most 1, the value of a cell for length 2, and a TST for longer keys. Inside a TST, the correctness of TST-GET, TST-PUT and TST-DELETE is that of the [ternary search tree](/ternary-search-tree/). The prefix walk is in order because the cells are visited in lexicographic order of their two symbols, and inside a cell the TST walk is in order. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $m = \lvert s \rvert$ and let $n_c$ be the number of keys in the cell of the first two symbols of $s$.

| operation | cost |
|---|---|
| get, put, delete with $m \le 2$ | $O(1)$ |
| get, put, delete with $m > 2$ | $O(1)$ plus a TST search on $m - 2$ symbols in a TST of $n_c$ keys: $O((m - 2) R)$ worst case, $O(m - 2)$ plus the left and right steps |
| keys with prefix $p$, $\lvert p \rvert \ge 2$ | the TST prefix walk in one cell |
| keys with prefix $p$, $\lvert p \rvert = 1$ | $O(R)$ plus the walks of the cells of the row |
| all keys | $O(R^2 + N)$ |
| space | $R^2$ cells plus 3 links for each TST node, at most $N$ nodes |

**Where the gain comes from.** In a TST, the left and right steps of a search happen in the sibling trees of the levels it crosses. The first two levels have the largest sibling trees: up to $R$ and $R$ symbols, while deep levels often have one or two. The table removes these two levels, so a search saves the BST searches for the first two symbols. If the first two symbols of the keys are spread over many pairs, each cell holds only about $n / (\text{number of used cells})$ keys, so the TST of a cell is much smaller than the whole TST.

**Space.** The table costs $R^2$ cells even when few are used. For $R = 256$ this is 65536 cells, which is small for a dictionary of millions of keys and wasteful for a few hundred keys. For Unicode, $R^2$ is too large, and the hybrid is used on bytes.

## Variants

- **One-symbol root table.** An array of $R$ TSTs, one for each first symbol, costs only $R$ cells and removes one level of BST search.
- **$R^k$ branching.** A table indexed by the first $k$ symbols removes $k$ levels, at the cost of $R^k$ cells. For $k \ge 3$ and bytes, the table is usually larger than the data, and a [hash table](/hash-table/) of the used prefixes is the better root.
- **Burst trie.** The [burst trie](/burst-trie/) is the opposite approach: it starts with a trie of arrays and switches to small containers only when few keys are left below a node.
- **MSD radix sort cut-off.** In sorting, the same idea is to start with key-indexed counting on the first symbols, as [MSD radix sort](/msd-radix-sort/) does, and switch to [multikey quicksort](/multikey-quicksort/) on the small subarrays.

## When to use it

Use the hybrid TST for a large static or slowly changing dictionary of byte strings, such as a word list or a set of URLs, where searches dominate and $R^2$ cells are cheap compared with the data. Use a plain [ternary search tree](/ternary-search-tree/) when the set is small or the alphabet is large. Use a [hash table](/hash-table/) if only exact get and put are needed.

## Pitfalls

- **Short keys.** Keys of length 0, 1 and 2 have no TST node below the table. Code that sends every key to a cell TST crashes on "a" or stores "by" as an empty string in a TST. Lines L1, L4, L6 and L8 handle them.
- **Empty cells after delete.** A cell whose TST becomes empty and whose value is NIL must be freed (line L14). Else a prefix query on a pair that has no key returns an empty answer only after visiting a dead cell, and a "some key starts with $p$" test gives a wrong yes.
- **The row walk.** A prefix of length 1 visits a whole row of $R$ cells, and the empty prefix visits $R^2$ cells. Do not use the empty-prefix walk to list a small table.
- **Symbols outside the alphabet.** The index $\iota(s[0]) \cdot R + \iota(s[1])$ is wrong or out of range for a symbol not in $\Sigma$. Check the symbols, or map them to bytes first.

## Implementations

The Python class takes the alphabet as a sorted string, so that tests can use a small alphabet, and stores the table as a list of $R^2$ cells. Its TST code is the same as on the [ternary search tree](/ternary-search-tree/) page, with an explicit stack for the walks.

## History

Bentley and Sedgewick introduced ternary search trees in 1997. Sedgewick and Wayne (Section 5.2) recommend $R^2$ branching at the root as the simplest improvement of the TST for large sets, and include it in their table of costs of string symbol tables. Clément, Flajolet and Vallée (1998) analysed tries whose nodes are arrays, lists or BSTs, which gives a framework for such hybrids.

## References
