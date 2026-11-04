---
tag: 7DAM2Y
kind: problem
slug: wildcard-matching-in-trie
name: Wildcard matching in a trie
aliases:
- Wildcard matches
area: data-structures/string-structures
level: core
summary: Problem of finding all trie keys that match a pattern in which a dot stands for any single character.
prereqs: [trie, prefix-matching]
see_also: [trie, ternary-search-tree, prefix-matching, string-symbol-table, kd-tree, backtracking-regex-matching, hamming-distance, approximate-string-matching]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.2 (Tries), the operation keysThatMatch and its collect method in TrieST and TST
  - paper: Ronald L. Rivest, Partial-match retrieval algorithms, SIAM Journal on Computing 5(1), 1976, doi:10.1137/0205003
    locator: pages 19 to 50, partial-match queries on tries and their average cost
  - paper: Richard Cole, Lee-Ad Gottlieb and Moshe Lewenstein, Dictionary matching and indexing with errors and don't cares, Proceedings of the 36th Annual ACM Symposium on Theory of Computing (STOC 2004), doi:10.1145/1007352.1007374
    locator: pages 91 to 100, the k-errata trie for patterns with a bounded number of don't care symbols
---

Wildcard matching in a trie is the problem of listing, for a set of keys stored in advance and a pattern $q$ over the alphabet plus a wildcard symbol ".", each key of the same length as $q$ that agrees with $q$ at every position where $q$ is not a wildcard. It is the `keys_that_match` query of the [string symbol table](/string-symbol-table/). A [trie](/trie/) answers it by a walk that follows one child for each fixed symbol and all children for each wildcard. The general form, where some positions are fixed and the others are free, is the partial-match query that Rivest analysed in 1976.

## In plain words

A crossword gives you a word with some letters known and some blank, say "s _ e". You want every word in the dictionary that fits. That is wildcard matching: the dot stands for any one letter, and the word must have exactly as many letters as the pattern.

In a tree of letters, a known letter tells you which branch to take. A blank tells you nothing, so you must try every branch at that level. The walk follows one branch for each known letter and fans out at each blank. A pattern with few blanks is fast. A pattern made only of blanks visits every word of that length.

## Definition

**Input.** A finite set $K \subseteq \Sigma^*$ of $n$ keys over an alphabet $\Sigma$ of size $R$, given for preprocessing. Then queries $q \in (\Sigma \cup \{.\})^m$, where the wildcard "." is not in $\Sigma$. Let $w$ be the number of wildcard positions of $q$.

**Output.** The set $K_q = \{ s \in K : \lvert s \rvert = m \text{ and } s[i] = q[i] \text{ for each } i \text{ with } q[i] \ne . \}$, usually in lexicographic order. Let $k = \lvert K_q \rvert$.

When all keys have the same length $m$, a key is a point of $\Sigma^m$, and a query with $m - w$ fixed positions asks for the points in an axis-parallel subspace. This is the *partial-match query* of multidimensional searching, with $m$ dimensions.

## Variants

- **Prefix form.** The key must match $q$ only on its first $m$ symbols and may be longer. With $q = p \cdot$ (no wildcards), this is [prefix matching](/prefix-matching/).
- **Variable-length wildcard.** A symbol "\*" matches any string, including the empty one, as in file name globbing. A trie walk handles it by trying, at each node, both to consume nothing and to descend one level. This is a special case of matching a [regular expression](/backtracking-regex-matching/) against the set of keys.
- **Character classes.** A position may allow a set of symbols, such as "[aeiou]". The walk follows the children whose symbols are in the set.
- **Mismatches.** Find the keys within [Hamming distance](/hamming-distance/) $d$ of $q$. The walk keeps a count of mismatches so far and stops a branch when the count exceeds $d$. Allowing insertions and deletions gives [approximate string matching](/approximate-string-matching/) on a dictionary.
- **Wildcards in the text.** In pattern matching with don't cares, the wildcards are in a long text and the pattern is searched in it, which is a different problem, solved with convolutions.

## Examples

Let $K = \{\text{by}, \text{sea}, \text{sells}, \text{she}, \text{shells}, \text{shore}, \text{the}\}$, the keys of the example of the [trie](/trie/) page.

| pattern $q$ | $K_q$ in order | $k$ |
|---|---|---|
| .he | she, the | 2 |
| s.. | sea, she | 2 |
| s.e | she | 1 |
| sh... | shore | 1 |
| ..... | sells, shore | 2 |
| .. | by | 1 |
| ...... | shells | 1 |
| . | none | 0 |
| s.e.. | none | 0 |

For ".he", the trie walk with children stored as a map visits the root, its three children b, s and t (the wildcard), then only the nodes sh and th (the child h of b does not exist), then she and the. That is 8 of the 20 nodes, and both end nodes carry a value. Note that "shells" does not match "sh..." because the lengths differ, while it would match in the prefix form.

## Known algorithms

| method | preprocessing | query cost | space |
|---|---|---|---|
| scan all keys | none | $O(N)$ | the keys |
| R-way [trie](/trie/), branch on each wildcard | $O(N R)$ | the number of nodes at depth at most $m$ that match $q$ so far, times $R$ for array nodes | $O(N R)$ |
| trie with map children | $O(N)$ expected | the number of matching nodes at depth at most $m$ | $O(N)$ |
| [ternary search tree](/ternary-search-tree/) | $O(N)$ insertions | as for the trie, plus a whole sibling tree at each wildcard | $O(N)$ |
| one hash table per length, enumerate fills | $O(N)$ | $R^w$ lookups | $O(N)$ |
| k-errata trie of Cole, Gottlieb and Lewenstein | built for a fixed bound on $w$ | $m$ plus a term polylogarithmic in $n$ whose exponent grows with $w$, plus $k$ | $O(n \log^w n)$ up to factors that depend on $w$ |

Here $N$ is the total length of the keys.

**The trie walk.** Keep a stack of pairs (node, depth $d$), starting with the root at depth 0. At a node at depth $d < m$, if $q[d]$ is a symbol, push its child for $q[d]$ if it exists; if $q[d]$ is the wildcard, push all children. At depth $m$, report the node if it has a value. Every node that the walk visits is the node of a string that matches the first $d$ positions of $q$, so the walk is output sensitive in the number of such partial matches, not only in $k$. Pushing the children in reverse order of their symbols reports the keys in lexicographic order. The [trie](/trie/) page gives the code of this walk.

**Pruning by length.** A walk can stop a branch at once if no key below it has length $m$, when each node stores the set (or the minimum and maximum) of key lengths below it.

**Enumerating fills.** If $w$ is small and $R$ is small, try all $R^w$ ways to fill the wildcards and look up each string in a [hash table](/hash-table/). This is fast for one wildcard over 26 letters and hopeless for many.

## Bounds

**Worst case of the trie walk.** For the pattern of $m$ wildcards, every node at depth at most $m$ matches, so the walk visits them all, while the output may be empty if no key has length exactly $m$. Pruning by length removes this example, but not others: for keys that agree on many prefixes of fixed positions and differ later, the walk can visit many nodes that lead to no answer.

**Average case.** Rivest (1976) studied partial-match queries on random keys of $m$ bits with $m - w$ fixed positions, and showed that tries answer them in about $n^{w/m}$ steps on average, up to lower order terms.

**With few wildcards.** Data structures that bound $w$ in advance, such as the k-errata trie, answer queries in time $m$ plus a polylogarithmic term plus $k$ for each fixed $w$, at the cost of space that grows like $n \log^w n$. When $w$ is not bounded, the problem is a partial-match query in many dimensions, and the known structures trade space against query time.

**Lower bound $\Omega(m + k)$.** As for [prefix matching](/prefix-matching/), each fixed symbol of $q$ must be read and each answer reported.

## Reductions

- **From prefix matching.** A pattern without wildcards, in the prefix form, is a prefix query, so the trie walk generalizes the walk of [prefix matching](/prefix-matching/).
- **To multidimensional searching.** Keys of length $m$ are points in $m$ dimensions with coordinates in $\Sigma$, and a wildcard query is an orthogonal range query whose ranges are a single value or the whole axis. So a [k-d tree](/kd-tree/) built on these points also answers it.
- **To regular expression matching on a set.** The pattern is the regular expression in which each dot is the class $\Sigma$. Running its automaton along the trie, one state set for each node, answers any regular expression query on the keys, with the wildcard query as the case of a single path automaton.

## Applications

- **Word games and crosswords.** A solver lists the dictionary words that fit a partly filled slot.
- **Spelling suggestions.** A misspelled word with one doubtful letter is looked up with a wildcard in that position, or with the mismatch variant.
- **Database queries.** `LIKE 's_e'` in SQL uses "_" for one character, and an index on the column can answer it with a trie or B-tree walk on the fixed prefix followed by a filter.
- **File name patterns.** Shell patterns such as `?` for one character and `*` for any string are the variable-length variant.

## References
