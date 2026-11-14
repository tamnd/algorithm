---
tag: VEC71F
kind: concept
slug: entanglement-entropy
name: Entanglement entropy
aliases:
- entropy of entanglement
area: quantum/quantum-primitives
level: advanced
summary: The entanglement entropy of a pure state across a cut is the von Neumann entropy of either reduced state. It counts the Bell pairs the state is worth.
prereqs: [entanglement, von-neumann-entropy, partial-trace]
see_also: [bell-states, singular-value-decomposition, shannon-entropy, binary-entropy-function, quantum-many-body-simulation, swap-test, density-matrix, min-entropy]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.5 (the Schmidt decomposition), Chapter 11 (entropy) and Section 12.5 (entanglement as a physical resource)
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Chapter 6 (bipartite entanglement)
  - paper: doi:10.1103/PhysRevA.53.2046
    title: Charles H. Bennett, Herbert J. Bernstein, Sandu Popescu and Benjamin Schumacher, Concentrating partial entanglement by local operations, Physical Review A 53, 1996, pages 2046 to 2052
    locator: entanglement concentration and dilution at the rate S(ρ_A)
  - paper: doi:10.1103/PhysRevA.56.R3319
    title: Sandu Popescu and Daniel Rohrlich, Thermodynamics and the measure of entanglement, Physical Review A 56, 1997, pages R3319 to R3321
    locator: the uniqueness of the measure for pure states
  - paper: doi:10.1103/PhysRevLett.83.436
    title: M. A. Nielsen, Conditions for a class of entanglement transformations, Physical Review Letters 83, 1999, pages 436 to 439
    locator: the majorization rule for one copy
  - paper: doi:10.1103/RevModPhys.81.865
    title: Ryszard Horodecki, Paweł Horodecki, Michał Horodecki and Karol Horodecki, Quantum entanglement, Reviews of Modern Physics 81, 2009, pages 865 to 942
    locator: the part on entanglement measures
  - paper: doi:10.1103/PhysRevA.54.3824
    title: Charles H. Bennett, David P. DiVincenzo, John A. Smolin and William K. Wootters, Mixed-state entanglement and quantum error correction, Physical Review A 54, 1996, pages 3824 to 3851
    locator: the entanglement of formation and distillable entanglement
  - paper: doi:10.1103/PhysRevLett.80.2245
    title: William K. Wootters, Entanglement of formation of an arbitrary state of two qubits, Physical Review Letters 80, 1998, pages 2245 to 2248
    locator: the closed form for two qubits
  - paper: doi:10.1103/PhysRevA.65.032314
    title: G. Vidal and R. F. Werner, Computable measure of entanglement, Physical Review A 65, 2002, article 032314
    locator: the negativity
  - paper: doi:10.1103/PhysRevLett.71.1291
    title: Don N. Page, Average entropy of a subsystem, Physical Review Letters 71, 1993, pages 1291 to 1294
    locator: the mean entropy of a random pure state
  - paper: doi:10.1088/1742-5468/2007/08/P08024
    title: M. B. Hastings, An area law for one-dimensional quantum systems, Journal of Statistical Mechanics, 2007, article P08024
    locator: the area law for gapped chains
  - paper: doi:10.1103/RevModPhys.82.277
    title: J. Eisert, M. Cramer and M. B. Plenio, Colloquium, area laws for the entanglement entropy, Reviews of Modern Physics 82, 2010, pages 277 to 306
    locator: the review of area laws
  - paper: doi:10.1088/1742-5468/2004/06/P06002
    title: Pasquale Calabrese and John Cardy, Entanglement entropy and quantum field theory, Journal of Statistical Mechanics, 2004, article P06002
    locator: the logarithmic law for critical chains
  - paper: doi:10.1103/PhysRevLett.91.147902
    title: Guifré Vidal, Efficient classical simulation of slightly entangled quantum computations, Physical Review Letters 91, 2003, article 147902
    locator: simulation cost in terms of the Schmidt rank across cuts
  - paper: doi:10.1103/PhysRevLett.96.110404
    title: Alexei Kitaev and John Preskill, Topological entanglement entropy, Physical Review Letters 96, 2006, article 110404
    locator: the constant correction for topological order
  - paper: doi:10.1103/PhysRevLett.96.110405
    title: Michael Levin and Xiao-Gang Wen, Detecting topological order in a ground state wave function, Physical Review Letters 96, 2006, article 110405
    locator: the same constant from a different subtraction
  - paper: doi:10.1038/nature15750
    title: Rajibul Islam and others, Measuring entanglement entropy in a quantum many-body system, Nature 528, 2015, pages 77 to 83
    locator: measuring the Rényi-2 entropy with two copies
---

The *entanglement entropy* of a pure state $|\psi\rangle_{AB}$ is the [von Neumann entropy](/von-neumann-entropy/) of the reduced state of one part, $E(\psi) = S(\rho_A) = -\mathrm{Tr}\,\rho_A \log_2 \rho_A$ with $\rho_A = \mathrm{Tr}_B |\psi\rangle\langle\psi|$. It is $0$ exactly for product states, it is $\log_2 d$ for a maximally entangled state of two $d$-level systems, and it is the same for $A$ and $B$. Its meaning is operational: from $n$ copies of $|\psi\rangle$, local operations and classical communication make about $n E(\psi)$ [Bell pairs](/bell-states/), and need about that many to make the copies back. For mixed states it is not a measure of entanglement, and other measures take its place.

## In plain words

Split a system into two parts and look at one part only. If the whole is in a definite state but the part looks random, the randomness comes from entanglement with the other part. Entanglement entropy measures how random the part looks, in bits. A product of two definite parts gives zero. One Bell pair gives one bit. Many copies of a weakly entangled state can be turned into fewer, fully entangled pairs, and this number tells how many. The number is the same from either side of the split. It only works for a whole system in a definite state; for noisy states, randomness in a part can have other causes.

## The idea

### Definition by Schmidt coefficients

Every pure state of two parts has a Schmidt decomposition $|\psi\rangle = \sum_{i=1}^r \lambda_i |a_i\rangle|b_i\rangle$, with orthonormal $|a_i\rangle$, orthonormal $|b_i\rangle$ and $\lambda_1 \ge \dots \ge \lambda_r > 0$, $\sum_i \lambda_i^2 = 1$. The $\lambda_i$ are the singular values of the matrix of amplitudes $C_{jk} = \langle j k|\psi\rangle$ ([singular value decomposition](/singular-value-decomposition/)). Then $\rho_A = \sum_i \lambda_i^2 |a_i\rangle\langle a_i|$ and $\rho_B = \sum_i \lambda_i^2 |b_i\rangle\langle b_i|$ have the same nonzero eigenvalues, so

$$E(\psi) = S(\rho_A) = S(\rho_B) = -\sum_{i=1}^r \lambda_i^2 \log_2 \lambda_i^2,$$

the [Shannon entropy](/shannon-entropy/) of the distribution $(\lambda_i^2)$. The number $r$ of terms is the Schmidt rank.

### Basic properties

- **Range.** $0 \le E(\psi) \le \log_2 \min(d_A, d_B)$, with $0$ exactly when $r = 1$, a product state, and the maximum exactly when all $\lambda_i^2 = 1/\min(d_A, d_B)$, a maximally entangled state. Also $E(\psi) \le \log_2 r$.
- **Local unitaries.** $(U_A \otimes U_B)|\psi\rangle$ has the same Schmidt coefficients, so the same entropy.
- **Additivity.** $E(\psi \otimes \phi) = E(\psi) + E(\phi)$ when the two states sit across the same cut, because the Schmidt coefficients multiply and the entropy of a product distribution is the sum.
- **Monotone under LOCC.** Local operations and classical communication cannot increase $E$ on average over their outcomes. For one copy the rule is exact: Nielsen (1999) proved that $|\psi\rangle$ can be turned into $|\phi\rangle$ by LOCC if and only if the vector $(\lambda_i^2)$ of $\psi$ is majorized by that of $\phi$.

### The asymptotic meaning

Bennett, Bernstein, Popescu and Schumacher (1996) showed that for every pure state, $n$ copies can be turned by LOCC into $n E(\psi) - o(n)$ Bell pairs with fidelity tending to $1$ (*concentration*), and $n E(\psi) + o(n)$ Bell pairs, with $o(n)$ bits of communication, make $n$ copies (*dilution*). So pure-state entanglement is reversible in the limit, with $E$ as the exchange rate. Popescu and Rohrlich (1997) showed that $E$ is the only measure with this property, in the same way that thermodynamic entropy is fixed by reversible processes.

### Mixed states

For a mixed $\rho_{AB}$, $S(\rho_A)$ also counts classical uncertainty, so it is not a measure of entanglement: the separable state $I/4$ has $S(\rho_A) = 1$. The main replacements are the *entanglement of formation*, the least average $E$ over the ways to write $\rho$ as a mixture of pure states, with a closed form for two qubits (Wootters 1998); the *distillable entanglement*, the rate of Bell pairs that LOCC can extract (Bennett, DiVincenzo, Smolin and Wootters 1996); the *relative entropy of entanglement*; and the *negativity*, $(\lVert \rho^{T_B}\rVert_1 - 1)/2$, which is easy to compute (Vidal and Werner 2002). The first three equal $E(\psi)$ on pure states; the negativity does not, as it is $1/2$ for a Bell pair, whose $E$ is $1$. For a pure state of $A$, $B$ and an environment, $S(\rho_A)$ still measures the entanglement of $A$ with everything else.

### Rényi entropies

The *Rényi entanglement entropies* $S_\alpha(\rho_A) = \frac{1}{1 - \alpha}\log_2 \mathrm{Tr}\,\rho_A^\alpha$ give the same zero and maximum. $S_2 = -\log_2 \mathrm{Tr}\,\rho_A^2$ is at most $S$, because the entropy $S$ is the average of $-\log_2 \lambda_i^2$ and $S_2$ is minus the log of the average of $\lambda_i^2$, and [Jensen's inequality](/jensens-inequality/) compares the two. $\mathrm{Tr}\,\rho_A^2$ is the probability that a [swap test](/swap-test/) on two copies passes, minus $\tfrac{1}{2}$, times $2$, so $S_2$ can be measured with two copies and no tomography (Islam and others 2015). The limit $\alpha \to \infty$ gives the [min-entropy](/min-entropy/) $-\log_2 \lambda_1^2$.

## Examples

All values are in bits.

- **A Bell pair.** $(|00\rangle + |11\rangle)/\sqrt{2}$ has $\lambda_1^2 = \lambda_2^2 = \tfrac{1}{2}$ and $E = 1$.
- **A product.** $(0.6|0\rangle + 0.8|1\rangle)|0\rangle$ has $r = 1$ and $E = 0$.
- **A two-qubit family.** $\cos t\,|00\rangle + \sin t\,|11\rangle$ has $E = h(\cos^2 t)$, with $h$ the [binary entropy function](/binary-entropy-function/). For $t = \pi/8$, $\cos^2 t = 0.8536$ and $E = 0.6009$. So about $1000$ copies are worth about $601$ Bell pairs.
- **GHZ.** $(|000\rangle + |111\rangle)/\sqrt{2}$ has $E = 1$ across every cut, one qubit against two or two against one.
- **W.** $(|001\rangle + |010\rangle + |100\rangle)/\sqrt{3}$ has $\rho_A = \mathrm{diag}(\tfrac{2}{3}, \tfrac{1}{3})$ for any single qubit, so $E = h(\tfrac{1}{3}) = \log_2 3 - \tfrac{2}{3} = 0.9183$, while $S_2 = -\log_2 \tfrac{5}{9} = 0.8480$.
- **Two pairs, two cuts.** Qubits $3, 2$ in one Bell pair and qubits $1, 0$ in another. The cut $\{3, 1\} \mid \{2, 0\}$ crosses both pairs and gives $E = 2$; the cut $\{3, 2\} \mid \{1, 0\}$ crosses none and gives $E = 0$. The entropy depends on the cut, not only on the state.
- **Random states.** For a uniformly random pure state with $\dim A = m \le n = \dim B$, Page (1993) gave the mean $\sum_{k = n + 1}^{mn} \tfrac{1}{k} - \tfrac{m - 1}{2n}$ in nats, close to $\ln m - \tfrac{m}{2n}$. For $3$ qubits against $3$ qubits it is $2.2918$ bits, close to the maximum $3$. A seeded sample of $40$ random six-qubit states gives the mean $2.2831$.
- **A non-example.** For the mixed state $I/4$ of two qubits, $S(\rho_A) = 1$, but the state is separable; the entropy of a part is not a measure for mixed states.

### Common errors

- Using natural logarithms in one formula and base $2$ in another. In nats the Bell pair has $E = \ln 2 \approx 0.693$.
- Taking $S(\rho_{AB})$ instead of $S(\rho_A)$. For a pure state the total entropy is $0$.
- Using $S(\rho_A)$ as an entanglement measure for mixed states, as in the non-example.

### Implementation

The folder `impl/python` computes the Schmidt coefficients as the square roots of the eigenvalues of $\rho_A$ and the entropy from them. The tests check the Bell, product, GHZ and W values above, the family $\cos t|00\rangle + \sin t|11\rangle$ against $h(\cos^2 t)$, that $S(\rho_A) = S(\rho_B)$ and $S_2 \le S \le \min(\lvert A\rvert, \lvert B\rvert)$ for random four-qubit states over several cuts, the invariance under local unitaries, the two-pair example, and Page's mean for random six-qubit states within $0.06$ bits.

## Where it is used

- **Counting entanglement as a resource.** Protocols that use up entanglement, such as [quantum teleportation](/quantum-teleportation/) and [superdense coding](/superdense-coding/), are measured in Bell pairs, and $E$ converts a pure state into that unit.
- **Classical simulation.** A state whose Schmidt rank across every cut of a chain is at most $\chi$ has a matrix product form with $O(n\chi^2)$ numbers, and circuits that keep $\chi$ small can be simulated efficiently (Vidal 2003). Since $E \le \log_2 r$, a low entropy is a necessary sign of low cost, and this is the basis of tensor-network methods in [quantum many-body simulation](/quantum-many-body-simulation/).
- **Area laws.** Ground states of gapped local Hamiltonians in one dimension have $E$ bounded by a constant across every cut (Hastings 2007), and in higher dimensions $E$ is expected to grow like the boundary of the region, not its volume (Eisert, Cramer and Plenio 2010). At a critical point in one dimension, a block of $\ell$ sites has $E = \tfrac{c}{3}\ln \ell + \text{const}$ in nats, where $c$ is the central charge (Calabrese and Cardy 2004). Random states and thermal states follow a volume law, as in Page's formula.
- **Phases of matter.** In two dimensions, a constant term $-\gamma$ in the area law detects topological order (Kitaev and Preskill 2006; Levin and Wen 2006).
- **Black holes.** Page's formula is the basis of the "Page curve" for the entropy of radiation from an evaporating black hole.

### History

Bennett, Bernstein, Popescu and Schumacher (1996) showed that $S(\rho_A)$ is the rate of entanglement concentration and dilution, which made it the standard measure for pure states, and Popescu and Rohrlich (1997) proved its uniqueness. Bennett, DiVincenzo, Smolin and Wootters (1996) and others then defined measures for mixed states. Page (1993) found the mean entropy of random states. Vidal (2003), Hastings (2007) and Calabrese and Cardy (2004) linked the entropy to simulation cost and to many-body physics.

## References
