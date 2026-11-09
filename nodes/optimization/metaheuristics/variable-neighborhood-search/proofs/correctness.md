---
title: Variable neighborhood descent ends at a local minimum of every neighborhood, and VNS never gets worse
proves: [correctness, termination]
status: full
---

The set of solutions $S$ is finite, $f : S \to \mathbb{R}$ is to be minimized, and $N_1, \ldots, N_m$ are neighborhoods used by the local search. We use the pseudocode of the page for VNS, and the procedure VND described there: start with $j = 1$; if some $y \in N_j(x)$ has $f(y) < f(x)$, move to the best such $y$ and set $j = 1$; otherwise set $j \leftarrow j + 1$; stop when $j > m$.

**Lemma 1 (VND stops).** VND stops on every start.

*Proof.* Each move strictly lowers $f$, so no solution is visited twice, and there are at most $|S| - 1$ moves. Between two moves, $j$ only grows, so there are at most $m$ tests of a neighborhood. So VND makes at most $m |S|$ tests and stops. $\square$

**Lemma 2 (VND ends at a local minimum of all neighborhoods).** The result $x$ of VND satisfies $f(y) \ge f(x)$ for every $j \le m$ and every $y \in N_j(x)$.

*Proof.* Consider the last move, or the start if there was none. After it, $j = 1$ and $x$ does not change again. VND stops only when $j > m$, and $j$ grows by one only when $N_j(x)$ has no strictly better neighbor of this same $x$. So each of $N_1(x), \ldots, N_m(x)$ was tested on $x$ and has no neighbor better than $x$. $\square$

**Theorem 1 (VNS).** Let the local search of VNS be VND, or any procedure that stops and returns a local minimum of each $N_j$. Let $k_{\max} \ge 1$ and $K \ge 0$. Then:

1. VNS stops after $K + 1$ runs of the local search and $K$ shakes.
2. After each iteration, the current solution $x$ is a local minimum of each $N_j$, and $f(x)$ is not larger than before the iteration.
3. The index $k$ is always in $\{1, \ldots, k_{\max}\}$. It is 1 after an iteration that moves, and the next value in the cycle $1, 2, \ldots, k_{\max}, 1, \ldots$ after an iteration that does not.
4. The returned $x$ is the best of all local minima that the local search returned during the run.

*Proof.* (1) Line L3 makes exactly $K$ passes, and the local search stops by assumption. (2) Line L1 sets $x$ to an output of the local search. Line L6 replaces $x$ only by an output $z$ of the local search with $f(z) < f(x)$. (3) Line L2 sets $k = 1$. Line L6 sets $k = 1$ after a move, and line L7 increases $k$ by one or sets it to 1 after $k_{\max}$. (4) By (2), the value of $x$ is non-increasing, and $x$ changes to $z$ whenever $f(z) < f(x)$. So after each iteration $f(x)$ is the least value among the outputs of the local search so far, which include the output of line L1. $\blacksquare$

**Two facts behind the method.** First, a local minimum of one neighborhood need not be a local minimum of another: in the example of the page, the cut 11100010 with uncut weight 11 has no better neighbor at Hamming distance 1, but its neighbor 11000011 at distance 2 has uncut weight 6. Second, a global minimum is a local minimum of every neighborhood, since no solution is better. Lemma 2 uses the first fact: VND removes the local minima of $N_1$ that are not local minima of $N_2$.

**What is not claimed.** VNS returns a local minimum of all the neighborhoods that its local search uses, not a global minimum. The shaking step is random, and no general bound is known on the number of iterations needed to reach a global minimum.
