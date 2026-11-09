---
title: Interpolation-based model checking is sound, and terminates on finite systems
proves: [correctness]
status: full
---

We use the notation of the page. The state set $S$ is finite, $|S| \le 2^n$, and $T$ is total: every state has a successor. This holds for circuits, where every input gives a next state. We identify a formula over one copy of the state variables with the set of states that satisfy it. Tseitin variables of the encoding are existentially quantified; they do not change which states satisfy a formula.

## The interpolation system

Let $A$ and $B$ be sets of clauses with $A \wedge B$ unsatisfiable. A variable is *shared* if it occurs in both, *$A$-local* if it occurs only in $A$. For a clause $C$, write $C \setminus B$ for its literals whose variable does not occur in $B$, and $C \restriction B$ for its literals whose variable occurs in $B$. Then $C = (C \setminus B) \vee (C \restriction B)$.

**Lemma 1.** In a resolution refutation of $A \wedge B$, with the partial interpolants $p(C)$ of the page, every clause $C$ satisfies

- (a) $A \models p(C) \vee (C \setminus B)$,
- (b) $B \wedge p(C) \models C \restriction B$,
- (c) $p(C)$ uses only shared variables.

*Proof.* By induction on the proof. Part (c) is clear from the rules.

*Input clause $C$ of $A$.* $p(C)$ is the disjunction of the literals of $C$ over shared variables. A literal of $C$ whose variable occurs in $B$ is shared, so $p(C) = C \restriction B$. (a) $A \models C = p(C) \vee (C \setminus B)$. (b) $p(C) \models C \restriction B$.

*Input clause $C$ of $B$.* $p(C) = \mathit{true}$, and all variables of $C$ occur in $B$, so $C \restriction B = C$. (a) is trivial, and (b) holds as $B \models C$.

*Resolvent* $D_1 \vee D_2$ of $C_1 = v \vee D_1$ and $C_2 = \neg v \vee D_2$.

If $v$ is $A$-local, then $p = p(C_1) \vee p(C_2)$. By (a) for $C_1$ and $C_2$, and since $v$ and $\neg v$ are in $C_i \setminus B$, we have $A \models p(C_1) \vee v \vee (D_1 \setminus B)$ and $A \models p(C_2) \vee \neg v \vee (D_2 \setminus B)$. Resolution on $v$ gives (a) for the resolvent. By (b), $B \wedge p(C_i) \models D_i \restriction B$, as $v$ does not occur in $B$. So $B \wedge (p(C_1) \vee p(C_2)) \models (D_1 \vee D_2) \restriction B$.

If $v$ occurs in $B$, then $p = p(C_1) \wedge p(C_2)$. By (a), $A \models p(C_i) \vee (D_i \setminus B)$, as $v \notin C_i \setminus B$. So $A \models (p(C_1) \wedge p(C_2)) \vee (D_1 \setminus B) \vee (D_2 \setminus B)$. By (b), $B \wedge p(C_1) \models v \vee (D_1 \restriction B)$ and $B \wedge p(C_2) \models \neg v \vee (D_2 \restriction B)$. Resolution on $v$ gives (b) for the resolvent. ∎

For the empty clause, (a) and (b) give $A \models J$ and $J \wedge B \models \mathit{false}$, with $J = p(\square)$ over shared variables: $J$ is a Craig interpolant. A CDCL solver derives each learned clause, and the empty clause at the end, by a chain of resolution steps from earlier clauses, so it computes the same values when it applies the rules along each chain.

## The image query

Fix $k \ge 1$ and a state set $R$. Line L5 builds $A = R(s_0) \wedge T(s_0, s_1)$ and $B = T(s_1, s_2) \wedge \cdots \wedge T(s_{k-1}, s_k) \wedge \bigvee_{j=1}^{k} \neg P(s_j)$. The only variables in both are those of $s_1$. Say that a state $t$ is *$k$-safe* if no path of length less than $k$ from $t$ ends in a state that violates $P$; the path of length 0 counts, so a $k$-safe state satisfies $P$.

**Lemma 2.** $A \wedge B$ is satisfiable if and only if a state of $R$ has a path of length between 1 and $k$ to a state that violates $P$. If it is unsatisfiable, the interpolant $J$ contains every successor of a state of $R$, and every state of $J$ is $k$-safe.

*Proof.* A model of $A \wedge B$ gives $s_0 \in R$ and a path $s_0, \ldots, s_k$ with some $s_j$, $j \ge 1$, outside $P$. Conversely, such a path to a bad state at step $j \le k$ extends to length $k$, as $T$ is total, and gives a model.

Let $t$ be a successor of $s_0 \in R$. The assignment with these values of $s_0$ and $s_1$, and the matching values of the Tseitin variables, satisfies $A$. So $J(t)$ holds, by $A \models J$. Let $t$ satisfy $J$, and suppose a path from $t$ of length $d < k$ ends in a state outside $P$. Extend it to $k - 1$ steps, which $T$ allows. With $s_1 = t$ this satisfies $B$, and $J$ holds in $s_1$, which contradicts the unsatisfiability of $J \wedge B$. ∎

## Soundness

**Lemma 3.** In each round $k$, at line L5, $R = I \cup J_1 \cup \cdots \cup J_r$, where each $J_i$ is an interpolant from round $k$. So $I \subseteq R$, and every state of $R$ is initial or $k$-safe. In particular $R \subseteq P$.

*Proof.* Line L3 sets $R = I$, and line L11 adds $J$ to $R$. Each $J$ is $k$-safe by Lemma 2. $I \subseteq P$ by line L1, and $k$-safe states satisfy $P$. ∎

**Theorem 1 (soundness of HOLDS).** If line L10 returns HOLDS, then $R$ is an inductive invariant and $P$ holds in every reachable state.

*Proof.* By Lemma 2, every successor of $R$ is in $J$, and $J \subseteq R$ by the test. So $R$ is closed under successors. $I \subseteq R$ and $R \subseteq P$ by Lemma 3. By induction on the length of a path, every reachable state is in $R$, so it satisfies $P$. ∎

**Theorem 2 (soundness of FAILS).** If line L1 or line L7 returns FAILS, the system has a counterexample.

*Proof.* Line L1 gives an initial state that violates $P$. At line L7, $R = I$, since $\mathit{exact}$ is true only before the first execution of line L11 in the round. By Lemma 2 the model gives a path from an initial state to a state that violates $P$. The implementation cuts the path at the first bad state. ∎

## Termination

**Lemma 4.** In each round $k$ the loop of line L4 runs at most $|S|$ times.

*Proof.* Each pass that does not leave the loop reaches line L11 with $J \not\subseteq R$, so $R$ gains at least one state. $R \subseteq S$. ∎

Let $D$ be the set of states that have a path to a state outside $P$, and for $t \in D$ let $\mathrm{dist}(t)$ be the length of a shortest such path. Let $b = \max_{t \in D} \mathrm{dist}(t)$, or $b = 0$ if $D$ is empty. A shortest path visits no state twice, so $b \le |S| - 1$.

**Theorem 3 (termination and completeness).** If $P$ is an invariant, the algorithm returns HOLDS in some round $k \le b + 1 \le |S|$. If $P$ is not an invariant and $m$ is the length of a shortest counterexample, it returns FAILS in some round $k \le m$.

*Proof.* Suppose $P$ is an invariant, and consider round $k = b + 1$ if it is reached. No initial state is in $D$, since otherwise a path from it would reach a bad state. A state in $D$ has a path of length at most $b = k - 1$ to a bad state, so it is not $k$-safe. By Lemma 3, $R \cap D = \emptyset$ throughout the round. By Lemma 2, a satisfiable query needs a state of $R$ with a path to a bad state, that is, a state of $R \cap D$. So no query in this round is satisfiable, and by Lemma 4 the loop ends at line L10 with HOLDS. Rounds before $k = b + 1$ cannot return FAILS, by Theorem 2. So the algorithm returns HOLDS in round $b + 1$ or earlier.

Suppose $P$ is not an invariant. Then $m \ge 1$, as line L1 handles $m = 0$. No round returns HOLDS, by Theorem 1, and each round ends, by Lemma 4. In round $m$, if reached, the first query has $R = I$ and is satisfiable by the shortest counterexample and Lemma 2, so line L7 returns FAILS. ∎
