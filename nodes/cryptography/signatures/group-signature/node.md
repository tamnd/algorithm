---
tag: 852SRK
kind: algorithm
slug: group-signature
name: Group signature
aliases:
- Chaum-van Heyst group signature
- anonymous group signature
area: cryptography/signatures
level: research
summary: Group members sign anonymously, and a manager can open a signature to reveal the signer.
model: word-ram
complexity:
  vars: {n: the number of group members, k: the length of the modulus p in machine words}
  time: {worst: Θ(n k^3), average: Θ(n k^3), best: Θ(n k^3)}
  space: {extra: Θ(n k)}
properties: {deterministic: false, randomized: true}
history:
  year: 1991
  people: [David Chaum, Eugène van Heyst]
  note: Chaum and van Heyst introduced group signatures at Eurocrypt 1991. Bellare, Micciancio and Warinschi gave the standard model of anonymity and traceability at Eurocrypt 2003.
prereqs: [digital-signature, elgamal-encryption, sigma-protocol]
see_also: [ring-signature, blind-signature, proxy-signature, threshold-signature, bilinear-pairing, bls-signature, zero-knowledge-proof, fiat-shamir-heuristic]
sources:
  - paper: doi:10.1007/3-540-46416-6_22
    title: "David Chaum and Eugène van Heyst, Group signatures, Eurocrypt 1991, LNCS 547, pages 257 to 265"
    locator: the definition of group signatures with a group manager who can reveal the signer, and the first four schemes
  - paper: doi:10.1007/3-540-39200-9_38
    title: "Mihir Bellare, Daniele Micciancio and Bogdan Warinschi, Foundations of group signatures, formal definitions, simplified requirements, and a construction based on general assumptions, Eurocrypt 2003, LNCS 2656, pages 614 to 629"
    locator: full anonymity and full traceability, and a generic construction from encryption, signatures and NIZK proofs
  - paper: doi:10.1007/978-3-540-28628-8_3
    title: "Dan Boneh, Xavier Boyen and Hovav Shacham, Short group signatures, Crypto 2004, LNCS 3152, pages 41 to 55"
    locator: a group signature of a few hundred bytes from bilinear pairings under the strong Diffie-Hellman and decision linear assumptions
  - paper: doi:10.1145/1030083.1030103
    title: "Ernie Brickell, Jan Camenisch and Liqun Chen, Direct anonymous attestation, ACM CCS 2004, pages 132 to 145"
    locator: DAA for the Trusted Platform Module, a group-signature-like scheme without an opener and with linkability chosen by the verifier
  - paper: doi:10.1145/1314333.1314337
    title: "Ernie Brickell and Jiangtao Li, Enhanced privacy ID, a direct anonymous attestation scheme with enhanced revocation capabilities, WPES 2007"
    locator: EPID, with revocation by private key and by signature without an opener
---

A group signature lets any member of a group sign on behalf of the group. A verifier checks the signature with one group public key and learns that some member signed, but not which one. A designated authority, the opener (in early papers the group manager), holds a secret key with which it can open any signature and reveal the signer, and can prove that it opened correctly. Chaum and van Heyst introduced group signatures at Eurocrypt 1991, for example for a printer shared by the employees of a company, where the printer must check that a job comes from an employee but the company may later need to find who printed what. Unlike a [ring signature](/ring-signature/) (anonymous signing among any chosen public keys, with nobody able to find the signer), a group signature needs setup and gives someone the power to remove the anonymity.

## In plain words

Every member has a secret key. To sign, a member puts its own name into a sealed envelope that only the opener can open, and adds a proof. The proof says: "the name in the envelope belongs to a member, and I am that member", without showing which name it is.

Anyone can check the proof, so anyone knows that a real member signed. Nobody but the opener can look in the envelope. If there is a dispute, the opener opens it, reads the name, and gives a proof that it read it correctly, so it cannot blame an innocent member.

## The problem

A group signature scheme has a group public key, a secret signing key per member and an opening key. It must give:

- **correctness:** a member's signature verifies with the group public key, and opening it finds that member;
- **anonymity:** without the opening key, nobody can tell which member signed (in the strong form, even with the keys of all members and the power to open other signatures);
- **traceability:** every valid signature opens to a member who signed, even if members collude;
- **non-frameability:** nobody, not even the opener or the issuer, can make a signature that opens to an honest member.

Bellare, Micciancio and Warinschi (2003) showed that, for static groups, full anonymity and full traceability imply the many earlier informal requirements (unlinkability, exculpability, coalition resistance).

## The algorithm

The code implements a simple construction, labelled as a toy: a group signature of linear size, whose group public key is the list of member keys $L = (y_0, \ldots, y_{n-1})$, $y_j = g^{x_j}$, and the opener's ElGamal key $Y = g^{x_o}$. It is not BMW, BBS or any standard scheme, but it has the three parts that all of them share: an encryption of the signer's identity to the opener, a zero-knowledge proof that the encryption holds a member's identity that the signer owns, and a provable opening.

```pseudo id=main
SIGN(i, x_i, L, Y, m)
L1  ρ ← random; C_1 ← g^ρ; C_2 ← y_i · Y^ρ             ▷ ElGamal encryption of y_i to the opener
L2  for j ≠ i: c_j, u_j, v_j ← random; T_j ← (g^{u_j} y_j^{c_j}, g^{v_j} C_1^{c_j}, Y^{v_j} (C_2/y_j)^{c_j})
L3  a, b ← random; T_i ← (g^a, g^b, Y^b)
L4  c ← H(L, Y, m, C_1, C_2, T_0, …, T_{n−1}); c_i ← c − Σ_{j≠i} c_j mod q
L5  u_i ← a − c_i · x_i mod q; v_i ← b − c_i · ρ mod q
L6  return σ = (C_1, C_2, (c_j, u_j, v_j) for all j)

VERIFY(L, Y, m, σ)
L7  recompute every T_j from (c_j, u_j, v_j) as in line L2
L8  return Σ_j c_j ≡ H(L, Y, m, C_1, C_2, T_0, …, T_{n−1})

OPEN(x_o, σ)
L9  y ← C_2 / C_1^{x_o}; i ← the index of y in L
L10 w ← random; A ← g^w; B ← C_1^w; e ← H(Y, C_1, C_2, y, A, B); return (i, A, B, z = w + e · x_o)
```

Lines L2 to L5 are a [sigma protocol](/sigma-protocol/) (a three-move proof: commit, challenge, respond) OR proof, made non-interactive with the Fiat-Shamir hash: branch $j$ proves knowledge of $x_j$ and $\rho$ with $y_j = g^{x_j}$, $C_1 = g^\rho$ and $C_2 / y_j = Y^\rho$. The signer answers its own branch and simulates the others. A judge accepts the opening if $g^z = A \cdot Y^e$ and $C_1^z = B \cdot (C_2 / y_i)^e$, a Chaum-Pedersen proof that $\log_g Y = \log_{C_1}(C_2 / y_i)$.

## Example

Toy group $p = 2039$, $q = 1019$, $g = 4$. Three members have $x = (5, 17, 101)$, so $L = (1024, 1458, 534)$, and the opener has $x_o = 33$, $Y = 1301$. Member 1 signs with $\rho = 10$: $C_1 = 4^{10} = 530$ and $C_2 = 1458 \cdot 1301^{10} = 463$. The OR proof adds three triples $(c_j, u_j, v_j)$, so the signature has $3 \cdot 3 + 2 = 11$ numbers. The pair $(530, 463)$ looks the same for all three members to anyone without $x_o$. The opener computes $530^{33} = 480$ and $463 / 480 = 1458 = y_1$, so member 1 signed, and adds a Chaum-Pedersen proof of this decryption.

## Correctness

In the signer's own branch, line L5 makes $g^{u_i} y_i^{c_i} = g^a$, $g^{v_i} C_1^{c_i} = g^b$ and $Y^{v_i} (C_2/y_i)^{c_i} = Y^b$, the commitments of line L3; the other branches are recomputed exactly; so the verifier hashes the same values, and the $c_j$ add up to the hash. Opening gives $C_2 / C_1^{x_o} = y_i Y^\rho / g^{\rho x_o} = y_i$, and the Chaum-Pedersen proof verifies. An opener that names the wrong member would need $C_2 / y' = C_1^{x_o}$, which fails, so by special soundness it cannot answer two hash values. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

In the toy scheme, signing and verifying each take about $5n$ exponentiations, so $\Theta(n k^3)$ time with schoolbook arithmetic modulo $p$ of $k$ words, and the signature has $3n + 2$ numbers. This is why it is only a toy. Practical schemes are of constant size: in BBS a signature is three elements of a 170-bit pairing group and six elements of $\mathbb{Z}_p$, 1533 bits in the parameters of the paper, and signing needs no knowledge of the other members.

## Properties

- **Toy scheme, static group.** The member list is fixed in the public key; adding a member changes the key.
- **Non-frameable.** Members make their own keys, so the opener cannot sign for them.
- **CPA anonymity only.** ElGamal hides the identity from those who cannot ask for openings; full anonymity in the BMW sense needs CCA-secure encryption.
- **Provable opening.** The opener's claim is checked by anyone.
- **Linkable only by the opener.** Two signatures by one member cannot be linked without $x_o$.

## Variants and improvements

- **Constant size with certificates.** Camenisch and Stadler (Crypto 1997) and Ateniese, Camenisch, Joye and Tsudik (Crypto 2000, strong RSA) gave members a certificate from an issuer and let them prove knowledge of a certificate, so that signatures do not grow with the group.
- **BMW (Eurocrypt 2003).** Formal definitions, and a generic construction from a signature scheme, a CCA-secure encryption and simulation-sound NIZK proofs. Bellare, Shi and Zhang (CT-RSA 2005) extended the model to dynamic groups with separate issuer and opener.
- **BBS short group signatures (Crypto 2004).** A pairing-based scheme with signatures of about 200 bytes, under the strong Diffie-Hellman and decision linear assumptions, in the random oracle model. It is the base of many later schemes.
- **Verifier-local revocation** (Boneh and Shacham, CCS 2004). Revocation lists go only to verifiers, and members need no updates.
- **Direct anonymous attestation** (Brickell, Camenisch and Chen, CCS 2004). A scheme for the Trusted Platform Module without an opener: the verifier can choose a base under which signatures of one TPM are linkable. TPM 1.2 used the RSA-based scheme; TPM 2.0 supports elliptic-curve DAA based on pairings.
- **Enhanced Privacy ID** (Brickell and Li, WPES 2007). An Intel scheme with revocation of a leaked private key and of a key known only through one of its signatures, without an opener. Intel SGX remote attestation used its pairing-based version, and ISO/IEC 20008-2 lists it.
- **Lattice-based group signatures.** Gordon, Katz and Vaikuntanathan (Asiacrypt 2010) gave the first, with linear size; later schemes reduced the size to logarithmic in the group.

## When to use it

Use a group signature when members must stay anonymous towards verifiers, but an authority must be able to identify a misbehaving member: anonymous attestation of devices, vehicle-to-vehicle messages, anonymous access to a service, and privacy-preserving electronic tolls. If no one should be able to find the signer, use a ring signature. If anonymity is wanted towards everyone and there is no fixed group, look at anonymous credentials. Use the toy scheme of this page only to learn the structure.

## Pitfalls

- **Trust in the opener.** The opener can remove the anonymity of everyone; split the role (threshold opening) or limit it by policy, and require provable openings.
- **Issuer framing.** If the issuer makes the members' keys, it can sign as them; members must make their own secret keys and join through a protocol.
- **Revocation.** Static schemes cannot remove a member without a new group key; plan revocation (verifier-local, accumulators or EPID-style lists) from the start.
- **CPA versus CCA anonymity.** A scheme with ElGamal and no CCA protection can lose anonymity if the attacker can see openings of related signatures.
- **Tagged or linkable variants.** DAA and EPID trade some anonymity for linkability per verifier; check what the deployed setting links.

## Implementations

The Python code is a simple construction, clearly a toy: it is not BMW, BBS, DAA or EPID, its signatures grow linearly with the group, and it gives only CPA anonymity. It is for study only: it is not constant time, and its group ($p = 2039$, $q = 1019$) has no security. There are no standard test vectors for it. The tests check that every member of a five-member group can sign, that opening finds the signer and the judge accepts, that the judge rejects the four false openings, that a changed ciphertext breaks the proof, and that neither outsiders nor the opener can sign.

## History

Chaum and van Heyst introduced group signatures at Eurocrypt 1991, with schemes whose size grew with the group. Camenisch and Stadler (1997) and Ateniese, Camenisch, Joye and Tsudik (2000) made them practical with constant size. Bellare, Micciancio and Warinschi gave the formal model in 2003, and Boneh, Boyen and Shacham made them short with pairings in 2004. In the same year Brickell, Camenisch and Chen designed direct anonymous attestation for the TPM. Brickell and Li proposed EPID in 2007, and Intel later used it in its chips. ISO/IEC 20008 (2013) standardizes anonymous digital signatures, including group signature mechanisms.

## References
