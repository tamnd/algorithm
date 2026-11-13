---
tag: JXGTEC
kind: algorithm
slug: quantum-modular-inversion
name: Quantum modular inversion
aliases:
- reversible modular inverse
area: quantum/quantum-number-theory
level: advanced
summary: A reversible circuit that maps |x>|0> to |x>|x^-1 mod N> for a classical odd N. It runs the extended binary GCD for a fixed number of rounds, copies the result and uncomputes the rest.
solves: [modular-inverse]
model: quantum-circuit-model
complexity:
  vars: {n: "the bit length of the odd modulus N"}
  time: {toffoli_gates: 128n^2 + 16n - 40, depth: O(n^2)}
  space: {data_qubits: 2n, ancilla_qubits: 9n + 6}
properties: {deterministic: true, exact: true, quantum: true, reversible: true, data_oblivious: true}
history:
  year: 2003
  people: [John Proos, Christof Zalka]
  note: Proos and Zalka gave reversible modular inversion by Euclid's algorithm for the elliptic-curve discrete logarithm. Roetteler, Naehrig, Svore and Lauter (2017) gave a fixed-schedule circuit for Kaliski's Montgomery inverse with full gate counts.
prereqs: [quantum-gcd, modular-inverse, extended-euclidean-algorithm, uncomputation]
see_also: [quantum-elliptic-curve-discrete-log, quantum-modular-exponentiation, elliptic-curve-cryptography, montgomery-multiplication, fermat-little-theorem, binary-gcd, quantum-resource-estimation-factoring, quantum-oracle]
sources:
  - paper: arxiv:1706.06752
    title: "Martin Roetteler, Michael Naehrig, Krysta M. Svore and Kristin Lauter, Quantum resource estimates for computing elliptic curve discrete logarithms, ASIACRYPT 2017"
    locator: Section 3.4 (the reversible Montgomery-Kaliski round function, 2n rounds and a counter) and Table 1 (the cost of inv modp)
  - paper: arxiv:quant-ph/0301141
    title: "John Proos and Christof Zalka, Shor's discrete logarithm quantum algorithm for elliptic curves, Quantum Information and Computation 3(4):317-344, 2003"
    locator: the modular inverse by Euclid's algorithm and the quantum halting problem
  - paper: arxiv:2001.09580
    title: "Thomas Häner, Samuel Jaques, Michael Naehrig, Martin Roetteler and Mathias Soeken, Improved quantum circuits for elliptic curve discrete logarithms, PQCrypto 2020"
    locator: the improved modular inversion by a reformulated binary Euclidean algorithm
  - paper: "Burton S. Kaliski Jr., The Montgomery inverse and its applications, IEEE Transactions on Computers 44(8):1064-1065, 1995"
    title: Burton S. Kaliski Jr., The Montgomery inverse and its applications
    locator: the almost inverse x^-1 2^k by the binary extended Euclidean algorithm, with k between n and 2n
  - paper: "Daniel J. Bernstein and Bo-Yin Yang, Fast constant-time gcd computation and modular inversion, IACR Transactions on Cryptographic Hardware and Embedded Systems 2019(3):340-398, 2019"
    title: Daniel J. Bernstein and Bo-Yin Yang, Fast constant-time gcd computation and modular inversion
    locator: inversion with a fixed number of division steps
  - paper: doi:10.1103/PhysRevA.54.147
    title: "Vlatko Vedral, Adriano Barenco and Artur Ekert, Quantum networks for elementary arithmetic operations, Physical Review A 54(1):147-153, 1996"
    locator: the adder modulo N, used here for the modular subtraction
  - paper: doi:10.1137/0218053
    title: "Charles H. Bennett, Time/space trade-offs for reversible computation, SIAM Journal on Computing 18(4):766-776, 1989"
    locator: computing, copying the output and uncomputing
---

Quantum modular inversion is a reversible circuit that maps $|x\rangle|0\rangle$ to $|x\rangle|x^{-1} \bmod N\rangle$ for a classical odd modulus $N$, so it computes the [modular inverse](/modular-inverse/) of every $x$ in a superposition at once. The circuit on this page extends the [quantum GCD](/quantum-gcd/) circuit with two coefficient registers, which follow the same swaps and subtractions as in the [extended Euclidean algorithm](/extended-euclidean-algorithm/). It is the most expensive step of elliptic-curve point addition, and so of the [quantum elliptic-curve discrete logarithm](/quantum-elliptic-curve-discrete-log/).

## In plain words

To find the inverse of a number, run the greatest common divisor method on it and on the modulus, and keep two extra numbers that record how each value was built from the input. When the method ends with one, one of the two extra numbers is the inverse.

Each step must be undoable, so the extra numbers are changed in a way that can be reversed: they swap when the main values swap, subtract when they subtract, and are halved with a wrap-around when the values are halved. As on the GCD page, the circuit always runs the largest number of steps, writes small notes, copies the answer and then undoes all steps to erase the notes.

## The problem

Given a classical odd integer $N \ge 3$ with bit length $n$, build a circuit of NOT, CNOT and Toffoli gates with

$$U\,|x\rangle|0\rangle|0\rangle = |x\rangle|x^{-1} \bmod N\rangle|0\rangle \quad \text{for all } 0 \le x < N \text{ with } \gcd(x, N) = 1,$$

where the last register holds all [ancillas](/ancilla-qubits/). The gate sequence must not depend on $x$. In elliptic-curve use, $N$ is the prime $p$ of the field, so every $x \ne 0$ is a unit.

## The algorithm

The state is $(u, v, A, B)$ with the invariants $A x \equiv u$ and $B x \equiv v \pmod N$, starting from $(N, x, 0, 1)$. The register of $x$ serves as $v$. The registers $u$, $A$ and $B$ are ancillas; $A$ and $B$ have $n + 1$ qubits. Each round $i$ stores the bits $e_i$ and $h_i$ of the quantum GCD.

```pseudo id=main
QINV(x; out)                          ▷ N odd and classical; out = 0
L1  u ← N; A ← 0; B ← 1               ▷ NOT gates; v is the register of x
L2  for i ← 1 to 2n - 1 do
L3      e_i ← v_0; h_i ← e_i ∧ [v < u]          ▷ the comparison bit is cleared again
L4      if h_i = 1 then swap u with v and A with B
L5      if e_i = 1 then v ← v - u and B ← (B - A) mod N
L6      v ← v / 2                                ▷ relabel the wires of v
L7      B ← B / 2 mod N                          ▷ B + N if B is odd, then relabel
L8  out ← out ⊕ A                                ▷ n CNOT gates
L9  run lines L2 to L7 backward, then undo line L1
```

Line L5 computes $B - A \bmod N$ with the modular adder of Vedral, Barenco and Ekert run backward, on a copy of $A$ made under the control $e_i$. Line L7 copies the parity of $B$ into a flag $p$, adds $N$ under $p$, so $B$ becomes even and stays below $2N$, and divides by 2 by relabeling wires. The flag is then cleared by one comparison, because $p = 1$ exactly when the new $B$ is at least $(N + 1)/2$. Lines L8 and L9 are the compute, copy and [uncompute](/uncomputation/) pattern.

## Example

Take $N = 15$ and $x = 7$, so $n = 4$ and there are 7 rounds. The table shows $(u, v, A, B)$ after each round.

| round | $e_i$ | $h_i$ | u | v | A | B |
|---|---|---|---|---|---|---|
| start | | | 15 | 7 | 0 | 1 |
| 1 | 1 | 1 | 7 | 4 | 1 | 7 |
| 2 | 0 | 0 | 7 | 2 | 1 | 11 |
| 3 | 0 | 0 | 7 | 1 | 1 | 13 |
| 4 | 1 | 1 | 1 | 3 | 13 | 9 |
| 5 | 1 | 0 | 1 | 1 | 13 | 13 |
| 6 | 1 | 0 | 1 | 0 | 13 | 0 |
| 7 | 0 | 0 | 1 | 0 | 13 | 0 |

In round 1, $7 < 15$, so the registers swap to $(7, 15, 1, 0)$, then $v = 8$ and $B = 0 - 1 = 14$, and halving gives $v = 4$ and $B = 14/2 = 7$; indeed $7 \cdot 7 = 49 \equiv 4$. In round 2, $B = 7$ is odd, so it becomes $(7 + 15)/2 = 11$. At the end $u = 1$ and $A = 13$, and $7 \cdot 13 = 91 = 6 \cdot 15 + 1$. Line L8 copies 13, and line L9 restores $x = 7$ and clears all ancillas.

## Correctness

The invariants hold at the start, since $0 \cdot x \equiv N \equiv 0$ and $1 \cdot x = x$. A swap swaps both pairs; a subtraction gives $(B - A)x \equiv v - u$; and halving gives $(B/2)x \equiv v/2$ because 2 is invertible modulo the odd $N$. The values $u$ and $v$ follow the quantum GCD exactly, so after $2n - 1$ rounds $v = 0$ and $u = \gcd(x, N)$. Once $v = 0$, $B x \equiv 0$ forces $B = 0$ for a unit $x$, so the extra rounds change nothing. Then $A x \equiv u = 1$, so $A = x^{-1} \bmod N$. For a non-unit $x$ the output is still a value $A$ with $A x \equiv \gcd(x, N)$. The full proof is in the proofs file.

## Complexity

In the gate set NOT, CNOT and Toffoli, with the adder of Cuccaro, Draper, Kutin and Moulton and schoolbook arithmetic, one round costs $32n + 20$ Toffolis: $8n + 1$ for the comparison, $2n + 1$ for the two swaps, $4n$ for $v - u$, $12(n + 1)$ for $B - A \bmod N$ with its copies, and $6(n + 1)$ for the halving. With the backward run the exact count is

$$2(2n - 1)(32n + 20) = 128 n^2 + 16 n - 40$$

Toffoli gates, for example 2072 for $N = 15$ and 8280 for $N = 251$ in the reference implementation. The depth is $O(n^2)$. The circuit uses $2n$ data qubits ($x$ and the output) and $9n + 6$ ancillas: $n$ for $u$, $4(n + 1)$ for $A$, $B$ and two work registers, 4 single flags, and $2(2n - 1)$ history qubits.

This circuit is written for clarity. Roetteler, Naehrig, Svore and Lauter report $7n + 2\lceil \log_2 n \rceil + 9$ qubits in total, of which $5n + 2\lceil \log_2 n \rceil + 9$ are ancillas, and about $32 n^2 \log_2 n$ Toffoli gates for their inversion, with adders that use fewer clean qubits. All these are logical counts; error correction adds its own overhead, as in [quantum resource estimation for factoring](/quantum-resource-estimation-factoring/).

## Properties

- **Data oblivious.** The gate sequence is fixed, so the circuit works on superpositions.
- **Exact.** The output is exact for every unit $x$.
- **Clean.** All ancillas and history qubits end in $|0\rangle$.
- **Out of place.** The inverse is written into a new register. An in-place version $|x\rangle \mapsto |x^{-1}\rangle$ needs a second inversion run backward, as in the in-place multiplier of [quantum modular exponentiation](/quantum-modular-exponentiation/).

## Variants and improvements

- **Montgomery inverse.** Kaliski's algorithm computes the "almost inverse" $x^{-1} 2^k$ with $n \le k \le 2n$ and no halving modulo $N$; the coefficients are doubled instead. Roetteler et al. run it for $2n$ rounds with a counter of $O(\log n)$ qubits for the rounds after $v = 0$, store only one history qubit per round by using the parity of the coefficients, and fix the power of 2 at the end with controlled modular doublings.
- **Lower depth and T count.** Häner, Jaques, Naehrig, Roetteler and Soeken reformulate the binary Euclidean algorithm and give trade-offs between qubits, depth and T gates.
- **Euclid with quotients.** Proos and Zalka use the classical Euclidean algorithm and share space between the shrinking remainders and the growing coefficients.
- **Fermat inversion.** For a prime $N$, $x^{-1} = x^{N-2} \bmod N$ by [Fermat's little theorem](/fermat-little-theorem/). This needs only multiplications but $O(n)$ of them, so $O(n^3)$ Toffolis with schoolbook multiplication.
- **Division steps.** The constant-time inversion of Bernstein and Yang uses a fixed number of simple steps and fits the same reversible pattern.
- **Avoiding inversions.** Classically, projective coordinates remove most inversions from point addition. Roetteler et al. leave their use in Shor's algorithm open, because each point becomes a class of coordinate vectors and the extra temporary values must be uncomputed.

## When to use it

Use it for point addition in the [quantum elliptic-curve discrete logarithm](/quantum-elliptic-curve-discrete-log/), where the slope of a line needs a field inverse of a value in superposition, and in any reversible oracle that divides modulo a known odd modulus. If the value to invert is classical, invert it classically, as in the constants $a^{-1}$ of modular exponentiation.

## Pitfalls

- **Even modulus.** Halving modulo $N$ needs an odd $N$; for an even $N$ the method fails.
- **Non-units.** If $\gcd(x, N) > 1$, the output is not an inverse; the input $x = 0$ gives 0. An oracle that may see such inputs must flag them.
- **Overflow.** $B + N$ can reach $2N - 1$, so $B$ needs $n + 1$ qubits.
- **Early stopping.** The loop cannot stop when $v = 0$, because the stopping time depends on $x$. This is the quantum halting problem of Proos and Zalka.
- **Cost estimates.** Toffoli counts depend on the adder and on how many clean ancillas are allowed, so compare circuits only under the same gate set and qubit budget.

## Implementations

## History

Kaliski (1995) defined the Montgomery inverse and computed it with the binary extended Euclidean algorithm. Proos and Zalka (2003) showed that inversion is the main cost of Shor's algorithm for elliptic curves and that its input-dependent stopping time must be handled. Roetteler, Naehrig, Svore and Lauter (2017) gave a fixed-schedule circuit with full Toffoli counts, simulated in LIQUi|>, and Häner, Jaques, Naehrig, Roetteler and Soeken (2020) improved its depth and T count.

## References
