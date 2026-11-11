---
tag: AZY9JE
kind: algorithm
slug: musig
name: MuSig
aliases:
- MuSig2
- Schnorr multisignature
- BIP 327
area: cryptography/signatures
level: advanced
summary: "A Schnorr multisignature with key aggregation: hash-derived key coefficients stop rogue keys, and MuSig2 signs in two rounds. The output is one ordinary BIP 340 signature."
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order, u: the number of signers}
  time: {worst: Θ(u n^3), average: Θ(u n^3), best: Θ(u n^3)}
  space: {extra: Θ(u n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2018
  people: [Gregory Maxwell, Andrew Poelstra, Yannick Seurin, Pieter Wuille, Jonas Nick, Tim Ruffing]
  note: MuSig appeared as a preprint in 2018 and in Designs, Codes and Cryptography in 2019. MuSig2 by Nick, Ruffing and Seurin appeared at Crypto 2021 and is specified for Bitcoin in BIP 327.
prereqs: [schnorr-signature, multisignature-problem]
see_also: [aggregate-signature, threshold-signature, adaptor-signature, forking-lemma, wagners-algorithm, nonce-reuse-attack, bls-signature, batch-verification]
sources:
  - paper: "Gregory Maxwell, Andrew Poelstra, Yannick Seurin and Pieter Wuille, Simple Schnorr multi-signatures with applications to Bitcoin, Designs, Codes and Cryptography 87(9), 2019, doi:10.1007/s10623-019-00608-x"
    locator: key aggregation with the coefficients a_i = H(L, X_i), the three round signing protocol with nonce commitments, and the proof in the plain public key model by double forking
  - paper: "Manu Drijvers, Kasra Edalatnejad, Bryan Ford, Eike Kiltz, Julian Loss, Gregory Neven and Igors Stepanovs, On the security of two-round multi-signatures, IEEE S&P 2019"
    locator: the flaw in the proof of the first two round version of MuSig, the attack by Wagner's algorithm on concurrent sessions, and the metareduction
  - paper: "Fabrice Benhamouda, Tancrede Lepoint, Julian Loss, Michele Orru and Mariana Raykova, On the (in)security of ROS, EUROCRYPT 2021, LNCS 12696, Springer"
    locator: the polynomial time solution of ROS for many concurrent sessions, which breaks two round Schnorr multisignatures with one nonce per signer
  - paper: "Jonas Nick, Tim Ruffing and Yannick Seurin, MuSig2, simple two-round Schnorr multi-signatures, CRYPTO 2021, LNCS 12825, Springer"
    locator: the two round protocol with several nonces per signer combined by the coefficient b, the preprocessing of the first round, and the proofs under the one-more discrete logarithm assumption
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki"
    title: Jonas Nick, Tim Ruffing and Elliott Jin, BIP 327, MuSig2 for BIP340-compatible multi-signatures
    locator: the algorithms KeyAgg, NonceGen, NonceAgg, Sign, PartialSigVerify and PartialSigAgg, and the file vectors/key_agg_vectors.json
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki"
    title: Pieter Wuille, Jonas Nick and Tim Ruffing, BIP 340, Schnorr signatures for secp256k1
    locator: the verification algorithm and x-only public keys, which the MuSig2 output satisfies
  - paper: "Jonas Nick, Tim Ruffing, Yannick Seurin and Pieter Wuille, MuSig-DN, Schnorr multi-signatures with verifiably deterministic nonces, ACM CCS 2020"
    locator: a deterministic nonce variant that proves in zero knowledge that each nonce was derived correctly
---

MuSig lets $u$ signers, each with its own [Schnorr](/schnorr-signature/) key, compute one aggregate public key and then jointly produce one signature under it. The signature and the key look exactly like those of a single signer, so a verifier runs plain BIP 340 verification and learns nothing about how many people signed. MuSig solves the [multisignature problem](/multisignature-problem/) in the plain public key model: keys need no registration or proof of possession, because each key is weighted by a hash of the whole key list, and a rogue key no longer cancels the honest ones. The version in use is MuSig2, with two rounds of signing, specified for Bitcoin in BIP 327.

**Notation.** $G$ is the base point of secp256k1, of prime order $n$, written additively. Signer $i$ has the secret $d_i$ and the public key $P_i = d_i G$, encoded in 33 bytes as $pk_i$. $H_{\mathrm{tag}}$ is the tagged SHA-256 of BIP 340. $x(R)$ is the x coordinate of $R$ in 32 bytes.

## In plain words

First, everyone computes the group key. Each member's key gets a weight that depends on the full list of keys, and the group key is the weighted sum. A cheater cannot pick a key that cancels the others, because changing any key changes every weight.

To sign, each member makes two secret random numbers and publishes the matching points. These can be sent before the message is known. When the message is fixed, everyone mixes the published points into one shared point, with a mixing factor from a hash. Each member then sends one number, its share of the signature. The sum of the shares, together with the shared point, is an ordinary signature for the group key.

## The problem

Given keys $P_1, \dots, P_u$ that the signers chose independently, the goal is a short key $Q$ and a signing protocol whose output is a valid BIP 340 signature under $Q$, such that no adversary that controls all but one signer, chooses its keys after it sees the honest key, and opens many sessions at once, can produce a signature under any $Q$ that includes the honest key on a message the honest signer did not agree to.

## The algorithm

```pseudo id=main
KEY-AGG(pk_1, ..., pk_u)
L1   L ← H_KeyAgg list(pk_1 ‖ … ‖ pk_u);  pk' ← the first pk_j that differs from pk_1
L2   a_i ← 1 if pk_i = pk', else H_KeyAgg coefficient(L ‖ pk_i) mod n
L3   Q ← Σ_i a_i P_i;  return Q

SIGN, round 1, at signer i (may run before m is known)
L4   pick k_{i,1}, k_{i,2} at random;  send R_{i,1} = k_{i,1} G and R_{i,2} = k_{i,2} G
NONCE-AGG
L5   R_1 ← Σ_i R_{i,1};  R_2 ← Σ_i R_{i,2}

SIGN, round 2, at signer i
L6   b ← H_MuSig/noncecoef(R_1 ‖ R_2 ‖ x(Q) ‖ m) mod n;  R ← R_1 + b R_2
L7   e ← H_BIP0340/challenge(x(R) ‖ x(Q) ‖ m) mod n
L8   if R has an odd y then negate k_{i,1}, k_{i,2};  g ← 1 if Q has an even y, else n − 1
L9   s_i ← k_{i,1} + b k_{i,2} + e a_i g d_i mod n;  send s_i, then erase k_{i,1}, k_{i,2}

PARTIAL-SIG-VERIFY(s_i), by any participant
L10  check s_i G = ±(R_{i,1} + b R_{i,2}) + e a_i g P_i, with the sign of L8
PARTIAL-SIG-AGG
L11  s ← Σ_i s_i mod n;  return (x(R), s)
```

**Why two nonces.** With one nonce per signer, the aggregate nonce is a sum that the adversary can steer by choosing its own nonces after it sees the honest ones in many concurrent sessions, and a ROS solution or [Wagner's algorithm](/wagners-algorithm/) then turns those sessions into a forgery. With two nonces and the coefficient $b$, which hashes the message and all nonces, the honest signer's effective nonce $R_{i,1} + b R_{i,2}$ depends on everything the adversary sent, so the adversary cannot plan the sum.

**Parity.** BIP 340 keys and nonces are x-only and stand for the point with an even y. Line L8 negates the nonces when $R$ has an odd y, and $g$ negates the secret when $Q$ has an odd y, so the final $(x(R), s)$ verifies against $x(Q)$.

**The second key.** Line L2 gives the coefficient 1 to the second distinct key. This saves one scalar multiplication and is safe, as BIP 327 explains, because the other coefficients are still unpredictable.

## Example

Two signers with $d_1 = 3$ and $d_2 = 7$ sign the message "hello". Their 33-byte keys start with 02F9308A0192 and 025CBDF0646E (both even y). KeyAgg gives $a_1 = $ 0x83FA25E908C1...7447, and $a_2 = 1$ because $pk_2$ is the second distinct key. The aggregate key is

$x(Q) =$ 3BB7AFBEA0D19B64F2FD95A71D7E850EDC644FF8D8E6FA22BA6605667B81B84D, with an even y, so $g = 1$.

With nonces from the fixed generator `random.Random(1)`, the session gives $b =$ 0xB85DB5A60C11... and $x(R) =$ 141B6864EF06E271AAEDED10A1DDA9C3DEA5CE69E135DF138CAC54F28A34A1B8. This $R$ has an odd y, so both signers negate their nonces at line L8. The partial signatures start with 0x5D700F4A6729 and 0x165DA4A8642B, and the final signature

141B6864...8A34A1B8 73CDB3F2CB558C5B7A80978AE6E36F456AE51C462285829BFE18EC92F3A79B4B

passes BIP 340 verification under $x(Q)$.

The rogue key test: the attacker sees $P_1$, picks $\beta$ and announces $P_2 = \beta G - P_1$. Under the naive sum $P_1 + P_2 = \beta G$, the attacker signs alone. Under KeyAgg, $Q = a_1 P_1 + P_2 = (a_1 - 1) P_1 + \beta G$ with $a_1$ fixed only after $P_2$ is chosen, so the attacker does not know the discrete logarithm of $Q$, and the same forgery fails.

## Correctness

Let $\hat{k}_{i,j}$ be the nonces after line L8 and $\hat{R}$ the point with an even y and x coordinate $x(R)$, so $\hat{R} = \sum_i (\hat{k}_{i,1} + b \hat{k}_{i,2}) G$. Let $\hat{Q} = gQ$, the even-y point with x coordinate $x(Q)$. Then

$$sG = \sum_i \big(\hat{k}_{i,1} + b \hat{k}_{i,2}\big) G + e g \sum_i a_i d_i G = \hat{R} + e \hat{Q},$$

which is the BIP 340 equation with challenge $e = H(x(R) \| x(Q) \| m)$. The full proof, with the check of line L10, is below.

## Complexity

Let $n$ also stand for the number of binary digits of the group order, and $u$ for the number of signers.

- **KeyAgg**: $u$ hashes and $u$ scalar multiplications, $\Theta(u n^3)$ with schoolbook arithmetic. It is done once per key set and can be cached.
- **Signing**: two scalar multiplications for the nonces, about $2u$ point additions for NonceAgg, and one scalar multiplication for $R$. Each signer sends 66 bytes in round 1 and 32 bytes in round 2.
- **Verification**: one BIP 340 verification, the same as for one signer. The output is 64 bytes and the key 32 bytes for any $u$.
- **Space**: $\Theta(u n)$ to hold the keys and nonces of a session.

## Properties

- **Plain public key model.** No registration of keys and no proofs of possession.
- **Key aggregation and privacy.** $Q$ is one point and the signature is one BIP 340 signature, so on chain a MuSig output cannot be told from a single signer output.
- **Security.** MuSig2 is proven secure in the random oracle model under the one-more discrete logarithm assumption with four nonces per signer, and with two nonces when the algebraic group model is also assumed (Nick, Ruffing and Seurin, 2021). BIP 327 uses two nonces.
- **Interactive and $u$-of-$u$.** All signers must take part; there is no threshold. For $t$-of-$n$ see [threshold signatures](/threshold-signature/).
- **Stateful.** Each signer must keep its secret nonces between the rounds and must never use them twice.

## Variants and improvements

- **MuSig (three rounds).** The original protocol adds a first round in which each signer commits to $H(R_i)$ before revealing $R_i$. A first preprint version had two rounds and one nonce, and Drijvers et al. (2019) showed that its proof was wrong and gave a subexponential attack on concurrent sessions; Benhamouda et al. (2021) made the attack polynomial. The published version has three rounds.
- **MuSig2.** Two rounds with $\nu \ge 2$ nonces per signer and the coefficient $b$, as above. The first round needs no message, so with preprocessing, signing proper takes one round.
- **MuSig-DN.** Deterministic nonces with a zero knowledge proof that each nonce was derived correctly, two rounds and stateless signers, at a large cost in proof size and time.
- **DWMS** (Alper and Burdges, 2021) is a two round scheme with a similar idea.
- **Tweaks.** BIP 327 supports plain and x-only tweaks of $Q$, for BIP 32 derivation and Taproot commitments. The code on this page omits them.
- **BLS.** With pairings, [BLS signatures](/bls-signature/) aggregate without interaction; the BDN scheme uses the same key coefficients.

## When to use it

Use MuSig2 when a fixed set of signers, each with its own key, must jointly control funds or a statement, and the result must be an ordinary Schnorr signature: shared Taproot outputs, two-party Lightning channels, and multi-party wallets that should look like single-key wallets. When any $t$ of $n$ must be able to sign, use a threshold scheme such as FROST. When the signers cannot interact, use BLS.

## Pitfalls

- **Nonce reuse.** If a signer signs two different sessions with the same $(k_{i,1}, k_{i,2})$, the values $b$ and $e$ change, and three such equations in $k_{i,1}$, $k_{i,2}$ and $d_i$ reveal the secret key; see [nonce reuse attacks](/nonce-reuse-attack/). Never derive nonces only from the message and the key, since the other signers can change $b$ by changing their nonces.
- **Copying state.** Restoring a signer from a backup or a virtual machine snapshot may reuse nonces.
- **Skipping partial signature checks** makes it impossible to blame the signer who sent a bad share; the final signature just fails.
- **Naive key sums** fall to rogue keys. Coefficients are needed even when keys come from "trusted" parties.
- **Key order.** KeyAgg of a reordered list gives a different $Q$, as the official vectors show, so all signers must agree on one order, for example sorted keys.

## Implementations

The Python code on this page implements BIP 327 KeyAgg without tweaks, which reproduces the official key aggregation vectors, and NonceAgg, Sign, PartialSigVerify and PartialSigAgg for 2 and 3 signers on secp256k1, with an independent BIP 340 verifier for the result. The nonce generation is simplified: it draws random nonces instead of running the hashed NonceGen of BIP 327, so the BIP 327 signing vectors are not reproduced. A test shows the rogue key attack on the naive key sum. The code is for study only, is not constant time, and does not erase secrets.

## History

Multisignatures go back to Itakura and Nakamura (1983), and the plain public key model with three round Schnorr signing to Bellare and Neven (2006), whose scheme had no key aggregation. Maxwell, Poelstra, Seurin and Wuille posted MuSig in January 2018, with key aggregation for Bitcoin. Drijvers et al. found the gap in its two round proof in 2018 and published at IEEE S&P 2019; the journal version of MuSig (2019) uses three rounds. Nick, Ruffing and Seurin presented MuSig2 at Crypto 2021, and BIP 327 later specified it for BIP 340 keys. Taproot (BIP 341), active on Bitcoin since November 2021, made such aggregate keys usable as ordinary outputs.

## References
