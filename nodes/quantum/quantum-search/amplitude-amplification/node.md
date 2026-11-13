---
tag: MTJXHG
kind: technique
slug: amplitude-amplification
name: Amplitude amplification
aliases:
- generalized Grover iteration
area: quantum/quantum-search
level: core
summary: Boost the success probability a of any measurement-free quantum algorithm A to near 1 with O(1/√a) calls of A and its inverse, where repetition needs O(1/a) runs.
prereqs: [grover-search, grover-diffusion-operator, quantum-measurement]
see_also: [grover-search, bbht-search, quantum-counting, fixed-point-quantum-search, durr-hoyer-minimum-finding, brassard-hoyer-tapp-collision, quantum-walk-search, error-amplification]
sources:
  - paper: arxiv:quant-ph/0005055
    title: "Gilles Brassard, Peter Høyer, Michele Mosca and Alain Tapp, Quantum amplitude amplification and estimation, in Quantum Computation and Information, Contemporary Mathematics 305, American Mathematical Society, 2002"
    locator: "arXiv version: Section 2 (Lemma 1, Theorem 2 on floor(pi/(4 theta_a)) iterations, Theorem 3 on QSearch for an unknown a, Theorem 4 and Section 2.1 on exact amplification) and Section 3 (amplitude estimation, Theorem 12)"
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 8, Section 8.2 (amplitude amplification) and Section 8.3 (quantum amplitude estimation and quantum counting)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6
    locator: Chapter 7, Section 7.3 (amplitude amplification)
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 6 (any unitary T' with T'|0> uniform can replace the Walsh-Hadamard transform in the iteration)
---

Amplitude amplification is the technique that turns a quantum algorithm $A$ with success probability $a$ into one that succeeds with probability close to 1, with $O(1/\sqrt{a})$ calls of $A$ and $A^{-1}$. Repeating $A$ and measuring each time needs $\Theta(1/a)$ runs, so the gain is a square root, as in search. [Grover's search algorithm](/grover-search/) is the special case where $A$ prepares the uniform superposition, and the [Grover diffusion operator](/grover-diffusion-operator/) is the special case of its reflection. This page is the general template.

## In plain words

Suppose you have a quantum program that gives a good answer only sometimes, say one time in a hundred. You can check each answer. The simple way is to run the program again and again until you get a good answer. That takes about a hundred runs.

Amplitude amplification does better. It runs the program without looking at the result. Then it marks the good results with a minus sign, runs the program backward, flips one sign, and runs it forward again. Each round turns the state a little toward the good answers. After about ten rounds, one look gives a good answer almost surely. The program must be quantum and must not look at its own result in the middle. Too many rounds turn the state past the good answers, so you must know how many rounds to do, or use a schedule that tries different counts.

## When it applies

You need:

- A quantum algorithm $A$ that uses no measurement, as a unitary: $A|0\rangle = \sqrt{a}\,|\psi_1\rangle + \sqrt{1-a}\,|\psi_0\rangle$, where $|\psi_1\rangle$ is a normalized superposition of *good* basis states and $|\psi_0\rangle$ of *bad* ones. A classical randomized algorithm qualifies after it is made reversible, with its random bits drawn from Hadamard gates.
- The inverse $A^{-1}$, which costs the same as $A$ when $A$ is a circuit (reverse the gates and invert each one).
- A test $\chi$ on basis states with $\chi(z) = 1$ for good $z$, as a phase flip $S_\chi|z\rangle = (-1)^{\chi(z)}|z\rangle$. It must be computable reversibly, like a [quantum oracle](/quantum-oracle/).
- The value of $a$, a lower bound on it, or a schedule that does not need it.

Let $\theta_a \in [0, \pi/2]$ with $\sin^2\theta_a = a$, and let $S_0 = I - 2|0\rangle\langle 0|$. The *amplification operator* is $Q = -A\,S_0\,A^{-1}\,S_\chi$. Here $-A S_0 A^{-1} = 2A|0\rangle\langle 0|A^\dagger - I$ is the reflection about $A|0\rangle$, the general form of the diffusion operator. On the plane of $|\psi_1\rangle$ and $|\psi_0\rangle$, $Q$ is a rotation by $2\theta_a$, with eigenvalues $e^{\pm 2i\theta_a}$. So

$$Q^m A|0\rangle = \sin((2m+1)\theta_a)\,|\psi_1\rangle + \cos((2m+1)\theta_a)\,|\psi_0\rangle,$$

and a measurement after $m$ rounds gives a good state with probability $\sin^2((2m+1)\theta_a)$. This is Lemma 1 of Brassard, Høyer, Mosca and Tapp. The proof is the one of [Grover's search algorithm](/grover-search/), with $A|0\rangle$ in place of the uniform state.

## The template

```pseudo id=main
AMPLIFY(A, χ, a)                           ▷ holes: the algorithm A, the test χ, the count rule
L1  θ ← arcsin(sqrt(a)); m ← ⌊π / (4θ)⌋     ▷ hole: a known a, or a schedule (BBHT, QSearch)
L2  |ψ⟩ ← A|0⟩                             ▷ hole: the algorithm A, without measurement
L3  repeat m times
L4      |ψ⟩ ← S_χ |ψ⟩                       ▷ hole: the test χ as a phase flip
L5      |ψ⟩ ← A S_0 A^(-1) |ψ⟩              ▷ the reflection about A|0⟩, up to sign
L6  measure |ψ⟩; let z be the result
L7  if χ(z) = 1 then return z else return FAIL
```

Line L5 omits the sign of $Q$, which is a global phase. With $m = \lfloor \pi/(4\theta_a) \rfloor$, the success probability is at least $\max(1 - a, a)$ (Theorem 2 of Brassard, Høyer, Mosca and Tapp). The cost is $2m + 1 \le (\pi/2)/\sqrt{a} + 1$ calls of $A$ or $A^{-1}$ and $m$ calls of $S_\chi$, plus one classical test in line L7.

**Unknown $a$.** Replace line L1 by a schedule: pick $m$ uniformly at random in a range that grows by a factor $c$ with $1 < c < 2$ after each failure, and test $A|0\rangle$ once without amplification first. This is QSearch (Theorem 3 of the same paper), the general form of [BBHT search](/bbht-search/). Its expected number of calls is $\Theta(1/\sqrt{a})$ when $a > 0$.

**Exact amplification.** If $a$ is known, success with probability 1 is possible (Theorem 4). One method of Section 2.1: let $\tilde m = \lceil \pi/(4\theta_a) - 1/2 \rceil$, and lower the success probability to $a' = \sin^2(\pi/(4\tilde m + 2)) \le a$ with an extra qubit that is good with probability $a'/a$. Then $(2\tilde m + 1)\theta_{a'} = \pi/2$ exactly. The other method changes the phases of the two reflections in the last round.

**Worked numbers.** Let $A$ be a one-qubit rotation with $A|0\rangle = \sqrt{0.9}\,|0\rangle + \sqrt{0.1}\,|1\rangle$, and let $|1\rangle$ be good, so $a = 0.1$ and $\theta_a = 0.3218$. Line L1 gives $m = \lfloor 2.441 \rfloor = 2$. The success probabilities after $m = 0, 1, 2, 3$ rounds are $0.1$, $0.676$, $0.9986$ and $0.603$. So 5 calls of $A$ or $A^{-1}$ give success $0.9986$, where repetition needs 10 runs on average and 63 runs for the same failure rate $0.0014$. For exact amplification, $\tilde m = 2$ and $a' = \sin^2(\pi/10) = 0.0955$: the extra qubit is good with probability $0.955$, and two rounds give success exactly 1. For $a = 0.001$, $m = 24$ rounds (49 calls) give $0.9996$, against 1000 expected runs.

## Classic examples

- [Grover's search algorithm](/grover-search/): $A = H^{\otimes n}$, $\chi = f$ and $a = M/N$.
- [BBHT search](/bbht-search/): the template with the random schedule for an unknown $a$.
- [Quantum counting](/quantum-counting/): [phase estimation](/quantum-phase-estimation/) of $Q$ estimates $\theta_a$, and so $a$. This is *amplitude estimation*: with $P$ calls of $Q$ it outputs $\tilde a = \sin^2(\pi y/P)$ with $|\tilde a - a| \le 2\pi\sqrt{a(1-a)}/P + \pi^2/P^2$, with probability at least $8/\pi^2$ (Theorem 12 of Brassard, Høyer, Mosca and Tapp). There is no separate page for amplitude estimation.
- [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/): amplification with the test "value below the current threshold".
- [Brassard-Høyer-Tapp collision finding](/brassard-hoyer-tapp-collision/): $A$ prepares a superposition over a large set, and $\chi$ tests for a collision with a stored table.
- [Quantum walk search](/quantum-walk-search/): the walk-based search frameworks use amplitude amplification on top of a walk to find a marked vertex.
- Classical Monte Carlo algorithms: a reversible version of a randomized algorithm with success probability $p$ needs $O(1/\sqrt{p})$ runs in place of $O(1/p)$. Compare classical [error amplification](/error-amplification/), which repeats runs.

## Variations

- **Fixed-point amplification.** Change the phases of the reflections so that more rounds never lower the success probability. See [fixed-point quantum search](/fixed-point-quantum-search/).
- **Amplitude estimation.** Estimate $a$ in place of finding a good state, with error $O(1/P)$ after $P$ calls, where sampling needs $O(1/P^2)$ runs for the same error. See [quantum counting](/quantum-counting/).
- **Oblivious amplitude amplification.** Berry, Childs, Cleve, Kothari and Somma (2014) amplify a probabilistic implementation of a unitary for every input state, without a reflection about the input. It is used in Hamiltonian simulation by linear combinations of unitaries.
- **Variable-time amplification.** Ambainis (2012) handles an $A$ whose branches stop at different times, so the cost depends on an average of the running times and not on the longest one.

## Pitfalls

- **A measurement inside $A$.** If $A$ measures in the middle, line L5 cannot apply $A^{-1}$ and the rotation is lost. Defer every measurement to the end of $A$, with ancillas in place of measured bits.
- **$A$ in place of $A^{-1}$.** Line L5 written as $A\,S_0\,A$ is not a reflection about $A|0\rangle$ unless $A$ is its own inverse. Use $A\,S_0\,A^{-1}$. Hadamard layers hide this mistake, because $H^{\otimes n}$ is its own inverse.
- **The wrong count.** A count $m$ from a wrong $a$ overshoots: for $a = 0.1$, three rounds give $0.603$ where two give $0.9986$. If $a$ is not known, use the schedule of line L1 in its QSearch form, not a guess.
- **A large $a$.** For $a \ge 1/2$, line L1 gives $m = 0$ or $m = 1$, and for $a > 3/4$ amplification gains nothing over a classical repeat. Run $A$ directly.
- **Free calls.** Each round costs one call of $A$, one of $A^{-1}$ and one of $S_\chi$. Count all three. The gain over $1/a$ repeats is real only if $A^{-1}$ and $S_\chi$ cost about as much as $A$.
- **Garbage in the good test.** If $\chi$ leaves garbage qubits that depend on $z$, they break the interference. Uncompute them in $S_\chi$, so its ancillas are returned clean.

## Exercises

1. Show that $Q = -A S_0 A^{-1} S_\chi$ maps the plane of $|\psi_1\rangle$ and $|\psi_0\rangle$ to itself, and that its eigenvalues there are $e^{\pm 2i\theta_a}$. (Hint: write $Q$ as the product of two reflections in that plane.)
2. Show that for $a = 1/4$ one round gives success with certainty, and that for $a = 1/2$ no number of rounds of the template does.
3. A randomized algorithm uses $r$ random bits and succeeds with probability $p$. Build $A$ from it, and show that $O(1/\sqrt{p})$ runs of $A$ and $A^{-1}$ find a success.
4. For $a = 0.1$, check the exact method: $\tilde m = 2$, $a' = \sin^2(\pi/10)$, and $5\,\theta_{a'} = \pi/2$.
5. Explain why amplitude amplification cannot decide whether $a = 0$ or $a = 2^{-n}$ with fewer than $\Omega(2^{n/2})$ calls of $A$. (Hint: use the [optimality theorem](/grover-optimality/) of search.)

## References
