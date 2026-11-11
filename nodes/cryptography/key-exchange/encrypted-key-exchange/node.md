---
tag: MY9FM0
kind: algorithm
slug: encrypted-key-exchange
name: Encrypted Key Exchange
aliases:
- EKE
- DH-EKE
- EKE2
area: cryptography/key-exchange
level: advanced
summary: The first PAKE. Each side sends its Diffie-Hellman share encrypted under the password, and the key is a hash of the shares and g^xy. Bellovin and Merritt 1992; proved with an ideal cipher in 2000.
solves: [password-authenticated-key-exchange]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the prime p}
  time: {worst: O(m^3), average: O(m^3), best: O(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1992
  people: [Steven M. Bellovin, Michael Merritt]
  note: Bellovin and Merritt introduced EKE at IEEE S&P 1992 and Augmented EKE at ACM CCS 1993. Bellare, Pointcheval and Rogaway proved the variant EKE2 secure in the ideal cipher model in 2000.
prereqs: [password-authenticated-key-exchange, diffie-hellman, ideal-cipher-model]
see_also: [spake2, cpace, secure-remote-password, j-pake, opaque, feistel-network, pseudorandom-permutation, quadratic-residue]
sources:
  - paper: "Steven M. Bellovin and Michael Merritt, Encrypted key exchange: password-based protocols secure against dictionary attacks, IEEE Symposium on Research in Security and Privacy 1992, pages 72 to 84"
    locator: EKE with RSA and with Diffie-Hellman, the partition attack and the rule that the encrypted values must look random under every password
  - paper: "Steven M. Bellovin and Michael Merritt, Augmented encrypted key exchange: a password-based protocol secure against dictionary attacks and password file compromise, ACM CCS 1993, pages 244 to 250"
    locator: the augmented protocol, in which the server stores a one-way function of the password and the client proves knowledge of the password with a signature
  - paper: doi:10.1007/3-540-45539-6_11
    title: Mihir Bellare, David Pointcheval and Phillip Rogaway, Authenticated key exchange secure against dictionary attacks, EUROCRYPT 2000, LNCS 1807, pages 139 to 155
    locator: the BPR model, the protocol EKE2, and its proof in the ideal cipher model and random oracle model under the computational Diffie-Hellman assumption
---

Encrypted Key Exchange (EKE) is the first [password-authenticated key exchange](/password-authenticated-key-exchange/), proposed by Steven Bellovin and Michael Merritt in 1992. In its [Diffie-Hellman](/diffie-hellman/) form, each party encrypts its share $g^x$ with a symmetric cipher keyed by the password, the other party decrypts it, and both compute $g^{xy}$. An eavesdropper who tries a wrong password gets a random-looking group element, so the transcript does not let it test guesses, provided that the cipher maps every ciphertext under every key to a valid group element. Bellare, Pointcheval and Rogaway proved a variant, EKE2, secure in 2000, in the [ideal cipher model](/ideal-cipher-model/).

**Notation.** $p = 2q + 1$ a [safe prime](/safe-prime/), $G$ the subgroup of [quadratic residues](/quadratic-residue/) modulo $p$, of prime order $q$, with generator $g$. $pw$ the shared password, $E_{pw}$ and $D_{pw}$ a block cipher on $G$ (a permutation of $G$ for each key) and its inverse. $x, y$ the random exponents of $A$ and $B$, $X = g^x$, $Y = g^y$, $K = g^{xy}$, and $H$ a hash function. All arithmetic is modulo $p$.

## In plain words

Two parties share a password. They want to do a Diffie-Hellman exchange, but an attacker in the middle could replace their values. So each party locks its value with the password before sending it.

The other party unlocks it with the same password and then finishes the exchange. A party with the wrong password unlocks a different value, so the two sides get different keys.

The lock must be chosen with care. An eavesdropper can try to unlock a value with every password in a list. If wrong passwords sometimes give values that cannot be correct, each recorded session removes many guesses, until one password is left. With a good lock, every guess gives a possible value, and the eavesdropper learns nothing.

## The problem

[Password-authenticated key exchange](/password-authenticated-key-exchange/): two parties that share a low-entropy password want a [session key](/session-key/), with no public key infrastructure, such that a passive attacker cannot test password guesses offline and an active attacker can test only one guess per run. In 1992 this was open: protocols that used a password as a key, such as [Kerberos](/kerberos/), allowed offline dictionary attacks on recorded traffic.

## The algorithm

```pseudo id=main
EKE2(pw; p, q, g)              ▷ Diffie-Hellman EKE in the form of BPR 2000
L1  A: x ← random in [1, q);  X ← g^x
L2  A: Xc ← E_pw(X)
L3  A → B: "A", Xc
L4  B → A: "B", Yc             ▷ B did lines L1 and L2 with y, Y = g^y and Yc = E_pw(Y)
L5  A: Y ← D_pw(Yc);  B: X ← D_pw(Xc)
L6  A: K ← Y^x;  B: K ← X^y
L7  abort if K = 1
L8  sk ← H("A", "B", X, Y, K)
```

Lines L1 to L4 are a Diffie-Hellman exchange in which each share travels encrypted under the password. The messages can be sent at the same time, so the protocol has one round. Line L5 decrypts the peer's share, and line L6 finishes the exchange. Line L8 hashes the identities, both shares and $K$; BPR show that this hash, together with the ideal cipher, gives a secure session key. EKE2 has no key confirmation; a confirmation round can be added with a MAC under a key derived from $K$.

**The encoding of the shares.** The security argument needs the following property: for every ciphertext $c$ and every password $pw'$, $D_{pw'}(c)$ is a valid element of $G$, and for a random $X$ the ciphertext is uniform. Otherwise the eavesdropper runs a **partition attack**: for each recorded ciphertext, it keeps only the passwords under which the decryption is a valid share. Each session removes a fixed fraction of the wrong passwords, and after a few dozen sessions one password is left. Bellovin and Merritt described this attack in 1992. It applies, for example, when an $m$-binary-digit block cipher encrypts a number modulo $p < 2^m$: a decryption in $[p, 2^m)$ rules the password out, and so does a decryption that is not a quadratic residue.

**The ideal cipher.** BPR prove EKE2 secure in the BPR model (see [PAKE](/password-authenticated-key-exchange/)) when $E$ is an ideal cipher on $G$ (a random permutation of $G$ for each key) and $H$ is a [random oracle](/random-oracle-model/), under the [computational Diffie-Hellman](/computational-diffie-hellman/) assumption. A real block cipher such as AES is a permutation of 128-bit strings, not of $G$, so a deployment must build a cipher on $G$. The page's code builds one in two steps. First, $y \mapsto \min(y, p - y)$ maps the quadratic residues one to one onto $[1, q]$, because exactly one of $y$ and $p - y$ is a residue when $p \equiv 3 \pmod 4$. Second, an 8-round [Feistel network](/feistel-network/) with HMAC-SHA512 round functions permutes $[0, 2^k)$, and cycle walking (apply it again until the value is below $q$) restricts it to a permutation of $[0, q)$. Every ciphertext in $[0, q)$ then decrypts, under every password, to a residue. This is a heuristic stand-in for an ideal cipher, not a proven one: the results that make a Feistel network behave like a random permutation assume ideal round functions, and HMAC and cycle walking are not covered by them.

**About the code.** The Python code is for study only. It is not constant time, and it must not protect real data. Agreement runs in the 1024-bit group of RFC 5054, Appendix A, with $g = 4$. The partition attack runs only on a 128-bit toy safe prime against local simulated parties. There is no official test vector for EKE.

## Example

The partition attack, on the 128-bit toy prime $p$, with $p / 2^{128} \approx 0.75$. The bad encoding XORs $X$ with a 128-binary-digit key stream derived from the password. A wrong password decrypts to a random 128-binary-digit number, which is in $[1, p)$ and a quadratic residue with probability about $0.75 \cdot 0.5 = 0.375$. The dictionary has 256 words; the eavesdropper records sessions of one user and keeps the words that pass every session. The code gives these counts (random seed 3):

| sessions | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| words left | 96 | 45 | 15 | 7 | 4 | 3 | 2 | 2 |

The expected count is $1 + 255 \cdot 0.375^k$, close to the table. With 40 sessions only the right password is left. Under the careful encoding of the code, every word passes every session, and after 20 sessions all 256 words are left.

## Correctness

**Claim.** With the same password, both parties compute the same $K = g^{xy}$ and the same session key. $D_{pw}$ inverts $E_{pw}$, so $A$ gets $Y = g^y$ and $B$ gets $X = g^x$; then $Y^x = g^{xy} = X^y$, and both hash the same tuple in line L8. $K \ne 1$ because $g$ has prime order $q$ and $x, y \in [1, q)$. The [full proof](/encrypted-key-exchange/proofs/correctness/) also shows that the page's encoding is a permutation of $G$ for each password.

**Security.** BPR (2000) prove EKE2 secure in their model in the ideal cipher model and the random oracle model, under CDH: an active attacker gains about one password guess per run, and a passive attacker gains no advantage. There is no proof with a concrete block cipher.

## Complexity

Each party does two [modular exponentiations](/modular-exponentiation/) ($g^x$ and $Y^x$), one encryption and one decryption on $G$, and one hash. An exponentiation costs $O(m^3)$ word operations with schoolbook multiplication, so a run costs $O(m^3)$. The Feistel encryption costs 8 HMAC calls per pass and, in expectation, at most $2^k / q < 4$ passes for cycle walking. The protocol has one round and two messages, of $O(m)$ binary digits each. Each party keeps $O(1)$ numbers of $m$ binary digits.

## Properties

- **Balanced**: both parties hold the password.
- **One round**, two messages, and the cost of plain Diffie-Hellman plus a symmetric cipher.
- **Implicit authentication**: no key confirmation in EKE2.
- **Forward secrecy**: the key depends on fresh $x$ and $y$.
- **Needs an ideal cipher on the group**, which no standard cipher provides; this is the main obstacle to deployment.
- **Not quantum-safe**.

## Variants and improvements

- **RSA-EKE** (1992): the client sends an RSA public key encrypted under the password. It is open to partition attacks through the public exponent and the modulus, and is not used.
- **Augmented EKE** (Bellovin and Merritt 1993) protects against a stolen password file. The server stores $T = h(pw)$, a one-way function of the password, and the parties run EKE with $T$ as the shared key. Then the client sends a value that only a holder of $pw$ can make, bound to the new key, and the server checks it with $T$. A thief who has the server file can play the server but cannot log in as the client without first finding the password. This idea led to verifier-based protocols such as [SRP](/secure-remote-password/) and later to [OPAQUE](/opaque/).
- **PAK and PPK** (Boyko, MacKenzie and Patel 2000) replace the encryption by multiplication with $H(pw)$, a hash to the group, and are proved in the random oracle model without an ideal cipher.
- **OEKE** (Bresson, Chevassut and Pointcheval 2003) encrypts only one of the two shares.
- **[SPAKE2](/spake2/)** (2005) replaces the encryption by adding $wM$, and **[CPace](/cpace/)** replaces it by a password-dependent generator; both avoid the ideal cipher.

## When to use it

Do not use EKE for a new design: it needs a cipher on the group that behaves like an ideal cipher, and there is no standard one. EKE is useful for study, because it shows the core problem of every PAKE (a transcript must not allow offline tests of guesses) and the partition attack. For a balanced PAKE, use [CPace](/cpace/); for client-server logins, use [OPAQUE](/opaque/).

## Pitfalls

- **Encrypting the binary digits of X with a standard cipher.** A wrong password then gives values that are $\ge p$ or not residues, and the partition attack applies. Line L2 needs a cipher whose message space is exactly $G$.
- **Encrypting both shares with a stream cipher.** XORing both shares with the same key stream gives $X_c \oplus Y_c = X \oplus Y$ and leaks structure. Each encryption must be a fresh permutation call.
- **No check of K.** Line L7 rejects $K = 1$; with a group that is not of prime order, also check that the decrypted share lies in $G$.
- **A key from K alone.** Line L8 must hash the identities and the shares; otherwise the security argument of BPR does not apply.
- **Reusing x.** A fixed $x$ lets an attacker who learns one key relate others; pick fresh exponents in line L1.

## Implementations

The Python code gives the careful encoding (`encrypt`, `decrypt`, with `_feistel` and `_prp`), the protocol (`start` for lines L1 and L2, `finish` for lines L5 to L8, and `run` for lines L3 and L4), and the attack (`bad_encrypt`, `bad_decrypt`, `partition_attack`). The tests check that both groups are safe primes, that the encoding is a round trip and that every ciphertext decodes to a group element, agreement and failure with a wrong password, and the partition attack against both encodings.

## History

In 1992, Bellovin and Merritt at AT&T Bell Labs proposed EKE to stop offline dictionary attacks on protocols such as Kerberos, and in 1993 they gave Augmented EKE against the theft of the password file. The protocol was patented, which limited its use until the patent expired. Jablon's SPEKE (1996) and Wu's [SRP](/secure-remote-password/) (1998) followed. Bellare, Pointcheval and Rogaway (2000) gave the first formal model for PAKE and proved EKE2 in it, with an ideal cipher; Boyko, MacKenzie and Patel gave proofs for PAK in the same year. Later PAKEs such as [SPAKE2](/spake2/) and [CPace](/cpace/) keep the idea of EKE but avoid the ideal cipher.

## References
