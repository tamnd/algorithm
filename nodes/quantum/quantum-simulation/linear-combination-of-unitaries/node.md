---
tag: XGJBQG
kind: technique
slug: linear-combination-of-unitaries
name: Linear combination of unitaries
aliases:
- LCU
- LCU technique
area: quantum/quantum-simulation
level: advanced
summary: "Apply V = sum_j beta_j U_j to a state: prepare the weights on an index register, apply U_j controlled on j, unprepare, and amplify the success branch obliviously."
prereqs: [hamiltonian-simulation, ancilla-qubits, amplitude-amplification]
see_also: [block-encoding, truncated-taylor-series-simulation, multi-product-formulas, interaction-picture-simulation, qubitization, grover-search, fixed-point-quantum-search, hadamard-test]
sources:
  - paper: arxiv:1202.5822
    title: "Andrew M. Childs and Nathan Wiebe, Hamiltonian simulation using linear combinations of unitary operations, Quantum Information and Computation 12(11-12), 2012, pages 901 to 924"
    locator: "Section III, Theorem 3 (the success probability of a linear combination of unitaries) and Lemma 2 (nearby unitaries); Section IV (multi-product formulas)"
  - paper: doi:10.1145/2591796.2591854
    title: "Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari and Rolando D. Somma, Exponential improvement in precision for simulating sparse Hamiltonians, Proceedings of the 46th ACM STOC, 2014, pages 283 to 292 (arXiv:1312.1414)"
    locator: "Section 3: Lemma 3.6 (oblivious amplitude amplification) and Lemma 3.7 (the two-dimensional invariant subspace)"
  - paper: doi:10.1103/PhysRevLett.114.090502
    title: "Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari and Rolando D. Somma, Simulating Hamiltonian dynamics with a truncated Taylor series, Physical Review Letters 114(9), 2015, article 090502 (arXiv:1412.4687)"
    locator: "the operator W, equations (13) and (14) (one round of amplification on a block that is close to unitary)"
  - paper: doi:10.1145/3313276.3316366
    title: "András Gilyén, Yuan Su, Guang Hao Low and Nathan Wiebe, Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics, Proceedings of the 51st ACM STOC, 2019, pages 193 to 204 (arXiv:1806.01838)"
    locator: "numbering of arXiv v1: Theorem 28 (robust oblivious amplitude amplification) and Lemma 52 (linear combinations of block encodings)"
  - paper: arxiv:cs/0506068
    title: "Chris Marriott and John Watrous, Quantum Arthur-Merlin games, Computational Complexity 14(2), 2005, pages 122 to 152"
    locator: "the amplification of a two-outcome procedure by alternating two reflections, which motivates Lemma 3.6 of Berry, Childs, Cleve, Kothari and Somma"
---

A *linear combination of unitaries* (LCU) applies an operator of the form
$$V = \sum_{j=0}^{m-1} \beta_j U_j, \qquad \beta_j > 0,$$
to a quantum state, where each $U_j$ is a unitary with a known circuit. The sum $V$ is usually not unitary, and when it is, it usually has no short circuit of its own. LCU puts the weights on an ancilla index register, applies $U_j$ controlled on the index $j$, and undoes the weights. The result is a [block encoding](/block-encoding/) of $V/s$ with $s = \sum_j \beta_j$. When $V$ is unitary, *oblivious amplitude amplification* then raises the chance of success to 1 with $O(s)$ calls, for every input state and without a copy of it. Childs and Wiebe (2012) introduced the method for [Hamiltonian simulation](/hamiltonian-simulation/), and Berry, Childs, Cleve, Kothari and Somma (2014) added the amplification. It is the core of the [truncated Taylor series](/truncated-taylor-series-simulation/), [multi-product formulas](/multi-product-formulas/) and the [interaction picture method](/interaction-picture-simulation/).

## In plain words

Suppose we know how to do a few simple operations, and we want to do a weighted mix of them. A quantum computer cannot just add operations. LCU uses a small helper register that holds a label. First the helper is put into a blend of labels, with more weight on the operations that should count more. Then the operation with each label is done, in all branches at once. Then the blend is undone. If the helper is now back to its start, the main qubits have received the weighted mix. If not, the attempt failed. The chance of success depends only on the total weight, not on the input. Because of this, a second trick can bend the failed part back into the good part, again and again, without looking at the input. With a small extra adjustment, the mix then happens every time.

## When it applies

- The target operator has an expansion $V = \sum_j \beta_j U_j$ with known unitary terms: a [Pauli string decomposition](/pauli-string-decomposition/) of a Hamiltonian, a Taylor or Dyson series of $e^{-iHt}$ whose terms are products of Pauli strings, or a sum of product formulas.
- The 1-norm $s = \sum_j \beta_j$ is small. It sets the cost: one round of the method succeeds with probability $\|V\psi\|^2/s^2$, and amplification needs about $s$ calls.
- There are enough ancilla qubits for the index register, $\lceil \log_2 m \rceil$ of them, and the controlled versions of the $U_j$ are cheap.
- For exact amplification, $V$ is unitary or close to unitary. For a general $V$, use the block encoding directly, as in [qubitization](/qubitization/) or [quantum signal processing](/quantum-signal-processing/).

## The template

The ancilla index register is on the high qubits, so the block $\langle 0|\,\cdot\,|0\rangle$ on the index register is the top-left block of a matrix. $B$ prepares the weights, SELECT applies the terms, and $R$ reflects about the all-zero index.

```pseudo id=main
LCU-OAA(β_0..β_{m-1}, U_0..U_{m-1}, |ψ>, ℓ)
L1  s ← β_0 + ... + β_{m-1}
L2  B ← a unitary on the index register with B|0> = s^{-1/2} Σ_j sqrt(β_j) |j>
L3  φ ← W |0>|ψ>,  W = (B^† ⊗ I) · SELECT · (B ⊗ I),  SELECT = Σ_j |j><j| ⊗ U_j
L4  repeat ℓ times
L5      φ ← -W R W^† R φ,  R = 2|0><0| ⊗ I - I
L6  measure the index register: outcome 0 leaves V|ψ>/‖V|ψ>‖ on the system
```

**Why the block is $V/s$.** With $|b\rangle = B|0\rangle = \sum_j b_j |j\rangle$, $b_j = \sqrt{\beta_j/s}$,
$$(\langle 0| \otimes I)\, W\, (|0\rangle \otimes I) = \sum_j b_j^2\, U_j = \frac{1}{s}\sum_j \beta_j U_j = \frac{V}{s},$$
because SELECT keeps the index, so only the diagonal terms survive. So after L3,
$$W|0\rangle|\psi\rangle = |0\rangle \frac{V}{s}|\psi\rangle + |\Phi^\perp\rangle, \qquad (\langle 0| \otimes I)|\Phi^\perp\rangle = 0.$$

**Why amplification is oblivious.** Let $V$ be unitary. Then $\|V\psi\| = 1$ for every $\psi$, so the good amplitude is $\sin\theta = 1/s$ for every input, and
$$W|0\rangle|\psi\rangle = \sin\theta\, |0\rangle V|\psi\rangle + \cos\theta\, |\Phi^\perp\rangle.$$
Berry, Childs, Cleve, Kothari and Somma (Lemma 3.7) show that $W$, $W^\dagger$ and $R$ keep the plane spanned by $|0\rangle V|\psi\rangle$ and $|\Phi^\perp\rangle$, and that in it $S = -WRW^\dagger R$ is a rotation by $2\theta$. So (Lemma 3.6)
$$S^\ell\, W|0\rangle|\psi\rangle = \sin((2\ell+1)\theta)\, |0\rangle V|\psi\rangle + \cos((2\ell+1)\theta)\, |\Phi^\perp\rangle.$$
This is the rotation of [amplitude amplification](/amplitude-amplification/), but the reflection about the start state is replaced by $W R W^\dagger$. The step needs no copy of $|\psi\rangle$ and no circuit that prepares it, because the angle $\theta$ is the same for every $\psi$. The proof uses only that $(\langle 0| \otimes I)W(|0\rangle \otimes I)$ is a multiple of a unitary, which makes the plane the same for every input. Marriott and Watrous (2005) used the same pair of reflections to amplify the acceptance of a verifier.

**Exact success.** If $(2\ell+1)\theta = \pi/2$, the outcome 0 is certain and the system holds $V|\psi\rangle$ exactly. This needs $s = 1/\sin(\pi/(2(2\ell+1)))$: $s = 1, 2, 3.2361, 4.4940$ for $\ell = 0, 1, 2, 3$. For other $s$, *pad*: add the two terms $+cI$ and $-cI$ with $2c$ equal to the gap. They cancel in $V$, so $V$ does not change, but $s$ grows to the next value in the list. This needs at most one more index qubit.

**Cost.** Each call to $W$ is one call to SELECT, which applies each controlled $U_j$ once, and one call each to $B$ and $B^\dagger$. The method calls $W$ or $W^\dagger$ $2\ell + 1 = O(s)$ times. The index register has $\lceil \log_2 m \rceil$ qubits.

**Example: a rotation.** Take $V = e^{-i(\pi/6)X} = \cos(\pi/6)\, I - i\sin(\pi/6)\, X$, with $\beta = (0.8660, 0.5)$, $U_0 = I$ and $U_1 = -iX$. Then $s = 1.3660$ and $\sin\theta = 1/s = 0.7321$, so one call to $W$ succeeds with probability $1/s^2 = 0.5359$. One round of $S$ overshoots: $\sin^2(3\theta) = 0.3930$, worse than before. Pad to $s = 2$ with $c = 0.3170$ on $+I$ and on $-I$. Now $\theta = \pi/6$, one round gives $\sin^2(\pi/2) = 1$, and the system holds $V|\psi\rangle$ for every $|\psi\rangle$. The code in `impl/python` keeps the joint state as one system vector per index value. Its tests check these numbers, the success probability $\sin^2((2\ell+1)\theta)$ for $\ell = 0$ to 3, and exact output after padding for random unitaries and random inputs.

## Classic examples

- **Hamiltonian simulation by a Taylor series.** $e^{-iHt/r} \approx \sum_{k \le K} (-iHt/r)^k/k!$ with $H = \sum_\ell \alpha_\ell P_\ell$ is a sum of products of Pauli strings with $s \approx e^{\lambda t/r}$. Choosing $r$ so that $s = 2$ needs one round per segment. See [truncated Taylor series simulation](/truncated-taylor-series-simulation/).
- **Multi-product formulas.** A weighted sum $\sum_q C_q S(t/\ell_q)^{\ell_q}$ of [product formulas](/trotter-suzuki-product-formulas/) with different step counts cancels low-order errors, as in [Richardson extrapolation](/richardson-extrapolation/). Some $C_q$ are negative, which goes into SELECT as a sign. See [multi-product formulas](/multi-product-formulas/).
- **Block encodings of Hamiltonians.** With $\beta_j = |c_j|$ and $U_j = \mathrm{sign}(c_j)P_j$, the step L3 alone is the standard [block encoding](/block-encoding/) of $H/\lambda$. [Qubitization](/qubitization/) then uses it without measuring.
- **Dyson series.** In the [interaction picture method](/interaction-picture-simulation/), the terms are time-ordered products of $e^{\pm iAs}$ and Pauli strings, and the index register also holds the times.
- **Linear systems.** Childs, Kothari and Somma (2017) write $1/x$ as a sum of Chebyshev polynomials or of exponentials and implement it as an LCU of quantum walk steps or of $e^{-iAt}$.

## Variations

- **Complex weights.** For $V = \sum_j c_j U_j$ with complex $c_j$, use $\beta_j = |c_j|$ and put the phase $c_j/|c_j|$ into $U_j$, as the code does with Pauli expansions.
- **Nearly unitary sums.** A truncated series is only close to a unitary. Then the block $A$ is close to $V/s$, and one round gives $(\langle 0| \otimes I)(-WRW^\dagger R W)(|0\rangle \otimes I) = 3A - 4AA^\dagger A$ (Berry, Childs, Cleve, Kothari and Somma 2015, equations (13) and (14)). For $s = 2$ and $A = V/2$ this is $V$, and the error stays of the order of $\|A - V/2\|$. Gilyén, Su, Low and Wiebe (Theorem 28) prove a robust version for any number of rounds.
- **Without amplification.** Childs and Wiebe (Theorem 3) repeat the basic circuit until it succeeds. A failed run applies a known wrong operator, so the method needs a way to undo it or a fresh copy of the input. The expected number of tries is $s^2/\|V\psi\|^2$.
- **Sums of block encodings.** If each $U_j$ is itself a block encoding of $A_j$ with normalization $\alpha_j$, the same circuit encodes $\sum_j \beta_j A_j$ with normalization $\sum_j \beta_j\alpha_j$ (Gilyén, Su, Low and Wiebe, Lemma 52).
- **Fixed-point amplification.** If $s$ is not known well enough to pad, the methods of [fixed-point quantum search](/fixed-point-quantum-search/) avoid the overshoot at the cost of a constant factor.

## Pitfalls

- **Overshoot.** Amplification is a rotation. Too many rounds lower the success probability: in the example one round takes it from 0.5359 down to 0.3930. Pick $\ell$ from $s$, and pad $s$ to an exact value.
- **Oblivious only for unitary $V$.** If $V$ is not proportional to a unitary, the good amplitude $\|V\psi\|/s$ depends on $\psi$, and a fixed number of rounds cannot be right for every input. The output after rounds is then a polynomial in the block, not $V$.
- **Signs.** The preparation can only make nonnegative amplitudes $\sqrt{\beta_j/s}$. A negative weight must go into SELECT as $-U_j$. Writing $|\beta_j|$ and forgetting the sign gives a wrong operator with no error message.
- **The 1-norm, not the norm.** The cost depends on $s = \sum_j \beta_j$, which can be much larger than $\|V\|$. Two expansions of the same $V$ can differ greatly in cost. Cancelling terms, as in padding, raise $s$ on purpose. Elsewhere they waste calls.
- **Reflection about the right register.** $R$ reflects about the zero state of the index register only, never about the system. Reflecting about the system state would need a copy of $\psi$, which is what the oblivious method avoids.

## Exercises

1. Show that $(\langle 0| \otimes I)W(|0\rangle \otimes I) = V/s$ does not depend on which unitary $B$ is used, as long as its first column is $(\sqrt{\beta_j/s})_j$.
2. For $V = (I + iX)/\sqrt2$ with $\beta = (1/\sqrt2, 1/\sqrt2)$, compute $s$, the success probability of one call to $W$, and the padding that makes one round of amplification exact.
3. Prove that if $A = (\langle 0| \otimes I)W(|0\rangle \otimes I)$, then one round gives the block $3A - 4AA^\dagger A$. Check that for $A = V/2$ with $V$ unitary the result is $V$.
4. Let $V$ be unitary and let $\sin\theta = 1/s$. Find $\ell$ and the padded $s$ for $s = 2.5$, and the success probability without padding after $\ell$ rounds.
5. Explain why $S = -WRW^\dagger R$ keeps the plane spanned by $|0\rangle V|\psi\rangle$ and $|\Phi^\perp\rangle$. Use that $W^\dagger(|0\rangle V|\psi\rangle) = \sin\theta\,|0\rangle|\psi\rangle + \cos\theta\,|\Psi^\perp\rangle$ for some $|\Psi^\perp\rangle$ with no index-0 part.

## References
