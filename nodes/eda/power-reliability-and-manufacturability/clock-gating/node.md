---
tag: B5KMK1
kind: technique
slug: clock-gating
name: Clock gating
aliases:
- gated clocks
area: eda/power-reliability-and-manufacturability
level: core
summary: Stops the clock of a register bank when an enable condition shows its value will not change, removing the clock and register power of idle cycles.
prereqs: [dynamic-power-dissipation, switching-activity, mealy-machine]
see_also: [operand-isolation, power-gating, clock-tree-synthesis, static-timing-analysis, setup-and-hold-constraints, markov-chain, scan-design, glitch-power]
sources:
  - paper: "Luca Benini and Giovanni De Micheli, Automatic synthesis of low-power gated-clock finite-state machines, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(6), 630 to 643, 1996"
    title: Luca Benini and Giovanni De Micheli, Automatic synthesis of low-power gated-clock finite-state machines, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(6), 630 to 643, 1996
    locator: the activation function from the self-loops of a finite-state machine, its simplification, and the latch-based gate that stops the clock of the state register
---

Clock gating stops the clock of a register when a condition shows that the register would load the value it already holds. The clock is the busiest net of a synchronous chip: in the notation $P = \alpha C V^2 f$ of [dynamic power](/dynamic-power-dissipation/), with $\alpha$ the number of rising transitions per cycle, every clock pin has $\alpha = 1$, while most data nets have $\alpha$ well below 1. A register that holds its value still burns the power of its clock pin, of its internal clock buffers and of the clock wires to it. Clock gating puts a gate on the clock of a register bank, controlled by an enable, so that in the cycles when the enable is off the gated clock does not rise and its whole subtree is quiet. The enable comes either from a load-enable that the design already has, or from the self-loops of a finite-state machine, as in Benini and De Micheli (1996). The gate must not make glitches on the clock, so it is built with a latch. Done right, it keeps the behavior of the circuit cycle for cycle.

## In plain words

Every flip-flop gets a clock tick in every cycle, even when it has nothing new to store. Each tick costs energy.

Clock gating asks, for each group of flip-flops: will they store anything new in this cycle? If the answer is no, it holds back their clock tick. The flip-flops keep their old value, which is what they would have stored anyway, and the energy of the tick is saved. The work is in finding a cheap and safe way to know the answer one cycle ahead, and in building the switch so that it never makes a false tick.

## When it applies

- A register bank often holds its value: it has a load-enable, which in the netlist shows as a multiplexer that feeds the output back to the input, $D = EN \,?\, \mathit{new} : Q$.
- A finite-state machine often stays in its state: its state transition graph has self-loops that are taken in many cycles, such as a wait state.
- The bank is wide enough that the gating cell, which itself has a clock pin that switches in every cycle, costs less than it saves. Banks of one or two flip-flops rarely pay off.
- The enable is known early enough in the cycle to meet the setup time of the gating latch, as checked by [static timing analysis](/static-timing-analysis/).

## The template

An **integrated clock gate** is a latch $L$ that is transparent while CLK = 0, with the enable $E$ at its input, followed by an AND gate: $\mathrm{GCLK} = \mathrm{CLK} \land L$. The register bank is clocked by GCLK on its rising edge.

```pseudo id=main
CLOCK-GATE(design)
L1  for each register bank R with D = EN ? new : Q do
L2      remove the feedback multiplexer, so that D = new
L3      insert an integrated clock gate with enable E = EN, or E = EN or TE for scan test
L4      clock R with GCLK of the gate
L5  for each finite-state machine with state register S, next state δ(x, s) and inputs x do
L6      choose an activation function F_a with F_a(x, s) = 1 only if δ(x, s) = s
L7      clock S with an integrated clock gate with enable E = not F_a(x, s)
```

The holes are the choice of the banks in line L1, the activation function in line L6, which can be any subset of the self-loops, small enough to be cheap logic, and the grain: one gate per bank, or a gate high in the [clock tree](/clock-tree-synthesis/) for a whole block.

**Why the latch.** In cycle $k$, the logic that makes $E$ is clocked by CLK, so $E$ may change while CLK = 1. A plain AND gate, $\mathrm{CLK} \land E$, would then cut the high phase short or add a pulse, and a short pulse can clock some flip-flops and not others. With the latch, $L$ follows $E$ only while CLK = 0, and it is frozen while CLK = 1. So during each high phase GCLK is CLK AND a constant: either the full pulse or nothing, with no glitch. At the rising edge that ends cycle $k$, $L$ holds the value of $E$ that settled during the low phase, so GCLK rises exactly when $E$ is 1 at the end of the cycle. This needs $E$ to meet the setup time of the latch before the rising edge, which STA checks as a clock gating check.

**Claim 1 (line L1 to L4 keep the behavior).** With the latch gate, the register R loads $\mathit{new}$ at the end of cycle $k$ if $EN_k = 1$ and keeps $Q$ otherwise, which is what the multiplexer did. *Proof.* If $EN_k = 1$, GCLK rises and R loads $D = \mathit{new}$. If $EN_k = 0$, GCLK stays low and R keeps $Q$, which the multiplexer would have loaded. $\square$

**Claim 2 (gating the self-loops keeps the behavior).** Take a synchronous machine with inputs $x_k$, state $s_k$, next state $s_{k+1} = \delta(x_k, s_k)$ and output $\lambda(x_k, s_k)$, a [Mealy machine](/mealy-machine/), with a [Moore machine](/moore-machine/) as the case where $\lambda$ does not depend on $x$. Let the gated machine load its state register only when $F_a(x_k, s'_k) = 0$, where $F_a(x, s) = 1$ implies $\delta(x, s) = s$. Then from the same initial state and for every input sequence, the gated machine has the same state sequence and the same output sequence.

*Proof.* By induction on $k$, $s'_k = s_k$. It holds for $k = 0$. Assume $s'_k = s_k$. If $F_a(x_k, s_k) = 0$, the gated register loads $\delta(x_k, s_k) = s_{k+1}$. If $F_a(x_k, s_k) = 1$, it keeps $s_k$, and $\delta(x_k, s_k) = s_k$ by the condition on $F_a$, so again $s'_{k+1} = s_{k+1}$. The outputs $\lambda(x_k, s'_k) = \lambda(x_k, s_k)$ agree because the states and inputs agree. $\square$

The proof does not need $F_a$ to cover all self-loops. A smaller $F_a$ gates fewer cycles and saves less, but it stays correct. A larger one, which also covers some $(x, s)$ with $\delta(x, s) \ne s$, breaks the machine. What is proved is the behavior. The saving is measured or estimated, since it depends on how often the self-loops are taken.

**What the saving is.** With the bank clock capacitance $C_R$ and the clock gate capacitance $C_g$ on the free clock, the clock power falls from $C_R V^2 f$ to $(C_g + p\, C_R) V^2 f$, where $p$ is the fraction of cycles with $E = 1$. The capacitances are extracted from the layout and the library, whose pin capacitances are fitted to circuit simulations of each cell, $p$ comes from simulation or from a probability model, and $V$ and $f$ are design values. The formula itself has no fitted parameter.

**Example (a register).** A 32-bit register loads in 20% of the cycles. Assume 3 fF of clock load per flip-flop, pin and wire, so $C_R = 96$ fF, and $C_g = 5$ fF for the clock gate. At 1 V and 1 GHz the clock power of the bank falls from $96\ \mu$W to $(5 + 0.2 \cdot 96) = 24.2\ \mu$W, a ratio of 0.25. The multiplexers of line L2 are gone as well. These capacitances are assumed numbers for the example.

**Example (a machine).** A controller has the states IDLE, RUN and DONE. In IDLE it stays while start = 0 and goes to RUN when start = 1. In RUN it stays while done = 0 and goes to DONE when done = 1. From DONE it goes to IDLE. Its output busy is 1 in RUN, and in IDLE when start = 1. The full self-loop function is $F_a = (s = \mathrm{IDLE} \land \lnot \mathit{start}) \lor (s = \mathrm{RUN} \land \lnot \mathit{done})$. If start is 1 with probability 0.1 and done with probability 0.05, independently in each cycle, the state is a [Markov chain](/markov-chain/) with the stationary probabilities $10/31$, $20/31$ and $1/31$, and the self-loops are taken in $(10 \cdot 0.9 + 20 \cdot 0.95)/31 = 28/31 \approx 90\%$ of the cycles. The state register then gets a clock in only $3/31 \approx 9.7\%$ of the cycles. A simulation of 200 000 cycles with seed 7 gave the same states and outputs as the ungated machine, with the register loaded in 9.56% of the cycles. The output is a Mealy output, and it stays right while the clock is off because it is computed from the inputs and the held state.

## Classic examples

- **Load-enable registers.** Synthesis tools find the feedback multiplexers of line L1 and replace them with clock gates, often for all banks above a minimum width.
- **Gated-clock finite-state machines.** Benini and De Micheli (1996) extract $F_a$ from the state transition graph, simplify it to keep its logic small, and gate the state register, as in lines L5 to L7.
- **Pipelines with valid bits.** A pipeline stage is clocked only when a valid item enters it.
- **Block-level gating.** A gate near the root of the clock tree of a block turns off the whole subtree when the block is idle, which saves the power of the clock buffers too.
- **Processors.** Units that are not used by the current instructions, such as a floating point unit, get no clock.

## Variations

- **Data-driven gating.** Compare $D$ with $Q$ by XOR gates and gate the clock when they agree. This needs no knowledge of the design, but the comparators cost power and the condition is late in the cycle.
- **Multi-level gating.** Gates in series down the clock tree: a coarse gate for a block and fine gates for its banks.
- **OR-based gates.** For registers on the falling edge, a latch transparent while CLK = 1 and an OR gate do the same job.
- **Gating with [operand isolation](/operand-isolation/).** The same idle signal that stops the clock of the registers can also hold the inputs of the logic between them.
- **[Power gating](/power-gating/).** For long idle periods, cut the supply too, which also removes the leakage that clock gating leaves.

## Pitfalls

- **Glitches from a plain AND.** Without the latch, an enable that changes while CLK = 1 makes a short clock pulse.
- **Clock skew.** The gate adds delay to the clock of its bank, which the clock tree must balance against the other banks, and the [hold](/setup-and-hold-constraints/) checks must include it.
- **Late enables.** The enable must meet the setup time of the gating latch. A complex $F_a$ can be too slow, which is one reason to simplify it.
- **Too small banks.** The gate and its latch switch in every cycle. For a narrow bank or one that is enabled most of the time, they can cost more than they save.
- **Test.** In [scan](/scan-design/) shift mode every flip-flop must get its clock, so each gate needs a test enable TE that forces it on, as in line L3.
- **A wrong activation function.** Gating any cycle in which $\delta(x, s) \ne s$ loses a state change. This is a design error, not a timing error, and only an equivalence check or Claim 2 catches it.
- **Supply noise.** Turning on a large gated tree at once draws a step of current, which the [power grid](/power-grid-analysis/) and its [decaps](/decoupling-capacitance-allocation/) must handle.

## Exercises

1. Draw the waveforms of CLK, $E$, the latch output and GCLK when $E$ falls in the middle of a high phase of CLK, for the latch gate and for a plain AND gate.
2. Show that Claim 2 fails if $F_a(x, s) = 1$ for one pair with $\delta(x, s) \ne s$: give a machine, a pair and an input sequence with a different output.
3. For the controller of the example, compute the fraction of gated cycles when $F_a$ covers only the self-loop of IDLE.
4. A bank of $n$ flip-flops with clock load $c$ each is enabled in a fraction $p$ of the cycles, and the gate has the load $C_g$. For which $n$ does gating save power?

## References
