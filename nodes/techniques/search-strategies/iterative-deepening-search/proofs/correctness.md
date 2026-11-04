---
title: Iterative deepening search returns a path with the fewest actions, and it costs at most b/(b-1) times breadth-first search
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode of the page and the facts proved for [depth-limited search](/depth-limited-search/) with the check for cycles, for a problem in which each state has finitely many successors.

- **(D1)** Each run of DEPTH-LIMITED-SEARCH with limit $\ell$ stops.
- **(D2)** It returns a path if and only if some goal has a path of at most $\ell$ actions from $s_0$, and then it returns such a path.
- **(D3)** If it returns failure, no goal can be reached from $s_0$.
- **(D4)** If it returns cutoff, some path from $s_0$ that repeats no state has more than $\ell$ actions.

Let $d$ be the least number of actions of a path from $s_0$ to a goal, with $d = \infty$ when no goal can be reached.

**Theorem 1 (the result has the fewest actions).** If the search returns a path, the path goes from $s_0$ to a goal and has exactly $d$ actions.

*Proof.* Let the loop return a path in the run with limit $\ell$. By (D2) the path goes from $s_0$ to a goal and has at most $\ell$ actions, so $d \le \ell$. If $d < \ell$, the run with limit $d$ came earlier. By (D2) it returned a path, and line L3 returned it, so the loop never reached $\ell$. Hence $d = \ell$, and the path has at most $d$ actions. No path to a goal has fewer than $d$ actions, so it has exactly $d$. $\square$

**Theorem 2 (completeness).** If a goal can be reached, the search returns a path after the runs with the limits $0, 1, \ldots, d$.

*Proof.* For $\ell < d$, no goal has a path of at most $\ell$ actions, so by (D2) the run does not return a path, and by (D3) it does not return failure, because a goal can be reached. So it returns cutoff, and the loop goes on. By (D1) each run stops. The run with $\ell = d$ returns a path by (D2). $\square$

**Theorem 3 (failure).** If the search returns failure, no goal can be reached. If the state space reachable from $s_0$ is finite and contains no goal, the search returns failure.

*Proof.* Failure is returned at line L3 only when a run returns failure, and (D3) applies. For the second part, let $L$ be the largest number of actions of a path from $s_0$ that repeats no state. It is finite, because a finite space has finitely many such paths. The run with $\ell = L$ cannot return a path, since no goal is reachable, and it cannot return cutoff by (D4). So it returns failure, and by (D1) each earlier run stops. $\square$

**Theorem 4 (nodes generated).** In a tree in which each node has at most $b \ge 2$ children and the search stops in the run with limit $d$, the search generates fewer than $\frac{b}{b-1} S_d$ nodes, where $S_\ell = \sum_{i=1}^{\ell} b^i$.

*Proof.* A run with limit $\ell$ generates only nodes of depth 1 to $\ell$, at most $b^i$ of depth $i$, so at most $S_\ell$ nodes. The total is at most $\sum_{\ell=1}^{d} S_\ell$. For $1 \le \ell \le d$,
$$ \frac{S_\ell}{S_d} = \frac{b^\ell - 1}{b^d - 1} \le \frac{b^\ell}{b^d}, $$
because $(b^\ell - 1) b^d \le (b^d - 1) b^\ell$ is the same as $b^\ell \le b^d$. So
$$ \sum_{\ell=1}^{d} S_\ell \le S_d \sum_{\ell=1}^{d} b^{\ell - d} = S_d \sum_{j=0}^{d-1} b^{-j} < S_d \cdot \frac{1}{1 - 1/b} = \frac{b}{b-1} S_d. \qquad \blacksquare $$
