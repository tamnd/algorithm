---
tag: QEHHHQ
kind: problem
slug: learning-parity-with-noise
name: Learning parity with noise
aliases:
- LPN
- LPN problem
area: cryptography/post-quantum
level: advanced
summary: Find a secret s from samples (a, <a,s> + e) with a uniform and e a biased coin, or tell such samples from random. The binary cousin of LWE, used by HB and other light protocols.
prereqs: [gaussian-elimination, linear-system-modulo-2]
see_also: [bkw-algorithm, learning-with-errors, syndrome-decoding-problem, information-set-decoding, code-based-cryptography, arora-ge-algorithm]
sources:
  - paper: "Avrim Blum, Merrick Furst, Michael Kearns and Richard J. Lipton, Cryptographic primitives based on hard learning problems, Crypto 1993, LNCS 773, pages 278 to 291"
    locator: the whole paper (pseudorandom generators and one-way functions from the hardness of learning parity with noise, and a search to decision reduction)
  - paper: "Avrim Blum, Adam Kalai and Hal Wasserman, Noise-tolerant learning, the parity problem, and the statistical query model, Journal of the ACM 50(4), pages 506 to 519, 2003"
    locator: the BKW algorithm in time 2^(O(n/log n)) for a constant noise rate
  - paper: "Nicholas J. Hopper and Manuel Blum, Secure human identification protocols, Asiacrypt 2001, LNCS 2248, pages 52 to 66"
    locator: the HB protocol and its security against passive attacks under LPN
  - paper: "Ari Juels and Stephen A. Weis, Authenticating pervasive devices with human protocols, Crypto 2005, LNCS 3621, pages 293 to 308"
    locator: the HB+ protocol with a blinding vector, and its proof against active attacks in the detection model
  - paper: "Henri Gilbert, Matthew Robshaw and Hervé Sibert, An active attack against HB+, a provably secure lightweight authentication protocol, Electronics Letters 41(21), pages 1169 to 1170, 2005"
    locator: the whole letter (a man in the middle adds a fixed vector to the challenges and learns one key bit per session from the reader's decision)
  - paper: "Benny Applebaum, David Cash, Chris Peikert and Amit Sahai, Fast cryptographic primitives and circular-secure encryption based on hard learning problems, Crypto 2009, LNCS 5677, pages 595 to 618"
    locator: the reduction that makes the secret follow the noise distribution
  - paper: "Michael Alekhnovich, More on average case vs approximation complexity, FOCS 2003, pages 298 to 307"
    locator: public-key encryption from LPN with a low noise rate
  - paper: "Éric Levieil and Pierre-Alain Fouque, An improved LPN algorithm, SCN 2006, LNCS 4116, pages 348 to 359"
    locator: the LF1 and LF2 variants of BKW, with the fast Walsh-Hadamard transform in the last step
  - paper: "Andre Esser, Robert Kübler and Alexander May, LPN decoded, Crypto 2017, LNCS 10401, pages 486 to 514"
    locator: the whole paper (LPN algorithms from information set decoding, and their cost for low noise)
---

Learning parity with noise (LPN) asks for a secret vector $s \in \mathbb{F}_2^n$ from noisy linear equations: each sample is $(a, \langle a, s \rangle + e)$, where $a$ is uniform and $e$ is 1 with a small probability $\tau$. Without noise, $n$ independent equations give $s$ by [Gaussian elimination](/gaussian-elimination/). With noise, the best known algorithms take time $2^{O(n/\log n)}$ for a constant $\tau$ ([BKW](/bkw-algorithm/)). Blum, Furst, Kearns and Lipton proposed it as a base for cryptography in 1993. LPN is the same as decoding a random linear code with random errors, and it is [learning with errors](/learning-with-errors/) with modulus 2. Its simplicity made it the base of the HB family of light authentication protocols.

**Notation.** $n$ is the length of the secret, which grows with the security parameter $\lambda$. $\tau \in (0, 1/2)$ is the noise rate and $\mathrm{Ber}_\tau$ the distribution with $\Pr[1] = \tau$. $\langle a, s \rangle = \sum_i a_i s_i$ over $\mathbb{F}_2$. $\mathcal{O}_{s,\tau}$ is the LPN oracle and $\mathcal{U}$ the oracle of uniform pairs $(a, b) \in \mathbb{F}_2^n \times \mathbb{F}_2$. $q$ is the number of samples, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. $H_2$ is the binary entropy function.

## In plain words

Someone has a secret string of $n$ bits. You may ask for as many random examples as you like. Each example is a random string $a$ and one bit: the parity of the secret bits at the positions where $a$ has a 1. But each answer bit is wrong, on purpose, with a small probability, such as 1 in 8.

Without the wrong bits, $n$ examples and school algebra give the secret. With them, a single wrong answer spoils the algebra, and you do not know which answers are wrong. The task is to find the secret anyway, or at least to tell these examples from coin flips.

## Definition

**The LPN oracle.** $\mathcal{O}_{s,\tau}$ returns, at each call, a fresh pair $(a, \langle a, s \rangle + e)$ with $a$ uniform in $\mathbb{F}_2^n$ and $e \leftarrow \mathrm{Ber}_\tau$ independent.

**Search LPN.** Given $q$ samples from $\mathcal{O}_{s,\tau}$ for a uniform $s$, output $s$. The success probability is $\Pr[\mathcal{A}^{\mathcal{O}_{s,\tau}} = s]$.

**Decision LPN.** Distinguish $\mathcal{O}_{s,\tau}$ from $\mathcal{U}$:

$$\mathrm{Adv}^{\mathrm{LPN}}_{n,\tau}(\mathcal{A}) = \left| \Pr[\mathcal{A}^{\mathcal{O}_{s,\tau}} = 1] - \Pr[\mathcal{A}^{\mathcal{U}} = 1] \right| .$$

The $(n, \tau)$-LPN assumption says that every $\mathcal{A}$ that runs in time polynomial in $n$ has negligible advantage. In matrix form, $q$ samples are $(A, b = As + e)$ with $A \in \mathbb{F}_2^{q \times n}$ uniform and $e \leftarrow \mathrm{Ber}_\tau^q$.

## Variants

- **Fixed number of samples.** The attacker gets only $q$ samples, as in most real uses; some algorithms (BKW) need many more samples than others (Gaussian elimination, information set decoding).
- **Low noise.** $\tau = n^{-c}$ for a constant $0 < c < 1$, for example $\tau = 1/\sqrt{n}$. Alekhnovich (2003) built public-key encryption from this case; constant noise is only known to give symmetric primitives.
- **Secret from the noise distribution.** $s \leftarrow \mathrm{Ber}_\tau^n$. Applebaum, Cash, Peikert and Sahai (2009) showed that it is as hard as uniform $s$.
- **Ring-LPN.** $a$ and $s$ live in a polynomial ring $\mathbb{F}_2[x]/(f)$, which gives shorter keys, as in the Lapin protocol; it has less evidence of hardness.
- **Exact LPN.** The noise vector of $q$ samples has exactly $\lfloor \tau q \rfloor$ ones, like the error of syndrome decoding.

## Examples

**A noise-free system.** Take $n = 4$ and $s = (1, 0, 1, 1)$. The four samples $a = (1,1,0,0)$, $(0,1,1,0)$, $(0,0,1,1)$, $(0,0,0,1)$ give the bits $1, 1, 0, 1$. Elimination gives $s_3 = 1$, then $s_2 = 0 + s_3 = 1$, then $s_1 = 1 + s_2 = 0$, then $s_0 = 1 + s_1 = 1$. If the last bit is wrong (0 instead of 1), elimination gives $(0, 1, 0, 0)$, which disagrees with about half of all fresh samples. So the attacker can test a candidate on new samples.

**The Gaussian elimination attack.** Draw $n$ fresh samples, solve, and test the candidate on fresh samples. A round succeeds when the $n$ samples have no noise, with probability $(1 - \tau)^n$, and when the matrix is invertible, with probability about $\prod_{i \ge 1}(1 - 2^{-i}) \approx 0.289$. For $n = 20$ and $\tau = 0.1$ the expected number of rounds is $1/(0.289 \cdot 0.9^{20}) \approx 28.5$; in 60 runs with a fixed seed the tests measured 25.2. For $n = 512$ and $\tau = 1/8$ it is about $2^{98.6}/0.289 \approx 2^{100}$ rounds, which is why low noise rates need larger $n$.

**HB authentication.** A tag and a reader share $x \in \mathbb{F}_2^k$. In each round the reader sends a random $a$, the tag answers $z = \langle a, x \rangle + \nu$ with $\nu \leftarrow \mathrm{Ber}_\eta$, and the reader accepts after $r$ rounds if at most $u r$ answers are wrong, with $\eta < u < 1/2$. The tests use $k = 32$, $\eta = 1/8$, $r = 100$ and a limit of 25 wrong answers. A passive eavesdropper sees LPN samples with secret $x$; the tests recover $x$ from transcripts by Gaussian elimination at $k = 24$, $\eta = 0.05$.

**The GRS attack on HB+.** HB+ adds a second secret $y$: the tag first sends a random blinding vector $b$, then answers $z = \langle a, x \rangle + \langle b, y \rangle + \nu$. Juels and Weis proved it secure against an attacker who can talk to the tag but not to the reader. Gilbert, Robshaw and Sibert attacked it in the middle: in session $i$ they add the unit vector $\delta = e_i$ to every challenge. The tag answers for $a + \delta$, so every answer changes by $\langle \delta, x \rangle = x_i$. If $x_i = 0$ the reader accepts as usual; if $x_i = 1$ almost all answers are wrong and the reader rejects. So $k$ sessions reveal $x$, and then the attacker passes as the tag by choosing $b = 0$ and answering $\langle a, x \rangle$. The tests run this attack at $k = 32$.

The Python code for these examples is for study only. It is not constant time and uses the random module; HB and HB+ are not safe protocols. Use a vetted library, for example a FIPS 140 validated module, for real authentication.

## Known algorithms

- **Exhaustive search.** Try all $2^n$ secrets and keep the one that agrees best with $O(n/(1 - 2\tau)^2)$ samples. Time $2^n$, few samples.
- **Gaussian elimination with noise.** As in the example: about $(1 - \tau)^{-n}$ rounds of $O(n^3)$ work. Polynomial when $\tau = O(\log n / n)$, and $2^{O(n^{1-c})}$ when $\tau = n^{-c}$.
- **[BKW](/bkw-algorithm/) (Blum, Kalai and Wasserman, 2003).** Add samples that agree on a block of coordinates to clear that block, level by level, at the cost of squaring the bias $1 - 2\tau$ at each level. Time, memory and samples $2^{O(n/\log n)}$ for constant $\tau$.
- **LF1 and LF2 (Levieil and Fouque, 2006).** BKW with a [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) to recover a whole block at the end, and other practical improvements.
- **Lyubashevsky (2005).** Turns $n^{1+\epsilon}$ samples into many more by adding small subsets, then runs BKW: time $2^{O(n/\log\log n)}$.
- **Decoding algorithms.** With a fixed number of samples, LPN is decoding a random code, so [information set decoding](/information-set-decoding/) applies; Esser, Kübler and May (2017) showed that this is the best approach for low noise.

## Bounds

- **Samples.** A unique answer needs about $q \ge n / (1 - H_2(\tau))$ samples, because a random code of rate $n/q$ above $1 - H_2(\tau)$ cannot be decoded at noise rate $\tau$. Maximum likelihood decoding reaches this with time $2^n$.
- **Upper bounds.** $2^{O(n/\log n)}$ time for constant $\tau$ (BKW); $e^{O(\tau n)}$ for small $\tau$ by Gaussian elimination.
- **Lower bounds.** No algorithm in time $2^{o(n/\log n)}$ is known for constant $\tau$. LPN is hard in the statistical query model, which BKW also showed. There is no proof of hardness from a worst-case problem comparable to that of LWE.

## Reductions

- **LPN and decoding.** $q$ samples are $b = As + e$, a codeword of the random code with generator matrix $A^T$ plus Bernoulli noise. With a parity check matrix $H$ of that code, $Hb = He$, an instance of the [syndrome decoding problem](/syndrome-decoding-problem/) with a random weight.
- **Search to decision.** Blum, Furst, Kearns and Lipton (1993) showed that an algorithm for decision LPN gives one for search LPN with the same $n$ and $\tau$ and a polynomial loss: to learn $s_i$, change the samples in a way that keeps them LPN samples if $s_i = 0$ and makes them uniform if $s_i = 1$.
- **LWE.** LPN is LWE with modulus $q = 2$ and Bernoulli errors. The worst-case lattice reductions of LWE need a larger modulus and do not cover LPN.
- **Secret from the noise.** Uniform secret LPN reduces to LPN with a secret drawn from $\mathrm{Ber}_\tau^n$ (Applebaum, Cash, Peikert and Sahai, 2009), with $n$ extra samples.

## Applications

- **Light authentication.** HB (Hopper and Blum, 2001) for humans and RFID tags, HB+ (Juels and Weis, 2005), and later variants such as HB# and Lapin after the GRS attack. They need only inner products and a biased coin.
- **Symmetric primitives.** Pseudorandom generators and one-way functions (Blum, Furst, Kearns and Lipton, 1993), and later MACs and symmetric encryption.
- **Public-key encryption.** From low-noise LPN (Alekhnovich, 2003), and code-based schemes such as [HQC](/hqc/) that use structured versions of the same problem.
- **Cryptanalysis.** Correlation attacks on stream ciphers and some side-channel attacks reduce to LPN, and BKW style algorithms solve them.

## References
