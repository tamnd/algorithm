---
tag: K6XYGK
kind: algorithm
slug: quantum-gcd
name: Quantum GCD circuits
aliases:
- quantum binary GCD
- reversible Euclidean algorithm
area: quantum/quantum-number-theory
level: advanced
summary: Reversible circuits that compute gcd(u, v) on a superposition of inputs. They run the binary GCD for a fixed number of rounds and erase the history. Used in quantum modular inversion.
model: quantum-circuit-model
complexity:
  vars: {n: "the number of bits of each input"}
  time: {toffoli_gates: 52n^2 - 22n - 2, depth: O(n^2)}
  space: {data_qubits: 3n, ancilla_qubits: 5n}
properties: {deterministic: true, exact: true, quantum: true, reversible: true, data_oblivious: true}
history:
  year: 2003
  people: [John Proos, Christof Zalka]
  note: Proos and Zalka gave a reversible Euclidean algorithm for the elliptic-curve discrete logarithm and named the problem of input-dependent stopping. Roetteler, Naehrig, Svore and Lauter (2017) used a fixed number of binary GCD rounds.
prereqs: [binary-gcd, greatest-common-divisor, ripple-carry-adder, toffoli-gate, reversible-computation, uncomputation, ancilla-qubits]
see_also: [quantum-modular-inversion, quantum-elliptic-curve-discrete-log, quantum-modular-exponentiation, euclidean-algorithm, extended-euclidean-algorithm, half-gcd, quantum-oracle, quantum-resource-estimation-factoring]
sources:
  - paper: arxiv:quant-ph/0301141
    title: "John Proos and Christof Zalka, Shor's discrete logarithm quantum algorithm for elliptic curves, Quantum Information and Computation 3(4):317-344, 2003"
    locator: the reversible Euclidean algorithm for modular inverses and the quantum halting problem
  - paper: arxiv:1706.06752
    title: "Martin Roetteler, Michael Naehrig, Krysta M. Svore and Kristin Lauter, Quantum resource estimates for computing elliptic curve discrete logarithms, ASIACRYPT 2017"
    locator: Section 3.4 (the binary extended Euclidean algorithm run for 2n rounds with a counter) and Table 1
  - paper: arxiv:2001.09580
    title: "Thomas Häner, Samuel Jaques, Michael Naehrig, Martin Roetteler and Mathias Soeken, Improved quantum circuits for elliptic curve discrete logarithms, PQCrypto 2020"
    locator: the reformulated binary Euclidean algorithm with fewer gates and lower depth
  - paper: "Josef Stein, Computational problems associated with Racah algebra, Journal of Computational Physics 1(3):397-405, 1967"
    title: Josef Stein, Computational problems associated with Racah algebra
    locator: the binary GCD algorithm
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.5.2 (the binary GCD algorithm and its analysis)
  - paper: doi:10.1137/0218053
    title: "Charles H. Bennett, Time/space trade-offs for reversible computation, SIAM Journal on Computing 18(4):766-776, 1989"
    locator: computing, copying the output and uncomputing to clear the history
  - paper: "Daniel J. Bernstein and Bo-Yin Yang, Fast constant-time gcd computation and modular inversion, IACR Transactions on Cryptographic Hardware and Embedded Systems 2019(3):340-398, 2019"
    title: Daniel J. Bernstein and Bo-Yin Yang, Fast constant-time gcd computation and modular inversion
    locator: the division steps with a fixed number of iterations
  - paper: arxiv:quant-ph/0410184
    title: Steven A. Cuccaro, Thomas G. Draper, Samuel A. Kutin and David Petrie Moulton, A new quantum ripple-carry addition circuit, 2004
    locator: the adder used for the subtraction and the comparison
---

A quantum GCD circuit is a reversible circuit that maps $|u\rangle|v\rangle|0\rangle$ to $|u\rangle|v\rangle|\gcd(u, v)\rangle$, so it computes the [greatest common divisor](/greatest-common-divisor/) of every input in a superposition at once. The circuit on this page runs the [binary GCD](/binary-gcd/) for a fixed number $2n - 1$ of rounds, keeps two history bits per round, copies the result and then runs the rounds backward. The fixed number of rounds solves the problem that the classical algorithm stops after a number of steps that depends on the input. Its main use is the extended form for [quantum modular inversion](/quantum-modular-inversion/) in the [quantum elliptic-curve discrete logarithm](/quantum-elliptic-curve-discrete-log/).

## In plain words

The binary GCD repeats one simple step: if the second number is odd, make sure it is the larger one and subtract the first; then halve it. When the second number reaches zero, the first one is the answer. On a quantum computer the inputs can be many numbers at once, and each one would stop at a different time. So the circuit always does the largest number of steps that any input can need. Extra steps do nothing once the second number is zero.

Each step forgets something: after a subtraction you cannot tell whether a swap happened. So each step writes down two small notes. At the end the answer is copied, and all the steps are undone in reverse order, which also erases the notes.

## The problem

Given $n$ and quantum registers holding an odd integer $u$ with $0 < u < 2^n$ and an integer $v$ with $0 \le v < 2^n$, build a circuit of NOT, CNOT and Toffoli gates with

$$U\,|u\rangle|v\rangle|0\rangle|0\rangle = |u\rangle|v\rangle|\gcd(u, v)\rangle|0\rangle,$$

where the last register holds all [ancillas](/ancilla-qubits/). The gate sequence must not depend on $u$ and $v$, since they are in superposition. In the main application $u$ is an odd prime modulus $p$, so the condition that $u$ is odd costs nothing.

## The algorithm

The registers are $u$, $v$ and the output $g$ ($n$ qubits each), a register $\mathit{tmp}$ of $n$ qubits, a comparison qubit $d$, the carry qubit of the [ripple-carry adder](/ripple-carry-adder/), and history qubits $e_i$ and $h_i$ for each round $i$.

```pseudo id=main
QGCD(u, v; g)                        ▷ u odd; g, tmp, d and the history are 0
L1  for i ← 1 to 2n - 1 do
L2      e_i ← e_i ⊕ v_0                  ▷ e_i = 1 when v is odd
L3      d ← [v < u]; h_i ← h_i ⊕ (e_i ∧ d); d ← d ⊕ [v < u]
L4      if h_i = 1 then swap u and v
L5      if e_i = 1 then v ← v - u        ▷ now v is even and v ≥ 0
L6      v ← v / 2                        ▷ relabel the wires of v; no gates
L7  g ← g ⊕ u                            ▷ n CNOT gates
L8  run lines L1 to L6 backward          ▷ restores u and v and clears every e_i and h_i
```

Line L3 computes the comparison with the adder run backward, which sets $d$ to the borrow of $v - u$, and then clears $d$ the same way. Line L5 copies $u$ into $\mathit{tmp}$ with Toffoli gates controlled by $e_i$, subtracts $\mathit{tmp}$ from $v$ and copies again to clear $\mathit{tmp}$. In line L6 the low bit of $v$ is 0, so moving each wire down by one place and the low wire to the top divides by 2. Lines L7 and L8 are Bennett's compute, copy and uncompute pattern; see [uncomputation](/uncomputation/).

## Example

Take $n = 4$, $u = 9$ and $v = 6$, so there are 7 rounds.

| round | v odd ($e_i$) | swap ($h_i$) | u after | v after |
|---|---|---|---|---|
| 1 | 0 | 0 | 9 | 3 |
| 2 | 1 | 1 | 3 | 3 |
| 3 | 1 | 0 | 3 | 0 |
| 4 to 7 | 0 | 0 | 3 | 0 |

In round 2, $v = 3 < 9$, so the registers swap to $u = 3$, $v = 9$, then $v$ becomes $9 - 3 = 6$ and is halved to 3. Round 3 gives $3 - 3 = 0$. Line L7 copies $u = 3 = \gcd(9, 6)$ into $g$, and line L8 runs the 7 rounds backward to $u = 9$, $v = 6$ with all history bits 0. Rounds 4 to 7 do nothing on this input, but other inputs need all 7: for example $u = 9$ and $v = 8$ reach $v = 0$ only in round 7.

## Correctness

Each round keeps three facts: $u$ is odd, $0 \le v < 2^n$, and $\gcd(u, v)$ is unchanged. The swap and the subtraction keep the GCD, and halving an even $v$ keeps it because $u$ is odd. When $v = 0$, a round sets $e_i = h_i = 0$ and changes nothing, and then $u = \gcd(u, 0)$ is the answer. A round with $v > 0$ lowers the total bit length of $u$ and $v$ by at least one, and that total starts at most at $2n$ and stays at least 1, so $2n - 1$ rounds reach $v = 0$ for every input. The backward run of line L8 inverts lines L1 to L6 exactly and does not touch $g$, so all ancillas return to 0. The full proof is in the proofs file.

## Complexity

In the gate set NOT, CNOT and Toffoli, with the adder of Cuccaro, Draper, Kutin and Moulton on $n$ bits ($2n$ Toffolis), one round costs $8n + 1$ Toffolis for line L3, $n$ for the swap and $4n$ for the controlled subtraction, that is $13n + 1$. The forward and backward runs give exactly

$$2(2n - 1)(13n + 1) = 52 n^2 - 22 n - 2$$

Toffoli gates, for example 742 for $n = 4$ and 3150 for $n = 8$ in the reference implementation. The depth is $O(n^2)$, because each round is a chain of ripple adders. The circuit uses $3n$ data qubits ($u$, $v$, $g$) and $5n$ ancillas: $n$ for $\mathit{tmp}$, 2 for $d$ and the carry, and $2(2n - 1)$ history qubits. All counts are logical; error correction adds its own overhead, as in [quantum resource estimation for factoring](/quantum-resource-estimation-factoring/).

## Properties

- **Data oblivious.** The gate sequence is the same for every input, which is required for superpositions and is also the property that constant-time classical code needs.
- **Exact.** The output is exact on every basis state with $u$ odd.
- **Clean.** All history is erased, so the output is not entangled with garbage.
- **Linear history.** Only two history bits per round are kept, which is $O(n)$ in total, because each round is reversible once its two decisions are known.

## Variants and improvements

- **Extended GCD.** Adding two coefficient registers that follow the same swaps and subtractions gives the inverse of $v$ modulo an odd $u$; this is [quantum modular inversion](/quantum-modular-inversion/). Roetteler, Naehrig, Svore and Lauter implement Kaliski's Montgomery inverse this way with $2n$ rounds, a counter of $O(\log n)$ qubits for the rounds after $v = 0$, and one history qubit per round, using the parity of the coefficients to recover the other branch bit.
- **Euclid with quotients.** Proos and Zalka run the classical [Euclidean algorithm](/euclidean-algorithm/) with quotients of variable length and share space between registers. They pointed out the "quantum halting problem": different inputs stop at different steps, so a fixed schedule is needed.
- **Fewer gates and lower depth.** Häner, Jaques, Naehrig, Roetteler and Soeken reformulate the binary Euclidean algorithm to cut the T count and depth.
- **Division steps.** The constant-time GCD of Bernstein and Yang uses a fixed number of simple division steps and is a natural template for reversible circuits. Fast recursive methods such as [half-GCD](/half-gcd/) lower the classical cost to $O(M(n) \log n)$, but their reversible forms need more space.
- **Even inputs.** For an even $u$, first strip the common factors of 2 with a fixed number of controlled shifts, as in the classical binary GCD.

## When to use it

Use it when a quantum algorithm needs a GCD or a modular inverse of a value in superposition, above all in point addition for the elliptic-curve discrete logarithm. If the modulus is prime and known, inversion by [Fermat's little theorem](/fermat-little-theorem/) as $x^{p-2} \bmod p$ is an alternative that uses only multiplications; it is simpler but costs $O(n)$ multiplications, so it has more gates for large $n$. A GCD of classical numbers should be computed classically.

## Pitfalls

- **Stopping early.** A loop that stops when $v = 0$ cannot run on a superposition; the number of rounds must be fixed at the worst case.
- **Too few rounds.** The bound $2n - 1$ is reached, for example by $u = 2^{n-1} + 1$ and $v = 2^{n-1}$, so fewer rounds give wrong results for some inputs.
- **Odd $u$.** Halving $v$ keeps the GCD only when $u$ is odd. With an even $u$ the circuit computes something else.
- **History.** Dropping the history bits instead of uncomputing them leaves garbage entangled with the inputs and destroys interference in the larger algorithm.
- **Wire order.** The halving is a relabeling of wires, so the position of each bit of $v$ changes from round to round; the backward run must use the same labels.

## Implementations

## History

Stein published the binary GCD in 1967, and Knuth analyzed it in detail. Bennett (1973 and 1989) showed how to make any computation reversible by keeping a history and erasing it after the output is copied. Proos and Zalka (2003) gave the first detailed reversible Euclidean algorithm for Shor's elliptic-curve discrete logarithm and named the quantum halting problem. Roetteler, Naehrig, Svore and Lauter (2017) ran the binary extended Euclidean algorithm for a fixed $2n$ rounds and counted its Toffoli gates, and Häner, Jaques, Naehrig, Roetteler and Soeken (2020) improved it further.

## References
