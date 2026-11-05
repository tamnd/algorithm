---
tag: ZXBX1X
kind: concept
slug: suffix-link
name: Suffix link
aliases:
- suffix pointer
area: strings/suffix-structures
level: core
summary: A pointer from a node for string aX to the node for string X, used to speed up construction.
prereqs: [suffix-tree]
see_also: [ukkonen-algorithm, mccreight-algorithm, weiner-algorithm, suffix-automaton, failure-link, aho-corasick, matching-statistics, implicit-suffix-tree]
sources:
  - paper: doi:10.1145/321941.321946
    title: Edward M. McCreight, A space-economical suffix tree construction algorithm, Journal of the ACM 23(2), 1976
    locator: pages 262 to 272; the suffix links and the rescanning step that uses them
  - paper: doi:10.1007/BF01206331
    title: Esko Ukkonen, On-line construction of suffix trees, Algorithmica 14(3), 1995
    locator: pages 249 to 260; suffix links in the suffix trie and in the suffix tree, and the traversal of the boundary path
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 6, Linear-time construction of suffix trees (suffix links, the lemma that each inner node has one, and the skip and count trick)
  - paper: doi:10.1016/0304-3975(85)90157-4
    title: A. Blumer, J. Blumer, D. Haussler, A. Ehrenfeucht, M. T. Chen and J. Seiferas, The smallest automaton recognizing the subwords of a text, Theoretical Computer Science 40, 1985
    locator: pages 31 to 55; the suffix pointers of the DAWG and their tree
---

A suffix link goes from the node of a string $cx$, where $c$ is one symbol, to the node of $x$: the same string with its first symbol removed. In a [suffix tree](/suffix-tree/) every inner node has one, and it points to an inner node. With suffix links, a construction that has just handled one suffix jumps to the place of the next shorter suffix without walking down from the root, which is how [Ukkonen's](/ukkonen-algorithm/) and [McCreight's](/mccreight-algorithm/) algorithms reach linear time. The [suffix automaton](/suffix-automaton/) has suffix links too, with a slightly different meaning, and they form a tree that is the suffix tree of the reversed string.

## In plain words

In a tree of all pieces of a word, each node stands for a piece, such as "ana" in "banana". A suffix link is an arrow from that node to the node of the same piece without its first letter: from "ana" to "na", from "na" to "a", from "a" to the top.

Building the tree means visiting the pieces "ana", "na", "a" one after the other. Without the arrows, each visit starts again from the top and reads the letters again. With the arrows, one step moves from a piece to the next shorter one. This saves so much reading that the whole tree can be built in time proportional to the length of the word.

## The idea

Fix a string $S = S[0 \ldots n-1]$, 0-based, over any alphabet, and a tree or automaton whose nodes stand for substrings of $S$. The links are defined on the structures as follows.

**In a suffix trie.** Each node other than the root has a path label $cx$, with $c$ a symbol, and $x$ is also a substring, so it has a node. The suffix link of $cx$ is the node of $x$. Following links from the node of a string $y$ visits the nodes of all suffixes of $y$, shortest last, and ends at the root.

**In a suffix tree.** Only nodes are linked, and the claim that the target is a node needs a proof.

> **Lemma.** In the suffix tree of $S\$$, with $\$$ a symbol not in $S$, if $cx$ is the path label of an inner node other than the root, then $x$ is the path label of an inner node.
>
> **Proof.** $cx$ labels an inner node, so it is right-branching: $cxa$ and $cxb$ are substrings of $S\$$ for some symbols $a \ne b$. Then $xa$ and $xb$ are substrings too, so $x$ is right-branching, and every right-branching substring labels an inner node. If $x$ is empty, the target is the root. $\square$

So $link(v)$ is defined for every inner node $v \ne$ root, with $depth(link(v)) = depth(v) - 1$. Leaves have links in the same way, from the leaf of $T_i$ to the leaf of $T_{i+1}$, but constructions do not need to store them.

**In a suffix automaton.** A state stands for a class of substrings with the same set of end positions; the strings of one class are the suffixes of its longest member that are longer than some length. The suffix link of a state goes to the state of the longest suffix of these strings that is in a different class. Its length is one less than the shortest string of the state. The links form a tree rooted at the start state, and this tree is the suffix tree of the reversed string, with the states as nodes.

**Why links save time.** Constructions handle the suffixes of the text in order of decreasing length, or the suffixes of a growing prefix. After handling the place of $cx$, the next place to handle is $x$. Going up to the nearest node with a link, following the link, and going down again by $|x|$ minus the depth reached costs only a few steps on average: the node depth, the number of nodes on the path from the root, drops by at most one at each link, and by an amortized argument the total down-walk over the whole construction is $O(n)$. Ukkonen's and McCreight's papers prove this with a potential on the depth of the current node, and Gusfield calls the fast down-walk, which reads only the first symbol of each edge, the skip and count trick.

**The reverse direction.** The link from $cx$ to $x$, read backwards, is an edge from $x$ to $cx$ labeled with $c$: a Weiner link. [Weiner's algorithm](/weiner-algorithm/) inserts the suffixes from the shortest and uses these reverse links, and the transitions of the suffix automaton between classes play the same role.

## Examples

**Suffix tree of $\texttt{banana\$}$.** The inner nodes are the root, $\texttt{a}$, $\texttt{na}$ and $\texttt{ana}$. The links are $\texttt{ana} \to \texttt{na}$, $\texttt{na} \to \texttt{a}$ and $\texttt{a} \to$ root. From $\texttt{ana}$, three links reach the root through all suffixes of $\texttt{ana}$, and the depths drop $3, 2, 1, 0$.

**Suffix trie of $\texttt{abab}$.** Each of the 7 non-root nodes has a link: $\texttt{abab} \to \texttt{bab} \to \texttt{ab} \to \texttt{b} \to$ root and $\texttt{aba} \to \texttt{ba} \to \texttt{a} \to$ root. In the suffix tree of $\texttt{abab\$}$, only $\texttt{ab}$ and $\texttt{b}$ are inner nodes, and the link of $\texttt{ab}$ goes to $\texttt{b}$.

**Suffix automaton of $\texttt{abbb}$.** The states, written as their classes, are $\{\varepsilon\}$, $\{\texttt{a}\}$, $\{\texttt{b}\}$, $\{\texttt{ab}\}$, $\{\texttt{bb}\}$, $\{\texttt{abb}\}$ and $\{\texttt{bbb}, \texttt{abbb}\}$. The links are

| state | link |
|---|---|
| $\{\texttt{bbb}, \texttt{abbb}\}$ | $\{\texttt{bb}\}$ |
| $\{\texttt{abb}\}$ | $\{\texttt{bb}\}$ |
| $\{\texttt{bb}\}$ | $\{\texttt{b}\}$ |
| $\{\texttt{ab}\}$ | $\{\texttt{b}\}$ |
| $\{\texttt{b}\}$, $\{\texttt{a}\}$ | $\{\varepsilon\}$ |

Here $\texttt{abb}$ ends only at position 2, but $\texttt{bb}$ ends at positions 2 and 3, so they are in different classes, and the link of $\{\texttt{abb}\}$ skips nothing. The link of $\{\texttt{bbb}, \texttt{abbb}\}$ skips the two strings of its class at once.

**A non-example.** The link of $cx$ does not go to the node of $xc$ or of any string other than $x$, and a link in a suffix tree never goes down: $depth(link(v)) = depth(v) - 1$ exactly. In the suffix automaton, the length drops by at least one and may drop by more.

## Where it is used

- **Linear-time suffix tree construction.** [Ukkonen's algorithm](/ukkonen-algorithm/) and [McCreight's algorithm](/mccreight-algorithm/) move between consecutive suffixes by suffix links; Weiner's uses their reverse. See [suffix tree construction](/suffix-tree-construction/).
- **Suffix automaton construction.** The online construction of [Blumer and others](/blumer-algorithm/) walks the links of the last state to add the transitions of a new symbol, and splits a state by cloning when a link must point into the middle of a class.
- **Matching statistics.** For each position of a second text, the longest substring of $S$ that starts there is found in $O(1)$ amortized time per position by following a suffix link when the match fails. See [matching statistics](/matching-statistics/) and the longest common substring.
- **Failure links.** The [failure links](/failure-link/) of the [Aho-Corasick](/aho-corasick/) automaton point to the longest proper suffix that is in the trie of the patterns. They are suffix links in a trie where the target need not be the suffix shorter by one symbol.
- **Tree of all suffixes of the reversed string.** In a suffix automaton, the link tree is the suffix tree of the reversed text, which gives a way to build one structure from the other.

## References
