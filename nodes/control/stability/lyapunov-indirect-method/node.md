---
tag: 2KCKMV
kind: theorem
slug: lyapunov-indirect-method
name: Lyapunov's indirect method
aliases:
- Lyapunov's first method
- linearization stability theorem
area: control/stability
level: core
summary: An equilibrium is locally exponentially stable if its linearization is Hurwitz, and unstable if the linearization has an eigenvalue with positive real part. Otherwise the test is silent.
prereqs: [lyapunov-direct-method, lyapunov-theorem-for-linear-systems, jacobian-linearization]
see_also: [jacobian-linearization, lyapunov-direct-method, lyapunov-theorem-for-linear-systems, hurwitz-matrix, exponential-stability, equilibrium-point, region-of-attraction, converse-lyapunov-theorem]
sources:
  - paper: doi:10.1080/00207179208934253
    title: "A. M. Lyapunov, The general problem of the stability of motion, translated by A. T. Fuller, International Journal of Control 55(3), 531-773, 1992"
    locator: the first method and the stability of motion in the first approximation
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.3, Linear Systems and Linearization (the theorem and its proof with a quadratic Lyapunov function and a Chetaev function), Section 4.1 (the instability theorem of Chetaev), and Chapter 8 (the center manifold theorem for the critical case)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, second edition, Princeton University Press, 2021
    locator: Chapter 5, Dynamic Behavior (stability of equilibria by linear approximation)
---

Lyapunov's indirect method decides the local stability of an equilibrium of a nonlinear differential equation from its linearization. Compute the Jacobian matrix $A$ of the right-hand side at the equilibrium. If $A$ is [Hurwitz](/hurwitz-matrix/), with every eigenvalue in the open left half plane, the equilibrium is locally [exponentially stable](/exponential-stability/). If $A$ has an eigenvalue with positive real part, the equilibrium is unstable. If the eigenvalues with the largest real part lie on the imaginary axis, the test says nothing, and the nonlinear terms decide. The method justifies the everyday practice of control engineers, who design with a linear model obtained by [Jacobian linearization](/jacobian-linearization/). The proof uses the [direct method](/lyapunov-direct-method/) with a quadratic function from the [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/).

## Statement

**Setting.** $\dot x = f(x)$, where $f : D \to \mathbb{R}^n$ is continuously differentiable on a domain $D$ that contains the origin, and $f(0) = 0$. Let

$$A = \frac{\partial f}{\partial x}(0)$$

be the Jacobian at the origin, and $\dot x = A x$ the linearization. A continuously differentiable $f$ is locally Lipschitz, so solutions exist and are unique.

**Theorem.**

(a) If $A$ is Hurwitz, that is $\operatorname{Re} \lambda < 0$ for every eigenvalue $\lambda$ of $A$, then the origin is exponentially stable, and so asymptotically stable.

(b) If $\operatorname{Re} \lambda > 0$ for at least one eigenvalue $\lambda$ of $A$, then the origin is unstable.

(c) If $\max_i \operatorname{Re} \lambda_i = 0$, the eigenvalues of $A$ do not decide: there are systems with the same $A$ whose origin is asymptotically stable, Lyapunov stable but not asymptotically stable, or unstable.

**Converse of (a).** If the origin is exponentially stable, then $A$ is Hurwitz (Khalil 2002, Chapter 4; the proof uses a [converse Lyapunov theorem](/converse-lyapunov-theorem/)). So for continuously differentiable $f$, local exponential stability and a Hurwitz linearization are the same property.

## In plain words

Near a resting point, a smooth nonlinear system looks almost like its straight-line approximation, because the curved terms become very small compared with the straight ones. If the approximation pulls every nearby state back to the resting point, the small curved terms are too weak to stop it, and the real system also comes back, fast. If the approximation pushes some state away, the curved terms cannot hold it, and the real system also moves away. There is one case where this reasoning fails: the approximation neither pulls nor pushes in some direction, and only holds the state level, as a frictionless swing does. Then the small curved terms are the only force in that direction, and they alone decide what happens.

## Proof

**The remainder.** Write $f(x) = A x + g(x)$. Since $f$ is continuously differentiable,

$$g(x) = \int_0^1 \left(\frac{\partial f}{\partial x}(s x) - A\right) x\, ds , \qquad\text{so}\qquad |g(x)| \le \gamma(|x|)\, |x| ,$$

where $\gamma(\rho) = \max_{|y| \le \rho} \|\partial f / \partial x\,(y) - A\|$ is nondecreasing and tends to $0$ as $\rho \to 0$. All norms below are Euclidean.

**Part (a).** Let $A$ be Hurwitz. By the Lyapunov theorem for linear systems there is a unique $P > 0$ with $A^T P + P A = -I$. Take $V(x) = x^T P x$. Then

$$\dot V = x^T (A^T P + P A) x + 2 x^T P g(x) \le -|x|^2 + 2 \|P\|\, \gamma(|x|)\, |x|^2 .$$

Choose $r > 0$ with $2 \|P\| \gamma(r) \le 1/2$ and with the ball $|x| < r$ in $D$. On that ball $\dot V \le -\tfrac12 |x|^2$, and $\lambda_{\min}(P) |x|^2 \le V(x) \le \lambda_{\max}(P) |x|^2$. The Lyapunov test on [exponential stability](/exponential-stability/), with $a = 2$, $k_1 = \lambda_{\min}(P)$, $k_2 = \lambda_{\max}(P)$ and $k_3 = 1/2$, gives

$$|x(t)| \le \sqrt{\lambda_{\max}(P) / \lambda_{\min}(P)}\; e^{-t / (4 \lambda_{\max}(P))}\, |x(0)|$$

for all $x(0)$ in a smaller ball. $\blacksquare$

**Part (b).** Let $\sigma = \min\{\operatorname{Re} \lambda : \lambda \text{ an eigenvalue of } A,\ \operatorname{Re} \lambda > 0\}$ and fix $\mu \in (0, \sigma)$. The matrix $B = A - \mu I$ has the eigenvalues $\lambda - \mu$. None of them is on the imaginary axis, because no eigenvalue of $A$ has real part in $(0, \sigma)$, and at least one is in the open right half plane.

So there is a real invertible $T$ with $T^{-1} B T = \operatorname{diag}(B_1, B_2)$, where all eigenvalues of $B_1$ have positive real part and $B_2$ is Hurwitz ($B_2$ may be empty), for example from the real [Jordan normal form](/jordan-normal-form/). Since $-B_1$ and $B_2$ are Hurwitz, the Lyapunov theorem for linear systems gives $P_1 > 0$ and $P_2 > 0$ with

$$B_1^T P_1 + P_1 B_1 = I , \qquad B_2^T P_2 + P_2 B_2 = -I .$$

In the coordinates $z = T^{-1} x = (z_1, z_2)$ the system is $\dot z = \operatorname{diag}(B_1 + \mu I, B_2 + \mu I)\, z + h(z)$ with $h(z) = T^{-1} g(T z)$, so $|h(z)| \le \tilde\gamma(|z|)\, |z|$ with $\tilde\gamma(\rho) \to 0$ as $\rho \to 0$. Take

$$W(z) = z_1^T P_1 z_1 - z_2^T P_2 z_2 .$$

With $S = \operatorname{diag}(P_1, -P_2)$ a direct computation gives

$$\dot W = |z_1|^2 + |z_2|^2 + 2 \mu W(z) + 2 z^T S\, h(z) \ge |z|^2 + 2 \mu W(z) - 2 \|S\|\, \tilde\gamma(|z|)\, |z|^2 .$$

Choose $r > 0$ with $2 \|S\| \tilde\gamma(r) \le 1/2$. On the set $U = \{|z| < r,\ W(z) > 0\}$ this gives $\dot W \ge \tfrac12 |z|^2 > 0$.

Now the instability argument of Chetaev. The set $U$ contains points arbitrarily close to $0$, for example $z = (\varepsilon e_1, 0)$. Fix $r' < r$, and let $z(0) \in U$ with $|z(0)| < r'$ and $W(z(0)) = a > 0$. While the solution stays in the ball $|z| \le r'$, it stays in $U$ and $W(z(t)) \ge a$, because $W$ increases on $U$. The set $K = \{|z| \le r',\ W(z) \ge a\}$ is compact and does not contain $0$, so $\dot W \ge c$ on $K$ for $c = \min_K \tfrac12 |z|^2 > 0$. Then $W(z(t)) \ge a + c t$. But $W$ is bounded on the ball, so the solution must leave the ball $|z| \le r'$ in finite time. Since $z(0)$ can be taken arbitrarily close to $0$, the origin is unstable in the $z$ coordinates, and so in the $x$ coordinates, because $T$ is a fixed invertible linear map. $\blacksquare$

**Part (c).** See the examples under Tightness.

The proof of (a) is the one of Khalil (2002, Section 4.3). The shift by $\mu$ in (b) handles eigenvalues on the imaginary axis next to eigenvalues in the right half plane.

## Consequences

**Examples with numbers.**

- *Damped pendulum.* $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 - b x_2$ with $b = 1$. At the bottom $(0, 0)$ the Jacobian is $\begin{bmatrix} 0 & 1 \\ -1 & -1 \end{bmatrix}$, with the eigenvalues $(-1 \pm i \sqrt 3)/2$: locally exponentially stable. At the top $(\pi, 0)$ it is $\begin{bmatrix} 0 & 1 \\ 1 & -1 \end{bmatrix}$, with the eigenvalues $(-1 \pm \sqrt 5)/2 = 0.618$ and $-1.618$: unstable by part (b). The energy function of the [direct method](/lyapunov-direct-method/) proves only Lyapunov stability of the bottom; the indirect method gives more here, with no search for a function.
- *Van der Pol in reverse time.* $\dot x_1 = -x_2$, $\dot x_2 = x_1 + (x_1^2 - 1) x_2$ has the Jacobian $A = \begin{bmatrix} 0 & -1 \\ 1 & -1 \end{bmatrix}$ at the origin, with trace $-1$ and determinant $1$, so $A$ is Hurwitz. With $Q = I$ the Lyapunov equation gives $P = \begin{bmatrix} 3/2 & -1/2 \\ -1/2 & 1 \end{bmatrix}$. The level sets of $x^T P x$ that lie in the set where $\dot V < 0$ estimate the [region of attraction](/region-of-attraction/), which here is bounded by an unstable [limit cycle](/limit-cycle/).
- *Local only.* $\dot x = -x + x^2$ has $A = -1$: exponentially stable, but the solution from $x(0) = 2$ escapes to infinity at $t = \ln 2$. The method never says anything global.

**Design by linearization.** If a controller makes the closed-loop Jacobian Hurwitz, for example by [state feedback](/state-feedback/) with the poles placed by the [pole placement theorem](/pole-placement-theorem/), part (a) proves that the nonlinear closed loop is locally exponentially stable. This is why a linear design around an [equilibrium point](/equilibrium-point/) is sound for small deviations.

**Robustness.** Part (a) also shows that local exponential stability survives small changes of $f$ that keep $f(0) = 0$ and change the Jacobian a little, since the set of Hurwitz matrices is open. Part (b) survives in the same way. Neither holds in the critical case (c).

**Hyperbolic and critical equilibria.** An equilibrium whose Jacobian has no eigenvalue on the imaginary axis is called hyperbolic, and for it the method always decides. The critical case, with eigenvalues on the axis and none to the right, is treated by center manifold theory, which reduces the question to a lower-dimensional system on the center manifold (Khalil 2002, Chapter 8).

**Discrete time.** For $x_{k+1} = F(x_k)$ with $F(0) = 0$ and Jacobian $A$ at $0$: if the [spectral radius](/spectral-radius/) of $A$ is less than 1, the origin is exponentially stable; if some eigenvalue has modulus greater than 1, it is unstable. The proof is the same, with $A^T P A - P = -I$.

## Tightness

**The critical case gives every answer.** For $\dot x = a x^3$ the Jacobian at $0$ is $A = 0$ for every $a$. With $a = -1$ the origin is asymptotically stable (with $V = x^2$, $\dot V = -2x^4$), with $a = 0$ it is Lyapunov stable and not asymptotically stable, and with $a = 1$ it is unstable, since $x(t) = x_0 / \sqrt{1 - 2 x_0^2 t}$ escapes at $t = 1/(2 x_0^2)$. A case with complex eigenvalues on the axis:

$$\dot x_1 = -x_2 + a x_1 (x_1^2 + x_2^2), \qquad \dot x_2 = x_1 + a x_2 (x_1^2 + x_2^2) .$$

The Jacobian is the rotation $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ with the eigenvalues $\pm i$ for every $a$. In polar coordinates $\dot r = a r^3$ and $\dot \theta = 1$. So the origin is asymptotically stable for $a < 0$, a center for $a = 0$, and unstable for $a > 0$.

**Asymptotic stability with a Jacobian that is not Hurwitz.** Part (a) is sufficient, not necessary, for asymptotic stability: $\dot x = -x^3$ is globally asymptotically stable with $A = 0$. It is necessary for exponential stability, by the converse above, which is why the origin of $\dot x = -x^3$ is not exponentially stable.

**Eigenvalue zero together with a right half plane eigenvalue.** Part (b) needs only one eigenvalue with positive real part, whatever the other eigenvalues are. For $\dot x_1 = x_1$, $\dot x_2 = -x_2^3$ the Jacobian $\operatorname{diag}(1, 0)$ has an eigenvalue on the axis, but the origin is unstable along $x_1$.

**Differentiability is needed.** The method needs a Jacobian at the equilibrium and a remainder that is small compared with $|x|$. The scalar system $\dot x = -x + 2|x|$ has a Lipschitz right-hand side, but no derivative at $0$: the slope is $-3$ on the left and $1$ on the right. The origin is unstable, since $\dot x = x$ for $x > 0$, although solutions from the left side approach it. No single linear model describes both sides, and the direct method must be used instead.

## History

In his thesis of 1892 Lyapunov called the study of stability by the equations of the first approximation, and by series expansions of the solutions, his first method, in contrast to the second method with auxiliary functions. He proved that the first approximation decides stability unless the critical case occurs, in which some characteristic roots have zero real part and none has a positive real part, and he studied some critical cases in detail. The instability theorem of Chetaev from the 1930s later gave the short proof of the instability part that is used above. The textbook proofs by a quadratic Lyapunov function from the Lyapunov equation are standard in control texts since the 1960s.

## References
