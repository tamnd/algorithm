---
title: Why the TIE solver returns the phase, and where it does not
proves: [correctness]
status: full
---

This page derives the transport of intensity equation from the paraxial wave equation, proves that the two Poisson solves of the code return the phase up to a constant when the energy flux is a gradient, and gives the two error terms of a real defocus series: the bias of the finite difference and the noise.

**Setting.** The field is $U(x, y, z) = A(x, y, z) e^{ikz}$ with $k = 2\pi/\lambda$ and the time factor $e^{-i\omega t}$. In the paraxial approximation the envelope obeys
$$\frac{\partial A}{\partial z} = \frac{i}{2k} \nabla^2 A,$$
where $\nabla$ acts on $x$ and $y$ only. In Fourier space this is $\hat A(f, z) = \hat A(f, 0)\, e^{-i\pi\lambda z |f|^2}$, which is the angular spectrum transfer function $e^{2\pi i z \sqrt{1/\lambda^2 - |f|^2}}$ with its square root expanded to first order and the factor $e^{ikz}$ removed: $\frac{i}{2k}(-4\pi^2|f|^2) = -i\pi\lambda|f|^2$. Write $A = \sqrt{I}\, e^{i\phi}$ where $I > 0$.

**Lemma 1 (the transport of intensity equation).** Under the paraxial equation,
$$-k \frac{\partial I}{\partial z} = \nabla \cdot (I \nabla \phi).$$

*Proof.* $I = \bar A A$, so $\partial_z I = 2\,\mathrm{Re}(\bar A\, \partial_z A) = 2\,\mathrm{Re}\big(\tfrac{i}{2k} \bar A \nabla^2 A\big) = -\tfrac{1}{k} \mathrm{Im}(\bar A \nabla^2 A)$. Since $\nabla \cdot (\bar A \nabla A) = |\nabla A|^2 + \bar A \nabla^2 A$ and $|\nabla A|^2$ is real, $\mathrm{Im}(\bar A \nabla^2 A) = \nabla \cdot \mathrm{Im}(\bar A \nabla A)$. From $\nabla A = (\nabla \sqrt{I} + i \sqrt{I} \nabla\phi) e^{i\phi}$ we get $\bar A \nabla A = \sqrt{I}\nabla\sqrt{I} + i I \nabla\phi$, whose imaginary part is $I\nabla\phi$. $\square$

The vector $I\nabla\phi$ is, up to a constant factor, the transverse energy flux. Lemma 1 says that the intensity changes along $z$ by the divergence of this flux.

**The method.** Teague's substitution writes $I\nabla\phi = \nabla\psi$. Then Lemma 1 gives the two Poisson equations
$$\nabla^2 \psi = -k\, \partial_z I, \qquad \nabla^2 \phi = \nabla \cdot \Big(\frac{\nabla\psi}{I}\Big).$$
The code solves both on a periodic grid with the operator $\mathcal{L}^{-1}$ of line L2 and line L5: take the DFT, divide each coefficient by $-4\pi^2|f|^2$, set the zero frequency to $0$, and take the inverse DFT. The gradient of line L3 multiplies by $2\pi i f$ and drops the Nyquist row or column, which has no sign.

**Lemma 2 (the spectral solver).** Let $g$ be a real image whose DFT is zero at the Nyquist row and column. Then $u = \mathcal{L}^{-1} g$ is the unique image with mean $0$ and the same property such that $\Delta u = g - \bar g$, where $\Delta$ is the spectral Laplacian (the divergence of the spectral gradient) and $\bar g$ is the mean of $g$.

*Proof.* The spectral gradient followed by the spectral divergence multiplies each coefficient with no Nyquist index by $(2\pi i f_x)^2 + (2\pi i f_y)^2 = -4\pi^2|f|^2$. This number is nonzero for $f \ne 0$, so the coefficient of $u$ at every $f \ne 0$ is fixed by $g$ and the coefficient at $0$ is the mean, which is set to $0$. $\square$

**Theorem (exact recovery).** On the periodic grid, let $\phi$ and $I > 0$ be given, and suppose that the flux $I\nabla\phi$ (with the spectral gradient) equals $\nabla\chi$ for some image $\chi$ with no Nyquist content, and that $\nabla\chi / I$ has none either. If the input satisfies $\frac{I_+ - I_-}{2\,\Delta z} = -\frac{1}{k} \Delta\chi$ exactly and $I_0 = I$, then lines L1 to L5 return $\phi - \bar\phi$.

*Proof.* Line L1 gives $-\frac{1}{k}\Delta\chi$, and line L2 applies $\mathcal{L}^{-1}$ to $\Delta\chi$; by Lemma 2 the result is $\psi = \chi - \bar\chi$, so $\nabla\psi = \nabla\chi = I\nabla\phi$. Line L4 gives $\nabla\phi$, and line L5 gives $\mathcal{L}^{-1}(\Delta\phi) = \phi - \bar\phi$, again by Lemma 2. $\square$

For a uniform intensity $I_0$ the hypothesis holds with $\chi = I_0 \phi$, and the two solves reduce to one: $\Delta\phi = -\frac{k}{I_0}\partial_z I$. The tests check both forms on band-limited data to rounding error, and the varying case with $I = e^{-\psi}$ and $\phi = e^{\psi}$, where $I\nabla\phi = \nabla\psi$ holds in the continuum.

**Where the method is not exact.**

1. *The flux is not always a gradient.* A periodic vector field splits into a gradient, a divergence-free part and a constant vector (the Helmholtz decomposition). Lemma 1 only constrains the divergence of $I\nabla\phi$, so the data say nothing about the other two parts, and Teague's substitution sets them to zero. If $I$ varies and $\nabla I$ is not parallel to $\nabla\phi$, the flux has a divergence-free part in general, and the result is not $\phi$. For the absorbing test object on the page the error from this source is about one percent (a measurement).
2. *The finite difference.* If $I$ is smooth in $z$, Taylor's theorem gives
$$\frac{I(\Delta z) - I(-\Delta z)}{2\,\Delta z} = \partial_z I(0) + \frac{\Delta z^2}{6}\, \partial_z^3 I(\xi)$$
at each point, for some $\xi$ in $(-\Delta z, \Delta z)$. The bias is of order $\Delta z^2$. It also includes the error of the paraxial equation when the images come from exact propagation.
3. *Noise.* The method is linear in the data for uniform intensity. Independent noise $e_\pm$ in the two images adds $\mathcal{L}^{-1}\big(-\frac{k}{I_0}\frac{e_+ - e_-}{2\,\Delta z}\big)$ to the phase. Its DFT coefficient at $f \ne 0$ is the coefficient of $e_+ - e_-$ times $\frac{k}{8\pi^2 I_0 \Delta z |f|^2}$. So the noise in the phase falls as $1/\Delta z$ and is largest at the lowest frequencies.

Items 2 and 3 pull $\Delta z$ in opposite directions: a small step amplifies noise, a large step adds bias. Neither the best step nor the size of the divergence-free part follows from the data alone, and the page reports them as measurements.
