---
tag: FBQ8D7
kind: definition
slug: perfect-secrecy
name: Perfect secrecy
aliases:
- Shannon secrecy
- information-theoretic secrecy
area: cryptography/symmetric-ciphers
level: intro
summary: An encryption scheme is perfectly secret if the ciphertext does not change the probability of any message, for every message distribution, even for an attacker with unlimited power.
prereqs: [symmetric-encryption]
see_also: [one-time-pad, shannon-perfect-secrecy-theorem, semantic-security, ind-cpa-security, bayes-theorem, conditional-entropy, shannon-entropy, ciphertext-only-attack]
sources:
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949, pp. 656-715
    locator: Part II, the section on perfect secrecy (the definition by a posteriori probabilities equal to a priori probabilities)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 2.1 (the definition of perfect secrecy, the equivalent formulation by ciphertext distributions, and perfect indistinguishability by the eavesdropping experiment)
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 3.3 (perfect secrecy, and the shift cipher with a new key for each letter)
---

An encryption scheme has perfect secrecy when seeing the ciphertext tells an attacker nothing new about the message: the probability of each message after the ciphertext is known equals its probability before. The attacker may have unlimited time and memory; the guarantee is about information, not about computation. Shannon gave the definition in 1949 and showed that the [one-time pad](/one-time-pad/) meets it. Three other forms are equivalent to it: the message and the ciphertext are independent, every message gives the same ciphertext distribution, and no attacker can tell which of two chosen messages was encrypted with a success probability above one half. The price is a key at least as large as the message, by [Shannon's theorem](/shannon-perfect-secrecy-theorem/).

## Definition

An encryption scheme $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ has a message space $\mathcal{M}$, a key space $\mathcal{K}$ and a ciphertext space $\mathcal{C}$, all finite. $\mathrm{Gen}$ outputs a key $K$ with some fixed distribution. $\mathrm{Enc}_k(m)$ may use its own randomness, independent of everything else, and $\mathrm{Dec}_k(\mathrm{Enc}_k(m)) = m$ always. For a random variable $M$ on $\mathcal{M}$, independent of $K$, let $C = \mathrm{Enc}_K(M)$.

**Definition (perfect secrecy).** $\Pi$ is *perfectly secret* if for every distribution of $M$, every message $m \in \mathcal{M}$ and every ciphertext $c \in \mathcal{C}$ with $\Pr[C = c] > 0$,
$$\Pr[M = m \mid C = c] = \Pr[M = m].$$

**Theorem (equivalent forms).** For a scheme $\Pi$ as above, the following are equivalent.

1. $\Pi$ is perfectly secret.
2. *Independence.* For every distribution of $M$, the random variables $M$ and $C$ are independent.
3. *Equal ciphertext distributions.* For all $m, m' \in \mathcal{M}$ and every $c \in \mathcal{C}$, $\Pr[\mathrm{Enc}_K(m) = c] = \Pr[\mathrm{Enc}_K(m') = c]$, where the probability is over $K$ and the randomness of $\mathrm{Enc}$.
4. *Perfect indistinguishability.* In the experiment below, every adversary $\mathcal{A}$, with no limit on its running time, succeeds with probability exactly $1/2$. The adversary outputs two messages $m_0, m_1 \in \mathcal{M}$; a key $K$ and a bit $b$ are chosen uniformly and independently; $\mathcal{A}$ receives $c = \mathrm{Enc}_K(m_b)$ and outputs a bit $b'$; it succeeds if $b' = b$.

*Proof.* We prove $1 \Leftrightarrow 2$, $1 \Leftrightarrow 3$ and $3 \Leftrightarrow 4$.

*$1 \Rightarrow 2$.* Fix a distribution of $M$. If $\Pr[C = c] > 0$, then $\Pr[M = m, C = c] = \Pr[M = m \mid C = c] \Pr[C = c] = \Pr[M = m] \Pr[C = c]$. If $\Pr[C = c] = 0$, both sides are 0. So $M$ and $C$ are independent. *$2 \Rightarrow 1$.* If $\Pr[C = c] > 0$, divide $\Pr[M = m, C = c] = \Pr[M = m] \Pr[C = c]$ by $\Pr[C = c]$.

*$3 \Rightarrow 1$.* Let $p_c$ be the common value of $\Pr[\mathrm{Enc}_K(m) = c]$. Fix a distribution of $M$. Since $M$ is independent of $K$ and of the randomness of $\mathrm{Enc}$, $\Pr[C = c \mid M = m] = \Pr[\mathrm{Enc}_K(m) = c] = p_c$ for each $m$ with $\Pr[M = m] > 0$. So $\Pr[C = c] = \sum_m \Pr[M = m] \, p_c = p_c$. If $p_c > 0$, Bayes' rule gives $\Pr[M = m \mid C = c] = p_c \Pr[M = m] / p_c = \Pr[M = m]$.

*$1 \Rightarrow 3$.* Take $M$ uniform on $\mathcal{M}$, so $\Pr[M = m] = 1/\lvert \mathcal{M} \rvert > 0$ for each $m$. Fix $c$. If $\Pr[C = c] > 0$, then by perfect secrecy and Bayes' rule
$$\Pr[\mathrm{Enc}_K(m) = c] = \Pr[C = c \mid M = m] = \frac{\Pr[M = m \mid C = c] \Pr[C = c]}{\Pr[M = m]} = \Pr[C = c],$$
which does not depend on $m$. If $\Pr[C = c] = 0$, then $\Pr[\mathrm{Enc}_K(m) = c] \le \Pr[C = c] / \Pr[M = m] = 0$ for each $m$. In both cases the value is the same for all $m$.

*$3 \Rightarrow 4$.* Fix the coins of $\mathcal{A}$, and so the pair $m_0, m_1$. By form 3, $c$ has the same distribution when $b = 0$ and when $b = 1$. Let $q$ be the probability that $\mathcal{A}$ outputs 1 on a ciphertext with this distribution. Then the success probability is $\frac12 (1 - q) + \frac12 q = \frac12$. Averaging over the coins of $\mathcal{A}$ keeps the value $\frac12$.

*$4 \Rightarrow 3$.* Suppose form 3 fails: there are $m_0, m_1, c$ with $p_0 = \Pr[\mathrm{Enc}_K(m_0) = c] > p_1 = \Pr[\mathrm{Enc}_K(m_1) = c]$ (swap the names if needed). The adversary that outputs $m_0, m_1$, and then outputs $b' = 0$ if it sees $c$ and $b' = 1$ otherwise, succeeds with probability $\frac12 p_0 + \frac12 (1 - p_1) = \frac12 + \frac12 (p_0 - p_1) > \frac12$. So form 4 fails. $\blacksquare$

In terms of [entropy](/shannon-entropy/), form 2 says that the mutual information of $M$ and $C$ is zero, or $H(M \mid C) = H(M)$ with the [conditional entropy](/conditional-entropy/), for every distribution of $M$.

## Examples and non-examples

- **The one-time pad.** XOR with a uniform key of the same length. For every $m$ and $c$, exactly one key maps $m$ to $c$, so $\Pr[\mathrm{Enc}_K(m) = c] = 2^{-N}$ for all $m$: form 3 holds. The code of the [one-time pad](/one-time-pad/) checks this by exact enumeration for 2-bit messages with the prior $(1/2, 1/4, 1/8, 1/8)$.
- **The shift cipher on one letter.** With a uniform key in $\mathbb{Z}_{26}$ and a message of one letter, each letter goes to each cipher letter with probability $1/26$. So the [Caesar cipher](/caesar-cipher/) is perfectly secret if a new key is used for each letter, which makes it a one-time pad on letters.
- **Non-example: the shift cipher on two letters.** With one key for both letters, the ciphertext keeps the difference of the two letters. The ciphertext BB can come from AA (key 1) but never from AB, so $\Pr[\mathrm{Enc}_K(\mathrm{AA}) = \mathrm{BB}] = 1/26 \ne 0 = \Pr[\mathrm{Enc}_K(\mathrm{AB}) = \mathrm{BB}]$.
- **Non-example: too few keys.** XOR on 2 bits with the keys 00 and 11 only. With the prior above, the ciphertext 00 gives the posterior $4/5$ for the message 00 and $1/5$ for 11, while the priors were $1/2$ and $1/8$. Every scheme with $\lvert \mathcal{K} \rvert < \lvert \mathcal{M} \rvert$ fails in this way, by Shannon's theorem.
- **Non-example: AES on long messages.** AES in a mode such as counter mode encrypts messages of many blocks with a 128-bit key. For messages longer than the key, $\lvert \mathcal{K} \rvert < \lvert \mathcal{M} \rvert$, so Shannon's theorem rules out perfect secrecy. AES is believed secure against attackers with bounded computation, which is a different and weaker notion.
- **Non-example: a reused one-time pad.** Two messages under one key reveal their XOR. Perfect secrecy is a property of the encryption of one message under one key.

## Related definitions

- **Semantic security** and **IND-CPA security** are the computational versions: an efficient attacker gains at most a negligible advantage. See [semantic security](/semantic-security/) and [IND-CPA security](/ind-cpa-security/).
- **Statistical secrecy.** The two ciphertext distributions of form 3 may differ by at most $\varepsilon$ in statistical distance. This allows a slightly shorter key.
- **Unicity distance.** For schemes that are not perfectly secret, Shannon measured the amount of ciphertext after which the key is determined in principle; see the [ciphertext-only attack](/ciphertext-only-attack/).
- **Perfect secrecy for many messages.** No scheme with a fixed key and deterministic encryption can encrypt two messages with perfect secrecy, since equal messages would give equal ciphertexts.

## References
