---
tag: J46GT5
kind: abstract-type
slug: string-symbol-table
name: String symbol table
area: data-structures/string-structures
level: intro
summary: Symbol table interface specialized for string keys, adding operations such as prefix search, longest prefix and wildcard matching.
prereqs: [dictionary, alphabet]
see_also: [trie, ternary-search-tree, hybrid-tst, radix-tree, prefix-matching, wildcard-matching-in-trie, longest-prefix-match, ordered-symbol-table]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.2 (Tries), the API StringST, the character-based operations, and the table of costs of string symbol table implementations
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.3 (Digital searching)
  - paper: Jon L. Bentley and Robert Sedgewick, Fast algorithms for sorting and searching strings, Proceedings of the 8th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1997)
    locator: pages 360 to 369, the operations of ternary search trees (search, near-neighbor and partial-match search)
---

A string symbol table is an abstract data type: a finite map from strings over an [alphabet](/alphabet/) to values, with the [dictionary](/dictionary/) operations put, get and delete, and three queries that use the symbols of the keys: all keys with a given prefix, the longest key that is a prefix of a given string, and all keys that match a pattern with wildcards. Sedgewick and Wayne define it as the API StringST. The [trie](/trie/), the [ternary search tree](/ternary-search-tree/) and the [radix tree](/radix-tree/) implement it with costs that depend on the length of the key and not on the number of keys.

## In plain words

A phone keeps your contacts. You type "Jo" and it shows "Joan", "John" and "Jordan". A router gets an address and must find the longest rule whose start matches that address. A crossword helper gets "c.t" and lists "cat", "cot" and "cut".

Each of these is a table of words with some data for each word. You can add a word, look it up and remove it. You can also ask questions about the letters of the words: which words start with these letters, which stored word is the longest start of this text, and which words fit this pattern with blanks. A string symbol table is the name for a table that can do all of this. It says what the answers are, not how to find them.

## Operations

Let $\Sigma$ be a finite alphabet of size $R$, and $\Sigma^*$ the set of finite strings over it. For strings $p$ and $s$, write $p \preceq s$ when $p$ is a prefix of $s$, that is, $s = p t$ for some $t \in \Sigma^*$. A string symbol table value $T$ is a finite partial function from $\Sigma^*$ to a set of values $V$. We write $\operatorname{keys}(T)$ for its domain and $T(s)$ for the value of a key $s$.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to T$ | the empty table |
| `put` | $\text{put}(T, s, v) \to T$ | $s$ maps to $v$; the old value of $s$, if any, is lost |
| `get` | $\text{get}(T, s) \to V \cup \{\bot\}$ | $T(s)$ if $s \in \operatorname{keys}(T)$, else $\bot$ (no value) |
| `delete` | $\text{delete}(T, s) \to T$ | removes $s$ from $\operatorname{keys}(T)$; no change if $s$ is not a key |
| `contains` | $\text{contains}(T, s) \to \text{bool}$ | true when $s \in \operatorname{keys}(T)$ |
| `size` | $\text{size}(T) \to \mathbb{N}$ | $\lvert \operatorname{keys}(T) \rvert$ |
| `keys` | $\text{keys}(T) \to$ list | all keys in lexicographic order |
| `keys_with_prefix` | $\text{keys\_with\_prefix}(T, p) \to$ list | the keys $s$ with $p \preceq s$, in lexicographic order |
| `longest_prefix_of` | $\text{longest\_prefix\_of}(T, s) \to \Sigma^* \cup \{\bot\}$ | the longest key $k$ with $k \preceq s$, or $\bot$ if there is none |
| `keys_that_match` | $\text{keys\_that\_match}(T, q) \to$ list | for $q$ over $\Sigma \cup \{\texttt{.}\}$: the keys of length $\lvert q \rvert$ equal to $q$ at each position where $q$ is not a dot, in lexicographic order |

The order on keys is the lexicographic order of $\Sigma^*$ from a fixed order of $\Sigma$, with a proper prefix before each of its extensions. The pages [prefix matching](/prefix-matching/) and [wildcard matching in a trie](/wildcard-matching-in-trie/) treat the two list queries as problems, and the [longest prefix match](/longest-prefix-match/) page treats the third.

**Ordered operations.** Since the keys have an order, a string symbol table can also offer the operations of an [ordered symbol table](/ordered-symbol-table/): minimum, maximum, floor, ceiling, rank and select. The trie gets them from a walk in symbol order. Sedgewick and Wayne leave them as exercises for tries.

### Example

Start with the empty table over the lowercase letters. The table is shown as a sorted list of pairs.

| step | operation | result | table after |
|---|---|---|---|
| 1 | put(she, 0) | | she:0 |
| 2 | put(sells, 1) | | sells:1, she:0 |
| 3 | put(sea, 2) | | sea:2, sells:1, she:0 |
| 4 | put(shells, 3) | | sea:2, sells:1, she:0, shells:3 |
| 5 | put(sea, 6) | | sea:6, sells:1, she:0, shells:3 |
| 6 | keys_with_prefix(sh) | she, shells | unchanged |
| 7 | longest_prefix_of(shellfish) | she | unchanged |
| 8 | keys_that_match(s.e) | she | unchanged |
| 9 | get(shell) | $\bot$ | unchanged |
| 10 | delete(she) | | sea:6, sells:1, shells:3 |
| 11 | longest_prefix_of(shellfish) | $\bot$ | unchanged |
| 12 | size | 3 | unchanged |

At step 7 the keys "she" and "shells" both start like "shellfish", but only "she" is a prefix of it. At step 11 no key is a prefix of "shellfish", although "shells" shares five letters with it.

## Laws

For each table $T$, strings $s, s', p, q$ with $s \ne s'$, and values $v, v'$:

$$\begin{aligned}
&(\text{S1})\quad \text{get}(\text{new}(), s) = \bot, \qquad \text{get}(\text{put}(T, s, v), s) = v, \qquad \text{get}(\text{put}(T, s', v), s) = \text{get}(T, s),\\
&(\text{S2})\quad \text{get}(\text{delete}(T, s), s) = \bot, \qquad \text{get}(\text{delete}(T, s'), s) = \text{get}(T, s),\\
&(\text{S3})\quad \text{put}(\text{put}(T, s, v), s, v') = \text{put}(T, s, v'), \qquad \text{contains}(T, s) \iff \text{get}(T, s) \ne \bot,\\
&(\text{S4})\quad \text{size}(\text{new}()) = 0, \qquad \text{size}(\text{put}(T, s, v)) = \text{size}(T) + [\,\neg\,\text{contains}(T, s)\,],\\
&(\text{S5})\quad \text{set}(\text{keys\_with\_prefix}(T, p)) = \{ s \in \operatorname{keys}(T) : p \preceq s \}, \qquad \text{keys}(T) = \text{keys\_with\_prefix}(T, \varepsilon),\\
&(\text{S6})\quad \text{longest\_prefix\_of}(T, s) = k \ne \bot \iff k \in \operatorname{keys}(T),\ k \preceq s,\ \text{and no key } k' \text{ has } k \prec k' \preceq s,\\
&(\text{S7})\quad \text{set}(\text{keys\_that\_match}(T, q)) = \{ s \in \operatorname{keys}(T) : \lvert s \rvert = \lvert q \rvert,\ \forall i\ (q[i] = \texttt{.} \lor q[i] = s[i]) \}.
\end{aligned}$$

Here $[\cdot]$ is 1 when the condition is true and 0 when it is false, $\text{set}(L)$ is the set of the items of a list $L$, and each list query returns its items in lexicographic order without repeats. Laws (S1) to (S4) are the laws of a [dictionary](/dictionary/): they fix the answer of get after each sequence of put and delete, so two implementations that meet them agree on each get. Laws (S5) to (S7) define the three string queries by the set of keys alone. So the answer of a string query depends only on $\operatorname{keys}(T)$, and not on the order of the puts.

**The prefix ranges are intervals.** In lexicographic order, the keys with prefix $p$ form a contiguous run of $\text{keys}(T)$. *Proof.* Let $a \le b \le c$ be keys with $p \preceq a$ and $p \preceq c$. If $p \not\preceq b$, let $i$ be the first position with $i \ge \lvert b \rvert$ or $b[i] \ne p[i]$, so $i < \lvert p \rvert$. If $i = \lvert b \rvert$, then $b$ is a proper prefix of $p$ and so of $a$, which gives $b < a$, a contradiction. Else $b[i] \ne p[i] = a[i] = c[i]$ and the first $i$ symbols agree, so $b[i] > a[i]$ by $a \le b$, and $b[i] < c[i]$ by $b \le c$, which is impossible since $a[i] = c[i]$. $\square$ This is why a sorted array or a search tree with string keys can answer `keys_with_prefix` with two searches for the ends of the run.

## Implementations

Let $n$ be the number of keys, $m$ the length of the query string, $N$ the total length of the keys, and $k$ the number of keys in the output. The costs count symbol operations in the [word RAM](/word-ram/). A comparison of two strings costs up to the length of their common prefix plus one.

| implementation | get, put | delete | keys_with_prefix | longest_prefix_of | space |
|---|---|---|---|---|---|
| unordered list ([sequential search](/sequential-search-symbol-table/)) | $O(nm)$ | $O(nm)$ | $O(N)$ plus a sort of the output | $O(N)$ | $\Theta(N)$ |
| sorted array ([binary search](/binary-search-symbol-table/)) | get $O(m \log n)$, put $O(m \log n + n)$ | $O(m \log n + n)$ | $O(m \log n + \text{output length})$ | $O(m^2 \log n)$ with one search for each prefix | $\Theta(N)$ |
| [balanced search tree](/balanced-binary-search-tree/) | $O(m \log n)$ | $O(m \log n)$ | $O(m \log n + \text{output length})$ | $O(m^2 \log n)$ | $\Theta(N)$ |
| [hash table](/hash-table/) | $O(m)$ expected | $O(m)$ expected | $O(N)$, the keys are not in order | $O(m^2)$ expected, one lookup for each prefix | $\Theta(N)$ |
| R-way [trie](/trie/) | $O(m)$, plus $O(R)$ for each new node | $O(m + R)$ | $O(m + tR)$ for a subtree of $t$ nodes | $O(m)$ | $O(R N)$ |
| [ternary search tree](/ternary-search-tree/) | $O(m \log R)$ if the BSTs of the TST are balanced | $O(m \log R)$ | $O(m \log R + t)$ | $O(m \log R)$ | $\Theta(N)$ |
| [radix tree](/radix-tree/) | $O(m)$ with array children | $O(m)$ | $O(m + k \cdot \text{key length})$ | $O(m)$ | $O(n)$ nodes plus the keys |

The trie-like structures read each symbol of the query a bounded number of times, so their search cost does not grow with $n$. The comparison-based structures pay a factor $\log n$ for the number of string comparisons, and their bound $O(m \log n)$ is often loose, since most comparisons stop at the first few symbols. The [hybrid TST](/hybrid-tst/), the [double-array trie](/double-array-trie/), the [burst trie](/burst-trie/), the [HAT-trie](/hat-trie/) and the [adaptive radix tree](/adaptive-radix-tree/) are tuned versions that cut the space or the cache misses. For `keys_that_match`, each trie walks only the branches that the pattern allows; the cost is studied on the [wildcard matching](/wildcard-matching-in-trie/) page.

## Lower bounds

**Reading the query.** Each implementation must read all $m$ symbols of a query $s$ in the worst case for a search hit. *Proof.* Let $T$ hold the single key $s$, and suppose that get never reads position $i$ of the query. Change $s[i]$ to another symbol (the alphabet has $R \ge 2$ symbols) to get $s'$. The run on $s'$ reads the same symbols and the same table, so it gives the same answer, but $s'$ is not a key. $\square$ So the cost $\Theta(m)$ of a trie search hit is optimal.

**Output.** Each list query must write its output, so `keys_with_prefix` costs $\Omega(\text{output length})$ when the keys are written out, or $\Omega(k)$ when the structure reports pointers to the keys.

**Comparisons.** If the only access to keys is a three-way comparison of two whole strings, then a search among $n$ keys needs $\lceil \lg(n + 1) \rceil$ comparisons in the worst case, as for a search in a sorted array (see the [sorted search lower bound](/sorted-search-lower-bound/)). Tries avoid this bound because they branch on single symbols, not on whole-key comparisons.

## References
