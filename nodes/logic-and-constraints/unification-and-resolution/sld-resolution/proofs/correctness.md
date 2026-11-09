---
title: SLD resolution is sound and complete for every computation rule
proves: [correctness]
status: full
---

Let $P$ be a definite program and $Q = \leftarrow A_1, \ldots, A_k$ a query. Substitutions are composed from left to right: $t(\theta\mu) = (t\theta)\mu$. All atoms are over the language of $P$ and $Q$, unless we add constants explicitly.

## 1. The fixpoint semantics

The *Herbrand base* $B_P$ is the set of ground atoms. A Herbrand interpretation is a subset $I \subseteq B_P$, the set of atoms that are true. Define

$$T_P(I) = \{ H\gamma \mid H \leftarrow B_1, \ldots, B_m \in P,\ H\gamma \text{ ground},\ B_1\gamma, \ldots, B_m\gamma \in I \}.$$

**Lemma 1.1.** $I$ is a model of $P$ if and only if $T_P(I) \subseteq I$.

*Proof.* $I$ is a model iff each ground instance of each clause is true in $I$, that is, iff the head is in $I$ whenever all body atoms are in $I$. This is $T_P(I) \subseteq I$. $\square$

**Lemma 1.2.** The intersection of a nonempty set of Herbrand models of $P$ is a Herbrand model of $P$. So $P$ has a least Herbrand model $M_P$, the intersection of all its Herbrand models.

*Proof.* Let $J = \bigcap_i I_i$. If the body of a ground instance is in $J$, it is in each $I_i$, so the head is in each $I_i$, and so in $J$. The set $B_P$ is a model, so the family is not empty. $\square$

**Theorem 1 (van Emden and Kowalski).** $M_P = \mathrm{lfp}(T_P) = T_P \uparrow \omega$, where $T_P \uparrow 0 = \emptyset$, $T_P \uparrow (n+1) = T_P(T_P \uparrow n)$ and $T_P \uparrow \omega = \bigcup_n T_P \uparrow n$. Also, for each ground atom $A$, $P \models A$ iff $A \in M_P$.

*Proof.* $T_P$ is monotone on the complete lattice of subsets of $B_P$. By the Knaster-Tarski theorem, $\mathrm{lfp}(T_P) = \bigcap \{ I \mid T_P(I) \subseteq I \}$, which by Lemma 1.1 is the intersection of all Herbrand models, that is $M_P$. Next, $T_P \uparrow n \subseteq \mathrm{lfp}(T_P)$ for each $n$ by induction and monotonicity, so $T_P \uparrow \omega \subseteq \mathrm{lfp}(T_P)$. Conversely $T_P(T_P \uparrow \omega) \subseteq T_P \uparrow \omega$: a clause body is a finite set of atoms, so if it lies in $T_P \uparrow \omega$, it lies in some $T_P \uparrow n$, and the head is in $T_P \uparrow (n+1)$. So $T_P \uparrow \omega$ is a model and contains $M_P$.

For the last claim: if $P \models A$, then $A$ is true in the model $M_P$. If $A \in M_P$, let $\mathcal{M}$ be any model of $P$, and let $I$ be the set of ground atoms true in $\mathcal{M}$. Each ground instance of a clause is true in $\mathcal{M}$, so $I$ is a Herbrand model, $M_P \subseteq I$, and $A$ is true in $\mathcal{M}$. $\square$

A *proof tree* for a ground atom $A$ is a finite tree whose root is $A$ and in which each node $B$ with children $C_1, \ldots, C_m$ comes with a ground instance $B \leftarrow C_1, \ldots, C_m$ of a clause of $P$. By induction on $n$, $A \in T_P \uparrow n$ iff $A$ has a proof tree of height at most $n$. So $A \in M_P$ iff $A$ has a proof tree.

## 2. Soundness

An SLD derivation from $G_0 = Q$ is a sequence of goals $G_0, G_1, \ldots, G_n$ with unifiers $\mu_1, \ldots, \mu_n$, where $G_{i}$ comes from $G_{i-1}$ by selecting an atom $A$, taking a clause $H \leftarrow B_1, \ldots, B_m$ with fresh variables and $\mu_i = \mathrm{mgu}(A, H)$, and replacing $A$ by the body, then applying $\mu_i$. It is a refutation if $G_n$ is empty, and then $\sigma = \mu_1 \cdots \mu_n$ restricted to the variables of $Q$ is a computed answer.

**Theorem 2 (soundness).** If $Q$ has a refutation with unifiers $\mu_1, \ldots, \mu_n$, then $P \models \forall\, (A_1 \wedge \cdots \wedge A_k)\mu_1 \cdots \mu_n$.

*Proof.* By induction on $n$. Let the first step select $A_j$ and use the clause $H \leftarrow B_1, \ldots, B_m$. Then $G_1 = \leftarrow (A_1, \ldots, A_{j-1}, B_1, \ldots, B_m, A_{j+1}, \ldots, A_k)\mu_1$ has a refutation with $\mu_2, \ldots, \mu_n$. Write $\rho = \mu_2 \cdots \mu_n$; for $n = 1$, $G_1$ is empty, $m = 0$, $k = 1$ and $\rho = \varepsilon$. By induction, $P \models \forall\, A_i\mu_1\rho$ for $i \neq j$ and $P \models \forall\, B_l\mu_1\rho$ for each $l$. The clause gives $P \models \forall\, (B_1 \wedge \cdots \wedge B_m \rightarrow H)\mu_1\rho$, so $P \models \forall\, H\mu_1\rho$. Since $H\mu_1 = A_j\mu_1$, this is $P \models \forall\, A_j\mu_1\rho$. $\square$

So each computed answer is a correct answer.

## 3. Completeness for every computation rule

A computation rule $R$ maps each goal (and, if one wants, the derivation so far) to one of its atoms. We use only that it selects some atom of each nonempty goal.

**Lemma 3.1 (ground refutations).** Let $G = \leftarrow C_1, \ldots, C_k$ be a goal, $V$ a finite set of variables with $\mathrm{vars}(G) \subseteq V$, and $\theta$ a substitution such that each $C_i\theta$ is a ground atom with a proof tree, the trees having $n$ nodes in total. Assume that the fresh variables of renamed clauses avoid $V$ and the variables of the range of $\theta$. Then for each computation rule $R$, there is a refutation of $G$ via $R$ of length exactly $n$, with unifiers whose composition $\sigma$ satisfies $x\theta = x\sigma\gamma$ for all $x \in V$ and some substitution $\gamma$.

*Proof.* By induction on $n$. If $n = 0$, then $k = 0$, the goal is empty, $\sigma = \varepsilon$ and $\gamma = \theta$.

Let $n > 0$, and let $R$ select $C_j$. The proof tree of $C_j\theta$ has a root instance $C_j\theta \leftarrow D_1, \ldots, D_m$, which is $(H \leftarrow B_1, \ldots, B_m)\beta$ for a clause of $P$. Rename this clause with fresh variables, outside $V$ and the range of $\theta$; then $\beta$ acts only on the fresh variables. The substitution $\theta \cup \beta$ (as $\theta$ on $V$ and $\beta$ on the clause) unifies $C_j$ and $H$, since $C_j\theta = H\beta$. So $C_j$ and $H$ have a most general unifier $\mu$, and there is a $\delta$ with $x(\theta \cup \beta) = x\mu\delta$ for all variables $x$ of $V$ and of the clause. We may take $\mu$ idempotent with $\mathrm{vars}(x\mu) \subseteq V \cup \mathrm{vars}(H)$ for $x \in V \cup \mathrm{vars}(H)$.

The next goal is $G_1 = \leftarrow (C_1, \ldots, C_{j-1}, B_1, \ldots, B_m, C_{j+1}, \ldots, C_k)\mu$. Apply $\delta$: we get $C_i\theta$ for $i \neq j$ and $B_l\beta = D_l$. These are ground atoms with proof trees: the trees of $C_i\theta$ and the subtrees of the root of the tree of $C_j\theta$. They have $n - 1$ nodes in total. Let $V_1 = V \cup \mathrm{vars}(\text{the renamed clause})$, which contains $\mathrm{vars}(G_1)$. By induction for $G_1$, $V_1$ and $\delta$, there is a refutation of $G_1$ via $R$ of length $n - 1$ with composition $\sigma_1$ and a $\gamma$ with $y\delta = y\sigma_1\gamma$ for $y \in V_1$. Then $\mu$ followed by this refutation is a refutation of $G$ of length $n$, with composition $\sigma = \mu\sigma_1$. For $x \in V$, $\mathrm{vars}(x\mu) \subseteq V_1$, so $x\theta = x\mu\delta = (x\mu)\sigma_1\gamma = x\sigma\gamma$. $\square$

**Theorem 3 (completeness).** Let $\theta$ be a correct answer for $Q$, that is $P \models \forall\, (A_1 \wedge \cdots \wedge A_k)\theta$. Then for each computation rule $R$ there is a refutation of $Q$ via $R$ with computed answer $\sigma$ and a substitution $\gamma$ such that $A_i\theta = A_i\sigma\gamma$ for each $i$.

*Proof.* Let $x_1, \ldots, x_r$ be the variables of $Q\theta$. Add new constants $c_1, \ldots, c_r$ to the language, and let $\varphi = \{x_1 \mapsto c_1, \ldots, x_r \mapsto c_r\}$. Since $P \models \forall\, Q\theta$, the ground atoms $A_i\theta\varphi$ are consequences of $P$ in the larger language. Theorem 1, applied in the larger language, gives each of them a proof tree. The clauses of $P$ do not mention the $c_l$, so each node of these trees is an instance of a clause of $P$. Lemma 3.1, with $V = \mathrm{vars}(Q)$ and the substitution $\theta\varphi$, gives a refutation via $R$ with composition $\sigma$ and a $\gamma$ with $x\theta\varphi = x\sigma\gamma$ for $x \in V$.

The unifiers of the refutation are most general unifiers of atoms of $P$ and $Q$, so they do not mention the new constants. Let $\gamma'$ be $\gamma$ with each $c_l$ replaced by $x_l$ in its range. Replacing each $c_l$ by $x_l$ on both sides of $x\theta\varphi = x\sigma\gamma$ gives $x\theta = x\sigma\gamma'$, because $x\theta$ and $x\sigma$ contain no $c_l$. So $A_i\theta = A_i\sigma\gamma'$. $\square$

**Corollary (independence of the computation rule).** For each $R$, the SLD tree of $Q$ via $R$ has a success leaf for each correct answer, up to an instance. In particular the set of computed answers, up to instances, is the same for every $R$. If $Q\theta$ is ground with proof trees of total size $n$, the refutation via each $R$ has length $n$.

*Proof.* Theorem 3 holds for each $R$, and Theorem 2 makes all computed answers correct. The length is given by Lemma 3.1. $\square$

**Corollary (success set).** The set of ground atoms $A$ such that $\leftarrow A$ has a refutation is $M_P = T_P \uparrow \omega$ (Apt and van Emden).

## 4. What the search finds

The procedure on the page searches the SLD tree via $R$ depth first, up to depth $d$. Every node it outputs is a success leaf, so by Theorem 2 every output is a correct answer. A success leaf at depth at most $d$ is reached, because the search with a bound visits every node of depth at most $d$ and the tree is finitely branching. So by Theorem 3, for every correct answer $\theta$ there is a $d$ such that the search with bound $d$ outputs a computed answer of which $\theta$ is an instance. Iterating $d = 1, 2, \ldots$ therefore gives a complete search. Without the bound the search can follow an infinite branch and miss success leaves to its right.

The tests check this on random Datalog programs: with each of three computation rules and bound $d = 7$, the set of answers equals the set of atoms of the least model whose smallest proof tree has at most 7 nodes, computed bottom-up.
