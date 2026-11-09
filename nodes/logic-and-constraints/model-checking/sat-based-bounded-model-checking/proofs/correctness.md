---
title: BMC returns real and shortest counterexamples, and the lasso search is complete for F q
proves: [correctness]
status: full
---

We use the notation of the page. A system has the state set $S = \{0, 1\}^n$, the input set $W$, initial states $I$, and next-state function $f : S \times W \to S$, so that $T(s, s')$ holds when $s' = f(s, w)$ for some $w \in W$. Every state has a successor, because $W$ is not empty. A path of length $k$ is a sequence $s_0, \ldots, s_k$ with $T(s_i, s_{i+1})$ for $i < k$.

**Lemma 1 (the encoding).** For each $k$, the models of the CNF of $\llbracket M \rrbracket_k$, restricted to the state and input variables, are exactly the pairs of a path $s_0, \ldots, s_k$ with $s_0 \in I$ and an input sequence $w_0, \ldots, w_{k-1}$ with $s_{i+1} = f(s_i, w_i)$. Each such pair extends to exactly one model of the CNF.

*Proof.* The Tseitin transformation introduces a variable $g$ for each gate with inputs $a$ and $b$, and clauses that are equivalent to $g \leftrightarrow \mathrm{op}(a, b)$. Given values of the state and input variables of step $i$, the values of the gate variables of step $i$ are forced, in topological order, and they equal the values of the gates. The 2 clauses for latch $j$ say $x_j^{(i+1)} \leftrightarrow f_j^{(i)}$, where $f_j^{(i)}$ is the literal of the output of the next-state function at step $i$. The unit clauses fix $s_0$ to an initial state. So an assignment to all variables satisfies the clauses if and only if $s_0 \in I$, each $s_{i+1} = f(s_i, w_i)$, and each gate variable has its forced value. Constant folding replaces a gate with a constant input by the equivalent constant or literal, which does not change the set of models restricted to the state and input variables. ∎

**Theorem 1 (safety).** BMC-SAFETY returns a path only if it is a counterexample: $s_0 \in I$, each step is a transition, and $\neg P(s_k)$. If the system has a counterexample of length at most $k_{\max}$, BMC-SAFETY returns one, and the returned one has the least possible length $k^*$. Moreover $P$ holds on $s_0, \ldots, s_{k^*-1}$.

*Proof.* The formula of round $k$ is $\llbracket M \rrbracket_k \wedge \neg P(s_k)$, with $\neg P(s_k)$ encoded by Tseitin variables and a unit clause. By Lemma 1, its models are exactly the paths of length $k$ from $I$ that end in a state where $P$ is false, with their gate values. So round $k$ answers SAT if and only if a counterexample of length exactly $k$ exists, and the path read from the model is one. The loop tries $k = 0, 1, \ldots$ in order, so it returns in round $k^*$, the least length of a counterexample, if $k^* \le k_{\max}$. If some $s_j$ with $j < k^*$ had $\neg P(s_j)$, the prefix $s_0, \ldots, s_j$ would be a counterexample of length $j < k^*$, a contradiction. ∎

**Lemma 2 (lassos).** In a finite system in which every state has a successor, there is an infinite path from $I$ on which $q$ is false in every state if and only if there are $k \le |S| - 1$, $l \le k$ and a path $s_0, \ldots, s_k$ from $I$ with $T(s_k, s_l)$ and $\neg q(s_i)$ for all $i \le k$.

*Proof.* ($\Leftarrow$) The infinite sequence $s_0, \ldots, s_{l-1}, (s_l, \ldots, s_k)^\omega$ is a path, because $T(s_k, s_l)$ holds and the other steps are steps of the finite path. Every state on it is one of $s_0, \ldots, s_k$, where $q$ is false.

($\Rightarrow$) Let $s_0, s_1, \ldots$ be an infinite path from $I$ with $q$ false everywhere. Among $s_0, \ldots, s_{|S|}$ there are $|S| + 1$ states, so two are equal. Let $k + 1$ be the least index such that $s_{k+1} = s_l$ for some $l \le k$. Then $s_0, \ldots, s_k$ are pairwise distinct, so $k + 1 \le |S|$, and $T(s_k, s_{k+1}) = T(s_k, s_l)$. ∎

**Theorem 2 (liveness).** BMC-LASSO returns a lasso only if it is a counterexample to $\mathbf{F}\, q$. If $\mathbf{F}\, q$ fails, BMC-LASSO with $k_{\max} \ge 2^n - 1$ returns a lasso.

*Proof.* In round $k$, line L8 adds a fresh copy $s_{\mathrm{back}}$ with $T(s_k, s_{\mathrm{back}})$, encoded as in Lemma 1 with its own inputs $w_k$. The clauses of line L10 say $e_l \rightarrow (s_{\mathrm{back}} = s_l)$, bit by bit: the clause $\neg e_l \vee \neg a \vee b$ is $e_l \wedge a \rightarrow b$, and $\neg e_l \vee a \vee \neg b$ is $e_l \wedge b \rightarrow a$. Line L11 forces some $e_l$. So a model gives a path $s_0, \ldots, s_k$ from $I$ with $\neg q$ in each state and $T(s_k, s_l)$ for an $l$ with $e_l$ true. By Lemma 2 ($\Leftarrow$), this lasso is an infinite path on which $q$ never holds, so $\mathbf{F}\, q$ fails on it. Conversely, if $\mathbf{F}\, q$ fails, there is an infinite path from $I$ on which $q$ is always false. By Lemma 2 ($\Rightarrow$) there is a lasso with $k \le |S| - 1 = 2^n - 1$. Setting $s_{\mathrm{back}} = s_l$, $e_l$ true and the other selectors false gives a model of round $k$. So the loop returns at the latest in round $k$. ∎

**Remark.** Both theorems need $W \ne \emptyset$ only for Lemma 2. Theorem 1 holds for any transition relation. Without the loop condition, round $k$ of BMC-LASSO would accept any path of length $k$ with $q$ false, and such a path can be the prefix of a path on which $q$ holds later; this is why line L11 is needed.
