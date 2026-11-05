---
tag: 595W2Q
kind: concept
slug: dictionary-suffix-link
name: Dictionary suffix link
aliases:
- output link
- dictionary link
- exit link
area: strings/multiple-pattern-matching
level: advanced
summary: Link to the nearest suffix node that marks a pattern end, letting Aho-Corasick report all matches at a position.
prereqs: [aho-corasick, failure-link, trie]
see_also: [output-sensitive-matching, dictionary-matching, multiple-string-matching, suffix-link, knuth-morris-pratt, prefix-function]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 3.4, Exact matching with a set of patterns (the subsection on output links, their linear-time computation, and the full Aho-Corasick search)
  - paper: doi:10.1145/360825.360855
    title: Alfred V. Aho and Margaret J. Corasick, Efficient string matching, an aid to bibliographic search, Communications of the ACM 18(6) (1975), 333-340
    locator: Algorithm 3 (the output function is extended by the output of the failure state, the method that dictionary links replace)
  - url: https://cp-algorithms.com/string/aho_corasick.html
    title: cp-algorithms, Aho-Corasick algorithm
    locator: Applications, Find all strings from a given set in a text (the nearest output vertex reachable by suffix links, called the exit link)
---

A dictionary suffix link is a pointer stored at each node $v$ of the [Aho-Corasick](/aho-corasick/) trie: it leads to the node of the longest proper suffix of $\mathrm{str}(v)$ that is a whole pattern, or to nil if there is none. Following these links from the current node visits exactly the patterns that end at the current text position, longest first, and skips the nodes of the [failure link](/failure-link/) chain that are not patterns. So reporting costs $O(1)$ plus $O(1)$ per occurrence, which makes the search [output-sensitive](/output-sensitive-matching/), with only one extra pointer per node.

## In plain words

Aho-Corasick walks through the text with a finger on a tree of the patterns. At each step, the finger sits on the longest piece of the text, ending here, that begins some pattern. Every pattern that ends here is a tail of that piece.

The failure links already lead from a piece to its shorter tails, one by one. But most tails are not whole patterns, and walking past all of them wastes time when nothing is found. A dictionary suffix link jumps straight to the next tail that is a whole pattern. Following these jumps lists every pattern that ends here and stops at once when there are no more.

## The idea

**Notation.** The trie of the patterns $P_0, \ldots, P_{k-1}$ has a node for each prefix of a pattern; $\mathrm{str}(v)$ is the string of node $v$, and the root spells the empty string. A node is a *pattern node* if $\mathrm{str}(v)$ equals some $P_j$. The failure link $\mathrm{fail}[v]$ is the node of the longest proper suffix of $\mathrm{str}(v)$ that is a node. Indices of text positions are 0-based.

**Definition.** For a node $v \ne \mathrm{root}$,

$$\mathrm{dict}[v] = \text{the node of the longest proper suffix of } \mathrm{str}(v) \text{ that is a pattern node, or nil.}$$

The root has $\mathrm{dict}[\mathrm{root}] = \mathrm{nil}$, since the empty string has no proper suffix. (If the empty string is a pattern, it is reported separately, at every position.)

**The recurrence.** For $v \ne \mathrm{root}$ with $f = \mathrm{fail}[v]$:

$$\mathrm{dict}[v] = \begin{cases} f & \text{if } f \text{ is a pattern node and } f \ne \mathrm{root}, \\ \mathrm{dict}[f] & \text{otherwise.} \end{cases}$$

*Why it holds.* Every proper suffix of $\mathrm{str}(v)$ that is a pattern is a node, so it is a suffix of $\mathrm{str}(f)$, the longest proper suffix that is a node. So the longest such pattern is either $\mathrm{str}(f)$ itself, if it is a pattern, or the longest proper suffix of $\mathrm{str}(f)$ that is a pattern, which is $\mathrm{dict}[f]$. Since $|\mathrm{str}(f)| < |\mathrm{str}(v)|$, the links can be computed in breadth-first order of the trie, right after the failure links, in $O(1)$ time per node.

**The chain lists all pattern suffixes.** By induction on the length of $\mathrm{str}(v)$, the chain $v' = \mathrm{dict}[v], \mathrm{dict}[v'], \ldots$ visits every proper suffix of $\mathrm{str}(v)$ that is a pattern, each once, in order of decreasing length. The first element is the longest by definition, and the rest of the chain lists the pattern suffixes of $\mathrm{str}(v')$, which are exactly the pattern suffixes of $\mathrm{str}(v)$ shorter than $\mathrm{str}(v')$.

**Reporting.** During the search, after reading $T[0 \ldots i]$, the current node $v$ spells the longest suffix of $T[0 \ldots i]$ that is a node. A pattern that ends at position $i$ is a suffix of $T[0 \ldots i]$ and a node, so it is a suffix of $\mathrm{str}(v)$. So the patterns ending at $i$ are $\mathrm{str}(v)$, if $v$ is a pattern node, followed by the chain from $\mathrm{dict}[v]$:

```
w ← v if v is a pattern node, else dict[v]
while w ≠ nil: report every pattern index of w; w ← dict[w]
```

Each node visited reports at least one occurrence, so the cost at position $i$ is $O(1 + z_i)$ for $z_i$ occurrences ending there, and $O(n + z)$ over the text.

**What it replaces.**

- *Walking the failure chain.* Testing every node of the chain $v, \mathrm{fail}[v], \ldots, \mathrm{root}$ for patterns gives the same output, but costs the depth of $v$ at each position even when nothing is reported. With the patterns $a^{L-1} b$ and b and the text $a^n$, no pattern occurs, yet the chain at most positions has $L - 1$ nodes, so the cost is $\Theta(nL)$.
- *Merged output sets.* The original algorithm of Aho and Corasick stores at each node the set of all patterns that are suffixes of $\mathrm{str}(v)$, built by copying the set of $\mathrm{fail}[v]$. Reporting is then direct, but the sets repeat each other. Their total size can reach $\Theta(m^{3/2})$ for patterns of total length $m$, while the dictionary links take one pointer per node. The size of each set is at most $\sqrt{2m}$, because the patterns on one chain have distinct lengths whose sum is at most $m$.

## Examples

The patterns $P_0, \ldots, P_6$ are a, ab, bab, bc, bca, c, caa. Their trie has 11 nodes. The table lists each node except the root, its failure link and its dictionary suffix link; a star marks the pattern nodes.

| node | a* | b | c* | ab* | ba | bc* | ca | bab* | bca* | caa* |
|---|---|---|---|---|---|---|---|---|---|---|
| fail | root | root | root | b | a | c | a | ab | ca | a |
| dict | nil | nil | nil | nil | a | c | a | ab | a | a |

The node bca shows the jump: its failure link goes to ca, which is not a pattern, and its dictionary link goes past ca to a. The node ab has failure link b, which is not a pattern and has no pattern suffix, so its dictionary link is nil.

Search the text bcabab. The table shows the node after each character, the nodes that reporting visits, and, for comparison, the failure chain.

| $i$ | $T[i]$ | node $v$ | visited by reporting | failure chain of $v$ |
|---|---|---|---|---|
| 0 | b | b | none | b |
| 1 | c | bc | bc, c | bc, c |
| 2 | a | bca | bca, a | bca, ca, a |
| 3 | b | ab | ab | ab, b |
| 4 | a | ba | a | ba, a |
| 5 | b | bab | bab, ab | bab, ab, b |

The output is the eight occurrences $(s, j)$: (0, 3) bc, (1, 5) c, (0, 4) bca, (2, 0) a, (2, 1) ab, (4, 0) a, (3, 2) bab and (4, 1) ab. Reporting visits 9 nodes, each with at least one pattern; the failure chains have 13 nodes, 4 of them with nothing to report. At $i = 4$, the node ba is not a pattern, and reporting starts at its dictionary link a.

**The bad case for failure chains.** With the patterns aaab and b ($L = 4$) and the text $a^{100}$, there are no occurrences. Reporting by dictionary links visits no node at all, while walking the failure chains visits 297 nodes; with $L = 8$ and $L = 16$, the counts are 679 and 1395, close to $(L - 1) \cdot 100$.

## Where it is used

- **Aho-Corasick search.** The dictionary links are the standard way to report all occurrences in $O(n + m + z)$ time with $O(m)$ space; see [Aho-Corasick](/aho-corasick/) and [output-sensitive matching](/output-sensitive-matching/).
- **Counting without listing.** Store at each node $c[v] = |\mathrm{out}[v]| + c[\mathrm{dict}[v]]$, the number of patterns that are suffixes of $\mathrm{str}(v)$. Then the number of occurrences ending at each position is one lookup, and the total count takes $O(n)$ time after the build, even when $z$ is large.
- **The longest match.** The longest pattern ending at a position is $\mathrm{str}(v)$ if $v$ is a pattern node and $\mathrm{dict}[v]$ otherwise, in $O(1)$ time; tokenizers and the longest-match variant of [dictionary matching](/dictionary-matching/) use this.
- **Dynamic programming over a text.** Problems such as "split the text into dictionary words" or "count the ways to cover the text" need, at each end position, the list of patterns ending there; the dictionary chain gives exactly that list.
- **Two-dimensional matching.** Row matching in the [Bird-Baker](/bird-baker/) method needs, at each position, the pattern row that ends there; with distinct rows of equal length, one lookup suffices.

## References
