---
tag: CKPRB9
kind: model
slug: quantum-turing-machine
name: Quantum Turing machine
aliases:
- QTM
area: quantum/quantum-primitives
level: advanced
summary: "A Turing machine whose configuration is a superposition and whose step is unitary. It computes the same functions as a Turing machine and is polynomially equivalent to uniform quantum circuits."
prereqs: [turing-machine, probabilistic-turing-machine, quantum-circuit-model]
see_also: [bqp, universal-turing-machine, church-turing-thesis, oracle-turing-machine, relativization, multitape-turing-machine, reversible-computation, pspace]
sources:
  - paper: doi:10.1098/rspa.1985.0070
    title: "David Deutsch, Quantum theory, the Church-Turing principle and the universal quantum computer, Proceedings of the Royal Society of London A 400(1818):97-117, 1985"
    locator: "the first definition of a quantum Turing machine and of a universal quantum computer, and the Church-Turing principle (general locator)"
  - paper: doi:10.1137/S0097539796300921
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, SIAM Journal on Computing 26(5):1411-1473, 1997"
    locator: "well-formed machines, efficiently computable amplitudes, machines in which all branches halt at the same time, the efficient universal quantum Turing machine, and an oracle relative to which BQP is not in BPP (general locator)"
  - paper: doi:10.1109/SFCS.1993.366852
    title: "Andrew Chi-Chih Yao, Quantum circuit complexity, Proceedings of the 34th Annual IEEE Symposium on Foundations of Computer Science, pages 352-361, 1993"
    locator: t steps of a quantum Turing machine simulated by a uniform family of quantum circuits of size quadratic in t, and the converse simulation in polynomial time
  - paper: doi:10.1016/S0304-3975(01)00111-6
    title: "Harumichi Nishimura and Masanao Ozawa, Computational complexity of uniform quantum circuit families and quantum Turing machines, Theoretical Computer Science 276(1-2):147-181, 2002"
    locator: "the equivalence of quantum Turing machines and uniform quantum circuit families, with a precise notion of uniformity (general locator)"
  - paper: doi:10.1098/rspa.2018.0767
    title: "Abel Molina and John Watrous, Revisiting the simulation of quantum Turing machines by quantum circuits, Proceedings of the Royal Society A 475(2226):20180767, 2019"
    locator: Yao's simulation revisited, with circuits of depth linear in t, and its extension to machines with multi-dimensional tapes
  - paper: doi:10.1137/S0097539795293639
    title: "Leonard M. Adleman, Jonathan DeMarrais and Ming-Deh A. Huang, Quantum computability, SIAM Journal on Computing 26(5):1524-1540, 1997"
    locator: "the dependence of the classes on the allowed amplitudes, and BQP ⊆ PP for algebraic amplitudes (general locator)"
  - paper: arxiv:0804.3401
    title: John Watrous, Quantum computational complexity, Encyclopedia of Complexity and Systems Science, Springer, 2009
    locator: "Section VII.2 (space-bounded quantum computation, the hybrid quantum Turing machine of Figure 13, and Theorem 18 with BQPSPACE = PSPACE)"
---

A *quantum Turing machine* (QTM) is a [Turing machine](/turing-machine/) whose configuration is a [superposition](/quantum-superposition/) of classical configurations, and whose transition function gives a complex amplitude to each possible move, so that one step is a [unitary](/unitary-operator/) operator on the space of configurations. Deutsch (1985) defined it, and Bernstein and Vazirani (1997) gave the form used in complexity theory, with an efficient [universal machine](/universal-turing-machine/). A QTM computes the same functions as a Turing machine, so quantum computing does not change the [Church-Turing thesis](/church-turing-thesis/); the questions are about time and space. Yao (1993) showed that QTMs and uniform families of [quantum circuits](/quantum-circuit-model/) simulate each other with polynomial overhead, so most work now uses circuits.

## The machine

**Parts.** A QTM has a finite set of states $Q$ with a start state $q_0$ and a final state $q_f$, a tape alphabet $\Sigma$ with a blank, one two-way infinite tape and one head. A *configuration* $c$ is the state, the tape contents (finitely many nonblank cells) and the head position.

**Transitions.** The transition function is $\delta\colon Q \times \Sigma \times \Sigma \times Q \times \{L, R\} \to \mathbb C$. The number $\delta(p, \sigma, \tau, q, d)$ is the amplitude that the machine in state $p$, reading $\sigma$, writes $\tau$, enters $q$ and moves in direction $d$. Bernstein and Vazirani allow only efficiently computable amplitudes: the first $k$ bits of each one must be computable in time polynomial in $k$.

**One step.** The state of the machine is a unit vector $\sum_c \alpha_c|c\rangle$ in the Hilbert space with one basis vector per configuration. The time evolution $U_\delta$ maps each $|c\rangle$ to the sum of the configurations that $\delta$ allows from $c$, with their amplitudes, and extends linearly. The machine is *well formed* if $U_\delta$ is unitary. This is a condition on infinitely many configurations, and a transition function can give every configuration an image of unit length and still fail it, because the images of two configurations overlap. Bernstein and Vazirani reduce it to finitely many local conditions on $\delta$, which compare only configurations that differ near the head.

**Halting and output.** If branches halt at different times, observing whether the machine has halted disturbs the branches that have not. Bernstein and Vazirani therefore use machines in which every branch on an input of length $n$ enters $q_f$ at the same step, with the head on the start cell. Then the output cell is measured, and the result is $1$ with the probability given by the [Born rule](/born-rule/).

**Example: a Hadamard machine.** Let $Q = \{p\}$ and $\Sigma = \{0, 1\}$, ignoring the blank, and let $\delta(p, \sigma, \tau, p, R) = (-1)^{\sigma\tau}/\sqrt2$ for all $\sigma, \tau$. Each step applies the [Hadamard gate](/hadamard-gate/) to the scanned cell and moves right. Two configurations that differ only in the scanned cell are mapped to orthogonal vectors, because $H$ is unitary. Two configurations that differ anywhere else, or in the head position, are mapped to vectors with disjoint supports. So $U_\delta$ is unitary, and $n$ steps on $0^n$ give the uniform superposition of all strings of length $n$ to the left of the head.

**Non-example: an eraser.** Let $\delta(p, \sigma, 0, p, R) = 1$ for $\sigma \in \{0, 1\}$: write $0$ and move right. Two configurations that differ only in the scanned cell are mapped to the same configuration, so $U_\delta$ is not injective and the machine is not well formed. Every QTM is reversible, and a computation that erases must keep a record, as in [reversible computation](/reversible-computation/).

## What it counts

- **Time**: the number of steps until all branches halt.
- **Space**: the number of tape cells that the head visits in any branch.
- **Error**: the probability of a wrong output. BQP is the class of languages that a QTM with efficiently computable amplitudes decides in polynomial time with error at most $\frac13$ on every input, and EQP is the same with error $0$.
- **Queries**: an oracle QTM has a query tape and a query state, and one query applies the unitary $|x\rangle|b\rangle \mapsto |x\rangle|b \oplus A(x)\rangle$ to the query tape, as for an [oracle Turing machine](/oracle-turing-machine/) with a [quantum oracle](/quantum-oracle/).

For space bounds Watrous uses a different machine: a classical Turing machine with a read-only input tape and a classical work tape, plus a tape of qubits on which it applies Toffoli, Hadamard and phase gates and one-qubit measurements. In that model BQL and BQPSPACE are defined, and $\mathrm{BQPSPACE} = \mathrm{PSPACE}$ (Watrous, Section VII.2).

## Relation to other models

- **Turing machines.** A reversible Turing machine is a QTM whose amplitudes are $0$ and $1$. Every Turing machine has a reversible simulation, so a QTM simulates a Turing machine with polynomial overhead. Conversely, a Turing machine simulates a QTM by computing the amplitudes, in exponential time, so both compute the same functions.
- **Probabilistic Turing machines.** A [probabilistic Turing machine](/probabilistic-turing-machine/) gives each move a probability and evolves a probability vector. A QTM gives each move an amplitude, and amplitudes can cancel ([quantum interference](/quantum-interference/)). A QTM simulates a fair coin with a Hadamard step on a fresh cell, so $\mathrm{BPP} \subseteq \mathrm{BQP}$.
- **Nondeterministic Turing machines.** A [nondeterministic Turing machine](/nondeterministic-turing-machine/) accepts if one branch accepts. A QTM is not of this kind: it accepts with a probability that depends on all branches together, and branches can cancel.
- **Multitape and multitrack machines.** Bernstein and Vazirani use one tape with several tracks, which costs the same as several tapes up to polynomial factors, as for a [multitape Turing machine](/multitape-turing-machine/). Molina and Watrous (2019) also treat machines with multi-dimensional tapes.
- **Quantum circuits.** Yao (1993) simulates $t \ge n$ steps of a QTM by a uniform family of circuits of size $O(t^2)$, and a QTM simulates a polynomial-time uniform family in polynomial time. Nishimura and Ozawa (2002) give a precise notion of uniformity for this equivalence. Molina and Watrous (2019) reduce the depth of the circuits to $O(t)$.
- **Oracles.** With a quantum oracle, results [relativize](/relativization/) or not as in the classical case. Relative to some oracle BQP is not contained in BPP (Bernstein and Vazirani, by recursive Fourier sampling), and relative to another, NP is not contained in BQP (Bennett, Bernstein, Brassard and Vazirani, 1997).

## Known results in the model

- **An efficient universal QTM.** Bernstein and Vazirani (1997) construct one QTM that, given the description of a well-formed QTM $M$, an input $x$, a number of steps $t$ and an accuracy $\varepsilon$, simulates $t$ steps of $M$ on $x$ to accuracy $\varepsilon$ with polynomial slowdown. This is the quantum form of the [universal Turing machine](/universal-turing-machine/).
- **Upper bounds.** $\mathrm{BQP} \subseteq \mathrm{PSPACE}$ (Bernstein and Vazirani, 1997), by summing amplitudes over paths one at a time. $\mathrm{BQP} \subseteq \mathrm{PP}$ for algebraic amplitudes (Adleman, DeMarrais and Huang, 1997).
- **The amplitudes matter.** If any complex amplitudes are allowed, an amplitude can encode the bits of an uncomputable real number, and polynomial-time QTMs decide uncountably many languages, so some of them are undecidable (Adleman, DeMarrais and Huang, 1997). With efficiently computable or algebraic amplitudes this does not happen.
- **Efficiency and the extended thesis.** Factoring is in BQP ([factoring in BQP](/factoring-in-bqp/)) and is not known to be in BPP. If it is not in BPP, the extended Church-Turing thesis, which says that every reasonable model is simulated by a probabilistic Turing machine with polynomial overhead, is false. Deutsch (1985) stated a physical form of the thesis, the Church-Turing principle, and proposed the QTM as the machine that satisfies it.
- **Space.** In the hybrid model of Watrous, $\mathrm{BQL} \subseteq \mathrm{PL}$ and $\mathrm{BQPSPACE} = \mathrm{PSPACE}$, so quantum space gives no large gain (Watrous, Section VII.2, Theorem 18).

## References
