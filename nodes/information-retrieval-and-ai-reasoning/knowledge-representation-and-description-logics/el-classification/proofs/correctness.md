---
title: The completion rules for EL with bottom are sound and complete and run in polynomial time
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, lines L1 to L11. The logic is EL with $\bot$: concepts are built from concept names, $\top$, $\bot$, $C \sqcap D$ and $\exists r.C$. The TBox $T$ is a finite set of general concept inclusions. The proof follows Baader, Brandt and Lutz (2005), restricted to these constructors.

## Normal form

After the simplification ($C \sqcap \bot$ and $\exists r.\bot$ become $\bot$, and $\top$ is dropped from conjunctions), each inclusion $C \sqsubseteq D$ with $C \neq \bot$ and $D \neq \top$ is replaced as follows. For the left side, LEFT$(C)$ returns $C$ when it is a name or $\top$; for $C = C_1 \sqcap C_2$ it returns a fresh name $X$ and adds $\mathrm{LEFT}(C_1) \sqcap \mathrm{LEFT}(C_2) \sqsubseteq X$; for $C = \exists r.C_1$ it returns a fresh $X$ and adds $\exists r.\mathrm{LEFT}(C_1) \sqsubseteq X$. For the right side, RIGHT$(D)$ returns $D$ when it is a name, $\top$ or $\bot$; for $D_1 \sqcap D_2$ it returns a fresh $X$ and adds $X \sqsubseteq \mathrm{RIGHT}(D_1)$ and $X \sqsubseteq \mathrm{RIGHT}(D_2)$; for $\exists r.D_1$ it returns a fresh $X$ and adds $X \sqsubseteq \exists r.\mathrm{RIGHT}(D_1)$. Then it adds $\mathrm{LEFT}(C) \sqsubseteq \mathrm{RIGHT}(D)$. The result $T'$ has only the four forms $A \sqsubseteq B$, $A_1 \sqcap A_2 \sqsubseteq B$, $A \sqsubseteq \exists r.B$ and $\exists r.A \sqsubseteq B$, where $A, A_1, A_2$ are names or $\top$ and $B$ is a name, $\top$ or $\bot$.

**Lemma 1.** For concept names $A, B$ of $T$: $A \sqsubseteq_T B$ if and only if $A \sqsubseteq_{T'} B$. The same holds for satisfiability.

*Proof.* Every model of $T'$ is a model of $T$: by induction on the structure, $C^I \subseteq \mathrm{LEFT}(C)^I$ and $\mathrm{RIGHT}(D)^I \subseteq D^I$, so $C^I \subseteq \mathrm{LEFT}(C)^I \subseteq \mathrm{RIGHT}(D)^I \subseteq D^I$. Every model $I$ of $T$ becomes a model of $T'$ when each fresh name $X$ made by LEFT$(C)$ or RIGHT$(D)$ gets $X^I = C^I$ or $X^I = D^I$: each added axiom then reads $C_1^I \cap C_2^I \subseteq (C_1 \sqcap C_2)^I$, $(\exists r.C_1)^I \subseteq (\exists r.C_1)^I$, and so on, and the last one is $C^I \subseteq D^I$. Fresh names do not occur in $T$, so the extensions of the old names do not change. Hence the two TBoxes have the same models up to the fresh names, and they agree on all questions about old names. $\square$

Each constructor of $T$ gives at most one fresh name and at most two axioms, so $|T'| = O(|T|)$.

## Termination

Let $k$ be the number of names of $T'$, with $\top$. Every set $S(X)$ is a subset of these names and $\bot$, and every $R(r)$ is a set of pairs of names. The procedure ADD puts a pair $(X, B)$ on the queue only when $B$ is new in $S(X)$, and line L8 adds an edge only when it is new. Nothing is ever removed. So there are at most $k(k+1)$ queue items and at most $k^2$ edges for each role, and the loop of line L2 stops.

## Soundness

**Lemma 2 (invariant).** At every moment, $B \in S(X)$ implies $X \sqsubseteq_{T'} B$, and $(X, Y) \in R(r)$ implies $X \sqsubseteq_{T'} \exists r.Y$.

*Proof.* At line L1, $X \sqsubseteq X$ and $X \sqsubseteq \top$ hold. Each later addition follows from earlier facts and one axiom of $T'$, in every model $I$ of $T'$:

- L4 (CR1): $X \sqsubseteq A$ and $A \sqsubseteq B$ give $X \sqsubseteq B$.
- L5 (CR2): $X \sqsubseteq A$, $X \sqsubseteq A'$ and $A \sqcap A' \sqsubseteq B$ give $X \sqsubseteq B$.
- L6 and L8 (CR3): $X \sqsubseteq A$ and $A \sqsubseteq \exists r.B$ give $X \sqsubseteq \exists r.B$.
- L7 and L9 (CR4): $X \sqsubseteq \exists r.Y$, $Y \sqsubseteq A$ and $\exists r.A \sqsubseteq B$ give $X \sqsubseteq \exists r.A \sqsubseteq B$.
- L7 and L10 (CR5): $X \sqsubseteq \exists r.Y$ and $Y \sqsubseteq \bot$ give $X \sqsubseteq \exists r.\bot \equiv \bot$. $\square$

So when line L11 answers yes, either $A \sqsubseteq_{T'} B$, or $A \sqsubseteq_{T'} \bot \sqsubseteq B$. By Lemma 1 the answer is right for $T$.

## Completeness

**Lemma 3 (closure).** When the loop of line L2 stops, the sets are closed under the five rules: no rule can add anything.

*Proof.* Every element $A$ of $S(X)$ went through the queue once, and at that time lines L4 to L7 applied every axiom with $A$ on the left. CR1 and CR3 depend only on $A \in S(X)$, so they were applied. For CR2 with $A, A' \in S(X)$, the one of the two that came second off the queue found the other in $S(X)$ at line L5. For CR4 and CR5 with $(X, Y) \in R(r)$ and $A \in S(Y)$: if $A$ was in $S(Y)$ when the edge was added, lines L9 and L10 applied the rule; otherwise the edge was there when $(Y, A)$ came off the queue, and line L7 applied it. $\square$

Assume $\bot \notin S(\top)$. Build the canonical interpretation $I$: the domain has one element $d_X$ for each name $X$ (with $\top$) such that $\bot \notin S(X)$; $A^I = \{d_X : A \in S(X)\}$; and $r^I = \{(d_X, d_Y) : (X, Y) \in R(r)\}$ for elements of the domain. The domain holds $d_\top$, so it is not empty.

**Lemma 4.** $I$ is a model of $T'$.

*Proof.* Take an element $d_X$, so $\bot \notin S(X)$, and recall $\top \in S(X)$, so $d_X \in A^I$ if and only if $A \in S(X)$ also for $A = \top$.

- $A \sqsubseteq B$: if $A \in S(X)$, CR1 gives $B \in S(X)$. $B \neq \bot$, because $\bot \notin S(X)$. So $d_X \in B^I$.
- $A_1 \sqcap A_2 \sqsubseteq B$: in the same way with CR2.
- $A \sqsubseteq \exists r.B$: CR3 gives $(X, B) \in R(r)$. If $\bot \in S(B)$, CR5 would put $\bot$ in $S(X)$, so $d_B$ is in the domain, and $d_B \in B^I$ because $B \in S(B)$. So $d_X \in (\exists r.B)^I$.
- $\exists r.A \sqsubseteq B$: if $(d_X, d_Y) \in r^I$ and $d_Y \in A^I$, then $(X, Y) \in R(r)$ and $A \in S(Y)$, and CR4 gives $B \in S(X)$, with $B \neq \bot$ as before. $\square$

**Lemma 5.** At the end, $S(\top) \subseteq S(X)$ for every name $X$.

*Proof.* We show, by induction on the order in which the run added facts about $\top$, that $B \in S(\top)$ implies $B \in S(X)$, and that $(\top, Y) \in R(r)$ implies $(X, Y) \in R(r)$. We use that the final sets are closed (Lemma 3). The first fact $\top \in S(\top)$ holds for $X$ by line L1. If $B$ came into $S(\top)$ by CR1 or CR2 from elements of $S(\top)$, those elements are in $S(X)$ by induction, and closure under the same rule puts $B$ in $S(X)$. If $(\top, Y)$ came into $R(r)$ by CR3 from $A \in S(\top)$, then $A \in S(X)$ and closure gives $(X, Y) \in R(r)$. If $B$ came into $S(\top)$ by CR4 or CR5 from an edge $(\top, Y)$, then $(X, Y) \in R(r)$ by induction, and closure gives $B \in S(X)$. $\square$

**Theorem.** For concept names $A$ and $B$ of $T$, line L11 answers yes if and only if $A \sqsubseteq_T B$.

*Proof.* "Only if" is soundness. For "if", suppose the answer is no: $B \notin S(A)$ and $\bot \notin S(A)$. By Lemma 5, $\bot \notin S(\top)$, so $I$ is defined. By Lemma 4 it is a model of $T'$, and $d_A \in A^I$ because $A \in S(A)$, while $d_A \notin B^I$. So $A \not\sqsubseteq_{T'} B$, and by Lemma 1, $A \not\sqsubseteq_T B$. $\blacksquare$

For a subsumption $C \sqsubseteq_T D$ between EL concepts, add two fresh names $Q$ and $P$ with $Q \sqsubseteq C$ and $D \sqsubseteq P$. Then $C \sqsubseteq_T D$ holds if and only if $Q \sqsubseteq P$ holds for the larger TBox: one direction is the chain $Q \sqsubseteq C \sqsubseteq D \sqsubseteq P$, and for the other, a model of $T$ with an element in $C$ and not in $D$ becomes a model of the larger TBox with $Q^I = C^I$ and $P^I = D^I$.

## Running time

Let $n = |T|$, so $k = O(n)$ names and $O(n)$ axioms after normalization. With the axioms indexed by their left side, an item $(X, A)$ costs $O(1)$ for each axiom with $A$ on the left at lines L4 to L6, and $O(|\mathrm{pred}(X)|)$ at line L7, where $\mathrm{pred}(X)$ is the set of edges into $X$. Edges into $X$ come only from axioms $A \sqsubseteq \exists r.X$, so the total number of edges is at most $k \cdot n$. Over all items:

- Lines L4 to L6: each of the $k$ names $X$ meets each axiom at most once, $O(k \cdot n) = O(n^2)$.
- Line L7: $\sum_X |S(X)| \cdot |\mathrm{pred}(X)| \le (k + 1) \cdot k n = O(n^3)$.
- Lines L8 to L10: each of the $O(n^2)$ edges scans $S(Y)$ once, $O(n^3)$.

The time is $O(n^3)$ and the space for $S$ and $R$ is $O(n^2)$.
