---
title: The Stanley law drives the cross-track error to zero on a straight path
proves: [correctness]
status: full
---

Line numbers refer to the pseudocode on the [Stanley controller](/stanley-controller/) page. The vehicle is the kinematic bicycle model with the reference point at the center of the front axle. The front wheels roll with speed $u$ in the direction $\theta + \delta$, and the rear wheels roll along $\theta$, so
$$x_f' = u\cos(\theta + \delta),\quad y_f' = u\sin(\theta + \delta),\quad \theta' = \frac{u}{L}\sin\delta.$$

**Hypotheses.** H1: the model above holds (no tire slip, no actuator delay, the steering is updated continuously). H2: the speed $u > 0$ is constant. H3: the steering does not saturate, $|\psi + \arctan(ke/u)| < \delta_{max} \le \pi/2$, so line L5 does not clip. The gain $k > 0$ is in 1/s. The path is the $x$ axis, except in Theorem 3. Then the closest point of the path to the front axle is $(x_f, 0)$, the cross-track error of line L2 is $e = -y_f$ (positive when the front axle is to the right of the path), and the heading error of line L3 is $\psi = -\theta$.

**Lemma 1 (the error equation).** Under H1 to H3, on the straight path,
$$\dot e = -\frac{k e}{\sqrt{1 + (k e/u)^2}},$$
for every heading $\theta$.

*Proof.* Line L4 gives $\delta = \psi + \arctan(ke/u) = -\theta + \arctan(ke/u)$, so $\theta + \delta = \arctan(ke/u)$. Then $\dot e = -\dot y_f = -u\sin(\arctan(ke/u))$. With $\sin(\arctan z) = z/\sqrt{1 + z^2}$, this is $-u\,(ke/u)/\sqrt{1 + (ke/u)^2}$. $\square$

The heading drops out: the law turns the front wheels to point at the path at the angle $\arctan(ke/u)$, whatever the body does. This is equation (8) of Thrun et al. (2006). The test `test_error_rate_is_independent_of_the_heading` checks the lemma on 3000 random unsaturated states to $10^{-9}$.

**Theorem 1 (the cross-track error).** Under H1 to H3 on the straight path, $e(t)$ keeps its sign, $|e(t)|$ decreases strictly to 0, and with $s = ke/u$ and
$$F(s) = \sqrt{1 + s^2} + \ln\frac{|s|}{1 + \sqrt{1 + s^2}},$$
the solution satisfies $F(s(t)) = F(s(0)) - kt$. Moreover $|e(t)| \le |e(0)|\exp\!\big(-kt/\sqrt{1 + s(0)^2}\big)$, and $|e(t)|$ decays like $e^{-kt}$ as $s \to 0$.

*Proof.* By Lemma 1, $\dot s = -ks/\sqrt{1 + s^2}$. The right side is Lipschitz, and $s = 0$ is an equilibrium, so a solution that starts at $s_0 \ne 0$ never reaches 0 in finite time and keeps its sign; $|s|$ decreases strictly because $s\dot s < 0$. For $s > 0$, separate the variables: $\frac{\sqrt{1 + s^2}}{s}\,ds = -k\,dt$. The derivative of $F$ is $\frac{s}{\sqrt{1+s^2}} + \frac{1}{s} - \frac{s}{\sqrt{1+s^2}\,(1 + \sqrt{1+s^2})}$. With $r = \sqrt{1 + s^2}$, the first and third terms sum to $\frac{s}{1 + r}$, and $\frac1s + \frac{s}{1+r} = \frac{1 + r + s^2}{s(1 + r)} = \frac{r(1 + r)}{s(1+r)} = \frac{r}{s}$. So $F' = \sqrt{1 + s^2}/s$ and $F(s(t)) - F(s_0) = -kt$. For $s < 0$ the equation is odd in $s$, and $F$ depends on $|s|$. Since $|s(t)| \le |s_0|$, $\sqrt{1 + s^2} \le \sqrt{1 + s_0^2}$, so $\frac{d}{dt}|e| \le -k|e|/\sqrt{1 + s_0^2}$, which gives the exponential bound. As $s \to 0$, $F(s) = \ln|s| + 1 - \ln 2 + O(s^2)$, so $|s(t)| = |s_0|\,e^{F(s_0) - 1 + \ln 2 - kt}(1 + o(1))$, which decays like $e^{-kt}$. $\square$

So the error converges for every initial error, at an exponential rate that depends on how large $|ke_0/u|$ is. For a large error, $\dot e \approx -u\,\mathrm{sign}(e)$: the front axle drives straight at the path at nearly full speed. The test `test_continuous_loop_matches_the_implicit_solution` integrates the continuous loop from $e_0 = -2$ m, $\theta_0 = 0.3$ rad with $k = 1$ 1/s and $u = 5$ m/s and finds $kt$ equal to $F(s_0) - F(s(t))$ within $10^{-8}$ s at every step of 10 ms.

**Theorem 2 (the heading and local exponential stability).** Under H1 to H3 on the straight path, $\theta(t) \to 0$. The state $(e, \theta) = (0, 0)$ is locally [exponentially stable](/exponential-stability/), with the eigenvalues $-k$ and $-u/L$ of the linearization.

*Proof.* Let $\varphi(t) = \arctan s(t)$, so $\delta = -(\theta + \varphi)$ and $\dot\theta = -(u/L)\sin(\theta + \varphi)$, with $|\theta + \varphi| = |\delta| < \pi/2$ by H3. By Theorem 1, $|\varphi(t)|$ decreases to 0. Fix $\epsilon > 0$ and a time $T$ with $|\varphi(t)| < \epsilon/2$ for $t \ge T$. When $|\theta| \ge \epsilon$ and $t \ge T$, $\theta + \varphi$ has the sign of $\theta$ and $|\theta + \varphi| \ge \epsilon/2$, so $\frac{d}{dt}|\theta| \le -(u/L)\sin(\epsilon/2) < 0$. So $|\theta|$ falls below $\epsilon$ in finite time and does not leave the interval $[-\epsilon, \epsilon]$ after that. As $\epsilon$ is arbitrary, $\theta \to 0$. For the second claim, linearize at the origin: $\dot s = -ks$ and $\dot\theta = -(u/L)(\theta + s)$. The matrix is triangular with eigenvalues $-k$ and $-u/L$, both negative, so by the [Jacobian linearization](/jacobian-linearization/) principle the origin of the nonlinear loop is locally exponentially stable. $\square$

**Theorem 3 (a circle is an equilibrium).** Let the path be a circle of radius $R > L$, traversed counterclockwise. If the front axle is on the circle and the heading lags the tangent of the circle by $\arcsin(L/R)$, then the law returns $\delta = \arcsin(L/R)$, and the vehicle keeps that relation for all time.

*Proof.* The front axle is on the path, so $e = 0$, $\psi = \arcsin(L/R)$, and line L4 gives $\delta = \psi$. The front wheels then point along the tangent, so the front axle moves along the circle with speed $u$, and the tangent turns at the rate $u/R$. The heading turns at $\dot\theta = (u/L)\sin\delta = u/R$, the same rate, so $\psi$ stays constant and $e$ stays 0. $\square$

The rear axle runs on the circle of radius $\sqrt{R^2 - L^2}$ inside the path. The test `test_circle_is_an_equilibrium` drives 30 m on a polyline of 20000 chords around a circle of radius 20 m and finds the front axle within $10^{-4}$ m of the circle; the steering stays within $4 \cdot 10^{-4}$ rad of $\arcsin(L/R) = 0.1430$ rad, a deviation that comes from the turn of $3.1 \cdot 10^{-4}$ rad between chords.

**What is not proved.** Theorems 1 and 2 need H3. With a steering limit, the law can saturate, and the paper's monotone convergence claim covers only the unsaturated equation. The test `test_converges_with_a_steering_limit` is a measurement, not a proof: from 25 random starts with errors up to 10 m and 1 rad, a limit of 24 degrees, and a held steering of 10 ms, the loop reaches the path within $10^{-6}$ m. At low speed, $ke/u$ is large and the law reduces to steering at the path at a right angle, which is why the softening constant of the page exists. The page does not prove stability on curved paths other than the equilibrium of Theorem 3, nor with dynamics, slip or delay.
