---
title: Hill climbing stops at a local minimum of its neighborhood
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is a finite or infinite set $S$ of solutions, a start $x_0 \in S$, an objective $f : S \to \mathbb{R}$ to minimize, and a neighborhood $N(x) \subseteq S$ for each $x \in S$, listed in a fixed order. We assume that $f$ takes finitely many values on the solutions that can be reached from $x_0$ by moves to neighbors. This holds when $S$ is finite. A solution $x$ is a *local minimum* of $N$ if $f(y) \ge f(x)$ for each $y \in N(x)$.

**Lemma 1 (one pass of the inner loop).** Consider one pass of lines L3 to L7 with the current solution $x$.

- (a) If line L8 finds $y^* = $ none, then $f(y) \ge f(x)$ for each $y \in N(x)$.
- (b) If $y^* \ne$ none, then $y^* \in N(x)$ and $f(y^*) < f(x)$. With the rule *best*, $f(y^*) = \min_{y \in N(x)} f(y)$.

*Proof.* The code keeps $f^*$, the value that a neighbor must beat; line L3 sets it to $f(x)$ and $y^*$ to none. We claim this invariant of the loop of line L4: after the loop has looked at the neighbors $y_1, \ldots, y_t$ in order, either $y^* = $ none and $f(y_s) \ge f(x)$ for $s \le t$, or $y^* = y_r$ for some $r \le t$ with $f(y_r) = f^* < f(x)$ and $f(y_s) \ge f^*$ for $s \le t$.

Before the first neighbor, $t = 0$ and $y^* = $ none, so the claim holds. Take the neighbor $y_{t+1}$. If $f(y_{t+1}) \ge f^*$, line L5 does nothing, and the claim holds for $t + 1$ because in both cases $f^* \le f(x)$ and the new neighbor is not below $f^*$. If $f(y_{t+1}) < f^*$, line L6 sets $y^* = y_{t+1}$ and $f^* = f(y_{t+1})$. The new value is below the old $f^*$, which is at most $f(x)$, so $f^* < f(x)$, and each earlier neighbor has $f(y_s) \ge$ old $f^* > $ new $f^*$. So the claim holds for $t + 1$.

The loop ends in one of two ways. With the rule *first*, line L7 can stop it right after line L6, and then $y^* \ne$ none. Otherwise it ends after all of $N(x)$. So if $y^* = $ none at line L8, the loop looked at all of $N(x)$ and the invariant gives (a). If $y^* \ne$ none, the invariant gives $y^* \in N(x)$ and $f(y^*) < f(x)$. With the rule *best* line L7 never stops the loop, so the invariant holds for all of $N(x)$, and $f(y^*) = f^* \le f(y)$ for each neighbor $y$. This is (b). $\square$

**Theorem.** Hill climbing stops. When it stops, it returns a solution $x \in S$ that is a local minimum of $N$, and $f(x) \le f(x_0)$. The values $f(x)$ at the starts of the passes of line L2 form a strictly decreasing sequence. If $f$ is integer-valued, the number of moves is at most $f(x_0) - \min_{x \in S} f(x)$.

*Proof.* Write $x_0, x_1, x_2, \ldots$ for the values of $x$ at the start of the passes of line L2.

*In $S$.* Line L1 sets $x = x_0 \in S$, and line L9 sets $x_{i+1} = y^* \in N(x_i) \subseteq S$ by Lemma 1(b). So by induction each $x_i$ is in $S$ and is reached from $x_0$ by moves to neighbors.

*Strict decrease.* By Lemma 1(b), each move gives $f(x_{i+1}) = f(y^*) < f(x_i)$. So $f(x_0) > f(x_1) > f(x_2) > \cdots$.

*Termination.* A strictly decreasing sequence takes each value at most once. The values all lie in the finite set $V$ of values of $f$ on the solutions that can be reached from $x_0$. So there are at most $|V|$ terms, and at most $|V| - 1$ moves. Each pass of line L2 either moves or returns, so the algorithm returns after at most $|V|$ passes. If $f$ is integer-valued, each move lowers $f$ by at least 1, and $f$ never goes below $\min_S f$, so there are at most $f(x_0) - \min_S f$ moves.

*Local minimum.* The algorithm returns only at line L8, where $y^* = $ none. By Lemma 1(a), $f(y) \ge f(x)$ for each $y \in N(x)$, so $x$ is a local minimum. Since the sequence of values decreases, $f(x) \le f(x_0)$. $\blacksquare$

**What the theorem does not say.** The returned solution is a local minimum of $N$. It need not be a global minimum, and the theorem gives no bound on $f(x) - \min_S f$. For some problems a separate argument bounds the quality of every local minimum: for Max-Cut with the flip neighborhood and non-negative weights, each local minimum of the uncut weight has a cut of at least half the total weight (Kleinberg and Tardos, Section 12.4).
