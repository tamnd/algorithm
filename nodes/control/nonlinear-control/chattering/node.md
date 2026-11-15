---
tag: B606X1
kind: concept
slug: chattering
name: Chattering in sliding mode control
aliases:
- sliding mode chattering
area: control/nonlinear-control
level: core
summary: High frequency oscillation of a switching control caused by sampling, delays and unmodeled dynamics, reduced by boundary layers or higher order sliding modes.
prereqs: [sliding-mode-control]
see_also: [super-twisting-algorithm, sliding-mode-observer, describing-function, limit-cycle, zeno-behavior, relay-autotuning, stiff-ode-problem]
sources:
  - paper: doi:10.1080/00207178408933284
    title: "J.-J. E. Slotine, Sliding controller design for non-linear systems, International Journal of Control 40(2), 421-434, 1984"
    locator: the boundary layer around the sliding surface and the trade between tracking precision and control bandwidth
  - paper: doi:10.1109/87.761053
    title: "K. David Young, Vadim I. Utkin and Ümit Özgüner, A control engineer's guide to sliding mode control, IEEE Transactions on Control Systems Technology 7(3), 328-342, 1999"
    locator: the analysis of chattering and the catalog of practical remedies
  - paper: "A. Levant, Chattering analysis, IEEE Transactions on Automatic Control 55(6), 1380-1389, 2010"
    title: Chattering analysis
    locator: the size of the oscillations of first order and higher order sliding modes in the presence of fast unmodeled dynamics and sampling
  - paper: "A. Levant, Sliding order and sliding accuracy in sliding mode control, International Journal of Control 58(6), 1247-1263, 1993"
    title: Sliding order and sliding accuracy in sliding mode control
    locator: the accuracy of sliding modes of order one and two with discrete sampling
  - book: isbn:9780130408907
    title: Jean-Jacques E. Slotine and Weiping Li, Applied Nonlinear Control, Prentice Hall, 1991
    locator: Chapter 7 (Sliding Control), the boundary layer and the trade between precision and robustness
---

Chattering is the fast oscillation of the sliding variable and the fast switching of the control that appear when a [sliding mode controller](/sliding-mode-control/) runs on a real system. Theory assumes that the control can switch infinitely fast, so that the state stays exactly on the sliding surface $s = 0$. A real controller samples at a finite rate, and real actuators and sensors have small delays and fast dynamics that the model leaves out. The switch then comes a little late every time, the state crosses the surface, and the control jumps between its two values at a high frequency. This page is about that phenomenon, its size and its remedies; it is not the [Zeno behavior](/zeno-behavior/) of hybrid systems, where infinitely many switches happen in finite time in the model itself.

## In plain words

Think of a thermostat with no dead band that switches a heater fully on or fully off. In theory it holds the temperature exactly. In practice the sensor reacts a little late, so the heater stays on a moment too long, then off a moment too long, and it clicks on and off many times per minute. The temperature shakes a little around the target, and the switch wears out. A sliding mode controller behaves the same way, only much faster: it pushes hard in one direction or the other, and every small delay in the loop turns into a fast back and forth motion. This motion can wear out motors and valves, waste energy and excite vibrations that the model does not know about. The usual cures are to soften the switch near the target, or to use a smarter law whose output is continuous.

## The idea

**Ideal sliding.** Take a sliding variable $s$ with $\dot s = -k \operatorname{sgn}(s) + d(t)$, $|d| \le D < k$. Then $s \dot s \le -(k - D)|s|$, so $s$ reaches $0$ in finite time and stays there. In the ideal model, on $s = 0$ the control switches with infinite frequency, and its average is the equivalent control that cancels $d$ (Filippov solutions make this precise; see [sliding mode control](/sliding-mode-control/)).

**Sources of chattering.** Three effects break the ideal picture.

- **Sampling.** If the control is computed every $h$ seconds and held, $s$ moves by up to $(k + D) h$ between samples. It overshoots the surface and the sign changes at almost every sample. The result is an oscillation with amplitude of order $h$ and a period of a few samples.
- **Delays.** A pure delay $\tau$ in the loop has the same effect, with amplitude of order $(k + D) \tau$.
- **Fast unmodeled dynamics.** If the actuator or the sensor has a small time constant $\mu$, the loop with the relay $-k \operatorname{sgn}(s)$ settles into a [limit cycle](/limit-cycle/) whose amplitude shrinks with $\mu$ but does not vanish. Levant (2010) analyzes how this amplitude scales with $\mu$ for sliding modes of each order. The [describing function](/describing-function/) method predicts the frequency and the amplitude approximately (example 4).

**Size, as a theorem.** For the sampled first order sliding mode above, once $|s|$ has entered the band $|s| \le (k + D) h$, it stays there, because $|\dot s| \le k + D$ and the sign of the correction always points back to $0$. So the steady accuracy is of order $h$. For sliding modes of order two, such as the [super-twisting algorithm](/super-twisting-algorithm/), the accuracy with sampling is of order $h^2$ in $s$ and $h$ in $\dot s$ (Levant 1993). Chattering does not go away with higher order sliding modes, but it gets smaller, and the control itself becomes continuous.

**Remedies.**

- **Boundary layer.** Replace $\operatorname{sgn}(s)$ by $\operatorname{sat}(s / \phi)$ with a layer width $\phi > 0$ (Slotine 1984). Outside the layer the control is the same, so the reaching phase does not change. Inside the layer the control is a high gain linear feedback, so it does not switch. The price is exactness: $s$ goes into the layer and then stays within $|s| \le \phi D / k$ instead of reaching $0$. This is a trade, not a free gain: a narrow layer gives precision and a high loop gain, which brings back the fast unmodeled dynamics.
- **Higher order sliding modes.** Move the discontinuity to a derivative of the control. The super-twisting law has a continuous control and keeps finite-time convergence and exact rejection of disturbances with a bounded derivative.
- **Smaller switching gain.** Most of the chattering amplitude is proportional to $k$. A model based term (the estimated equivalent control) or an adaptive gain lets $k$ be just above the remaining uncertainty.
- **Observer in the loop.** If the switching acts on an observer state instead of a measured state, the fast loop closes through the observer, which has no unmodeled dynamics, and the actuator sees a filtered control (Young, Utkin and Özgüner 1999).

## Examples

**1. Sampling, by hand.** Let $\dot s = -k \operatorname{sgn}(s)$ with $k = 1$, sampled with $h = 0.1$ and the control held. Then $s_{j+1} = s_j - k h \operatorname{sgn}(s_j)$. From $s_0 = 0.25$ the sequence is

$$0.25,\ 0.15,\ 0.05,\ -0.05,\ 0.05,\ -0.05,\ 0.05,\ \dots$$

After two steps the state is in the band $|s| \le k h = 0.1$, and then it oscillates with period $2h$ and amplitude $0.05$ forever. The control switches at every sample. A smaller $h$ makes the band smaller, but the switching never stops.

**2. A sampled sliding mode controller.** On the [sliding mode control](/sliding-mode-control/) page, the double integrator with $s = x_1 + x_2$, $k = 1.5$ and the disturbance $0.5 \sin 2t$ is simulated with RK4 and the control held over each step $h$. With $h = 0.002$ the sliding variable stays within $|s| \le 0.00399$ after the reaching time, and the switching term changes sign 365 times in the 500 steps between $t = 2$ and $t = 3$. With $h = 0.001$ the band is $0.00200$. The band is $(k + D) h = 2h$, as the theorem above says, and the chattering is an artifact of the step size that the simulation must not hide.

**3. Boundary layer.** Take $\dot s = -k \operatorname{sat}(s / \phi) + d$ with a constant $d = 0.5$, $k = 1$ and $\phi = 0.1$. Inside the layer the equation is $\dot s = -(k / \phi) s + d$, so $s$ goes to $\phi d / k = 0.05$ without any switching. The ideal sliding mode would give $s = 0$. In example 2 with $\phi = 0.05$, the simulation shows $|s| \le 0.0166$ after the transient, below the bound $\phi D / k = 0.0167$, and no switching at all.

**4. An actuator with fast dynamics.** Let the relay output $-k \operatorname{sgn}(s)$ pass through two first order lags $1 / (\tau p + 1)$ before it drives $\dot s$, so the linear part from relay output to $s$ is $G(p) = 1 / (p (\tau p + 1)^2)$, with $p$ the Laplace variable. The describing function of the relay is $N(A) = 4k / (\pi A)$. The phase of $G(j\omega)$ is $-180$ degrees at $\omega = 1/\tau$, where $|G| = \tau / 2$, so the predicted oscillation has frequency $\omega = 1/\tau$ and amplitude $A = 2 k \tau / \pi$. For $k = 1$ and $\tau = 0.05$ s this is $\omega = 20$ rad/s and $A = 0.0318$. An RK4 simulation with step $10^{-4}$ s gives a measured period of $0.3216$ s ($\omega = 19.54$ rad/s) and an amplitude of $0.0330$. The prediction is close but not exact, because the describing function method is approximate. The amplitude is proportional to $k \tau$: a faster actuator gives smaller chattering, but no actuator removes it.

## Where it is used

- **Every practical sliding mode design.** The choice between the ideal switching law, a boundary layer and a higher order algorithm is a choice about chattering. [Sliding mode control](/sliding-mode-control/), [sliding mode observers](/sliding-mode-observer/) and the [super-twisting algorithm](/super-twisting-algorithm/) all discuss it.
- **Power electronics and electric drives.** Here the actuator is a switch, so switching is natural, and a sliding mode can be implemented directly by the switching of the converter. Chattering then shows up as a switching frequency that must stay within the limits of the devices.
- **Mechanical systems.** Valves, hydraulic drives and robot joints suffer from fast switching, because it causes wear and excites resonances. Boundary layers and continuous higher order laws are the usual choice.
- **Simulation.** A simulation of a discontinuous control with a fixed step shows chattering of the size of the step, as in examples 1 and 2. An adaptive step size solver can take very small steps near the surface and become slow, much like a [stiff problem](/stiff-ode-problem/). The step must be stated with the results.
- **Analysis of relay loops.** The relay feedback experiment of [relay autotuning](/relay-autotuning/) uses the same oscillation on purpose: there the limit cycle measures the critical point of the plant.

## References
