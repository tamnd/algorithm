---
tag: WQWAEB
kind: definition
slug: semantic-security
name: Semantic security
area: cryptography/symmetric-ciphers
level: advanced
summary: A ciphertext lets an efficient adversary compute nothing about the message that it could not compute from the length alone. Under chosen-plaintext attack this equals IND-CPA.
prereqs: [chosen-plaintext-attack, computational-indistinguishability]
see_also: [symmetric-encryption, perfect-secrecy, probabilistic-encryption, goldwasser-micali-cryptosystem, ind-cpa-security, ind-cca-security, hybrid-argument, pseudorandom-function]
sources:
  - paper: doi:10.1016/0022-0000(84)90070-9
    title: Shafi Goldwasser and Silvio Micali, Probabilistic encryption, Journal of Computer and System Sciences 28(2), 1984
    locator: the definitions of semantic security and polynomial security and the proof that they are equivalent
  - paper: "Silvio Micali, Charles Rackoff and Robert H. Sloan, The notion of security for probabilistic cryptosystems, SIAM Journal on Computing 17(2), 1988"
    locator: the equivalence of several definitions of security for encryption
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 5, definitions of security for encryption schemes (semantic security, indistinguishability, their equivalence, and chosen plaintext attacks)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 3, the definition of semantic security and its relation to indistinguishability
---

Semantic security is the definition of secrecy for encryption that Goldwasser and Micali gave in 1984: whatever an efficient adversary can compute about a message from its ciphertext, it could also compute without the ciphertext, from the length of the message alone. It is a simulation definition, and it is hard to use directly. Under a [chosen-plaintext attack](/chosen-plaintext-attack/) it is equivalent to the indistinguishability game IND-CPA, which is what proofs use. It is a computational notion and differs from Shannon's [perfect secrecy](/perfect-secrecy/), which holds against unbounded adversaries but only for one message per key.

## Definition

**Notation.** $\lambda$ is the security parameter, $k$ a key, $\mathcal{A}$ an adversary that runs in time $t$ and makes $q$ encryption queries, and $\mathrm{Adv}$ an advantage. "Efficient" means probabilistic polynomial time (PPT) in $\lambda$. All results here are in the standard model.

Let $\Pi = (\mathsf{Gen}, \mathsf{Enc}, \mathsf{Dec})$ be a [symmetric encryption scheme](/symmetric-encryption/). A *message sampler* $\mathsf{Samp}(1^\lambda)$ is a PPT algorithm that outputs a message of length exactly $\ell(\lambda)$. Let $f$ and $h$ be functions on messages that are computable in polynomial time: $f(m)$ is what the adversary wants to learn, and $h(m)$ is side information it already has.

**Semantic security under CPA.** $\Pi$ is semantically secure under chosen-plaintext attack if for every PPT adversary $\mathcal{A}$ there is a PPT simulator $\mathcal{S}$ such that for every sampler $\mathsf{Samp}$ and all $f$, $h$ as above,

$$\Bigl|\Pr\bigl[\mathcal{A}^{\mathsf{Enc}_k(\cdot)}(1^\lambda, \mathsf{Enc}_k(m), h(m)) = f(m)\bigr] - \Pr\bigl[\mathcal{S}(1^\lambda, \ell, h(m)) = f(m)\bigr]\Bigr| \le \mathrm{negl}(\lambda),$$

where $k \leftarrow \mathsf{Gen}(1^\lambda)$ and $m \leftarrow \mathsf{Samp}(1^\lambda)$ in both terms. The adversary sees the ciphertext and may ask for more encryptions; the simulator sees neither, only the length and the side information. The definition allows the ciphertext to reveal the length, and nothing else that is efficiently computable.

**IND-CPA** is the game on the page [chosen-plaintext attack](/chosen-plaintext-attack/): the adversary picks $m_0, m_1$ of equal length and must guess which one was encrypted, with an encryption oracle. Its advantage is $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_\Pi(\mathcal{A}) = |\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]|$.

### IND-CPA implies semantic security

**Theorem 1.** Let $\mathcal{A}$ be an adversary in the semantic security experiment. Define the simulator $\mathcal{S}(1^\lambda, \ell, z)$: draw its own key $k' \leftarrow \mathsf{Gen}(1^\lambda)$, run $\mathcal{A}^{\mathsf{Enc}_{k'}(\cdot)}(1^\lambda, \mathsf{Enc}_{k'}(0^\ell), z)$ and output what $\mathcal{A}$ outputs. Then for each $\mathsf{Samp}$, $f$ and $h$ there is an IND-CPA adversary $\mathcal{B}$ with

$$\Bigl|\Pr[\mathcal{A} \text{ outputs } f(m)] - \Pr[\mathcal{S} \text{ outputs } f(m)]\Bigr| \le \mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_\Pi(\mathcal{B}),$$

and $\mathcal{B}$ makes the same $q$ queries as $\mathcal{A}$ and runs in the time of $\mathcal{A}$ plus one run of $\mathsf{Samp}$, $f$ and $h$. So if $\Pi$ is IND-CPA secure, it is semantically secure under CPA. The reduction is tight: it loses no factor.

*Proof.* $\mathcal{B}$ gets the oracle $\mathsf{Enc}_k(\cdot)$ of the IND-CPA game. It runs $m \leftarrow \mathsf{Samp}(1^\lambda)$ and submits the challenge pair $(m_0, m_1) = (m, 0^\ell)$. Both have length $\ell$, so the pair is legal. It gets $c^* = \mathsf{Enc}_k(m_b)$. It runs $\mathcal{A}(1^\lambda, c^*, h(m))$ and answers each query of $\mathcal{A}$ with its own oracle. When $\mathcal{A}$ outputs $y$, $\mathcal{B}$ outputs 1 if $y = f(m)$ and 0 otherwise.

Case $b = 0$. Then $c^* = \mathsf{Enc}_k(m)$, the oracle is $\mathsf{Enc}_k$, and $k$ and $m$ are drawn as in the real experiment. So $\mathcal{A}$ sees exactly the real view, and $\Pr[\mathcal{B} = 1 \mid b = 0] = \Pr[\mathcal{A} \text{ outputs } f(m)]$.

Case $b = 1$. Then $\mathcal{A}$ gets $\mathsf{Enc}_k(0^\ell)$, the oracle $\mathsf{Enc}_k$ and $h(m)$, where $k$ is a fresh key independent of $m$. This is the view that $\mathcal{S}$ gives $\mathcal{A}$, with $k$ in place of $k'$, and both keys have the distribution of $\mathsf{Gen}(1^\lambda)$. So $\Pr[\mathcal{B} = 1 \mid b = 1] = \Pr[\mathcal{S} \text{ outputs } f(m)]$.

Subtract the two cases. The difference is at most $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_\Pi(\mathcal{B})$ by definition. $\mathcal{S}$ is PPT because $\mathcal{A}$, $\mathsf{Gen}$ and $\mathsf{Enc}$ are. $\square$

The simulator does not depend on $\mathsf{Samp}$, $f$ or $h$, which is stronger than the definition asks.

### Semantic security implies IND-CPA

**Theorem 2.** Let $\mathcal{A}'$ be an IND-CPA adversary whose challenge pair $(m_0, m_1)$, with $m_0 \ne m_1$, is computed from $1^\lambda$ alone, before any query. If $\mathcal{A}'$ has advantage $\varepsilon$, then there are $\mathsf{Samp}$, $f$, $h$ and an adversary $\mathcal{A}$ such that every simulator $\mathcal{S}$ has a gap of at least $\varepsilon/2$ in the semantic security experiment. So semantic security under CPA implies IND-CPA security against such adversaries.

*Proof.* Let $\mathsf{Samp}(1^\lambda)$ compute $(m_0, m_1)$ as $\mathcal{A}'$ does, draw a uniform bit $b$ and output $m_b$. Let $h(m) = 1^\lambda$, which carries no information, and let $f(m) = 1$ if $m = m_1$ and $f(m) = 0$ otherwise. Since $m_0 \ne m_1$, $f(m_b) = b$. The adversary $\mathcal{A}$ gets $c = \mathsf{Enc}_k(m_b)$ and the oracle. It runs $\mathcal{A}'$ with challenge ciphertext $c$, answers its queries with the oracle, and outputs the guess $b'$ of $\mathcal{A}'$. The view of $\mathcal{A}'$ is the IND-CPA game with a uniform $b$, so

$$\Pr[\mathcal{A} \text{ outputs } f(m)] = \Pr[b' = b] = \tfrac{1}{2} + \tfrac{1}{2}\bigl(\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]\bigr).$$

Replace $\mathcal{A}'$ by the adversary that flips its output if needed; then the bracket is $\varepsilon$. A simulator gets $1^\lambda$, $\ell$ and $h(m) = 1^\lambda$. None of these depends on $b$, so its output is independent of $b$ and equals $b$ with probability exactly $\frac{1}{2}$. The gap is $\varepsilon/2$. $\square$

For adversaries that choose $(m_0, m_1)$ after seeing oracle answers, the equivalence needs the stronger form of semantic security in which the adversary picks the sampler during the attack. Goldreich (Volume 2, Chapter 5) proves the equivalence for that form. The two theorems explain why papers state and prove IND-CPA: it is one game with one advantage, and Theorem 1 turns each IND-CPA bound into a semantic security bound with no loss.

### Deterministic encryption is not IND-CPA

**Theorem 3.** Let $\Pi$ be stateless and let $\mathsf{Enc}$ be deterministic. If $\mathcal{M}$ contains two distinct messages of the same length, then there is an IND-CPA adversary with one encryption query and advantage 1.

*Proof.* $\mathcal{A}$ picks $m_0 \ne m_1$ with $|m_0| = |m_1|$. It asks for $c_0 = \mathsf{Enc}_k(m_0)$, then submits $(m_0, m_1)$ and gets $c^*$. It outputs $b' = 0$ if $c^* = c_0$ and $b' = 1$ otherwise. If $b = 0$, then $c^* = \mathsf{Enc}_k(m_0) = c_0$ because $\mathsf{Enc}_k$ is a deterministic function with no state, so $b' = 0$. If $b = 1$, then $c^* = \mathsf{Enc}_k(m_1)$. If $c^*$ were equal to $c_0$, correctness would give $m_1 = \mathsf{Dec}_k(c^*) = \mathsf{Dec}_k(c_0) = m_0$, because $\mathsf{Dec}_k$ is a function. This is false, so $c^* \ne c_0$ and $b' = 1$. Thus $\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0] = 1 - 0 = 1$. $\square$

So an IND-CPA scheme must use fresh randomness, as in [probabilistic encryption](/probabilistic-encryption/), or state, such as a counter that never repeats. A stateful deterministic scheme escapes Theorem 3, because the second encryption of $m_0$ uses a new state. Without an oracle and with one message per key, determinism is fine: the [one-time pad](/one-time-pad/) is deterministic and perfectly secret.

## Examples and non-examples

- **Randomized counter encryption.** $\mathsf{Enc}_k(m) = (r, F_k(r) \oplus m)$ with a [pseudorandom function](/pseudorandom-function/) $F$ and a uniform $n$-bit $r$ is IND-CPA secure, with advantage at most $2\,\mathrm{Adv}^{\mathrm{prf}}_F + 2q/2^n$ (proof on the page [symmetric encryption](/symmetric-encryption/)). By Theorem 1 it is semantically secure under CPA, with the same bound.
- **A block cipher in ECB mode.** Deterministic and stateless, so not IND-CPA by Theorem 3, and so not semantically secure under CPA.
- **A scheme that leaks one bit.** Let $\mathsf{Enc}'_k(m) = (m_1, \mathsf{Enc}_k(m))$, where $m_1$ is the first bit of $m$. Take a uniform $\ell$-bit $m$, $f(m) = m_1$ and $h(m) = 1^\lambda$. The adversary outputs $f(m)$ with probability 1, and each simulator with probability exactly $\frac{1}{2}$. So $\mathsf{Enc}'$ is not semantically secure, even if $\mathsf{Enc}$ is.
- **Length is allowed to leak.** Encryption of messages of different lengths may give ciphertexts of different lengths. The simulator gets $\ell$, so this is not a break. Real systems that must hide the length pad the messages first.
- **The one-time pad under CPA.** With $\mathsf{Enc}_k(m) = k \oplus m$, the answer $c_0$ to the query $m_0$ gives $k = c_0 \oplus m_0$. The one-time pad is perfectly secret for one message but not semantically secure under CPA.

## Related definitions

- **[Perfect secrecy](/perfect-secrecy/).** Shannon's notion: $\Pr[M = m \mid C = c] = \Pr[M = m]$ for every distribution of $M$. It holds against unbounded adversaries but for one message, and it needs a key at least as long as the message ([Shannon's theorem](/shannon-perfect-secrecy-theorem/)). Semantic security relaxes it to efficient adversaries, which allows short keys and many messages.
- **[Computational indistinguishability](/computational-indistinguishability/).** IND-CPA says that the two families of views, for $b = 0$ and $b = 1$, are computationally indistinguishable.
- **[IND-CPA for public-key encryption](/ind-cpa-security/).** The same game with the public key given to the adversary, which makes the encryption oracle redundant. Goldwasser and Micali stated semantic security for this setting and gave the [Goldwasser-Micali cryptosystem](/goldwasser-micali-cryptosystem/) as the first example.
- **[IND-CCA security](/ind-cca-security/).** The adversary also gets a decryption oracle. It is strictly stronger than IND-CPA.
- **Real-or-random security.** The challenge is either $\mathsf{Enc}_k(m)$ or $\mathsf{Enc}_k$ of a random string of the same length. It is equivalent to IND-CPA up to a factor 2 (Bellare, Desai, Jokipii and Rogaway, 1997).

## References
