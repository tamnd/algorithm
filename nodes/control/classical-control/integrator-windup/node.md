---
tag: 9DKBEJ
kind: concept
slug: integrator-windup
name: Integrator windup
aliases:
- integral windup
- reset windup
area: control/classical-control
level: core
summary: When the actuator saturates, the integral of a controller keeps growing, which causes a large overshoot once the error changes sign.
prereqs: [feedback-control-loop, steady-state-error]
see_also: [pid-controller, anti-windup, cascade-control, internal-model-principle, integral-state-feedback, reference-governor, model-predictive-control, two-degree-of-freedom-control]
sources:
  - paper: doi:10.23919/ACC.1989.4790464
    title: Karl Johan Åström and Lars Rundqwist, Integrator windup and how to avoid it, Proceedings of the 1989 American Control Conference, 1693-1698
    locator: the whole paper (the mechanism of windup and the ways to avoid it)
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: Chapter 3, PID Control (the section on integrator windup)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, second edition, Princeton University Press, 2021
    locator: Chapter 11, PID Control (the section on integral windup)
---

Integrator windup is a failure of a controller with integral action when the actuator reaches a limit. The actuator then gives a constant output, the loop is in effect open, and the error stays large. The integral of the controller keeps adding up this error, so it grows far beyond the value that the steady state needs. When the error changes sign, the integral must first come back down before the controller output leaves the limit. Until then the actuator stays at its limit, and the output overshoots. Every controller with integral action can wind up, including the [PID controller](/pid-controller/). The cure is [anti-windup](/anti-windup/), which keeps the integral consistent with the limited actuator.

## In plain words

A controller with an integral term remembers the past error and pushes harder the longer the error lasts. That is how it removes the last small error. Now suppose the valve is fully open and the level still rises too slowly. The controller cannot push harder, but its memory keeps growing. When the level finally reaches the target, the memory is huge, and the controller keeps the valve fully open for a long time while the memory empties. The level shoots far past the target. Then the same thing can happen in the other direction. The cause is not a bad tuning. It is a controller that does not know that the actuator has stopped following its commands.

## The idea

**The mechanism.** Take a PI controller $v = K e + I$, $I' = (K/T_i)\, e$, and an actuator with the limits $u_{\min} \le u \le u_{\max}$, so $u = \operatorname{sat}(v)$. While $v$ is inside the limits, $u = v$ and the loop is the linear loop that was designed. While $v$ is beyond a limit, $u$ is constant, the plant output does not depend on the controller, and $I$ integrates the error with nothing to stop it. The linear design does not cover this mode.

**Why it overshoots.** At the end of a large set-point step the error falls to zero. In the linear loop the integral then has about the value that holds the output at the set point. After saturation it has much more. The controller output $v = K e + I$ leaves the limit only when the negative error is large enough to cancel the extra integral, $K e \approx -(I - I_{\text{ss}})$, or when the integral has run down. Both need the output to be past the set point. The extra integral is about the integral of the error over the time of saturation, so a longer saturation gives a larger overshoot.

**What it depends on.** Windup needs three things: integral action, a limit in the path from the controller to the plant, and an error that lasts while the limit is active. The limit can be the actuator range, a rate limit, a limit set by a selector between two controllers, a manual mode in which the operator sets the actuator, or a saturated inner loop of a [cascade](/cascade-control/). A large set-point step, a large load, or a start-up are the usual causes.

**What it is not.** Windup is not a property of the linear loop. The [steady-state error](/steady-state-error/) analysis and the margins of the linear loop say nothing about it. The integral is still needed for zero steady-state error, as the [internal model principle](/internal-model-principle/) says for constant references and loads, so the answer is to control the integral, not to remove it.

## Examples

**An integrator plant.** Let $y' = u$, which models a tank with the inflow $u$ and the level $y$. Use the PI controller with $K = 1$ and $T_i = 1$, so $I' = e$, the limits $|u| \le 1$, and a set-point step from 0 to $r = 10$.

Without the limit, the loop is $y'' + y' + y = 10$ with $y(0) = 0$ and $y'(0) = 10$. The output peaks at 12.984 at $t = 2.418$ s and stays within 2 percent of 10 after 7.5 s.

With the limit you can follow the start by hand. At first $v = 10 + I$ is far above 1, so $u = 1$ and $y = t$. The error is $e = 10 - t$, so

$$I(t) = 10 t - \frac{t^2}{2}, \qquad I(10) = 50.$$

The output reaches the set point at $t = 10$ s with the integral at 50. The steady state needs $I = 0$, because $u = 0$ holds the level. After $t = 10$ the error is negative, but $v = e + I = 10 + 9 t - t^2/2$ stays above 1 until

$$t = 9 + \sqrt{99} = 18.95 \text{ s},$$

and all this time $u = 1$ and the level keeps rising at the full rate. The measured peak is 19.002 at $t = 19.055$ s, 90 percent above the set point. The integral is then far negative, the output swings down to 2.993, and the loop needs 62.3 s to stay within 2 percent of the set point.

With back-calculation, one form of anti-windup with the tracking time $T_t = 1$ s, the integral follows $I' = e + (u - v)/T_t$. During saturation this is $I' = 1 - I$, so $I$ stays below 1. The peak is 10.546 and the settling time 12.75 s. With conditional integration, which stops the integral while the actuator is at a limit and the error would drive it further, the peak is 10.298 and the settling time 12.40 s. The numbers after the hand computation are measurements of a simulation with the step 0.001 s.

**A lag plant with a PID controller.** On the [PID controller](/pid-controller/) page, the plant $1/(s + 1)^3$ with the Ziegler-Nichols PID and the limits $|u| \le 2$ has the set-point overshoot 0.569 without protection and 0.162 with back-calculation. Here the effect is smaller, because the saturation lasts only a few seconds. The [anti-windup](/anti-windup/) page compares the methods on this plant.

## Where it is used

- **PID controllers.** Industrial PID controllers normally have a protection against windup; the [PID controller](/pid-controller/) page gives the sampled algorithm with back-calculation.
- **Start-up and large set-point changes.** Batch processes, heating and level control often start far from the set point, with the actuator at a limit for minutes.
- **Selectors and overrides.** When two controllers share one actuator through a selector, the controller that is not selected sees its output ignored and winds up unless it tracks the actuator.
- **Cascade control.** When the inner loop of a [cascade](/cascade-control/) saturates, the outer controller winds up. The outer controller must know that its reference is not followed.
- **State feedback with integral action.** The same problem arises for [integral state feedback](/integral-state-feedback/) and for observer-based controllers whose states drift from the true actuator signal.
- **Methods that handle limits directly.** [Model predictive control](/model-predictive-control/) puts the limits into the optimization, and a [reference governor](/reference-governor/) changes the reference so that the limits are not reached. Both avoid windup by design.

## References
