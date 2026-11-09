---
title: Positive hyperresolution with factoring is sound and refutation complete, and the loop stops on ground input
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page and the notation of the proof for [Robinson's resolution principle](/robinson-resolution/). Clauses are finite sets of literals, $C$ subsumes $D$ when $|C| \le |D|$ and $C\rho \subseteq D$, an **electron** is a clause with no negative literal, and a **nucleus** is a clause of $S$ with a negative literal. Let $\mathcal{N}$ be the set of nuclei of $S$. We call a set $P$ of electrons **hyper-saturated** when every factor of a clause of $P$, and every hyperresolvent of a nucleus of $\mathcal{N}$ with electrons of $P$, is subsumed by a clause of $P$.

**Theorem.** Run the loop on a finite set $S$ of clauses.

1. If it returns UNSAT, then $S$ is unsatisfiable.
2. If it returns SATURATED, then $S$ is satisfiable.
3. If $S$ is unsatisfiable and there is no limit, then it returns UNSAT.
4. If $S$ is ground, it stops.

Part 1 holds because a hyperresolvent is the result of binary resolution steps with the same unifier, and factors and binary resolvents follow from their parents.

## The ground model

Fix a total well-founded order $\succ$ on ground atoms, for example by size and then by a fixed order of symbols. Compare finite sets of ground atoms by the multiset extension of $\succ$; for sets, $X \succ Y$ when $X \ne Y$ and the largest atom of the symmetric difference is in $X$. This is a total well-founded order.

**Lemma 1.** Let $T$ be a set of ground clauses, and let $Q$ be the set of ground electrons that can be derived from the electrons of $T$ by ground hyperresolution with the nuclei of $T$. If $\square \notin Q$, then $T$ is satisfiable.

*Proof.* Go through the clauses of $Q$ in increasing order. Let $I_E$ be the set of atoms made true before $E$. If $E$ is false in $I_E$, then $E$ **produces** its largest atom $\max E$, which is added. Let $I$ be the union of all produced atoms. This is well defined because the order is well founded.

(a) If $E$ produces $A = \max E$, then $E \setminus \{A\}$ is false in $I$. Its atoms are smaller than $A$ and false in $I_E$. A clause $E'$ after $E$ has $E' \succ E$, so $\max E' \succeq A$. If $\max E' = A$, then $A$ is already true, so $E'$ is true in $I_{E'}$ and does not produce. So every atom produced after $E$ is larger than $A$, and the atoms of $E \setminus \{A\}$ stay false.

(b) Every $E \in Q$ is true in $I$. $E \ne \square$, so it has a largest atom. If $E$ is true in $I_E$, it stays true, because $I \supseteq I_E$ and $E$ is positive. Otherwise $E$ produces $\max E$, which is in $I$.

(c) Every nucleus $N = \neg A_1 \vee \cdots \vee \neg A_k \vee B$ of $T$ is true in $I$. Otherwise all $A_i$ are in $I$ and $B$ is false in $I$. Each $A_i$ was produced by some $E_i = \{A_i\} \cup E_i'$, and $E_i'$ is false in $I$ by (a). The ground hyperresolvent $B \cup E_1' \cup \cdots \cup E_k'$ is in $Q$, and it is false in $I$, against (b).

The electrons of $T$ are in $Q$, so by (b) and (c), $I$ satisfies $T$. $\square$

## Lifting

**Lemma 2 (no merging).** Let $P$ be hyper-saturated, $C \in P$ and $\tau$ ground. Then some $C' \in P$ and ground $\tau'$ have $C'\tau' \subseteq C\tau$ and $|C'\tau'| = |C'|$.

*Proof.* This is Lemma 3 of the proof for Robinson's resolution principle. It uses only factors of clauses of $P$ and subsumption by clauses of $P$, and a positive clause is never a tautology. $\square$

**Lemma 3.** Let $P$ be hyper-saturated, and let every electron of $S$ be subsumed by a clause of $P$. Let $T$ be a set of ground instances of clauses of $S$, and let $Q$ be as in Lemma 1. Then every $E \in Q$ has $C\tau \subseteq E$ for some $C \in P$ and ground $\tau$.

*Proof.* Induction on the derivation of $E$. An electron of $T$ is $D\rho$ with $D$ an electron of $S$, and $C\rho' \subseteq D$ for some $C \in P$, so $C\rho'\rho \subseteq E$ after a ground extension. Now let $E$ be the ground hyperresolvent of a nucleus $N\tau_0 = \{\neg A_1, \ldots, \neg A_j\} \cup B'$ of $T$, where $N \in \mathcal{N}$ and the $A_i$ are distinct, with ground electrons $E_1 \ni A_1, \ldots, E_j \ni A_j$. By induction and Lemma 2, there are $C_i \in P$ and ground $\tau_i$ with $C_i\tau_i \subseteq E_i$ and no merging. If $A_i \notin C_i\tau_i$ for some $i$, then $C_i\tau_i \subseteq E_i \setminus \{A_i\} \subseteq E$. Otherwise let $L_i$ be the only literal of $C_i$ with $L_i\tau_i = A_i$. Write the negative literals of $N$ as $\neg M_1, \ldots, \neg M_k$, with $k \ge j$, and let $\pi(t)$ be the index $i$ with $M_t\tau_0 = A_i$. For each slot $t$ take a fresh copy $C_{\pi(t)}^{(t)}$ of $C_{\pi(t)}$. The substitution that is $\tau_0$ on $N$ and $\tau_{\pi(t)}$ on the copy $t$ unifies every pair $(M_t, L_{\pi(t)}^{(t)})$. So a most general unifier $\sigma$ of the pairs exists, with this substitution equal to $\sigma\theta$ for a ground $\theta$. The hyperresolvent $R$ of $N$ with the copies has

$$R\theta = B' \cup \bigcup_{i} (C_i\tau_i \setminus \{A_i\}) \subseteq B' \cup \bigcup_i (E_i \setminus \{A_i\}) = E,$$

where the first equality uses that nothing merges in the $C_i$. As $P$ is hyper-saturated, some $C \in P$ subsumes $R$, and $C\tau \subseteq E$ for a ground $\tau$. $\square$

**Lemma 4.** If $P$ is hyper-saturated, every electron of $S$ is subsumed by a clause of $P$, and $\square \notin P$, then $S$ is satisfiable.

*Proof.* If $S$ is unsatisfiable, [Herbrand's theorem](/herbrand-theorem/) gives a finite unsatisfiable set $T$ of ground instances of clauses of $S$. By Lemma 1, $\square \in Q$. By Lemma 3, $C\tau \subseteq \square$ for some $C \in P$, so $\square \in P$. $\square$

## The loop

Lines L3, L5, L6 and L9 are those of the loop of Robinson's resolution principle, applied to electrons. So Lemmas 5 and 6 of that proof hold: every clause that is in active at some time is subsumed by a clause of the set $A_\infty$ of clauses that enter active and stay there. Suppose that the run never returns UNSAT and that every stored electron is picked at some time. A picked electron is deleted at line L5 because a clause of active subsumes it, or it enters active, so every stored electron is subsumed by a clause of $A_\infty$. A clause that line L9 does not store is a variant of a stored one. Take a nucleus and electrons $C_1, \ldots, C_k \in A_\infty$, and let $G$ be the one among them picked last. When $G$ was picked, the others were in active, because a clause of $A_\infty$ never leaves active, so line L8 formed the hyperresolvent, with $G$ among the electrons. Line L8 also formed the factors of each clause of $A_\infty$. So $A_\infty$ is hyper-saturated, the electrons of $S$ were stored at line L1 and are subsumed by clauses of $A_\infty$, and $\square \notin A_\infty$, because line L4 would have returned.

For part 2, passive is empty at line L11, so every stored electron was picked, and Lemma 4 makes $S$ satisfiable. For part 3, suppose that the run does not return UNSAT. With no limit, it returns SATURATED, and part 2 applies, or it runs forever, and line L3 takes the oldest untaken clause at every $k$-th pick, so every stored electron is picked, and Lemma 4 applies. In both cases $S$ is satisfiable.

## Part 4

If $S$ is ground, every stored electron is a set of positive literals over the atoms of $S$, so there are at most $2^n$ of them for $n$ atoms. Line L9 stores each at most once, and each pass takes a stored electron that was not taken before, so the loop stops after at most $2^n$ passes. $\blacksquare$
