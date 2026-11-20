---
title: DSMC conserves momentum and energy and collides pairs at the kinetic rate
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform random numbers. Particles have unit mass. This proof covers what the algorithm does exactly: the conservation laws, the collision law of hard spheres and the rate at which NTC collides pairs. The convergence of DSMC to a kinetic equation is a theorem of Wagner (1992), cited on the page and not proved here.

**Lemma 1 (conservation).** Line L10 keeps $v_i + v_j$ and $|v_i|^2 + |v_j|^2$, and the relative speed $|v_i - v_j| = g$.

*Proof.* After line L10, $v_i + v_j = 2 v_{cm}$, which is the old sum. The new relative velocity is $v_i - v_j = g n$ with $|n| = 1$, so its length is $g$. Then $|v_i|^2 + |v_j|^2 = 2|v_{cm}|^2 + \frac{1}{2}|v_i - v_j|^2 = 2|v_{cm}|^2 + \frac{1}{2}g^2$, the same before and after, because the identity $|a|^2 + |b|^2 = \frac{1}{2}|a + b|^2 + \frac{1}{2}|a - b|^2$ holds for all vectors. $\square$

Line L1 does not change velocities, and the sort of line L2 does not change anything. So the total momentum and the total kinetic energy of the particles change only by boundary conditions, for example at walls or open faces. In a periodic box they are exact invariants.

**Lemma 2 (hard spheres scatter isotropically).** For two hard spheres of diameter $d$, the differential cross section in the centre of mass frame is $d\sigma/d\Omega = d^2/4$ for every scattering angle, and the total cross section is $\pi d^2$.

*Proof.* In the centre of mass frame the relative motion is a point that reflects specularly from a sphere of radius $d$. With impact parameter $b \in [0, d]$, the angle of incidence $\beta$ on the sphere satisfies $\sin\beta = b/d$, and the deflection is $\chi = \pi - 2\beta$, so $b = d\cos(\chi/2)$. The classical formula $d\sigma/d\Omega = \frac{b}{\sin\chi}\big|\frac{db}{d\chi}\big|$ gives $\frac{d\cos(\chi/2)}{\sin\chi} \cdot \frac{d}{2}\sin(\chi/2) = \frac{d^2}{4}$, using $\sin\chi = 2\sin(\chi/2)\cos(\chi/2)$. The integral over the sphere is $4\pi d^2/4 = \pi d^2$. $\square$

So, given that a pair collides, the new direction of the relative velocity is uniform on the sphere, which is line L9, and the relative speed is kept, which is line L10 by Lemma 1.

**Lemma 3 (pair choice).** Line L5 picks an unordered pair uniformly among the $\binom{N_c}{2}$ pairs of the cell.

*Proof.* The first particle is uniform among the $N_c$ particles. The second is uniform among the other $N_c - 1$ particles (the implementation draws an index among the first $N_c - 1$ and replaces the first particle by the last one). So each ordered pair of distinct particles has probability $1/(N_c(N_c - 1))$, and each unordered pair has probability $2/(N_c(N_c - 1)) = 1/\binom{N_c}{2}$. $\square$

**Theorem (the NTC rate).** Consider one candidate in a cell and suppose $(\sigma_T g)_{\max} \ge \sigma_T g_{ij}$ for all pairs of the cell. The probability that this candidate is the pair $\{i, j\}$ and collides is $\sigma_T g_{ij} / \big(\binom{N_c}{2} (\sigma_T g)_{\max}\big)$. If the velocities do not change during the step, the expected number of collisions of the pair $\{i, j\}$ among the $M_0 = \frac{1}{2}N_c(N_c - 1) F_N (\sigma_T g)_{\max} \Delta t / V_c$ candidates is

$$F_N \sigma_T g_{ij} \frac{\Delta t}{V_c},$$

which is the collision probability of the pair in time $\Delta t$ in the stochastic model of a gas in which every pair of molecules in the cell collides at the rate $\sigma_T g_{ij} / V_c$ and each simulated particle stands for $F_N$ molecules. The expected total number of collisions in the cell is $\frac{1}{2} N_c (N_c - 1) F_N \overline{\sigma_T g}\, \Delta t / V_c$, where $\overline{\sigma_T g}$ is the mean over the pairs.

*Proof.* By Lemma 3 the candidate is $\{i, j\}$ with probability $1/\binom{N_c}{2}$, and line L8 accepts it with probability $\sigma_T g_{ij}/(\sigma_T g)_{\max} \le 1$ using an independent uniform number. The product is the first claim. With $M_0$ candidates the expected count is $M_0$ times this probability, $\frac{1}{2}N_c(N_c - 1) F_N (\sigma_T g)_{\max} \frac{\Delta t}{V_c} \cdot \frac{2}{N_c(N_c - 1)} \cdot \frac{\sigma_T g_{ij}}{(\sigma_T g)_{\max}} = F_N \sigma_T g_{ij} \frac{\Delta t}{V_c}$. Summing over the pairs gives the total. $\blacksquare$

**The carry.** Line L4 draws $\lfloor M_0 + \text{carry} \rfloor$ candidates and keeps the fractional part. By induction, after $s$ steps the number of candidates drawn is the sum of the $s$ values $M_0$ minus the current carry, which lies in $[0, 1)$. So the mean number of candidates per step equals the mean of $M_0$ up to an error below $1/s$.

**What is not exact.** The theorem is for fixed velocities. In a step, earlier collisions change the velocities of later candidates, which is a time discretization error of order $\Delta t$ per step for the collision part. If the bound $(\sigma_T g)_{\max}$ is too small, a pair with a larger $\sigma_T g$ is accepted with probability 1 instead of a larger value, and its rate is too small until line L7 raises the bound. Collision partners anywhere in a cell, instead of at the same point, are the reason why the limit of Wagner's theorem is a mollified Boltzmann equation; the cell size error is studied in the paper of Alexander, Garcia and Alder cited on the page.

**The equilibrium rate.** For a Maxwellian at temperature $T$, the relative velocity of two independent molecules is Maxwellian with mass $m/2$, so $\langle g \rangle = \sqrt{8kT/(\pi m/2)} = 4\sqrt{kT/(\pi m)}$. With the theorem, the expected number of collisions in a cell per step is $\frac{1}{2}N_c(N_c - 1) F_N \sigma_T \langle g \rangle \Delta t / V_c$, which is the value of the example and of the test.
