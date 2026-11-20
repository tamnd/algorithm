---
tag: Q4V2JM
kind: model
slug: saleh-valenzuela-model
name: Saleh-Valenzuela model
aliases:
- clustered multipath model
area: communications/fading-channels
level: advanced
summary: "An indoor channel model fitted to measurements: rays arrive in clusters, both with Poisson arrival times, and mean ray power decays exponentially in cluster delay and in ray delay."
prereqs: [tapped-delay-line-channel-model, delay-spread]
see_also: [tapped-delay-line-channel-model, delay-spread, wssus-channel-model, geometry-based-stochastic-channel-model, rayleigh-fading-channel, coherence-bandwidth, rake-receiver, sparse-channel-estimation]
sources:
  - paper: doi:10.1109/JSAC.1987.1146527
    title: Adel A. M. Saleh and Reinaldo A. Valenzuela, A statistical model for indoor multipath propagation, IEEE Journal on Selected Areas in Communications 5(2), 1987
    locator: pp. 128 to 137 (measurements with 10 ns pulses at 1.5 GHz in a medium-size office building, the clustered model and its fitted parameters)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.7.5 (Saleh and Valenzuela indoor statistical model)
  - book: isbn:9780470741863
    title: Andreas F. Molisch, Wireless Communications, second edition, Wiley, 2011
    locator: Section 7.3.2 (models for the power delay profile)
  - url: https://www.et.byu.edu/~bjeffs/publications/Spencer_JSAC_00.pdf
    title: Quentin H. Spencer, Brian D. Jeffs, Michael A. Jensen and A. Lee Swindlehurst, Modeling the statistical time and angle of arrival characteristics of an indoor multipath channel, IEEE Journal on Selected Areas in Communications 18(3), 2000
    locator: whole paper (an extension of the clustered model to angles of arrival, fitted to indoor measurements)
---

The Saleh-Valenzuela (SV) model describes the impulse response of an indoor channel as rays that arrive in clusters. Cluster arrival times and ray arrival times within a cluster are both Poisson processes, and the mean power of a ray decays exponentially both in the delay of its cluster and in its delay inside the cluster. Saleh and Valenzuela fitted it in 1987 to wideband measurements in an office building; it is a fit, not a law of propagation. Each realization of the model is a [tapped delay line](/tapped-delay-line-channel-model/) with random delays, and its mean power delay profile is a particular case of the delay profiles of the [WSSUS model](/wssus-channel-model/). [Geometry-based stochastic models](/geometry-based-stochastic-channel-model/) reach a similar cluster structure from the positions of scatterers instead of from arrival processes.

## The machine

The complex baseband impulse response is

$$h(\tau) = \sum_{l=0}^{\infty} \sum_{k=0}^{\infty} \beta_{kl}\, e^{j\theta_{kl}}\, \delta(\tau - T_l - \tau_{kl}),$$

where $T_l$ is the arrival time of cluster $l$ and $\tau_{kl}$ the delay of ray $k$ within cluster $l$, measured from $T_l$. The assumptions are:

- **Cluster arrivals.** $T_0 = 0$, and the later $T_l$ form a Poisson process of rate $\Lambda$: the gaps $T_l - T_{l-1}$ are independent and exponential with mean $1/\Lambda$.
- **Ray arrivals.** In each cluster $\tau_{0l} = 0$, and the later ray delays form an independent Poisson process of rate $\lambda$, with $\lambda \gg \Lambda$.
- **Double exponential decay.** The mean power of a ray is
  $$\mathbb{E}\,\beta_{kl}^2 = \overline{\beta^2}(0, 0)\, e^{-T_l/\Gamma}\, e^{-\tau_{kl}/\gamma},$$
  with $\Gamma$ the cluster decay constant and $\gamma$ the ray decay constant.
- **Rayleigh amplitudes and uniform phases.** Given the delays, $\beta_{kl}$ is Rayleigh with that mean power and $\theta_{kl}$ is uniform on $[0, 2\pi)$, all independent.
- **A static channel.** The 1987 measurements found a slowly varying channel, so the model has no Doppler. Each realization is one fixed channel, as in block fading, and new realizations stand for new positions. The model says nothing about channel knowledge; pages that use it state CSIR and CSIT.

The fitted values in the 1987 paper are $\Gamma = 60$ ns, $\gamma = 20$ ns, $1/\Lambda = 300$ ns and $1/\lambda = 5$ ns. They come from measurements with $10$ ns pulses at $1.5$ GHz in a medium-size office building, which showed delay spreads up to about $200$ ns and RMS values up to about $50$ ns. These numbers are measurements and fits for that building. Other buildings and frequencies need other values.

## What it counts

The model gives random impulse responses. The useful predictions are the mean power delay profile, the RMS [delay spread](/delay-spread/) of that profile, and the spread of these quantities over realizations.

**Mean power delay profile.** With the normalization $\overline{\beta^2}(0, 0) = 1$, the expected power at delay $t$ is a unit mass at $t = 0$ plus the density

$$p(t) = \lambda e^{-t/\gamma} + \Lambda e^{-t/\Gamma} + \Lambda\lambda\, \frac{e^{-t/\Gamma} - e^{-t/\gamma}}{1/\gamma - 1/\Gamma}, \qquad t > 0.$$

The four parts are the first ray of the first cluster, the later rays of the first cluster, the first rays of the later clusters, and the later rays of the later clusters.

**Total energy and its shares.** The mean energy is $(1 + \Lambda\Gamma)(1 + \lambda\gamma)$. With the 1987 values, $\Lambda\Gamma = 0.2$ and $\lambda\gamma = 4$, so the mean energy is $1.2 \cdot 5 = 6$. The first cluster carries $1/1.2 = 5/6$ of it, and the very first ray carries $1/6$.

**Mean delay and RMS delay spread.** With $m_C = \frac{\Lambda\Gamma^2}{1 + \Lambda\Gamma}$, $s_C = \frac{2\Lambda\Gamma^3}{1 + \Lambda\Gamma}$ and the same with $(\lambda, \gamma)$ for $m_R$ and $s_R$,

$$\bar\tau = m_C + m_R, \qquad \sigma_\tau^2 = (s_C - m_C^2) + (s_R - m_R^2).$$

For the 1987 values: $m_C = 10$ ns, $s_C = 1200$ ns$^2$, $m_R = 16$ ns and $s_R = 640$ ns$^2$. So $\bar\tau = 26$ ns and $\sigma_\tau = \sqrt{1100 + 384} = 38.5$ ns, in line with the RMS values up to about $50$ ns that were measured. Numerical integration of $p(t)$ and a Monte Carlo average over $4000$ realizations give the same values within $0.5\%$.

**Coherence bandwidth.** Fleury's bound with $\sigma_\tau = 38.5$ ns gives $B_c(0.5) \ge 1/(6\sigma_\tau) = 4.3$ MHz for the mean profile; see [coherence bandwidth](/coherence-bandwidth/).

## Relation to other models

- **Tapped delay line.** One realization, filtered to a bandwidth $W$ and sampled, is a [TDL](/tapped-delay-line-channel-model/) whose taps are sinc-weighted sums of rays. At $W = 100$ MHz, a $10$ ns resolution, rays $5$ ns apart on average are not resolved one by one: the model's rays describe the measured profile, not single reflections.
- **Exponential profile.** With $\Lambda \to 0$ there is one cluster, and the profile is a unit mass at $0$ plus $\lambda e^{-t/\gamma}$. For $\lambda\gamma \gg 1$ this is close to the exponential profile, whose RMS spread equals its decay constant.
- **WSSUS.** Uncorrelated scattering holds: rays have independent uniform phases. The model is static, so a Doppler spectrum must be added to each ray to get a time-varying WSSUS channel.
- **Angles.** Spencer, Jeffs, Jensen and Swindlehurst (2000) extended the cluster structure to angles of arrival, with a mean angle per cluster and a spread of ray angles around it. Geometry-based models such as COST 2100 also organize paths in clusters; see [geometry-based stochastic channel models](/geometry-based-stochastic-channel-model/).
- **Sparse channels.** A realization has a few strong rays and many weak ones. This is the structure that [sparse channel estimation](/sparse-channel-estimation/) exploits.

## Known results in the model

1. **The mean profile (a theorem about the model, by Campbell's theorem).** For a Poisson process of rate $\Lambda$ on $(0, \infty)$, $\mathbb{E}\sum_l g(T_l) = \Lambda\int_0^\infty g(T)\, dT$. Apply it first to the rays of one cluster and then to the clusters. The expected power that arrives in $[t, t + dt]$ is the convolution of the cluster measure $\delta(T) + \Lambda e^{-T/\Gamma}$ with the ray measure $\delta(\tau) + \lambda e^{-\tau/\gamma}$. The convolution of the two continuous parts is
   $$\int_0^t \Lambda e^{-T/\Gamma}\, \lambda e^{-(t - T)/\gamma}\, dT = \Lambda\lambda\, \frac{e^{-t/\Gamma} - e^{-t/\gamma}}{1/\gamma - 1/\Gamma},$$
   which gives $p(t)$ above.
2. **Energy and moments (closed forms under the model).** Because the mean profile is a convolution, its total mass is the product of the masses $1 + \Lambda\Gamma$ and $1 + \lambda\gamma$. After normalization it is the law of $T + \tau$ with $T$ and $\tau$ independent, so means and variances add. The cluster part has mean $\frac{\Lambda\Gamma^2}{1 + \Lambda\Gamma}$ and second moment $\frac{2\Lambda\Gamma^3}{1 + \Lambda\Gamma}$, from $\int_0^\infty T e^{-T/\Gamma} dT = \Gamma^2$ and $\int_0^\infty T^2 e^{-T/\Gamma} dT = 2\Gamma^3$, and likewise for the rays.
3. **A fit, not a derivation.** The Poisson arrivals and the exponential decays are chosen because they fit the measured profiles, not because they follow from the physics of the building (Saleh and Valenzuela 1987). Their parameters are measurements of one site.
4. **Realizations vary.** The mean profile hides large differences between realizations. Clusters arrive at random times, so the RMS delay spread of one realization is a random variable, and its mean need not equal the $38.5$ ns of the mean profile.

### Pitfalls

- **Truncation.** A simulation must stop the sums. Clusters that arrive after a time $T_{\max}$ carry the mean share $\frac{\Lambda\Gamma}{1 + \Lambda\Gamma} e^{-T_{\max}/\Gamma}$ of the energy. With the 1987 values and $T_{\max} = 10\Gamma = 600$ ns this is $7.6 \cdot 10^{-6}$. Stopping much earlier lowers the delay spread.
- **Normalization.** $\overline{\beta^2}(0, 0)$ is the mean power of the first ray, not of the whole channel. To get a channel with unit mean energy, divide by $(1 + \Lambda\Gamma)(1 + \lambda\gamma)$, here $6$.
- **Bandwidth.** Parameters fitted at $10$ ns resolution do not describe the channel at much finer resolution, as in ultra-wideband links; later models refit them.
- **The first ray.** The first ray of the first cluster is placed at delay $0$ with the largest mean power. Real line-of-sight paths can be much stronger than that; the model has no Rician term.

## References
