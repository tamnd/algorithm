---
tag: NQ29ZT
kind: technique
slug: feistel-network
name: Feistel network
aliases:
- Feistel cipher
- Feistel structure
area: cryptography/symmetric-ciphers
level: core
summary: Split the block into two halves and in each round XOR a keyed function of one half into the other. The inverse is the same network with the keys reversed, so F need not be invertible.
prereqs: [block-cipher]
see_also: [data-encryption-standard, luby-rackoff-theorem, substitution-permutation-network, blowfish, twofish, camellia, tea, slide-attack]
sources:
  - paper: "Horst Feistel, Cryptography and computer privacy, Scientific American 228(5), May 1973"
    locator: the description of a product cipher that alternates substitution and transposition on the two halves of a block, the basis of IBM's Lucifer
  - paper: doi:10.1137/0217022
    title: Michael Luby and Charles Rackoff, How to construct pseudorandom permutations from pseudorandom functions, SIAM Journal on Computing 17(2), 1988
    locator: the Feistel network with pseudorandom round functions; 3 rounds give a pseudorandom permutation and 4 rounds a strong one
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 7, Section 7.4 (product ciphers, Feistel ciphers and DES)
  - url: "https://csrc.nist.gov/pubs/fips/46-3/final"
    title: NIST, FIPS 46-3, Data Encryption Standard (DES), October 1999, withdrawn 2005
    locator: the enciphering computation (16 rounds of L and R) and the deciphering with the keys in reverse order
---

A Feistel network is a way to build a [block cipher](/block-cipher/) from any keyed function $F$ on half blocks: split the block into halves $(L, R)$ and in each round replace them by $(R, L \oplus F_{k_i}(R))$. Each round is a permutation even when $F$ is not, and the inverse of the whole network is the same network with the round keys in reverse order. Horst Feistel described the design at IBM in 1973; it is the structure of Lucifer and of [DES](/data-encryption-standard/). With random round functions, 3 rounds give a pseudorandom permutation and 4 rounds a strong one, by the [Luby-Rackoff theorem](/luby-rackoff-theorem/).

## In plain words

Cut the block into a left half and a right half. In one round, feed the right half and a round key into a mixing function, and add the result to the left half with exclusive or. Then swap the two halves. Repeat for many rounds, each with its own key.

The mixing function can be anything, even a function that loses information. The round is still easy to undo: the right half is still there in the output, so you can feed it into the mixing function again and remove the same value from the left half.

This gives a second gift. Undoing the whole cipher is the same procedure as running it, with the round keys in the opposite order. So one circuit or one program does both jobs.

## When it applies

Use a Feistel network when you have a good keyed function on half blocks that is not a permutation, or that is cheap only in one direction, and you need a permutation on full blocks. It fits hardware well, because encryption and decryption share one data path. It also fits when the block is not a power of two in size, as in format-preserving encryption, because the halves can have any size.

The notation on this page: the block has $2h$ bits, the round function is $F : \{0,1\}^m \times \{0,1\}^h \to \{0,1\}^h$ with round keys $k_1, \ldots, k_r$, and $\Phi_k(L, R) = (R, L \oplus F_k(R))$ is one round. $\sigma(L, R) = (R, L)$ is the swap.

## The template

FEISTEL computes $E(x) = \sigma \circ \Phi_{k_r} \circ \cdots \circ \Phi_{k_1}(x)$. The last swap undoes the swap of the last round, as in DES.

```pseudo id=main
FEISTEL(F, k1, ..., kr, x)               ▷ x has 2h bits
L1  (L0, R0) ← the left and right h bits of x
L2  for i ← 1 to r do
L3      Li ← R(i−1)
L4      Ri ← L(i−1) ⊕ F(ki, R(i−1))
L5  return Rr ‖ Lr                         ▷ the halves swapped once more
```

The cost is $r$ calls of $F$ and $r$ XORs of $h$ bits. The Python code for this page is for study only, is not constant time, and must not be used to protect real data. For real data, use AES from a FIPS 140 validated module or from libsodium.

**Lemma (each round is a permutation).** For each $F$ and $k$, $\Phi_k$ is a bijection of $\{0,1\}^{2h}$, with inverse $\Phi_k^{-1}(L', R') = (R' \oplus F_k(L'), L')$, and $\Phi_k^{-1} = \sigma \circ \Phi_k \circ \sigma$.

*Proof.* Let $(L', R') = \Phi_k(L, R) = (R, L \oplus F_k(R))$. Then $R = L'$, and $L = R' \oplus F_k(R) = R' \oplus F_k(L')$, because $a \oplus b \oplus b = a$. So $(L, R)$ is determined by $(L', R')$ through the stated formula, and that formula maps each $(L', R')$ to a preimage. Thus $\Phi_k$ is a bijection with that inverse. No property of $F$ is used. For the second claim, $\sigma(L', R') = (R', L')$, then $\Phi_k(R', L') = (L', R' \oplus F_k(L'))$, then $\sigma$ gives $(R' \oplus F_k(L'), L')$, which is $\Phi_k^{-1}(L', R')$. $\square$

**Theorem (decryption reverses the keys).** Let $E = \sigma \circ \Phi_{k_r} \circ \cdots \circ \Phi_{k_1}$. Then $E^{-1} = \sigma \circ \Phi_{k_1} \circ \cdots \circ \Phi_{k_r}$, which is FEISTEL with the keys $k_r, \ldots, k_1$.

*Proof.* The inverse of a composition is the composition of the inverses in the reverse order, and $\sigma^{-1} = \sigma$. So

$$E^{-1} = \Phi_{k_1}^{-1} \circ \Phi_{k_2}^{-1} \circ \cdots \circ \Phi_{k_r}^{-1} \circ \sigma = (\sigma \Phi_{k_1} \sigma)(\sigma \Phi_{k_2} \sigma) \cdots (\sigma \Phi_{k_r} \sigma)\,\sigma$$

by the lemma. Each inner pair $\sigma \sigma$ is the identity, and so is the last pair. What is left is $\sigma \circ \Phi_{k_1} \circ \cdots \circ \Phi_{k_r}$. This map applies $\Phi_{k_r}$ first and $\Phi_{k_1}$ last, then swaps, which is FEISTEL with the keys in the order $k_r, \ldots, k_1$. $\blacksquare$

## Classic examples

**A worked trace.** Take $h = 16$, the toy round function $F_k(r) = (r \wedge k) \oplus \lfloor r^2 / 8 \rfloor \oplus \lfloor k/2 \rfloor \bmod 2^{16}$, the keys 0x0F0F, 0x3C3C, 0xA5A5, 0x5A5A and $x$ = 0x01234567. For $k$ = 0x0F0F, $F_k$ takes only 36471 of the 65536 possible values, so it is far from a permutation.

| round | key | $F(k_i, R_{i-1})$ | $L_i$ | $R_i$ |
|---|---|---|---|---|
| 0 | | | 0x0123 | 0x4567 |
| 1 | 0x0F0F | 0x176E | 0x4567 | 0x164D |
| 2 | 0x3C3C | 0x2077 | 0x164D | 0x6510 |
| 3 | 0xA5A5 | 0xC3F2 | 0x6510 | 0xD5BF |
| 4 | 0x5A5A | 0x91A7 | 0xD5BF | 0xF4B7 |

Line L5 returns $R_4 \| L_4$ = 0xF4B7D5BF. Decryption runs FEISTEL on 0xF4B7D5BF with the keys in reverse order: 0x5A5A, 0xA5A5, 0x3C3C, 0x0F0F. Its first round computes $F$(0x5A5A, 0xD5BF) = 0x91A7, the same value as round 4, and 0xF4B7 $\oplus$ 0x91A7 = 0x6510, which is $R_3$. The rows of the table are walked back in this way to 0x01234567.

- **DES.** 16 rounds on $h = 32$, with $F$ made of an expansion to 48 bits, a XOR with the 48-bit round key, eight S-boxes from 6 to 4 bits and a bit permutation. See [DES](/data-encryption-standard/).
- **Lucifer.** IBM's cipher of the early 1970s, the direct ancestor of DES.
- **Blowfish, Twofish and Camellia.** Feistel ciphers with 16 or 18 rounds and key-dependent or fixed S-boxes. See [Blowfish](/blowfish/), [Twofish](/twofish/) and [Camellia](/camellia/).
- **TEA and XTEA.** Feistel ciphers whose round function uses only addition, shifts and XOR. See [TEA](/tea/) and [XTEA](/xtea/).
- **The Luby-Rackoff construction.** The Feistel network with independent pseudorandom round functions, the object of the [Luby-Rackoff theorem](/luby-rackoff-theorem/).

## Variations

- **Unbalanced Feistel networks.** The halves have different sizes, so $F$ maps $a$ bits to $b$ bits with $a + b$ the block length.
- **Generalized Feistel networks.** The block is cut into more than two parts, and a round updates some of them from others. CLEFIA and the type-1, type-2 and type-3 schemes are examples.
- **Lai-Massey scheme.** A different structure that also allows a non-invertible round function; [IDEA](/idea/) uses it.
- **Format-preserving encryption.** NIST SP 800-38G (FF1, FF3-1) runs a Feistel network on numbers in a given radix, with AES inside $F$.
- **Without the final swap.** Some texts omit the swap of line L5. Then the inverse is $\sigma \circ (\text{the network with reversed keys}) \circ \sigma$, so the halves must be swapped before and after decryption.

## Pitfalls

- **Too few rounds.** One round leaves $R_0$ in the clear as the right half of the output. Two rounds keep $L_2 \oplus L'_2 = L_0 \oplus L'_0$ for inputs with the same $R_0$. Three rounds are a PRP but not a strong PRP. See the [Luby-Rackoff theorem](/luby-rackoff-theorem/) for the attacks.
- **Palindromic round keys.** If $k_i = k_{r+1-i}$ for each $i$, then by the theorem $E^{-1}$ is $E$ itself, so $E(E(x)) = x$ for each $x$. The four weak keys of DES produce 16 equal round keys and give exactly this.
- **Identical rounds.** If all rounds use the same key, the cipher is a power of one round function, and a [slide attack](/slide-attack/) costs about $2^{n/2}$ known plaintexts for any number of rounds.
- **Linear structure in F.** The proof of the theorem needs nothing from $F$, but security needs a lot. A round function that commutes with complement, as in DES, gives the complementation property $E_{\bar K}(\bar x) = \overline{E_K(x)}$.
- **Slow diffusion.** A round changes only one half, so a Feistel cipher needs about twice as many rounds as an SPN for full diffusion. DES reaches its full avalanche of about 32 changed bits only after about 5 rounds.

## Exercises

1. Run the decryption of the worked trace to the end and confirm that it returns 0x01234567.
2. Show that one Feistel round is an even permutation of $\{0,1\}^{2h}$ when $h \ge 2$. Hint: for a fixed $R$, the map $L \mapsto L \oplus F_k(R)$ is the identity or a product of $2^{h-1}$ disjoint transpositions.
3. Show that 2 rounds with independent random functions are not a PRP: with two queries $(L, R)$ and $(L', R)$, $L \ne L'$, the left halves of the outputs before the final swap satisfy $L_2 \oplus L'_2 = L \oplus L'$. Compute the advantage.
4. Let $E$ be FEISTEL with the round keys $k_1, \ldots, k_r$ and with no final swap. Write $E^{-1}$ in terms of $\sigma$ and the network with the keys reversed.
5. Show that a Feistel round with $F_k(R) = R \oplus k$ makes the whole $r$-round network affine over GF(2) in $x$, with a linear part that does not depend on the keys, so two queries suffice to tell it apart from a random permutation.

## References
