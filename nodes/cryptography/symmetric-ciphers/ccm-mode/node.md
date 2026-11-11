---
tag: 0AFYD8
kind: technique
slug: ccm-mode
name: Counter with CBC-MAC mode
aliases:
- CCM
area: cryptography/symmetric-ciphers
level: advanced
summary: AEAD mode with one AES key. CBC-MAC over a header block, the associated data and the message, then CTR on the message and the tag. Two passes, not online. In Wi-Fi WPA2.
prereqs: [cbc-mac, ctr-mode, authenticated-encryption]
see_also: [ccm-decryption-check, gcm-mode, eax-mode, ocb-mode, nonce, cmac, block-padding, message-authentication-code]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38C"
    title: Morris Dworkin, NIST Special Publication 800-38C, Recommendation for Block Cipher Modes of Operation, The CCM Mode for Authentication and Confidentiality, May 2004 (updated 2007)
    locator: Section 5.4 (the three properties of the formatting function), Section 6.1 (generation-encryption), Section 6.2 (decryption-verification), Appendix A (formatting and counter blocks), Appendix B.2 (MAC length) and Appendix C (Examples 1 to 4)
  - url: "https://www.rfc-editor.org/rfc/rfc3610"
    title: Doug Whiting, Russ Housley and Niels Ferguson, RFC 3610, Counter with CBC-MAC (CCM), 2003
    locator: Section 2.2 (B_0, the flags and the encoding of l(a)), Section 2.3 (the blocks A_i), Section 2.6 (the limit of 2^61 block cipher calls) and Section 8 (Packet Vectors 1 to 24)
  - paper: "Jakob Jonsson, On the security of CTR + CBC-MAC, Selected Areas in Cryptography (SAC 2002), LNCS 2595, pages 76 to 93"
    locator: the proofs of privacy and authenticity of CCM when the block cipher is a PRP
  - paper: "Phillip Rogaway and David Wagner, A critique of CCM, Cryptology ePrint Archive, Report 2003/070"
    locator: the list of efficiency problems, among them that CCM is not online and cannot preprocess static associated data
---

Counter with CBC-MAC (CCM) is an [authenticated encryption](/authenticated-encryption/) mode for a 128-bit block cipher. Whiting, Housley and Ferguson designed it in 2002 for IEEE 802.11i, and it is specified in RFC 3610 (2003) and NIST SP 800-38C (2004). It computes a [CBC-MAC](/cbc-mac/) of a formatted encoding of the nonce, the associated data and the message, and then encrypts the message and the tag with [CTR mode](/ctr-mode/). Both steps use the same key. The formatting puts the message length in the first block, which makes CBC-MAC secure for messages of varying length, and it makes the first MAC block differ from every counter block. CCM is the cipher of WPA2 Wi-Fi (CCMP), Bluetooth Low Energy, Zigbee and Thread.

**Notation.** $E_K$ is AES with key $K$. $N$ is the nonce of $15 - L$ bytes, $A$ the associated data, $P$ the payload (message), $M$ the tag length in bytes and $L$ the size in bytes of the length field. $B_0, B_1, \ldots, B_r$ are the formatted blocks, $A_i$ the counter blocks and $S_i = E_K(A_i)$. $[x]_L$ is $x$ as an $L$-byte big-endian integer. RFC 3610 writes $m$ and $a$ for the message and the associated data.

## In plain words

CCM reads the data twice with one key. In the first pass it builds a fingerprint: it writes a header block with the nonce and the message length, adds the associated data and the message, and runs CBC-MAC over all of it. In the second pass it hides the message and the fingerprint with counter mode: it encrypts numbered blocks made from the nonce, and XORs them in. Counter 0 hides the fingerprint, and counters 1, 2, 3 and so on hide the message. The receiver undoes the counter mode, recomputes the fingerprint, and gives out the message only if the two fingerprints match. CCM needs only the AES encryption function, so it fits small devices.

## When it applies

- **Constrained devices with AES hardware.** CCM needs only $E_K$, no field multiplication and no decryption function. This is why IEEE 802.11 (CCMP), IEEE 802.15.4, Bluetooth LE and Thread chose it.
- **Packets whose length is known before processing.** The length is in $B_0$, so a sender must know $|P|$ before it starts the MAC. This is natural for packets.
- **Small tags under control.** SP 800-38C, Appendix B.2, allows $M$ down to 4 bytes but says that tags of less than 8 bytes need a careful analysis of the number of failed decryptions.
- **Not for streams.** CCM is not online: a stream of unknown length cannot be processed, and the associated data cannot be preprocessed once for many messages (Rogaway and Wagner 2003). Use [GCM](/gcm-mode/), [EAX](/eax-mode/) or [OCB](/ocb-mode/) instead.
- **Not for maximum speed.** CBC-MAC is serial and each block costs two AES calls in total. GCM or OCB are faster on large processors.

## The template

```pseudo id=main
CCM-ENCRYPT(K, N, A, P)          ▷ tag of M bytes, length field of L bytes, |N| = 15 − L bytes
L1  B_0 ← flags ‖ N ‖ [|P|]_L     ▷ flags = 64·[A ≠ ε] + 8·(M − 2)/2 + (L − 1)
L2  if A ≠ ε then append pad(enc(|A|) ‖ A)     ▷ enc(|A|) has 2, 6 or 10 bytes
L3  append pad(P)                 ▷ zero bytes up to a whole block
L4  X ← 0^128
L5  for each block B_i, i = 0 … r do X ← E_K(X ⊕ B_i)          ▷ CBC-MAC
L6  T ← MSB_M(X)
L7  for i ← 1 to ⌈|P|/16⌉ do S_i ← E_K(A_i)     ▷ A_i = (L − 1) ‖ N ‖ [i]_L
L8  C ← P ⊕ MSB_|P|(S_1 ‖ S_2 ‖ …)
L9  U ← T ⊕ MSB_M(E_K(A_0))
L10 return C ‖ U

CCM-DECRYPT(K, N, A, C ‖ U)      ▷ details on the CCM decryption check page
L11 P ← C ⊕ MSB_|C|(S_1 ‖ S_2 ‖ …);  T ← U ⊕ MSB_M(E_K(A_0))
L12 T′ ← MSB_M(CBC-MAC of the blocks of N, A, P), as in L1 to L6
L13 if T′ ≠ T then return INVALID and release nothing     ▷ constant-time comparison
L14 return P
```

The holes are the block cipher (any 128-bit cipher, in practice AES), $M \in \{4, 6, \ldots, 16\}$ and $L \in \{2, \ldots, 8\}$. A larger $L$ allows longer messages ($|P| < 2^{8L}$ bytes) but leaves a shorter nonce. WPA2 CCMP uses $M = 8$, $L = 2$ and a 13-byte nonce built from the packet number and the sender address.

**The flags byte of $B_0$** (RFC 3610, Section 2.2). Bit 7 is reserved and zero. Bit 6 (Adata) is 1 if there is associated data. Bits 5 to 3 hold $M' = (M - 2)/2$, which is never zero because $M \ge 4$. Bits 2 to 0 hold $L' = L - 1$.

**The encoding of the length of $A$.** If $0 < |A| < 2^{16} - 2^8$, it is two bytes. If $2^{16} - 2^8 \le |A| < 2^{32}$, it is `ff fe` followed by four bytes. Otherwise it is `ff ff` followed by eight bytes. The encoded length and $A$ together are padded with zero bytes to whole blocks.

**The counter blocks.** $A_i$ has the flags byte $L - 1$, then $N$, then $[i]_L$. Bits 5 to 3 of this flags byte are zero, while those of $B_0$ hold $M' \ge 1$. So no counter block ever equals a $B_0$ under the key. This is property 3 of SP 800-38C, Section 5.4, and it is what makes the single key safe: the CTR outputs never reveal a CBC-MAC input value at position 0.

**Why the formatting works.** CBC-MAC alone is a secure PRF only for messages of one fixed length, as the splice attack on the [CBC-MAC](/cbc-mac/) page shows. Here $B_0$ contains $|P|$, and the encoding of $|A|$ comes first in the associated data, so the blocks form a prefix-free encoding of $(N, A, P)$: no valid formatted string is a proper prefix of another. CBC-MAC is a secure PRF on prefix-free inputs (Petrank and Rackoff 2000). Property 2 of Section 5.4 states exactly this.

**Security model and bounds.** Jonsson (SAC 2002) proved that CCM is private (indistinguishable from random bits) and authentic (INT-CTXT) against nonce-respecting adversaries, if $E$ is a PRP. The loss is a birthday term in the total number $\sigma$ of block cipher calls, of order $\sigma^2/2^{128}$, plus about $q_v/2^{8M}$ for $q_v$ forgery attempts. RFC 3610, Section 2.6, limits one key to $2^{61}$ block cipher calls. The reduction is tight up to these terms: a birthday attack on CBC-MAC needs about $2^{64}$ blocks. CCM is MAC-then-encrypt, which is not secure for every encryption scheme (see [authenticated encryption](/authenticated-encryption/)), but it is secure for this combination, because CTR has no redundant bits and the tag itself is encrypted.

**About the code.** The Python code of this page is for study only. It is not constant time, because the AES in `aes.py` uses table lookups. Do not use it to protect real data; use AES-CCM from a FIPS 140 validated module. The decryption checks the tag before it returns any plaintext and compares with OR folding.

## Classic examples

### RFC 3610, Packet Vector 1

Key `c0c1c2c3c4c5c6c7c8c9cacbcccdcecf`, nonce `00000003020100a0a1a2a3a4a5` (13 bytes, so $L = 2$), $M = 8$, header $A$ = bytes 00 to 07, payload = bytes 08 to 1e (23 bytes).

| step | value |
|---|---|
| $B_0$ ("CBC IV in") | `59000000030201` `00a0a1a2a3a4a5` `0017` |
| flags of $B_0$ | `59` = 64 (Adata) + 8 × 3 ($M' = 3$) + 1 ($L' = 1$) |
| $B_1$ (the header) | `0008` `0001020304050607` and 6 zero bytes |
| $B_2, B_3$ (the payload) | `08090a0b…17`, `18191a1b1c1d1e` and 9 zero bytes |
| $T$ ("CBC-MAC") | `2dc697e411ca83a8` |
| $A_1$ ("CTR Start") | `01000000030201` `00a0a1a2a3a4a5` `0001` |
| output after the header | `588c979a61c663d2f066d0c2c0f989806d5f6b61dac384` |
| $U$ | `17e8d12cfdf926e0` |

The tests check Packet Vectors 1 to 4, 7 and 13 of RFC 3610, Section 8, and Examples 1 to 4 of SP 800-38C, Appendix C. Example 4 has 65536 bytes of associated data, so its length uses the `ff fe` prefix. The tests also check $B_0$, $T$ and $A_1$ of Packet Vector 1, the encoding of $|A|$ at its boundaries, that no counter block equals $B_0$, round trips, the rejection of every changed bit of the ciphertext, the tag and the header, and the rejection of bad parameters.

## Variations

- **CCM\* (IEEE 802.15.4).** Allows $M = 0$, which gives encryption with no authentication, for some security levels of Zigbee.
- **CCMP (IEEE 802.11i, WPA2).** AES-CCM with $M = 8$ and $L = 2$, with the nonce from the packet number, which is never reused under one temporal key.
- **AES-CCM in TLS and IPsec.** RFC 6655 adds AES-CCM cipher suites to TLS, with a 16-byte or 8-byte tag (CCM_8). RFC 4309 adds it to IPsec ESP.
- **[EAX](/eax-mode/).** Bellare, Rogaway and Wagner proposed EAX in reply to the critique of CCM. It uses OMAC instead of a formatted CBC-MAC, it is online, and it can preprocess static headers.
- **[GCM](/gcm-mode/).** Also CTR plus a MAC, with a field-multiplication hash instead of CBC-MAC, which runs in parallel.

## Pitfalls

- **Releasing plaintext before the check.** CCM decrypts first and verifies after. Code that writes out the plaintext as it decrypts, or that returns it with an error flag, gives a decryption oracle. See the [CCM decryption check](/ccm-decryption-check/).
- **Nonce reuse.** A repeated nonce repeats the CTR keystream, so the XOR of the two payloads leaks. Unlike GCM, it does not give a universal forgery key, but the secrecy of the payloads is lost.
- **Mixing parameters.** $M$ and $L$ are part of $B_0$, so a tag made for one $(M, L)$ fails under another. Both sides must agree on them out of band.
- **Short tags.** With $M = 4$ an attacker succeeds once in about $2^{32}$ attempts. Limit the number of failures per key, as SP 800-38C, Appendix B.2, says.
- **Empty payloads in SP 800-38C.** Step 1 of Section 6.2 returns INVALID if $\mathrm{Clen} \le \mathrm{Tlen}$, so the decryption as written rejects a ciphertext with an empty payload, while RFC 3610 allows it. Check which rule a protocol uses.

## Exercises

1. Show that without the length in $B_0$, the CBC-MAC splice gives a forgery against CCM with a fixed nonce.
2. Show that if bits 5 to 3 of the flags of $A_i$ could equal those of $B_0$, an attacker who sees $S_0$ for some nonce would learn $E_K(B_0)$ for some formatted input, and say what this breaks.
3. Count the AES calls of CCM for a message of $\ell$ blocks and associated data of $a$ blocks (after encoding), and compare with GCM.
4. Explain why CCM cannot start the MAC of a stream before the end of the stream, and how EAX avoids the problem.

## References

- Morris Dworkin, NIST SP 800-38C, 2004 (updated 2007).
- Doug Whiting, Russ Housley and Niels Ferguson, RFC 3610, 2003.
- Jakob Jonsson, On the security of CTR + CBC-MAC, SAC 2002.
- Phillip Rogaway and David Wagner, A critique of CCM, 2003.
