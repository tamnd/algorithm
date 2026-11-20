---
tag: 3Q2A6K
kind: definition
slug: differential-phase-shift-keying
name: Differential phase-shift keying
aliases:
- DPSK
- DBPSK
- DQPSK
area: communications/modulation-and-detection
level: core
summary: PSK that carries the data in the phase change between consecutive symbols, so a receiver can detect it without a carrier phase reference.
prereqs: [phase-shift-keying, bit-error-rate]
see_also: [phase-shift-keying, noncoherent-detection, carrier-recovery, bit-error-rate, offset-qpsk, rayleigh-fading-channel, doppler-spread, gray-labeling]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 4 (optimum detection in additive white Gaussian noise, including differential PSK, its detector and its error probability)
  - paper: doi:10.1109/26.48887
    title: Dariush Divsalar and Marvin K. Simon, Multiple-symbol differential detection of MPSK, IEEE Transactions on Communications 38(3), 1990
    locator: pp. 300 to 308 (the conventional differential detector as the two-symbol case of a maximum-likelihood detector over N symbols, and the approach to coherent detection as N grows)
---

Differential phase-shift keying (DPSK) is [PSK](/phase-shift-keying/) in which the data selects the change of phase from one symbol to the next, not the phase itself. The receiver compares each received symbol with the one before it, so an unknown carrier phase cancels and no phase reference is needed. The cost is a loss in noise: about $0.75$ dB for binary DPSK at a bit error rate of $10^{-5}$, and close to $3$ dB for a large number of phases. DBPSK and DQPSK are the binary and four-phase cases.

## Definition

Let $M$ be a power of $2$ and $k = \log_2 M$. The data is a sequence of steps $m_1, m_2, \ldots$ in $\{0, 1, \ldots, M-1\}$, each from $k$ bits. The **M-ary DPSK** signal sends the symbols

$$s_0 = 1, \qquad s_n = s_{n-1}\, e^{j 2\pi m_n / M}, \quad n \ge 1,$$

where $j$ is the imaginary unit. So $s_n = e^{j\phi_n}$ with $\phi_n = \phi_{n-1} + 2\pi m_n/M$: the phase step carries the data. The first symbol is a reference and carries no data. A [Gray labeling](/gray-labeling/) of the steps makes neighboring steps differ in one bit. For $M = 2$ the bit $1$ gives a step of $\pi$ and the bit $0$ no step.

**The differential detector.** The receiver gets $r_n = e^{j\theta} s_n + w_n$, with an unknown phase $\theta$ and noise $w_n$. It forms

$$z_n = r_n\, r_{n-1}^{*}$$

and decides the step whose phase $2\pi m/M$ is nearest to $\arg z_n$. Without noise $z_n = e^{j 2\pi m_n/M}$: the factor $e^{j\theta}$ cancels. A phase that drifts slowly, by a small angle per symbol, only adds that angle to $\arg z_n$.

**Properties.**
- *No phase reference.* The receiver needs no [carrier recovery](/carrier-recovery/), and a phase jump in the channel costs at most one or two symbols.
- *Noncoherent optimality.* For DBPSK, $\mathrm{Re}(r_n r_{n-1}^*) > 0$ exactly when $|r_n + r_{n-1}| > |r_n - r_{n-1}|$, since $|a+b|^2 - |a-b|^2 = 4\,\mathrm{Re}(a b^*)$. The right side is the [noncoherent](/noncoherent-detection/) maximum-likelihood rule for the two signals $(1, 1)$ and $(1, -1)$ over two symbols with an unknown phase. So the differential detector is optimal for an observation of two symbols.
- *Bit error rate of DBPSK.* In white Gaussian noise, $P_b = \tfrac12 e^{-E_b/N_0}$. Coherent BPSK has $P_b = Q(\sqrt{2E_b/N_0})$, with $Q$ the [Gaussian Q function](/gaussian-q-function/).
- *Loss for larger M.* The noise in $z_n$ is the sum of two noise terms, from $r_n$ and from $r_{n-1}$. At high SNR, $M$-DPSK needs $\sin^2(\pi/M) / (2\sin^2(\pi/(2M)))$ times the energy of coherent $M$-PSK for the same symbol error rate. This factor is $0$ dB for $M = 2$, $2.32$ dB for $M = 4$, $2.84$ dB for $M = 8$, $2.97$ dB for $M = 16$, and it tends to $3$ dB.
- *Coherent detection of the same signal.* A receiver with a phase reference can detect each $s_n$ coherently and then take the difference of the decided phases. This removes the ambiguity of the carrier phase by multiples of $2\pi/M$, which a phase-locked loop leaves. Each wrong decision then spoils two steps: for BPSK, $P_b = 2p(1-p)$ with $p = Q(\sqrt{2E_b/N_0})$.

### The encoder and the detector

```pseudo id=main
DPSK-ENCODE(b_1, ..., b_{kN}, M)   ▷ k = log2 M
L1  s_0 ← 1   ▷ the reference symbol
    for n ← 1 to N
L2      m_n ← the step whose Gray label is the n-th group of k bits
L3      s_n ← s_{n-1} · e^{j2π m_n / M}
L4  return s_0, ..., s_N

DPSK-DETECT(r_0, ..., r_N, M)
    for n ← 1 to N
L5      z_n ← r_n · conj(r_{n-1})
L6      m̂_n ← round(M · arg(z_n) / (2π)) mod M
L7      output the Gray label of m̂_n as k bits
```

The tests check the examples below, recover random data for $M = 2, 4, 8, 16$ after an unknown phase and a drift of $1.8$ degrees per symbol, and show that coherent detection with a fixed reference fails under the same drift. They also measure the bit error rate of DBPSK and of coherent detection with differential decoding against the formulas above.

## Examples and non-examples

**DBPSK by hand.** The bits $1, 0, 1, 1, 0$ give the symbols $1, -1, -1, 1, -1, -1$. If the channel turns every symbol by $0.7$ rad, the products $r_n r_{n-1}^*$ are still $-1, 1, -1, -1, 1$, which give back $1, 0, 1, 1, 0$. A coherent BPSK receiver with a reference that is wrong by $\pi$ would invert every bit; the differential detector does not care.

**DQPSK by hand.** With the Gray labels $00 \to 0$, $01 \to \pi/2$, $11 \to \pi$, $10 \to 3\pi/2$, the bits $00\,01\,11\,10$ give the symbols $1, 1, j, -j, -1$.

**The cost in numbers.** At $E_b/N_0 = 10$ dB, DBPSK has $P_b = \tfrac12 e^{-10} = 2.27 \times 10^{-5}$. For $P_b = 10^{-5}$, DBPSK needs $E_b/N_0 = \ln(5 \times 10^4) = 10.82$, that is $10.34$ dB, and coherent BPSK needs $9.59$ dB: a loss of $0.75$ dB. At $E_b/N_0 = 4$ ($6.02$ dB) DBPSK has $P_b = 0.0092$ and coherent detection with differential decoding has $P_b = 0.0047$.

**Where it is used.** The $1$ and $2$ Mbit/s rates of the first IEEE 802.11 physical layer use DBPSK and DQPSK. The enhanced data rates of Bluetooth use $\pi/4$-DQPSK and 8DPSK. In $\pi/4$-DQPSK the steps are $\pm\pi/4$ and $\pm 3\pi/4$, so the phase changes at every symbol and never by $\pi$.

**Non-example: fast fading.** In a [Rayleigh fading channel](/rayleigh-fading-channel/) with a large [Doppler spread](/doppler-spread/), the channel phase changes between two symbols by a random amount. The differential detector then has an error floor: the error rate stops falling as the SNR grows. DPSK needs a channel that is close to constant over two symbols.

**Non-example: plain PSK.** In PSK the data is the absolute phase. A receiver must know the carrier phase, and a phase-locked loop on $M$-PSK has an ambiguity of a multiple of $2\pi/M$. Differential encoding is the usual way to remove this ambiguity, even in coherent receivers.

**Variation: detection over more symbols.** A detector that decides $N - 1$ steps jointly from $N$ received symbols with an unknown common phase closes most of the gap to coherent detection as $N$ grows. The ordinary differential detector is the case $N = 2$.

## Related definitions

- [Phase-shift keying](/phase-shift-keying/): the same constellation, detected with a phase reference.
- [Noncoherent detection](/noncoherent-detection/): the family of detectors without a phase reference; DPSK is its member with the best error rate for two symbols.
- [Carrier recovery](/carrier-recovery/): what a coherent receiver needs and a DPSK receiver can skip.
- [Bit error rate](/bit-error-rate/): $\tfrac12 e^{-E_b/N_0}$ for DBPSK, against $Q(\sqrt{2E_b/N_0})$ for BPSK.
- [Offset QPSK](/offset-qpsk/): another change to QPSK, which acts on the timing of the components and not on how the data is mapped to phase.

## References
