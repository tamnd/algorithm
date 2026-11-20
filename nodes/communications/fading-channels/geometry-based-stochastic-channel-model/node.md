---
tag: 573P89
kind: model
slug: geometry-based-stochastic-channel-model
name: Geometry-based stochastic channel model
aliases:
- GSCM
area: communications/fading-channels
level: advanced
summary: "A channel model that places scatterers at random by a distribution and derives the delay, angles and Doppler of each path from the geometry. COST 2100 is a fitted example."
prereqs: [clarke-model, tapped-delay-line-channel-model, wssus-channel-model]
see_also: [mimo-channel-model, kronecker-channel-model, clarke-model, saleh-valenzuela-model, wssus-channel-model, massive-mimo, beamforming, log-normal-shadowing]
sources:
  - paper: doi:10.1109/MWC.2012.6393523
    title: Lingfeng Liu, Claude Oestges, Juho Poutanen, Katsuyuki Haneda, Pertti Vainikainen, Francois Quitin, Fredrik Tufvesson and Philippe De Doncker, The COST 2100 MIMO channel model, IEEE Wireless Communications 19(6), 2012
    locator: pp. 92 to 99 (the COST 2100 model as a geometry-based stochastic channel model built from clusters)
  - url: https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/18.00.00_60/tr_138901v180000p.pdf
    title: 3GPP TR 38.901 V18.0.0 (Release 18), Study on channel model for frequencies from 0.5 to 100 GHz
    locator: Clause 7.5 (fast fading model), Clause 7.6 (additional modelling components) and Clause 7.7.1 (clustered delay line models)
  - book: isbn:9780470741863
    title: Andreas F. Molisch, Wireless Communications, second edition, Wiley, 2011
    locator: Section 7.4 (directional models, including geometry-based stochastic channel models) and Section 7.6 (standardized models)
  - paper: doi:10.1002/j.1538-7305.1968.tb00069.x
    title: R. H. Clarke, A statistical theory of mobile-radio reception, Bell System Technical Journal 47(6), 1968
    locator: pp. 957 to 1000 (isotropic scattering around a mobile, the limit case of a ring of scatterers)
---

A geometry-based stochastic channel model (GBSM, also GSCM) places scatterers, or clusters of scatterers, at random positions drawn from a chosen distribution, and computes each propagation path from the geometry. The delay, the angle of departure, the angle of arrival and the Doppler shift of a path then all follow from one position, so they fit together, and the channel changes in a consistent way when a terminal moves. The distributions are fitted to measurements: COST 2100 and the cluster models of 3GPP TR 38.901 are fitted models, not theorems. Compared with the [tapped delay line](/tapped-delay-line-channel-model/), which gives only delays and powers, and with the [Saleh-Valenzuela model](/saleh-valenzuela-model/), which draws arrival times directly, a GBSM gives the angles that multi-antenna systems need. Over a small area each realization behaves as a [WSSUS](/wssus-channel-model/) channel with a scattering function that is not separable.

## The machine

A transmitter and a receiver, each with an antenna array, are at known positions; the receiver may move with velocity $\mathbf v$. The model has three layers:

1. **Geometry.** Scatterers or clusters are drawn from a spatial distribution. Classic shapes are a ring around the mobile (one-ring), rings around both ends (two-ring) and ellipses with the two terminals at the foci. Cluster-based models such as COST 2100 draw clusters with their own delay and angle spreads, and make each cluster visible only from a region of terminal positions.
2. **Paths.** For a single-bounce path through a scatterer at $\mathbf s$, the delay is $\tau_p = (|\mathbf s - \mathbf x_T| + |\mathbf x_R - \mathbf s|)/c$, the angles are the directions of $\mathbf s$ seen from each end, and the Doppler shift is $\nu_p = \mathbf v \cdot \mathbf u_p / \lambda$, with $\mathbf u_p$ the unit vector from the receiver towards $\mathbf s$. Multiple-bounce paths are modelled through pairs of clusters.
3. **Gains.** Each path gets a mean power from a path loss law and from the cluster's decay with delay, and a random phase, usually uniform.

The output is a double-directional impulse response, a [MIMO channel](/mimo-channel-model/) that varies in time and delay:

$$\mathbf H(t, \tau) = \sum_p a_p\, e^{j 2\pi\nu_p t}\, \mathbf a_R(\phi_p^R)\, \mathbf a_T(\phi_p^T)^{\mathsf T}\, \delta(\tau - \tau_p),$$

where $\mathbf a_R$ and $\mathbf a_T$ are the array responses. The standing assumptions are plane waves at each array (scatterers in the far field of the arrays), specular paths and a static set of scatterers during a drive. The model describes time-correlated fading through the Doppler term. It is a model of the channel only; pages that use it state CSIR and CSIT.

## What it counts

- **Delays and powers.** The power delay profile and the [delay spread](/delay-spread/) follow from the distances to the scatterers.
- **Angles.** The angle spreads at each end, and so the correlation between antennas and the rank of the MIMO channel.
- **Doppler.** Each path's Doppler shift follows from its arrival direction. With scatterers all around the mobile the Doppler spectrum tends to the [Clarke spectrum](/clarke-model/).
- **Joint behavior.** Delays, angles and Doppler shifts are linked through geometry. As the terminal moves, delays drift, clusters appear and disappear, and the channel is not stationary over large distances.

### The one-ring model

The one-ring model is a GBSM simple enough to check by hand. A base station is at distance $D$ from a mobile, and scatterers lie on a ring of radius $R \ll D$ around the mobile, with angle $\psi$ uniform on the ring and equal powers. These are the assumptions of the closed forms below.

- **At the mobile.** Waves arrive from all directions with equal probability, which is Clarke's setting. Two mobile antennas spaced $d$ apart have correlation $J_0(2\pi d/\lambda)$, which is $0.5$ at $d = 0.242\lambda$.
- **At the base station.** The scatterers are seen within a small angle $\pm\Delta$ with $\Delta \approx R/D$. A scatterer at ring angle $\psi$ is seen at angle about $\Delta\sin\psi$ from the direction of the mobile. Two base station antennas spaced $d$ apart, broadside to the mobile, see a phase difference $2\pi d\Delta\sin\psi/\lambda$, and the average over uniform $\psi$ is $J_0(2\pi d\Delta/\lambda)$.
- **Numbers.** With $R = 50$ m and $D = 1$ km, $\Delta = 0.05$ rad. The base station correlation falls to $0.5$ at $d = 1.5211/(2\pi \cdot 0.05) = 4.84\lambda$, and to $0$ at $7.65\lambda$. An exact sum over $20000$ scatterers on the ring gives $0.9938$ at $0.5\lambda$, $0.9037$ at $2\lambda$ and $0.5004$ at $4.84\lambda$, in line with the approximation. So antennas at the base station must be about twenty times further apart than at the mobile to fade with the same low correlation.
- **Delays.** The path through the scatterer at $\psi$ has length about $D + R + R\cos\psi$, so the excess delay over the direct distance is $R(1 + \cos\psi)/c$, between $0$ and $2R/c = 333.6$ ns. Its mean is $R/c = 166.8$ ns and its RMS spread is $R/(c\sqrt2) = 117.9$ ns.

## Relation to other models

- **Clarke.** The one-ring model seen from a moving mobile is the [Clarke model](/clarke-model/); the GBSM adds the base station side and the delays.
- **Correlation-based MIMO models.** The [Kronecker model](/kronecker-channel-model/) gives each end a fixed correlation matrix and multiplies them. A GBSM produces the correlation from the scatterers; when the scatterers near each end act independently, the result is close to Kronecker, and when single clusters link the two ends it is not.
- **TDL and CDL.** For one antenna at each end, the angles fold into the path gains and a realization is a [TDL](/tapped-delay-line-channel-model/). 3GPP TR 38.901, Clause 7.7.1, tabulates clustered delay line (CDL) models: fixed lists of clusters with delays, powers and angles, a frozen realization for link-level tests.
- **3GPP TR 38.901.** Clause 7.5 draws cluster delays, powers and angles from distributions whose parameters are tabulated per scenario, rather than from explicit scatterer positions. Clause 7.6 adds components such as spatial consistency. The parameters are fits to measurement campaigns.
- **COST 2100.** Liu et al. (2012) describe it as a GSCM built from clusters, with the distributions fitted to measurements. It is used for [massive MIMO](/massive-mimo/) studies, where large arrays see different clusters across the array.
- **Large-scale effects.** Path loss and [log-normal shadowing](/log-normal-shadowing/) scale the cluster powers; in COST-type models they are part of the same parameter set.

## Known results in the model

1. **Base station correlation in the one-ring model (an approximation under $R \ll D$ and broadside antennas).** The phase difference is $2\pi d\,\theta/\lambda$ with $\theta \approx \Delta\sin\psi$. The mean of $e^{j 2\pi d\Delta\sin\psi/\lambda}$ over uniform $\psi$ is $\frac{1}{2\pi}\int_0^{2\pi} e^{jx\sin\psi}\, d\psi = J_0(x)$ with $x = 2\pi d\Delta/\lambda$. The exact sum quoted above confirms it at the values used.
2. **Mobile correlation and Doppler (a closed form under isotropic scattering).** With the scatterers uniform in angle around the mobile, the correlation in space is $J_0(2\pi d/\lambda)$ and the Doppler spectrum is the Clarke spectrum; the proofs are on the [Clarke model](/clarke-model/) page.
3. **Delay distribution of the one-ring model (a closed form under the same assumptions).** The excess delay $R(1 + \cos\psi)/c$ with uniform $\psi$ has the arcsine law on $[0, 2R/c]$, with mean $R/c$ and variance $R^2/(2c^2)$, since $\mathbb{E}\cos\psi = 0$ and $\mathbb{E}\cos^2\psi = 1/2$.
4. **Consistency (by construction).** All path parameters come from the same scatterer positions, so a moving terminal sees delays, angles and Doppler shifts that change together. Models that draw each quantity from its own distribution do not have this property unless they add it, as TR 38.901 does with spatial consistency.
5. **Fits, not theorems.** The spatial distributions, cluster counts, visibility regions and spreads of COST 2100 and TR 38.901 are fitted to measurements. A result derived inside such a model holds for the model; how well it holds for a real site is a question of measurement.

### Pitfalls

- **Geometry does not make a model physical.** Scatterer positions drawn from a fitted distribution are a way to produce consistent statistics. They are not a map of a real building or street.
- **Far-field assumption.** Large arrays or nearby scatterers break the plane-wave assumption across the array. Cluster visibility across a [massive MIMO](/massive-mimo/) array is one way models handle this.
- **Angle spread at the base station.** Using the mobile-side rule of half a wavelength for base station antennas overstates diversity badly: in the one-ring example the correlation at $0.5\lambda$ is still $0.994$.
- **Versions.** TR 38.901 has several releases with changes to the parameter tables. Quote the version, here V18.0.0, with any result.

## References
