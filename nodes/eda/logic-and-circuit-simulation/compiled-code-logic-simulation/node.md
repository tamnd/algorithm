---
tag: 6EDHZJ
kind: algorithm
slug: compiled-code-logic-simulation
name: Compiled-code logic simulation
aliases:
- levelized compiled-code simulation
- LCC simulation
area: eda/logic-and-circuit-simulation
level: core
summary: Levelizes a combinational netlist once and turns it into straight-line code with one statement per gate; with bit-parallel words, one run evaluates W input vectors.
solves: [logic-simulation]
model: word-ram
complexity:
  vars: {G: the number of gates, P: the number of gate input pins, N: the number of nets, m: the number of input vectors, W: the word width}
  time: {worst: "O(G log G + P + (m / W + 1) (G + P))", best: "O(G log G + P + (m / W + 1) (G + P))"}
  space: {extra: "O(N + P)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1987
  people: [Zeev Barzilai, J. Lawrence Carter, Barry K. Rosen, Joseph D. Rutledge]
  note: Compiled simulation of levelized logic is older; HSS of Barzilai, Carter, Rosen and Rutledge at IBM (1987) compiled the cycle-free parts of a design to machine code and simulated 16 or 32 patterns at once in a word.
prereqs: [logic-simulation, topological-sort, bit-parallelism]
see_also: [event-driven-logic-simulation, cycle-based-simulation, bitwise-operations, bit-slicing, parallel-fault-simulation, ppsfp, multi-valued-logic-simulation, boolean-circuit]
sources:
  - paper: doi:10.1109/TCAD.1987.1270308
    title: Zeev Barzilai, J. Lawrence Carter, Barry K. Rosen and Joseph D. Rutledge, HSS, a high-speed simulator, IEEE Transactions on Computer-Aided Design 6(4), 601 to 617, 1987
    locator: the compilation of the cycle-free parts of the netlist to machine instructions and the simulation of many patterns in parallel in one word
  - paper: "Gregory F. Pfister, The Yorktown Simulation Engine, introduction, Proceedings of the 19th Design Automation Conference, 51 to 54, 1982"
    title: G. F. Pfister, The Yorktown Simulation Engine, introduction, Proceedings of the 19th Design Automation Conference, 51 to 54, 1982
    locator: a special-purpose machine that runs a fixed compiled program of gate evaluations with no branches
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter Logic Simulation (compiled simulation, levelization and its limits)
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 4th edition, MIT Press, 2022
    locator: Section 20.4, Topological sort
---

Compiled-code logic simulation evaluates a combinational netlist by running a program made from it. The netlist is put in levelized order once, so that every gate comes after the gates that drive its inputs, and each gate becomes one statement of straight-line code with no tests and no loops. The delay model is zero delay: every gate is evaluated once per input vector, and only the settled values are computed. If each variable is a machine word and each statement uses the bitwise operations of the machine, bit $j$ of every word belongs to input vector $j$, and one run of the program simulates $W$ vectors. This page is in the logic simulation half of [logic and circuit simulation](/logic-simulation/), with the values 0 and 1. Compared with [event-driven simulation](/event-driven-logic-simulation/), it does more evaluations, since it evaluates every gate even when nothing changed, but each evaluation is one machine instruction with no queue and no branch.

## In plain words

Sort the gates so that each gate comes after the gates it reads. Then write one line of code per gate, in that order, such as `y = p | q`. Running these lines once gives every gate its value, because each line reads values that the lines above it have already set.

A computer word has 64 bits, and an AND of two words does 64 separate ANDs at once. So put the value of input $a$ for 64 different test vectors into the 64 bits of one word, and do the same for each input. One run of the code then gives the outputs for all 64 vectors.

The price is that the code says nothing about time. It gives the final values only, not glitches or delays.

## The problem

The input is a combinational netlist $C$ with $G$ gates, $N$ nets and $P$ gate input pins, and a list of $m$ input vectors in $\{0, 1\}^n$. The output is the value of every primary output for every vector. The gates must not form a loop. A sequential design is first cut at its registers, which is what [cycle-based simulation](/cycle-based-simulation/) does.

## The algorithm

```pseudo id=main
COMPILE(C, W)
L1  levelize C by Kahn's algorithm: level(input) = 0, level(out(g)) = 1 + the largest level of the inputs of g; stop with "loop" if some gate gets no level
L2  for each gate g in order of increasing level do
L3      emit the statement  word[out(g)] ← f_g(word of each input), with bitwise AND, OR and XOR, and XOR with the all-ones word for NOT
L4  translate the straight-line program to machine code

SIMULATE(program, vectors v_1, ..., v_m)
L5  for each block of W consecutive vectors do
L6      for each input i: word[i] ← the W bits of input i, bit j from vector j of the block
L7      run the program once
L8      for each output o and each j: the value of o in vector j is bit j of word[o]
```

Kahn's algorithm (see [topological sort](/topological-sort/)) keeps a queue of gates whose inputs are all levelized. It takes a gate, gives it its level and lowers the count of missing inputs of each gate in its fanout. Any order in which every gate follows its drivers would do; the order by level also groups gates that do not depend on each other, which helps when the code is spread over parallel units.

A NAND is an AND followed by XOR with the all-ones word $M = 2^W - 1$, so that only the $W$ lanes are inverted. Line L4 is the compile step. A production simulator emits C or machine code; the implementation of this page emits Python source and calls the Python compiler on it.

## Example

Take $y = ab + a'c$ with gates $\bar a = \mathrm{NOT}(a)$, $p = \mathrm{AND}(a, b)$, $q = \mathrm{AND}(\bar a, c)$ and $y = \mathrm{OR}(p, q)$, given in the netlist in the order $y, q, p, \bar a$. Kahn's algorithm gives $p$ and $\bar a$ level 1, $q$ level 2 and $y$ level 3. The implementation names the nets $a, b, c, y, p, q, \bar a$ as $v_0$ to $v_6$ and emits:

```text
def run(w):
    v0 = w[0]          # a
    v1 = w[1]          # b
    v2 = w[2]          # c
    v5 = v0 & v1       # p = a AND b
    v6 = v0 ^ M        # not a
    v4 = v6 & v2       # q = (not a) AND c
    v3 = v5 | v4       # y = p OR q
    return [v3]
```

With $W = 8$, put the eight vectors $abc = 000, 001, \ldots, 111$ into lanes $0$ to $7$, so bit $j$ of each word holds the bits of $j$:

| word | lane 7 to lane 0 |
| --- | --- |
| $a$ | 1 1 1 1 0 0 0 0 |
| $b$ | 1 1 0 0 1 1 0 0 |
| $c$ | 1 0 1 0 1 0 1 0 |
| $p = a \,\&\, b$ | 1 1 0 0 0 0 0 0 |
| $\bar a = a \oplus M$ | 0 0 0 0 1 1 1 1 |
| $q = \bar a \,\&\, c$ | 0 0 0 0 1 0 1 0 |
| $y = p \mid q$ | 1 1 0 0 1 0 1 0 |

So $y$ is the word `0b11001010`, which is the truth table of $ab + a'c$ read from lane 7 down to lane 0. One run of four instructions gave all eight vectors. The event-driven run on the [event-driven page](/event-driven-logic-simulation/) shows a glitch on $y$ when $a$ falls with $b = c = 1$; the compiled code cannot show it, since it has no time.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has two parts. Kahn's algorithm gives every gate a level exactly when the netlist has no loop, and then every gate comes after the drivers of its inputs. The bitwise operations act on each lane alone, so lane $j$ of the program is the program for vector $j$. Induction along the program shows that after the statement of gate $g$, lane $j$ of $\mathrm{word}[\mathrm{out}(g)]$ is the value of $\mathrm{out}(g)$ under vector $j$. The tests compare every output against a one-vector evaluation of the netlist, on all $2^n$ vectors of random circuits with up to 10 inputs and 60 gates, with the word widths 64, 7 and 1.

## Complexity

Levelization costs $O(N + P)$ for Kahn's algorithm plus the sort by level, which is $O(G \log G)$ in the implementation and $O(G)$ with a bucket per level. Emitting the code costs $O(G + P)$. Each run of the program costs one word operation per gate input pin, so $O(G + P)$, and there are $\lceil m / W \rceil$ runs. Packing and unpacking cost $O(m n)$ bit moves for the inputs and $O(m)$ per output. For an exhaustive check of a block with $n$ inputs, $m = 2^n$, and the run count is $2^n / W$.

Compared with event-driven simulation, the work per vector does not depend on how many nets change. When the activity is high, as with random vectors in fault simulation, compiled code is faster by a large factor. When only a few nets change per vector, event-driven simulation can do less work.

## Properties

- **Zero delay only.** The result is the settled value. Hazards, glitches and the order of changes are lost.
- **No branches.** The code has no data-dependent tests. This suits pipelined processors and was the base of hardware simulation engines such as IBM's Yorktown Simulation Engine.
- **Lanes are independent.** The $W$ vectors in a word never mix, so the lanes can hold different vectors, different faulty circuits, or both.
- **Exact.** On loop-free netlists the outputs equal the Boolean function of the circuit on each vector.

## Variants and improvements

- **Parallel fault simulation.** The lanes hold one good and $W - 1$ faulty circuits, each with a fault forced in its lane. See [parallel fault simulation](/parallel-fault-simulation/) and [PPSFP](/ppsfp/), which puts patterns in the lanes and handles one fault at a time.
- **Three values.** With X, each net needs two words, for example one with the lanes that can be 1 and one with the lanes that can be 0, and each gate becomes a few word operations. See [multi-valued logic simulation](/multi-valued-logic-simulation/).
- **Unit-delay compiled code.** Keeping one word per net per time step gives the unit-delay waveforms, at the cost of the depth of the circuit in extra statements.
- **Sequential designs.** Cut the loops at the registers and run the program once per clock: this is [cycle-based simulation](/cycle-based-simulation/).
- **Other parallelism.** [Bit slicing](/bit-slicing/) is the same idea in cryptography: a circuit in bitwise operations that processes $W$ blocks at once.

## When to use it

Use compiled code for functional simulation of synchronous logic where only the values at the clock edges matter, for exhaustive checks of small blocks, and for fault simulation with many patterns. Do not use it when the timing of signals inside a clock cycle matters, for asynchronous logic, or for circuits with combinational loops; an event-driven simulator with delays is the right tool there.

## Pitfalls

- **Combinational loops.** A netlist with a loop has no levelized order. Latches and loops that settle must be cut or simulated by events. The implementation reports such a netlist instead of emitting wrong code.
- **NOT without the mask.** In a language with unbounded integers, such as Python, `~x` gives a negative number. Use XOR with the all-ones word of width $W$.
- **The last block.** When $m$ is not a multiple of $W$, the unused lanes hold zeros. Unpack only the lanes in use.
- **Expecting glitches.** Zero-delay compiled code is blind to hazards. Use event-driven simulation with delays to see them.
- **Code size.** One statement per gate gives a large program for a large netlist. Compile time and instruction cache misses can then dominate, which is why some simulators keep the levelized netlist as a table and run a small interpreter over it.

## Implementations

## History

Compiled simulation, in which a netlist is translated into a program, was used for zero-delay functional checking from the early days of logic simulation. In the 1980s IBM built it into both hardware and software. The Yorktown Simulation Engine (Pfister, 1982) was a parallel machine that ran a fixed compiled list of gate evaluations with no branches. HSS (Barzilai, Carter, Rosen and Rutledge, 1987) compiled the cycle-free parts of a design into machine instructions, simulated 16 or 32 patterns in one word, and injected faults by changing instructions. The same bit-parallel idea is the base of parallel-pattern fault simulation and of cycle-based simulators.

## References
