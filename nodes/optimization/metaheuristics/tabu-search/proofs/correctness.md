---
title: Tabu search keeps the best solution it visits, and it begins with the hill-climbing descent
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The set of solutions $S$ is finite, $f : S \to \mathbb{R}$ is the objective to minimize, and each solution $x$ has a finite list of moves $(a, y)$ with $y \in N(x)$ and an attribute $a$. The neighbors are scanned in a fixed order. The tenure is $t \ge 0$ and the number of iterations is $K \ge 0$. Write $x_0$ for the start and $x_k$ for the current solution after $k$ moves.

**Lemma 1 (termination).** The algorithm stops after at most $K$ moves.

*Proof.* The loop of line L2 makes at most $K$ passes, each pass scans a finite list of moves, and line L7 can only end the loop earlier. $\square$

**Lemma 2 (the best solution).** After $k$ moves, $b$ is one of $x_0, \ldots, x_k$ and $f(b) = \min_{0 \le i \le k} f(x_i)$. So $f(b)$ never increases, and the returned $b$ is a best solution among those visited.

*Proof.* By induction on $k$. For $k = 0$, line L1 sets $b = x_0$. In the move to $x_{k+1}$, line L10 replaces $b$ by $x_{k+1}$ exactly when $f(x_{k+1}) < f(b)$. So the new value of $f(b)$ is $\min(f(b), f(x_{k+1}))$, which is the least value among $x_0, \ldots, x_{k+1}$, and it is not larger than the old value. $\square$

**Lemma 3 (the tabu list).** After $k$ moves with attributes $a_1, \ldots, a_k$, the list $T$ is $a_{j}, a_{j+1}, \ldots, a_k$ with $j = \max(1, k - t + 1)$, so $|T| = \min(k, t)$.

*Proof.* By induction on $k$. For $k = 0$ the list is empty. Line L9 appends $a_{k+1}$ at the end. If the new length is at most $t$, nothing is removed, and the list is the last $k + 1 \le t$ attributes. Otherwise the length is $t + 1$ and line L9 removes the oldest one, which leaves the last $t$ attributes. $\square$

**Lemma 4 (each move obeys the rule).** The move made at line L8 is admissible: its attribute is not in $T$, or it leads to $y$ with $f(y) < f(b)$, where $b$ is the best solution before the move. Among the admissible moves it has the least value of $f(y)$, and it is the first one in the scan order with that value.

*Proof.* Line L5 skips exactly the moves that are tabu and not aspirated, so every move that reaches line L6 is admissible. Line L6 replaces $m$ only by a move of strictly smaller value, so after the scan $m$ is the first admissible move of least value. $\square$

**Theorem 1 (the descent phase).** Let $y_0 = x_0, y_1, \ldots, y_H$ be the path of best-improvement hill climbing from $x_0$ with the same neighbor order, where $y_H$ is a local minimum of $N$. Then $x_k = y_k$ for $k \le \min(H, K)$. So if $K \ge H$, tabu search returns $b$ with $f(b) \le f(y_H)$.

*Proof.* We show by induction that for $k \le \min(H, K)$, $x_k = y_k$ and $b = x_k$ after $k$ moves. For $k = 0$ this is line L1. Suppose it holds for some $k < \min(H, K)$. Since $y_k$ is not a local minimum, it has a neighbor $y$ with $f(y) < f(y_k) = f(b)$. Every such neighbor is admissible, tabu or not, by the aspiration rule of line L5. Let $v$ be the least value of $f$ over all neighbors of $y_k$; then $v < f(b)$, so every neighbor with value $v$ is admissible. By Lemma 4 the search moves to the first neighbor in the scan order with value $v$. Best-improvement hill climbing moves to the same neighbor, because it also takes the first neighbor of least value. So $x_{k+1} = y_{k+1}$. Since $f(x_{k+1}) = v < f(b)$, line L10 sets $b = x_{k+1}$. This ends the induction. For $K \ge H$, Lemma 2 gives $f(b) \le f(x_H) = f(y_H)$. $\square$

**Theorem 2 (correctness).** Tabu search stops, and it returns a solution $b$ that is visited by the search, with $f(b)$ the least value among the visited solutions and $f(b) \le f(x_0)$. If every move of the neighborhood keeps a solution feasible, every visited solution is feasible.

*Proof.* Termination is Lemma 1 and the claim about $b$ is Lemma 2. Each $x_k$ is the end of a move from $x_{k-1}$, so feasibility passes from $x_0$ to all $x_k$ by induction. $\blacksquare$

**What is not claimed.** None of these results says that $b$ is a global minimum, or even a local minimum. After the descent phase, the search moves to the best admissible neighbor even when that neighbor is worse, and it can cycle: with $t = 0$ the list is always empty, and from a local minimum the search can step out and step straight back. A longer list blocks short cycles but not all cycles. The guarantee of Theorem 1 is only that the search is never worse than the first descent of hill climbing.
