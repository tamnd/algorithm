---
tag: G0GPRB
kind: problem
slug: crystallographic-phase-problem
name: Crystallographic phase problem
aliases:
- phase problem of crystallography
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: core
summary: Find the phases of the structure factors of a crystal from the measured diffraction intensities, which give only their magnitudes.
model: real-ram
prereqs: [phase-retrieval, discrete-fourier-transform, autocorrelation, lattice]
see_also: [patterson-function, direct-methods-crystallography, charge-flipping, coherent-diffraction-imaging, phase-retrieval-ambiguities, oversampling-in-phase-retrieval, difference-map, single-particle-reconstruction]
sources:
  - paper: doi:10.1103/PhysRev.46.372
    title: A. L. Patterson, A Fourier series method for the determination of the components of interatomic distances in crystals, Physical Review 46(5), 1934, 372 to 376
    locator: the Fourier series with the squared amplitudes as coefficients and its peaks at interatomic vectors (general locator)
  - paper: doi:10.1107/S0365110X50000446
    title: J. Karle and H. Hauptman, The phases and magnitudes of the structure factors, Acta Crystallographica 3(3), 1950, 181 to 187
    locator: the inequalities among structure factors that follow from a nonnegative density (general locator)
  - paper: doi:10.1107/S0365110X52000137
    title: D. Sayre, The squaring method, a new method for phase determination, Acta Crystallographica 5(1), 1952, 60 to 65
    locator: the relation between the structure factors of a density of equal, resolved atoms and of its square (general locator)
  - paper: doi:10.1107/S0365110X52002276
    title: D. Sayre, Some implications of a theorem due to Shannon, Acta Crystallographica 5(6), 1952, 843
    locator: the sampling of the diffraction pattern only at the Bragg peaks and the information between them (general locator)
  - paper: doi:10.1126/science.8451639
    title: Russ Miller, George T. DeTitta, Rob Jones, David A. Langs, Charles M. Weeks and Herbert A. Hauptman, On the application of the minimal principle to solve unknown structures, Science 259(5100), 1993, 1430 to 1433
    locator: the dual space method that alternates phase refinement and peak picking (general locator)
  - paper: doi:10.1107/S0108767303027569
    title: Gabor Oszlanyi and Andras Suto, Ab initio structure solution by charge flipping, Acta Crystallographica A 60(2), 2004, 134 to 141
    locator: the charge flipping algorithm (general locator)
  - book: isbn:9780198500728
    title: Carmelo Giacovazzo, Direct Phasing in Crystallography, Fundamentals and Applications, Oxford University Press, 1998
    locator: the phase problem, structure invariants, origin choice and the probabilistic theory of direct methods (general locator)
---

The crystallographic phase problem is the task of finding the phases of the structure factors of a crystal when a diffraction experiment gives only their magnitudes. A crystal diffracts X-rays, electrons or neutrons into sharp Bragg reflections, one for each point $h$ of the reciprocal lattice. The amplitude of reflection $h$ is the Fourier coefficient $F(h)$ of the periodic density in the crystal, and the detector measures the intensity $|F(h)|^2$. Without the phases, the Fourier series of the density cannot be summed. It is the case of [phase retrieval](/phase-retrieval/) for a periodic object sampled only at the Bragg peaks, and it was the central obstacle of structure determination for decades.

## In plain words

A crystal is a pattern of atoms that repeats in three directions. Shine X-rays at it and the rays leave only in certain directions, each making a bright spot. Each spot belongs to one wave in a sum of waves that adds up to a map of the atoms. The spot tells how strong its wave is. It does not tell where the crests of the wave lie, and that is the phase. With wrong phases, the same waves add up to a wrong map.

So the phase problem asks: from the brightness of all the spots, find the positions of the crests, and with them the atoms. The facts that help are that the map can never be negative, that it is made of round atoms, and that there are far more spots than atoms.

## Definition

**Crystal and structure factors.** A crystal has a unit cell with fractional coordinates $x \in [0, 1)^3$ and an electron density $\rho(x)$ that repeats with the cell. For each integer index $h = (h, k, l)$, the structure factor is the Fourier coefficient
$$F(h) = V \int_{[0,1)^3} \rho(x)\, e^{2\pi i\, h \cdot x}\, dx, \qquad \rho(x) = \frac{1}{V} \sum_h F(h)\, e^{-2\pi i\, h \cdot x},$$
with the sign convention of crystallography, which is the opposite of the [DFT](/discrete-fourier-transform/); nothing below depends on the sign. For $N$ atoms with scattering factors $f_j(h)$ at positions $x_j$, $F(h) = \sum_j f_j(h)\, e^{2\pi i\, h \cdot x_j}$.

**Input.** The magnitudes $|F(h)|$ for the reflections $h$ in a finite set $H$, usually all $h$ inside a resolution sphere $|h^*| \le 1/d_{\min}$ in reciprocal space, except a few that are too weak, too strong or hidden. Also known: the cell, the symmetry (space group) and the chemical composition. $F(0)$, the total number of electrons, follows from the composition.

**Output.** Phases $\varphi(h)$ such that the density $\rho$ with coefficients $|F(h)| e^{i\varphi(h)}$ is a physically sensible density: nonnegative, made of separated atoms of the right number and kind, with the right symmetry.

**Ambiguities.** For a real density, $F(-h) = \overline{F(h)}$ (Friedel's law, when absorption is negligible), and the data do not change under:

- a shift of the origin by $t$, which multiplies $F(h)$ by $e^{2\pi i\, h \cdot t}$; with symmetry only the shifts that keep the symmetry elements in allowed places count;
- the inversion $\rho(x) \to \rho(-x)$, which conjugates all $F(h)$ (the enantiomorph).

These are the trivial ambiguities. Combinations of phases that do not change under any origin shift, such as $\varphi(h) + \varphi(k) + \varphi(-h-k)$, are called structure invariants, and only these are fixed by the structure alone.

## Variants

- **Centrosymmetric crystals.** If the structure has a center of symmetry at the origin, every $F(h)$ is real, and each phase is $0$ or $\pi$. The problem becomes a sign problem with one sign for each independent reflection.
- **Small molecules and macromolecules.** For crystals with up to a few hundred atoms in the asymmetric unit and data to atomic resolution, ab initio methods usually solve the problem from the magnitudes alone. For proteins, data rarely reach atomic resolution, and extra experiments or a model are needed.
- **Experimental phasing.** Extra data change the problem: heavy atoms soaked into the crystal (isomorphous replacement), or data at several wavelengths near an absorption edge (anomalous dispersion), give differences of magnitudes from which the phases follow by geometry once the heavy atoms are found.
- **Molecular replacement.** A known similar structure is placed in the cell by a search over rotations and translations, and its phases start the refinement.
- **Powder data.** The reflections overlap in one dimension, so even the magnitudes $|F(h)|$ must be partly recovered.
- **Non-crystalline objects.** For an isolated object, the intensity can be sampled between the Bragg positions, which makes the problem much better posed; this is [coherent diffraction imaging](/coherent-diffraction-imaging/).

## Examples

- **Two atoms in one dimension.** With equal atoms at $x_1$ and $x_2$, $|F(h)|^2 = 2f^2\big(1 + \cos 2\pi h (x_1 - x_2)\big)$. The data fix only the distance $x_1 - x_2$, and every pair at that distance fits. Here all solutions are related by the trivial ambiguities.
- **Homometric structures.** Two point sets with the same multiset of differences have the same $|F|$ for equal atoms. The one-dimensional sets $\{0, 1, 3, 10, 11, 13, 30, 31, 33\}$ and $\{0, 1, 3, 20, 21, 23, 30, 31, 33\}$ are of this kind: they are $A + B$ and $A - B$ (after a shift) for $A = \{0, 1, 3\}$ and $B = \{0, 10, 30\}$, so their difference multisets agree, but neither is a shift or a reflection of the other (a theorem; it is checked by listing the 72 differences). So the magnitudes alone do not always determine the structure even up to the trivial ambiguities.
- **The wrong phases.** The density with the true magnitudes and random phases is spread over the cell with many negative values, while the density with the true magnitudes and phases has a few sharp peaks. The constraints of positivity and atomicity are what pick the right phases.

## Known algorithms

- **[Patterson methods](/patterson-function/).** The Fourier series with coefficients $|F(h)|^2$ is the autocorrelation of the density, with peaks at the vectors between atoms. For a few heavy atoms among light ones, their positions can be read from it, and their contribution gives starting phases (Patterson 1934).
- **[Direct methods](/direct-methods-crystallography/).** Positivity and atomicity imply inequalities and probability relations among the phases (Karle and Hauptman 1950, Sayre 1952). The triplet relation $\varphi(h) + \varphi(k) + \varphi(-h-k) \approx 0$ for strong reflections, the tangent formula and multisolution searches solve most small molecule structures.
- **Dual space methods.** Shake-and-Bake (Miller and coworkers 1993) alternates phase refinement in reciprocal space with picking peaks in real space, and extends direct methods to larger structures.
- **[Charge flipping](/charge-flipping/).** An iterative projection method that changes the sign of weak density and imposes the measured magnitudes (Oszlanyi and Suto 2004). It needs no symmetry and no atom types.
- **Iterative projection methods** from optics, such as the [difference map](/difference-map/), with a constraint of atomicity or of a known density histogram.
- **Experimental phasing and molecular replacement** for macromolecules, as described under Variants.

## Bounds

- **Information.** The magnitudes determine the Patterson function, the autocorrelation of one cell made periodic, and nothing more. No method can separate structures with the same Patterson function, such as the homometric sets above.
- **No oversampling.** The Bragg reflections sample the transform at the reciprocal lattice, which is exactly the sampling of one cell. The autocorrelation, which is twice as wide as the content of a cell, wraps around and overlaps itself. This is why the support constraint of [oversampling](/oversampling-in-phase-retrieval/) is not available for a crystal (Sayre 1952), and why crystallography relies on atomicity instead.
- **Counting.** At atomic resolution the number of independent reflections is many times the number of atomic coordinates, so the problem is heavily overdetermined in practice (a heuristic count, not a uniqueness proof).
- **Complexity.** No algorithm with a proved polynomial bound is known for the general problem with the atomicity constraint. The methods above are heuristics whose success is a measurement on known structures.

## Reductions

- **To phase retrieval.** The crystal problem is Fourier phase retrieval of a periodic signal sampled at the Bragg peaks, with prior knowledge of atomicity in place of a support.
- **To a point set from its differences.** For equal point atoms, the Patterson function gives the multiset of differences of the positions, so finding the structure is the problem of rebuilding a point set from its difference multiset (in one dimension, the turnpike problem).
- **Centrosymmetric case to a sign problem.** The phases are $0$ or $\pi$, so the search space is finite, with $2^m$ sign choices for $m$ independent reflections, and probability relations such as $s(h)\, s(k)\, s(h+k) \approx +1$ guide the search.
- **To a feasibility problem.** Charge flipping and the difference map treat the problem as finding a point in the intersection of the set of densities with the measured magnitudes and the set of atomic or nonnegative densities, a nonconvex [feasibility problem](/convex-feasibility-problem/).

## Applications

- **Chemistry and mineralogy.** The structures of small molecules, salts and minerals are solved routinely from the magnitudes alone.
- **Structural biology.** The structures of proteins and nucleic acids come from crystallography with experimental phasing or molecular replacement, and they underlie drug design.
- **Materials science.** Structures of new compounds, including modulated and incommensurate crystals, are solved by charge flipping and direct methods.
- **Diffraction imaging.** The phase problem for non-crystalline objects led to [coherent diffraction imaging](/coherent-diffraction-imaging/), which borrows the name and the algorithms and adds oversampling.

## References
