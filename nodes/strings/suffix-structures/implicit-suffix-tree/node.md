---
tag: 9Q8BZR
kind: concept
slug: implicit-suffix-tree
name: Implicit suffix tree
aliases:
- implicit suffix trie
area: strings/suffix-structures
level: core
summary: A suffix tree without the sentinel, where some suffixes end inside internal edges.
prereqs: [suffix-tree, sentinel-character, suffix]
see_also: [ukkonen-algorithm, suffix-tree, sentinel-character, suffix-trie, suffix-link, mccreight-algorithm, count-distinct-substrings, suffix-tree-size-theorem]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 6.1 (Ukkonen's linear-time suffix tree algorithm), the definition of the implicit suffix tree and the phases and extensions that build it
  - paper: doi:10.1007/BF01206331
    title: Esko Ukkonen, On-line construction of suffix trees, Algorithmica 14(3), 1995
    locator: pages 249 to 260, the suffix trees of the prefixes of the text without an end marker and the open leaf edges
---

The implicit suffix tree of a string $T$ is the compacted trie of the [suffixes](/suffix/) of $T$ with no [sentinel](/sentinel-character/) appended. A suffix that also occurs earlier in $T$ is a prefix of a longer suffix, so it does not end at a leaf: it ends at an internal node or inside an edge. The implicit tree is what [Ukkonen's algorithm](/ukkonen-algorithm/) keeps for each prefix of the text, and one more step with a sentinel turns it into the true [suffix tree](/suffix-tree/).

## In plain words

A suffix tree stores all endings of a word in one tree, and normally each ending stops at its own leaf. That needs a special end mark at the end of the word. Without it, an ending such as "a" of "banana" is also the start of the longer ending "anana", so its path stops in the middle of the path of "anana" and gets no leaf.

The tree that you get in this way is the implicit suffix tree. It still holds every piece of the word as a path from the root, so it still answers "is this a piece of the word?". But you cannot see from the leaves where every ending is.

Ukkonen's algorithm reads a word one letter at a time and keeps this tree for the part read so far. At the end it adds the end mark, and every ending gets its leaf.

## The idea

Let $T = T[0 \ldots n-1]$ be a string over a general ordered alphabet, with 0-based positions, and $T_i = T[i \ldots n-1]$.

**Definition.** Gusfield defines the implicit suffix tree of $T$ from the suffix tree of $T\$$: remove every copy of $\$$ from the edge labels, then remove each edge whose label is now empty, then remove each node other than the root that has fewer than two children, and join its two edges into one. The result is the compacted trie of the set $\{T_0, \ldots, T_{n-1}\}$:

- the *leaves* are the suffixes that are not a proper prefix of another suffix;
- the *internal nodes* other than the root are the substrings $u \ne \varepsilon$ that are followed by two different symbols in $T$ (the end of $T$ does not count);
- every other substring of $T$ is a point inside an edge, an *implicit node*.

The word "implicit" is used in two ways. An *implicit node* is a point inside an edge, in any suffix tree. The *implicit suffix tree* is the tree in which some suffixes end at such points.

**Nested suffixes.** Call $T_i$ *nested* if it is a proper prefix of another suffix. That holds if and only if $T_i$ occurs in $T$ at a position $j \ne i$: an occurrence at $j$ of a string of length $n - i$ needs $j \le i$, so $j < i$ and $T_i$ is a prefix of $T_j$. If $T_i$ is nested, so is each shorter suffix, because its occurrence at $j$ contains an occurrence of each suffix of $T_i$ at another place. So the nested suffixes are exactly the suffixes of length at most $L$, where $L$ is the length of the longest suffix that occurs twice in $T$. Then:

- the implicit suffix tree has exactly $n - L$ leaves, for $n \ge 1$;
- it is a true suffix tree, with one leaf for each suffix, if and only if $L = 0$, that is, if and only if the last symbol of $T$ occurs nowhere else in $T$. A sentinel is a symbol with this property.

**Size.** At most $n$ leaves, and each internal node other than the root has at least two children, so there are fewer internal nodes than leaves, and $O(n)$ nodes and edges in all. With edge labels stored as two positions of $T$, it takes $O(n)$ words.

**Each point is one substring.** Each nonempty substring of $T$ is a prefix of a suffix, so it is one point of the tree, a node or a place inside an edge, and different points spell different strings. Since no $\$$ is in the labels, the sum of the edge lengths of the implicit suffix tree is the number of distinct nonempty substrings of $T$, the [count of distinct substrings](/count-distinct-substrings/).

**Online growth.** Let $I_i$ be the implicit suffix tree of the prefix $T[0 \ldots i]$. Ukkonen's algorithm turns $I_{i-1}$ into $I_i$ in amortized $O(1)$ time:

- a leaf stays a leaf: if $T[j \ldots i-1]$ occurs only at $j$, then $T[j \ldots i]$ also occurs only at $j$, so it is not nested either, and its leaf edge grows by $T[i]$. All leaf edges share one end index that grows with $i$, so they grow for free;
- the nested suffixes of $T[0 \ldots i-1]$ are extended by $T[i]$ from the longest to the shortest. The longest one is the *active point*. Extending a nested suffix either creates a new leaf (and maybe a new internal node), or finds that the extended string is already in the tree, and then all shorter ones are too, so the phase stops;
- the length $L$ grows by at most 1 per step: if a suffix of length $\ell$ of $T[0 \ldots i]$ occurs twice, then the suffix of length $\ell - 1$ of $T[0 \ldots i-1]$ occurs twice. This bounds the total work with [suffix links](/suffix-link/).

## Examples

| $T$ | $n$ | longest nested suffix | leaves of the implicit tree | internal nodes besides the root | suffix tree of $T\$$: internal nodes besides the root |
|---|---|---|---|---|---|
| `xabxa` | 5 | `xa`, $L = 2$ | 3 | none | `a`, `xa` |
| `banana` | 6 | `ana`, $L = 3$ | 3 | none | `a`, `ana`, `na` |
| `abab` | 4 | `ab`, $L = 2$ | 2 | none | `ab`, `b` |
| `aaaa` | 4 | `aaa`, $L = 3$ | 1 | none | `a`, `aa`, `aaa` |
| `mississippi` | 11 | `i`, $L = 1$ | 10 | `i`, `issi`, `p`, `s`, `si`, `ssi` | the same six |
| `abc` | 3 | none, $L = 0$ | 3 | none | none |

**`xabxa`.** This is the example of Gusfield. The implicit tree is the root with three leaf edges, `xabxa`, `abxa` and `bxa`. The suffix `xa` ends inside the edge `xabxa`, after 2 symbols, and the suffix `a` ends inside the edge `abxa`, after 1 symbol. With a sentinel, the suffix tree of `xabxa$` gets the nodes `a` and `xa`, and six leaves, one for each nonempty suffix of $T$ and one for the suffix `$`.

**`banana`.** The implicit tree has only three leaf edges, `banana`, `anana` and `nana`. The sum of their lengths is $6 + 5 + 4 = 15$, which is the number of distinct nonempty substrings of `banana`. In the suffix tree of `banana$`, the suffixes `a`, `ana` and `na` each get a leaf below a new internal node.

**`aaaa`.** All suffixes are on one path. The implicit tree is one edge `aaaa`, of length 4, and `aaaa` has 4 distinct nonempty substrings.

**`mississippi`.** Only the last symbol `i` occurs elsewhere, so only the suffix `i` is nested. It ends at the internal node `i`, which exists anyway because `i` is followed by `p`, `s` and `m`. The implicit tree has 10 leaves; the suffix tree of `mississippi$` adds a leaf `$` below the node `i` and a leaf for `$` below the root.

**Ukkonen on `xabxa`.** $I_0$ is one edge `x`. $I_1$ has the leaf edges `xa` and `a`, and $I_2$ has `xab`, `ab` and `b`. At $i = 3$ the leaf edges grow to `xabx`, `abx` and `bx`, and the new suffix `x` is already in the tree, inside the edge `xabx`, so nothing else changes: the active point is now at `x`. At $i = 4$ the leaves grow again, and the nested suffixes `xa` and `a` are already in the tree. A final phase with $\$$ makes the nodes `xa` and `a` explicit and adds their leaves.

## Where it is used

- **Ukkonen's algorithm.** The algorithm keeps $I_i$ for each prefix and so builds the suffix tree online, in $O(n)$ time for a constant alphabet. Because it never needs the end of the text, it can index a stream, and it can stop at any time with a valid tree of the prefix.
- **Pattern search.** Each substring of $T$ is a point of the implicit tree, so "does $P$ occur in $T$?" is answered by a walk from the root, and no sentinel is needed. Listing all occurrences needs the leaves, so it needs the sentinel or a list of the nested suffixes at their points.
- **Counting distinct substrings.** The sum of the edge lengths, as above.
- **Generalized trees.** In a [generalized suffix tree](/generalized-suffix-tree/) built string by string with Ukkonen's algorithm, each string is ended with a separator before the next string starts, so that the nested suffixes of one string get their leaves.
- **Teaching.** The implicit tree explains why a suffix tree needs an end marker: without it, the [suffix tree size theorem](/suffix-tree-size-theorem/) still holds, but not every suffix is a leaf. The same issue arises in the [suffix trie](/suffix-trie/), where a suffix without an end marker ends at an inner node.

## References
