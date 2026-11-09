---
title: The CTL labelling algorithm computes the set of states that satisfy the formula
proves: [correctness]
status: full
---

Let $M = (S, I, R, L)$ be a finite Kripke structure with a total relation $R$. For $A \subseteq S$ write $\mathit{pre}_\exists(A) = \{s : R(s) \cap A \ne \emptyset\}$ and $\mathit{pre}_\forall(A) = \{s : R(s) \subseteq A\}$. A *path in $A$* is a path all of whose states are in $A$.

**Lemma 1 (CHECK-EU).** CHECK-EU$(A, B)$ returns the set $U$ of states $s$ that have a finite path $s = s_0 s_1 \ldots s_j$ with $s_j \in B$ and $s_0, \ldots, s_{j-1} \in A$.

*Proof.* *Soundness.* We show that each state in $X$ is in $U$, by induction on the time when it enters $X$. The states of $B$ (line L13) are in $U$ with $j = 0$. A state $s$ added at line L17 is in $A$ and has the edge $(s, t)$ to a state $t$ that was already in $X$, so in $U$ by induction; $s$ followed by the path of $t$ shows $s \in U$.

*Completeness.* Each state enters $Q$ when it enters $X$, and leaves $Q$ once, so the loop of line L14 ends and each state of $X$ is dequeued. We show by induction on $j$ that a state with a path of length $j$ as above is in $X$ at the end. For $j = 0$ it is in $B \subseteq X$. For $j > 0$, $s_1$ has such a path of length $j - 1$, so it enters $X$ and is dequeued at some time. At that time line L16 looks at its predecessor $s_0 \in A$, and line L17 adds $s_0$ unless it is already in $X$. $\square$

**Lemma 2 (CHECK-AU).** CHECK-AU$(A, B)$ returns the least fixed point $V$ of $g(Z) = B \cup (A \cap \mathit{pre}_\forall(Z))$.

*Proof.* The counter invariant: at each time, $c[s] = |R(s)| - |\{\text{edges } (s, t) : t \text{ has been dequeued}\}|$, since line L21 runs once for each edge into each dequeued state. Each state of $X$ is enqueued once and dequeued once. So at the end, when all states of $X$ have been dequeued, $c[s] = 0$ if and only if $R(s) \subseteq X$ (edges are counted with their multiplicity on both sides).

*$X \subseteq V$.* By induction on the time of entry. $B \subseteq g(V) = V$. A state added at line L22 is in $A$ and has $c[s] = 0$ at that time, so all its successors were already in $X$, hence in $V$ by induction; so $s \in A \cap \mathit{pre}_\forall(V) \subseteq V$.

*$V \subseteq X$.* At the end, $X$ satisfies $g(X) \subseteq X$: $B \subseteq X$, and a state $s \in A$ with $R(s) \subseteq X$ has had its counter lowered to $0$ when its last successor was dequeued, and then line L22 added it unless it was already in $X$. By the [Knaster-Tarski theorem](/knaster-tarski-theorem/), the least fixed point is the intersection of all $Z$ with $g(Z) \subseteq Z$, so $V \subseteq X$. $\square$

**Lemma 2a.** If $A = [\![\alpha]\!]$ and $B = [\![\beta]\!]$, then $V = W$, where $W = [\![\mathsf{A}[\alpha\,\mathsf{U}\,\beta]]\!]$.

*Proof.* *$V \subseteq W$.* It is enough to show $g(W) \subseteq W$, since $V$ is the least such set. A state of $B$ is in $W$. Let $s \in A$ with $R(s) \subseteq W$. Each path from $s$ is $s$ followed by a path from a successor $t \in W$, which satisfies $\alpha\,\mathsf{U}\,\beta$; since $s \models \alpha$, the whole path does too. So $s \in W$.

*$W \subseteq V$.* Suppose $s_0 \in W \setminus V$. Then $s_0 \notin B$, since $B \subseteq V$, so every path from $s_0$ reaches $\beta$ only after position $0$, and $s_0 \in A$. Since $s_0 \notin V = g(V)$ and $s_0 \in A$, some successor $s_1$ is not in $V$, and $s_1 \in W$ because the paths from $s_1$ are suffixes of paths from $s_0$. Repeating this gives an infinite path $s_0 s_1 s_2 \ldots$ with each $s_i \in W \setminus V$, so no $s_i$ is in $B$. This path does not satisfy $\alpha\,\mathsf{U}\,\beta$, which contradicts $s_0 \in W$. $\square$

**Lemma 3 (CHECK-EG).** CHECK-EG$(A)$ returns the set $G$ of states that have an infinite path in $A$.

*Proof.* Let $M_A$ be the subgraph of $M$ on $A$, and call a strongly connected component of $M_A$ *nontrivial* if it has an edge of $M_A$, that is, two or more states, or one state with a self-loop. Let $N$ be the union of the nontrivial components.

*Claim: $s \in G$ if and only if $s \in A$ and $s$ has a path in $A$ to a state of $N$.* Suppose $\pi = s_0 s_1 \ldots$ is an infinite path in $A$ from $s$. Since $A$ is finite, some state $t$ occurs twice on $\pi$, at positions $i < j$. The segment $s_i \ldots s_j$ is a cycle of $M_A$, so all its states lie in one component of $M_A$, and that component has an edge, so it is nontrivial. So $s_0 \ldots s_i$ is a path in $A$ from $s$ to $N$. Conversely, let $s_0 \ldots s_i$ be a path in $A$ with $s_i$ in a nontrivial component $C$. Then $s_i$ lies on a cycle inside $C$: if $|C| \ge 2$, take a path in $C$ from $s_i$ to another state of $C$ and back; if $|C| = 1$, take the self-loop. The path followed by this cycle forever is an infinite path in $A$.

Line L25 sets $X = N$, by the correctness of Tarjan's algorithm on $M_A$. Lines L26 and L27 are CHECK-EU with target $N$ and the condition $s \in A$, so by Lemma 1 they return the states with a path in $A$ to $N$ (the states of $N$ are in $A$). By the claim, this is $G$. $\square$

**Theorem.** SAT$(M, \varphi)$ returns $[\![\varphi]\!]$.

*Proof.* Line L1 visits the distinct subformulas of $\varphi$ so that each one comes after all its proper subformulas. We show by induction along this order that after $\psi$ is processed, $T[\psi] = [\![\psi]\!]$. When $\psi$ is processed, $T[\alpha] = [\![\alpha]\!]$ and $T[\beta] = [\![\beta]\!]$ for its parts, by induction.

- Lines L3 to L6 are the definitions of the atomic and Boolean cases.
- Line L7 is the definition of $\mathsf{EX}$. Line L8 gives the states all of whose successors are in $[\![\alpha]\!]$, which is $\mathsf{AX}\,\alpha$.
- Line L9: by Lemma 1, CHECK-EU returns the states with a finite path through $[\![\alpha]\!]$ to $[\![\beta]\!]$. Each finite path extends to an infinite one because $R$ is total, so this is $[\![\mathsf{E}[\alpha\,\mathsf{U}\,\beta]]\!]$.
- Line L10: by Lemmas 2 and 2a, $[\![\mathsf{A}[\alpha\,\mathsf{U}\,\beta]]\!]$.
- Line L11: by Lemma 3 with $A = [\![\alpha]\!]$, the states with an infinite path on which $\alpha$ holds everywhere, which is $[\![\mathsf{EG}\,\alpha]\!]$.

The derived operators $\mathsf{EF}$, $\mathsf{AF}$ and $\mathsf{AG}$ are computed through their definitions, so they are correct too. Line L12 returns $T[\varphi] = [\![\varphi]\!]$. $\blacksquare$

**Termination and cost.** Each loop enqueues each state at most once, so every call ends. The cost bound $O(|M|\,|\varphi|)$ is proved on the page of the [linear-time theorem](/ctl-model-checking-linear-time/). ∎
