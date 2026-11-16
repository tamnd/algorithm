---
title: Pure pursuit steers along the arc through the goal point and converges on a straight path
proves: [correctness]
status: full
---

Line numbers refer to the pseudocode on the [pure pursuit](/pure-pursuit/) page. The vehicle is the rear-axle [kinematic bicycle model](/kinematic-bicycle-model/): $x' = v\cos\theta$, $y' = v\sin\theta$, $\theta' = (v/L)\tan\delta$. Pure pursuit is a heuristic for path tracking: it does not minimize a cost, and nothing guarantees that it tracks every path. This proof shows three things that do hold. Lemma 1 and Lemma 2 say that lines L3 to L5 do what the page says. Theorem 1 gives the local behavior on a straight path, and Theorem 2 shows that a circle is tracked with zero error.

**Lemma 1 (the arc through the goal point).** Let the goal point have coordinates $(x_g, y_g)$ in the vehicle frame of line L3, with $D^2 = x_g^2 + y_g^2 > 0$. The circle that passes through the rear axle, is tangent to the heading there and passes through the goal point has signed curvature $\kappa = 2y_g/D^2$. If $y_g = 0$ and $x_g > 0$, the arc is the straight line, with $\kappa = 0$.

*Proof.* In the vehicle frame the rear axle is the origin and the heading is the $x$ axis. A circle tangent to the $x$ axis at the origin has its center at $(0, r)$ for a signed radius $r$, with $r > 0$ for a left turn. The goal point is on it when $x_g^2 + (y_g - r)^2 = r^2$, that is $x_g^2 + y_g^2 = 2 r y_g$. If $y_g \ne 0$, then $r = D^2/(2y_g)$ and $\kappa = 1/r = 2y_g/D^2$. If $y_g = 0$, no circle of finite radius passes through $(x_g, 0)$ with $x_g \ne 0$, and the line $y = 0$ does. $\square$

When the goal point is at the lookahead distance, $D = \ell_d$, and with $\alpha$ the angle of the goal point seen from the heading, $y_g = \ell_d\sin\alpha$, so $\kappa = 2\sin\alpha/\ell_d$, the form of Coulter's report. At the end of the path the goal point can be closer than $\ell_d$; the code uses $D$, so Lemma 1 still holds.

**Lemma 2 (the steering angle).** With $\delta = \arctan(\kappa L)$ held constant, the rear axle moves on a circle of curvature $\kappa$.

*Proof.* The curvature of the rear axle path is $\theta'/|(x', y')| = (v/L)\tan\delta / |v| = \tan(\delta)/L$ for $v > 0$, which is $\kappa$ when $\tan\delta = \kappa L$. $\square$

So, if the steering acted at once and the vehicle were exactly the model, the rear axle would leave each pose along the arc of Lemma 1. The test `test_the_arc_passes_through_the_goal_point` checks Lemma 1 on 2000 random cases, and `test_rk4_follows_the_exact_arc` checks that the integrator of line L7 reproduces the circle of Lemma 2 to $10^{-9}$ m.

**Theorem 1 (local behavior on a straight path).** Let the path be the $x$ axis, let $v > 0$ be constant and let the steering be updated continuously (the limit of lines L6 and L7 as the time step goes to 0). Let $e = y$ be the cross-track error of the rear axle and $\psi = \theta$ the heading error. The linearization of the closed loop at $e = \psi = 0$ is
$$\ddot e + \frac{2v}{\ell_d}\,\dot e + \frac{2v^2}{\ell_d^2}\,e = 0,$$
with natural frequency $\omega_n = \sqrt{2}\,v/\ell_d$ and damping ratio $\zeta = 1/\sqrt{2}$. The origin is locally exponentially stable, with rate $v/\ell_d$, and with $\dot e(0) = 0$ the linear solution is $e(t) = e_0\, e^{-at}(\cos at + \sin at)$, $a = v/\ell_d$.

*Proof.* Near the origin the closest point is $(x, 0)$ and the goal point is $(x + \sqrt{\ell_d^2 - e^2}, 0)$. In the vehicle frame its lateral coordinate is $y_g = -e\cos\psi - \sqrt{\ell_d^2 - e^2}\,\sin\psi$, and $D = \ell_d$. To first order, $y_g = -e - \ell_d\psi$, so line L4 gives $\kappa = -2(e + \ell_d\psi)/\ell_d^2$. Lemma 2 gives $\dot\psi = v\kappa$ exactly, and $\dot e = v\sin\psi \approx v\psi$. Then $\ddot e = v\dot\psi = -(2v^2/\ell_d^2)\,e - (2v/\ell_d)\,\dot e$. The characteristic roots of $r^2 + (2v/\ell_d) r + 2v^2/\ell_d^2$ are $r = (-1 \pm i)\,v/\ell_d$. Both have real part $-v/\ell_d < 0$, so the linearization is exponentially stable, and by the [Jacobian linearization](/jacobian-linearization/) principle the nonlinear origin is locally [exponentially stable](/exponential-stability/). Matching $\omega_n^2 = 2v^2/\ell_d^2$ and $2\zeta\omega_n = 2v/\ell_d$ gives the stated values. The general solution is $e^{-at}(A\cos at + B\sin at)$; $e(0) = e_0$ gives $A = e_0$, and $\dot e(0) = a(B - A) = 0$ gives $B = e_0$. $\square$

The test `test_small_error_matches_the_linear_closed_form` runs the code with $v = 5$ m/s, $\ell_d = 5$ m, $e_0 = 1$ mm and a time step of 1 ms, and finds the simulated error within $0.1\%$ of $e_0$ of the formula for 6 s. The residual comes from the zero-order hold of line L6. The theorem is local. With a steering limit, a large heading error, or a path with corners, the closed loop is not covered by it.

**Theorem 2 (a circle is tracked exactly).** Let the path be a circle of radius $R$ with $\ell_d < 2R$, and let the rear axle be on the circle with the heading of the circle, driving forward. Then line L5 returns $\delta = \arctan(L/R)$, and the vehicle stays on the circle.

*Proof.* The goal point is on the circle, at distance $\ell_d$ ahead, so it exists because $\ell_d < 2R$. The path circle passes through the rear axle, is tangent to the heading there and passes through the goal point. By the uniqueness in Lemma 1 it is the arc of line L4, so $\kappa = 1/R$ with the sign of the turn, and by Lemma 2 the vehicle moves on it. Its pose then stays on the circle with the same heading, so the same argument holds at every later time. $\square$

The test `test_tracks_a_circle_exactly` drives 25 m on a polyline of 4000 chords around a circle of radius 10 m and finds a radial error below $10^{-5}$ m and a steering angle within $10^{-5}$ rad of $\arctan(L/R) = 0.2450$ rad.

**What is not proved.** Pure pursuit has no global guarantee. A steering limit can saturate line L5, a corner of the path can make the goal point jump, and a vehicle far from the path can choose a goal point behind a bend. The choice of $\ell_d$ is a tuning decision, not a result; see the page.
