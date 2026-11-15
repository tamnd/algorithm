---
title: The stopping test O_t = O_(t+1) gives the maximal positively invariant set, and the test is reached under stability, observability and a bounded constraint set
proves: [correctness]
status: full
---

The system is $x_{k+1} = A x_k$ with output $y_k = C x_k$, $A \in \mathbb{R}^{n \times n}$, $C \in \mathbb{R}^{p \times n}$. The constraint set is $Y = \{y : F y \le g\}$. For $t \ge 0$ let

$$O_t = \{x : F C A^k x \le g \text{ for } k = 0, 1, \dots, t\}, \qquad O_\infty = \bigcap_{t \ge 0} O_t.$$

So $O_\infty$ is the set of initial states whose output stays in $Y$ for all time. The sets are nested: $O_0 \supseteq O_1 \supseteq \dots \supseteq O_\infty$.

## Part 1: $O_\infty$ is the maximal positively invariant set in $O_0$

**Lemma 1.** $O_\infty$ is positively invariant ($A O_\infty \subseteq O_\infty$), it lies in $O_0$, and every positively invariant set $S \subseteq O_0$ lies in $O_\infty$.

*Proof.* If $x \in O_\infty$ then $F C A^k (A x) = F C A^{k+1} x \le g$ for all $k \ge 0$, so $A x \in O_\infty$. $O_\infty \subseteq O_0$ by definition. If $S \subseteq O_0$ is positively invariant and $x \in S$, then $A^k x \in S \subseteq O_0$ for every $k$, that is, $F C A^k x \le g$ for all $k$, so $x \in O_\infty$. $\square$

## Part 2: the stopping test

**Lemma 2.** $O_{t+1} = \{x \in O_0 : A x \in O_t\}$.

*Proof.* $A x \in O_t$ means $F C A^{k} A x \le g$ for $k = 0, \dots, t$, that is, the conditions $k = 1, \dots, t + 1$ on $x$. Together with $x \in O_0$ these are the conditions of $O_{t+1}$. $\square$

**Lemma 3.** If $O_t = O_{t+1}$, then $O_t = O_\infty$.

*Proof.* Let $x \in O_t$. Then $x \in O_{t+1}$, so $A x \in O_t$ by Lemma 2. So $O_t$ is positively invariant, and $O_t \subseteq O_0$. By Lemma 1, $O_t \subseteq O_\infty$. The other inclusion holds because the sets are nested. $\square$

So once the test succeeds, every later set is the same, and the algorithm may stop.

**Lemma 4 (the LP test, lines L4 to L6).** Let $R_t x \le c_t$ be any description of $O_t$. Then $O_{t+1} = O_t$ if and only if, for each row $i$ of $F$,

$$\max\{ (F C A^{t+1})_i \, x : R_t x \le c_t \} \le g_i,$$

where an unbounded maximum counts as a failure.

*Proof.* $O_{t+1} = O_t \cap \{x : F C A^{t+1} x \le g\}$. This equals $O_t$ if and only if every $x \in O_t$ satisfies each new row, which is the condition on the maximum. $\square$

**Lemma 5 (the stored description).** At the start of iteration $t$ of line L2, the stored rows describe $O_t$.

*Proof.* Line L1 stores $F C$, the rows of $O_0$. In iteration $t$, line L8 adds the rows of $F C A^{t+1}$ whose maximum over the stored set is larger than the bound. A row whose maximum is at most its bound holds at every point of $O_t$, so adding it would not change the set. So the stored rows after the iteration describe $O_t \cap \{F C A^{t+1} x \le g\} = O_{t+1}$. $\square$

**Theorem 1 (correctness).** If the algorithm returns at line L7 with index $t^*$, the returned rows describe $O_{t^*} = O_\infty$, the maximal positively invariant subset of $O_0$, and $t^*$ is the smallest $t$ with $O_t = O_{t+1}$.

*Proof.* Line L7 returns when no row of step $t + 1$ is new, that is, when $O_t = O_{t+1}$ by Lemmas 4 and 5. Lemma 3 and Lemma 1 give the rest. The loop tries $t = 0, 1, \dots$ in order, so the first success is the smallest such $t$. $\square$

## Part 3: finite determination

The loop is guaranteed to reach the test only under extra hypotheses. Without them it can run forever: for a rotation $A$ by an angle that is not a rational multiple of $\pi$ and a box $Y$, the sets $O_t$ keep gaining facets.

**Theorem 2.** Suppose $A$ is Schur (all eigenvalues in the open unit disc), $(C, A)$ is observable, $Y$ is bounded, and $Y$ contains a ball $\{y : |y| \le \rho\}$ with $\rho > 0$. Then $O_t = O_{t+1}$ for some $t$, so the algorithm stops.

*Proof.* Step 1: $O_{n-1}$ is bounded. Since $Y$ is bounded there is $c$ with $|y| \le c$ for $y \in Y$. The observability matrix $\mathcal{O} = (C; C A; \dots; C A^{n-1})$ has full column rank, so $\mathcal{O}^T \mathcal{O}$ is invertible and $|x| \le \|(\mathcal{O}^T \mathcal{O})^{-1} \mathcal{O}^T\| \, |\mathcal{O} x|$. For $x \in O_{n-1}$ each block $C A^k x$ lies in $Y$, so $|\mathcal{O} x| \le \sqrt{n} \, c$. Hence $|x| \le \beta$ on $O_{n-1}$ for some $\beta$.

Step 2: late constraints are automatic. Since $A$ is Schur, $A^k \to 0$, so there is $k_0$ with $\|C A^k\| \beta \le \rho$ for all $k \ge k_0$. For $x \in O_{n-1}$ and $k \ge k_0$, $|C A^k x| \le \rho$, so $C A^k x \in Y$.

Step 3: let $t = \max(n - 1, k_0)$. For $x \in O_t \subseteq O_{n-1}$ the condition of step $t + 1 \ge k_0$ holds by Step 2. So $O_{t+1} = O_t$. $\square$

The bound $t^* \le \max(n - 1, k_0)$ from the proof depends on how fast $\|C A^k\|$ decays, so $t^*$ grows without bound as the spectral radius of $A$ tends to 1. This is why the iteration count is part of the output and not a constant.

## Part 4: the linear programs

Each LP of line L5 has the form maximize $c^T x$ subject to $R x \le b$ with $x$ free. The routine writes $x = x^+ - x^-$ with $x^\pm \ge 0$ and adds a slack per row. Rows with $b_i < 0$ get an artificial variable, and phase one maximizes minus the sum of the artificials; a positive optimal sum means no feasible point. Phase two runs the simplex method on the original cost. Both phases use Bland's rule (the first improving column enters, ties in the ratio test are broken by the smallest basic index), which prevents cycling, so each phase stops after finitely many pivots. A column with an improving reduced cost and no positive entry is a ray along which the objective grows without bound, which is the unbounded report. These are the standard correctness facts of the simplex method; see the [simplex method](/simplex-method/) page. With integer and rational data the code uses exact rational arithmetic, so the tests $v > g_i$ of line L6 have no rounding error.
