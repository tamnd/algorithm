---
tag: QDN400
kind: theorem
slug: lqg-guaranteed-margins-counterexample
name: LQG has no guaranteed margins
aliases:
- Doyle's LQG counterexample
area: control/optimal-and-predictive-control
level: advanced
summary: An example of Doyle in 1978 shows that LQG loops can have arbitrarily small gain margin, unlike LQR loops.
history:
  year: 1978
  people: [John C. Doyle]
  note: "Doyle (1978) gave a plant with two states for which the LQG loop loses stability under input gains arbitrarily close to 1 when the weights grow."
prereqs: [lqg-control, lqr-stability-margins, gain-margin, routh-hurwitz-criterion]
see_also: [loop-transfer-recovery, phase-margin, kalman-bucy-filter, infinite-horizon-lqr, separation-principle, h-infinity-control-problem, model-uncertainty, sensitivity-function]
sources:
  - paper: doi:10.1109/TAC.1978.1101812
    title: John C. Doyle, Guaranteed margins for LQG regulators, IEEE Transactions on Automatic Control 23(4), 756-757, 1978
    locator: the example with two states and weights along a common direction, whose LQG loop has a gain margin that goes to zero
  - paper: doi:10.1109/TAC.1979.1102095
    title: John C. Doyle and Gunter Stein, Robustness with observers, IEEE Transactions on Automatic Control 24(4), 607-611, 1979
    locator: the loss of the state feedback robustness when an observer is added, and its recovery for minimum phase plants
---

This page is a counterexample, not a positive result. A continuous-time [LQR](/infinite-horizon-lqr/) loop with the full state has guaranteed margins: every input gain in $[1/2, \infty)$ and every phase lag below 60 degrees keep the closed loop Hurwitz ([LQR stability margins](/lqr-stability-margins/)). One could hope that an [LQG](/lqg-control/) loop, which applies the same gain to a Kalman-Bucy estimate, keeps some margin of this kind. Doyle (1978) showed that it does not. He gave a plant with two states for which the LQG loop becomes unstable under input gains arbitrarily close to 1 as the weights grow. So no positive margin holds for all LQG designs.

## Statement

**The claim that fails.** There are numbers $g_- < 1 < g_+$ such that, for every plant $(A, B, C)$ and all weights $Q, R, W, V$ that satisfy the LQG assumptions, the LQG closed loop stays Hurwitz when a real gain $m \in [g_-, g_+]$ multiplies the plant input. For LQR with the full state the claim is true with $g_- = 1/2$ and $g_+ = \infty$.

**The counterexample.** Take

$$A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad h = \begin{bmatrix} 1 \\ 1 \end{bmatrix},$$

with $Q = q\, h h^T$, $W = \sigma\, h h^T$, $R = V = 1$ and $q, \sigma > 0$. So the cost weights the output $h^T x = x_1 + x_2$, and the process noise enters along $h$. Put

$$f = 2 + \sqrt{4 + q}, \qquad d = 2 + \sqrt{4 + \sigma}.$$

**Theorem (Doyle 1978).**

1. The LQG gains are $K = f \begin{bmatrix} 1 & 1 \end{bmatrix}$ and $L_o = d \begin{bmatrix} 1 \\ 1 \end{bmatrix}$.
2. With the plant input multiplied by $m$, the closed-loop characteristic polynomial is
$$\chi_m(s) = s^4 + a_1 s^3 + a_2 s^2 + \left(a_1 + 2 (m - 1) d f\right) s + 1 - (m - 1) d f,$$
with $a_1 = d + f - 4$ and $a_2 = 6 - 2d - 2f + d f$.
3. If the closed loop is Hurwitz, then
$$1 - \frac{d + f - 4}{2 d f} < m < 1 + \frac{1}{d f}.$$
Both bounds tend to 1 as $q$ and $\sigma$ go to infinity together. So for every $\varepsilon > 0$ there are weights for which the gain margin is inside $(1 - \varepsilon, 1 + \varepsilon)$, and the claim fails.
4. For $q = \sigma = 60$, $K = \begin{bmatrix} 10 & 10 \end{bmatrix}$, $L_o = \begin{bmatrix} 10 \\ 10 \end{bmatrix}$, and the closed loop is Hurwitz exactly for
$$\frac{97 - 8\sqrt{85}}{25} < m < 1.01, \qquad \text{that is } 0.9297 < m < 1.01.$$

## In plain words

When a controller can measure the whole state of a machine, the best quadratic controller is very tolerant: the motor can be twice as strong as assumed, or half as strong, and the loop still settles. When the controller must estimate the state from a sensor, the best controller for the noise model can lose this tolerance completely. Doyle built a small machine with two unstable modes where the cost and the noise both point along the same direction. As both become large, the controller and the estimator become very aggressive and cancel each other in a delicate way. Then a motor that is one percent stronger than assumed already makes the loop unstable.

## Proof

**Regulator gain.** Look for the CARE solution in the form $P = f \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$, so that $K = B^T P = f \begin{bmatrix} 1 & 1 \end{bmatrix}$ and $P B = f h$. Then

$$A^T P + P A = f \begin{bmatrix} 4 & 4 \\ 4 & 4 \end{bmatrix} = 4 f\, h h^T, \qquad P B B^T P = f^2 h h^T,$$

and the CARE $A^T P + P A - P B B^T P + q h h^T = 0$ reduces to the scalar equation $f^2 - 4 f - q = 0$, whose positive root is $f = 2 + \sqrt{4 + q}$. $P$ is positive definite since $\det P = f^2 > 0$. The matrix $A - B K = \begin{bmatrix} 1 & 1 \\ -f & 1 - f \end{bmatrix}$ has the characteristic polynomial $\Delta_K(s) = s^2 + (f - 2) s + 1$, which is Hurwitz because $f > 2$. So $P$ is the stabilizing solution, and it is unique.

**Filter gain.** The filter equation $A S + S A^T - S C^T C S + \sigma h h^T = 0$ is the CARE for the dual data $(A^T, C^T, \sigma h h^T, 1)$. Let $J = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$. Then $J A^T J = A$, $J C^T = B$ and $J h = h$, so the dual problem is the regulator problem above with $q$ replaced by $\sigma$, written in swapped coordinates. Hence $S = d\, J \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix} J = d \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}$, $L_o = S C^T = d\, h$, and $A - L_o C$ has the characteristic polynomial $\Delta_L(s) = s^2 + (d - 2) s + 1$. This proves part 1.

**Closed loop.** The controller is $\dot{\hat x} = A_c \hat x + L_o y$, $u = -K \hat x$ with

$$A_c = A - B K - L_o C = \begin{bmatrix} 1 - d & 1 \\ -f - d & 1 - f \end{bmatrix}.$$

With the gain $m$, the plant is $\dot x = A x + m B u$, and the closed-loop matrix is $\begin{bmatrix} A & -m B K \\ L_o C & A_c \end{bmatrix}$. By the Schur complement and the matrix determinant lemma, its characteristic polynomial is

$$\chi_m(s) = \Delta(s)\, \Delta_c(s) + m\, n_G(s)\, n_C(s),$$

where $\Delta(s) = (s - 1)^2 = \det(sI - A)$, $\Delta_c(s) = \det(sI - A_c)$, $C\, \mathrm{adj}(sI - A) B = n_G(s) = 1$ and $n_C(s) = K\, \mathrm{adj}(sI - A_c) L_o$. Here

$$\mathrm{adj}(sI - A_c) = \begin{bmatrix} s - 1 + f & 1 \\ -(f + d) & s - 1 + d \end{bmatrix},$$

and $K\, \mathrm{adj}(sI - A_c) L_o = d f$ times the sum of the four entries, so $n_C(s) = d f (2 s - 1)$. At $m = 1$ the [separation principle](/separation-principle/) gives $\chi_1 = \Delta_K \Delta_L$. Subtract the two expressions:

$$\chi_m(s) = \Delta_K(s) \Delta_L(s) + (m - 1)\, d f\, (2 s - 1).$$

Expand $\Delta_K \Delta_L = s^4 + (d + f - 4) s^3 + (6 - 2d - 2f + d f) s^2 + (d + f - 4) s + 1$. This proves part 2.

**The interval shrinks.** A Hurwitz polynomial with leading coefficient 1 has all coefficients positive. The coefficient of $s$ gives $a_1 + 2 (m - 1) d f > 0$, and the constant gives $1 - (m - 1) d f > 0$. These are the two bounds of part 3. As $q, \sigma \to \infty$, both $d$ and $f$ go to infinity, $1 / (d f) \to 0$ and $(d + f - 4)/(2 d f) < 1/(2f) + 1/(2d) \to 0$. This proves part 3.

**The numbers for $q = \sigma = 60$.** Here $\sqrt{64} = 8$, so $d = f = 10$, $a_1 = 16$, $a_2 = 66$, and with $e = m - 1$,

$$\chi_m(s) = s^4 + 16 s^3 + 66 s^2 + (16 + 200 e) s + (1 - 100 e).$$

The [Routh-Hurwitz](/routh-hurwitz-criterion/) conditions for $s^4 + a_1 s^3 + a_2 s^2 + a_3 s + a_4$ are $a_1, a_3, a_4 > 0$, $a_1 a_2 - a_3 > 0$ and $a_3 (a_1 a_2 - a_3) - a_1^2 a_4 > 0$. They give $e > -0.08$, $e < 0.01$, $e < 5.2$ and

$$(16 + 200 e)(1040 - 200 e) - 256 (1 - 100 e) = 16 \left(1024 + 14400 e - 2500 e^2\right) > 0.$$

The roots of $2500 e^2 - 14400 e - 1024$ are $e = (72 \pm 8\sqrt{85})/25$, that is $-0.0703$ and $5.83$. The intersection of all the conditions is $(72 - 8\sqrt{85})/25 < e < 0.01$, which is part 4. $\square$

## Consequences

- **The LQR loop of the same design is robust.** With the full state, the loop $K (sI - A)^{-1} B = f s / (s - 1)^2$ closed with a gain $k$ has the polynomial $s^2 + (k f - 2) s + 1$, so it is Hurwitz for every $k > 2/f$. For $f = 10$ this is $k > 0.2$, which contains $[1/2, \infty)$, and the phase margin is about 78.5 degrees. Only the estimator removes the margin.
- **Phase margin goes too.** For $q = \sigma = 60$ the LQG loop gain crosses the unit circle at $\omega \approx 0.102$ rad/s about 0.92 degrees away from $-1$, so a phase lag of 1 degree at the input already makes the closed loop unstable. For $q = \sigma = 1000$ the gain interval is $(0.97296, 1.00088)$ and the phase margin is about 0.095 degrees.
- **Check every LQG design.** Optimality for the noise model says nothing about robustness. The margins of the actual loop must be computed at the plant input and at the output.
- **Loop transfer recovery.** Doyle and Stein (1979) showed that the margins come back for plants that are square and minimum phase when fictitious noise is added along the input matrix $B$. Here the noise enters along $h$, not along $B$, and the filter becomes fast in a direction that does not recover the LQR loop. See [loop transfer recovery](/loop-transfer-recovery/).
- **Robust synthesis.** The example was one of the reasons for frequency domain robustness tools such as [H-infinity control](/h-infinity-control-problem/), which take a [model uncertainty](/model-uncertainty/) description into the design.

## Tightness

The bounds of part 3 come only from the signs of two coefficients, so they are necessary, not sufficient. The exact interval needs the full Routh test, as in part 4: the lower end $0.9297$ is a little above the necessary bound $0.92$, and the upper end $1.01$ is exact. For $q = \sigma = 60$ and for $q = \sigma = 1000$ the upper end is the bound $1 + 1/(d f)$ itself: at that gain the constant coefficient becomes 0, and a real root crosses the origin.

The example does not show that every LQG loop has a small margin. For the double integrator with $Q = I$, $W = I$ and $R = V = 1$, the LQG loop is Hurwitz for all gains in $(0, 4)$ (see [LQG control](/lqg-control/)). It shows that there is no bound that holds for all plants and weights. The limit needs both weights large: if $\sigma$ grows with $q$ fixed, the upper bound $1 + 1/(d f)$ still goes to 1, but the necessary lower bound tends to $1 - 1/(2f)$.

## History

Safonov and Athans (1977) had proved the gain and phase margins of multiloop LQR regulators with the full state, and it was a common belief that LQG regulators share them. Doyle answered in a note of two pages in IEEE Transactions on Automatic Control in 1978 with the plant on this page and weights along a common direction. Doyle and Stein (1979) then showed how to recover the LQR margins for minimum phase plants with fictitious noise at the input, and Doyle and Stein (1981) put the robustness question into the frequency domain with singular values, which led to loop shaping and H-infinity methods.

## References
