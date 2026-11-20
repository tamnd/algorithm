---
tag: DAAJYN
kind: model
slug: reconfigurable-intelligent-surface
name: Reconfigurable intelligent surface
aliases:
- RIS
- intelligent reflecting surface
area: communications/mimo-communications
level: research
summary: "A model of a passive surface of N reflecting elements, each with a tunable phase, between a base station and a user. With the phases aligned, the received SNR grows as N squared."
prereqs: [mimo-channel-model, maximum-ratio-transmission, beamforming]
see_also: [hybrid-beamforming, semidefinite-programming, maximum-cut, np-hard, free-space-path-loss, rician-fading-channel, cell-free-massive-mimo, law-of-large-numbers]
sources:
  - paper: doi:10.1109/TWC.2019.2936025
    title: "Qingqing Wu and Rui Zhang, Intelligent reflecting surface enhanced wireless network via joint active and passive beamforming, IEEE Transactions on Wireless Communications 18(11), 5394-5409, 2019"
    locator: "the multiuser MISO model with a direct link and a link reflected by the surface, the phase shifts of the passive elements, the joint design of the active beamformer at the access point and the passive reflect beamformer, and the result that the transmit power can fall in proportion to 1/N^2 as the number N of elements grows"
---

A reconfigurable intelligent surface (RIS) is a flat panel of $N$ small passive elements. Each element reflects the wave that falls on it with a phase shift that a controller can set, but it does not amplify the wave and has no radio of its own. Placed on a wall between a base station and its users, the surface adds a reflected path whose phase, element by element, is under the control of the network. This page is the standard narrowband model of one base station with $M$ antennas, one RIS and one single-antenna user, as used by Wu and Zhang (2019) and much of the work that followed. The design problem in the model is to choose the base station precoder and the $N$ phases together.

## The machine

The base station sends $x \in \mathbb{C}^M$ with $\mathbb{E}\|x\|^2 \le P$ (in watts). The user receives

$$y = \left( h_d^H + h_r^H\, \Theta\, G \right) x + w, \qquad \Theta = \mathrm{diag}\!\left( e^{j\theta_1}, \ldots, e^{j\theta_N} \right), \qquad w \sim \mathcal{CN}(0, N_0),$$

where

- $h_d \in \mathbb{C}^M$ is the direct channel from the base station to the user,
- $G \in \mathbb{C}^{N \times M}$ is the channel from the base station to the RIS, with row $g_n^T$ for element $n$,
- $h_r \in \mathbb{C}^N$ is the channel from the RIS to the user, with entry $h_{r,n}$ for element $n$,
- $\theta_n$ is the phase shift of element $n$.

**Phases.** In the base model the phases are continuous, $\theta_n \in [0, 2\pi)$. In the quantized model with $b$-bit elements, $\theta_n \in \{0, 2\pi/2^b, \ldots, 2\pi(2^b - 1)/2^b\}$. The results below cover both models.

**Cascaded form.** Let $v = (e^{j\theta_1}, \ldots, e^{j\theta_N})^T$ and $\Phi = \mathrm{diag}(h_r^H)\, G \in \mathbb{C}^{N \times M}$. Then $h_r^H \Theta G = v^T \Phi$, and the effective channel

$$h^H(v) = h_d^H + v^T \Phi$$

is affine in $v$. Row $n$ of $\Phi$, $h_{r,n}^* g_n^T$, is the cascaded channel through element $n$.

**Standing assumptions.**

- Passive and lossless reflection: every element has gain of modulus exactly 1, so $|v_n| = 1$, and adds no noise.
- No coupling: the phase of one element does not change the reflection of another, and the reflection does not depend on the angle of arrival.
- Narrowband and quasi-static: the channels are flat in frequency and fixed over a block, and one $\Theta$ serves the whole band.
- Single reflection: waves that bounce more than once off the surface are neglected.
- Perfect channel knowledge: $h_d$, $G$ and $h_r$ (or $\Phi$) are known where the design is done.
- The fading law is left open. The examples here use independent Rayleigh fading on each link; a line-of-sight link from the base station to the RIS is often modeled as [Rician](/rician-fading-channel/).

## What it counts

- **Received SNR** for given $x$ and $\Theta$. With a beamformer $x = \sqrt{P}\, f\, s$, $\|f\| = 1$, $\mathbb{E}|s|^2 = 1$, it is $\mathrm{SNR} = \frac{P}{N_0} |h^H(v) f|^2$. For fixed $v$ the best $f$ is [maximum ratio transmission](/maximum-ratio-transmission/), $f = h(v)/\|h(v)\|$, which gives $\mathrm{SNR}(v) = \frac{P}{N_0} \|h_d^H + v^T \Phi\|^2$.
- **Rate**, $\log_2(1 + \mathrm{SNR})$ bits per channel use.
- **Transmit power** needed to reach a target SNR, and in the multiuser form the least total power that meets an SINR target for every user, which is the problem of Wu and Zhang (2019).
- **Gain over no RIS**, the ratio of $\max_v \mathrm{SNR}(v)$ to $\frac{P}{N_0}\|h_d\|^2$, and its growth with $N$.

## Relation to other models

- **MIMO channel model.** For a fixed $\Theta$ the model is a single-user MISO case of the [MIMO channel model](/mimo-channel-model/) with channel $h(v)$. The new part is that the channel itself has $N$ control variables.
- **Relays.** An amplify-and-forward relay also adds a second path, but it amplifies, adds its own noise and needs a radio. The RIS does none of these, so it costs little power, but it also gives no power gain of its own.
- **Hybrid beamforming.** The constraint $|v_n| = 1$ is the same as for the phase shifters of [hybrid beamforming](/hybrid-beamforming/). There the phase shifters are part of the transmitter; here they are in the environment, and the signal reaches them through $G$.
- **Path loss.** With [free-space path loss](/free-space-path-loss/) on each hop in the far field, the cascaded gain of each element is the product of the gains of the two hops, so the power of the reflected path falls as $1/(d_1^2 d_2^2)$ for distances $d_1$ to the RIS and $d_2$ from it (closed form under these assumptions). This "double path loss" is why a surface helps most when it is close to the base station or to the user.

## Known results in the model

1. **Optimal phases for one transmit antenna (theorem).** With $M = 1$, write $a_n = h_{r,n}^* g_n$ for the scalar cascaded channel. The SNR is $\frac{P}{N_0} |h_d^* + \sum_n a_n e^{j\theta_n}|^2$, and its maximum over continuous phases is

   $$\mathrm{SNR}^\star = \frac{P}{N_0} \left( |h_d| + \sum_{n=1}^{N} |a_n| \right)^2, \qquad \theta_n^\star = \arg(h_d^*) - \arg(a_n).$$

   Proof. By the triangle inequality $|h_d^* + \sum_n a_n e^{j\theta_n}| \le |h_d| + \sum_n |a_n|$, and the bound is reached when every term has the phase of $h_d^*$, which the given $\theta_n^\star$ does. $\square$

2. **The $N^2$ law (theorem).** In the setting of result 1, let the $|a_n|$ be independent with the same distribution and mean $\mu > 0$, and let $h_d$ be fixed. Then $\mathrm{SNR}^\star / N^2 \to \frac{P}{N_0}\, \mu^2$ almost surely as $N \to \infty$. Proof. By the strong [law of large numbers](/law-of-large-numbers/), $\frac{1}{N} \sum_n |a_n| \to \mu$, and $|h_d|/N \to 0$; square the sum. $\square$ For independent $h_{r,n} \sim \mathcal{CN}(0, \beta_r)$ and $g_n \sim \mathcal{CN}(0, \beta_g)$, $\mu = \frac{\pi}{4}\sqrt{\beta_r \beta_g}$. With random phases in place of $\theta^\star$, the mean SNR is $\frac{P}{N_0}(|h_d|^2 + N \beta_r \beta_g)$, which grows only linearly. The $N^2$ comes from coherent addition of $N$ reflected waves: the amplitude grows as $N$. In the same terms, the power needed for a fixed SNR falls as $1/N^2$, which is the scaling that Wu and Zhang (2019) point out. The law needs $N$ large enough for the reflected sum to pass the direct path, and the double path loss makes $\mu$ small.

   *Example.* Let $M = 1$, $h_d \sim \mathcal{CN}(0, 1)$ with $P/N_0 = 1$ (0 dB direct SNR on average), and let each cascaded channel $a_n$ be the product of two independent $\mathcal{CN}(0, 1)$ variables times 0.01, so each element is 40 dB weaker than the direct path. With independent links the mean of result 1 is $\frac{P}{N_0}\left(\mathbb{E}|h_d|^2 + 2N\,\mathbb{E}|h_d|\,\mu + N\,\mathbb{E}|a_n|^2 + N(N-1)\mu^2\right)$ with $\mathbb{E}|h_d| = \sqrt{\pi}/2$ and $\mu = 0.01\,\pi/4$ (closed form). This gives a mean SNR of 0.48, 1.79, 5.79 and 13.86 dB for $N = 8, 32, 128$ and $512$, while random phases give 0.003, 0.014, 0.055 and 0.217 dB. The reflected amplitude passes the direct one at $N = \mathbb{E}|h_d|/\mu \approx 113$.

3. **Loss from $b$-bit phases (theorem).** Let $h_d = 0$, round each $\theta_n^\star$ to the nearest of the $2^b$ allowed phases on a fixed grid, and let the phases of the $a_n$ be independent and uniform on $[0, 2\pi)$ and independent of the $|a_n|$, as for products of circular Gaussian variables. Then, as $N \to \infty$,

   $$\frac{\mathrm{SNR}_b}{\mathrm{SNR}^\star} \to \left( \frac{\sin(\pi/2^b)}{\pi/2^b} \right)^2 \quad \text{almost surely}.$$

   Proof. The rounding errors $\varepsilon_n$ are independent, uniform on $[-\pi/2^b, \pi/2^b)$, and independent of the $|a_n|$, because $\theta_n^\star$ is uniform and the grid is fixed. The received amplitude is $|\sum_n |a_n| e^{j\varepsilon_n}|$. By the strong law of large numbers, $\frac{1}{N}\sum_n |a_n| e^{j\varepsilon_n} \to \mu\, \mathbb{E}[e^{j\varepsilon}]$ and $\frac{1}{N}\sum_n |a_n| \to \mu$. For $\delta = \pi/2^b$, $\mathbb{E}[e^{j\varepsilon}] = \frac{1}{2\delta}\int_{-\delta}^{\delta} e^{j t}\, dt = \frac{\sin\delta}{\delta}$. Take the ratio and square. $\square$

   The loss is 3.92 dB for 1 bit, 0.91 dB for 2 bits and 0.22 dB for 3 bits. A simulation of the same setting (2000 trials per point, fixed seed, independent $\mathcal{CN}(0,1)$ factors) gives losses of the mean SNR of 3.34, 3.75, 3.89 and 3.91 dB for 1 bit at $N = 16, 64, 256, 1024$, of 0.81, 0.89, 0.91 and 0.91 dB for 2 bits, and of 0.20, 0.22, 0.22 and 0.22 dB for 3 bits (measurement). At small $N$ the loss is a little smaller than the limit.

4. **Multiple transmit antennas.** With maximum ratio transmission at the base station the design is $\max_{|v_n| = 1} \|h_d^H + v^T \Phi\|^2$. The objective equals $\|h_d + \Phi^H u\|^2$ with $u = v^*$, which also has unit-modulus entries. With $\bar u = (u^T, 1)^T$ and $A = [\Phi^H\ \ h_d] \in \mathbb{C}^{M \times (N+1)}$ this is the quadratic form $\bar u^H R\, \bar u$ with the Hermitian positive semidefinite matrix $R = A^H A$ of size $(N+1) \times (N+1)$, maximized over unit-modulus vectors.

   - *Hardness with 1-bit phases (theorem).* With phases in $\{0, \pi\}$, and with $M$ allowed to grow with $N$, the design problem is [NP-hard](/np-hard/). Proof. Reduce from [maximum cut](/maximum-cut/) on a graph with $N$ vertices and $E$ edges, no weights. For $v \in \{\pm 1\}^N$, the number of edges cut by the set $\{i : v_i = -1\}$ is $\frac{1}{4} v^T L v$, where $L = B B^T$ is the Laplacian and $B$ is the $N \times E$ oriented incidence matrix, with entries in $\{0, 1, -1\}$. Set $M = E$, $h_d = 0$, $h_r = (1, \ldots, 1)^T$ and $G = B$. Then $\Phi = G$ and $\|v^T \Phi\|^2 = v^T L v$, so an optimal 1-bit phase vector gives a maximum cut, and the instance has integer entries and polynomial size. $\square$ With continuous phases the problem is a nonconvex quadratic program with unit-modulus constraints, and no polynomial-time exact method is known for it in general.
   - *Semidefinite relaxation.* Replace $\bar u \bar u^H$ by a positive semidefinite matrix $V$ with $V_{nn} = 1$ for all $n$ and maximize $\mathrm{tr}(R V)$, a [semidefinite program](/semidefinite-programming/). Its value is an upper bound on the optimum. If $V$ has rank 1, its factor is optimal; otherwise, draw random vectors with covariance $V$, divide each by its last entry, project each entry to unit modulus and keep the best.
   - *Alternating optimization.* For fixed $v$ the best $f$ is maximum ratio transmission. For fixed $f$, the SNR is $\frac{P}{N_0}|h_d^H f + \sum_n v_n [\Phi f]_n|^2$, which result 1 maximizes in closed form. Each step does not decrease the SNR, and the SNR is bounded, so the sequence of values converges (theorem), in general to a local and not a global optimum.

5. **Multiple users.** With $K$ users, the base station sends $\sum_k w_k s_k$, and the SINR of user $k$ depends on all $w_k$ and on $v$. Wu and Zhang (2019) minimize the total transmit power subject to an SINR target for each user. The problem is nonconvex; for a fixed $v$ it is the usual downlink beamforming problem with effective channels $h_k(v)$, so the methods of result 4 combine with standard downlink beamforming designs.

## References
