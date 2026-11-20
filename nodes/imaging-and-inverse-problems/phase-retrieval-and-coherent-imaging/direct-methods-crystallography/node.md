---
tag: C688GG
kind: technique
slug: direct-methods-crystallography
name: Direct methods in crystallography
aliases:
- Hauptman-Karle direct methods
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: Determine the phases of structure factors from probabilistic relations among them, such as the triplet relation, that follow from atomicity and positivity.
prereqs: [crystallographic-phase-problem, patterson-function, discrete-fourier-transform]
see_also: [charge-flipping, phase-retrieval, central-limit-theorem, convolution-theorem, simulated-annealing, genetic-algorithm, difference-map, coherent-diffraction-imaging]
sources:
  - paper: doi:10.1107/S0365110X50000446
    title: J. Karle and H. Hauptman, The phases and magnitudes of the structure factors, Acta Crystallographica 3(3), 1950, 181 to 187
    locator: the inequalities among structure factors that follow from a nonnegative density, written as determinants (general locator)
  - paper: doi:10.1107/S0365110X52000137
    title: D. Sayre, The squaring method, a new method for phase determination, Acta Crystallographica 5(1), 1952, 60 to 65
    locator: the equation that relates each structure factor to a sum of products of two others, for equal resolved atoms (general locator)
  - paper: "H. Hauptman and J. Karle, Solution of the Phase Problem. I. The Centrosymmetric Crystal, ACA Monograph No. 3, American Crystallographic Association, 1953"
    locator: the probabilistic theory of the phases of centrosymmetric crystals (general locator)
  - paper: doi:10.1107/S0365110X55001485
    title: W. Cochran, Relations between the phases of structure factors, Acta Crystallographica 8(8), 1955, 473 to 478
    locator: the probability distribution of the triplet phase sum (general locator)
  - paper: doi:10.1107/S0365110X56001741
    title: J. Karle and H. Hauptman, A theory of phase determination for the four types of non-centrosymmetric space groups 1P222, 2P22, 3P12, 3P22, Acta Crystallographica 9(8), 1956, 635 to 651
    locator: the tangent formula for non-centrosymmetric crystals (general locator)
  - paper: doi:10.1126/science.8451639
    title: Russ Miller, George T. DeTitta, Rob Jones, David A. Langs, Charles M. Weeks and Herbert A. Hauptman, On the application of the minimal principle to solve unknown structures, Science 259(5100), 1993, 1430 to 1433
    locator: the minimal function and the dual space cycle of Shake-and-Bake (general locator)
  - book: isbn:9780198500728
    title: Carmelo Giacovazzo, Direct Phasing in Crystallography, Fundamentals and Applications, Oxford University Press, 1998
    locator: normalized structure factors, structure invariants, the triplet distribution, the tangent formula and the multisolution approach (general locator)
---

Direct methods find the phases of the structure factors of a crystal from their magnitudes alone, by using relations among the phases that hold because the electron density is nonnegative and made of separated atoms. The central relation is that, for three strong reflections whose indices add to zero, the sum of the three phases is probably close to zero. Starting from a few phases fixed by the choice of origin and a few trial values, the relations extend the phases to all strong reflections, and the Fourier map then shows the atoms. Karle and Hauptman (1950), Sayre (1952) and Cochran (1955) laid the foundations, and direct methods became the standard way to solve the [crystallographic phase problem](/crystallographic-phase-problem/) for small molecules. Hauptman and Karle received the Nobel Prize in Chemistry in 1985 for this work.

## In plain words

The brightness of each X-ray spot of a crystal is known, but the phase of its wave is not. Direct methods use a simple fact: the crystal is made of separate atoms, and the map of atoms is never negative. Not every set of phases can give such a map. For the brightest spots, the phases are tied together in threes: if two of them are known, the third is likely close to a value that follows from them.

So you fix a few phases freely, because the origin of the crystal can be put anywhere, and you guess a few more. The rules of three then give more phases, and those give more again, until all bright spots have a phase. You make a map. If it shows clean atoms, the guess was right. If not, you try other guesses.

## When it applies

- **Atomic resolution.** The data reach a resolution at which the atoms are resolved, often taken as about 1.2 angstrom (a heuristic rule of thumb; the methods degrade gradually). The probability relations assume separated atoms.
- **Few atoms.** The strength of the relations falls as $1/\sqrt{N}$ for $N$ atoms in the cell (a theorem of the probabilistic theory below). Classical direct methods solve structures with up to a few hundred independent atoms; dual space methods reach larger ones.
- **Roughly equal atoms.** The theory is simplest when no atom dominates. A few heavy atoms do not stop the method, but then the [Patterson function](/patterson-function/) is often the easier route.
- **Complete strong data.** The strong reflections at low and medium angles carry the relations. If many of them are missing, for example behind the beam stop or because of overloads, the phase extension breaks down.

## The template

**Normalized structure factors.** Divide each structure factor by its expected size, $E(h) = F(h)/\sqrt{\varepsilon_h \sum_j f_j(h)^2}$, where $\varepsilon_h$ is a small integer that corrects for symmetry and the sum runs over the atoms of the cell. The scale and a mean thermal motion come from a plot of the intensities against the resolution. Then $\langle |E|^2 \rangle = 1$, and $E$ behaves like the structure factor of point atoms at rest.

**The relations.**

- *Positivity (a theorem).* For a nonnegative density and any indices $h_1, \dots, h_m$, the matrix with entries $F(h_i - h_j)$ is Hermitian and positive semidefinite, because $\sum_{i,j} \overline{c_i} c_j F(h_i - h_j) = \int \rho(x) \big|\sum_j c_j e^{-2\pi i\, h_j \cdot x}\big|^2 dx \ge 0$. Its determinants give the inequalities of Karle and Hauptman (1950).
- *Sayre's equation (a theorem for equal, resolved atoms).* If all atoms are equal and do not overlap, $\rho^2$ is a density of the same atoms with a sharper shape, so $F(h) = \frac{\theta(h)}{V} \sum_k F(k)\, F(h - k)$, where $\theta(h)$ is the ratio of the scattering factors of an atom and of a squared atom (Sayre 1952). For strong $F(h)$ the sum is dominated by its large terms, which suggests $\varphi(h) \approx \varphi(k) + \varphi(h - k)$.
- *The triplet distribution (a theorem in the limit of many atoms at random positions).* For $N$ equal atoms, given the three magnitudes, the phase sum $\Phi = \varphi(h) + \varphi(k) + \varphi(-h-k)$ has the density $P(\Phi) \propto \exp(\kappa \cos\Phi)$ with $\kappa = 2|E(h) E(k) E(h+k)|/\sqrt{N}$ (Cochran 1955). The relation $\Phi \approx 0$ is reliable only when $\kappa$ is large.
- *The tangent formula.* Combining all triplets that contain $h$ gives the estimate
$$\tan\varphi(h) = \frac{\sum_k |E(k) E(h - k)| \sin\big(\varphi(k) + \varphi(h - k)\big)}{\sum_k |E(k) E(h - k)| \cos\big(\varphi(k) + \varphi(h - k)\big)},$$
which is applied over and over to extend and refine the phases (Karle and Hauptman 1956).

**The procedure.**

1. Compute $E(h)$, and keep the few hundred reflections with the largest $|E|$.
2. List the triplets among them with large $\kappa$.
3. Fix the origin and, for chiral structures, the enantiomorph, by giving arbitrary phases to a few chosen reflections. This is allowed because the data do not change under these operations.
4. Give trial phases to a few more reflections: random values, or a small set of values for each (the multisolution approach).
5. Extend and refine all phases with the tangent formula until they stop changing.
6. Rank the trial sets by figures of merit, such as the agreement with the triplet relations.
7. For the best sets, compute the Fourier map with coefficients $E(h) e^{i\varphi(h)}$ (an E-map), pick the peaks as atoms, and complete and refine the structure.

Each trial costs a number of tangent cycles, each linear in the number of triplets. The number of trials needed is not known in advance; the success rate per trial is a measurement for each structure.

## Classic examples

- **Centrosymmetric structures.** Each phase is $0$ or $\pi$, a sign $s(h) = \pm 1$, and the triplet relation becomes $s(h) \approx s(k)\, s(h - k)$. With the origin fixed by three signs, the strongest relations give the signs of many reflections in terms of a few symbols, which the early direct methods resolved by hand. The monograph of Hauptman and Karle (1953) treats this case.
- **Routine small molecule crystallography.** Programs built on the tangent formula and the multisolution approach solve most organic and inorganic structures with up to a few hundred atoms from the magnitudes alone.
- **Shake-and-Bake.** Miller and coworkers (1993) alternated a refinement of the phases that minimizes a function of the triplets, the minimal function, with a step in real space that keeps only the strongest peaks of the map as atoms. This dual space cycle solved structures much larger than classical direct methods could.

## Variations

- **Quartet invariants.** Sums of four phases add relations, including some that are probably near $\pi$ (negative quartets), which help in difficult cases.
- **Dual space methods.** Alternate between reciprocal space, where the phases are refined, and real space, where atomicity is imposed by picking peaks. [Charge flipping](/charge-flipping/) is a simpler relative that imposes atomicity by flipping the sign of weak density and uses no probability theory.
- **Global search.** The trial phases can be optimized against figures of merit with [simulated annealing](/simulated-annealing/) or [genetic algorithms](/genetic-algorithm/) in place of random restarts.
- **Direct methods with extra data.** The same relations help to find heavy atoms from difference data in isomorphous replacement or anomalous dispersion, and to extend phases from a partial model.

## Pitfalls

- **Low resolution.** Without resolved atoms the relations lose their basis, and the E-map is noise even with good figures of merit.
- **Bad normalization.** Errors in the scale or the thermal factor distort $|E|$ at high angles and give the wrong reflections the most weight.
- **Missing strong reflections.** Overloaded or hidden strong reflections remove the most reliable triplets.
- **False minima.** A trial can converge to a phase set that satisfies the relations but gives a wrong map, for example a single large peak at the origin with weak features around it. Figures of merit can rank such a solution high; check that the map has a chemically sensible structure.
- **Pseudo-symmetry.** A structure that is close to a higher symmetry or has a near translation produces systematically weak reflections, which breaks the statistics of $|E|$.
- **Wrong space group.** The origin fixing and the relations depend on the symmetry. Solving in $P1$ and finding the symmetry afterwards avoids this, at the cost of more unknowns.

## Exercises

1. Show that the matrix with entries $F(h_i - h_j)$ is positive semidefinite for a nonnegative density, and derive from the $2 \times 2$ case that $|F(h)| \le F(0)$.
2. For a density of equal atoms that do not overlap, show that $\rho^2$ is a sum of equal atoms at the same positions with a sharper shape, and derive Sayre's equation from it.
3. Show that the triplet phase sum $\varphi(h) + \varphi(k) + \varphi(-h-k)$ does not change under a shift of the origin, while a single phase does.
4. Compute $\kappa$ for $N = 50$ and $|E(h)| = |E(k)| = |E(h+k)| = 2$. What is the most probable value of the triplet sum, and how sharp is the distribution?
5. Derive the tangent formula as the phase of the sum $\sum_k E(k) E(h - k)$, and explain why each term is weighted by $|E(k) E(h-k)|$.
6. In a centrosymmetric structure, three reflections are used to fix the origin. Explain why their indices must be independent modulo 2.

## References
