---
tag: A625JB
kind: technique
slug: scan-design
name: Scan design
aliases:
- scan chain
- full scan
area: eda/timing-and-verification
level: core
summary: Links the registers of a circuit into shift registers in test mode, so test generation needs only the combinational logic between registers.
prereqs: [stuck-at-fault-model, automatic-test-pattern-generation]
see_also: [podem, fault-simulation, built-in-self-test, scoap, setup-and-hold-constraints, feedback-vertex-set-problem, traveling-salesman-problem]
sources:
  - paper: "E. B. Eichelberger and T. W. Williams, A logic design structure for LSI testability, Proceedings of the 14th Design Automation Conference, 462 to 468, 1977"
    title: E. B. Eichelberger and T. W. Williams, A logic design structure for LSI testability, Proceedings of the 14th Design Automation Conference, 462 to 468, 1977
    locator: level-sensitive scan design, with pairs of latches, non-overlapping clocks and shift clocks for test
  - paper: doi:10.1109/PROC.1983.12531
    title: T. W. Williams and K. P. Parker, Design for testability, a survey, Proceedings of the IEEE 71(1), 98 to 112, 1983
    locator: the survey of ad hoc and structured design for testability, with scan path, LSSD, scan/set and random access scan
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Digital DFT and Scan Design (scan flip-flops, the scan test protocol, test time, partial scan), and the chapter Boundary Scan
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter Design for Testability (scan registers, full and partial scan, LSSD)
---

Scan design adds a test mode in which the flip-flops of a synchronous sequential circuit are linked into one or more shift registers, called scan paths. In test mode, the tester shifts a chosen state into the flip-flops, applies the primary inputs, gives one functional clock to capture the next state, and shifts the captured state out while the next state goes in. So each flip-flop output acts as an extra primary input and each flip-flop input as an extra primary output, and a test for the sequential circuit is a test for its combinational logic. With full scan, every flip-flop is in a scan path, and [automatic test pattern generation](/automatic-test-pattern-generation/) only has to solve the combinational problem. The price is a multiplexer at each flip-flop, the wiring of the paths, a small delay on the functional path, and a test time that grows with the length of the paths. This is an EDA page. Level-sensitive scan design, or LSSD, is the latch-based form of Eichelberger and Williams (1977) at IBM.

## In plain words

A chip with memory is hard to test. To check one gate deep inside, you must first steer the memory into the right state, which can take many clock cycles. Then you must wait until a wrong value reaches a pin.

Scan design adds a back door. In test mode, all the flip-flops join into one long shift register. You shift in any state you want, one bit per clock. Then the circuit runs for one normal clock, and the flip-flops catch the next state. Then you shift that out and read it.

Now every flip-flop is like an extra input pin and an extra output pin. The test only has to deal with the logic between flip-flops, which has no memory.

## When it applies

- The circuit is synchronous: flip-flops with a common clock or a few clocks, and combinational logic between them. In the usual model, the combinational logic $C$ has the primary inputs $X$, the primary outputs $Z$, the present state $Y$ from the flip-flop outputs and the next state $Y'$ into the flip-flop inputs.
- Test generation without scan is too hard. A sequential test is a sequence of vectors from a known state, and its search grows with the number of clock cycles it needs. The example below has a fault that needs $2^k - 1$ clock cycles to reach in a $k$-bit counter.
- The design can pay for a multiplexer at each flip-flop and a scan enable signal, and the tester can control the clocks in test mode.

## The template

A **mux-D scan flip-flop** is a D flip-flop with a two-input multiplexer in front of its D input. The scan enable SE selects the functional input when SE = 0 and the scan input SI when SE = 1.

```pseudo id=main
SCAN-INSERT(C)
L1  for each flip-flop F of C do replace F by a scan flip-flop with SE and SI
L2  order the scan flip-flops into paths F_1, ..., F_N
L3  connect a scan-in pin to SI of F_1, Q of F_k to SI of F_(k+1), and Q of F_N to a scan-out pin
L4  run combinational ATPG on C with inputs X ∪ Y and outputs Z ∪ Y'

SCAN-TEST(the patterns (x_1, y_1), ..., (x_T, y_T))
L5  SE ← 1; shift y_1 in with N clocks
L6  for j ← 1 to T do
L7      SE ← 0; apply x_j; compare Z with the expected outputs; give one clock to capture Y'
L8      SE ← 1; shift N clocks: the captured Y' comes out and is compared, and y_(j+1) goes in
L9  return pass if every compare agreed
```

The holes are the scan cell (mux-D, the LSSD latch pair, or a flip-flop with a second clock), the order of the flip-flops in line L2, and the number of paths. In the last pass of line L8 there is no $y_{T+1}$, and any bits go in.

**Why full scan makes ATPG combinational.** Assume that the scan paths themselves work. Line L5 or the previous line L8 puts any wanted value $y_j$ on $Y$. Line L7 puts $x_j$ on $X$ and reads $Z$, and the clock stores $Y'$ in the flip-flops. Line L8 reads $Y'$ at the scan-out pin, since in shift mode the flip-flops only pass bits along and the logic $C$ does not take part. So a scan pattern applies one vector of $C$ with the inputs $X \cup Y$ and reads every output of $Z \cup Y'$. A single stuck-at fault inside $C$ does not change the shift, so the fault is detected by some scan pattern exactly when it is detectable in the combinational circuit $C$ with these inputs and outputs. Faults on the scan paths and on SE are tested separately, by the flush test under Pitfalls.

**Test time.** With $N$ flip-flops in one path and $T$ patterns, line L5 takes $N$ clocks and each pass of lines L7 and L8 takes $1 + N$, so the test takes

$$N + T(1 + N) = (T + 1) N + T$$

clock cycles. With the flip-flops split into $c$ balanced paths that shift at the same time, $N$ becomes $\lceil N / c \rceil$. For $T = 1000$ patterns and $N = 10^4$ flip-flops, one path takes 10 011 000 cycles and 100 paths take 101 100 cycles.

**Example.** Take a 3-bit counter with state $q_2 q_1 q_0$, reset to 000, and the output $z = q_2 q_1 q_0$, the carry out. The next state logic is $d_0 = \lnot q_0$, $d_1 = q_1 \oplus q_0$, $c_1 = q_1 q_0$, $d_2 = q_2 \oplus c_1$, and the output is $z = q_2 c_1$. With the stems of $q_2$, $q_1$, $q_0$ and $c_1$ split into branches, $C$ has 17 lines and 34 single stuck-at faults.

Without scan, the counter has no inputs, so the only test is to reset it and watch $z$. The fault $z$/0 shows only in the state 111, which is reached 7 clock edges after reset, and the fault $c_1$/0 also needs the good machine in 111 to differ. A run of 8 clock periods that reads $z$ in the states 000 to 111 detects all 34 faults, if the reset works in the faulty machine too.

With full scan, $C$ has the inputs $q_2, q_1, q_0$ and the outputs $d_2, d_1, d_0, z$. All 34 faults are detectable, and a search over all sets of vectors shows that the smallest test set has 4 vectors, for example 001, 011, 110 and 111. With $N = 3$ and $T = 4$, the scan test takes $(4 + 1) \cdot 3 + 4 = 19$ cycles, more than the 8 cycles of the functional run. The gain shows as the counter grows. In a $k$-bit counter, $z$/0 needs $2^k - 1$ clock edges from reset, about $4.3 \times 10^9$ for $k = 32$, but one scan pattern sets the state of all ones with $k$ shift clocks. And this counter has no inputs, so its functional run is forced. In a circuit with inputs, a sequential test generator must also search over the input sequences, and scan removes that search.

## Classic examples

- [Automatic test pattern generation](/automatic-test-pattern-generation/): with full scan, [PODEM](/podem/), the [D-algorithm](/d-algorithm/) and [SAT-based ATPG](/sat-based-atpg/) work on the combinational logic, and the flip-flops are inputs and outputs.
- [Fault simulation](/fault-simulation/): scan patterns are independent vectors of a combinational circuit, so the fast bit-parallel methods apply, and the order of the patterns does not matter.
- [Built-in self-test](/built-in-self-test/): in the usual logic BIST design, an on-chip pattern generator feeds many scan paths at once, and a compactor takes their outputs.
- Diagnosis and debug: a scan dump stops the clock and shifts out the full state of a failing chip, which locates the cycle and the register where the state first goes wrong.
- Boundary scan, the IEEE 1149.1 standard, puts scan cells at the pins of each chip so that the wiring between chips on a board can be tested.

## Variations

- **LSSD.** Eichelberger and Williams replace each flip-flop by a pair of level-sensitive latches, L1 and L2. In normal mode, non-overlapping system clocks drive them. In test mode, two shift clocks A and B move the bits from L1 to L2 and on to the next pair. Their design rules make the steady-state behavior of the circuit independent of the delays inside it, which also makes test less sensitive to timing.
- **Partial scan.** Put only some flip-flops in scan paths. Draw the S-graph, with a vertex per flip-flop and an edge from $F$ to $G$ when $F$ feeds $G$ through combinational logic. If the flip-flops left out of scan form no cycle, the rest of the circuit is a pipeline, and a sequential test generator needs only a number of time frames bounded by its depth. Choosing the fewest flip-flops that break all cycles is a directed [feedback vertex set problem](/feedback-vertex-set-problem/), which is NP-hard, so tools use heuristics, often with the [SCOAP](/scoap/) sequential measures.
- **Many paths and compression.** Test time falls as the paths get shorter, but each path needs pins. Scan compression puts a decompressor between a few scan-in pins and hundreds of short internal paths, and a compactor before the scan-out pins. Embedded deterministic test, from 2004, is one such scheme.
- **Delay test.** A transition fault needs two vectors: one sets the line and one launches the change, captured at speed. Launch on capture uses two functional clocks after the shift. Launch on shift uses the last shift clock as the launch, which needs a scan enable that can switch at speed.
- **Order of the flip-flops.** Line L2 is free for test, so tools order the flip-flops after placement to keep the scan wiring short. This is a shortest open path through all flip-flops, a form of the [traveling salesman problem](/traveling-salesman-problem/), solved by heuristics.

## Pitfalls

- **Hold time on the scan path.** The path from Q of one flip-flop to SI of the next has little or no logic, so a clock that arrives later at the next flip-flop can make the new bit pass through in the same cycle. Check [hold constraints](/setup-and-hold-constraints/) on every scan connection, add delay where needed, and order the flip-flops by clock domain with a lockup latch where a path crosses domains.
- **The paths must be tested first.** A stuck-at fault on any connection of a path ruins every test that uses it. The flush test shifts a sequence such as 00110011 through each path and compares it at the scan-out pin, which detects a stuck line on the path, since the sequence holds both values.
- **Faults in the scan logic.** The multiplexers and the SE net add new faults. A stem fault on Q that also feeds SI of the next cell disturbs the shift, so it is caught by the flush test, not by a combinational pattern.
- **Shift power.** During shift, many flip-flops change value on each clock, much more than in normal operation. The current can cause supply droop and false failures. Shift at a lower clock rate, or fill the don't-care bits of the patterns so that neighbors agree.
- **Unknown values.** Memories, analog blocks and uninitialized latches can put $X$ values on $Y'$. An $X$ on a captured bit makes the compare useless, and inside a compactor it can hide the whole signature. Block the $X$ sources in test mode.
- **Clocks and resets.** Gated clocks and asynchronous set and reset must be controllable in test mode, or a scan flip-flop cannot shift.
- **Security.** Scan gives full access to the internal state, for example to the key in a cryptographic block. Designs that hold secrets reset the sensitive registers on entry to test mode, or lock the test mode.

## Exercises

1. Derive the test time $(T + 1) N + T$, and give the formula for $c$ paths with lengths $N_1, \ldots, N_c$ that shift at the same time.
2. Show that a $k$-bit counter with the output $z = q_{k-1} \cdots q_0$ and no scan needs $2^k - 1$ clock edges from reset to detect $z$/0.
3. For the 3-bit counter of the example, check that 001, 011, 110 and 111 detect all 34 faults of $C$, and that no 3 vectors do.
4. Show that the flush sequence 0011 detects a stuck-at fault on any connection of a scan path. Which stuck-at faults on the SE net does it detect, and which need a capture cycle?

## References
