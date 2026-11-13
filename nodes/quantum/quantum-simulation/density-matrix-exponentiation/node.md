---
tag: QD2N3E
kind: technique
slug: density-matrix-exponentiation
name: Density matrix exponentiation
aliases:
- Lloyd-Mohseni-Rebentrost exponentiation
- sample-based Hamiltonian simulation
area: quantum/quantum-simulation
level: research
summary: "Approximate e^(-i rho t) for an unknown density matrix rho from copies of rho: each copy is swapped partly into the target and then discarded. Error t^2/n with n copies, which is optimal."
prereqs: [density-matrix, partial-trace, quantum-channel, hamiltonian-simulation]
see_also: [swap-test, quantum-phase-estimation, trace-distance, lie-trotter-product-formula, principal-component-analysis, quantum-state-tomography, hamiltonian-learning, mixed-state]
sources:
  - paper: doi:10.1038/nphys3029
    title: Seth Lloyd, Masoud Mohseni and Patrick Rebentrost, Quantum principal component analysis, Nature Physics 10, 2014, pages 631-633
    locator: the partial SWAP step Tr_1[e^(-iS dt)(rho (x) sigma)e^(iS dt)] = sigma - i dt [rho, sigma] + O(dt^2), and its use with phase estimation to find the large eigenvalues of rho
  - paper: doi:10.1038/s41534-017-0013-7
    title: Shelby Kimmel, Cedric Yen-Yu Lin, Guang Hao Low, Maris Ozols and Theodore J. Yoder, Hamiltonian simulation with optimal sample complexity, npj Quantum Information 3, 2017, article 13
    locator: the lower bound of order t^2/epsilon copies for simulating e^(-i rho t), which shows that density matrix exponentiation is optimal, and the extension to Hamiltonians given as linear combinations of states
  - paper: arxiv:2412.02134
    title: Beatriz Go, Hyukjoon Kwon, Soohyun Park, Dhrumil Patel and Mark M. Wilde, Density matrix exponentiation and sample-based Hamiltonian simulation, non-asymptotic analysis of sample complexity, 2024 (Quantum Science and Technology 10, 2025, 045058)
    locator: the bound of at most 4t^2/epsilon copies for error epsilon in normalized diamond distance, and the remark that earlier analyses appear to be incomplete
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: the chapters on density operators, the partial trace and quantum operations (general locator)
---

*Density matrix exponentiation* is a technique that applies the unitary $e^{-i\rho t}$ to a target state $\sigma$ when the [density matrix](/density-matrix/) $\rho$ is not known but many copies of it are available. Lloyd, Mohseni and Rebentrost introduced it in 2014 for quantum principal component analysis. One step takes a fresh copy of $\rho$, applies $e^{-i\delta S}$ to the copy and the target, where $S$ is the SWAP of the two registers, and discards the copy. The target becomes $\cos^2\delta\,\sigma + \sin^2\delta\,\rho - i\sin\delta\cos\delta\,[\rho, \sigma]$, which agrees with $e^{-i\rho\delta}\sigma e^{i\rho\delta}$ up to $O(\delta^2)$. With $n$ steps of size $\delta = t/n$ the error is $O(t^2/n)$, so $O(t^2/\epsilon)$ copies give error $\epsilon$; Go, Kwon, Park, Patel and Wilde prove that $4t^2/\epsilon$ copies suffice in normalized diamond distance, and Kimmel et al. prove that order $t^2/\epsilon$ copies are necessary.

## In plain words

Usually a quantum computer runs a process that is written down in advance. Here the process is given only by a supply of identical quantum states that nobody has described, and the goal is to make the state act as the rule of motion for another system. The trick is to take one of the given states, let it trade places with the target system by a very small amount, and then throw it away. Each such small exchange moves the target a little in the right direction and adds a small error. Many small exchanges, each with a new copy, add up to a large motion, and the error shrinks when the exchanges are made smaller and more numerous. The price is that every copy is used up.

## When it applies

- You have many copies of an unknown state $\rho$ on $m$ qubits, from a preparation circuit, an experiment or an earlier step of a computation, and you want to use $\rho$ as a Hamiltonian, not to learn it.
- You can apply a SWAP of two $m$-qubit registers, and for phase estimation a controlled SWAP. No other knowledge of $\rho$ is needed: no matrix entries, no block encoding, no sparse access.
- The evolution time $t$ is moderate. The number of copies grows as $t^2/\epsilon$, so long times or high precision cost many copies.
- For a Hamiltonian $H$ that is a known sparse matrix, [Hamiltonian simulation](/hamiltonian-simulation/) is cheaper; density matrix exponentiation is for the case where the "Hamiltonian" is a state.

## The template

```pseudo id=main
DME(copies of ρ, σ, t, n)
L1  δ ← t/n                                          ▷ hole: n from the error budget, n ≥ 4t²/ε
L2  repeat n times
L3      take a fresh copy of ρ next to the target
L4      apply e^(-iδS) to the copy and the target    ▷ hole: a circuit for the partial SWAP
L5      discard the copy                             ▷ the partial trace over the copy
L6  return the target
```

**Why one step works.** $S^2 = I$, so $e^{-i\delta S} = \cos\delta\,I - i\sin\delta\,S$. Write $\tau = \rho \otimes \sigma$ with the copy first. Then $e^{-i\delta S}\tau e^{i\delta S} = \cos^2\delta\,\tau + \sin^2\delta\,S\tau S - i\sin\delta\cos\delta\,(S\tau - \tau S)$. The [partial trace](/partial-trace/) over the copy gives $\mathrm{Tr}_1\tau = \sigma$, $\mathrm{Tr}_1(S\tau S) = \mathrm{Tr}_1(\sigma \otimes \rho) = \rho$, $\mathrm{Tr}_1(S(\rho \otimes \sigma)) = \rho\sigma$ and $\mathrm{Tr}_1((\rho \otimes \sigma)S) = \sigma\rho$. The last two identities follow from the matrix elements of $S$: $\langle a|\langle b|S|c\rangle|d\rangle = \delta_{ad}\delta_{bc}$. So one step is the [quantum channel](/quantum-channel/)

$$\mathcal{E}_\delta(\sigma) = \cos^2\delta\,\sigma + \sin^2\delta\,\rho - i\sin\delta\cos\delta\,[\rho, \sigma] = \sigma - i\delta[\rho, \sigma] + \delta^2(\rho - \sigma) + O(\delta^3).$$

The exact step is $e^{-i\rho\delta}\sigma e^{i\rho\delta} = \sigma - i\delta[\rho, \sigma] - \tfrac{\delta^2}{2}[\rho, [\rho, \sigma]] + O(\delta^3)$. The first-order terms agree, and the second-order difference $\delta^2(\rho - \sigma + \tfrac12[\rho, [\rho, \sigma]])$ has trace norm at most $4\delta^2$, since $\|\rho - \sigma\|_1 \le 2$ and $\|[\rho, [\rho, \sigma]]\|_1 \le 4$.

**Why n steps work.** The channels $\mathcal{E}_\delta$ and the exact unitary channels contract the trace norm, so the errors of the $n$ steps add: the total error is at most $n$ times the error of one step, $O(n\delta^2) = O(t^2/n)$, by the same telescoping argument as for the [Lie-Trotter product formula](/lie-trotter-product-formula/). Go et al. make the constants rigorous: $n \ge 4t^2/\epsilon$ copies give error at most $\epsilon$ in normalized diamond distance, for every input, including inputs entangled with other systems.

**The partial SWAP.** $S$ is a product of $m$ swaps of qubit pairs. Since $S^2 = I$, the circuit $W$ that applies a Hadamard gate to one ancilla qubit, then a SWAP controlled by the ancilla, then a Hadamard gate again, satisfies $W^2 = I$, and $W\,e^{-i\delta Z_a}\,W$ acts as $e^{-i\delta S}$ on the registers with the ancilla starting and ending in $|0\rangle$. This takes $2m$ controlled-SWAP gates and one rotation.

**Example.** All numbers below are from the page's simulator with exact density matrices. Let $\rho = \mathrm{diag}(3/4, 1/4)$, $\sigma = |{+}\rangle\langle{+}|$ and $t = 1$. Exactly, $e^{-i\rho t}$ only rotates the phase of the off-diagonal entry: it becomes $\tfrac12e^{-i/2}$. Since $[\rho, \sigma]$ has off-diagonal entries $\pm\tfrac12\sigma_{01}$, one step multiplies $\sigma_{01}$ by $\cos\delta(\cos\delta - \tfrac i2\sin\delta)$; the modulus of this factor is below 1, so the main error is a loss of coherence. The [trace distance](/trace-distance/) to the exact result is:

| copies $n$ | 1 | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|---|
| error | 0.365 | 0.208 | 0.114 | 0.0597 | 0.0306 | 0.0155 | 0.00782 |

The product $n \cdot \text{error}$ tends to $0.50$, so the error falls as $1/n$. For a random one-qubit $\rho$ of rank 2 and a random pure $\sigma$ (seed 3), $n \cdot \text{error}/t^2$ is between $0.38$ and $0.45$ for $t \in \{0.5, 1, 2\}$ and $n$ from 10 to 160. Over 20 random pairs of one-qubit states (seed 11), with $t \in \{0.5, 1, 3\}$ and $n \in \{5, 20, 50\}$, the largest value of $n \cdot \text{error}/t^2$ is $0.85$, below the constant 4 of the bound.

## Classic examples

- **Quantum principal component analysis.** Lloyd, Mohseni and Rebentrost run [quantum phase estimation](/quantum-phase-estimation/) with controlled $e^{-i\rho t}$ on a copy of $\rho$ itself. The output is an eigenvalue $\lambda_k$ of $\rho$ with probability $\lambda_k$, together with its eigenvector, so the large eigenvalues of $\rho$, the principal components in the sense of [principal component analysis](/principal-component-analysis/), are found without [tomography](/quantum-state-tomography/) when $\rho$ has low rank.
- **Sample-based Hamiltonian simulation.** Kimmel et al. simulate $e^{-iHt}$ for a Hamiltonian given as a combination of states, $H = \sum_jc_j\rho_j$, from copies of the $\rho_j$, with the same $t^2/\epsilon$ scaling in the number of samples.
- **States as programs.** In quantum machine learning proposals, data are encoded in a state $\rho$, and $e^{-i\rho t}$ is the subroutine that lets a later phase estimation or linear-system step act on the data without reading them out.

## Variations

- **Controlled exponentiation.** Replacing $e^{-i\delta S}$ by a controlled $e^{-i\delta S}$ gives controlled $e^{-i\rho t}$, which phase estimation needs. The copy count is the same.
- **Higher-order steps.** Unlike product formulas, the step cannot be made higher order by a cleverer schedule: the lower bound of Kimmel et al. shows that order $t^2/\epsilon$ copies are necessary for any protocol, so the second-order step is already optimal in the number of copies.
- **Combinations of states.** Steps with copies of several states $\rho_j$, chosen at random with probabilities proportional to $|c_j|$ and with the sign of $c_j$ in the direction of the partial SWAP, give $e^{-iHt}$ for $H = \sum_jc_j\rho_j$, in the spirit of [qDRIFT](/qdrift/).
- **Overlaps instead of evolutions.** If only the number $\mathrm{Tr}(\rho\sigma)$ is needed, the [swap test](/swap-test/) gives it directly with one copy per run; exponentiation is needed only when the evolution itself feeds a later step.

## Pitfalls

- **The copies are consumed.** Each step destroys a copy, so $n$ copies are spent for one application of $e^{-i\rho t}$. Phase estimation to precision $\epsilon$ needs times of order $1/\epsilon$, hence of order $1/\epsilon^3$ copies, which often removes the speedup that the application hoped for.
- **The error is not unitary.** One step is a channel that is close to a unitary channel, not a unitary; the error shows up as loss of coherence, as in the example, and it does not cancel between steps.
- **The sign.** The step gives $e^{-i\rho\delta}$, not $e^{+i\rho\delta}$, for $e^{-i\delta S}$ with the copy and the target in either order, since $S$ is symmetric. To get the inverse, use $e^{+i\delta S}$.
- **Small eigenvalues are hard to see.** The method reveals the spectrum of $\rho$ only to additive precision; for a state close to the maximally mixed state on $m$ qubits the eigenvalues are of order $2^{-m}$, and quantum principal component analysis is useful only when a few eigenvalues dominate.
- **Older error constants.** Go et al. note that earlier analyses of the sample complexity appear to be incomplete; cite their bound, $4t^2/\epsilon$ copies, for a rigorous constant.

## Exercises

1. Prove the identities $\mathrm{Tr}_1(S(\rho \otimes \sigma)) = \rho\sigma$ and $\mathrm{Tr}_1((\rho \otimes \sigma)S) = \sigma\rho$ from the matrix elements of $S$.
2. Show that $\mathcal{E}_\delta(\rho) = \rho$: a target that equals the copies does not move. Why is this also true for the exact evolution?
3. For $\rho = \mathrm{diag}(p, 1 - p)$ and $\sigma = |{+}\rangle\langle{+}|$, find the off-diagonal entry of the target after $n$ steps with $\delta = t/n$, and its limit for $n \to \infty$.
4. Check that the circuit $W\,e^{-i\delta Z_a}\,W$ of the template acts as $e^{-i\delta S}$, using the projectors $(I \pm S)/2$.
5. How many copies does the bound of Go et al. require for $t = 10$ and $\epsilon = 0.01$? How many are needed for phase estimation of the eigenvalues of $\rho$ to precision $10^{-2}$, if $t$ must be of order $1/\epsilon$?

## References
