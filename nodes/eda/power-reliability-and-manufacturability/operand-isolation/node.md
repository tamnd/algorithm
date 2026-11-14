---
tag: C86RHS
kind: technique
slug: operand-isolation
name: Operand isolation
aliases:
- guarded evaluation
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Holds the inputs of a datapath unit constant with AND gates or latches when its output is not used, so the unit does not switch in those cycles.
prereqs: [dynamic-power-dissipation, switching-activity]
see_also: [clock-gating, glitch-power, power-gating, finite-state-machine-with-datapath, signal-probability-propagation, transition-density, bus-invert-coding, static-timing-analysis]
sources:
  - paper: doi:10.1145/224081.224095
    title: Anthony Correale Jr., Overview of the power minimization techniques employed in the IBM PowerPC 4xx embedded controllers, Proceedings of the 1995 International Symposium on Low Power Design, 75 to 80, 1995
    locator: operand isolation of datapath units in the PowerPC 4xx controllers, among the other power saving methods of that design
  - paper: doi:10.1109/DATE.2000.840850
    title: M. Münch, B. Wurth, R. Mehra, J. Sproch and N. Wehn, Automating RT-level operand isolation to minimize power consumption in datapaths, Proceedings of Design, Automation and Test in Europe, 624 to 631, 2000
    locator: the activation function from the multiplexer selects and register enables, the isolation cells, and the cost model that decides which units to isolate
  - paper: "Vivek Tiwari, Sharad Malik and Pranav Ashar, Guarded evaluation: pushing power management to logic synthesis/design, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 17(10), 1051 to 1060, 1998"
    title: "Vivek Tiwari, Sharad Malik and Pranav Ashar, Guarded evaluation: pushing power management to logic synthesis/design, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 17(10), 1051 to 1060, 1998"
    locator: the gate-level method that finds existing signals which show that the output of a subcircuit is not observed, and puts transparent latches at its inputs; a first version appeared at the International Symposium on Low Power Design, 221 to 226, 1995
---

Operand isolation stops a datapath unit, such as an adder or a multiplier, from computing in the cycles when its result is not used. A unit in a datapath often feeds a multiplexer that selects another input, or a register that does not load, and in those cycles its work is thrown away. But its inputs still change, so its gates still switch and burn [dynamic power](/dynamic-power-dissipation/), often with many [glitches](/glitch-power/) in arithmetic logic. Operand isolation puts an isolation cell in front of each input of the unit: an AND gate that forces the input to 0, an OR gate that forces it to 1, or a latch that holds the last value. A control signal, the activation signal, opens the cells only in the cycles when the result is used. The activation signal comes from the selects of the multiplexers and the enables of the registers that the unit feeds. Correale (1995) used it in the IBM PowerPC 4xx controllers, and Münch et al. (2000) automated it at the register transfer level. It is the datapath partner of [clock gating](/clock-gating/): clock gating stops registers that would not change, operand isolation stops logic whose output would not be stored.

## In plain words

A calculator that computes every answer, even the ones that nobody reads, wastes energy. In a chip, a multiplier keeps working each time its inputs change, whether or not its result goes anywhere.

Operand isolation puts a gate in front of the multiplier's inputs. When the control logic knows that the result will not be used in this cycle, the gate freezes the inputs, so nothing inside the multiplier moves. When the result is needed again, the gate opens. The design does exactly the same job, with less switching.

## When it applies

- A unit with many gates, such as a multiplier, an adder or a shifter, whose result is used in only a part of the cycles.
- The design shows when the result is used: the unit feeds a multiplexer with a select signal, or a register with a load enable, as in a [finite-state machine with datapath](/finite-state-machine-with-datapath/).
- The inputs of the unit change in the cycles when it is not used. If they are already stable, for example because they come from registers that are clock gated, there is little to save.
- The activation signal is ready before the operands arrive, or the timing of the unit can take the delay of the isolation cell.

## The template

```pseudo id=main
OPERAND-ISOLATE(design)
L1  for each datapath unit U do
L2      AS_U ← OR, over each path from the output of U to a register or an output, of the AND of the conditions along it
            ▷ a condition is "the multiplexer selects this input" or "the register loads"
L3      if the estimated power saved on U exceeds the power and area of its isolation then
L4          put an isolation cell on each input of U, open when AS_U = 1:
            an AND gate with AS_U, an OR gate with NOT AS_U, or a latch transparent while AS_U = 1
L5          check that AS_U settles before the operands of U, or that U still meets its timing
```

The holes are the analysis of line L2, which may also use other knowledge of when the result is not needed, the cost model of line L3, and the style of the cells in line L4.

**Claim (isolation keeps the behavior).** Suppose that in every cycle with $AS_U = 0$, the output of $U$ does not reach any register that loads in that cycle, nor any primary output. Then the isolated design has the same register states and the same outputs as the original in every cycle.

*Proof.* By induction on the cycle $k$, the registers agree. Assume they agree at the start of cycle $k$. If $AS_U = 1$, every isolation cell passes its input, so $U$ sees the same operands and gives the same output as in the original, and all of the logic agrees. If $AS_U = 0$, the output of $U$ may differ, but by the assumption it reaches no loading register and no output, and all other logic sees the same values as in the original. So the registers that load get the same values, the others keep the same values, and the outputs agree. $\square$

The activation signal of line L2 meets the assumption: if, on every path from $U$ to a register or an output, some multiplexer selects another input or the register does not load, the output of $U$ is blocked. $AS_U$ may be 1 in more cycles than needed, which saves less but is still correct. If it is 0 in a cycle in which the output is used, the design is broken. What is proved is the behavior. The saving is estimated or measured, and it depends on the data.

**Example.** An 8-bit ripple-carry adder, built from 8 full adders with 7 nets each, including its inputs, sum and carry, gets the operand pairs (in hex) 5A+33, C3+0F, 7E+81, 12+F0, A5+5A, 3C+66, FF+01 and 24+42 in 8 cycles, starting from all nets at 0. Its result is used only in cycles 1, 5 and 8. The table counts rising transitions, the $\alpha$ of the power formula, on the 16 input bits and on all 56 nets, in a zero-delay model, computed by a script.

| style | inputs seen in cycles 2 to 4 | rising inputs | rising nets |
|---|---|---|---|
| no isolation | C3+0F, 7E+81, 12+F0 | 37 | 116 |
| AND gates | 00+00 | 20 | 60 |
| latches | 5A+33, held | 14 | 38 |

AND isolation halves the activity here. Latches do better, because they hold the last operands, while AND gates pull the inputs to 0 on entry and the next used operands must then rise from 0. Over 20 000 cycles of random operands with seed 11, the rising transitions on all nets per cycle were 12.59 with no isolation; 5.13 with AND gates and 3.19 with latches when the result is used in 25% of the cycles; and 12.26 with AND gates and 11.35 with latches when it is used in 90% of the cycles. These are runs on a toy circuit, not benchmark results, and the zero-delay model has no glitches, which isolation also removes in a real adder. The counts are exact for this model. Turning them into power needs the capacitance of each net, which comes from extraction and from library pin capacitances fitted to circuit simulation, as on the [dynamic power](/dynamic-power-dissipation/) page.

## Classic examples

- **PowerPC 4xx.** Correale (1995) describes operand isolation of datapath units among the power saving methods of IBM's embedded controllers.
- **RT-level automation.** Münch et al. (2000) find the activation functions from the multiplexers and register enables of an RTL design, and choose the units to isolate with a cost model of the power saved and the power, area and delay added.
- **Arithmetic units of processors.** A multiplier or a divider is isolated when the current instruction does not use it.
- **Gate-level isolation by Tiwari, Malik and Ashar.** Their method (1995, journal form 1998) works on a gate-level netlist during logic synthesis. It looks for signals that already exist in the circuit and that imply that the output of a subcircuit is not observed, using observability don't-care conditions, and it puts transparent latches at the inputs of that subcircuit, controlled by those signals. It differs from operand isolation in three points: it works on gates, not on RTL units; its control signals are found by logic analysis among the existing signals, not built from multiplexer selects and register enables; and it uses latches only.

## Variations

- **AND, OR or latch cells.** AND and OR cells are small and fast but add transitions when isolation starts and ends. Latches hold the last value, which saves more, as in the example, but they cost area and need care in timing.
- **Isolation at the register.** If the operands come straight from registers, gating the clock of those registers holds the operands too, with no extra cells.
- **Isolation of buses.** The same idea stops a bus from switching when no receiver reads it, which can be combined with codes such as [bus-invert coding](/bus-invert-coding/).
- **Precomputation.** A related method computes the output from a part of the inputs in the cycles where that part decides it, and stops the rest of the inputs from loading.

## Pitfalls

- **A late activation signal.** If $AS_U$ settles after the operands, the unit first starts on the new operands and then stops, which wastes power and makes glitches. The activation signal must also not lengthen the critical path through the unit.
- **Short idle periods.** With AND or OR cells, each entry to and exit from isolation adds transitions. When the result is used most of the time, the saving can vanish, as the 90% run of the example shows.
- **The cost of the cells.** Each input bit needs a cell, and $AS_U$ drives all of them. For small units the cells cost more than they save.
- **A wrong activation signal.** If $AS_U = 0$ in a cycle where the result is used, the design computes wrong values. Derive it from the RTL, and check with an equivalence checker.
- **Latches and test.** Isolation latches add state that scan test and timing analysis must handle.
- **Ignoring glitches.** Power estimates that count only one transition per net per cycle miss most of the power of arithmetic units, and so underestimate the saving.

## Exercises

1. Derive the expected number of rising input transitions per cycle for AND isolation and for latch isolation of a unit with $m$ input bits, random operands and a result used in each cycle with probability $p$, independently. Compare with the runs of the example.
2. A multiplier feeds input 1 of a multiplexer with select $s$, whose output goes to a register with load enable $e$, and also feeds a primary output through an AND gate with a control $c$. Write the activation signal of line L2.
3. Show that the claim fails if $AS_U$ is 0 in a cycle where the register after the multiplexer loads the result of $U$.
4. For the 8-cycle trace of the example, recount the rising transitions if the isolation cells are OR gates.

## References
