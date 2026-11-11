---
tag: M0PBSY
kind: problem
slug: public-key-encryption
name: Public-key encryption
aliases:
- asymmetric encryption
area: cryptography/public-key
level: intro
summary: "Encrypt to a public key so that only the holder of the private key can read the message. The problem is the syntax (Gen, Enc, Dec) plus a security notion, and the notion is the hard part."
model: word-ram
prereqs: [public-key-cryptography, semantic-security]
see_also: [ind-cpa-security, ind-cca-security, non-malleability, probabilistic-encryption, trapdoor-one-way-function, key-encapsulation-mechanism, hybrid-encryption]
sources:
  - url: "https://doi.org/10.1016/0022-0000(84)90070-9"
    title: Shafi Goldwasser and Silvio Micali, Probabilistic encryption, Journal of Computer and System Sciences 28(2), pages 270 to 299, 1984
    locator: Sections 1 and 5 (the definition of semantic security, the proof that encryption must be randomized, and the first scheme that meets the definition)
  - paper: doi:10.1007/BFb0055718
    title: Mihir Bellare, Anand Desai, David Pointcheval and Phillip Rogaway, Relations among notions of security for public-key encryption schemes, Advances in Cryptology, CRYPTO 1998, LNCS 1462, pages 26 to 45, 1998
    locator: Sections 2 and 3 and the figure of implications (the six notions IND-CPA, IND-CCA1, IND-CCA2, NM-CPA, NM-CCA1, NM-CCA2, with every implication and every separation)
  - paper: doi:10.1007/3-540-46766-1_35
    title: Charles Rackoff and Daniel R. Simon, Non-interactive zero-knowledge proof of knowledge and chosen ciphertext attack, Advances in Cryptology, CRYPTO 1991, LNCS 576, pages 433 to 444, 1992
    locator: Section 1 (the adaptive chosen ciphertext notion that is now called IND-CCA2)
  - paper: doi:10.1137/S0097539702403773
    title: Ronald Cramer and Victor Shoup, Design and analysis of practical public-key encryption schemes secure against adaptive chosen ciphertext attack, SIAM Journal on Computing 33(1), pages 167 to 226, 2003
    locator: Sections 1 and 6 (the scheme, and the hybrid KEM and DEM framework for public-key encryption of long messages)
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 5 (the syntax of an encryption scheme, semantic security, indistinguishability, and the equivalence of the two)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2021
    locator: the public-key encryption chapter (the definitions, the hybrid encryption theorem, and the construction of a CPA secure scheme from a trapdoor permutation)
---

Public-key encryption is the problem of sending a secret message to a party you have never met, using only a key that party has published. The *syntax* is three algorithms, key generation, encryption and decryption, and it is easy to state. The content of the problem is the *security notion*: what an adversary may do, and what it must not learn. Goldwasser and Micali settled the first question in 1984 with semantic security, and the strongest standard notion today is indistinguishability under adaptive chosen ciphertext attack, [IND-CCA2](/ind-cca-security/). The page [public-key cryptography](/public-key-cryptography/) covers the setting and its history; this page is the problem statement and the map of the notions.

**Notation.** $1^k$ is the security parameter in unary, $pk$ and $sk$ the public and private keys, $\mathcal{M}$ the message space, $m$ a message, $c$ a ciphertext, and $\mathrm{negl}(k)$ a function smaller than $1/k^t$ for every $t$ and all large $k$. All adversaries are probabilistic algorithms whose running time is polynomial in $k$.

## In plain words

You publish a key. Anybody may use it to lock a message for you, and only you can unlock it. That is the whole requirement, and writing it down exactly took eight years after the idea appeared.

The reason is that "cannot read the message" is too weak. An adversary that learns the first half of the message, or learns that two ciphertexts carry the same message, or can change a ciphertext into the encryption of a related message, has broken the system in practice even if it never recovers a plaintext in full. The right requirement is that a ciphertext is useless: anything the adversary can compute with it, it could compute without it, knowing only how long the message is.

Two consequences follow at once. Encryption must use fresh random coins, and the number of messages must be large.

## Definition

A **public-key encryption scheme** is a triple of algorithms $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$:

- $\mathrm{Gen}(1^k) \to (pk, sk)$ is randomized and outputs a key pair.
- $\mathrm{Enc}(pk, m) \to c$ is randomized and defined for every $m$ in the message space $\mathcal{M}_{pk}$.
- $\mathrm{Dec}(sk, c) \to m$ or $\bot$ is usually deterministic.

All three run in time polynomial in $k$ and in the length of their input.

**Correctness.** For every $k$, every $(pk, sk)$ in the support of $\mathrm{Gen}(1^k)$ and every $m \in \mathcal{M}_{pk}$,

$$\Pr\left[\mathrm{Dec}(sk, \mathrm{Enc}(pk, m)) = m\right] = 1 ,$$

the probability being over the coins of $\mathrm{Enc}$. A scheme with a failure probability $\mathrm{negl}(k)$ instead of 0 is *almost all correct*; lattice schemes such as [ML-KEM](/crystals-kyber/) are of this kind, and a decryption failure that the adversary can trigger is itself an attack.

**Security: indistinguishability.** For an adversary $\mathcal{A}$ define the experiment $\mathrm{Exp}^{\mathrm{ind}\text{-}\mathrm{atk}}_{\Pi, \mathcal{A}}(k)$:

1. $(pk, sk) \leftarrow \mathrm{Gen}(1^k)$; give $pk$ to $\mathcal{A}$.
2. $\mathcal{A}$ outputs two messages $m_0, m_1$ of equal length, with access to the oracles that $\mathrm{atk}$ allows.
3. Draw $\beta \leftarrow \{0,1\}$ and give $\mathcal{A}$ the *challenge* $c^* = \mathrm{Enc}(pk, m_\beta)$.
4. $\mathcal{A}$ outputs a guess $\beta'$, again with the oracles that $\mathrm{atk}$ allows.

The *advantage* is $\mathrm{Adv}(\mathcal{A}) = \left| 2\Pr[\beta' = \beta] - 1 \right|$, and $\Pi$ is **IND-ATK secure** when every polynomial time $\mathcal{A}$ has advantage $\mathrm{negl}(k)$. The three attack models are

| $\mathrm{atk}$ | oracles before the challenge | oracles after the challenge | name |
|---|---|---|---|
| CPA | none beyond $pk$ | none | [IND-CPA](/ind-cpa-security/) |
| CCA1 | $\mathrm{Dec}(sk, \cdot)$ | none | lunchtime attack |
| CCA2 | $\mathrm{Dec}(sk, \cdot)$ | $\mathrm{Dec}(sk, \cdot)$ on every $c \ne c^*$ | [IND-CCA2](/ind-cca-security/) |

A chosen plaintext oracle is not listed because $pk$ is public: the adversary encrypts whatever it likes by itself. This is the structural difference from the symmetric setting and the reason encryption must be randomized.

**Security: semantic security.** $\Pi$ is semantically secure when for every polynomial time $\mathcal{A}$ there is a polynomial time $\mathcal{S}$ such that for every message distribution and every function $f$ of the message, $\mathcal{A}$ given $\mathrm{Enc}(pk, m)$ and $\mathcal{S}$ given only $|m|$ compute $f(m)$ with probabilities that differ by $\mathrm{negl}(k)$. Goldwasser and Micali proved that this is equivalent to IND-CPA, which is why every proof in practice uses the indistinguishability form; see [semantic security](/semantic-security/).

**Security: non-malleability.** NM-ATK asks that no adversary, given $c^*$, can output a ciphertext whose plaintext is related to $m_\beta$ by a relation of its choice. See [non-malleability](/non-malleability/).

## Variants

- **By attack model.** CPA, CCA1 and CCA2 as in the table above. CCA2 is the notion to target; it is what a scheme needs when an attacker can submit ciphertexts and observe any reaction, which is the normal situation in a protocol. The [padding oracle attack](/padding-oracle-attack/) is the practical form of a decryption oracle.
- **By goal.** Indistinguishability (IND), non-malleability (NM), and the older one-wayness (OW), which asks only that a random message cannot be recovered in full. OW is far too weak: textbook [RSA](/rsa-cryptosystem/) is one way under the [RSA assumption](/rsa-problem/) and leaks the whole message when the message space is small.
- **Key encapsulation.** Instead of encrypting a chosen message, $\mathrm{Encaps}(pk)$ returns a ciphertext and a uniform key. This is the form all current standards use; see [key encapsulation mechanism](/key-encapsulation-mechanism/) and [hybrid encryption](/hybrid-encryption/).
- **Multi-user and multi-challenge.** The adversary sees many public keys or many challenges. The notions are equivalent to the single challenge ones up to a loss factor equal to the number of challenges, and that factor matters for concrete parameters.
- **Deterministic and searchable encryption.** Deterministic schemes cannot be IND-CPA, so they use weaker definitions that assume the message has high entropy. They exist because an encrypted database has to be searchable.
- **Extra structure.** [Homomorphic encryption](/homomorphic-encryption/) allows computation on ciphertexts, which contradicts non-malleability by design, so the target there is IND-CPA. [Identity based encryption](/identity-based-encryption/) replaces the public key by a name. [Functional encryption](/functional-encryption/) reveals a function of the plaintext to the holder of a function key.

## Examples

**A scheme that fails every notion.** Textbook RSA: $\mathrm{Enc}((N,e), m) = m^e \bmod N$. The same message gives the same ciphertext, so an adversary that outputs $m_0 = 0$ and $m_1 = 1$ wins with advantage 1 after one encryption of its own. It is also malleable: $c \cdot r^e$ decrypts to $m r$, which is the basis of [RSA blinding](/rsa-blinding/) when the owner does it on purpose and of a forgery when an attacker does.

**A scheme that meets IND-CPA and nothing more.** [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) encrypts one binary digit as a random square or a random non-square with [Jacobi symbol](/jacobi-symbol/) 1. It is IND-CPA under the [quadratic residuosity assumption](/quadratic-residuosity-problem/), and it is homomorphic for the exclusive or, hence malleable. [ElGamal](/elgamal-encryption/) is the practical member of this class, IND-CPA under [DDH](/decisional-diffie-hellman/).

**Schemes that meet IND-CCA2.** [Cramer-Shoup](/cramer-shoup-cryptosystem/) under DDH with no random oracle. [RSA-OAEP](/rsa-oaep/) under the RSA assumption in the [random oracle model](/random-oracle-model/). [ML-KEM](/crystals-kyber/) under module learning with errors, through the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/).

**A scheme that is provably as hard as factoring and still insecure.** [Rabin](/rabin-cryptosystem/). Inverting it is equivalent to factoring, and the proof of that equivalence is a chosen ciphertext attack that recovers the private key in two queries. The example shows that the hardness of the underlying problem and the security of the scheme are different statements.

## Known algorithms

The schemes that solve the problem, with the assumption and the best notion each reaches.

| scheme | assumption | notion | note |
|---|---|---|---|
| [RSA-OAEP](/rsa-oaep/) | [RSA problem](/rsa-problem/) | IND-CCA2 in the [ROM](/random-oracle-model/) | the standard for RSA encryption |
| [PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/) | RSA problem | none, broken by [Bleichenbacher](/padding-oracle-attack/) | kept only for compatibility |
| [Rabin](/rabin-cryptosystem/) | factoring | one way only | the reduction is the attack |
| [ElGamal](/elgamal-encryption/) | [DDH](/decisional-diffie-hellman/) | IND-CPA | multiplicatively homomorphic |
| [Cramer-Shoup](/cramer-shoup-cryptosystem/) | DDH | IND-CCA2, no ROM | the first practical one |
| [ECIES](/ecies/) | CDH on a curve | IND-CCA2 in the ROM | a KEM and DEM hybrid |
| [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) | [QR](/quadratic-residuosity-problem/) | IND-CPA | one digit per ciphertext |
| [Paillier](/paillier-cryptosystem/) | [DCR](/decisional-composite-residuosity/) | IND-CPA | additively homomorphic |
| [ML-KEM](/crystals-kyber/) | module LWE | IND-CCA2 | the post-quantum standard |
| [McEliece](/mceliece-cryptosystem/) | decoding a Goppa code | IND-CCA2 with a transform | large keys, long record |
| [Merkle-Hellman](/merkle-hellman-knapsack-cryptosystem/) | subset sum with a trapdoor | broken | the warning example |

Two generic constructions matter more than any single scheme. From any trapdoor permutation and a [hard core predicate](/hard-core-predicate/) one gets an IND-CPA scheme, which is the theory answer. From any IND-CPA scheme in the random oracle model the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) gives an IND-CCA2 KEM, which is the practical answer and is used by every post-quantum standard.

## Bounds

**What is necessary.** Public-key encryption implies one way functions, so it cannot exist if $\mathrm{P} = \mathrm{NP}$. It is strictly stronger than symmetric encryption as far as anybody can prove: Impagliazzo and Rudich showed that no black box construction gets a key agreement protocol from a one way function alone.

**What is impossible.** A deterministic scheme cannot be IND-CPA, since the adversary encrypts $m_0$ itself. A scheme whose ciphertext is shorter than the message cannot be IND-CPA for the same counting reason that applies to compression. Perfect secrecy in the sense of Shannon is impossible, because $pk$ determines $sk$ and an unbounded adversary finds it; see [perfect secrecy](/perfect-secrecy/).

**The relations among the notions.** The implications and separations of Bellare, Desai, Pointcheval and Rogaway (1998) are the complete picture. An arrow is an implication, and a crossed arrow is a separation, meaning a scheme that meets the first notion and not the second.

```text
    NM-CPA  --------->  NM-CCA1  <---------  NM-CCA2
       |                   |                   ||
       |                   |                   ||  equivalent
       v                   v                   vv
    IND-CPA  <---------  IND-CCA1  <--------  IND-CCA2

  the vertical arrows:   NM-ATK  ==>  IND-ATK   for each of the three ATK
  the horizontal arrows: CCA2 ==> CCA1 ==> CPA  for each of the two goals
  the double arrow:      NM-CCA2 <==> IND-CCA2

  separations (no arrow exists in that direction):
    IND-CPA  =/=>  NM-CPA          IND-CCA1 =/=>  NM-CPA
    NM-CPA   =/=>  IND-CCA1        NM-CCA1  =/=>  IND-CCA2
    IND-CCA1 =/=>  IND-CCA2        NM-CPA   =/=>  NM-CCA1
```

The two facts to remember: non-malleability is strictly stronger than indistinguishability in the CPA and CCA1 models, and the two collapse into one notion at CCA2. That collapse is why IND-CCA2 is *the* target, and why a scheme that reaches it needs nothing further for standard use.

**Concrete bounds.** The best attack on every scheme in the table above is to solve its assumption, so the key sizes come from the cost of the best algorithm for that problem. At 128 bit security, factoring and discrete logarithms modulo a prime need 3072 binary digit keys, an elliptic curve needs 256, and ML-KEM-768 needs about 1184 octets of public key. See the key size table in [post-quantum cryptography](/post-quantum-cryptography/).

## Reductions

**To and from other problems.**

- **From a trapdoor permutation.** Given a family $\{f_{pk}\}$ of trapdoor permutations and a hard core predicate $b$, the scheme $\mathrm{Enc}(pk, m) = (f_{pk}(r), b(r) \oplus m)$ encrypts one binary digit and is IND-CPA. Repeating it with the Blum-Micali chain gives many digits. This reduces public-key encryption to [trapdoor one way functions](/trapdoor-one-way-function/), and it is how the existence question is settled in theory, though no scheme in use is built this way.
- **To key encapsulation and back.** A KEM plus an [authenticated](/authenticated-encryption/) symmetric cipher gives a public-key encryption scheme for messages of any length, and the composition is IND-CCA2 when both parts are; this is the KEM and DEM theorem of Cramer and Shoup. In the other direction, encrypting a random key with an IND-CCA2 scheme gives a KEM. So the two problems are equivalent, and the KEM form is preferred because its security proof does not depend on the message distribution.
- **To the hardness assumption.** Every security proof is a reduction from the scheme to its assumption: an adversary with advantage $\epsilon$ against the scheme gives an algorithm with success probability about $\epsilon/q$ for the assumption, where $q$ counts the oracle queries. The loss factor is what "tight" means and it decides the parameters.
- **From semantic security to indistinguishability.** The two definitions are equivalent, with a simulator built from the adversary. Goldreich gives the proof in both directions.

## Applications

Public-key encryption is almost never used on data directly. It is used to move a key.

- **[TLS](/tls-handshake/)**, where a KEM or a [key exchange](/diffie-hellman/) establishes the session key that a symmetric cipher then uses. TLS 1.3 removed RSA key transport entirely and kept only the exchange, because every deployed version of PKCS #1 v1.5 key transport had suffered a [Bleichenbacher attack](/padding-oracle-attack/).
- **Encrypted mail and files**, where the message key is encrypted once per recipient. This is the one place where the message is encrypted to many public keys, and it is the original use case of the hybrid construction.
- **Key wrapping and escrow**, where a long term public key protects a stored symmetric key.
- **Secure messaging**, where encapsulation to a published key gives the first message of a session before any interaction, as in the sealed sender and prekey designs.
- **Voting, auctions and private aggregation**, where the homomorphic property of [Paillier](/paillier-cryptosystem/) or [ElGamal](/elgamal-encryption/) is the point and IND-CPA is the right notion.
- **Post-quantum migration**, where a [KEM](/key-encapsulation-mechanism/) is combined with a classical exchange so that both must break before the session does.

## References
