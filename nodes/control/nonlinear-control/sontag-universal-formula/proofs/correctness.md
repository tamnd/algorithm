---
title: Sontag's formula makes the derivative of the control Lyapunov function negative, is smooth away from the origin, and is continuous at the origin exactly under the small control property
proves: [correctness, regularity]
status: full
---

The system is $\dot x = f(x) + g(x) u$ with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, $f$ and $g$ smooth ($C^\infty$) and $f(0) = 0$. $V : \mathbb{R}^n \to \mathbb{R}$ is smooth, positive definite and proper (radially unbounded). For a state $x$ write

$$a(x) = \nabla V(x) \cdot f(x), \qquad b(x) = \nabla V(x)\, g(x) \in \mathbb{R}^{1 \times m}, \qquad \beta(x) = |b(x)|^2,$$

where $|\cdot|$ is the Euclidean norm. $V$ is a control Lyapunov function if $\beta(x) = 0$ implies $a(x) < 0$ for every $x \neq 0$. $V$ has the small control property if for every $\varepsilon > 0$ there is $\delta > 0$ such that every $x$ with $0 < |x| < \delta$ has some $u$ with $|u| < \varepsilon$ and $a(x) + b(x) u < 0$.

The algorithm (lines L1 to L6) returns $k(x) = 0$ if $\beta(x) = 0$ and $k(x) = -\varphi(a(x), \beta(x))\, b(x)^T$ otherwise, where

$$\varphi(a, \beta) = \frac{a + \sqrt{a^2 + \beta^2}}{\beta} \quad (\beta > 0), \qquad \varphi(a, 0) = 0.$$

## Lemma 1: the two forms at line L5 agree

Let $\beta > 0$ and $s = \sqrt{a^2 + \beta^2}$. Then $s > |a| \ge a$, so $s - a > 0$, and $(a + s)(s - a) = s^2 - a^2 = \beta^2$. Divide by $\beta (s - a)$: $(a + s)/\beta = \beta / (s - a)$. So both branches of line L5 compute $\varphi(a, \beta)$. The second form adds two nonnegative numbers when $a \le 0$, so it has no cancellation. $\square$

## Lemma 2: the closed loop derivative

For every $x$, with $u = k(x)$,

$$\dot V = a + b\, k(x) = \begin{cases} -\sqrt{a^2 + \beta^2} & \text{if } \beta > 0, \\ a & \text{if } \beta = 0. \end{cases}$$

*Proof.* If $\beta = 0$, $k = 0$ and $\dot V = a$. If $\beta > 0$, $b\, k = -\varphi\, b b^T = -\varphi \beta = -(a + \sqrt{a^2 + \beta^2})$, so $a + b k = -\sqrt{a^2 + \beta^2}$. $\square$

**Consequence.** If $V$ is a control Lyapunov function, then $\dot V(x) < 0$ for every $x \neq 0$. If $\beta(x) > 0$, $\dot V = -\sqrt{a^2 + \beta^2} \le -\beta < 0$. If $\beta(x) = 0$ and $x \neq 0$, the definition gives $\dot V = a(x) < 0$.

## Lemma 3: phi is real-analytic on the set S

Let $S = \{(a, \beta) \in \mathbb{R}^2 : \beta > 0 \text{ or } a < 0\}$. $S$ is open, and $\varphi$ is real-analytic on $S$.

*Proof.* Put $F(a, \beta, p) = \beta p^2 - 2 a p - \beta$. For $\beta > 0$ the roots of $F(a, \beta, \cdot)$ are $(a \pm \sqrt{a^2 + \beta^2})/\beta$, and $\varphi$ is the larger one, so $F(a, \beta, \varphi(a, \beta)) = 0$. For $\beta = 0$ and $a < 0$, $F(a, 0, p) = -2 a p$, which is zero at $p = 0 = \varphi(a, 0)$. So $F(a, \beta, \varphi(a, \beta)) = 0$ on all of $S$. The partial derivative is $\partial F / \partial p = 2 \beta p - 2 a$. At $p = \varphi$ with $\beta > 0$ it equals $2 \sqrt{a^2 + \beta^2} > 0$. At $p = 0$ with $\beta = 0$, $a < 0$ it equals $-2 a > 0$. By the real-analytic implicit function theorem, near each point of $S$ the equation $F = 0$ has a unique real-analytic solution $p(a, \beta)$ close to $\varphi$. It remains to show that this solution is $\varphi$ itself. On $\beta > 0$, $\varphi$ is the larger root, which is analytic there by the formula. Near a point $(a_0, 0)$ with $a_0 < 0$, Lemma 1 gives $\varphi = \beta / (\sqrt{a^2 + \beta^2} - a)$ for $\beta > 0$, and this expression is also $0$ at $\beta = 0$. The expression is a quotient of analytic functions with a denominator near $-2 a_0 > 0$, so it is analytic near $(a_0, 0)$, and it equals $\varphi$ there. So $\varphi$ is real-analytic on $S$. $\square$

## Theorem 1: smooth away from the origin

If $V$ is a control Lyapunov function, then $k$ is smooth on $\mathbb{R}^n \setminus \{0\}$.

*Proof.* Let $x \neq 0$. If $\beta(x) > 0$, then $(a(x), \beta(x)) \in S$. If $\beta(x) = 0$, the definition gives $a(x) < 0$, so again $(a(x), \beta(x)) \in S$. The maps $x \mapsto a(x)$, $x \mapsto \beta(x)$ and $x \mapsto b(x)$ are smooth, and $S$ is open. On a neighborhood of $x$, $k(x) = -\varphi(a(x), \beta(x))\, b(x)^T$ is a composition and product of smooth maps, by Lemma 3. Note that on $\beta = 0$ the formula $-\varphi b^T$ gives $0$, which is the value that line L4 returns, so one smooth expression covers both branches. $\square$

## Theorem 2: continuity at the origin

Set $k(0) = 0$. Then $k$ is continuous at $0$ if and only if $V$ has the small control property.

*Proof.* First, $b(0) = 0$. $V$ has a minimum at $0$, so $\nabla V(0) = 0$.

($\Leftarrow$) Let $\varepsilon > 0$. Take $\delta$ from the small control property, and take $\delta' > 0$ such that $|b(x)| < \varepsilon$ when $|x| < \delta'$; $\delta'$ exists because $b$ is continuous and $b(0) = 0$. Let $0 < |x| < \min(\delta, \delta')$. If $\beta(x) = 0$, $k(x) = 0$. Otherwise $|k(x)| = \varphi\, |b|$. There are two cases.

- $a \le 0$. By Lemma 1, $\varphi = \beta / (s - a)$ with $s = \sqrt{a^2 + \beta^2} \ge \beta$ and $-a \ge 0$, so $\varphi \le 1$ and $|k(x)| \le |b(x)| < \varepsilon$.
- $a > 0$. The small control property gives a $u$ with $|u| < \varepsilon$ and $a + b u < 0$. By the Cauchy-Schwarz inequality, $a < -b u \le |b|\, \varepsilon$. Also $s \le a + \beta$. So $\varphi \le (2 a + \beta)/\beta$, and $|k(x)| \le (2 a + \beta) / |b| = 2 a / |b| + |b| < 2 \varepsilon + \varepsilon$.

In both cases $|k(x)| < 3 \varepsilon$. As $\varepsilon$ is arbitrary, $k(x) \to 0 = k(0)$.

($\Rightarrow$) Let $k$ be continuous at $0$, and let $\varepsilon > 0$. Take $\delta$ with $|k(x)| < \varepsilon$ for $|x| < \delta$. For $0 < |x| < \delta$, the input $u = k(x)$ has $|u| < \varepsilon$ and, by Lemma 2 and its consequence, $a + b u < 0$. This is the small control property. $\square$

## Theorem 3: global asymptotic stability

If $V$ is a control Lyapunov function with the small control property, the closed loop $\dot x = F(x) = f(x) + g(x) k(x)$ has the origin as a globally asymptotically stable equilibrium.

*Proof.* $F$ is continuous on $\mathbb{R}^n$ by Theorems 1 and 2, and $F(0) = f(0) = 0$. On $\mathbb{R}^n \setminus \{0\}$, $F$ is smooth, so it is locally Lipschitz there, and solutions are unique while they stay away from $0$ (Picard-Lindelöf). A solution that is at $0$ at some time $t_0$ stays at $0$ for $t \ge t_0$: along any solution, $\frac{d}{dt} V(x(t)) = \nabla V \cdot F \le 0$, because it is negative for $x \neq 0$ and $\nabla V(0) = 0$. So $V(x(t)) \le V(x(t_0)) = 0$ for $t \ge t_0$, and $V$ is positive definite. So every initial state has a unique forward solution. $V$ is proper, so the sublevel set $\{V \le V(x_0)\}$ is compact and holds the whole solution, which therefore exists for all $t \ge 0$. With $V$ positive definite and proper and $\dot V < 0$ for $x \neq 0$, Lyapunov's direct method gives global asymptotic stability; its proof uses only existence, uniqueness and the decrease of $V$ along solutions. $\square$

## The implementation

`sontag_feedback` computes $a$ at line L1 and the $m$ entries of $b$ at line L2 from the given $f$, $g$ and $\nabla V$. `sontag_gain` computes $\beta$ at line L3, returns $0$ at line L4 when $\beta = 0$, computes $\varphi$ at line L5 with the form of Lemma 1 that has no cancellation, and returns $-\varphi b^T$ at line L6. Each line is a direct transcription of the definition of $k$, so the code returns $k(x)$ up to the rounding of floating point arithmetic. $\blacksquare$
