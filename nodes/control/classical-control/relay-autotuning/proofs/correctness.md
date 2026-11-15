---
title: The relay experiment gives a describing function estimate of the ultimate point, and the exact cycle can be computed
proves: [correctness]
status: full
---

Notation is that of the page. The plant is $x' = A x + B u(t - \theta)$, $y = C x$, with one input and one output, transfer function $P(s) = C (sI - A)^{-1} B e^{-\theta s}$ and a delay $\theta \ge 0$. The set point is $r = 0$, so the error is $e = -y$. The relay gives $u = +d$ when $e > \varepsilon$, $u = -d$ when $e < -\varepsilon$, and keeps its last value in between, with $d > 0$ and the hysteresis $\varepsilon \ge 0$.

The claims are of three kinds. Claims 1 and 2 are exact statements about the loop. Claim 3 is the describing function approximation, which is not exact; the page gives measured errors. Claim 4 is about the analysis of a sampled record.

## Claim 1: the cycle scales with the relay amplitude

*Let $\varepsilon = 0$ and $c > 0$. If $(x(t), u(t))$ is a solution of the loop with the relay amplitude $d$, then $(c\, x(t), c\, u(t))$ is a solution with the amplitude $c\, d$. So the period of a limit cycle does not depend on $d$, and its amplitude is proportional to $d$. With $\varepsilon > 0$ the same holds when $\varepsilon$ is scaled by $c$ too.*

*Proof.* The plant equation is linear, so $c\, x$ solves it with the input $c\, u$. The relay with no hysteresis uses only the sign of $e = -C x$, and the sign of $-C (c\, x)$ is that of $-C x$. So the relay with amplitude $c\, d$ gives exactly $c\, u$. With hysteresis the thresholds $\pm \varepsilon$ must scale with $x$, which needs the hysteresis $c\, \varepsilon$. $\square$

## Claim 2: the symmetric cycle without delay and hysteresis

*Let $\theta = 0$ and $\varepsilon = 0$. For $\tau > 0$ let $\Phi = e^{A\tau}$ and $\Gamma = \int_0^\tau e^{As}\, ds\, B$, and assume that $I + \Phi$ is invertible. The loop has a symmetric periodic solution with the period $2\tau$, in which $y$ crosses 0 downward at $t = 0$ and $u = +d$ on $(0, \tau)$, if and only if*

$$x_0 = -(I + \Phi)^{-1} \Gamma d \quad \text{satisfies} \quad C x_0 = 0,$$

*$y(t) < 0$ on $(0, \tau)$ for the solution from $x_0$ with $u = +d$, and $C(A x_0 - B d) < 0$, so that $y$ indeed falls through 0 just before $t = 0$.*

*Proof.* Assume such a solution. On $(0, \tau)$ the input is the constant $+d$, so $x(\tau) = \Phi x_0 + \Gamma d$. Symmetry means that the second half of the period is the first half with all signs changed, so $x(\tau) = -x_0$. Then $(I + \Phi) x_0 = -\Gamma d$, which gives the formula. The switch at $t = 0$ needs $y(0) = C x_0 = 0$, and the input stays at $+d$ only if $e = -y > 0$, that is $y < 0$, on $(0, \tau)$. Just before $t = 0$ the input was $-d$, so $y'(0^-) = C(A x_0 - B d)$, and a downward crossing needs this to be negative.

Conversely, let $x_0$ satisfy the conditions. From $x_0$ with $u = +d$, $y$ stays below 0 on $(0, \tau)$, so the relay keeps $u = +d$, and $x(\tau) = \Phi x_0 + \Gamma d = -x_0$. Now $y(\tau) = -C x_0 = 0$ and $y$ rises through 0, so the relay switches to $-d$. By the symmetry of the equations under $(x, u) \to (-x, -u)$, the next half period is the first one with signs changed, and the state returns to $x_0$ at $2\tau$. $\square$

The code finds the first sign change of $\tau \mapsto C x_0(\tau)$ on a grid and refines it by bisection. It computes $\Phi$ and $\Gamma$ together, as the upper blocks of the exponential of the matrix $\left[\begin{smallmatrix} A & B \\ 0 & 0 \end{smallmatrix}\right] \tau$. The tests check the conditions on the solution afterwards. The cycle may still be one of several, and the claim says nothing about whether nearby solutions converge to it; the simulation shows that they do for the example plants.

**A closed form with a delay.** For $P(s) = e^{-\theta s}/(s + 1)$ and $\varepsilon = 0$, take $y(t_0) = 0$ with $y$ falling, so the relay switches to $+d$ at $t_0$. For the time $\theta$ the plant still gets $-d$, so $y(t_0 + \theta) = -d(1 - e^{-\theta})$. Then $y$ rises toward $+d$:

$$y(t) = d - d (2 - e^{-\theta}) e^{-(t - t_0 - \theta)},$$

which is 0 after the further time $\ln(2 - e^{-\theta})$. So the half period is $\tau = \theta + \ln(2 - e^{-\theta})$ and the amplitude is $a = d(1 - e^{-\theta})$. The tests compare the simulation with these values.

## Claim 3: the describing function estimate

*Assume that $y$ is close to a sine, $y(t) = -a \sin \omega t$. Keep only the first harmonic of the relay output. Then $P(j\omega) = -\frac{\pi a}{4 d} e^{j \arcsin(\varepsilon/a)}$. With $\varepsilon = 0$ this is the point where the phase of $P$ is $-180$ degrees, so $\omega$ estimates $\omega_u$ and $4 d/(\pi a)$ estimates $K_u$.*

*Proof.* With no hysteresis, $e = a \sin \omega t$ and the relay output is a square wave of amplitude $d$ in phase with $e$. Its Fourier series is $\frac{4 d}{\pi} \sum_{k \text{ odd}} \frac{\sin k\omega t}{k}$, so the first harmonic is $\frac{4 d}{\pi} \sin \omega t$. With hysteresis the relay switches when $e$ passes $+\varepsilon$ upward and $-\varepsilon$ downward. This delays the square wave by $\arcsin(\varepsilon/a)/\omega$, so the first harmonic is $\frac{4 d}{\pi} \sin(\omega t - \psi)$ with $\psi = \arcsin(\varepsilon/a)$. Harmonic balance asks that the plant maps this first harmonic to the assumed $y$: in phasor form, $P(j\omega) \frac{4 d}{\pi} e^{-j\psi} = -a$. Solve for $P(j\omega)$. $\square$

The assumption is not exact: $y$ also contains the odd harmonics of the square wave, filtered by $P$. The estimate is good when $|P(3 j\omega)|$ is small compared with $|P(j\omega)|$, which holds for plants with several lags. It is worse for plants close to a first order lag with a delay, whose output has corners. The page gives the measured errors.

## Claim 4: the analysis of the record has an error of order $\Delta t^2$ for a fixed cycle

*Let the record be samples, with the step $\Delta t$, of a periodic function $y$ that is twice continuously differentiable near its upward crossings of 0 and near its extrema, with $y' \ne 0$ at the crossings. Then the period and the amplitude from lines L4 to L6 have errors $O(\Delta t^2)$.*

*Proof.* Near a crossing $t_c$, linear interpolation between the samples around it has the error $O(\Delta t^2 \max |y''|)$ in $y$, so the interpolated crossing time has the error $O(\Delta t^2 / |y'(t_c)|)$. The period is a difference of two such times divided by the number of periods. At an extremum $t_e$, $y'(t_e) = 0$, so the nearest sample $t_j$ with $|t_j - t_e| \le \Delta t/2$ has $|y(t_j) - y(t_e)| \le \frac18 \Delta t^2 \max|y''|$. $\square$

The claim is about the analysis of a given record. The sampled relay itself acts on $y$ at the steps only, so each switch comes up to one step late. This changes the loop: in the tests the period of the simulated loop is longer than the exact period by about $2 \Delta t$. That is a measurement.

## Claim 5: the cost

*A record of $k$ steps of a plant of order $n$ costs $O(k n^2)$ time, and its analysis costs $O(k)$.*

*Proof.* One step of the classical Runge-Kutta method evaluates $A x + B u$ four times, each $O(n^2)$, and the relay and the delay line cost $O(1)$ per step (the delay line is a queue). The analysis visits each sample a fixed number of times. $\square$
