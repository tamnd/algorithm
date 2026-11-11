---
tag: 180BZ6
kind: concept
slug: non-repudiation
name: Non-repudiation
aliases:
- signer cannot deny signing
- non-repudiation of origin
area: cryptography/signatures
level: intro
summary: "The goal that a signer cannot later deny a signature to a third party. Digital signatures give its technical core; keys bound to people, timestamps and law give the rest."
prereqs: [digital-signature]
see_also: [existential-unforgeability, message-authentication-code, undeniable-signature, designated-verifier-signature, forward-secure-signature, ring-signature, signature-forgery, signature-scheme]
sources:
  - url: "https://eur-lex.europa.eu/eli/reg/2014/910/oj"
    title: Regulation (EU) No 910/2014 of the European Parliament and of the Council on electronic identification and trust services (eIDAS), 23 July 2014
    locator: Article 3 (definitions of electronic, advanced and qualified electronic signatures), Article 25 (legal effects), Article 26 (requirements for advanced electronic signatures)
  - url: "https://www.govinfo.gov/content/pkg/PLAW-106publ229/pdf/PLAW-106publ229.pdf"
    title: Electronic Signatures in Global and National Commerce Act (E-SIGN), Public Law 106-229, 30 June 2000, codified at 15 U.S.C. 7001 and following
    locator: Section 101(a), a signature or contract may not be denied legal effect only because it is in electronic form
  - url: "https://www.rfc-editor.org/rfc/rfc3161"
    title: Carlisle Adams, Pat Cain, Denis Pinkas and Robert Zuccherato, RFC 3161, Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP), August 2001
    locator: Section 1 and Section 2, a time-stamping authority signs a hash of the data together with the time, to prove that the data existed before that time
  - url: "https://www.rfc-editor.org/rfc/rfc5280"
    title: David Cooper and others, RFC 5280, Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile, May 2008
    locator: Section 5.3.1, the revocation reason keyCompromise; Section 4.2.1.3, the nonRepudiation (contentCommitment) key usage bit
  - paper: "Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, 1976"
    locator: Section on one-way authentication, signatures that a third party can check and that the receiver cannot produce
  - paper: "Nikita Borisov, Ian Goldberg and Eric Brewer, Off-the-record communication, or, why not to use PGP, ACM WPES 2004"
    locator: deniable authentication as a deliberate design goal for private conversations
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 1, Section 1.2 (non-repudiation as an information security objective) and Chapter 13, Section 13.8 (trusted third parties, notaries and timestamping)
---

Non-repudiation is the security goal that the author of a message cannot later deny, to a third party such as a judge, that they produced it. A [digital signature](/digital-signature/) gives the technical core of the goal: only the holder of the private key can make a valid signature, and anyone with the public key can check it. The goal as a whole also needs a trusted binding of the key to a person, protection of the key, proof of the time of signing, and law that gives the signature an effect.

**Notation.** $sk$ and $pk$ are the private and public keys of the signer, $m$ the message and $\sigma$ the signature. A message authentication code (MAC) tag is $\tau$, made with a key $K$ that two parties share.

## In plain words

When you sign a paper contract, your handwriting ties you to it, and you cannot easily say later that someone else signed. Non-repudiation is the same idea for digital data.

A digital signature can only be made with a secret key that only the signer has, but anyone can check it with a public key. So if a valid signature exists, it shows that the key holder made it, and a court or any other outsider can check this without the signer's help.

This works only if everyone agrees which person owns which public key, if the secret key was not stolen, and if there is proof of when the signature was made. Laws in many countries then say that such a signature counts like a handwritten one.

## The idea

**What signatures give and MACs do not.** With a MAC, sender and receiver share $K$. A valid tag $\tau$ shows the receiver that the message came from the sender, because only the two of them know $K$. But the receiver could have made $\tau$ too, so a third party cannot tell who made it, and the sender can deny it. With a signature, the verifier has only $pk$, and [existential unforgeability](/existential-unforgeability/) says that nobody without $sk$ can make a valid $\sigma$ on a new message, the receiver included. So a valid $\sigma$ is evidence against the holder of $sk$ that a third party can check. Diffie and Hellman (1976) named this property when they proposed public-key signatures.

**What the mathematics does not give.** The proof that only the key holder can sign leaves several ways to deny a signature:

1. **"That is not my key."** The verifier must know that $pk$ belongs to the signer. In practice a certificate authority binds the key to a name, and the binding is only as good as the authority's checks of identity.
2. **"My key was stolen."** If $sk$ leaked, anyone could have signed. The signer reports the compromise and the authority revokes the certificate, for example with the reason keyCompromise of RFC 5280. A signer could also leak the key on purpose and then claim that a signature was forged, so rules must fix who carries the risk for signatures made before the report.
3. **"I signed it after the key was revoked" or "before the key was valid."** The verifier must know when the signature was made. A time-stamping authority (RFC 3161) signs a hash of the signed data together with the current time. A signature with a timestamp from before the revocation stays valid; one without a timestamp can be denied by a claim that it was made after the key was compromised.
4. **"I did not see that text."** The signing device or software showed the signer something different from what it signed. Rules for qualified signatures require certified devices for this reason.
5. **"The algorithm is broken."** When the hash or the signature scheme is broken, old signatures lose their value as evidence, as happened for certificates with [MD5](/md5/). Archives re-timestamp old documents with stronger algorithms before the old ones fail.

**The law.** In the European Union, the eIDAS Regulation (No 910/2014) defines electronic, advanced and qualified electronic signatures. Article 25 says that an electronic signature may not be denied legal effect only because it is electronic, and that a qualified electronic signature has the same legal effect as a handwritten signature. A qualified signature needs a qualified certificate and a qualified signature creation device. In the United States, the E-SIGN Act of 2000 (15 U.S.C. 7001) says that a signature or contract may not be denied legal effect only because it is electronic; it does not require any particular technology, so a typed name or a click can also be an electronic signature in the legal sense.

**Non-repudiation is sometimes unwanted.** In a private conversation, a transferable proof of who said what can harm the speaker. Off-the-record messaging (Borisov, Goldberg and Brewer 2004) authenticates messages with MACs and publishes the MAC keys afterwards, so that the receiver is convinced but cannot convince anyone else. [Designated verifier signatures](/designated-verifier-signature/), [undeniable signatures](/undeniable-signature/) and [ring signatures](/ring-signature/) limit who can verify or who can be identified.

## Examples

- **A signed contract.** A PDF signed with a qualified certificate and a timestamp from a qualified time-stamping service. Years later, a court can check the signature, the certificate chain, the revocation status at the time in the timestamp, and the strength of the algorithms used.
- **MAC versus signature.** A bank and a customer who share an HMAC key can both make every tag, so a disputed payment order with a valid tag does not show who made it. The same order signed with a key held only in the customer's smart card does.
- **Key compromise.** A signer reports on day 100 that the key leaked. A signature with an RFC 3161 timestamp of day 90 is still evidence; one with no timestamp is not, because the signer can say it was made on day 101 by the thief. [Forward-secure signatures](/forward-secure-signature/) reduce this problem: they change the private key each period, so a key stolen in one period cannot sign for earlier periods.
- **Certificate key usage.** RFC 5280 defines a key usage bit, first called nonRepudiation and later contentCommitment, that marks keys meant to sign content that the signer commits to, as opposed to keys for authentication in a protocol.

## Where it is used

- **Electronic contracts and public administration.** Qualified and advanced electronic signatures under eIDAS, and electronic signatures under E-SIGN and similar laws.
- **Software distribution.** Signed software and updates, where the signature both protects the users and makes the publisher accountable for what it shipped.
- **Payments and trading.** Signed orders and transactions, so that disputes can be settled by evidence that a third party can check.
- **Logs and archives.** Signed and timestamped records, for audits and long-term evidence.
- **Blockchains.** A transaction signed with a key proves that the key holder authorized it, which every node can check without any trusted party.

## References
