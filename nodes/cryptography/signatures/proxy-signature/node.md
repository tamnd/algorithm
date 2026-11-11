---
tag: HJZ5RV
kind: algorithm
slug: proxy-signature
name: Proxy signature
aliases:
- delegated signature
- proxy signature with warrant
area: cryptography/signatures
level: research
summary: An original signer delegates signing rights to a proxy who signs on its behalf.
model: word-ram
complexity:
  vars: {k: the length of the modulus p in machine words}
  time: {worst: Θ(k^3), average: Θ(k^3), best: Θ(k^3)}
  space: {extra: Θ(k)}
properties: {deterministic: false, randomized: true}
history:
  year: 1996
  people: [Masahiro Mambo, Keisuke Usuda, Eiji Okamoto]
  note: Mambo, Usuda and Okamoto defined proxy signatures at ACM CCS 1996, with full delegation, partial delegation and delegation by warrant. Boldyreva, Palacio and Warinschi gave the first formal model in 2003.
prereqs: [schnorr-signature, digital-signature]
see_also: [threshold-signature, group-signature, ring-signature, designated-verifier-signature, blind-signature, forking-lemma, random-oracle-model, discrete-logarithm-problem]
sources:
  - paper: "Masahiro Mambo, Keisuke Usuda and Eiji Okamoto, Proxy signatures for delegating signing operation, Proceedings of the 3rd ACM Conference on Computer and Communications Security (CCS 1996), pages 48 to 57"
    title: "Masahiro Mambo, Keisuke Usuda and Eiji Okamoto, Proxy signatures for delegating signing operation, ACM CCS 1996"
    locator: the three kinds of delegation (full, partial, by warrant) and the proxy-protected and proxy-unprotected forms of partial delegation
  - paper: doi:10.1007/BFb0028478
    title: "Seungjoo Kim, Sangjoon Park and Dongho Won, Proxy signatures, revisited, ICICS 1997, LNCS 1334, pages 223 to 232"
    locator: partial delegation with warrant, where the proxy key comes from a Schnorr signature on the warrant
  - paper: doi:10.1007/s00145-010-9082-x
    title: "Alexandra Boldyreva, Adriana Palacio and Bogdan Warinschi, Secure proxy signature schemes for delegation of signing rights, Journal of Cryptology 25(1), 2012, pages 57 to 115 (Cryptology ePrint Archive 2003/096)"
    locator: the security model for proxy signatures, the analysis of delegation by certificate and of the KPW scheme, and the Triple Schnorr scheme with its proof in the random oracle model
---

A proxy signature lets an original signer A delegate its signing right to a proxy B, so that B can sign messages on A's behalf while A is away. A verifier sees that the message was signed by B on behalf of A, and checks this with A's public key alone, or with A's and B's public keys. In delegation by warrant, A signs a warrant: a statement that names B, the kinds of messages B may sign and the period of the delegation. Mambo, Usuda and Okamoto introduced proxy signatures at ACM CCS 1996. The scheme here is the Schnorr form of Kim, Park and Won (1997): A's signature on the warrant becomes part of B's proxy secret key.

## In plain words

A manager going on holiday writes a note: "Bob may sign purchase orders for me until Friday", and signs it. Bob mixes the signed note with his own secret key to make a special proxy key. With it he signs purchase orders, and each one carries the note. A supplier checks the note first: is it from the manager, does it name Bob, does it cover this order, has it expired? Then the supplier checks the signature with a public key it can compute from the manager's key, the note and Bob's key. The manager alone cannot make Bob's signatures, and Bob cannot use the note for anything it does not cover.

## The problem

Given an original signer A with key pair $(x_a, y_a = g^{x_a})$ and a proxy B with $(x_b, y_b = g^{x_b})$, and a warrant $w$ that A agrees to, let B sign messages $m$ so that:

- **verifiability:** a verifier with $y_a$ is convinced that A agreed to the delegation and that B signed $m$;
- **strong unforgeability:** nobody except B, not even A, can make a proxy signature;
- **identifiability and undeniability:** the proxy signature shows that B, not A, signed, and B cannot deny it later;
- **restriction:** B can sign only messages that the warrant allows.

Delegation can also be **full** (A gives B its secret key, which allows nothing of the above) or **partial without warrant** (B gets a proxy key but nothing limits what it signs).

## The algorithm

$H_1$ and $H_2$ are hash functions into $\mathbb{Z}_q$ with separate domains. A checks the warrant $w$ before it signs; it contains $y_a$, $y_b$, a scope and an expiry time.

```pseudo id=main
DELEGATE(x_a, w)                                        ▷ run by A
L1  k ← random in Z_q*; K ← g^k
L2  s_w ← x_a · H_1(w, K) + k mod q; send (w, K, s_w) to B privately

PROXY-KEY(x_b, (w, K, s_w))                             ▷ run by B
L3  check g^{s_w} = y_a^{H_1(w, K)} · K
L4  x_p ← s_w + x_b mod q

PROXY-SIGN(x_p, (w, K), m, t)
L5  require w allows m at time t
L6  r ← random in Z_q*; R ← g^r
L7  return (w, K, R, z = r + H_2(w, K, R, m) · x_p mod q)

VERIFY(y_a, m, (w, K, R, z), t)
L8  require w names y_a and allows m at time t
L9  y_p ← y_a^{H_1(w, K)} · K · y_b;  e ← H_2(w, K, R, m)
L10 return g^z = R · y_p^e
```

Lines L1 and L2 are a Schnorr-type signature on the warrant, and lines L6 and L7 are a Schnorr signature under the proxy key pair $(x_p, y_p)$. Since $g^{s_w} = y_a^{H_1(w,K)} K$, the verifier can compute $y_p = g^{x_p}$ from public values.

## Example

Toy group $p = 2039$, $q = 1019$, $g = 4$. A has $x_a = 5$, $y_a = 1024$, and B has $x_b = 17$, $y_b = 1458$. The warrant lets B sign messages that start with "buy:" until time 100. A delegates with $k = 33$, and B signs "buy: 3 pens" at time 10 with $r = 77$.

| line | computation | result |
|---|---|---|
| L1 | $K = 4^{33}$ | $1301$ |
| L2 | $H_1(w, K) = 323$; $s_w = 5 \cdot 323 + 33 \bmod 1019$ | $629$ |
| L4 | $x_p = 629 + 17$ | $646$ |
| L7 | $R = 4^{77} = 360$; $e = H_2(w, K, R, m) = 475$; $z = 77 + 475 \cdot 646 \bmod 1019$ | $208$ |
| L9 | $y_p = 1024^{323} \cdot 1301 \cdot 1458$ | $271 = 4^{646}$ |

The verifier checks that "buy: 3 pens" starts with "buy:" and that $10 \le 100$, then that $4^{208} = 360 \cdot 271^{475}$. The message "sell the house" is rejected at line L8, whatever the signature.

## Correctness

Line L2 gives $g^{s_w} = y_a^{H_1(w,K)} g^k$, so B's check at line L3 passes, and $g^{x_p} = g^{s_w} g^{x_b} = y_p$. The proxy signature is then an ordinary Schnorr signature for the key pair $(x_p, y_p)$, which the verifier accepts. Line L8 uses only public data, so a message outside the warrant is rejected even if B skips its own check at line L5; and a changed warrant changes $H_1$ and $H_2$, so the old signature fails. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Delegation costs one exponentiation; B's check costs two. Proxy signing costs one exponentiation, and verification three (with $y_a^{H_1(w,K)} K y_b$ computed once per warrant, two). With schoolbook arithmetic modulo $p$ of $k$ words each exponentiation costs $\Theta(k^3)$. A proxy signature carries the warrant, $K$, and the two values $R$ and $z$.

## Properties

- **Proxy-protected.** The proxy key contains $x_b$, so A cannot sign for B. In the proxy-unprotected form ($x_p = s_w$) both can sign and the verifier cannot tell which did.
- **Identifiable.** The warrant and $y_p$ name B, so a proxy signature shows who signed for A.
- **Restricted by the warrant.** The verifier enforces the scope and the period; the cryptography binds the warrant to the signature.
- **No interaction at verification.** The verifier needs only public keys and the warrant.
- **No built-in revocation.** A proxy key stays valid until the warrant expires.

## Variants and improvements

- **Delegation by certificate.** A signs the warrant with its ordinary signature, and B attaches that certificate to an ordinary signature by B on $(w, m)$. Boldyreva, Palacio and Warinschi showed that this simple scheme is secure when the signing of warrants and of messages are kept apart, and that it is the generic solution.
- **Triple Schnorr** (Boldyreva, Palacio and Warinschi). A modification of the KPW scheme with separate hash functions for ordinary signing, delegation and proxy signing, proved secure in the random oracle model under the discrete logarithm assumption. It has shorter proxy signatures than delegation by certificate.
- **Threshold proxy signatures.** Any $t$ of $n$ proxies must work together, combining proxy signatures with [threshold signatures](/threshold-signature/) (signatures that need $t$ of $n$ key holders).
- **Proxy multi-signatures and multi-proxy signatures.** Several original signers delegate to one proxy, or one signer delegates to a group.
- **Anonymous proxy signatures.** The proxy is hidden among the possible proxies, as in a [group signature](/group-signature/) (anyone in a group can sign, and a manager can find the signer).
- **Proxy re-signatures.** A different notion (Blaze, Bleumer and Strauss, Eurocrypt 1998): a proxy converts A's signature into B's signature on the same message.

## When to use it

Use a proxy signature when a principal must hand limited signing power to another party for some time: a manager to a deputy, a user to a mobile agent that buys goods on remote hosts, a node in a grid to a job that runs elsewhere. Mobile agents were a main motivation in early 2000s papers. In practice, most systems do this with delegation by certificate: X.509 proxy certificates (RFC 3820) in grid computing, and certificate chains with name constraints. Choose the KPW-style scheme only when short signatures and one combined key matter.

## Pitfalls

- **Unlimited delegation.** If the warrant does not limit the messages and the period, or the verifier does not check them, the proxy can sign anything for ever. Several early schemes did not put the warrant into the proxy signing step at all.
- **Hash reuse.** If the delegation $s_w$ uses the same hash function and format as A's ordinary Schnorr signatures, a delegation is also an ordinary signature of A on $w$, and an ordinary signature can be turned into a delegation. Keep the domains apart.
- **Secure channel.** Send $s_w$ to B privately unless the scheme is proved secure without this. Lee, Cheon and Kim (CT-RSA 2003) studied which proxy schemes stay secure when the delegation is sent in the clear.
- **Name the proxy.** The warrant must contain $y_b$; otherwise the delegation is not bound to one proxy.

## Implementations

The Python code is for study only: it is not constant time, and its group ($p = 2039$, $q = 1019$) has no security. It implements partial delegation with warrant in the Schnorr form of Kim, Park and Won, with separate hash domains for delegation and proxy signing. It is close to Triple Schnorr but is not claimed to be identical to it. There are no standard test vectors. The tests check that B signs within the warrant, that messages outside the scope or after expiry fail even if B skips its own check, that a widened warrant fails, and that neither A alone nor B's ordinary key can make a proxy signature.

## History

Neuman (ICDCS 1993) described delegation by warrant for distributed systems. Mambo, Usuda and Okamoto (CCS 1996) named proxy signatures and introduced partial delegation, in which the proxy gets a new key derived from the original signer's key. Kim, Park and Won (ICICS 1997) combined partial delegation with a warrant. Many schemes and attacks followed, until Boldyreva, Palacio and Warinschi gave a formal model and the first provably secure schemes in 2003 (journal version 2012).

## References
