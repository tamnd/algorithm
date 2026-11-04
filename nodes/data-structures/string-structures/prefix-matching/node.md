---
tag: NCH2NW
kind: problem
slug: prefix-matching
name: Prefix matching
aliases:
- Prefix matches
area: data-structures/string-structures
level: intro
summary: Problem of listing every key in a string set that starts with a given prefix, solved by walking a trie.
prereqs: [trie, string-symbol-table]
see_also: [trie, ternary-search-tree, radix-tree, longest-prefix-match, wildcard-matching-in-trie, suffix-array-search, substring-queries, binary-search]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.2 (Tries), the operations keysWithPrefix and collect in TrieST and TST
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.3 (Digital searching), tries and Patricia
  - paper: Jon L. Bentley and Robert Sedgewick, Fast algorithms for sorting and searching strings, Proceedings of the 8th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1997)
    locator: pages 360 to 369, searching in ternary search trees
---

Prefix matching is the problem of listing, for a set of strings stored in advance and a query string $p$, each stored key that starts with $p$. It is the `keys_with_prefix` query of the [string symbol table](/string-symbol-table/). A [trie](/trie/) solves it by walking down the symbols of $p$ and listing the subtree below, in time that depends on the length of $p$ and on the size of the answer, but not on the number of keys. The same query on the suffixes of one text is the [substring query](/substring-queries/).

## In plain words

You type the first letters of a word, and a search box shows each stored word that begins with those letters. That is prefix matching. The stored words are known in advance, and many queries come later, so it pays to organize the words first.

If the words are in a tree where each branch is one letter, the words that begin with "sh" all hang below the branch for "s" and then "h". You walk down two branches and then collect everything below. If the words are in sorted order instead, the words that begin with "sh" sit next to each other in the list, and two binary searches find the start and the end of that block.

## Definition

**Input.** A finite set $K \subseteq \Sigma^*$ of $n$ keys over an alphabet $\Sigma$ of size $R$, given for preprocessing, and then query strings $p \in \Sigma^*$ of length $m$.

**Output.** For each query, the set $K_p = \{ s \in K : p \preceq s \}$, where $p \preceq s$ means that $s = pt$ for some $t \in \Sigma^*$. The usual form reports $K_p$ in lexicographic order. Let $k = \lvert K_p \rvert$.

The set $K$ is *static* if it does not change after preprocessing, and *dynamic* if keys can be inserted and deleted between queries.

## Variants

- **Counting.** Output only $k = \lvert K_p \rvert$. A trie with a count of keys in each subtree, or a sorted array with two binary searches, answers it without listing the keys.
- **Existence.** Decide whether $k > 0$. In a trie whose nodes are all on a path to a key, this is "does the node of $p$ exist".
- **Top $k$ completion.** Each key has a weight, and the output is the $k$ keys of $K_p$ of largest weight, as in search-box completion. A trie with the largest weight of each subtree stored at the node answers it with a priority walk.
- **Longest prefix.** The reverse question: given $s$, find the longest key that is a prefix of $s$. This is the [longest prefix match](/longest-prefix-match/) of IP routing.
- **Patterns with wildcards.** A pattern in which a dot matches any one symbol. See [wildcard matching in a trie](/wildcard-matching-in-trie/).
- **Prefixes of suffixes.** When $K$ is the set of all suffixes of a text $T$, the keys with prefix $p$ are the positions where $p$ occurs in $T$. This is the [substring query](/substring-queries/) problem, solved by the [suffix tree](/suffix-tree/) and [suffix array search](/suffix-array-search/).

## Examples

Let $K = \{\text{by}, \text{sea}, \text{sells}, \text{she}, \text{shells}, \text{shore}, \text{the}\}$, the keys of the example of the [trie](/trie/) page.

| query $p$ | $K_p$ in order | $k$ |
|---|---|---|
| sh | she, shells, shore | 3 |
| s | sea, sells, she, shells, shore | 5 |
| se | sea, sells | 2 |
| shells | shells | 1 |
| shellsx | none | 0 |
| x | none | 0 |
| (the empty string) | all 7 keys | 7 |

The key "shells" is in $K_p$ for $p$ = shells, because each string is a prefix of itself. In sorted order, the answer for "s" is the run from position 2 to position 6 of the sorted list of $K$, counting from 1.

## Known algorithms

| method | preprocessing | query time | space |
|---|---|---|---|
| scan all keys | none | $O(N)$, plus a sort of the output | the keys |
| sorted array and [binary search](/binary-search/) | sort, $O(N \log n)$ symbol comparisons | $O(m \log n + \text{output length})$ | the keys and $n$ pointers |
| R-way [trie](/trie/), walk then collect | $O(N R)$ | $O(m + tR)$, for $t$ nodes in the subtree of $p$ | $O(N R)$ |
| trie with hashed children | $O(N)$ expected | $O(m + t)$ expected | $O(N)$ |
| [ternary search tree](/ternary-search-tree/) | $O(N \log R)$ for balanced inner BSTs | $O(m \log R + t)$ | $O(N)$ |
| [radix tree](/radix-tree/) | $O(N)$ with hashed children | $O(m + k)$ nodes, plus the output length | $O(n)$ nodes |

Here $N$ is the total length of the keys. In the trie, $t \ge k$, and $t$ can be up to $k$ times the longest key length below $p$, because the trie has a node for each symbol. In the radix tree, the subtree of the node at $p$ has $k$ keys and fewer than $2k$ nodes, because each inner node has at least two children, so the walk is proportional to $k$. The output length is the total length of the reported strings, which is at least $k \cdot m$ when the keys are written out in full. Many systems report pointers to the keys instead, and then the cost is $O(m + k)$ for the radix tree.

**Sorted array.** By the interval property proved on the [string symbol table](/string-symbol-table/) page, $K_p$ is a contiguous run of the sorted keys. The first key of the run is the first key $\ge p$. The run ends before the first key that is greater than $p$ and does not start with $p$. Each end needs one binary search with string comparisons, and each comparison reads at most $m + 1$ symbols of the key, which gives $O(m \log n)$. With the LCP values of neighbouring keys, the search can be made $O(m + \log n)$, as in [suffix array search](/suffix-array-search/).

## Bounds

**Lower bound $\Omega(m + k)$.** An algorithm must read each symbol of $p$ in the worst case: for $K = \{p\}$, a symbol of $p$ that is not read can be changed so that the answer becomes empty while the run stays the same. It must also report each of the $k$ keys. So each method needs $\Omega(m + k)$ time when it reports pointers to the keys, and the radix tree with constant-time child access meets this bound.

**Comparison model.** If the keys can only be compared as whole strings with a three-way comparison, finding the start of the run among $n$ keys needs $\lceil \lg(n + 1) \rceil$ comparisons in the worst case, by the [sorted search lower bound](/sorted-search-lower-bound/).

**Dynamic sets.** With hashed children, a trie or a radix tree supports insert and delete in $O(\lvert s \rvert)$ expected time and keeps the query bounds above.

## Reductions

- **To a range query.** If $\Sigma$ is ordered and $p \ne \varepsilon$, then $K_p$ is the set of keys in the half-open interval $[p, p^+)$, where $p^+$ is $p$ with its last symbol replaced by the next larger symbol. If the last symbol is the largest symbol of $\Sigma$, drop it and repeat; if every symbol of $p$ is the largest, the interval has no upper end. So each [ordered symbol table](/ordered-symbol-table/) with a range query solves prefix matching with two searches.
- **From substring queries.** The occurrences of $p$ in a text $T$ are the suffixes of $T$ that have prefix $p$. So prefix matching on the $\lvert T \rvert$ suffixes solves the [substring query](/substring-queries/) problem. The [suffix trie](/suffix-trie/) and the [suffix tree](/suffix-tree/) are the trie and the radix tree of these suffixes.
- **Counting from listing.** A trie that stores the number of keys of each subtree at each node answers the counting variant in $O(m)$ time.

## Applications

- **Autocompletion.** Search boxes, shells and code editors complete a typed prefix from a dictionary of words, commands or names, often with the top $k$ variant.
- **Spelling and word games.** A word game solver stops a search branch as soon as the letters so far are the prefix of no word, which is the existence variant.
- **Databases.** A query `LIKE 'abc%'` in SQL is a prefix query on a string column, and a B-tree index answers it as a range query by the reduction above.
- **Routing tables and file systems.** Lookups by path or by address prefix use tries and radix trees, often in the longest prefix form.

## References
