---
tag: 3F0WFR
kind: concept
slug: reversible-computation
name: Reversible computation
aliases:
- reversible circuits
- reversible computing
- logically reversible computation
area: quantum/quantum-primitives
level: intro
summary: "Computation in which each step is a bijection, so the past state can be found from the present one. Quantum circuits run classical logic only in this form."
prereqs: [boolean-circuit, toffoli-gate]
see_also: [uncomputation, ancilla-qubits, quantum-oracle, cnot-gate, quantum-circuit-model, turing-machine, xor-swap, quantum-modular-exponentiation]
sources:
  - paper: doi:10.1147/rd.53.0183
    title: "Rolf Landauer, Irreversibility and heat generation in the computing process, IBM Journal of Research and Development 5(3):183-191, 1961"
    locator: the erasure of one bit dissipates at least kT ln 2 of heat
  - paper: doi:10.1147/rd.176.0525
    title: "Charles H. Bennett, Logical reversibility of computation, IBM Journal of Research and Development 17(6):525-532, 1973"
    locator: a reversible three-tape Turing machine that computes, copies the output and runs backward
  - paper: doi:10.1137/0218053
    title: "Charles H. Bennett, Time/space trade-offs for reversible computation, SIAM Journal on Computing 18(4):766-776, 1989"
    locator: the recursive checkpoint (pebble) strategy, time O(T^(1+e)) and space O(S log T)
  - paper: doi:10.1007/3-540-10003-2_104
    title: "Tommaso Toffoli, Reversible computing, ICALP 1980, Lecture Notes in Computer Science 85, Springer, 1980, pp. 632-644"
    locator: reversible gates, the Toffoli gate and the realization of any function with constant inputs and garbage outputs
  - paper: doi:10.1006/jcss.1999.1672
    title: "Klaus-Jörn Lange, Pierre McKenzie and Alain Tapp, Reversible space equals deterministic space, Journal of Computer and System Sciences 60(2):354-367, 2000"
    locator: a reversible machine simulates a deterministic one in the same space
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 3.2.5 (energy and computation, Landauer's principle, reversible gates, Bennett's construction) and Section 1.4.1 (classical computations on a quantum computer)"
  - book: isbn:9780198570004
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 1 (reversible computation and the Toffoli gate)
---

A computation is *reversible* when each of its steps is a bijection on the states of the machine, so the previous state can always be found from the current one. The AND gate is not reversible, but the [Toffoli gate](/toffoli-gate/), the [CNOT gate](/cnot-gate/) and NOT are, and with constant inputs they compute every Boolean function. Landauer (1961) showed that only irreversible steps must dissipate heat, and Bennett (1973) showed that every computation can be made reversible. A quantum computer needs this: its gates are [unitary](/unitary-operator/), so it runs classical logic only as reversible logic.

## In plain words

A normal computer forgets things all the time. When it adds two numbers and keeps only the sum, the two numbers are lost, because many pairs give the same sum. A reversible computer never forgets. Each step can be run backward to get exactly the state before it.

You can make any program reversible. Keep the input, and write each step into fresh scratch memory instead of over old values. At the end, copy the answer, then run all the steps backward. The scratch memory goes back to blank, and only the input and the answer stay. This costs about twice the steps, plus scratch memory.

Quantum computers need this, because the laws of quantum physics only allow steps that can be undone. Each classical part of a quantum algorithm is written as a reversible circuit.

## The idea

### Reversible gates

A $k$-bit gate is a map $g : \{0,1\}^k \to \{0,1\}^k$. It is *reversible* when $g$ is a bijection. So there are $(2^k)!$ reversible $k$-bit gates, for example $4! = 24$ on two bits and $8! = 40320$ on three. A circuit of reversible gates on $w$ wires computes a permutation of $\{0,1\}^w$. The standard gates are NOT, CNOT $(a, b) \mapsto (a, a \oplus b)$, the Toffoli gate $(a, b, c) \mapsto (a, b, c \oplus ab)$ and the Fredkin gate (a swap of $b$ and $c$ when $a = 1$). The CNOT and NOT gates alone compute only affine maps over $\mathrm{GF}(2)$, so they are not universal. The Toffoli gate is universal: with constant inputs it gives AND, NAND, NOT and FANOUT (see the [Toffoli gate](/toffoli-gate/) page).

### Why quantum circuits need it

A quantum circuit without measurement applies a unitary $U$. If $U$ maps each basis state $|z\rangle$ to a basis state, then $U$ is injective on the basis, so it permutes the basis: it is a reversible classical circuit. A function $f : \{0,1\}^n \to \{0,1\}^m$ that is not a bijection cannot be computed in place as $|x\rangle \mapsto |f(x)\rangle$. The standard way is to keep the input and add the value to an output register:

$$U_f : |x\rangle|y\rangle \mapsto |x\rangle|y \oplus f(x)\rangle, \qquad x \in \{0,1\}^n,\ y \in \{0,1\}^m.$$

This map is a bijection for every $f$, and it is its own inverse, because $y \oplus f(x) \oplus f(x) = y$. It is the bit form of a [quantum oracle](/quantum-oracle/).

### Landauer's principle

Landauer (1961) argued that a logically irreversible step, which merges two states into one, must increase the entropy of the surroundings. For the erasure of one bit at temperature $T$ the heat is at least $k_B T \ln 2$, where $k_B$ is the Boltzmann constant. At $T = 300$ K this is about $2.87 \times 10^{-21}$ joule. A logically reversible step merges no states, so this bound does not apply to it. This was the first reason to study reversible computing. Nielsen and Chuang, Section 3.2.5, give the argument and its history.

### From any circuit to a reversible circuit

Take a [Boolean circuit](/boolean-circuit/) with inputs $x_1, \ldots, x_n$ and $s$ gates. Give each gate its own fresh *work bit*, which starts at 0, and write the gate value into it:

- AND of $a, b$: one Toffoli gate with target the work bit.
- XOR of $a, b$: two CNOT gates.
- OR of $a, b$: $a \oplus b \oplus ab$, so two CNOT gates and one Toffoli gate.
- NOT of $a$: one CNOT gate and one NOT gate.

This *compute* circuit $C$ maps $(x, 0^s)$ to $(x, v(x))$, where $v(x)$ lists all gate values. The outputs are in $v(x)$, and the other values are *garbage*. Toffoli (1980) gave this form: constant inputs and garbage outputs.

### Bennett's construction

Bennett (1973) removed the garbage. Add $m$ fresh output bits. Run $C$, copy each output bit to an output wire with a CNOT, then run $C^{-1}$, which is the gates of $C$ in reverse order (each gate here is its own inverse):

$$(x, 0^s, 0^m) \xrightarrow{C} (x, v(x), 0^m) \xrightarrow{\text{copy}} (x, v(x), f(x)) \xrightarrow{C^{-1}} (x, 0^s, f(x)).$$

The last step is correct because $C^{-1}$ does not touch the output wires and undoes $C$ on the other wires. The cost is $2|C| + m$ gates on $n + s + m$ wires, and every work bit ends at 0, so it can be used again. Bennett proved this for Turing machines: a reversible machine with three tapes writes a history of its steps, copies the output, and then runs backward to erase the history. In the quantum setting the same step is called [uncomputation](/uncomputation/), and the work bits are [ancilla qubits](/ancilla-qubits/).

### Time and space

Bennett's 1973 machine needs space for the whole history, about the running time $T$. Bennett (1989) cut this with checkpoints. Split the run into $T$ segments, and think of a pebble on segment $i$ as a stored copy of the state after segment $i$. A pebble can be put on or taken off segment $i$ only when segment $i - 1$ holds a pebble, because the step from $i - 1$ to $i$ runs forward or backward from a stored state. To advance $2^k$ segments: advance $2^{k-1}$, advance $2^{k-1}$ more, then run the first half backward to remove its pebble. This takes $3^k = T^{\log_2 3} \approx T^{1.585}$ moves and holds at most $k + 1 = \log_2 T + 1$ pebbles. With $m$ parts per level instead of 2, it takes $(2m - 1)^k$ moves and $(m - 1)k + 1$ pebbles for $T = m^k$. The exponent $\log_m(2m - 1)$ is about 1.465 for $m = 3$ and 1.404 for $m = 4$, and it tends to 1. Bennett's theorem: a machine that runs in time $T$ and space $S$ has a reversible simulation in time $O(T^{1+\varepsilon})$ and space $O(S \log T)$, for each fixed $\varepsilon > 0$. Lange, McKenzie and Tapp (2000) showed that a reversible machine can also simulate a deterministic one in the same space $O(S)$, at the price of exponential time.

## Examples

**The AND gate is not reversible.** The inputs 00, 01 and 10 all give 0. Any reversible version must keep extra output bits, for example the Toffoli gate keeps $a$ and $b$.

**Bennett's construction for majority.** The majority of three bits is $\mathrm{maj}(x) = x_0x_1 \oplus x_0x_2 \oplus x_1x_2$. Wires 0 to 2 hold $x$, wires 3 to 7 are work bits, and wire 8 is the output. The compute part has 7 gates: Toffoli gates write $x_0x_1$, $x_0x_2$, $x_1x_2$ to wires 3, 4, 5. CNOT gates from 3 and 4 write their XOR to wire 6, and CNOT gates from 6 and 5 write $\mathrm{maj}(x)$ to wire 7. One CNOT copies wire 7 to wire 8, and the 7 gates run again in reverse. On $x_0 = 1, x_1 = 1, x_2 = 0$ the work wires 3 to 7 hold $1, 0, 0, 1, 1$ after the compute part, wire 8 gets 1, and after the reverse part wires 3 to 7 are all 0. The whole circuit has $2 \cdot 7 + 1 = 15$ gates on 9 wires, and on all 8 inputs it gives the majority with clean work bits.

**The pebble game for 4 segments.** With $k = 2$, Bennett's schedule toggles the segments 1, 2, 1, 3, 4, 3, 1, 2, 1. The pebbled sets are $\{1\}, \{1,2\}, \{2\}, \{2,3\}, \{2,3,4\}, \{2,4\}, \{1,2,4\}, \{1,4\}, \{4\}$. This is $3^2 = 9$ moves with at most 3 pebbles, and it ends with only the last state stored.

**A reversible program.** The [XOR swap](/xor-swap/) exchanges two words with three steps $x \mathrel{\oplus}= y$, $y \mathrel{\oplus}= x$, $x \mathrel{\oplus}= y$. Each step is a CNOT on each bit position, so the program is reversible and uses no scratch word.

**Embedding a function.** For $f : \{0,1\}^3 \to \{0,1\}^2$, the map $(x, y) \mapsto (x, y \oplus f(x))$ is a permutation of the 32 strings of 5 bits, and applying it twice gives the identity. This holds for each of the $4^8$ such functions, also for the ones that are far from injective.

## Where it is used

- **Quantum oracles.** Every classical function inside a quantum algorithm, such as the test of [Grover search](/grover-search/) or the function of [Simon's algorithm](/simon-algorithm/), is a reversible circuit in the form $U_f$, with its work qubits cleaned by [uncomputation](/uncomputation/).
- **Quantum arithmetic.** The modular exponentiation of [Shor's algorithm](/shor-algorithm/) is a reversible circuit of adders and multipliers made of Toffoli and CNOT gates; see [quantum modular exponentiation](/quantum-modular-exponentiation/). Its qubit count is set by the reversible space bound, not by the classical one.
- **Complexity theory.** Bennett's simulation shows that the class of problems solved by polynomial-size reversible circuits with clean ancillas equals the class for ordinary [Boolean circuits](/boolean-circuit/), with only a constant factor more gates. This is the first step of the proof that [BPP](/bpp/) is inside [BQP](/bqp/).
- **The thermodynamics of computation.** Landauer's bound applies only to steps that erase information. Bennett's construction shows that a computation can avoid such steps, so the bound does not limit the energy per logical step of a reversible machine.

## References
