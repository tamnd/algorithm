---
tag: R8N0ZK
kind: concept
slug: bloch-sphere
name: Bloch sphere
aliases:
- Bloch representation
area: quantum/quantum-primitives
level: intro
summary: "The Bloch sphere maps the pure states of one qubit to the points of the unit sphere in R^3 and the mixed states to the inside of the ball. One-qubit gates act as rotations."
prereqs: [qubit]
see_also: [pauli-gates, hadamard-gate, phase-and-t-gates, density-matrix, mixed-state, unitary-operator, vector-rotation, quantum-state-tomography]
sources:
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.2 (the Bloch sphere picture of a qubit), Section 4.2 (single qubit operations and rotation operators) and Section 2.4 (the Bloch vector of a density matrix)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 1 (qubits) and Appendix A.9 (Pauli matrices)
  - paper: doi:10.1103/PhysRev.70.460
    title: F. Bloch, Nuclear induction, Physical Review 70, 1946, pages 460 to 474
    locator: the vector model of a spin one-half in a magnetic field, the origin of the name
---

The *Bloch sphere* is a picture of the states of one [qubit](/qubit/) as points of the unit ball in $\mathbb{R}^3$. The pure state $\cos(\theta/2)|0\rangle + e^{i\varphi}\sin(\theta/2)|1\rangle$ is the point with polar angle $\theta$ and azimuth $\varphi$ on the surface, and the mixed states are the points inside. Orthogonal states are antipodal points, one-qubit [unitary](/unitary-operator/) gates are rotations of the ball, and the three coordinates of a point are the expected values of the three [Pauli](/pauli-gates/) measurements.

## In plain words

A qubit has infinitely many possible states, but up to a phase that no experiment can see, two real numbers describe a pure state. These two numbers are a latitude and a longitude. So each pure state of a qubit is a place on the surface of a globe. The north pole is the state zero and the south pole is the state one. Points on the equator are equal mixes of zero and one that differ only in phase. Two states that can be told apart with certainty sit at opposite places on the globe. A gate on one qubit turns the globe. Noise and lack of knowledge move a state from the surface toward the center, and the center is a fair coin. The picture works only for a single qubit; there is no globe of this kind for two or more qubits.

## The idea

**Pure states.** Every unit vector $a|0\rangle + b|1\rangle$ equals, up to a global phase, the vector

$$|\psi\rangle = \cos\tfrac{\theta}{2}\,|0\rangle + e^{i\varphi}\sin\tfrac{\theta}{2}\,|1\rangle, \qquad 0 \le \theta \le \pi, \quad 0 \le \varphi < 2\pi.$$

To get the angles, multiply by $e^{-i\arg a}$ so that the first amplitude is real and nonnegative, then $\theta = 2\arctan(|b|/|a|)$ and $\varphi = \arg b - \arg a$. At the poles $\theta = 0$ and $\theta = \pi$, the azimuth $\varphi$ is undefined. The *Bloch vector* of $|\psi\rangle$ is the point

$$\vec r = (\sin\theta\cos\varphi,\ \sin\theta\sin\varphi,\ \cos\theta) = \bigl(2\,\mathrm{Re}(\bar a b),\ 2\,\mathrm{Im}(\bar a b),\ |a|^2 - |b|^2\bigr).$$

The right-hand form needs no angles and does not change when $a$ and $b$ are multiplied by a common phase. The map from states to points is a bijection between pure states (unit vectors up to phase) and the unit sphere $S^2$.

**The coordinates are Pauli expectations.** $x = \langle\psi|X|\psi\rangle$, $y = \langle\psi|Y|\psi\rangle$ and $z = \langle\psi|Z|\psi\rangle$. A measurement in the computational basis gives $0$ with probability $\cos^2(\theta/2) = (1 + z)/2$. In the same way a measurement in the basis $|\pm\rangle$ gives $+$ with probability $(1 + x)/2$.

**The cardinal points.**

| point | state | $(\theta, \varphi)$ |
|---|---|---|
| $(0, 0, 1)$ | $\lvert 0\rangle$, north pole | $(0, \text{any})$ |
| $(0, 0, -1)$ | $\lvert 1\rangle$, south pole | $(\pi, \text{any})$ |
| $(1, 0, 0)$ | $\lvert +\rangle = (\lvert 0\rangle + \lvert 1\rangle)/\sqrt{2}$ | $(\pi/2, 0)$ |
| $(-1, 0, 0)$ | $\lvert -\rangle = (\lvert 0\rangle - \lvert 1\rangle)/\sqrt{2}$ | $(\pi/2, \pi)$ |
| $(0, 1, 0)$ | $\lvert {+i}\rangle = (\lvert 0\rangle + i\lvert 1\rangle)/\sqrt{2}$ | $(\pi/2, \pi/2)$ |
| $(0, -1, 0)$ | $\lvert {-i}\rangle = (\lvert 0\rangle - i\lvert 1\rangle)/\sqrt{2}$ | $(\pi/2, 3\pi/2)$ |

**Angles are halved.** For two pure states with Bloch vectors $\vec r$ and $\vec s$, $|\langle\phi|\psi\rangle|^2 = (1 + \vec r \cdot \vec s)/2$. So orthogonal states have $\vec r \cdot \vec s = -1$: they are antipodal, at an angle of $\pi$ on the sphere, although as vectors in $\mathbb{C}^2$ they are at a right angle. $|0\rangle$ and $|1\rangle$ are the two poles. This halving is the reason for $\theta/2$ in the formula.

**Mixed states are inside the ball.** A [density matrix](/density-matrix/) of one qubit is

$$\rho = \tfrac{1}{2}(I + x X + y Y + z Z), \qquad \vec r = (x, y, z) = (2\,\mathrm{Re}\,\rho_{10},\ 2\,\mathrm{Im}\,\rho_{10},\ \rho_{00} - \rho_{11}),$$

and its eigenvalues are $(1 \pm |\vec r|)/2$. So $\rho$ is a density matrix exactly when $|\vec r| \le 1$, it is pure exactly when $|\vec r| = 1$, and $\operatorname{tr}\rho^2 = (1 + |\vec r|^2)/2$. The center $\vec r = 0$ is $I/2$, the maximally [mixed state](/mixed-state/). A mixture $p\rho + (1-p)\sigma$ has the Bloch vector $p\vec r + (1-p)\vec s$, so the ball is convex and the pure states are its extreme points.

**Gates are rotations.** For a unit vector $\hat n$ and an angle $\alpha$, the rotation operator is

$$R_{\hat n}(\alpha) = e^{-i\alpha(\hat n \cdot \vec\sigma)/2} = \cos\tfrac{\alpha}{2}\,I - i\sin\tfrac{\alpha}{2}\,(n_x X + n_y Y + n_z Z).$$

It turns the Bloch ball by the angle $\alpha$ about the axis $\hat n$, in the positive sense. Every one-qubit unitary is $e^{i\gamma} R_{\hat n}(\alpha)$ for some $\gamma$, $\hat n$ and $\alpha$, so up to a global phase every gate is a rotation of the ball. The map from $U$ to its rotation $R$ with $R_{ij} = \tfrac{1}{2}\operatorname{tr}(\sigma_i U \sigma_j U^\dagger)$ is the double cover $SU(2) \to SO(3)$: $U$ and $-U$ give the same rotation.

## Examples

- **Pauli gates.** $X = i R_x(\pi)$, $Y = i R_y(\pi)$ and $Z = i R_z(\pi)$ are half turns about the three axes ([Pauli gates](/pauli-gates/)). $X$ swaps the poles.
- **Hadamard.** $H$ is the half turn about the axis $(1, 0, 1)/\sqrt{2}$, between $x$ and $z$. It maps $(x, y, z)$ to $(z, -y, x)$, so it swaps $|0\rangle$ with $|+\rangle$ and $|1\rangle$ with $|-\rangle$ ([Hadamard gate](/hadamard-gate/)).
- **Phase gates.** $R_z(\alpha)$ adds $\alpha$ to the azimuth $\varphi$ and leaves $\theta$ unchanged. $S$ is a quarter turn and $T$ an eighth of a turn about the $z$ axis, up to a global phase ([phase and T gates](/phase-and-t-gates/)). They change only the relative phase, so the probabilities $|a|^2$ and $|b|^2$ stay the same.
- **A worked point.** $\tfrac{3}{5}|0\rangle + \tfrac{4i}{5}|1\rangle$ has $\bar a b = \tfrac{12i}{25}$, so $\vec r = (0, \tfrac{24}{25}, -\tfrac{7}{25})$, with $|\vec r|^2 = \tfrac{576 + 49}{625} = 1$. The angles are $\cos\theta = -\tfrac{7}{25}$ and $\varphi = \pi/2$.
- **Decoherence.** Dephasing noise shrinks $x$ and $y$ and keeps $z$, so the state moves toward the $z$ axis. Amplitude damping moves every point toward the north pole $|0\rangle$. Both are [quantum channels](/quantum-channel/), and they map the ball into itself.
- **Not for two qubits.** The pure states of two qubits form a space of real dimension $6$, not $2$, and the mixed states have $15$ real parameters. There is no ball picture with rotations for them, and the Bloch vector of one qubit of an entangled pair lies strictly inside the ball.

### Implementation

The file `impl/python/bloch_sphere.py` converts between amplitudes, angles and Bloch vectors, between Bloch vectors and density matrices, and builds $R_{\hat n}(\alpha)$ and its $3 \times 3$ rotation matrix. Its tests compare the angle form with the amplitude form of $\vec r$ for 200 random angles with a fixed seed, and check that orthogonal states are antipodal, that $|\langle\phi|\psi\rangle|^2 = (1 + \vec r \cdot \vec s)/2$, that mixtures lie inside the ball, that $H$ maps $(x, y, z)$ to $(z, -y, x)$, and that a global phase does not move the point.

## Where it is used

- Designing and reading one-qubit gates and pulse sequences: a gate is an axis and an angle. The Euler decomposition $U = e^{i\alpha}R_z(\beta)R_y(\gamma)R_z(\delta)$ of the [unitary operator](/unitary-operator/) page is a statement about rotations of the ball.
- Nuclear magnetic resonance and spin physics, where Bloch introduced the vector picture of a spin in a magnetic field.
- [Quantum state tomography](/quantum-state-tomography/) of one qubit: estimate $x$, $y$ and $z$ from measurements of $X$, $Y$ and $Z$, which gives $\rho$.
- Noise models, which act as maps of the ball into itself, and the geometry of [trace distance](/trace-distance/), which for one qubit is half the Euclidean distance between Bloch vectors.

### Common errors

- Using $\theta$ instead of $\theta/2$ in the amplitudes. Then $|0\rangle$ and $|1\rangle$ would be at an angle of $\pi/2$ and the map would not be one to one.
- Reading the sphere as the state space of $\mathbb{C}^2$. The sphere is the space of rays; the unit vectors of $\mathbb{C}^2$ form the 3-sphere $S^3$, and a global phase is a circle in it.
- Expecting gates to act on the angle $\theta$ alone. A rotation about an axis in the equatorial plane changes both angles.

## References
