---
title: Source iteration sums the collision series, contracts by the scattering ratio in a weighted norm with vacuum, given or reflecting faces, has the Fourier factors of the page, and the change bounds the error
proves: [correctness]
status: full
---

We assume exact arithmetic. The slab, the cross sections and the lines L1 to L6 are those of the page. Every cell has $\Sigma_{t,j} > 0$, $0 \le \Sigma_{s,j} \le \Sigma_{t,j}$ and $\Delta x_j > 0$, and $c = \max_j \Sigma_{s,j}/\Sigma_{t,j}$. The directions $\mu_n$ and the weights $w_n$ are the $N$-point Gauss-Legendre rule with $N$ even. The rule is symmetric, the weights are positive, and they sum to 2. So the directions form $N/2$ pairs $\pm\mu$ with the same weight, and the weights of the pairs sum to 1.

For one direction and one cell, $\psi_a$, $\psi_b$ and $\psi_c$ are the incoming face value, the outgoing face value and the cell value. The diamond difference equations are
$$|\mu|\,\frac{\psi_b - \psi_a}{\Delta x_j} + \Sigma_{t,j}\,\psi_c = S_j, \qquad \psi_c = \frac{\psi_a + \psi_b}{2}. \tag{1}$$
The [discrete ordinates](/discrete-ordinates-method/) proof shows that one cell has exactly one solution, $\psi_b = r_j\psi_a + 2S_j/(\Sigma_{t,j} + 2|\mu|/\Delta x_j)$ with $r_j = (2 - \tau_j)/(2 + \tau_j)$ and $\tau_j = \Sigma_{t,j}\Delta x_j/|\mu|$, and that a sweep in the direction of flight solves a whole direction for a given incoming value.

## The sweep with reflection

**Lemma 1 (one pair of directions).** Fix the sources $S_j$ and a pair $\pm\mu$ with $\mu > 0$. For each choice of the faces (vacuum or data at a face, or reflection at one face or at both faces), the equations (1) of the two directions in all cells, with the face conditions, have exactly one solution, and line L4 computes it.

*Proof.* The outgoing value of a sweep is affine in its incoming value, with the slope $R = \prod_j r_j$. Since $\tau_j > 0$, $|r_j| < 1$ for every cell, so $|R| < 1$.

With data or vacuum at both faces, each direction is a separate sweep from its incoming face. With reflection at $x = L$ only, the direction $+\mu$ has its incoming value at $x = 0$ given, its sweep gives $\psi_{+}(L)$, and reflection sets $\psi_{-}(L) = \psi_{+}(L)$, after which the sweep of $-\mu$ is fixed. Reflection at $x = 0$ only is the mirror case.

With reflection at both faces, let $a = \psi_+(0)$. The sweep of $+\mu$ gives $\psi_+(L) = Ra + s_1$, where $s_1$ is its outgoing value from a zero incoming value. Reflection at $x = L$ makes this the incoming value of $-\mu$. That sweep gives $\psi_-(0) = R(Ra + s_1) + t_2$, where $t_2$ is its outgoing value from a zero incoming value, because the two directions have the same $|\mu|$ and so the same $R$. Reflection at $x = 0$ requires $\psi_-(0) = a$. So $a(1 - R^2) = Rs_1 + t_2$. Since $|R| < 1$, this has exactly one solution. Every solution of the equations satisfies this equation, so the solution is unique. $\square$

So one iteration of lines L3 and L4 is the affine map $\phi \mapsto T\phi + b$. Here $b$ is the result of line L4 with the source $q/2$ and the given incoming data. $T$ is the linear map that sweeps the source $\Sigma_s v/2$ with zero data (vacuum where a face has data) and the same reflection.

## The collision series

**Theorem 2 (Neumann series).** From $\phi^{(0)} = 0$, the iterate after $l$ passes of lines L3 to L4 is
$$\phi^{(l)} = \sum_{k=0}^{l-1} T^k b .$$

*Proof.* By induction on $l$. For $l = 1$, $\phi^{(1)} = T \cdot 0 + b = b$. If the formula holds for $l$, then $\phi^{(l+1)} = T\phi^{(l)} + b = \sum_{k=1}^{l} T^k b + b$. $\square$

Here $b$ is the flux of the particles that have not collided yet, and $T$ turns the flux of the particles after $k$ collisions into the flux after $k + 1$ collisions. So iterate $l$ is the flux of the particles with fewer than $l$ collisions. The series converges when the spectral radius of $T$ is less than 1 ([Neumann series](/neumann-series/)). The next theorem shows this for $c < 1$.

## Contraction

Write $\langle u, v\rangle_t = \sum_j \Sigma_{t,j}\, u_j v_j\, \Delta x_j$ and $\|v\|_t^2 = \langle v, v\rangle_t$.

**Theorem 3 (contraction by $c$).** For every choice of the faces in Lemma 1 and every vector $v$, $\|Tv\|_t \le c\,\|v\|_t$. If $c < 1$, the discrete equations have exactly one solution $\phi$, and every start gives $\|\phi^{(l)} - \phi\|_t \le c^{\,l}\,\|\phi^{(0)} - \phi\|_t$.

*Proof.* Fix $v$ and one pair $\pm\mu$, and solve Lemma 1 with $S_j = \Sigma_{s,j}v_j/2$ and zero data. Multiply the balance in (1) by $\psi_c\Delta x_j$. With the diamond relation, $|\mu|(\psi_b - \psi_a)\psi_c = |\mu|(\psi_b^2 - \psi_a^2)/2$. Sum over the cells and over the two directions. The face terms telescope:
$$\frac{|\mu|}{2}\Big(\psi_+(L)^2 - \psi_+(0)^2 + \psi_-(0)^2 - \psi_-(L)^2\Big) + \|x\|_t^2 + \|y\|_t^2 = \langle s, x + y\rangle_t,$$
where $x$ and $y$ are the cell values of $+\mu$ and $-\mu$ and $s_j = S_j/\Sigma_{t,j}$. At a reflecting face the two terms of that face cancel, since the incoming value equals the outgoing one. At a face with zero data the incoming term is 0 and the outgoing term is not negative. So the face part is not negative and
$$\|x\|_t^2 + \|y\|_t^2 \le \langle s, x + y\rangle_t \le \|s\|_t\, \|x + y\|_t .$$
For all vectors, $\|x + y\|_t^2 \le 2(\|x\|_t^2 + \|y\|_t^2)$. So $\|x + y\|_t^2 \le 2\|s\|_t\|x + y\|_t$, that is $\|x + y\|_t \le 2\|s\|_t$. Since $s_j = (\Sigma_{s,j}/\Sigma_{t,j})\,v_j/2$ and $\Sigma_{s,j}/\Sigma_{t,j} \le c$, $\|s\|_t \le (c/2)\|v\|_t$. So $\|x + y\|_t \le c\|v\|_t$.

Line L4 forms $Tv = \sum_{\text{pairs}} w\,(x + y)$. The weights of the pairs are positive and sum to 1, so the triangle inequality gives $\|Tv\|_t \le c\|v\|_t$. For $c < 1$, the contraction mapping theorem ([fixed-point iteration](/fixed-point-iteration/)) gives one fixed point, and the error of iterate $l$ is $T^l$ applied to the first error. $\square$

The proof does not use the sign of the cell values, so it holds for diamond difference with thick cells. With reflection at both faces it also holds when the slab is a homogeneous infinite medium, and the next theorem shows that the bound is then attained.

## The rate

**Theorem 4 (the flat mode).** Let all cells have the same $\Sigma_t$ and $\Sigma_s$, and let both faces reflect. Then the constant vector $v = 1$ satisfies $Tv = c\,v$. So the bound of Theorem 3 is attained, and for $q$ constant the iterates from 0 are $\phi^{(l)} = (q/\Sigma_t)(1 - c^l)/(1 - c)$.

*Proof.* The source is $S = \Sigma_s/2$ in every cell. The values $\psi_a = \psi_b = \psi_c = S/\Sigma_t$ in every cell and every direction satisfy (1), and they satisfy both reflection conditions. By Lemma 1 they are the solution, so $Tv = \sum_n w_n S/\Sigma_t = 2 \cdot \Sigma_s/(2\Sigma_t) = c$. In the same way $b = q/\Sigma_t$ for a constant $q$. Theorem 2 then gives $\phi^{(l)} = (q/\Sigma_t)(1 + c + \cdots + c^{l-1})$. $\square$

**Theorem 5 (Fourier modes of diamond difference).** Let the slab have $M$ equal cells of width $h$ with the same $\Sigma_t$ and $\Sigma_s$, and let both faces reflect. For $k = 0, 1, \ldots, M - 1$, let $\theta = \pi k/M$ and $e_j = \cos(\theta(j + 1/2))$ for the cells $j = 0, \ldots, M - 1$. Then $Te = \omega(\theta)\, e$ with
$$\omega(\theta) = \frac{c}{2}\sum_{n=1}^{N} \frac{w_n}{1 + \lambda^2\mu_n^2}, \qquad \lambda = \frac{2\tan(\theta/2)}{\Sigma_t h}.$$

*Proof.* Number the faces by integers, so that cell $j$ lies between faces $j$ and $j + 1$. Take the complex source $S_j = (\Sigma_s/2)\,e^{i\theta(j + 1/2)}$ on all integers $j$, and try the face values $B_\mu e^{i\theta j}$ and the cell values $A_\mu e^{i\theta(j + 1/2)}$ for the direction $\mu$. The diamond relation gives $A_\mu = B_\mu\cos(\theta/2)$. The balance, divided by $e^{i\theta(j + 1/2)}$, gives $\mu B_\mu\, 2i\sin(\theta/2)/h + \Sigma_t A_\mu = \Sigma_s/2$. The two equations give
$$A_\mu = \frac{\Sigma_s/2}{\Sigma_t + 2i\mu\tan(\theta/2)/h} = \frac{c/2}{1 + i\lambda\mu}.$$
Since $0 \le \theta < \pi$, $\cos(\theta/2) > 0$, so these values are well defined. The equations (1) are real, so the real parts solve them with the source $(\Sigma_s/2)e_j$.

We now check the faces. Since $A_{-\mu}$ is the complex conjugate of $A_\mu$, so is $B_{-\mu}$ of $B_\mu$. At face 0, the real parts of $B_\mu$ and $B_{-\mu}$ are equal, which is reflection. At face $M$ the values are the real parts of $B_{\pm\mu}e^{i\pi k} = (-1)^k B_{\pm\mu}$, which are again equal. So the real parts, restricted to the slab, satisfy (1) and both reflection conditions. By Lemma 1 they are the solution of line L4. The pair gives $A_\mu + A_{-\mu} = c/(1 + \lambda^2\mu^2)$, which is real. So
$$(Te)_j = \sum_{\text{pairs}} w\,\frac{c}{1 + \lambda^2\mu^2}\, e_j = \omega(\theta)\, e_j. \qquad\square$$

The $M$ vectors $e$ are orthogonal, so they are all the eigenvectors of $T$ in this case. Since $\omega$ decreases in $\lambda$ and $\lambda = 0$ only for $k = 0$, the spectral radius is $\omega(0) = c$. When $\Sigma_t h \to 0$ with $\lambda$ fixed, the factor is the same formula, which is the factor of the $S_N$ equations exact in space. If also $N \to \infty$, the sum tends to the integral $(c/2)\int_{-1}^{1} d\mu/(1 + \lambda^2\mu^2) = c\arctan(\lambda)/\lambda$, the factor of the continuous problem.

## Stopping

**Theorem 6 (the change bounds the error).** Suppose $\|\phi^{(l)} - \phi\| \le \rho\,\|\phi^{(l-1)} - \phi\|$ in some norm, with $\rho < 1$. Then
$$\|\phi^{(l)} - \phi\| \le \frac{\rho}{1 - \rho}\,\|\phi^{(l)} - \phi^{(l-1)}\|.$$
In the homogeneous infinite medium of Theorem 4 with $\rho = c$, equality holds in every norm.

*Proof.* Write $e_l = \phi^{(l)} - \phi$. Then $e_{l-1} = e_l - (\phi^{(l)} - \phi^{(l-1)})$, so $\|e_l\| \le \rho\|e_{l-1}\| \le \rho\|e_l\| + \rho\|\phi^{(l)} - \phi^{(l-1)}\|$. Move $\rho\|e_l\|$ to the left and divide by $1 - \rho$. In the case of Theorem 4 from $\phi^{(0)} = 0$, $e_l = -(q/\Sigma_t)c^l/(1 - c)$ and $\phi^{(l)} - \phi^{(l-1)} = (q/\Sigma_t)c^{l-1}$ in every cell, so the ratio of the two is exactly $c/(1 - c)$. $\square$

So with $c = 0.99$, a stopping test on the change at a tolerance tol leaves an error of up to $99$ tol in the infinite medium.
