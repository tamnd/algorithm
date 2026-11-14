---
tag: Y1FH5E
kind: technique
slug: power-gating
name: Power gating
aliases:
- MTCMOS
- sleep transistor insertion
area: eda/power-reliability-and-manufacturability
level: core
summary: Cuts idle blocks from the supply through high-threshold sleep transistors to remove their leakage, with sizing, state retention and wake-up control to design.
prereqs: [leakage-power, dynamic-power-dissipation]
see_also: [clock-gating, multi-threshold-voltage-assignment, decoupling-capacitance-allocation, power-grid-analysis, shichman-hodges-model, ski-rental-problem, speed-scaling, operand-isolation]
sources:
  - paper: "Shin'ichiro Mutoh, Takakuni Douseki, Yasuyuki Matsuya, Takahiro Aoki, Satoshi Shigematsu and Junzo Yamada, 1-V power supply high-speed digital circuit technology with multithreshold-voltage CMOS, IEEE Journal of Solid-State Circuits 30(8), 847 to 854, 1995"
    title: Shin'ichiro Mutoh, Takakuni Douseki, Yasuyuki Matsuya, Takahiro Aoki, Satoshi Shigematsu and Junzo Yamada, 1-V power supply high-speed digital circuit technology with multithreshold-voltage CMOS, IEEE Journal of Solid-State Circuits 30(8), 847 to 854, 1995
    locator: the MTCMOS scheme, low-threshold logic between virtual rails and high-threshold switches to the real rails, turned off in sleep mode
  - paper: "James Kao, Siva Narendra and Anantha Chandrakasan, MTCMOS hierarchical sizing based on mutual exclusive discharge patterns, Proceedings of the 35th Design Automation Conference, 495 to 500, 1998"
    title: James Kao, Siva Narendra and Anantha Chandrakasan, MTCMOS hierarchical sizing based on mutual exclusive discharge patterns, Proceedings of the 35th Design Automation Conference, 495 to 500, 1998
    locator: sizing the shared sleep transistor for the largest total current over time instead of the sum of the peak currents of the gates, using gates that discharge at mutually exclusive times
---

Power gating cuts a block of logic off from its supply while it is idle, so that it draws almost no [leakage](/leakage-power/) current. A wide transistor with a high threshold voltage, the sleep transistor, sits between the real supply rail and a virtual rail that feeds the block: a PMOS header on the $V_{DD}$ side or an NMOS footer on the ground side. In active mode the sleep transistor is on, and the block works almost as if it were on the real rail. In sleep mode it is off, and the leakage of the whole block is limited by the leakage of the sleep transistor, which is small because of its high threshold and its small width compared with the block. The scheme was named multi-threshold CMOS, or MTCMOS, by Mutoh et al. (1995). Power gating targets the leakage that [clock gating](/clock-gating/) leaves, and it has costs that clock gating does not: the sleep transistor adds a resistance that slows the block, the block loses its state, its outputs float, and waking it up takes time and energy. A design that uses power gating must size the switches, keep the state that matters, clamp the outputs, control the wake-up current and decide when sleeping pays off.

## In plain words

A modern chip leaks power through its transistors even when it does nothing, like a tap that drips. For a block that sits idle for long stretches, the simplest cure is to turn off its supply with a big switch.

The switch is not free. While the block works, the current must flow through the switch, which costs a little voltage and speed. When the block sleeps, it forgets what it held, unless special flip-flops keep it. And turning the block back on takes time and a burst of charge. So power gating pays off only for blocks that stay idle long enough, and only with careful design of the switch and its control.

## When it applies

- Leakage is a large part of the power of the block, as in technologies with low threshold voltages, and the block is idle for long periods: a processor core between tasks, a radio between bursts, a unit that some modes do not use.
- The idle periods are longer than the break-even time below, and the wake-up latency is acceptable.
- The design can pay the area of the switches, a small loss of speed in active mode, and the always-on logic that controls the sleep.
- The state of the block can be lost, or a small part of it can be kept in retention registers or saved elsewhere.

## The template

```pseudo id=main
POWER-GATE(block B)
L1  choose header or footer switches, and one shared switch network or switches per cell
L2  size the switches so that I_peak · R_sleep ≤ ΔV, with I_peak the largest total current of B over time
L3  put isolation cells on the outputs of B that clamp them to a fixed value while B sleeps
L4  keep the needed state: retention registers with an always-on supply, or a save to memory
L5  add a controller on an always-on supply
        sleep: clamp the outputs, save the state, turn the switches off
        wake:  turn the switches on in steps, wait until the virtual rail settles, restore the state, release the clamps
L6  enter sleep only when the idle period is expected to exceed the break-even time t_be
```

The holes are the switch style and grain of line L1, the current model of line L2, the retention scheme of line L4, and the sleep policy of line L6.

**Sizing the switch.** In active mode the switch is a transistor in its linear region with a small drain to source voltage. In the square-law model of the [Shichman-Hodges](/shichman-hodges-model/) page its resistance is close to

$$ R_{\text{sleep}} \approx \frac{1}{\mu C_{ox} (W/L) (V_{DD} - V_{TH,\text{high}})}, $$

where the process transconductance $\mu C_{ox}$ and the high threshold $V_{TH,\text{high}}$ are fitted to measured devices. For example, with $\mu C_{ox} = 300\ \mu$A/V$^2$, $V_{DD} = 1$ V and $V_{TH,\text{high}} = 0.45$ V, all assumed numbers, a block with a peak current of 50 mA and an allowed drop of 5% of $V_{DD}$ needs $R_{\text{sleep}} \le 1\ \Omega$, so $W/L \ge 1/(300 \cdot 10^{-6} \cdot 0.55) \approx 6060$, or a total width of about 303 $\mu$m at $L = 50$ nm. The drop $I R_{\text{sleep}}$ also slows the gates of the block, which the delay model of the library must include. In a real design the switch tables of the library replace this formula.

**Claim 1 (the maximum of the sum, not the sum of the maxima).** Let gate $g$ of the block draw the current $I_g(t)$ through a shared switch. The current of the switch is $\sum_g I_g(t)$, so the switch must be sized for $\max_t \sum_g I_g(t)$, and

$$ \max_t \sum_g I_g(t) \ \le\ \sum_g \max_t I_g(t), $$

with equality only if some time $t$ is a peak time for every gate at once. *Proof.* For every $t$, $\sum_g I_g(t) \le \sum_g \max_{t'} I_g(t')$, so the maximum over $t$ obeys the same bound. If the bound is reached at $t^*$, then each term $I_g(t^*)$ must reach its maximum. $\square$

Kao, Narendra and Chandrakasan (1998) used this: in a chain of gates, the gates switch one after another and their discharge currents do not overlap, so a switch sized for the sum of their peaks is far too large. For three gates with peaks of 1 mA at three separate times, the shared switch needs to carry 1 mA, not 3 mA.

**Claim 2 (break-even time).** Let $P_{\text{on}}$ be the leakage power of the block when on and idle, $P_{\text{off}}$ the leakage when asleep, and $E_{\text{tr}}$ the energy of one sleep and wake cycle: recharging the virtual rail, switching the gates of the switches, and saving and restoring the state. Then sleeping during an idle period of length $t$ saves energy if and only if

$$ t > t_{\text{be}} = \frac{E_{\text{tr}}}{P_{\text{on}} - P_{\text{off}}}. $$

*Proof.* Staying on costs $P_{\text{on}} t$, and sleeping costs $E_{\text{tr}} + P_{\text{off}} t$, if the transitions are short compared with $t$. The second is smaller exactly when $t (P_{\text{on}} - P_{\text{off}}) > E_{\text{tr}}$. $\square$

For example, recharging a virtual rail of 1 nF from 0 to 1 V draws $C V^2 = 1$ nJ from the supply, and the switch gates and the control take another 0.1 nJ, an assumed number. With $P_{\text{on}} = 10$ mW and $P_{\text{off}} = 10\ \mu$W, $t_{\text{be}} \approx 110$ ns. When the length of the idle period is not known in advance, the decision of line L6 is the [ski rental problem](/ski-rental-problem/): staying awake until $t_{\text{be}}$ has passed and then sleeping uses at most twice the energy of the best choice made with hindsight.

**The leakage in sleep.** The subthreshold current of a transistor is close to $I_0 (W/L) e^{-V_T/(n v_T)}$ at $V_{GS} = 0$, with the slope factor $n$ and the prefactor $I_0$ fitted, as on the [leakage power](/leakage-power/) page. With $n = 1.5$, a switch with 0.15 V more threshold than the logic and 5% of its total width leaks about $0.05 \cdot e^{-0.15/(1.5 \cdot 0.02585)} \approx 10^{-3}$ of the leakage of the block. These are assumed numbers. Real ratios also depend on gate leakage and on the voltage left on the virtual rail.

## Classic examples

- **MTCMOS.** Mutoh et al. (1995) put low-threshold logic between virtual rails and high-threshold switches to the real rails, for 1 V circuits that are fast when on and leak little when off.
- **Hierarchical sizing.** Kao, Narendra and Chandrakasan (1998) size the shared switches from the patterns of the discharge currents of the gates, as in Claim 1.
- **Processor cores.** Mobile and server processors gate the supply of idle cores, with the state saved before sleep, and gate units such as vector units within a core.
- **Memories.** Arrays drop to a retention voltage or switch off their periphery in sleep, a related form that keeps the data.

## Variations

- **Fine grain and coarse grain.** A switch in each cell responds fast and needs no shared rail, but costs area in every cell. A ring or grid of shared switches for a block costs less area and needs the sizing of Claim 1.
- **Header or footer.** NMOS footers have more drive per width. PMOS headers keep the ground common, which helps the isolation and the level of the signals.
- **Retention.** A retention register keeps its value in a small extra latch on an always-on supply while the main latch is off. Only the needed registers are made retention registers, since they cost area and leak.
- **Multi-mode switches.** Some designs drive the switch gates to an intermediate voltage, which keeps the virtual rail at a level that holds the state with less leakage than full on.
- **Dynamic voltage scaling.** Lowering the supply and the clock of a busy block saves power when it cannot sleep. The online policy is studied as [speed scaling](/speed-scaling/).
- **Multi-threshold design.** The [threshold assignment](/multi-threshold-voltage-assignment/) reduces the leakage of a block while it is on. Power gating reduces it while it is off. Designs use both.

## Pitfalls

- **Inrush current.** Turning on all the switches at once recharges the virtual rail from near 0 with a large current step, which makes the supply of the neighbor blocks droop. Turn the switches on in a chain with delay, and check the neighbors with [power grid analysis](/power-grid-analysis/) and their [decaps](/decoupling-capacitance-allocation/).
- **Floating outputs.** The outputs of a sleeping block drift to unknown levels. An input of an active block that floats near the middle turns on both of its transistors and draws a large current. Clamp the outputs with isolation cells, as in line L3, before the switch turns off.
- **Losing state.** Registers without retention lose their value. A wrong order in line L5, such as turning off before the save is done, loses the state.
- **Undersized switches.** Too much drop across the switch makes the block slow and can fail timing. Size for the largest total current, and include the drop in timing analysis.
- **Too short sleeps.** Sleeping for less than $t_{\text{be}}$ costs more energy than it saves, and each wake adds latency.
- **Verification.** The always-on control, the clamps and the retention form a power intent that the RTL alone does not show. It must be written in a format that the tools check, and simulated with the supply turned off and on.

## Exercises

1. Show that the deterministic policy of waiting $t_{\text{be}}$ before sleeping uses at most twice the energy of the best policy that knows the idle length in advance.
2. Two gates draw triangular currents of peak 2 mA, each 20 ps wide, that start 10 ps apart. Compute $\max_t \sum_g I_g(t)$ and compare it with the sum of the peaks.
3. With the numbers of the sizing example, how much wider must the switch be if the allowed drop falls from 5% to 2% of $V_{DD}$?
4. A virtual rail has decayed to 0.4 V when the block wakes. How much energy does recharging it to 1 V draw from the supply, with $C = 1$ nF?

## References
