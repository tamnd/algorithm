---
tag: W9842S
kind: algorithm
slug: deutsch-jozsa-algorithm
name: Deutsch-Jozsa algorithm
aliases:
- Deutsch's algorithm
area: quantum/quantum-primitives
level: intro
summary: Decides with one oracle query and no error whether a promised Boolean function is constant or balanced. A deterministic classical algorithm needs 2^(n-1) + 1 queries.
solves: [deutsch-jozsa-problem]
model: quantum-query-model
complexity:
  vars: {n: the number of input bits of f}
  queries: {worst: "1"}
  gates: {worst: 2n + 2}
  qubits: {worst: n + 1}
  time: {worst: Θ(n)}
properties: {exact: true, randomized: false, recursive: false}
history:
  year: 1992
  people: [David Deutsch, Richard Jozsa]
  note: Deutsch and Jozsa gave the problem for n bits in 1992, with two queries. Cleve, Ekert, Macchiavello and Mosca gave the one-query form in 1998.
prereqs: [deutsch-jozsa-problem, hadamard-gate, quantum-oracle, phase-kickback, quantum-interference]
see_also: [bernstein-vazirani-algorithm, simon-algorithm, fourier-sampling, walsh-hadamard-transform, quantum-parallelism, quantum-query-complexity]
sources:
  - paper: doi:10.1098/rspa.1992.0167
    title: "David Deutsch and Richard Jozsa, Rapid solution of problems by quantum computation, Proceedings of the Royal Society of London A 439(1907):553-558, 1992"
    locator: the original algorithm for n bits, with two evaluations of f
  - paper: doi:10.1098/rspa.1998.0164
    title: "Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca, Quantum algorithms revisited, Proceedings of the Royal Society of London A 454(1969):339-354, 1998"
    locator: the one-query form with the ancilla in the state |0> - |1>, for n = 1 and for n bits
  - paper: doi:10.1098/rspa.1985.0070
    title: "David Deutsch, Quantum theory, the Church-Turing principle and the universal quantum computer, Proceedings of the Royal Society of London A 400(1818):97-117, 1985"
    locator: the first quantum algorithm, for the case n = 1
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.4.3 (Deutsch's algorithm) and Section 1.4.4 (the Deutsch-Jozsa algorithm)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 6 (phase kickback, the Deutsch algorithm and the Deutsch-Jozsa algorithm)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 2 (the Deutsch-Jozsa algorithm in the circuit model)
---

The Deutsch-Jozsa algorithm solves the [Deutsch-Jozsa problem](/deutsch-jozsa-problem/): given an oracle for $f : \{0,1\}^n \to \{0,1\}$ that is promised to be constant or balanced, it decides which. It uses one query to the bit oracle, $n + 1$ qubits and $2n + 2$ one-qubit gates, and it is always right. A deterministic classical algorithm needs $2^{n-1} + 1$ queries. A randomized classical algorithm with bounded error needs only $2$, so the gap is against exact classical computation only. The algorithm is the simplest example of [Fourier sampling](/fourier-sampling/): it puts the input register in a uniform superposition, turns the values of $f$ into signs, and applies a Hadamard transform before it measures.

## In plain words

A box hides a rule that turns a string of bits into one bit. The rule gives the same bit for all strings, or it gives 0 for exactly half of them. A quantum computer can ask the box about all strings at once in one question. The box does not give back a list of answers. It marks each string with a plus sign or a minus sign, one for each answer.

Then the computer mixes all the marked strings together. If all the signs are the same, they add up, and the computer lands for certain on the string of all zeros. If half of the signs are plus and half are minus, they cancel there, and the computer never lands on all zeros. So one look at the result tells the two kinds apart, and the answer is never wrong.

## The problem

The input is an integer $n \ge 1$ and an oracle for $f : \{0,1\}^n \to \{0,1\}$, with the promise that $f$ is constant or balanced (it has exactly $2^{n-1}$ ones). The output is "constant" or "balanced". The oracle is the bit oracle $U_f |x\rangle |b\rangle = |x\rangle |b \oplus f(x)\rangle$ on $n + 1$ qubits. See the [Deutsch-Jozsa problem](/deutsch-jozsa-problem/) for the classical bounds.

We use the qubit order of [quantum state](/quantum-state/): qubit $j$ holds bit $x_j$ of $x = x_{n-1} \cdots x_0$, and qubit $0$ is the least significant bit. The input register is qubits $0$ to $n - 1$, and the ancilla is qubit $n$. We write $N = 2^n$, $x \cdot y = \sum_j x_j y_j \bmod 2$, $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$ and $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$.

## The algorithm

```pseudo id=main
DEUTSCH-JOZSA(U_f, n)                    ▷ U_f |x⟩|b⟩ = |x⟩|b ⊕ f(x)⟩
L1  prepare |0...0⟩ on qubits 0 .. n-1 and |1⟩ on qubit n
L2  apply H to each of the n + 1 qubits
L3  apply U_f once                       ▷ the only query
L4  apply H to each of qubits 0 .. n-1
L5  measure qubits 0 .. n-1 and let y be the outcome
L6  if y = 0 then return "constant" else return "balanced"
```

Line L1 uses one $X$ gate on the ancilla. After line L2 the input register is in the uniform superposition $N^{-1/2} \sum_x |x\rangle$, and the ancilla is in $|-\rangle$. On $|x\rangle|-\rangle$ the query of line L3 gives $(-1)^{f(x)} |x\rangle|-\rangle$, by [phase kickback](/phase-kickback/). So the ancilla does not change, and each $|x\rangle$ gets the sign $(-1)^{f(x)}$. Line L4 applies the Hadamard transform $H^{\otimes n}$, which maps $|x\rangle$ to $N^{-1/2} \sum_y (-1)^{x \cdot y} |y\rangle$. The amplitude of $|y\rangle$ is then

$$a_y = \frac{1}{N} \sum_{x \in \{0,1\}^n} (-1)^{f(x) + x \cdot y},$$

the Walsh-Hadamard coefficient of $(-1)^f$ at $y$ (see [Walsh-Hadamard transform](/walsh-hadamard-transform/)). In particular $a_0 = (N - 2|f|)/N$, where $|f|$ is the number of ones of $f$. This is $\pm 1$ for a constant $f$ and $0$ for a balanced $f$, so line L6 is always right.

The ancilla is left in $|-\rangle$ and is not entangled with the input register. One $H$ and one $X$ return it to $|0\rangle$, so it can be reused.

## Example

Take $n = 2$ and the balanced function $f(x) = x_0 \oplus x_1$, with $f(00) = 0$, $f(01) = 1$, $f(10) = 1$ and $f(11) = 0$. The kets below show qubit $1$ on the left and qubit $0$ on the right, and the ancilla is not shown after line L2.

| after | state of qubits 1 and 0 |
|---|---|
| L1 | $\lvert 00 \rangle$, ancilla $\lvert 1 \rangle$ |
| L2 | $\tfrac{1}{2}(\lvert 00 \rangle + \lvert 01 \rangle + \lvert 10 \rangle + \lvert 11 \rangle)$, ancilla $\lvert - \rangle$ |
| L3 | $\tfrac{1}{2}(\lvert 00 \rangle - \lvert 01 \rangle - \lvert 10 \rangle + \lvert 11 \rangle) = \lvert - \rangle \lvert - \rangle$ |
| L4 | $\lvert 11 \rangle$ |

Line L5 gives $y = 11$ with probability $1$, and line L6 returns "balanced". For the balanced $f(x) = x_1$ (truth table $0011$), the state after line L3 is $\lvert - \rangle \lvert + \rangle$, and $y = 10$ with probability $1$. For the constant $f = 1$, the state after line L3 is $-\tfrac{1}{2} \sum_x \lvert x \rangle$, and line L4 gives $-\lvert 00 \rangle$. The sign is a global phase, so $y = 00$ with probability $1$ and the answer is "constant".

A balanced function need not give one $y$ with certainty. For $n = 3$ and $f(x) = x_2 \oplus x_0 x_1$, with truth table $0, 0, 0, 1, 1, 1, 1, 0$ for $x = 0, \ldots, 7$, the outcome $y$ is $100$, $101$, $110$ or $111$, each with probability $1/4$. All four are nonzero, so the answer is still "balanced". These numbers come from the exact distribution of the simulator in the implementation.

## Correctness

The output distribution is $\Pr[y] = a_y^2$ with $a_y$ as above, because the ancilla stays in the product state $|-\rangle$. The full proof is below. It has three steps: $H^{\otimes n} |0\rangle = N^{-1/2} \sum_x |x\rangle$ and $H^{\otimes n} |x\rangle = N^{-1/2} \sum_y (-1)^{x \cdot y} |y\rangle$ by the [tensor product](/tensor-product/) of the one-qubit maps; the query on $|x\rangle|-\rangle$ gives $(-1)^{f(x)} |x\rangle|-\rangle$; and $a_0 = (N - 2|f|)/N$. So $\Pr[y = 0] = 1$ for a constant $f$ and $\Pr[y = 0] = 0$ for a balanced $f$.

## Complexity

- **Queries.** One query to $U_f$, on all $n + 1$ qubits at once. This is optimal: with zero queries the output does not depend on $f$.
- **Gates.** One $X$ gate and $2n + 1$ Hadamard gates, so $2n + 2$ one-qubit gates. All are exact Clifford gates. The depth is $3$ apart from the oracle: the $X$ gate, one layer of $H$ before the query and one layer of $H$ after it.
- **Qubits.** $n$ data qubits and one ancilla, which is returned clean as $|-\rangle$.
- **Classical work.** The test $y = 0$ takes $O(n)$ time.

Against classical algorithms, in the query model: a deterministic algorithm needs $2^{n-1} + 1$ queries, a zero-error randomized algorithm needs $2^{n-1} + 1$ queries on each constant input, and a bounded-error randomized algorithm needs $2$. The [Deutsch-Jozsa problem](/deutsch-jozsa-problem/) has the proofs.

## Properties

- **Exact.** The answer is right with probability $1$ on every input that obeys the promise. The measurement is random, but the answer does not depend on its outcome.
- **One non-adaptive query.** There is nothing to adapt: the query is the first and only one.
- **The output is the Fourier spectrum.** The outcome $y$ has probability $a_y^2$, the square of the Walsh-Hadamard coefficient of $(-1)^f$ at $y$. The algorithm decides only whether $a_0^2$ is $1$ or $0$. The same circuit, with a different promise, is the [Bernstein-Vazirani algorithm](/bernstein-vazirani-algorithm/).
- **Outside the promise.** For any $f$, $\Pr[y = 0] = (1 - 2w)^2$, where $w = |f|/N$ is the fraction of ones. For $n = 3$ and $f$ with one $1$, $\Pr[y = 0] = (6/8)^2 = 0.5625$. So the answer has no meaning when the promise fails.

## Variants and improvements

- **The case $n = 1$.** For one input bit the algorithm uses two qubits and decides whether $f(0) = f(1)$. The circuit is $H \otimes H$ on $|0\rangle|1\rangle$, one query and $H$ on qubit $0$, and the measured bit is exactly $f(0) \oplus f(1)$. A classical algorithm needs both values. Deutsch gave the first quantum algorithm for this case in 1985. His version gave a definite answer only with probability $1/2$. The exact form with one query is from Cleve, Ekert, Macchiavello and Mosca (1998).
- **The phase oracle.** With the phase oracle $O_f |x\rangle = (-1)^{f(x)} |x\rangle$, drop the ancilla and lines L1 and L2 on it. The circuit is $H^{\otimes n}$, one query and $H^{\otimes n}$, on $n$ qubits with $2n$ Hadamard gates.
- **The two-query original.** Deutsch and Jozsa (1992) used two evaluations of $f$, with an output register that starts in $|0\rangle$ and a second evaluation to clear it. The ancilla in $|-\rangle$ removes the second query.
- **Affine functions.** If $f(x) = s \cdot x \oplus c$, the outcome is $y = s$ with certainty. This is the [Bernstein-Vazirani algorithm](/bernstein-vazirani-algorithm/).
- **Repetition under noise.** On a device with noise, run the circuit a few times and take the majority answer; each run is independent, so $k$ runs with error $\eta < 1/2$ each give error $e^{-\Omega(k)}$ by the [Chernoff bound](/chernoff-bound/).

## When to use it

Use the algorithm as the first example of interference in a quantum algorithm, and as a small test of a quantum device or simulator, because the right output is known exactly. It is not a useful speedup in practice. A classical program that may be wrong with a small chance needs only two queries, and real oracles have noise, so an exact answer cannot be had on hardware anyway. When a gap against randomized algorithms matters, use [Simon's algorithm](/simon-algorithm/) as the example.

## Pitfalls

- **The ancilla in $|0\rangle$.** Without the $X$ gate of line L1, the ancilla starts in $|0\rangle$, the query writes $f(x)$ into it, and the input register becomes entangled with it. Then a balanced $f$ gives $y = 0$ with probability $1/2$, and the test fails half the time.
- **Garbage in the oracle.** The oracle must be exactly $U_f$. If a circuit for $f$ leaves work qubits that depend on $x$, they destroy the interference in the same way. Clear them by [uncomputation](/uncomputation/).
- **Claiming an exponential speedup.** The gap is only against deterministic and zero-error classical algorithms. Against a bounded-error randomized algorithm the gap is $1$ query against $2$.
- **Reading $y$ as data.** For a balanced $f$, the value of $y$ tells which Fourier coefficients are nonzero, not which strings have $f(x) = 1$. Only the test $y = 0$ has a meaning here.
- **Bit order of $y$.** The test $y = 0$ does not depend on the order of the bits. If you use the full value of $y$, as in the Bernstein-Vazirani algorithm, read qubit $j$ as bit $y_j$.

## Implementations

## History

David Deutsch described the first quantum algorithm in 1985, for the case of one input bit, in the paper that defined the universal quantum computer. In 1992 Deutsch and Richard Jozsa extended the problem to $n$ bits and gave an algorithm with two evaluations of $f$ that is always right, against $2^{n-1} + 1$ queries for a deterministic classical machine. In 1998 Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca put the ancilla in the state $(|0\rangle - |1\rangle)/\sqrt{2}$ and got the form with one query that is used today. They also showed that it is an instance of the pattern of phase estimation. The algorithm keeps the names of Deutsch and Jozsa. In 1993 Bernstein and Vazirani and in 1994 Simon used the same oracle model for problems with a larger gap.

## References
