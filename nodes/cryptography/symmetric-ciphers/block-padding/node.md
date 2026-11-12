---
tag: YE2JDS
kind: problem
slug: block-padding
name: Block padding
aliases:
area: cryptography/symmetric-ciphers
level: intro
summary: "Extend a message to a whole number of cipher blocks so that the receiver can remove the extension without doubt. PKCS #7 and ISO/IEC 7816-4 are unambiguous; zero padding is not."
prereqs: [block-cipher]
see_also: [pkcs7-padding, ecb-mode, cbc-mode, padding-oracle-attack, ctr-mode, xts-mode]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Appendix A (padding, the example of a 1 bit followed by 0 bits, and padding every message)
  - url: "https://csrc.nist.gov/pubs/sp/800/38/a/sup/final"
    title: Morris Dworkin, Addendum to NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Three Variants of Ciphertext Stealing for CBC Mode, 2010
    locator: the variants CBC-CS1, CBC-CS2 and CBC-CS3
  - url: "https://www.rfc-editor.org/rfc/rfc5652"
    title: Russ Housley, RFC 5652, Cryptographic Message Syntax (CMS), 2009
    locator: "Section 6.3 (content-encryption process, the PKCS #7 padding rule)"
  - url: "https://www.rfc-editor.org/rfc/rfc3962"
    title: Ken Raeburn, RFC 3962, Advanced Encryption Standard (AES) Encryption for Kerberos 5, 2005
    locator: Section 5 (CBC with ciphertext stealing) and Appendix B (test vectors for CBC with ciphertext stealing)
  - paper: "ISO/IEC 9797-1:2011, Information technology, Security techniques, Message Authentication Codes (MACs), Part 1, Mechanisms using a block cipher"
    locator: the padding methods 1, 2 and 3 (method 2 is the 0x80 then zeros padding also used by ISO/IEC 7816-4)
  - paper: "Serge Vaudenay, Security flaws induced by CBC padding, applications to SSL, IPSEC, WTLS, EUROCRYPT 2002, LNCS 2332, pages 534 to 545"
    locator: the padding oracle attack, and the remark that other padding rules give similar oracles
---

Block padding is the problem of extending a message to a whole number of blocks, so that a block mode such as [ECB](/ecb-mode/) or [CBC](/cbc-mode/) can encrypt it, in a way that the receiver can undo exactly. The extension must be reversible for every message, including messages that already fill their last block and messages whose last bytes look like padding. PKCS #7, ISO/IEC 7816-4 and ANSI X9.23 solve it by always adding between 1 and $b$ bytes that encode their own length. Zero padding does not solve it. Ciphertext stealing avoids padding altogether, and stream modes such as [CTR](/ctr-mode/) never need it.

## In plain words

A block cipher eats data in fixed pieces, for example 16 bytes for AES. Most messages do not have a length that is a multiple of 16. So the sender adds some bytes to the end before encryption, and the receiver must take them away after decryption. The hard part is that the receiver sees only the padded result. It must be able to tell where the message stops and the padding starts, without any other information.

If the padding is only zeros, a message that really ends in a zero byte loses that byte. Good padding schemes always add at least one byte, and the added bytes say how many there are. When the message already fills its last block, they add a full extra block.

## Definition

**Input.** A block length $b$ in bytes ($b = 16$ for AES, $b = 8$ for DES and [Triple DES](/triple-des/)) and a message $M$ of any length $\ell \ge 0$ bytes.

**Output.** A padding function $\mathrm{pad}_b$ and an unpadding function $\mathrm{unpad}_b$ such that:

1. $|\mathrm{pad}_b(M)|$ is a positive multiple of $b$ for every $M$ (positive, because ECB and CBC need at least one block);
2. $\mathrm{unpad}_b(\mathrm{pad}_b(M)) = M$ for every $M$, which forces $\mathrm{pad}_b$ to be injective;
3. $\mathrm{unpad}_b$ rejects strings that are not in the image of $\mathrm{pad}_b$, if the scheme is strict.

The cost measures are the expansion $|\mathrm{pad}_b(M)| - |M|$ and the work, which for all common schemes is $O(b)$.

**Why this matters for security.** After decryption, $\mathrm{unpad}$ looks at secret plaintext. If an attacker can learn whether it accepted, for example from an error message or from timing, then that one bit per query is enough to decrypt CBC ciphertexts, as Vaudenay showed in 2002. This is a property of the system, not of the padding scheme, and every scheme in this page with a check is exposed.

## Variants

- **Byte padding versus bit padding.** SP 800-38A, Appendix A, gives the bit-level form: append one 1 bit, then as few 0 bits as needed. On bytes this is ISO/IEC 7816-4.
- **Pad always versus pad when needed.** Pad-always schemes add a full block to aligned messages. A scheme may skip padding for aligned messages only if the receiver can tell from outside information, such as a length field, that the message is not padded (SP 800-38A, Appendix A).
- **Length-preserving encryption.** When the ciphertext must not be longer than the plaintext, as for disk sectors or in fixed-size fields, padding is not allowed. Then ciphertext stealing or a stream mode is used.

## Examples

All examples use $b = 8$. The tests of this page check every row.

| scheme | rule | `hello` (5 bytes) | `abcdefgh` (8 bytes) |
|---|---|---|---|
| PKCS #7 | add $k$ bytes of value $k$, $1 \le k \le b$ | `68656c6c6f` `030303` | message, then `08` eight times |
| ISO/IEC 7816-4 | add `80`, then $k - 1$ bytes `00` | `68656c6c6f` `800000` | message, then `80` and seven `00` |
| ANSI X9.23 | add $k - 1$ bytes `00`, then $k$ | `68656c6c6f` `000003` | message, then seven `00` and `08` |
| zero padding | add `00` bytes only if needed | `68656c6c6f` `000000` | message, nothing added |

**The failure of zero padding.** `hello` and `hello` followed by one `00` byte both pad to `68656c6c6f000000`. The receiver cannot know which one was sent. Zero padding is safe only for data that never ends in a zero byte (for example, printable text) or when the length is sent elsewhere.

**Why the other three work.** In PKCS #7 and X9.23 the last byte is the count $k$, and $1 \le k \le b$, so the receiver always knows how many bytes to remove. In ISO/IEC 7816-4 the receiver removes trailing `00` bytes and then exactly one `80`; the `80` marks the end of the message even if the message itself ends in `00` or `80`.

## Known algorithms

- **[PKCS #7 padding](/pkcs7-padding/)** (RFC 5652, Section 6.3). The most common choice in software. PKCS #5 padding is the same rule for $b = 8$.
- **ISO/IEC 7816-4 padding**, also padding method 2 of ISO/IEC 9797-1. Used in smart cards and in some MAC standards.
- **ANSI X9.23 padding.** Zero bytes and a final count byte. A related rule from ISO 10126 (now withdrawn) fills with random bytes instead of zeros.
- **Zero padding**, padding method 1 of ISO/IEC 9797-1. Ambiguous unless the length is known.
- **Length prefix**, padding method 3 of ISO/IEC 9797-1. Put the length in a first block, then zero pad. Unambiguous, but the length must be known before the first block is processed.
- **Ciphertext stealing** for CBC, defined in three variants CS1, CS2 and CS3 by the SP 800-38A Addendum (2010). No padding at all for messages of at least one block. The last partial block is zero filled for the cipher, and the bytes that this zero fill hides are taken ("stolen") from the previous ciphertext block, which is then cut short. The three variants differ only in the order of the last two ciphertext blocks: CS1 never swaps them, CS2 swaps them when the last block is partial, and CS3 always swaps them. Kerberos (RFC 3962) uses CS3, and the code of this page reproduces the four RFC 3962 Appendix B vectors (17, 31, 32 and 47 bytes). XTS uses the same idea, see [XTS mode](/xts-mode/).

**About the code.** The Python code of this page, with its own AES, is for study only. It is not constant time, and its unpad functions branch on secret bytes, so they can act as padding oracles. Use an AEAD from a FIPS 140 validated module or libsodium, which needs no padding.

## Bounds

**Claim.** Let $b \ge 2$. No injective padding maps every message to the shortest multiple of $b$ at or above its length. More precisely, for every $k \ge 1$, an injective padding sends some message of length at most $kb$ to a string longer than $kb$.

**Proof.** There are $\sum_{i=0}^{kb} 256^i$ messages of length at most $kb$. The strings of length at most $kb$ that are multiples of $b$ number $\sum_{j=0}^{k} 256^{jb}$. Since $b \ge 2$, this sum has $k + 1$ terms, all of which also appear in the first sum, and the first sum has other positive terms, for example $256^1$. So the first sum is larger, and by the pigeonhole principle two messages would share a padded string if all of them stayed within length $kb$. That contradicts injectivity. $\blacksquare$

So some expansion past the next block boundary is unavoidable. The pad-always schemes pay it on every aligned message: the expansion is between 1 and $b$ bytes, $b$ when $\ell$ is a multiple of $b$. A scheme can pay less often, for example by padding an aligned message only when its last byte looks like padding, but this saves little and makes the code more complex.

## Reductions

- **Padding from a length field.** Any unambiguous scheme can be built from a length encoding: the pad must let the receiver find $\ell$. PKCS #7 encodes $b - (\ell \bmod b)$ in the last byte; ISO/IEC 7816-4 encodes it by the position of the last nonzero byte.
- **Removing the need for padding.** CBC with ciphertext stealing, or a stream mode such as [CTR](/ctr-mode/), [OFB](/ofb-mode/) or GCM, encrypts messages of any length (for CBC-CS, at least one block) with no expansion beyond the IV.

## Applications

- **CBC encryption in TLS up to 1.2, IPsec ESP, CMS and many file formats.** All use a padding rule; TLS uses a variant in which every pad byte has the value $k - 1$.
- **MACs.** CBC-MAC and [CMAC](/cmac/) pad the last block; CMAC uses the ISO/IEC 7816-4 rule plus a different subkey, so that padded and unpadded messages do not collide.
- **Hash functions.** Merkle-Damgård hashes such as SHA-256 use a related rule: a 1 bit, zeros, and the message length.

## References
