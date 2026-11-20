---
tag: GF16T9
kind: model
slug: gibson-lanni-model
name: Gibson-Lanni model
aliases:
- Gibson-Lanni PSF
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "A scalar model of the 3D point spread function of a widefield microscope in which the immersion, coverslip and sample indices differ from the design, so the PSF changes with depth."
history:
  year: 1991
  people: [Sarah Frisken Gibson, Frederick Lanni]
  note: Gibson and Lanni computed the optical path difference of the actual and the design layers between the object and an ideal objective, put it in a scalar Kirchhoff integral and tested the result against measured PSFs of beads.
prereqs: [point-spread-function, optical-transfer-function]
see_also: [rayleigh-criterion, abbe-diffraction-limit, nearest-neighbor-deconvolution, richardson-lucy-deconvolution, image-deblurring, phase-diversity, parsevals-theorem, forward-operator]
sources:
  - paper: doi:10.1364/JOSAA.8.001601
    title: Sarah Frisken Gibson and Frederick Lanni, Experimental test of an analytical model of aberration in an oil-immersion objective lens used in three-dimensional light microscopy, Journal of the Optical Society of America A 8(10), 1991
    locator: the article from page 1601 (the optical path difference of the design and actual layers, the scalar PSF integral and the comparison with measured bead images)
  - paper: doi:10.1364/JOSAA.9.000154
    title: Sarah Frisken Gibson and Frederick Lanni, Experimental test of an analytical model of aberration in an oil-immersion objective lens used in three-dimensional light microscopy, Journal of the Optical Society of America A 9(1), 1992
    locator: the reprint of the 1991 article, from page 154
  - paper: doi:10.1364/JOSAA.34.001029
    title: Jizhou Li, Feng Xue and Thierry Blu, Fast and accurate three-dimensional point spread function computation for fluorescence microscopy, Journal of the Optical Society of America A 34(6), 2017
    locator: the article from page 1029 (equations 1 and 2 give the model in the form used here; the method fits the phase factor by a short sum of Bessel functions)
  - paper: doi:10.1098/rspa.1959.0200
    title: B. Richards and E. Wolf, Electromagnetic diffraction in optical systems II. Structure of the image field in an aplanatic system, Proceedings of the Royal Society of London A 253(1274), 1959
    locator: pages 358 to 379 (the vectorial focal field of a high aperture lens)
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, 3rd edition, Roberts and Company, 2005
    locator: sections 6.4.1 (the generalized pupil function) and 6.4.4 (the focusing error)
---

The Gibson-Lanni model gives the three-dimensional [point spread function](/point-spread-function/) of a widefield fluorescence microscope when the layers between the object and the lens are not the ones the lens was designed for. An oil objective is corrected for one immersion oil, one coverslip thickness and an object right under the coverslip. In practice the coverslip thickness varies, the oil may differ, and the object often sits several micrometers deep in water or in a mounting medium with another refractive index. Gibson and Lanni (1991) computed the optical path difference that these changes add to the wavefront, as a function of the angle of the ray, and put it into a scalar diffraction integral. The result is a PSF that changes with the depth of the source: it loses its peak, grows asymmetric along the axis, and its best focus moves. So a thick specimen is not imaged by a convolution with one PSF. The model assumes that the objective is perfect under the design conditions, and it ignores polarization; it is the standard scalar model for depth-dependent PSFs in deconvolution microscopy.

## The machine

**Parameters.** The emission wavelength in vacuum $\lambda$, with $k = 2\pi/\lambda$, and the numerical aperture $\mathrm{NA}$. Three layers lie between the source and the objective: the specimen (index $n_s$), the coverslip (index $n_g$, thickness $t_g$) and the immersion medium (index $n_i$). The objective was designed for a coverslip with $n_g^\ast$, $t_g^\ast$ and an immersion with $n_i^\ast$ and working distance $t_i^\ast$, and for a source on the coverslip surface. Starred symbols are design values and plain ones are actual values.

**Input.** A point source at lateral position $(x_p, y_p)$ and depth $z_p \ge 0$ below the coverslip, and the axial position $z$ of the focal plane, set by the stage. For the design conditions and $z_p = 0$, the best focus is at $z = 0$.

**The optical path difference.** For the normalized pupil radius $\rho \in [0, 1]$, the ray at $\rho$ leaves the source at the angle with $n \sin\theta = \mathrm{NA}\,\rho$ in each layer of index $n$. The difference between the optical path of the actual system and that of the design system along this ray is (Li, Xue and Blu, equation 1, after Gibson and Lanni)

$$\begin{aligned}
\mathrm{OPD}(\rho, z; z_p) = {} & (z + t_i^\ast)\sqrt{n_i^2 - (\mathrm{NA}\,\rho)^2} + z_p\sqrt{n_s^2 - (\mathrm{NA}\,\rho)^2} - t_i^\ast\sqrt{n_i^{\ast 2} - (\mathrm{NA}\,\rho)^2} \\
& + t_g\sqrt{n_g^2 - (\mathrm{NA}\,\rho)^2} - t_g^\ast\sqrt{n_g^{\ast 2} - (\mathrm{NA}\,\rho)^2}.
\end{aligned}$$

**The PSF.** With $r = \sqrt{(x - x_p)^2 + (y - y_p)^2}$, the intensity in the image of the plane at focus position $z$ is (Li, Xue and Blu, equation 2)

$$\mathrm{PSF}(r, z; z_p) = \left| A \int_0^{a} e^{\,i k\, \mathrm{OPD}(\rho, z; z_p)}\, J_0(k\, r\, \mathrm{NA}\, \rho)\, \rho\, d\rho \right|^2, \qquad a = \frac{\min\{\mathrm{NA}, n_s, n_g, n_g^\ast, n_i, n_i^\ast\}}{\mathrm{NA}},$$

with a constant $A$ and the Bessel function $J_0$. The upper limit $a \le 1$ keeps every square root real: a ray whose angle would need $\mathrm{NA}\,\rho > n$ in some layer is beyond the critical angle there and does not reach the lens.

**Output.** A 3D image of an object $o(x_p, y_p, z_p) \ge 0$ made of incoherent sources is

$$i(x, y, z) = \iiint \mathrm{PSF}\big(r, z; z_p\big)\, o(x_p, y_p, z_p)\, dx_p\, dy_p\, dz_p .$$

For each fixed depth $z_p$ the map is a 2D convolution in $(x, y)$. Along the axis it is not a convolution, because the PSF depends on $z$ and $z_p$ separately, not only on $z + z_p$, as soon as $n_s \ne n_i$.

**Assumptions.** Scalar Kirchhoff diffraction, one wavelength, incoherent sources, layers that are flat and uniform, an objective that is aberration-free under the design conditions, and the same apodization as an ideal lens (the amplitude in the pupil is constant). Polarization and the vector nature of the field are left out.

## What it counts

The model gives an intensity, in arbitrary units fixed by $A$, at each point $(x, y, z)$ of the image space for one point source. It does not count photons; a noise model, Poisson counts with a background, is added on top for a forward model of real data. The voxel size, the pixel integration and the camera are also outside the model.

Cost, in the real-RAM model with a Bessel function evaluation counted as one operation: one PSF value is a one-dimensional integral over $\rho$. With $Q$ quadrature nodes, one value costs $O(Q)$, and a PSF on $N_r$ radii and $N_z$ planes costs $O(Q N_r N_z)$. The phase $k\,\mathrm{OPD}$ grows linearly in $z$ and $z_p$, so for planes far from focus the integrand oscillates fast and $Q$ must grow in proportion to $k\,|z|\,n_i$. Li, Xue and Blu replace $e^{ik\,\mathrm{OPD}}$ by a sum of $M$ scaled Bessel functions $J_0(\sigma_m \rho)$ with coefficients fitted by least squares for each plane; then each radial integral has a closed form, and one PSF value costs $O(M)$ after the fit.

## Relation to other models

- **The Airy pattern and the defocus model.** With all actual values equal to the design values and $z_p = 0$, the OPD is $z\sqrt{n_i^2 - (\mathrm{NA}\rho)^2}$. This is the pure focusing error of a lens in a uniform medium (Goodman, section 6.4.4). At $z = 0$ the OPD is zero, and the PSF is the Airy pattern (see Known results).
- **The generalized pupil.** The model is a special case of the generalized pupil $P(\rho)\,e^{ikW(\rho)}$ (Goodman, section 6.4.1), with the wavefront error $W = \mathrm{OPD}$ and a clear pupil of radius $a$. So all statements about pupils with aberrations, such as the bound of the MTF by the aberration-free one on the [optical transfer function](/optical-transfer-function/) page, apply to each plane.
- **Vectorial models.** For a high NA the field at focus has components along the axis, and the scalar model is an approximation. Richards and Wolf (1959) gave the vectorial focal field of an aplanatic lens in one medium. Vectorial models of focusing through layered media keep the same OPD idea and add the polarization and the transmission at each interface.
- **Gaussian and measured PSFs.** Deconvolution software also uses a 3D Gaussian fitted to the PSF, or a PSF measured from beads. The Gaussian has no depth dependence and no axial asymmetry. A measured PSF holds every real aberration, but only at the depth of the bead.

## Known results in the model

**1. With matched layers it is the Airy pattern.** Let the actual values equal the design values, $z_p = 0$ and $z = 0$. Then $\mathrm{OPD} = 0$, $a = 1$, and $\int_0^1 J_0(c\rho)\,\rho\, d\rho = J_1(c)/c$ with $c = k r \mathrm{NA}$, from $\frac{d}{dc}\big(c J_1(c)\big) = c J_0(c)$. So $\mathrm{PSF} = A^2 \big(J_1(c)/c\big)^2 = \tfrac{A^2}{4}\big(2J_1(v)/v\big)^2$ with $v = 2\pi\,\mathrm{NA}\,r/\lambda$: the Airy pattern of the [Rayleigh criterion](/rayleigh-criterion/) page. If only $n_s$ differs and $z_p = 0$, $z = 0$, the OPD is still zero but the aperture is cut at $a = n_s/\mathrm{NA}$ when $n_s < \mathrm{NA}$, and the peak drops to $a^4$ of the full aperture value, because the peak is $A^2 (a^2/2)^2$. For $\mathrm{NA} = 1.4$ and water, $n_s = 1.33$, this is $0.95^4 = 0.8145$.

**2. Each plane holds the same total light.** For every $z$ and $z_p$,

$$\int_0^\infty \mathrm{PSF}(r, z; z_p)\, 2\pi r\, dr = \frac{\pi A^2 a^2}{(k\,\mathrm{NA})^2}.$$

*Proof.* The inner integral is the Hankel transform of order zero of $f(\rho) = e^{ik\,\mathrm{OPD}}$ on $[0, a]$, evaluated at $s = k\,\mathrm{NA}\, r$. The Hankel transform keeps the norm (the Parseval identity for it): $\int_0^\infty |\int_0^a f(\rho) J_0(s\rho)\rho\, d\rho|^2 s\, ds = \int_0^a |f(\rho)|^2 \rho\, d\rho$. Change variables $s = k\,\mathrm{NA}\,r$, and use $|f| = 1$, so the right side is $a^2/2$. $\square$

So a widefield microscope has no optical sectioning in this model: a plane far from focus receives as much light from a source as the focal plane, only spread wider. This is the reason for the out-of-focus haze that [nearest-neighbor deconvolution](/nearest-neighbor-deconvolution/) and 3D deconvolution remove.

**3. Paraxial focal shift.** Expand $\sqrt{n^2 - s} = n - s/(2n) + O(s^2)$ in $s = (\mathrm{NA}\rho)^2$, with matched coverslip and immersion. The part of the OPD that is linear in $s$ is $-s\big(z/n_i + z_p/n_s\big)/2$, and it vanishes for $z = -z_p\, n_i/n_s$. So for small apertures the stage must move $n_i/n_s$ times the true depth to focus a source; an axial stack taken with a stage step $\Delta z$ samples the specimen with the step $\Delta z\, n_s/n_i$, and objects look stretched along the axis by $n_i/n_s$.

**4. A worked case at high NA.** Take $\lambda = 500$ nm, $\mathrm{NA} = 1.4$, oil $n_i = n_i^\ast = 1.515$, a coverslip as designed ($n_g = n_g^\ast$, $t_g = t_g^\ast$), and a bead at $z_p = 10\ \mu$m in water, $n_s = 1.33$. The paraxial rule gives the best focus at $z = -10 \cdot 1.515/1.33 = -11.39\ \mu$m. A numerical evaluation of the on-axis PSF ($r = 0$, Simpson's rule with 1500 intervals, a scan in $z$ with a step of $0.05\ \mu$m, then a local refinement) puts the brightest point at $z = -12.24\ \mu$m, and its value is $0.25$ of the peak of the matched system with a bead in oil. With $n_s = 1.515$ the same computation gives $z = -10.00\ \mu$m and the full peak. These numbers are computed from the model, not measured. They show the two effects that matter for deconvolution: the high NA focal shift is larger than the paraxial one, and at 10 micrometers depth the cut aperture (a factor of 0.81) and the spherical aberration together take three quarters of the peak.

**5. The PSF depends on depth.** By result 4 the PSF at $z_p = 10\ \mu$m differs from the PSF at $z_p = 0$ in its peak, its position and its axial shape. So 3D deconvolution of a thick specimen with one PSF is a model error. Methods split the volume into slabs with one PSF each, or interpolate between PSFs computed at several depths.

**6. Agreement with data.** Gibson and Lanni compared the model with measured images of small beads under the oil objective of their experiment and found that it reproduced the axial asymmetry and the change with depth. This is a measurement on their setup, not a guarantee for other objectives; real lenses also have residual aberrations under the design conditions, which the model does not hold.

## References
