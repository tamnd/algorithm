---
tag: 2ZD3YZ
kind: technique
slug: phase-kickback
name: Phase kickback
aliases:
- kickback
- phase kick-back
area: quantum/quantum-primitives
level: intro
summary: "When a controlled-U gate acts on an eigenvector of U, the eigenvalue becomes a relative phase on the control qubit and the target does not change. Oracles use it to write f(x) into a phase."
prereqs: [quantum-oracle, hadamard-gate, cnot-gate]
see_also: [hadamard-test, quantum-phase-estimation, deutsch-jozsa-algorithm, bernstein-vazirani-algorithm, grover-search, uncomputation, ancilla-qubits, unitary-operator]
sources:
  - paper: doi:10.1098/rspa.1998.0164
    title: "Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca, Quantum algorithms revisited, Proceedings of the Royal Society of London A 454(1969):339-354, 1998"
    locator: the target qubit in the state |0> - |1>, the eigenvalue written on the control, and the one-query forms of the Deutsch and Deutsch-Jozsa algorithms
  - paper: doi:10.1098/rspa.1992.0167
    title: "David Deutsch and Richard Jozsa, Rapid solution of problems by quantum computation, Proceedings of the Royal Society of London A 439(1907):553-558, 1992"
    locator: the constant or balanced problem, solved there with two queries
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, lecture notes
    locator: "Section 2.4 (the phase kick-back trick: a standard query with the target in |-> gives a phase query)"
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 1.4.3 (Deutsch's algorithm with the target in |0> - |1>) and Section 5.2 (phase estimation with controlled U^(2^j) on an eigenvector)"
---

*Phase kickback* is the effect of a controlled-$U$ gate whose target holds an eigenvector $|u\rangle$ of $U$ with eigenvalue $e^{i\varphi}$: the target does not change, and the control qubit gets the relative phase $e^{i\varphi}$ on its $|1\rangle$ part. A gate that looks as if it changes only the target thus changes only the control. With the bit [oracle](/quantum-oracle/) $U_f$ and the target in $|{-}\rangle$, this turns $|x\rangle|{-}\rangle$ into $(-1)^{f(x)}|x\rangle|{-}\rangle$, the step behind the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/), [Grover search](/grover-search/) and [quantum phase estimation](/quantum-phase-estimation/).

## In plain words

A controlled gate seems to have a direction: one wire decides, and the other wire is changed. In quantum circuits this is not the whole story. Some states of the target wire are not changed by the gate at all, except for a factor that has no effect on the target alone.

If the target holds such a state, the factor still appears, and it appears on the part of the state where the control is on. So the control wire picks up a phase. The target wire stays exactly as it was and can be used again. A later gate on the control turns this phase into something a measurement can see.

An oracle uses this trick to put the answer to a yes or no question into a sign.

## When it applies

- A controlled unitary $C\text{-}U = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes U$ is available, with the control first.
- The target register can be prepared in an eigenvector $|u\rangle$ of $U$, or the input is promised to be one. For the bit oracle on one output qubit, $|{-}\rangle$ is an eigenvector of $X^{f(x)}$ with eigenvalue $(-1)^{f(x)}$ for each $x$.
- The algorithm needs the eigenvalue as a phase: to make terms interfere, or to read the phase out with a Hadamard gate or an inverse [quantum Fourier transform](/quantum-fourier-transform/).

## The template

```pseudo id=main
PHASE-KICKBACK(U, |u⟩, α|0⟩ + β|1⟩)
L1  prepare the target in |u⟩               ▷ hole: an eigenvector, U|u⟩ = e^(iφ)|u⟩
L2  prepare the control in α|0⟩ + β|1⟩       ▷ hole: often |+⟩, or a register of controls
L3  apply controlled-U
L4  the state is (α|0⟩ + e^(iφ) β|1⟩) ⊗ |u⟩  ▷ the target is unchanged
L5  apply H to the control and measure       ▷ hole: the readout, or more gates
```

**Why it works.** By linearity, $C\text{-}U\,(\alpha|0\rangle + \beta|1\rangle)|u\rangle = \alpha|0\rangle|u\rangle + \beta|1\rangle U|u\rangle = \alpha|0\rangle|u\rangle + \beta e^{i\varphi}|1\rangle|u\rangle = (\alpha|0\rangle + e^{i\varphi}\beta|1\rangle)|u\rangle$. The result is a product state, so the control is not entangled with the target. The factor $e^{i\varphi}$ is a global phase for $U|u\rangle$ alone, but it is a relative phase between the two parts of the control.

**The readout.** With $\alpha = \beta = 1/\sqrt2$ and $H$ on the control, the amplitudes are $(1 + e^{i\varphi})/2$ for $0$ and $(1 - e^{i\varphi})/2$ for $1$. So the control reads $1$ with probability $|1 - e^{i\varphi}|^2/4 = (1 - \cos\varphi)/2 = \sin^2(\varphi/2)$. For $\varphi \in \{0, \pi\}$ the readout is exact.

**The oracle form.** For the bit oracle $U_f|x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle$ the control is the whole register $|x\rangle$, and on the branch $|x\rangle$ the target gets $X^{f(x)}$. Since $X|{-}\rangle = -|{-}\rangle$,

$$U_f\,|x\rangle|{-}\rangle = |x\rangle \frac{|f(x)\rangle - |1 \oplus f(x)\rangle}{\sqrt2} = (-1)^{f(x)}|x\rangle|{-}\rangle.$$

By linearity $U_f\bigl(\sum_x \alpha_x|x\rangle\bigr)|{-}\rangle = \bigl(\sum_x (-1)^{f(x)}\alpha_x|x\rangle\bigr)|{-}\rangle$, which is one query to the phase oracle $O_f$, and the ancilla stays $|{-}\rangle$.

**Example: the CNOT gate.** $|{-}\rangle$ is an eigenvector of $X$ with eigenvalue $-1$. So $\mathrm{CNOT}\,|{+}\rangle|{-}\rangle = |{-}\rangle|{-}\rangle$ and $\mathrm{CNOT}\,|{-}\rangle|{-}\rangle = |{+}\rangle|{-}\rangle$, with the control on the left. The target $|{+}\rangle$ has eigenvalue $1$, so $\mathrm{CNOT}\,|{+}\rangle|{+}\rangle = |{+}\rangle|{+}\rangle$. In the Hadamard basis the roles of control and target swap: $(H \otimes H)\,\mathrm{CNOT}\,(H \otimes H)$ is the CNOT gate with control and target exchanged.

**Example: a phase gate.** Let $U = S = \mathrm{diag}(1, i)$ and $|u\rangle = |1\rangle$, with eigenvalue $i$. The control $|{+}\rangle$ becomes $(|0\rangle + i|1\rangle)/\sqrt2$, and after $H$ it reads $1$ with probability $\sin^2(\pi/4) = \frac12$. For $U = T$ the probability is $\sin^2(\pi/8) \approx 0.1464$.

## Classic examples

- **Deutsch's problem.** Prepare $|{+}\rangle|{-}\rangle$, apply $U_f$ once, apply $H$ to the first qubit and measure. The first qubit is $\pm|{+}\rangle$ when $f(0) = f(1)$ and $\pm|{-}\rangle$ when $f(0) \ne f(1)$, so the outcome is $f(0) \oplus f(1)$ with certainty. Cleve, Ekert, Macchiavello and Mosca (1998) gave this one-query form.
- **Deutsch-Jozsa and Bernstein-Vazirani.** The same step with a register of $n$ controls writes $(-1)^{f(x)}$ on every $|x\rangle$ of the uniform superposition. Then $H^{\otimes n}$ decides constant or balanced in the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/), and it gives the hidden string $s$ of $f(x) = s \cdot x$ in the [Bernstein-Vazirani algorithm](/bernstein-vazirani-algorithm/). Deutsch and Jozsa (1992) used two queries, and phase kickback brings this to one.
- **Grover search.** The oracle step of [Grover search](/grover-search/) is $U_f$ with the output qubit in $|{-}\rangle$, which flips the sign of the marked items.
- **Phase estimation.** [Quantum phase estimation](/quantum-phase-estimation/) applies controlled-$U^{2^j}$ from control qubit $j$ to an eigenvector of $U$. Each control gets the phase $e^{i 2^j \varphi}$, and an inverse quantum Fourier transform reads $\varphi$ from all of them.
- **The Hadamard test.** The [Hadamard test](/hadamard-test/) is the template with a target that need not be an eigenvector, and it estimates $\mathrm{Re}\langle\psi|U|\psi\rangle$.

## Variations

- **A target register.** The target can be many qubits, and $U$ any unitary on them. For example $X \otimes Z$ has the eigenvector $|{-}\rangle|1\rangle$ with eigenvalue $(-1)(-1) = 1$, and $|{-}\rangle|0\rangle$ with eigenvalue $-1$.
- **Multi-bit oracles.** For $U_f$ with $m$ output bits, put the output register in $H^{\otimes m}|z\rangle$. This is an eigenvector of each $X^{f(x)}$ with eigenvalue $(-1)^{z \cdot f(x)}$, so one query gives $|x\rangle \mapsto (-1)^{z \cdot f(x)}|x\rangle$.
- **Modular addition.** For an oracle $|x\rangle|y\rangle \mapsto |x\rangle|y + f(x) \bmod N\rangle$, the Fourier state $\frac{1}{\sqrt N}\sum_y e^{-2\pi i k y/N}|y\rangle$ is an eigenvector with eigenvalue $e^{2\pi i k f(x)/N}$. This is how arithmetic in the Fourier basis puts a value into a phase.
- **Powers of $U$.** Controlled-$U^k$ kicks back $e^{ik\varphi}$. This is the step that phase estimation repeats with $k = 1, 2, 4, \ldots$

## Pitfalls

- **A target that is not an eigenvector.** Then the control and the target become entangled, and the control is mixed. For example $\mathrm{CNOT}\,|{+}\rangle|0\rangle$ is the Bell state $\frac{1}{\sqrt2}(|00\rangle + |11\rangle)$, and the control alone has purity $\frac12$. For a superposition of eigenvectors with different eigenvalues, the phase depends on the branch.
- **The global phase of $U$ matters once $U$ is controlled.** The gates $U$ and $e^{i\alpha}U$ are the same gate, but controlled-$(e^{i\alpha}U)$ equals controlled-$U$ followed by $\mathrm{diag}(1, e^{i\alpha})$ on the control. A circuit for controlled-$U$ must get this phase right.
- **The uncontrolled phase oracle loses information.** $O_f$ and $O_{1-f} = -O_f$ cannot be told apart, so the phase form is enough for Deutsch-Jozsa and Grover but not for every use of $U_f$; see the [quantum oracle](/quantum-oracle/) page.
- **The ancilla must be exactly $|{-}\rangle$.** With the ancilla in $|0\rangle$ the oracle writes $f(x)$ into the ancilla instead of into a phase, and the input register becomes entangled with it.
- **Nothing travels backward.** The phase is a property of the joint state. It can be read on the control only because the joint state is a product state.

## Exercises

1. Show with phase kickback that $(H \otimes H)\,\mathrm{CNOT}\,(H \otimes H)$ is the CNOT gate with control and target exchanged.
2. Let $U = R_y(\theta)$. Find its eigenvectors and eigenvalues, and give the probability of reading $1$ in the template.
3. Show that with one query to $U_f$ and the output qubit in $|{-}\rangle$, the Bernstein-Vazirani algorithm finds $s$ with certainty.
4. Show that controlled-$(e^{i\alpha}I)$ equals the phase gate $\mathrm{diag}(1, e^{i\alpha})$ on the control.
5. For $U_f$ with the output qubit in $\cos\theta|0\rangle + \sin\theta|1\rangle$ and the input $|{+}\rangle$ for a balanced $f$ on one bit, compute the purity of the input qubit after the query. For which $\theta$ is it $1$?

## References
