---
tag: 8T4YVE
kind: concept
slug: failure-link
name: Failure link
aliases:
- failure function
- suffix link (in a pattern trie)
- fail pointer
area: strings/multiple-pattern-matching
level: core
summary: A pointer from a trie node to the node of the longest proper suffix of its string that is also in the trie; it drives Aho-Corasick and generalizes the KMP prefix function.
prereqs: [trie, prefix-function, border]
see_also: [aho-corasick, dictionary-suffix-link, knuth-morris-pratt, string-matching-automaton, suffix-link, multiple-string-matching]
sources:
  - paper: doi:10.1145/360825.360855
    title: Alfred V. Aho and Margaret J. Corasick, Efficient string matching, an aid to bibliographic search, Communications of the ACM 18(6) (1975), 333-340
    locator: the failure function f, Algorithm 3 (its construction in breadth-first order) and Lemma 1 on its meaning
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 3.4.3, Failure functions for the keyword tree, and Section 3.4.5, Linear preprocessing for the failure function
  - paper: doi:10.1137/0206024
    title: D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350
    locator: the failure function of one pattern and its computation
---

A failure link is a pointer from a node $v$ of a [trie](/trie/) of patterns to the node of the longest proper suffix of $\mathrm{str}(v)$ that is also a node of the trie. When a search reaches $v$ and the next text character has no child, the search follows the failure link instead of going back in the text. For a trie of one pattern, the failure link of the node of length $q$ is the [prefix function](/prefix-function/) value $\pi[q-1]$, and the links of a whole trie are the base of the [Aho-Corasick algorithm](/aho-corasick/).

## In plain words

Picture all the words in one tree of letters. A spot in the tree stands for some letters read so far, and those letters are the start of at least one word.

When the next letter of the text leads nowhere, you would like to keep as much of your progress as you can. The best you can keep is the longest end of the letters read that is still the start of some word. The failure link of the spot points at the spot for that end.

Following it never loses a match, because any word that could still appear must start inside that end. Each link leads to a shorter string, so a chain of links always reaches the top of the tree, which stands for nothing read.

## The idea

**Definition.** Let $N$ be a finite set of strings that is closed under prefixes, such as the set of prefixes of a list of patterns. Its trie has one node for each string of $N$; write $\mathrm{str}(v)$ for the string of node $v$ and $|v|$ for its length. For each node $v$ other than the root,

$$\mathrm{fail}(v) = \text{the node of the longest proper suffix of } \mathrm{str}(v) \text{ that lies in } N.$$

The empty string is in $N$, so $\mathrm{fail}(v)$ always exists, and $|\mathrm{fail}(v)| < |v|$. The root has no failure link, or a link to itself by convention.

**The chain lists all suffixes in the trie.** For each node $v$, the nodes whose strings are proper suffixes of $\mathrm{str}(v)$ are exactly $\mathrm{fail}(v), \mathrm{fail}^2(v), \ldots$, ending at the root, in decreasing order of length. *Proof*, by induction on $|v|$: let $x \in N$ be a proper suffix of $\mathrm{str}(v)$ and $w = \mathrm{fail}(v)$. By the definition, $|x| \le |w|$. If $|x| = |w|$, then $x = \mathrm{str}(w)$, since both are suffixes of $\mathrm{str}(v)$ with the same length. If $|x| < |w|$, then $x$ is a proper suffix of $\mathrm{str}(w)$, and the induction hypothesis for $w$, which is shorter, puts $x$ on the chain of $w$. Each node on the chain spells a suffix of $\mathrm{str}(v)$, because a suffix of a suffix is a suffix. $\square$

**The recurrence.** If $u$ is the child of $v$ along the character $a$ and $|u| \ge 2$, then

$$\mathrm{fail}(u) = \mathrm{child}(f, a), \quad f = \text{the first node on the chain } \mathrm{fail}(v), \mathrm{fail}^2(v), \ldots \text{ that has a child along } a,$$

and $\mathrm{fail}(u) = \mathrm{root}$ if no node on the chain, the root included, has such a child; for $|u| = 1$, $\mathrm{fail}(u) = \mathrm{root}$. The reason: a nonempty proper suffix of $\mathrm{str}(v)a$ in $N$ has the form $ya$, where $y$ is a proper suffix of $\mathrm{str}(v)$, and $y \in N$ because $N$ is closed under prefixes; by the chain property the possible $y$ are the chain of $v$, longest first. Computed in breadth-first order, all links take $O(m)$ child lookups for patterns of total length $m$, by the same telescoping argument as for the prefix function, done once along the path of each pattern.

**The search step.** If a search is at node $v$ with $\mathrm{str}(v)$ the longest suffix of the text read that lies in $N$, and the next character is $c$, then the new longest suffix is $\mathrm{child}(w, c)$ for the first $w$ on $v, \mathrm{fail}(v), \mathrm{fail}^2(v), \ldots$ with a child along $c$, or the root. Any suffix of the text in $N$ that ends with $c$ is $yc$ with $y$ on this sequence, so no occurrence is skipped. The depth of the current node rises by at most 1 for each character and falls by at least 1 for each failure step, so a text of length $n$ causes at most $n$ failure steps in all.

**The failure tree.** Each non-root node has one failure link to a shorter node, so the links form a tree rooted at the root, often called the *failure tree* or *suffix-link tree*. The ancestors of $v$ in this tree are exactly the nodes on its chain. So a pattern $P$ is a suffix of $\mathrm{str}(v)$ if and only if the node of $P$ is an ancestor of $v$, or $v$ itself, in the failure tree.

**The automaton.** The failure links define the full transition function of the matching automaton without storing it: $\delta(v, a) = \mathrm{child}(v, a)$ if it exists, else $\delta(\mathrm{fail}(v), a)$, with $\delta(\mathrm{root}, a) = \mathrm{root}$ when the root has no such child. Storing $\delta$ for all pairs costs $\Theta(m\sigma)$ space and removes the failure steps from the search; see the [string-matching automaton](/string-matching-automaton/).

## Examples

**One pattern.** For the pattern aabaa, the trie is a path, and the failure links agree with the prefix function $\pi = [0, 1, 0, 1, 2]$: the node of length $q$ links to the node of length $\pi[q-1]$.

| node | a | aa | aab | aaba | aabaa |
|---|---|---|---|---|---|
| fail | root | a | root | a | aa |

**Several patterns.** For the patterns he, she, his, hers, the links are:

| node | h | he | s | sh | she | hi | his | her | hers |
|---|---|---|---|---|---|---|---|---|---|
| fail | root | root | root | h | he | root | s | root | s |

The link of his goes to s, a node that is not a pattern: it is only the start of she. This is why reporting needs a second link, the [dictionary suffix link](/dictionary-suffix-link/), which skips such nodes. The failure tree has the root with the children h, he, s, hi and her; then sh under h, she under he, and his and hers under s.

**Counting with the failure tree.** Search the text ushers and mark the node reached after each character: root, s, sh, she, her, hers, one visit each. The number of occurrences of a pattern is the number of visits in its subtree of the failure tree. The subtree of he is $\{$he, she$\}$, with one visit, so he occurs once. The subtree of hers is $\{$hers$\}$, with one visit. The subtree of his is $\{$his$\}$, with no visit.

**A non-example.** The link must point to the longest suffix that is a node of the trie, not to the longest suffix that is a pattern. Suppose the link of sh pointed to the root, because h is not a pattern. On the text shis, the search reaches sh after two characters, finds no child i, and falls to the root, which has no child i either. The last character s then leads to the node s, and the occurrence of his at position 1 is lost. With the correct link to h, the search goes from sh to h, then to hi and to his, and reports it.

## Where it is used

- [Aho-Corasick](/aho-corasick/) computes the failure links of the trie of the patterns and uses them in the search.
- [Knuth-Morris-Pratt](/knuth-morris-pratt/) and [Morris-Pratt](/morris-pratt/) use the failure links of a single pattern, stored as the [prefix function](/prefix-function/).
- The [dictionary suffix link](/dictionary-suffix-link/) is the failure chain restricted to pattern nodes.
- The [string-matching automaton](/string-matching-automaton/) is built from the failure links, one transition at a time.
- The [suffix link](/suffix-link/) of a suffix tree or a suffix automaton is the same idea for a structure of all substrings, and the [palindromic tree](/palindromic-tree/) uses suffix links between palindromes.
- [Dynamic dictionary matching](/dynamic-dictionary-matching/) studies how to keep failure links correct when patterns are inserted and deleted.

## References
