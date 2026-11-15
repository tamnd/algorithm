---
tag: CG1NCJ
kind: technique
slug: cascade-control
name: Cascade control
aliases:
- cascade loop
- master-slave control
area: control/classical-control
level: intro
summary: An inner loop controls a fast secondary variable and an outer loop sets its reference, so inner disturbances are rejected early.
prereqs: [feedback-control-loop, sensitivity-function]
see_also: [pid-controller, anti-windup, feedforward-control, internal-model-control, two-degree-of-freedom-control, relative-gain-array, integrator-windup, loop-shaping]
sources:
  - book: isbn:9781556179426
    title: Karl Johan Åström and Tore Hägglund, Advanced PID Control, ISA, 2006
    locator: Section 12.4, Cascade control
  - paper: doi:10.1016/S0959-1524(02)00062-8
    title: Sigurd Skogestad, Simple analytic rules for model reduction and PID controller tuning, Journal of Process Control 13(4) (2003) 291-309
    locator: the whole paper (the half rule and the SIMC settings used in the example)
---

Cascade control uses two feedback loops, one inside the other, with one actuator. The inner (secondary) loop measures a variable $y_2$ that the actuator moves quickly, such as a flow, a current or a speed, and holds it at a set point $r_2$. The outer (primary) loop measures the variable $y_1$ that really matters and computes $r_2$. A disturbance that acts on $y_2$ is then corrected by the fast inner loop before it reaches $y_1$. The inner loop also makes the outer loop see a simpler and more linear plant. The cost is a second sensor and a second controller to tune.

## In plain words

Think of a room heated by hot water. The room temperature changes slowly, and the water flow changes fast. If the pressure of the water supply drops, a single temperature controller sees nothing until the room has already cooled. With cascade control, a fast flow controller keeps the flow at its target and fixes the pressure drop in seconds. The temperature controller does not move the valve itself; it only says which flow it wants. Each controller then has a simpler job. The inner loop must be clearly faster than the outer loop, and it is tuned first. A second sensor is needed, and it must see the disturbance that you want to remove early.

## When it applies

- A second measurement $y_2$ exists between the actuator and the main output $y_1$, so that the plant is a series $y_1 = P_1 y_2$, $y_2 = P_2 (u + d_2)$.
- $P_2$ responds clearly faster than $P_1$.
- Important disturbances $d_2$ enter at the inner part, or the actuator is nonlinear (a valve, a motor), and the inner loop can hide this from the outer loop.
- Classic cases: a temperature controller that sets the set point of a steam or coolant flow controller; a level controller that sets a flow; the position, speed and current loops of a motor drive.

## The template

1. **Choose the inner variable.** It should react to the actuator fast and should see the disturbances to reject.
2. **Tune the inner loop first**, with the outer loop open. Often a P or PI controller with a high gain is enough, since a small offset in $y_2$ is corrected by the outer loop.
3. **Model the inner loop as closed.** With the inner loop closed, the outer loop sees $P_1 T_2$, where $T_2 = C_2 P_2/(1 + C_2 P_2)$. Often $T_2 \approx 1/(\tau_{c2} s + 1)$.
4. **Tune the outer loop** on $P_1 T_2$, for example with the SIMC rules or [internal model control](/internal-model-control/). A common rule of thumb asks for an inner loop 3 to 5 times faster than the outer loop.
5. **Handle the limits and the modes.** If the inner loop saturates or is in manual mode, the outer controller must track the measured $y_2$ instead of its own output, or it winds up; see [anti-windup](/anti-windup/). Close the inner loop first and open the outer loop first.

**Why it works (theorem).** Write $S_2 = 1/(1 + C_2 P_2)$ and $T_2 = 1 - S_2$. From $y_2 = P_2(u + d_2)$, $u = C_2(r_2 - y_2)$ and $r_2 = C_1(r - y_1)$:

$$y_2 = P_2 S_2 d_2 + T_2 r_2, \qquad y_1 = \frac{P_1 T_2 C_1}{1 + P_1 T_2 C_1} r + \frac{P_1 P_2 S_2}{1 + P_1 T_2 C_1} d_2.$$

Without the inner loop the factor $S_2$ is absent. So at the frequencies where the inner loop has high gain, $|S_2| \ll 1$ and the inner disturbance reaches the outer loop much reduced. A disturbance $d_1$ at the input of $P_1$ is not seen by $y_2$, and only the outer loop acts on it; there the gain from the cascade comes only from the faster outer loop that the simpler plant $P_1 T_2$ allows.

## Classic examples

**Two lags in series.** Let $P_2 = 1/(s + 1)$ (inner) and $P_1 = 1/(5s + 1)^2$ (outer), with a load $d_2$ at the input of $P_2$ and a load $d_1$ at the input of $P_1$. All controllers are PI with the SIMC rules and $\tau_c = \theta$ (Skogestad 2003).

- Single loop on $1/((s + 1)(5s + 1)^2)$. The half rule gives $\tau_1 = 5 + 2.5 = 7.5$ and $\theta = 2.5 + 1 = 3.5$, so $K_c = 7.5/7 = 1.0714$ and $T_i = 7.5$.
- Inner loop on $1/(s + 1)$ with $\tau_c = 0.25$: $K_c = 4$, $T_i = 1$, and $T_2 = 1/(0.25 s + 1)$ exactly.
- Outer loop on $1/((0.25 s + 1)(5s + 1)^2)$: $\tau_1 = 7.5$, $\theta = 2.75$, so $K_c = 7.5/5.5 = 1.3636$ and $T_i = 7.5$.

Measured with a simulation step of 0.01 s, for unit steps:

| structure | set point: overshoot, settling time (2 percent) | inner load $d_2$: peak of $y_1$, IAE | outer load $d_1$: peak of $y_1$, IAE |
|---|---|---|---|
| single loop | 0.088, 27.19 s | 0.4485, 7.0 | 0.454, 7.0 |
| cascade | 0.092, 23.11 s | 0.0146, 0.19 | 0.383, 5.5 |

The inner load is reduced by a factor of about 30 in peak, because the inner loop removes it early (the inner variable peaks at 0.157). The outer load is not seen by the inner loop, but the outer controller can be faster, and the IAE drops from 7.0 to 5.5. Both values equal $T_i/K_c$ of the controller that has to absorb the load (7.5/1.0714 and 7.5/1.3636), which is the theorem on the integral of the error for a PI loop with a unit load and no change of sign of the error.

## Variations

- **More than two levels.** Motor drives often use three: current, speed and position.
- **P control in the inner loop.** A P controller with a high gain is common in the inner loop; the outer integral removes the offset.
- **Feedforward into the inner loop.** A measured disturbance can enter $r_2$ or $u$ directly; see [feedforward control](/feedforward-control/).
- **Parallel cascade.** The disturbance or the actuator also acts on $y_1$ by a second path that does not pass through $y_2$. The design is similar, but the outer loop sees a different plant.
- **Ratio control.** The inner set point is a measured flow times a ratio that the outer loop adjusts, a common structure in process control.

## Pitfalls

- **An inner loop that is not faster.** If the two loops have similar speeds, they interact, and the model of the inner loop as a simple lag no longer holds. Retune the outer loop slower or make the inner loop faster.
- **Wrong tuning order.** Tuning the outer loop before the inner loop is closed, or tuning both loops with rules made for single loops without the inner loop model, can give an outer loop that does not converge. Tune the outer loop on $P_1 T_2$.
- **Windup of the outer loop.** When the inner loop saturates, or is in manual, the outer integral keeps growing. Feed the measured $y_2$ back as the tracking signal of the outer controller, and limit $r_2$ to values that the inner loop can reach.
- **The wrong inner variable.** If the main disturbance does not act on $y_2$, the cascade does little for it, as the outer load in the example shows.
- **Noise.** A fast inner loop with a high gain amplifies the noise of $y_2$ onto the actuator.

## Exercises

1. Show that the PI controller $K_c = 4$, $T_i = 1$ on $P_2 = 1/(s + 1)$ gives $T_2 = 1/(0.25 s + 1)$. (Answer: $C_2 P_2 = 4(s + 1)/s \cdot 1/(s + 1) = 4/s$, so $T_2 = 4/(s + 4)$.)
2. Use the half rule on $1/((0.25 s + 1)(5s + 1)^2)$. (Answer: keep one time constant 5, add half of the second, $\tau_1 = 7.5$; the delay is the other half plus 0.25, $\theta = 2.75$.)
3. Derive the map from $d_2$ to $y_1$ in the cascade. (Answer: $P_1 P_2 S_2/(1 + P_1 T_2 C_1)$.)
4. In the example, why is the IAE for the outer load 5.5 in the cascade? (Answer: the error has one sign, and its integral is $T_i/K_c = 7.5/1.3636 = 5.5$.)
5. A temperature loop sets the set point of a steam flow loop. Which disturbance does the cascade remove early, a change of the supply pressure of the steam or a change of the inlet temperature of the product? (Answer: the supply pressure, because it changes the flow, which the inner loop measures.)

## References
