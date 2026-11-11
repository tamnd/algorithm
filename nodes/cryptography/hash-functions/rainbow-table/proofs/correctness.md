---
title: A rainbow table lookup is always right and finds every covered target
proves: [correctness]
status: full
---

Fix $f : X \to Y$, $t \ge 1$ and reductions $R_0, \ldots, R_{t-1} : Y \to X$. For a start $x_0$, define $x_{j+1} = R_j(f(x_j))$ for $0 \le j < t$. Let $E$ be the map from end points to start points kept by the table.

**Lemma 1 (invariant).** After any sequence of ADD-CHAIN calls, for each key $e$ of $E$, the chain from $E[e]$ has $x_t = e$.

*Proof.* By induction on the number of calls. The empty table satisfies it. A call computes $x = x_t$ from $x_0$ by the loop of line L2, with $x$ equal to $x_j$ after $j$ rounds. If $x$ is already a key, line L3 returns and $E$ does not change. Otherwise line L4 adds the key $x_t$ with value $x_0$, which satisfies the claim, and leaves the other keys unchanged. $\square$

**Lemma 2 (the guess of column $j$).** In LOOKUP($y$), for the value $j$ of the loop of line L5, after line L7, $z = g_j(y)$ where $g_j(y) = R_{t-1}(f(\cdots R_{j+1}(f(R_j(y)))\cdots))$. If $y = f(x_j)$ for a chain with start $x_0$, then $g_j(y) = x_t$ of that chain.

*Proof.* Line L6 sets $z = R_j(y)$ and line L7 applies $R_c \circ f$ for $c = j + 1, \ldots, t - 1$, which is the definition of $g_j$. If $y = f(x_j)$, then $R_j(y) = x_{j+1}$, and each step of line L7 with index $c$ maps $x_c$ to $x_{c+1}$, so $z = x_t$ at the end. $\square$

**Lemma 3 (soundness).** If LOOKUP($y$) returns $x$, then $f(x) = y$.

*Proof.* The only return of a value is at line L10, after the test $f(x) = y$. $\square$

**Lemma 4 (completeness).** Suppose $E$ holds a pair $(x_t, x_0)$ whose chain has $f(x_j) = y$ for some $0 \le j \le t - 1$. Then LOOKUP($y$) returns a value.

*Proof.* If an earlier iteration returns, we are done. Otherwise the loop reaches this $j$. By Lemma 2, $z = x_t$ after line L7, and $x_t$ is a key of $E$. Two chains in the table may not share an end point, so $E[x_t] = x_0$. Line L9 applies $R_c \circ f$ for $c = 0, \ldots, j - 1$ to $x_0$, which gives $x_j$. Since $f(x_j) = y$, line L10 returns $x_j$. A false alarm at another iteration does not end the loop. $\square$

**Lemma 5 (cost).** LOOKUP makes at most $t(t-1)/2 + a(t + 1)$ calls of $f$ and at most $t$ lookups in $E$, where $a$ is the number of end point matches at line L8.

*Proof.* The iteration for $j$ makes $t - 1 - j$ calls at line L7 and one lookup at line L8. Summing over $j = 0, \ldots, t - 1$ gives $t(t-1)/2$ calls and $t$ lookups. Each match costs $j \le t - 1$ calls at line L9 and one at line L10. $\square$

**Theorem.** A rainbow table keeps its invariant under ADD-CHAIN. LOOKUP never returns a wrong preimage, returns a preimage for every target that is the image of a point in columns $0$ to $t - 1$ of a stored chain, and makes $O(t^2 + a t)$ calls of $f$ and $O(t)$ table lookups.

*Proof.* Lemmas 1, 3, 4 and 5. $\blacksquare$
