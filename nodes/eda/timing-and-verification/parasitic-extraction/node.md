---
tag: ZQFSDE
kind: problem
slug: parasitic-extraction
name: Parasitic extraction
aliases:
- RC extraction
- interconnect parasitic extraction
area: eda/timing-and-verification
level: advanced
summary: Compute the resistances, capacitances and sometimes inductances of the wires of a layout, as an RC network for timing and signal integrity.
prereqs: [circuit-extraction, rc-tree, poisson-equation]
see_also: [floating-random-walk-capacitance, elmore-delay, prima, asymptotic-waveform-evaluation, model-order-reduction, static-timing-analysis, gmres, krylov-subspace]
sources:
  - paper: doi:10.1109/43.97624
    title: K. Nabors and J. White, FastCap, a multipole accelerated 3-D capacitance extraction program, IEEE Transactions on Computer-Aided Design 10(11), 1447 to 1459, 1991
    locator: the capacitance matrix of a set of conductors, the boundary element formulation with panels, the iterative solution with GMRES, and the multipole acceleration of the matrix-vector product
  - paper: doi:10.1016/0038-1101(92)90332-7
    title: Y. L. Le Coz and R. B. Iverson, A stochastic algorithm for high speed capacitance extraction in integrated circuits, Solid-State Electronics 35(7), 1005 to 1012, 1992
    locator: the floating random walk method for the capacitance of integrated circuit conductors (general locator)
  - paper: doi:10.1109/TCAD.2012.2224346
    title: Wenjian Yu, Hao Zhuang, Chao Zhang, Gang Hu and Zhi Liu, RWCap, a floating random walk solver for 3-D capacitance extraction of very-large-scale integration interconnects, IEEE Transactions on Computer-Aided Design 32(3), 353 to 366, 2013
    locator: a floating random walk extractor for layered dielectrics, with its comparison against field solvers
  - paper: doi:10.1063/1.1697872
    title: W. C. Elmore, The transient response of damped linear networks with particular regard to wideband amplifiers, Journal of Applied Physics 19(1), 55 to 63, 1948
    locator: the delay as the first moment of the impulse response, used on the extracted RC network
  - paper: "Altan Odabasioglu, Mustafa Celik and Lawrence T. Pileggi, PRIMA: passive reduced-order interconnect macromodeling algorithm, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 17(8), 645 to 654, 1998"
    locator: the passive reduction of the extracted RLC network by a congruence transform with a Krylov basis
  - paper: "M. Kamon, M. J. Tsuk and J. K. White, FASTHENRY, a multipole-accelerated 3-D inductance extraction program, IEEE Transactions on Microwave Theory and Techniques 42(9), 1750 to 1758, 1994"
    locator: the partial inductances of wire filaments and their multipole-accelerated solution
---

Parasitic extraction computes the electrical effect of the wires of a chip. Its input is the layout geometry of the nets that [circuit extraction](/circuit-extraction/) found, with the process data: the thickness and the resistivity of each metal layer and the permittivity of each dielectric. Its output is a network of resistors and capacitors, and at high frequency also inductors, that stands for the wires in simulation and in [static timing analysis](/static-timing-analysis/). In EDA "extraction" means this problem or netlist extraction. In mechanical CAD the same word means feature extraction from a solid model, which is a different problem. The core numerical task is the capacitance of a set of conductors, which is a boundary value problem of the [Poisson equation](/poisson-equation/) type.

## In plain words

A wire on a chip is not a perfect connection. It resists the current a little, and it stores charge, both to the ground below it and to the wires next to it. These small unwanted effects are the parasitics. They make signals slow, and a fast change on one wire can push a glitch onto its neighbor.

Parasitic extraction measures them. The resistance of a wire follows from its length, its width and its metal. The capacitance is harder, because the electric field spreads around the wire in three dimensions and every nearby wire changes it. The result is a model of each net as many small resistors and capacitors, which a timing tool can use to compute how late each signal arrives.

## Definition

**Input.** A set of conductors $\Omega_1, \dots, \Omega_m$ in space (the wires and vias of the nets, as boxes or polygons with thickness), a dielectric $\varepsilon(x)$ around them, usually in layers, a resistivity for each conductor layer, and an accuracy target.

**Capacitance.** Put potential $V_j$ on conductor $j$ and let $\phi$ satisfy $\nabla \cdot (\varepsilon \nabla \phi) = 0$ outside the conductors, $\phi = V_j$ on $\Omega_j$, and $\phi \to 0$ at infinity or $\phi = 0$ on a grounded box. The charge on conductor $i$ is $Q_i = -\oint_{\partial \Omega_i} \varepsilon \, \partial \phi / \partial n \, dS$, with $n$ the normal into the dielectric. The map from $V$ to $Q$ is linear, $Q = C V$, and the $m \times m$ matrix $C$ is the *capacitance matrix*. The coupling capacitance between $i$ and $j \ne i$ is $-C_{ij}$.

**Resistance.** For a wire of uniform cross-section, $R = \rho L / (W t) = R_s L / W$, where $R_s = \rho / t$ is the sheet resistance and $L / W$ is the number of squares. For general shapes it comes from the Laplace equation for the current inside the conductor.

**Output.** For each net an RC network: the net is cut into segments, each segment gets its resistance, and each node gets its capacitance to ground and its coupling capacitances to the nodes of other nets, with the error of each value within the target. With inductance, it is an RLC network with partial inductances.

## Variants

- **Field solver extraction.** Solve the 3D problem directly, by the boundary element method (FastCap), finite differences or finite elements, or by the [floating random walk](/floating-random-walk-capacitance/). This gives reference accuracy at a high cost.
- **Rule-based extraction.** Cut the layout into short pieces, classify each piece by its local pattern (a wire above a plane, two parallel wires, a crossing), and read the capacitance from tables built once per process with a field solver. Full-chip extractors usually work this way, and use field solvers only for the critical nets.
- **2D and 2.5D models.** Use the cross-section of long parallel wires, which reduces the problem to the plane, plus corrections at the ends.
- **Inductance extraction.** Partial inductances of filaments of the wires, for example by FastHenry. They matter for wide, fast wires such as clocks and supplies.
- **Network reduction.** The raw network has millions of nodes. [Model order reduction](/model-order-reduction/), for example [PRIMA](/prima/) or [AWE](/asymptotic-waveform-evaluation/), replaces it with a small network that has the same low-frequency behavior.

## Examples

**One wire.** A wire of length $100\,\mu m$ and width $0.1\,\mu m$ on a layer with sheet resistance $0.08\ \Omega$ per square has $1000$ squares, so $R = 80\ \Omega$. If it lies $0.2\,\mu m$ above a ground plane in oxide with $\varepsilon_r = 3.9$, the parallel plate formula gives $C = \varepsilon_0 \varepsilon_r A / t = 8.854 \times 10^{-12} \cdot 3.9 \cdot 10^{-11} / (2 \times 10^{-7}) \approx 1.727\ \mathrm{fF}$. The real value is larger, because the field also leaves the sides and the top of the wire, and for a wire this narrow that fringe part is not small. This gap is the reason why field solvers and tables exist. With the plate value, $RC \approx 138.1\ \mathrm{fs}$.

**The network and its delay.** Cut the wire into $N$ equal sections, each with $R / N$ in series and $C / N$ at its far end, and drive it from an ideal step at the near end. This is an RC tree model, and the [Elmore delay](/elmore-delay/) at the far end is
$$\sum_{k=1}^{N} \frac{k R}{N} \cdot \frac{C}{N} = RC\,\frac{N + 1}{2N}.$$
A scratch script computed the true 50 percent delay of each ladder by time stepping:

| $N$ | Elmore delay | Elmore in fs | true 50 percent delay |
| --- | --- | --- | --- |
| 1 | $RC$ | 138.1 | $0.69\,RC$ |
| 2 | $\tfrac{3}{4} RC$ | 103.6 | $0.56\,RC$ |
| 4 | $\tfrac{5}{8} RC$ | 86.3 | $0.47\,RC$ |
| 8 | $\tfrac{9}{16} RC$ | 77.7 | $0.43\,RC$ |

As $N$ grows the Elmore delay tends to $RC / 2 \approx 69.1\ \mathrm{fs}$, the value for the distributed line. One lumped section gives twice that value. So the way the extractor cuts the wire changes the delay, and a fine cut is needed for long wires. In every row the Elmore delay is above the true delay, as the theorem for RC trees says.

## Known algorithms

| Method | Idea | What is known |
| --- | --- | --- |
| Dense boundary elements | put unknown charges on panels of the conductor surfaces, collocate the potential, and solve the dense system | $O(N^2)$ memory and per matrix-vector product, $O(N^3)$ for a direct solve, for $N$ panels |
| FastCap | boundary elements with [GMRES](/gmres/) in a [Krylov subspace](/krylov-subspace/), and multipole expansions for the far interactions | $O(N)$ per product for a fixed expansion order on well-spread panels; the number of iterations is measured |
| [Floating random walk](/floating-random-walk-capacitance/) | Monte Carlo walks that jump between empty cubes, no mesh | unbiased with a computable error bar; the walk length is measured |
| Finite differences or finite elements | mesh the dielectric and solve the sparse system with [conjugate gradients](/conjugate-gradient-method/) or multigrid | converges as the mesh is refined; the mesh covers the whole volume |
| Pattern tables | match local geometry against tables precomputed with a field solver | linear in the layout size; the error depends on the table and is measured against field solvers |
| [PRIMA](/prima/), [AWE](/asymptotic-waveform-evaluation/) | reduce the extracted network by matching moments | PRIMA is proved passive; AWE can give unstable models |

## Bounds

**Proved properties of the answer.** $C$ is symmetric, by Green's reciprocity. Its diagonal is positive and its off-diagonal entries are negative or zero, and each row sum is at least zero, with equality when a grounded box encloses all conductors and is itself one of them. These follow from the maximum principle, and they are also checks on any extractor. For an RC tree model driven by a step, the Elmore delay is an upper bound on the 50 percent delay at each node (Gupta and others, 1997). This is not true for general RC meshes or for RLC networks.

**Proved costs.** A dense boundary element system with $N$ panels has $N^2$ entries, so a plain matrix-vector product costs $\Theta(N^2)$ and Gaussian elimination $O(N^3)$. With multipole acceleration at a fixed order, the product costs $O(N)$ for well-spread panels, with an error that falls geometrically in the order. A floating random walk estimate with $n$ walks has a standard error that falls as $1 / \sqrt{n}$.

**What is measured.** How many GMRES iterations FastCap needs, how many jumps a random walk makes, and how close the table values come to a field solver are all reported from experiments, not proved. No nontrivial lower bound is known for the problem beyond the size of the output.

## Reductions

- **From circuit extraction.** The nets come from [circuit extraction](/circuit-extraction/). Parasitic extraction adds values to the connections that it found and does not change them.
- **To a boundary value problem.** Capacitance is the solution of a Laplace problem in the dielectric, the [Poisson equation](/poisson-equation/) with zero source. Resistance is a Laplace problem inside the conductor.
- **To linear systems.** Every field solver ends with a large linear system, solved by Krylov methods such as [GMRES](/gmres/) or the [conjugate gradient method](/conjugate-gradient-method/).
- **To timing.** The RC network goes to [model order reduction](/model-order-reduction/) and then to delay calculation, for example the [Elmore delay](/elmore-delay/) on the [RC tree model](/rc-tree/), and so to [static timing analysis](/static-timing-analysis/).

## Applications

- **Timing sign-off.** Wire delay is a large part of path delay in modern processes, so timing without extracted parasitics is wrong.
- **Signal integrity.** Coupling capacitances give the noise that a switching wire puts on its quiet neighbors, and the extra delay when neighbors switch the other way.
- **Power and supply analysis.** The resistance of the supply network gives the voltage drop, and the capacitance gives the switching power $C V^2 f$ of each net.
- **Clock design.** Clock trees are built and checked with extracted values, as in [clock tree synthesis](/clock-tree-synthesis/).

## References
