---
tag: R21EJV
kind: definition
slug: projective-dependency-tree
name: Projective dependency tree
aliases:
- projectivity
area: natural-language-and-speech/natural-language-parsing
level: core
summary: "A dependency tree in which every word between a head and its dependent is a descendant of that head, so arcs drawn above do not cross."
prereqs: [dependency-tree]
see_also: [eisner-algorithm, arc-standard-parsing, swap-transition-system, mst-dependency-parsing, inorder-traversal, head-rules, dependency-parsing, catalan-numbers]
sources:
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 2, Dependency Parsing (the definition of projectivity and its relation to crossing arcs)"
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: the definition of projective dependency trees and the proofs that the stack-based systems build exactly the projective trees
  - url: https://aclanthology.org/P09-1040/
    title: "Joakim Nivre, Non-projective dependency parsing in expected linear time, ACL-IJCNLP 2009"
    locator: "the projective order of a tree, defined by an inorder traversal, which the swap oracle uses"
---

A [dependency tree](/dependency-tree/) is projective when each head dominates all the words between itself and each of its dependents. Drawn with the root at the left edge and every arc above the words, a projective tree has no two crossing arcs. In a projective tree every subtree covers a contiguous block of words, as a phrase does in a [parse tree](/parse-tree/). Projectivity is what makes the cubic [Eisner algorithm](/eisner-algorithm/) and the stack-based transition systems ([arc-standard](/arc-standard-parsing/), [arc-eager](/arc-eager-parsing/), [arc-hybrid](/arc-hybrid-parsing/)) work, and the parsers that drop it, [MST parsing](/mst-dependency-parsing/) and the [swap system](/swap-transition-system/), are built around its absence.

## Definition

Take a sentence $w_1 \cdots w_n$ with the artificial root $w_0$ at the left edge, and a dependency tree with head function $h$. A word $k$ dominates a word $d$ when $k$ is on the chain $d, h(d), h(h(d)), \ldots, 0$; every word dominates itself and the root dominates every word. The root may have one child or several; projectivity does not depend on that choice.

**Projective arc.** An arc $(h, d)$ is projective if $h$ dominates every word $k$ strictly between $h$ and $d$, that is, with $\min(h, d) < k < \max(h, d)$.

**Projective tree.** A tree is projective if every one of its arcs is projective.

**Crossing form.** Two arcs $(a, b)$ and $(c, e)$ cross if exactly one endpoint of each lies strictly between the endpoints of the other, that is, after renaming, $\min(a, b) < \min(c, e) < \max(a, b) < \max(c, e)$. A tree is projective exactly when no two of its arcs cross, with the root at position 0 and its arcs drawn too.

*Proof of the equivalence.* Suppose two arcs cross, with positions $p < q < r < t$, the first arc joining $p$ and $r$ and the second joining $q$ and $t$. If the tree were projective, the head of the first arc would dominate $q$ and the head of the second arc would dominate $r$. If the first head is $p$, then $r$ is a child of $p$, and $q$ is below $p$. If the second head is $q$, then $q$ dominates $r$, so $q$ is on the chain from the child $r$ up to its head $p$, which holds only $r$ and $p$; impossible. If the second head is $t$, then $q$ is a child of $t$ and $t$ dominates $r$, hence also dominates its head $p$, while $p$ dominates $q$ and hence its head $t$; two distinct words cannot dominate each other. The case where the first head is $r$ is the same with the roles of the two arcs exchanged. So a projective tree has no crossing arcs.

Conversely, let the arc $(h, d)$ be not projective, with a word $k$ strictly between $h$ and $d$ that $h$ does not dominate. Then $h \neq 0$, because 0 dominates every word. Follow the chain of heads from $k$ to 0. It never meets $h$, and it never meets $d$, because $h$ dominates everything that $d$ dominates. It starts strictly inside the interval between $h$ and $d$ and ends at 0, which is to the left of the interval. So one arc of the chain joins a word strictly inside to a word strictly outside, and that arc crosses $(h, d)$. $\square$

**Two more equivalent forms.** A tree is projective exactly when the yield of every word (its subtree) is a contiguous interval of positions. It is also projective exactly when the [inorder traversal](/inorder-traversal/) that visits, at each node, the subtrees of its left dependents, then the node, then the subtrees of its right dependents (each group in word order) lists the positions $0, 1, \ldots, n$ in order. Nivre (2009) calls the order of this traversal the projective order of the tree; the [swap system](/swap-transition-system/) sorts the words into it.

## Examples and non-examples

**Projective.** *the cat sat on the mat* with the head list `[-1, 2, 3, 0, 6, 6, 3]`. Every subtree is an interval: *the cat* (1 to 2), *on the mat* (4 to 6), and the whole sentence under *sat*.

**Not projective.** *A hearing is scheduled on the issue today* with the head list `[-1, 2, 3, 0, 3, 2, 7, 5, 4]`. The arc from *hearing* (2) to *on* (5) passes over *is* (3), which *hearing* does not dominate. This arc does not cross the arc from *is* (3) to *scheduled* (4), because that arc is nested inside it. It crosses the arc from *scheduled* (4) to *today* (8), since $2 < 4 < 5 < 8$, and the arc from the root to *is*, since $0 < 2 < 3 < 5$. The yield of *hearing* is $\{1, 2, 5, 6, 7\}$, which has a gap.

**Why the root arc counts.** The head list `[-1, 3, 0, 2]` has the arcs $0 \to 2$, $2 \to 3$ and $3 \to 1$. Among the words alone, the arcs $(2, 3)$ and $(3, 1)$ are nested and do not cross. But the arc $3 \to 1$ passes over word 2, which is the head of 3, not a descendant. With the root at position 0, the arcs $(0, 2)$ and $(3, 1)$ cross, since $0 < 1 < 2 < 3$. A test that forgets the root arcs accepts this tree by mistake.

**Counts.** Over $n$ words, the projective trees number 1, 3, 12, 55, 273 for $n = 1$ to 5, and 1428, 7752, 43263, 246675, 1430715 for $n = 6$ to 10. With exactly one child of the root they number 1, 2, 7, 30, 143 for $n = 1$ to 5. The tests of the Eisner page compute these numbers with the counting semiring and check the small ones against a search over all $(n + 1)^{n - 1}$ trees. At $n = 5$ only 273 of the 1296 trees are projective, about 21 percent, and the fraction keeps falling as $n$ grows.

**Converted treebanks.** A constituency tree with contiguous phrases, converted to dependencies by [head rules](/head-rules/), always gives a projective tree: each phrase becomes the yield of its head word, and the phrases are intervals. Non-projective arcs in such a treebank can only come from other information in the original annotation, such as traces, not from the head rules.

## Related definitions

- [Dependency tree](/dependency-tree/): the general structure, with crossing arcs allowed.
- [Eisner algorithm](/eisner-algorithm/): finds the best projective tree under arc scores in $O(n^3)$ time, by building the intervals of the third equivalent form.
- [Arc-standard](/arc-standard-parsing/), [arc-eager](/arc-eager-parsing/) and [arc-hybrid](/arc-hybrid-parsing/) parsing: each of these transition systems builds exactly the projective trees.
- [Swap transition system](/swap-transition-system/) and [MST dependency parsing](/mst-dependency-parsing/): build trees that need not be projective.
- [Catalan numbers](/catalan-numbers/): another family of non-crossing structures; they count, for example, the binary bracketings of a sentence, which is the corresponding count for constituency trees.
- Weaker conditions studied in the literature, such as bounded gap degree and well-nestedness, allow some crossing arcs but keep polynomial parsing.

## References
