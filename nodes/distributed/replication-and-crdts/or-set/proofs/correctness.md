---
title: The op-based and the optimized OR-Set meet the add-wins set specification
proves: [correctness, invariant, termination]
status: full
---

**Events and histories.** An ADD$(e)$ event $a$ has an element $\mathrm{el}(a) = e$ and a tag $\tau(a) = (j, c)$: it is the $c$-th add made at replica $j$. A REMOVE$(e)$ event $r$ has an element and a set $R(r)$ of tags, fixed at its source (line L4 for the op-based form, the dots of $e$ in $E$ for the optimized form). The causal history $C_i$ of replica $i$ grows by the events made at $i$ and by the events that $i$ receives (op-based) or by the histories of the states it merges (state-based). Write $u \prec w$ when $u$ is in the history of the source of $w$ when $w$ is made. Every history is down-closed under $\prec$, and the adds of each replica in a history are a prefix of its adds, by the same induction as for the MV-Register.

Say that an add $a$ is **covered** in a history $H$ when some remove $r \in H$ of the same element has $a \prec r$. The add-wins specification says: LOOKUP$(e)$ at $i$ returns true exactly when $C_i$ has an uncovered add of $e$.

## Part 1. The op-based OR-Set

**Setting.** Replica $i$ runs the main block. Operations are sent by causal broadcast: each one is delivered exactly once at each replica, and an operation is delivered only after every operation in its causal past. The source delivers its own operation at once. $C_i$ is the set of operations delivered at $i$.

**Claim 1 (what a remove collects).** For a remove $r$ of $e$ and an add $a$ of $e$: if $\tau(a) \in R(r)$ then $a \prec r$. If $a \prec r$ and $\tau(a) \notin R(r)$ then some remove $r'$ of $e$ with $r' \prec r$ has $\tau(a) \in R(r')$.

*Proof.* This uses Claim 2 for the state at the source of $r$, which by induction on time holds before $r$ is made. $R(r)$ is the set of tags of $e$ in $S$ at the source, and by Claim 2 every such tag belongs to a delivered add, so to an add in the causal past of $r$. If $a \prec r$, then $a$ was delivered at the source before $r$ was made; if its tag is not in $S$ there, then by Claim 2 some delivered remove $r'$ collected it, and $r' \prec r$. $\square$

**Claim 2 (invariant).** At every time, $S_i = \{(\mathrm{el}(a), \tau(a)) : a \in C_i \text{ is an add and } \tau(a) \notin R(r) \text{ for every remove } r \in C_i\}$.

*Proof.* By induction on deliveries. At the start both sides are empty. Delivery of an add $a$ (line L5) puts its pair in $S_i$. No remove $r \in C_i$ has $\tau(a) \in R(r)$: by Claim 1 that would need $a \prec r$, and causal delivery would then have delivered $a$ before $r$, but $a$ is new at $i$. Tags are unique, so no other pair changes. Delivery of a remove $r$ (line L6) deletes the pairs with tags in $R(r)$, which are exactly the pairs that the new right side loses. $\square$

**Theorem 1 (add-wins).** LOOKUP$(e)$ at $i$ returns true exactly when $C_i$ has an uncovered add of $e$.

*Proof.* By Claim 2, line L2 returns true exactly when some add $a$ of $e$ in $C_i$ has its tag in no $R(r)$ with $r \in C_i$. If $a$ is covered by $r \in C_i$, then by Claim 1 either $\tau(a) \in R(r)$ or $\tau(a) \in R(r')$ for some $r' \prec r$, and $r' \in C_i$ because histories are down-closed; so the tag is collected. Conversely, if $\tau(a) \in R(r)$ with $r \in C_i$, then $a \prec r$ by Claim 1, and $r$ removes the same element because tags are unique, so $a$ is covered. $\square$

**Theorem 2 (convergence).** Two replicas that have delivered the same set of operations have the same state. If operations stop, every replica in the end delivers every operation, and then all replicas have the same state.

*Proof.* By Claim 2, $S_i$ is a function of $C_i$. Causal broadcast delivers every operation at every replica. $\square$

**Commutativity.** Claim 2 also shows directly that concurrent operations commute, which is the condition of the op-based CRDT theorem: two adds insert different pairs; a remove $r$ and a concurrent add $a$ touch different pairs, since $\tau(a) \in R(r)$ would need $a \prec r$; two removes are set differences.

## Part 2. The optimized state-based OR-Set

**Setting.** Replica $i$ runs the second block with state $(E_i, V_i)$. A remove $r$ of $e$ at $i$ has $R(r) = \{(j, c) : (e, c, j) \in E_i\}$. Steps are ADD, REMOVE, sending a copy of the state, and MERGE of a copy sent earlier. Copies may be lost, merged more than once and merged in any order. For a history $H$, let $\Phi(H)$ be the state $(E, V)$ with

- $V[j]$ = the number of adds of replica $j$ in $H$, and
- $E$ = the set of $(e, c, j)$ such that the $c$-th add of $j$ is in $H$, adds $e$, is the latest add of $e$ by $j$ in $H$, and is not covered in $H$.

**Claim 3 (covered adds of one element and replica are a prefix).** Let $a_1 \prec a_2$ be adds of $e$ by the same replica. If $a_2$ is covered in $H$, so is $a_1$. Hence $H$ has an uncovered add of $e$ exactly when, for some $j$, the latest add of $e$ by $j$ in $H$ is uncovered.

*Proof.* If $a_2 \prec r$ then $a_1 \prec r$. For the second part, if some add of $e$ by $j$ is uncovered, the latest one is too, by the first part. $\square$

**Claim 4 (invariant).** At every time, $(E_i, V_i) = \Phi(C_i)$, and a copy in transit equals $\Phi$ of its history.

*Proof.* By induction on the steps. At the start both are empty states.

*ADD at $i$ of $e$.* The new add $a$ is the $(V_i[i] + 1)$-th add of $i$, since $V_i[i]$ counts the adds of $i$. Line 1 updates $V$. The new add is the latest add of $e$ by $i$ and is uncovered, since no remove has it in its past. The older add of $e$ by $i$, if it is in $E_i$, is no longer the latest, and line 2 removes it. Nothing else changes.

*REMOVE at $i$ of $e$.* Every add of $e$ in $C_i$ is in the causal past of $r$, so every add of $e$ becomes covered, and line 3 removes all triples of $e$. $V$ does not change, since $r$ is not an add.

*MERGE at $i$ of a copy $\Phi(H)$, with $C = C_i$.* The target is $\Phi(C \cup H)$. Line 9 gives its $V$, since the adds of $j$ in each history form a prefix. For $E$, two facts help. (i) An add is covered in $C \cup H$ exactly when it is covered in each of $C$ and $H$ that contain it, because a remove $r \in H$ with $a \prec r$ forces $a \in H$. (ii) The latest add of $e$ by $j$ in $C \cup H$ is the latest one in $C$ or in $H$, whichever is later. Let $a$ be the $c$-th add of $j$, adding $e$, and the latest add of $e$ by $j$ in $C \cup H$.

- If $a \in C$ and $a \in H$, it is the latest in both, and by (i) it belongs in the target exactly when it is uncovered in both, that is when its triple is in $E \cap E'$ (line 4). Lines 5 and 6 do not add it, because $c \le V'[j]$ and $c \le V[j]$.
- If $a \in C$ and $a \notin H$, then $c > V'[j]$, and $a$ belongs in the target exactly when it is uncovered in $C$, that is when its triple is in $E$; its triple is not in $E'$, and line 5 keeps it.
- The case $a \notin C$, $a \in H$ is the same with line 6.

Every triple in $E$ or $E'$ is the latest add of its element and replica on its side. If it is not the latest in $C \cup H$, the other side has a later add of the same element by the same replica, so it also holds this add, its counter is at most that side's vector entry, and it is not in that side's set; so lines 4 to 6 do not take it. Hence $U = $ the target set. $U$ then has at most one triple per element and replica, and line 8 removes nothing. $\square$

**Theorem 3 (add-wins).** LOOKUP$(e)$ at $i$ returns true exactly when $C_i$ has an uncovered add of $e$.

*Proof.* LOOKUP returns whether $E_i$ has a triple of $e$. By Claim 4 such a triple is an uncovered latest add, and by Claim 3 one exists exactly when an uncovered add of $e$ exists. $\square$

**Theorem 4 (semilattice laws and convergence).** On reachable states, MERGE is commutative, associative and idempotent, and ADD and REMOVE are inflationary in the order $s \le t$ when MERGE$(s, t) = t$. If updates stop and every replica sends its state to every other replica infinitely often over fair-lossy channels, all replicas reach $\Phi$ of the whole history.

*Proof.* By Claim 4, MERGE$(\Phi(C), \Phi(H)) = \Phi(C \cup H)$ for any histories that produce the two states, so the laws of $\cup$ carry over: for example MERGE$(s, t) = \Phi(C \cup H) = \Phi(H \cup C) = $ MERGE$(t, s)$. An update at $i$ turns $C_i$ into a larger history $C'$, and MERGE$(\Phi(C_i), \Phi(C')) = \Phi(C') $, so the update is inflationary. Convergence follows as for the G-Set: after the last update, finitely many merges make every history the set of all events. $\square$

**Termination.** All loops run over finite sets. $\blacksquare$
