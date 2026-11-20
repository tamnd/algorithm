---
tag: 7W42N2
kind: algorithm
slug: kahn-compton-sampling
name: "Kahn's method for Compton scattering"
aliases:
- Klein-Nishina sampling
area: scientific-computing/particle-transport
level: advanced
summary: Samples the energy and angle of a Compton scattered photon from the Klein-Nishina law by mixing two simple densities and rejecting, with no square roots or tables.
model: real-ram
complexity:
  vars: {N: the number of samples}
  time: {average: O(N)}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true, exact: true, iterative: true}
history:
  year: 1954
  people: [Herman Kahn]
  note: Kahn gave the method in his 1954 RAND report on applications of Monte Carlo. Production photon codes still use it at low and medium energies.
prereqs: [rejection-sampling, inverse-transform-sampling]
see_also: [rejection-sampling, inverse-transform-sampling, analog-monte-carlo-transport, free-flight-sampling, alias-method, random-variate-generation, volumetric-path-tracing, monte-carlo-integration]
sources:
  - url: "https://www.osti.gov/biblio/4353680"
    title: Herman Kahn, Applications of Monte Carlo, RAND Corporation report AECU-3259, 1954 (revised 1956 as RM-1237-AEC)
    locator: Section 23, the Klein-Nishina scattering formula
  - paper: doi:10.1007/BF01366453
    title: O. Klein and Y. Nishina, Über die Streuung von Strahlung durch freie Elektronen nach der neuen relativistischen Quantendynamik von Dirac, Zeitschrift für Physik 52, 1929, 853-868
    locator: the cross section for the scattering of a photon by a free electron
  - book: isbn:9780849360749
    title: Ivan Lux and Laszlo Koblinger, Monte Carlo Particle Transport Methods, Neutron and Photon Calculations, CRC Press, 1991
    locator: the chapter on photon transport, with the sampling of Compton scattering
  - book: isbn:9783527407606
    title: Malvin H. Kalos and Paula A. Whitlock, Monte Carlo Methods, second edition, Wiley-VCH, 2008
    locator: Chapter 3 (sampling random variables), composition and rejection
---

Kahn's method samples the scattering of a photon by a free electron at rest (Compton scattering) from the Klein-Nishina cross section. The photon energy before and after, in units of the electron rest energy $mc^2 = 510.999$ keV, are $\alpha$ and $\alpha'$, and the method samples the ratio $q = \alpha/\alpha'$, which lies in $[1, 1 + 2\alpha]$; the scattering angle then follows from the Compton formula. It writes the target density as a mixture of two densities that are easy to sample by [inverse transform sampling](/inverse-transform-sampling/) and uses [rejection sampling](/rejection-sampling/) in each branch, with acceptance factors that are at most 1. The accepted samples have exactly the Klein-Nishina law. Each try needs three uniform numbers and a few arithmetic operations, with no square roots, logarithms or tables, and about 60 percent of the tries are accepted at the energies of nuclear medicine and reactor shielding. Other algorithms sample the same law (Koblinger's direct method, table methods with the [alias method](/alias-method/)); this page is about Kahn's scheme.

## In plain words

When an X-ray or gamma ray hits an electron, it bounces off in a new direction and loses some energy. A small angle means a small loss, and a back bounce means the largest loss. A physics formula from 1929 gives how likely each angle is.

A simulation must pick a random angle that follows this formula. There is no simple trick that turns one random number into such an angle. Kahn's method makes a guess from one of two simple shapes, chosen at random, and then keeps or throws away the guess with a test. Guesses that are kept follow the formula exactly. More than half of the guesses are kept at the usual energies, and every step uses only additions, multiplications and divisions.

## The problem

A photon of energy $E$ scatters off a free electron at rest. Write $\alpha = E/(mc^2)$ and $\mu = \cos\theta$ for the cosine of the scattering angle. The Compton formula gives the energy after the scattering, $\alpha' = \alpha/(1 + \alpha(1 - \mu))$, so $q = \alpha/\alpha' = 1 + \alpha(1 - \mu)$ runs from $1$ (forward, $\mu = 1$) to $1 + 2\alpha$ (backward, $\mu = -1$). The Klein-Nishina cross section per unit solid angle is

$$\frac{d\sigma}{d\Omega} = \frac{r_e^2}{2} \Big(\frac{\alpha'}{\alpha}\Big)^2 \Big(\frac{\alpha'}{\alpha} + \frac{\alpha}{\alpha'} - 1 + \mu^2\Big),$$

with $r_e$ the classical electron radius. With $d\Omega = 2\pi\, d\mu$ and $d\mu = -dq/\alpha$, the density of $q$ on $[1, 1 + 2\alpha]$ is proportional to

$$f(q) = \frac{1}{q^2}\Big(q + \frac{1}{q} - 1 + \mu^2\Big), \qquad \mu = 1 - \frac{q - 1}{\alpha}.$$

The task is to draw $q$ (and so $\mu$ and $\alpha'$) with this density, for any $\alpha > 0$. The azimuth of the new direction is uniform on $[0, 2\pi)$ and is sampled separately. In the limit $\alpha \to 0$ the law becomes the Thomson law with density proportional to $1 + \mu^2$ in $\mu$.

## The algorithm

```pseudo id=main
KAHN(α)                                   ▷ α = E / (m c²) > 0
L1  loop
L2      draw ξ_1, ξ_2, ξ_3 uniform in [0, 1)
L3      if ξ_1 ≤ (1 + 2α) / (9 + 2α) then        ▷ branch 1
L4          q ← 1 + 2α ξ_2                       ▷ uniform on [1, 1 + 2α]
L5          if ξ_3 ≤ 4 (1/q - 1/q²) then accept
L6      else                                     ▷ branch 2
L7          q ← (1 + 2α) / (1 + 2α ξ_2)          ▷ density proportional to 1/q² on [1, 1 + 2α]
L8          μ ← 1 - (q - 1)/α; if ξ_3 ≤ (μ² + 1/q) / 2 then accept
L9  return α' = α / q and μ = 1 - (q - 1)/α
```

Branch 1 proposes $q$ uniformly; the factor $4(1/q - 1/q^2) = 4(q - 1)/q^2$ has its maximum 1 at $q = 2$, so it is a valid acceptance probability. Branch 2 proposes $q$ with density proportional to $1/q^2$, by inverse transform sampling: the distribution function of that density on $[1, 1 + 2\alpha]$ inverts to line L7. Its factor $(\mu^2 + 1/q)/2$ is at most 1. The branch weights $(1 + 2\alpha)/(9 + 2\alpha)$ and $8/(9 + 2\alpha)$ make the sum of the two accepted densities proportional to $f$, as the proof shows.

## Example

**Hand trace with $\alpha = 1$** (a 511 keV photon). The weight of branch 1 is $3/11 = 0.272727$.

| try | $\xi_1$ | branch | $\xi_2$ | $q$ | $\mu$ | test | result |
|---|---|---|---|---|---|---|---|
| 1 | 0.5 | 2 | 0.25 | $3/1.5 = 2$ | 0 | $\xi_3 = 0.6 \le (0 + 0.5)/2 = 0.25$? | reject |
| 2 | 0.2 | 1 | 0.5 | $1 + 1 = 2$ | 0 | $\xi_3 = 0.9 \le 4(0.5 - 0.25) = 1$? | accept |

The photon scatters at 90 degrees with $\alpha' = 1/2$: it leaves with $255.5$ keV, and the electron takes the other half. A back scattering of the same photon ($\mu = -1$) gives $q = 3$ and $170.3$ keV.

**The acceptance rate.** The probability that one try is accepted is $\frac{4(1 + 2\alpha)}{2\alpha(9 + 2\alpha)} \int_1^{1 + 2\alpha} f(q)\, dq$. Numerical integration gives:

| $\alpha$ | $E$ | accepted fraction |
|---|---|---|
| 0.01 | 5.1 keV | 0.591 |
| 0.1 | 51 keV | 0.585 |
| 1 | 511 keV | 0.627 |
| 2 | 1.02 MeV | 0.644 |
| 5 | 2.55 MeV | 0.589 |
| 10 | 5.11 MeV | 0.474 |
| 100 | 51.1 MeV | 0.110 |

As $\alpha \to 0$ the fraction tends to $32/54 = 0.593$. At high energy the law is strongly forward and the two proposal shapes fit it badly, so the method gets slow; codes switch to another sampler there.

**Moments.** Numerical integration of $f$ gives the exact mean of $\mu$: $0.0686$ for $\alpha = 0.1$, $0.2914$ for $\alpha = 1$ and $0.4477$ for $\alpha = 5$, so the scattering gets more forward as the energy grows. With $10^5$ samples of Kahn's method at $\alpha = 1$ (`random.Random(1)`) the sample mean is $0.2912$, within the statistical error of about $0.0019$. At $\alpha = 10^{-4}$ the exact mean of $\mu^2$ is the Thomson value $2/5$.

## Correctness

The claim is a theorem: the accepted $q$ has the density $f(q)/\int f$ on $[1, 1 + 2\alpha]$ for every $\alpha > 0$, so the method is exact. The reason is a short computation. Branch 1 has the proposal density $1/(2\alpha)$ and the acceptance $4(q - 1)/q^2$. Branch 2 has the proposal density $(1 + 2\alpha)/(2\alpha q^2)$ and the acceptance $(\mu^2 + 1/q)/2$. With the branch weights, the density of an accepted $q$ in one try is

$$\frac{4(1 + 2\alpha)}{2\alpha(9 + 2\alpha)} \cdot \frac{1}{q^2}\Big(q - 1 + \mu^2 + \frac{1}{q}\Big),$$

which is a constant times $f(q)$. A rejected try starts afresh, so the accepted value has the normalised density. The full proof is below.

## Complexity

Each try costs three uniform numbers and $O(1)$ arithmetic, with no transcendental functions. The number of tries is geometric with success probability $p(\alpha)$ from the table, so the expected cost of one sample is $1/p(\alpha)$ tries: about 1.6 tries for $\alpha \le 5$ and about 9 at $\alpha = 100$. A run of $N$ samples costs $O(N)$ in expectation for a fixed $\alpha$, with $O(1)$ space.

## Properties

- **Exact.** No table, fit or truncation; the law is exact up to rounding.
- **Cheap per try.** Only additions, multiplications and divisions. This mattered in 1954 and still matters on hardware where logarithms are slow.
- **Valid for all energies.** The acceptance factors are at most 1 for every $\alpha > 0$, but the efficiency falls at high energy.
- **Free electrons only.** It samples the Klein-Nishina law for an electron at rest. Binding effects need a correction.

## Variants and improvements

- **Koblinger's method.** Koblinger wrote $f$ as a mixture of four terms that can each be sampled exactly by inversion, with no rejection. Codes use it at higher energies, where Kahn's method is slow.
- **Bound electrons.** Multiply the Klein-Nishina law by an incoherent scattering function $S(x, Z)$ of the momentum transfer, and reject with $S/S_{\max}$ after Kahn's step. This lowers forward scattering at low energy.
- **Doppler broadening.** For bound electrons with a momentum distribution, sample the electron momentum from the Compton profile and correct the scattered energy.
- **Tables.** Tabulate the inverse distribution function in $q$ for a grid of $\alpha$ and interpolate, or use the [alias method](/alias-method/) on a fine grid. This is fast but approximate.
- **Other rejection schemes.** Butcher and Messel wrote another mixture with rejection for their shower calculations, and the EGS codes use a scheme of that type.

## When to use it

Use Kahn's method to sample free-electron Compton scattering in photon transport at energies up to a few MeV, for example in shielding, medical physics and gamma-ray detector codes. At higher energies use Koblinger's direct method or a table. Where binding matters (low energies, high atomic number), add the incoherent scattering function correction.

## Pitfalls

- **The wrong density.** The density in $\mu$ and the density in $q$ differ by the factor $d\mu/dq = -1/\alpha$, which is constant, so they have the same shape; but a density in $\theta$ needs the factor $\sin\theta$. Mixing these up gives the wrong angles.
- **The direction update.** The sampled $\mu$ is the cosine relative to the old direction. The new direction must be built by rotating the old one by $\theta$ and a uniform azimuth, not set to $\mu$ along a fixed axis.
- **Units.** $\alpha$ is the energy in units of $mc^2 = 0.510999$ MeV. Using MeV directly gives a wrong law.
- **Small $\alpha$.** Line L8 divides by $\alpha$. For $\alpha$ near the smallest positive float the rounding of $\mu$ is poor; use the Thomson limit there.
- **The weights of the branches.** The weight of branch 1 is $(1 + 2\alpha)/(9 + 2\alpha)$, not $1/2$. With wrong weights the method is still a valid sampler of some law, so tests on ranges do not catch the error; compare moments with the exact law.

## Implementations

## History

Oskar Klein and Yoshio Nishina derived the cross section in 1929 from Dirac's equation. Herman Kahn, then at RAND, collected the sampling methods for Monte Carlo transport in his 1954 report Applications of Monte Carlo, and Section 23 of the report gives the rejection scheme for the Klein-Nishina formula. The method went into the photon codes of the following decades. Koblinger gave a direct sampling method for photon energies above 1.4 MeV in 1975, and some codes use both, with Kahn's method at the lower energies.

## References
