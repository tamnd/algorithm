---
tag: AV5038
kind: technique
slug: condensed-history-method
name: Condensed history method
area: scientific-computing/particle-transport
level: advanced
summary: Groups many small collisions of charged particles into steps sampled from multiple scattering theory, which makes electron transport tractable.
prereqs: [analog-monte-carlo-transport, linear-boltzmann-transport-equation]
see_also: [analog-monte-carlo-transport, free-flight-sampling, kahn-compton-sampling, implicit-capture, operator-splitting, central-limit-theorem]
sources:
  - paper: doi:10.1103/PhysRev.57.24
    title: S. Goudsmit and J. L. Saunderson, Multiple scattering of electrons, Physical Review 57(1), 1940, 24-29
    locator: the exact angular distribution after a path length s as a Legendre series with factors exp(-s/λ_l)
  - paper: doi:10.1103/PhysRev.78.526
    title: H. W. Lewis, Multiple scattering in an infinite medium, Physical Review 78(5), 1950, 526-529
    locator: the exact moments of the angular and spatial distributions after a path length s, including the mean depth λ_1(1 - exp(-s/λ_1))
  - paper: doi:10.1016/S0168-583X(86)80027-1
    title: Alex F. Bielajew and D. W. O. Rogers, PRESTA, the parameter reduced electron-step transport algorithm for electron Monte Carlo transport, Nuclear Instruments and Methods in Physics Research B 18, 1987, 165-181
    locator: the path-length correction, the lateral correlation and the boundary crossing algorithm that remove step-size artefacts
  - paper: doi:10.1016/0306-4549(92)90013-2
    title: Edward W. Larsen, A theoretical derivation of the condensed history algorithm, Annals of Nuclear Energy 19(10-12), 1992, 701-714
    locator: the derivation of the algorithm from the transport equation and its convergence as the step size goes to zero
  - paper: doi:10.1016/S0168-583X(98)00274-2
    title: Iwan Kawrakow and Alex F. Bielajew, On the condensed history technique for electron transport, Nuclear Instruments and Methods in Physics Research B 142, 1998, 253-280
    locator: the analysis of electron-step algorithms and a step algorithm with accurate spatial moments
---

The condensed history method is how Monte Carlo codes transport electrons, positrons and other charged particles. A fast electron loses energy and changes direction in a very large number of collisions with the atoms and their electrons, and most of them change its energy and direction only a little. Following each collision, as [analog Monte Carlo transport](/analog-monte-carlo-transport/) does for neutrons and photons, is far too slow. The condensed history method cuts the path into steps, each containing many collisions, and samples the net effect of each step from a theory of multiple scattering: the energy loss from the stopping power and its straggling, the deflection from the Goudsmit-Saunderson or Molière distribution, and the displacement from a step algorithm. Berger introduced the method and its two classes in 1963. The method is an approximation whose error depends on the step size, so the step algorithm and the treatment of boundaries are the core of every implementation.

## In plain words

A fast electron in matter is like a ball in a pinball machine with millions of tiny pins. Each pin turns it only a little and slows it only a little, but there are so many pins that a computer cannot follow every one.

The condensed history method jumps over many pins at once. Physics tells us how much, on average and in its spread, the ball turns and slows over a stretch of path. So the computer moves the ball a stretch, then turns it and slows it by a random amount from that law, and then moves on.

The catch is that the ball does not really move in a straight line over the stretch. Where it ends up is a guess, and the guess is worse for long stretches and near the walls of the machine.

## When it applies

- The particle has collisions that are very frequent and mostly soft: elastic scattering by nuclei at small angles, and many ionizations and excitations with small energy loss. This is the case for electrons and positrons, and for protons and ions, as long as the energy is high enough for many soft collisions per step.
- A theory gives the distribution of the net effect of the soft collisions over a path length: multiple scattering theory for the angle and a stopping power with straggling for the energy.
- The tallies are on a scale larger than the step: dose in a voxel, energy deposited in a detector, transmission through a foil. Quantities on the scale of single collisions need detailed simulation.

It does not apply to neutral particles, whose collisions are rare and are sampled one by one with [free-flight sampling](/free-flight-sampling/). In a coupled electron-photon code, photons are tracked by analog methods with [Kahn's method](/kahn-compton-sampling/) or similar for Compton scattering, and the electrons they make are tracked by condensed history.

## The template

A condensed history step of a class II scheme: soft collisions are grouped, and hard collisions, those above energy thresholds, are sampled one by one.

```pseudo id=main
CONDENSED-STEP(r, Ω, E)
L1  s_hard ← distance to the next hard collision, by free-flight sampling with the hard cross section
L2  s ← min(s_hard, step limit, distance to the boundary)     ▷ hole: the step-size rule
L3  ΔE ← energy loss over s from the restricted stopping power, with straggling
L4  θ ← a deflection sampled from the multiple scattering law for path s at energy E
L5  move r to the end of the step                                ▷ hole: the step algorithm
L6  Ω ← Ω rotated by θ and a uniform azimuth;  E ← E - ΔE;  deposit ΔE locally
L7  if s = s_hard then sample the hard collision (a knock-on electron, a bremsstrahlung photon) and track the secondary
```

In a class I scheme, used in Berger's ETRAN code, the step ends at a fixed grid of energies, and all collisions, hard ones too, are grouped by sampling the secondaries along the step. Class II schemes, used in EGS, are the common choice in newer codes.

**The angular law.** For a path length $s$ with no energy loss and a scattering cross section $\sigma(\theta)$ per atom in a medium with $N$ atoms per unit volume, Goudsmit and Saunderson showed that the angular distribution is exactly

$$F(\theta, s) = \sum_{l = 0}^\infty \frac{2l + 1}{4\pi}\, e^{-s/\lambda_l}\, P_l(\cos\theta), \qquad \frac{1}{\lambda_l} = N\int \sigma(\theta')\big(1 - P_l(\cos\theta')\big)\, d\Omega',$$

with $P_l$ the Legendre polynomials. So $\langle\cos\theta\rangle = e^{-s/\lambda_1}$, where $\lambda_1$ is the transport mean free path. This is a theorem.

**The step algorithm.** The deflection is a theorem; the position is not. Lewis derived the exact moments of the position: with the initial direction along $z$ and no energy loss, the mean depth after a path $s$ is

$$\langle z\rangle = \lambda_1\big(1 - e^{-s/\lambda_1}\big),$$

which is less than $s$ because the path curves. A step algorithm places the end of the step so that these moments come out right, at least approximately. The simplest algorithm moves straight a distance $s$ along the old direction and then deflects, which gets $\langle z\rangle$ wrong; a path-length correction moves a shorter chord, and a lateral correction moves the end point sideways in the plane of the deflection.

## Classic examples

**The error of a straight step.** For a path of length $s = \lambda_1$ cut into $n$ straight steps of length $\Delta s = s/n$, with a deflection from the exact law at the end of each step, the mean cosine of the direction in step $k$ is $e^{-k\Delta s/\lambda_1}$, because the mean cosines of independent deflections that are symmetric about the axis multiply. So the mean depth is $\Delta s\,(1 - e^{-s/\lambda_1})/(1 - e^{-\Delta s/\lambda_1})$. Compared with the exact $\langle z\rangle = 0.6321\,\lambda_1$ (theorems, computed exactly):

| $n$ | mean depth of the straight steps, in units of $\lambda_1$ | relative error |
|---|---|---|
| 1 | 1.0000 | 58.2% |
| 2 | 0.8033 | 27.1% |
| 5 | 0.6974 | 10.3% |
| 10 | 0.6643 | 5.1% |
| 100 | 0.6353 | 0.5% |

For small steps the error is close to $\Delta s/(2\lambda_1)$, first order in the step size. If each step instead moves the chord $\lambda_1(1 - e^{-\Delta s/\lambda_1})$ along the old direction, the mean depth is exact for every $n$. Higher moments, such as the lateral spread and the correlation of the depth with the final angle, are still wrong, which is why the better step algorithms add a lateral displacement.

**PRESTA.** Bielajew and Rogers found that results of the EGS4 code changed with the step size in thin layers and near interfaces. Their algorithm PRESTA added a path-length correction, a lateral correlation and a boundary crossing algorithm, which shortens steps near a boundary so that the multiple scattering theory is not used across an interface. The results then depended much less on the step size.

**Convergence.** Larsen derived the condensed history algorithm from the transport equation and showed that its solution converges to the solution of the [transport equation](/linear-boltzmann-transport-equation/) as the step size goes to zero, with a rate that depends on how well the step algorithm reproduces the spatial moments. Kawrakow and Bielajew analysed the step algorithms of the codes and built one with accurate spatial moments, so that larger steps give the same accuracy.

## Variations

- **Class I and class II.** Group all collisions on a fixed energy grid (class I), or sample hard collisions individually above thresholds and group the soft ones (class II).
- **The angular law.** The Goudsmit-Saunderson series is exact for a given cross section and any step; Molière's theory is a small-angle approximation that is cheaper and needs a minimum number of collisions per step.
- **Random hinge.** Move a random fraction of the step straight, deflect, and move the rest along the new direction. This reproduces the first moments well with little cost.
- **Mixed or detailed simulation near boundaries.** Switch to collision-by-collision simulation in thin layers or close to interfaces, where the multiple scattering theory does not hold.
- **Energy loss.** The continuous slowing down approximation uses the mean stopping power only; Landau and Vavilov distributions add straggling.

## Pitfalls

- **Step-size artefacts.** Results that change with the step size mean the step algorithm is inaccurate. Check convergence in the step size for each new geometry.
- **Boundary crossing.** A step that crosses an interface uses the multiple scattering law of one medium for a path in two. Shorten steps near boundaries, or stop at the boundary and restart.
- **Too short steps for the angular law.** Molière's theory needs many collisions per step; very short steps break it. The Goudsmit-Saunderson law has no such limit but is more costly.
- **Energy loss in the step.** The cross sections change as the energy falls; a step that loses a large fraction of its energy must use averaged values or be cut.
- **Backscatter.** Low-energy electrons at large angles are where the approximations are worst; backscatter coefficients are a sensitive test.

## Exercises

1. Show from the Goudsmit-Saunderson series that the mean cosine after a path $s$ is $e^{-s/\lambda_1}$ and that the mean of $P_2(\cos\theta)$ is $e^{-s/\lambda_2}$.
2. Prove that the mean cosines of independent deflections that are symmetric about the axis multiply, using the addition theorem of the Legendre polynomials.
3. Derive the mean depth of $n$ straight steps given in the table and show that its relative error is $\Delta s/(2\lambda_1) + O(\Delta s^2)$.
4. Show that the chord $\lambda_1(1 - e^{-\Delta s/\lambda_1})$ makes the mean depth exact for every $n$.
5. For the random hinge method with a uniform hinge point, compute the mean depth of one step to first order in $\Delta s/\lambda_1$.

## References
