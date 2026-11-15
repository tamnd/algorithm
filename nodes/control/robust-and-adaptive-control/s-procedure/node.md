---
tag: E4NDGT
kind: theorem
slug: s-procedure
name: S-procedure
aliases:
- S-lemma
- Yakubovich S-lemma
area: control/robust-and-adaptive-control
level: advanced
summary: "If F_0 - tau F_1 >= 0 everywhere for some tau >= 0, then F_0 >= 0 wherever F_1 >= 0. For one quadratic F_1 that is positive at some point the converse holds; for two or more it can fail."
prereqs: [positive-definite-matrix, linear-matrix-inequality]
see_also: [linear-matrix-inequality, lagrangian-duality, farkas-lemma, semidefinite-programming, bounded-real-lemma, lure-problem, circle-criterion, quadratic-stability]
sources:
  - book: isbn:089871334X
    title: Stephen Boyd, Laurent El Ghaoui, Eric Feron and Venkataramanan Balakrishnan, Linear Matrix Inequalities in System and Control Theory, SIAM Studies in Applied Mathematics 15, SIAM, 1994
    locator: Section 2.6.3, The S-procedure (the nonstrict and strict forms, the case of one constraint, the affine case, and the Lyapunov example with a norm-bounded nonlinearity), and the Notes and References of Chapter 2
  - paper: doi:10.1137/S003614450444614X
    title: Imre Pólik and Tamás Terlaky, A survey of the S-lemma, SIAM Review 49(3) (2007) 371-418
    locator: the statement of the S-lemma with the Slater condition, its proofs, the counterexamples with two constraints, and the history
  - paper: "V. A. Yakubovich, S-procedure in nonlinear control theory, Vestnik Leningrad University, 1971 (in Russian); English translation in Vestnik Leningrad University Mathematics 4 (1977) 73-93"
    locator: the proof that the S-procedure is lossless for one constraint
---

The S-procedure is a way to prove that a quadratic function is nonnegative on a set described by other quadratic inequalities. Instead of the hard question "is $F_0(x) \ge 0$ for every $x$ with $F_1(x) \ge 0, \dots, F_p(x) \ge 0$?", it asks the easier question "are there multipliers $\tau_i \ge 0$ with $F_0 - \sum_i \tau_i F_i \ge 0$ everywhere?". The second question is a [linear matrix inequality](/linear-matrix-inequality/) in the $\tau_i$. A yes always answers the first question. The S-lemma of Yakubovich says that for one constraint, with a point where the constraint is strict, the two questions have the same answer. This is why many robustness tests with one norm-bounded or sector-bounded uncertainty are exact LMIs.

## Statement

**Setting.** For $i = 0, 1, \dots, p$, let $F_i(x) = x^T T_i x + 2 u_i^T x + v_i$ on $\mathbb{R}^n$, with $T_i$ symmetric, $u_i \in \mathbb{R}^n$ and $v_i \in \mathbb{R}$. Write

$$M_i = \begin{bmatrix} T_i & u_i \\ u_i^T & v_i \end{bmatrix}, \qquad F_i(x) = \begin{bmatrix} x \\ 1 \end{bmatrix}^T M_i \begin{bmatrix} x \\ 1 \end{bmatrix}.$$

For symmetric matrices, $\succeq 0$ means positive semidefinite.

**Theorem 1 (the S-procedure).** If there are $\tau_1, \dots, \tau_p \ge 0$ with

$$M_0 - \tau_1 M_1 - \dots - \tau_p M_p \succeq 0,$$

then $F_0(x) \ge 0$ for every $x$ with $F_1(x) \ge 0, \dots, F_p(x) \ge 0$.

**Theorem 2 (the S-lemma, Yakubovich 1971).** Let $p = 1$ and assume that $F_1(x_0) > 0$ for some $x_0$. Then $F_0(x) \ge 0$ for every $x$ with $F_1(x) \ge 0$ if and only if there is $\tau \ge 0$ with $M_0 - \tau M_1 \succeq 0$, that is, with $F_0(x) - \tau F_1(x) \ge 0$ for all $x \in \mathbb{R}^n$.

## In plain words

You want to show that one quadratic function is never negative inside a region cut out by another quadratic function. Checking every point of the region is hard, because the functions need not be convex. The trick is to add a nonnegative multiple of the constraint function to the target function. Inside the region the constraint is nonnegative, so subtracting it can only make the target smaller there. If the difference is never negative anywhere, the target is never negative in the region. The S-lemma says that with one constraint, and a point where that constraint is strictly positive, this trick never misses: if the target is nonnegative in the region, some multiple works.

## Proof

**Theorem 1.** Let $F_i(x) \ge 0$ for $i = 1, \dots, p$. Then $F_0(x) \ge F_0(x) - \sum_i \tau_i F_i(x) \ge 0$, because each $\tau_i F_i(x) \ge 0$. The matrix condition is the same as $F_0 - \sum_i \tau_i F_i \ge 0$ on $\mathbb{R}^n$: one direction takes the vector $(x, 1)$, and for the other, a quadratic form $q(x, t)$ that is $\ge 0$ for all $t \ne 0$ (where $q(x, t) = t^2 q(x/t, 1)$) is $\ge 0$ at $t = 0$ too, by continuity.

The "if" part of Theorem 2 is Theorem 1 with $p = 1$. The "only if" part takes three steps.

**Step 1 (Dines' lemma).** For symmetric matrices $Q_0, Q_1$ of size $N$, the set $S = \{(z^T Q_0 z,\ z^T Q_1 z) : z \in \mathbb{R}^N\}$ is a convex cone in $\mathbb{R}^2$.

It is a cone because $(c z)^T Q_i (c z) = c^2 z^T Q_i z$. For convexity, take $z, w \in \mathbb{R}^N$ and put $z(\theta) = \cos\theta\, z + \sin\theta\, w$. Then

$$z(\theta)^T Q_i z(\theta) = \frac{z^T Q_i z + w^T Q_i w}{2} + \cos 2\theta\, \frac{z^T Q_i z - w^T Q_i w}{2} + \sin 2\theta\, z^T Q_i w ,$$

so as $\theta$ runs over $[0, \pi)$, the image point runs over a curve $E$ that is an affine image of the unit circle: an ellipse, a segment or a point. Let $\bar E$ be its convex hull (the filled ellipse, or $E$ itself). The image of the plane spanned by $z$ and $w$ is $\{r^2 e : r \ge 0,\ e \in E\}$, the cone generated by $E$. It is also the cone generated by $\bar E$: for $y \in \bar E$, $y \ne 0$, the farthest point $s^* y$ ($s^* \ge 1$) of $\bar E$ on the ray through $y$ lies on $E$, and $y = (1/s^*)(s^* y)$. The cone generated by a convex set is convex, and it contains the images of $z$ ($\theta = 0$) and of $w$ ($\theta = \pi/2$). So the segment between these two points of $S$ lies in $S$.

**Step 2 (homogenization).** Put $q_i(x, t) = (x, t)^T M_i (x, t)$ on $\mathbb{R}^{n+1}$, so that $q_i(x, 1) = F_i(x)$. Claim: $q_1(x, t) > 0$ implies $q_0(x, t) \ge 0$. If $t \ne 0$, this is the hypothesis at the point $x/t$, multiplied by $t^2$. If $t = 0$, then $x^T T_1 x > 0$. For large $s$, $F_1(s x) = s^2 x^T T_1 x + 2 s u_1^T x + v_1 > 0$, so $F_0(s x) \ge 0$; divide by $s^2$ and let $s \to \infty$ to get $q_0(x, 0) = x^T T_0 x \ge 0$.

**Step 3 (separation).** By Steps 1 and 2, the image $S$ of $\mathbb{R}^{n+1}$ under $(q_0, q_1)$ is a convex set that does not meet the open convex set $W = \{(a, b) : a < 0,\ b > 0\}$. Two disjoint convex sets in the plane, one of them open, are separated by a line, and since both are cones the line passes through the origin. So there are $\lambda_0, \lambda_1$, not both zero, with $\lambda_0 a - \lambda_1 b \ge 0$ on $S$ and $\le 0$ on $W$. Testing points of $W$ near $(-1, 0)$ and near $(0, 1)$ gives $\lambda_0 \ge 0$ and $\lambda_1 \ge 0$. If $\lambda_0 = 0$, then $\lambda_1 > 0$ and $-\lambda_1 q_1 \ge 0$ everywhere, which is false at $(x_0, 1)$, where $q_1 = F_1(x_0) > 0$. So $\lambda_0 > 0$, and with $\tau = \lambda_1 / \lambda_0 \ge 0$, $q_0 - \tau q_1 \ge 0$ on $\mathbb{R}^{n+1}$, that is, $M_0 - \tau M_1 \succeq 0$.

## Consequences

- **An LMI test.** For fixed $M_i$, the condition of Theorem 1 is an LMI in $p$ scalars of size $n + 1$, a small [semidefinite program](/semidefinite-programming/). If the $M_i$ depend affinely on other unknowns, such as a Lyapunov matrix, the condition stays an LMI in all unknowns together. This is how the S-procedure is used in control.
- **The strict form.** For quadratic forms ($u_i = 0$, $v_i = 0$) there is a strict version (Boyd et al. 1994, Section 2.6.3): if $\zeta^T T_0 \zeta > 0$ for every $\zeta \ne 0$ with $\zeta^T T_1 \zeta \ge 0$, and $\zeta_0^T T_1 \zeta_0 > 0$ for some $\zeta_0$, then $T_0 - \tau T_1 \succ 0$ for some $\tau \ge 0$; the converse is the easy direction.
- **Lyapunov functions with a norm-bounded nonlinearity.** For $x' = A x + B p$ with $|p| \le |C x|$ and $C \ne 0$, the derivative of $V = x^T P x$ is negative for every such $p$ and every $(x, p) \ne 0$ if and only if, for some $\tau \ge 0$,
$$\begin{bmatrix} A^T P + P A + \tau C^T C & P B \\ B^T P & -\tau I \end{bmatrix} \prec 0 .$$
This is the strict form with the constraint $|C x|^2 - |p|^2 \ge 0$ and the target $-2 x^T P (A x + B p)$ (Boyd et al. 1994, Section 2.6.3). Together with $P \succ 0$ it is one LMI in $(P, \tau)$. The lower right block forces $\tau > 0$, and after division by $\tau$ it is the [bounded real lemma](/bounded-real-lemma/) for $C (sI - A)^{-1} B$ with $\gamma = 1$: the small gain test. It is also the basis of the [Lur'e problem](/lure-problem/) and of the [circle criterion](/circle-criterion/). With a polytope of state matrices instead, one gets [quadratic stability](/quadratic-stability/).
- **A theorem of alternatives.** In terms of [Lagrangian duality](/lagrangian-duality/), the S-lemma says that the problem "minimize $F_0(x)$ subject to $F_1(x) \ge 0$" has no duality gap under the Slater condition, even when $F_0$ and $F_1$ are not convex. An example is the trust region problem: minimize a quadratic with an indefinite $T_0$ over a ball.
- **Affine constraints.** If all $T_i = 0$ and the set $\{F_1 \ge 0, \dots, F_p \ge 0\}$ is not empty, Theorem 1 is lossless for every $p$: this is the affine [Farkas lemma](/farkas-lemma/).

**Example.** Let $F_1(x) = 1 - x^2$, so the set is $[-1, 1]$, and $F_0(x) = 2 - x - x^2 = (1 - x)(2 + x)$, a concave function that is $\ge 0$ on $[-1, 1]$ and $0$ at $x = 1$. The Slater point is $x_0 = 0$. Then

$$F_0 - \tau F_1 = (\tau - 1) x^2 - x + (2 - \tau),$$

which is $\ge 0$ for all $x$ exactly when $\tau > 1$ and $1 - 4(\tau - 1)(2 - \tau) \le 0$, that is $(2\tau - 3)^2 \le 0$. So $\tau = 3/2$ is the only multiplier, and $F_0 - \frac{3}{2} F_1 = \frac{1}{2}(x - 1)^2$. In matrix form, $M_0 = \begin{bmatrix} -1 & -1/2 \\ -1/2 & 2 \end{bmatrix}$, $M_1 = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$, and $M_0 - \frac{3}{2} M_1 = \frac{1}{2}\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix} \succeq 0$, singular because the bound is reached at $x = 1$.

## Tightness

- **Two constraints.** Theorem 1 can be lossy for $p = 2$, even in one variable and with Slater points. Take $F_1(x) = x^2 - 1$ and $F_2(x) = x$, so the set is $\{x \ge 1\}$, and $F_0(x) = x - 1 \ge 0$ on it. For $\tau_1, \tau_2 \ge 0$, $F_0 - \tau_1 F_1 - \tau_2 F_2 = -\tau_1 x^2 + (1 - \tau_2) x - 1 + \tau_1$. Nonnegativity for all $x$ needs $\tau_1 = 0$ (the leading coefficient), and then $(1 - \tau_2) x - 1 \ge 0$ for all $x$ fails at $x = 0$. So no multipliers exist, although $x = 2$ makes both constraints strict. In general, deciding whether $F_0 \ge 0$ on the set of several quadratic constraints is hard; Boyd et al. (1994, notes to Chapter 2) state that it is NP-complete.
- **The Slater point.** Theorem 2 fails without it. Take $F_1(x) = -x^2$, so the set is $\{0\}$, and $F_0(x) = x$, which is $0$ there. For $\tau > 0$, $x + \tau x^2$ is $-1/(4\tau)$ at $x = -1/(2\tau)$, and for $\tau = 0$ it is $x$, so no $\tau \ge 0$ works.
- **The multiplier must be nonnegative.** With $\tau < 0$ allowed, the condition would prove $F_0 \ge 0$ on $\{F_1 \le 0\}$, a different set. For an equality constraint $F_1(x) = 0$ the multiplier is free, and the lossless version needs extra assumptions (see Pólik and Terlaky 2007).

## History

Lur'e and Postnikov used the idea in 1944 to find Lyapunov functions for systems with a sector-bounded nonlinearity, and Aizerman and Gantmacher gave it the name S-procedure in 1964 (as recorded in the notes of Boyd et al. 1994). The convexity of the joint range of two quadratic forms is due to Dines (1941). Yakubovich (1971) proved that the procedure is lossless for one constraint with a strictly feasible point. With interior point methods for LMIs in the 1990s, the S-procedure became a standard step that turns a robustness question into a semidefinite program. Pólik and Terlaky (2007) survey the proofs, the extensions and the links to optimization.

## References
