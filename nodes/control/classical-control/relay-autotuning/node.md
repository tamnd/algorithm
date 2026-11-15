---
tag: WBZ78H
kind: algorithm
slug: relay-autotuning
name: Relay feedback autotuning
aliases:
- Astrom-Hagglund relay autotuning
- relay tuning
area: control/classical-control
level: core
summary: Puts a relay in the loop to make a limit cycle, reads the ultimate gain and period from it, and tunes a PID from them.
model: real-ram
complexity:
  vars: {k: the number of simulation steps or samples, n: the order of the plant}
  time: {worst: "O(k n^2)"}
  space: {extra: O(k)}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 1984
  people: [Karl Johan Åström, Tore Hägglund]
  note: "Åström and Hägglund proposed in 1984 to find the ultimate point with a relay in the loop in place of a P controller at high gain, and to tune the controller from it automatically."
prereqs: [feedback-control-loop, frequency-response, gain-margin]
see_also: [ziegler-nichols-tuning, pid-controller, describing-function, limit-cycle, nyquist-plot, self-tuning-regulator, gain-scheduling, time-delay-system]
sources:
  - paper: doi:10.1016/0005-1098(84)90014-1
    title: K. J. Åström and T. Hägglund, Automatic tuning of simple regulators with specifications on phase and amplitude margins, Automatica 20(5) (1984) 645-651
    locator: the whole paper (the relay experiment and the describing function analysis)
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: Chapter 9, Automatic tuning and adaptation
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, second edition, Princeton University Press, 2021
    locator: Chapter 11, PID Control (the section on tuning with relay feedback)
---

Relay feedback autotuning finds the ultimate point of a plant with a short experiment in closed loop. A relay, a switch with the two outputs $+d$ and $-d$, replaces the controller. For most process plants the loop then settles into a limit cycle. Its period is close to the ultimate period $T_u$, and its amplitude $a$ gives the estimate $4 d/(\pi a)$ of the ultimate gain $K_u$. A rule such as the [Ziegler-Nichols](/ziegler-nichols-tuning/) ultimate cycle rule then gives the settings of a [PID controller](/pid-controller/). Unlike the original Ziegler-Nichols experiment, the loop is never brought close to a growing oscillation, and the size of the oscillation is set by $d$.

## In plain words

Put a simple switch in place of the controller. When the output is below the target, the switch pushes up with full force. When the output is above the target, it pushes down. The output then swings up and down at a steady rate. The time of one swing tells how fast the plant is. The size of the swing, compared with the size of the push, tells how much gain the plant has at that rate. These two numbers are almost the same as the two numbers that the Ziegler-Nichols method needs. So a controller can run the test by itself, compute its settings and switch back to normal control, all in a few swings. The person who starts the test only chooses how hard the switch pushes.

## The problem

**Input.** A plant that can run in closed loop with a relay. For a simulation, a linear model $x' = A x + B u(t - \theta)$, $y = C x$ of order $n$ with a delay $\theta \ge 0$. The relay amplitude $d > 0$, an optional hysteresis $\varepsilon \ge 0$, the step $\Delta t$ and the length of the experiment.

**Output.** The period $T$ and the amplitude $a$ of the limit cycle, the estimates $\hat K_u = 4 d/(\pi a)$ and $\hat T_u = T$, and the controller settings from a tuning rule.

**The relay.** With the error $e = r - y$, the relay gives $u = +d$ when $e > \varepsilon$, $u = -d$ when $e < -\varepsilon$, and keeps its last value in between.

**Why it works.** Assume that $y$ is close to a sine of amplitude $a$. The relay output is a square wave in phase with $e$, and the first harmonic of a square wave of amplitude $d$ has the amplitude $4 d/\pi$. A plant that passes this first harmonic and damps the higher ones gives the loop condition

$$P(j\omega) = -\frac{\pi a}{4 d}.$$

So the cycle runs at a frequency where the phase of $P$ is $-180$ degrees, and $1/|P(j\omega)| = 4 d/(\pi a)$. This is the [describing function](/describing-function/) method. It is an approximation, because $y$ is not a pure sine. With hysteresis the relay switches later, and the same argument gives the point where the phase of $P$ is $-180 + \arcsin(\varepsilon/a)$ degrees.

## The algorithm

```pseudo id=main
RELAY-AUTOTUNE(plant, d, eps, rule)
L1  u ← +d
L2  at each step: e ← r - y;  if e > eps then u ← +d;  if e < -eps then u ← -d
L3  apply u to the plant for one step and record y
L4  when the run ends: find the upward crossings of r by y, by linear interpolation
L5  T ← the mean time between crossings over the last m periods
L6  a ← half the peak-to-peak value of y over the same periods
L7  K ← 4 d / (pi a)
L8  return rule(K, T)
```

Lines L2 and L3 repeat until the cycle has settled. The code runs a fixed time and uses the last $m = 3$ full periods; a real autotuner stops when two periods in a row agree within a tolerance. A real relay acts at the sampling instants only, and so does the simulated one, which adds up to one sample of delay to each switch. The simulation uses the classical Runge-Kutta method with the step $\Delta t$, and the delay is a queue of whole steps.

The code also computes the exact symmetric limit cycle for a plant with no delay and no hysteresis. With $\Phi = e^{A\tau}$ and $\Gamma = \int_0^\tau e^{As}\, ds\, B$, the state at a switch is $x_0 = -(I + \Phi)^{-1} \Gamma d$, and the half period $\tau$ solves $C x_0(\tau) = 0$. A grid scan and bisection give $\tau$. This shows how large the error of the describing function is, apart from the effects of sampling.

## Example

**A third order lag.** Take $P(s) = 1/(s + 1)^3$ and $d = 1$. The true ultimate point is $K_u = 8$ and $T_u = 2\pi/\sqrt 3 = 3.62760$ s.

| quantity | exact cycle | simulation, $\Delta t = 0.005$ s | true value |
|---|---|---|---|
| period $T$ (s) | 3.67975 | 3.69000 | $T_u = 3.62760$ |
| amplitude $a$ | 0.163061 | 0.164096 | |
| $4 d/(\pi a)$ | 7.8083 | 7.7591 | $K_u = 8$ |

The exact cycle has a period 1.4 percent longer than $T_u$ and a gain estimate 2.4 percent below $K_u$. That is the error of the describing function for this plant. The simulation adds about $2 \Delta t$ to the period, because each switch waits for the next step. The ultimate cycle PID rule gives $K = 4.6555$, $T_i = 1.8450$ s and $T_d = 0.46125$ s, close to the values 4.8, 1.8138 s and 0.4534 s from the true ultimate point. With a derivative filter $N = 20$ the loop has an overshoot of 0.504 to a set-point step. These numbers are measurements.

**A plant with an integrator.** For $P(s) = 1/(s(s + 1)(s + 2))$, with $K_u = 6$ and $T_u = 4.44288$ s, the exact cycle has $T = 4.55107$ s and $4 d/(\pi a) = 5.7865$. The errors are 2.4 and 3.6 percent.

**A first order lag with a delay.** For $P(s) = e^{-\theta s}/(s + 1)$ the cycle has a closed form: the half period is $\theta + \ln(2 - e^{-\theta})$ and the amplitude is $d(1 - e^{-\theta})$. The output has corners, so the describing function is less accurate here.

| $\theta$ (s) | cycle period (s) | true $T_u$ (s) | $4 d/(\pi a)$ | true $K_u$ |
|---|---|---|---|---|
| 0.5 | 1.6636 | 1.7106 | 3.2359 | 3.8069 |
| 1 | 2.9798 | 3.0971 | 2.0142 | 2.2618 |
| 2 | 5.2462 | 5.4901 | 1.4725 | 1.5198 |

The gain estimate is 15 percent low for $\theta = 0.5$ s and 3 percent low for $\theta = 2$ s. A low estimate gives a lower controller gain, which errs on the safe side.

**Hysteresis.** With $\varepsilon = 0.05$ on the third order lag the cycle slows to $T = 4.33$ s with $a = 0.23283$. The estimate is the point with the gain $5.4686$ at the phase $-167.60$ degrees. At $\omega = 2\pi/T$ the plant has $1/|P| = 5.4730$ and the phase $-166.28$ degrees. So the hysteresis moves the point found away from the ultimate point, as the formula says.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **Scaling (theorem).** Without hysteresis, the period of the cycle does not depend on $d$ and its amplitude is proportional to $d$. So $d$ sets the size of the test without a change of the result.
- **The exact cycle (theorem).** For a plant with no delay, a symmetric cycle with the half period $\tau$ has the switching state $x_0 = -(I + \Phi)^{-1} \Gamma d$ with $C x_0 = 0$, and such an $x_0$ gives a cycle if $y$ keeps its sign over the half period. For a first order lag with a delay the cycle has a closed form.
- **The estimate (approximation).** If $y$ is a sine, harmonic balance gives $P(j\omega) = -(\pi a/(4 d)) e^{j \arcsin(\varepsilon/a)}$. Because $y$ is not a sine, $4 d/(\pi a)$ is an estimate of $K_u$, not its value. The errors in the example are measurements.
- **The analysis of the record (theorem).** Linear interpolation of the crossings and the largest samples give the period and the amplitude of a sampled smooth cycle with an error of order $\Delta t^2$.
- **Convergence to the cycle (measurement).** The page does not prove that the loop converges to the cycle. In the simulations it does within a few periods for every plant above.

## Complexity

Each simulation step evaluates $A x + B u$ four times, which costs $O(n^2)$, so an experiment of $k$ steps costs $O(k n^2)$ time. The analysis visits each sample once, $O(k)$. The record takes $O(k)$ space; a real autotuner keeps only the last crossing times and extreme values, $O(1)$. The exact cycle costs one matrix exponential of order $n + 1$ per trial value of $\tau$, $O(n^3)$ each. On a real plant the cost is the time of the experiment, usually 2 to 4 periods after the start.

## Properties

- **Closed loop all the time.** The plant output stays near the set point, within $\pm a$, during the test.
- **Amplitude set by $d$.** The size of the oscillation is proportional to $d$, so the operator can keep the test inside the allowed range.
- **No prior model.** The method needs only the sign of the plant gain and a rough size for $d$.
- **One frequency.** The test gives one point of the frequency response. Two plants with the same point get the same controller.
- **Noise.** A relay with no hysteresis switches on noise near the crossings. Hysteresis stops this, at the cost of a different point of the Nyquist curve.

## Variants and improvements

- **Hysteresis.** A hysteresis wider than the noise band makes the switching clean. The point found has the phase $-180 + \arcsin(\varepsilon/a)$ degrees.
- **Bias.** A relay with unequal levels, or an extra constant input, also gives the static gain of the plant from the mean values of $u$ and $y$. With the static gain and the ultimate point, a first order model with a delay can be fitted.
- **Other points.** A relay in series with an integrator adds $-90$ degrees to the loop, so it finds the point where the phase of the plant is $-90$ degrees. A relay with hysteresis or with a known delay finds other points of the third quadrant. With several points, rules with a phase or gain margin target can be used, as in the 1984 paper.
- **Other rules.** The ultimate cycle rule is the classic choice, but the rules with a given phase margin, or the AMIGO rules of Åström and Hägglund, give a better damped loop.
- **Gain scheduling and adaptation.** An autotuner can run the test at several operating points and store the settings in a table. See [gain scheduling](/gain-scheduling/). Continuous adaptation is a different method; see [self-tuning regulator](/self-tuning-regulator/).

## When to use it

Use relay autotuning to set the first PID settings of a process loop, or to retune a loop whose plant has drifted, when a short oscillation of a known small size is acceptable. It suits plants with a phase that falls below $-180$ degrees, which covers lags of order two or more and plants with a delay. It does not suit plants that do not oscillate under relay feedback, such as a first order lag with no delay, plants with lightly damped modes, where the cycle can lock onto the wrong frequency, or plants where any oscillation is unsafe.

## Pitfalls

- **The estimate is not exact.** The describing function underestimates $K_u$ by a few percent on lag plants and by 10 percent or more on plants close to a first order lag with a delay. The tuning rule should allow for this.
- **Noise and switching.** Without hysteresis, noise near the set point makes the relay chatter. Choose $\varepsilon$ larger than the noise band.
- **Load changes during the test.** A load step during the test makes the cycle unsymmetric. Use the time between crossings of the same direction, and check that the half periods agree.
- **Sign of the plant gain.** For a plant with a negative gain the relay must act in reverse. A wrong sign drives the output away.
- **Sampling.** A sampled relay switches up to one sample late, which adds phase lag and lengthens the period. In the example the period grows by about $2 \Delta t$. Sample many times per period.
- **Start-up.** The first periods differ from the later ones, because the plant starts from rest. Use the later periods only.

## Implementations

## History

The use of relays to make oscillations is old: relay servos were common in the 1940s and 1950s, and their limit cycles were analysed with the describing function. Karl Johan Åström and Tore Hägglund, at Lund, proposed in 1984 to use a relay experiment to tune simple controllers automatically. Their paper in Automatica showed how the relay gives a point of the Nyquist curve and how to design a PID controller from it with specifications on the phase and gain margins. The method became the basis of automatic tuning in industrial PID controllers, and it is now a standard feature of process controllers.

## References
