---
title: The safeguarded Newton method keeps its bracket, ends within (N + 1)^2 passes, converges for every C^1 function, and is quadratic once it takes a good Newton step
proves: [correctness, termination, invariant, global-convergence, local-convergence]
status: full
---

We write $[a_k, b_k]$ for the bracket after line L6 of pass $k$, $w_k = b_k - a_k$, $x_k$ for the point evaluated in pass $k$, and $s_k = x_{k+1} - x_k$ for the step chosen in pass $k$ (line L11). A pass is a *Newton pass* if line L9 keeps the Newton point and a *bisection pass* otherwise. Let $w_0 = b - a$ for the input bracket.

**Claim 1 (termination and the invariant).** The method returns after at most $k_{\max}$ passes. If line L2 passes, then in every pass $x_k \in (a_{k-1}, b_{k-1})$, and $f(a_k)$, $f(b_k)$ are finite, nonzero and of opposite signs; $x_k$ is one of $a_k$, $b_k$, and $[a_k, b_k] \subseteq [a_{k-1}, b_{k-1}]$.

*Proof.* The loop runs at most $k_{\max}$ times. For $k = 1$, $x_1$ is the midpoint. For $k \ge 2$, line L9 chooses $x_k$ strictly inside the bracket or as its midpoint. (In floating point the computed midpoint can equal an end when the ends are adjacent; then it equals $x_{k-1}$, the step is $0$, and line L10 returns.) Line L5 returns unless $f(x_k)$ is finite and nonzero, and line L6 replaces the end whose value has the sign of $f(x_k)$ by $x_k$, which keeps opposite signs at the ends and makes $x_k$ an end. $\square$

**Claim 2 (the number of passes).** In exact arithmetic with $\delta > 0$, let $N = \lceil \log_2 (w_0/\delta) \rceil$. The method returns after at most $(N + 1)^2$ passes.

*Proof.* (i) *Bisection passes.* In a bisection pass $k$, $x_{k+1}$ is the midpoint of $[a_k, b_k]$, and in pass $k + 1$ line L6 makes it an end, so $w_{k+1} = w_k/2$. Widths never increase. So after $j$ bisection passes, the width is at most $w_0 2^{-j}$, and once it is at most $2\delta$, line L7 returns at the next pass. Hence there are at most $N$ bisection passes before the pass in which line L7 returns.

(ii) *Runs of Newton passes.* Every step satisfies $|s_k| < w_{k} \le w_0$, since both $x_k$ and $x_{k+1}$ lie in $[a_k, b_k]$; also $|s_0| := w_0$ for the initial value of $s_{\text{prev}}$. A Newton pass $k$ has $|s_k| \le |s_{k-1}|/2$. So in a run of $r$ consecutive Newton passes that starts after the step $s_j$, the last step has $|s| \le |s_j| 2^{-r} \le w_0 2^{-r}$, and line L10 returns as soon as $|s| \le \delta$. So every run of Newton passes has at most $N$ passes.

(iii) The passes form at most $N + 1$ runs of Newton passes separated by at most $N$ bisection passes, followed by the final pass. That is at most $N(N + 1) + N + 1 = (N + 1)^2$ passes. $\square$

**Claim 3 (global convergence).** Let $f \in C^1$ on $[a, b]$ with $f(a) f(b) < 0$, and run in exact arithmetic with $\delta = 0$ and $k_{\max} = \infty$. If the method does not return an exact root, then $x_k$ converges to a root of $f$ in $[a, b]$.

*Proof.* The ends $a_k$ and $b_k$ are monotone and bounded, with limits $\alpha \le \beta$, and $f(\alpha)$ and $f(\beta)$ have weakly opposite signs by continuity. *Case 1: infinitely many bisection passes.* Then $w_k \to 0$ by Claim 2(i), so $\alpha = \beta$, and $f(\alpha) = 0$. Since $x_k \in [a_k, b_k]$, $x_k \to \alpha$. *Case 2: finitely many.* Then from some pass on all passes are Newton passes, and $|s_k| \le |s_{k-1}|/2$, so $\sum |s_k| < \infty$ and $x_k$ converges to some $L \in [a, b]$. Since $|f(x_k)| = |f'(x_k)|\,|s_k| \le \max_{[a, b]} |f'| \cdot |s_k| \to 0$, continuity gives $f(L) = 0$. $\square$

**Claim 4 (local quadratic convergence).** Let $f \in C^2$ on $[a, b]$ with $f' > 0$ and $f'' > 0$ there, let $x^*$ be the root, and $M = \max |f''|/(2 \min |f'|)$ over $[a, b]$. Suppose pass $k$ is a Newton pass from $x_k > x^*$ with $M(x_k - x^*) \le 1/6$. Then every later pass is a Newton pass, $x^* < x_{j+1} < x_j$ (or an exact root is found), and $e_{j+1} \le M e_j^2$ for all $j \ge k$.

*Proof.* We show by induction on $j \ge k$: pass $j$ is a Newton pass from $x_j > x^*$ with $M e_j \le 1/6$. It holds for $j = k$. By the error identity of Newton's method, $e_{j+1} = f''(\xi) e_j^2/(2 f'(x_j))$ with $\xi \in (x^*, x_j)$, so $0 \le e_{j+1} \le M e_j^2 \le e_j/6$. If $e_{j+1} = 0$ the next pass returns at line L5. Otherwise $x^* < x_{j+1} < x_j$, and $M e_{j+1} \le 1/6$. Now consider pass $j + 1$. Since $f(x_{j+1}) > 0$, line L6 sets $b = x_{j+1}$, and the bracket is $[a_{j+1}, x_{j+1}]$ with $a_{j+1} < x^*$. The Newton point $x_{j+2}$ lies in $(x^*, x_{j+1})$ by the same identity, so it is strictly inside the bracket. For the halving test, $|s_j| = e_j - e_{j+1} \ge \tfrac56 e_j$ and $|s_{j+1}| = e_{j+1} - e_{j+2} \le e_{j+1} \le \tfrac16 e_j$, so $|s_{j+1}| \le \tfrac15 |s_j| \le \tfrac12 |s_j|$. So pass $j + 1$ is a Newton pass from $x_{j+1} > x^*$ with $M e_{j+1} \le 1/6$. $\square$

The other sign cases follow by applying Claim 4 to $-f(x)$, $f(-x)$ or $-f(-x)$. Claim 4 does not say that such a pass occurs: after a bisection pass the next Newton step can fail the halving test against the long bisection step. In that case the width still halves, and Claim 2 bounds the number of passes.

**Floating point.** Claim 1 holds as stated. Claims 2 to 4 hold in exact arithmetic; in floating point the iterates follow them until $|f|$ reaches its rounding level, and the zero-step argument in Claim 1 ends the loop even with $\delta = 0$. $\blacksquare$
