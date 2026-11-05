---
tag: 6DMXQ2
kind: data-structure
slug: palindromic-tree
name: Palindromic tree (eertree)
aliases:
- eertree
- palindrome tree
area: strings/palindromes
level: advanced
summary: Online structure with one node per distinct palindromic substring, built in linear time.
model: comparison-model
complexity:
  vars: {n: the length of the text, k: the number of distinct symbols in the text}
  time: {worst: O(n log k)}
  space: {extra: Θ(n)}
prereqs: [palindrome, palindrome-count-bound, trie]
see_also: [series-links, count-palindromic-substrings, minimum-palindrome-partition, rich-string, manacher, suffix-tree, suffix-automaton, palindrome-substring-queries]
sources:
  - paper: doi:10.1016/j.ejc.2017.07.021
    title: Mikhail Rubinchik and Arseny M. Shur, EERTREE, an efficient data structure for processing palindromes in strings, European Journal of Combinatorics 68 (2018), 249-265
    locator: the definition of the eertree (two roots, edges, suffix links), the online construction and its linear bound, and the applications to counting palindromes and to palindromic factorization
  - paper: arxiv:1506.04862
    title: Mikhail Rubinchik and Arseny M. Shur, EERTREE, an efficient data structure for processing palindromes in strings, arXiv preprint (2015)
    locator: the same results as the journal version, with the construction algorithm and its analysis
  - paper: doi:10.1016/j.ipl.2010.07.018
    title: Richard Groult, Élise Prieur and Gwénaël Richomme, Counting distinct palindromes in a word in linear time, Information Processing Letters 110(20) (2010), 908-912
    locator: the main algorithm, an earlier linear-time count of the distinct palindromes by other means
  - paper: doi:10.1016/j.jda.2014.08.001
    title: Gabriele Fici, Travis Gagie, Juha Kärkkäinen and Dominik Kempa, A subquadratic algorithm for minimum palindromic factorization, Journal of Discrete Algorithms 28 (2014), 41-48
    locator: the structure of the palindromic suffixes of a prefix (arithmetic progressions), used with the eertree for factorization
---

The palindromic tree, or eertree, stores every distinct [palindrome](/palindrome/) of a text, one node each, with two roots: one for the empty string and one imaginary root of length $-1$. An edge labeled $c$ goes from the node of $p$ to the node of $c\,p\,c$, and a suffix link goes from each node to the node of its longest proper palindromic suffix. A text of length $n$ has at most $n$ distinct nonempty palindromes, by the [palindrome count bound](/palindrome-count-bound/), so the tree has at most $n + 2$ nodes. Rubinchik and Shur build it online, one symbol at a time, in $O(n \log k)$ time for $k$ distinct symbols, and $O(n)$ time for a constant alphabet.

## In plain words

Keep a list of all different palindromes in the text read so far. When a new letter comes, at most one new palindrome appears: the longest one that ends at the new letter. To find it, take the longest palindrome that ended at the old last letter and check whether the letter just before it equals the new letter. If yes, wrap that palindrome in two copies of the new letter. If no, try the next shorter palindrome that ends there, and so on. Each palindrome points to its longest shorter palindrome at the end, so these tries are quick. Over the whole text, the number of tries is at most about twice the length.

## The abstract type

The structure holds a text $t = t[0..i-1]$, with 0-based indices, over an alphabet whose symbols are tested for equality and used as keys in a dictionary. Odd and even palindromes are both stored. The operations are:

- **ADD$(c)$.** Append the symbol $c$ to the text. Report whether the text now has a new distinct palindrome; if so, it is the longest palindromic suffix.
- **LAST.** The node of the longest palindromic suffix of the text.
- **Queries on nodes.** The length of a node, its suffix link, its child by a symbol, and the position where its palindrome first ends.

From these, the structure gives the number of distinct palindromes, the number of palindromes that end at each position, and the number of occurrences of each palindrome.

## Representation

- **Node 0, the imaginary root.** Length $-1$, suffix link to itself. Its child by $c$ is the one-symbol palindrome $c$, because "wrapping" a string of length $-1$ in $c$ and $c$ gives length 1.
- **Node 1, the empty root.** Length 0, suffix link to node 0. Its child by $c$ is $c\,c$.
- **Other nodes.** One per distinct nonempty palindrome $p$, with $\mathrm{len}[v] = |p|$, $\mathrm{link}[v]$ the node of the longest proper palindromic suffix of $p$ (node 1 if there is none), a dictionary $\mathrm{to}[v]$ of children, and the position $\mathrm{end}[v]$ where $p$ first ends, which gives $p$ as $t[\mathrm{end}[v] - \mathrm{len}[v] + 1 .. \mathrm{end}[v]]$.
- **Extra fields.** $\mathrm{depth}[v]$, the number of nonempty palindromic suffixes of $p$, and a counter of the positions whose longest palindromic suffix is $v$.

Node $v$ *fits* at position $i$ for the symbol $c$ if $j = i - \mathrm{len}[v] - 1 \ge 0$ and $t[j] = c$, that is, if $c\,p\,c$ ends at $i$. Node 0 always fits, since $j = i$.

## Operations

```pseudo id=main
ADD(c)                                   ▷ append c; i is its position
L1  append c to t, i ← |t| − 1, v ← last
L2  while v does not fit at i for c do v ← link[v]
L3  if to[v] has c then last ← to[v][c], return false
L4  w ← new node, len[w] ← len[v] + 2, end[w] ← i
L5  if len[w] = 1 then link[w] ← 1
L6  else u ← link[v]
L7      while u does not fit at i for c do u ← link[u]
L8      link[w] ← to[u][c]
L9  depth[w] ← depth[link[w]] + 1, to[v][c] ← w, last ← w, return true
```

Lines L1 and L2 walk down the suffix-link chain of $\mathrm{last}$, the palindromic suffixes of $t[0..i-1]$ from the longest, until one is preceded by $c$. Line L3 handles an old palindrome. Lines L4 to L8 make a new node and find its suffix link by a second walk, which starts one step below $v$ and stops at the next suffix that fits.

**Derived queries.**

- **Distinct count.** The number of nodes minus 2.
- **Palindromes that end at $i$.** After ADD of $t[i]$, $\mathrm{depth}[\mathrm{last}]$. The sum over $i$ is the number of palindromic occurrences, as on the [counting](/count-palindromic-substrings/) page.
- **Occurrences of each palindrome.** Each position counts for its longest palindromic suffix; then, for the nodes from the newest to the oldest, add the count of $v$ to the count of $\mathrm{link}[v]$. A suffix link points to a node made earlier, so one backward pass is enough.

## Example

Build the tree of `eertree`. The table lists, for each position $i$, the node $v$ where line L2 stops, the number of suffix links it follows, and the result.

| $i$ | $c$ | $v$ at L2 (length) | links followed | new node | its suffix link | $\mathrm{depth}$ |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | e | imaginary ($-1$) | 1 | `e` | empty | 1 |
| 1 | e | empty (0) | 1 | `ee` | `e` | 2 |
| 2 | r | imaginary ($-1$) | 3 | `r` | empty | 1 |
| 3 | t | imaginary ($-1$) | 2 | `t` | empty | 1 |
| 4 | r | `t` (1) | 0 | `rtr` | `r` | 2 |
| 5 | e | `rtr` (3) | 0 | `ertre` | `e` | 2 |
| 6 | e | `ertre` (5) | 0 | `eertree` | `ee` | 3 |

Every position adds a node, so `eertree` has 7 distinct nonempty palindromes, the most possible for length 7: it is a [rich string](/rich-string/). At $i = 2$ the walk goes `ee`, `e`, empty, imaginary, because no palindromic suffix of `ee` is preceded by `r`. The sum of the depths, $1 + 2 + 1 + 1 + 2 + 2 + 3 = 12$, is the number of palindromic occurrences, and the backward pass gives 4 occurrences of `e`, 2 of `ee`, 2 of `r`, and 1 each of `t`, `rtr`, `ertre` and `eertree`. The children are $\mathrm{to}[\text{imaginary}] = \{e, r, t\}$, $\mathrm{to}[\text{empty}] = \{ee\}$, $\mathrm{to}[t] = \{rtr\}$, $\mathrm{to}[rtr] = \{ertre\}$ and $\mathrm{to}[ertre] = \{eertree\}$.

## Correctness

Two facts carry the proof. First, each palindromic suffix of $t[0..i]$ of length at least 2 is $c\,q\,c$ for a palindromic suffix $q$ of $t[0..i-1]$ preceded by $c$, and the one-symbol suffix $c$ comes from the imaginary root. So the longest palindromic suffix of $t[0..i]$ is $c\,v\,c$ for the longest fitting $v$ on the suffix-link chain of $\mathrm{last}$, which is what line L2 finds; the chain lists all palindromic suffixes of $t[0..i-1]$ in decreasing length. Second, at most one new distinct palindrome appears at each step, and it can only be the longest palindromic suffix: a shorter palindromic suffix is also a prefix of it, by symmetry, so it occurred before. Line L3 tests whether that suffix is old. For a new node, the same argument applied to the proper suffixes of $c\,v\,c$ shows that its suffix link is $c\,u\,c$ for the longest fitting $u$ below $v$, which line L7 finds; this node exists already because it is a shorter palindromic suffix. The full proof is in the proof file of this page.

## Complexity

**Nodes.** At most $n + 2$, since each ADD makes at most one node.

**Walks.** Let $s_i$ be the start of the longest palindromic suffix of $t[0..i]$. Each link that line L2 follows makes the start of the candidate $v$ later by at least 1, and $s_i$ is one less than the start of the final $v$, while the walk begins at the start $s_{i-1}$. So the walk at step $i$ follows at most $s_i - s_{i-1} + 1$ links, and the total over all steps is at most $2n$. The same argument with the start of the longest *proper* palindromic suffix, $\mathrm{link}[\mathrm{last}]$, bounds the walks of line L7 by $2n$ in all. Each ADD is $O(1)$ apart from the walks and one dictionary access.

- **Time.** $O(n)$ steps and $O(n)$ dictionary operations. With a hash table per node this is $O(n)$ expected time; with sorted arrays or balanced trees it is $O(n \log k)$; with arrays indexed by symbol it is $O(n)$ for a constant alphabet but $\Theta(nk)$ space.
- **Per step.** One ADD can follow $\Theta(n)$ links, as at the `b` after $a^{n-1}$, so the bound is amortized. Rubinchik and Shur describe variants with a better bound per symbol.
- **Space.** $\Theta(n)$ words for the nodes and the edges, since there are at most $n$ edges.

## Variants

- **Series links.** Add $\mathrm{diff}[v] = \mathrm{len}[v] - \mathrm{len}[\mathrm{link}[v]]$ and the [series link](/series-links/), which jumps over a run of equal differences. This gives the $O(n \log n)$ algorithms for [minimum palindrome partition](/minimum-palindrome-partition/) and for counting palindromic partitions.
- **Faster walks.** Rubinchik and Shur also describe extra links per node that shorten the walks of lines L2 and L7 in the worst case, at the cost of more memory per node.
- **Several strings.** Adding the strings one after another, with $\mathrm{last}$ reset to the empty root between them, gives one tree of the palindromes of all strings, which answers the longest common palindrome and similar questions.
- **Deletion at the end.** Removing the last symbol undoes one ADD: remove the node it made, if any, and restore $\mathrm{last}$ from a stack of old values. With the amortized walks, a sequence of additions and deletions can be slow; the variants with extra links avoid this.

## When to use it

Use the eertree when the task is about distinct palindromes or about the palindromic suffixes of each prefix: the distinct count, occurrences of each palindrome, the test for [rich strings](/rich-string/), and palindromic factorization. Use [Manacher's algorithm](/manacher/) when only the maximal palindrome at each center is needed, such as the longest palindromic substring or the occurrence count: it is shorter and does not need a dictionary.

## Pitfalls

- **The two roots.** The imaginary root has length $-1$ and links to itself, and the empty root links to the imaginary root. A new node of length 1 links to the empty root, not to the imaginary one; otherwise the walks of the next steps skip the empty suffix.
- **Bounds check.** The fit test must check $j \ge 0$ before it reads $t[j]$. In Python, $t[-1]$ is the last symbol, not an error.
- **The stop of the walks.** The imaginary root fits at every position, so a walk always stops there at the latest and needs no other end test. A walk that stops at the empty root instead misses the one-symbol palindromes.
- **Amortized bound.** The linear bound is over the whole text. A single ADD can be slow.
- **Counts of occurrences.** The hit counter of a node counts only the positions where it is the longest palindromic suffix. The backward pass over the suffix links is needed to get all occurrences.

## Implementations

## History

Rubinchik and Shur introduced the eertree in 2015, first at the IWOCA workshop and in an arXiv preprint, with the journal version in 2018. They described it as a tree with two roots that gives a linear online algorithm for the distinct count and for other problems on palindromes, including palindromic factorization with series links. An earlier linear count of the distinct palindromes, by Groult, Prieur and Richomme (2010), used maximal palindromes and the longest previous factor array. The structure is now standard in programming contests under the name palindromic tree.

## References
