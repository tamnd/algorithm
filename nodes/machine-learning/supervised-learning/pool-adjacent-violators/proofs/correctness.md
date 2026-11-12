---
title: PAV returns the unique weighted isotonic least squares fit
proves: [correctness, termination]
status: full
---

Let $y \in \mathbb{R}^n$ and $\omega_1, \dots, \omega_n > 0$. Write $f(u) = \tfrac{1}{2}\sum_{i=1}^{n} \omega_i (u_i - y_i)^2$ and $K = \{u \in \mathbb{R}^n : u_1 \le \dots \le u_n\}$. For a block $B$ of consecutive indices, $W(B) = \sum_{i \in B}\omega_i$ and $\operatorname{Av}(B) = \sum_{i \in B}\omega_i y_i / W(B)$.

**Lemma 1 (a sufficient condition).** Let $z \in K$. Define $R_0 = 0$ and $R_k = \sum_{i=1}^{k} \omega_i (y_i - z_i)$ for $1 \le k \le n$. Assume that (a) $R_n = 0$, (b) $R_k \ge 0$ for $1 \le k \le n-1$, and (c) $R_k = 0$ for each $k$ with $z_k < z_{k+1}$. Then for each $u \in K$, $f(u) - f(z) \ge \tfrac{1}{2}\sum_i \omega_i (u_i - z_i)^2$. So $z$ is the unique minimizer of $f$ on $K$.

*Proof.* Let $\delta = u - z$. Expand the square:

$$f(u) - f(z) = \sum_{i=1}^{n} \omega_i (z_i - y_i)\delta_i + \tfrac{1}{2}\sum_{i=1}^{n}\omega_i \delta_i^2 .$$

Here $\omega_i (z_i - y_i) = -(R_i - R_{i-1})$. Summation by parts with $R_0 = R_n = 0$ gives

$$\sum_{i=1}^{n} (R_i - R_{i-1})\delta_i = \sum_{k=1}^{n-1} R_k (\delta_k - \delta_{k+1}),$$

so the first sum is $\sum_{k=1}^{n-1} R_k(\delta_{k+1} - \delta_k) = \sum_{k=1}^{n-1} R_k (u_{k+1} - u_k) - \sum_{k=1}^{n-1} R_k (z_{k+1} - z_k)$. Each term of the first sum is a product of two numbers $\ge 0$, by (b) and $u \in K$. Each term of the second sum is 0: if $z_{k+1} = z_k$ the factor is 0, and else $R_k = 0$ by (c). So the first sum is $\ge 0$, and $f(u) - f(z) \ge \tfrac{1}{2}\sum_i \omega_i \delta_i^2$. This is $> 0$ when $u \ne z$, because each $\omega_i > 0$. $\square$

**The invariant.** Call a block $B = \{a, \dots, b\}$ with value $v$ *good* if $v = \operatorname{Av}(B)$ and $\sum_{i=a}^{k}\omega_i(y_i - v) \ge 0$ for each $k$ with $a \le k \le b$. (For $k = b$ the sum is 0, because $v$ is the mean.) The invariant of the outer loop of line L2, at the start of iteration $i$, is:

> **(P)** The blocks of $S$, from the bottom to the top, partition $\{1, \dots, i-1\}$ into consecutive blocks in order. Each block is good, and its weight and length fields are $W(B)$ and $|B|$. The values do not decrease from the bottom to the top.

Inside the loop of line L4 we use the weaker invariant **(Q)**: (P) holds for $\{1, \dots, i\}$, except that the top value may be less than the value below it.

*Initialization.* At $i = 1$ the stack is empty, and (P) holds.

*Line L3.* The block $\{i\}$ with value $y_i$ is good: its value is its mean, and its only partial sum is $\omega_i(y_i - y_i) = 0$. The blocks below are unchanged, so (Q) holds.

*Lines L5 and L6.* The loop pools the second block $B_1$ (value $v_1$) and the top block $B_2$ (value $v_2$), with $v_1 > v_2$. Let $B = B_1 \cup B_2$ and $v = (W_1 v_1 + W_2 v_2)/(W_1 + W_2)$. Since $W_1 v_1 + W_2 v_2 = \sum_{i \in B}\omega_i y_i$, we get $v = \operatorname{Av}(B)$, and $v_2 < v < v_1$. We show that $B$ is good. Take a prefix $P$ of $B$ that ends at index $k$.

- If $P \subseteq B_1$, then $\sum_{P}\omega_i(y_i - v) = \sum_P \omega_i(y_i - v_1) + W(P)(v_1 - v) \ge 0$, since $B_1$ is good and $v_1 > v$.
- Else $P = B_1 \cup P_2$ with $P_2$ a prefix of $B_2$. The complement $Q = B \setminus P$ is a suffix of $B_2$. Since $B_2$ is good, $\sum_{P_2}\omega_i(y_i - v_2) \ge 0$, and the full sum over $B_2$ is 0, so $\sum_Q \omega_i (y_i - v_2) \le 0$. Then $\sum_Q \omega_i(y_i - v) = \sum_Q\omega_i(y_i - v_2) - W(Q)(v - v_2) \le 0$. The full sum over $B$ is 0, so $\sum_P \omega_i (y_i - v) = -\sum_Q \omega_i (y_i - v) \ge 0$.

So $B$ is good, its fields are right, and the blocks below it are unchanged. (Q) holds again.

*End of the loop of line L4.* The loop stops when $|S| \le 1$ or the second value is at most the top value. The values below the top did not decrease before the pools began (by (P) at the start of the iteration), and a pool removes the top two blocks and adds one. So when the loop stops, all values are in order, and (P) holds for $i + 1$.

*Termination.* Each pass of the loop of line L4 lowers $|S|$ by exactly one, and $|S| \ge 1$ after line L3, so the loop stops after fewer than $|S|$ passes. Over the whole run there are $n$ pushes, so there are at most $n - 1$ pools in total. The outer loop runs $n$ times.

**Theorem.** PAV returns the unique minimizer $z$ of $f$ on $K$.

*Proof.* After the last iteration, (P) holds for $\{1, \dots, n\}$. Lines L7 to L9 set $z_i$ to the value of the block of $i$. The values do not decrease, so $z \in K$. Check the conditions of Lemma 1. Let $k$ be in block $B = \{a, \dots, b\}$ with value $v$. The blocks before $B$ are good, so each has total residual sum 0, and $R_k = R_{a-1} + \sum_{i=a}^{k}\omega_i(y_i - v) = 0 + \sum_{i=a}^{k}\omega_i(y_i - v) \ge 0$. This gives (b), and with $k = n$ it gives (a), $R_n = 0$. For (c): if $z_k < z_{k+1}$, then $k$ and $k+1$ lie in different blocks, so $k = b$ is the end of a block, and $R_k = 0$. By Lemma 1, $z$ is the unique minimizer. Minimizing $f$ is the same as minimizing $\sum_i \omega_i (y_i - u_i)^2 = 2f(u)$. $\blacksquare$

**Remark.** The numbers $R_k$ are the [KKT](/kkt-conditions/) multipliers of the constraints $z_k \le z_{k+1}$: Lemma 1 is the sufficiency of the KKT conditions for this convex quadratic program, proved directly.
