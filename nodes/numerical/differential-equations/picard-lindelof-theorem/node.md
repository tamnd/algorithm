---
tag: M0BRGQ
kind: theorem
slug: picard-lindelof-theorem
name: Picard-Lindelöf theorem
aliases:
- Cauchy-Lipschitz theorem
- existence and uniqueness theorem for ODEs
- Picard existence theorem
area: numerical/differential-equations
level: core
summary: "If f is continuous and Lipschitz in y near (t_0, y_0), then y' = f(t, y), y(t_0) = y_0 has exactly one solution on an interval of length 2 min(a, b/M), the limit of the Picard iterates."
prereqs: [ode-initial-value-problem, lipschitz-condition]
see_also: [picard-iteration, gronwall-inequality, banach-fixed-point-theorem, euler-method, global-error, delay-differential-equations]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section I.7 (existence theory by Euler polygons, Cauchy and Lipschitz), Section I.8 (existence by successive approximations, Picard and Lindelöf, with historical notes), Section I.10 (differential inequalities and Gronwall's lemma)
  - book: isbn:9780821883280
    title: Gerald Teschl, Ordinary Differential Equations and Dynamical Systems, Graduate Studies in Mathematics 140, American Mathematical Society, 2012
    locator: Chapter 2, Section 2.2 (the basic existence and uniqueness result) and Section 2.3 (dependence on the initial condition)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1, Section 1.1 (the Lipschitz condition and the existence and uniqueness of solutions, as the base of the convergence proofs)
  - paper: "Émile Picard, Mémoire sur la théorie des équations aux dérivées partielles et la méthode des approximations successives, Journal de Mathématiques Pures et Appliquées, 4e série, 6 (1890) 145-210"
    locator: the method of successive approximations
  - paper: "Ernst Lindelöf, Sur l'application de la méthode des approximations successives aux équations différentielles ordinaires du premier ordre, Comptes Rendus de l'Académie des Sciences 118 (1894) 454-457"
    locator: successive approximations under a Lipschitz condition
---

The Picard-Lindelöf theorem says that the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$ has exactly one solution near $t_0$ when $f$ is continuous and [Lipschitz](/lipschitz-condition/) in $y$. The proof constructs the solution as the limit of the [Picard iterates](/picard-iteration/) and gives an explicit interval of existence. Every convergence proof for a numerical method for ODEs starts from this theorem: it guarantees that there is a unique function $y(t)$ to approximate.

## Statement

**Notation.** $\|\cdot\|$ is a norm on $\mathbb{R}^d$. For $a > 0$ and $b > 0$, let $D = \{(t, y) : |t - t_0| \le a,\ \|y - y_0\| \le b\}$.

**Theorem (local version).** Let $f : D \to \mathbb{R}^d$ be continuous, and Lipschitz in $y$ on $D$: there is an $L \ge 0$ with

$$\|f(t, u) - f(t, v)\| \le L\, \|u - v\| \qquad \text{for all } (t, u), (t, v) \in D.$$

Let $M = \max_D \|f\|$ and $\alpha = \min(a, b/M)$, with $\alpha = a$ when $M = 0$. Then:

1. There is exactly one $C^1$ function $y : [t_0 - \alpha, t_0 + \alpha] \to \mathbb{R}^d$ with $y(t_0) = y_0$, $\|y(t) - y_0\| \le b$ and $y'(t) = f(t, y(t))$ for all $t$ in the interval.
2. The Picard iterates $y^{[0]}(t) = y_0$, $y^{[k+1]}(t) = y_0 + \int_{t_0}^t f(s, y^{[k]}(s))\, ds$ converge to $y$ uniformly on the interval, with

$$\|y(t) - y^{[k]}(t)\| \le \frac{M}{L} \sum_{j > k} \frac{(L|t - t_0|)^j}{j!} \le \frac{M}{L}\, \frac{(L\alpha)^{k+1}}{(k+1)!}\, e^{L\alpha} \qquad (L > 0).$$

3. Each $C^1$ solution of the problem with its graph in $D$, on a subinterval $J \ni t_0$ of $[t_0 - \alpha, t_0 + \alpha]$ equals $y$ on $J$.

**Theorem (global version).** Let $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ be continuous and Lipschitz in $y$ with one constant $L$ for all $t \in [t_0, T]$ and all $u, v \in \mathbb{R}^d$. Then the problem has exactly one solution on all of $[t_0, T]$.

## In plain words

A differential equation tells you the direction of motion at each point. Picard's idea is to guess a path, compute where the directions along that guess would take you, and use the result as the next guess. The theorem says that the guesses settle down to one path, and that no other path follows the directions, as long as the directions change in a controlled way when you move a little. The control is a bound on how fast the direction can change with the position.

The answer is only promised for a short time. The time is short enough that the path cannot leave the region where the bound holds. When the bound holds everywhere, the path exists for all the time you ask for.

## Proof

**Step 1: an integral equation.** A continuous function $y$ on an interval $J \ni t_0$ with values in the ball $\|y - y_0\| \le b$ is a $C^1$ solution of the initial value problem if and only if

$$y(t) = y_0 + \int_{t_0}^t f(s, y(s))\, ds \qquad \text{for all } t \in J. \tag{1}$$

If $y$ solves the problem, integrate $y' = f(t, y)$ from $t_0$ to $t$. Conversely, if $y$ is continuous and satisfies (1), the integrand $s \mapsto f(s, y(s))$ is continuous, so by the fundamental theorem of calculus $y$ is $C^1$ with $y' = f(t, y)$, and $y(t_0) = y_0$.

**Step 2: the iterates are defined and stay in $D$.** Let $I = [t_0 - \alpha, t_0 + \alpha]$. We show by induction on $k$ that $y^{[k]}$ is continuous on $I$ and $\|y^{[k]}(t) - y_0\| \le M |t - t_0| \le b$. For $k = 0$ this is true. If it holds for $k$, then $(s, y^{[k]}(s)) \in D$ for $s \in I$, so the integrand of $y^{[k+1]}$ is continuous and bounded by $M$. Hence $y^{[k+1]}$ is continuous and $\|y^{[k+1]}(t) - y_0\| \le M|t - t_0| \le M\alpha \le b$, since $\alpha \le b/M$.

**Step 3: the differences decrease like a factorial.** We show that $\|y^{[k+1]}(t) - y^{[k]}(t)\| \le M L^k |t - t_0|^{k+1}/(k+1)!$ for $t \in I$ and $k \ge 0$. For $k = 0$ this is Step 2. Assume it for $k - 1$. Take $t \ge t_0$ (the case $t < t_0$ is the same with the integral reversed). By the Lipschitz condition, which applies because both iterates stay in $D$,

$$\|y^{[k+1]}(t) - y^{[k]}(t)\| \le \int_{t_0}^t L\, \|y^{[k]}(s) - y^{[k-1]}(s)\|\, ds \le \int_{t_0}^t L \frac{M L^{k-1} (s - t_0)^k}{k!}\, ds = \frac{M L^k (t - t_0)^{k+1}}{(k+1)!}.$$

**Step 4: uniform convergence.** The series $\sum_k \max_I \|y^{[k+1]} - y^{[k]}\|$ is bounded by $\sum_k M L^k \alpha^{k+1}/(k+1)!$, which converges. By the Weierstrass M-test, $y^{[k]} = y^{[0]} + \sum_{j < k} (y^{[j+1]} - y^{[j]})$ converges uniformly on $I$ to a continuous function $y$, and summing the tail of the bound of Step 3 gives the error bound of part 2 (with $L > 0$; for $L = 0$ the iterates are equal from $k = 1$ on). The closed ball is closed, so $\|y(t) - y_0\| \le b$.

**Step 5: the limit solves (1).** For $s \in I$, $\|f(s, y(s)) - f(s, y^{[k]}(s))\| \le L \|y(s) - y^{[k]}(s)\|$, which tends to $0$ uniformly. So $\int_{t_0}^t f(s, y^{[k]}(s))\, ds \to \int_{t_0}^t f(s, y(s))\, ds$, and letting $k \to \infty$ in the definition of $y^{[k+1]}$ gives (1). By Step 1, $y$ is a $C^1$ solution on $I$. This proves part 1 (existence) and part 2.

**Step 6: uniqueness.** Let $z$ be a $C^1$ solution on a subinterval $J \ni t_0$ of $I$. Since $f$ is defined only on $D$, the graph of $z$ lies in $D$, and by Step 1 $z$ satisfies (1). We show by induction that $\|z(t) - y^{[k]}(t)\| \le M L^k |t - t_0|^{k+1}/(k+1)!$ on $J$. For $k = 0$, (1) gives $\|z(t) - y_0\| \le M |t - t_0|$. The induction step is the integral estimate of Step 3, with $z$ in place of $y^{[k+1]}$. The right side tends to $0$, so $z = \lim_k y^{[k]} = y$ on $J$. This proves part 3.

**Step 7: the global version.** With a global Lipschitz constant, there is no ball to stay in. Define the iterates on $[t_0, T]$ and let $M_0 = \max_{[t_0, T]} \|f(t, y_0)\|$. The same induction gives $\|y^{[k+1]}(t) - y^{[k]}(t)\| \le M_0 L^k (t - t_0)^{k+1}/(k+1)!$, and Steps 4 to 6 go through on the whole interval with $b = \infty$. $\blacksquare$

The proof is also an instance of the [Banach fixed-point theorem](/banach-fixed-point-theorem/): the map $\Phi(y)(t) = y_0 + \int_{t_0}^t f(s, y(s))\, ds$ is a contraction on $C([t_0, t_0 + \alpha])$ in the weighted norm $\max_t e^{-2L(t - t_0)}\|y(t)\|$, with the factor $\frac12$. The factorial estimate of Step 3 avoids the weighted norm.

## Consequences

- **Continuous dependence on the data.** If $y$ and $z$ solve the same equation with $y(t_0) = y_0$ and $z(t_0) = z_0$, then $\|y(t) - z(t)\| \le e^{L|t - t_0|} \|y_0 - z_0\|$ by the [Gronwall inequality](/gronwall-inequality/). With the existence and uniqueness, this makes the initial value problem well posed in the sense of Hadamard. The factor $e^{L(t - t_0)}$ is the same factor that appears in the [global error](/global-error/) bounds of one-step methods.
- **Linear systems.** For $y' = A(t) y + g(t)$ with continuous $A$ and $g$ on $[t_0, T]$, the constant $L = \max_t \|A(t)\|$ works globally, so the solution exists on all of $[t_0, T]$.
- **Maximal solutions.** For $f$ locally Lipschitz on an open set, repeated use of the local theorem extends the solution to a maximal interval. At an end of that interval the solution leaves every compact subset of the domain. For $f$ defined on all of $\mathbb{R}^d$ this means that $\|y(t)\| \to \infty$ in finite time, or the solution exists for all time.
- **Numerical methods.** The convergence theorems for the [Euler method](/euler-method/), for Runge-Kutta methods and, with [zero-stability](/zero-stability/), for linear multistep methods, assume a Lipschitz $f$. Their proofs repeat Step 3 in a discrete form.
- **Example: the exponential.** For $y' = y$, $y(0) = 1$, the iterates are the Taylor polynomials $y^{[k]}(t) = \sum_{j=0}^k t^j/j!$. With $a = \frac12$ and $b = 1$ the constants are $M = 2$, $L = 1$, $\alpha = \frac12$. At $t = \frac12$ the true errors for $k = 1, 2, 3, 4, 5$ are $1.487 \cdot 10^{-1}$, $2.372 \cdot 10^{-2}$, $2.888 \cdot 10^{-3}$, $2.838 \cdot 10^{-4}$ and $2.335 \cdot 10^{-5}$. The bound of part 2 gives $4.122 \cdot 10^{-1}$, $6.870 \cdot 10^{-2}$, $8.587 \cdot 10^{-3}$, $8.587 \cdot 10^{-4}$ and $7.156 \cdot 10^{-5}$, about 3 times the true error.

## Tightness

- **Without the Lipschitz condition, uniqueness can fail.** For $y' = 2\sqrt{|y|}$, $y(0) = 0$, the function $f$ is continuous but not Lipschitz near $y = 0$. Both $y = 0$ and $y = t^2$ for $t \ge 0$ (and $0$ for $t < 0$) are solutions, and so is each function that is $0$ up to some $c \ge 0$ and $(t - c)^2$ after. Existence alone still holds for continuous $f$ (Peano's theorem, HNW I, Section I.7), but not uniqueness.
- **The solution may exist only locally.** For $y' = y^2$, $y(0) = 1$, $f$ is Lipschitz on each bounded set, but not globally. The solution $y = 1/(1 - t)$ blows up at $t = 1$. The local theorem with $D = [-a, a] \times [0, 2]$ gives $M = 4$ and $\alpha = \min(a, \frac14)$. The best choice over all $b$ is $\alpha = \max_b b/(1 + b)^2 = \frac14$, at $b = 1$. So the interval of the theorem can be much shorter than the true interval of existence $(-\infty, 1)$. The theorem gives a lower bound on the interval, not its length.
- **The Lipschitz condition is sufficient, not necessary.** The weaker Osgood condition $\|f(t, u) - f(t, v)\| \le \omega(\|u - v\|)$ with $\int_0 dr/\omega(r) = \infty$ also gives uniqueness, for example $\omega(r) = r \log(1/r)$. For $y' = 2\sqrt{|y|}$, $\omega(r) = 2\sqrt r$ has a finite integral, which matches the failure above.
- **Continuity in $t$ can be weakened.** For $f$ measurable in $t$ and Lipschitz in $y$ with an integrable bound, the same proof gives a unique absolutely continuous solution (the Carathéodory setting). The solution is then not $C^1$.
- **The error bound is attained in order.** For $y' = y$ the error of the iterate $y^{[k]}$ at $t$ is $\sum_{j > k} t^j/j!$, whose first term is the first term of the bound. So the factor $(L\alpha)^{k+1}/(k+1)!$ cannot be improved in general.

## History

Cauchy proved existence and uniqueness in his lectures of the 1820s, with Euler polygons and a bounded derivative $f_y$, and Lipschitz replaced the derivative by the Lipschitz condition in 1868 (HNW I, Section I.7). Picard introduced the method of successive approximations in 1890, and Lindelöf published an existence proof by this method under a Lipschitz condition in 1894 (HNW I, Section I.8). In French texts the result is called the Cauchy-Lipschitz theorem.

## References
