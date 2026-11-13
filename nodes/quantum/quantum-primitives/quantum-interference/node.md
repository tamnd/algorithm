---
tag: V31EB7
kind: concept
slug: quantum-interference
name: Quantum interference
aliases:
- amplitude interference
area: quantum/quantum-primitives
level: intro
summary: "The amplitude of an outcome is a sum over all computation paths that lead to it. The terms are complex, so they can add or cancel, and quantum algorithms make the paths to wrong answers cancel."
prereqs: [quantum-superposition, hadamard-gate]
see_also: [quantum-parallelism, uncomputation, deutsch-jozsa-algorithm, grover-search, quantum-fourier-transform, mixed-state, probabilistic-turing-machine, pp]
sources:
  - paper: doi:10.1137/S0097539795293639
    title: "Leonard M. Adleman, Jonathan DeMarrais and Ming-Deh A. Huang, Quantum computability, SIAM Journal on Computing 26(5):1524-1540, 1997"
    locator: "the proof of BQP ⊆ PP, which writes an acceptance amplitude as a sum over computation paths (general locator)"
  - paper: doi:10.1137/S0097539796300921
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, SIAM Journal on Computing 26(5):1411-1473, 1997"
    locator: "the simulation of a quantum Turing machine in polynomial space, path by path, which gives BQP ⊆ PSPACE (general locator)"
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, lecture notes
    locator: "Section 1.4 (H applied to |+>: the positive and negative amplitudes of |1> cancel, an effect called interference), Section 2.3 (parallelism must be combined with interference) and Section 13.3 (amplitudes as sums over paths, and BQP ⊆ PSPACE)"
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 1.4.3 (Deutsch's algorithm, where the two values of f interfere) and Section 1.4.4 (the Deutsch-Jozsa algorithm)"
---

*Quantum interference* is the effect that the [amplitude](/quantum-state/) of an outcome is a sum over all computation paths that lead to it, and since amplitudes are complex numbers, the terms can add (constructive interference) or cancel (destructive interference). Probabilities are nonnegative and only add, so interference is what a quantum computer has and a [probabilistic Turing machine](/probabilistic-turing-machine/) does not. Every quantum speedup comes from a circuit that makes the paths to wrong answers cancel and the paths to the right answer add. Interference works only between paths that leave no record of which path was taken.

## In plain words

Think of a computation as a set of routes from the start to each possible answer. A random algorithm gives each route a chance, and the chance of an answer is the total over its routes. Totals of chances only grow.

A quantum computer gives each route a weight that can be positive, negative or complex. The weight of an answer is the total over its routes, and the chance of the answer comes from the size of that total. So two routes with opposite weights cancel, and their answer never occurs, even though each route alone would lead there.

A good quantum algorithm is a careful plan of these weights: routes to wrong answers cancel, and routes to the right answer agree. If anything keeps a note of the route, the routes can no longer cancel, and the advantage is gone.

## The idea

**Sum over paths.** Let a circuit apply the gates $U_1, \ldots, U_T$ to the basis state $|x\rangle$. Inserting a sum over basis states between gates gives

$$\langle y|U_T \cdots U_1|x\rangle = \sum_{z_1, \ldots, z_{T-1}} \langle y|U_T|z_{T-1}\rangle \cdots \langle z_2|U_2|z_1\rangle\langle z_1|U_1|x\rangle.$$

Each sequence $x \to z_1 \to \cdots \to y$ is a *path*, and its term is the product of the gate entries along it. The outcome $y$ has probability $|\sum_{\text{paths}} a_p|^2$ by the [Born rule](/born-rule/). For two paths, $|a + b|^2 = |a|^2 + |b|^2 + 2\,\mathrm{Re}(a\bar b)$, and the last term, the *interference term*, can be positive or negative.

**Compared with randomness.** A probabilistic computation is the same sum with stochastic matrices, whose entries are probabilities. Then the probability of $y$ is the sum of the path probabilities, and no term is negative. A quantum circuit has [unitary](/unitary-operator/) gates whose entries can have any phase. The two sums have the same form; the difference is only in the sign or phase of each term.

**Phases decide.** Let a qubit go through $H$, then the phase gate $\mathrm{diag}(1, e^{i\varphi})$, then $H$. Its two paths to the outcome $0$ have the terms $\frac12$ and $\frac12 e^{i\varphi}$, so $P(0) = |1 + e^{i\varphi}|^2/4 = \cos^2(\varphi/2)$. For $\varphi = 0$ the paths to $1$ cancel, and for $\varphi = \pi$ the paths to $0$ cancel. A global phase multiplies every path by the same factor and has no effect; only relative phases between paths matter.

**Which-path information destroys interference.** Paths interfere only if they end in the same basis state of the whole system. If another register records the path, the state has the form $\sum_x \alpha_x|x\rangle|g(x)\rangle$, and terms with different records $g(x)$ end in orthogonal states. Their probabilities then add like classical probabilities. The record can be garbage of a reversible circuit, so the circuit must remove it by [uncomputation](/uncomputation/). It can also be the environment, which turns the state into a [mixed state](/mixed-state/); this is decoherence.

**What this costs a classical simulation.** A classical computer can evaluate the path sum one path at a time in polynomial space, which gives $\mathrm{BQP} \subseteq \mathrm{PSPACE}$ (Bernstein and Vazirani, 1997). With Toffoli and Hadamard gates every nonzero term is $\pm 2^{-h/2}$, for $h$ Hadamard gates, so an amplitude is a difference of two path counts. Adleman, DeMarrais and Huang (1997) used such counts to show $\mathrm{BQP} \subseteq$ [PP](/pp/). The number of paths grows exponentially, and the cancellations between them are why no fast simulation is known.

## Examples

**The gate $HZH$.** The two paths from $|0\rangle$ through $H$, $Z$, $H$ pass $|0\rangle$ or $|1\rangle$ in the middle. To the outcome $1$ they give $\frac{1}{\sqrt2}\cdot 1 \cdot \frac{1}{\sqrt2} = \frac12$ and $\frac{1}{\sqrt2}\cdot(-1)\cdot(-\frac{1}{\sqrt2}) = \frac12$, so the amplitude is $1$. To the outcome $0$ they give $\frac12$ and $-\frac12$, which cancel. So $HZH|0\rangle = |1\rangle$, and indeed $HZH = X$. With $Z$ removed the result is $HH|0\rangle = |0\rangle$, the example on the [superposition](/quantum-superposition/) page.

**A which-path record.** Start from $|0\rangle|0\rangle$, apply $H$ to the first qubit, then a [CNOT gate](/cnot-gate/) to copy it into the second, then $H$ to the first again. The state is $\frac12(|0\rangle + |1\rangle)|0\rangle + \frac12(|0\rangle - |1\rangle)|1\rangle$, and the first qubit reads $0$ or $1$ with probability $\frac12$ each. Without the CNOT it reads $0$ every time. The second qubit has kept a note of the path.

**Deutsch-Jozsa.** After the query with [phase kickback](/phase-kickback/) and Hadamard gates on all $n$ qubits, the amplitude of $|0^n\rangle$ is $2^{-n}\sum_x (-1)^{f(x)}$. Its absolute value is $1$ for a constant $f$, and it is $0$ for a balanced $f$, where the $2^n$ paths cancel in pairs of sign. One measurement decides the [Deutsch-Jozsa problem](/deutsch-jozsa-problem/).

**Grover search with four items.** Let one of $N = 4$ items be marked. The uniform superposition has amplitude $\frac12$ on each item, and the oracle changes the marked one to $-\frac12$. The [diffusion operator](/grover-diffusion-operator/) maps each amplitude $a$ to $2\bar a - a$, where $\bar a = \frac14(3 \cdot \frac12 - \frac12) = \frac14$ is the mean. The marked item gets $2 \cdot \frac14 + \frac12 = 1$ and the others get $2 \cdot \frac14 - \frac12 = 0$. After one query the marked item is found with certainty.

**The Fourier transform.** The [quantum Fourier transform](/quantum-fourier-transform/) of a periodic state with period $r$ gives amplitude only near multiples of $2^n/r$. At other outcomes the phases $e^{2\pi i k y/2^n}$ of the terms are spread around the circle and cancel.

## Where it is used

- Every quantum algorithm with a speedup. The gates after an oracle query, such as Hadamard gates, a diffusion step or a Fourier transform, are there to make paths interfere.
- [Amplitude amplification](/amplitude-amplification/) and [Grover search](/grover-search/), where each round adds amplitude to the marked items by constructive interference.
- [Quantum phase estimation](/quantum-phase-estimation/) and [Shor's algorithm](/shor-algorithm/), where the inverse Fourier transform turns phases into a sharp peak.
- The design of reversible subroutines: garbage left in work qubits is a which-path record, so it must be uncomputed.
- Complexity theory: the path sum gives the upper bounds $\mathrm{BQP} \subseteq \mathrm{PP} \subseteq \mathrm{PSPACE}$ and explains why sign cancellations make quantum circuits hard to simulate.

## References
