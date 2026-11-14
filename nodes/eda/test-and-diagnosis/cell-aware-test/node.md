---
tag: 3RSPMX
kind: technique
slug: cell-aware-test
name: Cell-aware test
aliases:
- cell-internal fault test
- CAT
area: eda/test-and-diagnosis
level: research
summary: Hapke and coauthors' method that simulates defects inside each library cell at transistor level and targets the resulting cell-input patterns in ATPG.
prereqs: [stuck-at-fault-model, automatic-test-pattern-generation]
see_also: [bridging-fault-model, iddq-testing, n-detect-test, switch-level-simulation, modified-nodal-analysis, critical-area, transition-fault-model, fault-coverage]
sources:
  - paper: "F. Hapke, R. Krenz-Baath, A. Glowatz, J. Schloeffel, H. Hashempour, S. Eichenberger, C. Hora and D. Adolfsson, Defect-oriented cell-aware ATPG and fault simulation for industrial cell libraries and designs, Proceedings of the IEEE International Test Conference, paper 1.2, 2009"
    title: F. Hapke and coauthors, Defect-oriented cell-aware ATPG and fault simulation for industrial cell libraries and designs, Proceedings of the IEEE International Test Conference, paper 1.2, 2009
    locator: the cell-aware flow (layout extraction, defect simulation of every cell at transistor level, the defect detection matrix, and cell-aware ATPG), applied to a 65 nm library of about 1500 cells and to 10 designs
  - paper: doi:10.1109/TCAD.2014.2323216
    title: F. Hapke, W. Redemund, A. Glowatz, J. Rajski, M. Reese, M. Hustava, M. Keim, J. Schloeffel and A. Fast, Cell-aware test, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 33(9), 1396 to 1409, 2014
    locator: the journal account of the method, with the cell-aware fault model generation for 1940 library cells and its use on several industrial designs
  - paper: doi:10.1002/j.1538-7305.1978.tb02106.x
    title: R. L. Wadsack, Fault modeling and logic simulation of CMOS and MOS integrated circuits, Bell System Technical Journal 57(5), 1449 to 1474, 1978
    locator: the CMOS stuck-open fault, which makes a gate output float and needs a two-pattern test
---

Cell-aware test is a way to make test patterns for defects inside the library cells of a chip, such as a short between two internal nodes of an AOI gate, which the [stuck-at fault model](/stuck-at-fault-model/) on cell pins does not describe. For every cell of the library it lists the possible opens and shorts in the cell layout, simulates each defective cell at transistor level for every input pattern, and records in a **defect detection matrix** which cell-input patterns make the output wrong. ATPG then gets, for every instance of the cell, the target "apply one of these patterns at the cell inputs and propagate the output error". Hapke and coauthors introduced the method in 2009. This page proves when such a target is detected and when a stuck-at test already detects it, proves that a logic-level transistor model cannot fill the matrix by itself, and shows a short in an AOI22 cell that a complete stuck-at test can miss.

## In plain words

A stuck-at test checks the wires between cells. Many real defects sit inside a cell: an extra piece of metal shorts two internal nodes, or a contact is missing and a transistor never turns on. Such a defect can make the cell wrong for only one or two of its input patterns, and a stuck-at test set may never apply those patterns to that cell.

Cell-aware test does the work cell by cell, once per library. It asks a circuit simulator: with this defect, for which input patterns is the output wrong? The answer is a short list of patterns per defect. Test generation then makes sure that each cell in the chip gets one of those patterns, and that the wrong output reaches a scan cell or an output pin.

## When it applies

- Scan-based test of standard-cell designs, where the combinational logic between scan cells is built from library cells and ATPG controls the cell inputs.
- The layout of every cell is available, so the candidate defects can be extracted from it, and a transistor-level circuit simulator is available for the characterization.
- The defect effect stays inside one cell: it changes the output of the cell but not the nets that drive its inputs. A short from a cell input to another net breaks this, and is a [bridging fault](/bridging-fault-model/) between nets instead.
- High quality targets, such as automotive parts, where defects that escape stuck-at and [transition](/transition-fault-model/) tests matter.

## The template

Write a cell with inputs $x_1, \dots, x_k$, output $o$ and good function $y$. For a test vector $v$ of the circuit, $p(v) \in \{0,1\}^k$ is the pattern that $v$ puts on the inputs of one cell instance. For a defect $\delta$ of the cell, $D_\delta \subseteq \{0,1\}^k$ is its row of the defect detection matrix: the patterns $p$ for which the defective cell output reads $\lnot y(p)$.

```pseudo id=main
CELL-AWARE(L, C)
L1  for each cell type k of the library L
L2      extract the transistor netlist of k, with parasitics, from its layout
L3      list the candidate opens and shorts of k, each with a chosen resistance
L4      for each defect δ and each input pattern p of k
L5          simulate the defective cell at transistor level; put p in D_δ if the output reads the wrong value
L6      merge defects with equal rows; drop the rows that a pin stuck-at fault covers
L7  for each instance of a cell type k in the circuit C and each row D_δ that is left
L8      add the target: some p in D_δ at the instance inputs, with the output error propagated
L9  run ATPG and fault simulation on these targets together with the stuck-at faults
```

Lines L1 to L6 are the **library characterization**. They run once per library and per process, and their result is stored as a cell-aware fault model of each cell. Lines L7 to L9 run per design. The holes are the defect list and the resistances at line L3, the simulator and the pass threshold at line L5, and the ATPG at line L9. Two-cycle defects, such as opens that make the output float, get a matrix over pattern pairs $(p_1, p_2)$ instead of single patterns, applied as in [launch-on-capture and launch-on-shift](/launch-on-capture-and-launch-on-shift/) tests.

**When a vector detects a cell-internal defect.** Assume the circuit is combinational, the defect sits in one instance of a single-output cell, and it does not change the nets that drive the inputs of that instance. Then a vector $v$ detects $\delta$ exactly when $p(v) \in D_\delta$ and $v$ detects the stuck-at fault $o$ stuck at $\lnot y(p(v))$. Proof: the inputs of the instance are not in its own fanout cone, because a combinational circuit has no cycle, and the defect does not change them, so the defective circuit also puts $p(v)$ on them. If $p(v) \notin D_\delta$ the cell output is right, every other gate computes what it computes in the good circuit, and the outputs agree. If $p(v) \in D_\delta$ the defective circuit under $v$ is the good circuit with $o$ forced to $\lnot y(p(v))$, which is the circuit with that stuck-at fault, so the outputs differ exactly when $v$ detects it. So a cell-aware fault is a stuck-at fault on the cell output with a condition on the cell inputs, and line L8 is an ordinary ATPG target with extra input constraints.

**When a stuck-at test already covers it.** Let $\varphi$ be a stuck-at fault on a pin of the same instance: on an input pin (the branch of the input net that enters this cell) or on $o$. Let $S_\varphi$ be the patterns $p$ for which the cell output with $\varphi$ differs from $y(p)$. If $S_\varphi \subseteq D_\delta$, every test of $\varphi$ detects $\delta$. Proof: the effect of $\varphi$ is also confined to the cell output, so by the same argument, $v$ detects $\varphi$ exactly when $p(v) \in S_\varphi$ and $v$ detects $o$ stuck at $\lnot y(p(v))$. Then $p(v) \in D_\delta$, and the condition above gives that $v$ detects $\delta$. This is the test at line L6. The converse does not hold: a row that contains no $S_\varphi$ can still be detected by luck, but no stuck-at target forces it.

**Why the matrix needs a circuit simulator.** Model a static complementary CMOS cell at switch level: every transistor is an ideal switch, and for each input pattern exactly one of the pull-up and pull-down networks connects $o$ to its supply rail. An open removes a conducting path. A transistor that is always on, or a short between two nodes, adds a connection. Claim: for every pattern, the defective output is the good value, or **Z** (connected to no rail) for a defect that removes, or **C** (connected to both rails) for a defect that adds. Proof: removing connections cannot connect $o$ to the wrong rail, so it keeps the good value or loses both rails. Adding connections cannot disconnect $o$ from the right rail, so it keeps the good value or also reaches the wrong rail. In the C case the two rails are connected, so a quiescent supply current flows, which is what [IDDQ testing](/iddq-testing/) measures. So no single defect of this kind gives a clean wrong logic value in the switch model. Whether a C entry reads 0 or 1 is decided by the resistances of the two paths, and a Z entry holds the charge of the previous pattern, so it needs a pattern pair. This is why line L5 uses transistor-level simulation, such as a SPICE run built on [modified nodal analysis](/modified-nodal-analysis/), and not a [switch-level model](/switch-level-simulation/).

**Example: the NAND2 matrix at switch level.** The NAND2 cell $o = \lnot(AB)$ has PMOS transistors $P_A$ and $P_B$ in parallel from VDD to $o$, and NMOS transistors $N_A$ from $o$ to an internal node $n_1$ and $N_B$ from $n_1$ to GND. With 4 opens, 4 stuck-on transistors and the 5 shorts between the nodes VDD, GND, $o$ and $n_1$ (all pairs except VDD with GND), the switch-level rows over the patterns $AB = 00, 01, 10, 11$ are:

| defect | 00 | 01 | 10 | 11 |
|---|---|---|---|---|
| good cell | 1 | 1 | 1 | 0 |
| $P_A$ open | 1 | Z | 1 | 0 |
| $P_B$ open | 1 | 1 | Z | 0 |
| $N_A$ open, $N_B$ open | 1 | 1 | 1 | Z |
| $P_A$ on, $P_B$ on, short $o$ to VDD | 1 | 1 | 1 | C |
| $N_A$ on, short $o$ to $n_1$ | 1 | C | 1 | 0 |
| $N_B$ on, short $n_1$ to GND | 1 | 1 | C | 0 |
| short $o$ to GND | C | C | C | 0 |
| short $n_1$ to VDD | 1 | C | 1 | C |

Every entry is good, Z or C, as the claim says. The defects on one line have equal rows and are merged at line L6. The $P_A$ open gives the classic CMOS stuck-open fault: the pair $(11, 01)$ first sets $o = 0$, then leaves $o$ floating at 0 where the good cell gives 1.

**Example: one short, three behaviours.** Resolve the short from $o$ to GND with a linear resistor model: a conducting PMOS has resistance $R_p$, the short has resistance $R_s$, and the output reads 0 below half the supply voltage. At pattern 00 both PMOS conduct and the output voltage is $R_s / (R_s + R_p/2)$ times the supply. At 01 and 10 one PMOS conducts and it is $R_s / (R_s + R_p)$. So the row is $\{00, 01, 10\}$ if $R_s < R_p/2$, the same as the pin fault $o$ stuck-at 0. It is $\{01, 10\}$ if $R_p/2 < R_s < R_p$, which contains $S_{A/1} = \{01\}$, so a test for $A$ stuck-at 1 covers it. And it is empty if $R_s > R_p$: the defect is invisible to a logic test, and only the extra supply current, or a slower transition, shows it. The same defect is three different faults depending on $R_s$ and $R_p$, and these numbers are not known from the logic. $R_p$, $R_n$ and $R_s$ here are model parameters, not measured values.

**Example: a short that a complete stuck-at test misses.** The AOI22 cell $o = \lnot(AB + CD)$ has pull-down paths $N_A$, $N_B$ through node $n_1$ and $N_C$, $N_D$ through node $n_2$, and a pull-up of $P_A \parallel P_B$ in series with $P_C \parallel P_D$. A short between $n_1$ and $n_2$ adds a connection, so its only non-good entries are C, and they are at the patterns where it closes a new path from $o$ to GND while the good output is 1: $ABCD = 0110$ (through $N_C$, the short and $N_B$) and $1001$ (through $N_A$, the short and $N_D$). At 0110 the pull-up is $P_A$ in series with $P_D$, so the output voltage is

$$\frac{2R_n + R_s}{2R_n + R_s + 2R_p}$$

times the supply, and the output reads 0 exactly when $R_s < 2(R_p - R_n)$. With $R_p = 2R_n$, a typical textbook ratio for PMOS and NMOS of equal width, a short below $2R_n$ gives the row $\{0110, 1001\}$. With a PMOS sized so that $R_p = R_n$, it never reads wrong, and only IDDQ or delay can show it. Now take the row $\{0110, 1001\}$. Every pin set of the AOI22 has 3 or 9 or 7 patterns, so none fits inside it, and line L6 keeps it. The four patterns $\{0101, 1010, 1100, 0011\}$ meet every pin set of the cell ($A/1$ and $C/1$ by 0101, $B/1$ and $D/1$ by 1010, $A/0$ and $B/0$ by 1100, $C/0$ and $D/0$ by 0011, and the output faults by these too), so a stuck-at test set can detect all 10 pin faults of this instance while it puts only these four patterns on it. Such a test set never applies 0110 or 1001 to the cell, so it never detects the short, whatever $R_s$ is. The cell-aware target at line L8 forces one of the two.

**Counts in the toy model.** These are computed with the linear resistor model above, not with a real library: $R_n = 1$, $R_p = 2$, $R_s = 1/1000$, threshold one half, and the same defect list (opens, stuck-on transistors, and shorts between every pair of nodes except VDD with GND). Of the 30 defects of the AOI22, 14 have a row that a pin fault covers, 4 have a non-empty row that no pin fault covers (the shorts $n_1$ to $n_2$, $m$ to $n_2$, $o$ to $m$ and VDD to $m$, where $m$ is the node between the two PMOS pairs), 8 opens need a pattern pair, and the 4 PMOS stuck-on defects never read wrong and show only as supply current. With $R_p = R_n$ instead, several entries sit exactly at the threshold, which a real flow resolves with a delay or voltage margin.

**Cost.** Line L5 runs $2^k$ static simulations per defect, or $2^{2k}$ pattern pairs for two-cycle defects, for each of the hundreds or thousands of cells of a library. This is expensive, but done once per library. Per design, the number of targets grows with the number of instances times the rows that remain after line L6, so cell-aware ATPG makes more patterns than stuck-at ATPG.

## Classic examples

- **Hapke and coauthors (2009).** The first cell-aware flow, with layout extraction, analog defect simulation and cell-aware ATPG, applied to a 65 nm library of about 1500 cells and to 10 designs.
- **Hapke and coauthors (2014).** The journal account of the method, with cell-aware fault models generated for 1940 library cells and applied to industrial designs.
- **The CMOS stuck-open fault.** Wadsack (1978) showed that an open transistor in a CMOS gate makes the output float for some patterns, so a single pattern cannot detect it. It is the classic example of a cell-internal defect that needs a two-pattern test.

## Variations

- **Static and two-cycle faults.** A static row lists single patterns. A two-cycle row lists pattern pairs, for opens and for resistive defects that only slow the cell, as with [transition faults](/transition-fault-model/).
- **Applying every pattern at every cell.** Without defect simulation, one can ask ATPG to apply all $2^k$ patterns at the inputs of every cell. This needs no layout, but makes many more targets than the rows that defects actually produce.
- **Layout-driven defect lists.** The shorts at line L3 can be weighted by their [critical area](/critical-area/), so that likely defects count more in the coverage figure.
- **Diagnosis.** The same matrices let diagnosis name a defect inside a cell, not only a failing cell pin.
- **Compared with N-detect.** [N-detect tests](/n-detect-test/) raise the chance of hitting unmodelled defects by detecting each stuck-at fault many times. Cell-aware test models the defects instead, at a characterization cost.

## Pitfalls

- **The matrix depends on the resistances.** As the examples show, the same short can be a stuck-at fault, a pattern-specific fault or a logically invisible one, depending on resistance values that are chosen, not measured. Report the values used.
- **Defects that change cell inputs.** A short from a gate input of the cell to another node can disturb the cell that drives that input. The detection condition above then does not hold, and the defect needs a model across cells.
- **Multi-output cells and flip-flops.** Full adders and sequential cells have more than one output or state, so a row must say which output is wrong, and the pin coverage test must compare the right outputs.
- **Pattern count.** Cell-aware targets add patterns. Use [dynamic test compaction](/dynamic-test-compaction/) and drop the rows that a pin fault covers before ATPG.

## Exercises

1. Build the switch-level matrix of an inverter with its 2 opens, 2 stuck-on transistors and 2 shorts (output to VDD and output to GND), and check the claim that every entry is good, Z or C.
2. In the NAND2, find the pattern pairs that detect the $N_A$ open, and explain why no single pattern detects it.
3. For the AOI22 short between $n_1$ and $n_2$, compute the output voltage at 1001 and show that the condition for a wrong value is the same as at 0110.
4. Prove that the row of the short from $o$ to GND in an AOI22 contains $S_\varphi$ for the output fault $o$ stuck-at 0 when $R_s$ is small enough, so that it is covered by a stuck-at test.

## References
