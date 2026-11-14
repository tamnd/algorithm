---
tag: ZDMNMW
kind: technique
slug: boundary-scan
name: Boundary scan
aliases:
- IEEE 1149.1
- JTAG
area: eda/test-and-diagnosis
level: core
summary: The IEEE 1149.1 standard that places a scan cell at each chip pin, driven by a test access port controller, to test board interconnect and access chip test logic.
prereqs: [scan-design]
see_also: [soc-test-wrapper-and-tam-design, built-in-self-test, moore-machine, deterministic-finite-automaton, bridging-fault-model, stuck-at-fault-model, dilworth-theorem, hamming-distance]
sources:
  - paper: "IEEE Std 1149.1-1990, IEEE Standard Test Access Port and Boundary-Scan Architecture, IEEE, 1990, revised 2001 and 2013"
    title: IEEE Standard Test Access Port and Boundary-Scan Architecture, IEEE Std 1149.1
    locator: the test access port, the 16-state TAP controller and its state diagram, the instruction register, the boundary-scan and bypass registers, and the instructions BYPASS, SAMPLE, PRELOAD, EXTEST and IDCODE
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer Academic Publishers, 2000
    locator: the chapter on boundary scan (the TAP controller, the boundary cells, and interconnect test and diagnosis with counting sequences)
  - book: isbn:9780123705976
    title: Laung-Terng Wang, Cheng-Wen Wu and Xiaoqing Wen, VLSI Test Principles and Architectures, Morgan Kaufmann, 2006
    locator: the chapter on boundary scan and core-based test (IEEE 1149.1 and IEEE 1500)
---

Boundary scan puts a scan cell between each pin of a chip and its core logic, and links these cells into a shift register, the boundary register, that is reached through four dedicated pins: test data in (TDI), test data out (TDO), test clock (TCK) and test mode select (TMS), with an optional reset (TRST). The rules are IEEE Std 1149.1, first published in 1990 from the work of the Joint Test Action Group, so the technique is also called JTAG. A small state machine, the test access port (TAP) controller, decides on each TCK edge, from TMS alone, whether the bits shifted in go to the instruction register or to a data register. With the chips of a board chained TDI to TDO, a tester can drive any output pin and read any input pin without probes, which tests the wires between chips. The same port reaches test logic inside a chip, such as [built-in self-test](/built-in-self-test/) and the core wrappers of [SoC test](/soc-test-wrapper-and-tam-design/).

## In plain words

On a crowded circuit board, the tiny wires between chips cannot be reached with test probes. Boundary scan adds a small storage cell at every pin of every chip, and links all the cells into one long chain that runs through every chip on the board.

To test a wire, we shift a 1 or a 0 into the cell at the pin that drives it, let the cell put that value on the wire, and then let the cell at the receiving pin record what arrived. Then we shift all the recorded values out and compare. A wire that is broken, or touches another wire, shows the wrong value.

Four extra pins control everything. One of them, together with the clock, steers a small control circuit through its steps.

## When it applies

- The board or system has chips whose pins cannot be probed, such as ball grid array packages, and the chips implement IEEE 1149.1.
- The target faults are on the wires between chips: open wires, wires stuck at a value, and shorts between wires. The cells read and drive the pins, so they test the pins and wires, not the core logic.
- A chip needs a standard serial port into its test logic: an internal [scan design](/scan-design/) chain, a BIST engine, a device code, or the wrappers of embedded cores.

## The template

The TAP controller has 16 states, and TMS, sampled at the rising edge of TCK, chooses the next state. Its transitions are below, written as the next state for TMS = 0 and for TMS = 1. The five missing states, Capture-IR, Shift-IR, Exit1-IR, Pause-IR and Exit2-IR, behave like the matching DR states with IR in place of DR.

| state | TMS = 0 | TMS = 1 |
|---|---|---|
| Test-Logic-Reset | Run-Test/Idle | Test-Logic-Reset |
| Run-Test/Idle | Run-Test/Idle | Select-DR-Scan |
| Select-DR-Scan | Capture-DR | Select-IR-Scan |
| Select-IR-Scan | Capture-IR | Test-Logic-Reset |
| Capture-DR | Shift-DR | Exit1-DR |
| Shift-DR | Shift-DR | Exit1-DR |
| Exit1-DR | Pause-DR | Update-DR |
| Pause-DR | Pause-DR | Exit2-DR |
| Exit2-DR | Shift-DR | Update-DR |
| Update-DR | Run-Test/Idle | Select-DR-Scan |
| Update-IR | Run-Test/Idle | Select-DR-Scan |

Each boundary cell has a shift stage, which is part of the chain, and an update stage, which holds the value applied to the pin, so that values do not ripple on the pins during the shift. The template of a board interconnect test is then:

```pseudo id=main
INTERCONNECT-TEST(the chain of chips, the vectors v_1, ..., v_k)
L1  hold TMS = 1 for 5 TCK cycles                 ▷ Test-Logic-Reset from any state
L2  shift the instruction SAMPLE/PRELOAD into every chip, shift v_1 into the boundary registers
L3  shift the instruction EXTEST into every chip  ▷ the update stages now drive the pins
L4  for i ← 1 to k do
L5      Capture-DR: every input cell records the value on its pin
L6      Shift-DR: shift the recorded values out on TDO while v_(i+1) shifts in on TDI
L7      Update-DR: the output cells drive v_(i+1)
L8      compare the recorded values with those expected for v_i
L9  return the nets whose recorded values differ
```

After the last vector, line L6 shifts in a safe vector. The holes are the vectors $v_i$, the order of chips in the chain, and the instructions. A chip that takes no part in a test is put in BYPASS, which makes it a 1-bit register in the chain, so its cells do not lengthen the shifts.

**Why 5 cycles reset the controller.** Let $d$ be 0 for Test-Logic-Reset, 1 for Select-IR-Scan, 2 for Select-DR-Scan, 3 for Run-Test/Idle and both Update states, 4 for the four Exit states, and 5 for the Capture, Shift and Pause states of both columns. Every state gets a value, since these lists cover all 16. From the table, TMS = 1 moves each state with $d \ge 1$ to a state with $d$ smaller by exactly one: Select-IR-Scan to Test-Logic-Reset, Select-DR-Scan to Select-IR-Scan, Run-Test/Idle and the Update states to Select-DR-Scan, each Exit state to its Update state, and each Capture, Shift and Pause state to an Exit state. TMS = 1 keeps Test-Logic-Reset where it is. So after $j$ cycles with TMS = 1 the state has $d \le \max(0, 5 - j)$, and after 5 cycles it is Test-Logic-Reset, whatever the start state was, even right after power-up, when the state is unknown. Five is the least number that works: from Shift-DR, four cycles reach only Select-IR-Scan, since each cycle lowers $d$ by exactly one. $\blacksquare$

This is why the TRST pin is optional: TMS alone can always bring the controller to a known state. From Test-Logic-Reset, TMS = 0, 1, 0, 0 reaches Shift-DR, and TMS = 0, 1, 1, 0, 0 reaches Shift-IR.

**The vectors.** Consider $n$ nets, each with one driver, and read the $k$ vectors one net at a time: net $i$ receives the $k$-bit code $c_i$, the bits that $v_1, \ldots, v_k$ give its driver. Model faults as follows: an open or stuck net reads all 0 or all 1, and a short between two nets makes both read the AND of their codes (or the OR, depending on the technology). Then:

- If the codes are distinct and none is all 0 or all 1, every stuck net and every short of two nets is detected. A stuck net reads a constant code, which is not its own. A shorted pair both read $c_i \wedge c_j$, and if neither changed, $c_i = c_i \wedge c_j = c_j$, which contradicts distinct codes. The same holds for OR.
- So $k = \lceil \log_2 (n + 2) \rceil$ vectors suffice, with the codes $1, 2, \ldots, n$ in binary, the counting sequence. For $n = 6$ nets, 3 vectors give the codes 001, 010, 011, 100, 101, 110. For $n = 1000$ nets, 10 vectors suffice, against 1000 vectors of one changing net at a time.
- Detection is not diagnosis. In the 6-net example, a wired-AND short of the nets with codes 001 and 011 makes both read 001. The net with code 011 then reads the code of the other net, so the response looks like net 011 shorted to net 001 or like other faults, and the culprit can be ambiguous. Diagnosis needs codes in which no code is covered by another (an antichain), for example codes of $k$ bits with exactly $\lfloor k/2 \rfloor$ ones. Then the AND of two distinct codes is never a code. There are $\binom{k}{\lfloor k/2 \rfloor}$ such codes, and by Sperner's theorem no antichain is larger, so this choice uses the fewest vectors among antichain codes, a little more than $\log_2 n$.

The test time is about $k (B + c)$ TCK cycles for $B$ boundary cells in the chain and a few cycles $c$ of state moves per vector.

## Classic examples

- **Board interconnect test.** The case above: EXTEST drives the output pins of one chip from its boundary cells and captures the input pins of the next, finding opens, [stuck nets](/stuck-at-fault-model/) and shorts of the kind in the [bridging fault model](/bridging-fault-model/).
- **Sampling a running system.** SAMPLE copies the values on all pins into the boundary register without disturbing the chip, which is used for debug.
- **Access to on-chip test logic.** Private instructions connect TDI and TDO to an internal [scan chain](/scan-design/), start a [built-in self-test](/built-in-self-test/) engine and read its signature, or reach the wrappers and test buses of embedded cores in [SoC test](/soc-test-wrapper-and-tam-design/).
- **Identification and programming.** The optional 32-bit IDCODE register tells which chip sits where in the chain, and in-system programming of flash memories and programmable logic uses the same port.

## Variations

- **IEEE 1149.4** adds analog test buses for mixed-signal boards, **IEEE 1149.6** tests AC-coupled and differential links, whose capacitors block the static values of 1149.1, and **IEEE 1149.7** reduces the port to two pins.
- **IEEE 1500** reuses the ideas of boundary scan for cores inside a chip: a wrapper of boundary cells around each core, a serial instruction port and an optional parallel port, controlled from the chip-level TAP.
- **IEEE 1687 (IJTAG)** describes networks of instruments inside a chip, with segments that can be switched into or out of the scan path, all reached through the TAP.
- **Codes for diagnosis.** Besides counting and constant-weight codes, a "walking one" sequence of $n$ vectors gives each net its own one-hot code. It is long but makes every short of two nets fully diagnosable.

## Pitfalls

- **EXTEST without PRELOAD.** If EXTEST is loaded while the update stages hold random values, the output pins drive those values at once, and two chips can drive one bus against each other. Preload a safe vector first with SAMPLE/PRELOAD, as in line L2.
- **One shared net, several drivers.** Tri-state and bidirectional nets have several possible drivers. Each vector must enable exactly one of them, using the control cells, or the test itself makes a short.
- **The all-0 and all-1 codes.** A net with code 00...0 or 11...1 reads the same code when it is stuck, so its fault is missed. Leave both codes out, which is why the count is $n + 2$.
- **Counting codes for diagnosis.** Codes where one covers another, such as 001 and 011, detect a short but may blame the wrong net. Use antichain codes when the repair needs the culprit.
- **Long chains.** All chips in the chain add to every shift. Put chips that take no part in BYPASS, and split long chains if the board has more than one TAP.
- **TMS errors.** One wrong TMS bit moves the controller to another state, and the rest of the sequence lands somewhere else. Make test sequences start with the 5-cycle reset, so a run never depends on the state left by the last one.

## Exercises

1. Draw the 16-state TAP controller and give the shortest TMS sequence from Pause-IR to Shift-DR.
2. Show that from every state some TMS sequence of at most 5 bits reaches Shift-DR, and that the states Select-IR-Scan, Capture-IR, Shift-IR and Pause-IR need 5.
3. A wired-AND short of $r \ge 2$ nets makes all of them read the AND of their codes. Show that distinct codes, none all 0 or all 1, detect every such short, for every $r$, and the same for wired-OR.
4. Show that with constant-weight codes of weight $\lfloor k/2 \rfloor$, the AND of two distinct codes is never a code and the OR of two distinct codes is never a code.

## References
