---
tag: XXGWGN
kind: technique
slug: mixed-mode-simulation
name: Mixed-mode simulation
aliases:
- mixed-signal simulation
- analog and digital co-simulation
area: eda/logic-and-circuit-simulation
level: advanced
summary: Simulates analog parts by numerical integration and digital parts by events in one run, passing signals across converters at the boundaries.
prereqs: [event-driven-logic-simulation, transient-circuit-analysis]
see_also: [timing-simulation, event-driven-logic-simulation, transient-circuit-analysis, companion-model, modified-nodal-analysis, iterated-timing-analysis, chandy-misra-bryant, time-warp]
sources:
  - paper: "A. Richard Newton, The simulation of large-scale integrated circuits, Memorandum UCB/ERL M78/52, Electronics Research Laboratory, University of California, Berkeley, July 1978"
    title: A. R. Newton, The simulation of large-scale integrated circuits, UCB/ERL M78/52, July 1978
    locator: the PhD work that describes the SPLICE program, with logic and electrical simulation in one event-driven framework (general locator)
  - paper: "A. Richard Newton, Techniques for the simulation of large-scale integrated circuits, IEEE Transactions on Circuits and Systems CAS-26(9), 741 to 749, 1979"
    title: A. Richard Newton, Techniques for the simulation of large-scale integrated circuits, IEEE Transactions on Circuits and Systems CAS-26(9), 741 to 749, 1979
    locator: the event-driven scheduling of electrical and logic nodes, the selective trace, and the interface between the logic and the electrical parts of a circuit
  - paper: doi:10.1109/TCS.1975.1084003
    title: B. R. Chawla, H. K. Gummel and P. Kozak, MOTIS, an MOS timing simulator, IEEE Transactions on Circuits and Systems CAS-22(12), 901 to 910, 1975
    locator: the timing simulation of MOS circuits, node by node with simple device models, which serves as a fast analog engine (general locator)
---

Mixed-mode simulation runs one design in which some parts are simulated as electrical circuits, with node voltages that change continuously, and other parts as logic, with values such as 0, 1 and X that change at events. The technique joins the two halves of the sub-area. The analog parts use the circuit half: [modified nodal analysis](/modified-nodal-analysis/), [companion models](/companion-model/) and Newton's method, or a faster [timing simulation](/timing-simulation/). The digital parts use the logic half: [event-driven logic simulation](/event-driven-logic-simulation/) with nominal gate delays and an inertial or transport delay model. At each boundary a converter turns a voltage into a logic value or a logic value into a voltage, and a scheduler keeps the two time axes in step. This gives the accuracy of circuit simulation where it is needed, for example in a comparator or a phase-locked loop, at the speed of logic simulation elsewhere. Newton's SPLICE program (UCB/ERL memorandum M78/52, 1978, and IEEE Transactions on Circuits and Systems, 1979) put logic and electrical nodes in one event-driven scheduler.

## In plain words

Some parts of a chip need exact voltages, such as an amplifier or a converter. Other parts are plain logic, and 0 and 1 are enough for them. Simulating everything as voltages is slow. Simulating everything as logic misses what the analog parts do.

So the simulator splits the design. The analog parts are solved in small time steps. The logic parts only wake up when something changes.

Where the two parts meet, a translator stands in between. When an analog voltage passes a threshold, it tells the logic part that the wire is now 1 or 0. When a logic output changes, it drives the analog wire up or down with a short slope.

The hard part is the clock of each side. Neither side may run ahead and miss a change that the other side makes.

## When it applies

- The design has a small analog part and a large digital part that talk to each other: a phase-locked loop, an analog-to-digital converter with its control logic, a sense amplifier with its memory array, or an I/O buffer with its core logic.
- The question is about the interaction: does the loop lock, does the converter give the right code, does the sense amplifier fire after the bit line has moved far enough. A pure logic model of the analog part, or a pure circuit model of the whole design, does not answer it at an acceptable cost.
- The digital part can be modeled with a value set and a delay model, as in [logic simulation](/logic-simulation/). The analog part can be written as a set of node equations that a transient solver can integrate.

## The template

The design is split into an analog part $A$, with node voltages $v(t)$, and a digital part $D$, with nets and gates. Each boundary net has a converter. The template has five holes.

1. **H1, the analog engine.** It advances $v$ from $t$ to $t + h$. It can be full [transient circuit analysis](/transient-circuit-analysis/), with an integration formula, Newton's method and a sparse solve, or a [timing simulation](/timing-simulation/) or [iterated timing analysis](/iterated-timing-analysis/) step.
2. **H2, the digital engine.** It applies the events of one time, with all their [delta cycles](/delta-cycle/), and schedules new events. It is an event-driven simulator with a delay model.
3. **H3, the A/D rule.** For an analog node read by a gate: the value is 0 below $V_{IL}$, 1 above $V_{IH}$, and either X or the last value in between. A crossing makes a digital event, possibly after a converter delay.
4. **H4, the D/A rule.** For a net that drives an analog node: a change from 0 to 1 starts a voltage ramp from 0 to $V_{DD}$ over a rise time $t_r$, applied through an output resistance. A change to Z opens the source. A change to X has no single voltage; a common choice is the midpoint, with a warning.
5. **H5, the synchronization rule.** The order in which the two engines advance. The template below is the conservative rule: the analog engine never steps past the next digital event, and the digital engine never handles an event later than the analog time.

```pseudo id=main
MIXED(A, D, t_end)
L1  set the digital nets to their initial values and find the analog operating point with the D/A sources at those values
L2  t ← 0
L3  while t < t_end do
L4      t_d ← the time of the next digital event, or ∞ if there is none
L5      h ← the step that H1 asks for, cut so that t + h ≤ min(t_d, t_end)
L6      take one analog step from t to t + h (hole H1), with the D/A sources of H4
L7      if a node read by H3 crossed a threshold in (t, t + h] then
L8          t_c ← the earliest crossing time in the step, by interpolation
L9          take the step again from t to t_c, so that the analog time equals the event time
L10         schedule the digital event of H3 at t_c plus the converter delay
L11         t ← t_c
L12     else t ← t + h
L13     apply all digital events at time t (hole H2); for each D/A net that changed, start its ramp at t (hole H4)
L14 return the analog waveforms and the digital events
```

**What the template keeps exact.** Two properties hold whatever H1 to H4 are.

- *No missed source change.* Line L5 ends every analog step at or before the next digital event. So during a step, every D/A source follows a known ramp that started at or before the start of the step, and H1 integrates the right equations.
- *Causality.* No event is ever scheduled at a time earlier than the present time of either engine. *Proof.* A digital event comes either from a gate, at the present time plus a delay of at least 0, or from line L10, at $t_c$ plus a delay of at least 0. After line L9 the analog time is $t_c$, and the digital engine has handled only events up to the old $t \le t_c$. So both engines are at most at the new event time, and a step of either engine never has to be undone. $\square$

What is not exact is the analog solution itself and the crossing time, which carry the error of the integration formula of H1 and of the interpolation at line L8.

**Cost.** Each digital event that changes a D/A source cuts the current analog step, and each threshold crossing costs one extra analog step at line L9. So a design with frequent digital activity at the boundary forces small analog steps, even if the analog part changes slowly. The digital part costs what event-driven simulation costs.

**Example.** A digital inverter drives an analog RC load, $R = 1\ \mathrm{k\Omega}$ and $C = 1$ pF, so $\tau = RC = 1$ ns, and a gate reads the capacitor node with a single threshold at $V_{DD}/2$, $V_{DD} = 1$ V. The inverter output rises at $t = 0$ with an ideal step. The exact node voltage is $v(t) = 1 - e^{-t/\tau}$, and it crosses 0.5 V at $\tau \ln 2 = 0.6931$ ns. With backward Euler as H1, the crossing time found by linear interpolation between steps is:

| step $h$ (ns) | end of the crossing step | interpolated crossing | error (ns) |
|---|---|---|---|
| 0.25 | 1.0000 | 0.7793 | +0.0861 |
| 0.1 | 0.8000 | 0.7282 | +0.0351 |
| 0.05 | 0.7500 | 0.7105 | +0.0174 |
| 0.025 | 0.7250 | 0.7018 | +0.0086 |
| 0.0125 | 0.7000 | 0.6975 | +0.0043 |

The error halves with $h$, the first-order behavior of backward Euler, and is much smaller than the error of putting the event at the end of the step, which can be as large as $h$. Line L9 then takes one step from the last accepted point to the crossing; with $h = 0.1$ ns, the step that lands on 0.5 V ends at 0.7263 ns. With a D/A ramp of $t_r = 0.2$ ns in place of the ideal step, the exact crossing moves to 0.7948 ns, later by about $t_r / 2$. A script computed every number in this paragraph.

## Classic examples

- **SPLICE.** Newton's program (1978, 1979) handled logic gates, and electrical nodes solved by timing simulation, in one event-driven scheduler with selective trace: a node, electrical or logic, was processed only when one of its inputs had changed. This is the template with H1 a timing simulation step, H5 one shared event queue, and the converters at the boundary between the two kinds of nodes.
- **Timing simulation as the analog engine.** The node-by-node method of MOTIS (Chawla, Gummel and Kozak 1975), described on the [timing simulation](/timing-simulation/) page, can skip nodes that do not change, so it fits an event-driven scheduler better than a full Newton solve of all nodes at each step.
- **Phase-locked loop.** The phase detector and the divider are logic, and the charge pump, loop filter and oscillator are analog. The divider output is a D/A net, and the oscillator output goes through an A/D converter to the divider. Each oscillator period makes two crossings, so the analog step is cut twice per period.
- **Successive-approximation converter.** The comparator and the capacitor array are analog; the register that holds the trial code is logic. Each comparison is an A/D event, and each new trial bit is a D/A event.

## Variations

- **One engine with mixed models.** A single simulator holds both kinds of node in one data structure and one time axis, as SPLICE did. The boundary is cheap, but the simulator must contain both engines.
- **Co-simulation of two simulators.** A circuit simulator and a logic simulator run as separate programs and exchange events through an interface. The conservative rule of the template is the [Chandy-Misra-Bryant](/chandy-misra-bryant/) idea applied to two processes. An optimistic rule lets each simulator run ahead, saves its state, and rolls back when an event from the other side arrives in its past, as in [Time Warp](/time-warp/). Rolling back an analog solver means keeping its earlier states, which costs memory.
- **Relaxation across the boundary.** The analog part can be solved by [iterated timing analysis](/iterated-timing-analysis/), which treats each node or component on its own and fits the event-driven scheme, since an inactive analog node is not solved again.
- **Hysteresis in H3.** Two thresholds, $V_{IL} < V_{IH}$, with the last value kept in between, stop a slow or noisy analog edge from making a burst of digital events.
- **Behavioral analog models.** The analog part can be written as equations in a hardware description language for analog behavior, in place of a transistor netlist. The template stays the same; only H1 changes.

## Pitfalls

- **Events at the end of the step.** Putting a crossing at $t + h$ instead of at the interpolated time adds an error of up to $h$ to every A/D event. In a loop such as a phase-locked loop, this error appears as phase noise that the real circuit does not have.
- **Ideal steps from D/A converters.** A zero rise time makes the analog equations jump. The solver must restart with a tiny step, Newton's method may fail, and the coupling capacitances spread the jump to other nodes. Give every D/A converter a finite rise time and an output resistance.
- **X and Z at the boundary.** An analog node has a voltage, never X. An X on a D/A net must become some voltage, and every choice can hide a bug. Between the thresholds, an A/D converter that reports X makes the digital part pessimistic, and one that keeps the last value can be optimistic.
- **Zero-delay loops through the boundary.** If an A/D event changes a D/A source through gates of zero delay, the analog step must end at the crossing time, as line L9 does. A simulator that keeps the full step uses a source value that is wrong for part of the step.
- **Partitioning.** A node that a designer puts in the digital part because it "is logic", such as a weak keeper or a dynamic node that shares charge, can need the analog engine. The partition is a modeling choice, and the results are only as good as it is.
- **Comparing with full circuit simulation.** The digital part has the delays of its delay model, not those of the transistors. A check of mixed-mode results against a full transistor-level transient run of a small case is the only way to measure the error of the partition.

## Exercises

1. For the RC example, show that backward Euler with step $h$ gives $v_n = 1 - (1 + h/\tau)^{-n}$, and find the first step $n$ with $v_n \ge 0.5$ for $h = 0.1$ ns. Check that the step ends at 0.8 ns.
2. Prove that for a linear circuit driven by a ramp of rise time $t_r$, the response after $t_r$ is the average of the step response over a window of width $t_r$, and so the crossing moves by about $t_r / 2$ when the response is close to linear in that window.
3. A ring of three inverters has one stage simulated as an analog circuit and two as logic gates of delay $d$. Write down the sequence of events and analog steps for one period with the template, and say how many times line L9 runs per period.
4. Give an example in which an optimistic co-simulation rolls back the analog engine, and estimate the memory needed to keep its states for a rollback over $k$ steps of a circuit with $n$ nodes.

## References
