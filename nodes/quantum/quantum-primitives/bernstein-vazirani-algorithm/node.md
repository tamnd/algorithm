---
tag: 93HVEH
kind: algorithm
slug: bernstein-vazirani-algorithm
name: Bernstein-Vazirani algorithm
area: quantum/quantum-primitives
level: intro
summary: Recovers the hidden string s of f(x) = s . x mod 2 with one oracle query and no error. Every classical algorithm, even with randomness and bounded error, needs n queries.
solves: [bernstein-vazirani-problem]
model: quantum-query-model
complexity:
  vars: {n: the length of the hidden string s}
  queries: {worst: "1"}
  gates: {worst: 2n + 2}
  qubits: {worst: n + 1}
  time: {worst: Θ(n)}
properties: {exact: true, randomized: false, recursive: false}
history:
  year: 1993
  people: [Ethan Bernstein, Umesh Vazirani]
  note: Bernstein and Vazirani gave the problem and the one-query solution at STOC 1993, with a recursive form for a superpolynomial separation. The journal version appeared in 1997.
prereqs: [bernstein-vazirani-problem, deutsch-jozsa-algorithm, hadamard-gate, phase-kickback]
see_also: [fourier-sampling, simon-algorithm, walsh-hadamard-transform, hadamard-code, quantum-interference, quantum-query-complexity]
sources:
  - paper: doi:10.1145/167088.167097
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, Proceedings of the 25th Annual ACM Symposium on Theory of Computing (STOC 1993), pages 11-20, 1993"
    locator: the conference version; the Fourier sampling of the function x -> s . x
  - paper: doi:10.1137/S0097539796300921
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, SIAM Journal on Computing 26(5):1411-1473, 1997"
    locator: the journal version, which this page follows; the recursive Fourier sampling problem (section number not checked)
  - paper: doi:10.1098/rspa.1998.0164
    title: "Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca, Quantum algorithms revisited, Proceedings of the Royal Society of London A 454(1969):339-354, 1998"
    locator: the ancilla in the state |0> - |1> that turns the bit oracle into a phase oracle
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 2 (the Bernstein-Vazirani algorithm)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.4.4 (the Deutsch-Jozsa circuit and the Hadamard transform identity it uses)
---

The Bernstein-Vazirani algorithm solves the [Bernstein-Vazirani problem](/bernstein-vazirani-problem/): given an oracle for $f(x) = s \cdot x \bmod 2$ with a hidden $s \in \{0,1\}^n$, it returns $s$. It uses one query to the bit oracle, $n + 1$ qubits and $2n + 2$ one-qubit gates, and it is always right. Every classical algorithm needs $n$ queries, even with randomness and bounded error. The circuit is the circuit of the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/); only the promise and the reading of the outcome change. It is the cleanest example of [Fourier sampling](/fourier-sampling/), because the Fourier spectrum of $(-1)^{f}$ is the single point $s$.

## In plain words

A box hides a secret string of bits. You give it a string, and it says whether the two strings share an odd or an even number of places with a 1. A classical program learns one bit of the secret with each question.

The quantum program asks once, about all strings at the same time. The box answers by giving each string a plus sign or a minus sign. This pattern of signs is a wave, and each secret makes a different wave. The program then applies a step that turns each such wave back into the one string that made it. So when it looks at the result, it reads the secret directly, with no chance of a wrong answer.

## The problem

The input is $n \ge 1$ and a bit oracle $U_f |x\rangle |b\rangle = |x\rangle |b \oplus f(x)\rangle$ on $n + 1$ qubits, with the promise that $f(x) = s \cdot x$ for some $s$, where $s \cdot x = \sum_j s_j x_j \bmod 2$. The output is $s$. The algorithm also works when $f(x) = s \cdot x \oplus c$.

We use the qubit order of [quantum state](/quantum-state/): qubit $j$ holds bit $j$ of $x = x_{n-1} \cdots x_0$, and qubit $0$ is the least significant bit. The input register is qubits $0$ to $n - 1$ and the ancilla is qubit $n$. The outcome $y$ has bit $y_j$ from qubit $j$. We write $N = 2^n$.

## The algorithm

```pseudo id=main
BERNSTEIN-VAZIRANI(U_f, n)               ▷ U_f |x⟩|b⟩ = |x⟩|b ⊕ f(x)⟩
L1  prepare |0...0⟩ on qubits 0 .. n-1 and |1⟩ on qubit n
L2  apply H to each of the n + 1 qubits
L3  apply U_f once                       ▷ the only query
L4  apply H to each of qubits 0 .. n-1
L5  measure qubits 0 .. n-1 and return the outcome y as s
```

After line L2 the input register is $N^{-1/2} \sum_x |x\rangle$ and the ancilla is $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$. By [phase kickback](/phase-kickback/), line L3 gives
$$\frac{1}{\sqrt{N}} \sum_x (-1)^{s \cdot x} |x\rangle \otimes |-\rangle = H^{\otimes n} |s\rangle \otimes |-\rangle .$$
The equation on the right is the Hadamard transform identity $H^{\otimes n} |s\rangle = N^{-1/2} \sum_x (-1)^{s \cdot x} |x\rangle$, which is a product of one-qubit identities: the state is $\bigotimes_j H|s_j\rangle$, with $|+\rangle$ where $s_j = 0$ and $|-\rangle$ where $s_j = 1$. Since $H^2 = I$, line L4 gives exactly $|s\rangle \otimes |-\rangle$, and line L5 reads $s$.

With $f(x) = s \cdot x \oplus c$, every sign has the extra factor $(-1)^c$. That is a global phase, so the outcome is still $s$.

## Example

Take $n = 3$ and $s = 101$, so $f(x) = x_0 \oplus x_2$. The kets show qubit $2$ on the left and qubit $0$ on the right.

| after | state of qubits 2, 1 and 0 |
|---|---|
| L1 | $\lvert 000 \rangle$, ancilla $\lvert 1 \rangle$ |
| L2 | $\tfrac{1}{\sqrt{8}} \sum_x \lvert x \rangle$, ancilla $\lvert - \rangle$ |
| L3 | $\tfrac{1}{\sqrt{8}} (\lvert 000 \rangle - \lvert 001 \rangle + \lvert 010 \rangle - \lvert 011 \rangle - \lvert 100 \rangle + \lvert 101 \rangle - \lvert 110 \rangle + \lvert 111 \rangle) = \lvert - \rangle \lvert + \rangle \lvert - \rangle$ |
| L4 | $\lvert 101 \rangle$ |

The sign of $|x\rangle$ after line L3 is $(-1)^{x_0 \oplus x_2}$: it is minus when exactly one of $x_0$ and $x_2$ is $1$. Each qubit is now $|+\rangle$ or $|-\rangle$ on its own, and $H$ maps them to $|0\rangle$ and $|1\rangle$. So line L5 returns $y = 101 = s$ with probability $1$. A classical algorithm asks $f(001) = 1$, $f(010) = 0$ and $f(100) = 1$, three queries for the same answer.

The exact distribution from the simulator in the implementation gives $\Pr[y = s] = 1$ for all $s$ with $n \le 6$, with and without the constant $c$.

## Correctness

The final state is $|s\rangle \otimes |-\rangle$ up to the global phase $(-1)^c$, so the measurement of the input register returns $s$ with probability $1$. The proof below shows this from the general amplitude formula $a_y = N^{-1} \sum_x (-1)^{f(x) + x \cdot y}$, which is the same as for the Deutsch-Jozsa circuit, and the orthogonality of the characters: $\sum_x (-1)^{(s \oplus y) \cdot x} = N$ if $y = s$ and $0$ otherwise.

## Complexity

- **Queries.** One query to $U_f$. This is optimal, since zero queries cannot find $s$.
- **Gates.** One $X$ gate and $2n + 1$ Hadamard gates, so $2n + 2$ exact Clifford gates. The depth is $3$ apart from the oracle.
- **Qubits.** $n$ data qubits and one ancilla, returned clean in the state $|-\rangle$. With the phase oracle $O_f |x\rangle = (-1)^{f(x)} |x\rangle$ there is no ancilla, and the circuit has $2n$ Hadamard gates.
- **Classical work.** None beyond reading $y$.

In the query model, every classical algorithm needs $n$ queries, and with $q < n$ queries it succeeds with probability at most $2^{q-n}$ on a uniform $s$. The [Bernstein-Vazirani problem](/bernstein-vazirani-problem/) has the proof. So the gap is $1$ against $n$, against randomized algorithms too. The cost of the oracle itself is not counted: a circuit for $s \cdot x$ needs one CNOT for each $j$ with $s_j = 1$.

## Properties

- **Exact.** The output is $s$ with probability $1$ on every input that obeys the promise.
- **Non-adaptive.** One query, with no classical post-processing.
- **No entanglement in the main state.** After each line the input register is a product state of its qubits, and the ancilla is apart from it. The gain comes from interference of the signs, not from entanglement between the qubits of the input register.
- **Samples the spectrum.** For any $f$, outside the promise too, the outcome $y$ has probability $\hat{F}(y)^2$, the square of the Walsh-Hadamard coefficient of $(-1)^f$ at $y$. For the linear $f$ the spectrum is the point $s$.

## Variants and improvements

- **The phase oracle.** With $O_f$, the circuit is $H^{\otimes n}$, $O_f$, $H^{\otimes n}$ on $n$ qubits.
- **Other moduli.** For $f(x) = s \cdot x \bmod d$ on $\mathbb{Z}_d^n$, use the quantum Fourier transform over $\mathbb{Z}_d$ on each register in place of $H$. One query to the phase oracle $|x\rangle \mapsto e^{2 \pi i f(x)/d} |x\rangle$ then gives $s$ with certainty. See the [quantum Fourier transform](/quantum-fourier-transform/).
- **Recursive Fourier sampling.** Bernstein and Vazirani nested instances in a tree of height $h$, where the hidden string of each instance decides a bit of the instance one level up. The quantum algorithm runs this algorithm at each level and clears the work registers by [uncomputation](/uncomputation/), for about $2^h$ queries. The classical cost grows like $n^{\Omega(h)}$. This gave a superpolynomial oracle separation of bounded-error quantum and classical computation.
- **Noisy oracles.** If the oracle has noise, repeat the circuit and take the majority of each bit of $y$. With $k$ runs, each bit is right with probability $1 - e^{-\Omega(k)}$ when each run is right with probability more than $1/2$; see [error amplification](/error-amplification/).

## When to use it

Use the algorithm as the first example of a quantum query algorithm with a gap against randomized classical algorithms, and as the clearest case of [Fourier sampling](/fourier-sampling/). It is also a standard benchmark of quantum hardware, because the right output is known and the circuit has no rotations. It is not a practical speedup: building the oracle for $s \cdot x$ requires knowing $s$, and with $s$ unknown a classical program reads the $n$ bits with $n$ queries, which is cheap.

## Pitfalls

- **Bit order.** The outcome lists qubit $0$ as the least significant bit. A program that prints qubit $0$ on the left, as some tools and books do, shows $s$ reversed. For $s = 110$ in the order of this page, the reversed print is $011$.
- **The ancilla in $|0\rangle$.** Without the $X$ gate of line L1, the query entangles the input register with the ancilla, and the output is uniformly random over two values of $y$ for $s \ne 0$: $y = 0$ or $y = s$, each with probability $1/2$.
- **A function outside the promise.** If $f$ is not of the form $s \cdot x \oplus c$, the outcome is a sample of the Walsh-Hadamard spectrum. For example, $f(x) = x_0 x_1$ on two bits gives each $y$ with probability $1/4$. The algorithm does not detect this. Check the answer with classical queries if the promise is in doubt.
- **Expecting $n$ bits for free.** One query gives $n$ bits only because the oracle is linear. For a general $f$, one query cannot reveal $n$ bits of information about it.

## Implementations

## History

Ethan Bernstein and Umesh Vazirani studied the problem in their paper on quantum complexity theory at STOC 1993, which also gave an efficient universal quantum Turing machine. They nested the problem in a recursive problem, now called recursive Fourier sampling, to get the first superpolynomial separation between quantum and classical bounded-error computation relative to an oracle. The journal version appeared in SIAM Journal on Computing in 1997, in the same issue as Simon's paper. The form with the ancilla in $(|0\rangle - |1\rangle)/\sqrt{2}$ and one query is the one of Cleve, Ekert, Macchiavello and Mosca (1998).

## References
