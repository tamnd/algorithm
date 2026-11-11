---
tag: 5YKDCX
kind: definition
slug: ciphertext-only-attack
name: Ciphertext-only attack
aliases:
- COA
area: cryptography/symmetric-ciphers
level: intro
summary: The weakest attack model. The attacker sees only ciphertexts. Shannon's unicity distance H(K)/D estimates how much ciphertext fixes the key, about 28 letters for simple substitution.
prereqs: [symmetric-encryption, kerckhoffs-principle]
see_also: [known-plaintext-attack, chosen-plaintext-attack, cryptanalysis, frequency-analysis, shannon-entropy, entropy-rate, perfect-secrecy, cipher-breaking]
sources:
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949, pp. 656-715
    locator: Part II, the sections on equivocation and the random cipher (the unicity distance H(K)/D and its value for simple substitution)
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 3.5 (spurious keys and unicity distance, with the substitution cipher as the example)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 1, Section 1.13 (classes of attacks on encryption schemes) and Chapter 7 (the redundancy of English and the unicity distance of classical ciphers)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 1.2 (the attack scenarios, from ciphertext-only to chosen-ciphertext attacks)
---

In a ciphertext-only attack, the attacker sees only encrypted messages. It knows the cipher, by [Kerckhoffs's principle](/kerckhoffs-principle/), and something about the kind of plaintext, for example that it is English text, but it has no plaintext and cannot make the system encrypt or decrypt anything. This is the weakest of the standard attack models, and every classical cipher falls to it. Shannon measured how much ciphertext an attacker with unlimited computing power needs in principle: the unicity distance $U = H(K)/D$, the key entropy divided by the redundancy of the language per letter. For simple substitution on English, $U$ is about 28 letters.

## Definition

Let $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ be an encryption scheme. In a **ciphertext-only attack**, a key $K$ is chosen by $\mathrm{Gen}$, messages $m_1, \ldots, m_q$ are drawn from a distribution $\mathcal{D}$ that the attacker knows but does not control, and the attacker receives $c_i = \mathrm{Enc}_K(m_i)$ for $i = 1, \ldots, q$. The attacker knows $\Pi$ and $\mathcal{D}$. It succeeds if it reaches its goal: the key ([key recovery](/key-recovery/)), one of the messages, or some information about them. The scheme resists the attack if every attacker within the given resources succeeds with at most a small probability.

**Unicity distance.** Let the plaintext be text over an alphabet $\Sigma$, with absolute rate $R = \log_2 \lvert \Sigma \rvert$ bits per letter and true rate $r$, the [entropy rate](/entropy-rate/) of the language in bits per letter. The **redundancy** is $D = R - r$. For a key $K$ with [entropy](/shannon-entropy/) $H(K)$, the unicity distance is
$$U = \frac{H(K)}{D}.$$

*Derivation.* Make these assumptions:

1. The key is uniform on $\mathcal{K}$, so $H(K) = \log_2 \lvert \mathcal{K} \rvert$.
2. Meaningful plaintexts of $n$ letters number about $2^{rn}$ out of the $2^{Rn}$ strings, and they are about equally likely (true for large $n$ by the definition of the entropy rate).
3. *The random cipher model.* For a ciphertext of $n$ letters, the decryption under each wrong key behaves like a uniformly random string of $n$ letters, independently for different keys.

Take a ciphertext of $n$ letters from the true key. Under a wrong key, the decryption is meaningful with probability about $2^{rn} / 2^{Rn} = 2^{-Dn}$. A wrong key with a meaningful decryption is a *spurious key*, since the attacker cannot rule it out. The expected number of spurious keys is
$$s_n \approx (\lvert \mathcal{K} \rvert - 1) \, 2^{-Dn} \approx 2^{H(K) - Dn}.$$
This drops below 1 when $n > H(K)/D$. So $U = H(K)/D$ is the length at which one key, the true key, is expected to remain. Stinson gives a version of this bound from the conditional entropy $H(K \mid C^n)$ with fewer assumptions; it gives the same value of $U$.

The unicity distance is a statement about information, not about work. Below $U$ letters, even an unlimited attacker cannot in general decide the key. Above $U$, the key is determined in principle, but finding it may still take an infeasible search.

## Examples and non-examples

- **Simple substitution.** The key is one of $26!$ permutations, so $H(K) = \log_2 26! \approx 88.4$ bits. With $R = \log_2 26 \approx 4.70$ and a rate of English of about $r = 1.5$ bits per letter, $D \approx 3.2$ and $U \approx 88.4 / 3.2 \approx 27.6$, about 28 letters. With $r = 1.0$, $D \approx 3.7$ and $U \approx 23.9$. In practice, [frequency analysis](/frequency-analysis/) with hill climbing needs a few hundred letters, more than $U$, because it cannot search all keys.
- **The shift cipher.** $H(K) = \log_2 26 \approx 4.70$ bits, so $U \approx 4.70 / 3.2 \approx 1.5$: two letters fix the key in principle. A brute force over 26 keys is an easy ciphertext-only attack.
- **The Vigenère cipher.** With a key of $m$ letters, $U \approx 1.47\, m$ letters. The [Kasiski examination](/kasiski-examination/) and the [index of coincidence](/index-of-coincidence/) find $m$ from ciphertext only, and frequency analysis then finds each shift.
- **Enigma indicators.** Rejewski's characteristic method used only the enciphered message keys at the start of the messages of one day: a ciphertext-only attack on the [Enigma machine](/enigma-machine/).
- **The two-time pad.** Two ciphertexts under one [one-time pad](/one-time-pad/) key give the XOR of the messages, and crib dragging recovers them from ciphertexts only.
- **Modern ciphers.** For a 128-bit key and ASCII English with $R = 8$ and $r \approx 1.5$, $U \approx 128 / 6.5 \approx 20$ characters. The key of AES is thus determined by a short text in principle, but no attack faster than about $2^{128}$ work is known, so the unicity distance tells nothing about practical security.
- **Non-example: the one-time pad.** With a new uniform key for each message, the key entropy grows with the message, $H(K) = Rn \ge Dn$, and no length of ciphertext is enough. This is [perfect secrecy](/perfect-secrecy/).
- **Non-example: compressed plaintext.** If the plaintext were perfectly compressed, $D = 0$ and $U$ would be infinite. Real compression lowers $D$ but does not remove the structure of headers and formats.

**Why modern ciphers must resist stronger models.** Resistance to ciphertext-only attacks is necessary but far from sufficient. In practice the attacker often knows parts of the plaintext, such as protocol headers, file formats and fixed greetings, which is a [known-plaintext attack](/known-plaintext-attack/). It can often make the system encrypt data of its choice, for example by sending a message that a server stores or a browser encrypts, which is a [chosen-plaintext attack](/chosen-plaintext-attack/). And error messages can leak information about decryptions, which gives a [chosen-ciphertext attack](/chosen-ciphertext-attack/). So modern schemes are designed and proved secure against chosen-plaintext and chosen-ciphertext attacks, and they treat the ciphertext-only case as the easy one.

## Related definitions

- **Known-plaintext attack.** The attacker also has plaintexts of some ciphertexts. See [known-plaintext attack](/known-plaintext-attack/).
- **Eavesdropping security.** The modern definition of security against a passive attacker, as in Katz and Lindell, lets the attacker choose two messages and see the encryption of one of them. It is stronger than resistance to ciphertext-only attacks on a fixed message distribution.
- **Perfect secrecy.** A scheme with [perfect secrecy](/perfect-secrecy/) resists every ciphertext-only attack on one message, even an unlimited one.
- **Cryptanalysis.** The [field](/cryptanalysis/) and its attack models, and the general method of [cipher breaking](/cipher-breaking/).

## References
