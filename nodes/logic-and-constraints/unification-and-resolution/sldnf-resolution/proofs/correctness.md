---
title: SLDNF resolution is sound for the Clark completion, and it is not complete
proves: [correctness]
status: full
---

Let $P$ be a normal program and $\mathrm{comp}(P)$ its completion, with Clark's equality theory $\mathrm{CET}$. We read a goal $\leftarrow L_1, \ldots, L_k$ as the conjunction $L_1 \wedge \cdots \wedge L_k$, with $\mathit{not}$ read as $\neg$. We use the following facts.

- **(E1) Unification and equality (Clark 1978).** If $s$ and $t$ (or two tuples of terms) have no unifier, then $\mathrm{CET} \models \neg (s = t)$. If they have the most general unifier $\mu = \{x_1 \mapsto r_1, \ldots, x_n \mapsto r_n\}$, then $\mathrm{CET} \models (s = t) \leftrightarrow (x_1 = r_1 \wedge \cdots \wedge x_n = r_n)$. Both follow by induction along the steps of a unification algorithm, since each step replaces equations by equivalent ones under the axioms of $\mathrm{CET}$ (different symbols differ, symbols are injective, no term equals a proper subterm of itself).
- **(E2) The "if" half.** $\mathrm{comp}(P) \models P$: each clause $p(\bar t) \leftarrow B$ follows from the "if" direction of the definition of $p$, with $\bar x = \bar t$.
- **(E3) The "only if" half.** If $p$ has the clauses $p(\bar t_i) \leftarrow B_i$ for $i = 1, \ldots, r$, then $\mathrm{comp}(P) \models \forall \bar x\, (p(\bar x) \rightarrow \bigvee_i \exists \bar y_i\, (\bar x = \bar t_i \wedge B_i))$, where $\bar y_i$ are the variables of the $i$-th clause.

We consider SLDNF trees built by the procedure on the page, with the safe rule. The *rank* of a tree is the nesting depth of the subsidiary trees that it uses: a tree that never selects a negative literal has rank 0, and a tree whose subsidiary trees have rank at most $r$ has rank $r + 1$.

## Theorem (soundness, Clark 1978)

(a) If a goal $G$ has a refutation in its SLDNF tree with composed unifier $\sigma$, then $\mathrm{comp}(P) \models \forall\, G\sigma$.

(b) If $G$ has a finitely failed SLDNF tree, then $\mathrm{comp}(P) \models \neg \exists\, G$.

*Proof.* By induction on the rank, and inside one rank by induction on the length of the refutation for (a) and on the height of the finite tree for (b). Assume both statements for all trees of smaller rank.

**(a), positive step.** The first step selects an atom $A$ of $G$, uses a renamed clause $H \leftarrow B$ with $\mu = \mathrm{mgu}(A, H)$, and gives $G_1 = (G \text{ with } A \text{ replaced by } B)\mu$, which has a shorter refutation with unifier $\rho$. By induction $\mathrm{comp}(P) \models \forall\, G_1\rho$. So the literals of $G$ other than $A$, and the body $B$, hold under $\mu\rho$. By (E2), $\mathrm{comp}(P) \models \forall\, (B \rightarrow H)\mu\rho$, so $H\mu\rho = A\mu\rho$ holds too. Hence $\mathrm{comp}(P) \models \forall\, G\mu\rho$, and $\sigma = \mu\rho$.

**(a), negative step.** The first step selects a ground literal $\mathit{not}\ A$, the subsidiary tree for $\leftarrow A$ is finitely failed, and $G$ without the literal has a shorter refutation with unifier $\sigma$. The subsidiary tree has smaller rank, so by (b), $\mathrm{comp}(P) \models \neg A$. With the induction hypothesis for the rest of $G$, and since $A$ is ground, $\mathrm{comp}(P) \models \forall\, G\sigma$.

**(b), positive node.** The root selects an atom $A = p(\bar s)$ of $G = \leftarrow C, A, D$ (with $C$ and $D$ lists of literals). Let the clauses for $p$ be $p(\bar t_i) \leftarrow B_i$, renamed apart. For each $i$ where $\bar s$ and $\bar t_i$ do not unify, $\mathrm{CET} \models \neg (\bar s = \bar t_i)$ by (E1). For each $i$ where they unify with $\mu_i$, the child $(C, B_i, D)\mu_i$ has a finitely failed subtree of smaller height, so by induction $\mathrm{comp}(P) \models \neg \exists\, (C \wedge B_i \wedge D)\mu_i$, and by (E1) this means $\mathrm{comp}(P) \models \neg \exists\, (\bar s = \bar t_i \wedge C \wedge B_i \wedge D)$. Now assume that some instance of $C \wedge A \wedge D$ holds in a model of $\mathrm{comp}(P)$. By (E3), $p(\bar s)$ gives an $i$ and values of $\bar y_i$ with $\bar s = \bar t_i$ and $B_i$. Together with $C$ and $D$ this contradicts the statement for that $i$. So $\mathrm{comp}(P) \models \neg \exists\, G$.

**(b), negative node.** The root selects a ground literal $\mathit{not}\ A$ of $G$. The node fails in one of two ways. Either the subsidiary tree for $\leftarrow A$ has a refutation, and since $A$ is ground, (a) for smaller rank gives $\mathrm{comp}(P) \models A$, so $\mathit{not}\ A$ is false and $\mathrm{comp}(P) \models \neg \exists\, G$. Or the subsidiary tree is finitely failed, and the only child, $G$ without $\mathit{not}\ A$, has a finitely failed tree of smaller height. Then by induction $\mathrm{comp}(P) \models \neg \exists\, (G \text{ without } \mathit{not}\ A)$, which implies $\mathrm{comp}(P) \models \neg \exists\, G$. $\square$

The safe rule matters in the negative steps, where the proof uses that $A$ is ground. If $\mathit{not}\ A$ were selected with $A$ not ground, a refutation of $\leftarrow A$ would only show that some instance of $A$ holds. Failing the node would then be unsound, because other instances of $\mathit{not}\ A$ may be true. This is the unsound case of Prolog: for `p(X) ← not q(X).` and `q(a).`, the completion gives $\forall x\, (q(x) \leftrightarrow x = a)$ and $\forall x\, (p(x) \leftrightarrow \neg q(x))$, so $p(b)$ holds, but an unsafe rule makes $\leftarrow p(X)$ fail.

## Incompleteness

Let $P$ be `p ← q.`, `p ← not q.`, `q ← q.`. Its completion is $p \leftrightarrow (q \vee \neg q)$ and $q \leftrightarrow q$, so $\mathrm{comp}(P) \models p$. The SLDNF tree of $\leftarrow q$ is one infinite branch $q, q, q, \ldots$, so it has no refutation and is not finitely failed. In the tree of $\leftarrow p$, the first child is $\leftarrow q$, whose subtree is that infinite branch. The second child is $\leftarrow \mathit{not}\ q$, and the step on it needs the subsidiary tree of $\leftarrow q$ to succeed or fail finitely, which it never does. So the tree of $\leftarrow p$ has no success leaf, for any depth: SLDNF resolution cannot derive $p$, although $p$ follows from the completion. The tests run this program with the depth bounds 5, 20 and 60 and get no answer and the status *cut* each time.

## Stratified programs

For a stratified program, the perfect model $M$ is built stratum by stratum: each stratum takes the least fixed point of its clauses, with negative literals read in the strata below. Apt, Blair and Walker (1988) proved that $M$ is a supported model, so it satisfies each "if and only if" of $\mathrm{comp}(P)$; it is a Herbrand model, so it satisfies $\mathrm{CET}$. By the theorem, each computed answer of a query is true in $M$, and each query with a finitely failed tree is false in $M$. In particular, for a ground atom $A$ whose SLDNF tree is finite and does not flounder, $\leftarrow A$ succeeds iff $A \in M$: a success makes $A$ true in $M$, and a finitely failed tree makes it false. The tests check this for all ground atoms, and they also check that the set of computed answers of each non-ground query equals the set of its instances in $M$, on random stratified programs with three strata and finite trees.
