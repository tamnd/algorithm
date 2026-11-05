---
tag: 7NCBQB
kind: algorithm
slug: weiner-algorithm
name: Weiner's algorithm
aliases:
- Weiner's suffix tree algorithm
area: strings/suffix-structures
level: advanced
summary: The first linear-time suffix tree construction, building the tree from right to left.
solves: [suffix-tree-construction]
model: word-ram
complexity:
  vars: {n: the length of the text, σ: the size of the alphabet}
  time: {worst: O(n log σ), constant-alphabet: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
prereqs: [suffix-tree, suffix-link]
see_also: [mccreight-algorithm, ukkonen-algorithm, suffix-tree-construction, suffix-tree-size-theorem, suffix-automaton, blumer-algorithm, fm-index, suffix-trie]
sources:
  - paper: doi:10.1109/SWAT.1973.13
    title: Peter Weiner, Linear pattern matching algorithms, 14th Annual Symposium on Switching and Automata Theory, 1973
    locator: pages 1 to 11; the insertion of the suffixes from right to left with the indicator vectors and the link vectors
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 6, the section on Weiner's linear-time suffix tree algorithm (indicator vector, link vector, and the copy of the indicator vector at a new node)
  - paper: doi:10.1007/pl00009177
    title: Robert Giegerich and Stefan Kurtz, From Ukkonen to McCreight and Weiner, a unifying view of linear-time suffix tree construction, Algorithmica 19(3), 1997
    locator: pages 331 to 353; Weiner's algorithm compared with the online construction of the tree of the reversed string
---

Weiner's algorithm builds the [suffix tree](/suffix-tree/) of a string by reading it from right to left and inserting the suffixes from the shortest to the longest. Each new suffix $x\,t_{i+1}$ is the previous one with one symbol in front, so its branching point is found by walking up from the leaf of $t_{i+1}$ and jumping across a *Weiner link*, the reverse of a [suffix link](/suffix-link/), from a node $v$ to the node of $x\,\mathrm{str}(v)$. With an indicator set and a link map at each node, the total work is $O(n)$ for a constant alphabet. Peter Weiner published it in 1973; it was the first linear-time suffix tree construction.

## In plain words

Read the text from its last letter to its first. Each step, a new ending of the text appears, and it is the previous ending with one more letter in front. Put it into a tree of all endings seen so far.

The new ending shares a start with some older ending, and the shared part is the old ending's shared part with the new letter in front. To find it, go up from the leaf of the previous ending until you reach a branch point whose string, with the new letter in front, occurs somewhere. Each branch point keeps notes: which letters occur in front of its string, and where the tree has a branch point for each such longer string. A note leads to the right place, and at most one edge is cut. The walks up add up to about the length of the text.

## The problem

**Input.** A string $S = S[0 \ldots n-1]$, 0-based, over an alphabet $\Sigma$ of size $\sigma$ whose symbols can be keys of a hash map. The algorithm reads $S$ from right to left; it is online in that direction, and after each step the tree is the suffix tree of the current suffix of $S$, followed by the sentinel.

**Output.** The suffix tree of $t = S\$$, where the [sentinel](/sentinel-character/) $\$$ occurs nowhere in $S$: one leaf for each suffix $t_i = t[i \ldots n]$, inner nodes with at least two children, edges labeled by index pairs. The algorithm also leaves the Weiner links of the inner nodes; the suffix links are their reverses.

## The algorithm

Write $\mathrm{str}(v)$ for the string of a node $v$ and $|v|$ for its length. After the suffixes $t_{i+1}, \ldots, t_n$ are in the tree, each inner node and the root $v$ keeps:

- the *indicator set* $I_v$: the symbols $x$ such that $x\,\mathrm{str}(v)$ is a prefix of some inserted suffix, that is, occurs in $t_{i+1}$ as a substring with a symbol after it;
- the *link map* $L_v$: for each $x$ such that $x\,\mathrm{str}(v)$ is a node, $L_v(x)$ is that node.

A virtual node $\bot$ above the root, of depth $-1$, has $L_\bot(x) = \text{root}$ for every $x$. It stands for "the empty string with any symbol in front is the root".

```pseudo id=main
WEINER(t)                                   ▷ t = S$, suffixes inserted from t_n to t_0
L1  create the root and the leaf of t_n = $; I_root ← {$}
L2  for i ← n − 1 down to 0 do
L3      x ← t[i]; u ← parent of the leaf of t_(i+1)
L4      walk up from u to the lowest node v with x ∈ I_v, adding x to I of every node passed and to I_v
L5      if there is no such v then add the leaf of t_i below the root; continue      ▷ x occurs for the first time
L6      walk up from v to the lowest node v′ (possibly ⊥) with L_v′(x) defined
L7      v″ ← L_v′(x); g ← |v| − |v′|
L8      if g = 0 then h ← v″                       ▷ x str(v) is already a node
L9      else go down g symbols from v″, all inside one edge; split it there by a new node h;
             I_h ← I of the node below h; L_v(x) ← h
L10     add the leaf of t_i below h               ▷ h is the head of t_i
L11 return the tree
```

**Why this finds the head.** The head of $t_i = x\,t_{i+1}$ is its longest prefix that is a prefix of a later suffix. Such a prefix is $x\beta$ with $\beta$ a prefix of $t_{i+1}$ for which $x \in I$ at the place of $\beta$. The lowest node $v$ on the path of $t_{i+1}$ with $x \in I_v$ gives the longest one: a place inside the edge below $v$ cannot have $x$ in front, because every later suffix through that place also goes through the lower node, and that node does not have $x$. So the head is $x\,\mathrm{str}(v)$.

**Why the walk down stays in one edge.** If $x\beta$ is a node for some $\beta$ strictly between $\mathrm{str}(v')$ and $\mathrm{str}(v)$ on the path, then $\beta$ branches too, so $\beta$ is a node with a link for $x$, below $v'$, which contradicts the choice of $v'$. So between $v'' = x\,\mathrm{str}(v')$ and the head there is no node, and if $g > 0$ the head is not a node yet, since otherwise $L_v(x)$ would be defined and $v' = v$.

**Why the indicator set of the new node is a copy.** Before $t_i$ is added, every later suffix that passes $h$ continues to the node $c$ below it, so $y\,\mathrm{str}(h)$ occurs with a symbol after it exactly when $y\,\mathrm{str}(c)$ does. For a leaf $c$ of $t_k$, this set is $\{t[k-1]\}$.

## Example

Take $S = \texttt{abaaa}$, $n = 5$, $t = \texttt{abaaa\$}$.

| $i$ | $t_i$ | $x$ | $v$ | $v'$ | $g$ | case | head $h$ |
|---|---|---|---|---|---|---|---|
| 5 | `$` | | | | | start | |
| 4 | `a$` | a | none | | | L5, new symbol | empty |
| 3 | `aa$` | a | root | $\bot$ | 1 | L9, split the leaf edge `a$` | `a` |
| 2 | `aaa$` | a | `a` | root, $L_{root}(a) = $ `a` | 1 | L9, split the leaf edge `a$` below `a` | `aa` |
| 1 | `baaa$` | b | none | | | L5, new symbol | empty |
| 0 | `abaaa$` | a | root | root | 0 | L8, $L_{root}(a) = $ `a` | `a` |

In step 3, $\texttt{a}$ is in $I_{root}$ (the suffix $\texttt{a\$}$ starts with it), the root has no link for $\texttt{a}$ yet, so $v' = \bot$ and $v'' = $ root, and the walk goes down one symbol into the edge of $\texttt{a\$}$. The new node $\texttt{a}$ gets $I = \{t[3]\} = \{\texttt{a}\}$, the indicator of the leaf of $t_4$, and $L_{root}(\texttt{a}) = \texttt{a}$. In step 1 the walk from the node $\texttt{aa}$ passes $\texttt{aa}$, $\texttt{a}$ and the root without finding $\texttt{b}$, adds $\texttt{b}$ to all three, and the new leaf hangs from the root. In step 0, $v = v' = $ root and the link leads directly to the head $\texttt{a}$. The final tree has the root, the inner nodes $\texttt{a}$ and $\texttt{aa}$, and six leaves, 9 nodes; the leaves in symbol order give the suffix array $[4, 3, 2, 0, 1]$ of $S$. At the end $I_{root} = \{\$, \texttt{a}, \texttt{b}\}$ and $I_{\texttt{a}} = I_{\texttt{aa}} = \{\texttt{a}, \texttt{b}\}$. The code checks this trace.

## Correctness

The invariant before the step for $i$ is: the tree is the compact trie of $t_{i+1}, \ldots, t_n$; for each inner node and the root, $I_v$ and $L_v$ match their definitions. Line L4 finds the lowest node with $x$ in front, and by the argument above the head of $t_i$ is $x\,\mathrm{str}(v)$, or empty if there is no such node. Lines L6 to L9 reach the head with one link and one partial edge, and split the edge if the head is not yet a node. Line L10 adds the leaf. The updates keep the invariant: every node on the path of $t_{i+1}$ now has $x$ in front, which line L4 records; the only new inner node is $h$, which gets the copied indicator set, an empty link map (no string $y\,\mathrm{str}(h)$ can be a node yet), and the incoming link $L_v(x) = h$. The proof file gives the details.

## Complexity

**Walks up.** Let $nd(w)$ be the node depth, the number of nodes on the root path of $w$. A Weiner link raises the node depth by at most one: each node above $x\,\mathrm{str}(v')$ other than the root is $x\beta$ for a node $\beta$ above $v'$, and different nodes give different $\beta$. So the new leaf has $nd(\text{leaf of } t_i) \le nd(v') + 3$, counting the link, the split and the leaf. Lines L4 and L6 pass $nd(\text{leaf of } t_{i+1}) - nd(v')$ nodes, which is at most $nd(\text{leaf of } t_{i+1}) - nd(\text{leaf of } t_i) + 3$. Summed over $i$, this telescopes to $O(n)$.

**Indicator sets.** Each set only grows, and the copy in line L9 creates as many entries as it reads. The total number of entries is the number of pairs $(v, x)$ with $x\,\mathrm{str}(v)$ a substring followed by a symbol, the explicit and implicit Weiner links. Reversing the text maps these pairs to pairs (left-maximal string, right extension) of $S^R$; their number is at most the number of edges of the suffix tree of the reverse plus the number of nodes of this tree, which is $O(n)$. So all set operations together are $O(n)$.

**Total.** $O(n)$ dictionary operations: $O(n)$ expected time with hashing, $O(n)$ for a constant alphabet, and $O(n \log \sigma)$ with balanced search trees as maps. Weiner's original used arrays of size $\sigma$ at each node, with $O(n\sigma)$ space.

| resource | bound |
|---|---|
| time, constant alphabet or hashing | $O(n)$, expected for hashing |
| time, ordered maps | $O(n \log \sigma)$ |
| space with sparse sets and maps | $O(n)$ words |
| space with arrays of size $\sigma$ | $O(n\sigma)$ words |

## Properties

- **Online from the right.** After the step for $i$, the tree is the suffix tree of $S[i \ldots n-1]\$$; a text that grows at its front can be indexed as it grows.
- **Equality tests only.** Symbol order is used only to list children in order afterwards.
- **Builds Weiner links as a by-product.** The links are the transitions used by backward search in the [FM-index](/fm-index/) and by the [suffix automaton](/suffix-automaton/) of the reversed text.
- **Iterative.** The code uses no recursion.

## Variants and improvements

- **McCreight's algorithm.** [McCreight's](/mccreight-algorithm/) 1976 algorithm inserts the suffixes from the longest, needs only suffix links, and uses less space; it replaced Weiner's in most presentations.
- **Ukkonen's algorithm.** [Ukkonen's](/ukkonen-algorithm/) online algorithm reads the text from left to right. Building the suffix tree of the reversed text with Weiner's algorithm is related to building the suffix automaton of the text from the left, as the Weiner links of one are the transitions of the other.
- **The DAWG connection.** Blumer and others noted that the Weiner links of the suffix tree of $S^R$ give the edges of the [suffix automaton](/suffix-automaton/) of $S$; Chen and Seiferas (1985) built both in one pass.
- **Space-efficient construction.** Modern algorithms use Weiner links over a Burrows-Wheeler index to traverse suffix tree nodes in compact space, without storing the tree.

## When to use it

Weiner's algorithm is mainly of historical and conceptual interest: it explains Weiner links, which are central to compressed indexes. Use it when the text grows at its front, or when you also need the Weiner links. To build a suffix tree of a fixed text, McCreight's or Ukkonen's algorithm is simpler, and a [suffix array](/suffix-array/) with an LCP array is often faster in practice.

## Pitfalls

- **Searching down from the root.** The head is reached through a link and one partial edge; searching down from the root symbol by symbol gives quadratic time on texts such as $a^n$.
- **Forgetting the virtual node.** When no node on the way has a link for $x$, the walk goes down from the root by $|v| + 1$ symbols, starting with $x$; treating this case as "head at the root" gives a wrong tree.
- **Not updating the indicator sets on the path.** Every node passed in line L4 must get $x$, or a later step stops too high.
- **Linking from leaves.** Leaves never become $v$ or $v'$, so the code stores no indicator sets at leaves and computes the copy for a leaf child as $\{t[k-1]\}$.
- **No unique sentinel.** Without it, some suffix is a prefix of a longer one and has no leaf.

## Implementations

## History

Peter Weiner presented the algorithm at the 14th Annual Symposium on Switching and Automata Theory in 1973, under the title "Linear pattern matching algorithms". It gave the first linear-time solution for many string problems, including the longest repeated substring and the longest common substring. McCreight (1976) gave a simpler left-to-right construction, and Ukkonen (1995) an online one; Giegerich and Kurtz (1997) compared the three.

## References
