---
tag: VV7FPS
kind: model
slug: transition-fault-model
name: Transition fault model
aliases:
- transition delay fault
- slow-to-rise and slow-to-fall faults
area: eda/test-and-diagnosis
level: core
summary: A fault model in which one node is slow to rise or slow to fall, tested by a two-pattern test that launches the transition and captures it after one clock.
prereqs: [stuck-at-fault-model]
see_also: [path-delay-fault-model, launch-on-capture-and-launch-on-shift, scan-design, ppsfp, static-timing-analysis, fault-coverage, robust-path-delay-test, bridging-fault-model]
sources:
  - paper: "J. A. Waicukauski, E. Lindbloom, B. K. Rosen and V. S. Iyengar, Transition fault simulation by parallel pattern single fault propagation, Proceedings of the International Test Conference, 542 to 549, 1986"
    title: J. A. Waicukauski, E. Lindbloom, B. K. Rosen and V. S. Iyengar, Transition fault simulation by parallel pattern single fault propagation, Proceedings of the International Test Conference, 542 to 549, 1986
    locator: the slow-to-rise and slow-to-fall faults, their two-pattern tests, and their simulation with PPSFP
  - paper: doi:10.1109/MDT.1987.295104
    title: J. A. Waicukauski, E. Lindbloom, B. K. Rosen and V. S. Iyengar, Transition fault simulation, IEEE Design and Test of Computers 4(2), 32 to 38, 1987
    locator: the journal version of the transition fault model and its simulation
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Delay Test (transition faults, two-pattern tests and their relation to path delay faults)
---

The transition fault model describes a timing defect as one line of a circuit that is too slow to change its value. Each line has two faults: slow to rise, where a change from 0 to 1 arrives too late, and slow to fall, where a change from 1 to 0 arrives too late. The delay is assumed large enough that the late value misses the clock edge whatever path the change takes to an output. A test is a pair of vectors: the first sets the old value, the second launches the change and makes the line visible at an output. The model keeps the $2L$ fault count and the tools of the [stuck-at fault model](/stuck-at-fault-model/), which is why it is the standard delay fault model in production test.

## The machine

The circuit is a combinational gate circuit $C$ with lines $\ell$, between launch flip-flops or inputs and capture flip-flops or outputs, clocked with period $\tau$. A transition fault is a pair $(\ell, \uparrow)$, slow to rise, or $(\ell, \downarrow)$, slow to fall. A test is a pair of input vectors $(v_1, v_2)$: $v_1$ is applied and the circuit settles, then $v_2$ is applied, and the outputs are captured $\tau$ later.

The assumptions are:

- **One slow line.** Only $\ell$ is slow. All other lines settle within $\tau$ after $v_2$, as in the good circuit.
- **Gross delay.** The slow transition at $\ell$ does not complete before the capture, so at the capture $\ell$ still holds its old value. The model does not say how large the delay is, only that it exceeds the slack of every path through $\ell$.
- **No hazards.** The captured values of the good circuit are the values of $C$ under $v_2$.

Under these assumptions, $(v_1, v_2)$ detects $(\ell, \uparrow)$ if and only if
$$\ell(v_1) = 0 \quad \text{and} \quad v_2 \text{ detects the stuck-at fault } \ell/0,$$
and in the same way $(\ell, \downarrow)$ with $\ell(v_1) = 1$ and $\ell/1$. *Proof.* If $\ell(v_1) = 1$, the line has no rising transition to delay, and the circuit is fault-free under $v_2$. If $\ell(v_2) = 0$, there is no rising transition either. If $\ell(v_1) = 0$ and $\ell(v_2) = 1$, the slow line holds 0 at the capture while all other lines compute their gates from it, which is the circuit with $\ell/0$ under $v_2$. Since $v_2$ detects $\ell/0$ only if $\ell(v_2) = 1$, the condition covers all cases. $\square$

## What it counts

The model predicts which pairs detect which faults, and so the transition [fault coverage](/fault-coverage/) of a test sequence, over the list of $2L$ faults. By the condition above, a transition fault simulator is a stuck-at fault simulator on $v_2$ with an initialization check on $v_1$. Waicukauski, Lindbloom, Rosen and Iyengar built it on [PPSFP](/ppsfp/): the good values under $v_1$ select the faults whose line has the right old value, and a stuck-at simulation of $v_2$ finds which of them reach an output.

Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, with 8 lines and so 16 transition faults. The sequence 101, 010, 011, 110 detects all 16 stuck-at faults. Applied as the three consecutive pairs, it detects 7 of the 16 transition faults.

| pair $(v_1, v_2)$ | transition faults detected |
|---|---|
| 101, 010 | a slow to fall, c slow to fall |
| 010, 011 | c slow to rise, h slow to fall, z slow to rise |
| 011, 110 | a slow to rise, g slow to fall |

All 16 faults are detectable by some pair. A search over all sequences of up to 6 vectors finds that 6 vectors are the fewest that detect all 16 as consecutive pairs, for example 000, 011, 000, 110, 101, 010. Each fault needs a pair with the right first vector, so a good stuck-at test set does not give a good transition test set when its vectors are just applied in order.

## Relation to other models

- **Stuck-at faults.** A test for $(\ell, \uparrow)$ contains a test for $\ell/0$ in its second vector. So a transition fault is detectable by some pair if and only if the stuck-at fault is detectable and the line can take the old value. A line that is constant 1 has a detectable $\ell/0$ but an undetectable slow-to-rise fault.
- **Path delay faults.** The [path delay fault model](/path-delay-fault-model/) puts the delay on a whole path, so a sum of small delays along the path can fail the test. The transition model puts it on one line, and a transition test may propagate the change along a short path with much slack, where a small extra delay is not seen. Transition tests catch gross delays; small delay defects need tests along long paths, as in timing-aware test generation that uses [static timing analysis](/static-timing-analysis/).
- **Scan tests.** In a scan design, $v_1$ is shifted in, and $v_2$ either comes from one more shift or from the response of the circuit to $v_1$. These are [launch on shift and launch on capture](/launch-on-capture-and-launch-on-shift/). Both constrain the pair, so some transition faults that are detectable with free pairs are not detectable with a given launch method.
- **Gate delay faults.** A variant puts a finite extra delay on a gate output. Whether a test detects it then depends on the delays of the paths through the gate, so it needs timing data.
- **Bridging and opens.** A resistive [bridge](/bridging-fault-model/) or a resistive open often shows as a slow transition, which is one reason transition tests catch defects that stuck-at tests miss.

## Known results in the model

- **Two-pattern condition.** Proved above: $(v_1, v_2)$ detects $(\ell, \uparrow)$ exactly when $\ell(v_1) = 0$ and $v_2$ detects $\ell/0$. So test generation is stuck-at test generation for $v_2$ plus a justification of the old value for $v_1$, and simulation costs about one stuck-at simulation per pair.
- **Detection is NP-complete.** With free pairs, a slow-to-rise fault at $\ell$ is detectable exactly when $\ell/0$ is detectable and $\ell$ is not constant 1. The second question is a satisfiability check, and the first is NP-complete for stuck-at faults (Ibarra and Sahni, 1975, cited on the [stuck-at fault model](/stuck-at-fault-model/) page). A stuck-at instance $\ell/0$ maps to a slow-to-rise instance: put a new line $\ell' = \mathrm{AND}(\ell, x)$, for a new input $x$, between $\ell$ and all its sinks. With $x = 0$ the line $\ell'$ is 0, and with $x = 1$ the circuit is the old one, so $\ell'/0$ is detectable exactly when $\ell/0$ is.
- **Fault count.** There are $2L$ transition faults, the same count as stuck-at faults. [Fault collapsing](/fault-collapsing/) by equivalence does not carry over as it is. For a circuit with the one gate $g = \mathrm{NAND}(a, b)$ and the output $g$, the stuck-at faults a/0 and g/1 are equivalent. Every pair that detects a slow to rise also detects g slow to fall, but the pair 10, 11 on $ab$ detects g slow to fall and not a slow to rise, since $a$ does not change.
- **Coverage is lower.** Every transition test of a fault contains a stuck-at test of a fault on the same line, so for the same set of second vectors, the transition coverage is at most the stuck-at coverage when both lists have $2L$ faults. The example shows the gap: 16 of 16 stuck-at faults against 7 of 16 transition faults.

## References
