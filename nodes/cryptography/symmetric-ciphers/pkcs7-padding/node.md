---
tag: TD8JXS
kind: algorithm
slug: pkcs7-padding
name: PKCS#7 padding
aliases:
- PKCS#5 padding
area: cryptography/symmetric-ciphers
level: intro
summary: Always add k bytes of value k, with 1 ≤ k ≤ b, to reach a multiple of the block length b. Removal is unambiguous; a strict check is needed, and its errors must not leak.
solves: [block-padding]
model: word-ram
complexity:
  vars: {b: the block length in bytes, n: the message length in bytes}
  time: {worst: Θ(b), average: Θ(b), best: Θ(1)}
  space: {extra: Θ(b)}
properties: {deterministic: true}
history:
  year: 1993
  people: [RSA Laboratories]
  note: "RSA Laboratories published PKCS #5 and PKCS #7 version 1.5 in 1993. The rule was later reissued in RFC 2315 (1998) and RFC 5652 (2009), Section 6.3."
prereqs: [block-padding]
see_also: [block-padding, cbc-mode, padding-oracle-attack, ecb-mode, timing-attack, authenticated-encryption]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc5652"
    title: Russ Housley, RFC 5652, Cryptographic Message Syntax (CMS), 2009
    locator: Section 6.3 (content-encryption process, the padding rule and the remark that it is well defined only for block lengths below 256)
  - url: "https://www.rfc-editor.org/rfc/rfc2315"
    title: "Burt Kaliski, RFC 2315, PKCS #7, Cryptographic Message Syntax Version 1.5, 1998"
    locator: "Section 10.3, Note 2 (the same padding rule in PKCS #7 version 1.5)"
  - url: "https://www.rfc-editor.org/rfc/rfc8018"
    title: "Kathleen Moriarty, Burt Kaliski and Andreas Rusch, RFC 8018, PKCS #5, Password-Based Cryptography Specification Version 2.1, 2017"
    locator: Section 6.1.1 (PBES1 encryption, step 4, the padding string for 8-octet blocks)
  - paper: "Serge Vaudenay, Security flaws induced by CBC padding, applications to SSL, IPSEC, WTLS, EUROCRYPT 2002, LNCS 2332, pages 534 to 545"
    locator: the padding oracle attack on CBC with this padding
---

PKCS #7 padding extends a message to a multiple of the block length $b$ by appending $k$ bytes, each with the value $k$, where $k = b - (n \bmod b)$ and $n$ is the message length. So $1 \le k \le b$: a message that already fills its last block gets a whole extra block. RFC 5652, Section 6.3, defines it, and PKCS #5 uses the same rule with $b = 8$. Removal reads the last byte, checks that the last $k$ bytes all equal $k$, and cuts them off. The check must be strict, and the receiver must never reveal whether it failed, because a padding error reported after CBC decryption is the oracle of Vaudenay's attack.

## In plain words

Take the number of bytes that are missing to fill the last block. If no bytes are missing, take a full block instead. Write that number into each of the missing bytes. For a 16-byte block and the 14-byte message `attack at dawn`, two bytes are missing, so you add the byte `02` twice.

To remove the padding, read the last byte. It tells you how many bytes to remove. Before you remove them, check that all of them have that same value and that the value is between 1 and the block length. If a check fails, the data is damaged or forged.

## The problem

The input is a byte string $M$ of length $n \ge 0$ and a block length $b$ with $1 \le b \le 255$. Padding must produce a string whose length is a positive multiple of $b$, and unpadding must give back $M$ exactly. A strict unpadding must also reject every string that is not the padding of some message. This is an instance of [block padding](/block-padding/).

## The algorithm

```pseudo id=main
PKCS7-PAD(M, b)                             ▷ 1 ≤ b ≤ 255
L1  k ← b − (|M| mod b)                     ▷ 1 ≤ k ≤ b
L2  return M ‖ (byte k repeated k times)

PKCS7-UNPAD(X, b)                           ▷ strict
L3  if |X| = 0 or |X| mod b ≠ 0 then reject
L4  k ← X[|X|]                              ▷ the last byte
L5  if k = 0 or k > b then reject
L6  for i ← 1 to k: if X[|X| − i + 1] ≠ k then reject
L7  return X[1 .. |X| − k]
```

Line L1 is the only computation. Lines L3 to L6 are the strict check: length, range of $k$, and the value of every pad byte. A lenient unpad that only does L4 and L7 returns wrong data for damaged input and gives no error, which is worse. Why $b \le 255$: $k$ must fit in one byte, and $k = b$ is possible.

**About the code.** The Python code of this page is for study only. It is not constant time: `pkcs7_unpad` stops at the first bad byte, so its running time and its error depend on secret plaintext. The file also has a masked check that reads all $b$ bytes and folds the result with bit masks, which is the shape of a constant-time check in C. Use an AEAD from a FIPS 140 validated module or libsodium, which needs no padding at all.

## Example

Block length $b = 16$.

| message $M$ | $n$ | $k$ | padded string, last block in hex |
|---|---|---|---|
| `attack at dawn` | 14 | 2 | `61747461636b206174206461776e` `0202` |
| `ICE ICE BABY` | 12 | 4 | `494345204943452042414259` `04040404` |
| `YELLOW SUBMARINE` | 16 | 16 | a new block of sixteen `10` bytes |
| (empty) | 0 | 16 | sixteen `10` bytes |

Trace of PKCS7-UNPAD on three 16-byte inputs.

| input (last 4 bytes) | L4: $k$ | L5 | L6 | result |
|---|---|---|---|---|
| `ICE ICE BABY` `04 04 04 04` | 4 | pass | all four equal 4 | `ICE ICE BABY` |
| `ICE ICE BABY` `05 05 05 05` | 5 | pass | byte 12 is `59` (`Y`), not 5 | reject |
| `ICE ICE BABY` `01 02 03 04` | 4 | pass | byte 15 is `03`, not 4 | reject |

The lenient unpad of the code would return `ICE ICE BABY` for the third input as if it were valid.

## Correctness

**Claim.** For every $M$ and $1 \le b \le 255$: PKCS7-PAD$(M, b)$ has a length that is a positive multiple of $b$; PKCS7-UNPAD(PKCS7-PAD$(M, b), b) = M$; and PKCS7-UNPAD accepts $X$ only if $X = $ PKCS7-PAD$(M, b)$ for the $M$ it returns. So padding is injective, and the strict unpad accepts exactly the image of padding. The key step: if the strict check passes with last byte $k$, then the returned message has length $\equiv -k \pmod b$, so padding it again gives back the same $k$ and the same bytes. The full proof is below.

## Complexity

PKCS7-PAD writes $k \le b$ bytes, so it costs $\Theta(b)$ in the worst case on a buffer that can grow in place; a copy of the message adds $\Theta(n)$. PKCS7-UNPAD reads at most $b$ bytes: $\Theta(1)$ when it rejects at L3 or L5, $\Theta(k)$ otherwise. The expansion is $k$ bytes, between 1 and $b$, and $b$ bytes when $n$ is a multiple of $b$. A constant-time unpad must read all $b$ final bytes on every input, so its cost is $\Theta(b)$ always.

## Properties

- **Unambiguous.** The last byte always gives the pad length, so no message is lost, even one that ends in bytes that look like padding.
- **Always pads.** Even an aligned message grows by one block. This is required: see the counting argument in [block padding](/block-padding/).
- **A random block is valid with probability about $1/255$.** For a uniformly random final block of 16 bytes, padding of length $k$ is valid with probability $256^{-k}$, and the total is $\sum_{k=1}^{16} 256^{-k} \approx 1/255 \approx 0.00392$. Most of this is $k = 1$ (a last byte `01`). A padding oracle attack uses exactly this: it changes the last byte of the previous ciphertext block until the padding becomes valid.
- **Leaks under an oracle.** After CBC decryption, an answer "padding valid or not" for chosen ciphertexts reveals the plaintext byte by byte, with at most 256 queries per byte. See [CBC mode](/cbc-mode/) for an implementation and [padding oracle attack](/padding-oracle-attack/).

## Variants and improvements

- **PKCS #5 padding.** The same rule with $b = 8$ (RFC 8018, Section 6.1.1). Many libraries, for example the Java name `PKCS5Padding`, use the name for any $b$, including AES with $b = 16$.
- **TLS CBC padding.** TLS 1.0 to 1.2 add $k$ bytes of value $k - 1$, and allow up to 256 bytes of padding to hide the length. SSL 3.0 checked only the last byte, which the POODLE attack (2014) used.
- **Constant-time check.** Read all of the last $b$ bytes, compute a mask for "$i \le k$" for each position, and OR together the mismatches under the mask. Return one error for every failure, after the MAC check, in the same time.
- **No padding.** Encrypt-then-MAC with a stream mode, or an AEAD such as [GCM](/gcm-mode/), avoids padding and padding oracles altogether.

## When to use it

Use PKCS #7 padding when a format requires ECB or CBC with a block cipher, for example CMS, or when reading old data. In new designs prefer an AEAD, which needs no padding. If you must decrypt CBC with padding, verify a MAC over the ciphertext first, and check the padding only after the MAC is valid.

## Pitfalls

- **Lenient unpadding.** Reading only the last byte accepts forged data and can remove up to 255 bytes, even past the start of the message.
- **Reporting padding errors.** Distinct errors, distinct alerts or measurably different timing for bad padding versus bad MAC give a padding oracle.
- **Forgetting the full block when aligned.** An implementation that does not pad aligned messages cannot be unpadded correctly when such a message ends in `01`.
- **Accepting $k = 0$ or $k > b$.** Both are invalid; accepting $k = 0$ returns the input unchanged, and $k > b$ removes data.
- **Checking padding before the MAC.** In MAC-then-encrypt, the padding check happens on unauthenticated data. This is the setting of Vaudenay's attack and of Lucky Thirteen.

## Implementations

The Python code has `pkcs7_pad`, the strict `pkcs7_unpad` (with a marker for each line of the pseudocode), a masked check and, only as a counterexample for the tests, a lenient unpad. The tests check the rule, all lengths for several $b$, exhaustive acceptance on small inputs and the probability above.

## History

RSA Laboratories published version 1.5 of PKCS #5 (password-based encryption with DES-CBC, so $b = 8$) and of PKCS #7 (the cryptographic message syntax) in November 1993. RFC 2315 (1998) republished PKCS #7 version 1.5, and RFC 5652 (2009) is the current CMS standard with the rule in Section 6.3. Vaudenay (Eurocrypt 2002) showed that a receiver that reveals padding validity after CBC decryption lets an attacker decrypt; the attack later broke deployed systems such as ASP.NET (2010) and SSL 3.0 (POODLE, 2014).

## References
