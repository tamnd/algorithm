---
tag: GMTEEK
kind: algorithm
slug: rsa-pkcs1-v1-5-encryption
name: RSA PKCS#1 v1.5 encryption
aliases:
- PKCS#1 v1.5
area: cryptography/public-key
level: core
summary: "The old randomized RSA padding of RFC 8017 Section 7.2. A server that reports a padding error turns it into Bleichenbacher's million message attack."
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus, k: the number of octets of the modulus}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1993
  people: [RSA Data Security, Burt Kaliski, Daniel Bleichenbacher]
  note: "Published as PKCS #1 v1.5 in November 1993 and written up in RFC 2313 in 1998. Bleichenbacher broke it as used in protocols in 1998, and RFC 8017 keeps it only for old systems."
prereqs: [rsa-cryptosystem]
see_also: [rsa-oaep, padding-oracle-attack, chosen-ciphertext-attack, ind-cca-security, rsa-cryptosystem, tls-handshake, rsa-signature]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: "Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1, RSA Cryptography Specifications Version 2.2, 2016"
    locator: Section 7.2 (RSAES-PKCS1-v1_5), Section 7.2.1 (the encoding), Section 7.2.2 (the decoding and the note on error messages) and Section 7 (OAEP is required for new applications)
  - paper: "Daniel Bleichenbacher, Chosen ciphertext attacks against protocols based on the RSA encryption standard PKCS #1, CRYPTO 1998, LNCS 1462, pages 1 to 12"
    locator: Section 3 (the oracle and the four steps) and Section 4 (the number of queries, about one million for a modulus of 1024 binary digits)
  - url: "https://www.rfc-editor.org/rfc/rfc2313"
    title: "Burt Kaliski, RFC 2313, PKCS #1, RSA Encryption Version 1.5, 1998"
    locator: Section 8 (the encryption process with block type 02)
  - url: "https://www.rfc-editor.org/rfc/rfc5246"
    title: Tim Dierks and Eric Rescorla, RFC 5246, The Transport Layer Security (TLS) Protocol Version 1.2, 2008
    locator: Section 7.4.7.1 (treat a bad premaster secret as a random one, and do not report the padding error)
  - url: "https://www.usenix.org/conference/usenixsecurity18/presentation/bock"
    title: Hanno Böck, Juraj Somorovsky and Craig Young, Return Of Bleichenbacher's Oracle Threat (ROBOT), 27th USENIX Security Symposium, 2018
    locator: Sections 3 and 4 (the oracle variants found in vendor stacks, and the affected products)
  - url: "https://doi.org/10.1007/978-3-031-51479-1_13"
    title: Hubert Kario, Everlasting ROBOT, the Marvin Attack, ESORICS 2023, LNCS 14345, pages 243 to 262
    locator: Sections 4 and 5 (timing oracles in current libraries and the test method)
---

RSAES-PKCS1-v1_5 is the first standard padding for RSA encryption. It puts the message after a random nonzero padding string, as $\mathrm{EM} = \texttt{0x00} \Vert \texttt{0x02} \Vert \mathrm{PS} \Vert \texttt{0x00} \Vert M$, and then applies the [RSA](/rsa-cryptosystem/) encryption primitive. The padding makes encryption randomized, but the scheme is not [IND-CCA](/ind-cca-security/) secure: a receiver that says "bad padding" leaks one bit for each chosen ciphertext, and Bleichenbacher's attack of 1998 turns those bits into the whole plaintext. RFC 8017 keeps the scheme only for old systems and requires [OAEP](/rsa-oaep/) for new ones.

**Notation.** $N$ is the modulus, $b$ its number of binary digits, $k = \lceil b/8 \rceil$ its number of octets, $e$ the public exponent, $d$ the private exponent, $M$ the message of $\mathrm{mLen}$ octets, $\mathrm{PS}$ the padding string, $\mathrm{EM}$ the encoded message of $k$ octets and $C$ the ciphertext. $B = 2^{8(k-2)}$, so an encoded message $m = \mathrm{OS2IP}(\mathrm{EM})$ satisfies $2B \le m < 3B$.

## In plain words

RSA on its own always gives the same ciphertext for the same message, so it cannot be used as it is. This scheme fixes that in the simplest way. It puts random filler in front of the message, with a marker byte at the start and a zero byte between the filler and the message, and then it raises the whole block to the public power.

The receiver undoes the power, looks for the marker and the zero byte, and returns what follows. The danger is in that check. If the receiver tells the sender that the check failed, an attacker can send millions of changed copies of a ciphertext and learn, one answer at a time, which values pass. Each answer narrows the range of the secret message. After about a million answers the message is known. New systems must use OAEP instead.

## The problem

The scheme solves [public-key encryption](/public-key-encryption/) for short messages, of up to $k - 11$ octets. It was designed to give [probabilistic encryption](/probabilistic-encryption/), which textbook RSA is not, and it was the key transport step of SSL and of TLS up to version 1.2.

## The algorithm

```pseudo id=main
EME-PKCS1-V1_5-ENCODE(M, k)              ▷ k octets of modulus, mLen = |M|
L1  if |M| > k − 11 then return "message too long"
L2  PS ← k − |M| − 3 random octets, each one nonzero
L3  return 0x00 ‖ 0x02 ‖ PS ‖ 0x00 ‖ M

RSAES-PKCS1-V1_5-ENCRYPT((N, e), M)
L4  EM ← EME-PKCS1-V1_5-ENCODE(M, k)
L5  m ← OS2IP(EM)
L6  return I2OSP(m^e mod N, k)

RSAES-PKCS1-V1_5-DECRYPT(private key, C)
L7  if |C| ≠ k or k < 11 then return "decryption error"
L8  m ← RSADP(OS2IP(C)),  EM ← I2OSP(m, k)
L9  if EM[0] ≠ 0x00 or EM[1] ≠ 0x02 then return "decryption error"
L10 i ← the least index i > 1 with EM[i] = 0x00, or none
L11 if there is no such i or i < 10 then return "decryption error"
L12 return EM[i+1 .. k−1]
```

Line L1 is the length limit: three octets go to the two leading octets and the separator, and the eight octets that stay are the shortest allowed padding string. Line L2 draws the padding string from the system random source; every octet must be nonzero, so that line L10 finds the separator and not a padding octet. Line L3 gives $\mathrm{EM} < 3 \cdot 2^{8(k-2)} < N$, so line L6 never overflows.

Lines L4 to L6 are RSAES-PKCS1-V1_5-ENCRYPT of RFC 8017 Section 7.2.1, with OS2IP and I2OSP from Section 4. Lines L7 to L12 are the decryption of Section 7.2.2; RSADP is the private operation, with the [Chinese remainder theorem](/chinese-remainder-theorem/) in practice. The test $i < 10$ on line L11 means that at least eight padding octets came before the separator, because the indices 0 and 1 hold the two leading octets.

RFC 8017 Section 7.2.2 then says: the three failures of lines L9 and L11 must not be told apart, and the error must not say which one happened. The next sections show what goes wrong when they are told apart.

**About the code.** The Python code of this page is for study only. It is not constant time, and it must not be used to protect real data. The attack code runs only against the local simulated oracle in the same file, on a toy key that the test file makes.

### Bleichenbacher's attack

The attacker has a ciphertext $C$ with the integer $c_0 = m^e \bmod N$ and an oracle that answers "yes" when the decryption of a chosen ciphertext starts with $\texttt{0x00}\,\texttt{0x02}$. A "yes" for $c_0 \cdot s^e$ means $2B \le ms \bmod N < 3B$, so $ms - rN$ lies in $[2B, 3B)$ for some integer $r$, which bounds $m$ in a short range. The search keeps a set of ranges and shrinks it.

```pseudo id=bleichenbacher
BLEICHENBACHER(N, e, c0, ORACLE)         ▷ B = 2^(8(k−2)); c0 conforming, so s0 = 1
L1  s ← ⌈N / 3B⌉
L2  while not ORACLE(c0·s^e mod N) do s ← s + 1          ▷ step 2a
L3  M ← NARROW({[2B, 3B − 1]}, s)                        ▷ step 3
L4  while M is not a single value do
L5      if |M| > 1 then                                  ▷ step 2b
L6          repeat s ← s + 1 until ORACLE(c0·s^e mod N)
L7      else  [a, b] ← the one range of M                ▷ step 2c
L8          for r ← ⌈2(b·s − 2B)/N⌉, ⌈2(b·s − 2B)/N⌉ + 1, ... do
L9              for s' ← ⌈(2B + rN)/b⌉ to ⌊(3B + rN)/a⌋ do
                    if ORACLE(c0·s'^e mod N) then s ← s', exit both loops
L10     M ← NARROW(M, s)
    return the one value of M, which is OS2IP(EM)

NARROW(M, s)
    for each [a, b] in M and each r with ⌈(a·s − 3B + 1)/N⌉ ≤ r ≤ ⌊(b·s − 2B)/N⌋
        add [max(a, ⌈(2B + rN)/s⌉), min(b, ⌊(3B − 1 + rN)/s⌋)] when it is not empty
    return the union of the ranges that were added
```

Step 2a needs about $N/B \approx 2^{16}$ queries for a modulus of 1024 binary digits, because a random $s$ gives a conforming value with probability near $B/N$. After that, step 2c roughly doubles $s$ and halves the range, so the whole search costs about $2\log_2 N$ more rounds with a few queries each. Bleichenbacher's estimate is about one million chosen ciphertexts in total. The [padding oracle attack](/padding-oracle-attack/) page puts this in the family of the CBC padding oracle.

## Example

The toy key of the test file has $N = pq$ with $p$ and $q$ of 125 binary digits, so $b = 249$ and $k = 32$. Encoding the message $M = \texttt{"toy key"}$ of 7 octets gives a padding string of $32 - 7 - 3 = 22$ octets:

| field | octets | value |
|---|---|---|
| leading pair | 2 | `0002` |
| PS, all nonzero | 22 | `3b5ff7612132b50c162440d0823667a508767d75647f` |
| separator | 1 | `00` |
| $M$ | 7 | `746f79206b6579` |

So $\mathrm{EM} =$ `00023b5ff7612132b50c162440d0823667a508767d75647f00746f79206b6579`, and $2B \le \mathrm{OS2IP}(\mathrm{EM}) < 3B$ holds because the second octet is 2. Encryption raises this integer to the power $e = 65537$ modulo $N$, and decryption on lines L7 to L12 finds the separator at index $i = 24 \ge 10$ and returns the 7 message octets.

### A trace of the attack on the toy key

The same ciphertext goes to the local oracle. The modulus has 249 binary digits and $k = 32$, so $N/B = 387$: a conforming value is much more common than for a real key, which is why the toy run is short. The search starts at $s = \lceil N/3B \rceil = 130$ and finds the first conforming $s = 522$ after 394 queries, the first of which only checks that $c_0$ itself is conforming.

| step | $s$ | ranges | width of the range set in binary digits |
|---|---|---|---|
| 1 | 522 | 2 | 232 |
| 2 | 869 | 1 | 230 |
| 3 | 2258 | 1 | 229 |
| 25 | 10941987220 | 1 | 206 |
| 50 | 367152173459921220 | 1 | 182 |
| 100 | 413376597895592619762270396817502 | 1 | 131 |
| 150 | 465420673061568570829809817758252362553282463198 | 1 | 82 |
| 200 | 524017092442651415327668371238791133601748284486220226623788390 | 1 | 31 |
| 231 | 1125318137293098292180224389202097462697137785146210018001440657788728377 | 1 | 1 |

The run ends after 231 steps and 1167 oracle queries, and the single value left is exactly $\mathrm{EM}$ above. The attacker never sees the private key and never factors $N$: the only information is 1167 yes or no answers.

## Correctness

Encoding and decoding are inverse for every message of at most $k - 11$ octets. The decoder can only go wrong if it finds the wrong separator, and that cannot happen: every octet of $\mathrm{PS}$ is nonzero on line L2, so the least zero octet after index 1 is the separator written on line L3. The RSA step is correct because $\mathrm{EM} < 3 \cdot 2^{8(k-2)} \le N$, so $\mathrm{OS2IP}(\mathrm{EM})$ is a valid message representative and $\mathrm{RSADP}(\mathrm{RSAEP}(m)) = m$. The soundness of the attack, that a conforming answer keeps the true $m$ in the new range set, is proved with the full statement in the proof below.

## Complexity

Let $b$ be the number of binary digits of $N$ and $k = \lceil b/8 \rceil$.

- **Encoding and decoding**: $\Theta(k)$ octet operations, so $\Theta(b)$.
- **Encryption**: one [modular exponentiation](/modular-exponentiation/) with the public exponent, $\Theta(b^2)$ for $e = 65537$ with schoolbook arithmetic.
- **Decryption**: one private exponentiation, $\Theta(b^3)$, or about a quarter of that with the CRT form.
- **Message length**: at most $k - 11$ octets, so a 2048 digit modulus carries at most 245 octets. Longer data needs [hybrid encryption](/hybrid-encryption/).
- **The attack**: about $N/B \approx 2^{16}$ queries for step 2a, then about $2\log_2 N$ rounds of a few queries, so about $2^{20}$ queries for $b = 1024$. The trimming of Bardou and others (CRYPTO 2012) cuts this to a few thousand queries for some devices.

## Properties

- **Randomized but not IND-CCA.** The padding string gives different ciphertexts for the same message, and the scheme is believed [IND-CPA](/ind-cpa-security/) secure under the [RSA assumption](/rsa-problem/) in practice, with no proof. It is not IND-CCA secure, and the attack above is the witness. No security proof of the scheme exists in any model.
- **The oracle is the whole weakness.** The attack needs one bit for each chosen ciphertext: "did the decoding succeed". The bit can come from an error message, a TLS alert, a distinct error code, a timing difference, or any later protocol step that fails only for a bad padding.
- **A stricter oracle still works.** A server that checks the separator too, or the length of the recovered message, says "yes" less often, so the attack needs more queries. It does not stop the attack: every "yes" still proves $2B \le ms \bmod N < 3B$. The test file measures the two answer rates.
- **Malleable.** Like textbook RSA, a ciphertext can be multiplied by $s^e$, which the attack uses. The scheme has no integrity check of any kind, so it is not [non-malleable](/non-malleability/).
- **No label and no associated data.** OAEP has an optional label; v1.5 has nothing to bind the ciphertext to its context.

## Variants and improvements

- **[OAEP](/rsa-oaep/)** (RFC 8017 Section 7.1) replaces this encoding and has an IND-CCA2 proof in the [random oracle model](/random-oracle-model/). This is the choice for every new application.
- **The TLS countermeasure.** RFC 5246 Section 7.4.7.1 says that a server which finds a bad padding, or a wrong version in the premaster secret, must continue with a 48 octet random premaster secret. The handshake then fails at the Finished message, with no bit that depends on the padding. The code must be written so that both paths run the same work, which is harder than it looks; see the ROBOT and Marvin results.
- **Implicit rejection in general.** The same idea gives the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) and the modern [KEM](/key-encapsulation-mechanism/) rule: never report a decryption failure, return a pseudorandom key that depends on the ciphertext.
- **RSA-KEM.** Encrypt a random integer below $N$ with no padding and hash it to get the key. The scheme has a proof and no padding check at all, so there is no oracle. RFC 5990 gives it for CMS.
- **PKCS #1 v1.5 signatures** use block type `0x01` with `0xff` padding and a deterministic digest info. They are a different scheme on the same encoding idea, and they are not broken by this attack; see [RSA signature](/rsa-signature/).

## When to use it

Use it only when an old peer or an old format leaves no choice, for example a stored key blob or a protocol version that you cannot change. Then follow three rules: return no information on the failure reason, keep the work after a failure the same as after a success, and never use the same RSA key for a v1.5 decryption service and for anything else. For new work use [OAEP](/rsa-oaep/), or better a [KEM](/key-encapsulation-mechanism/) with implicit rejection such as RSA-KEM, [ECIES](/ecies/) or ML-KEM. TLS 1.3 (RFC 8446) removed RSA key transport, so a modern TLS stack needs this scheme for nothing.

## Pitfalls

- **Two different error paths.** Returning one error from line L9 and another from line L11, or returning at L9 much sooner than at L11, gives the oracle. Do not return early: run the whole decoding and give one result, or use the random premaster secret of RFC 5246 Section 7.4.7.1.
- **A padding string that can hold a zero octet.** If line L2 draws uniform octets instead of nonzero octets, then line L10 can find a zero inside $\mathrm{PS}$, the decoder returns the wrong message, and the shortest paddings fail at L11. Draw again on a zero, or use a rejection loop.
- **A predictable padding string.** A counter or a constant on line L2 makes encryption deterministic and loses IND-CPA security. The padding string is not a nonce; it must come from the system random source.
- **Skipping the length check.** Without line L1 the padding string can fall below eight octets, which weakens the search space of the padding, and with $\mathrm{mLen} > k - 3$ the encoding has no separator at all.
- **Not checking the ciphertext length.** Line L7 must reject a ciphertext whose length is not $k$ octets. A shorter input, read as an integer, is still a valid group element, and accepting it can create a second oracle.
- **A shared RSA key.** A key used for v1.5 key transport and for signatures lets the attack recover any signed value, because the attack returns the private operation of any chosen input. This is how the DROWN attack of 2016 and the ROBOT report of 2018 broke sessions of other protocols that shared the key.
- **Trusting a library to be constant time.** The Marvin results of 2023 found timing oracles in current libraries, 25 years after the first attack. If you must keep v1.5, test it with the published tools.

## Implementations

## History

RSA Data Security published PKCS #1 v1.5 in November 1993, and RFC 2313 wrote it up in March 1998 with block type `0x02` for encryption. In the same year Bleichenbacher showed at CRYPTO 1998 that an SSL server which answers "bad padding" lets an attacker decrypt any ciphertext with about one million chosen ciphertexts. PKCS #1 v2.0 added OAEP a few months later, and SSL and TLS added the random premaster secret countermeasure.

The weakness came back many times. Klíma, Pokorný and Rosa found a version oracle in 2003. Bardou and others cut the query count with trimmers at CRYPTO 2012 and broke several hardware tokens. The 2016 DROWN attack used an SSLv2 oracle to break TLS sessions of the same key. ROBOT, at USENIX Security 2018, found the old oracle again in the stacks of F5, Citrix, Cisco and others, 19 years after the fix. The Marvin attack of Kario, at ESORICS 2023, found timing oracles in current libraries, including some that only leaked a few nanoseconds. TLS 1.3 removed RSA key transport, which is the lasting fix.

## References
