---
title: ALC concept satisfiability without a TBox is PSPACE-complete
proves: [statement]
status: full
---

ALC concepts are built from concept names $A$, $\top$ and $\bot$ with $\neg$, $\sqcap$, $\sqcup$, $\exists r$ and $\forall r$ for role names $r$. The size $|C|$ is the number of symbols. There is no TBox. A concept is satisfiable if $C^I \ne \emptyset$ in some interpretation $I$.

## Upper bound

Put $C$ in negation normal form; this is linear time and at most doubles the size. Let $\mathrm{sub}(C)$ be its set of subconcepts, so $|\mathrm{sub}(C)| \le 2|C|$. For a set $S \subseteq \mathrm{sub}(C)$, a *completion* of $S$ is a set $S'$ with $S \subseteq S' \subseteq \mathrm{sub}(C)$ such that

- $D \sqcap E \in S'$ implies $D \in S'$ and $E \in S'$;
- $D \sqcup E \in S'$ implies $D \in S'$ or $E \in S'$;
- $\bot \notin S'$, and there is no name $A$ with both $A$ and $\neg A$ in $S'$.

For $\exists r.D \in S'$, the *successor set* is $\mathrm{succ}(S', \exists r.D) = \{D\} \cup \{E : \forall r.E \in S'\}$. The procedure is

    SAT(S): for each completion S' of S, in a fixed order:
                if SAT(succ(S', ∃r.D)) holds for every ∃r.D in S', return true
            return false

Every concept of a successor set has smaller role depth than the existential or value restriction it came from, so the recursion depth is at most the role depth of $C$ plus one, and SAT stops.

**Lemma 1 (soundness).** If SAT$(S)$ returns true, some interpretation has an element in every concept of $S$.

*Proof.* By induction on the largest role depth $k$ in $S$. Let $S'$ be the completion that succeeded, and for each $\exists r.D \in S'$ let $I_{r,D}$ be an interpretation with an element $e_{r,D}$ in every concept of the successor set, given by induction. Take the disjoint union of the $I_{r,D}$, add a new element $d$, put $d$ in $A$ exactly when $A \in S'$, and add the edges $(d, e_{r,D})$ to $r$. Then $d \in E^I$ for every $E \in S'$, by induction on $E$. A name $A \in S'$ holds at $d$ by construction; for $\neg A \in S'$, $A \notin S'$ because $S'$ has no clash, so $d \notin A^I$. Conjunctions and disjunctions follow from the first two conditions. For $\exists r.D \in S'$ the element $e_{r,D}$ is an $r$-successor in $D$. For $\forall r.E \in S'$, the $r$-successors of $d$ are exactly the elements $e_{r,D}$, and each of them is in $E$ because $E$ is in its successor set. The concepts of the parts $I_{r,D}$ do not change in the union, because $d$ has no incoming edges. $\square$

**Lemma 2 (completeness).** If some interpretation $I$ has an element $d$ in every concept of $S$, then SAT$(S)$ returns true.

*Proof.* By induction on the largest role depth in $S$. The set $S' = \{E \in \mathrm{sub}(C) : d \in E^I\}$ is a completion of $S$: it contains $S$, it satisfies the two closure conditions by the semantics of $\sqcap$ and $\sqcup$, and it has no clash. The loop reaches $S'$ unless an earlier completion succeeds. For $\exists r.D \in S'$, $d$ has an $r$-successor $e \in D^I$, and $e \in E^I$ for every $\forall r.E \in S'$, so $e$ is in every concept of the successor set, and by induction SAT returns true on it. $\square$

By the two lemmas, $C$ is satisfiable if and only if SAT$(\{C\})$ returns true.

**Space.** A call keeps its current completion as a bit vector of length $|\mathrm{sub}(C)|$, which also serves as the counter of the loop over all subsets, and the position of the current existential restriction. That is $O(|C|)$ bits for each of the at most $|C| + 1$ active calls, so the procedure runs in $O(|C|^2)$ space. The problem is in PSPACE.

## Lower bound

We reduce the truth of quantified Boolean formulas, which is PSPACE-complete, to concept satisfiability. Let $\varphi = Q_1 p_1 \dots Q_m p_m.\, \psi$ with $Q_i \in \{\forall, \exists\}$ and $\psi$ propositional over $p_1, \dots, p_m$. Use one role $r$, concept names $P_1, \dots, P_m$, and write $\forall r^i.E$ for $E$ under $i$ nested $\forall r$. Let $C_\varphi$ be the conjunction of

1. $\forall r^{i}.(\exists r.P_{i+1} \sqcap \exists r.\neg P_{i+1})$ for each $i < m$ with $Q_{i+1} = \forall$, and $\forall r^{i}.\exists r.\top$ for each $i < m$ with $Q_{i+1} = \exists$;
2. $\forall r^{i}.\big((\neg P_j \sqcup \forall r.P_j) \sqcap (P_j \sqcup \forall r.\neg P_j)\big)$ for each $i < m$ and each $j \le i$;
3. $\forall r^{m}.\psi'$, where $\psi'$ is $\psi$ with each $p_j$ replaced by $P_j$, $\wedge$ by $\sqcap$, $\vee$ by $\sqcup$ and negation by $\neg$.

There are $O(m^2)$ conjuncts of size $O(m + |\psi|)$, so $C_\varphi$ is built in polynomial time.

**Lemma 3.** $\varphi$ is true if and only if $C_\varphi$ is satisfiable.

*Proof.* Suppose $\varphi$ is true. Build a tree of depth $m$ in which a node at depth $i$ stands for an assignment to $p_1, \dots, p_i$ under which the rest of the formula, $Q_{i+1} p_{i+1} \dots Q_m p_m.\, \psi$, is true. The root stands for the empty assignment. A node at depth $i < m$ gets two children, with $p_{i+1}$ true and false, when $Q_{i+1} = \forall$, and one child with a value of $p_{i+1}$ that keeps the rest true when $Q_{i+1} = \exists$; edges are in $r$. Put a node in $P_j$ when its assignment makes $p_j$ true. The root is in every conjunct: the nodes at depth $i$ have the children that item 1 asks for, children keep the values of the parent as item 2 asks, and the leaves satisfy $\psi$, which is item 3.

Conversely, let $d \in C_\varphi^I$. Say that $e$ is *at depth* $i$ if some $r$-path of length $i$ leads from $d$ to $e$; then $e$ satisfies every concept $E$ for which $\forall r^i.E$ is a conjunct. For $e$ at depth $i$, let $\alpha_e$ assign to $p_j$, $j \le i$, the value of $e \in P_j^I$. We show by induction on $m - i$ that $Q_{i+1} p_{i+1} \dots Q_m p_m.\, \psi$ is true under $\alpha_e$. For $i = m$, $e \in \psi'^I$, so $\psi$ is true under $\alpha_e$. For $i < m$, every $r$-successor $e'$ of $e$ is at depth $i + 1$, and by item 2 at $e$ it agrees with $e$ on $P_1, \dots, P_i$, so $\alpha_{e'}$ extends $\alpha_e$. If $Q_{i+1} = \forall$, item 1 gives successors with $p_{i+1}$ true and with $p_{i+1}$ false, and the formula is true under both extensions by induction. If $Q_{i+1} = \exists$, item 1 gives one successor, and the formula is true under its extension. At $i = 0$, $e = d$ and $\varphi$ is true. $\square$

So concept satisfiability is PSPACE-hard, already with a single role name.

## Subsumption

$C \sqsubseteq D$ holds if and only if $C \sqcap \neg D$ is unsatisfiable, and $C$ is satisfiable if and only if $C \not\sqsubseteq \bot$. These are polynomial reductions both ways between satisfiability and the complement of subsumption. PSPACE is closed under complement, so subsumption is PSPACE-complete too. $\blacksquare$
