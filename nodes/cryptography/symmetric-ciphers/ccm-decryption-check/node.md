---
tag: PYJ12X
kind: algorithm
slug: ccm-decryption-check
name: CCM decryption-verification
aliases:
- CCM authenticated decryption
area: cryptography/symmetric-ciphers
level: advanced
summary: "The receiver side of CCM, SP 800-38C Section 6.2: decrypt into a private buffer, recompute the CBC-MAC, compare without early exit, and release the payload or one error only."
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {m: the number of payload blocks, a: the number of formatted associated data blocks}
  time: {worst: Θ(m + a), average: Θ(m + a), best: Θ(1)}
  space: {extra: Θ(m)}
properties: {deterministic: true}
history:
  year: 2004
  people: [Doug Whiting, Russ Housley, Niels Ferguson, Morris Dworkin]
  note: RFC 3610 (2003) said that a receiver must reveal nothing but the failure. NIST SP 800-38C (2004) wrote the check as ten steps and added that the two kinds of failure must look the same.
prereqs: [ccm-mode]
see_also: [authenticated-encryption, padding-oracle-attack, timing-attack, chosen-ciphertext-attack, gcm-mode, cbc-mac]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38C"
    title: Morris Dworkin, NIST Special Publication 800-38C, Recommendation for Block Cipher Modes of Operation, The CCM Mode for Authentication and Confidentiality, May 2004 (updated 2007)
    locator: Section 6.2 (decryption-verification, Steps 1 to 10, and the paragraph after them), Section 5.4 (valid inputs), Appendix A (formatting and counter blocks) and Appendix C (Examples 1 to 4)
  - url: "https://www.rfc-editor.org/rfc/rfc3610"
    title: Doug Whiting, Russ Housley and Niels Ferguson, RFC 3610, Counter with CBC-MAC (CCM), 2003
    locator: Section 2.5 (decryption and authentication checking) and Section 2.6 (the receiver must verify before it releases any information)
  - paper: "Elena Andreeva, Andrey Bogdanov, Atul Luykx, Bart Mennink, Nicky Mouha and Kan Yasuda, How to securely release unverified plaintext in authenticated encryption, ASIACRYPT 2014, LNCS 8873, pages 105 to 125"
    locator: the RUP setting, where decryption releases plaintext before verification, and the attacks on CCM, GCM and other modes in that setting
  - paper: "Serge Vaudenay, Security flaws induced by CBC padding, EUROCRYPT 2002, LNCS 2332, pages 534 to 545"
    locator: the padding oracle, an error that depends on the plaintext and is returned before any integrity check
---

CCM decryption-verification is the receiver side of [CCM](/ccm-mode/). It takes a nonce, the associated data and a purported ciphertext, and it returns either the payload or the single message INVALID. NIST SP 800-38C, Section 6.2, gives it as ten steps: decrypt with CTR mode, recompute the [CBC-MAC](/cbc-mac/) over the formatted nonce, associated data and payload, and compare it with the decrypted tag. The part that matters for security is what happens on failure. The payload and the tag "shall not be revealed", and an outsider must not be able to tell a failure of the input check from a failure of the tag check, "for example, from the timing of the error message". Code that hands out plaintext first and checks later turns CCM into an oracle that decrypts any ciphertext.

**Notation.** $E_K$ is AES with key $K$, $N$ the nonce, $A$ the associated data, $C$ the purported ciphertext of $\mathrm{Clen}$ bits, $\mathrm{Tlen}$ the tag length in bits, $\mathrm{Ctr}_j$ the counter blocks and $S_j = E_K(\mathrm{Ctr}_j)$. $\mathrm{MSB}_k$ and $\mathrm{LSB}_k$ are the leftmost and rightmost $k$ bits.

## In plain words

A CCM ciphertext is a message hidden by counter mode, followed by a hidden fingerprint. To check it, the receiver must first remove the counter mode, because the fingerprint was made from the plain message. So for a moment the receiver holds a message that may be fake. This step keeps that message locked away. It recomputes the fingerprint from the decrypted message, compares it with the received one byte by byte without stopping early, and only then releases the message. If anything is wrong it says one word, INVALID, and nothing else: no partial message, no reason, no different timing. Without this discipline, an attacker could change a stolen ciphertext, send it, and read the decryption.

## The problem

Input: a key $K$ shared with the sender, a nonce $N$, associated data $A$, a purported ciphertext $C$ and the agreed tag length $\mathrm{Tlen}$. Output: the payload $P$ if $C$ is exactly the output of CCM generation-encryption on $(N, A, P)$ under $K$, and INVALID otherwise. The output INVALID must carry no other information. In the model of [authenticated encryption](/authenticated-encryption/), this is what lets the decryption oracle of the IND-CCA game be simulated by "always INVALID" for every ciphertext the sender did not make.

## The algorithm

```pseudo id=main
CCM-DECRYPT-VERIFY(K, N, A, C)      ▷ SP 800-38C, Section 6.2; Tlen and the formatting are fixed
L1  if Clen ≤ Tlen then return INVALID
L2  m ← ⌈(Clen − Tlen)/128⌉;  Ctr_0, …, Ctr_m ← counter blocks of N
L3  S_0 ← E_K(Ctr_0)
L4  S ← E_K(Ctr_1) ‖ … ‖ E_K(Ctr_m)
L5  P ← MSB_{Clen−Tlen}(C) ⊕ MSB_{Clen−Tlen}(S)       ▷ kept in a private buffer
L6  T ← LSB_Tlen(C) ⊕ MSB_Tlen(S_0)
L7  ok ← (N, A, P) valid;  B_0, …, B_r ← format(N, A, P)
L8  Y ← CBC-MAC_K(B_0, …, B_r)        ▷ Y_0 = E_K(B_0), Y_i = E_K(B_i ⊕ Y_{i−1})
L9  ok ← ok and (T = MSB_Tlen(Y))      ▷ read every byte; no early exit
L10 if not ok then erase P and T; return INVALID
L11 return P
```

Lines L1 to L10 are Steps 1 to 10 of Section 6.2. The standard returns at once if the inputs are not valid in Step 7. The code computes a dummy MAC in that case and joins both failures at L10, so that the two failures take the same path. "Valid" means the conditions of Appendix A.1: a nonce of 7 to 13 bytes, a tag of 4 to 16 bytes in steps of 2, and a payload shorter than $2^{8q}$ bytes with $q = 15 - |N|$.

**About the code.** The Python code of this page is for study only. It is not constant time: AES uses table lookups, and Python itself gives no timing guarantees. Do not use it to protect real data. Use AES-CCM from a FIPS 140 validated module. The file also has two wrong decryptors, used only by the tests to show the harm.

## Example

SP 800-38C, Appendix C.1: key `404142434445464748494a4b4c4d4e4f`, $N$ = `10111213141516`, $A$ = `0001020304050607`, $\mathrm{Tlen} = 32$, and the ciphertext $C$ = `7162015b4dac255d`.

| step | value |
|---|---|
| L1 | $\mathrm{Clen} = 64 > 32$, go on |
| L2 | $m = 1$, $\mathrm{Ctr}_0$ = `07101112131415160000000000000000` |
| L3 | $S_0$ = `2d28114610676c2632bad748559a679a` |
| L4 | $S_1$ = `51432378e474b33971318484103cddfb` |
| L5 | $P$ = `7162015b` ⊕ `51432378` = `20212223` |
| L6 | $T$ = `4dac255d` ⊕ `2d281146` = `6084341b` |
| L7 | $B_0 B_1 B_2$ = `4f101112131415160000000000000004` `00080001020304050607000000000000` `20212223000000000000000000000000` |
| L8 | $Y_2$ = `6084341b32042bf000b4b7995553a3c5` |
| L9, L10 | $\mathrm{MSB}_{32}(Y_2)$ = `6084341b` = $T$, so return `20212223` |

Now flip the last bit of the first byte group: $C'$ = `7162015a4dac255d`. L5 gives $P'$ = `20212222` and L6 the same $T$ = `6084341b`. The MAC of the new blocks is $Y_2'$ = `247820b3594cc1d46a48b70601d27dc3`, which does not start with $T$, so the result is INVALID and $P'$ is erased. A receiver that released $P'$ first would have shown the attacker that a flip of bit $i$ of $C$ flips bit $i$ of $P$, and with it any payload under that nonce could be read.

## Correctness

Three claims hold. (1) Completeness: for every output $C$ of generation-encryption on a valid $(N, A, P)$, the algorithm returns $P$. (2) Canonical verification: if the algorithm returns some $P$ on $(N, A, C)$, then $C$ is exactly the output of generation-encryption on $(N, A, P)$; so an accepted $C$ that the sender never made is a forgery against CCM. (3) No release: on every rejected input the output is the constant INVALID, so the view of a caller is a function of the accept bit alone. The first two follow because CTR with the same counter blocks is an involution on the payload and on the tag, and generation-encryption is deterministic. With (3), the decryption oracle in the IND-CCA game of [authenticated encryption](/authenticated-encryption/) is the "always INVALID" oracle until a forgery happens, which is the step that makes ciphertext integrity imply chosen-ciphertext security. The full proof is below.

## Complexity

For a payload of $m$ blocks and $a$ blocks of formatted associated data, the algorithm makes $m + 1$ block cipher calls for the CTR part and $1 + a + m$ calls for the CBC-MAC, so $\Theta(m + a)$ time. Step L1 rejects a too-short input in $\Theta(1)$. The CBC-MAC is serial, the CTR part is parallel. The extra space is $\Theta(m)$: the payload must be held back until L9 is done, because it cannot be released before. A streaming decryptor with $\Theta(1)$ memory is exactly the wrong design that this page warns against; if memory is short, split the data into separate CCM messages, each with its own tag.

## Properties

- **Deterministic.** The same inputs always give the same output.
- **One error.** Every failure gives the same output, INVALID, with no payload, no tag and no reason.
- **Constant-time comparison.** L9 compares all $\mathrm{Tlen}/8$ bytes and folds the differences with OR. An early-exit comparison leaks the length of the correct prefix through timing and lets an attacker find a valid tag byte by byte.
- **Not online.** The payload is released only after the whole ciphertext is read.
- **Rejects an empty payload as written.** L1 returns INVALID when $\mathrm{Clen} = \mathrm{Tlen}$, although RFC 3610 allows an empty message.

## Variants and improvements

- **RFC 3610, Section 2.5.** The same process in prose: recompute the key stream, recover $m$ and $T$, recompute the CBC-MAC, and on failure "MUST NOT reveal the decrypted message, the value T, or any other information".
- **Other AEAD modes.** GCM, EAX and ChaCha20-Poly1305 can check the tag before they decrypt, because their MAC is over the ciphertext. CCM and SIV must decrypt first, because their MAC is over the plaintext, so the buffer of L5 is unavoidable for them.
- **Release of unverified plaintext (RUP).** Andreeva, Bogdanov, Luykx, Mennink, Mouha and Yasuda (ASIACRYPT 2014) studied what security remains if decryption does release plaintext before verification. CCM keeps almost none: its privacy fails at once, as the tests show. Modes built for RUP need a different design.
- **Chunked encryption.** For large files, protocols such as the STREAM construction split the data into chunks with their own tags, so each chunk can be verified and released on its own.

## When to use it

Every CCM receiver must run this check exactly in this order. The same discipline applies to every AEAD: never act on, store, log, render or parse a plaintext before its tag is verified, and give one error for every failure. In particular, a receiver must not check the format of the payload (a version byte, padding, a length field) before the tag, because the result of such a check is a [padding oracle](/padding-oracle-attack/) in a new form.

## Pitfalls

- **Releasing plaintext first.** A streaming API that writes plaintext to its output and reports the tag result at the end gives the attacker a decryption oracle: send $C \oplus \Delta$ with the original nonce and tag, read $P \oplus \Delta$. The test `test_release_before_check_decrypts_any_target_with_one_query` does this in one query.
- **Checking the payload before the tag.** The test `test_parse_before_check_reveals_the_first_byte` uses a receiver that checks a version byte before the tag and answers BAD VERSION or INVALID. By trying the 256 values of the first ciphertext byte, the attacker learns the first payload byte. The correct process gives INVALID to all 255 changed queries.
- **Different errors or timings for Step 7 and Step 10.** SP 800-38C asks that the two be indistinguishable. A fast reject on a bad length and a slow reject on a bad tag tell the attacker which test failed.
- **Early-exit comparison.** `==` on byte strings in many languages stops at the first difference.
- **Keeping the plaintext after a failure.** Logs, crash dumps and error messages that contain the buffer of L5 release it.
- **Real cases.** The EFAIL attacks (Poddebniak and others, USENIX Security 2018) made email clients render decrypted content of OpenPGP and S/MIME messages whose integrity was not checked first, and so leaked the plaintext to the attacker.

## Implementations

The Python code gives `decrypt_verify` with the line markers of the pseudocode, `generate_encrypt` for the tests, and the two wrong decryptors `decrypt_release_first` and `decrypt_parse_first`. The tests check AES against FIPS 197, Appendix C.1. They run Examples 1 to 4 of SP 800-38C, Appendix C, through decryption-verification, and Packet Vector 1 of RFC 3610, Section 8. They check that every changed bit of the ciphertext, a changed header and a changed nonce give INVALID, that short ciphertexts fail at Step 1, and that an invalid nonce and a bad tag give the same error. The two attack tests show the harm of each wrong decryptor and show that the correct one leaks nothing in the same queries.

## History

The CCM authors wrote in RFC 3610 (September 2003) that the receiver must verify the CBC-MAC before it releases any information, and must destroy everything else on failure. NIST SP 800-38C (May 2004) wrote the process as ten numbered steps and added the requirement that a failure in the validity check of Step 7 must not be distinguishable from a failure of the tag in Step 10. The danger of plaintext-dependent errors had been shown by Vaudenay's padding oracle against CBC (EUROCRYPT 2002). The question of what remains when plaintext is released early was studied formally from 2014 under the name RUP.

## References

- Morris Dworkin, NIST SP 800-38C, Section 6.2, 2004 (updated 2007).
- Doug Whiting, Russ Housley and Niels Ferguson, RFC 3610, Sections 2.5 and 2.6, 2003.
- Elena Andreeva, Andrey Bogdanov, Atul Luykx, Bart Mennink, Nicky Mouha and Kan Yasuda, ASIACRYPT 2014.
- Serge Vaudenay, Security flaws induced by CBC padding, EUROCRYPT 2002.
