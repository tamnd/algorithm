---
tag: 9JD6DB
kind: definition
slug: known-plaintext-attack
name: Known-plaintext attack
aliases:
- KPA
area: cryptography/symmetric-ciphers
level: intro
summary: The attacker knows some plaintexts and their ciphertexts under the key, but did not choose them. It breaks the Hill and affine ciphers at once, gave the Enigma cribs, and drives linear cryptanalysis.
prereqs: [ciphertext-only-attack]
see_also: [ciphertext-only-attack, chosen-plaintext-attack, linear-cryptanalysis, hill-cipher, affine-cipher, enigma-machine, cryptanalysis, key-recovery]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 1, Section 1.13 (classes of attacks on encryption schemes, the known-plaintext attack)
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.2 (the attack models, and the known-plaintext attacks on the affine and Hill ciphers)
  - paper: "Mitsuru Matsui, Linear cryptanalysis method for DES cipher, Advances in Cryptology, EUROCRYPT '93, Lecture Notes in Computer Science 765, Springer, 1994, pp. 386-397"
    locator: the known-plaintext attack on DES by linear approximations
  - paper: "Gordon Welchman, The Hut Six Story, Breaking the Enigma Codes, McGraw-Hill, 1982"
    locator: the account of cribs and of their use on the bombe
---

In a known-plaintext attack, the attacker has some pairs of plaintext and ciphertext under the unknown key, and it wants the key or the plaintext of other ciphertexts. The plaintexts are given by circumstance, not chosen by the attacker: a standard greeting, a weather report, a file header, a message that was later made public. The model is stronger than the [ciphertext-only attack](/ciphertext-only-attack/) and weaker than the [chosen-plaintext attack](/chosen-plaintext-attack/). Linear ciphers such as the [affine](/affine-cipher/) and [Hill ciphers](/hill-cipher/) fall to a few known letters by solving equations. Guessed plaintext, the *crib*, was the basis of the bombe attack on the [Enigma machine](/enigma-machine/). And Matsui's [linear cryptanalysis](/linear-cryptanalysis/) of DES is the classic modern known-plaintext attack.

## Definition

Let $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ be an encryption scheme and let $K$ be a key chosen by $\mathrm{Gen}$. In a **known-plaintext attack**, the attacker receives pairs $(m_1, c_1), \ldots, (m_q, c_q)$ with $c_i = \mathrm{Enc}_K(m_i)$, where the messages $m_i$ are drawn from a distribution, or fixed in advance, independently of the attacker. It may also receive further ciphertexts whose plaintexts it does not know. It knows $\Pi$, by [Kerckhoffs's principle](/kerckhoffs-principle/). Its goal is to find the key ([key recovery](/key-recovery/)), or to decrypt a ciphertext whose plaintext is not among the $m_i$, or to learn some information about such a plaintext.

**How it differs from a chosen-plaintext attack.** In a [chosen-plaintext attack](/chosen-plaintext-attack/), the attacker picks the messages $m_i$, possibly one at a time after seeing earlier answers. So every known-plaintext attack also works with chosen plaintexts, but not the other way round. Some attacks need the choice: differential cryptanalysis needs pairs of plaintexts with a fixed difference, which random known plaintexts give only rarely. Modern definitions such as [IND-CPA security](/ind-cpa-security/) use the chosen-plaintext model, which covers all known-plaintext attacks.

## Examples and non-examples

- **The affine cipher.** Two known letter pairs give two equations $y_i = a x_i + b \pmod{26}$. With the key $(5, 8)$, A encrypts to I and F to H. Subtracting gives $a \cdot (0 - 5) \equiv 8 - 7$, that is $21 a \equiv 1$, so $a = 21^{-1} = 5$, and then $b = 8$. Two letters fix the key whenever their difference is coprime to 26, and in more cases with a short search.
- **The Hill cipher.** The cipher is linear, $c = K p$. Knowing that HELP becomes LGKL gives two plaintext columns $(7, 4)$ and $(11, 15)$ and two cipher columns $(11, 6)$ and $(10, 11)$. The plaintext matrix has determinant $61 \equiv 9$, which is invertible modulo 26, so $K = C P^{-1} \bmod 26$, which is the key with rows $(11, 3)$ and $(8, 7)$. When the plaintext matrix is not invertible, more known blocks are needed.
- **The Vigenère cipher and the one-time pad.** The key letter at each position is the cipher letter minus the plaintext letter. For the [Vigenère cipher](/vigenere-cipher/), one period of known text gives the whole key. For the [one-time pad](/one-time-pad/), known text gives the key of that message only, which is harmless as long as the key is never used again.
- **Enigma cribs.** Code breakers at Bletchley Park guessed words that were likely in a message, such as WETTERBERICHT (weather report) in daily weather messages. Since Enigma never encrypts a letter to itself, a crib cannot sit under a cipher letter equal to its own letter, which rules out many positions. A placed crib gives a chain of letter pairs at known rotor positions, and the bombe searched for the rotor settings consistent with it.
- **Linear cryptanalysis.** Matsui found linear relations between some plaintext, ciphertext and key bits of DES that hold with probability slightly different from 1/2. Counting how often they hold over many known pairs reveals key bits. His attack of 1994 recovered a DES key from $2^{43}$ known plaintexts. See [linear cryptanalysis](/linear-cryptanalysis/).
- **Non-example: frequency analysis.** [Frequency analysis](/frequency-analysis/) uses only statistics of the language, not known pairs; it is a ciphertext-only attack.
- **Non-example: differential cryptanalysis.** Its basic form chooses plaintext pairs with a fixed difference, so it is a chosen-plaintext attack. With random known pairs it needs far more data.

## Related definitions

- **Ciphertext-only attack.** No plaintext is known. See [ciphertext-only attack](/ciphertext-only-attack/).
- **Chosen-plaintext attack.** The attacker chooses the plaintexts. See [chosen-plaintext attack](/chosen-plaintext-attack/).
- **Probable plaintext.** A weaker form in which the attacker only guesses words that are likely, as with cribs, and must test each guess.
- **Cryptanalysis.** The [field](/cryptanalysis/) and its full list of attack models and goals.

## References
