---
title: Structural subsumption is sound and complete for FL- and runs in linear time
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, lines L1 to L12. FL- concepts are built from concept names, $\top$, $C \sqcap D$, $\forall r.C$ and $\exists r.\top$ (written $\exists r$). There is no TBox. A normal form node $x$ has a set $N_x$ of concept names, a set $E_x$ of roles and a partial map $V_x$ from roles to nodes. The concept of a node is

$$\mathrm{con}(x) = \mathop{\large\sqcap}_{A \in N_x} A \;\sqcap\; \mathop{\large\sqcap}_{r \in E_x} \exists r \;\sqcap\; \mathop{\large\sqcap}_{r \in \mathrm{dom}(V_x)} \forall r.\mathrm{con}(V_x(r)),$$

with the empty conjunction equal to $\top$. A node is empty when $N_x$, $E_x$ and $V_x$ are all empty; then $\mathrm{con}(x) = \top$.

## Termination

INSERT (lines L5 to L8) calls itself only on direct subconcepts, so it makes one call for each occurrence of a subconcept of $C$. PRUNE visits each node once. SUBSUMES (lines L9 to L12) calls itself only on $(V_c(r), V_d(r))$, one level deeper in both trees, so it stops after at most $\mathrm{rd}(D) + 1$ levels, where $\mathrm{rd}$ is the role depth. All three procedures stop.

## Lemma 1 (the normal form is equivalent)

For every FL- concept $C$, $\mathrm{con}(\mathrm{NORMALIZE}(C)) \equiv C$.

*Proof.* Before PRUNE, we show by induction on the INSERT calls that after INSERT$(x, C')$ the concept $\mathrm{con}(x)$ is equivalent to the old $\mathrm{con}(x) \sqcap C'$. For a name (L5) and for $\exists r$ (L6) this is the definition of con. For $C_1 \sqcap C_2$ (L7) it follows from two applications of the induction hypothesis. For $\forall r.D$ (L8), the call changes only the child $y = V_x(r)$, and by induction $\mathrm{con}(y)$ becomes $\mathrm{con}(y) \sqcap D$ (a new child starts empty, with concept $\top$). The equivalence $\forall r.(Y \sqcap D) \equiv \forall r.Y \sqcap \forall r.D$ holds in every interpretation: an element has all its $r$-successors in $Y \cap D$ exactly when it has them all in $Y$ and all in $D$. For $\top$ nothing changes and $X \sqcap \top \equiv X$. The root starts empty (L1), so after L2 the root has concept equivalent to $C$.

PRUNE removes a child $V_x(r)$ only when its subtree is empty, so its concept is $\top$. Since $\forall r.\top \equiv \top$ (every successor is in the domain), the removal does not change the concept of $x$ up to equivalence. $\square$

From now on $c$ and $d$ are the pruned normal forms of $C$ and $D$. After PRUNE, every child is nonempty.

## Lemma 2 (soundness)

If SUBSUMES$(c, d)$ returns true, then $\mathrm{con}(c) \sqsubseteq \mathrm{con}(d)$.

*Proof.* By induction on the depth of $d$. Take an interpretation $I$ and $e \in \mathrm{con}(c)^I$. Line L9 passed, so $N_d \subseteq N_c$ and $E_d \subseteq E_c$; each name of $N_d$ and each $\exists r$ with $r \in E_d$ is a conjunct of $\mathrm{con}(c)$, so $e$ is in it. For each $r \in \mathrm{dom}(V_d)$, line L11 passed, so $V_c(r)$ exists and SUBSUMES$(V_c(r), V_d(r))$ is true. Each $r$-successor $f$ of $e$ is in $\mathrm{con}(V_c(r))^I$, because $\forall r.\mathrm{con}(V_c(r))$ is a conjunct of $\mathrm{con}(c)$. By induction $f \in \mathrm{con}(V_d(r))^I$. So $e \in (\forall r.\mathrm{con}(V_d(r)))^I$. All conjuncts of $\mathrm{con}(d)$ hold at $e$. $\square$

## Lemma 3 (completeness, with a counter-model)

Let TREE$(x)$ make an element $e$ with the names $N_x$ and, for each $r \in E_x$, one $r$-successor TREE$(V_x(r))$, or TREE of an empty node when $V_x(r)$ is undefined. Then $e \in \mathrm{con}(x)$ in the interpretation that is built.

If SUBSUMES$(c, d)$ returns false, then COUNTER$(c, d)$ of the implementation builds a finite tree interpretation with an element $e$ in $\mathrm{con}(c)$ and not in $\mathrm{con}(d)$. So $C \not\sqsubseteq D$.

*Proof.* For TREE, by induction on the depth of $x$: $e$ has the names of $N_x$; it has an $r$-successor for each $r \in E_x$; and for each $r \in \mathrm{dom}(V_x)$, every $r$-successor of $e$ is TREE$(V_x(r))$ (when $r \in E_x$) or there is none (when $r \notin E_x$), and in both cases every $r$-successor is in $\mathrm{con}(V_x(r))$. Elements get no other names or edges, and the tree has no edges back, so the evaluation of each subtree does not change.

For COUNTER, by induction on the depth of $d$. Case 1: line L9 fails. COUNTER returns TREE$(c)$, which is in $\mathrm{con}(c)$. Either a name $A \in N_d \setminus N_c$, and $e$ is not in $A$, or a role $r \in E_d \setminus E_c$, and $e$ has no $r$-successor, so $e \notin \exists r$. Case 2: line L11 fails for a role $r$. Let $c' = V_c(r)$, or an empty node if it is undefined, and $d' = V_d(r)$, which is nonempty after PRUNE. SUBSUMES$(c', d')$ is false. When $V_c(r)$ is defined, this is what L11 found. When it is undefined, $c'$ is empty and $d'$ is not: if $d'$ has a name or a role, L9 fails; otherwise $d'$ has a child, and L11 fails because $c'$ has none. COUNTER makes $e$ with the names $N_c$, one $s$-successor TREE$(V_c(s))$ for each $s \in E_c$ with $s \neq r$, and exactly one $r$-successor $f = $ COUNTER$(c', d')$. By induction $f \in \mathrm{con}(c')$ and $f \notin \mathrm{con}(d')$. So $e \in \mathrm{con}(c)$: the names hold, each $\exists s$ holds (for $s = r$ the successor is $f$), and every successor satisfies the matching value restriction. And $e \notin \forall r.\mathrm{con}(d')$, so $e \notin \mathrm{con}(d)$. $\square$

## Theorem

SUBSUMES(NORMALIZE$(C)$, NORMALIZE$(D)$) returns true if and only if $C \sqsubseteq D$.

*Proof.* By Lemma 1, $C \equiv \mathrm{con}(c)$ and $D \equiv \mathrm{con}(d)$. If the answer is true, Lemma 2 gives $C \sqsubseteq D$. If it is false, Lemma 3 gives an interpretation with an element in $C$ and not in $D$. $\blacksquare$

## Size of the counter-model

With one role name, the element of TREE$(x)$ has at most one successor, so TREE builds a path with at most $\mathrm{rd}(\mathrm{con}(x)) + 1$ elements. COUNTER also gives each element at most one successor, and each step goes one level deeper in $c$ or in $d$. So a counter-model exists with at most $\max(\mathrm{rd}(C), \mathrm{rd}(D)) + 1$ elements. The tests use this bound: for one role and role depth at most 2, a search over all interpretations with at most 3 elements decides subsumption.

## Running time

INSERT does a constant number of set or map operations for each occurrence of a constructor or name in $C$, so NORMALIZE takes $O(|C|)$ operations and makes at most $|C|$ nodes. SUBSUMES visits each node of $d$ at most once and pairs it with one node of $c$; the inclusion tests of L9 cost $O(|N_d| + |E_d|)$ lookups for that node. The total is $O(|C| + |D|)$ hash set operations, so $O(|C| + |D|)$ expected time, and $O(|C| + |D|)$ space.
