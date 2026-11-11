---
tag: YATRJE
kind: problem
slug: blind-signature
name: Blind signature
aliases:
- Blind signing problem
- blind signature problem
- blinded signature
- blind signature scheme
area: cryptography/signatures
level: advanced
summary: A signer signs a message it cannot read, and the signature later cannot be linked to the signing session.
prereqs: [digital-signature, existential-unforgeability]
see_also: [chaum-blind-signature, schnorr-signature, bls-signature, generalized-birthday-problem, rsa-problem, random-oracle-model, group-signature, ring-signature]
sources:
  - paper: doi:10.1007/978-1-4757-0602-4_18
    title: "David Chaum, Blind signatures for untraceable payments, Advances in Cryptology: Proceedings of Crypto 82, Plenum Press, 1983, pages 199 to 203"
    locator: the idea of a blind signature and its use for untraceable payments
  - paper: doi:10.1007/s001450010003
    title: "David Pointcheval and Jacques Stern, Security arguments for digital signatures and blind signatures, Journal of Cryptology 13(3), 2000, pages 361 to 396"
    locator: the definition of one-more forgery and the proof for the Okamoto-Schnorr blind signature with a poly-logarithmic number of sessions
  - paper: doi:10.1007/BFb0052233
    title: "Ari Juels, Michael Luby and Rafail Ostrovsky, Security of blind digital signatures, CRYPTO 1997, LNCS 1294, pages 150 to 164"
    locator: the first formal definitions of blindness and unforgeability, and a construction from any trapdoor permutation
  - paper: doi:10.1007/978-3-030-77870-5_2
    title: "Fabrice Benhamouda, Tancrède Lepoint, Julian Loss, Michele Orrù and Mariana Raykova, On the (in)security of ROS, Eurocrypt 2021, LNCS 12696, pages 33 to 53"
    locator: the polynomial-time ROS algorithm for l > log p and the concurrent attacks on Schnorr and Okamoto-Schnorr blind signatures
  - url: "https://www.rfc-editor.org/rfc/rfc9474"
    title: "Frank Denis, Frederic Jacobs and Christopher A. Wood, RFC 9474, RSA Blind Signatures, October 2023"
    locator: Section 1 (applications) and Section 7 (one-more unforgeability, blindness, malicious keys)
  - url: "https://www.rfc-editor.org/rfc/rfc9578"
    title: "Sofía Celi, Alex Davidson, Steven Valdez and Christopher A. Wood, RFC 9578, Privacy Pass Issuance Protocols, June 2024"
    locator: Section 5 (VOPRF tokens) and Section 6 (blind RSA tokens)
---

A blind signature is an interactive signing protocol in which a user gets a signature on a message of its choice, while the signer learns nothing about the message and cannot later link the signature to the session that produced it. David Chaum proposed it at Crypto 1982 for untraceable electronic cash: a bank signs a coin that the customer blinded, and when the coin is spent the bank sees a valid signature that it cannot connect to the withdrawal. A secure scheme must satisfy two opposite needs. Blindness protects the user from the signer. One-more unforgeability, defined by Pointcheval and Stern (2000), protects the signer from the user: after $\ell$ sessions the user holds at most $\ell$ signatures. The RSA construction is on the page [Chaum's blind signature](/chaum-blind-signature/); this page covers the problem, the security notions and the known schemes.

## In plain words

A bank wants to give you a digital coin worth one euro. The coin is a signed serial number. If the bank sees the serial number when it signs, it can recognise the coin when a shop deposits it, and so it knows where you spent your money.

A blind signature lets the bank sign without seeing the serial number. You hide the number, the bank signs the hidden form, and you take the hiding away. You now hold a normal signed coin. The bank cannot tell which visit made which coin.

The bank still needs one guarantee: each visit gives you exactly one coin, not two. A good scheme gives both guarantees at the same time.

## Definition

**Syntax.** A blind signature scheme has three parts.

- $\text{KeyGen}(1^\lambda) \to (sk, pk)$.
- An interactive protocol $\langle \mathcal{S}(sk), \mathcal{U}(pk, m) \rangle$, in which the signer $\mathcal{S}$ outputs nothing about the message and the user $\mathcal{U}$ outputs a signature $\sigma$ or a failure.
- $\text{Verify}(pk, m, \sigma) \in \{0, 1\}$, which is a normal, non-interactive check.

**Correctness.** If both parties are honest, the user's $\sigma$ satisfies $\text{Verify}(pk, m, \sigma) = 1$.

**Blindness** (Juels, Luby and Ostrovsky 1997). The game runs against a malicious signer $\mathcal{A}$:

1. $\mathcal{A}$ outputs a public key $pk$ (in the strong form it may choose $pk$ maliciously) and two messages $m_0, m_1$.
2. A hidden bit $b$ is drawn. $\mathcal{A}$ runs one session with a user holding $m_b$ and one with a user holding $m_{1-b}$, in any order and interleaving.
3. If both users finish, $\mathcal{A}$ gets $(\sigma_0, \sigma_1)$, the signatures on $m_0$ and $m_1$; if either fails, it gets nothing.
4. $\mathcal{A}$ outputs a guess $b'$. The scheme is blind if $\lvert \Pr[b' = b] - 1/2 \rvert$ is negligible.

**One-more unforgeability** (Pointcheval and Stern 2000). A malicious user $\mathcal{A}$ gets $pk$ and completes at most $\ell$ sessions with the honest signer. It wins if it outputs $\ell + 1$ pairs $(m_i, \sigma_i)$ with distinct messages that all verify. The scheme is secure if every efficient $\mathcal{A}$ wins with negligible probability. This replaces [existential unforgeability](/existential-unforgeability/) (no valid signature on a message that was not queried), which cannot apply because the signer never sees the messages. Two settings differ:

- **Sequential:** each session ends before the next one starts.
- **Concurrent:** the user opens many sessions at once and interleaves their messages. Some schemes are secure in the first setting but not in the second.

## Variants

- **Partially blind signatures** (Abe and Fujisaki, Asiacrypt 1996). Signer and user agree on public information $info$, such as an expiry date or a coin value, that becomes part of the signature; the message stays blind. One key then serves many coin values.
- **Fair blind signatures** (Stadler, Piveteau and Camenisch, Eurocrypt 1995). A trusted judge can remove blindness for one session or one signature, for example under a court order against money laundering.
- **Restrictive blind signatures** (Brands 1993). The user can blind the message only within a structure fixed by the signer, so that an identity stays embedded in the coin; this enables offline cash in which double spending reveals the spender.
- **Selective-failure blindness** (Camenisch, Neven and shelat 2007). Blindness must hold even when the signer makes a session fail on purpose depending on the message.
- **Round-optimal blind signatures.** Two moves: one message from the user and one from the signer. Chaum's RSA scheme and the BLS scheme have this form.
- **Threshold blind signatures.** The signing key is shared among several signers, and a quorum must take part.
- **Blind signatures with attributes.** The signed message holds hidden attributes, about which the user proves statements; this leads to anonymous credentials.

## Examples

**Chaum's RSA scheme.** The user sends $z = H(m) \cdot r^e \bmod n$, the signer returns $z^d$, and the user divides by $r$ to get $H(m)^d$. RFC 9474 (2023) standardises it with PSS encoding. See [Chaum's blind signature](/chaum-blind-signature/).

**Blind Schnorr.** The signer has $X = g^x$ in a group of prime order $p$. In three moves:

1. The signer sends $R = g^k$.
2. The user picks random $\alpha, \beta$, sets $R' = R \cdot g^\alpha \cdot X^\beta$ and $c' = H(R', m)$, and sends $c = c' + \beta$.
3. The signer returns $s = k + c x$. The user sets $s' = s + \alpha$.

Then $g^{s'} = R \cdot g^{\alpha} \cdot X^{c} = R' \cdot X^{c'}$, so $(R', s')$ is a normal [Schnorr signature](/schnorr-signature/) on $m$. The values $(R, c, s)$ that the signer sees are independent of $(R', c', s')$, since $\alpha$ and $\beta$ are uniform.

**Blind BLS.** With a pairing and the [BLS signature](/bls-signature/) $\sigma = H(m)^x$, the user sends $H(m) \cdot g^r$, gets $(H(m) \cdot g^r)^x$, and multiplies by $X^{-r}$ (Boldyreva, PKC 2003).

## Known algorithms

| scheme | moves | assumption | concurrent sessions |
|---|---|---|---|
| Chaum RSA-FDH, RSABSSA | 2 | one-more RSA inversion, random oracle | secure |
| Blind BLS (Boldyreva 2003) | 2 | chosen-target CDH, random oracle | secure |
| Blind Schnorr, Okamoto-Schnorr | 3 | discrete logarithm, random oracle | secure for poly-logarithmically many sessions; broken by the ROS attack for more |
| Juels-Luby-Ostrovsky (1997) | generic | any trapdoor permutation (via secure two-party computation) | feasibility result |
| Fischlin (Crypto 2006) | 2 | signatures, commitments and NIZK with a common reference string | secure |

Lattice-based and other post-quantum blind signatures exist, but they are much larger than the classical ones. The RSA and pairing schemes are the ones used in practice.

## Bounds

**Blindness can be perfect.** In Chaum's scheme for an honest key, and in blind Schnorr, the signer's view is independent of the message even for an unbounded signer.

**Rounds.** Two moves are the minimum for an interactive protocol, and Chaum's scheme, blind BLS and Fischlin's generic scheme reach it.

**The ROS attack.** The ROS problem (Random inhomogeneities in an Overdetermined Solvable system of linear equations, Schnorr 2001) asks, for a random function $H$ into $\mathbb{Z}_p$, for $\ell + 1$ vectors $a_i \in \mathbb{Z}_p^\ell$ and one vector $c$ with $H(a_i) = \langle a_i, c \rangle$ for every $i$. A solution lets a user who opens $\ell$ concurrent blind Schnorr sessions finish them with $\ell + 1$ signatures. Wagner's [generalized birthday](/generalized-birthday-problem/) algorithm (find $k$ list elements whose sum is zero) gave a subexponential attack in 2002. Benhamouda, Lepoint, Loss, Orrù and Raykova (Eurocrypt 2021) solved ROS in polynomial time for $\ell > \log_2 p$, which breaks concurrent blind Schnorr and Okamoto-Schnorr with about 256 sessions in a 256-bit group, and also some threshold, multi-signature and partially blind schemes built the same way. Pointcheval and Stern's proof, which covers only a poly-logarithmic number of sessions, is therefore close to tight.

**Limits of proofs.** Fischlin and Schröder (Eurocrypt 2010) showed that a large class of blind signatures with three or fewer moves cannot be proved one-more unforgeable by black-box reductions to non-interactive assumptions, which is why the efficient schemes rely on one-more assumptions, random oracles or idealised group models.

## Reductions

- **Chaum's scheme and one-more RSA.** One-more unforgeability of the RSA-FDH blind signature in the random oracle model is equivalent to the one-more RSA inversion problem (Bellare, Namprempre, Pointcheval and Semanko 2003): given $q + 1$ random targets and $q$ calls to an $e$-th root oracle, find all $q + 1$ roots. It is not known to follow from the plain [RSA problem](/rsa-problem/).
- **Blind BLS and chosen-target CDH.** Boldyreva reduced blind BLS to the analogous one-more problem in a gap Diffie-Hellman group.
- **Blind Schnorr and ROS.** A concurrent forgery against blind Schnorr gives either a solution to the one-more discrete logarithm problem or a ROS solution (Fuchsbauer, Plouviez and Seurin, Eurocrypt 2020, in the algebraic group model), and a ROS solution gives a forgery; so the security of concurrent blind Schnorr stands or falls with ROS.
- **To oblivious pseudorandom functions.** Hashing a message with its deterministic blind signature gives a verifiable oblivious pseudorandom function in the random oracle model (Jarecki, Kiayias and Krawczyk 2014, cited in RFC 9474).
- **From general primitives.** Any secure signature scheme, a commitment and non-interactive zero-knowledge proofs give a round-optimal blind signature (Fischlin 2006): the user commits to $m$, the signer signs the commitment, and the user outputs a proof that it holds a signed commitment to $m$.

## Applications

- **Electronic cash.** Chaum's payment system (1982), the offline cash of Chaum, Fiat and Naor (1988), and DigiCash's eCash in the 1990s. Recent systems such as GNU Taler use RSA blind signatures for coins.
- **Electronic voting.** Fujioka, Okamoto and Ohta (Auscrypt 1992) let an administrator blindly sign a voter's ballot after checking eligibility, so that the anonymous ballot later carries a valid signature.
- **Privacy Pass.** Anonymous tokens let a client prove that it solved a challenge without being tracked across sites. RFC 9578 (2024) defines a VOPRF token type, which only the issuer can verify, and a blind RSA token type (RSABSSA, RFC 9474), which anyone can verify with the public key.
- **Anonymous access tokens.** Apple's iCloud Private Relay and Google's VPN use RSA blind signatures to authorise a client without linking its traffic to its account (RFC 9474, Section 1).
- **Anonymous credentials.** Blind signatures with attributes are the issuing step of credential systems such as Brands' and Microsoft U-Prove.

## References
