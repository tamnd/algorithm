---
title: Gemini netlist comparison reports only real differences, and with backtracking it finds a match whenever one exists
proves: [correctness, termination, complexity]
status: full
---

We use the model and the pseudocode of the page. A netlist $G$ has a set $D$ of devices, a set $V$ of nets and a set of named nets. Each device $u$ has a type $\tau(u)$, and each pin of $u$ has a pin class and a net. For a device $u$ and a pin class $c$, let $N_c(u)$ be the multiset of nets on the pins of $u$ of class $c$. Two netlists $G$ and $G'$ are *isomorphic* when there are bijections $\pi : D \to D'$ and $\varphi : V \to V'$ such that

1. $\tau(\pi(u)) = \tau(u)$ and $\varphi(N_c(u)) = N_c(\pi(u))$ for every device $u$ and class $c$, and
2. a named net $v$ maps to the net $\varphi(v)$ with the same name, and an unnamed net to an unnamed net.

Write $f = \pi \cup \varphi$ for the map on all vertices of the bipartite device and net graph. The algorithm keeps one label $\lambda(x)$ for each vertex $x$ of $G$ and of $G'$, from one common set of labels.

**Definition.** A labeling is *sound* for a set of pairs $I = \{(x_1, y_1), \ldots, (x_r, y_r)\}$ if every isomorphism $f$ with $f(x_i) = y_i$ for all $i$ also has $\lambda(f(x)) = \lambda(x)$ for every vertex $x$ of $G$.

**Lemma 1 (the start is sound).** The labels of line L1 are sound for $I = \emptyset$.

*Proof.* A device gets its type, and an isomorphism keeps the type. A net gets its name (or the empty name) and its number of pins. An isomorphism keeps the name by condition 2. The number of pins of a net $v$ is the number of pairs (device $u$, pin of $u$) with net $v$, which is the sum over $u$ and $c$ of the multiplicity of $v$ in $N_c(u)$. By condition 1 it equals the same sum for $\varphi(v)$. $\square$

**Lemma 2 (relabeling keeps soundness).** If $\lambda$ is sound for $I$, then the labels after one pass of lines L4 to L6 are sound for $I$.

*Proof.* Line L4 gives a net $v$ the key $(\lambda(v), M(v))$ with $M(v)$ the multiset of the pairs $(c, \lambda(u))$ over the pins of class $c$ of the devices $u$ on $v$, one pair per pin. Take an isomorphism $f$ that agrees with $I$. By condition 1, the pins on $\varphi(v)$ are the images of the pins on $v$, with the same classes, and their devices are the images $\pi(u)$. By soundness $\lambda(\pi(u)) = \lambda(u)$, so $M(\varphi(v)) = M(v)$, and also $\lambda(\varphi(v)) = \lambda(v)$. So the keys of $v$ and $\varphi(v)$ are equal. Line L6 maps equal keys to equal labels, because it renumbers the keys of both netlists with one table. Line L5 is the same argument for devices, with the new net labels. $\square$

**Lemma 3 (individualization keeps soundness).** If $\lambda$ is sound for $I$ and $x$, $y$ have the same label, then the labeling that gives $x$ and $y$ one new label, used by no other vertex, is sound for $I \cup \{(x, y)\}$.

*Proof.* Take an isomorphism $f$ that agrees with $I$ and has $f(x) = y$. For a vertex $z \ne x$, $f(z) \ne y$, so neither $z$ nor $f(z)$ got the new label, and $\lambda(f(z)) = \lambda(z)$ as before. For $z = x$ both have the new label. $\square$

**Theorem 4 (a mismatch is real).** If the algorithm reports a mismatch at line L7 while the pairs $I$ are fixed, then no isomorphism agrees with $I$. In particular, a mismatch with $I = \emptyset$ proves that the netlists are not isomorphic, and the report names a label with more vertices on one side than on the other.

*Proof.* By Lemmas 1 to 3 the labeling is sound for $I$. An isomorphism $f$ that agrees with $I$ maps the vertices of $G$ with label $\ell$ one to one into the vertices of $G'$ with label $\ell$, and $f^{-1}$ does the same in the other direction, so the two counts are equal for every label. Line L7 fires only when some count differs. $\square$

**Lemma 5 (the stable map is an isomorphism).** Suppose that after line L8 every label has exactly one vertex in $G$ and one in $G'$. Let $f$ map each vertex of $G$ to the vertex of $G'$ with the same label. Then $f$ is an isomorphism.

*Proof.* $f$ maps devices to devices and nets to nets, because the two kinds are labeled in separate arrays, and it is a bijection on each kind. The loop stopped because one pass did not split any class, so every vertex has the same label as before the pass, and the label of a vertex now determines its key in the last pass. Take a device $u$ and $u' = f(u)$. Their keys are equal, so the multisets of pairs (class, net label) on their pins are equal. Each net label belongs to exactly one net of $G$ and one net of $G'$, which $f$ pairs, so $\varphi(N_c(u)) = N_c(u')$ for every class $c$. Types are kept since a device label always contains its type from line L1. A net and its image have equal labels, so they carry the same name by line L1. $\square$

The implementation also checks the map directly before it returns it, which is a second guard against a bug.

**Lemma 6 (termination of one refinement).** The loop of lines L3 to L8 runs at most $|D| + |V| + |D'| + |V'|$ passes.

*Proof.* The key of a vertex contains its old label, so two vertices with different labels keep different labels: each pass splits classes or leaves them unchanged. Line L8 stops the loop when the number of labels did not grow. While it grows, it grows by at least 1 per pass, and it cannot pass the number of vertices. $\square$

**Theorem 7 (completeness with backtracking).** If the netlists are isomorphic, the search with backtracking returns an isomorphism. Every returned map is an isomorphism.

*Proof.* The second statement is Lemma 5. For the first, we show by induction on the number of classes with two or more members that SEARCH returns a map when some isomorphism $f$ agrees with the current pairs $I$. By soundness, line L7 does not fire. If all classes are singletons on each side, line L9 returns a map. Else line L10 picks a class $K$ and a vertex $x \in K$ in $G$. By soundness $f(x)$ has the label of $x$, so $f(x)$ is one of the candidates $y$ of line L11. For $y = f(x)$, the call at line L12 runs with the pairs $I \cup \{(x, f(x))\}$, with which $f$ still agrees, so by Lemma 3 the labels stay sound. The new label of $x$ is a class of one member on each side, and $x$ came from a class of two or more, so the number of labels grows by at least 1. The depth of the search is at most the number of vertices of $G$, and by induction the call for $y = f(x)$ returns a map, which the loop returns. $\square$

**Without backtracking.** If line L11 tries only the first candidate, Theorem 4 still makes every reported mismatch at the top level real, but a mismatch that appears after a guess can be caused by the guess. The test file gives such a case: two netlists, each a ring of six resistors plus two rings of three, where every net has the same label until a guess, and the first guess pairs a net of the long ring with a net of a short ring. If for any two vertices $y$, $y'$ of $K$ in $G'$ some automorphism of $G'$ that fixes the vertices already paired in $I$ maps $y$ to $y'$, then every guess is as good as any other: if an isomorphism maps $x$ to $y$, its composition with that automorphism maps $x$ to $y'$. This is the usual case of identical cells in a layout.

**Complexity.** Let $n = |D|$, $m = |V|$ and $P$ the number of pins. One pass builds $n + m$ keys of total size $O(P)$ and sorts them, in $O(P \log P + (n + m) \log (n + m))$ time with comparisons of keys. By Lemma 6 one refinement makes at most $2(n + m)$ passes. A search without backtracking makes at most $n + m$ guesses, since each makes a new class, so it costs $O((n + m)^2 (P + n + m) \log (n + m))$ in the worst case. With backtracking the number of calls can be exponential in $n + m$: Neuen and Schweitzer (2018) give graphs on which every individualization and refinement method with color refinement visits exponentially many nodes.
