---
tag: VY28AZ
kind: technique
slug: batch-verification
name: Batch verification of signatures
aliases:
- batch signature verification
- small exponents test
area: cryptography/signatures
level: advanced
summary: "Check many signatures with one random linear combination of their equations and one multi-exponentiation. A bad batch passes with probability at most 2^-l for l-bit weights."
prereqs: [schnorr-signature, modular-exponentiation]
see_also: [ed25519, bls-signature, aggregate-signature, signature-forgery, existential-unforgeability, elliptic-curve-cryptography]
sources:
  - paper: "David Naccache, David M'Raïhi, Serge Vaudenay and Dan Raphaeli, Can D.S.A. be improved? Complexity trade-offs with the digital signature standard, EUROCRYPT 1994, LNCS 950, Springer, pages 77 to 85"
    locator: the first proposal to verify several DSA-type signatures together
  - paper: doi:10.1007/BFb0054130
    title: Mihir Bellare, Juan A. Garay and Tal Rabin, Fast batch verification for modular exponentiation and digital signatures, EUROCRYPT 1998, LNCS 1403, pages 236 to 250
    locator: the random subset test, the small exponents test with error 2^-l, and the bucket test, with their proofs
  - paper: doi:10.1007/s13389-012-0027-1
    title: Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe and Bo-Yin Yang, High-speed high-security signatures, Journal of Cryptographic Engineering 2(2), 2012, pages 77 to 89
    locator: the section on batch verification of Ed25519 with random 128-bit weights and the Bos-Coster multi-scalar multiplication
  - paper: "Konstantinos Chalkias, Francois Garillot and Valeria Nikolaenko, Taming the many EdDSAs, Security Standardisation Research (SSR) 2020, LNCS 12529, Springer, 2020"
    locator: the cases where batch and single verification of Ed25519 disagree, and the rules that make them agree
  - url: "https://zips.z.cash/zip-0215"
    title: Henry de Valence, ZIP 215, Explicitly Defining and Modifying Ed25519 Validation Rules, 2020
    locator: the cofactored single and batch equations that accept the same set of signatures
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki"
    title: Pieter Wuille, Jonas Nick and Tim Ruffing, BIP 340, Schnorr Signatures for secp256k1, 2020
    locator: section Batch Verification, the weighted equation with a1 = 1 and random a2 to au
  - paper: "Nicholas Pippenger, On the evaluation of powers and monomials, SIAM Journal on Computing 9(2), 1980, pages 230 to 250"
    locator: the bucket method for a product of many powers, the basis of fast multi-scalar multiplication
---

Batch verification checks $N$ signatures faster than $N$ separate verifications. For schemes whose verification is a group equation, such as [Schnorr](/schnorr-signature/), [Ed25519](/ed25519/) and [BLS](/bls-signature/), the verifier raises each equation to a random weight, multiplies them all together, and checks the single result with one multi-exponentiation, whose cost grows much more slowly than $N$ separate exponentiations. Bellare, Garay and Rabin (1998) proved that with weights of $l$ binary digits a batch that holds a bad signature passes with probability at most $2^{-l}$. If the batch fails, the verifier falls back to checking the signatures one by one, or by halves, to find the bad ones.

**Notation.** $G$ is a cyclic group of prime order $q$ with generator $g$. A Schnorr signature $(R_i, s_i)$ on $m_i$ under the key $y_i$ is valid if $g^{s_i} = R_i \, y_i^{e_i}$ with $e_i = H(R_i \| y_i \| m_i)$. $N$ is the batch size and $l$ the length of the random weights $z_i$, with $2^l \le q$.

## In plain words

Checking a signature costs about one big computation. With thousands of signatures, for example all the transactions of a block, the cost adds up. The idea is to check them all at once. Multiply all the checks together and test the product once.

A plain product is not safe: two wrong signatures with errors that cancel each other give a correct product. The fix is to give each signature a secret random weight before the multiplication. An error then survives unless the weights happen to cancel it, and with long random weights that happens almost never.

The product of many powers costs much less than the powers one by one, which is the source of the speed.

## When it applies

- **The verification is a group equation** $\prod_j a_j^{c_j} = 1$, whose terms are group elements and exponents computable from the signature. Schnorr, EdDSA, BIP 340 and BLS (with pairings) fit. ECDSA does not fit directly, because its check compares the $x$ coordinate of a point with $r$, and a signature carries only $r$ and not the full point.
- **The group has prime order, or the equation is made to live in the prime order subgroup.** The error bound uses that every nonzero exponent mod $q$ is invertible. Elements of small order outside the subgroup break it, as in Ed25519.
- **Many signatures are checked at the same time and a bad batch is rare**, so the fallback cost is paid seldom: blocks of a blockchain, certificate chains, logs, and consensus messages.

## The template

```pseudo id=main
BATCH-VERIFY((y_i, m_i, (R_i, s_i)) for i = 1..N, l)
L1  for i = 1..N: if R_i ∉ G or y_i ∉ G or s_i ∉ [0, q − 1] then return false
L2  for i = 1..N: e_i ← H(R_i ‖ y_i ‖ m_i) mod q
L3  for i = 1..N: z_i ← uniform in [0, 2^l − 1]        ▷ secret, fresh for each batch
L4  S ← Σ z_i · s_i mod q
L5  return g^S = Π R_i^{z_i} · y_i^{z_i e_i mod q}      ▷ one multi-exponentiation
```

**Why it is sound (the small exponents test).** Every element of $G$ is a power of $g$, so for each $i$ let $\Delta_i = s_i - \log_g R_i - e_i \log_g y_i \bmod q$. Signature $i$ is valid if and only if $\Delta_i = 0$. Line L5 holds if and only if $\sum_i z_i \Delta_i \equiv 0 \pmod q$. If some $\Delta_j \ne 0$, fix all the other weights. Then $z_j \Delta_j$ must equal one fixed value mod $q$, so $z_j$ must be one fixed residue mod $q$, because $\Delta_j$ is invertible. Since $z_j$ is uniform in $[0, 2^l - 1]$ and $2^l \le q$, at most one of its $2^l$ values hits that residue. So a bad batch passes with probability at most $2^{-l}$, over the choice of the weights, whatever the adversary did. The weights must be unknown to the adversary when it picks the signatures. Line L1 matters: the argument needs $R_i$ and $y_i$ in $G$.

BIP 340 fixes $z_1 = 1$, which saves one multiplication and keeps the bound. The weights can be 128 binary digits long for a $2^{-128}$ error, half the size of a full exponent, which makes the multi-exponentiation cheaper.

**Multi-exponentiation.** Line L5 is a product of $2N + 1$ powers. Straus's method (Shamir's trick) shares one sequence of squarings among all the bases. The Bos-Coster method repeatedly replaces the two largest exponents $a \ge b$ of bases $P$, $Q$ by $a - b$ and $b$ of $P$ and $P + Q$, using $aP + bQ = (a - b)P + b(P + Q)$; Bernstein et al. used it for Ed25519 batches. Pippenger's bucket method sorts the digits of the exponents into buckets and costs about $N b / \log N$ group operations for $N$ exponents of $b$ binary digits, which is the method of choice for large batches. Either way, the cost per signature falls well below that of one verification.

## Classic examples

**Ed25519.** For signatures $(R_i, S_i)$ on $M_i$ under $A_i$, with $k_i = \mathrm{SHA\text{-}512}(R_i \| A_i \| M_i)$ and random 128-binary-digit $z_i$, the batch equation of Bernstein et al. (2011) is

$$[8]\Big(\big[-\textstyle\sum_i z_i S_i \bmod L\big] B + \sum_i [z_i] R_i + \sum_i [z_i k_i \bmod L] A_i\Big) = O.$$

The multiplication by 8 matters. The curve has cofactor 8, so $R_i$ and $A_i$ can have a small order part, and the error bound above fails for it. A single verifier that uses the cofactorless check $[S]B = R + [k]A$ rejects some signatures that the batch accepts, because a small order error vanishes in the random combination with probability at least $1/8$ (when 8 divides its weight) even without the factor 8, and always with it. Chalkias, Garillot and Nikolaenko (2020) showed that libraries disagree here; ZIP 215 makes single and batch verification agree by using the cofactored equation for both.

**BIP 340.** The batch equation is $(s_1 + a_2 s_2 + \dots + a_u s_u) G = R_1 + a_2 R_2 + \dots + a_u R_u + e_1 P_1 + (a_2 e_2) P_2 + \dots + (a_u e_u) P_u$, with the weights $a_i$ from a CSPRNG seeded with all the inputs. Even $y$ coordinates make $R_i$ and $P_i$ unique from their $x$ coordinates, so the batch accepts exactly when all the single checks accept, except with negligible probability.

**A toy batch and the naive attack.** In the code, 10 toy Schnorr signatures pass both the weighted test and the plain product without weights. Then signature 2 gets $s_2 + 99$ and signature 7 gets $s_7 - 99$. Both are now invalid, and the plain product still holds, because the errors cancel in $\sum s_i$. The weighted test rejects, except in the rare case $z_2 \equiv z_7 \pmod q$. With one bad signature and weights of only 4 binary digits, the weighted test accepts in about 1 run in 16, which is the bound $2^{-l}$. The toy group has order 1019 and offers no security.

## Variations

- **The random subset test** of Bellare, Garay and Rabin keeps each equation with probability 1/2 and multiplies them; one round has error 1/2, so it needs $l$ rounds for $2^{-l}$.
- **The bucket test** sorts the equations into random buckets and runs the small exponents test on the bucket products, which is cheaper when $l$ is large.
- **Pairing based batches.** For BLS signatures, a batch of $N$ signatures on distinct messages is checked with random weights and $N + 1$ pairings instead of $2N$. Aggregate signatures go further and compress the signatures themselves; see [aggregate signatures](/aggregate-signature/).
- **Finding the bad signatures.** When a batch fails, split it in halves and test again (binary search), which finds $b$ bad ones out of $N$ with about $2b \log_2 N$ batch tests.
- **Screening.** Bellare, Garay and Rabin also define screening, a weaker test that only says the messages were signed at some point, which is what some uses need.

## Pitfalls

- **No weights or predictable weights.** A batch without random weights, or with weights the adversary can predict, accepts invalid signatures whose errors cancel, as the code shows. Derive the weights from a secret random source or from a hash of all the inputs.
- **Weights longer than the group allows.** The bound $2^{-l}$ needs $2^l \le q$. In a group of composite order, or with elements outside the prime order subgroup, an error of small order cancels with probability about one over that order.
- **Disagreement with single verification.** A system that verifies some signatures alone and others in batches must use rules under which both accept the same set, or nodes split. For Ed25519 this means the cofactored single equation.
- **Skipping the range and membership checks of line L1.** They are part of the proof.
- **Hiding which signature failed.** Batch verification only says that some signature is bad. Report and retry by halves, and do not treat a failed batch as proof that all its signatures are bad.

## Exercises

1. Show that the plain product without weights accepts any batch where the errors $\Delta_i$ sum to 0 mod $q$, and build such a batch with three invalid signatures.
2. Prove that the random subset test, with each $z_i$ in $\{0, 1\}$, accepts a batch with a bad signature with probability at most $1/2$.
3. Let the group have order $8q$ and let one $R_i$ have a component of order 2. Show that the weighted test without the factor 8 accepts with probability about $1/2$, and that the cofactored test accepts it whenever the single cofactored check does.

The code on this page is for study only and is not constant time.

## References
