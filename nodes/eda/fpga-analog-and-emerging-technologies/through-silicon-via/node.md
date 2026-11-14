---
tag: WNHTQG
kind: definition
slug: through-silicon-via
name: Through-silicon via
aliases:
- TSV
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: A vertical metal connection through the silicon substrate of a stacked die, large and with keep-out zones, whose count and placement 3D IC tools must plan.
prereqs: [three-dimensional-integrated-circuit]
see_also: [tier-partitioning, thermal-driven-3d-floorplanning, shrunk-2d, compact-thermal-model, elmore-delay, static-timing-analysis]
sources:
  - paper: doi:10.1109/TED.2009.2034508
    title: "Guruprasad Katti, Michele Stucchi, Kristin De Meyer and Wim Dehaene, Electrical modeling and characterization of through silicon via for three-dimensional ICs, IEEE Transactions on Electron Devices 57(1), 256 to 262, 2010"
    locator: the resistance, the oxide and depletion capacitance and the inductance of a TSV as functions of its geometry and materials, checked against field solvers and measurements, and the lumped TSV model (general locator)
  - paper: "Jae-Seok Yang, Krit Athikulwongse, Young-Joon Lee, Sung Kyu Lim and David Z. Pan, TSV stress aware timing analysis with applications to 3D-IC layout optimization, Proceedings of the 47th ACM/IEEE Design Automation Conference (DAC 2010), Anaheim, pages 803 to 806"
    title: TSV stress aware timing analysis with applications to 3D-IC layout optimization
    locator: Section 3 (Formula 2, the Lame stress solution; a TSV of radius 1.5 um with a 0.5 um keep-out zone; above 200 MPa outside the keep-out zone, about 100 MPa 1 um from its edge; Formula 3, the mobility change with channel direction; linear superposition over many TSVs) and the introduction (up to 7.2% hole mobility loss at 100 MPa longitudinal stress)
  - paper: doi:10.1109/ECTC.2009.5074079
    title: "K. H. Lu, X. Zhang, S.-K. Ryu, J. Im, R. Huang and P. S. Ho, Thermo-mechanical reliability of 3-D ICs containing through silicon vias, Proceedings of the 59th Electronic Components and Technology Conference (ECTC 2009), San Diego, pages 630 to 634"
    locator: the analytical stress solution around a TSV from the thermal mismatch of copper and silicon, and its comparison with finite element analysis (general locator)
  - paper: doi:10.1145/2627369.2627642
    title: "Shreepad Panth, Kambiz Samadi, Yang Du and Sung Kyu Lim, Design and CAD methodologies for low power gate-level monolithic 3D ICs, Proceedings of the International Symposium on Low Power Electronics and Design (ISLPED 2014)"
    locator: Section 4 (a monolithic inter-tier via of 100 nm diameter, 2 ohm and 0.1 fF, against a face-to-face via of 500 nm)
  - book: isbn:9781441995414
    title: Sung Kyu Lim, Design for High Performance, Low Power, and Reliable 3D Integrated Circuits, Springer, 2013 (doi 10.1007/978-1-4419-9542-1)
    locator: Chapter 13 (mechanical reliability analysis and optimization) and Chapter 16 (chip and package co-analysis of stress-induced timing variations); the TSV models used in physical design (general locator)
---

A through-silicon via (TSV) is a vertical conductor, usually copper, that goes through the thinned silicon substrate of a die and joins the front side of the die to the back side. It is the vertical link of a stacked [3D IC](/three-dimensional-integrated-circuit/) and of a silicon interposer. A thin insulating liner separates it from the silicon. A TSV is much larger than a gate and much larger than a normal via, it adds capacitance to the net that uses it, and its thermal stress changes the speed of the transistors near it. So a 3D design tool keeps a zone around each TSV free of cells, and it counts and places the TSVs as a cost.

## Definition

**Geometry.** A TSV is a cylinder of conductor with radius $R$ and height $L$, where $L$ is the thickness of the thinned substrate, inside a liner of oxide with thickness $t_{ox}$. Typical values are a few micrometers for $R$ and tens of micrometers for $L$. A TSV takes area on every die that it passes through, and a landing pad on each end.

**Keep-out zone.** The keep-out zone (KOZ) of a TSV is the ring around it in which no cell may be placed. Its width is a design rule. Yang, Athikulwongse, Lee, Lim and Pan (DAC 2010) use a KOZ of 0.5 µm from the edge of a TSV of radius 1.5 µm, because the silicon near the TSV may crack or carry very high stress. The area that a TSV costs a placer is the area of the TSV and its KOZ, not of the TSV alone.

**Electrical model.** The resistance of the conductor is

$$R_{\mathrm{TSV}} = \frac{\rho L}{\pi R^2},$$

with $\rho$ the resistivity of the conductor. The conductor, the liner and the silicon form a coaxial capacitor, and the capacitance of the liner is

$$C_{ox} = \frac{2 \pi \varepsilon_{ox} L}{\ln\left((R + t_{ox}) / R\right)}.$$

In silicon the liner is part of a MOS structure, so a depletion capacitance forms in series with $C_{ox}$ and lowers the total; Katti, Stucchi, De Meyer and Dehaene (IEEE TED 2010) model it, together with the inductance, and give a lumped RLC model of the TSV. For timing, the TSV is one more RC segment of the net, used in the same way as a wire segment in the [Elmore delay](/elmore-delay/).

**Thermal stress.** Copper expands with heat several times more than silicon. A TSV is filled at a high temperature, and when the die cools, the mismatch leaves stress in the silicon around it. For a long cylinder, the Lamé solution gives the radial stress at distance $r \ge R$ from the center as

$$\sigma_{rr}(r) = -\frac{B \, \Delta\alpha \, \Delta T}{2} \left( \frac{R}{r} \right)^{2},$$

where $B$ is the biaxial modulus, $\Delta\alpha$ the difference of the thermal expansion coefficients of copper and silicon, and $\Delta T$ the difference between the annealing temperature and the operating temperature. This is the form that Yang et al. take from Lu et al. (ECTC 2009); they use $\Delta T = 175\,^\circ\mathrm{C}$ (200 °C annealing, 25 °C room). The tangential stress has the same size and the opposite sign. The stress decays with $1/r^2$, so it is large only within a few radii of the TSV.

**Effect on transistors.** Stress changes carrier mobility by the piezoresistive effect. Yang et al. use $\Delta\mu / \mu = -\Pi \, \sigma_{rr} \, \alpha(\theta)$, where $\Pi$ is the piezoresistive coefficient and $\alpha(\theta)$ depends on the angle between the transistor channel and the direction to the TSV. Electron mobility rises under tensile stress. Hole mobility falls or rises with the direction: they report a loss of up to 7.2% at 100 MPa of longitudinal stress, which slows a PMOS transistor. The stress of several TSVs is added by linear superposition. A cell on a critical path next to a TSV can therefore miss timing unless the timing analysis uses the changed mobility.

## Examples and non-examples

**Example (electrical).** A copper TSV with $R = 2.5$ µm, $L = 50$ µm and $t_{ox} = 0.2$ µm, with $\rho = 1.68 \times 10^{-8}$ Ω m and $\varepsilon_{ox} = 3.9 \varepsilon_0$, has

$$R_{\mathrm{TSV}} = \frac{1.68 \times 10^{-8} \cdot 50 \times 10^{-6}}{\pi (2.5 \times 10^{-6})^2} \approx 43 \text{ m}\Omega, \qquad C_{ox} = \frac{2 \pi \cdot 3.9 \cdot 8.854 \times 10^{-12} \cdot 50 \times 10^{-6}}{\ln(2.7 / 2.5)} \approx 141 \text{ fF}.$$

The resistance is small. The capacitance is the load of roughly a hundred small gate inputs (assuming about 1 fF each), before the depletion capacitance lowers it. This is why a net through a TSV needs a stronger driver, and why a partitioner tries to keep the number of TSVs low.

**Example (stress).** Take $R = 1.5$ µm and a KOZ of 0.5 µm, as in Yang et al. Relative to the stress at the TSV wall, the factor $(R/r)^2$ is $1$ at $r = 1.5$ µm, $0.5625$ at the edge of the KOZ ($r = 2$ µm) and $0.25$ at $r = 3$ µm, 1 µm past the KOZ. The ratio between the last two is $0.25 / 0.5625 \approx 0.44$. This agrees with the values they report: above 200 MPa at the KOZ edge and about 100 MPa 1 µm farther out.

**Non-example: a monolithic inter-tier via.** In a monolithic 3D IC the upper tier is grown on the lower one, and the tiers are joined by monolithic inter-tier vias that go through a thin layer, not through a substrate. Panth et al. (ISLPED 2014) assume a diameter of 100 nm. It is a normal via in size and needs no KOZ, so gate-level partitioning such as [Shrunk-2D](/shrunk-2d/) can use one for almost every cut net.

**Non-example: a face-to-face bond.** Two dies bonded with their top metal layers facing each other connect through bond pads or hybrid bonds between the metals. No conductor goes through silicon, so it is not a TSV, although a face-to-face stack still needs TSVs to reach the outside or a third die.

**Non-example: a thermal TSV.** A *thermal* TSV has the same structure but carries no signal. It is placed to lead heat down to the sink. It is a TSV by this definition; what changes is the use, and a thermal model treats it as a column of high conductance.

## Related definitions

- **[Three-dimensional integrated circuit](/three-dimensional-integrated-circuit/)**: the stack in which TSVs are the vertical links; it compares TSVs, face-to-face bonds and monolithic vias.
- **[Tier partitioning](/tier-partitioning/)**: the step that decides which nets cross tiers, so it sets the number of TSVs.
- **Keep-out zone**: defined above; it is the area cost of a TSV in placement.
- **[Compact thermal model](/compact-thermal-model/)**: the thermal network in which signal and thermal TSVs appear as vertical conductances.
- **[Elmore delay](/elmore-delay/)** and **[static timing analysis](/static-timing-analysis/)**: where the RC of a TSV and the stress-changed delay of nearby cells enter the timing.

## References
