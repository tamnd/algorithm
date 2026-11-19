---
title: Stripping undoes parent annotation, and the annotated parse of a sentence maps to exactly one plain parse
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page: ANNOTATE (lines L1 to L7) and STRIP (line L8). A tree is a finite ordered tree whose leaves are words and whose internal nodes carry labels. A preterminal is an internal node whose only child is a word. Let $\#$ be the separator (the code uses ^), and assume that no label of the input tree contains $\#$; the code checks this and raises an error otherwise. Write $\mathrm{base}(x)$ for the part of a label $x$ before its first $\#$, or $x$ itself if it has none.

## Lemma 1: the shape is kept

ANNOTATE stops, and its output has the same shape as its input: there is a bijection $\phi$ from the nodes of $t$ to the nodes of $A(t) = \text{ANNOTATE}(t)$ that keeps the root, the order of the children and the words. For every node $u$ with parent $v$, the label of $\phi(u)$ is $\mathrm{label}(u)$ if $u$ is a preterminal (in the default mode), and $\mathrm{label}(u)\,\#\,\mathrm{label}(v)$ otherwise. The root gets $\mathrm{label}(\text{root})\,\#\,\text{ROOT}$.

*Proof.* Each node of $t$ is pushed exactly once: the root at line L1, and every other node at line L6, when its parent is popped. A preterminal is copied whole at line L4 and its word child is not pushed. So the loop of line L2 runs once per internal node of $t$ and stops. At line L3 the pair $(u, p)$ has $p = \mathrm{label}(v)$ for the parent $v$ of $u$, because line L6 pushes each child with the label of the node just popped, and $p = \text{ROOT}$ for the root. Line L5 or L4 appends the copy of $u$ to the list of children of the copy of $v$. The children of $v$ are pushed in reverse order, so the first child is popped first. All nodes pushed after it lie in its subtree, so the second child is popped only after the whole subtree of the first child, and so on. Hence the copies of the children of $v$ are appended in their original order. This defines $\phi$ and proves the claim. $\square$

## Theorem 1: STRIP undoes ANNOTATE

$\text{STRIP}(\text{ANNOTATE}(t)) = t$ for every tree $t$ whose labels do not contain $\#$. This also holds when the preterminals are annotated.

*Proof.* STRIP has the same walk as ANNOTATE, so by the argument of Lemma 1 it keeps the shape and replaces each label $x$ by $\mathrm{base}(x)$. By Lemma 1, each label of $A(t)$ is $\mathrm{label}(u)$ or $\mathrm{label}(u)\,\#\,p$ for the corresponding node $u$ of $t$. Since $\mathrm{label}(u)$ contains no $\#$, in both cases $\mathrm{base}$ returns $\mathrm{label}(u)$. $\square$

## Theorem 2: annotated parses map to plain parses

Let $G'$ be the grammar read off the annotated treebank, and let $G$ be the grammar read off the plain treebank. Every rule $X\#P \to Y_1\#X \cdots Y_k\#X$ of $G'$ maps under $\mathrm{base}$ to a rule $X \to Y_1 \cdots Y_k$ of $G$, and every parse of a sentence $w$ under $G'$ is mapped by STRIP to a parse of $w$ under $G$. Conversely, ANNOTATE maps every parse of $w$ under $G$ to exactly one tree over the annotated labels, and STRIP maps that tree back. So the parses that the annotated grammar can return, after stripping, are among the parses of the plain grammar, and two different annotated parses that are both images of ANNOTATE strip to two different plain parses.

*Proof.* A rule of $G'$ comes from a node $\phi(u)$ of some $A(t)$. Its left side is $\mathrm{label}(u)\,\#\,p$ and its right side lists the labels of the copies of the children of $u$, which by Lemma 1 are the labels of the children of $u$, annotated or not. Applying $\mathrm{base}$ gives the rule that $u$ uses in $t$, which is a rule of $G$. A parse under $G'$ uses only rules of $G'$, so after STRIP, which keeps the shape and the words, it uses only rules of $G$ and has the same yield $w$. ANNOTATE is a function, so it maps a plain tree to one annotated tree, and by Theorem 1 two different plain trees have different annotations. $\blacksquare$

The converse direction is not onto: an annotated tree whose labels do not follow the parent pattern, such as a child $Y\#Z$ under a node $X\#P$ with $Z \ne X$, is never produced by ANNOTATE. Grammars read off annotated trees contain no such rules, so a parser with $G'$ only builds trees that follow the pattern.
