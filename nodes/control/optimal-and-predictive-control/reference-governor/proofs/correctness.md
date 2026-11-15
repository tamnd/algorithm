---
title: The admissible set is finitely determined and invariant, so the governed loop meets the constraints for all time and reaches a constant admissible reference in finite time
proves: [correctness]
status: full
---

**Setting.** The closed loop is $x_{k+1} = A x_k + B v_k$, $y_k = C x_k + D v_k$, with $x \in \mathbb{R}^n$, $v \in \mathbb{R}^m$ and $A$ Schur. The constraint is $H y \le h$ with $h > 0$ componentwise, and $Y = \{y : H y \le h\}$ is bounded. Fix $\varepsilon \in (0, 1)$. Let $S_t = I + A + \dots + A^{t-1}$ ($S_0 = 0$), let $G_0 = C (I - A)^{-1} B + D$ be the steady state gain, and assume that $(C, A)$ is observable and $G_0$ has full column rank. If $v$ is held constant from the state $x$, the output at time $t$ is

$$y_t(x, v) = C A^t x + (C S_t B + D) v. \tag{1}$$

Write $z = (x, v)$ and $M z = (A x + B v, v)$ for one step with $v$ held. Then $y_t(M z) = y_{t+1}(z)$, because $A^t (A x + B v) + S_t B v = A^{t+1} x + S_{t+1} B v$.

Define the sets $\mathcal{S} = \{z : H G_0 v \le (1 - \varepsilon) h\}$, $R_t = \{z : H y_t(z) \le h\}$, $O_{-1} = \mathcal{S}$ and $O_t = O_{t-1} \cap R_t$, and

$$O = \mathcal{S} \cap \bigcap_{t \ge 0} R_t.$$

## Part 1: the LP

`lp_max` solves $\max\, c^T z$ subject to $G z \le g$ with $g \ge 0$. The point $z = 0$ is feasible. By LP duality, the primal is bounded if and only if the dual $\min\, g^T \lambda$ subject to $G^T \lambda = c$, $\lambda \ge 0$ is feasible, and then both optima are equal. Phase 1 minimizes the sum of the artificial variables; its value is 0 exactly when the dual is feasible, and the code then returns `None` otherwise. After the artificial variables are pivoted out of the basis (an equation whose row has no nonzero entry outside the artificial columns is a linear combination of the others and is dropped), phase 2 starts from a feasible basis. Bland's rule makes both phases end after finitely many pivots (Bland 1977). Phase 2 cannot be unbounded, since every dual feasible $\lambda$ has $g^T \lambda \ge c^T 0 = 0$ by weak duality. So the returned value is the primal maximum. With rational data and `tol = 0` all operations are exact.

## Part 2: the stopping test is correct

**Lemma 1.** For every $t \ge 0$, $O_t = \mathcal{S} \cap R_0 \cap M^{-1}(O_{t-1})$.

*Proof.* $z \in M^{-1}(R_{s}) \iff H y_s(M z) \le h \iff H y_{s+1}(z) \le h \iff z \in R_{s+1}$. Also $M^{-1}(\mathcal{S}) = \mathcal{S}$ because $M$ does not change $v$. So $M^{-1}(O_{t-1}) = \mathcal{S} \cap R_1 \cap \dots \cap R_t$, and intersecting with $\mathcal{S} \cap R_0$ gives $O_t$. $\square$

**Lemma 2.** If $O_t = O_{t-1}$ for some $t \ge 0$, then $O = O_{t-1}$.

*Proof.* By Lemma 1, $O_{t+1} = \mathcal{S} \cap R_0 \cap M^{-1}(O_t) = \mathcal{S} \cap R_0 \cap M^{-1}(O_{t-1}) = O_t$. By induction $O_s = O_{t-1}$ for all $s \ge t - 1$, so $O = \bigcap_s O_s = O_{t-1}$. $\square$

Lines L4 and L5 test whether every row of $R_t$ is redundant in the current set, by one LP per row: the row $a^T z \le b$ is redundant in $\{G z \le g\}$ if and only if $\max\{a^T z : G z \le g\} \le b$. The code adds to the set only the rows that are not redundant; this does not change the set. If all rows of $R_t$ are redundant, then $O_t = O_{t-1}$, and by Lemma 2 the rows found so far define $O$.

## Part 3: the loop stops

**Lemma 3.** There is a finite $t^*$ such that $O_{t^* - 1} = O_{t^*}$.

*Proof.* First, $O_{n-1}$ is bounded. On $\mathcal{S}$, $H G_0 v \le (1 - \varepsilon) h$, so $G_0 v \in Y$, which is bounded, and $v$ is bounded because $G_0$ has full column rank. On $R_0 \cap \dots \cap R_{n-1}$, the vector $\mathcal{O} x$, where $\mathcal{O}$ stacks $C, C A, \dots, C A^{n-1}$, equals the stacked outputs minus terms linear in $v$; the outputs lie in $Y$ and $v$ is bounded, and $\mathcal{O}$ has full column rank by observability, so $x$ is bounded. Let $\rho$ bound $|x - (I - A)^{-1} B v|$ on $O_{n-1}$.

Next, with $x_s(v) = (I - A)^{-1} B v$, (1) gives $y_t(z) = G_0 v + C A^t (x - x_s(v))$. Since $A$ is Schur, $\|C A^t\| \to 0$, so there is $t_1$ such that $\|H_i\|\, \|C A^t\|\, \rho \le \varepsilon h_i$ for all rows $i$ and all $t \ge t_1$. For $z \in O_{n-1}$ and $t \ge t_1$,

$$H_i y_t(z) \le H_i G_0 v + \|H_i\|\, \|C A^t\|\, \rho \le (1 - \varepsilon) h_i + \varepsilon h_i = h_i.$$

So every row of $R_t$ is redundant in $O_{n-1} \supseteq O_{t-1}$ for $t \ge \max(n, t_1)$, and the loop stops at the latest at that $t$. $\square$

## Part 4: the online step

**Lemma 4.** If $(x, v_{\rm prev}) \in O$, `governor_step` returns the largest $\kappa \in [0, 1]$ with $(x, v_{\rm prev} + \kappa (r - v_{\rm prev})) \in O$.

*Proof.* Let $d = r - v_{\rm prev}$. A row $a_x^T x + a_v^T v \le b$ at $v = v_{\rm prev} + \kappa d$ reads $\kappa \alpha \le \beta$ with $\alpha = a_v^T d$ and $\beta = b - a_x^T x - a_v^T v_{\rm prev} \ge 0$. If $\alpha \le 0$ the row holds for all $\kappa \ge 0$. If $\alpha > 0$ it holds exactly for $\kappa \le \beta/\alpha$. So the set of feasible $\kappa \in [0, 1]$ is $[0, \min(1, \min_{\alpha > 0} \beta/\alpha)]$, which is what line L7 computes. $\square$

**Theorem.** Let $(x_0, v_{-1}) \in O$. Then for all $k \ge 0$:

1. the step is defined, $\kappa_k \in [0, 1]$, and $(x_k, v_k) \in O$;
2. $H y_k \le h$;
3. if $r_k = r$ for all $k \ge k_0$ and $H G_0 r \le (1 - \varepsilon) h$, then $v_k = r$ for all $k$ after some finite time.

*Proof.* (1) and (2). $O$ is invariant under $M$: if $z \in O$, then $z \in O_t$ for all $t$, and by Lemma 1 $M z \in O_{t-1}$ for all $t$, so $M z \in O$. Suppose $(x_k, v_{k-1}) \in O$. By Lemma 4, $\kappa_k$ exists and $(x_k, v_k) \in O \subseteq R_0$, so $H y_k = H (C x_k + D v_k) \le h$. Then $(x_{k+1}, v_k) = M (x_k, v_k) \in O$. Induction on $k$ gives (1) and (2).

(3). For $k \ge k_0$ the values $v_k$ lie on the segment from $v_{k_0 - 1}$ to $r$ and move toward $r$: $r - v_k = (1 - \kappa_k)(r - v_{k-1})$. So $|r - v_k|$ is nonincreasing and $v_k \to \bar v$ for some $\bar v$ on the segment. Suppose that $v_k \ne r$ for all $k$. The rows of $\mathcal{S}$ never limit $\kappa$: they are linear in $v$ alone and hold at $v_{k-1}$ and at $r$, so they hold on the segment between. Since $\mathcal{S}$ is convex and contains $v_{k_0 - 1}$ and $r$, it contains $\bar v$ and every $v'$ between $\bar v$ and $r$. Because $v_k \to \bar v$ and $A$ is Schur, $x_k \to x_s(\bar v)$. For a row of $R_t$ at $(x_k, v')$,

$$H_i y_t(x_k, v') = H_i G_0 v' + H_i C A^t (x_k - x_s(v')) \le (1 - \varepsilon) h_i + c \left(|x_k - x_s(\bar v)| + |v' - \bar v|\right)$$

with $c = \max_i \|H_i\| \sup_t \|C A^t\| \max(1, \|(I - A)^{-1} B\|)$, which is finite since $A$ is Schur. Choose $\delta > 0$ with $2 c \delta \le \varepsilon \min_i h_i$. For $k$ large, $|x_k - x_s(\bar v)| \le \delta$ and $|v_{k-1} - \bar v| \le \delta / 2$; then every $v'$ on the segment with $|v' - v_{k-1}| \le \delta / 2$ is admissible at $x_k$, so either $v_k = r$ or $|v_k - v_{k-1}| \ge \delta / 2$. The second case cannot happen infinitely often for a convergent sequence, so $v_k = r$ for some $k$, against the assumption. Once $v_k = r$, the direction is $d = 0$ and $v$ stays at $r$. $\square$

## Part 5: what the code computes

- **Line L1** forms $G_0$ by solving $(I - A) X = B$ and adds the rows of $\mathcal{S}$, which is $O_{-1}$.
- **Lines L2 and L3** keep $A^t$ and $S_t B$ with the recursions $A^{t+1} = A A^t$ and $S_{t+1} B = B + A S_t B$, and form the rows of $R_t$ from (1).
- **Lines L4 and L5** are the test of Part 2. The returned $t^*$ is the first $t$ with $O_t = O_{t-1}$, so the rows of $\mathcal{S}$ and of $R_0, \dots, R_{t^* - 1}$ define $O$.
- **Lines L6 to L8** are the step of Lemma 4 and the plant update. With floating point data, $\beta$ can be slightly negative from rounding; the code then sets $\kappa = 0$, which keeps the old $v$ and is the choice that the theorem allows.
