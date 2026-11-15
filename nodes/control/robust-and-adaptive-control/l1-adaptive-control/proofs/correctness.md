---
title: The L1 adaptive law with projection bounds the prediction error by a term of order one over the square root of the adaptation gain
proves: [correctness]
status: full
---

Notation is that of the page. The plant is $\dot x = a_m x + b(u + \theta x)$ with $a_m < 0$, $b \ne 0$ and $|\theta| \le \theta_b$. The predictor is $\dot{\hat x} = a_m\hat x + b(u + \hat\theta x)$, the law is $\dot{\hat\theta} = \Gamma\,\mathrm{Proj}(\hat\theta, y)$ with $y = -\tilde x\,p\,b\,x$, $\tilde x = \hat x - x$, $\tilde\theta = \hat\theta - \theta$ and $p = -1/(2a_m) > 0$. The projection is $\mathrm{Proj}(\hat\theta, y) = y(1 - f(\hat\theta))$ if $f(\hat\theta) > 0$ and $y f'(\hat\theta) > 0$, and $y$ otherwise, with $f(\theta) = (\theta^2 - \theta_b^2)/(\epsilon\theta_b^2)$.

**Claim 1 (the estimate stays in the band).** If $|\hat\theta(0)| \le \theta_b\sqrt{1 + \epsilon}$, then $|\hat\theta(t)| \le \theta_b\sqrt{1 + \epsilon}$ for all $t$.

*Proof.* The bound is the set $f(\hat\theta) \le 1$. Along solutions, $\frac{d}{dt}f(\hat\theta) = f'(\hat\theta)\,\Gamma\,\mathrm{Proj}(\hat\theta, y)$. When $f(\hat\theta) > 0$ and $y f' > 0$, this is $\Gamma f' y (1 - f)$, which is at most $0$ when $f \ge 1$. In the other case, either $f \le 0 < 1$, or $y f' \le 0$ and the derivative is $\Gamma f' y \le 0$. So $f$ cannot increase while $f \ge 1$, and it cannot cross the level $1$ from below. $\square$

**Claim 2 (projection does not increase the parameter error).** If $|\theta| \le \theta_b$, then $\tilde\theta\,(\mathrm{Proj}(\hat\theta, y) - y) \le 0$.

*Proof.* The difference is nonzero only when $f(\hat\theta) > 0$ and $y f'(\hat\theta) > 0$, and then it equals $-f(\hat\theta)\,y$. Here $f(\hat\theta) > 0$ means $|\hat\theta| > \theta_b \ge |\theta|$, and $f' = 2\hat\theta/(\epsilon\theta_b^2)$ has the sign of $\hat\theta$, so $y$ has the sign of $\hat\theta$. Also $\tilde\theta = \hat\theta - \theta$ has the sign of $\hat\theta$, because $|\hat\theta| > |\theta|$. So $\tilde\theta y > 0$ and $\tilde\theta(\mathrm{Proj} - y) = -f\,\tilde\theta y < 0$. $\square$

**Claim 3 (Lyapunov function).** Let $V = p\tilde x^2 + \tilde\theta^2/\Gamma$. Then $\dot V \le -\tilde x^2$.

*Proof.* Subtract the plant from the predictor: $\dot{\tilde x} = a_m\tilde x + b\tilde\theta x$. Since $\theta$ is constant, $\dot{\tilde\theta} = \dot{\hat\theta}$. Then
$$\dot V = 2p\tilde x(a_m\tilde x + b\tilde\theta x) + 2\tilde\theta\,\mathrm{Proj}(\hat\theta, y) = 2pa_m\tilde x^2 + 2\tilde\theta\,p b x\tilde x + 2\tilde\theta y + 2\tilde\theta(\mathrm{Proj} - y).$$
With $y = -\tilde x p b x$ the second and third terms cancel, $2pa_m = -1$, and the last term is at most $0$ by Claim 2. $\square$

**Claim 4 (the bound).** If $\hat x(0) = x(0)$, then for all $t \ge 0$,
$$|\tilde x(t)| \le \sqrt{\frac{\tilde\theta(0)^2}{\Gamma p}} \le \frac{2\theta_b\sqrt{1+\epsilon}}{\sqrt{\Gamma p}}.$$

*Proof.* The solution exists for all $t \ge 0$: by Claim 1, $\hat\theta$ is bounded, and for a given $\hat\theta(t)$ the equations of $x$, $\hat x$ and $u$ are linear with bounded coefficients, so they have no finite escape time. By Claim 3, $p\tilde x(t)^2 \le V(t) \le V(0) = \tilde\theta(0)^2/\Gamma$. For the second form, $|\tilde\theta(0)| \le |\hat\theta(0)| + |\theta| \le \theta_b\sqrt{1 + \epsilon} + \theta_b \le 2\theta_b\sqrt{1+\epsilon}$. $\square$

Claim 4 holds whatever the input $u$ is, so it needs no assumption on the filter. It is the first step of the analysis of Cao and Hovakimyan. Their main theorem, which is not reproved here, adds the condition $\|G\|_{L_1} L < 1$ for $G = H(1 - C)$ and $L = \theta_b$, uses the [small gain theorem](/small-gain-theorem/) to show that the reference system with the true $\theta$ in the control law is bounded in the $L_\infty$ norm, and then shows $\|x - x_{\mathrm{ref}}\|_{L_\infty} \le \gamma_1/\sqrt\Gamma$ and $\|u - u_{\mathrm{ref}}\|_{L_\infty} \le \gamma_2/\sqrt\Gamma$.

**The L1 norm in the example.** For $G(s) = s/((s + 1)(s + \omega_c))$ with $\omega_c \ne 1$, partial fractions give $g(t) = (\omega_c e^{-\omega_c t} - e^{-t})/(\omega_c - 1)$. The function $g$ is positive for $t < t_0$ and negative for $t > t_0$, where $\omega_c e^{-\omega_c t_0} = e^{-t_0}$, that is $t_0 = \ln\omega_c/(\omega_c - 1)$. Since $\int_0^\infty g\,dt = G(0) = 0$, $\int_0^\infty |g|\,dt = 2\int_0^{t_0} g\,dt = 2\,\frac{(1 - e^{-\omega_c t_0}) - (1 - e^{-t_0})}{\omega_c - 1}$, which is the formula of the page. For $\omega_c = 2$, $t_0 = \ln 2$ and the norm is $2(1/2 - 1/4) = 1/2$. The tests check the formula against a numerical integral and the bound of Claim 4 against the simulation.
