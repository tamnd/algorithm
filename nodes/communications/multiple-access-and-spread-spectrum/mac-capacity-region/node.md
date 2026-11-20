---
tag: N91HDD
kind: theorem
slug: mac-capacity-region
name: Multiple access channel capacity region
aliases:
- Ahlswede-Liao region
- MAC capacity region
area: communications/multiple-access-and-spread-spectrum
level: advanced
summary: The set of rate tuples that users of a multiple access channel can reach together, a polymatroid for the Gaussian case.
prereqs: [channel-capacity, channel-coding-theorem, additive-white-gaussian-noise-channel]
see_also: [successive-interference-cancellation, superposition-coding, non-orthogonal-multiple-access, frequency-division-multiple-access, time-division-multiple-access, dirty-paper-coding, submodular-function, multiuser-diversity]
sources:
  - paper: "Rudolf Ahlswede, Multi-way communication channels, Proceedings of the 2nd International Symposium on Information Theory, Tsahkadsor, 1971, Akademiai Kiado, Budapest, 1973"
    locator: pp. 23 to 52 (the capacity region of the discrete memoryless channel with two senders and one receiver)
  - paper: "Henry Herng-Jiunn Liao, Multiple access channels, PhD dissertation, Department of Electrical Engineering, University of Hawaii, 1972"
    locator: The whole dissertation (the capacity region of the multiple access channel, found independently of Ahlswede)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 15, Section 15.3 (the multiple access channel, the achievability by joint typicality, the converse, the region for m users and the Gaussian multiple access channel) and the historical notes of Chapter 15
  - paper: doi:10.1109/18.737513
    title: David N. C. Tse and Stephen V. Hanly, Multiaccess fading channels, Part I, Polymatroid structure, optimal resource allocation and throughput capacities, IEEE Transactions on Information Theory 44(7), 1998
    locator: pp. 2796 to 2815 (the Gaussian region as a polymatroid, its vertices from the decoding orders, and the fading case)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 6, Section 6.1 (uplink AWGN channel, the capacity region, successive interference cancellation and the comparison with orthogonal multiple access)
---

The capacity region of a multiple access channel is the set of all rate tuples $(R_1, \ldots, R_K)$ at which $K$ independent senders can talk to one receiver at the same time with an error probability that goes to zero. A single number is not enough here, because one user's rate can be traded for another's. For the two-user Gaussian channel the region is a **pentagon**, and its two corner points are reached by successive decoding: decode one user while the other is noise, subtract it, then decode the other user clean. For $K$ Gaussian users the region is a **polymatroid**. This page states and proves the theorem. The schemes that reach parts of it are separate pages: [successive interference cancellation](/successive-interference-cancellation/) is the receiver, [FDMA](/frequency-division-multiple-access/) and [TDMA](/time-division-multiple-access/) are orthogonal schemes that reach one point of the boundary at best, and [non-orthogonal multiple access](/non-orthogonal-multiple-access/) is the practical form. The downlink, with one sender and many receivers, is a different channel; see [superposition coding](/superposition-coding/) and [dirty paper coding](/dirty-paper-coding/).

## Statement

**Theorem (Ahlswede 1971, Liao 1972; Cover and Thomas, Section 15.3).** (a) Let a discrete memoryless multiple access channel have inputs $X_1 \in \mathcal{X}_1$ and $X_2 \in \mathcal{X}_2$, output $Y$ and transition law $p(y \mid x_1, x_2)$. Each sender encodes its own message, uniform and independent of the other message, into a block of $T$ symbols, without seeing the other message. One receiver decodes both messages. The capacity region is the closure of the convex hull of the union, over product input laws $p(x_1) p(x_2)$, of the sets

$$R_1 \le I(X_1; Y \mid X_2), \quad R_2 \le I(X_2; Y \mid X_1), \quad R_1 + R_2 \le I(X_1, X_2; Y), \quad R_1, R_2 \ge 0.$$

For $K$ users the region has one bound for each nonempty subset $S$ of users: $\sum_{k \in S} R_k \le I(X_S; Y \mid X_{S^c})$.

(b) **Gaussian channel.** Let $y[t] = \sum_{k=1}^{K} x_k[t] + w[t]$ for $t = 1, \ldots, T$, with complex inputs, noise $w[t]$ i.i.d. $\mathcal{CN}(0, N_0)$, no fading, and an average power constraint per codeword, $\frac{1}{T} \sum_t |x_k[t]|^2 \le P_k$. The receiver knows all codebooks; no sender knows the others' messages. Define the SNR of user $k$ as $\mathrm{SNR}_k = P_k / N_0$, which is $E_s/N_0$ per complex symbol. Rates are in bits per complex channel use. Then the capacity region is the set of $R \ge 0$ with

$$\sum_{k \in S} R_k \le \log_2\!\left(1 + \sum_{k \in S} \mathrm{SNR}_k\right) \quad \text{for every nonempty } S \subseteq \{1, \ldots, K\}.$$

No convex hull is needed in (b). With $f(S) = \log_2(1 + \sum_{k \in S} \mathrm{SNR}_k)$ and $f(\emptyset) = 0$, the function $f$ is nondecreasing and submodular, so the region is the **polymatroid** of $f$. A polymatroid is the set of nonnegative vectors whose sum over each subset $S$ is at most $f(S)$, for a set function $f$ that is zero on the empty set, nondecreasing and [submodular](/submodular-function/). Its vertices are, for each order $\pi$ of the users,

$$R_{\pi(i)} = \log_2\!\left(1 + \frac{\mathrm{SNR}_{\pi(i)}}{1 + \sum_{l < i} \mathrm{SNR}_{\pi(l)}}\right), \quad i = 1, \ldots, K,$$

which is the rate of user $\pi(i)$ when it is decoded after users $\pi(i+1), \ldots, \pi(K)$ have been removed and users $\pi(1), \ldots, \pi(i-1)$ are still noise (Tse and Hanly 1998).

For two Gaussian users the region is the pentagon $R_1 \le \log_2(1 + \mathrm{SNR}_1)$, $R_2 \le \log_2(1 + \mathrm{SNR}_2)$, $R_1 + R_2 \le \log_2(1 + \mathrm{SNR}_1 + \mathrm{SNR}_2)$, with the corner points

$$A = \left(\log_2(1 + \mathrm{SNR}_1), \ \log_2\!\left(1 + \frac{\mathrm{SNR}_2}{1 + \mathrm{SNR}_1}\right)\right), \quad B = \left(\log_2\!\left(1 + \frac{\mathrm{SNR}_1}{1 + \mathrm{SNR}_2}\right), \ \log_2(1 + \mathrm{SNR}_2)\right).$$

## In plain words

Two people speak to one listener at the same time. Each can speak at some speed. If one speaks slowly, the other can speak fast, and the listener still follows both. The region is the list of all pairs of speeds that work.

Each speaker alone can never go faster than if the other were silent. And the two together can never go faster than one speaker with both voices' power. These three limits cut out a five-sided shape.

The best corners come from a simple trick. The listener first understands the louder message while the other one is still noise. Then the listener takes that message away and hears the second one clean. Swapping the order gives the other corner, and sharing time between the two orders fills the edge between them.

## Proof

We prove part (b) for $K = 2$; the argument for every subset $S$ in the $K$-user case is the same with $X_S$ in place of one input. Part (a) has the same structure with joint typicality decoding in place of the Gaussian codebooks (Cover and Thomas, Section 15.3). Logarithms are base 2, and $h(\cdot)$ is the differential entropy. A circularly symmetric complex Gaussian of variance $v$ has entropy $\log_2(\pi e v)$, the largest of all complex random variables with variance $v$.

**Achievability of the corner $A$.** Draw a codebook of $2^{T R_1}$ words for user 1 and $2^{T R_2}$ words for user 2, every symbol i.i.d. $\mathcal{CN}(0, P_k - \delta)$ for a small $\delta > 0$. The receiver first decodes user 2 and treats $x_1 + w$ as noise. Under the random code, $x_1[t] + w[t]$ is i.i.d. $\mathcal{CN}(0, P_1 - \delta + N_0)$ and independent of $x_2$, so user 2 sees a point-to-point Gaussian channel with SNR $(P_2 - \delta)/(P_1 - \delta + N_0)$. By the [channel coding theorem](/channel-coding-theorem/) for this channel, the error probability of this step goes to zero if $R_2 < \log_2(1 + (P_2 - \delta)/(P_1 - \delta + N_0))$. The receiver then subtracts the decoded $x_2$ and decodes user 1 from $x_1 + w$, which succeeds if $R_1 < \log_2(1 + (P_1 - \delta)/N_0)$. The union bound adds the two error probabilities. Let $\delta \to 0$; the power constraint holds with probability going to one, and the few codewords that break it can be dropped at no loss of rate. So every point below $A$ is achievable, and $B$ follows by exchanging the users.

**The rest of the pentagon.** Use the code of $A$ for a fraction $\lambda$ of the block and the code of $B$ for the rest. The rates are $\lambda A + (1 - \lambda) B$, and each user's average power is still $P_k$. So the whole segment from $A$ to $B$ is achievable. Note that $R_1^A + R_2^A = \log_2(1 + \mathrm{SNR}_1) + \log_2\!\big((1 + \mathrm{SNR}_1 + \mathrm{SNR}_2)/(1 + \mathrm{SNR}_1)\big) = \log_2(1 + \mathrm{SNR}_1 + \mathrm{SNR}_2)$, so the segment lies on the sum-rate line. A user can always send at a lower rate, so every point of the pentagon below the segment and below the single-user bounds is achievable.

**Converse.** Fix codes of block length $T$ with error probability $P_e^{(T)} \to 0$. The messages $W_1$ and $W_2$ are independent and uniform, and $x_k^T$ is a function of $W_k$ alone. By Fano's inequality, $H(W_1, W_2 \mid y^T) \le 1 + P_e^{(T)} T (R_1 + R_2) = T \epsilon_T$ with $\epsilon_T \to 0$. Then

$$T R_1 = H(W_1 \mid W_2) \le I(W_1; y^T \mid W_2) + T \epsilon_T \le I(x_1^T; y^T \mid x_2^T) + T \epsilon_T.$$

Given $x_2^T$, the output is $x_1^T + w^T$ plus a known term, so

$$I(x_1^T; y^T \mid x_2^T) = h(x_1^T + w^T \mid x_2^T) - h(w^T) \le \sum_{t=1}^{T} \big[h(x_1[t] + w[t]) - h(w[t])\big] \le \sum_{t=1}^{T} \log_2\!\left(1 + \frac{P_1[t]}{N_0}\right),$$

where $P_1[t] = E|x_1[t]|^2$, by independence of $x_1^T$ and $x_2^T$, the chain rule, conditioning that does not increase entropy, and the Gaussian maximum. The log is concave and $\frac{1}{T}\sum_t P_1[t] \le P_1$, so by Jensen's inequality $R_1 \le \log_2(1 + \mathrm{SNR}_1) + \epsilon_T$. The bound on $R_2$ is the same. For the sum,

$$T(R_1 + R_2) \le I(x_1^T, x_2^T; y^T) + T \epsilon_T \le \sum_{t=1}^{T} \big[h(y[t]) - h(w[t])\big] + T \epsilon_T.$$

The variance of $y[t]$ is $\mathrm{Var}(x_1[t]) + \mathrm{Var}(x_2[t]) + N_0 \le P_1[t] + P_2[t] + N_0$, because $x_1[t]$, $x_2[t]$ and $w[t]$ are independent. The Gaussian maximum and Jensen's inequality give $R_1 + R_2 \le \log_2(1 + \mathrm{SNR}_1 + \mathrm{SNR}_2) + \epsilon_T$. Let $T \to \infty$. The independence of the two inputs is the place where the separate encoders enter: with a common encoder, the cross term $2 \,\mathrm{Re}\, E[x_1 x_2^*]$ could raise the sum bound to $\log_2(1 + (\sqrt{\mathrm{SNR}_1} + \sqrt{\mathrm{SNR}_2})^2)$.

**Polymatroid and vertices.** For a set $S$ of users, write $s(S) = \sum_{k \in S} \mathrm{SNR}_k$. Then $f(S) = \log_2(1 + s(S))$ is a concave nondecreasing function of a sum of nonnegative weights, and such a function is submodular: for $S \subseteq T'$ and $k \notin T'$, $f(S \cup \{k\}) - f(S) = \log_2(1 + \mathrm{SNR}_k / (1 + s(S))) \ge \log_2(1 + \mathrm{SNR}_k/(1 + s(T'))) = f(T' \cup \{k\}) - f(T')$. Edmonds' greedy theorem on polymatroids says the vertices are the vectors $R_{\pi(i)} = f(\{\pi(1), \ldots, \pi(i)\}) - f(\{\pi(1), \ldots, \pi(i-1)\})$, one for each order $\pi$, which is the formula in the Statement. Each vertex is reached by successive decoding in the order $\pi(K), \pi(K-1), \ldots, \pi(1)$, by the same argument as for corner $A$. $\blacksquare$

## Consequences

- **Successive decoding is optimal at the vertices.** No joint decoder is needed at a vertex; a chain of single-user decoders with cancellation is enough. This is the basis of [successive interference cancellation](/successive-interference-cancellation/) and of uplink NOMA. Between vertices, the theorem uses time sharing. Rate splitting (Rimoldi and Urbanke 1996) reaches every point of the sum-rate face with successive decoding of split virtual users and no time sharing.
- **Orthogonal schemes and the sum capacity.** FDMA or TDMA under an average power constraint, with the fractions in proportion to the powers, reaches exactly one point of the sum-rate face: user $k$ gets $\alpha_k = \mathrm{SNR}_k / \sum_i \mathrm{SNR}_i$ of the resource and the rate $\alpha_k \log_2(1 + \sum_i \mathrm{SNR}_i)$. Every other split, and TDMA under a peak constraint, is strictly inside the region. See the example below.
- **Treating interference as noise loses rate.** If the receiver decodes each user with all others as noise, the sum rate is $\sum_k \log_2(1 + \mathrm{SNR}_k / (1 + s_{\mathrm{tot}} - \mathrm{SNR}_k))$ with $s_{\mathrm{tot}} = \sum_i \mathrm{SNR}_i$, which stays bounded as all powers grow at a fixed ratio. The capacity region has a sum rate that grows as $\log_2$ of the total power.
- **Equal powers.** With $K$ users of the same $\mathrm{SNR}$, the symmetric rate is $\frac{1}{K} \log_2(1 + K \,\mathrm{SNR})$ per user. The sum grows without bound in $K$, but each user's share goes to zero.
- **Fading.** With i.i.d. fading known to the receiver and the transmitters, the sum capacity is reached by letting only the user with the best channel send in each state, with power control (Knopp and Humblet 1995). This is [multiuser diversity](/multiuser-diversity/). Tse and Hanly 1998 give the full fading region through the polymatroid structure.
- **The downlink.** The broadcast channel (one sender, many receivers) has a different region. For the Gaussian scalar case it is reached by [superposition coding](/superposition-coding/), and for the MIMO case by [dirty paper coding](/dirty-paper-coding/). Under a sum power constraint, the two regions are linked by the uplink-downlink duality (Goldsmith, Section 14.7).

**Example (two users, checked by hand).** Let $\mathrm{SNR}_1 = 10$ and $\mathrm{SNR}_2 = 5$. The bounds are $R_1 \le \log_2 11 = 3.4594$, $R_2 \le \log_2 6 = 2.5850$ and $R_1 + R_2 \le \log_2 16 = 4$. The corners are $A = (3.4594, \log_2(16/11)) = (3.4594, 0.5406)$ and $B = (\log_2(16/6), 2.5850) = (1.4150, 2.5850)$. The sum rate is 4 at both corners. FDMA with $\alpha_1 = 2/3$ gives $(2.6667, 1.3333)$, on the segment $AB$. FDMA with $\alpha_1 = 1/2$ gives $(2.1962, 1.7297)$, a sum of 3.9259, just inside. TDMA with half the time each under a peak power constraint gives $(1.7297, 1.2925)$, a sum of 3.0222, well inside. The symmetric rate is $\frac{1}{2} \log_2 16 = 2$ for each user, which needs time sharing between $A$ and $B$ with $\lambda = (2 - 1.4150)/(3.4594 - 1.4150) = 0.286$. These numbers come from the formulas above and were checked with a short script.

## Tightness

- **Every bound is active.** For two users each of the three constraints holds with equality on some edge of the pentagon. The sum bound is strictly less than the sum of the single-user bounds whenever both SNRs are positive: in the example, $4 < 3.4594 + 2.5850 = 6.0444$. So the region is not a rectangle, and the users really do share a resource.
- **Gaussian inputs are optimal.** The converse uses only the entropy maximum of the Gaussian, so no other input law can do better. With a finite constellation such as QPSK, each bound becomes the mutual information of that constellation, and the region shrinks.
- **The convex hull is needed in (a).** For a discrete memoryless channel the union of pentagons over product laws need not be convex. Time sharing, or a time-sharing variable in the statement, is then part of the region. In (b) one input law (Gaussian at full power) gives every bound at once, so the union is already one convex polymatroid.
- **The hypotheses matter.** If the senders could cooperate, the sum bound would be larger, as noted in the proof. If the receiver must decode each user without the others' codebooks, or the senders are not frame synchronous, other regions apply. With fading, the region depends on what the senders know about the channel.

## History

Shannon 1961 posed the problem of channels with several senders and receivers in his paper on two-way channels. Ahlswede found the capacity region of the discrete memoryless channel with two senders and one receiver in his talk at the 1971 Tsahkadsor symposium, printed in 1973. Liao found it independently in his 1972 dissertation at the University of Hawaii, which is why the region is also called the Ahlswede-Liao region. The Gaussian case and the successive decoding argument for its corners are due to Cover and to Wyner in the mid 1970s (Cover and Thomas, historical notes of Chapter 15). Tse and Hanly 1998 showed that the Gaussian region is a polymatroid, gave its vertices as the decoding orders, and used this to solve the power and rate allocation in fading channels.

## References
