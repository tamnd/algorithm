---
tag: H7PF86
kind: algorithm
slug: irradiance-environment-map
name: Spherical harmonic irradiance environment map
aliases:
- Ramamoorthi-Hanrahan irradiance map
area: graphics-and-signals/real-time-rendering
level: advanced
summary: "Nine spherical harmonic coefficients give the diffuse irradiance of a distant environment as E(n) = n^T M n. The error is at most 3/32 (about 9%) of the total light, and under 3% on average."
model: real-ram
complexity:
  vars: {s: the number of texels of the environment map}
  time: {build: Θ(s), evaluate: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, in_place: false}
history:
  year: 2001
  people: [Ravi Ramamoorthi, Pat Hanrahan]
  note: Ramamoorthi and Hanrahan showed in their SIGGRAPH 2001 paper that the irradiance of a distant environment is almost band limited, and replaced the convolution of a whole map by nine coefficients and a quadratic form.
prereqs: [spherical-harmonic-lighting, lambertian-reflectance]
see_also: [image-based-lighting, environment-mapping, cube-map, irradiance-volume, precomputed-radiance-transfer, split-sum-approximation, rendering-equation, monte-carlo-integration]
sources:
  - paper: doi:10.1145/383259.383317
    title: Ravi Ramamoorthi and Pat Hanrahan, An efficient representation for irradiance environment maps, SIGGRAPH 2001, 497 to 500
    locator: Section 2 (Equations 3 to 9, the basis and the clamped cosine coefficients), Section 3.1 (prefiltering, Equation 10, and the error statement) and Section 3.2 (Equations 11 to 13, the matrix form and the constants c1 to c5)
  - paper: "Ronen Basri and David W. Jacobs, Lambertian reflectance and linear subspaces, IEEE International Conference on Computer Vision (ICCV), 2001"
    locator: the analysis of the clamped cosine kernel and the bound on the average error of a nine term approximation (general locator, cited by Ramamoorthi and Hanrahan for the 3% figure)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 10, Local Illumination (the parts on spherical harmonics and on environment lighting)
---

A spherical harmonic irradiance environment map gives the light that a diffuse surface receives from a distant environment, for any normal, with nine numbers per color channel. The input is an environment map of radiance. The algorithm projects it onto the nine real spherical harmonics of order $l \le 2$, multiplies them by the coefficients of the clamped cosine, and puts the result into a symmetric $4 \times 4$ matrix $M$. The irradiance at a unit normal $n$ is then $E(n) = \tilde n^T M \tilde n$ with $\tilde n = (n_x, n_y, n_z, 1)$, a few multiply-adds in a shader. Ramamoorthi and Hanrahan published it in 2001. The error is at most $3/32 \approx 9\%$ of the total light of the environment for any lighting, which is a proved bound, and the average error over all normals is under 3% for any physical lighting, which the paper takes from Basri and Jacobs. On natural maps the paper measured smaller errors. The page handles the diffuse part of [image-based lighting](/image-based-lighting/); the glossy part is the [split sum approximation](/split-sum-approximation/), and the general use of spherical harmonics for light is [spherical harmonic lighting](/spherical-harmonic-lighting/).

## In plain words

A matte surface gets light from every direction above it, and it weights each direction by how much it faces that direction. This sum changes slowly when the surface turns, because it averages over half of the sky. A slow function can be described by a few numbers, like a smooth curve that needs only a few terms of a series. The method finds nine such numbers for the whole environment, once. To shade a pixel, it combines the nine numbers with the normal of the pixel, which gives the light for that normal at once, without a look at the environment again. The answer is smooth and fast, but it loses sharp detail such as the exact edge of a shadow from the sun.

## The problem

The input is a distant lighting environment, given as $s$ texels $(\omega_k, L_k, \Delta\omega_k)$: a unit direction, a radiance and a solid angle, for one color channel. The solid angles add up to $4\pi$. The output is a function that returns, for a unit normal $n$, an approximation of the irradiance

$$E(n) = \int_{S^2} L(\omega) \max(0, n \cdot \omega)\, d\omega.$$

A Lambertian surface with albedo $\rho$ then has the outgoing radiance $\rho E(n) / \pi$, see [Lambertian reflectance](/lambertian-reflectance/). The standing assumptions are: the sources are far away, so $L$ does not depend on the position (a physical approximation); the surface is diffuse; and nothing blocks the light, so there is no shadow and no interreflection. The environment can be a [cube map](/cube-map/) or a latitude and longitude map; only the texel directions and solid angles matter.

The spherical harmonics are the ones of the paper, with $z$ as the polar axis: $Y_{00} = 0.282095$; $Y_{1,-1}, Y_{10}, Y_{11} = 0.488603\,(y, z, x)$; $Y_{2,-2}, Y_{2,-1}, Y_{21} = 1.092548\,(xy, yz, xz)$; $Y_{20} = 0.315392\,(3z^2 - 1)$; and $Y_{22} = 0.546274\,(x^2 - y^2)$. They are orthonormal on the sphere (a proved property).

## The algorithm

```pseudo id=main
IRRADIANCE-MAP(texels)
L1  L_lm ← 0 for the nine pairs (l, m) with l ≤ 2
L2  for each texel (ω, L, Δω)
L3      for each (l, m):  L_lm ← L_lm + L · Y_lm(ω) · Δω
L4  M ← [[c1 L22,  c1 L2-2,  c1 L21,  c2 L11],
         [c1 L2-2, -c1 L22,  c1 L2-1, c2 L1-1],
         [c1 L21,  c1 L2-1,  c3 L20,  c2 L10],
         [c2 L11,  c2 L1-1,  c2 L10,  c4 L00 - c5 L20]]
L5  return M

IRRADIANCE(M, n)
L6  ñ ← (n_x, n_y, n_z, 1)
L7  return ñᵀ M ñ
```

**Projection (lines L1 to L3).** This is Equation 10 of the paper, a quadrature of $\int L Y_{lm}\, d\omega$. Each texel adds its radiance times the nine basis values times its solid angle. The texels can come in any order and need no storage, so the loop is one pass over the map.

**The kernel.** The irradiance is the convolution of $L$ with the clamped cosine $A(t) = \max(t, 0)$. By the Funk-Hecke theorem, this convolution multiplies each coefficient of band $l$ by one number, $\hat A_l = 2\pi \int_0^1 t P_l(t)\, dt$. The values are $\hat A_0 = \pi$, $\hat A_1 = 2\pi/3$ and $\hat A_2 = \pi/4$. The paper gives the general formula: $\hat A_l$ is 0 for odd $l > 1$, and for even $l$ it falls off like $l^{-5/2}$, so $\hat A_4 = -0.1309$ and $\hat A_6 = 0.0491$ are already small. This decay is why nine terms are enough.

**The matrix (line L4).** Line L4 folds $\hat A_l$ and the basis constants into five numbers: $c_1 = 0.429043$, $c_2 = 0.511664$, $c_3 = 0.743125$, $c_4 = 0.886227$ and $c_5 = 0.247708$, for example $c_4 = \hat A_0 Y_{00}$ and $c_1 = \hat A_2 \cdot 0.546274$. The quadratic form $\tilde n^T M \tilde n$ then equals $\sum_{l \le 2} \hat A_l L_{lm} Y_{lm}(n)$ term by term. One matrix is built per color channel, so an RGB map gives three matrices.

**Evaluation (lines L6 and L7).** Line L7 is Equation 11 of the paper. In a shader it is three 4-vector products per channel. The expanded form of Equation 13, $c_1 L_{22}(x^2 - y^2) + c_3 L_{20} z^2 + c_4 L_{00} - c_5 L_{20} + 2 c_1 (L_{2,-2} xy + L_{21} xz + L_{2,-1} yz) + 2 c_2 (L_{11} x + L_{1,-1} y + L_{10} z)$, gives the same number.

## Example

The environment has two texels that act as point lights: power $L \Delta\omega = 2$ from $+z$ and power $1$ from $+x$. The table shows the nonzero coefficients after each texel.

| step | $L_{00}$ | $L_{10}$ | $L_{11}$ | $L_{20}$ | $L_{22}$ |
|---|---|---|---|---|---|
| after L1 | 0 | 0 | 0 | 0 | 0 |
| texel $+z$, weight 2 | 0.564190 | 0.977206 | 0 | 1.261566 | 0 |
| texel $+x$, weight 1 | 0.846284 | 0.977206 | 0.488603 | 0.946174 | 0.546274 |

At $+z$, $Y_{20} = 0.315392 \cdot 2$; at $+x$, $Y_{20} = 0.315392 \cdot (-1)$ and $Y_{22} = 0.546274$. Line L4 gives, in exact fractions,

$$M = \begin{pmatrix} 15/64 & 0 & 0 & 1/4 \\ 0 & -15/64 & 0 & 0 \\ 0 & 0 & 45/64 & 1/2 \\ 1/4 & 0 & 1/2 & 33/64 \end{pmatrix}.$$

| normal $n$ | $E_9(n) = \tilde n^T M \tilde n$ | exact $E(n)$ | error |
|---|---|---|---|
| $+z$ | 142/64 = 2.21875 | 2 | 0.21875 |
| $+x$ | 80/64 = 1.25 | 1 | 0.25 |
| $+y$ | 18/64 = 0.28125 | 0 | 0.28125 |
| $-z$ | 14/64 = 0.21875 | 0 | 0.21875 |

The total power is 3, so the bound is $3 \cdot 3/32 = 0.28125$. The normal $+y$ is perpendicular to both lights and reaches the bound. Point lights are the worst case for the method. A smooth sky is the best case: for the radiance $L = 1$ on the upper hemisphere and 0 below, the projection gives $L_{00} = \sqrt\pi$, $L_{10} = 0.488603\,\pi$ and 0 for the other seven coefficients, and $E_9(n) = \pi(1 + n_z)/2$, which is the exact irradiance.

## Correctness

Three facts make the algorithm correct; the [proof](proofs/correctness.md) gives all steps. First, by the Funk-Hecke theorem, the convolution with the clamped cosine maps each harmonic $Y_{lm}$ to $\hat A_l Y_{lm}$. Second, the quadratic form of line L7 equals $\sum_{l \le 2} \hat A_l L_{lm} Y_{lm}(n)$, term by term. Together they give $E_9 = E$ for lighting with no component above band 2 (a proved property). Third, for any lighting $L \ge 0$, $E_9(n) = \int L(\omega) A_9(n \cdot \omega)\, d\omega$ with $A_9(t) = 3/32 + t/2 + 15 t^2/32$. Since $|A - A_9| \le 3/32$, with equality at $t = 0$, the error is at most $3/32$ of $\int L\, d\omega$, the total light, at every normal (a proved bound). The same bound holds exactly for the texel sums, which is what the tests check.

The paper states the error in two ways (Section 3.1). The maximum error for any pixel, as a fraction of the total intensity of the lighting, is 9%, the value of $3/32$. The average error over all surface orientations is under 3% for any physical lighting, a result of Basri and Jacobs. For its three natural environment maps, the paper measured an average error under 1% and a maximum pixel error under 5% (a measurement). The stub summary of this page said only "an error below about three percent"; that number is an average, not a worst case.

## Complexity

The model is the real RAM, with one unit per arithmetic operation and per evaluation of $\sin$ and $\cos$, and $s$ texels.

- **Build: $\Theta(s)$.** Lines L2 and L3 do 9 multiply-adds for each texel. Line L4 is constant work. The paper compares this with the direct convolution of the map, which costs $\Theta(T s)$ for $T$ output texels, and reports under a second against about two hours for a $300 \times 300$ map on the hardware of 2001 (a measurement).
- **Evaluate: $\Theta(1)$.** Lines L6 and L7 cost 16 multiplications and additions per channel. There is no texture fetch.
- **Space: $\Theta(1)$.** The algorithm keeps 9 coefficients, or 10 distinct entries of the symmetric matrix, per channel. The output map is not stored.

## Properties

- **Exact for band limited lighting.** Lighting that is a polynomial of degree at most 2 in the direction gives the exact irradiance. The hemisphere sky above is one such case for the irradiance.
- **Error bound.** At most $3/32$ of the total light at any normal, for lighting that is not negative (proved). The bound is tight for a point light.
- **Linear in the lighting.** The coefficients and the matrix depend linearly on $L$, so the map of a sum of environments is the sum of their maps, and an environment can be blended over time by blending the matrices.
- **Smooth output.** $E_9$ is a quadratic polynomial in $n$, so it has no seams and no aliasing, and it needs no filtering.
- **Rotation.** A rotation of the environment mixes the coefficients only inside each band: $M$ goes to $R M R^T$ for the $4 \times 4$ rotation $R$ that acts on $(x, y, z)$ and keeps the last coordinate.

## Variants and improvements

- **Tabulated irradiance map.** The older way to get the same function is to convolve the environment with the clamped cosine into a small cube map, the irradiance map of Miller and Hoffman and Greene. It costs one texture fetch per pixel, and its memory and build cost are higher.
- **Coefficients in place of the matrix.** Many engines store the nine $\hat A_l L_{lm}$ values per channel and evaluate the sum of Equation 7 in the shader. It is the same function.
- **Fewer bands.** Bands 0 and 1 (four coefficients) give the constant and linear part only, with a larger error. More bands add little for the diffuse term, because $\hat A_l$ is small.
- **Windowing.** Bright small sources make $E_9$ go below zero on the far side, because the truncated series rings. A window on the coefficients, for example the Hanning window that Sloan describes, reduces the ringing and blurs the light. The window is tuning.
- **Probes in space.** One map per point of a grid gives an [irradiance volume](/irradiance-volume/), with interpolation between the probes.
- **Shadows and interreflection.** The method ignores visibility. [Precomputed radiance transfer](/precomputed-radiance-transfer/) adds them with a transfer vector per vertex.

## When to use it

Use it for the diffuse part of image-based lighting on dynamic objects, when the environment is far away and smooth enough, and when memory and bandwidth matter: nine numbers per channel replace a texture. It is a good fit for sky and probe lighting, and for lighting that changes every frame, because the projection is one pass. For sharp lighting such as a small sun, add the sun as a separate light and leave it out of the map. For glossy reflection, use a prefiltered map and the [split sum approximation](/split-sum-approximation/). For the reference answer, integrate the environment by [Monte Carlo integration](/monte-carlo-integration/).

## Pitfalls

- **Solid angles left out.** Line L3 must multiply by $\Delta\omega$. On a cube map or a latitude and longitude map, the texels near the corners or the poles have a smaller solid angle. Equal weights at line L3 give a biased $L_{lm}$.
- **Wrong axis convention.** The paper uses $z$ as the polar axis. In a $y$ up engine, either rotate the directions at line L3 and the normal at line L6 in the same way, or permute the entries of $M$. Mixing the two conventions gives light from the wrong side.
- **Forgetting $\hat A_l$, or applying it twice.** Line L4 already holds $\hat A_l$ in $c_1$ to $c_5$. If the code stores convolved coefficients $\hat A_l L_{lm}$ and then uses the matrix of line L4, the bands are scaled twice.
- **The $1/\pi$ of the BRDF.** Line L7 returns irradiance. The diffuse radiance is $\rho E / \pi$. Using $\rho E$ makes the surface $\pi$ times too bright.
- **Negative values.** For lighting with a bright small source, $E_9$ can be negative at normals that face away from it. Clamp the result of line L7 at 0, or window the coefficients.
- **Gamma encoded input.** The projection needs linear radiance. Decode an sRGB map first, see [gamma correction](/gamma-correction/).
- **Rounded constants.** The printed $c_2 = 0.511664$ and $c_3 = 0.743125$ come from the rounded basis constants; the exact values are $0.5116634$ and $0.7431239$. Compute them from $\pi$ when a check needs more than six digits.

## Implementations

## History

Reflection mapping goes back to Blinn and Newell (1976), and Miller and Hoffman (1984) convolved environment maps to get diffuse and glossy reflection maps; Greene (1986) stored environments as cube maps and also prefiltered them. These maps were built by direct convolution, which was slow. In 2001, Ramamoorthi and Hanrahan, and at the same time Basri and Jacobs in computer vision, showed that the clamped cosine acts as a low pass filter on the sphere, so that the irradiance is close to a function of the first nine spherical harmonics. Ramamoorthi and Hanrahan wrote it as a quadratic form in the normal that a vertex or pixel shader could evaluate. Spherical harmonics then became the common way to store diffuse lighting in games, in [precomputed radiance transfer](/precomputed-radiance-transfer/) (Sloan, Kautz and Snyder 2002) and in light probes.

## References
