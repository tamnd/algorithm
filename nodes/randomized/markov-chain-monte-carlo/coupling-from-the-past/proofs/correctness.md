---
title: Coupling from the past returns an exact sample from π
proves: [correctness]
status: full
---

**Setting.** $P$ is an irreducible transition matrix on a finite set $\mathcal X$ with stationary distribution $\pi$. The update rule $\phi$ satisfies $\Pr[\phi(x, U) = y] = P(x, y)$ for a random draw $U$. The draws $u_1, u_2, \ldots$ are independent copies of $U$, and $u_t$ drives the step from time $-t$ to time $-t + 1$. Write $f_t = \phi(\cdot, u_t)$ and
$$
F_{-t} = f_1 \circ f_2 \circ \cdots \circ f_t,
$$
the map from the state at time $-t$ to the state at time 0. Let $T_* = \min\{t \ge 1 : F_{-t} \text{ is constant}\}$, with $T_* = \infty$ if there is no such $t$.

**Lemma 1 (stability).** If $F_{-t}$ is constant with value $Y$, then $F_{-s}$ is constant with value $Y$ for every $s \ge t$.

*Proof.* $F_{-s} = F_{-t} \circ g$ with $g = f_{t+1} \circ \cdots \circ f_s$. For every $x$, $F_{-s}(x) = F_{-t}(g(x)) = Y$. $\square$

On $\{T_* < \infty\}$ let $Y = F_{-T_*}(x)$ for any $x$. By Lemma 1, $Y = F_{-s}(x)$ for all $s \ge T_*$ and all $x$.

**Lemma 2 (sandwiching).** Assume $\phi(\cdot, u)$ is monotone and $\hat0 \le x \le \hat1$ for all $x$. In the round with start time $T$, after lines L5 to L7 have processed the draws $u_T, u_{T-1}, \ldots, u_s$, the values satisfy $lo \le G(x) \le hi$ for every $x$, where $G = f_s \circ \cdots \circ f_T$. In particular, at the end of the round, $lo = F_{-T}(\hat0)$, $hi = F_{-T}(\hat1)$, and $lo = hi$ holds if and only if $F_{-T}$ is constant.

*Proof.* Before the first step, $G$ is the identity and line L5 sets $lo = \hat0 \le x \le \hat1 = hi$. Line L7 applies the monotone map $f_s$ to all three sides, which keeps the order. At the end, $lo = F_{-T}(\hat0) \le F_{-T}(x) \le F_{-T}(\hat1) = hi$. If $lo = hi$ every $F_{-T}(x)$ equals it. Conversely, if $F_{-T}$ is constant then $F_{-T}(\hat0) = F_{-T}(\hat1)$. $\square$

**Lemma 3 (what the algorithm returns).** Line L4 keeps the old draws, so the round with start time $T$ uses exactly $u_1, \ldots, u_T$, and line L6 applies them from $u_T$ to $u_1$, which computes $F_{-T}$. By Lemma 2 the round returns exactly when $F_{-T}$ is constant, that is, when $T \ge T_*$ (by Lemma 1 and the definition of $T_*$). So the algorithm returns at the first $T \in \{1, 2, 4, \ldots\}$ with $T \ge T_*$, and its output is $F_{-T}(\hat0) = Y$. If $T_* = \infty$ it never returns.

**Theorem 1 (exactness).** If $\Pr[T_* < \infty] = 1$, then $\Pr[Y = y] = \pi(y)$ for every $y \in \mathcal X$.

*Proof.* Let $X$ have law $\pi$ and be independent of all draws. Fix $t$. The map $F_{-t}$ is a composition of $t$ independent random maps, each with $\Pr[f(x) = y] = P(x, y)$, so $\Pr[F_{-t}(x) = y] = P^t(x, y)$. Hence
$$
\Pr[F_{-t}(X) = y] = \sum_x\pi(x)P^t(x, y) = (\pi P^t)(y) = \pi(y).
$$
On the event $\{T_* \le t\}$, $F_{-t}(X) = Y$ by Lemma 1. So the events $\{Y = y\}$ and $\{F_{-t}(X) = y\}$ differ only inside $\{T_* > t\}$, and
$$
|\Pr[Y = y] - \pi(y)| \le \Pr[T_* > t].
$$
The left side does not depend on $t$, and the right side tends to $\Pr[T_* = \infty] = 0$. So $\Pr[Y = y] = \pi(y)$. $\square$

The proof uses neither reversibility nor aperiodicity.

**Theorem 2 (termination).**

1. If there is an $L$ with $p = \Pr[f_1 \circ \cdots \circ f_L \text{ is constant}] > 0$, then $\Pr[T_* > kL] \le (1 - p)^k$, so $\Pr[T_* < \infty] = 1$ and $\mathbb E[T_*] \le L/p$.
2. In the monotone case, let $\ell$ be the length of the longest chain $x_0 < x_1 < \cdots < x_\ell$ in the order. Then $\Pr[T_* > t] \le \ell\,\|P^t(\hat1, \cdot) - P^t(\hat0, \cdot)\|_{TV}$. If $P$ is also aperiodic, the right side tends to 0, so $\Pr[T_* < \infty] = 1$.

*Proof of part 1.* Split $F_{-kL}$ into $k$ blocks $B_j = f_{(j-1)L+1} \circ \cdots \circ f_{jL}$, so $F_{-kL} = B_1 \circ \cdots \circ B_k$. The blocks are independent, and each is constant with probability $p$. If some $B_j$ is constant with value $c$, then for every $x$, $F_{-kL}(x) = B_1 \circ \cdots \circ B_{j-1}(c)$, so $F_{-kL}$ is constant. So $\Pr[T_* > kL] \le \Pr[\text{no block is constant}] = (1 - p)^k$. Then $\mathbb E[T_*] = \sum_{t \ge 0}\Pr[T_* > t] \le L\sum_{k \ge 0}(1 - p)^k = L/p$. $\square$

*Proof of part 2.* Let $h(x)$ be the length of the longest chain in the order that ends at $x$. If $x < y$, then $h(y) \ge h(x) + 1$, and $0 \le h \le \ell$. Let $A = F_{-t}(\hat0)$ and $B = F_{-t}(\hat1)$. By Lemma 2, $A \le B$, and $F_{-t}$ is constant if and only if $A = B$. On $\{A \ne B\}$, $A < B$ and so $h(B) - h(A) \ge 1$; on $\{A = B\}$ the difference is 0. Therefore
$$
\Pr[T_* > t] = \Pr[A \ne B] \le \mathbb E[h(B)] - \mathbb E[h(A)].
$$
Here $A \sim P^t(\hat0, \cdot)$ and $B \sim P^t(\hat1, \cdot)$. For two laws $\mu$, $\nu$ and a function $h$ with values in $[0, \ell]$, $\sum_xh(x)(\mu(x) - \nu(x)) \le \ell\sum_x(\mu(x) - \nu(x))^+ = \ell\,\|\mu - \nu\|_{TV}$. This gives the bound. For an irreducible aperiodic chain on a finite set, $P^t(x, \cdot) \to \pi$ for each $x$, so the total variation distance tends to 0. $\square$

**Corollary (cost of doubling).** The algorithm stops at the first power of two $T \ge T_*$, so $T < 2T_*$, and it performs $1 + 2 + \cdots + T = 2T - 1 < 4T_*$ updates of each copy.

**Proposition (reusing the draws is necessary, and reading forward is biased).** Consider the walk on $\{0, 1, 2\}$ in which a uniform $u \in \{0, 1, 2, 3\}$ moves down for $u \in \{0, 1\}$, moves up for $u = 3$, and stays for $u = 2$, with moves blocked at the ends. Its stationary law is $\pi = (4/7, 2/7, 1/7)$.

1. *Forward reading.* Run copies from 0 and 2 forward with the same draws and output the state at their first meeting. Before the meeting the lower copy is strictly below the upper one, since the update is monotone. If they meet at state 1, then in that step the lower copy went from 0 to 1 and the upper from 2 to 1, so the same draw moved one copy up and the other down. No draw does both. So the meeting state is 0 or 2, and the output is never 1, while $\pi(1) = 2/7 > 0$.
2. *Why backward is different.* In CFTP the output is the state at the fixed time 0, and the start time is chosen by looking only at whether $F_{-T}$ is constant. By Lemma 1, $Y$ does not depend on which $T \ge T_*$ is used, so the stopping rule does not affect the value. In forward reading, the output is the state at a random time that depends on the path, so the stopping rule selects states.
3. *Fresh draws.* If each round drew new values, the output would be the value of $F_{-T}$ in the first round in which a freshly drawn $F_{-T}$ is constant. That is a draw conditioned on coalescence within $T$ steps for a random $T$, and Lemma 1 no longer links the rounds. Theorem 1 then does not apply. $\square$
