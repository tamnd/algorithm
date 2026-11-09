---
title: Algorithm X lists each exact cover exactly once
proves: [correctness]
status: full
---

We use the terms of the page. Let $P$ be the set of primary items, $Q$ the set of secondary items, and $O$ the list of options. A *state* is a set $A_P \subseteq P$ of active primary items, a set $A_Q \subseteq Q$ of active secondary items, and a set $A_O$ of active options. For a list $S$ of pairwise disjoint options, write $\bigcup S$ for the set of items that its options contain. The state is *faithful* to $S$ when

> **(F)** $A_P = P \setminus \bigcup S$, $A_Q = Q \setminus \bigcup S$, and $A_O$ is the set of options that are disjoint from $\bigcup S$.

The *residual problem* of a faithful state has the primary items $A_P$, the secondary items $A_Q$ and the options $A_O$. Every option of $A_O$ has a primary item in $A_P$: it has a primary item, and that item is not in $\bigcup S$ because the option is disjoint from $\bigcup S$.

**Lemma 1 (residual problem).** Let the state be faithful to $S$. A set $T$ of options extends $S$ to a solution, that is, $S \cup T$ is a solution, if and only if $T$ is a solution of the residual problem.

*Proof.* If $S \cup T$ is a solution, its options are pairwise disjoint, so each option of $T$ is disjoint from $\bigcup S$ and lies in $A_O$. The options of $T$ are pairwise disjoint, and they cover each item of $A_P = P \setminus \bigcup S$ exactly once, because $S \cup T$ covers it exactly once and $S$ does not cover it. Conversely, if $T \subseteq A_O$ is a solution of the residual problem, then its options are disjoint from $\bigcup S$ and from each other, so the options of $S \cup T$ are pairwise disjoint. Each primary item is covered by $S$ or by $T$, so $S \cup T$ is a solution. $\square$

**Lemma 2 (COVER and UNCOVER).** Let the state be faithful to $S$, and let $i \in A_P \cup A_Q$. After COVER$(i)$, the active items are those of the state less $i$, and the active options are those of the state that do not contain $i$. UNCOVER$(i)$ right after this restores the state exactly.

*Proof.* This is the specification of the two operations. The [dancing links](/dancing-links/) page proves it for the linked representation, on the condition that the uncovers run in the reverse order of the covers. In the algorithm, each UNCOVER$(j)$ of line L10 undoes the COVER$(j)$ of line L8 in the reverse order, and the UNCOVER$(i)$ of line L12 undoes the COVER$(i)$ of line L5 after all the covers of the loop are undone, so the condition holds. $\square$

Lemma 2 also gives the list of line L6: after COVER$(i)$, the options of $i$ are still in the list of $i$, and they are the options of $A_O$ that contain $i$, because the cover leaves the list of $i$ itself as it was.

**Theorem.** If ALGORITHM-X is called in a state that is faithful to $S$, then it outputs $S \cup T$ once for each solution $T$ of the residual problem, it outputs nothing else, and it returns with the state and $S$ unchanged.

*Proof.* By induction on $|A_P|$.

*Base, $|A_P| = 0$.* Lines L1 to L3 output $S$ and return, and nothing changes. The residual problem has no primary items. Every option of $A_O$ has a primary item in $A_P$, so $A_O$ is empty, and the only solution of the residual problem is $T = \emptyset$. The output $S$ is $S \cup \emptyset$.

*Step, $|A_P| \ge 1$.* Line L4 picks $i \in A_P$. Let $o_1, \ldots, o_k$ be the options of $A_O$ that contain $i$, in the order of line L6. If $k = 0$, then no solution of the residual problem covers $i$, so there is no solution, and the call outputs nothing, does COVER$(i)$ and UNCOVER$(i)$, and returns with the state unchanged by Lemma 2.

If $k \ge 1$, each solution $T$ of the residual problem contains exactly one option that contains $i$, so the solutions fall into $k$ disjoint classes: the class of $o_t$ is the set of solutions that contain $o_t$. Fix $t$. Lines L5, L7 and L8 make the list $S' = S, o_t$ and cover every item of $o_t$. These items are active and pairwise distinct, so by Lemma 2 the new state has the active items of the old state less the items of $o_t$, and the active options of the old state that are disjoint from $o_t$. That is exactly (F) for $S'$, and the options of $S'$ are pairwise disjoint because $o_t \in A_O$. The item $i$ is now inactive, so the new $|A_P|$ is smaller. By the induction hypothesis, line L9 outputs $S' \cup T'$ once for each solution $T'$ of the residual problem of $S'$, and returns with the state unchanged. By Lemma 1 used twice, the sets $S' \cup T'$ are exactly the sets $S \cup T$ for the solutions $T$ of the old residual problem that contain $o_t$, with $T = \{o_t\} \cup T'$. Lines L10 and L11 undo lines L8 and L7, so by Lemma 2 the state is again the state after line L5 and the list is $S$.

So the iteration for $o_t$ outputs the class of $o_t$, each member once, and the $k$ classes are disjoint and cover all solutions. Line L12 undoes line L5. The state and the list are as at the call. $\blacksquare$

**Corollary.** The first call runs in the start state, which is faithful to the empty list, and the residual problem is then the whole problem. So the algorithm outputs each solution of the problem exactly once.

**Termination.** Each recursive call has a smaller $|A_P|$, and each loop runs over a finite list, so the search tree is finite and every call returns.
