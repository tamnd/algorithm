---
title: Ordered resolution with selection is sound and refutation complete, and the loop stops on ground input
proves: [correctness, termination]
status: full
---

We use the pseudocode and the definitions of the page, and the proof for [Robinson's resolution principle](/robinson-resolution/), whose lemmas we cite by number. A clause is a finite set of literals. $C$ **subsumes** $D$ (multiset subsumption) when $C\rho \subseteq D$ for a substitution $\rho$ that maps distinct literals of $C$ to distinct literals of $D$. This relation is transitive, because a composition of injective maps is injective, and a clause subsumes each of its variants.

**The ordering.** The atom ordering $\succ$ is well-founded, total on ground atoms, and stable: $A \succ B$ implies $A\theta \succ B\theta$. The Knuth-Bendix ordering with positive weights and a total precedence has these three properties. Literals are ordered by $K \succ L$ when the atom of $K$ is greater than the atom of $L$, or when $K = \neg A$ and $L = A$. This is the multiset extension of the page, it is total and well-founded on ground literals, and it is stable, since in the first case the atoms stay ordered under $\theta$ and in the second case $\neg A\theta \succ A\theta$. A **ground clause** below is a finite multiset of ground literals. Ground clauses are ordered by the multiset extension of the literal order, which is total and well-founded. We use three facts about it.

- (M1) If $G \subseteq G'$ as multisets, then $G \preceq G'$.
- (M2) If $G'$ comes from $G$ by removing one copy of a literal $L$ and adding finitely many literals that are each smaller than $L$, then $G' \prec G$.
- (M3) If $G \preceq G'$ and $G \ne \square$, then $\max G \preceq \max G'$.

**Herbrand interpretations.** Let $H$ be the set of ground terms over the function symbols of $S$, with one constant added if $S$ has none. Every derived clause uses only symbols of $S$. A set $I$ of ground atoms is a Herbrand interpretation, and it satisfies a clause $C$ when, for every substitution $\tau$ from the variables of $C$ to $H$, the ground clause $C\tau = \{L\tau : L \in C\}$, read as a multiset, has a true literal. A set of clauses with a Herbrand model is satisfiable.

**Theorem.** Run the loop on a finite set $S$ of clauses.

1. If it returns UNSAT, then $S$ is unsatisfiable.
2. If it returns SATURATED, then $S$ is satisfiable.
3. If $S$ is unsatisfiable and there is no limit, then it returns UNSAT.
4. If $S$ is ground, it stops.

Part 1 holds because an ordered resolvent is a binary resolvent and an ordered factor is a factor, and these follow from their parents (Lemma 1 of the proof for Robinson's resolution principle).

## The model of a saturated set

Call a set $P$ of clauses **saturated** when every ordered factor of a clause of $P$, and every ordered resolvent of two clauses of $P$ (a clause and a renamed copy of itself included), is a tautology or is subsumed by a clause of $P$.

**Lemma 1.** If $P$ is saturated and $\square \notin P$, then $P$ has a Herbrand model.

*Proof.* Let $\mathcal{G}$ be the set of ground clauses $C\tau$ with $C \in P$ and $\tau$ from the variables of $C$ to $H$. Call $G \in \mathcal{G}$ **free** when $G = C\tau$ for some $C \in P$ with nothing selected in $C$. By well-founded recursion on the order of ground clauses, define for each $G \in \mathcal{G}$ the set $I_G$ of the atoms produced by the clauses $G' \in \mathcal{G}$ with $G' \prec G$, and say that $G$ **produces** $A$ when $G$ is free, $G$ is false in $I_G$, and $A$ is a positive literal that occurs once in $G$ and is greater than every other literal of $G$. Let $I$ be the set of all produced atoms. Note that a clause that produces $A$ has $\max G = A$.

(a) *If $G$ produces $A$, then $A \in I$ and every other literal of $G$ is false in $I$.* Let $G''$ produce $A''$ with $G \prec G''$. By (M3), $A'' \succeq A$. If $A'' = A$, then $A \in I_{G''}$, so $G''$ is true in $I_{G''}$ and does not produce. So $A'' \succ A$. Now a positive literal $B \ne A$ of $G$ has $B \prec A$. It is false in $I_G$, and it is not produced by $G$ or by a later clause, so $B \notin I$. A negative literal $\neg B$ of $G$ is false in $I_G \subseteq I$, so $B \in I$.

(b) *If $G \in \mathcal{G}$ is false in $I$ and $\max G$ is a positive literal $A$, then $G$ is false in $I_G$.* Positive literals of $G$ are false in $I \supseteq I_G$. Let $\neg B \in G$. Then $B \in I$, so some $G'$ produces $B$, and $\max G' = B$. As $\neg B \prec A$, also $B \prec A$, so $\max G' \prec \max G$, and $G' \prec G$ by (M3). So $B \in I_G$.

(c) *A tool for the main step.* Let $R_0$ be a clause that is a tautology or subsumed by a clause of $P$, let $\theta$ be a substitution that makes $R_0$ ground, and let $R$ be a ground clause with $R_0\theta \subseteq R$ as multisets, where $R_0\theta$ lists $K\theta$ once for each $K \in R_0$. If $R$ is false in $I$, then some $E\tau' \in \mathcal{G}$ is false in $I$ and $E\tau' \preceq R$. Indeed, if $R_0$ held $K$ and $\neg K$, then $R$ would hold $K\theta$ and $\neg K\theta$ and would be true. So $E\pi \subseteq R_0$ for some $E \in P$ and some $\pi$ that is injective on the literals of $E$. Let $\tau'$ be $\pi\theta$ on the variables of $E$, with any terms of $H$ on the variables that it leaves open. Distinct literals of $E$ go to distinct literals of $R_0$, so $E\tau' \subseteq R_0\theta \subseteq R$ as multisets. Then $E\tau'$ is false, and $E\tau' \preceq R$ by (M1).

Now suppose that some clause of $\mathcal{G}$ is false in $I$, and let $G$ be the smallest one. As $\square \notin P$, $G \ne \square$. Write $G = C\tau$ with $C \in P$. There are three cases.

*Case 1: a literal of $C$ is selected, or nothing is selected and $\max G$ is a negative literal.* Let $M \in C$ be the selected literal, or in the second case a literal with $M\tau = \max G$. Write $M\tau = \neg A$. $G$ is false, so $A \in I$, and some free $G' \in \mathcal{G}$ produces $A$. Write $G' = D\rho$ with $D \in P$, nothing selected in $D$, and $D$ renamed apart from $C$. As $A$ occurs once in $G'$, exactly one literal $L$ of $D$ has $L\rho = A$. The substitution $\tau \cup \rho$ unifies the atoms of $L$ and $M$, so they have an mgu $\sigma$ with $\tau \cup \rho = \sigma\theta$ on the variables of $C$ and $D$. The step is an ordered resolution step:

- nothing is selected in $D$, and $L\sigma$ is strictly maximal in $D\sigma$: if $K \in D \setminus \{L\}$ had $K\sigma \succeq L\sigma$, then by stability $K\rho \succeq A$, and $K\rho \ne A$ because $A$ occurs once in $G'$, so $K\rho \succ A = \max G'$, which is impossible;
- $M$ is selected in $C$, or nothing is selected and $M\sigma$ is maximal in $C\sigma$: if $K\sigma \succ M\sigma$ for some $K \in C$, then $K\tau \succ \neg A = \max G$, which is impossible.

So $R_0 = ((C \setminus \{M\}) \cup (D \setminus \{L\}))\sigma$ is an ordered resolvent of two clauses of $P$. Let $R$ be the multiset sum of $G$ minus one copy of $\neg A$ and $G'$ minus $A$. Each literal of $R_0$ is $N\sigma$ for some $N$ in $C \setminus \{M\}$ or $D \setminus \{L\}$, distinct literals of $R_0$ come from distinct $N$, and $N\sigma\theta$ is the copy of $N\tau$ or $N\rho$ in $R$. So $R_0\theta \subseteq R$. $R$ is false in $I$: $G$ is false, and the literals of $G'$ other than $A$ are false by (a). Every literal of $G'$ other than $A$ is smaller than $A$, and so smaller than $\neg A$, so $R \prec G$ by (M2). By saturation and (c), some clause of $\mathcal{G}$ is false and at most $R \prec G$, against the choice of $G$.

*Case 2: nothing is selected in $C$, $\max G$ is a positive literal $A$, and $A$ occurs at least twice in $G$.* Then two distinct literals $L_1, L_2$ of $C$ are positive with $L_1\tau = L_2\tau = A$. Their atoms have an mgu $\sigma$ with $\tau = \sigma\theta$. If $K\sigma \succ L_1\sigma$ for some $K \in C$, then $K\tau \succ A$, which is impossible. So $L_1\sigma$ is maximal in $C\sigma$, and $F = C\sigma$ is an ordered factor of $C$, with $L_1\sigma = L_2\sigma$ merged. Every literal of $F$ is $N\sigma$ for some $N \in C \setminus \{L_2\}$, from distinct $N$ for distinct literals, so $F\theta \subseteq G$ minus one copy of $A$, which is false and smaller than $G$ by (M2). By saturation and (c), this contradicts the choice of $G$.

*Case 3: nothing is selected in $C$, and $\max G$ is a positive literal $A$ that occurs once in $G$.* Then $G$ is free and $A$ is greater than every other literal of $G$. By (b), $G$ is false in $I_G$, so $G$ produces $A$. Then $A \in I$ and $G$ is true in $I$, a contradiction.

The cases cover all clauses $G \ne \square$, so every clause of $\mathcal{G}$ is true in $I$, and $I$ is a model of $P$. $\square$

## The loop

Let $A_\infty$ be the set of stored clauses that enter active and are never removed afterwards. A stored clause is picked at most once, so it enters active at most once.

**Lemma 2.** Every clause that is in active at some time is subsumed by a clause of $A_\infty$.

*Proof.* Let $D_0$ be in active. If line L6 removes it, the given clause $D_1$ that removes it subsumes $D_0$ and enters active; if $D_1$ is removed, the clause $D_2$ that removes it subsumes $D_1$, and so on. By transitivity each $D_j$ subsumes every $D_i$ with $i < j$. Suppose that $D_j$ is a variant of $D_i$ with $i < j$. When $D_j$ was picked, $D_{j-1}$ was in active, and $D_{j-1}$ subsumes $D_i$ (or is $D_i$), so it subsumes its variant $D_j$, and line L5 would have deleted $D_j$. So the $D_i$ are not variants of each other. Multiset subsumption is a case of the subsumption of the proof for Robinson's resolution principle, so by its Lemma 5 the chain is finite, and its last clause is in $A_\infty$. $\square$

**Lemma 3.** Suppose that the run never returns UNSAT and that every stored clause is picked at some time. Then every stored clause is a tautology or is subsumed by a clause of $A_\infty$, $A_\infty$ is saturated, and $\square \notin A_\infty$.

*Proof.* A picked clause $G$ is deleted at line L5 as a tautology, or because a clause of active subsumes it, or it enters active. In the last two cases Lemma 2 and transitivity give a clause of $A_\infty$ that subsumes $G$. Line L10 skips a clause only if the same clause was stored before. Now let $C, D \in A_\infty$, with $D$ picked after $C$ or $D = C$. When $D$ was picked, $C$ was in active, so line L8 formed every ordered factor of $D$, and line L9 formed every ordered resolvent of $D$ and $C$, in both roles, and of $D$ and a renamed copy of $D$. All of them were stored, so each is a tautology or is subsumed by a clause of $A_\infty$. If $\square$ were in $A_\infty$, line L4 would have returned UNSAT when it was picked. $\square$

## Parts 2, 3 and 4

For part 2, the loop leaves line L2 only when every stored clause was picked, and then $A_\infty$ is the final active set. By Lemma 3 and Lemma 1, $A_\infty$ has a Herbrand model $I$. Each clause $D$ of $S$ was stored at line L1, so it is a tautology, which is true in $I$, or $E\pi \subseteq D$ for some $E \in A_\infty$. Then every ground instance $D\tau$ contains the ground instance $E\pi\tau$, which is true in $I$. So $I$ is a model of $S$.

For part 3, suppose that the run does not return UNSAT. With no limit, line L11 never returns, so the run returns SATURATED, and part 2 applies, or it runs forever. In that case every stored clause is picked at some time, because line L3 takes the oldest untaken clause at every $k$-th pick and only finitely many clauses are older than a given one. Lemmas 3 and 1 give a model of $A_\infty$, and it is a model of $S$ as in part 2. In both cases $S$ is satisfiable.

For part 4, an ordered factor of a ground clause would merge two equal literals, so a ground clause has none, and an ordered resolvent of ground clauses is a set of literals over the atoms of its parents. So every stored clause is a set of literals over the $n$ atoms of $S$. Each atom is absent, positive, negative or both, so there are at most $4^n$ such sets. Line L10 stores each at most once, and each pass of the loop takes a stored clause that was not taken before, so the loop stops after at most $4^n$ passes. $\blacksquare$
