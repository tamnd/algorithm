---
title: The planning graph is monotone, its mutexes are sound, and it levels off after at most n(n+1)/2 + 1 levels
proves: [correctness, termination]
status: full
---

We use the notation and the pseudocode of the page. The task is $(F, A, I, G)$ with $n = |F|$. Two actions interfere when one deletes a precondition or an add effect of the other. A parallel step in a state $s$ is a set of pairwise non-interfering actions, all applicable in $s$, and its result is $(s \setminus \bigcup \mathrm{del}) \cup \bigcup \mathrm{add}$. Let $R_k$ be the set of states reachable from $I$ by at most $k$ parallel steps. So $R_0 = \{I\}$ and $R_k \subseteq R_{k+1}$.

Write $N_k$ for the set of non-mutex pairs at fact level $k$: the unordered pairs $\{p, q\}$ with $p, q \in P_k$ (we allow $p = q$) and $\{p, q\} \notin FM_k$. A fact $p$ is in $P_k$ exactly when $\{p\} = \{p, p\} \in N_k$.

**Lemma 1 (monotonicity).** For every $k$ for which level $k+1$ exists: $N_k \subseteq N_{k+1}$. If level $k+1$ exists, then $A_k \subseteq A_{k+1}$, and two actions of $A_k$ that are not mutex in $AM_k$ are not mutex in $AM_{k+1}$.

*Proof.* We show the two claims together by induction on $k$, first for the facts and then for the actions.

Base, the facts at $k = 0$. $FM_0 = \emptyset$, so $N_0$ is the set of all pairs of $I$. Take $p, q \in I$. Their no-ops are in $A_0$, and they are not mutex in $AM_0$: a no-op deletes nothing, so there is no interference, and the precondition pair $\{p, q\}$ is not in $FM_0$, so there are no competing needs. If $p = q$, the no-op puts $p$ in $P_1$. If $p \ne q$, the no-ops are distinct achievers of $p$ and $q$ that are not mutex, so line L11 does not mark $\{p, q\}$. So $N_0 \subseteq N_1$.

Step for the actions. Suppose $N_k \subseteq N_{k+1}$. An action enters $A_k$ when its preconditions are in $P_k$ and pairwise not mutex, that is, when all pairs of its preconditions are in $N_k$. These pairs are in $N_{k+1}$, so the action enters $A_{k+1}$. A no-op of $f \in P_k$ is in $A_{k+1}$ because $f \in P_{k+1}$. Now take $a, b \in A_k$ that are not mutex in $AM_k$. They do not interfere, and interference does not depend on the level. For $p \in \mathrm{pre}(a)$ and $q \in \mathrm{pre}(b)$, the pair is in $N_k \subseteq N_{k+1}$, so there are no competing needs at level $k+1$ either.

Step for the facts. Suppose the action claim holds for level $k$, and let $\{p, q\} \in N_{k+1}$. If $p = q$, some action $a \in A_k$ adds $p$; then $a \in A_{k+1}$, so $p \in P_{k+2}$. If $p \ne q$, line L11 did not mark the pair, so there are achievers $a$ of $p$ and $b$ of $q$ in $A_k$ with $a = b$ or $\{a, b\} \notin AM_k$. Both are in $A_{k+1}$, and by the action claim, $a = b$ or $\{a, b\} \notin AM_{k+1}$. So line L11 does not mark $\{p, q\}$ at level $k+2$, and $\{p, q\} \in N_{k+2}$. $\square$

So $P_k \subseteq P_{k+1}$, and a pair of $P_k$ that is mutex at level $k+1$ was already mutex at level $k$. Mutexes only disappear.

**Theorem 1 (soundness).** For every $k$ and every $s \in R_k$, every pair of facts of $s$ (including $\{p, p\}$) is in $N_k$. If level $k+1$ exists, then every parallel step $S$ applicable in $s$ satisfies $S \subseteq A_k$, and no two actions of $S$ are mutex in $AM_k$.

*Proof.* By induction on $k$. For $k = 0$, $R_0 = \{I\}$ and $N_0$ holds all pairs of $I$.

Suppose the fact claim holds at level $k$, and let $s \in R_k$ and $S$ a parallel step applicable in $s$. Each $a \in S$ has $\mathrm{pre}(a) \subseteq s$, so all pairs of $\mathrm{pre}(a)$ are in $N_k$, and line L3 puts $a$ in $A_k$. Take $a \ne b$ in $S$. They do not interfere, by the definition of a parallel step. For $p \in \mathrm{pre}(a)$ and $q \in \mathrm{pre}(b)$, both facts are in $s$, so $\{p, q\} \in N_k$ and there are no competing needs. So $\{a, b\} \notin AM_k$.

Now the fact claim at level $k+1$. Let $s' \in R_{k+1}$. If $s' \in R_k$, then $s'$ is reached by at most $k$ steps, and by the fact claim at level $k$ and Lemma 1, every pair of $s'$ is in $N_k \subseteq N_{k+1}$. Otherwise $s'$ is the result of a parallel step $S$ in some $s \in R_k$. Add to $S$ the no-ops of the facts of $s$ that no action of $S$ deletes, and call the result $S^+$. Every fact of $s'$ has an achiever in $S^+$: either an action of $S$ adds it, or it is in $s$ and not deleted, and then its no-op adds it. Every member of $S^+$ is in $A_k$ (a no-op of $f \in s \subseteq P_k$ is in $A_k$ by line L1). No two members of $S^+$ are mutex in $AM_k$. For two actions of $S$ this is the step above. For a no-op of $f$ and an action $a \in S$: $a$ does not delete $f$ by the choice of the no-ops, the no-op deletes nothing, and the pairs of preconditions are pairs of $s$, so they are in $N_k$. For two no-ops of $f, g \in s$: they delete nothing and $\{f, g\} \in N_k$. Now take two facts $p, q$ of $s'$, with achievers $a, b \in S^+$. Then $a = b$ or $\{a, b\} \notin AM_k$, so line L11 does not mark $\{p, q\}$, and $p, q \in P_{k+1}$ by line L8. So $\{p, q\} \in N_{k+1}$. $\square$

**Corollary.** If a plan of at most $k$ parallel steps reaches the goal, then the goal holds at level $k$: $G \subseteq P_k$ and no two goals are mutex. Hence the first level at which the goal holds is a lower bound on the number of parallel steps of every plan, and so also on the number of actions of every sequential plan.

*Proof.* The final state of the plan is in $R_k$ and contains $G$. Apply Theorem 1. $\square$

**Theorem 2 (level off).** Let $L$ be the first $k \ge 1$ with $P_k = P_{k-1}$ and $FM_k = FM_{k-1}$. Then $L \le n(n+1)/2 + 1$, and $P_j = P_L$ and $FM_j = FM_L$ for all $j \ge L$.

*Proof.* Level $k+1$ is computed from $P_k$ and $FM_k$ alone (and the fixed action set), so equal inputs give equal outputs: once two consecutive levels are equal, all later levels are equal. By Lemma 1, $N_0 \subseteq N_1 \subseteq \cdots$. If $N_k = N_{k+1}$, then $P_k = P_{k+1}$ (the pairs $\{p, p\}$) and $FM_k = FM_{k+1}$ (the pairs of $P_k$ not in $N_k$). So before the level off each step adds at least one pair to $N$. There are $n(n+1)/2$ unordered pairs with repetition over $n$ facts, so at most $n(n+1)/2$ strict increases can occur, and the first $k$ with $N_{k-1} = N_k$ is at most $n(n+1)/2 + 1$. $\square$

**Remark (not complete).** The converse of Theorem 1 is false. In the task of the mutex relation page, two tokens can be put on three slots $x$, $y$, $z$, one token per slot, and the facts $u$ (needs $x$ and $y$) and $v$ (needs $z$) are never true together, because that needs three tokens. The rules look only at pairs, and every pair among $x$, $y$, $z$ is reachable, so $\{u, v\}$ is never marked.
