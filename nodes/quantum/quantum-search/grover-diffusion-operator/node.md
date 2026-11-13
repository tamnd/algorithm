---
tag: MGR1MD
kind: concept
slug: grover-diffusion-operator
name: Grover diffusion operator
aliases:
- inversion about the mean
area: quantum/quantum-search
level: intro
summary: The reflection D = 2|s><s| - I about the uniform superposition. It maps each amplitude a to 2 mean - a, and with the oracle it makes one Grover iteration.
prereqs: [quantum-superposition, hadamard-gate, unitary-operator]
see_also: [grover-search, amplitude-amplification, fixed-point-quantum-search, quantum-counting, quantum-walk-search, walsh-hadamard-transform, quantum-interference]
sources:
  - paper: doi:10.1145/237814.237866
    title: "Lov K. Grover, A fast quantum mechanical algorithm for database search, Proceedings of the 28th Annual ACM Symposium on Theory of Computing (STOC 1996), pages 212-219"
    locator: the diffusion transform D with entries 2/N off the diagonal and -1 + 2/N on it, and its form as W R W
  - paper: doi:10.1103/PhysRevLett.79.325
    title: "Lov K. Grover, Quantum mechanics helps in searching for a needle in a haystack, Physical Review Letters 79(2), 1997, pages 325-328"
    locator: the description of the diffusion step as an inversion about the average
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 6 (the iteration -T S_0 T S_i0, and any T' with T'|0> uniform in place of the Walsh-Hadamard transform)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 6, Section 6.1 (the Grover operator, its circuit and its geometric picture as two reflections)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6
    locator: Chapter 7, Section 7.2 (Grover's algorithm, with the reflection about the uniform state)
---

The Grover diffusion operator is the unitary $D = 2|s\rangle\langle s| - I$ on $N$ basis states, where $|s\rangle = N^{-1/2}\sum_x |x\rangle$ is the uniform superposition. It is the reflection about $|s\rangle$, and on amplitudes it maps each $a_x$ to $2\bar a - a_x$, where $\bar a$ is the mean, so it is also called the inversion about the mean. This page is about this one reflection. [Grover's search algorithm](/grover-search/) applies it after each oracle call, and [amplitude amplification](/amplitude-amplification/) replaces $|s\rangle$ by the output state of any algorithm.

## In plain words

Think of a row of numbers, one for each item. First find their average. Then move each number to the other side of the average, at the same distance. A number a little above the average goes to a little below it. A number far below the average goes far above it.

In a search, the oracle first turns the number of each good item negative. The good items are then far below the average. The diffusion step moves them far above it, and it moves the other numbers a little down. So each round makes the good items stand out more. The step only moves weight between the items. It never asks the oracle anything.

## The idea

**As a reflection.** For a unit vector $|s\rangle$, the operator $2|s\rangle\langle s| - I$ keeps $|s\rangle$ fixed and multiplies each vector orthogonal to $|s\rangle$ by $-1$. So it is the reflection about the line through $|s\rangle$. It is unitary and Hermitian, $D^2 = I$, and it has the eigenvalue $+1$ once (on $|s\rangle$) and $-1$ with multiplicity $N - 1$.

**As an inversion about the mean.** Let $|\psi\rangle = \sum_x a_x |x\rangle$. Then $\langle s|\psi\rangle = N^{-1/2}\sum_x a_x = \sqrt{N}\,\bar a$, so

$$D|\psi\rangle = 2\sqrt{N}\,\bar a\,|s\rangle - |\psi\rangle = \sum_x (2\bar a - a_x)\,|x\rangle.$$

As a matrix, $D$ has $2/N$ off the diagonal and $-1 + 2/N$ on the diagonal. This is the form in Grover's 1996 paper.

**As a circuit.** For $N = 2^n$, $|s\rangle = H^{\otimes n}|0\rangle$, so

$$D = H^{\otimes n}\,(2|0\rangle\langle 0| - I)\,H^{\otimes n}.$$

The middle operator puts the phase $-1$ on each basis state except $|0\rangle$. Up to a global phase $-1$, it is $X^{\otimes n}$, then a $Z$ gate on one qubit with the other $n - 1$ qubits as controls, then $X^{\otimes n}$. The controlled $Z$ needs $O(n)$ Toffoli and one-qubit gates with $n - 2$ clean ancillas. So $D$ costs $O(n) = O(\log N)$ gates. It makes no oracle query. The $H$ layers are the [Walsh-Hadamard transform](/walsh-hadamard-transform/) of the state.

**For other start states.** If $A$ is any unitary with $A|0\rangle = |s\rangle$, then $D = A(2|0\rangle\langle 0| - I)A^\dagger$. This works for any $N$, not only a power of two. With a general $A$ the same formula gives the reflection about $A|0\rangle$, which is the step of [amplitude amplification](/amplitude-amplification/).

**With the oracle.** Let $O$ be the phase oracle, which multiplies the marked items by $-1$. In the plane of the marked and the unmarked superpositions, $O$ is a reflection and $D$ is a reflection, and the axes are at an angle $\theta$ with $\sin\theta = \sqrt{M/N}$. The product $G = D\,O$ is a rotation by $2\theta$. This is the Grover iteration, and its eigenvalues on that plane are $e^{\pm 2i\theta}$.

**Signs.** Some texts write $I - 2|s\rangle\langle s| = -D$. This changes only a global phase, so all probabilities stay the same. A version with a phase other than $-1$, $I - (1 - e^{i\alpha})|s\rangle\langle s|$, is not a reflection. [Fixed-point quantum search](/fixed-point-quantum-search/) uses such phases on purpose.

## Examples

**Two qubits.** For $N = 4$, $D$ has $-1/2$ on the diagonal and $1/2$ elsewhere. Let the marked item be $x = 2$. Start with $|s\rangle$, all amplitudes $1/2$. The oracle gives $(1/2, 1/2, -1/2, 1/2)$. The mean is $1/4$. The inversion gives $(2 \cdot 1/4 - 1/2, \ldots) = (0, 0, 1, 0)$. One iteration finds the marked item with certainty. In general, one iteration is exact when $M = N/4$, because then $\theta = \pi/6$ and $3\theta = \pi/2$.

**A row of amplitudes.** The real amplitudes $(0.5, 0.1, 0.3, 0.1)$ have the mean $0.25$. The inversion gives $(0, 0.4, 0.2, 0.4)$. The sum of the squares is $0.36$ before and $0.36$ after, as for each unitary map. (These four numbers are not a unit vector, but $D$ is linear, so the example scales.)

**Eight items.** For $N = 8$ and one marked item, after the first oracle call the amplitudes are $-0.3536$ (marked) and $0.3536$ (the other 7). The mean is $0.2652$. The inversion gives $0.8839$ to the marked item and $0.1768$ to each other. The probability of the marked item goes from $1/8$ to $25/32$.

**The circuit on one qubit.** For $n = 1$, $2|0\rangle\langle 0| - I = Z$, and $D = HZH = X$. With $N = 2$ and one marked item, $\theta = \pi/4$, and $G|s\rangle = (|g\rangle - |b\rangle)/\sqrt{2}$, where $|g\rangle$ is the marked item and $|b\rangle$ the other: the probability stays $1/2$. Search on two items gains nothing.

## Where it is used

- [Grover's search algorithm](/grover-search/): one diffusion after each oracle call.
- [Amplitude amplification](/amplitude-amplification/): the reflection about $A|0\rangle$ for a general algorithm $A$.
- [BBHT search](/bbht-search/), [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/) and [Grover adaptive search](/grover-adaptive-search/): the same iteration with other oracles.
- [Quantum counting](/quantum-counting/): [phase estimation](/quantum-phase-estimation/) of $G = D\,O$ reads off $\theta$ from the eigenvalues $e^{\pm 2i\theta}$.
- [Fixed-point quantum search](/fixed-point-quantum-search/): a version of $D$ with a general phase.
- [Quantum walk search](/quantum-walk-search/): a step of a Szegedy walk is also a product of two reflections, and the diffusion on the coin space of a coined walk is $2|s\rangle\langle s| - I$ on the neighbors of a vertex.

The diffusion operator alone does nothing useful: on $|s\rangle$ it is the identity. The gain comes from its [interference](/quantum-interference/) with the oracle.

## References
