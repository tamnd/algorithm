---
tag: JDCYVP
kind: algorithm
slug: cloud-in-cell-assignment
name: Cloud-in-cell assignment
aliases:
- cloud-in-cell scheme
- CIC assignment
area: scientific-computing/n-body-and-particle-methods
level: core
summary: Spreads each particle's charge or mass over the nearest grid points with linear weights, and uses the same weights to interpolate the field back, so no particle feels its own field.
model: real-ram
complexity:
  vars: {N: the number of particles, M: the number of grid points}
  time: {worst: "Θ(N + M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, conservative: true, order: "2"}
history:
  year: 1969
  people: [Charles K. Birdsall, Dieter Fuss]
  note: Birdsall and Fuss introduced clouds-in-cells for plasma simulation in 1969; Hockney and Eastwood placed it between NGP and TSC in a family of assignment functions.
prereqs: [lagrange-interpolation]
see_also: [particle-mesh-method, plasma-particle-in-cell, p3m-method, particle-in-cell, partition-of-unity, poisson-equation, particle-mesh-ewald]
sources:
  - book: isbn:9780852743928
    title: Roger W. Hockney and James W. Eastwood, Computer Simulation Using Particles, Adam Hilger, 1988
    locator: Chapter 5 (the particle-mesh force calculation, the assignment functions NGP, CIC and TSC, momentum conservation and the self-force)
  - book: isbn:9780750310253
    title: Charles K. Birdsall and A. Bruce Langdon, Plasma Physics via Computer Simulation, Taylor and Francis, 2004 (reprint of the IOP edition of 1991)
    locator: Part 1, the chapter on the numerical methods of the program ES1 (linear weighting), and Part 2, the chapter on the effects of the spatial grid
  - paper: doi:10.1016/0021-9991(69)90058-8
    title: Charles K. Birdsall and Dieter Fuss, Clouds-in-clouds, clouds-in-cells physics for many-body plasma simulation, Journal of Computational Physics 3(4), 1969, 494-511
    locator: the clouds-in-cells method and its lower noise compared with nearest grid point assignment
---

Cloud-in-cell (CIC) assignment is the step of a [particle-mesh method](/particle-mesh-method/) that moves charge or mass from particles to a grid, and moves the grid field back to the particles. Each particle is a uniform cloud one cell wide, and the part of the cloud that falls in the cell of a grid point goes to that point. In one dimension this gives linear weights to the 2 nearest grid points, in two dimensions bilinear weights to 4 points, and in three dimensions trilinear weights to 8 points. When the same weights are used in both directions, the total charge is kept exactly and the total force on all particles is zero, so no particle pushes itself. The graphics [particle-in-cell](/particle-in-cell/) transfer of velocities uses the same bilinear weights; this page treats the weights as part of a field solver, where the conservation of charge and momentum is what makes the result accurate.

## In plain words

Particles sit anywhere, but a fast field solver needs values on a grid. So each particle shares its charge with the grid points next to it. A particle close to a point gives most of its charge to that point, and a particle halfway between two points gives each one half.

After the solver finds the field on the grid, each particle reads the field back by the same rule: it mixes the values of the same points in the same shares. Using one rule in both directions is important. It makes the push from a particle on the others balance the push from the others on it, so the particles cannot speed up all together, and a lone particle stays at rest.

## The problem

The input is a periodic grid of $M$ points $x_j = j\,\Delta x$, $j = 0, \ldots, M - 1$, on $[0, L)$ with $\Delta x = L / M$, and $N$ particles with positions $x_i$ and charges $q_i$ (masses on gravity pages). The first output is the grid density

$$\rho_j = \frac{1}{\Delta x} \sum_{i=1}^{N} q_i \, W(x_i - x_j), \qquad W(s) = \max\Bigl(0, \; 1 - \frac{|s|}{\Delta x}\Bigr),$$

with $x_i - x_j$ taken over the periodic images. The second output, for a grid field $E_j$, is the field at each particle, $E(x_i) = \sum_j W(x_i - x_j) E_j$. The function $W$ is the overlap of a cloud of width $\Delta x$ centred at $x_i$ with the cell $[x_j - \Delta x/2, x_j + \Delta x/2]$, divided by $\Delta x$. Hockney and Eastwood write the assignment function as $W$ and call this choice CIC; nearest grid point (NGP) and triangular shaped cloud (TSC) are its neighbours of lower and higher order.

## The algorithm

```pseudo id=main
CIC-DEPOSIT(x[1..N], q[1..N], M, L)
L1  dx ← L / M;  ρ[j] ← 0 for j = 0, ..., M - 1
L2  for i ← 1 to N do
L3      s ← x[i] / dx;  j ← ⌊s⌋;  w ← s - j          ▷ 0 ≤ w < 1
L4      ρ[j mod M] ← ρ[j mod M] + q[i] (1 - w) / dx
L5      ρ[(j + 1) mod M] ← ρ[(j + 1) mod M] + q[i] w / dx
L6  return ρ

CIC-INTERPOLATE(E[0..M-1], x[1..N], L)
L7  for i ← 1 to N do
L8      s ← x[i] / dx;  j ← ⌊s⌋;  w ← s - j          ▷ the same j and w as in L3
L9      E_i ← (1 - w) E[j mod M] + w E[(j + 1) mod M]
L10 return (E_1, ..., E_N)
```

Line L3 finds the grid point $j$ to the left of the particle and the fraction $w$ of a cell from that point to the particle. Lines L4 and L5 split the charge in the shares $1 - w$ and $w$; the point nearer to the particle gets the larger share. Division by $\Delta x$ turns a charge into a charge per length. Line L9 reads the field with the same two shares. In two dimensions, lines L3 to L5 run in each direction, and the 4 products $(1 - w_x)(1 - w_y)$, $w_x (1 - w_y)$, $(1 - w_x) w_y$ and $w_x w_y$ are the weights.

## Example

Take $M = 4$ and $L = 4$, so $\Delta x = 1$ and the grid points are 0, 1, 2 and 3. Three particles have $(x, q) = (0.25, 1)$, $(1.5, 2)$ and $(3.75, 1)$.

| particle | $j$ | $w$ | to point $j$ | to point $j + 1$ |
|---|---|---|---|---|
| $x = 0.25$, $q = 1$ | 0 | 0.25 | 0.75 to point 0 | 0.25 to point 1 |
| $x = 1.5$, $q = 2$ | 1 | 0.5 | 1 to point 1 | 1 to point 2 |
| $x = 3.75$, $q = 1$ | 3 | 0.75 | 0.25 to point 3 | 0.75 to point 0 (periodic) |

So $\rho = (1.5, 1.25, 1, 0.25)$, and $\sum_j \rho_j \Delta x = 4 = \sum_i q_i$.

Now solve for a field on the grid. In normalized units, Gauss's law $dE/dx = \rho - \bar\rho$ with $\bar\rho = 1$, differenced as $E_{j+1/2} - E_{j-1/2} = \Delta x (\rho_j - \bar\rho)$ with a mean-free $E$ and $E_j = (E_{j-1/2} + E_{j+1/2}) / 2$, gives $E = (-0.25, 0.125, 0.25, -0.125)$. This is minus the centred difference of the potential of the 3-point Laplacian. Lines L7 to L9 give the fields $-0.15625$, $0.1875$ and $-0.21875$ at the three particles. The forces $q_i E_i$ are $-0.15625$, $0.375$ and $-0.21875$, and their sum is exactly 0.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It shows four facts. Lines L3 to L5 compute $\rho_j = \sum_i q_i W(x_i - x_j) / \Delta x$ exactly. The weights of one particle add to 1, so $\sum_j \rho_j \Delta x = \sum_i q_i$ exactly, in rational arithmetic and up to rounding in floating point. Line L9 is exact for every field that is linear between two grid points. And if the grid field is $E_j = \sum_k K_{j - k} \rho_k$ with an odd kernel, $K_{-m} = -K_m$, then the total force $\sum_i q_i E(x_i)$ is zero; for a single particle this sum is its self-force, so the self-force is zero.

The key step is a change of the order of summation: $\sum_i q_i E(x_i) = \sum_i q_i \sum_j W(x_i - x_j) E_j = \Delta x \sum_j \rho_j E_j$, which uses the same $W$ in L4, L5 and L9.

## Complexity

In the [real-RAM](/real-ram/) model, line L1 costs $\Theta(M)$ and each particle costs $O(1)$ in lines L3 to L5 and in lines L8 and L9. So a deposit and an interpolation cost $\Theta(N + M)$ time in each case, and $\Theta(M)$ extra space for the grid. In $d$ dimensions each particle touches $2^d$ grid points, which gives $\Theta(2^d N + M)$. The cost of the whole force step is that of the field solver, for example $O(M \log M)$ with the [fast Fourier transform](/fast-fourier-transform/) on the [particle-mesh method](/particle-mesh-method/) page.

## Properties

- **Charge is conserved exactly.** The two shares of each particle add to 1.
- **Momentum is conserved.** With the same weights in both directions and an odd field kernel, the forces sum to zero, and a lone particle feels no force from its own charge (Hockney and Eastwood, chapter 5).
- **Continuous density.** The density at each grid point is a continuous, piecewise linear function of the particle position. With NGP the density jumps when a particle crosses a cell boundary, which makes the force jump and adds noise.
- **Not smooth.** The CIC force is continuous, but its derivative jumps when a particle crosses a grid point. TSC has a continuous derivative.
- **Second order interpolation.** Line L9 is linear interpolation, with an error of $O(\Delta x^2)$ for a smooth field.
- **Not translation invariant.** The force between two particles at a fixed separation depends a little on where the pair sits relative to the grid. This error is largest for separations of one or two cells, and is one source of grid heating in plasma codes (Birdsall and Langdon, Part 2).

## Variants and improvements

- **Nearest grid point (NGP).** All the charge goes to the nearest point. It costs one point per particle in each direction, but the force jumps by a large amount when a particle crosses a cell boundary.
- **Triangular shaped cloud (TSC).** The cloud is a triangle of width $2 \Delta x$, which gives quadratic weights on 3 points in each direction. The force has a continuous first derivative and less aliasing noise, at a cost of $3^d$ points per particle.
- **Higher order B-splines.** NGP, CIC and TSC are the B-splines of order 1, 2 and 3. Higher orders are used in [smooth particle mesh Ewald](/smooth-particle-mesh-ewald/) and in the [P3M method](/p3m-method/).
- **Deconvolution.** In Fourier space, the CIC weight is $\operatorname{sinc}^2(k \Delta x / 2)$ in each direction. Dividing the density by this factor, or folding it into the Green's function, reduces the smoothing of short waves.
- **Charge-conserving current deposit.** Electromagnetic PIC codes deposit the current with weights that satisfy the discrete continuity equation, so that Gauss's law stays true without a correction step.

## When to use it

Use CIC as the default in a [particle-mesh method](/particle-mesh-method/) or a [plasma particle-in-cell](/plasma-particle-in-cell/) code. It is the least costly scheme with a continuous force, and its noise is much lower than that of NGP (Birdsall and Fuss 1969). Use TSC or a higher order spline when the force must be smooth or when aliasing noise matters, for example in cosmological runs and in particle mesh Ewald. Use NGP only when the cost per particle must be as low as possible.

## Pitfalls

- **Different weights in the two directions.** Depositing with CIC in lines L4 and L5 but interpolating with NGP in line L9 breaks the identity $\sum_i q_i E(x_i) = \Delta x \sum_j \rho_j E_j$. The particles then feel self-forces and the total momentum drifts. Use the same $j$ and $w$ in line L8 as in line L3.
- **A wrong floor for negative positions.** Using truncation toward zero in line L3, as `int(s)` does, gives $w < 0$ for a particle at $x < 0$. Use the floor, or wrap the position into $[0, L)$ first.
- **Forgetting to divide by $\Delta x$.** Lines L4 and L5 give a density. Without the division, the field solver receives a charge per cell, and every field is off by the factor $\Delta x$.
- **The periodic seam.** For a particle in the last cell, point $j + 1$ is point 0. Without the reduction mod $M$, the program writes outside the array.
- **An even kernel.** The momentum identity needs an odd field kernel. A one-sided difference of the potential gives a kernel that is not odd, and then the self-force is not zero even with CIC.

## Implementations

## History

Birdsall and Fuss (1969) introduced the clouds-in-cells method for plasma simulation, and showed that it has much less noise than nearest grid point assignment. Hockney and Eastwood (1988) treat NGP, CIC and TSC as one family of assignment functions, and derive the conditions for momentum conservation and for a zero self-force.

## References
