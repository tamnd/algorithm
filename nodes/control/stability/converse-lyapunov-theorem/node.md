---
tag: DWAZ4N
kind: theorem
slug: converse-lyapunov-theorem
name: Converse Lyapunov theorem
aliases:
- Massera's theorem
area: control/stability
level: advanced
summary: If an equilibrium is exponentially or uniformly asymptotically stable, a Lyapunov function that proves it exists. The proof builds it from the solutions, so it gives existence, not a formula.
prereqs: [lyapunov-direct-method, exponential-stability]
see_also: [lyapunov-function, lyapunov-direct-method, lyapunov-indirect-method, lyapunov-theorem-for-linear-systems, exponential-stability, input-to-state-stability, sum-of-squares-programming, region-of-attraction]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.7, Converse Theorems; Section 4.4 for the comparison functions
  - paper: doi:10.2307/1969558
    title: "J. L. Massera, On Liapounoff's conditions of stability, Annals of Mathematics 50(3), 705-721, 1949"
    locator: the converse theorem for asymptotic stability, and the lemma on the choice of the function G in section 12, p. 716
  - paper: "J. Kurzweil, On the inversion of Ljapunov's second theorem on stability of motion, Czechoslovak Mathematical Journal 6(81), 217-259 and 455-484, 1956 (in Russian); English translation in American Mathematical Society Translations, Series 2, 24, 19-77"
    locator: smooth Lyapunov functions for asymptotic stability when the right-hand side is only continuous
  - paper: doi:10.3934/dcdsb.2015.20.2333
    title: "C. M. Kellett, Classical converse theorems in Lyapunov's second method, Discrete and Continuous Dynamical Systems, Series B, 20(8), 2333-2360, 2015"
    locator: the history of the converse theorems, from Lyapunov's linear case to Massera and Kurzweil
  - paper: doi:10.1109/CDC.2011.6161499
    title: "A. A. Ahmadi, M. Krstic and P. A. Parrilo, A globally asymptotically stable polynomial vector field with no polynomial Lyapunov function, Proceedings of the 50th IEEE Conference on Decision and Control, 7579-7580, 2011"
    locator: Theorem 1.1, p. 7579
---

A converse Lyapunov theorem says that the [direct method of Lyapunov](/lyapunov-direct-method/) is not only sufficient but also necessary. The direct method goes from a [Lyapunov function](/lyapunov-function/) to a stability property. The converse goes back: if the equilibrium has the property, a Lyapunov function with matching bounds exists. There are several converse theorems, one for each stability property. The two that are used most are the one for [exponential stability](/exponential-stability/), where the function is bounded above and below by quadratics, and the one for uniform asymptotic stability, where the bounds are comparison functions. The proofs build the function from the solutions of the system, so they show existence but do not give a formula that one can use without the solutions. The theorems are a tool for proofs: they let one start from a Lyapunov function when only the stability property is known, for example to show that the property survives a perturbation.

## Statement

**Setting.** $\dot x = f(t, x)$ with $f(t, 0) = 0$ for all $t \ge 0$, on $[0, \infty) \times D$, where $D = \{x \in \mathbb{R}^n : |x| < r\}$. The function $f$ is continuously differentiable, and the Jacobian is bounded on $D$ uniformly in $t$: $\|\partial f / \partial x\,(t, x)\| \le L$. The norm $|\cdot|$ is the Euclidean norm. A function $\alpha : [0, a) \to [0, \infty)$ is of *class $\mathcal K$* if it is continuous, strictly increasing and $\alpha(0) = 0$. A function $\beta(s, t)$ is of *class $\mathcal{KL}$* if $\beta(\cdot, t)$ is of class $\mathcal K$ for each fixed $t$, and $\beta(s, \cdot)$ is decreasing with $\beta(s, t) \to 0$ as $t \to \infty$ for each fixed $s$ (Khalil 2002, Section 4.4).

**Theorem A (exponential stability).** Let $k \ge 1$, $\lambda > 0$ and $r_0 < r / k$, and let every solution with $|x(t_0)| < r_0$ satisfy

$$|x(t)| \le k\, |x(t_0)|\, e^{-\lambda (t - t_0)}, \qquad t \ge t_0 \ge 0 .$$

Then there are a continuously differentiable function $V(t, x)$ on $[0, \infty) \times \{|x| < r_0\}$ and constants $c_1, c_2, c_3, c_4 > 0$ such that

$$c_1 |x|^2 \le V(t, x) \le c_2 |x|^2, \qquad \frac{\partial V}{\partial t} + \frac{\partial V}{\partial x} f(t, x) \le -c_3 |x|^2, \qquad \left| \frac{\partial V}{\partial x} \right| \le c_4 |x| .$$

If the system is autonomous, $V$ can be chosen independent of $t$. If $r = \infty$ and the bounds on the solutions and on the Jacobian hold on all of $\mathbb{R}^n$, then $V$ is defined on $\mathbb{R}^n$ and the inequalities hold globally.

**Theorem B (uniform asymptotic stability).** Let $\beta$ be of class $\mathcal{KL}$ and $r_0 > 0$ with $\beta(r_0, 0) < r$, and let every solution with $|x(t_0)| < r_0$ satisfy

$$|x(t)| \le \beta(|x(t_0)|, t - t_0), \qquad t \ge t_0 \ge 0 .$$

Then there are a continuously differentiable $V(t, x)$ on $[0, \infty) \times \{|x| < r_0\}$ and class $\mathcal K$ functions $\alpha_1, \alpha_2, \alpha_3, \alpha_4$ on $[0, r_0)$ such that

$$\alpha_1(|x|) \le V(t, x) \le \alpha_2(|x|), \qquad \frac{\partial V}{\partial t} + \frac{\partial V}{\partial x} f(t, x) \le -\alpha_3(|x|), \qquad \left| \frac{\partial V}{\partial x} \right| \le \alpha_4(|x|) .$$

If the system is autonomous, $V$ can be chosen independent of $t$.

**Theorem C (the region of attraction).** Let $f$ be locally Lipschitz and autonomous, and let the origin of $\dot x = f(x)$ be asymptotically stable with [region of attraction](/region-of-attraction/) $R_A$. Then there are a smooth positive definite function $V$ and a continuous positive definite function $W$ on $R_A$ with $\frac{\partial V}{\partial x} f(x) \le -W(x)$ on $R_A$, $V(x) \to \infty$ as $x$ approaches the boundary of $R_A$, and $\{x : V(x) \le c\}$ a compact subset of $R_A$ for every $c > 0$. If $R_A = \mathbb{R}^n$, $V$ is radially unbounded.

**Theorem D (linear systems).** For $\dot x = A x$, the origin is exponentially stable if and only if $A$ is Hurwitz, and then for each $Q = Q^T > 0$ the Lyapunov equation $A^T P + P A = -Q$ has the unique solution $P = \int_0^\infty e^{A^T t} Q e^{A t}\, dt > 0$. So $V = x^T P x$ is a quadratic Lyapunov function. This is the case on the [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/) page, and the equation is solved on the [Lyapunov equation](/lyapunov-equation/) page.

Theorems A, B and C are in Khalil (2002, Section 4.7). With the direct method, Theorems A and B are equivalences: a function with the bounds of Theorem A proves exponential stability, and a function with the bounds of Theorem B proves uniform asymptotic stability.

## In plain words

If every solution near an equilibrium goes to it, there is a way to measure the distance to the equilibrium that always goes down along solutions. The proof finds this measure by following each solution for a while and adding up how far it is from the equilibrium along the way. A state whose future solution stays far away for a long time gets a large value; a state that is already close gets a small value. Moving along a solution removes a piece from the start of this sum, so the value goes down.

## Proof

**Proof of Theorem A, autonomous case.** Let $\phi(s; x)$ be the solution with $\phi(0; x) = x$. For $|x| < r_0$, $|\phi(s; x)| \le k |x| e^{-\lambda s} < r$, so the solution stays in $D$. Fix $\delta > 0$ and define

$$V(x) = \int_0^\delta |\phi(s; x)|^2\, ds .$$

*Upper bound.* $V(x) \le \int_0^\delta k^2 e^{-2\lambda s} ds\, |x|^2 = \frac{k^2 (1 - e^{-2\lambda\delta})}{2\lambda} |x|^2 = c_2 |x|^2$.

*Lower bound.* $f(0) = 0$ and $\|\partial f / \partial x\| \le L$ on the ball $D$ give $|f(x)| \le L |x|$. So $\frac{d}{ds} |\phi|^2 = 2 \phi^T f(\phi) \ge -2 L |\phi|^2$, and $|\phi(s; x)|^2 \ge |x|^2 e^{-2 L s}$. Then $V(x) \ge \frac{1 - e^{-2 L \delta}}{2 L} |x|^2 = c_1 |x|^2$.

*Decrease.* By uniqueness, $\phi(s; \phi(h; x)) = \phi(s + h; x)$, so

$$V(\phi(h; x)) = \int_h^{h + \delta} |\phi(s; x)|^2\, ds .$$

The derivative at $h = 0$ is $\dot V(x) = |\phi(\delta; x)|^2 - |x|^2 \le -(1 - k^2 e^{-2\lambda\delta}) |x|^2$. With $\delta = \ln(2 k^2) / (2\lambda)$, which is positive because $k \ge 1$, this gives $c_3 = 1/2$.

*Gradient bound.* Since $f$ is continuously differentiable, $\phi$ is continuously differentiable in $x$, and $\psi(s) = \partial \phi / \partial x\,(s; x)$ solves $\dot \psi = \frac{\partial f}{\partial x}(\phi)\, \psi$ with $\psi(0) = I$. By the [Gronwall inequality](/gronwall-inequality/), $\|\psi(s)\| \le e^{L s}$. Then

$$\left| \frac{\partial V}{\partial x} \right| = \left| \int_0^\delta 2\, \phi^T \psi\, ds \right| \le 2 k |x| \int_0^\delta e^{(L - \lambda) s}\, ds = c_4 |x| .$$

The integrand is continuous in $x$ and the interval is finite, so $V$ is continuously differentiable. $\square$

For the time-varying case, the same steps work with $V(t, x) = \int_t^{t + \delta} |\phi(\tau; t, x)|^2\, d\tau$, where $\phi(\tau; t, x)$ is the solution that starts at $x$ at time $t$; the terms in $\partial V / \partial t$ come from the dependence on the initial time (Khalil 2002, Section 4.7).

**A worked example of Theorem A.** For $\dot x = -x - x^3$ in $\mathbb{R}$, the solution is

$$\phi(s; x)^2 = \frac{x^2 e^{-2s}}{1 + x^2 (1 - e^{-2s})} \le x^2 e^{-2s},$$

so $k = 1$ and $\lambda = 1$. The substitution $u = 1 - e^{-2s}$ gives the integral in closed form:

$$V(x) = \int_0^\delta \phi(s; x)^2\, ds = \frac{1}{2} \ln\left(1 + (1 - e^{-2\delta}) x^2\right) .$$

The proof takes $\delta = \ln(2) / 2$, so $1 - e^{-2\delta} = 1/2$, and $V(x) = \frac{1}{2} \ln(1 + x^2 / 2)$. Along solutions,

$$\dot V = \frac{x}{2 + x^2} (-x - x^3) = -\frac{x^2 (1 + x^2)}{2 + x^2} \le -\frac{1}{2} x^2 ,$$

and $V(x) \le x^2 / 4 = c_2 x^2$, as the proof says. The simpler function $x^2 / 2$, with derivative $-x^2 - x^4$, also works. The construction gives one Lyapunov function, not the simplest one.

**Proof sketch of Theorem B.** With a decay that is slower than exponential, a finite horizon $\delta$ does not give a uniform decrease, so the integral runs to infinity, with a weight $G$ that removes the small values:

$$V(x) = \int_0^\infty G\left(|\phi(s; x)|^2\right) ds .$$

Massera's lemma gives a continuously differentiable class $\mathcal K$ function $G$, with $G'$ also of class $\mathcal K$, such that $\int_0^\infty G(\beta(r_0, s)^2)\, ds$ and $\int_0^\infty G'(\beta(r_0, s)^2)\, \beta(r_0, s)\, e^{L s}\, ds$ are finite (Massera 1949, section 12). Then:

- $V(x) \le \int_0^\infty G(\beta(|x|, s)^2)\, ds = \alpha_2(|x|)$;
- $V(\phi(h; x)) = \int_h^\infty G(|\phi(s; x)|^2)\, ds$, so $\dot V(x) = -G(|x|^2) = -\alpha_3(|x|)$;
- $|\phi(s; x)| \ge |x| e^{-L s}$ gives $V(x) \ge \int_0^1 G(|x|^2 e^{-2 L s})\, ds \ge G(|x|^2 e^{-2L}) = \alpha_1(|x|)$;
- the bound $\|\psi(s)\| \le e^{L s}$ on the sensitivity, with the second finite integral, gives $\alpha_4$.

The time-varying case is the same with the initial time $t$ as a parameter (Khalil 2002, Section 4.7). $\square$

**A worked example of Theorem B.** For $\dot x = -x^3$, the solution is $\phi(s; x) = x / \sqrt{1 + 2 x^2 s}$. The origin is asymptotically stable with $\beta(r, s) = r / \sqrt{1 + 2 r^2 s}$, but not exponentially stable. With $G(u) = u$, the integral $\int_0^\infty x^2 / (1 + 2x^2 s)\, ds$ diverges. With $G(u) = u^2$,

$$V(x) = \int_0^\infty \frac{x^4}{(1 + 2 x^2 s)^2}\, ds = \frac{x^2}{2},$$

and $\dot V = x \cdot (-x^3) = -x^4 = -G(x^2)$, as the proof says.

**On Theorem C.** The construction is longer than the one above, because $V$ must grow without bound near the boundary of $R_A$, and it is not repeated here. Khalil (2002, Section 4.7) states the theorem.

## Consequences

**The converse of the indirect method.** Let $f$ be continuously differentiable with $f(0) = 0$ and $A = \partial f / \partial x\,(0)$. If the origin of $\dot x = f(x)$ is exponentially stable, then $A$ is Hurwitz. Proof: $\phi(s; \varepsilon v) / \varepsilon \to e^{A s} v$ as $\varepsilon \to 0$, and $|\phi(s; \varepsilon v)| \le k \varepsilon |v| e^{-\lambda s}$, so $|e^{A s} v| \le k |v| e^{-\lambda s}$ for every $v$. With the [indirect method](/lyapunov-indirect-method/), exponential stability of a $C^1$ system is the same as a Hurwitz linearization. For $\dot x = -x^3$ the linearization is $0$, which is why its origin is not exponentially stable.

**Robustness to vanishing perturbations.** Let the origin of $\dot x = f(t, x)$ be exponentially stable, with $V$ from Theorem A, and let $g(t, x)$ satisfy $|g(t, x)| \le \gamma |x|$. For the perturbed system $\dot x = f(t, x) + g(t, x)$,

$$\dot V \le -c_3 |x|^2 + c_4 \gamma |x|^2 .$$

If $\gamma < c_3 / c_4$, the origin is still exponentially stable, and $|x(t)| \le \sqrt{c_2 / c_1}\, |x(t_0)|\, e^{-(c_3 - \gamma c_4)(t - t_0) / (2 c_2)}$. The gradient bound $c_4$ is what makes this work, and only the converse theorem supplies it when one knows the exponential bound on the solutions but has no Lyapunov function at hand.

**Lyapunov functions are a complete tool.** The theorems show that a search for a Lyapunov function is not a weaker method than stability itself: if the property holds, a certificate of the right form exists. Many results are proved this way. A stability property is turned into a Lyapunov function, and the function is used for a new system. [Input-to-state stability](/input-to-state-stability/), for example, is equivalent to the existence of an ISS Lyapunov function (Sontag and Wang 1995).

**Rule of thumb, not a theorem.** A failed search for a quadratic, polynomial or [sum-of-squares](/sum-of-squares-programming/) Lyapunov function does not show that the equilibrium is not asymptotically stable. The converse theorems give a continuously differentiable function, not a function in the class that a computer searches. Raising the degree of the search often helps in practice, but this is experience, not a guarantee (see the counterexample below).

## Tightness

**The theorems give existence, not a formula.** The constructions need every solution of the system, which one does not have in general. A restricted class can be too small: the system

$$\dot x = -x + x y, \qquad \dot y = -y$$

has a globally asymptotically stable origin, proved by $V(x, y) = \ln(1 + x^2) + y^2$, but it has no polynomial Lyapunov function of any degree (Ahmadi, Krstic and Parrilo 2011, Theorem 1.1). The solutions are $x(t) = x(0)\, e^{y(0)(1 - e^{-t}) - t}$, $y(t) = y(0) e^{-t}$. From $(x(0), y(0)) = (1, k)$, $x(t)$ grows to $e^{k - 1 - \ln k}$ at $t = \ln k$ before it decays. The paper shows that no polynomial can decrease along such long excursions.

**Uniformity is needed for time-varying systems.** For $\dot x = -x / (1 + t)$, the solution is $x(t) = x(t_0) (1 + t_0) / (1 + t)$. Every solution goes to $0$, so the origin is globally asymptotically stable, but the time to halve $|x|$ is $1 + t_0$, which grows without bound with $t_0$. The origin is not uniformly asymptotically stable. A function with the bounds of Theorem B would prove uniform asymptotic stability by the direct method, so no such function exists here.

**Global quadratic bounds need the global Jacobian bound.** In the example $\dot x = -x - x^3$, the solutions satisfy the global exponential bound, but the Jacobian $-1 - 3x^2$ is not bounded on $\mathbb{R}$. The constructed $V(x) = \frac{1}{2}\ln(1 + x^2/2)$ grows like $\ln |x|$, so it has no global quadratic lower bound. Theorem A gives the bounds only on bounded sets here, as its hypothesis says.

**Smoothness of $f$.** Theorems A and B as stated need a continuously differentiable $f$. Kurzweil (1956) showed that for asymptotic stability a smooth Lyapunov function exists even when $f$ is only continuous. For systems with inputs, the analogous question for [control Lyapunov functions](/control-lyapunov-function/) has a different answer: an asymptotically controllable system has a continuous control Lyapunov function (Sontag 1983), but in general not a smooth one.

## History

Lyapunov's monograph of 1892 already contained a converse theorem (Kellett 2015). The first converse theorem for asymptotic stability of nonlinear systems is due to Massera (1949), for autonomous and periodic systems; his lemma on the weight $G$ is the core of the proof of Theorem B, and he left the general time-varying case open. Kurzweil (1956) proved the existence of smooth Lyapunov functions for asymptotic stability when the right-hand side is only continuous. The extensions to uniform asymptotic stability of time-varying systems, to the region of attraction and to systems with inputs followed. Kellett (2015) reviews the classical converse theorems, and Khalil (2002, Section 4.7) gives the forms of Theorems A, B and C that are used in control.

## References
