---
tag: 66J2N7
kind: technique
slug: event-triggered-control
name: Event-triggered control
aliases:
- event-based control
area: control/discrete-event-and-hybrid-systems
level: research
summary: Updates the control only when a state-dependent condition says the error has grown too large, so it uses less communication than periodic sampling.
prereqs: [sampled-data-system, input-to-state-stability, lyapunov-function]
see_also: [sampled-data-system, input-to-state-stability, zeno-behavior, lyapunov-equation, exponential-stability, hybrid-automata, time-triggered-scheduling, linear-matrix-inequality]
sources:
  - paper: doi:10.1109/TAC.2007.904277
    title: "P. Tabuada, Event-triggered real-time scheduling of stabilizing control tasks, IEEE Transactions on Automatic Control 52(9), 2007, pages 1680 to 1685"
    locator: the relative trigger from an ISS Lyapunov function, asymptotic stability, and the positive lower bound on the inter-event times
  - paper: doi:10.1109/CDC.2002.1184824
    title: "K. J. Åström and B. M. Bernhardsson, Comparison of Riemann and Lebesgue sampling for first order stochastic systems, IEEE Conference on Decision and Control, 2002, pages 2011 to 2016"
    locator: event-based (Lebesgue) sampling against periodic (Riemann) sampling for a first order system
  - paper: doi:10.1109/CDC.2012.6425820
    title: "W. P. M. H. Heemels, K. H. Johansson and P. Tabuada, An introduction to event-triggered and self-triggered control, IEEE Conference on Decision and Control, 2012, pages 3270 to 3285"
    locator: the tutorial overview of triggers, inter-event times, periodic event-triggered and self-triggered control
  - paper: doi:10.1109/TAC.2014.2366855
    title: "A. Girard, Dynamic triggering mechanisms for event-triggered control, IEEE Transactions on Automatic Control 60(7), 2015, pages 1992 to 1997"
    locator: the dynamic trigger with an internal variable and its larger inter-event times
  - paper: doi:10.1109/TAC.2014.2325272
    title: "D. P. Borgers and W. P. M. H. Heemels, Event-separation properties of event-triggered control systems, IEEE Transactions on Automatic Control 59(10), 2014, pages 2644 to 2656"
    locator: which triggers keep a positive minimum time between events when disturbances act
---

Event-triggered control is a way to implement a feedback law $u = -Kx$ (or any $u = k(x)$) on a digital platform without a fixed sampling period. The controller holds the last computed input. It measures the state, compares it with the state used for the last update, and computes and sends a new input only when the difference is too large compared with the state. Tabuada (2007) gave the standard trigger $\|x(t_k) - x(t)\| \ge \sigma \|x(t)\|$, proved asymptotic stability when the closed loop is input-to-state stable with respect to the measurement error, and proved a positive lower bound on the time between two events. The aim is fewer updates, and so less traffic on a shared network, less computation, and less energy in a wireless sensor, than a [sampled-data](/sampled-data-system/) loop with a fixed period that must be short enough for the worst case.

## In plain words

A thermostat that reads the room every second, and sends a command every second, wastes most of its messages: the room barely changes. A better rule is to send a new command only when the room has changed enough since the last command. "Enough" is measured relative to how far the room is from the target. Far from the target, small changes do not matter. Close to the target, the rule asks for more care.

The rule must keep the feedback working, and it must not ask for updates infinitely often in a finite time. For a linear plant with a good feedback, both hold: there is a proof that the state goes to the target, and a proof that two updates are never closer than a fixed time.

## When it applies

- **A feedback that works when continuous.** You need a law $u = k(x)$ that stabilizes the plant without sampling, and an ISS Lyapunov function: $V' \le -a(\|x\|) + g(\|e\|)$ for the loop $x' = f(x, k(x + e))$, with $e$ the measurement error and $a$, $g$ class-K functions. For linear systems with a Hurwitz $A - BK$, $V = x^T P x$ with $(A - BK)^T P + P(A - BK) = -Q$ works (see [Lyapunov equation](/lyapunov-equation/)).
- **Cheap monitoring, expensive updates.** The trigger must be checked often, at the sensor, while the costly part (computing, sending, actuating) happens only at events. If checking costs as much as updating, there is little to gain.
- **A cost of communication.** The method pays off on shared networks, wireless links and processors that run many tasks. On a dedicated wired loop, periodic sampling is simpler and easier to analyze.

## The template

The plant is $x' = Ax + Bu$, the law is $u = -Kx$, and the trigger uses the Euclidean norm. The code checks the trigger after each step of a fixed-step Runge-Kutta solver, as a sensor that samples fast would.

```pseudo id=template
EVENT-TRIGGERED-LOOP(A, B, K, x0, sigma, T, dt)
L1  xhat ← x0
L2  u ← -K xhat
    for t ← dt, 2 dt, ..., T do
L3      x ← one step of x' = A x + B u from x, with u held
L4      e ← ||xhat - x||
L5      if e >= sigma ||x|| then
L6          xhat ← x
L7          u ← -K xhat
```

**Theorem (Tabuada 2007, the linear case).** Let $A_{cl} = A - BK$ be Hurwitz, $Q \succ 0$ and $A_{cl}^T P + P A_{cl} = -Q$. With the error $e = \hat x - x$, the loop between events is $x' = A_{cl} x - BKe$, so $V = x^T P x$ has $V' = -x^T Q x - 2x^T PBKe$. The trigger keeps $\|e\| \le \sigma\|x\|$, so

$$V' \le -\big(\lambda_{\min}(Q) - 2\sigma\|PBK\|_2\big)\|x\|^2,$$

and every $\sigma < \bar\sigma = \lambda_{\min}(Q) / (2\|PBK\|_2)$ makes the origin globally exponentially stable. With $\alpha = \|A_{cl}\|_2$ and $\beta = \|BK\|_2$, the ratio $y = \|e\| / \|x\|$ starts at $0$ at each event and obeys $y' \le (\alpha + \beta y)(1 + y)$. So it needs at least

$$\tau^* = \frac{1}{\alpha - \beta}\ln\frac{\alpha(1 + \sigma)}{\alpha + \beta\sigma}$$

to reach $\sigma$ (and $\sigma / (\alpha(1 + \sigma))$ if $\alpha = \beta$). Every two events are at least $\tau^*$ apart, so there is no [Zeno behavior](/zeno-behavior/). The derivations are in [the correctness proof](proofs/correctness.md). Note that $\tau^*$ is a lower bound for all states, so a periodic loop with the period $\tau^*$ is also stable; the gain of the trigger is that the actual gaps are usually much longer.

## Classic examples

**An unstable plant of order 2.** Take $A = \begin{pmatrix} 0 & 1 \\ -2 & 3 \end{pmatrix}$, $B = (0, 1)^T$ and $K = (-1, 4)$, that is $u = x_1 - 4x_2$. Then $A_{cl} = \begin{pmatrix} 0 & 1 \\ -1 & -1 \end{pmatrix}$, which is Hurwitz. With $Q = I$, the Lyapunov equation gives exactly $P = \begin{pmatrix} 3/2 & 1/2 \\ 1/2 & 1 \end{pmatrix}$. $PBK = \begin{pmatrix} -1/2 & 2 \\ -1 & 4 \end{pmatrix}$ has rank 1, so $\|PBK\|_2 = \sqrt{21.25} = 4.6098$, and $\bar\sigma = 0.10847$. Also $\alpha = \|A_{cl}\|_2 = 1.6180$ (the golden ratio) and $\beta = \|BK\|_2 = \sqrt{17} = 4.1231$. For $\sigma = 0.05$, $\tau^* = 0.028396$. A simulation from $x_0 = (1, 0)$ for 10 seconds, with the trigger checked every $0.001$ seconds, gives 218 events, counting the one at $t = 0$. The gaps are between $0.030$ and $0.079$, and $\|x(10)\| = 0.0034$. A periodic loop with the guaranteed period $\tau^*$ would need about 352 updates in the same time. These numbers are measurements of one run; the tests check them, and they also check the bound $\tau^*$ and the decrease of the state on random stable loops.

**Lebesgue sampling.** Åström and Bernhardsson (2002) compared periodic sampling (Riemann) with sampling when the signal crosses a level (Lebesgue) for a first order stochastic system. With the same mean rate of samples, the event-based scheme gave a smaller variance of the state in their analysis. This paper started much of the later interest.

**Send-on-delta sensors.** A sensor that transmits only when its reading has moved by more than a fixed amount uses an absolute trigger $\|e\| \ge \delta$. The loop then converges only to a neighborhood of the origin, whose size depends on $\delta$, but the time between events stays bounded below even with disturbances.

## Variations

- **Mixed trigger.** $\|e\| \ge \sigma\|x\| + \delta$ adds an absolute part. It gives practical stability (convergence to a ball of size of order $\delta$), and Borgers and Heemels (2014) showed that such triggers keep a positive time between events when disturbances act, which a purely relative trigger can lose.
- **Dynamic trigger.** Girard (2015) adds an internal variable $\eta$ with $\eta' = -\gamma(\eta) + \sigma a(\|x\|) - g(\|e\|)$ and triggers when $\eta + \theta(\sigma a(\|x\|) - g(\|e\|)) \le 0$, for a parameter $\theta > 0$. The trigger then uses the margin that the decrease of $V$ has saved, and the events come less often.
- **Periodic event-triggered control.** Check the trigger only at the instants of a fixed fast period, as the template does. Then the time between events is at least that period by construction, and stability can be checked with [linear matrix inequalities](/linear-matrix-inequality/) on the sampled model (Heemels, Johansson and Tabuada 2012).
- **Self-triggered control.** At each event, compute the time of the next one from the current state and the model, so the sensor need not monitor the state between events. The times are more conservative than with event triggering.
- **The loop as a hybrid system.** The closed loop flows between events and jumps at events, when $\hat x$ takes the value of $x$. So it is a [hybrid automaton](/hybrid-automata/) with one location, the guard $\|e\| \ge \sigma\|x\|$ and a reset of $\hat x$. Unlike a [timed automaton](/timed-automata/), its flow is a general linear differential equation, so the analysis uses Lyapunov functions, not a finite quotient.
- **Output feedback and networks.** With only an output measured, or with several sensors that trigger separately, the triggers and the proofs need more care; Heemels, Johansson and Tabuada (2012) survey the results.

## Pitfalls

- **Threshold too large (line L5).** For $\sigma \ge \bar\sigma$ the Lyapunov argument fails, and the loop may diverge. $\bar\sigma$ depends on $Q$ and on the norm; it is a sufficient bound, not the true limit.
- **The state at the origin (line L5).** With a purely relative trigger, $\sigma\|x\| = 0$ at the origin, so a measured state that is exactly zero, or noise near zero, makes the trigger fire at every check. Add an absolute part $\delta$ in practice.
- **Disturbances and noise.** The bound $\tau^*$ is for the nominal plant. With disturbances, a relative trigger can give events that come arbitrarily close together; this is the event-separation problem studied by Borgers and Heemels (2014).
- **Delays.** The theorem assumes that the update is instantaneous. Communication and computation delays add an error that the trigger does not see; the threshold must leave a margin for them.
- **Checking period (line L3).** A trigger checked every $\Delta t$ can fire up to $\Delta t$ late, so $\|e\|$ can exceed $\sigma\|x\|$ for a short time. Make $\Delta t$ small compared with $\tau^*$, or use the periodic event-triggered analysis.
- **Comparing with the wrong baseline.** Compare the number of events with the longest period that keeps the periodic loop stable, not with $\tau^*$, which is a conservative bound.

## Exercises

1. For the example, compute $\bar\sigma$ with $Q = 2I$ and with $Q = \mathrm{diag}(1, 4)$. How does the choice of $Q$ change the allowed threshold?
2. Take the scalar plant $x' = u$ with $u = -kx$ and $k > 0$. Show that every gap between two events is exactly $\sigma / (k(1 + \sigma))$, so the bound $\tau^*$ is reached here. (Hint: between events, $x(t) = \hat x (1 - k(t - t_k))$.)
3. Derive $\tau^*$ for the case $\alpha = \beta$ by solving $z' = \alpha(1 + z)^2$.
4. Replace the trigger by $\|e\| \ge \delta$ with a fixed $\delta > 0$. Show that the state enters a ball whose radius is proportional to $\delta$, and give a lower bound on the time between events.
5. Explain why a periodic loop with the period $\tau^*$ is stable, using the fact that $\|e\| \le \sigma\|x\|$ holds on every interval of length at most $\tau^*$ after an update.

## References
