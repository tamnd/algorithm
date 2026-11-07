---
title: The integer Newton iteration stops exactly at the floor of the k-th root
proves: [correctness, termination]
status: full
---

Let $N \ge 0$ and $k \ge 1$ be integers and $s = \lfloor N^{1/k} \rfloor$, the unique integer $s \ge 0$ with $s^k \le N < (s + 1)^k$.

**Theorem.** NEWTON-ROOT$(N, k)$ terminates and returns $s$.

*Proof.* If $k = 1$, then $s = N$, and if $N \in \{0, 1\}$, then $s = N$; line L1 returns $N$ in these cases. From now on $k \ge 2$ and $N \ge 2$, so $s \ge 1$.

*The start.* Let $B \ge 2$ be the binary length of $N$, so $2^{B-1} \le N < 2^B$. Then $x_0 = 2^{\lceil B/k \rceil} \ge 2^{B/k} > N^{1/k} \ge s$. In particular $x_0 \ge 1$.

*Lemma 1 (one step).* For an integer $x \ge 1$, let $y = \lfloor ((k - 1)x + \lfloor N / x^{k-1} \rfloor) / k \rfloor$, the value of line L4. Then

(a) $y = \lfloor g(x) \rfloor$, where $g(x) = \big((k - 1)x + N / x^{k-1}\big)/k$;

(b) $y \ge s$;

(c) if $x > s$, then $y < x$;

(d) if $x = s$, then $y \ge x$.

*Proof of (a).* Let $a = (k - 1)x$, an integer, and $t = N / x^{k-1} \ge 0$. For an integer $a$ and a real $t$, $\lfloor (a + \lfloor t \rfloor)/k \rfloor = \lfloor (a + t)/k \rfloor$: write $a + \lfloor t \rfloor = qk + \rho$ with $0 \le \rho \le k - 1$; then $(a + t)/k = q + (\rho + \{t\})/k$ with $0 \le \rho + \{t\} < k$, so both sides equal $q$.

*Proof of (b).* By the inequality of the arithmetic and geometric means for the $k$ nonnegative numbers $x, \ldots, x$ ($k - 1$ times) and $N / x^{k-1}$,

$$g(x) \ge \big( x^{k-1} \cdot N / x^{k-1} \big)^{1/k} = N^{1/k} .$$

So $y = \lfloor g(x) \rfloor \ge \lfloor N^{1/k} \rfloor = s$, since the floor is monotone.

*Proof of (c).* If $x > s$, then $x \ge s + 1$, so $x^k \ge (s + 1)^k > N$, hence $N / x^{k-1} < x$ and $g(x) < ((k - 1)x + x)/k = x$. Since $x$ is an integer, $y = \lfloor g(x) \rfloor \le g(x) < x$.

*Proof of (d).* If $x = s \ge 1$, then $x^k \le N$, so $N / x^{k-1} \ge x$ and $g(x) \ge x$. Since $x$ is an integer, $y = \lfloor g(x) \rfloor \ge x$. $\square$

*Invariant.* At each execution of line L4, $x$ is an integer with $x \ge s \ge 1$. It holds for $x_0$. If the loop continues at line L6, then $x \leftarrow y$ with $y \ge s$ by (b), and $y$ is an integer.

*Termination.* The loop continues only when $y < x$, so the values of $x$ at line L4 form a strictly decreasing sequence of integers bounded below by $s$. Hence there are at most $x_0 - s + 1$ executions of line L4, and the loop stops at line L5.

*Result.* Let $x$ be the value returned at line L5, so $y \ge x$ for its step. By the invariant $x \ge s$. If $x > s$, then (c) gives $y < x$, a contradiction. So $x = s$. Conversely, (d) shows that the loop does stop once $x = s$ is reached, which agrees with the termination argument. $\blacksquare$

*Remark (the stopping test).* The test must be $y \ge x$, not $y = x$. For $k = 2$ and $N = s^2 + 2s$, the step from $x = s$ gives $y = \lfloor (s + \lfloor (s^2 + 2s)/s \rfloor)/2 \rfloor = \lfloor (2s + 2)/2 \rfloor = s + 1 > x$, so a test for equality would continue to $s + 1$, which maps back to $\lfloor (s + 1 + \lfloor (s^2 + 2s)/(s + 1) \rfloor)/2 \rfloor = \lfloor (s + 1 + s)/2 \rfloor = s$, a cycle of length two.
