---
title: k-induction is sound, and complete for finite systems with simple paths
proves: [correctness]
status: full
---

We use the notation of the page. The state set $S$ is finite, $|S| \le 2^n$. A path of length $m$ is a sequence $s_0, \ldots, s_m$ with $T(s_i, s_{i+1})$ for $i < m$; it is *simple* if its states are pairwise distinct. A counterexample is a path with $s_0 \in I$ and $\neg P(s_m)$. For $k \ge 0$ we write

- $\mathrm{Base}(k)$: no counterexample of length exactly $k$ exists (line L2 is unsatisfiable);
- $\mathrm{Step}(k)$: no simple path $s_0, \ldots, s_{k+1}$ has $P(s_0), \ldots, P(s_k)$ and $\neg P(s_{k+1})$ (lines L4 to L6 give unsatisfiable);
- $\mathrm{Step}^{\circ}(k)$: the same without the word "simple" (the variant without line L5).

By Lemma 1 of the [SAT-based BMC](/sat-based-bounded-model-checking/) proof, the formula of line L2 is satisfiable if and only if a counterexample of length $k$ exists, and the formula of lines L4 and L5 is satisfiable if and only if a simple path as in $\mathrm{Step}(k)$ exists: the clause $\bigvee_t (x_t^{(i)} \oplus x_t^{(j)})$ holds exactly when $s_i \ne s_j$. So line L2 decides $\mathrm{Base}(k)$, and line L6 decides $\mathrm{Step}(k)$.

**Lemma 1.** A shortest counterexample is a simple path, and $P$ holds on all its states but the last.

*Proof.* Let $s_0, \ldots, s_m$ be a counterexample of least length. If $s_i = s_j$ with $i < j$, then $s_0, \ldots, s_i, s_{j+1}, \ldots, s_m$ is a counterexample of length $m - (j - i) < m$. If $\neg P(s_j)$ with $j < m$, then $s_0, \ldots, s_j$ is a counterexample of length $j < m$. Both contradict the choice of $m$. ∎

**Theorem 1 (soundness of HOLDS).** If $\mathrm{Base}(j)$ holds for all $j \le k$ and $\mathrm{Step}(k)$ holds, then $P$ is an invariant. The same is true with $\mathrm{Step}^{\circ}(k)$ in place of $\mathrm{Step}(k)$.

*Proof.* Assume that $P$ is not an invariant, and let $s_0, \ldots, s_m$ be a shortest counterexample. By the base cases, $m > k$, so $m - k - 1 \ge 0$. By Lemma 1, the path $s_{m-k-1}, \ldots, s_m$ has $k + 2$ pairwise distinct states, $P$ holds in the first $k + 1$ of them, and $P$ fails in the last. This path violates $\mathrm{Step}(k)$. As $\mathrm{Step}^{\circ}(k)$ excludes more paths, it is violated too. ∎

When the algorithm returns HOLDS at round $k$, it has checked $\mathrm{Base}(j)$ in rounds $j = 0, \ldots, k$ (each of them was unsatisfiable, or the algorithm would have returned FAILS), and $\mathrm{Step}(k)$. So by Theorem 1 the answer is correct.

**Theorem 2 (soundness of FAILS).** If the algorithm returns FAILS in round $k$, the returned path is a counterexample of the least possible length.

*Proof.* The model of line L2 gives a counterexample of length $k$, and rounds $0, \ldots, k - 1$ found none, so no shorter counterexample exists. ∎

**Theorem 3 (completeness with simple paths).** If $P$ is an invariant, then $\mathrm{Step}(k)$ holds for every $k \ge |S| - 1$, and the algorithm with $k_{\max} \ge |S| - 1$ returns HOLDS. If $P$ is not an invariant, the algorithm with $k_{\max}$ at least the length of a shortest counterexample returns FAILS.

*Proof.* If $P$ is an invariant, no counterexample exists, so every base case is unsatisfiable. A simple path with $k + 2$ states needs $k + 2 \le |S|$. For $k \ge |S| - 1$ there is none, so $\mathrm{Step}(k)$ holds vacuously, and the algorithm stops with HOLDS in round $|S| - 1$ or earlier. If $P$ is not an invariant, let $m$ be the length of a shortest counterexample. For $j < m$ the base case is unsatisfiable, and the step case cannot succeed in a round $j < m$, since by Theorem 1 that would make $P$ an invariant. So round $m$ is reached, and its base case returns FAILS. ∎

**Remark (the constraint is needed).** Without line L5, completeness fails. In the example of the page, the state $(1, 0)$ satisfies $P$ and has itself as a successor (input $e = 0$) and the bad state $(1, 1)$ as a successor (input $e = 1$). So for each $k$ the path $(1, 0)^{k+1}, (1, 1)$ violates $\mathrm{Step}^{\circ}(k)$, although $P$ is an invariant.

**Remark (monotonicity).** If $\mathrm{Step}(k)$ holds, so does $\mathrm{Step}(k+1)$: a simple path that violates $\mathrm{Step}(k+1)$ has a suffix of $k + 2$ states, which is simple and violates $\mathrm{Step}(k)$.
