---
tag: A130R5
kind: problem
slug: multisignature-problem
name: Multisignature problem
aliases:
- rogue key problem
area: cryptography/signatures
level: advanced
summary: "Many signers with their own keys sign one message, and the result is one short signature, secure even when some signers pick their keys to cancel the honest keys (rogue keys)."
prereqs: [digital-signature, schnorr-signature]
see_also: [musig, bls-signature, aggregate-signature, threshold-signing-problem, forking-lemma, existential-unforgeability, wagners-algorithm, proof-of-knowledge]
sources:
  - paper: "K. Itakura and K. Nakamura, A public-key cryptosystem suitable for digital multisignatures, NEC Research and Development 71, 1983"
    locator: the first proposal of a multisignature, built from RSA, where the signers sign one after another
  - paper: "Silvio Micali, Kazuo Ohta and Leonid Reyzin, Accountable-subgroup multisignatures, ACM CCS 2001"
    locator: the first formal security definition, and a scheme with a key registration step before signing
  - paper: "Alexandra Boldyreva, Threshold signatures, multisignatures and blind signatures based on the gap-Diffie-Hellman-group signature scheme, PKC 2003, LNCS 2567, Springer"
    locator: the BLS based multisignature, proved under the assumption that every signer knows the secret of its key
  - paper: "Mihir Bellare and Gregory Neven, Multi-signatures in the plain public-key model and a general forking lemma, ACM CCS 2006"
    locator: the plain public key model, the name knowledge of secret key (KOSK) for the stronger setting, and a three round Schnorr scheme that needs no key registration
  - paper: "Thomas Ristenpart and Scott Yilek, The power of proofs-of-possession, EUROCRYPT 2007, LNCS 4515, Springer"
    locator: the analysis of proofs of possession, which shows that some proofs fail and that a BLS signature on the key itself, with its own hash function, is a sound proof for BLS multisignatures
  - paper: "Gregory Maxwell, Andrew Poelstra, Yannick Seurin and Pieter Wuille, Simple Schnorr multi-signatures with applications to Bitcoin, Designs, Codes and Cryptography 87(9), 2019, doi:10.1007/s10623-019-00608-x"
    locator: MuSig, the first Schnorr multisignature with key aggregation in the plain public key model
  - paper: "Manu Drijvers, Kasra Edalatnejad, Bryan Ford, Eike Kiltz, Julian Loss, Gregory Neven and Igors Stepanovs, On the security of two-round multi-signatures, IEEE S&P 2019"
    locator: the attacks with Wagner's algorithm on CoSi, the first two-round MuSig and BCJ, the metareduction against their proofs, and the mBCJ fix
  - paper: "Dan Boneh, Manu Drijvers and Gregory Neven, Compact multi-signatures for smaller blockchains, ASIACRYPT 2018, LNCS 11273, Springer"
    locator: BLS multisignatures with key coefficients in the plain public key model, and accountable subgroups
---

The multisignature problem asks how $N$ signers, each with its own independent key pair, can sign the same message $m$ so that the result is one short signature, and how to keep this secure when some signers are dishonest and choose their keys after they see the honest keys. The naive answer, adding the keys and the signatures, fails to a rogue key: a cheater announces a key that cancels the honest ones and then signs alone for the whole group. The problem is to remove this attack with as few rounds of interaction, as little setup and as small an output as possible. It differs from the [threshold signing problem](/threshold-signing-problem/), where one key is shared among the parties.

**Notation.** $G$ is a group of prime order $q$ with generator $g$, written multiplicatively. Signer $i$ has the secret key $x_i$ and the public key $X_i = g^{x_i}$, and $L = \{X_1, \dots, X_N\}$ is the set of keys that sign.

## In plain words

A group of people each have their own signing key. They agree on one document, and they want to give the reader one small signature that shows all of them signed it. The reader should not need a list of separate signatures, and in the best case not even a list of keys, just one combined key.

The hard part is a cheater in the group. If the combined key is just the sum of the keys, a cheater who sees the other keys can pick a key that cancels them all. Then the cheater alone can sign for the whole group. A good solution stops this without trusting a central office to check every key.

## Definition

A multisignature scheme has the algorithms:

- $\mathrm{KeyGen}() \to (x, X)$, run by each signer alone.
- Optional $\mathrm{KeyAgg}(L) \to \tilde{X}$, a short aggregate key that anyone computes from $L$.
- An interactive protocol $\mathrm{Sign}$, run by the signers in $L$ on input $m$, with output $\sigma$.
- $\mathrm{Verify}(L, m, \sigma)$, or $\mathrm{Verify}(\tilde{X}, m, \sigma)$ when keys aggregate.

**Correctness.** If all the signers in $L$ follow the protocol on $m$, then $\mathrm{Verify}$ accepts.

**Security (unforgeability in the plain public key model).** The adversary gets one honest key $X^*$. It may create every other key as it likes, with no proof that it knows the secrets, and it may start any number of signing sessions with the honest signer, concurrently, on any $(L, m)$ that contains $X^*$. It wins if it outputs $(L, m, \sigma)$ that verifies, with $X^* \in L$, such that the honest signer never ran a session on $(L, m)$. The scheme is secure if every efficient adversary wins with negligible probability. This is the definition of Bellare and Neven (2006); it extends [existential unforgeability](/existential-unforgeability/) to many signers.

The **rogue key attack** on the naive scheme shows why the free choice of keys matters. Let $\tilde{X} = \prod_i X_i$ and let the signature be an ordinary [Schnorr signature](/schnorr-signature/) under $\tilde{X}$. After it sees $X_1$, the adversary picks $\beta$ and announces $X_2 = g^\beta X_1^{-1}$. Then $\tilde{X} = X_1 X_2 = g^\beta$, the adversary knows its secret $\beta$, and it signs any message as "both signers" alone.

## Variants

- **Key models.** In the *knowledge of secret key* (KOSK) or *key registration* model, each key is accepted only after its owner proves it knows the secret, and the rogue key attack disappears. With a *proof of possession*, the proof is a signature on the key itself, checked once and stored. In the *plain public key* model there is no such step, and the scheme itself must defeat rogue keys.
- **Key aggregation.** Some schemes give one aggregate key $\tilde{X}$, and the signature verifies as an ordinary signature under it. Others need the full list $L$ to verify.
- **Accountable subgroups** (Micali, Ohta and Reyzin, 2001). Any subset $S$ of a group can sign, and the verifier learns exactly which members signed.
- **Interactive or not.** Pairing-based schemes are non-interactive: each signer sends one signature and anyone combines them. Schnorr-type schemes need rounds of interaction for the joint nonce.
- **Aggregate signatures** allow different messages; see [aggregate signatures](/aggregate-signature/).

## Examples

- **Naive key sum.** Insecure in the plain public key model, by the rogue key attack above. Secure only with registered keys.
- **BLS with proofs of possession.** Each signer publishes $X_i$ and a [BLS signature](/bls-signature/) on $X_i$. Any group then signs $m$ by $\sigma = \prod_i H(m)^{x_i}$ and is checked against $\prod_i X_i$, with two pairings in total.
- **Two signers on Bitcoin.** Two parties of a payment channel lock coins to one Taproot key, the [MuSig](/musig/) aggregate of their two keys. The spend shows one ordinary BIP 340 signature, and no observer can tell that two people signed.

## Known algorithms

| scheme | rounds to sign | key model | aggregate key | assumption |
|---|---|---|---|---|
| Boldyreva BLS (2003) | 1 | KOSK | yes | CDH in pairing groups, ROM |
| BLS with proof of possession (Ristenpart and Yilek, 2007) | 1 | proof of possession | yes | CDH in pairing groups, ROM |
| Bellare and Neven (2006) | 3 | plain | no | discrete logarithm, ROM |
| BDN (Boneh, Drijvers and Neven, 2018), BLS with key coefficients | 1 | plain | yes | CDH in pairing groups, ROM |
| MuSig (Maxwell, Poelstra, Seurin and Wuille, 2019) | 3 | plain | yes | discrete logarithm, ROM |
| MuSig2 (Nick, Ruffing and Seurin, 2021) | 2, the first before the message | plain | yes | one-more discrete logarithm, ROM |

The fix in the plain public key model is the same idea in each Schnorr and BLS scheme with key aggregation: each key gets a coefficient $a_i = H(L, X_i)$ and $\tilde{X} = \prod_i X_i^{a_i}$. A rogue key changes $L$, which changes every coefficient, so the adversary cannot fix $\tilde{X}$ in advance.

## Bounds

- **Size.** With key aggregation the verifier stores one key and one signature of constant size, independent of $N$. Without it, the verifier needs all $N$ keys. With accountable subgroups the verifier needs at least $N$ bits to know the subset.
- **Rounds for Schnorr outputs.** The first two-round schemes (CoSi, the first two-round MuSig, BCJ) were broken by Drijvers et al. (2019) with [Wagner's algorithm](/wagners-algorithm/) on $\ell$ concurrent sessions, and Benhamouda et al. (2021) made the attack polynomial time once $\ell$ exceeds the number of binary digits of $q$. The same paper of Drijvers et al. gave a metareduction: no algebraic reduction can prove those schemes secure under the discrete logarithm or one-more discrete logarithm assumption. Two rounds are possible with two or more nonces per signer, as in MuSig2, or with the mBCJ fix of Drijvers et al.
- **Tightness.** Proofs for Schnorr-type schemes use a [forking lemma](/forking-lemma/) and lose a polynomial factor in $q_H$, the number of hash queries. The MuSig proof forks twice and loses more than a proof with one fork.

## Reductions

- **From threshold signatures.** An $N$-of-$N$ [threshold scheme](/threshold-signature/) with joint key generation gives a multisignature for one fixed group. It does not give one for groups chosen at signing time, which multisignatures allow.
- **To aggregate signatures.** A multisignature is the special case of an aggregate signature in which all messages are equal; BGLS aggregation forbids equal messages, so the equal case needs one of the fixes above.
- **KOSK to plain.** Adding a sound proof of possession to each key turns a KOSK scheme into one secure with keys that the adversary chooses, at the cost of one extra signature per key.

## Applications

- Bitcoin Taproot outputs shared by several parties, signed with MuSig2 (BIP 327), including two-party payment channels.
- Proof of stake consensus, where many validators sign the same block or checkpoint with BLS and proofs of possession.
- Collective signing and witness cosigning of logs and software releases, such as CoSi.
- Certificates for Byzantine fault tolerant replication, where a quorum of replicas signs the same decision.

## References
