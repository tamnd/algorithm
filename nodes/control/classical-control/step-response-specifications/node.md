---
tag: E40QZC
kind: definition
slug: step-response-specifications
name: Step response specifications
aliases:
- time-domain specifications
- transient response specifications
area: control/classical-control
level: intro
summary: The rise time, peak time, overshoot, settling time and steady-state value of the response to a unit step. Books differ on the rise time and the settling band, so a definition must state them.
prereqs: [second-order-system]
see_also: [second-order-system, steady-state-error, root-locus, complementary-sensitivity-function, final-value-theorem, minimum-phase, impulse-response, pid-controller]
sources:
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Chapter 5, Transient and Steady-State Response Analyses (the definitions of delay time, rise time, peak time, maximum overshoot and settling time, and their formulas for the second-order system)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 3, Dynamic Response (the time-domain specifications and the effects of zeros and extra poles)
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 6, Linear Systems (the step response and its specifications)
---

Step response specifications are numbers read from the response of a stable system to a unit step input: how fast it rises, how far it goes past its final value, when it stays close to that value, and what the final value is. They state in the time domain what a closed loop must do, for example "overshoot at most 10 percent, 2 percent settling time at most 3 s, zero error to a step". Books do not agree on all definitions. The rise time is measured from 10 to 90 percent of the final value in some texts and from 0 to 100 percent in others, and the settling band is 1, 2 or 5 percent. So a specification is only complete when it says which definition it uses. This page fixes one set and gives the values for the [standard second-order system](/second-order-system/) and other examples.

## Definition

Let $G(s)$ be a rational transfer function whose poles are all in the open left half plane (so the system is asymptotically stable), with $G(0) \ne 0$. Let $y(t)$ be the output for the unit step input $u(t) = 1$ for $t \ge 0$, with zero initial state. Then $y(t) \to y_\infty = G(0)$, by the [final value theorem](/final-value-theorem/). The specifications below are relative to $y_\infty$; take $y_\infty > 0$ (otherwise use $-y$).

- **Steady-state value** $y_\infty = G(0)$. For a closed loop from a reference $r$ to $y$, the step error is $e_\infty = 1 - y_\infty$; see [steady-state error](/steady-state-error/).
- **Rise time** $t_r = t_{90} - t_{10}$, where $t_q$ is the first time with $y(t) = (q/100)\,y_\infty$. This page uses the 10 to 90 percent rise time. The *0 to 100 percent rise time* is the first time with $y(t) = y_\infty$; it exists only if $y$ reaches $y_\infty$ in finite time, which an overdamped response never does.
- **Delay time** $t_d = t_{50}$, the first time the response reaches half its final value.
- **Peak time** $t_p$, the time of the largest value $y_{\max} = \sup_{t \ge 0} y(t)$, when that value exceeds $y_\infty$.
- **Overshoot** $M_p = (y_{\max} - y_\infty)/y_\infty$, often given in percent. It is 0 when $y(t) \le y_\infty$ for all $t$.
- **Settling time** $t_s$ for the band $\varepsilon$: the smallest $t_s$ such that $|y(t) - y_\infty| \le \varepsilon\,|y_\infty|$ for all $t \ge t_s$. This page uses $\varepsilon = 0.02$, the 2 percent settling time, unless it says otherwise.
- **Undershoot** $\max(0, -\inf_t y(t))/y_\infty$, the largest move in the wrong direction.

Because $G$ has all poles in the open left half plane, $y(t) - y_\infty$ decays exponentially, so $t_s$ exists for every $\varepsilon > 0$ and $y_{\max}$ is finite. The other numbers are defined whenever their crossing times exist.

**Formulas for the standard second-order system.** For $G = \omega_n^2/(s^2 + 2\zeta\omega_n s + \omega_n^2)$ with $0 < \zeta < 1$, the exact values are $M_p = e^{-\zeta\pi/\sqrt{1 - \zeta^2}}$, $t_p = \pi/(\omega_n\sqrt{1 - \zeta^2})$ and the 0 to 100 percent rise time $(\pi - \arccos\zeta)/(\omega_n\sqrt{1 - \zeta^2})$. The 10 to 90 percent rise time and the settling time have no closed form. The formulas $t_r \approx 1.8/\omega_n$ and $t_s \approx 4/(\zeta\omega_n)$ (2 percent band) are rules of thumb. The bound $t_s \le \ln(1/(\varepsilon\sqrt{1 - \zeta^2}))/(\zeta\omega_n)$ is exact, from the envelope of the response; the derivations are on the [second-order system](/second-order-system/) page.

## Examples and non-examples

**Example: a second-order system.** For $\zeta = 0.5$ and $\omega_n = 1$ rad/s:

| quantity | value | rule of thumb |
|---|---|---|
| overshoot $M_p$ | 0.16303 (16.3 percent) | |
| peak time $t_p$ | 3.6276 s | |
| rise time, 10 to 90 percent | 1.6376 s | $1.8/\omega_n = 1.8$ s |
| rise time, 0 to 100 percent | 2.4184 s | |
| delay time $t_{50}$ | 1.2940 s | |
| settling time, 1 percent band | 8.7805 s | $4.6/(\zeta\omega_n) = 9.2$ s |
| settling time, 2 percent band | 8.0763 s | $4/(\zeta\omega_n) = 8$ s |
| settling time, 5 percent band | 5.2891 s | $3/(\zeta\omega_n) = 6$ s |

The two rise times differ by almost 50 percent, which is why the definition must be stated.

**Example: a first-order system.** For $G = 1/(\tau s + 1)$, $y = 1 - e^{-t/\tau}$. There is no overshoot. The 10 to 90 percent rise time is $\tau \ln 9 = 2.1972\,\tau$, and the 2 percent settling time is $\tau \ln 50 = 3.912\,\tau$. The 0 to 100 percent rise time does not exist.

**Example: a third-order loop with a dominant pair.** The unity feedback loop with $L(s) = K/(s(s + 1)(s + 2))$ and $K = 28/27$ has the closed-loop poles $-1/3 \pm j/\sqrt 3$ (damping ratio 0.5, natural frequency $2/3$ rad/s) and $-7/3$. A simulation of its step response gives the overshoot 15.54 percent, the peak time 5.928 s and the 2 percent settling time 12.487 s. The second-order pair alone predicts 16.30 percent, 5.441 s and 12.114 s. The third pole is 7 times farther from the imaginary axis than the pair, and it still delays the peak by about 0.5 s; see [root locus](/root-locus/).

**Example: a response with undershoot.** $G(s) = (1 - s)/(s + 1)^2$ has a zero at $s = 1$ in the right half plane. Its step response is $y = 1 - e^{-t} - 2 t e^{-t}$, which falls to $-0.2131$ at $t = 0.5$ s before it rises to 1: an undershoot of 21.3 percent. A real zero in the right half plane always gives some undershoot (see [minimum phase](/minimum-phase/) and [complementary sensitivity function](/complementary-sensitivity-function/)).

**Example: the settling time can jump.** For the second-order system with $\omega_n = 1$, the overshoot equals the 2 percent band when $\zeta = \sqrt{\ln^2 50/(\pi^2 + \ln^2 50)} = 0.7797$. Just below this value the first peak leaves the band and the settling time is about 5.07 s, which is the time the response re-enters the band after the peak. Just above it the response enters the band on the way up and stays there, and the settling time is about 3.60 s. So $t_s$ is not a continuous function of the parameters, and an optimizer that uses it as a cost must allow for this.

**Non-example: an unstable or marginally stable system.** For $G = 1/(s^2 + 1)$ the step response is $1 - \cos t$, which oscillates between 0 and 2 for ever. There is no final value and no settling time. The formula $\lim_{s \to 0} s\,G(s)/s = 1$ gives a number, but it is not a limit of $y$.

**Non-example: a system with zero gain at zero frequency.** For $G = s/(s + 1)$, $y = e^{-t}$ and $y_\infty = 0$. The relative numbers $M_p$ and the band $\varepsilon\,|y_\infty|$ are not defined. Such a response is described by its peak and its decay time instead.

**Non-example: a rule of thumb used as a definition.** "$t_s = 4/(\zeta\omega_n)$" is not the settling time of a third-order loop, nor even exactly that of a second-order system (8 s against 8.0763 s above). Use it only to place the poles in the first pass of a design.

## Related definitions

- **Steady-state error** to a step, a ramp and a parabola, and the error constants; see [steady-state error](/steady-state-error/).
- **Frequency-domain specifications.** The bandwidth and the resonant peak of the [complementary sensitivity function](/complementary-sensitivity-function/), and the [phase margin](/phase-margin/) of the loop, are the frequency-domain partners of the rise time and the overshoot. For the second-order system both sets follow from $\zeta$ and $\omega_n$.
- **Regions in the s plane.** For a dominant pair, $M_p \le \bar M$ means $\zeta \ge \bar\zeta$, and a settling time bound means a lower bound on $\zeta\omega_n$. The [root locus](/root-locus/) method places the dominant poles inside these regions.
- **Integral criteria.** The integral of the absolute error (IAE) or of the time-weighted absolute error (ITAE) of the step response measures the whole transient in one number; tuning rules such as those for the [PID controller](/pid-controller/) often minimize one of them.
- **Impulse response.** The step response is the integral of the [impulse response](/impulse-response/), so the overshoot is zero when the impulse response is nonnegative.

## References
