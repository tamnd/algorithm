---
tag: S5NABE
kind: algorithm
slug: quantum-modular-exponentiation
name: Quantum modular exponentiation
aliases:
- reversible modular exponentiation circuit
area: quantum/quantum-number-theory
level: advanced
summary: A reversible circuit that maps |x>|y> to |x>|y a^x mod N> with Toffoli, CNOT and NOT gates. It is the costly step of Shor's algorithm.
solves: [modular-exponentiation]
model: quantum-circuit-model
complexity:
  vars: {n: "the bit length of N", t: "the number of exponent qubits, t = 2n in Shor's algorithm"}
  time: {toffoli_gates: O(t n^2), toffoli_gates_shor: O(n^3), depth: O(t n^2), toffoli_gates_fast_multiplication: O(t n log n log log n)}
  space: {data_qubits: t + n, ancilla_qubits: 2n + 4}
properties: {deterministic: true, exact: true, quantum: true, reversible: true}
history:
  year: 1996
  people: [Vlatko Vedral, Adriano Barenco, Artur Ekert]
  note: Vedral, Barenco and Ekert gave the first full reversible network for modular exponentiation; Beckman, Chari, Devabhaktuni and Preskill gave a smaller one in the same year.
prereqs: [modular-exponentiation, binary-exponentiation, modular-inverse, ripple-carry-adder, toffoli-gate, reversible-computation, uncomputation, ancilla-qubits]
see_also: [shor-algorithm, order-finding, quantum-phase-estimation, quantum-gcd, quantum-modular-inversion, quantum-resource-estimation-factoring, quantum-discrete-logarithm, montgomery-multiplication]
sources:
  - paper: doi:10.1103/PhysRevA.54.147
    title: "Vlatko Vedral, Adriano Barenco and Artur Ekert, Quantum networks for elementary arithmetic operations, Physical Review A 54(1):147-153, 1996"
    locator: the plain adder, the adder modulo N, the controlled multiplier and the modular exponentiation network
  - paper: doi:10.1103/PhysRevA.54.1034
    title: "David Beckman, Amalavoyal N. Chari, Srikrishna Devabhaktuni and John Preskill, Efficient networks for quantum factoring, Physical Review A 54(2):1034-1063, 1996"
    locator: the network with 5K + 1 qubits and about 72K^3 gates for a K-bit modulus
  - paper: arxiv:quant-ph/0410184
    title: Steven A. Cuccaro, Thomas G. Draper, Samuel A. Kutin and David Petrie Moulton, A new quantum ripple-carry addition circuit, 2004
    locator: the MAJ and UMA blocks and the adder with one ancilla
  - paper: arxiv:quant-ph/0008033
    title: Thomas G. Draper, Addition on a quantum computer, 2000
    locator: addition in the Fourier basis without carry qubits
  - paper: arxiv:quant-ph/0205095
    title: "Stephane Beauregard, Circuit for Shor's algorithm using 2n+3 qubits, Quantum Information and Computation 3(2):175-185, 2003"
    locator: the modular adder with Fourier-basis addition of classical constants and the circuit with 2n + 3 qubits
  - paper: arxiv:1611.07995
    title: "Thomas Häner, Martin Roetteler and Krysta M. Svore, Factoring using 2n+2 qubits with Toffoli based modular multiplication, Quantum Information and Computation 17(7-8):673-684, 2017"
    locator: the Toffoli-based modular multiplier with dirty ancillas
  - paper: arxiv:quant-ph/9806084
    title: Christof Zalka, Fast versions of Shor's quantum factoring algorithm, 1998
    locator: modular exponentiation with fast multiplication and parallel circuits
  - paper: arxiv:1905.07682
    title: Craig Gidney, Windowed quantum arithmetic, 2019
    locator: table lookups that process a window of exponent qubits at once
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: the section on reversible modular exponentiation and its cost with schoolbook and with fast multiplication
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.3.1 (the cost of modular exponentiation in order finding)
  - paper: doi:10.1038/nature12290
    title: "John A. Smolin, Graeme Smith and Alexander Vargo, Oversimplifying quantum factoring, Nature 499:163-165, 2013"
    locator: compiled circuits that use the answer
---

Quantum modular exponentiation is a reversible circuit that maps $|x\rangle|y\rangle$ to $|x\rangle|y\,a^x \bmod N\rangle$ for a fixed base $a$ and modulus $N$. It is the step of [Shor's algorithm](/shor-algorithm/) and [order finding](/order-finding/) that uses almost all of the gates. This page builds it from a reversible [ripple-carry adder](/ripple-carry-adder/), with the network of Vedral, Barenco and Ekert: modular adders make a modular multiplier, and multipliers by the constants $a^{2^j} \bmod N$ make the exponentiation. The circuit uses only NOT, CNOT and [Toffoli](/toffoli-gate/) gates and returns all its [ancillas](/ancilla-qubits/) to 0.

## In plain words

To raise a number to a power, square it again and again and multiply together the squares that the bits of the exponent pick out. A quantum computer must do this without losing any information, because its steps must be undoable. So each step is built from adders that can be run backward.

First an adder that adds a fixed number and wraps around at the modulus. Many of these, one for each bit of the input, make a multiplier by a fixed number. A multiplier writes its answer into a new register, so the old input is then cleaned away by a second multiplier run backward. Each bit of the exponent switches on one multiplier. All scratch space is clean at the end, so the circuit works on a superposition of all exponents at once.

## The problem

Given classical integers $N \ge 3$ and $a$ with $\gcd(a, N) = 1$, and a number $t$ of exponent qubits, build a circuit $U$ of NOT, CNOT and Toffoli gates with

$$U\,|x\rangle|y\rangle|0\rangle = |x\rangle|y\,a^x \bmod N\rangle|0\rangle \quad \text{for all } 0 \le x < 2^t,\ 0 \le y < N,$$

where the last register holds the ancillas. With $y = 1$ this computes the [modular exponentiation](/modular-exponentiation/) $a^x \bmod N$. Because $U$ permutes basis states, it acts linearly on superpositions of $x$, which is what [phase estimation](/quantum-phase-estimation/) needs. Let $n$ be the bit length of $N$.

## The algorithm

The registers are the exponent $x$ ($t$ qubits), the work register $y$ ($n$ qubits), an accumulator $b$ ($n + 1$ qubits), a register for constants ($n + 1$ qubits), the carry qubit of the adder and one flag qubit $f$. The adder is the one of Cuccaro, Draper, Kutin and Moulton: "$b \leftarrow b + k$" loads the classical constant $k$ into the constant register with NOT gates (controlled by the same controls), adds it to $b$ modulo $2^{n+1}$, and unloads it. Subtraction is the adder run backward. On $n + 1$ qubits, the top bit of $b$ is the sign of $b$ in [two's complement](/twos-complement/).

```pseudo id=main
MODADD(k, N; controls C; b)          ▷ 0 ≤ b < N and 0 ≤ k < N; f = 0
L1  if all of C are 1 then b ← b + k
L2  b ← b - N                         ▷ modulo 2^(n+1)
L3  f ← f ⊕ top(b)                    ▷ f = 1 when b < 0
L4  if f = 1 then b ← b + N
L5  if all of C are 1 then b ← b - k  ▷ now top(b) = 1 exactly when f = 0
L6  f ← f ⊕ (1 ⊕ top(b))              ▷ resets f to 0
L7  if all of C are 1 then b ← b + k

CMULT(a, N; ctrl; y, b)               ▷ b ← (b + a y) mod N when ctrl = 1
L8  for i ← 0 to n - 1 do
L9      MODADD(2^i a mod N, N; {ctrl, y_i}; b)

CU(a, N; ctrl; y)                     ▷ y ← a y mod N when ctrl = 1; b = 0 before and after
L10 CMULT(a, N; ctrl; y, b)           ▷ b = a y mod N
L11 if ctrl = 1 then swap y and the low n bits of b
L12 run CMULT(a^(-1) mod N, N; ctrl; y, b) backward   ▷ b ← b - a^(-1) y mod N, which is 0

MODEXP(a, N; x, y)                    ▷ c = a mod N at the start
L13 for j ← 0 to t - 1 do
L14     CU(c, N; x_j; y)
L15     c ← c^2 mod N                 ▷ classical
```

Lines L2 to L4 subtract $N$ and add it back when the result is negative, so after L4 $b$ holds $(b + k) \bmod N$. The flag $f$ now records whether a wrap-around happened, and lines L5 to L7 erase it by a second comparison, which is a small case of [uncomputation](/uncomputation/). Line L9 adds the classical constants $2^i a \bmod N$, so the bits of $y$ choose which ones to add. Lines L10 to L12 are the in-place multiplication described on the uncomputation page; they need $a^{-1} \bmod N$, which is computed classically with the [extended Euclidean algorithm](/extended-euclidean-algorithm/). Line L15 computes the next constant by [repeated squaring](/binary-exponentiation/) on a classical computer, so no quantum gates are spent on it.

## Example

Take $N = 15$ and $a = 7$, so $n = 4$ and $7^{-1} \bmod 15 = 13$.

**One modular addition.** MODADD with $k = 7$ on $b = 9$, both controls 1. Line L1 gives $b = 16$, line L2 gives $1$, which is not negative, so $f$ stays 0 and line L4 does nothing. Line L5 gives $1 - 7 = -6$, stored as $26$ on 5 bits, whose top bit is 1. So line L6 leaves $f = 0$, and line L7 gives $b = 1 = (9 + 7) \bmod 15$.

**One in-place multiplication.** CU with $c = 7$ on $y = 4$ and control 1. Line L10 adds $7 \cdot 4 \bmod 15 = 13$ to $b = 0$. Line L11 swaps, so $y = 13$ and $b = 4$. Line L12 subtracts $13 \cdot 13 \bmod 15 = 4$ from $b$, so $b = 0$, and $y = 13 = 7 \cdot 4 \bmod 15$.

**The exponentiation.** With $t = 3$ the constants are $c = 7, 4, 1$ for $j = 0, 1, 2$. For $x = 5 = 101_2$ and $y = 1$, the circuit multiplies by 7 and by 1, so $y = 7 = 7^5 \bmod 15$. Shor's algorithm for $N = 15$ uses $t = 8$; the gate counts of that circuit are in the table below.

## Correctness

Each piece is checked on basis states, and linearity extends it to superpositions. MODADD maps $b$ to $(b + k) \bmod N$ and resets $f$, because after line L5 the sign of $b$ is the negation of $f$; the value $b + k < 2N \le 2^{n+1}$ never overflows the $n + 1$ qubits. CMULT adds $\sum_i y_i 2^i a = a y$ modulo $N$. CU leaves $y \leftarrow a y$ and $b = y - a^{-1} a y = 0$. MODEXP multiplies $y$ by $\prod_j c_j^{x_j} = a^{\sum_j x_j 2^j} = a^x$. When a control is 0 the corresponding piece is the identity. The full proof is in the proofs file.

## Complexity

The adder on $n + 1$ bits uses $2(n + 1)$ Toffoli gates. MODADD uses five adders, and its two-controlled loads of $k$ add $6\,w(k)$ Toffoli gates, where $w(k)$ is the number of 1 bits of $k$; the loads of $N$ use only NOT and CNOT gates. CU uses $2n$ MODADDs and $n$ Fredkin gates of one Toffoli each. So the exact Toffoli count is

$$T = t\,(20 n^2 + 21 n) + 6P,$$

where $P$ is the sum of $w$ over the $2tn$ constants $2^i c \bmod N$ and $2^i c^{-1} \bmod N$. As $0 \le w \le n$, this gives $t(20n^2 + 21n) \le T \le t(32n^2 + 21n)$, and with $t = 2n$ about $40 n^3$ to $64 n^3$ Toffolis, with about $52 n^3$ for typical constants. The depth is $O(t n^2)$ because the adders run one after the other.

| N | a | n | t | Toffoli | CNOT | NOT | data qubits | ancillas |
|---|---|---|---|---|---|---|---|---|
| 15 | 7 | 4 | 8 | 3712 | 7104 | 640 | 12 | 12 |
| 21 | 2 | 5 | 9 | 6201 | 11610 | 720 | 14 | 14 |
| 35 | 2 | 6 | 11 | 11034 | 19668 | 1056 | 17 | 16 |
| 255 | 2 | 8 | 16 | 24704 | 50944 | 4608 | 24 | 20 |

The counts are from the gate lists of the reference implementation with $t$ equal to the bit length of $N^2 - 1$; there is no randomness. For $N = 255$ the measured value is $T \approx 48 n^3$.

The circuit uses $t + n$ data qubits and $2n + 4$ ancillas. The gate set is NOT, CNOT and Toffoli, and the multiplication method is schoolbook shift-and-add. In the Clifford+T set each Toffoli costs 7 [T gates](/phase-and-t-gates/). These are logical counts; on real hardware each logical qubit and gate also costs the overhead of [quantum error correction](/quantum-error-correction/), which is covered in [quantum resource estimation for factoring](/quantum-resource-estimation-factoring/). With [Schönhage-Strassen multiplication](/schonhage-strassen-multiplication/) instead of [schoolbook multiplication](/schoolbook-multiplication/), the gate count falls to $O(t\, n \log n \log\log n)$, but only for very large $n$.

## Properties

- **Exact.** The circuit computes the map with no error on every basis state with $y < N$.
- **Clean ancillas.** Every ancilla is 0 at the end, so no garbage is entangled with $x$.
- **Classical constants.** The base and its powers are classical, so each multiplication is by a constant and needs no second quantum operand.
- **Controlled by single qubits.** Each exponent qubit controls one CU, which allows the semiclassical Fourier transform to reuse one control qubit for all $t$ steps.

## Variants and improvements

- **Fourier-basis adders.** Draper's adder works in the Fourier basis with controlled rotations and no carry qubits. Beauregard adds classical constants this way and gets Shor's algorithm with $2n + 3$ qubits, at the cost of $O(n^3 \log n)$ gates with rotations.
- **Fewer qubits with Toffoli gates.** Häner, Roetteler and Svore use borrowed (dirty) qubits for the constant adder and need $2n + 2$ qubits.
- **Early networks.** Beckman, Chari, Devabhaktuni and Preskill gave a network with $5K + 1$ qubits and about $72 K^3$ gates for a $K$-bit modulus, and studied trade-offs of space against time.
- **Fast multiplication.** Zalka used FFT-based multiplication and parallel circuits to lower the depth.
- **Windowed arithmetic.** Gidney's windowed arithmetic replaces the controls of several exponent qubits by one table lookup, which cuts the number of multiplications by the window size. Gidney and Ekerå combine it with coset representations and approximate arithmetic in their 2021 estimate.
- **Other reductions.** [Montgomery multiplication](/montgomery-multiplication/) replaces the reduction modulo $N$ by divisions by 2, and some quantum multipliers use it. The [Ekerå-Håstad algorithm](/ekera-hastad-algorithm/) uses shorter exponents, and [Regev's algorithm](/regev-factoring-algorithm/) uses many small bases instead of one large exponent.

## When to use it

Use it inside [order finding](/order-finding/), [Shor's algorithm](/shor-algorithm/) and the [quantum discrete logarithm](/quantum-discrete-logarithm/), where the base is known and the exponent is in superposition. For a resource estimate, count the Toffoli gates of the circuit you will build, with the windowed variants for large $n$. For a demonstration on a small device, a circuit specialized to one known $N$ and $a$ is smaller, but it does not show that the general circuit works.

## Pitfalls

- **Input range.** The map holds only for $y < N$ and $b < N$. For $y \ge N$ the circuit is still reversible but computes a different map.
- **Non-units.** If $\gcd(a, N) > 1$, then $a^{-1}$ does not exist and line L12 cannot run. This case gives a factor classically, so test it first.
- **Overflow.** The accumulator needs $n + 1$ qubits, because $b + k$ can reach $2N - 2$ and the sign of $b - N$ must be read.
- **Garbage.** Ancillas that are not reset stay entangled with $x$ and destroy the interference of the Fourier transform. A test must check that all ancillas return to 0.
- **Compiled circuits.** A circuit that uses the answer, such as the known order of $a$, can be reduced to almost nothing; Smolin, Smith and Vargo showed how far this goes. Small demonstrations for $N = 15$ were of this kind.
- **Counting.** Report data qubits and ancillas apart, and state the gate set, because a Toffoli is one gate in this count but 7 T gates and several CNOTs in Clifford+T.

## Implementations

## History

Shor (1994) noted that modular exponentiation can be done reversibly with $O(n^3)$ gates by Bennett's methods, and with fast multiplication in $O(n^2 \log n \log\log n)$. Vedral, Barenco and Ekert (1996) gave the first explicit network of adders, modular adders and multipliers, and Beckman, Chari, Devabhaktuni and Preskill (1996) gave a smaller one with counts for ion traps. Draper (2000) introduced Fourier-basis addition, Beauregard (2003) used it to reach $2n + 3$ qubits, and Cuccaro, Draper, Kutin and Moulton (2004) gave the ripple-carry adder with one ancilla used here. Later work by Häner, Roetteler and Svore (2017), Gidney (2019) and Gidney and Ekerå (2021) lowered the qubit and Toffoli counts for practical sizes.

## References
