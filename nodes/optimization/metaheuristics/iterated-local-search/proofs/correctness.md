---
title: Iterated local search returns the best local optimum it visits
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The objective $f$ is to be minimized, LOCAL-SEARCH is a procedure that stops and returns a local minimum of a neighborhood $N$ (for example [hill climbing](/hill-climbing/)), PERTURB returns a solution, and $K \ge 0$ is the number of iterations. Write $x_0^*$ for the result of line L1, $z_k$ for the local minimum of line L4 in iteration $k$, and $x_k^*$ for the current solution after iteration $k$.

**Lemma 1 (termination).** If LOCAL-SEARCH stops on every input, the algorithm stops after $K + 1$ calls of LOCAL-SEARCH and $K$ calls of PERTURB.

*Proof.* Line L2 makes exactly $K$ passes, and each pass calls PERTURB once and LOCAL-SEARCH once. Line L1 makes the remaining call. $\square$

**Lemma 2 (local optima only).** Every current solution $x_k^*$ and the returned $b$ are local minima of $N$.

*Proof.* $x_0^*$ is the output of LOCAL-SEARCH. Line L5 replaces the current solution only by $z_k$, also an output of LOCAL-SEARCH. Line L6 sets $b$ only to a current solution. $\square$

**Theorem 1 (correctness).** The algorithm returns $b$ with $f(b) = \min_{0 \le k \le K} f(x_k^*)$ and $f(b) \le f(x_0^*)$. With the acceptance rule *better* (accept $z_k$ if $f(z_k) < f(x_{k-1}^*)$), the values $f(x_k^*)$ never increase and $b = x_K^*$.

*Proof.* Line L1 sets $b = x_0^*$, and line L6 replaces $b$ by the current solution exactly when it is strictly better, so by induction $f(b)$ is the least value of a current solution so far. With the rule *better*, the current solution changes only to a strictly better one, so $f(x_k^*) \le f(x_{k-1}^*)$, and the current solution is always the best one so far; line L6 then keeps $b$ equal to it. Together with Lemma 2 and Lemma 1 this proves the claim. $\square$

**Lemma 3 (a success bound).** Let $G$ be a set of solutions, for example the global minima. Suppose that in every iteration, whatever happened before, the new local minimum $z_k$ lies in $G$ with probability at least $q > 0$. Then the probability that no $z_k$ with $k \le K$ lies in $G$ is at most $(1-q)^K \le e^{-qK}$. If $G$ is the set of global minima, $b \in G$ with at least the probability $1 - (1-q)^K$.

*Proof.* Let $A_k$ be the event that $z_k \notin G$. By the assumption, $\Pr[A_k \mid A_1, \ldots, A_{k-1}] \le 1 - q$ for every $k$. By the chain rule, $\Pr[A_1 \cap \cdots \cap A_K] = \prod_k \Pr[A_k \mid A_1, \ldots, A_{k-1}] \le (1 - q)^K$, and $1 - q \le e^{-q}$. If some $z_k$ is a global minimum, then the acceptance rule *better* accepts it unless the current solution is already a global minimum, and line L6 keeps a global minimum in $b$. With the rule *always*, the current solution becomes $z_k$, and line L6 again stores a global minimum. $\square$

**Lemma 4 (the double bridge).** Cut a tour into four nonempty segments $A, B, C, D$ in this order and reconnect them as $A, D, C, B$, without reversing any segment. The new tour has the same cities. It changes at most four edges, and it changes exactly four edges unless two segments that follow each other around the tour, counting $D$ and $A$ as neighbors, have one city each.

*Proof.* The edges inside the segments are kept. The old tour has the four junction edges $\{a_e, b_s\}$, $\{b_e, c_s\}$, $\{c_e, d_s\}$, $\{d_e, a_s\}$, where $a_s$ and $a_e$ are the first and last cities of $A$, and so on. The new tour has the junctions $\{a_e, d_s\}$, $\{d_e, c_s\}$, $\{c_e, b_s\}$, $\{b_e, a_s\}$. So at most four edges change. A new junction is an old edge only if it equals an old junction, since it joins two different segments. Compare $\{a_e, d_s\}$ with the old junctions: it cannot equal $\{a_e, b_s\}$ or $\{c_e, d_s\}$, since the segments are disjoint, nor $\{b_e, c_s\}$; it equals $\{d_e, a_s\}$ exactly when $a_e = a_s$ and $d_s = d_e$, that is, when $A$ and $D$ have one city each. In the same way, $\{d_e, c_s\}$ is old exactly when $C$ and $D$ have one city each, $\{c_e, b_s\}$ exactly when $B$ and $C$ do, and $\{b_e, a_s\}$ exactly when $A$ and $B$ do. $\blacksquare$

**What is not claimed.** Lemma 3 needs a lower bound $q$ that holds in every iteration. For the double bridge followed by 2-opt, no such bound is known in general: from some local minima, the kick and the descent may never reach a global minimum. So iterated local search has no general guarantee of finding a global minimum.
