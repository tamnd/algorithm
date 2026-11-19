---
tag: CCPJNB
kind: algorithm
slug: swap-transition-system
name: Swap transition system
aliases:
- non-projective swap parsing
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: "Arc-standard parsing with an extra swap move that reorders words, so it builds any non-projective tree, in quadratic time at worst and near linear time on treebanks."
solves: [dependency-parsing]
model: word-ram
complexity:
  vars: {n: "the number of words, with a scorer of constant cost for each of a fixed number of transitions"}
  time: {worst: Θ(n^2), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2009
  people: [Joakim Nivre]
  note: "Nivre (2009) added a SWAP move to the arc-standard system, proved that the result builds every dependency tree, and found that the number of swaps on treebanks is small, so parsing time is close to linear in practice."
prereqs: [arc-standard-parsing]
see_also: [projective-dependency-tree, mst-dependency-parsing, arc-hybrid-parsing, inorder-traversal, inversion, counting-inversions, bubble-sort, dynamic-oracle]
sources:
  - url: https://aclanthology.org/P09-1040/
    title: "Joakim Nivre, Non-projective dependency parsing in expected linear time, ACL-IJCNLP 2009"
    locator: "the SWAP transition, the proof of soundness and completeness for all trees, the oracle based on the projective order, the quadratic worst case and the experiments"
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: "the arc-standard system that the swap system extends"
---

The swap transition system extends [arc-standard parsing](/arc-standard-parsing/) so that it can build every [dependency tree](/dependency-tree/), not only the [projective](/projective-dependency-tree/) ones. It adds one move, SWAP, which takes the second word of the stack and puts it back at the front of the buffer. This changes the order in which words meet on the stack. Arcs are still made only between the two top stack words, so the system builds a projective tree over a reordered sentence, and every tree is projective under some order of its words: its projective order, given by an [inorder traversal](/inorder-traversal/). Nivre (2009) proposed the system. With $k$ swaps a parse takes $2n + 2k$ moves for $n$ words. Each pair of words can be swapped at most once, so $k \le n(n - 1)/2$ and the worst case is quadratic. On treebanks, few swaps are needed, and the time is close to linear. The title of the paper speaks of expected linear time; that is a statement about real data, not a bound.

## In plain words

Arc-standard parsing reads the words onto a pile and joins the two words on top. It can only join words that become neighbours on the pile, so it cannot build arrows that cross. The swap system adds one more move: take the word under the top and put it back in front of the unread words. The two words now come in the opposite order. By doing this several times, the parser can bring words that belong together next to each other, join them, and leave the rest for later. A word that has been put back can come up again later. Any tree can be built this way, but each swap costs two extra moves, so many swaps make the parse slower.

## The problem

The input is a sentence $w_1 \cdots w_n$ with features and a scoring function on the legal transitions of a configuration. The output is a labeled [dependency tree](/dependency-tree/), with crossing arcs allowed. In the version on this page the root may have several children, since RIGHT-ARC can attach any number of words to the root. The single-root rule of arc-standard parsing, RIGHT-ARC from the root only when the buffer is empty, can be added in the same way.

## The algorithm

Configurations are as in arc-standard parsing, but the buffer is now a list that SWAP can add to, not just a suffix of the sentence. The initial configuration is $([0], [1, \ldots, n], \emptyset)$, the terminal ones are $([0], [\,], A)$, and the words are compared by their original positions. The transitions, for each label $l$:

| transition | before | after | condition |
|---|---|---|---|
| SHIFT | $(\sigma, b \mid \beta, A)$ | $(\sigma \mid b, \beta, A)$ | |
| LEFT-ARC$_l$ | $(\sigma \mid s_1 \mid s_0, \beta, A)$ | $(\sigma \mid s_0, \beta, A \cup \{s_0 \xrightarrow{l} s_1\})$ | $s_1 \ne 0$ |
| RIGHT-ARC$_l$ | $(\sigma \mid s_1 \mid s_0, \beta, A)$ | $(\sigma \mid s_1, \beta, A \cup \{s_1 \xrightarrow{l} s_0\})$ | |
| SWAP | $(\sigma \mid s_1 \mid s_0, \beta, A)$ | $(\sigma \mid s_0, s_1 \mid \beta, A)$ | $0 < s_1 < s_0$ |

The condition $s_1 < s_0$ lets SWAP only undo the original order of a pair, so a pair is never swapped back and the parser cannot loop.

```pseudo id=main
SWAP-PARSE(x, score)
L1  c <- ([0], [1, ..., n], {})
L2  while c is not terminal do
L3      for each legal transition t of c
L4          compute score(c, t), and keep the best t
L5      if t = SHIFT then move the front of the buffer onto the stack
L6      if t = LEFT-ARC_l then add s0 -l-> s1 and remove s1 from the stack
L7      if t = RIGHT-ARC_l then add s1 -l-> s0 and remove s0 from the stack
L8      if t = SWAP then move s1 from the stack to the front of the buffer
L9  return the tree A
```

**The oracle.** For a gold tree, let $\mathrm{pos}(w)$ be the rank of $w$ in its projective order: the inorder traversal that visits, at each word, the subtrees of its left dependents, then the word, then the subtrees of its right dependents, each group in word order. In a configuration with top words $s_1, s_0$: choose LEFT-ARC if $s_0$ is the gold head of $s_1$ and $s_1$ has all its dependents; RIGHT-ARC if $s_1$ is the gold head of $s_0$ and $s_0$ has all its dependents; SWAP if $\mathrm{pos}(s_0) < \mathrm{pos}(s_1)$; else SHIFT.

## Example

**A small tree.** The head list `[-1, 3, 0, 2]` has the arcs $0 \to 2$, $2 \to 3$ and $3 \to 1$. The arc $3 \to 1$ passes over word 2, the head of 3, so the tree is not projective. Its projective order is 0, 2, 1, 3. The oracle:

| step | transition | stack | buffer | new arc |
|---|---|---|---|---|
| 0 | | 0 | 1 2 3 | |
| 1 | SH | 0 1 | 2 3 | |
| 2 | SH | 0 1 2 | 3 | |
| 3 | SWAP | 0 2 | 1 3 | |
| 4 | SH | 0 2 1 | 3 | |
| 5 | SH | 0 2 1 3 | | |
| 6 | LA | 0 2 3 | | $3 \to 1$ |
| 7 | RA | 0 2 | | $2 \to 3$ |
| 8 | RA | 0 | | $0 \to 2$ |

At step 3, word 2 comes before word 1 in the projective order, so SWAP puts word 1 back. After that the stack meets the words in the order 0, 2, 1, 3, in which the tree is projective, and the rest is arc-standard parsing. There are $8 = 2 \cdot 3 + 2 \cdot 1$ moves.

**A longer sentence.** In *A hearing is scheduled on the issue today*, with the heads `[-1, 2, 3, 0, 3, 2, 7, 5, 4]`, the phrase *on the issue* belongs to *hearing* but comes after *is scheduled*. The projective order is 0 1 2 5 6 7 3 4 8: the phrase moves before *is scheduled*. The oracle of this page swaps eagerly, word by word, and uses 6 swaps and 28 moves. A search over all sequences finds that 2 swaps suffice, 20 moves: first build *on the issue* into one subtree headed by *on*, then swap *on* past *scheduled* and past *is*. The tests check all three numbers.

## Correctness

**Every run ends in a tree.** If the buffer is not empty, SHIFT is legal; otherwise RIGHT-ARC is legal while the stack has two words. So the parser never gets stuck before a terminal configuration. Each word gets its head when it leaves the stack by an arc, and a word that has left the stack this way never comes back; SWAP puts back only words without a head. In a terminal configuration every word has thus exactly one head, and no cycle can form, because a word with a head is never again a head. The result is a tree, but not always a projective one.

**Termination.** A SWAP inverts a pair of words, and a pair cannot be swapped back, so there are at most $n(n - 1)/2$ swaps. Between swaps the run behaves as in arc-standard parsing.

**Every tree is reached.** A tree is projective with respect to its projective order. Run arc-standard parsing on the words in that order, and replace each SHIFT of a word $w$ by shifting the words in front of $w$ in the buffer, shifting $w$, and swapping those words back one by one. The SWAPs are legal because the buffer stays in the original order. So every tree has a sequence. The proof is in [the correctness proof](proofs/correctness.md). The tests build all complete sequences for $n \le 4$ and find all $(n + 1)^{n - 1}$ trees, and they run the oracle on every tree with $n \le 5$.

## Complexity

**Number of transitions.** Let $k$ be the number of swaps. SHIFT and SWAP move a word between the buffer and the stack in opposite directions, so there are $n + k$ shifts, and there are $n$ arcs. The total is $2n + 2k$. Since $k \le n(n - 1)/2$, a run has at most $n + n^2$ transitions, and a parser that swaps every pair reaches this bound.

**The oracle's swaps.** Let $\mathrm{inv}$ be the number of pairs of words whose order in the sentence is the opposite of their order in the projective order, and $k_{\min}$ the least number of swaps of any sequence for the tree. Then the eager oracle uses $k$ swaps with $k_{\min} \le k \le \mathrm{inv}$. For projective trees $k = 0$. $k$ can be smaller than $\mathrm{inv}$, because an arc can remove a word before it has to be moved: for the tree `[-1, 0, 0, 2, 1]`, $k = 1$ and $\mathrm{inv} = 2$. The largest $k$ over all trees of $n$ words is 0, 0, 1, 2, 4, 7 for $n = 1$ to 6. The tests check the upper bound for every tree with $n \le 5$, and compare $k$ with $k_{\min}$, found by search, for every tree with $n \le 4$ and 150 sampled trees with $n = 5$.

**Time.** With a scorer of constant cost, $\Theta(n + k)$, which is $\Theta(n)$ at best and $\Theta(n^2)$ at worst. Nivre (2009) reports that on treebanks the number of swaps stays small, so the running time is close to linear in practice.

**Space.** $\Theta(n)$: the buffer never holds more than $n$ words.

## Properties

- **Sound and complete for all trees.** Every terminal configuration holds a dependency tree, and every tree, projective or not, has a sequence.
- **Projective trees need no swap.** For a projective tree the projective order is the word order, and the oracle gives exactly the arc-standard sequence.
- **Sorting by adjacent exchanges.** SWAP exchanges two neighbours, much as [bubble sort](/bubble-sort/) does; the number of [inversions](/inversion/) between the word order and the projective order bounds the swaps the oracle needs, as it bounds the exchanges of bubble sort.
- **Spurious ambiguity.** A tree has many sequences, with different numbers of swaps, as the hearing example shows.
- **Not exact.** The greedy parser can miss the best tree. Unlike the projective systems, there is no known polynomial dynamic program over its sequences for arc scores; for exact non-projective search with arc scores, use [MST parsing](/mst-dependency-parsing/).

## Variants and improvements

- **Lazy swapping.** Nivre, Kuhlmann and Hall (2009) delay each SWAP until the words to be moved form a complete subtree, so that whole phrases move at once and fewer swaps are needed. On the hearing example the best sequence, found by search in the tests, moves the subtree of *on* as one unit in this way.
- **Other scorers.** The scorer is separate from the system, so [beam search](/beam-search/) and neural scorers can be used with the swap system as with arc-standard parsing.
- **Training on own errors.** The [dynamic oracle](/dynamic-oracle/) method needs the cost of each move. For the swap system these costs are harder to compute than for arc-eager or arc-hybrid parsing, and the oracle of this page is static.
- **Other routes to crossing arcs.** Pseudo-projective parsing transforms the treebank into projective trees and undoes the transformation after parsing. Graph-based parsers find the best tree of all directly, with [MST parsing](/mst-dependency-parsing/).

## When to use it

Use the swap system when a transition-based parser must produce non-projective trees, for languages with free word order or treebanks with many crossing arcs, and greedy or beam parsing at near linear speed is wanted. When exact search with arc scores is wanted, use MST parsing. When the treebank is almost all projective, a projective system with fewer moves is simpler.

## Pitfalls

- **Comparing by stack order instead of word order.** The condition $s_1 < s_0$ uses the original positions. Without it, the parser can swap a pair back and forth for ever.
- **SWAP with the root.** The root must stay at the bottom of the stack; SWAP requires $s_1 > 0$.
- **Eager oracle, many swaps.** The eager oracle moves words one at a time and can use many more swaps than needed (6 against 2 on the hearing example), which gives the classifier longer sequences to learn. Lazy swapping helps.
- **The projective order.** The oracle must use the inorder traversal with the left dependents before the head and the right dependents after it, each group in word order. Another order can make the gold tree non-projective under it, and the oracle then fails.
- **Expected linear time is not a bound.** On a hostile input, or with a bad classifier, the parse takes quadratic time.

## Implementations

## History

Before 2009, transition-based parsers handled crossing arcs by pseudo-projective transformations of the treebank, or by systems that could add arcs between words further apart on the stack. Nivre (2009) proposed the SWAP move, proved that the extended system is sound and complete for all trees, gave the oracle that sorts the words into the projective order, and reported that the number of swaps on several treebanks was small, so the parser ran in about linear time on real data. Later in 2009, Nivre, Kuhlmann and Hall proposed lazy swapping, which moves whole subtrees and needs fewer swaps.

## References
