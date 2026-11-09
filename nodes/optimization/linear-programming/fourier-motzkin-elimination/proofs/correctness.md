---
title: Fourier-Motzkin elimination returns a solution or a Farkas certificate
proves: [correctness]
status: full
---

We use the pseudocode of the main page. Let $Q = \{x \in \mathbb{R}^n : Ax \le b\}$. For a set $R$ of rows in the variables $x_1, \ldots, x_k$ (all other coefficients zero), let $S(R) \subseteq \mathbb{R}^k$ be its set of solutions. Write $\pi_k(x) = (x_1, \ldots, x_k)$ for the projection to the first $k$ coordinates, with $\pi_0(x)$ the empty vector and $\mathbb{R}^0$ the set that holds only the empty vector.

**Invariant (I), certificates.** Every row $(a, \beta, y)$ of $R$ has $y \ge 0$, $y^\top A = a^\top$ and $y^\top b = \beta$.

**Invariant (II), projection.** At the start of the round for $k$ (line L2), the rows of $R$ have zero coefficients on $x_{k+1}, \ldots, x_n$, and $S(R) = \pi_k(Q)$.

**Lemma 1 (cleaning).** Line L8 does not change $S(R')$, and it keeps (I).

*Proof.* A row $0 \le \beta$ with $\beta \ge 0$ holds for every point, so removing it changes nothing. Scaling a row $(a, \beta, y)$ by a number $\lambda > 0$ gives $(\lambda a, \lambda \beta, \lambda y)$, which has the same solutions and still satisfies (I). If two rows have the same scaled coefficient vector $a$ and right sides $\beta \le \beta'$, every solution of $a^\top x \le \beta$ satisfies $a^\top x \le \beta'$, so removing the second row changes nothing. The kept rows are rows of $R'$, scaled, so they satisfy (I). $\square$

**Lemma 2 (one round).** Let $R$ be a set of rows in $x_1, \ldots, x_k$ that satisfies (I), and let $R'$ be the set built by lines L3 to L7. Then $R'$ satisfies (I), every row of $R'$ has a zero coefficient on $x_k$, and

$$S(R') = \{ x' \in \mathbb{R}^{k-1} : (x', t) \in S(R) \text{ for some } t \in \mathbb{R} \}.$$

*Proof.* Rows of $Z$ (line L5) have $a[k] = 0$ and are copied. For $p \in P$ and $q \in N$, line L7 forms $\lambda p + \mu q$ with $\lambda = -q.a[k] > 0$ and $\mu = p.a[k] > 0$. Its coefficient on $x_k$ is $\lambda\, p.a[k] + \mu\, q.a[k] = -q.a[k]\, p.a[k] + p.a[k]\, q.a[k] = 0$. Its multiplier vector $\lambda y_p + \mu y_q$ is nonnegative, and by linearity it builds the new row from $(A, b)$. So (I) holds for $R'$.

($\supseteq$) Let $(x', t) \in S(R)$. Each row of $R'$ is a row of $R$ or a combination of two rows of $R$ with positive weights. A point that satisfies two inequalities satisfies every combination of them with nonnegative weights, so $(x', t)$ satisfies each row of $R'$. These rows do not involve $x_k$, so $x'$ satisfies them.

($\subseteq$) Let $x' \in S(R')$. For a row $r$ and the point $x'$, write $s_r = \beta_r - \sum_{j < k} a_{rj} x'_j$. A row $p \in P$ holds at $(x', t)$ exactly when $t \le u_p = s_p / p.a[k]$, and a row $q \in N$ holds exactly when $t \ge \ell_q = s_q / q.a[k]$. The combined row of $(p, q)$ holds at $x'$, which says $\lambda s_p + \mu s_q \ge 0$, that is, $-q.a[k]\, s_p + p.a[k]\, s_q \ge 0$. Divide by the positive number $p.a[k] \cdot (-q.a[k])$: this gives $s_p / p.a[k] + s_q / (-q.a[k]) \ge 0$, so $\ell_q = s_q / q.a[k] \le s_p / p.a[k] = u_p$. Hence $\max_{q \in N} \ell_q \le \min_{p \in P} u_p$, with $\max \emptyset = -\infty$ and $\min \emptyset = +\infty$, and some real $t$ lies between them. The point $(x', t)$ satisfies all rows of $P$ and $N$, and the rows of $Z$, which are rows of $R'$ that do not involve $x_k$. So $(x', t) \in S(R)$. $\square$

**Proof of (I) and (II).** At line L1, the row $i$ is $(a_i, b_i, e_i)$, and $e_i^\top A = a_i^\top$, $e_i^\top b = b_i$, $e_i \ge 0$; so (I) holds. The rows involve $x_1, \ldots, x_n$, and $S(R) = Q = \pi_n(Q)$; so (II) holds for $k = n$. Assume (I) and (II) at the start of the round for $k$. By Lemma 2 and Lemma 1, after line L8, $R$ satisfies (I), has zero coefficients on $x_k, \ldots, x_n$, and

$$S(R) = \{ x' : (x', t) \in \pi_k(Q) \text{ for some } t \} = \pi_{k-1}(Q).$$

So (II) holds at the start of the round for $k - 1$. The loop runs $n$ rounds, and each round builds a finite set of rows, so it stops.

**Line L9.** After the loop, (II) with $k = 0$ says that every row has all coefficients zero, and $S(R) = \pi_0(Q)$. A row $0 \le \beta$ holds exactly when $\beta \ge 0$. So $S(R)$ is nonempty, that is $Q \ne \emptyset$, exactly when no row has $\beta < 0$. If a row $(0, \beta, y)$ has $\beta < 0$, then by (I), $y \ge 0$, $y^\top A = 0$ and $y^\top b = \beta < 0$. So line L9 returns a valid certificate, and then $Q = \emptyset$, since $0 = y^\top A x \le y^\top b < 0$ is impossible for $x \in Q$.

**Back-substitution.** Assume that line L9 does not return, so $Q \ne \emptyset$. We show by induction on $k$ that after line L12 for $k$, $(x_1, \ldots, x_k) \in \pi_k(Q)$. For $k = 0$ the empty vector is in $\pi_0(Q)$ because $Q \ne \emptyset$. Let $x' = (x_1, \ldots, x_{k-1}) \in \pi_{k-1}(Q)$. The set $R_k$ saved at line L4 has $S(R_k) = \pi_k(Q)$ by (II), and by Lemma 2 and Lemma 1, $\pi_{k-1}(Q) = \{x' : (x', t) \in S(R_k) \text{ for some } t\}$. So some $t$ has $(x', t) \in S(R_k)$, and the proof of Lemma 2 shows that the set of such $t$ is exactly the interval $[lo, hi]$ computed at line L11, which is therefore nonempty. Line L12 picks a point of this interval: $lo$ if it is finite, otherwise $hi$ if it is finite, otherwise $0 \in (-\infty, +\infty)$. So $(x_1, \ldots, x_k) \in S(R_k) = \pi_k(Q)$. For $k = n$ this gives $x \in Q$, and line L13 returns a solution.

**Theorem.** FOURIER-MOTZKIN$(A, b)$ stops. It returns (INFEASIBLE, $y$) with $y \ge 0$, $y^\top A = 0$ and $y^\top b < 0$ if $Ax \le b$ has no solution, and (FEASIBLE, $x$) with $Ax \le b$ otherwise.

*Proof.* Termination was shown above. If $Q = \emptyset$, then by line L9's analysis some row has $\beta < 0$, and the returned $y$ is a certificate. If $Q \ne \emptyset$, no row has $\beta < 0$, and the back-substitution returns a point of $Q$. As a corollary, exactly one of "$Ax \le b$ has a solution" and "some $y \ge 0$ has $y^\top A = 0$, $y^\top b < 0$" holds, which is the [Farkas lemma](/farkas-lemma/). ∎
