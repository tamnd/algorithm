---
tag: D3XRM3
kind: definition
slug: setup-and-hold-constraints
name: Setup and hold constraints
aliases:
- setup time
- hold time
area: eda/timing-and-verification
level: intro
summary: A register's data must be stable from the setup time before to the hold time after the clock edge, which bounds the longest and the shortest paths.
prereqs: [arrival-and-required-time, timing-graph]
see_also: [static-timing-analysis, arrival-and-required-time, clock-skew-scheduling, clock-tree-synthesis, retiming, difference-constraints, false-path]
sources:
  - book: doi:10.1007/978-0-387-93820-2
    title: J. Bhasker and Rakesh Chadha, Static Timing Analysis for Nanometer Designs, A Practical Approach, Springer, 2009
    locator: Chapter 8, Timing Verification (the setup and hold timing checks, multicycle paths and false paths)
  - paper: doi:10.1109/12.55696
    title: John P. Fishburn, Clock skew optimization, IEEE Transactions on Computers 39(7), 945 to 951, 1990
    locator: the two constraints on each pair of registers (zero clocking for the long paths and double clocking for the short paths)
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 1st edition, 2011
    locator: Chapter 8, Timing Closure, Section 8.2 (timing analysis and performance constraints)
---

An edge-triggered register (a flip-flop) copies its data input $D$ to its output $Q$ at each active edge of its clock. It copies the value correctly only if $D$ is stable during a short window around the edge: from the *setup time* $t_{\text{setup}}$ before the edge to the *hold time* $t_{\text{hold}}$ after it. For a path from one register to another this gives two inequalities: the *setup constraint* bounds the longest delay of the path from above, and the *hold constraint* bounds the shortest delay from below. [Static timing analysis](/static-timing-analysis/) checks the setup constraint with the late [arrival times](/arrival-and-required-time/) and the hold constraint with the early ones.

## Definition

Consider a *launch* register $R_1$ and a *capture* register $R_2$ with a combinational path from $Q$ of $R_1$ to $D$ of $R_2$, and a clock with period $T$. Let $c_{\text{launch}}$ and $c_{\text{capture}}$ be the times at which a clock edge reaches the clock pins of $R_1$ and $R_2$. Let $d_{\max}$ and $d_{\min}$ be the largest and the smallest delay from the clock pin of $R_1$ to the data pin of $R_2$, over all paths between them; they include the clock-to-output delay of $R_1$.

**Setup constraint.** The value launched at an edge must reach $R_2$ at least $t_{\text{setup}}$ before the next edge at $R_2$:
$$ c_{\text{launch}} + d_{\max} + t_{\text{setup}} \le c_{\text{capture}} + T. $$
The *setup slack* is $S = c_{\text{capture}} + T - t_{\text{setup}} - (c_{\text{launch}} + d_{\max})$.

**Hold constraint.** The value launched at an edge must not reach $R_2$ before $t_{\text{hold}}$ after the same edge at $R_2$, or it would replace the value that $R_2$ is capturing at that edge:
$$ c_{\text{launch}} + d_{\min} \ge c_{\text{capture}} + t_{\text{hold}}. $$
The *hold slack* is $H = c_{\text{launch}} + d_{\min} - (c_{\text{capture}} + t_{\text{hold}})$. A negative $S$ or $H$ is a violation.

**Late for setup, early for hold.** The setup check uses the largest delay and the latest launch, and the hold check uses the smallest delay and the earliest launch. In the words of [arrival and required time](/arrival-and-required-time/): the data pin of $R_2$ has the late required time $c_{\text{capture}} + T - t_{\text{setup}}$ and the early required time $c_{\text{capture}} + t_{\text{hold}}$. Using the late arrival for the hold check would hide every hold violation.

**Skew.** Let $s = c_{\text{capture}} - c_{\text{launch}}$ be the *clock skew* of the pair. The constraints become
$$ d_{\max} \le T + s - t_{\text{setup}}, \qquad d_{\min} \ge s + t_{\text{hold}}. $$
A positive skew helps the setup constraint and hurts the hold constraint by the same amount. This is the clock skew between two registers of one chip. The [clock skew of distributed systems](/clock-skew/) is the offset between the clocks of two processes, a different idea.

**Two facts that follow.**

- The hold constraint does not contain $T$. A hold violation stays at every clock period, so it cannot be fixed by a slower clock. It is fixed by more delay on the short path or by less skew.
- If every register pair meets its hold constraint, the circuit works at every period $T \ge T_{\min}$, where $T_{\min} = \max (c_{\text{launch}} - c_{\text{capture}} + d_{\max} + t_{\text{setup}})$ over all register pairs joined by a path. With zero skew, $T_{\min}$ is the longest register-to-register delay plus the setup time.

The values $t_{\text{setup}}$ and $t_{\text{hold}}$ are properties of the register cell, given in its library, and can depend on the slews of the data and clock signals. Either one can be negative, but their sum, the width of the window in which $D$ must be stable, is positive for a real register.

## Examples and non-examples

**One register pair.** Let $T = 10$, $c_{\text{launch}} = 0$, $c_{\text{capture}} = 1$, $d_{\max} = 7$, $d_{\min} = 2$, $t_{\text{setup}} = 1$ and $t_{\text{hold}} = 1.5$. The setup slack is $1 + 10 - 1 - (0 + 7) = 3$, so the path meets setup, and it would meet setup at every period $T \ge 7$. The hold slack is $0 + 2 - (1 + 1.5) = -0.5$, a violation at every period. A delay buffer of $0.5$ on the short path only gives $d_{\min} = 2.5$ and hold slack 0. If the buffer also lies on the long path, $d_{\max}$ becomes $7.5$ and the setup slack $2.5$.

**A shift register.** Let the output $Q$ of $R_1$ drive $D$ of $R_2$ by a wire with no delay, with clock-to-output delay $0.3$, so $d_{\min} = d_{\max} = 0.3$. With $t_{\text{hold}} = 0.2$ and a skew $s = 0.2$, the hold slack is $0.3 - 0.2 - 0.2 = -0.1$. Short paths between neighboring registers are where hold violations appear, and they become worse when the clock reaches the capture register later.

**Non-example: a latch.** A level-sensitive latch is transparent while its clock is high. Data that arrives late during the transparent phase passes through and uses time of the next stage (*time borrowing*). The two inequalities above, with a single edge per register, do not describe it; latch timing needs a constraint per phase.

**Non-example: the delay of one path.** $d_{\max}$ and $d_{\min}$ range over all paths from $R_1$ to $R_2$. Checking only the path that a simulation happens to excite is not a setup or hold check. A path that no input can excite may be excluded, but only as a declared [false path](/false-path/).

## Related definitions

- **Multicycle path.** If the design captures the data of a path only every $k$ cycles, the setup constraint uses $kT$ in place of $T$, and the hold check moves by $k - 1$ cycles too. Tools need both settings, and forgetting the hold setting is a known mistake.
- **Clock skew scheduling.** If the clock times $c_i$ are variables, all setup and hold inequalities are [difference constraints](/difference-constraints/) $c_i - c_j \le w_{ij}$. [Clock skew scheduling](/clock-skew-scheduling/) chooses the $c_i$, and [retiming](/retiming/) moves the registers instead.
- **Clock tree synthesis.** The skews $s$ come from the [clock tree](/clock-tree-synthesis/), which is built for zero or bounded skew.
- **Recovery and removal.** For an asynchronous reset pin, the same two checks against the clock edge are called recovery (like setup) and removal (like hold).
- **Metastability.** When $D$ changes inside the window, the register may stay between 0 and 1 for an unbounded time. Setup and hold constraints are the condition under which this does not happen for synchronous paths.

## References
