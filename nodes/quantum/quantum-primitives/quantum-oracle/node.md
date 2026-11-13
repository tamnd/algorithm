---
tag: KDN9PQ
kind: definition
slug: quantum-oracle
name: Quantum oracle
aliases:
- black-box oracle
- oracle access
- phase oracle
- bit oracle
- standard quantum oracle
area: quantum/quantum-primitives
level: intro
summary: "A unitary that gives a quantum algorithm access to a function f. The bit form maps |x>|y> to |x>|y xor f(x)>, the phase form maps |x> to (-1)^f(x)|x>, and each use counts as one query."
prereqs: [unitary-operator, query-model, reversible-computation]
see_also: [quantum-query-model, quantum-query-complexity, oracle-turing-machine, phase-kickback, uncomputation, relativization, quantum-random-access-memory, quantum-random-oracle-model]
sources:
  - paper: doi:10.1137/S0097539796300933
    title: "Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5):1510-1523, 1997"
    locator: quantum machines with oracle access, and the bound that relative to a random oracle NP is not solved in time o(2^(n/2))
  - paper: doi:10.1145/502090.502097
    title: "Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4):778-797, 2001"
    locator: the query model with the oracle |i, b> -> |i, b xor x_i> for an input string x
  - paper: doi:10.1098/rspa.1998.0164
    title: "Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca, Quantum algorithms revisited, Proceedings of the Royal Society of London A 454(1969):339-354, 1998"
    locator: the oracle on a target qubit in the state |0> - |1>, which writes f(x) into a phase
  - paper: doi:10.1103/PhysRevA.65.050304
    title: "Elham Kashefi, Adrian Kent, Vlatko Vedral and Konrad Banaszek, Comparison of quantum oracles, Physical Review A 65(5):050304, 2002"
    locator: "minimal (in-place) oracles |x> -> |pi(x)> for a permutation pi, and their cost compared with standard oracles"
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, lecture notes
    locator: "Section 2.4 (queries, and the phase query from a standard query) and Exercise 2.10 (a standard query from a controlled phase query)"
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Sections 1.4.2 to 1.4.4 (U_f and its use in Deutsch's algorithm) and Chapter 6 (the oracle of quantum search)"
---

A *quantum oracle* for a function $f$ is a fixed unitary that a quantum algorithm may apply, but whose inner circuit it may not look at; each application is one *query*. The bit form $U_f|x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle$ works for every function, and the phase form $O_f|x\rangle = (-1)^{f(x)}|x\rangle$ works for Boolean functions. One query to the bit form gives the phase form by [phase kickback](/phase-kickback/), but the way back needs a controlled phase oracle. Oracles are the input model of [quantum query complexity](/quantum-query-complexity/) and the quantum form of the oracle of an [oracle Turing machine](/oracle-turing-machine/).

## Definition

### The bit oracle

Let $f : \{0,1\}^n \to \{0,1\}^m$. The *bit oracle* (or *standard oracle*) of $f$ is the unitary on $n + m$ qubits

$$U_f\,|x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle, \qquad x \in \{0,1\}^n,\ y \in \{0,1\}^m,$$

where $\oplus$ is the bitwise XOR. It permutes the basis states, so it is unitary, and $U_f U_f = I$, so $U_f$ is its own inverse. This holds for every $f$, also for one that is far from injective. The register $|x\rangle$ holds the high-order qubits, as the [quantum state](/quantum-state/) page fixes, so the basis index of $|x\rangle|y\rangle$ is $x \cdot 2^m + y$.

### The phase oracle

For a Boolean function $f : \{0,1\}^n \to \{0,1\}$, the *phase oracle* is the diagonal unitary on $n$ qubits

$$O_f\,|x\rangle = (-1)^{f(x)}|x\rangle.$$

For $m > 1$ output bits the phase form is $|x\rangle|y\rangle \mapsto (-1)^{y \cdot f(x)}|x\rangle|y\rangle$, with $y \cdot f(x)$ the inner product mod 2. It equals $(I \otimes H^{\otimes m})\,U_f\,(I \otimes H^{\otimes m})$, so it is the bit oracle in the Hadamard basis of the output register.

### From one form to the other

- **Bit to phase: one query and one ancilla.** Put the output qubit in $|{-}\rangle = (|0\rangle - |1\rangle)/\sqrt2$. Then $U_f|x\rangle|{-}\rangle = (-1)^{f(x)}|x\rangle|{-}\rangle$, because $|0 \oplus f(x)\rangle - |1 \oplus f(x)\rangle = (-1)^{f(x)}(|0\rangle - |1\rangle)$. The ancilla is not changed and is not entangled with $|x\rangle$, so on every superposition one query to $U_f$ acts as one query to $O_f$.
- **Phase to bit: one query to the controlled phase oracle.** Let $C\text{-}O_f|x\rangle|c\rangle = (-1)^{c f(x)}|x\rangle|c\rangle$. Then $(I \otimes H)\,C\text{-}O_f\,(I \otimes H) = U_f$, because $H Z^{f(x)} H = X^{f(x)}$ on the qubit $c$.
- **The uncontrolled phase oracle is weaker.** The functions $f$ and $1 - f$ have $O_{1-f} = -O_f$. The two unitaries differ by a global phase, so every circuit that uses $O_f$ gives the same measurement statistics as the same circuit with $O_{1-f}$. Their bit oracles differ, since $U_{1-f} = (I \otimes X)\,U_f$. So no circuit with only uncontrolled queries to $O_f$ can compute $U_f$. A controlled phase query tells $f$ from $1 - f$: with the control in $|{+}\rangle$, the two controlled oracles give orthogonal states. The quantum query model therefore states which form it uses, or it assumes controlled queries.

### Oracles for an input string

In the [quantum query model](/quantum-query-model/) the input is a string $x \in \{0,1\}^N$, and the oracle is $O_x|i, b\rangle = |i, b \oplus x_i\rangle$ for $i \in \{0, \ldots, N - 1\}$. This is the bit oracle of the function $i \mapsto x_i$. An algorithm is a sequence $U_T O_x U_{T-1} \cdots U_1 O_x U_0$, where the $U_t$ do not depend on $x$, and its cost is the number $T$ of queries. The model may let the algorithm use work qubits that the oracle does not touch. This is the quantum form of the classical [query model](/query-model/).

### Oracles as subroutines

In an algorithm for a real problem, the oracle is a circuit. A [reversible](/reversible-computation/) circuit for $f$ with $s$ gates leaves garbage on work qubits. [Uncomputation](/uncomputation/) removes it, so that the circuit implements $U_f$ exactly with clean [ancilla qubits](/ancilla-qubits/), at a cost of about $2s$ gates. The oracle must leave no garbage: an oracle with garbage $|x\rangle|0\rangle \mapsto (-1)^{f(x)}|x\rangle|g(x)\rangle$ is a different unitary, and it breaks the interference of the algorithm that calls it.

### In-place oracles

The map $|x\rangle \mapsto |f(x)\rangle$ is unitary only when $f$ is a bijection; otherwise two basis states go to the same state. Of the $4^4 = 256$ functions from $\{0,1\}^2$ to itself, only the $4! = 24$ permutations give an in-place oracle. Kashefi, Kent, Vedral and Banaszek (2002) compare these *minimal oracles* with standard ones. One query to a permutation $\pi$ and one to $\pi^{-1}$ give $U_\pi$: copy $x$ into a clean register with CNOT gates, apply $\pi$ to it, add it into $y$, apply $\pi^{-1}$, and remove the copy of $x$. The other way needs on the order of $\sqrt{N}$ standard queries.

## Examples and non-examples

**Example: the four functions on one bit.** With $x$ the left (high) qubit and $y$ the right one, and the basis order $|00\rangle, |01\rangle, |10\rangle, |11\rangle$:

- $f = 0$: $U_f = I$, and $O_f = I$.
- $f = 1$: $U_f = I \otimes X$, and $O_f = -I$.
- $f(x) = x$: $U_f$ is the [CNOT gate](/cnot-gate/) with control $x$, and $O_f = Z$.
- $f(x) = 1 - x$: $U_f = (I \otimes X)\,\mathrm{CNOT}$, and $O_f = -Z$.

So $O_f$ for $f = 0$ and $f = 1$ give the same state up to a global phase, and the same holds for the two balanced functions. Deutsch's problem, constant or balanced, is still solved with one query to $O_f$, because it asks only for $f(0) \oplus f(1)$: the state $O_f|{+}\rangle$ is $\pm|{+}\rangle$ when $f$ is constant and $\pm|{-}\rangle$ when it is balanced.

**Example: a bit oracle with two output bits.** For $f : \{0,1\}^2 \to \{0,1\}^2$ the oracle $U_f$ permutes the 16 basis states of 4 qubits, and it is an involution for each of the 256 functions $f$. On the input $|x\rangle$ it applies $X^{f_j(x)}$ to output qubit $j$. Since $HX^bH = Z^b$, the conjugated oracle $(I \otimes H^{\otimes 2})\,U_f\,(I \otimes H^{\otimes 2})$ applies $Z^{f_j(x)}$ to output qubit $j$, which multiplies $|x\rangle|y\rangle$ by $(-1)^{y_1f_1(x) + y_0f_0(x)} = (-1)^{y \cdot f(x)}$.

**Example: phase kickback for AND.** Let $f(x_1x_0) = x_1 \wedge x_0$. Then $U_f|11\rangle|{-}\rangle = |11\rangle(|1\rangle - |0\rangle)/\sqrt2 = -|11\rangle|{-}\rangle$, and the other three basis states are unchanged. On the uniform superposition, one bit query gives $\frac12(|00\rangle + |01\rangle + |10\rangle - |11\rangle) \otimes |{-}\rangle$, which is $O_f$ applied to the input with the ancilla unchanged.

**Non-example: overwriting the input.** The map $|x\rangle|y\rangle \mapsto |x\rangle|f(x)\rangle$ forgets $y$, so it is not injective and not a unitary. The XOR in $y \oplus f(x)$ is what makes the bit oracle reversible.

**Non-example: the in-place AND.** The map $|x_1x_0\rangle \mapsto |0\, (x_1 \wedge x_0)\rangle$ sends three basis states to $|00\rangle$. It is not unitary, and no quantum circuit computes it without extra output qubits.

**Non-example: an oracle with garbage.** A circuit that maps $|x\rangle|0\rangle|0\rangle$ to $|x\rangle|g(x)\rangle|f(x)\rangle$ gives the correct $f(x)$ on each basis state, but it is not $U_f$ on the first and last registers. With a uniform superposition of inputs, the first and last registers end in a mixed state.

## Related definitions

- [Oracle Turing machine](/oracle-turing-machine/): the classical machine that asks an oracle set $A$ whether $x \in A$ in one step. The quantum machine with oracle $A$ uses the bit oracle of the indicator function of $A$. Bennett, Bernstein, Brassard and Vazirani (1997) showed that, relative to a random oracle and with probability 1, a quantum machine needs time $\Omega(2^{n/2})$ for some problems in NP, so oracle results do not show that BQP contains NP; see [relativization](/relativization/).
- [Quantum query model](/quantum-query-model/) and [quantum query complexity](/quantum-query-complexity/): the cost model in which only queries count. The [polynomial method](/polynomial-method/) and the [quantum adversary method](/quantum-adversary-method/) bound the number of queries from below.
- [Phase kickback](/phase-kickback/): the technique that turns the bit form into the phase form.
- [Quantum random access memory](/quantum-random-access-memory/): a device that implements the oracle of a stored string $x$, with $|i, b\rangle \mapsto |i, b \oplus x_i\rangle$.
- [Quantum random oracle model](/quantum-random-oracle-model/): in cryptography, a random function that the adversary can query in superposition through its bit oracle.

## References
