---
tag: E8HPZJ
kind: technique
slug: variational-method
name: Variational method
aliases:
- variational principle
- variational method of quantum mechanics
area: quantum/quantum-simulation
level: advanced
summary: "Bound the lowest eigenvalue of a Hamiltonian from above by minimizing the energy <psi|H|psi> over a family of normalized trial states; the minimizer approximates the ground state."
prereqs: [rayleigh-quotient, quantum-state, quantum-measurement]
see_also: [rayleigh-ritz-method, courant-fischer-theorem, variational-quantum-eigensolver, ground-state-energy-estimation, ground-state-preparation, quantum-chemistry-simulation, gibbs-state-preparation, lanczos-algorithm]
sources:
  - paper: doi:10.1515/crll.1909.135.1
    title: Walther Ritz, Ueber eine neue Methode zur Loesung gewisser Variationsprobleme der mathematischen Physik, Journal fuer die reine und angewandte Mathematik 135, 1909, pages 1-61
    locator: the method of minimizing over a finite linear family of trial functions, the origin of the Rayleigh-Ritz method
  - paper: doi:10.1103/PhysRev.43.830
    title: J. K. L. MacDonald, Successive approximations by the Rayleigh-Ritz variation method, Physical Review 43, 1933, pages 830-833
    locator: the theorem that the k-th lowest Ritz value of a linear trial space is an upper bound on the k-th eigenvalue, and that it does not increase when the trial space grows
  - paper: doi:10.1098/rspa.1928.0098
    title: George Temple, The theory of Rayleigh's principle as applied to continuous systems, Proceedings of the Royal Society of London A 119, 1928, pages 276-293
    locator: the lower bound on the lowest eigenvalue from the energy and the variance of a trial state, now called Temple's inequality
  - book: isbn:9781107189638
    title: David J. Griffiths and Darrell F. Schroeter, Introduction to Quantum Mechanics, 3rd edition, Cambridge University Press, 2018
    locator: the chapter on the variational principle, with the Gaussian trial function for hydrogen and the effective nuclear charge for helium (general locator)
  - book: isbn:9780486691862
    title: Attila Szabo and Neil S. Ostlund, Modern Quantum Chemistry, Dover, 1996
    locator: the chapter on mathematical review, with the variational principle and the linear variational problem (general locator)
---

The *variational method* finds an upper bound on the lowest eigenvalue $E_0$ of a Hamiltonian $H$, and an approximation of the ground state, without diagonalizing $H$. It rests on the *variational principle*: for every normalized state, $\langle\psi|H|\psi\rangle \ge E_0$, with equality exactly when $|\psi\rangle$ lies in the ground space. One picks a family of trial states $|\psi(\theta)\rangle$ that can be handled, by hand, by a classical computer or on a quantum computer, and minimizes the energy $E(\theta) = \langle\psi(\theta)|H|\psi(\theta)\rangle$ over the parameters. The minimum is never below $E_0$, and it is close to $E_0$ when the family contains a state close to the ground state. For a linear family the method becomes the [Rayleigh-Ritz method](/rayleigh-ritz-method/), and by the [Courant-Fischer theorem](/courant-fischer-theorem/) it also bounds the excited energies from above. The principle is a theorem; how good a given family is, is a matter of experience and measurement.

## In plain words

A system always has a state of lowest energy, but finding it exactly is usually too hard. The variational method makes a guess with a few adjustable knobs, computes the energy of the guess, and turns the knobs until the energy is as low as possible. No guess can have less energy than the true lowest state, so every computed value is a safe upper limit, and a lower value is always a better one. If the guess can take a shape close to the true state, the result is close to the true energy. If the guess has the wrong shape, the result stays too high, and the method alone does not tell you by how much.

## When it applies

- $H$ is Hermitian and bounded below, so $E_0 = \min\mathrm{spec}(H)$ exists: a finite matrix, a spin or qubit Hamiltonian, or a Schrodinger operator such as the hydrogen Hamiltonian.
- You can compute or estimate the energy of a trial state: by integrals, by a classical tensor contraction, by Monte Carlo sampling, or by measuring Pauli terms on a quantum computer.
- An upper bound is useful, or you trust the family enough to take the minimizer as the ground state. For error bars, a lower bound is needed in addition.
- The trial family has fewer parameters than the state space has dimensions; otherwise you could diagonalize $H$ directly.

## The template

```pseudo id=main
VARIATIONAL(H, ψ(θ))
L1  choose a family of normalized trial states ψ(θ)       ▷ hole: the ansatz
L2  for parameters θ, compute E(θ) = ⟨ψ(θ)|H|ψ(θ)⟩      ▷ hole: exact, sampled or measured energies
L3  minimize E over θ                                     ▷ hole: the optimizer
L4  return E(θ*) ≥ E_0 and the trial state ψ(θ*)
```

**The variational principle.** Let $|E_i\rangle$ be an orthonormal eigenbasis of $H$ with $H|E_i\rangle = E_i|E_i\rangle$ and $E_0 \le E_1 \le \cdots$. Write $|\psi\rangle = \sum_ia_i|E_i\rangle$ with $\sum_i|a_i|^2 = 1$. Then

$$\langle\psi|H|\psi\rangle - E_0 = \sum_i|a_i|^2(E_i - E_0) \ge 0,$$

since every term is nonnegative. Equality holds if and only if $a_i = 0$ for every $i$ with $E_i > E_0$, that is, $|\psi\rangle$ is in the ground space. For a state that is not normalized, the same holds for the [Rayleigh quotient](/rayleigh-quotient/) $\langle\psi|H|\psi\rangle/\langle\psi|\psi\rangle$. In infinite dimensions the sum becomes an integral over the spectral measure of $H$, with the same conclusion.

**What a small energy error says about the state.** Let $\Delta$ be the gap from $E_0$ to the next distinct eigenvalue and $w$ the weight of $|\psi\rangle$ on the ground space. Every term with $E_i > E_0$ has $E_i - E_0 \ge \Delta$, so $\langle\psi|H|\psi\rangle - E_0 \ge \Delta(1 - w)$, and an energy error $\eta$ gives $1 - w \le \eta/\Delta$. In the other direction, a state at distance $\epsilon$ from a ground state has energy error at most $\|H - E_0\|\epsilon^2$: the energy is quadratic in the error of the state, which is why variational energies are much better than variational states.

**Linear families.** If the trial states are the combinations $|\psi\rangle = \sum_{j=1}^mc_j|\chi_j\rangle$ of $m$ fixed vectors, minimizing the Rayleigh quotient gives the generalized eigenproblem $\mathbf Hc = E\mathbf Sc$ with $\mathbf H_{jl} = \langle\chi_j|H|\chi_l\rangle$ and $\mathbf S_{jl} = \langle\chi_j|\chi_l\rangle$, as in the [Rayleigh-Ritz method](/rayleigh-ritz-method/). By the Courant-Fischer theorem the $k$-th lowest eigenvalue of this problem is at least $E_{k-1}$ for every $k \le m$, and adding vectors to the family never raises any of them (Hylleraas and Undheim 1930, MacDonald 1933).

## Classic examples

- **Hydrogen with a Gaussian.** In atomic units, $H = -\tfrac12\nabla^2 - 1/r$ and the exact $E_0 = -0.5$ Hartree. For the trial function $e^{-\alpha r^2}$, the kinetic energy is $3\alpha/2$ and the potential energy is $-2\sqrt{2\alpha/\pi}$, so $E(\alpha) = 3\alpha/2 - 2\sqrt{2\alpha/\pi}$. The minimum is at $\alpha = 8/(9\pi)$, with $E = -4/(3\pi) \approx -0.4244$ Hartree, 15 percent above the exact value: a Gaussian has the wrong shape at the nucleus and in the tail.
- **Helium with an effective charge.** Take the product of two hydrogen-like $1s$ orbitals for nuclear charge $Z$. The energy in Hartree is $E(Z) = Z^2 - 4Z + \tfrac58Z$: kinetic energy $Z^2$, attraction to the nucleus of charge 2 equal to $-4Z$, and electron repulsion $\tfrac58Z$. The minimum is at $Z = 27/16$, with $E = -(27/16)^2 \approx -2.8477$ Hartree, against the exact $-2.9037$. The optimal $Z < 2$ shows how each electron screens the nucleus from the other.
- **A two-level system.** For $H = \begin{pmatrix}0 & 1\\ 1 & 1\end{pmatrix}$ and the real trial states $(\cos\theta, \sin\theta)$, $E(\theta) = \tfrac12 - \tfrac12\cos2\theta + \sin2\theta$, with minimum $\tfrac12 - \tfrac{\sqrt5}2 \approx -0.618$, which is $E_0$: the family contains every real state. The basis state $(1, 0)$ alone gives the bound $0$.
- **Hartree-Fock and configuration interaction.** In [quantum chemistry](/quantum-chemistry-simulation/), Hartree-Fock minimizes over single Slater determinants, a nonlinear family; configuration interaction minimizes over linear combinations of determinants, a linear family.
- **Tensor networks.** The density matrix renormalization group minimizes the energy over matrix product states of a fixed bond dimension, one tensor at a time.
- **Parameterized circuits.** The [variational quantum eigensolver](/variational-quantum-eigensolver/) takes the trial states from a quantum circuit with adjustable gates and estimates the energy by measuring Pauli terms; the classical optimizer runs line L3.

## Variations

- **Excited states.** Minimizing over trial states orthogonal to the exact ground state bounds $E_1$, and a symmetry that separates the sectors gives such states for free; with an approximate ground state the bound can fail. In a linear family all Ritz values are upper bounds, as above.
- **Lower bounds.** If $E_1 \ge b > \langle H\rangle$ for a known $b$, *Temple's inequality* gives $E_0 \ge \langle H\rangle - \sigma^2/(b - \langle H\rangle)$, with $\sigma^2 = \langle H^2\rangle - \langle H\rangle^2$ the energy variance of the trial state. Together with the variational bound it gives an interval for $E_0$.
- **Variational Monte Carlo.** The energy of a trial wave function that cannot be integrated exactly is estimated by sampling $|\psi|^2$ with a Markov chain; the bound then holds only up to the statistical error.
- **Time-dependent variational principles.** The Dirac-Frenkel and McLachlan principles project the Schrodinger equation, or the imaginary-time equation, onto the tangent space of the trial family; they give equations of motion for the parameters instead of a minimization.
- **Thermal states.** The Gibbs-Bogoliubov inequality $F \le \mathrm{Tr}(\rho H) - \beta^{-1}S(\rho)$ is the variational principle for the free energy, with equality at the Gibbs state; see [Gibbs state preparation](/gibbs-state-preparation/).

## Pitfalls

- **An upper bound has no error bar.** A low energy does not show that the family is good; the true $E_0$ may be far lower. Use a lower bound such as Temple's, an exact method on small sizes, or a growing family, and watch the convergence.
- **Good energies, poor states.** Since the energy error is quadratic in the error of the state, observables other than $H$ are usually much less accurate than the energy.
- **Noisy energies break the bound.** If $E(\theta)$ is estimated from samples or measurements, the estimate can fall below $E_0$ by the statistical error, and minimizing a noisy function favours such low estimates. Report the bound with its confidence interval.
- **Local minima.** For nonlinear families, such as Hartree-Fock or circuits, the energy landscape has local minima and flat regions, and the optimizer may stop far from the best member of the family. Finding the ground energy of a local Hamiltonian is QMA-hard in general, so no family and optimizer can be efficient and exact for all inputs.
- **Wrong symmetry.** A family that stays in one symmetry sector finds the lowest state of that sector, which may not be the ground state.
- **Unnormalized trial states.** Minimizing $\langle\psi|H|\psi\rangle$ without the normalization goes to zero or to minus infinity; minimize the Rayleigh quotient instead.

## Exercises

1. Prove the variational principle from the spectral expansion, and show that equality holds only on the ground space.
2. For the trial function $e^{-\alpha r^2}$ for hydrogen, derive $E(\alpha) = 3\alpha/2 - 2\sqrt{2\alpha/\pi}$ and its minimum $-4/(3\pi)$.
3. For helium with the effective charge $Z$, find the minimizing $Z$ and compare the bound with the exact $-2.9037$ Hartree. What is the relative error?
4. Show that an energy error $\eta$ implies a weight at most $\eta/\Delta$ outside the ground space, and that a state at distance $\epsilon$ from a ground state has energy error at most $\|H - E_0\|\epsilon^2$.
5. For the two-level example and the trial state $(1, 0)$, compute Temple's lower bound with $b = E_1 = (1 + \sqrt5)/2$, and compare it with $E_0$.
6. Show that minimizing the Rayleigh quotient over a linear family gives the generalized eigenproblem $\mathbf Hc = E\mathbf Sc$.

## References
