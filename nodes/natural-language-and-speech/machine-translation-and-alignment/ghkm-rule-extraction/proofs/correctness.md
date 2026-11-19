---
title: GHKM finds the frontier nodes, and its minimal rules derive the given tree and source sentence
proves: [correctness]
status: full
---

The input is a parse tree $T$ of the target sentence $e = e_1 \ldots e_l$, whose leaves in order are the positions $1, \ldots, l$, a source sentence $f = f_1 \ldots f_m$, and a set $A$ of links $(j, i)$ between source position $j$ and target position $i$. Only internal nodes of $T$ are considered as nodes below. For a node $n$, let $Y(n)$ be the set of leaf positions under $n$, and

$$\mathrm{span}(n) = \{j : (j, i) \in A, i \in Y(n)\}, \qquad \mathrm{comp}(n) = \{j : (j, i) \in A, i \notin Y(n)\}.$$

Write $\mathrm{cl}(S) = \{\min S, \ldots, \max S\}$ for the closure of a non-empty set of positions. The node $n$ is a *frontier node* if $\mathrm{span}(n) \ne \emptyset$ and $\mathrm{cl}(\mathrm{span}(n)) \cap \mathrm{comp}(n) = \emptyset$.

**Lemma 1 (lines L1 to L3 compute these sets).** After line L1, $\mathrm{span}[n] = \mathrm{span}(n)$; after line L2, $\mathrm{comp}[n] = \mathrm{comp}(n)$; line L3 marks exactly the frontier nodes.

*Proof.* Line L1 goes over the nodes children first, and sets the span of a node to the union of the spans of its children and of its leaf children, so by induction it is the set of positions aligned to $Y(n)$. Line L2 goes over the nodes parents first. The root has $Y = \{1, \ldots, l\}$, so $\mathrm{comp} = \emptyset$. For a child $k$ of $n$, the leaves outside $Y(k)$ are the leaves outside $Y(n)$ and the leaves under the other children of $n$, so $\mathrm{comp}(k)$ is $\mathrm{comp}(n)$ together with the spans of the siblings, which is what line L2 sets. Line L3 tests the definition. $\square$

The test file checks Lemma 1 against a second form of the definition: $n$ is a frontier node if and only if it has an aligned leaf, and every link whose source lies in $\mathrm{cl}(\mathrm{span}(n))$ has its target in $Y(n)$. The two forms agree, because a position of $\mathrm{cl}(\mathrm{span}(n))$ is in $\mathrm{comp}(n)$ exactly when it has a link to a target outside $Y(n)$.

For a frontier node $n$, line L5 builds the fragment: it walks down from $n$ and stops at frontier nodes (which become the variables $x_0, x_1, \ldots$ in tree order) and at leaves (which become words). Let $V(n)$ be its variable nodes. Line L6 sets the range $R(n) = \mathrm{cl}(\mathrm{span}(n))$, or $\{1, \ldots, m\}$ for the root.

**Lemma 2 (the variables have disjoint closures inside the range).** For $v \in V(n)$, $\mathrm{cl}(\mathrm{span}(v)) \subseteq R(n)$. For distinct $v, v' \in V(n)$, $\mathrm{cl}(\mathrm{span}(v)) \cap \mathrm{cl}(\mathrm{span}(v')) = \emptyset$. Every aligned position in $R(n)$ that is not in a closure of a variable is aligned to a leaf of the fragment.

*Proof.* $\mathrm{span}(v) \subseteq \mathrm{span}(n)$ because $Y(v) \subseteq Y(n)$, so its closure lies in the closure of $\mathrm{span}(n)$, which is in $R(n)$. Neither of $v, v'$ is below the other (the fragment stops at the first frontier node), so $Y(v') \cap Y(v) = \emptyset$ and $\mathrm{span}(v') \subseteq \mathrm{comp}(v)$. Since $v$ is a frontier node, $\mathrm{cl}(\mathrm{span}(v))$ holds no point of $\mathrm{span}(v')$, in particular neither end of $\mathrm{cl}(\mathrm{span}(v'))$; by symmetry the converse holds too. Two intervals that do not contain an end of each other are disjoint. For the last claim, let $j \in R(n)$ be aligned to some target $i$. If $n$ is not the root, $j \notin \mathrm{comp}(n)$ because $n$ is a frontier node, so every link of $j$ has its target in $Y(n)$. If $n$ is the root, every target is in $Y(n)$. A leaf in $Y(n)$ is under some $v \in V(n)$ or is a leaf of the fragment. If $i \in Y(v)$, then $j \in \mathrm{span}(v)$. $\square$

So line L7 is well defined: it walks over $R(n)$ from left to right, writes $x_q$ once for the closure of the variable $v_q$ and jumps over it, and writes the source word $f_j$ for every other position. Each variable occurs exactly once on each side.

**Theorem.** Let $\rho(n)$ be the rule of the frontier node $n$. If $A \ne \emptyset$, the root is a frontier node, and substituting, for each variable $x_q$ of $\rho(n)$, the result of the rule of $v_q$, recursively, gives from $\rho(\mathrm{root})$ the tree $T$ on the target side and the sentence $f$ on the source side. If $A = \emptyset$, no node is a frontier node and there are no rules.

*Proof.* The root has $\mathrm{comp} = \emptyset$ and a non-empty span if $A \ne \emptyset$, so it is a frontier node; with $A = \emptyset$ every span is empty. Target side: by induction from the bottom, substituting the subtree of $v_q$ at the variable $x_q$ in the fragment of $n$ gives the subtree of $n$, because the fragment is the subtree of $n$ cut at the variables. Source side: by induction from the bottom, the rule of a frontier node $v$ derives the words $f_j$ for $j \in R(v)$ in order: the rule writes the positions of $R(v)$ from left to right, with the closure of each variable replaced by that variable, and by induction the variable derives exactly the words of its closure, which is its range. For the root, $R = \{1, \ldots, m\}$, so the result is $f$. $\square$

**Unaligned words.** A source position that is not aligned lies in the range of the root. It is written by the rule of the lowest frontier node whose range holds it, because a node writes a position of its range unless the position is inside the closure of one of its variables, where the variable's rule takes it. This is one fixed choice. Galley et al. (2006) keep every possible attachment instead.

**Cost.** Lines L1 to L3 cost $O(|T| \cdot m)$ with sets of size up to $m$. Each node is in at most one fragment as an inner node, and each range has at most $m$ positions, so lines L4 to L8 cost $O(|T| + F m)$ with $F$ the number of frontier nodes.
