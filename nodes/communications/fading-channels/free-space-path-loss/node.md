---
tag: 5T32SC
kind: model
slug: free-space-path-loss
name: Free-space path loss
aliases:
- Friis transmission equation
- Friis formula
area: communications/fading-channels
level: intro
summary: "The loss (4 pi d / lambda)^2 between two isotropic antennas at distance d in free space: 20 dB more per decade of distance, and 100.05 dB at 1 km and 2.4 GHz."
see_also: [log-distance-path-loss-model, log-normal-shadowing, okumura-hata-model, multipath-fading, radar-range-equation, additive-white-gaussian-noise-channel, energy-per-bit-to-noise-density-ratio]
sources:
  - paper: doi:10.1109/JRPROC.1946.234568
    title: H. T. Friis, A note on a simple transmission formula, Proceedings of the IRE 34(5), 1946
    locator: pp. 254 to 256 (the ratio of received to transmitted power between two antennas in free space, written with the effective areas of the antennas)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 2.3 (free-space path loss) and Section 2.4.1 (the two-ray model)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 4.2 (free space propagation model, the Friis equation and the far-field distance)
---

Free-space path loss is the ratio of the transmitted power to the received power between two isotropic antennas at distance $d$ in empty space: $(4 \pi d / \lambda)^2$, where $\lambda$ is the wavelength. With the antenna gains added, the received power is given by the Friis transmission equation (Friis 1946). It is the one path loss model that follows from physics alone, and the other models of large-scale loss ([log-distance](/log-distance-path-loss-model/), [log-normal shadowing](/log-normal-shadowing/), [Okumura-Hata](/okumura-hata-model/)) are fits to measurements that use it as a reference. It says nothing about the fast changes of the signal over a few wavelengths; those are [multipath fading](/multipath-fading/).

## The machine

A transmitter sends a narrowband signal of power $P_t$ (W) at the carrier frequency $f_c$ (Hz), with the wavelength $\lambda = c / f_c$ and $c = 299\,792\,458$ m/s. The transmit antenna has the gain $G_t$ and the receive antenna has the gain $G_r$, both linear and in the direction of the other antenna (in dB they are given in dBi, relative to an isotropic antenna). The antennas are at the distance $d$ (m). The standing assumptions are:

- **Free space.** There is no ground, no obstacle and no absorption in the medium. One path joins the two antennas.
- **Far field.** $d \ge 2D^2/\lambda$, where $D$ is the largest dimension of the antenna, and also $d \gg D$ and $d \gg \lambda$. This is the Fraunhofer distance.
- **Matched antennas.** The polarizations and the impedances match, and each antenna points at the other.

Under these assumptions, the received power is

$$P_r = P_t \, G_t \, G_r \left(\frac{\lambda}{4 \pi d}\right)^2 .$$

This is the Friis transmission equation. The **free-space path loss** is the ratio for unit gains:

$$\mathrm{PL} = \left(\frac{4 \pi d}{\lambda}\right)^2 = \left(\frac{4 \pi d f_c}{c}\right)^2, \qquad \mathrm{PL}_{\mathrm{dB}} = 20 \log_{10}\frac{4 \pi d}{\lambda} = 20 \log_{10} d_{\mathrm{km}} + 20 \log_{10} f_{\mathrm{MHz}} + 32.45,$$

with $d$ in km and $f_c$ in MHz in the last form. The constant is $20 \log_{10}(4 \pi \cdot 10^9 / c) = 32.448$.

In complex baseband, the free-space link is $y = h x + w$ with a fixed gain $h = \sqrt{G_t G_r}\,\frac{\lambda}{4 \pi d}\, e^{-j 2 \pi d / \lambda}$ and noise $w \sim \mathcal{CN}(0, N_0)$. So $|h|^2 = G_t G_r / \mathrm{PL}$, and there is no fading.

## What it counts

The model predicts one number for each distance: the received power, or the loss in dB. The link budget in dB is

$$P_r(\mathrm{dBm}) = P_t(\mathrm{dBm}) + G_t(\mathrm{dBi}) + G_r(\mathrm{dBi}) - \mathrm{PL}_{\mathrm{dB}}(d) - L_{\mathrm{other}}(\mathrm{dB}),$$

where $L_{\mathrm{other}}$ collects cable and other losses. With the noise power $N_0 B$ in the band $B$, the receiver SNR is $P_r / (N_0 B)$. At the temperature $T_0 = 290$ K, $N_0 = k T_0$ is $-173.98$ dBm/Hz, and a receiver with noise figure $F$ adds $F$ dB.

From the same equation, the largest distance at which the received power is at least $P_{\min}$ is

$$d_{\max} = \frac{\lambda}{4 \pi} \sqrt{\frac{P_t G_t G_r}{P_{\min}}} .$$

**Example.** At $d = 1$ km and $f_c = 2.4$ GHz, $\mathrm{PL}_{\mathrm{dB}} = 20 \log_{10} 1 + 20 \log_{10} 2400 + 32.45 = 100.05$ dB. At 900 MHz the same distance gives 91.53 dB. At 100 m and 2.4 GHz the loss is 80.05 dB. A Wi-Fi link with $P_t = 20$ dBm (100 mW) and two antennas of 2 dBi then receives $20 + 2 + 2 - 80.05 = -56.05$ dBm. In a band of 20 MHz the thermal noise is $-173.98 + 10 \log_{10}(2 \cdot 10^7) = -100.97$ dBm, and with a noise figure of 7 dB it is $-93.97$ dBm. The SNR is about 37.9 dB.

**Example of the far-field condition.** A dish of diameter $D = 0.5$ m at 2.4 GHz ($\lambda = 0.1249$ m) has the Fraunhofer distance $2 \cdot 0.5^2 / 0.1249 = 4.0$ m. Closer than that, the equation does not apply.

## Relation to other models

- **Log-distance model.** The [log-distance path loss model](/log-distance-path-loss-model/) replaces the exponent 2 by a fitted exponent $n$, and often takes the free-space value at a reference distance $d_0$ as its intercept. Free space is the case $n = 2$.
- **Two-ray ground reflection.** Add one path reflected from a flat ground with reflection coefficient $-1$, with antenna heights $h_t$ and $h_r$. Beyond the critical distance $d_c = 4 h_t h_r / \lambda$, the received power is close to $P_t G_t G_r h_t^2 h_r^2 / d^4$, so the loss grows by 40 dB per decade and does not depend on the frequency (Goldsmith, Section 2.4.1). For $h_t = 30$ m, $h_r = 1.5$ m and 900 MHz, $d_c = 540$ m. At 5 km the exact two-ray loss is 114.94 dB, the $d^4$ form gives 114.89 dB, and free space gives 105.51 dB.
- **Empirical models.** The [Okumura-Hata model](/okumura-hata-model/) gives 126.40 dB at 1 km and 900 MHz in a city, 34.9 dB more than free space. Real paths lose more than free space because of the ground, buildings and foliage.
- **Shadowing and fading.** [Log-normal shadowing](/log-normal-shadowing/) adds a random term in dB to the mean loss. [Multipath fading](/multipath-fading/) multiplies the gain $h$ by a random factor that changes over a fraction of a wavelength.
- **Radar.** The [radar range equation](/radar-range-equation/) applies the same spreading twice, out to the target and back, so the received power falls as $d^{-4}$.
- **Noise model.** After the path loss, the link is an [AWGN channel](/additive-white-gaussian-noise-channel/) with the SNR found above.

## Known results in the model

1. **The Friis equation (a closed form under the stated assumptions).** Proof. An isotropic antenna spreads the power $P_t$ evenly over a sphere of area $4 \pi d^2$, so the power density at distance $d$ is $P_t / (4 \pi d^2)$ W/m$^2$. An antenna of gain $G_t$ multiplies the density in its main direction by $G_t$. A receive antenna collects the power that falls on its effective area $A_r$, so $P_r = P_t G_t A_r / (4 \pi d^2)$. For every antenna, the gain and the effective area satisfy $G = 4 \pi A / \lambda^2$ (Rappaport, Section 4.2). Put $A_r = G_r \lambda^2 / (4 \pi)$ in the last formula, and the result is $P_t G_t G_r \lambda^2 / (4 \pi d)^2$.
2. **Friis' own form.** With $G_t = 4 \pi A_t / \lambda^2$ as well, $P_r / P_t = A_t A_r / (d^2 \lambda^2)$. This is the form of Friis 1946.
3. **The inverse square law.** $\mathrm{PL}_{\mathrm{dB}}$ grows by $20 \log_{10} 2 = 6.02$ dB when $d$ doubles, and by 20 dB for each factor of 10.
4. **Range and power.** $d_{\max}$ grows as $\sqrt{P_t}$: 6.02 dB more power doubles the range in free space.

### Pitfalls

- **"Higher frequencies lose more."** The loss between isotropic antennas grows as $f_c^2$, but the medium does not cause it. It comes from the smaller effective area $\lambda^2 / (4 \pi)$ of an isotropic antenna at a short wavelength. With antennas of fixed area at both ends, item 2 shows that the received power grows as $f_c^2$.
- **The near field.** The equation is false for $d$ below the Fraunhofer distance. At $d \to 0$ it gives a received power larger than $P_t$.
- **Amplitude and power.** The loss in dB is $20 \log_{10}$ of the distance ratio because power falls as $d^{-2}$; a ratio of amplitudes uses $20 \log_{10}$ and a ratio of powers uses $10 \log_{10}$.
- **Units.** The constant 32.45 is for km and MHz. With m and Hz the constant is $-147.55$, and with km and GHz it is 92.45.

## References
