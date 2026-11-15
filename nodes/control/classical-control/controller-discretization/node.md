---
tag: WMT4YH
kind: technique
slug: controller-discretization
name: Controller discretization by emulation
aliases:
- emulation design
- digital redesign
area: control/classical-control
level: core
summary: Designs a continuous controller and turns it into a discrete one by Tustin, matched pole-zero or hold equivalents.
prereqs: [lead-lag-compensator, phase-margin, zero-order-hold-discretization]
see_also: [bilinear-transform, sampled-data-system, z-transform, aliasing, sampling-theorem, pid-controller, iir-filter, frequency-response]
sources:
  - paper: doi:10.1049/ji-2a.1947.0020
    title: Arnold Tustin, A method of analysing the behaviour of linear systems in terms of time series, Journal of the Institution of Electrical Engineers, Part IIA 94(1) (1947) 130-142
    locator: the whole paper (the bilinear substitution)
  - book: isbn:0-13-314899-8
    title: Karl Johan Åström and Björn Wittenmark, Computer-Controlled Systems, third edition, Prentice Hall, 1997
    locator: Chapter 8 (approximation of continuous-time controllers)
---

Emulation design first designs a continuous controller $C(s)$ by the usual tools, then replaces it by a discrete controller $C_d(z)$ that runs on a computer with the sampling period $h$. The plant still gets its input through a zero-order hold. The common maps are the Tustin (bilinear) map, Tustin with prewarping, the matched pole-zero map, the hold equivalent of $C$, and the Euler maps. This page covers the choice among them and what each does to the margins of the loop. For the map $s = (2/h)(z - 1)/(z + 1)$ itself and its use for filters, see the [bilinear transform](/bilinear-transform/); for the exact discrete model of the plant, see [zero-order hold discretization](/zero-order-hold-discretization/). The emulated loop is an approximation: the hold adds a delay of about $h/2$, which costs phase margin, and this cost is the main check.

## In plain words

Most controllers are designed with continuous formulas, but they run on a computer that reads the sensor and sets the actuator only at fixed times. Emulation keeps the continuous design and turns its formula into a rule that updates at each sample. There are several ways to do this. The best common way keeps the behaviour of the controller at low and middle frequencies close to the original and never turns a well-behaved controller into a badly behaved one. All ways have one cost that no formula removes: the actuator value is held between the samples, which acts like a small delay of half a sample. This delay reduces the safety margin of the loop. If the samples are frequent compared with the speed of the loop, the loss is small; if not, design the controller with the delay in mind or design it directly in discrete time.

## When it applies

- A continuous controller exists, or the designer prefers continuous tools such as [loop shaping](/loop-shaping/) or PID rules.
- The sampling is fast compared with the loop: the crossover frequency $\omega_c$ and the period $h$ give a small $\omega_c h$, so that the loss $\omega_c h/2$ rad of phase is acceptable.
- An anti-aliasing filter before the sampler is in the design or its lag is small at $\omega_c$; see [aliasing](/aliasing/).
- If $\omega_c h$ is large, or the plant has fast dynamics near the Nyquist frequency $\pi/h$, a direct discrete design on the exact sampled plant is better.

## The template

1. **Design $C(s)$** with some margin to spare for the hold: plan on losing about $\omega_c h/2$ rad of phase margin (a rule of thumb from the delay of $h/2$ of the hold).
2. **Choose $h$.** Take $h$ so that $\omega_c h/2$ is a few degrees, and so that the anti-aliasing filter has little lag at $\omega_c$.
3. **Map $C(s)$ to $C_d(z)$**:
   - *Tustin:* $s \leftarrow \dfrac{2}{h} \dfrac{z - 1}{z + 1}$.
   - *Tustin with prewarping at $\omega_0$:* $s \leftarrow \dfrac{\omega_0}{\tan(\omega_0 h/2)} \dfrac{z - 1}{z + 1}$, which makes $C_d$ equal to $C$ exactly at $\omega_0$, usually the crossover or a notch frequency.
   - *Matched pole-zero:* map each pole and zero $p$ to $e^{p h}$, put zeros at $z = -1$ for excess poles if wanted, and match the gain at $s = 0$ (or at another frequency).
   - *Hold equivalent:* $C_d(z) = (1 - z^{-1}) \, \mathcal{Z}\{C(s)/s\}$, exact for inputs that are constant between samples.
   - *Euler:* forward $s \leftarrow (z - 1)/h$ or backward $s \leftarrow (z - 1)/(h z)$.
4. **Write the difference equation.** From $C_d(z) = (b_0 + b_1 z^{-1})/(1 + a_1 z^{-1})$ comes $u_k = -a_1 u_{k-1} + b_0 e_k + b_1 e_{k-1}$. For PID controllers, see the [PID controller](/pid-controller/) page for the usual forms and the anti-windup.
5. **Check the sampled loop.** Discretize the plant exactly with the zero-order hold, close the loop with $C_d$, and compute the phase margin, $M_s$ and the closed-loop poles in $z$ (all inside the unit circle for an asymptotically stable loop).

**What each map preserves (theorems).**

- *Tustin.* With $z = e^{j\omega_d h}$, $(z - 1)/(z + 1) = j \tan(\omega_d h/2)$. So $C_d(e^{j\omega_d h}) = C(j \omega)$ with $\omega = (2/h) \tan(\omega_d h/2)$: the discrete response is the exact continuous response at a warped frequency. The map sends the open left half-plane onto the open unit disc, so a BIBO stable $C$ gives a BIBO stable $C_d$ of the same order, and the gain at $\omega = 0$ is exact. Prewarping changes the constant so that $\omega_0$ maps to itself.
- *Backward Euler* sends the left half-plane into the disc $|z - 1/2| < 1/2$, so BIBO stability is kept.
- *Forward Euler* sends a pole $p$ to $1 + h p$, which is inside the unit circle if and only if $|1 + hp| < 1$; for a real $p < 0$ this needs $h < 2/|p|$. It can turn a BIBO stable $C$ into a $C_d$ that is not.
- *Matched pole-zero* places the poles exactly at $e^{p h}$, the poles of the sampled version of $C$.
- *Hold equivalent* gives the exact samples of the output of $C$ when its input is held, so it treats the controller as if it had a hold at its input.

## Classic examples

**The lead network of the lead-lag page.** Take $P = 10/(s(s + 1))$ and the lead $C = (1 + 0.45284 s)/(1 + 0.11321 s)$ from the [lead-lag compensator](/lead-lag-compensator/) page: crossover 4.41659 rad/s, phase margin 49.63 degrees and $M_s = 1.42139$ in continuous time. The plant is discretized exactly with the zero-order hold, and the controller by each map. Measured phase margins of the sampled loop, in degrees; the column "rule" is $49.63 - \omega_c h/2$ in degrees:

| $h$ | rule | forward Euler | backward Euler | Tustin | Tustin, prewarped at $\omega_c$ | matched | hold equivalent |
|---|---|---|---|---|---|---|---|
| 0.01 s | 48.36 | 49.13 | 47.61 | 48.36 | 48.36 | 48.35 | 48.82 |
| 0.02 s | 47.10 | 48.65 | 45.61 | 47.10 | 47.10 | 47.04 | 47.88 |
| 0.05 s | 43.30 | 47.31 | 39.71 | 43.30 | 43.33 | 42.98 | 44.23 |
| 0.1 s | 36.98 | 45.50 | 30.25 | 36.94 | 37.13 | 35.76 | 35.15 |
| 0.2 s | 24.32 | 43.64 | 12.83 | 24.14 | 25.34 | 20.25 | 7.20 |

Measured peak sensitivity $M_s$:

| $h$ | forward Euler | backward Euler | Tustin | prewarped | matched | hold equivalent |
|---|---|---|---|---|---|---|
| 0.05 s | 1.514 | 1.762 | 1.638 | 1.636 | 1.647 | 1.661 |
| 0.1 s | 1.597 | 2.295 | 1.935 | 1.921 | 1.985 | 2.153 |
| 0.2 s | 1.644 | 5.308 | 3.030 | 2.849 | 3.495 | 10.502 |

All closed loops in the table have their poles inside the unit circle. What the numbers show:

- Tustin follows the rule $\omega_c h/2$ to within 0.2 degrees for all $h$: the map itself is nearly exact near $\omega_c$, and the loss is the hold.
- Prewarping helps only a little here (25.34 against 24.14 degrees at $h = 0.2$ s), since the warp moves $\omega_c$ only from 4.417 to 4.347 rad/s at $h = 0.1$ s and to 4.159 rad/s at $h = 0.2$ s.
- The Euler maps turn the frequency variable: $(e^{j\omega h} - 1)/h = e^{j\omega h/2} (2j/h) \sin(\omega h/2)$, so forward Euler evaluates $C$ at $j\omega$ turned by $+\omega h/2$, and backward Euler at $j\omega$ turned by $-\omega h/2$. On this lead, backward Euler loses the most margin among the Euler and Tustin maps.
- Forward Euler keeps the most phase margin on this lead, because its turn offsets part of the hold. This is a property of this example, not a rule: its controller pole $1 - h/0.11321$ is $-0.767$ at $h = 0.2$ s, which makes $u$ alternate in sign from sample to sample, and for $h > 0.2264$ s the pole leaves the unit circle.
- The hold equivalent of the lead raises the crossover (5.43 rad/s at $h = 0.1$ s, 6.39 rad/s at $h = 0.2$ s) and is the worst at large $h$.

With $\omega_c h = 0.22$ (at $h = 0.05$ s) the loss is about 6 degrees, which most designs accept.

## Variations

- **Discrete design.** Discretize the plant exactly and design $C_d$ in the $z$-domain, by root locus or loop shaping in $z$ or by a state-space method. This avoids the approximation of emulation and is needed for slow sampling.
- **Account for the hold in the design.** Add a delay $e^{-sh/2}$, or a Padé approximation of it, to the plant before the continuous design, then emulate. The design then sees the loss of phase and can make up for it.
- **Delta operator.** Writing the discrete controller in the variable $(z - 1)/h$ improves the numerical behaviour at fast sampling, when the poles in $z$ crowd near 1.
- **PID specific forms.** Backward differences for the derivative with the filter, forward or Tustin for the integral; see the [PID controller](/pid-controller/) page.
- **Digital redesign.** Methods that choose $C_d$ to match the continuous closed loop, not only $C$, at the sampling instants or in a norm.

## Pitfalls

- **Slow sampling.** The hold costs $\omega_c h/2$ rad of phase whatever map is used. At $h = 0.2$ s the example lost about 25 degrees with Tustin and more with the others.
- **Forward Euler on fast poles.** It maps a pole $p$ to $1 + hp$, which leaves the unit circle when $h > 2/|p|$.
- **Warping of sharp features.** A notch or a resonance moves in frequency with Tustin. Prewarp at that frequency.
- **No anti-aliasing filter.** Noise above $\pi/h$ folds down into the band of the loop; the filter itself adds lag that must enter the margin check.
- **Checking only $C_d$ against $C$.** The comparison must include the hold and the exact sampled plant; a $C_d$ that matches $C$ well can still give a poor loop.
- **Numbers at fast sampling.** With very small $h$, the coefficients of $C_d$ in $z$ are close to each other and lose digits; use the delta operator or a state-space form.

## Exercises

1. Apply Tustin to $C = (1 + a s)/(1 + b s)$. (Answer: $C_d = \dfrac{(1 + 2a/h) z + (1 - 2a/h)}{(1 + 2b/h) z + (1 - 2b/h)}$.)
2. For the lead of the example and $h = 0.2$ s, where does forward Euler put the controller pole, and what is the largest $h$ that keeps it inside the unit circle? (Answer: $1 - 0.2/0.11321 = -0.767$; $h < 2 \times 0.11321 = 0.2264$ s.)
3. At $h = 0.1$ s, to which discrete frequency does Tustin map the continuous frequency 4.41659 rad/s? (Answer: $\omega_d = (2/h) \arctan(\omega h/2) = 4.347$ rad/s.)
4. Use the rule to predict the phase margin with Tustin at $h = 0.05$ s. (Answer: $\omega_c h/2 = 0.1104$ rad $= 6.33$ degrees, so 43.30 degrees, as measured.)
5. Compute the prewarped constant for $\omega_0 = 4.41659$ rad/s at $h = 0.1$ s, and compare it with $2/h$. (Answer: $\omega_0/\tan(\omega_0 h/2) = 19.674$, against 20.)

## References
