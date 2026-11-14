---
tag: 5H7ZEG
kind: technique
slug: junction-voltage-limiting
name: Junction voltage limiting
aliases:
- pnjlim
- Newton step limiting in circuit simulation
area: eda/logic-and-circuit-simulation
level: advanced
summary: Limits the change of a diode or transistor junction voltage between Newton iterations, as SPICE does, so the exponential device law does not overflow or diverge.
prereqs: [newton-method-for-systems, dc-operating-point-analysis]
see_also: [gmin-stepping, source-stepping, pseudo-transient-analysis, modified-nodal-analysis, shichman-hodges-model, transient-circuit-analysis, kantorovich-theorem, homotopy-continuation]
sources:
  - paper: "Laurence W. Nagel, SPICE2: A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, Electronics Research Laboratory, University of California, Berkeley, 1975"
    title: Laurence W. Nagel, SPICE2, A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, University of California, Berkeley, May 1975
    locator: the chapter on the solution of nonlinear equations (Newton iteration and the limiting of junction voltages); the exact section was not checked
  - url: "https://sourceforge.net/p/ngspice/ngspice/ci/master/tree/src/spicelib/devices/devsup.c"
    title: ngspice source, src/spicelib/devices/devsup.c
    locator: the function DEVpnjlim, the limiting rule that ngspice keeps from SPICE3 (with a later change to the branch for reverse steps)
  - url: "https://sourceforge.net/p/ngspice/ngspice/ci/master/tree/src/spicelib/devices/dio/dioload.c"
    title: ngspice source, src/spicelib/devices/dio/dioload.c
    locator: the start of each junction at its critical voltage in the first iteration, the call of DEVpnjlim, and the count of limited devices that blocks convergence
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 4, Section 4.2.2 (Newton's method for circuits) and Section 4.4.1 (damping and limiting of the Newton step)
---

Junction voltage limiting changes Newton's method for the [DC operating point](/dc-operating-point-analysis/) so that the voltage across a pn junction never moves far up the exponential in one iteration. When Newton proposes a large forward step for a diode or transistor junction, the device is evaluated at a much smaller step, the one at which the true junction current equals the current that the linearized model predicted. It is a technique of the circuit simulation half of the logic and circuit simulation sub-area, and the rule that SPICE uses, the function pnjlim, comes from Nagel's SPICE2 of 1975.

## In plain words

A diode passes almost no current until its voltage reaches about 0.7 V, and then its current grows very fast: about ten times for each extra 60 mV. Newton's method replaces the diode by a straight line at the present guess and solves the circuit. Far below the bend, that line is almost flat, so the next guess can be several volts, where the true diode current is larger than any number a computer can hold.

Limiting does not trust that guess. It asks what current the straight line promised, and it moves the diode voltage only as far as needed to give that current. Large proposed jumps then become small, safe ones, and the guess walks up the bend in a few steps instead of jumping over it.

## When it applies

Use it inside Newton's method, for DC analysis and for every time step of [transient circuit analysis](/transient-circuit-analysis/), whenever an element law grows exponentially with a voltage: diodes, the base-emitter and base-collector junctions of bipolar transistors, and the bulk junctions of MOS transistors. SPICE has related rules for other device voltages, for example a rule for the gate voltage of MOS transistors (fetlim) and one for the drain voltage (limvds); those rules are heuristics of a different form. Limiting acts on device voltages, not on node voltages, so it needs no change to the [MNA](/modified-nodal-analysis/) solver.

## The template

Let a junction have the law $i(v) = I_s (e^{v/V_t} - 1)$ with saturation current $I_s$ and thermal voltage $V_t$, and let $u$ be the junction voltage at which the device was evaluated in the last iteration. Newton solves the circuit with the junction replaced by its tangent at $u$,

$$i \approx i(u) + g(u)\,(v - u), \qquad g(u) = i'(u) = \frac{I_s e^{u/V_t}}{V_t},$$

and the solution gives a new junction voltage $v$. Limiting replaces $v$ by a value $\tilde v$ before the device is evaluated again.

```pseudo id=main
NEWTON-WITH-LIMITING(circuit, x)
L1  repeat
L2      limited ← false
L3      for each junction k do
L4          v ← the junction voltage of k computed from x
L5          (ṽ, changed) ← LIMIT(v, u_k)                ▷ hole: the limiting rule, PNJLIM below
L6          u_k ← ṽ; limited ← limited or changed
L7          stamp the tangent of the device law of k at u_k into the MNA matrix
L8      x_new ← the solution of the linearized MNA system
L9      done ← (x_new is close to x) and not limited
L10     x ← x_new
L11 until done
L12 return x
```

The limiting rule of SPICE3 for a pn junction, with the critical voltage $V_{\text{crit}} = V_t \ln\big(V_t / (\sqrt{2}\, I_s)\big)$:

```pseudo id=pnjlim
PNJLIM(v, u, V_t, V_crit)
L1  if v > V_crit and |v − u| > 2 V_t then
L2      if u > 0 then
L3          a ← 1 + (v − u) / V_t
L4          if a > 0 then v ← u + V_t ln a
L5          else v ← V_crit
L6      else v ← V_t ln(v / V_t)
L7      return (v, true)
L8  return (v, false)
```

Line L9 of the main loop is the rule of SPICE: an iteration in which any device was limited does not count as converged, because its device currents are not those of the computed node voltages.

**The rule keeps the promised current.** *Claim.* For $u > 0$ and $a = 1 + (v - u)/V_t > 0$, the value $\tilde v = u + V_t \ln a$ of line L4 is the unique voltage at which the true junction current equals the value at $v$ of the tangent at $u$: $i(\tilde v) = i(u) + g(u)(v - u)$. *Proof.* Since $i + I_s = I_s e^{v/V_t}$ and $g(u) = (i(u) + I_s)/V_t$, the right side plus $I_s$ is $(i(u) + I_s)(1 + (v - u)/V_t) = I_s e^{u/V_t} a$. Setting $I_s e^{\tilde v/V_t} = I_s e^{u/V_t} a$ gives $\tilde v = u + V_t \ln a$, and the exponential is one to one. $\blacksquare$

So the limited step is a Newton step on the junction current instead of the junction voltage, mapped back through the device law. Because $\ln(1 + y) < y$ for $y > 0$, a forward step always shrinks: $0 < \tilde v - u < v - u$. It shrinks a lot: a proposed step of 10 V from $u = 0.5$ V with $V_t = 25.85$ mV becomes $V_t \ln(1 + 10/V_t) \approx 0.154$ V. The new device current is the current that the linear system already produced, so it is finite, and one iteration cannot overflow the exponential.

**The other branches.** Line L5 handles a large backward step from a point above $V_{\text{crit}}$: $a \le 0$ means the tangent promises a current of at most $-I_s$, which no voltage gives, so the rule falls back to $V_{\text{crit}}$. Line L6 handles a forward step from a junction that is off ($u \le 0$): it is line L4 with $u = 0$ and $1 + v/V_t$ replaced by $v/V_t$, almost equal when $v > V_{\text{crit}} \gg V_t$.

**Why $V_{\text{crit}}$.** The curve $i = I_s e^{v/V_t}$ bends most sharply at $V_{\text{crit}}$. *Proof.* The curvature of the graph is $\kappa = i'' / (1 + i'^2)^{3/2}$ with $i' = s$ and $i'' = s/V_t$, where $s = i/V_t$. As a function of $s$, $\kappa = (s/V_t)(1 + s^2)^{-3/2}$ has derivative proportional to $(1 + s^2) - 3s^2$, which is zero at $s = 1/\sqrt 2$. So the curvature is largest where $I_s e^{v/V_t} = V_t/\sqrt 2$, that is at $v = V_t \ln(V_t/(\sqrt 2 I_s))$. $\blacksquare$ Below the bend the law is almost flat and Newton steps are harmless; above it the law is almost vertical and the rule acts. The curvature depends on the units of the axes, so the bend is a choice tied to volts and amperes, not a property of the device. For $I_s = 10^{-14}$ A and $V_t = 25.852$ mV, $V_{\text{crit}} \approx 0.7299$ V.

**What is proved and what is measured.** The claims above are exact. If the limited iteration converges and no device is limited in the last iteration, the last step is a plain Newton step with a zero update, so the limit solves the circuit equations. Nothing more is proved in general: limiting can make the iteration cycle, and no global convergence theorem for Newton with pnjlim on general circuits is known to us. The local quadratic rate of Newton, with its [Kantorovich](/kantorovich-theorem/) conditions, still holds near a solution, because the rule acts only on steps larger than $2V_t$.

**Measured on one circuit.** A source $E$ drives a diode through $1\ \text{k}\Omega$, with $I_s = 10^{-14}$ A and $V_t = 25.852$ mV. Iterations of Newton until the update is below $10^{-9}$ relative:

| $E$ | solution $v$ | plain, from 0 V | limited, from 0 V | plain, from $V_{\text{crit}}$ | limited, from $V_{\text{crit}}$ |
|---|---|---|---|---|---|
| 5 V | 0.69254 V | 173 | 12 | 6 | 6 |
| 20 V | 0.73127 V | overflow | 8 | 4 | 4 |
| 100 V | 0.77364 V | overflow | 8 | 9 | 4 |

From 0 V the first plain step puts nearly all of $E$ on the diode. At 5 V the iteration then walks back down the exponential by about $V_t$ per step; at 20 V the next evaluation needs $e^{20/V_t} = e^{774}$, beyond the largest double. With limiting, the first step from 0 V is $V_t \ln(E/V_t)$ by line L6 and later steps grow by about $V_t \ln(E/V_t)$ each until the bend. SPICE starts every junction at $V_{\text{crit}}$, which explains the last two columns.

## Classic examples

- The diode and bipolar models of SPICE call pnjlim on every junction voltage in every Newton iteration, in DC and in [transient analysis](/transient-circuit-analysis/).
- The MOS models of SPICE limit the bulk junction voltages with pnjlim and the gate and drain voltages with fetlim and limvds; the [Shichman-Hodges model](/shichman-hodges-model/) is the device law that they protect in Level 1.
- When limiting alone fails, simulators fall back on [gmin stepping](/gmin-stepping/), [source stepping](/source-stepping/) and [pseudo-transient analysis](/pseudo-transient-analysis/), and each of these still uses limiting inside its Newton runs.

## Variations

- **Damped Newton.** Scale the whole update by a factor in $(0, 1]$, chosen so that the residual norm falls. It acts on all unknowns, while pnjlim acts on each device separately; damping has a global theory for line searches on a merit function, limiting has none.
- **Fixed voltage clamp.** Bound every change of a node voltage, for example by $1$ V. It is simple but slows convergence on circuits with large voltage swings.
- **Current iteration.** Iterate on the junction current and recover the voltage from $v = V_t \ln(1 + i/I_s)$. The claim above shows that pnjlim's forward branch is this idea applied one step at a time.
- **Modified reverse rule.** Current ngspice changes the branch for steps from a reverse-biased or off junction; the forward rule of line L4 is unchanged.

## Pitfalls

- **Convergence test.** An iteration whose devices were limited must not be accepted, as line L9 does; otherwise the reported currents do not match the reported voltages.
- **Units.** $V_{\text{crit}}$ comes from a curvature that depends on units. With currents in milliamperes the bend moves, so the formula must be used with volts and amperes, as SPICE does.
- **Large reverse steps.** The rule does not act on downward steps above $V_{\text{crit}}$ unless $a \le 0$, so a junction can still swing far into reverse bias; that is safe for the exponential but can slow convergence.
- **Cycling.** Limiting can stop Newton from overflowing and still not converge; the simulator then needs one of the continuation methods above.

## Exercises

1. Show that for $u > 0$ and $d = v - u > 0$, the limited step $\tilde v - u$ of line L4 is less than $d$, and that $\tilde v - u - V_t \ln(d/V_t) \to 0$ as $d \to \infty$.
2. Compute $V_{\text{crit}}$ for $I_s = 10^{-16}$ A and $V_t = 25.852$ mV, and the first limited step from $u = 0$ when Newton proposes $v = 3$ V.
3. For the circuit of the table with $E = 5$ V and plain Newton from 0 V, explain why each iteration after the first lowers $v$ by about $V_t$, and estimate the number of iterations.
4. Give a circuit in which the voltage of a junction is limited in every iteration, so that the test of line L9 never passes, and propose a fix.

## References
