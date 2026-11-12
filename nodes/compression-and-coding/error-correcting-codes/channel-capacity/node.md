---
tag: MBQ0RF
kind: concept
slug: channel-capacity
name: Channel capacity
aliases:
- Shannon capacity of a channel
area: compression-and-coding/error-correcting-codes
level: core
summary: The largest mutual information between input and output of a channel, over all input laws. It is the highest rate of reliable communication, and Blahut-Arimoto computes it.
prereqs: [binary-symmetric-channel, binary-erasure-channel, conditional-entropy]
see_also: [channel-coding-theorem, additive-white-gaussian-noise-channel, shannon-entropy, source-coding-theorem, convex-optimization-problem, jensens-inequality, polar-code, forward-error-correction]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part II (the discrete channel with noise), Section 12 (equivocation and channel capacity) and Section 13 (the fundamental theorem for a discrete channel with noise)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 7.1 (examples of channel capacity, p. 184), Section 7.2 (symmetric channels, p. 189), Section 7.3 (properties of channel capacity, p. 191) and Section 10.8 (computation of channel capacity and the rate distortion function, p. 332)
  - paper: doi:10.1109/TIT.1972.1054855
    title: Richard E. Blahut, Computation of channel capacity and rate-distortion functions, IEEE Transactions on Information Theory 18(4), 1972
    locator: pp. 460 to 473 (the alternating maximization for the capacity of a discrete memoryless channel, with upper and lower bounds at each step)
  - paper: doi:10.1109/TIT.1972.1054753
    title: Suguru Arimoto, An algorithm for computing the capacity of arbitrary discrete memoryless channels, IEEE Transactions on Information Theory 18(1), 1972
    locator: pp. 14 to 20 (the iterative algorithm and its convergence)
---

The capacity of a noisy channel is the largest number of bits per channel use that can be sent with an error probability as small as one wants. Shannon defined it in 1948 as the largest mutual information between the input and the output, over all ways of choosing the input, and proved that this number is exactly the limit of reliable communication. For a few channels it has a closed form; for any discrete memoryless channel the Blahut-Arimoto algorithm computes it to any accuracy.

## In plain words

A channel takes a symbol in and gives a symbol out, but noise makes the output uncertain. Each output tells the receiver something about the input, but not everything. The capacity is the most that one output can tell about one input, on average, when the sender chooses well which inputs to use and how often.

The surprise is that this number is also a speed limit for perfect communication. Below it, long codes make errors as rare as we like. Above it, errors cannot be avoided, whatever code we use.

A channel that never makes mistakes with two inputs has a capacity of one bit per use. A channel whose output has nothing to do with its input has a capacity of zero.

## The idea

**Definition.** A discrete memoryless channel has finite input and output alphabets $\mathcal{X}$, $\mathcal{Y}$ and transition probabilities $W(y \mid x)$. For an input law $r$ on $\mathcal{X}$, the output law is $q(y) = \sum_x r(x) W(y \mid x)$, and the mutual information is

$$I(r, W) = H(Y) - H(Y \mid X) = \sum_{x, y} r(x) W(y \mid x) \log_2 \frac{W(y \mid x)}{q(y)}.$$

The **capacity** is

$$C = \max_{r} I(r, W) \quad \text{bits per channel use}.$$

The maximum exists because $I$ is continuous on the compact set of input laws. With the [conditional entropy](/conditional-entropy/), $I = H(Y) - H(Y \mid X) = H(X) - H(X \mid Y)$: the uncertainty about the input minus what is left after the output is seen.

**Why it is the right number.** The [noisy-channel coding theorem](/channel-coding-theorem/) gives $C$ its operational meaning: every rate $R < C$ has codes whose error probability tends to 0 as the block length grows, and no rate $R > C$ has. The definition above is a single-letter formula, which is what makes the theorem useful: a property of long blocks is computed from one use of the channel.

**Properties.**

1. $0 \le C \le \min(\log_2 |\mathcal{X}|, \log_2 |\mathcal{Y}|)$, because $I \ge 0$, $I \le H(X)$ and $I \le H(Y)$.
2. $I(r, W)$ is a concave function of $r$ for a fixed $W$. So computing $C$ is a [convex optimization problem](/convex-optimization-problem/): any local maximum is global.
3. **Optimality conditions.** An input law $r^*$ achieves capacity if and only if, with $q^*$ its output law, $D\bigl(W(\cdot \mid x) \,\|\, q^*\bigr) = C$ for every $x$ with $r^*(x) > 0$ and $D\bigl(W(\cdot \mid x) \,\|\, q^*\bigr) \le C$ for every other $x$, where $D$ is the relative entropy. The best output law $q^*$ is unique, but the best input law need not be.
4. **Symmetric channels.** If all rows of $W$ are permutations of each other and all columns are too, then the uniform input is best and $C = \log_2 |\mathcal{Y}| - H(\text{row})$.
5. **Feedback** does not raise the capacity of a discrete memoryless channel. **Zero error** is a different question: the zero-error capacity, where the error probability must be exactly 0, depends only on which pairs of inputs can be confused, and is often smaller.

**The Blahut-Arimoto algorithm.** For a channel without a closed form, alternate between the input law and the output law. Start with the uniform input law $r$ and repeat:

1. Compute the output law $q(y) = \sum_x r(x) W(y \mid x)$.
2. For each input, compute $c(x) = 2^{D(W(\cdot \mid x) \,\|\, q)}$.
3. The bounds $\log_2 \sum_x r(x) c(x) \le C \le \log_2 \max_x c(x)$ hold. Stop when they are closer than the tolerance.
4. Set $r(x) \leftarrow r(x) c(x) / \sum_{x'} r(x') c(x')$.

The update is the exact maximum of a function of two variables, $r$ and a backward channel $\phi(x \mid y) \propto r(x) W(y \mid x)$, taken in turn over each one, so $I$ never decreases. Each step costs $O(|\mathcal{X}| |\mathcal{Y}|)$ operations, the lower bound tends to $C$, and the two bounds give a certificate of accuracy at every step. Blahut and Arimoto published it independently in 1972. The lower bound is the value of the two-variable function at the next input law, which is at most its mutual information. The upper bound holds because $C \le \max_x D\bigl(W(\cdot \mid x) \,\|\, q\bigr)$ for every output law $q$, with equality at $q^*$.

## Examples

- **[Binary symmetric channel](/binary-symmetric-channel/)** with crossover probability $p$: $C = 1 - h(p)$, where $h$ is the [binary entropy function](/binary-entropy-function/). It is 0.5 at $p \approx 0.11$ and 0 at $p = 1/2$.
- **[Binary erasure channel](/binary-erasure-channel/)** with erasure probability $\varepsilon$: $C = 1 - \varepsilon$, the fraction of bits that arrive.
- **Z channel.** Input 0 always arrives as 0, and input 1 arrives as 0 with probability $p$. If 1 is sent with probability $u$, then $I = h\bigl(u(1 - p)\bigr) - u\,h(p)$. Setting the derivative to 0 gives $s = u(1 - p) = a/(1 + a)$ with $a = (1 - p) p^{p/(1 - p)}$, and then
  $$C = h(s) - s \frac{h(p)}{1 - p} = h(s) + s \log_2 a = \log_2\bigl(1 + (1 - p)\, p^{p/(1 - p)}\bigr),$$
  using $2^{-h(p)/(1 - p)} = a$ and $h(s) = \log_2(1 + a) - s \log_2 a$. At $p = 1/2$, $a = 1/4$, so $C = \log_2 1.25 \approx 0.322$, and the best input sends 1 with probability $0.4$, not $0.5$. The channel is not symmetric, so the uniform input is not best.
- **Noisy typewriter.** Each of 26 letters arrives as itself or as the next letter, each with probability $1/2$. Use only every other letter: those 13 inputs are never confused, so $C \ge \log_2 13$, and the symmetric channel formula gives $C = \log_2 26 - 1 = \log_2 13$.
- **A symmetric channel with three symbols** whose rows are rotations of $(0.5, 0.3, 0.2)$: $C = \log_2 3 - H(0.5, 0.3, 0.2) \approx 0.0995$ bits.
- **[Additive white Gaussian noise channel](/additive-white-gaussian-noise-channel/)** with power $P$ and noise variance $\sigma^2$: $C = \frac12 \log_2(1 + P/\sigma^2)$ per real use. The input alphabet is not finite here; a power limit replaces the finite alphabet, and the best input law is Gaussian.

## Where it is used

- **Judging codes.** Engineers report how far a code operates from capacity, in rate at a fixed noise level or in decibels of $E_b/N_0$ at a fixed rate. [Turbo codes](/turbo-code/), [LDPC codes](/ldpc-code/) and [polar codes](/polar-code/) are called capacity-approaching or capacity-achieving by this yardstick.
- **System design.** Capacity tells how much rate a link can support at a given power and bandwidth, and so whether better codes or more power are worth seeking.
- **Constrained inputs.** Blahut-Arimoto computes the capacity of quantized channels, of a modulation with a fixed set of signal points, and of channels measured in the laboratory, where there is no formula. A close relative computes the rate distortion function of lossy compression.
- **Joint design with compression.** The source-channel separation result says that a source of entropy rate $H$ can be sent reliably over a channel exactly when $H < C$, so [source coding](/source-coding-theorem/) and channel coding can be designed apart.

## References
