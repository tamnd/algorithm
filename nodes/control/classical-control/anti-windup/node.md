---
tag: NFWJA3
kind: technique
slug: anti-windup
name: Anti-windup
aliases:
- anti-windup compensation
- back-calculation
area: control/classical-control
level: core
summary: Stops or bleeds the integrator of a controller while the actuator saturates, by conditional integration or by feeding back the saturation error.
prereqs: [feedback-control-loop, steady-state-error]
see_also: [integrator-windup, pid-controller, cascade-control, internal-model-control, reference-governor, model-predictive-control, circle-criterion, small-gain-theorem]
sources:
  - paper: doi:10.23919/ACC.1989.4790464
    title: Karl Johan Åström and Lars Rundqwist, Integrator windup and how to avoid it, Proceedings of the 1989 American Control Conference, 1693-1698
    locator: the whole paper (conditional integration, tracking with back-calculation and the observer view)
  - paper: doi:10.1016/0005-1098(94)90048-5
    title: Mayuresh V. Kothare, Peter J. Campo, Manfred Morari and Carl N. Nett, A unified framework for the study of anti-windup designs, Automatica 30(12) (1994) 1869-1883
    locator: the whole paper (the known anti-windup schemes as special cases of one structure)
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: Chapter 3, PID Control (the section on integrator windup); Section 13.3, Computer implementations
---

Anti-windup is the set of methods that keep the integral of a controller in line with what the actuator really does. When the actuator is at a limit, the loop is in effect open, and an unprotected integral grows without bound; this is [integrator windup](/integrator-windup/). An anti-windup method either stops the integration while the actuator saturates (conditional integration) or drives the integral so that the controller output tracks the limited actuator signal (tracking, with back-calculation as its usual form). Inside the limits the methods change nothing, so the linear design still holds. Every [PID controller](/pid-controller/) used on a real plant needs one of them.

## In plain words

A controller with an integral term keeps a memory of the past error. When the actuator is fully open and cannot do more, this memory should not keep growing, because the growth has no effect now and causes a large overshoot later. Anti-windup tells the controller what the actuator really did. One way is simple: stop adding to the memory while the actuator is at its limit and the error pushes further out. The other way compares what the controller asked for with what the actuator gave, and uses the difference to pull the memory back, so the request stays close to the limit. When the actuator is not at a limit, both ways do nothing. The time that the pull-back takes is a tuning knob.

## When it applies

- The controller has integral action, or other states that integrate or drift, and the actuator has a limit on its range or its rate.
- The limits are reached in normal operation: large set-point changes, start-up, large loads, or a manual mode.
- The controller can know the actuator signal $u$ that the plant really gets, by a model of the limits in the controller or by a measurement of the actuator position.
- The linear design is fine inside the limits. Anti-windup repairs the behaviour at the limits; it does not fix a loop that is too fast or a set point that the actuator cannot reach.

## The template

1. **Model the limit.** Write the controller output before the limit as $v$ and the actuator signal as $u = \operatorname{sat}(v)$, with the same limits as the real actuator. If the actuator has its own limits that the controller cannot know exactly, measure $u$.
2. **Choose the method.** For a PI or PID controller $v = K(b r - y) + I + D$:
   - *Back-calculation (tracking).* Let the integral follow
     $$I' = \frac{K}{T_i} e + \frac{1}{T_t} (u - v).$$
     Inside the limits $u = v$ and the second term is 0.
   - *Conditional integration.* Integrate only when $u = v$, or when the error drives $v$ back toward the limits: $I' = (K/T_i) e$ if $u = v$ or $e (v - u) < 0$, else $I' = 0$.
3. **Choose the tracking time $T_t$.** A small $T_t$ resets the integral fast. A large $T_t$ acts like no protection. Åström and Hägglund give the rule of thumb $T_t = \sqrt{T_i T_d}$, with $T_t$ between $T_d$ and $T_i$ (a rule of thumb, not a theorem). For a PI controller, a value below $T_i$ is common.
4. **Sample it.** With the period $h$:
   $$I_{k+1} = I_k + \frac{K h}{T_i} e_k + \frac{h}{T_t} (u_k - v_k).$$
   This is the form of the [PID controller](/pid-controller/) page. Keep $h/T_t \le 1$ (see below).
5. **Check it.** Simulate a large set-point step and a large load with the actuator limits, and compare the overshoot and the settling time with and without the protection.

**Why it works (theorems).** Inside the limits $u = v$, so both methods give the linear controller and the linear analysis holds unchanged. Under saturation, hold $e$ and $u$ constant. Back-calculation then has the fixed point where $(K/T_i) e + (u - v)/T_t = 0$, that is

$$v = u + \frac{T_t K}{T_i} e,$$

which it approaches with the time constant $T_t$. So $v$ stays within $T_t K |e|/T_i$ of the limit instead of running away, and the controller leaves the limit soon after the error changes sign. In the sampled form the integral obeys $I_{k+1} = (1 - h/T_t) I_k + c$ with a constant $c$ while $e$, $u$ and the other terms are held. This converges if and only if $0 < h/T_t < 2$, and without a change of sign of $I_{k+1} - I_k$ if and only if $h/T_t \le 1$. Conditional integration holds $I$ constant under saturation, so it cannot wind up at all.

**What is not proved here.** Both methods keep the integral bounded under saturation, but neither guarantees that the loop with the limits converges for every set point and load. Analysis of the loop with the saturation uses tools such as the [circle criterion](/circle-criterion/) and the [small gain theorem](/small-gain-theorem/); Kothare et al. (1994) show that the common schemes are special cases of one structure, which makes this analysis uniform.

## Classic examples

**An integrator plant.** Let $y' = u$, with the PI controller $K = 1$, $T_i = 1$, the limits $|u| \le 1$ and a set-point step to $r = 10$. The [integrator windup](/integrator-windup/) page works out the case without protection by hand: the integral reaches 50 at $t = 10$ s, and the actuator stays at its limit until $t = 9 + \sqrt{99} = 18.95$ s. Measured with a simulation step of 0.001 s:

| method | peak of $y$ | settling time (2 percent) |
|---|---|---|
| no protection | 19.002 | 62.3 s |
| back-calculation, $T_t = 1$ s | 10.546 | 12.75 s |
| back-calculation, $T_t = 0.5$ s | 10.350 | 12.48 s |
| back-calculation, $T_t = 0.1$ s | 10.300 | 12.40 s |
| conditional integration | 10.298 | 12.40 s |

With $T_t = 1$ the integral follows $I' = e + (1 - (e + I)) = 1 - I$ during saturation, so it rises toward 1 and never passes it. With conditional integration the integral stays 0 while $u = 1$, so $v = e = 10 - y$ and the actuator leaves the limit at $y = 9$, at $t = 9$ s.

**A third order lag with a PID controller.** Take $P(s) = 1/(s + 1)^3$, the Ziegler-Nichols PID $K = 4.8$, $T_i = 1.8138$ s, $T_d = 0.45345$ s with the derivative filter $N = 10$, the sampling period $h = 0.05$ s, a unit set-point step and the limits $|u| \le 2$. The rule $T_t = \sqrt{T_i T_d}$ gives 0.907 s. The numbers are measurements; IAE is the integral of $|e|$ over 40 s.

| method | overshoot | settling time (2 percent) | IAE |
|---|---|---|---|
| no limits | 0.550 | 9.72 s | 2.304 |
| limits, no protection | 0.569 | 9.96 s | 3.164 |
| back-calculation, $T_t = 0.1$ s | 0.019 | 6.18 s | 1.888 |
| back-calculation, $T_t = 0.3$ s | 0.035 | 7.71 s | 1.890 |
| back-calculation, $T_t = 0.907$ s | 0.162 | 8.38 s | 2.054 |
| back-calculation, $T_t = 2$ s | 0.300 | 8.89 s | 2.344 |
| back-calculation, $T_t = 5$ s | 0.431 | 9.38 s | 2.695 |
| conditional integration | 0.076 | 7.99 s | 1.924 |

A smaller $T_t$ helps on this plant, and the rule of thumb is far from the best value here. As $T_t$ grows, the result moves toward the case without protection. With protection the loop even does better than the loop without limits, because the limit cuts the large first push of the aggressive Ziegler-Nichols tuning and the integral does not pay for it later.

## Variations

- **Conditional integration (clamping).** Stop the integral when the actuator is at a limit, or only when the error would drive it further. Some versions also stop it when the error is large. It needs no extra parameter.
- **Back-calculation (tracking).** Feed $u - v$ back into the integral with the gain $1/T_t$, as in the template. The same input can carry a manual value of $u$, which gives bumpless transfer from manual to automatic mode.
- **Velocity form.** A controller that computes the change $\Delta u_k$ and adds it to the last actuator value cannot wind up if it adds to the limited value. The integral is implicit in the sum.
- **Observer form for general controllers.** Write a controller with integral action as an observer of the plant state and feed it the limited $u$, so its states follow the plant that really runs. This works for state space controllers, not only PID.
- **Unified and model-based designs.** Kothare et al. (1994) write the known schemes as one structure with a gain on $u - v$. Later designs choose this gain to guarantee properties of the loop with the saturation.
- **Avoid the limit.** Ramp the set point, or use a [reference governor](/reference-governor/), so that the actuator does not saturate. [Model predictive control](/model-predictive-control/) puts the limits into the optimization.
- **Cascade loops.** When an inner loop of a [cascade](/cascade-control/) saturates, the outer controller tracks the measured value of the inner set point, which is the same idea one level up.

## Pitfalls

- **Wrong limits in the controller.** If the limits in the controller are wider than those of the actuator, the controller sees $u = v$ while the actuator saturates, and windup comes back. Use the true limits, or measure $u$.
- **$T_t$ too small for the sampling period.** In the sampled form a value $h/T_t > 1$ makes the integral overshoot its fixed point at each sample, and $h/T_t \ge 2$ makes it diverge.
- **$T_t$ too small with noise.** Noise that drives $v$ over a limit for one sample resets the integral by back-calculation. A larger $T_t$ filters this.
- **Rate limits.** A valve with a limited speed saturates in rate, not in range. The model of the limit must include the rate limit, or the protection does not act.
- **Derivative and set-point weights.** The limit acts on the sum $v$, so a large derivative kick or a large proportional step can push $v$ to a limit for a short time. That is not windup, but it can trigger the protection.
- **An unreachable set point.** If the actuator cannot hold the output at the set point, no anti-windup method removes the error. It only keeps the controller ready to act when the set point becomes reachable.

## Exercises

1. In the integrator example without protection, compute $I(10)$. (Answer: $\int_0^{10} (10 - t)\, dt = 50$.)
2. Show that back-calculation with $e$ and $u$ held has the fixed point $v = u + T_t K e/T_i$, and that $I$ approaches it with the time constant $T_t$. (Answer: $I' = (K/T_i) e + (u - v)/T_t$ and $v = K e + I$, so $I' = -(I - I^*)/T_t$ with $I^* = u - K e + T_t K e/T_i$.)
3. For the sampled form with $h = 0.05$ s, for which $T_t$ does the integral converge under saturation without a change of sign of its steps? (Answer: $h/T_t \le 1$, so $T_t \ge 0.05$ s.)
4. In the integrator example with conditional integration, when does the actuator leave the limit? (Answer: $I = 0$, so $v = 10 - y = 1$ at $y = 9$, at $t = 9$ s.)
5. In the integrator example with back-calculation and $T_t = 1$ s, what value does $I$ approach during the saturation? (Answer: $I' = 1 - I$, so $I \to 1$.)

## References
