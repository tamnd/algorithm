---
tag: 2T84BT
kind: technique
slug: non-orthogonal-multiple-access
name: Non-orthogonal multiple access
aliases:
- NOMA
- power-domain NOMA
area: communications/multiple-access-and-spread-spectrum
level: advanced
summary: Serves several users on the same resource at different powers, with superposition coding and SIC at the receivers.
prereqs: [superposition-coding, successive-interference-cancellation, orthogonal-frequency-division-multiple-access]
see_also: [mac-capacity-region, sparse-code-multiple-access, ofdma-resource-allocation, multiuser-detection, near-far-problem, proportional-fair-scheduling, dirty-paper-coding, outage-probability]
sources:
  - paper: doi:10.1109/VTCSpring.2013.6692652
    title: Yuya Saito, Yoshihisa Kishiyama, Anass Benjebbour, Takehiro Nakamura, Anxin Li and Kenichi Higuchi, Non-orthogonal multiple access (NOMA) for cellular future radio access, IEEE 77th Vehicular Technology Conference (VTC Spring), Dresden, 2013
    locator: pp. 1 to 5 (downlink superposition with power allocation, SIC at the cell-center user, the comparison with OFDMA under proportional fair scheduling)
  - paper: doi:10.1109/LSP.2014.2343971
    title: Zhiguo Ding, Zheng Yang, Pingzhi Fan and H. Vincent Poor, On the performance of non-orthogonal multiple access in 5G systems with randomly deployed users, IEEE Signal Processing Letters 21(12), 2014
    locator: pp. 1501 to 1505 (outage probability and ergodic sum rate of downlink NOMA with fixed power fractions)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 6, Section 6.1 (uplink with successive interference cancellation) and Section 6.2 (downlink with superposition coding and the comparison with orthogonal schemes)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 15, Section 15.3 (the Gaussian multiple access channel) and Section 15.6 (the Gaussian broadcast channel)
---

Non-orthogonal multiple access (NOMA) puts two or more users on the same time-frequency resource and tells them apart by power. In the downlink the base station adds the users' signals with different power fractions, and each user with a good channel removes the signals of weaker users by [successive interference cancellation](/successive-interference-cancellation/) (SIC) before it decodes its own. In the uplink the users send at the same time, and the base station decodes them one after another with SIC. Power-domain NOMA is, in short, [superposition coding](/superposition-coding/) with SIC, run on top of an [OFDMA](/orthogonal-frequency-division-multiple-access/) grid with a scheduler that pairs users and splits power. The theory pages are [superposition coding](/superposition-coding/) for the downlink and the [MAC capacity region](/mac-capacity-region/) for the uplink; this page is about the system design: pairing, power fractions, decoding order and the losses of real receivers. Saito and coauthors at NTT DOCOMO proposed it for cellular radio access in 2013. A code-domain relative is [sparse code multiple access](/sparse-code-multiple-access/), which separates users by sparse codebooks instead of power.

## In plain words

In OFDMA each slice of the band carries one user. NOMA lets a slice carry two users at once.

The base station pairs a user near the cell center with a user at the cell edge. It sends both signals on the same slice. The edge user gets most of the power, and the center user gets a little.

The edge user decodes its own signal and ignores the weak one, which looks like a bit of noise. The center user hears both well. It first decodes the edge user's signal, removes it, and then decodes its own signal.

The edge user gets more air time than with turns, and the center user still gets a good rate with little power. The cost is a more complex receiver and a need to know which user is stronger.

## When it applies

- The users paired on one resource have very different channel gains, for example a cell-center user and a cell-edge user. The larger the gap, the larger the gain over orthogonal access.
- The base station knows the order of the channel gains, from channel reports in the downlink or from measurements in the uplink.
- The strong receivers can run SIC: decode the weak user's signal, rebuild it, and subtract it. This costs a second decoder pass.
- The goal is fairness, cell-edge rate or the number of users served, rather than the largest sum rate. In the downlink the largest sum rate on one resource comes from serving the strongest user alone.
- Many devices must be served at once with little data each, so orthogonal resources run out. NOMA lets more users than resource blocks share the grid.

## The template

**Downlink, two users on one resource.** The base station sends $x = \sqrt{a P}\, s_1 + \sqrt{(1 - a) P}\, s_2$ with unit-power symbols $s_1$ and $s_2$ and the power fraction $a \in (0, 1/2)$ for the strong user. User $k$ receives $y_k = h_k x + w_k$ with $w_k \sim \mathcal{CN}(0, N_0)$. Let $\gamma_k = P |h_k|^2 / N_0$ be the SNR of user $k$ if it got the whole power $P$, which is $E_s/N_0$ per complex symbol scaled by the gain; order the users so that $\gamma_1 \ge \gamma_2$ (user 1 is the strong user).

```pseudo id=main
NOMA-DOWNLINK(users, power P)
L1  pair users: one strong user 1 and one weak user 2 per resource      ▷ gamma_1 ≥ gamma_2
L2  choose the power fraction a for user 1, with a < 1/2
L3  send x ← sqrt(a P) s_1 + sqrt((1 - a) P) s_2
WEAK-RECEIVER(y_2)
L4  decode s_2, with the layer of user 1 as noise
STRONG-RECEIVER(y_1)
L5  decode s_2, with the layer of user 1 as noise
L6  y_1' ← y_1 - h_1 sqrt((1 - a) P) ŝ_2                                 ▷ SIC step
L7  decode s_1 from y_1'
```

With Gaussian codes and perfect SIC the rates are (a closed form, by the [superposition coding](/superposition-coding/) rates)

$$R_2 = \log_2\!\left(1 + \frac{(1 - a) \gamma_2}{a \gamma_2 + 1}\right), \qquad R_1 = \log_2(1 + a \gamma_1).$$

Step L5 works whenever L4 does, because the SINR of $s_2$ at user 1, $(1 - a) \gamma_1 / (a \gamma_1 + 1)$, is at least that at user 2 when $\gamma_1 \ge \gamma_2$.

**Uplink.** Users send $\sqrt{P_k} s_k$ at the same time and the base station receives $y = \sum_k h_k \sqrt{P_k} s_k + w$. It decodes the users one by one in a chosen order and subtracts each one. With Gaussian codes the rates are the vertices of the [MAC capacity region](/mac-capacity-region/), and time sharing between orders reaches the rest of the sum-rate face. In the uplink the decoding order is free; it changes who gets which rate, not the sum.

**Cost.** In the downlink the strong user runs two decoder passes per resource, and with $K$ users on one resource the strongest runs $K$. In the uplink the base station runs $K$ decoders in sequence per resource. Pairing $K$ users by an exhaustive search over pairs costs $O(K^2)$ pair evaluations per resource; most systems use a simple rule such as strongest with weakest.

## Classic examples

**Max-min rate, downlink.** Let $\gamma_1 = 100$ (20 dB) and $\gamma_2 = 10$ (10 dB). The fraction that gives both users the same rate is $a = 0.0591$, and then $R_1 = R_2 = 2.7893$ bits per channel use. With orthogonal access, the best equal rate, over all splits of time or band and of power between the two users, is 2.3013 (band fraction 0.3775 and power fraction 0.255 for user 1, found by a grid search). Plain time sharing gives 2.2766. NOMA gives both users 21 percent more. These are closed-form rates for Gaussian codes with perfect SIC, computed with a short script.

**Fixed power fraction.** With the same users and $a = 0.2$, the weak user gets $\log_2(1 + 8/3) = 1.8745$ and the strong user gets $\log_2 21 = 4.3923$. The strong user sees the weak user's layer at SINR $80/21 = 3.81$, above the 2.67 that the weak user itself sees, so the SIC step succeeds whenever the weak user's own decoding does.

**Sum rate is not the point.** On one resource the largest sum rate is $\log_2(1 + \gamma_1) = 6.6582$, reached by giving all power to the strong user. Every NOMA split has a lower sum rate, and so has every split of orthogonal access. Claims that NOMA beats OMA on sum rate compare against a fixed equal split, not against the best orthogonal schedule.

## Variations

- **Multiuser superposition transmission (MUST).** The form of downlink NOMA studied by 3GPP for LTE, with the two layers mapped to a joint constellation with Gray labels, as in the 4-PAM example of [superposition coding](/superposition-coding/).
- **Cooperative NOMA.** The strong user decodes the weak user's message anyway, so it can relay it in a second phase, which gives the weak user diversity.
- **MIMO-NOMA.** Users in the same beam share it by power. Users in different beams are separated by precoding. The MIMO downlink is not degraded, so SIC with superposition is no longer optimal; [dirty paper coding](/dirty-paper-coding/) is the limit there.
- **Code-domain NOMA.** Users are separated by sparse or low-correlation codes and a joint detector, not by power. [Sparse code multiple access](/sparse-code-multiple-access/) and low-density spreading belong here, and the receivers are those of [multiuser detection](/multiuser-detection/).
- **Grant-free NOMA.** Users send without a schedule and the base station detects who is active, the setting of [unsourced random access](/unsourced-random-access/) and of [coded slotted ALOHA](/coded-slotted-aloha/).
- **NOMA with OFDMA scheduling.** The scheduler of [OFDMA resource allocation](/ofdma-resource-allocation/) picks pairs per resource block, often by [proportional fair](/proportional-fair-scheduling/) metrics, as in Saito et al. 2013.

## Pitfalls

- **Imperfect SIC.** If the strong user's decoding of the weak layer fails, it subtracts the wrong signal, and its own decoding fails too. Even with correct decoding, channel estimation errors leave a residue $\epsilon$ of the weak layer, and the strong user's SINR becomes $a \gamma_1 / (\epsilon (1 - a) \gamma_1 + 1)$, which saturates at high SNR.
- **Wrong order.** With stale or wrong channel knowledge the order of the users can flip. Then the user that tries SIC cannot decode the other layer, and both users may fail.
- **Similar channels.** Two users with equal gains get no benefit from NOMA over time sharing; pair users with a large gap.
- **Power fraction near one half.** If $a$ is close to $1/2$, the two layers have about the same power and the strong user's first decoding step has a low SINR. Keep $a$ well below $1/2$ and use codes with margin.
- **Comparing against a weak baseline.** Compare NOMA with the best orthogonal schedule at the same total power, not with an equal split of time at equal power.
- **Privacy.** The strong user decodes the weak user's data as part of SIC.

## Exercises

1. For $\gamma_1 = 100$ and $\gamma_2 = 10$, verify that $a = 0.0591$ gives equal rates of about 2.79 bits per channel use.
2. Show that the SINR of $s_2$ at the strong user is at least the SINR at the weak user whenever $\gamma_1 \ge \gamma_2$.
3. Show that the downlink sum rate $R_1 + R_2$ grows with $a$ when $\gamma_1 > \gamma_2$. What does this say about a scheduler that maximizes the sum rate only?
4. With a SIC residue of $\epsilon = 0.01$ and $a = 0.2$, find the strong user's rate at $\gamma_1 = 100$ and at $\gamma_1 = 10^4$. Compare with perfect SIC.
5. In the uplink with $\mathrm{SNR}_1 = 10$ and $\mathrm{SNR}_2 = 5$, give the two rate pairs of SIC in the two orders, and check that both sums are 4.

## References
