---
title: The conserved energy, the constraint steps and the orbital frequency of Car-Parrinello dynamics
proves: [correctness]
status: full
---

Let $E(X, c)$ be continuously differentiable in the nuclear positions $X = (x_1, \dots, x_N)$ and the orbital $c \in \mathbb R^n$, and let $S = \{c : |c| = 1\}$. The Car-Parrinello equations with one orbital are
$$M_k \ddot x_k = -\frac{\partial E}{\partial x_k}, \qquad \mu \ddot c = -\nabla_c E + 2 \Lambda c, \qquad |c| = 1,$$
where $\Lambda(t)$ is the multiplier that keeps $c$ on $S$.

**Claim 1 (the conserved energy).** Along any solution, $E_{\text{cons}} = \sum_k \frac{M_k}{2} \dot x_k^2 + \frac{\mu}{2} |\dot c|^2 + E(X, c)$ is constant.

*Proof.*
$$\frac{d E_{\text{cons}}}{dt} = \sum_k \dot x_k \Bigl(M_k \ddot x_k + \frac{\partial E}{\partial x_k}\Bigr) + \dot c \cdot (\mu \ddot c + \nabla_c E) = 2 \Lambda\, c \cdot \dot c = \Lambda \frac{d}{dt} |c|^2 = 0,$$
because the first bracket is 0 by the nuclear equation, the second is $2\Lambda c$ by the orbital equation, and $|c|^2 = 1$ for all $t$. $\square$

$E_{\text{cons}}$ is not the physical energy: it contains the fictitious kinetic energy $\frac{\mu}{2}|\dot c|^2$, and $E(X, c) \ge E_{\text{BO}}(X)$ when $E_{\text{BO}}(X) = \min_{c \in S} E(X, c)$. The physical energy $\sum_k \frac{M_k}{2} \dot x_k^2 + E_{\text{BO}}(X)$ is conserved only up to these two terms, which is why the page reports the fictitious kinetic energy and the energy above the BO surface.

**Claim 2 (the constraint steps).** Let $c$ be the old orbital with $|c| = 1$, let $\dot c$ be the orbital velocity after line L4, and write $\dot c_\perp = \dot c - (c \cdot \dot c)\, c$. Let $d = c + h \dot c$.

(a) The equation $|d + \lambda c|^2 = 1$ has a real root if and only if $h |\dot c_\perp| \le 1$. Its roots are $\lambda_\pm = -d \cdot c \pm \sqrt{1 - h^2 |\dot c_\perp|^2}$, and line L5 takes $\lambda_+$. If also $h |\dot c| < 1$, then $|\lambda_+| < |\lambda_-|$, and $\lambda_+ = -h\,(c \cdot \dot c) + O(h^2 |\dot c_\perp|^2)$. After line L5, $|c_{\text{new}}| = 1$ and $c_{\text{new}} = c + h \dot c_{\text{new}}$.

(b) Line L8 replaces $\dot c$ by $\dot c - (c \cdot \dot c)\, c$, which is the vector closest to $\dot c$ among those $u$ with $c \cdot u = 0$.

*Proof.* (a) $|d + \lambda c|^2 = \lambda^2 + 2 \lambda\, d \cdot c + |d|^2$, so the roots are $-d \cdot c \pm \sqrt{(d \cdot c)^2 - |d|^2 + 1}$. With $d \cdot c = 1 + h\, c \cdot \dot c$ and $|d|^2 = 1 + 2h\, c \cdot \dot c + h^2 |\dot c|^2$, the discriminant is $1 + h^2 (c \cdot \dot c)^2 - h^2 |\dot c|^2 = 1 - h^2 |\dot c_\perp|^2$. If $h|\dot c| < 1$ then $d \cdot c \ge 1 - h |\dot c| > 0$, so $\lambda_+$ is the root of smaller size. Expanding the square root, $\lambda_+ = -1 - h\, c \cdot \dot c + 1 - \frac12 h^2 |\dot c_\perp|^2 + O(h^4 |\dot c_\perp|^4)$. The code sets $\dot c_{\text{new}} = \dot c + \lambda c / h$ and $c_{\text{new}} = d + \lambda c = c + h \dot c_{\text{new}}$, which has norm 1 by the choice of $\lambda$. (b) The set $\{u : c \cdot u = 0\}$ is a subspace, and the closest point of a subspace is the orthogonal projection, which for the complement of the unit vector $c$ is $u = \dot c - (c \cdot \dot c)\, c$. $\square$

Thus each step keeps $|c| = 1$ to rounding, as measured on the page ($10^{-15}$), and the velocity is tangent to $S$ at the end of each step, which is the hidden constraint $\frac{d}{dt} |c|^2 = 0$. With these two projections, velocity Verlet becomes the RATTLE method, which is symplectic and time reversible on the constrained phase space (see the [RATTLE algorithm](/rattle-algorithm/)); this note does not repeat that proof.

**Claim 3 (the orbital frequency).** Let $E(X, c) = 2 c^T H c + \text{const}$ with $X$ fixed and $H$ symmetric, with orthonormal eigenvectors $e_0, e_j$ and eigenvalues $\epsilon_0 < \epsilon_j$, and let $\Delta = \epsilon_j - \epsilon_0$. If $c(0)$ and $\dot c(0)$ lie in the plane $P$ spanned by $e_0$ and $e_j$, then $c(t) = \cos\theta(t)\, e_0 + \sin\theta(t)\, e_j$ for all $t$, with
$$\mu \ddot \theta = -2 \Delta \sin 2\theta.$$
Small oscillations about the ground state $\theta = 0$ have angular frequency $\omega = 2 \sqrt{\Delta / \mu}$.

*Proof.* Let $\theta(t)$ solve the scalar equation with the initial data of $c$, and put $c(t) = \cos\theta\, e_0 + \sin\theta\, e_j$ and $c_\perp = -\sin\theta\, e_0 + \cos\theta\, e_j$. Then $|c| = 1$ and $\ddot c = -\dot\theta^2 c + \ddot\theta\, c_\perp$. Also $H c = \epsilon_0 \cos\theta\, e_0 + \epsilon_j \sin\theta\, e_j$, so $c_\perp \cdot (-4 H c) = 4 \sin\theta \cos\theta\, (\epsilon_0 - \epsilon_j) = -2\Delta \sin 2\theta$, and $-4Hc$ lies in $P$. Choose $2\Lambda = -\mu \dot\theta^2 + c \cdot 4 H c$. Then the component of $\mu \ddot c + 4 H c - 2 \Lambda c$ along $c$ is $-\mu \dot\theta^2 + c \cdot 4Hc - 2\Lambda = 0$, the component along $c_\perp$ is $\mu \ddot \theta + 2\Delta \sin 2\theta = 0$, and there is no component outside $P$. So this $c$ solves the constrained equations, and by uniqueness of solutions of the constrained system it is the solution. For small $\theta$, $\sin 2\theta = 2\theta + O(\theta^3)$, which gives $\ddot\theta = -(4\Delta / \mu)\theta$ and the frequency. $\square$

For the dimer of the page with $U = 0$ at $r = 1$, $H = H_0$ is $2 \times 2$ with eigenvalues $\mp 1$, so every motion lies in $P$, $\Delta = 2$ and $\omega = 2\sqrt{2 / \mu}$. With $\phi = 2\theta$ the equation is that of a pendulum, $\ddot \phi = -(4\Delta/\mu) \sin\phi$, whose frequency at amplitude $\phi_0$ is lower by the factor $1 - \phi_0^2 / 16 + O(\phi_0^4)$. The start at $\theta_0 = 0.05$ has $\phi_0 = 0.1$, a relative shift of $6 \times 10^{-4}$, which accounts for the measured $28.268$ against $28.284$.

**Remark (adiabaticity).** Claim 3 shows that the orbital oscillates about the ground state at a frequency that grows like $\mu^{-1/2}$. When this frequency is far above the frequencies of the nuclei, little energy flows between the two, and the orbital stays close to the instantaneous ground state. This adiabatic argument (Car and Parrinello 1985; Pastore, Smargiassi and Buda 1991) explains why the error of CPMD shrinks with $\mu$. It is not a theorem proved here; the deviations on the page, which grow about linearly in $\mu$, are measurements.
