---
tag: 2V47CD
kind: technique
slug: uncomputation
name: Uncomputation
aliases:
- garbage uncomputation
- compute-copy-uncompute
area: quantum/quantum-primitives
level: core
summary: "Compute a value with a reversible circuit, copy it to a fresh register, then run the circuit backward. The work qubits return to |0> and leave no garbage entangled with the result."
prereqs: [reversible-computation, ancilla-qubits]
see_also: [entanglement, quantum-oracle, phase-kickback, partial-trace, quantum-interference, toffoli-gate, grover-search, linear-combination-of-unitaries]
sources:
  - paper: doi:10.1147/rd.176.0525
    title: "Charles H. Bennett, Logical reversibility of computation, IBM Journal of Research and Development 17(6):525-532, 1973"
    locator: the three stages of the reversible machine (compute with a history, copy the output, run backward to erase the history)
  - paper: doi:10.1137/0218053
    title: "Charles H. Bennett, Time/space trade-offs for reversible computation, SIAM Journal on Computing 18(4):766-776, 1989"
    locator: uncomputing in stages with checkpoints to save space
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, lecture notes
    locator: "Exercise 2.11 (workspace left by a query destroys interference) and Section 7.4 (the phase oracle for satisfiability: compute, apply Z, uncompute)"
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 3.2.5 (Bennett's construction) and Section 1.4.1 (classical computations on a quantum computer, garbage bits)"
  - paper: doi:10.22331/q-2018-06-18-74
    title: "Craig Gidney, Halving the cost of quantum addition, Quantum 2:74, 2018"
    locator: the temporary logical-AND, computed with four T gates and uncomputed by a measurement with no T gate
---

*Uncomputation* removes the intermediate values that a reversible circuit leaves on its work qubits. Run the circuit $C$ that computes $f(x)$, copy $f(x)$ to a fresh output register with CNOT gates, then run $C^{-1}$: every work qubit returns to $|0\rangle$, and the result is $|x\rangle|0\rangle|y \oplus f(x)\rangle$. On classical bits this only frees memory. On a superposition of inputs it is necessary, because values left on the work qubits stay [entangled](/entanglement/) with the result, and they stop the interference that a quantum algorithm needs.

## In plain words

A circuit that computes a value often writes partial results on scratch qubits. On one classical input these leftovers are harmless. In a quantum computer the input is often a superposition of many inputs. Then each input leaves its own leftovers, and the leftovers mark which input each part of the state came from.

Marked parts cannot cancel each other, so a later step that relies on cancellation fails. Uncomputation removes the marks. First compute the answer. Then copy the answer to a fresh place. Then run the first step backward. The scratch qubits go back to blank, and only the input and the copied answer stay.

## When it applies

- A reversible circuit $C$ computes a function $f$ of a register: $C|x\rangle|0^s\rangle = |x\rangle|w(x)\rangle$, where $w(x)$ holds $f(x)$ at known positions and other values (the *garbage*) at the rest.
- The next step needs only $f(x)$, not the garbage. This is the usual case for an [oracle](/quantum-oracle/), whose definition allows no garbage.
- The inverse $C^{-1}$ is available. For a gate list it is the gates in reverse order, each inverted.
- The circuit runs on a superposition, or it is a subroutine of a circuit that does. On classical inputs alone the garbage costs only memory.

## The template

The registers are the input $x$ ($n$ qubits), the work register ($s$ qubits, all $|0\rangle$) and the output $y$ ($m$ qubits).

```pseudo id=main
UNCOMPUTE(C, COPY)
L1  apply C to (input, work)        ▷ hole: a reversible circuit; work ends as w(x) ⊇ f(x)
L2  apply COPY to (work, output)    ▷ hole: one CNOT per bit of f(x), or Z on f(x) for a phase
L3  apply C^-1 to (input, work)     ▷ the gates of C in reverse order, each inverted
```

On a basis state the three lines give

$$|x\rangle|0^s\rangle|y\rangle \xrightarrow{C} |x\rangle|w(x)\rangle|y\rangle \xrightarrow{\text{COPY}} |x\rangle|w(x)\rangle|y \oplus f(x)\rangle \xrightarrow{C^{-1}} |x\rangle|0^s\rangle|y \oplus f(x)\rangle.$$

**Why it works.** The COPY gates only read the work register, so after L2 the input and work registers still hold $C|x\rangle|0^s\rangle$. Line L3 acts only on these two registers, and $C^{-1}C = I$, so it gives back $|x\rangle|0^s\rangle$. The output register is not touched by L1 or L3. By linearity the same holds for every superposition $\sum_x \alpha_x |x\rangle$: the result is $\sum_x \alpha_x |x\rangle|0^s\rangle|y \oplus f(x)\rangle$, and the work register is a fixed $|0^s\rangle$ that factors out. The argument also holds when $C$ changes the input register on the way, for example in an in-place adder.

**The phase form.** For one output bit, take the COPY step to be a $Z$ gate on the wire that holds $f(x)$. Then the template maps $|x\rangle|0^s\rangle$ to $(-1)^{f(x)}|x\rangle|0^s\rangle$, the phase form of the oracle, with no output qubit. The bit form with the output in $|{-}\rangle$ gives the same phase by [phase kickback](/phase-kickback/). Both give an exact phase only because the work register returns to $|0^s\rangle$.

**Cost.** The template uses $2|C| + m$ gates and $s$ work qubits, and every work qubit is free again at the end. In the Clifford plus T gate set, $C^{-1}$ has the same number of T gates as $C$, because the inverse of $T$ is $T^\dagger$.

**Example: majority of three bits.** Let $C$ compute $x_0x_1$, $x_0x_2$ and $x_1x_2$ with three [Toffoli gates](/toffoli-gate/) on work qubits 3, 4, 5, then $x_0x_1 \oplus x_0x_2$ on qubit 6 and $\mathrm{maj}(x)$ on qubit 7 with four CNOT gates. Qubit 8 is the output. The garbage $w(x)$ on qubits 3 to 7 takes five different values: the inputs $000, 001, 010, 100$ share the value $0$, and $011, 101, 110, 111$ each have their own. Start with the input in the uniform superposition and the output in $|0\rangle$.

- *With uncomputation* ($7 + 1 + 7 = 15$ gates), the input and the output form the pure state $\frac{1}{\sqrt8}\sum_x |x\rangle|\mathrm{maj}(x)\rangle$, with purity $\mathrm{Tr}\,\rho^2 = 1$.
- *Without* L3, the state of input and output is a mixture over the five garbage values with weights $\frac12, \frac18, \frac18, \frac18, \frac18$. Its purity is $\frac14 + 4 \cdot \frac{1}{64} = \frac{5}{16}$.

Now put the output in $|{-}\rangle$, apply the oracle, then $H$ on each input qubit, and measure the input. The majority function is balanced, so with uncomputation the amplitude of $000$ is $\frac18\sum_x (-1)^{\mathrm{maj}(x)} = 0$, as in the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/). Without L3, only terms with the same garbage value can cancel. The four inputs with garbage $0$ add up to amplitude $\frac12$ and the other four give $\frac18$ each, so $000$ has probability $\frac14 + \frac{4}{64} = \frac{5}{16}$.

## Classic examples

- **The oracle of [Grover search](/grover-search/) for satisfiability.** A reversible circuit for a formula $\varphi$ maps $|i, 0, 0\rangle$ to $|i, \varphi(i), w_i\rangle$. A $Z$ gate on the result and the inverse circuit give the phase oracle $|i\rangle \mapsto (-1)^{\varphi(i)}|i\rangle$ that Grover search needs (de Wolf, Section 7.4).
- **Multi-controlled gates with clean ancillas.** The V-chain on the [ancilla qubits](/ancilla-qubits/) page computes the AND of $k - 1$ controls into ancillas, uses it once, and uncomputes it, so $2k - 3$ Toffoli gates give $C^kX$.
- **Modular multiplication in [quantum modular exponentiation](/quantum-modular-exponentiation/).** To map $|x\rangle$ to $|ax \bmod N\rangle$ in place, compute $|x\rangle|ax \bmod N\rangle$ and swap the registers to get $|ax \bmod N\rangle|x\rangle$. Then subtract $a^{-1} \cdot (ax) \bmod N$ from the second register, with a circuit for multiplication by $a^{-1} \bmod N$. The second register ends at $0$. This works because $x$ can be computed from the result, not because the circuit is run backward on the same data.
- **Linear combinations of unitaries.** A [linear combination of unitaries](/linear-combination-of-unitaries/) prepares a state on an ancilla register, applies the controlled unitaries, and then applies the inverse of the preparation step. This is the same pattern with a quantum state in place of a classical value.

## Variations

- **Pebbling (Bennett 1989).** Uncompute intermediate states in stages to keep few of them at a time. A chain of $T$ steps then needs about $\log_2 T$ stored states and $T^{\log_2 3}$ steps; see [reversible computation](/reversible-computation/).
- **Uncomputation by measurement.** For a value $a \wedge b$ stored on an ancilla, apply $H$ to the ancilla and measure it. On outcome $0$ the ancilla is already clean. On outcome $1$ the state has the phase $(-1)^{ab}$, which a CZ gate on $a$ and $b$ removes, and an $X$ gate resets the ancilla. Gidney (2018) uses this to compute an AND with four T gates and to remove it with none.
- **Lazy uncomputation.** When the same $C$ is called twice in a row, the $C^{-1}$ of the first call and the $C$ of the second call cancel, so both can be left out.
- **Approximate computation.** Suppose $C|x\rangle|0^s\rangle = |\varphi\rangle$, and the part of $|\varphi\rangle$ with a wrong value of $f(x)$ has squared norm $\varepsilon$. Then the template output is within distance $2\sqrt{\varepsilon}$ of $|x\rangle|0^s\rangle|y \oplus f(x)\rangle$. Compare the state after COPY with the vector $|\varphi\rangle|y \oplus f(x)\rangle$. The two agree on the good part of $|\varphi\rangle$, and on the bad part each has norm $\sqrt\varepsilon$, so their distance is at most $2\sqrt\varepsilon$. The unitary $C^{-1}$ keeps distances, and it maps the second vector to the ideal output. So a bounded-error subroutine can first be amplified to small $\varepsilon$ and then be uncomputed.

## Pitfalls

- **Testing only on basis states.** On each basis state, a circuit with garbage gives the correct output bit. The error shows only on a superposition, as an entangled work register. Test the purity of the result register, or the interference that follows.
- **A copy that writes on a wire of $C$.** If the COPY step changes a qubit that $C$ reads or writes, then $C^{-1}$ no longer undoes $C$. The output register must be outside the wires of $C$.
- **Copying is not cloning.** The CNOT copy makes $\sum_x \alpha_x |x\rangle|x\rangle$, an entangled state, not two copies of $\sum_x \alpha_x|x\rangle$. This is why it does not conflict with the [no-cloning theorem](/no-cloning-theorem/), and why it only works for values that are functions of the basis state.
- **A measurement between L1 and L3.** A measurement of the work register in the middle collapses the superposition, and L3 cannot undo it.
- **Wrong inverse.** $C^{-1}$ reverses the order of the gates and inverts each gate: $T$ becomes $T^\dagger$, $S$ becomes $S^\dagger$. Toffoli, CNOT, $X$, $H$ and $Z$ are their own inverses.

## Exercises

1. (de Wolf, Exercise 2.11.) A phase query maps $|b\rangle$ to $(-1)^{x_b}|b\rangle$ for a 2-bit input $x = x_0x_1$. Show that $H O H|0\rangle$ gives $0$ with probability $1$ when $x_0 = x_1$ and $0$ when $x_0 \ne x_1$. Then let the query leave workspace, $|b, 0\rangle \mapsto (-1)^{x_b}|b, b\rangle$, and show that the first qubit now gives $0$ with probability $\frac12$ for every $x$.
2. For the OR of two bits written as $a \oplus b \oplus ab$ on one work qubit (two CNOT gates and a Toffoli gate), compute the purity of the input and output registers with and without uncomputation when the input is $|{+}{+}\rangle$.
3. Write out the proof of the $2\sqrt\varepsilon$ bound in the variation on approximate computation.
4. Let $f$ have $m$ output bits, and let the COPY step be a $Z$ gate on each wire of $f(x)$ with index in a set $S$. Show that the template maps $|x\rangle|0^s\rangle$ to $(-1)^{\sum_{j \in S} f_j(x)}|x\rangle|0^s\rangle$.
5. In the measurement-based uncomputation of $a \wedge b$, check both outcomes on the input $\frac12(|00\rangle + |01\rangle + |10\rangle - |11\rangle)$ of $a, b$.

## References
