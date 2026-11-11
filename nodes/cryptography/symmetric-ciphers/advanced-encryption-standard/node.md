---
tag: 4E36FN
kind: algorithm
slug: advanced-encryption-standard
name: Advanced Encryption Standard
aliases:
- AES
- Rijndael
area: cryptography/symmetric-ciphers
level: core
summary: The NIST block cipher of FIPS 197 (2001), a 128-bit substitution-permutation network with 128, 192 or 256-bit keys and 10, 12 or 14 rounds. It is Rijndael with a fixed block size.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {b: the number of 128-bit blocks}
  time: {worst: Θ(b), average: Θ(b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2001
  people: [Joan Daemen, Vincent Rijmen]
  note: Daemen and Rijmen submitted Rijndael to the open AES competition of NIST in 1998. NIST selected it in October 2000 and published FIPS 197 in November 2001.
prereqs: [substitution-permutation-network, key-schedule, gf2-polynomial-arithmetic]
see_also: [s-box, data-encryption-standard, differential-cryptanalysis, linear-cryptanalysis, related-key-attack, integral-cryptanalysis, gcm-mode, timing-attack]
sources:
  - paper: doi:10.6028/NIST.FIPS.197-upd1
    title: NIST, FIPS 197, Advanced Encryption Standard (AES), November 26, 2001, updated May 9, 2023
    locator: Sections 5.1 to 5.3 (Cipher, KeyExpansion, InvCipher and the equivalent inverse cipher), Appendix A (key expansion), Appendix B (cipher example) and Appendix C.1 to C.3 (example vectors)
  - book: isbn:9783540425809
    title: Joan Daemen and Vincent Rijmen, The Design of Rijndael, Springer, 2002
    locator: Chapter 3 (the specification), Chapter 9 (the wide trail strategy and the four-round propagation theorem)
  - paper: "Andrey Bogdanov, Dmitry Khovratovich and Christian Rechberger, Biclique cryptanalysis of the full AES, Advances in Cryptology, ASIACRYPT 2011, LNCS 7073, Springer, 2011"
    locator: key recovery for AES-128, AES-192 and AES-256 in time 2^126.1, 2^189.7 and 2^254.4
  - paper: "Alex Biryukov and Dmitry Khovratovich, Related-key cryptanalysis of the full AES-192 and AES-256, Advances in Cryptology, ASIACRYPT 2009, LNCS 5912, Springer, 2009"
    locator: the related-key attack on AES-256 with time and data 2^99.5 and four related keys
  - url: "https://cr.yp.to/antiforgery/cachetiming-20050414.pdf"
    title: Daniel J. Bernstein, Cache-timing attacks on AES, preprint, April 2005
    locator: the timing attack on the table-based AES of OpenSSL over a network
  - paper: "Dag Arne Osvik, Adi Shamir and Eran Tromer, Cache attacks and countermeasures: the case of AES, Topics in Cryptology, CT-RSA 2006, LNCS 3860, Springer, 2006"
    locator: the Evict+Time and Prime+Probe attacks on the first and second rounds of T-table AES
  - paper: "Shay Gueron, Intel Advanced Encryption Standard (AES) New Instructions Set, Intel white paper 323641, 2010"
    locator: the AESENC, AESENCLAST, AESDEC, AESDECLAST, AESIMC and AESKEYGENASSIST instructions
---

The Advanced Encryption Standard (AES) is the [block cipher](/block-cipher/) of NIST FIPS 197. It encrypts 128-bit blocks with a key of 128, 192 or 256 bits, in 10, 12 or 14 rounds. It is the cipher Rijndael of Joan Daemen and Vincent Rijmen, restricted to a 128-bit block, and it won an open competition that NIST ran from 1997 to 2000. AES is a [substitution-permutation network](/substitution-permutation-network/): each round applies one [S-box](/s-box/) to every byte, moves bytes between columns, mixes each column by a linear map over GF($2^8$), and adds a round key from the [key expansion](/key-schedule/). Its design follows the *wide trail strategy*: a branch number of 5 forces at least 25 active S-boxes in any four-round trail, which bounds differential and linear trails. The best known key recovery on the full cipher, the biclique attack, saves less than a factor of 4 over [exhaustive search](/exhaustive-key-search/). Real breaks come from implementations, such as cache timing on table lookups.

## In plain words

AES holds the 16 bytes of a block in a 4 by 4 grid. A round does four things. It replaces every byte by its entry in a fixed table of 256 bytes. It slides row 1 of the grid by one place, row 2 by two places and row 3 by three. It mixes the four bytes of each column, so that each output byte depends on all four. Then it adds the round key with XOR.

The table gives the nonlinear part. The row shifts and the column mixing spread every byte over the whole grid in two rounds. The key enters at every round.

The round keys come from the cipher key by a short rule that copies and mixes 4-byte words. Decryption runs the inverse of each step in the reverse order.

## The problem

AES computes a permutation $E_K$ of $\{0,1\}^{128}$ for each key $K$ of $32 N_k$ bits, with $N_k \in \{4, 6, 8\}$, and its inverse. The number of rounds is $N_r = N_k + 6$, so 10, 12 or 14. The state is a $4 \times 4$ array of bytes $s_{r,c}$, filled column by column from the input bytes: $s_{r,c} = \mathit{in}[r + 4c]$. A byte is an element of GF($2^8$) = GF(2)$[x]/(m(x))$ with $m(x) = x^8 + x^4 + x^3 + x + 1$, written in hexadecimal; see [arithmetic on GF(2) polynomials](/gf2-polynomial-arithmetic/). Encryption of messages needs a mode of operation, such as [GCM](/gcm-mode/), CTR or XTS.

## The algorithm

The four steps are as follows.

- **SubBytes.** $s_{r,c} \leftarrow S(s_{r,c})$, where $S(a) = A \cdot a^{-1} \oplus \mathtt{63}$, with $a^{-1}$ the inverse in GF($2^8$) ($0^{-1} := 0$) and $A$ a fixed invertible $8 \times 8$ matrix over GF(2). So $S(\mathtt{00}) = \mathtt{63}$ and $S(\mathtt{53}) = \mathtt{ED}$.
- **ShiftRows.** $s'_{r,c} = s_{r, (c + r) \bmod 4}$: row $r$ rotates left by $r$ places.
- **MixColumns.** Each column is multiplied by the circulant matrix with first row $(\mathtt{02}, \mathtt{03}, \mathtt{01}, \mathtt{01})$. As polynomials, the column is multiplied by $a(x) = \mathtt{03}x^3 + \mathtt{01}x^2 + \mathtt{01}x + \mathtt{02}$ modulo $x^4 + 1$.
- **AddRoundKey.** Column $c$ is XORed with the word $w[4t + c]$ in round $t$.

```pseudo id=main
AES-ENCRYPT(key, in)
L1  Nr ← Nk + 6
L2  w ← KEY-EXPANSION(key)
L3  state ← ADDROUNDKEY(in, w[0..3])
L4  for t ← 1 to Nr − 1 do
L5      state ← SUBBYTES(state)
L6      state ← SHIFTROWS(state)
L7      state ← MIXCOLUMNS(state)
L8      state ← ADDROUNDKEY(state, w[4t..4t+3])
L9  state ← SUBBYTES(state)                 ▷ the last round has no MixColumns
L10 state ← SHIFTROWS(state)
L11 state ← ADDROUNDKEY(state, w[4Nr..4Nr+3])
L12 return state

KEY-EXPANSION(key)                           ▷ key has Nk words of 4 bytes
L13 w[i] ← word i of key, for i = 0, ..., Nk − 1
L14 for i ← Nk to 4Nr + 3 do
L15     temp ← w[i − 1]
L16     if i mod Nk = 0 then temp ← SUBWORD(ROTWORD(temp)) ⊕ Rcon[i/Nk]
L17     else if Nk > 6 and i mod Nk = 4 then temp ← SUBWORD(temp)
L18     w[i] ← w[i − Nk] ⊕ temp
L19 return w
```

ROTWORD$(a_0, a_1, a_2, a_3) = (a_1, a_2, a_3, a_0)$, SUBWORD applies $S$ to each byte, and $\mathrm{Rcon}[j] = (x^{j-1}, \mathtt{00}, \mathtt{00}, \mathtt{00})$, that is 01, 02, 04, 08, 10, 20, 40, 80, 1B, 36.

**The inverse cipher.** It applies AddRoundKey with $w[4N_r..4N_r+3]$, then for $t = N_r - 1$ down to 1 the steps InvShiftRows, InvSubBytes, AddRoundKey with round key $t$ and InvMixColumns, and ends with InvShiftRows, InvSubBytes and AddRoundKey with round key 0. InvShiftRows rotates row $r$ right by $r$ places, InvSubBytes uses $S^{-1}$, and InvMixColumns multiplies by $a^{-1}(x) = \mathtt{0B}x^3 + \mathtt{0D}x^2 + \mathtt{09}x + \mathtt{0E}$. FIPS 197 also gives an *equivalent inverse cipher* with the same order of steps as encryption, which applies InvMixColumns to round keys 1 to $N_r - 1$.

## Example

**FIPS 197 Appendix C.1 (AES-128).** Plaintext 00112233445566778899aabbccddeeff, key 000102030405060708090a0b0c0d0e0f. The state is written column by column.

| step | state |
|---|---|
| input XOR round key 0 | 00102030405060708090a0b0c0d0e0f0 |
| round 1, after SubBytes | 63cab7040953d051cd60e0e7ba70e18c |
| round 1, after ShiftRows | 6353e08c0960e104cd70b751bacad0e7 |
| round 1, after MixColumns | 5f72641557f5bc92f7be3b291db9f91a |
| round key 1 | d6aa74fdd2af72fadaa678f1d6ab76fe |
| start of round 2 | 89d810e8855ace682d1843d8cb128fe4 |
| start of round 10 | bd6e7c3df2b5779e0b61216e8b10b689 |
| round key 10 | 13111d7fe3944a17f307a78b4d2b30c5 |
| output | 69c4e0d86a7b0430d8cdb78070b4c55a |

**FIPS 197 Appendix C.2 and C.3.** With the same plaintext and the keys 000102...1617 (AES-192) and 000102...1e1f (AES-256), the outputs are dda97ca4864cdfe06eaf70a0ec0d7191 and 8ea2b7ca516745bfeafc49904b496089.

**FIPS 197 Appendix A and B.** The key 2b7e151628aed2a6abf7158809cf4f3c expands to $w[4..7]$ = a0fafe17 88542cb1 23a33939 2a6c7605, $w[36]$ = ac7766f3 and $w[40..43]$ = d014f9a8 c9ee2589 e13f0cc8 b6630ca6. With this key, the input 3243f6a8885a308d313198a2e0370734 of Appendix B encrypts to 3925841d02dc09fbdc118597196a0b32. The tests also check words of the 192-bit and 256-bit expansions of Appendix A.2 and A.3.

## Correctness

Each step is a bijection of the state with a known inverse: XOR with a fixed key is its own inverse, ShiftRows is undone by the opposite rotations, $S$ is a bijection because inversion in a field and the affine map are bijections, and MixColumns is undone by InvMixColumns because $a(x) \cdot a^{-1}(x) \equiv \mathtt{01} \pmod{x^4 + 1}$. The inverse cipher applies these inverses in the reverse order, using that InvShiftRows and InvSubBytes commute. The full proof, with the product $a(x) a^{-1}(x)$ worked out and the proof that the AES-128 key expansion can be inverted, is given below.

## Complexity

For a fixed key size, one block costs $N_r$ rounds of 16 S-box lookups, $N_r - 1$ MixColumns steps and $N_r + 1$ round key additions, so $\Theta(b)$ time for $b$ blocks and $\Theta(1)$ extra space after the key expansion, which has $4(N_r + 1)$ words. Fast software merges SubBytes, ShiftRows and MixColumns into four tables of 256 words of 32 bits (the *T-tables*), so a round is 16 lookups and 16 XORs. With the AES-NI instructions, one round is one instruction, AESENC, and modern processors encrypt at about 1 cycle per byte or less in parallel modes.

**Wide trail bound.** Let a *trail* be a sequence of state differences through the rounds, and call an S-box active when its input difference is nonzero.

**Theorem.** Every four-round trail with a nonzero input difference has at least 25 active S-boxes.

*Proof.* Key additions do not change differences, SubBytes keeps the set of nonzero bytes (as $S$ is a bijection), and ShiftRows moves bytes. MixColumns acts on each column by a linear map $\theta$ of branch number 5: for any nonzero column difference $u$, the number of nonzero bytes of $u$ and of $\theta(u)$ together is at least 5. This holds because the MixColumns matrix is MDS: every square submatrix is nonsingular.

Let $a_i$ be the number of active S-boxes in round $i$, and $c_i$ the number of nonzero columns at the input of MixColumns in round $i$.

*Two rounds.* $a_i + a_{i+1} \ge 5 c_i$. The nonzero bytes at the MixColumns input of round $i$ number $a_i$, and those at its output number $a_{i+1}$, since only a key addition lies between them and round $i+1$. An inactive column stays zero. For each active column the two counts sum to at least 5. Add over the $c_i$ active columns.

*ShiftRows spreads columns.* ShiftRows sends the 4 bytes of any column to 4 different columns, and so does its inverse. So the number of nonzero columns of a state before ShiftRows is at least the largest number of nonzero bytes in one column after it, and the number of nonzero columns after ShiftRows is at least the largest number of nonzero bytes in one column before it.

*Four rounds.* Let $X$ be the state at the input of round 2. MixColumns maps each column of round 1 to the same column, and is a bijection on columns, so $X$ has exactly $c_1$ nonzero columns. Let $Y$ be the output of MixColumns in round 2. By the same argument, $Y$ has as many nonzero columns as its image after SubBytes, and after ShiftRows of round 3 it has $c_3$ nonzero columns. Pick a nonzero column $j$ at the MixColumns input of round 2, with $u$ nonzero bytes, and let its output column in $Y$ have $v$ nonzero bytes, so $u + v \ge 5$. These $u$ bytes came from $u$ different columns of $X$, so $c_1 \ge u$. The $v$ bytes of column $j$ of $Y$ go to $v$ different columns in round 3, so $c_3 \ge v$. Hence $c_1 + c_3 \ge 5$, and

$$a_1 + a_2 + a_3 + a_4 \ge 5 c_1 + 5 c_3 \ge 25. \qquad \blacksquare$$

The AES S-box has differential uniformity 4 and largest linear correlation $2^{-3}$ in absolute value. So any four-round differential trail has probability at most $(4/256)^{25} = 2^{-150}$, and any four-round linear trail has correlation at most $2^{-75}$ in absolute value. This bounds single trails, not differentials, which can sum many trails, but it is the base of the design argument.

## Properties

- **Attack status.** No attack on full AES is known that is faster than exhaustive search by more than a small factor. The table lists the main results.

| attack | target | data | time | note |
|---|---|---|---|---|
| biclique (BKR 2011) | AES-128 | $2^{88}$ chosen | $2^{126.1}$ | full 10 rounds |
| biclique (BKR 2011) | AES-192 | $2^{80}$ chosen | $2^{189.7}$ | full 12 rounds |
| biclique (BKR 2011) | AES-256 | $2^{40}$ chosen | $2^{254.4}$ | full 14 rounds |
| related key (Biryukov and Khovratovich 2009) | AES-256 | $2^{99.5}$ | $2^{99.5}$ | needs 4 related keys |
| square (integral) attack | 6 of 10 rounds | $2^{32}$ chosen | about $2^{72}$ | Daemen and Rijmen |

- **Related keys.** The related-key attack does not apply when keys are random and independent, as in normal use. It matters when AES-256 is used to build a hash function or with keys derived by simple relations.
- **Key expansion.** For AES-128, any one round key gives the cipher key by running the expansion backward. See [key schedule](/key-schedule/).
- **Algebraic structure.** All steps except the S-box are linear over GF(2), and the S-box is inversion in GF($2^8$) up to an affine map. No attack has used this structure on the full cipher.

## Variants and improvements

- **Rijndael.** The original design allows blocks and keys of 128, 160, 192, 224 and 256 bits. AES fixes the block at 128 bits.
- **T-tables.** Software that merges the round steps into table lookups. It is fast but leaks the indexes through the cache.
- **Bitsliced AES.** Software that computes the S-box with Boolean operations on many blocks at once, with no secret indexes. It is constant time.
- **AES-NI and ARMv8 AES.** Hardware instructions that compute one round in constant time. Intel added AES-NI with the Westmere processors in 2010.
- **Modes.** [GCM](/gcm-mode/) for authenticated encryption, [XTS](/xts-mode/) for disk sectors, [CTR](/ctr-mode/) and [CBC](/cbc-mode/) for plain encryption. AES alone on independent blocks is [ECB](/ecb-mode/) and is not semantically secure.

## When to use it

AES is the default block cipher for new systems, in an authenticated mode such as GCM. Use it through a FIPS 140 validated module or a well-reviewed library, such as libsodium, that uses hardware instructions or bitsliced code. On processors without AES instructions, ChaCha20-Poly1305 is often faster and easier to make constant time. AES-256 gives a larger margin against quantum key search, where Grover's algorithm needs about $2^{k/2}$ steps.

## Pitfalls

- **Cache timing.** In the T-table code, the first-round indexes are $p_i \oplus k_i$. Take a cost model in which the attacker learns, for each lookup, which 64-byte cache line was used. A table of 256 entries of 4 bytes covers 16 lines, so each lookup reveals the top 4 bits of $p_i \oplus k_i$, and with known $p_i$ the top 4 bits of each of the 16 key bytes: 64 key bits from the first round. Osvik, Shamir and Tromer (2006) used the second round to get the rest. Bernstein (2005) recovered a key through network timing alone. The code on this page has the same problem, as it indexes a table by secret bytes. It is for study only and is not constant time.
- **Reduced-round code.** The parameter for the number of rounds in the study code exists only to study reduced-round AES. Fewer rounds are broken.
- **Byte order.** The state fills column by column. Reading the input row by row gives a cipher that round-trips but fails the vectors.
- **The last round.** It has no MixColumns. Code that applies MixColumns in round $N_r$ also round-trips but fails the vectors.
- **ECB and nonce reuse.** Most failures of AES in practice come from the mode: ECB leaks equal blocks, and a repeated nonce in GCM or CTR leaks the XOR of plaintexts and, in GCM, allows forgery.

## Implementations

## History

NIST announced the AES competition in January 1997 to replace DES. Fifteen candidates entered in 1998, five reached the final round (MARS, RC6, Rijndael, Serpent and Twofish), and NIST selected Rijndael on October 2, 2000. FIPS 197 was published on November 26, 2001, and took effect in May 2002. Daemen and Rijmen built Rijndael on their earlier ciphers Square and SHARK and on the wide trail strategy from Daemen's 1995 thesis. Bernstein showed cache-timing attacks on table-based AES in 2005, and Osvik, Shamir and Tromer refined them in 2006. Intel added AES-NI in 2010. Biryukov and Khovratovich gave related-key attacks on AES-192 and AES-256 in 2009, and Bogdanov, Khovratovich and Rechberger gave the biclique attacks in 2011. NIST published an editorial update of FIPS 197 in May 2023 without changing the algorithm.

## References
