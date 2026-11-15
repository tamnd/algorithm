---
tag: PVCKWK
kind: concept
slug: feedback-control-loop
name: Feedback control loop
aliases:
- closed-loop control
- unity feedback loop
area: control/classical-control
level: intro
summary: A loop in which a controller acts on the error between a reference and the measured output. It lowers the effect of disturbances and plant errors, but feeds sensor noise in and can destabilize.
history:
  year: 1868
  people: [James Clerk Maxwell, Harold S. Black]
  note: Maxwell analyzed the stability of governors in 1868. Black published the negative feedback amplifier in 1934.
prereqs: [transfer-function, laplace-transform, linear-time-invariant-system]
see_also: [sensitivity-function, complementary-sensitivity-function, steady-state-error, internal-model-principle, nyquist-stability-criterion, pid-controller, block-diagram-reduction, bibo-stability]
sources:
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 1, Introduction, Chapter 2, Feedback Principles, and Chapter 12, Frequency Domain Design (the section Sensitivity Functions, with the four transfer functions of the loop)
  - paper: doi:10.1098/rspl.1867.0055
    title: J. C. Maxwell, On governors, Proceedings of the Royal Society of London 16 (1868) 270-283
    locator: the whole paper (the linearized equations of governors and the conditions for their stability)
  - paper: doi:10.1109/EE.1934.6540374
    title: H. S. Black, Stabilized feed-back amplifiers, Electrical Engineering 53(1) (1934) 114-120; also in the Bell System Technical Journal 13(1) (1934) 1-18
    locator: the whole paper (the gain mu / (1 - mu beta) of an amplifier with feedback, and its low sensitivity to changes in the tube gain)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 4, A First Analysis of Feedback
---

A feedback control loop is a connection in which a controller measures the output $y$ of a system, compares it with a reference $r$, and acts on the error $e = r - y$ to drive the system. The system to control is the *plant* $P$, and the controller is $C$. In the linear case the whole loop is described by the [transfer functions](/transfer-function/) of $P$ and $C$: the product $L = P C$ is the loop transfer function, and the [sensitivity function](/sensitivity-function/) $S = 1/(1 + L)$ and the [complementary sensitivity function](/complementary-sensitivity-function/) $T = L/(1 + L)$ give the response of the loop to each external signal. Feedback makes the output follow the reference with little dependence on the exact plant, and it reduces the effect of disturbances. The price is that sensor noise enters the loop, and that a loop can be unstable even when the plant and the controller are each stable.

## In plain words

A thermostat measures the room temperature, compares it with the temperature you set, and turns the heater on when the room is too cold. It does not need to know how big the room is or how cold it is outside. It only looks at the difference between what you want and what you get. This is feedback.

The same idea works for a cruise control, an amplifier or a robot arm. The controller corrects errors after they appear, so it corrects errors from any cause, also causes that nobody modeled. Two costs come with it. The controller only knows what the sensor tells it, so sensor errors become output errors. And a controller that reacts too strongly or too late can make the output swing more and more, so that the loop becomes unstable.

## The idea

**The loop and its signals.** Take a linear time-invariant plant $P(s)$ and controller $C(s)$, with $s$ the Laplace variable of the one-sided [Laplace transform](/laplace-transform/). The external signals are the reference $r$, a load disturbance $d$ at the plant input and a measurement noise $n$. The loop equations are

$$u = C\,(r - y - n), \qquad y = P\,(u + d).$$

The controller sees the measured output $y + n$, not the true output. This is negative feedback, the default in this area. When the loop is well posed, that is $1 + L(\infty) \ne 0$, solving the two equations gives

$$y = T\,r + P S\,d - T\,n, \qquad e = r - y - n = S\,r - P S\,d - S\,n, \qquad u = C S\,r - T\,d - C S\,n,$$

with $L = P C$, $S = 1/(1 + L)$ and $T = L/(1 + L)$. The four transfer functions $S$, $T$, $P S$ and $C S$ (the "gang of four" of Åström and Murray) describe the loop fully. A loop with a controller in the forward path and the plain output fed back, as here, is a *unity feedback loop*. A sensor with its own dynamics $H(s)$ gives $L = P C H$ and a reference path that has to be scaled; [block diagram reduction](/block-diagram-reduction/) handles such loops.

**Internal stability.** Write $P = b/a$ and $C = n_c/d_c$ as ratios of coprime polynomials. The loop is *internally stable* if the four transfer functions above are all stable, which holds if and only if the characteristic polynomial

$$\chi(s) = a(s)\,d_c(s) + b(s)\,n_c(s)$$

has all its roots in the open left half plane. Then a bounded $r$, $d$ and $n$ give a bounded $u$ and $y$ ([BIBO stability](/bibo-stability/)). Stability of $T$ alone is not enough, because a pole-zero cancellation in the right half plane can hide an unstable mode from $T$ (see [poles and zeros](/poles-and-zeros/)). Whether $\chi$ is Hurwitz is decided by the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/), or from the frequency response of $L$ by the [Nyquist stability criterion](/nyquist-stability-criterion/).

**What feedback buys.** Four effects follow from the formulas:

- *Disturbance rejection.* A disturbance $d_o$ added at the plant output reaches $y$ through $S$. Where $|L(j\omega)| \gg 1$, $|S(j\omega)| \approx 1/|L(j\omega)|$ is small.
- *Robustness to the plant.* The relative change of $T$ per relative change of $P$ is $S$, so where $|S|$ is small, errors in the plant model hardly change the response.
- *Tracking.* $y = T r$ with $T \approx 1$ where $|L| \gg 1$. With an integrator in $L$, $S(0) = 0$, and a constant reference is followed with zero [steady-state error](/steady-state-error/).
- *Change of dynamics.* The closed-loop poles are the roots of $\chi$, not the poles of $P$. Feedback can make an unstable plant stable, and it can make a slow plant fast.

**What feedback costs.** Noise reaches the output through $T$, and $S + T = 1$ at each frequency, so $S$ and $T$ cannot both be small at one frequency. The loop is therefore designed with $|S|$ small at low frequencies, where references and disturbances live, and $|T|$ small at high frequencies, where the noise and the model errors are. Feedback can also destabilize a stable plant: the loop with $L(s) = k/(s(s + 1)(s + 2))$ is internally stable for $0 < k < 6$ and unstable for $k > 6$, because at $k = 6$ two closed-loop poles cross the imaginary axis at $\pm j\sqrt{2}$. The control signal $u = C S\,r + \ldots$ can be large when $|C S|$ is large, and actuators saturate. Feedback reacts only after an error appears; [feedforward control](/feedforward-control/) acts before, from a measured disturbance or a known reference.

## Examples

**Black's amplifier.** An amplifier with gain $A$ and a feedback network with gain $\beta$ has the closed-loop gain $A/(1 + A\beta)$. With $A = 10^5$ and $\beta = 0.01$ the gain is $99.90$. If the amplifier gain drops by half, to $A = 5 \cdot 10^4$, the closed-loop gain is $99.80$: a 50 percent change of $A$ gives a 0.1 percent change of the loop. The ratio of the two relative changes is close to $S = 1/(1 + A\beta) = 1/1001$. Black traded a large, unreliable gain for a smaller, precise one.

**A load disturbance on a first-order plant.** Let $P(s) = 1/(s + 1)$ (time constant 1 s, unit gain) and $C(s) = k$, a proportional controller. A unit step disturbance $d_o$ at the output gives $y(t) \to S(0) = 1/(1 + k)$. Without feedback the output moves by 1. With $k = 9$ it moves by 0.1. The closed-loop pole is at $s = -(1 + k) = -10$, so the loop is also ten times faster than the plant. A finite gain leaves an error; integral action in $C$ removes it (see [steady-state error](/steady-state-error/)).

**An unstable plant made stable.** Let $P(s) = 1/(s - 1)$ and $C(s) = k$. Then $\chi(s) = s - 1 + k$, and the loop is internally stable for every $k > 1$. A controller in series with the plant and without feedback cannot do this: the mode $e^{t}$ stays in the system, and any nonzero initial state of the plant makes it grow.

**A loop that looks stable and is not.** Let $P(s) = 1/(s - 1)$ and $C(s) = (s - 1)/(s + 1)$. Then $L = 1/(s + 1)$ and $T = 1/(s + 2)$, which is stable. But $P S = (s + 1)/((s - 1)(s + 2))$ has a pole at $s = 1$, and $\chi(s) = (s - 1)(s + 1) + (s - 1) = (s - 1)(s + 2)$. A small load disturbance makes the output grow like $e^t$. The controller zero cancels the unstable plant pole only in the formula for $T$.

## Where it is used

- Feedback loops are in process control, flight control, power electronics, disk drives, biology and economics. The [PID controller](/pid-controller/) is the most used controller in such loops.
- The analysis of a loop in the frequency domain uses the [sensitivity function](/sensitivity-function/), the [complementary sensitivity function](/complementary-sensitivity-function/), the [Nyquist stability criterion](/nyquist-stability-criterion/), and the [gain margin](/gain-margin/) and [phase margin](/phase-margin/).
- The time-domain view uses the [root locus](/root-locus/), the [step response specifications](/step-response-specifications/) and the [steady-state error](/steady-state-error/).
- The [internal model principle](/internal-model-principle/) says what a loop must contain to reject a class of disturbances in a robust way.
- State feedback $u = -K x$ is the multivariable form of the same idea; see [state feedback](/state-feedback/).

## References
