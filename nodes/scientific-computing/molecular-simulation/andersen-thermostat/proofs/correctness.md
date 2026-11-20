---
title: The Andersen collisions keep the canonical distribution, and they give an exponential velocity memory
proves: [correctness]
status: full
---

We use the pseudocode of the page. The state is $(x, v)$ with $x, v \in \mathbb{R}^{N d}$. The canonical density is
$$\rho(x, v) = \frac{1}{Z} e^{-\beta (K(v) + U(x))} = \frac{1}{Z_x} e^{-\beta U(x)} \cdot \prod_{i = 1}^{N} \Bigl(\frac{\beta m_i}{2 \pi}\Bigr)^{d/2} e^{-\beta m_i |v_i|^2 / 2},$$
with $\beta = 1 / (k_B T)$ and $K(v) = \sum_i \frac12 m_i |v_i|^2$. So under $\rho$ the positions and the velocities are independent, the velocities of different particles are independent, and each velocity component $v_{i a}$ is normal with mean 0 and variance $k_B T / m_i$: the Maxwell-Boltzmann distribution.

**Claim 1 (one collision keeps $\rho$).** Fix a particle $i$ and a probability $p \in [0, 1]$. Let $C_i$ be the random map that, with probability $p$, replaces $v_i$ by a new vector whose components are independent normals with variance $k_B T / m_i$, independent of everything else, and with probability $1 - p$ changes nothing. If $(x, v)$ has density $\rho$, then $C_i(x, v)$ has density $\rho$.

*Proof.* Write $(x, v) = (y, v_i)$, where $y$ holds $x$ and the velocities of the other particles. Under $\rho$, $y$ and $v_i$ are independent and $v_i$ has the Maxwell-Boltzmann law $\mu_i$. With probability $1 - p$ the state is unchanged, so its law is $\rho$. With probability $p$ the new state is $(y, w)$ with $w \sim \mu_i$ independent of $y$, so its law is (law of $y$) $\times \mu_i = \rho$. A mixture of two copies of $\rho$ is $\rho$. $\square$

Lines L7 to L9 apply $C_1, \ldots, C_N$ in turn with $p = 1 - e^{-\nu h}$, where line L9 draws each component as $\sqrt{k_B T / m_i}$ times a standard normal. By Claim 1, applied $N$ times, the collision part of a step keeps $\rho$.

**Claim 2 (the Hamiltonian part keeps $\rho$ in exact time).** The exact flow $\phi_t$ of $\dot x = v$, $m_i \dot v_i = f_i(x)$ keeps $\rho$.

*Proof.* The flow is Hamiltonian, so it keeps the volume $dx\,dv$ (Liouville's theorem), and it keeps $H = K + U$. A density that is a function of $H$ alone is therefore carried to itself. $\square$

Lines L3 to L6 replace $\phi_h$ by one velocity Verlet step. That step keeps the volume and is time-reversible, but it keeps $H$ only up to $O(h^2)$, so it keeps $\rho$ only approximately. So the algorithm samples a distribution close to $\rho$. The exact statement is Claim 1 for the collisions and Claim 2 for the dynamics that the Verlet step approximates. The difference is the time step error of the integrator, which this proof does not bound.

**Claim 3 (collision times).** In each step each particle has a collision with probability $p = 1 - e^{-\nu h}$, independently of the other particles and of the other steps. So the probability that particle $i$ has no collision in $n$ steps is $e^{-\nu n h}$, the same as for a Poisson process of rate $\nu$ observed at the times $h, 2h, \ldots$

*Proof.* Line L8 uses a fresh uniform number for each particle in each step, and the test $u < p$ succeeds with probability $p$. Independence gives $(1 - p)^n = e^{-\nu n h}$. $\square$

**Claim 4 (velocity memory of free particles).** Let $f = 0$ and let the velocities at step 0 have the Maxwell-Boltzmann law. Then for each particle and component, $\mathbb{E}[v_{ia}(0)\, v_{ia}(n h)] = (k_B T / m_i)\, e^{-\nu n h}$.

*Proof.* With $f = 0$, lines L3 and L6 change nothing, so $v_i$ changes only at a collision. Let $A$ be the event that particle $i$ has no collision in steps 1 to $n$. On $A$, $v_{ia}(nh) = v_{ia}(0)$. Off $A$, $v_{ia}(nh)$ is the value drawn at the last collision, which is independent of $v_{ia}(0)$ and has mean 0. $A$ is independent of the velocities, so
$$\mathbb{E}[v_{ia}(0)\, v_{ia}(nh)] = P(A)\, \mathbb{E}[v_{ia}(0)^2] + (1 - P(A)) \cdot 0 = e^{-\nu n h}\, \frac{k_B T}{m_i}. \qquad \square$$

In continuous time this gives the self-diffusion coefficient $D = \int_0^\infty \mathbb{E}[v_{ia}(0) v_{ia}(t)]\,dt = k_B T / (m_i \nu)$. It depends on the collision rate $\nu$, a parameter of the thermostat. So the static averages are canonical, but the transport coefficients are those of the thermostat and not those of the physical system.

**Claim 5 (inputs).** The function copies $x$ and $v$ before line L1, so the caller's lists do not change. With $\nu = 0$, $p = 0$, no velocity is replaced, and the run is velocity Verlet. $\square$
