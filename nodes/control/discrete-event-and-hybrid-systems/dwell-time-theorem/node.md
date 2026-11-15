---
tag: E7SGQ6
kind: theorem
slug: dwell-time-theorem
name: Dwell-time stability theorem
aliases:
- average dwell time theorem
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: "If every mode decays and switches come slowly enough on average, the switched system is globally uniformly exponentially (or asymptotically) stable."
prereqs: [switched-system, lyapunov-function, exponential-stability]
see_also: [common-lyapunov-function, joint-spectral-radius, matrix-exponential, lyapunov-equation, gain-scheduling, hybrid-automata, zeno-behavior, input-to-state-stability]
sources:
  - paper: "A. Stephen Morse, Supervisory control of families of linear set-point controllers, Part 1, Exact matching, IEEE Transactions on Automatic Control 41(10), 1413-1431, 1996"
    locator: the dwell-time switching logic and the stability argument for slow switching between stable linear systems
  - paper: doi:10.1109/CDC.1999.831330
    title: João P. Hespanha and A. Stephen Morse, Stability of switched systems with average dwell-time, Proceedings of the 38th IEEE Conference on Decision and Control, vol. 3, 2655-2660, 1999
    locator: the definition of average dwell time and the stability theorem
  - book: isbn:9780817642976
    title: Daniel Liberzon, Switching in Systems and Control, Birkhäuser, 2003
    locator: the chapter on stability under constrained switching (dwell time, average dwell time, multiple Lyapunov functions)
  - paper: doi:10.1109/37.793443
    title: Daniel Liberzon and A. Stephen Morse, Basic problems in stability and design of switched systems, IEEE Control Systems Magazine 19(5), 59-70, 1999
    locator: the section on stability under slow switching
---

The dwell-time theorem says that switching between stable modes is safe if it is slow enough. A [switched system](/switched-system/) can be unstable even when every mode is exponentially stable, because each switch can move the state to a part of the space where the new mode first makes it grow. But each mode, if it stays active long enough, shrinks the state by more than any switch can enlarge it. The theorem turns this into a number: if the time between switches, the dwell time, is above a bound computed from the modes, the origin is globally uniformly exponentially stable (GUES) for every such switching signal. A. Stephen Morse proved the linear version in 1996 for supervisory control. João Hespanha and Morse extended it in 1999 to an average dwell time, which also allows short bursts of fast switching. The theorem needs no [common Lyapunov function](/common-lyapunov-function/), only one Lyapunov function per mode.

## Statement

Let $\dot x = f_{\sigma(t)}(x)$ be a switched system with a finite set of modes $\mathcal{P}$, each $f_p$ locally Lipschitz with $f_p(0) = 0$, and let $N_\sigma(t, t_0)$ be the number of switches of $\sigma$ in the interval $(t_0, t]$.

**Part 1 (dwell time, linear modes).** Let $f_p(x) = A_p x$, and let $c \ge 1$ and $\lambda_0 > 0$ satisfy $\|e^{A_p t}\| \le c\, e^{-\lambda_0 t}$ for all $p \in \mathcal{P}$ and $t \ge 0$. Let $\tau_D > (\ln c)/\lambda_0$. Then for every switching signal whose consecutive switching times are at least $\tau_D$ apart,

$$|x(t)| \le c\, e^{-\lambda (t - t_0)} |x(t_0)|, \qquad \lambda = \lambda_0 - \frac{\ln c}{\tau_D} > 0,$$

so the origin is GUES over this class of signals.

**Part 2 (average dwell time).** Let $V_p : \mathbb{R}^n \to \mathbb{R}$, $p \in \mathcal{P}$, be $C^1$ functions, $\alpha_1, \alpha_2$ class $\mathcal{K}_\infty$ functions and $\lambda_0 > 0$, $\mu \ge 1$ constants with

$$\alpha_1(|x|) \le V_p(x) \le \alpha_2(|x|), \qquad \nabla V_p(x) \cdot f_p(x) \le -2\lambda_0 V_p(x), \qquad V_p(x) \le \mu V_q(x)$$

for all $x \in \mathbb{R}^n$ and $p, q \in \mathcal{P}$. Let $N_0 \ge 1$ and $\tau_a > (\ln \mu)/(2\lambda_0)$. Then for every switching signal with

$$N_\sigma(t, t_0) \le N_0 + \frac{t - t_0}{\tau_a} \quad \text{for all } t \ge t_0 \ge 0,$$

the origin is globally uniformly asymptotically stable (GUAS) over this class of signals. If $\alpha_1(r) = a r^2$ and $\alpha_2(r) = b r^2$, it is GUES, with

$$|x(t)| \le \sqrt{\frac{b\, \mu^{N_0}}{a}}\; e^{-\lambda (t - t_0)/2} |x(t_0)|, \qquad \lambda = 2\lambda_0 - \frac{\ln \mu}{\tau_a} > 0.$$

For linear modes, Part 2 applies with $V_p(x) = x^\top P_p x$, where $A_p^\top P_p + P_p A_p \preceq -2\lambda_0 P_p$, and $\mu$ is the largest of the numbers $\lambda_{\max}(P_q^{-1/2} P_p P_q^{-1/2})$ over pairs $p, q$.

## In plain words

Each mode, left alone, makes the state shrink at a steady rate. A switch can make things worse for a short while, because the new mode measures the state in its own way and may first push it outward. The worst push per switch is a fixed factor. So if every mode runs long enough before the next switch, the shrinking it does is bigger than the push from the switch, and the state still goes to zero. The theorem says how long is long enough, from the decay rate of the modes and the worst push. The average version allows some quick switches in a row, as long as the switches over a long time are not too many on average. The rule makes no other demand on when the switches happen.

## Proof

**Part 1.** Fix $t \ge t_0$, let $t_1 < \cdots < t_N$ be the switching times in $(t_0, t]$, and let $p_i$ be the mode on $[t_i, t_{i+1})$, with $t_{N+1} = t$. The state at time $t$ is

$$x(t) = e^{A_{p_N}(t - t_N)} \cdots e^{A_{p_1}(t_2 - t_1)} e^{A_{p_0}(t_1 - t_0)} x(t_0).$$

Each factor has norm at most $c\, e^{-\lambda_0 (t_{i+1} - t_i)}$, and the lengths add up to $t - t_0$, so $|x(t)| \le c^{N+1} e^{-\lambda_0 (t - t_0)} |x(t_0)|$. The switches are at least $\tau_D$ apart, so $N \le (t - t_0)/\tau_D$ and $c^N \le e^{(\ln c)(t - t_0)/\tau_D}$, because $c \ge 1$. Then $|x(t)| \le c\, e^{-\lambda (t - t_0)} |x(t_0)|$ with $\lambda = \lambda_0 - (\ln c)/\tau_D$, and $\lambda > 0$ exactly when $\tau_D > (\ln c)/\lambda_0$. The constants $c$ and $\lambda$ do not depend on the signal.

**Part 2.** Fix a solution and set $W(t) = e^{2\lambda_0 t} V_{\sigma(t)}(x(t))$.

1. On an interval without switches, $\sigma = p$ is constant and $\dot W = e^{2\lambda_0 t} \left(2\lambda_0 V_p(x) + \nabla V_p(x) \cdot f_p(x)\right) \le 0$. So $W$ does not increase between switches.
2. At a switching time $t_i$ from mode $q$ to mode $p$, the state is continuous, so $V_p(x(t_i)) \le \mu V_q(x(t_i))$. So $W$ grows by at most the factor $\mu$ at each switch.
3. From steps 1 and 2, $W(t) \le \mu^{N_\sigma(t, t_0)} W(t_0)$, that is,
$$V_{\sigma(t)}(x(t)) \le e^{-2\lambda_0 (t - t_0)} \mu^{N_\sigma(t, t_0)} V_{\sigma(t_0)}(x(t_0)).$$
4. With the average dwell time bound and $\mu \ge 1$, $\mu^{N_\sigma(t, t_0)} \le \mu^{N_0} e^{(\ln \mu)(t - t_0)/\tau_a}$. Hence
$$V_{\sigma(t)}(x(t)) \le \mu^{N_0} e^{-\lambda (t - t_0)} V_{\sigma(t_0)}(x(t_0)), \qquad \lambda = 2\lambda_0 - \frac{\ln \mu}{\tau_a} > 0.$$
5. With the sandwich bounds, $\alpha_1(|x(t)|) \le \mu^{N_0} e^{-\lambda (t - t_0)} \alpha_2(|x(t_0)|)$, so $|x(t)| \le \alpha_1^{-1}\left(\mu^{N_0} e^{-\lambda (t - t_0)} \alpha_2(|x(t_0)|)\right)$. The right side is a class $\mathcal{KL}$ function of $|x(t_0)|$ and $t - t_0$, the same for every signal in the class. This is GUAS. In the quadratic case it reads $a |x(t)|^2 \le \mu^{N_0} e^{-\lambda (t - t_0)} b |x(t_0)|^2$, which is the GUES bound of the statement.

For the matrix form of $\mu$: $x^\top P_p x \le \mu\, x^\top P_q x$ for all $x$ exactly when $\mu$ is at least the largest eigenvalue of $P_q^{-1/2} P_p P_q^{-1/2}$. $\blacksquare$

## Consequences

- **Dwell time is a special case of average dwell time.** Switches at least $\tau_D$ apart satisfy $N_\sigma(t, t_0) \le 1 + (t - t_0)/\tau_D$, so Part 2 applies with $N_0 = 1$ and $\tau_a = \tau_D$.
- **Common Lyapunov function as the limit case.** If all $V_p$ are the same function, then $\mu = 1$, the bound on $\tau_a$ is 0, and the result is stability under arbitrary switching, as for a [common Lyapunov function](/common-lyapunov-function/).
- **A worked bound.** For the two modes $A_1 = \begin{bmatrix} -0.1 & 1 \\ -10 & -0.1 \end{bmatrix}$ and $A_2 = \begin{bmatrix} -0.1 & 10 \\ -1 & -0.1 \end{bmatrix}$ of the [switched system](/switched-system/) example, $\|e^{A_p t}\|_2 \le \sqrt{10}\, e^{-0.1 t}$, so Part 1 gives $\tau_D > \ln\sqrt{10}/0.1 \approx 11.513$ s. For Part 2, $P_1 = \mathrm{diag}(10, 1)$ and $P_2 = \mathrm{diag}(1, 10)$ satisfy $A_p^\top P_p + P_p A_p = -0.2 P_p$, so $\lambda_0 = 0.1$, and $\mu = 10$. The bound is $\tau_a > \ln 10/0.2 \approx 11.513$ s, the same number.
- **Rate.** A longer dwell time gives a faster guaranteed rate, up to $\lambda_0$ as $\tau_D \to \infty$. The rate is what makes the result robust: GUES survives small perturbations and gives [input-to-state stability](/input-to-state-stability/) bounds when inputs are added.
- **Supervisory control.** In Morse's setting, a supervisor picks one controller from a family by comparing prediction errors. A dwell-time or hysteresis rule prevents chattering between controllers, and this theorem gives the stability of the closed loop. The same reasoning applies to [gain scheduling](/gain-scheduling/) with slowly changing operating points.

## Tightness

The bound is sufficient, not necessary, but for some systems it is close to sharp. Take the two modes above and switch periodically, with each mode active for $T$ seconds. The state after one period is multiplied by the monodromy matrix $e^{A_2 T} e^{A_1 T}$, and the periodic signal is unstable when its spectral radius is above 1:

| $T$ (s) | 0.4967 | 1.4902 | 5.0 | 10.4313 | 11.4248 | 12.0 |
|---|---|---|---|---|---|---|
| spectral radius | 9.054 | 7.423 | 0.368 | 1.242 | 1.018 | 0.091 |

For $T$ equal to an odd number of quarter turns, $T = (2k+1)\pi/(2\sqrt{10})$, the spectral radius is $10\, e^{-0.2 T}$, and it is above 1 up to $T \approx 11.4248$. So a dwell time of 11.42 s does not give GUES, and the theorem's 11.513 s is within 1% of the best dwell-time bound for this pair. Other periods, such as 5 s, give a stable periodic signal, which shows that a dwell-time bound speaks about the worst signal in the class, not about each signal.

The hypothesis that each mode is stable cannot be dropped from Part 1. With an unstable mode, no dwell time helps, since the signal that stays in that mode forever has every dwell time. Extensions allow unstable modes when the total time spent in them is a small enough fraction.

## History

Morse (1996) used a dwell-time switching logic in supervisory control of families of linear set-point controllers, and proved that the switched closed loop is exponentially stable if the dwell time is large enough. Hespanha and Morse (1999) introduced the average dwell time, which allows the supervisor to switch quickly now and then, and proved the Lyapunov form of Part 2. Liberzon and Morse (1999) placed slow switching among the basic problems of switched systems, next to stability under arbitrary switching and the design of switching signals, and Liberzon's book (2003) gives the version stated here.

## References
