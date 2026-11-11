---
tag: TMD2FZ
kind: definition
slug: non-malleability
name: Non-malleability
aliases:
- NM-CPA
- NM-CCA
area: cryptography/public-key
level: research
summary: An encryption scheme is non-malleable if, given a ciphertext, no efficient adversary can make other ciphertexts whose plaintexts are related to the hidden one. NM-CCA2 equals IND-CCA2.
prereqs: [ind-cca-security]
see_also: [ind-cpa-security, chosen-ciphertext-attack, elgamal-encryption, homomorphic-encryption, naor-yung-paradigm, cramer-shoup-cryptosystem, commitment-scheme, zero-knowledge-proof]
sources:
  - paper: "Danny Dolev, Cynthia Dwork and Moni Naor, Non-malleable cryptography, STOC 1991, pages 542 to 552"
    locator: the first definition of non-malleability and the first non-malleable encryption scheme
  - paper: "Danny Dolev, Cynthia Dwork and Moni Naor, Nonmalleable cryptography, SIAM Journal on Computing 30(2), pages 391 to 437, 2000"
    locator: the journal version with the simulation-based definition
  - paper: "Mihir Bellare, Anand Desai, David Pointcheval and Phillip Rogaway, Relations among notions of security for public-key encryption schemes, CRYPTO 1998, LNCS 1462, pages 26 to 45"
    locator: the comparison-based definition NM-ATK, the implications and separations, and NM-CCA2 = IND-CCA2
  - paper: "Mihir Bellare and Amit Sahai, Non-malleable encryption, equivalence between two notions, and an indistinguishability-based characterization, CRYPTO 1999, LNCS 1666, pages 519 to 536"
    locator: the equivalence of the simulation and comparison definitions, and the characterization by parallel chosen-ciphertext attack
  - paper: "Rafael Pass, abhi shelat and Vinod Vaikuntanathan, Construction of a non-malleable encryption scheme from any semantically secure one, CRYPTO 2006, LNCS 4117, pages 271 to 289"
    locator: NM-CPA encryption from any IND-CPA encryption
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.7.3, Definition 8.60 and Fact 8.61
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 5, the section on non-malleable encryption schemes
---

An encryption scheme is non-malleable if an adversary that sees a ciphertext $y$ of an unknown message $x$ cannot make new ciphertexts whose plaintexts are related to $x$ in a meaningful way, with better success than if it had not seen $y$ at all. Dolev, Dwork and Naor introduced the notion in 1991, motivated by sealed-bid auctions: a bidder who sees an encrypted bid must not be able to submit an encryption of that bid plus one. Non-malleability under chosen-plaintext attack (NM-CPA) is strictly stronger than [IND-CPA](/ind-cpa-security/), and under adaptive chosen-ciphertext attack it is equivalent to [IND-CCA2](/ind-cca-security/). [ElGamal](/elgamal-encryption/) is the standard example of a scheme that is IND-CPA but malleable.

**Notation.** $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ is a public-key scheme and $\lambda$ the security parameter. $\mathcal{A} = (\mathcal{A}_1, \mathcal{A}_2)$ is a two-stage adversary that runs in time $t$. ATK is one of CPA, CCA1 and CCA2, with oracles $O_1$ and $O_2$ as in the [IND-CCA game](/ind-cca-security/): none for CPA, $O_1 = \mathrm{Dec}(sk, \cdot)$ for CCA1, and both for CCA2, where $O_2$ refuses the challenge $y$. A relation $R$ is a predicate computable in time polynomial in $\lambda$. Bold $\mathbf{y}$ denotes a vector of ciphertexts and $\mathbf{x}$ the vector of their plaintexts. All statements are in the standard model.

## Definition

**Comparison-based definition (Bellare, Desai, Pointcheval and Rogaway, 1998).** Run the experiment twice, once "real" and once "random".

1. $(pk, sk) \leftarrow \mathrm{Gen}(1^\lambda)$.
2. $(M, s) \leftarrow \mathcal{A}_1^{O_1}(pk)$, where $M$ is a distribution on messages of one length that can be sampled in polynomial time, and $s$ is a state.
3. $x, \tilde{x} \leftarrow M$, independently. $y \leftarrow \mathrm{Enc}(pk, x)$.
4. $(R, \mathbf{y}) \leftarrow \mathcal{A}_2^{O_2}(M, s, y)$, where $y$ is not an entry of $\mathbf{y}$.
5. $\mathbf{x} = \mathrm{Dec}(sk, \mathbf{y})$, entry by entry.

The real experiment succeeds if $R(x, \mathbf{x})$ holds; the random one if $R(\tilde{x}, \mathbf{x})$ holds. The advantage is

$$\mathrm{Adv}^{\mathrm{nm\text{-}atk}}_\Pi(\mathcal{A}) = \Pr[R(x, \mathbf{x})] - \Pr[R(\tilde{x}, \mathbf{x})],$$

and $\Pi$ is **NM-ATK secure** if it is negligible in $\lambda$ for every adversary that runs in polynomial time. In the random run, $\mathbf{x}$ is computed from $y$, which carries no information about $\tilde{x}$; so the random run measures what the adversary can achieve without the ciphertext.

**Simulation-based definition (Dolev, Dwork and Naor).** For every adversary $\mathcal{A}$ there is a simulator $\mathcal{S}$ that, without seeing $y$, outputs $\mathbf{x}'$ such that $R(x, \mathbf{x}')$ holds with nearly the same probability as $R(x, \mathbf{x})$ for $\mathcal{A}$. Bellare and Sahai (1999) proved that the two definitions are equivalent, and that NM-ATK is equivalent to indistinguishability against an adversary that may make one parallel batch of decryption queries after the challenge.

The rule that $y$ is not in $\mathbf{y}$ excludes copying. Without it the adversary would output $y$ and the relation "equal", and no scheme would qualify.

### NM-CPA implies IND-CPA

**Theorem 1 (Dolev, Dwork and Naor; Bellare, Desai, Pointcheval and Rogaway).** For every IND-CPA adversary $\mathcal{B}$ there is an NM-CPA adversary $\mathcal{A}$, running in the time of $\mathcal{B}$ plus one encryption, with $\mathrm{Adv}^{\mathrm{nm\text{-}cpa}}(\mathcal{A}) = \tfrac{1}{2}\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}(\mathcal{B})$, up to the negligible chance that a fresh encryption equals $y$.

*Proof.* Let $\mathcal{B}$ choose $m_0, m_1$ and guess with advantage $\varepsilon$; assume without loss that $\Pr[\mathcal{B}$ guesses right$] = \tfrac12 + \tfrac{\varepsilon}{2}$. $\mathcal{A}_1$ runs $\mathcal{B}$ up to the choice of $m_0, m_1$ and outputs $M$, the uniform distribution on $\{m_0, m_1\}$. $\mathcal{A}_2$ runs $\mathcal{B}$ on $y$ to get a guess $b'$, outputs a fresh encryption of $m_{b'}$ (encrypting again if it equals $y$), and the relation $R(a, b) = [a = b]$. In the real run $x = m_\beta$ for a uniform $\beta$ and $y$ encrypts it, so $R(x, m_{b'})$ holds with probability $\tfrac12 + \tfrac{\varepsilon}{2}$. In the random run $\tilde{x}$ is independent of everything $\mathcal{B}$ sees, so $R(\tilde{x}, m_{b'})$ holds with probability $\tfrac12$. $\square$

### The converse fails

**Theorem 2.** If DDH holds in a group $G$ of prime order $q$, ElGamal in $G$ is IND-CPA secure but not NM-CPA secure.

*Proof.* IND-CPA is proved on the [ElGamal](/elgamal-encryption/) page. For NM-CPA, let $\mathcal{A}_1$ output $M$ uniform on $G$ and let $\mathcal{A}_2$, given $y = (c_1, c_2)$, output $\mathbf{y} = ((c_1, g c_2))$ and $R(a, b) = [b = g a]$. The new ciphertext differs from $y$ and decrypts to $g x$, so the real run always succeeds. In the random run $R(\tilde{x}, g x)$ holds only if $\tilde{x} = x$, with probability $1/q$. The advantage is $1 - 1/q$. $\square$

The same argument works for every scheme with a public homomorphism: [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) (flip the bit), [Paillier](/paillier-cryptosystem/) (add one), and [homomorphic encryption](/homomorphic-encryption/) in general, which is malleable by design.

### The BDPR hierarchy

Bellare, Desai, Pointcheval and Rogaway (1998) related the six notions IND-ATK and NM-ATK for ATK in CPA, CCA1 and CCA2.

- NM-ATK implies IND-ATK for each ATK, and both notions get stronger from CPA to CCA1 to CCA2.
- **NM-CCA2 is equivalent to IND-CCA2.** An IND-CCA2 adversary can decrypt the related ciphertexts that a mauling adversary makes, since they differ from the challenge, and test the relation itself.
- IND-CPA does not imply NM-CPA, and IND-CCA1 does not imply NM-CCA1.
- NM-CPA does not imply IND-CCA1, and IND-CCA1 does not imply NM-CPA.

The separations assume that some secure scheme of the stronger kind exists, and modify it.

## Examples and non-examples

- **Non-malleable, NM-CCA2.** Every IND-CCA2 scheme: [Cramer-Shoup](/cramer-shoup-cryptosystem/), [RSA-OAEP](/rsa-oaep/), [ECIES](/ecies/), schemes from the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/), and the [Naor-Yung](/naor-yung-paradigm/) construction with simulation-sound proofs.
- **NM-CPA from any IND-CPA scheme.** Pass, shelat and Vaikuntanathan (2006) built NM-CPA encryption from any IND-CPA scheme, without random oracles.
- **Malleable.** ElGamal, Goldwasser-Micali, Paillier, textbook [RSA](/rsa-cryptosystem/) ($c \cdot 2^e$ encrypts $2m$), and stream ciphers or CTR mode in the symmetric world (flip a ciphertext bit to flip a plaintext bit). The [one-time pad](/one-time-pad/) has [perfect secrecy](/perfect-secrecy/) and is still malleable, which shows that secrecy and non-malleability are different goals.
- **The auction.** Bids are sent as ElGamal encryptions of $g^{\text{bid}}$ (exponential ElGamal). A cheater who sees $(c_1, c_2)$ for an unknown bid $v$ sends $(c_1, g c_2)$, an encryption of $v + 1$, and wins by one unit without knowing $v$. A non-malleable scheme, or a proof of knowledge of the plaintext attached to each bid, prevents this.

The Python code next to this page runs the experiment against ElGamal with the adversary of Theorem 2, and it turns an IND-CPA guesser into an NM-CPA adversary as in Theorem 1. It is for study only and not constant time.

## Related definitions

- **[IND-CPA](/ind-cpa-security/) and [IND-CCA](/ind-cca-security/).** The indistinguishability notions; NM-CCA2 equals IND-CCA2.
- **Plaintext awareness.** The adversary cannot make a valid ciphertext without knowing its plaintext; with IND-CPA it gives IND-CCA2 in the [random oracle model](/random-oracle-model/), and so non-malleability.
- **Replayable CCA.** Allows changes that keep the plaintext, and forbids all others; see [IND-CCA](/ind-cca-security/).
- **Non-malleable commitments.** The same idea for a [commitment scheme](/commitment-scheme/): seeing a commitment must not help to commit to a related value. Also from Dolev, Dwork and Naor.
- **Non-malleable codes.** Dziembowski, Pietrzak and Wichs (2010): an encoding such that tampering with a codeword gives the original message or an unrelated one.
- **[Homomorphic encryption](/homomorphic-encryption/).** The opposite goal: controlled malleability as a feature.

## References
