---
tag: A3D86P
kind: concept
slug: nonce-reuse-attack
name: Nonce reuse attack
aliases:
- ECDSA nonce reuse
- PlayStation 3 key recovery
- biased nonce attack
area: cryptography/signatures
level: intro
summary: "Two (EC)DSA or Schnorr signatures with the same nonce give the secret key by two divisions. A few leaked binary digits of many nonces give it by a lattice attack (the hidden number problem)."
prereqs: [ecdsa, dsa]
see_also: [deterministic-nonce-generation, schnorr-signature, ed25519, lll-algorithm, closest-vector-problem, babai-nearest-plane, timing-attack]
sources:
  - paper: "fail0verflow (bushing, marcan, segher and sven), Console Hacking 2010, PS3 Epic Fail, talk at the 27th Chaos Communication Congress (27C3), Berlin, December 2010"
    locator: the part on the ECDSA signatures of Sony, which used the same nonce for every signature, and the recovery of the private key
  - url: "https://bitcoin.org/en/alert/2013-08-11-android"
    title: Bitcoin.org, Android Security Vulnerability, alert of 11 August 2013
    locator: the weak SecureRandom of Android, which repeated ECDSA nonces in Bitcoin wallets, and the advice to move coins to new keys
  - paper: "Dan Boneh and Ramarathnam Venkatesan, Hardness of computing the most significant bits of secret keys in Diffie-Hellman and related schemes, CRYPTO 1996, LNCS 1109, Springer, pages 129 to 142"
    locator: the hidden number problem and its solution with a lattice when about the square root of the binary digits of p are known
  - paper: doi:10.1023/A:1011214926272
    title: Nick Howgrave-Graham and Nigel P. Smart, Lattice attacks on digital signature schemes, Designs, Codes and Cryptography 23(3), 2001, pages 283 to 290
    locator: the first lattice attack that recovers a DSA key from signatures whose nonces are partly known
  - paper: doi:10.1007/s00145-002-0021-3
    title: Phong Q. Nguyen and Igor E. Shparlinski, The insecurity of the Digital Signature Algorithm with partially known nonces, Journal of Cryptology 15(3), 2002, pages 151 to 176
    locator: the reduction of DSA with partly known nonces to the hidden number problem, with a proof, and the lattice that the code here uses
  - paper: doi:10.13154/tches.v2020.i4.281-308
    title: Jan Jancar, Vladimir Sedlacek, Petr Svenda and Marek Sys, Minerva, The curse of ECDSA nonces, IACR Transactions on Cryptographic Hardware and Embedded Systems 2020(4), pages 281 to 308
    locator: the timing leak of the bit length of the nonce in smart cards and libraries, and the lattice attack that uses it
  - paper: "Daniel Moghimi, Berk Sunar, Thomas Eisenbarth and Nadia Heninger, TPM-FAIL, TPM meets timing and lattice attacks, USENIX Security Symposium 2020"
    locator: the timing leaks of ECDSA and ECSchnorr nonces in Intel firmware TPM and an STMicroelectronics TPM, and the key recovery by lattice
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 11, the security notes on the per-message secret of ElGamal and DSA signatures
---

A signature of the [DSA](/dsa/), [ECDSA](/ecdsa/) or [Schnorr](/schnorr-signature/) family uses a secret nonce $k$ for each message. The signature is a linear equation in $k$ and the secret key, and it is safe only because $k$ is uniform and unknown. If the same $k$ signs two different messages, the two equations have two unknowns, and anyone can solve them for the key. If $k$ is only partly known, for example a few top binary digits leak by timing, the equations of many signatures form an instance of the hidden number problem, which a lattice reduction solves. Sony's PlayStation 3 key (2010), Bitcoin wallets on Android (2013), and the Minerva and TPM-Fail timing attacks (2020) all failed this way.

**Notation.** $q$ (or $n$ for curves) is the prime group order, $x$ (or $d$) the secret key, $k_i$ the nonce of signature $i$, $z_i$ the hash of message $i$ as an integer, and $(r_i, s_i)$ the signature. All the equations are mod $q$.

## In plain words

Each signature hides the secret key behind a one-time random number, like a one-time pad. Two signatures with the same pad on different messages let anyone cancel the pad: subtract one from the other, and the random number falls out; put it back in either signature, and the secret key falls out. Nothing more than school algebra is needed.

A weaker leak is enough with more signatures. If an attacker learns only the first few digits of each random number, each signature gives a rough hint about the key. A lattice algorithm combines dozens or hundreds of rough hints into the exact key.

## The idea

### Reuse of the same nonce

ECDSA computes $r = x(kG) \bmod q$ and $s = k^{-1}(z + r x) \bmod q$. With the same $k$ for two messages, $r_1 = r_2 = r$, which is visible, and

$$s_1 k = z_1 + r x, \quad s_2 k = z_2 + r x \quad\Longrightarrow\quad k = \frac{z_1 - z_2}{s_1 - s_2}, \quad x = \frac{s_1 k - z_1}{r} \pmod q.$$

DSA is the same with $r = (g^k \bmod p) \bmod q$. For a Schnorr signature $s_i = k + e_i x$ with $e_1 \ne e_2$, so $x = (s_1 - s_2)/(e_1 - e_2)$. A known relation such as $k_2 = k_1 + 1$ breaks the scheme in the same way, because it also leaves two unknowns.

### Partly known nonces and the hidden number problem

Suppose the attacker knows $a_i$ with $k_i = a_i + b_i$ and $0 \le b_i < B$, where $B$ is much smaller than $q$; for example the top binary digits of $k_i$ leak and only the low $\log_2 B$ ones are unknown. From $s_i k_i = z_i + r_i x$,

$$b_i \equiv t_i x + u_i \pmod q, \quad t_i = r_i s_i^{-1}, \quad u_i = z_i s_i^{-1} - a_i.$$

Each equation says that $t_i x + u_i \bmod q$ is small. Finding $x$ from such equations is the hidden number problem of Boneh and Venkatesan (1996). Put the equations in a lattice of dimension $m + 2$ with the rows

- $q^2 e_i$ for $i = 1, \dots, m$,
- $(q t_1, \dots, q t_m, B, 0)$,
- $(q u_1, \dots, q u_m, 0, qB)$.

The integer combination $x$ times the second row, plus the third, minus the right multiples of the first rows, is the vector $(q b_1, \dots, q b_m, xB, qB)$. All its entries are at most about $qB$, while the lattice has determinant $q^{2m+1} B^2$. When $B$ is small enough this vector is unusually short, and a lattice reduction such as [LLL](/lll-algorithm/) finds it; its second to last entry divided by $B$ is $x$. Centering, which replaces $b_i$ by $b_i - B/2$, halves the entries. Finding the vector is an instance of the [closest vector problem](/closest-vector-problem/) in disguise, and Babai's [nearest plane](/babai-nearest-plane/) method gives the same result.

Howgrave-Graham and Smart (2001) first used this on DSA, and Nguyen and Shparlinski (2002) proved that a few known binary digits per nonce and a number of signatures that grows with $\log q$ suffice. In practice a handful of known digits per nonce and some tens to hundreds of signatures are enough for groups of 160 to 256 binary digits. Stronger reduction (BKZ, sieving) and Fourier methods in the style of Bleichenbacher go down to one known digit or a small bias, at the cost of many more signatures.

## Examples

**Reuse in a toy DSA group.** Take $p = 2039$, $q = 1019$, $g = 4$, the key $x = 123$, and let one nonce $k = 456$ sign two messages with hashes $z_1 = 100$ and $z_2 = 200$. Then $r = (4^{456} \bmod 2039) \bmod 1019 = 758$, $s_1 = 522$ and $s_2 = 263$. The attacker sees $r$ twice and computes $k = (100 - 200)/(522 - 263) = 919/259 \equiv 456$ and $x = (522 \cdot 456 - 100)/758 \equiv 123 \pmod{1019}$. The code does the same on secp256k1 with a 256-digit key, and then signs a message of its choice.

**The PlayStation 3.** Sony signed the PS3 software with ECDSA and the same $k$ every time. In December 2010, at the 27th Chaos Communication Congress, the group fail0verflow showed that two signatures were enough to compute the private key, which let anyone sign software for the console.

**Android Bitcoin wallets.** In August 2013 a flaw in Android's `SecureRandom` made wallets on Android repeat ECDSA nonces. Signatures with repeated $r$ in the public block chain gave the keys, and coins were stolen. The fix was to repair the generator and to move funds to fresh keys.

**Timing leaks.** Minerva (Jancar, Sedlacek, Svenda and Sys, 2020) found smart cards and libraries whose ECDSA signing time depended on the bit length of $k$. A signature that is fast has a $k$ with leading zeros, which is a known top part, and the lattice attack above recovered keys from some hundreds to thousands of such signatures. TPM-Fail (Moghimi, Sunar, Eisenbarth and Heninger, 2020) found the same kind of leak in Intel's firmware TPM and an STMicroelectronics TPM chip, and recovered ECDSA and ECSchnorr keys, also over a network.

**The lattice attack in the code.** A simulated DSA signer in a group with a 40-binary-digit $q$ leaks the top 10 binary digits of each nonce. With 12 signatures the lattice has dimension 14, and an exact LLL finds $x$ in well under a second. With only 2 known digits per nonce and 12 signatures it fails, as the size estimate predicts. The group is far too small to be secure, and the attack runs only against the local simulated signer.

## Where it is used

- **Key recovery from flawed signers**: game consoles, wallets, smart cards, TPMs and libraries with weak random generators, a fixed nonce, or timing leaks of the nonce.
- **Audits of public signatures**: researchers scan public keys and signatures (for example in Bitcoin and in TLS or SSH handshakes) for repeated $r$ values and for biased nonces.
- **The design of defenses**: [deterministic nonce generation](/deterministic-nonce-generation/) (RFC 6979, EdDSA) removes reuse across messages, hedged nonces add resistance to faults, and constant time scalar multiplication removes the timing leaks that feed the lattice attack.
- **Teaching and research on lattices**: the hidden number problem is a standard test for lattice reduction and Fourier analysis methods.

The code on this page is for study only and is not constant time.

## References
