---
tag: H1WS41
kind: concept
slug: cell-free-massive-mimo
name: Cell-free massive MIMO
aliases:
- distributed massive MIMO
area: communications/mimo-communications
level: research
summary: Many access points spread over an area serve all users jointly on the same time and frequency resources, with no cell boundaries, coordinated through a central processor.
prereqs: [massive-mimo, maximum-ratio-transmission, lmmse-channel-estimation]
see_also: [pilot-contamination, max-min-sinr-power-control, second-order-cone-programming, bisection-method, channel-hardening, favorable-propagation, maximal-ratio-combining, log-distance-path-loss-model]
sources:
  - paper: doi:10.1109/TWC.2017.2655515
    title: "Hien Quoc Ngo, Alexei Ashikhmin, Hong Yang, Erik G. Larsson and Thomas L. Marzetta, Cell-free massive MIMO versus small cells, IEEE Transactions on Wireless Communications 16(3), 1834-1850, 2017"
    locator: "the cell-free system with distributed single-antenna access points, uplink pilots in TDD, conjugate beamforming in the downlink and matched filtering in the uplink, closed-form throughput expressions, max-min power control, pilot assignment, and the comparison of the 95%-likely per-user throughput with small cells"
---

Cell-free massive MIMO is a network in which $M$ access points (APs), spread over a large area, serve $K$ users together on the same time and frequency resources. There are no cells: every AP takes part in the service of every user. The APs connect over a fronthaul network to a central processing unit (CPU), which sends the data and the power control coefficients to the APs and combines what they receive. Each AP estimates its own channels from uplink pilots in time division duplex (TDD) and uses them locally, so no channel estimates go over the fronthaul. It is [massive MIMO](/massive-mimo/) with the antennas spread over the area in place of one array at one site. Ngo, Ashikhmin, Yang, Larsson and Marzetta (2017) defined the system with single-antenna APs and compared it with small cells.

## In plain words

In a normal cellular network, each phone talks to one base station, and a phone at the edge of a cell is far from its base station and close to the next one, which is a source of interference. In a cell-free network, many small antennas are spread out, for example on lamp posts, and all of them send to and listen to every phone at the same time. A phone is almost always close to some of the antennas, so there are no bad cell edges.

Each antenna learns its own channel to each phone from a short known signal and does its part of the work without help. A central computer only sends the data and tells each antenna how much power to give each phone. The main gain is not a higher peak speed but a much better speed for the users who are worst off.

## The idea

**Model.** AP $m$ has one antenna, and its channel to user $k$ is $g_{mk} = \sqrt{\beta_{mk}}\, h_{mk}$ with large-scale fading $\beta_{mk}$ and independent $h_{mk} \sim \mathcal{CN}(0, 1)$. The noise has unit power, $\rho_p$ and $\rho_d$ are the pilot and the downlink SNR, and the users send orthogonal pilots of length $\tau \ge K$. From the pilot, AP $m$ forms the MMSE estimate $\hat g_{mk}$ of $g_{mk}$ (see [LMMSE channel estimation](/lmmse-channel-estimation/)), which is $\mathcal{CN}(0, \gamma_{mk})$ with

$$\gamma_{mk} = \frac{\tau \rho_p\, \beta_{mk}^2}{\tau \rho_p\, \beta_{mk} + 1},$$

and the error $e_{mk} = g_{mk} - \hat g_{mk}$ is independent of $\hat g_{mk}$ with variance $\beta_{mk} - \gamma_{mk}$.

**Downlink with conjugate beamforming.** AP $m$ sends

$$x_m = \sqrt{\rho_d} \sum_{k=1}^{K} \sqrt{\eta_{mk}}\; \hat g_{mk}^{*}\, q_k,$$

where $q_k$ is the unit-power symbol of user $k$ and $\eta_{mk} \ge 0$ are power coefficients with $\sum_k \eta_{mk} \gamma_{mk} \le 1$, so each AP keeps $\mathbb{E}|x_m|^2 \le \rho_d$. Each AP applies maximum ratio transmission with its own estimates, and the array formed by all APs together beams toward each user. User $k$ receives $r_k = \sum_m g_{mk} x_m + w_k$.

**SINR (closed form).** If user $k$ treats the mean of its effective gain as known and everything else as noise, its SINR is

$$\mathrm{SINR}_k = \frac{\rho_d \left( \sum_{m} \sqrt{\eta_{mk}}\, \gamma_{mk} \right)^2}{\rho_d \sum_{k'=1}^{K} \sum_{m} \eta_{mk'}\, \gamma_{mk'}\, \beta_{mk} + 1}.$$

Proof. The mean gain is $\sqrt{\rho_d} \sum_m \sqrt{\eta_{mk}}\, \mathbb{E}[g_{mk} \hat g_{mk}^*] = \sqrt{\rho_d} \sum_m \sqrt{\eta_{mk}}\, \gamma_{mk}$, which gives the numerator. For $k' \ne k$, $g_{mk}$ and $\hat g_{mk'}$ are independent (orthogonal pilots), so $\mathrm{Var}(g_{mk} \hat g_{mk'}^*) = \beta_{mk} \gamma_{mk'}$. For $k' = k$, $\mathbb{E}|g_{mk} \hat g_{mk}^*|^2 = \mathbb{E}|\hat g_{mk}|^4 + \mathbb{E}|e_{mk}|^2\, \mathbb{E}|\hat g_{mk}|^2 = 2\gamma_{mk}^2 + (\beta_{mk} - \gamma_{mk})\gamma_{mk}$, so the variance is $\beta_{mk} \gamma_{mk}$ as well. The terms of different APs are independent, so the variances add, and the noise adds 1. $\square$

The rate $\log_2(1 + \mathrm{SINR}_k)$ is the lower bound on the achievable rate that is standard in massive MIMO analysis, and it is the type of closed form that Ngo et al. (2017) derive. With $\tau < K$ the pilots are reused and a [pilot contamination](/pilot-contamination/) term adds to the denominator.

**Max-min power control (theorem).** Choosing $\eta$ to maximize $\min_k \mathrm{SINR}_k$ under the per-AP power constraints is a quasi-concave problem, solved by [bisection](/bisection-method/) on a target $t$ with a [second-order cone](/second-order-cone-programming/) feasibility problem at each step. Proof. Set $c_{mk} = \sqrt{\eta_{mk}} \ge 0$. The power constraint $\sum_k c_{mk}^2 \gamma_{mk} \le 1$ is a norm bound on a vector linear in $c$. The condition $\mathrm{SINR}_k \ge t$ reads

$$\sqrt{t}\, \left\| \left( \sqrt{\rho_d\, \beta_{mk} \gamma_{mk'}}\; c_{mk'} \right)_{m, k'},\ 1 \right\|_2 \le \sqrt{\rho_d} \sum_m c_{mk}\, \gamma_{mk},$$

because both sides are nonnegative and squaring gives back the SINR condition. The left side is a norm of an affine function of $c$ and the right side is linear, so this is a second-order cone constraint, and the set of $c$ with all SINRs at least $t$ is convex. It shrinks as $t$ grows, so the largest feasible $t$ is found by bisection. $\square$ The same problem is the cell-free form of [max-min SINR power control](/max-min-sinr-power-control/).

**Uplink.** Each AP multiplies its received signal by $\hat g_{mk}^*$ (local [maximal-ratio combining](/maximal-ratio-combining/)) and sends the result to the CPU, which adds the contributions of all APs and decodes. The SINR has the same structure as in the downlink.

**Less channel hardening.** For one user the effective gain is close to $\sum_m |g_{mk}|^2$, whose variance over mean squared is $\sum_m \beta_{mk}^2 / (\sum_m \beta_{mk})^2$ (closed form, independent $h_{mk}$). In a collocated array all $\beta_{mk}$ are equal and this is $1/M$. In a cell-free network a few close APs dominate the sums, so the ratio stays large even for large $M$, and [channel hardening](/channel-hardening/) is weaker. The closed form above uses only the mean gain at the user, so in a cell-free network it can be far below the rate that a user with an estimate of its actual gain gets.

## Examples

**A simulation (measurement).** Put $M = 100$ APs on a $10 \times 10$ grid with spacing 1, so they cover a $9 \times 9$ square, drop $K$ users uniformly at random in the square, and set $\beta_{mk} = (1 + d_{mk}^2)^{-2}$ for the distance $d_{mk}$, $\rho_p = \rho_d = 100$ (20 dB at distance 0) and $\tau = K$. The cell-free system uses the closed form above with a simple power rule, $\eta_{mk} = 1 / \sum_{k'} \gamma_{mk'}$, so each AP sends at full power and splits it among the users in proportion to $\gamma_{mk}$. The small-cell system serves each user from one AP: in turn, each user takes the free AP with the largest $\beta_{mk}$, that AP sends at full power with perfect channel knowledge, the other serving APs interfere, and the unused APs are silent. Pilot overhead is not counted in either system, and no max-min power control is used. Over 300 random drops (fixed seed), the per-user rates in bits per channel use are:

| $K$ | cell-free, 5th percentile | cell-free, median | small cells, 5th percentile | small cells, median |
|---|---|---|---|---|
| 5 | 2.83 | 3.58 | 1.15 | 4.06 |
| 10 | 2.34 | 2.97 | 0.81 | 2.49 |
| 20 | 1.78 | 2.30 | 0.43 | 1.44 |

The rate that 95% of the users get or beat (the 5th percentile) is 2.5 to 4.1 times higher in the cell-free system. The median is not always higher: with $K = 5$, a user close to its own small-cell AP with few interferers does better alone. This matches the claim of Ngo et al. (2017) that the gain is in the 95%-likely throughput. They report close to a 5-fold gain with uncorrelated shadow fading in their model, with max-min power control (measurement, their setup). Their path loss model and power control differ from the simple ones here, so the numbers differ.

**Why the cell edge goes away.** A user halfway between two APs has $\beta$ about equal to both. In a small-cell system one of them is its server and the other is its strongest interferer. In the cell-free system both send its signal, coherently, and the numerator of the SINR gets $(\sqrt{\eta_{1k}}\gamma_{1k} + \sqrt{\eta_{2k}}\gamma_{2k})^2$, up to 4 times the power of one AP alone when the two terms are equal.

## Where it is used

- **Research on networks after 5G.** Cell-free massive MIMO is an active research topic for future radio access, often in user-centric forms in which each user is served only by the APs with the largest $\beta_{mk}$, to cut the fronthaul load.
- **Fronthaul design.** The local processing in the model above needs only data and power coefficients on the fronthaul. Centralized forms send the received signals to the CPU and use MMSE combining, which removes more interference at a higher fronthaul cost.
- **Power control and pilot assignment.** The closed form SINR turns the network design into a convex power control problem as shown above. Pilot assignment matters because users that share a pilot contaminate the estimates at every AP.
- **Indoor and campus networks.** Distributed antenna systems in buildings, stadiums and factories use the same idea of spreading antennas over the area and processing them jointly.

## References
