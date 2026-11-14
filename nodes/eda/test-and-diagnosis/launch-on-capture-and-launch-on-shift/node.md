---
tag: 4NY376
kind: technique
slug: launch-on-capture-and-launch-on-shift
name: Launch-on-capture and launch-on-shift
aliases:
- broadside test
- skewed-load test
- LOC and LOS
area: eda/test-and-diagnosis
level: core
summary: The two ways a scan design applies at-speed two-pattern tests, launching the transition by a functional capture or by the last shift of the scan chain.
prereqs: [transition-fault-model, scan-design]
see_also: [time-frame-expansion, path-delay-fault-model, automatic-test-pattern-generation, static-timing-analysis, scan-chain-ordering, fault-coverage, ppsfp, power-grid-analysis]
sources:
  - paper: "J. Savir, Skewed-load transition test: Part I, calculus, Proceedings of the International Test Conference, 705 to 713, 1992"
    title: J. Savir, Skewed-load transition test, Part I, calculus, Proceedings of the International Test Conference, 705 to 713, 1992
    locator: the skewed-load test, where the second vector is the one-bit shift of the first, and the calculus of which transitions it can launch
  - paper: "J. Savir and S. Patil, Broad-side delay test, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 13(8), 1057 to 1064, 1994"
    title: J. Savir and S. Patil, Broad-side delay test, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 13(8), 1057 to 1064, 1994
    locator: the broadside test, where the second vector is the response of the circuit to the first, and its comparison with skewed-load tests
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Delay Test (two-pattern tests in scan designs)
---

A [transition fault](/transition-fault-model/) test is a pair of vectors $(v_1, v_2)$ applied one clock period apart: $v_1$ sets the old values, $v_2$ launches the transitions, and the response is captured one period $\tau$ later. A [scan design](/scan-design/) can shift any $v_1$ into its flip-flops, slowly. It cannot shift in a second vector at speed, so it needs another way to make $v_2$ from $v_1$ within one clock period. There are two. In **launch on shift** (LOS), also called the **skewed-load test**, $v_2$ is $v_1$ shifted by one more position along the scan chain. In **launch on capture** (LOC), also called the **broadside test**, $v_2$ is the response of the circuit to $v_1$, loaded by one functional clock. Both turn the free pair of the transition fault model into a constrained pair, and each can detect faults that the other cannot. This page states the two constraints, proves that neither method covers the other, and shows what each costs on the chip.

## In plain words

To test whether a part of a chip is fast enough, you need a "before" value and an "after" value, given one fast clock tick apart. The scan chain is a slow conveyor belt. You can put any "before" pattern on it, but you cannot load a whole new "after" pattern in one fast tick.

So you cheat. One way is to move the belt one more step: every bit moves to its neighbor, and that is the "after" pattern. The other way is to let the circuit run for one normal tick: what it computes from the "before" pattern is the "after" pattern. Either way, you then catch the result with a second fast tick and shift it out slowly. Each way can make some "after" patterns that the other cannot, so each misses some faults the other catches.

## When it applies

- The design has full scan. The combinational logic $C$ has primary inputs $x$ and present-state inputs $q_0, \ldots, q_{n-1}$ (the scan cells), and computes primary outputs and next-state values $N(x, q)$, which the cells capture. A test vector is $v = (x, q)$.
- The scan chain runs from the scan-in pin through $q_0, q_1, \ldots, q_{n-1}$ to the scan-out pin. A shift moves the value of $q_{i-1}$ into $q_i$ and the scan-in bit into $q_0$. A scan-enable signal SE selects shift (SE = 1) or functional capture (SE = 0).
- The faults are transition faults, or [path delay faults](/path-delay-fault-model/), whose tests are pairs. A pair $(v_1, v_2)$ detects the slow-to-rise fault $(\ell, \uparrow)$ exactly when $\ell(v_1) = 0$ and $v_2$ detects $\ell/0$, as proved on the transition fault model page.
- The tester changes the primary inputs only slowly, so during the two fast clocks the primary inputs stay at $x_1$, and in many flows the primary outputs are not compared at speed.

## The template

```pseudo id=main
APPLY-TWO-PATTERN(s1, x1, b, mode)
L1  SE ← 1; shift s1 into the scan cells with slow clocks
L2  apply x1 to the primary inputs and let the circuit settle; this is v1 = (x1, s1)
L3  if mode = LOS
L4      give one more shift clock with scan-in bit b: the cells become s2 = (b, s1[0], …, s1[n-2])
L5      switch SE to 0 within one period, then give the capture clock τ after the shift clock
L6  else
L7      SE ← 0; give a functional clock: the cells become s2 = N(x1, s1)
L8      give the capture clock τ after the launch clock
L9  the launch made v2 = (x1, s2); the cells now hold N(x1, s2)
L10 SE ← 1; shift out the captured values (and shift in the next s1) and compare them
```

The holes are the mode, the scan-in bit $b$ of LOS, and the clocking: the launch and capture clocks are fast, usually made by an on-chip clock generator, and everything else is slow.

**The two constraints.** Line L4 makes the state part of $v_2$ a shift of the state part of $v_1$:
$$\text{LOS:}\quad q_0(v_2) = b, \qquad q_i(v_2) = q_{i-1}(v_1) \ \text{ for } 1 \le i < n.$$
Line L7 makes it the next state:
$$\text{LOC:}\quad q(v_2) = N(x_1, q(v_1)).$$
In both, $x(v_2) = x(v_1)$. Given $v_1$, LOS allows 2 second vectors and LOC allows 1, against $2^{n}$ for a free pair with the same inputs. So both methods can detect only faults that have a test among these pairs, and each misses the rest.

**LOC is a two-frame test.** By line L7, $v_2$ is what the circuit computes from $v_1$. So the circuit under LOC is the two-frame iterative logic array of [time-frame expansion](/time-frame-expansion/), with the state of frame 1 free (it was scanned in), the state of frame 2 wired to the next state of frame 1, and only the outputs of frame 2 observed. A transition fault $(\ell, \uparrow)$ is LOC-testable exactly when this array has an input with $\ell = 0$ in frame 1 and a detection of $\ell/0$ in frame 2. The fault is in frame 2 only, since it is a delay and frame 1 is applied slowly. This is how test generators handle LOC: as sequential test generation over two frames with a free initial state.

**LOS is a combinational test with a wired second vector.** By line L4, the state part of $v_2$ is a copy of the inputs of $v_1$, wired one cell over. So LOS test generation is one combinational problem on $C$ for $v_1$, a second copy of $C$ for $v_2$, and wires $q_i(v_2) = q_{i-1}(v_1)$ between them. Both methods use two copies of $C$. The difference is that under LOS the second vector depends on the first through wires, and under LOC through the logic $N$.

**Neither method covers the other.** Take three scan cells in the chain order $q_0, q_1, q_2$, no primary inputs, and the next-state logic
$$d_0 = q_1 q_2, \qquad d_1 = q_0 + q_2, \qquad d_2 = q_1 \oplus q_2 .$$
The stem $q_1$ feeds $d_0$ and $d_2$, and $q_2$ feeds all three, so with branches $C$ has 11 lines and 22 transition faults. All 22 are detectable by free pairs.

- *LOS misses $(q_1{>}d_0, \uparrow)$*, slow to rise on the branch from $q_1$ to $d_0$. A test needs $q_1(v_1) = 0$, and $v_2$ must detect the branch stuck-at 0, so $q_1(v_2) = 1$ and $q_2(v_2) = 1$ to pass the effect through the AND. Under LOS, $q_2(v_2) = q_1(v_1) = 0$. No LOS pair works, whatever the scan-in bit. Under LOC, $v_1 = (q_0, q_1, q_2) = (0, 0, 1)$ gives $v_2 = N(v_1) = (0, 1, 1)$, which is a test.
- *LOC misses $(q_2{>}d_1, \downarrow)$*, slow to fall on the branch from $q_2$ to $d_1$. A test needs $q_2(v_1) = 1$, and $v_2$ must detect the branch stuck-at 1 through the OR, so $q_2(v_2) = 0$ and $q_0(v_2) = 0$. Under LOC with $q_2(v_1) = 1$, $q_0(v_2) = q_1(v_1)$ and $q_2(v_2) = \lnot q_1(v_1)$, which are never both 0. Under LOS, $v_1 = (q_0, 0, 1)$ with scan-in bit 0 gives $v_2 = (0, q_0, 0)$, which is a test.

A brute force over all pairs confirms that each method detects 21 of the 22 faults and that these two faults are the only gaps. So the sets of faults that the two methods can detect are incomparable in general, and a flow that wants the most coverage uses both or a variation below.

**Measured, not proved.** Over the 3375 circuits of the family above (three scan cells, no primary inputs, each $d_i$ an AND, OR, NAND, NOR or XOR of two of the three cells), there are 76 500 transition faults, of which 75 750 are detectable by free pairs. LOS can detect 70 078 of them, LOC 53 295, either method 72 874 and both 50 499. This is an exhaustive count over a toy family, not a benchmark result. Here LOC suffers because two-input gates on all the state bits make $N$ far from onto, and no primary input adds freedom.

**Cost.** For $n$ scan cells in one chain, each pair takes about $n$ slow shift clocks and two fast clocks, the same for both methods. The cost is in the hardware and the timing. LOS needs SE to switch from shift to capture within one fast period at line L5, so SE must be routed and timed like a clock to every scan cell. LOC lets SE switch slowly, between L1 and L7.

## Classic examples

- **Savir's skewed-load test (1992).** The second vector is the one-bit shift of the first. Savir gave a calculus of the transitions that such a shift can launch.
- **Savir and Patil's broadside test (1994).** The second vector is the response of the circuit to the first, and the paper compares it with skewed-load tests.
- **Production transition test.** LOC is common in production at-speed scan test, with an on-chip clock controller that issues the two fast pulses, because it avoids the fast SE that LOS needs, which is hard to close in timing on a large design.
- **Path delay tests.** The same two methods apply path delay tests. Robust tests add conditions on the side inputs of the path in both vectors, and these are harder to meet under the constraints above.

## Variations

- **Enhanced scan.** A hold latch after each scan cell keeps $v_1$ while $v_2$ is shifted in, so any pair can be applied. It costs a latch per cell and adds delay on functional paths.
- **Hybrid launch.** Give only some scan cells a fast scan-enable and use LOS on those and LOC on the rest, to recover coverage at a smaller timing cost.
- **More capture frames.** Launch on capture with $k > 1$ functional clocks before the last one, which is a $k + 1$ frame test in the sense of time-frame expansion.
- **Chain order for LOS.** Since LOS ties $q_i(v_2)$ to $q_{i-1}(v_1)$, the order of the cells in the chain changes the coverage. [Scan chain ordering](/scan-chain-ordering/) can take this into account.
- **Pairs from fault simulation.** Transition fault simulation of LOS and LOC pairs is stuck-at simulation of $v_2$ with a check on $v_1$, as with [PPSFP](/ppsfp/), with $v_2$ computed by the shift or by one good-machine simulation of $v_1$.

## Pitfalls

- **Overtesting with LOS.** A LOS pair can put the circuit in a state that it never reaches in normal operation, and launch transitions on paths that are never exercised at speed in the field. A chip that fails such a test may work in its application. LOC launches from $N(x_1, s_1)$, which is a state the circuit can reach in one step, though $s_1$ itself may still be unreachable.
- **Fast scan-enable.** LOS fails if SE does not reach every cell within one period. A late SE makes the capture a second shift.
- **Power during launch.** Scan patterns often switch far more lines at once than functional operation does. The supply voltage droops (see [power grid analysis](/power-grid-analysis/)) and the paths slow down, so a good chip can fail at speed. Low-power fills of the X bits reduce this.
- **Primary inputs and outputs.** If the tester cannot change inputs or strobe outputs at speed, the flow must hold $x$ and mask the outputs, and faults that need them become untestable by both methods.
- **Coverage of transition faults is not of small delays.** A transition test may launch along a short path with much slack. Both methods share this limit of the [transition fault model](/transition-fault-model/).

## Exercises

1. In the three-cell example, find all LOS pairs that detect $(q_2{>}d_1, \downarrow)$, and all LOC pairs that detect $(q_1{>}d_0, \uparrow)$.
2. Prove that every fault that LOC or LOS can detect is detectable by a free pair, and give a circuit with a transition fault that is detectable by a free pair but by neither method.
3. Show that no order of the three scan cells of the example lets LOS detect all 22 transition faults.

## References
