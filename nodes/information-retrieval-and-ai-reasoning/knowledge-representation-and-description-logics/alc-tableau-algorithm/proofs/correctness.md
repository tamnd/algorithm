---
title: The ALC tableau is sound, complete and terminates, with and without a general TBox
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, lines L1 to L15. All concepts are in negation normal form (NNF). $T$ is a TBox, and $\mathcal{C}_T = \{\mathrm{nnf}(\neg D \sqcup E) : D \sqsubseteq E \in T\}$ (line L1). Blocking is on when $T \neq \emptyset$.

Let $\mathrm{cl}$ be the set of all subconcepts of $\mathrm{nnf}(C)$ and of the concepts in $\mathcal{C}_T$, and let $m = |\mathrm{cl}|$. Then $m$ is at most the sum of the sizes of these concepts, so $m = O(n)$ for an input of size $n$.

**Lemma 0 (NNF).** For every concept $D$ and every interpretation $I$, $\mathrm{nnf}(D)^I = D^I$.

*Proof.* By induction on the size of $D$. The rules of nnf are the identities $(\neg \neg D)^I = D^I$, $(\neg(D \sqcap E))^I = (\neg D \sqcup \neg E)^I$, $(\neg(D \sqcup E))^I = (\neg D \sqcap \neg E)^I$, $(\neg \exists r.D)^I = (\forall r.\neg D)^I$, $(\neg \forall r.D)^I = (\exists r.\neg D)^I$, $(\neg \top)^I = \bot^I$ and $(\neg \bot)^I = \top^I$. Each one follows from the semantics: for example, $x \notin (\exists r.D)^I$ if and only if no $r$-successor of $x$ is in $D^I$, if and only if every $r$-successor of $x$ is in $(\neg D)^I$. Each rule calls nnf on smaller concepts, so the induction hypothesis applies. $\square$

**Lemma 1 (labels stay in cl).** Every label that the algorithm builds is a subset of $\mathrm{cl}$.

*Proof.* The root label is $\{\mathrm{nnf}(C)\} \cup \mathcal{C}_T \subseteq \mathrm{cl}$. Lines L11 and L14 add only a direct subconcept of a concept of the label. Line L6 puts in a child the subconcepts $D$ of $\exists r.D$ and $E$ of $\forall r.E$, and the concepts of $\mathcal{C}_T$. Since $\mathrm{cl}$ is closed under subconcepts, induction on the steps gives the claim. $\square$

## Termination

**Lemma 2 (COMPLETIONS stops).** A call COMPLETIONS$(S)$ makes at most $2^{m}$ recursive calls in total.

*Proof.* Line L14 makes a call only on $L \cup \{D\}$ with $D \notin L$, so each nested call has a label with at least one more element of $\mathrm{cl}$ than its caller. Labels have at most $m$ elements (Lemma 1), so the nesting depth is at most $m$, and each call makes at most 2 calls. $\square$

**Lemma 3 (depth without a TBox).** If $T = \emptyset$, a node at depth $d$ has a label of role depth at most $\mathrm{rd}(\mathrm{nnf}(C)) - d$. So the depth of the tree is at most $\mathrm{rd}(\mathrm{nnf}(C))$.

*Proof.* The ⊓-rule and the ⊔-rule add subconcepts, which do not have a larger role depth. A child label (line L6, with $\mathcal{C}_T = \emptyset$) holds only concepts $D$ with $\exists r.D$ or $\forall r.D$ in the parent label, and each has a role depth at least 1 smaller than the parent concept. So the largest role depth drops by at least 1 at each level. A label with role depth 0 has no $\exists r.D$, so line L5 makes no child. $\square$

**Lemma 4 (depth with blocking).** If blocking is on, every path from the root has at most $2^{m}$ nodes that are expanded.

*Proof.* Let $v$ be a node that line L8 expands, with initial label $S_v$, and let $u$ be an ancestor of $v$ with initial label $S_u$ and completed label $L_u$. Line L7 did not block $v$, so $S_v \not\subseteq L_u$. COMPLETIONS only adds concepts, so $S_u \subseteq L_u$, and so $S_v \neq S_u$. Thus the initial labels on one path are pairwise different subsets of $\mathrm{cl}$, and there are at most $2^m$ of them. The number of subsets of $\mathrm{cl}$ that are not yet used on the path drops by exactly 1 at each level. $\square$

**Theorem 1 (termination).** SAT$(C, T)$ stops. With $T = \emptyset$ the run takes at most $2^{O(n^2)}$ steps. With blocking it takes at most $2^{2^{O(n)}}$ steps.

*Proof.* A completed label has at most $m$ concepts of the form $\exists r.D$, so line L5 makes at most $m$ calls for one completion. By Lemma 2 there are at most $2^m$ completions of one label, each built in time polynomial in $m$. Let $N(h)$ be the largest number of steps of a call of NODE whose subtree has height at most $h$. Then $N(h) \le 2^m \cdot (p(m) + m \cdot N(h - 1))$ for a polynomial $p$, so $N(h) \le (2^m (p(m) + m))^{h + 1}$. With $T = \emptyset$, Lemma 3 gives $h \le \mathrm{rd}(\mathrm{nnf}(C)) \le m$, so the time is $2^{O(m^2)} = 2^{O(n^2)}$. With blocking, Lemma 4 gives $h \le 2^m$, so the time is $2^{O(m \cdot 2^m)} = 2^{2^{O(n)}}$. Both bounds are finite. $\square$

## Soundness

**Theorem 2 (soundness).** If SAT$(C, T)$ returns true, then the interpretation $I$ built from the successful calls is a model of $T$ in which the root is an instance of $C$.

*Proof.* A call of NODE that returns true does so at line L9 for one completion $L$, its last one, and each call that line L8 made for $L$ returned true. Take as nodes the root call and, below each node, the calls of line L8 made for its last completion. Call this the tree of successful calls. Each node $u$ in it was called with the last completions of all its ancestors in $P$, because a call for an earlier completion of an ancestor is not in the tree. The tree has these properties, by lines L3 to L9:

- (P1) Each node $u$ has a label $L_u$, its last completion, that COMPLETIONS yielded. So $L_u$ has no clash (line L12): $\bot \notin L_u$, and no $A$ with $A, \neg A \in L_u$. It is closed under ⊓: if $D \sqcap E \in L_u$ then $D, E \in L_u$ (line L11). It is complete for ⊔: if $D \sqcup E \in L_u$ then $D \in L_u$ or $E \in L_u$ (lines L13 and L15).
- (P2) $\mathcal{C}_T \subseteq L_u$ for each node $u$, because each initial label holds $\mathcal{C}_T$ (lines L2 and L6) and COMPLETIONS only adds concepts.
- (P3) For each $\exists r.D \in L_u$, line L7 or line L8 gives an edge $u \xrightarrow{r} t$, where $t$ is the child call of line L8, or the node whose label blocks the child at line L7. In both cases $S \subseteq L_t$ for the set $S$ of line L6. Every edge comes from this step.

A blocking label is in $P + [L_u]$, so it is the label of $u$ or of an ancestor of $u$, and by the remark above it is the last completion of that node. So $t$ is a node of the tree, and $S \subseteq L_t$. Let $\Delta^I$ be the set of nodes, $A^I = \{u : A \in L_u\}$ and $r^I$ the set of $r$-edges.

Claim: for every node $u$ and every $D \in L_u$, $u \in D^I$. The proof is by induction on the size of $D$.

- $D = \top$: true. $D = \bot$: impossible by (P1). $D = A$: by the definition of $A^I$. $D = \neg A$: $A \notin L_u$ by (P1), so $u \notin A^I$.
- $D = D_1 \sqcap D_2$: both are in $L_u$ by (P1), and the induction hypothesis applies.
- $D = D_1 \sqcup D_2$: one of them is in $L_u$ by (P1).
- $D = \exists r.E$: by (P3) there is an edge $u \xrightarrow{r} t$ with $E \in S \subseteq L_t$, so $t \in E^I$ by the induction hypothesis, and $u \in D^I$.
- $D = \forall r.E$: each $r$-successor $t$ of $u$ in $I$ comes from an edge of (P3), made for some $\exists r.D' \in L_u$. Its set $S$ holds every $E'$ with $\forall r.E' \in L_u$, so $E \in S \subseteq L_t$, and $t \in E^I$ by the induction hypothesis.

The root label holds $\mathrm{nnf}(C)$, so the root is in $\mathrm{nnf}(C)^I = C^I$ (Lemma 0). For an inclusion $D \sqsubseteq E$ of $T$ and any node $u$, (P2) and the claim give $u \in \mathrm{nnf}(\neg D \sqcup E)^I = \Delta^I \setminus D^I \cup E^I$. So $D^I \subseteq E^I$, and $I$ is a model of $T$. $\square$

The model has as many elements as the tree of successful calls has nodes, so it is finite. This also proves the finite model property of ALC with general TBoxes.

## Completeness

**Theorem 3 (completeness).** If $C$ has an instance in some model $J$ of $T$, then SAT$(C, T)$ returns true.

*Proof.* Say that an element $x \in \Delta^J$ *satisfies* a set $S$ when $x \in D^J$ for all $D \in S$. Every element of $J$ satisfies $\mathcal{C}_T$: for $D \sqsubseteq E \in T$, $D^J \subseteq E^J$, so each element is in $(\neg D \sqcup E)^J = \mathrm{nnf}(\neg D \sqcup E)^J$ (Lemma 0).

Step 1. If $x$ satisfies $S$, then COMPLETIONS$(S)$ yields at least one label that $x$ satisfies. By induction on the depth of recursion that is left, which is finite by Lemma 2. The closure of line L11 keeps the property, since $x \in (D \sqcap E)^J$ gives $x \in D^J$ and $x \in E^J$. Then line L12 finds no clash, because $x \notin \bot^J$ and $x$ cannot be in both $A^J$ and $(\neg A)^J$. If line L13 picks $D \sqcup E$, then $x \in D^J$ or $x \in E^J$, so one of the two calls of line L14 gets a set that $x$ satisfies, and the induction hypothesis gives a label. Otherwise line L15 yields $L$ itself.

Step 2. If $x$ satisfies $S$, then NODE$(S, P)$ returns true, for every list $P$ of ancestors. By induction on the height of the recursion below this call, which is finite by Theorem 1. By Step 1 the loop of line L3 reaches a completion $L$ that $x$ satisfies, unless it returned true for an earlier completion, and then we are done. For each $\exists r.D \in L$, $x$ has an $r$-successor $y$ in $D^J$. Then $y$ is in $E^J$ for every $\forall r.E \in L$, and $y$ satisfies $\mathcal{C}_T$, so $y$ satisfies the set $S'$ of line L6. If line L7 blocks the child, the loop goes on. Otherwise the induction hypothesis says that NODE$(S', \ldots)$ returns true. So no call fails, the loop of line L5 ends with $ok = $ true, and line L9 returns true.

The element of $J$ in $C^J$ satisfies $\{\mathrm{nnf}(C)\} \cup \mathcal{C}_T$ (Lemma 0), so line L2 returns true. $\square$

**Corollary.** SAT$(C, T)$ returns true if and only if $C$ is satisfiable with respect to $T$. So $C \sqsubseteq_T D$ holds if and only if SAT$(C \sqcap \neg D, T)$ returns false.

## Space with an empty TBox

With $T = \emptyset$ the recursion has depth at most $\mathrm{rd}(\mathrm{nnf}(C)) \le m$ (Lemma 3). Each level of NODE holds its list of ancestors, one completed label of at most $m$ concepts, and the stack of COMPLETIONS, which has at most $m$ open calls (Lemma 2), each with a label of at most $m$ concepts. A concept in a label is a reference to a subtree of the input. So the space is $O(m^3) = O(n^3)$ words, and the procedure runs in polynomial space. This gives the upper bound of the theorem that ALC concept satisfiability without a TBox is PSPACE-complete (Schmidt-Schauß and Smolka 1991; see [ALC is PSPACE-complete](/alc-pspace-completeness/)). With blocking, the list of ancestors can hold $2^m$ labels, so this bound does not hold.

## The bounds of the problem

The bounds above are bounds of this algorithm. The problem has these exact bounds.

- Empty TBox: PSPACE-complete. The upper bound is the space bound above. Schmidt-Schauß and Smolka (1991) also prove the lower bound, and it also follows from the PSPACE-hardness of the modal logic K (Ladner 1977) by the correspondence of Schild (1991). See [ALC is PSPACE-complete](/alc-pspace-completeness/).
- General TBox: EXPTIME-complete (Schild 1991, from the EXPTIME-hardness of propositional dynamic logic by Fischer and Ladner 1979, and the EXPTIME upper bound of Pratt 1979). See [ALC with general TBoxes is EXPTIME-complete](/alc-general-tbox-exptime/). The search of this page takes $2^{2^{O(n)}}$ time on such inputs (Theorem 1), so it is not worst-case optimal. Global caching of labels brings it to $2^{O(n)}$ (Donini and Massacci 2000, Goré and Nguyen 2013). The Description Logic Handbook (second edition, Chapter 2, Section 2.3, and Chapter 3) and Baader, Horrocks, Lutz and Sattler (2017, Chapter 4, Section 4.2, and Chapter 5) give both results.
