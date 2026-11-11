---
tag: ACW4G6
kind: concept
slug: key-schedule
name: Key schedule
aliases:
- key expansion
area: cryptography/symmetric-ciphers
level: core
summary: The map from the cipher key to the round keys, such as the AES key expansion or the DES schedule with PC-1, shifts and PC-2. A weak schedule allows slide and related-key attacks.
prereqs: [block-cipher]
see_also: [advanced-encryption-standard, data-encryption-standard, related-key-attack, slide-attack, key-whitening, feistel-network, blowfish, substitution-permutation-network]
sources:
  - paper: doi:10.6028/NIST.FIPS.197-upd1
    title: NIST, FIPS 197, Advanced Encryption Standard (AES), November 2001, updated May 2023
    locator: Section 5.2 (KeyExpansion, RotWord, SubWord and Rcon) and Appendix A (key expansion examples)
  - url: "https://csrc.nist.gov/pubs/fips/46-3/final"
    title: NIST, FIPS 46-3, Data Encryption Standard (DES), October 1999, withdrawn 2005
    locator: the key schedule calculation (permuted choice 1, the table of left shifts and permuted choice 2)
  - paper: "Alex Biryukov and David Wagner, Slide attacks, Fast Software Encryption, FSE 1999, LNCS 1636, Springer, 1999"
    locator: the slide attack on ciphers whose rounds are all equal
  - paper: "Alex Biryukov and Dmitry Khovratovich, Related-key cryptanalysis of the full AES-192 and AES-256, Advances in Cryptology, ASIACRYPT 2009, LNCS 5912, Springer, 2009"
    locator: the related-key attacks on AES-256 with time and data 2^99.5 and on AES-192 with time 2^176
  - paper: "Eli Biham, New types of cryptanalytic attacks using related keys, Journal of Cryptology 7(4), 1994"
    locator: related-key attacks on ciphers with a simple key schedule
---

A key schedule is the part of a [block cipher](/block-cipher/) that derives the round keys $k_1, \ldots, k_r$ from the cipher key $K$. In [AES](/advanced-encryption-standard/) it is the key expansion of FIPS 197 Section 5.2, which grows the key word by word with a nonlinear step every few words. In [DES](/data-encryption-standard/) it selects 48 of the 56 key bits for each round, after rotations of two 28-bit registers. A schedule that is too regular gives the attacker structure: equal round keys allow [slide attacks](/slide-attack/), and simple relations between the schedules of related keys allow [related-key attacks](/related-key-attack/).

## In plain words

A cipher runs many rounds, and each round needs its own piece of key. The key schedule is the recipe that cuts and stirs the one secret key into these pieces.

The recipe must not be too lazy. If every round gets the same piece, all rounds look alike, and an attacker can line up two runs of the cipher that are one round apart. Then the number of rounds no longer matters. If a small change of the key gives a predictable change of every piece, an attacker who can use two keys with a known difference can learn a lot.

The recipe must also be cheap, because a program may change keys often. Good recipes use a few table lookups and constants that differ from round to round.

## The idea

**Notation.** $K$ is the cipher key of $k$ bits, $r$ the number of rounds, and $\mathrm{KS}(K) = (k_0, \ldots, k_r)$ the round keys. In AES, $N_k \in \{4, 6, 8\}$ is the key length in 32-bit words and $N_r = N_k + 6$ the number of rounds.

**What a schedule must do.**

- Each key bit must affect many rounds, so that no round key can be guessed from a small part of the key.
- The round keys must differ, and rounds must not be all the same function, so that the cipher is not a power of one round.
- The map $K \mapsto \mathrm{KS}(K)$ must have no simple relation of the form $\mathrm{KS}(\phi(K)) = \psi(\mathrm{KS}(K))$ that the round function respects.
- It must be fast, and ideally computable on the fly in both directions.

**The AES key expansion.** The schedule produces $4(N_r + 1)$ words $w[0], w[1], \ldots$ of 4 bytes. The first $N_k$ words are the key. For $i \ge N_k$,

$$w[i] = w[i - N_k] \oplus \begin{cases} \mathrm{SubWord}(\mathrm{RotWord}(w[i-1])) \oplus \mathrm{Rcon}[i / N_k] & \text{if } N_k \mid i, \\ \mathrm{SubWord}(w[i-1]) & \text{if } N_k = 8 \text{ and } i \bmod 8 = 4, \\ w[i-1] & \text{otherwise.} \end{cases}$$

RotWord rotates the 4 bytes of a word by one byte, SubWord applies the AES S-box to each byte, and $\mathrm{Rcon}[j]$ is the word $(x^{j-1}, 0, 0, 0)$ in GF($2^8$): 01, 02, 04, 08, 10, 20, 40, 80, 1B, 36. Round key $t$ is $w[4t], \ldots, w[4t + 3]$. So AES-128, AES-192 and AES-256 use 44, 52 and 60 words.

**The AES-128 schedule can be run backward.** The rule gives $w[i - 4] = w[i] \oplus T_i(w[i-1])$, where $T_i$ is the map of the case that applies, and $T_i$ uses only $w[i-1]$. So from the four words of any round key, all earlier words follow, down to the cipher key. A consequence: an attacker who learns one full round key of AES-128, for example the last one in a side-channel attack, learns the cipher key.

**The DES schedule.** The 64-bit key has 8 parity bits. Permuted choice 1 (PC-1) drops them and splits the other 56 bits into two 28-bit registers $C_0$ and $D_0$. For round $i = 1, \ldots, 16$, both registers rotate left by $s_i$ places, with

$$(s_1, \ldots, s_{16}) = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1),$$

and permuted choice 2 (PC-2) selects 48 of the 56 bits of $C_i D_i$ as the round key $k_i$. The shifts sum to 28, so $C_{16} = C_0$ and $D_{16} = D_0$. Decryption can then produce the round keys in reverse order by rotating right, with no table of keys. Each key bit enters between 12 and 15 of the 16 round keys, and $16 \cdot 48 / 56 \approx 13.7$ on average.

**Why weak schedules allow attacks.**

- *Identical rounds.* If every round uses the same key and the same function $F_k$, then $E_K = F_k^r$. A pair with $x' = F_k(x)$, a slid pair, gives $E_K(x') = F_k(E_K(x))$, which yields equations in $k$ for one round only. With about $2^{n/2}$ known plaintexts, a slid pair exists by the [birthday bound](/birthday-paradox/), and the attack costs the same for any $r$ (Biryukov and Wagner 1999). Round constants, such as Rcon in AES, break this self-similarity.
- *Linear structure.* PC-1, the rotations and PC-2 only move bits, so $\mathrm{KS}(\bar K) = \overline{\mathrm{KS}(K)}$ for DES. With the round function, this gives the complementation property $E_{\bar K}(\bar x) = \overline{E_K(x)}$.
- *Palindromic schedules.* A DES key whose round keys satisfy $k_i = k_{17-i}$ makes encryption equal to decryption. See below.
- *Slow nonlinearity.* A related-key attack chooses a key difference whose effect on the schedule cancels with the effect on the state. The AES-256 schedule applies SubWord to only two words in each group of eight, and Biryukov and Khovratovich (2009) used this for a related-key key recovery on full AES-256 with time and data $2^{99.5}$, using four related keys. The attack does not apply when keys are random and independent, as in normal use.

## Examples

**AES-128, FIPS 197 Appendix A.1.** For the key 2b7e1516 28aed2a6 abf71588 09cf4f3c, the first expanded words are $w[4], \ldots, w[7]$ = a0fafe17 88542cb1 23a33939 2a6c7605, and the last round key is $w[40], \ldots, w[43]$ = d014f9a8 c9ee2589 e13f0cc8 b6630ca6. Running the schedule backward from these four words returns 2b7e1516 28aed2a6 abf71588 09cf4f3c.

**AES-128, FIPS 197 Appendix C.1.** For the key 00010203 04050607 08090a0b 0c0d0e0f, round key 1 is d6aa74fd d2af72fa daa678f1 d6ab76fe.

**The zero key.** For the AES-128 key of all zeros, round key 1 is 62636363 62636363 62636363 62636363 and round key 10 is b4ef5bcb 3e92e211 23e951cf 6f8f188e. The S-box gives $S(0) = \mathtt{63}$, and Rcon makes the first byte differ. Structure in the key shows in the first round keys and fades in later ones.

**DES.** For the key 0131D9619DC1376E of NIST SP 800-17, the round keys start with $k_1$ = 46126F180F46 and $k_2$ = 38A7B1441164, and end with $k_{16}$ = E3698217500A.

**DES weak keys.** For the four keys 0101010101010101, FEFEFEFEFEFEFEFE, E0E0E0E0F1F1F1F1 and 1F1F1F1F0E0E0E0E, the registers $C_0$ and $D_0$ are each all zeros or all ones, so every rotation leaves them unchanged, and all 16 round keys are equal (for example all zeros for 0101010101010101). By the decryption theorem of the [Feistel network](/feistel-network/), $E_K$ is then an involution: $E_K(E_K(x)) = x$.

**DES semi-weak keys.** For the pair 01FE01FE01FE01FE and FE01FE01FE01FE01, the round keys of one key are those of the other in reverse order, and each schedule has only 2 distinct round keys. So encryption under one key is decryption under the other: encrypting 0123456789ABCDEF under the second key and then under the first returns 0123456789ABCDEF. DES has 6 such pairs.

## Where it is used

- **Every iterated block cipher.** The schedule is part of the definition of AES, DES, [Blowfish](/blowfish/) and the others. Blowfish uses a slow schedule, which runs the cipher 521 times, on purpose.
- **Implementation choices.** Software usually expands the key once and stores the round keys. Small hardware computes them on the fly, which is easy when the schedule runs in both directions, as in AES-128 and DES.
- **Key whitening and key-alternating designs.** In the [Even-Mansour cipher](/key-whitening/) and its iterated forms, the schedule is the only place where the key enters, and the security proofs model it.
- **Cryptanalysis.** Slide, related-key and side-channel attacks all exploit the schedule. Side-channel attacks on AES-128 usually target the first or the last round key, because either one gives the cipher key.

## References
