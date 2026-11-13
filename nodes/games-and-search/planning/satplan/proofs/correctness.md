---
title: The models of the SATPLAN formula are exactly the parallel plans of k steps, and SATPLAN returns a plan with the fewest steps
proves: [correctness, termination]
status: full
---

We use the notation and the pseudocode of the page. The task is $(F, A, I, G)$ with $n = |F|$ facts and $m = |A|$ actions, and for each action $a$ the sets $\mathrm{add}(a)$ and $\mathrm{del}(a)$ are disjoint. Two distinct actions *interfere* when one deletes a precondition or an add effect of the other. A *step* is a set $S$ of actions, applicable in a state $s$ (every precondition holds in $s$), of which no two interfere. Its result is $s' = (s \setminus D) \cup P$ with $D = \bigcup_{a \in S} \mathrm{del}(a)$ and $P = \bigcup_{a \in S} \mathrm{add}(a)$. The empty step is allowed. A *parallel plan of $k$ steps* is a sequence $S_1, \ldots, S_k$ of steps with states $s_0 = I$ and $s_t$ the result of $S_t$ in $s_{t-1}$, such that $G \subseteq s_k$.

The formula $\Phi_k$ has a variable $f_t$ for each fact $f$ and time $0 \le t \le k$, and a variable $a_t$ for each action $a$ and step $1 \le t \le k$. Its clauses are those of lines L6 to L10:

- (L6) $f_0$ for $f \in I$ and $\neg f_0$ for $f \notin I$;
- (L7) $g_k$ for $g \in G$;
- (L8) for each $t$ and $a$: $\neg a_t \lor p_{t-1}$ for $p \in \mathrm{pre}(a)$, $\neg a_t \lor f_t$ for $f \in \mathrm{add}(a)$, and $\neg a_t \lor \neg f_t$ for $f \in \mathrm{del}(a)$;
- (L9) for each $t$ and $f$: $\neg f_{t-1} \lor f_t \lor \bigvee_{a : f \in \mathrm{del}(a)} a_t$ and $f_{t-1} \lor \neg f_t \lor \bigvee_{a : f \in \mathrm{add}(a)} a_t$;
- (L10) for each $t$ and each interfering pair $a, b$: $\neg a_t \lor \neg b_t$.

For an assignment $\sigma$ write $s_t^\sigma = \{f : \sigma(f_t) = 1\}$ and $S_t^\sigma = \{a : \sigma(a_t) = 1\}$.

## Lemma 1. A step result is consistent

Let $S$ be a step in $s$, with $D$ and $P$ as above. Then $D \cap P = \emptyset$.

*Proof.* Suppose $f \in \mathrm{del}(b) \cap \mathrm{add}(a)$ with $a, b \in S$. If $a = b$, this contradicts the disjointness of add and del. If $a \neq b$, then $b$ deletes an add effect of $a$, so $a$ and $b$ interfere, which a step does not allow. $\square$

## Theorem 1. Models are plans

If $\sigma$ satisfies $\Phi_k$, then $S_1^\sigma, \ldots, S_k^\sigma$ is a parallel plan of $k$ steps, and its states are $s_0^\sigma, \ldots, s_k^\sigma$.

*Proof.* By the L6 clauses, $s_0^\sigma = I$. Fix $t \ge 1$ and assume that $s_{t-1}^\sigma$ is the state before step $t$. Write $S = S_t^\sigma$.

*$S$ is a step in $s_{t-1}^\sigma$.* For $a \in S$ and $p \in \mathrm{pre}(a)$, the clause $\neg a_t \lor p_{t-1}$ gives $p \in s_{t-1}^\sigma$. For distinct interfering $a, b$, the L10 clause forbids that both are in $S$.

*The result of $S$ is $s_t^\sigma$.* Let $s' = (s_{t-1}^\sigma \setminus D) \cup P$. We show $f \in s'$ if and only if $f \in s_t^\sigma$, by cases.

1. $f \in P$. Some $a \in S$ adds $f$, and the clause $\neg a_t \lor f_t$ gives $f \in s_t^\sigma$. Also $f \in s'$.
2. $f \in D$. By Lemma 1, $f \notin P$, so $f \notin s'$. Some $a \in S$ deletes $f$, and the clause $\neg a_t \lor \neg f_t$ gives $f \notin s_t^\sigma$.
3. $f \notin P \cup D$ and $f \in s_{t-1}^\sigma$. Then $f \in s'$. The first L9 clause for $f$ and $t$ has $f_{t-1}$ true and every $a_t$ with $f \in \mathrm{del}(a)$ false, so $f_t$ is true.
4. $f \notin P \cup D$ and $f \notin s_{t-1}^\sigma$. Then $f \notin s'$. The second L9 clause has $f_{t-1}$ false and every $a_t$ with $f \in \mathrm{add}(a)$ false, so $f_t$ is false.

By induction on $t$, every $s_t^\sigma$ is the state after $t$ steps. The L7 clauses give $G \subseteq s_k^\sigma$. $\square$

## Theorem 2. Plans are models

If $S_1, \ldots, S_k$ is a parallel plan of $k$ steps with states $s_0, \ldots, s_k$, then the assignment $\sigma$ with $\sigma(f_t) = [f \in s_t]$ and $\sigma(a_t) = [a \in S_t]$ satisfies $\Phi_k$. It is the only model $\sigma'$ with $S_t^{\sigma'} = S_t$ for all $t$.

*Proof.* L6 holds because $s_0 = I$, and L7 because $G \subseteq s_k$. For L8: an action in $S_t$ is applicable in $s_{t-1}$; its add effects are in $P \subseteq s_t$; its delete effects are in $D$, and by Lemma 1 they are not in $P$, so they are not in $s_t$. For the first L9 clause: if $f \in s_{t-1}$ and $f \notin s_t$, then $f \in D$, so some action of $S_t$ deletes $f$. For the second: if $f \notin s_{t-1}$ and $f \in s_t$, then $f \in P$, so some action of $S_t$ adds $f$. L10 holds because no two actions of a step interfere.

For uniqueness, let $\sigma'$ be a model with the same action values. By Theorem 1, $s_t^{\sigma'}$ is the state after the steps $S_1, \ldots, S_t$ from $I$, which is $s_t$. So $\sigma'$ and $\sigma$ agree on the fact variables too. $\square$

**Corollary.** The map $\sigma \mapsto (S_1^\sigma, \ldots, S_k^\sigma)$ is a bijection from the models of $\Phi_k$ to the parallel plans of $k$ steps. In particular, $\Phi_k$ is satisfiable if and only if a parallel plan of $k$ steps exists, and the decoded plan of line L4 is valid.

## Lemma 2. Monotonicity

If a parallel plan of $k$ steps exists, then one of $k + 1$ steps exists, and a plan of $j$ nonempty steps gives a plan of $k$ steps for every $k \ge j$.

*Proof.* Append empty steps. The empty step is applicable everywhere and leaves the state unchanged. $\square$

## Theorem 3. SATPLAN returns a plan with the fewest steps

Let $K$ be the bound of line L1. If some parallel plan has at most $K$ steps, SATPLAN returns a parallel plan with the fewest steps $k^*$, and none of its steps is empty. Otherwise it returns no plan.

*Proof.* The loop tries $k = 0, 1, \ldots, K$ in order, and the solver is complete, so line L4 is reached at the first $k$ for which $\Phi_k$ is satisfiable. By the corollary and Lemma 2, $\Phi_k$ is satisfiable exactly when $k \ge k^*$. So SATPLAN stops at $k = k^*$ when $k^* \le K$, and the decoded plan is valid. If one of its steps were empty, removing it would give a plan of $k^* - 1$ steps, which contradicts the choice of $k^*$. If $k^* > K$ or no plan exists, every $\Phi_k$ with $k \le K$ is unsatisfiable, and line L5 returns no plan. $\square$

## Theorem 4. The default bound decides plan existence

With $K = 2^n - 1$, SATPLAN returns no plan exactly when the task has no plan.

*Proof.* If a sequential plan exists, take a shortest one. It visits no state twice, since otherwise the part between the two visits could be cut out. There are at most $2^n$ states, so it has at most $2^n - 1$ actions. Each action alone is a step (a single action interferes with nothing), so it is a parallel plan of at most $K$ steps, and Theorem 3 applies. Conversely, every parallel plan gives a sequential plan by listing the actions of each step in any order: an action of a step is applicable after the others, because no other action of the step deletes its preconditions, and the final state is the same, because no action of the step deletes an add effect of another. So if no sequential plan exists, no parallel plan exists, and SATPLAN returns no plan. $\square$

## Termination

The loop of line L1 runs at most $K + 1$ times. Each formula $\Phi_k$ is finite and is built in time linear in its size. DPLL terminates on a finite formula: each recursive call assigns at least one more variable, so the recursion depth is at most the number of variables and each call branches at most twice. So SATPLAN terminates. $\square$
