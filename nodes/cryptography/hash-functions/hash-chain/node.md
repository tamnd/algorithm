---
tag: WAQZTJ
kind: data-structure
slug: hash-chain
name: Hash chain
aliases:
- iterated hash chain
- Lamport hash chain
- S/KEY chain
area: cryptography/hash-functions
level: intro
summary: "A sequence x_i = f(x_(i-1)) from a secret seed, revealed backward. Each value is checked with one hash, and seen values do not give the next one. Used in S/KEY, OTP (RFC 2289) and TESLA."
model: word-ram
complexity:
  vars: {n: the chain length, t: the checkpoint spacing}
  time: {worst: Θ(t)}
  space: {extra: Θ(n/t)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [cryptographic-hash-function, preimage-resistance]
see_also: [merkle-tree, lamport-signature, winternitz-one-time-signature, hellman-time-memory-tradeoff, rainbow-table, md4, md5, sha-1]
sources:
  - paper: "Leslie Lamport, Password authentication with insecure communication, Communications of the ACM 24(11), November 1981, pages 770 to 772"
    locator: the scheme that stores F^n(x) on the server and sends F^(n-1)(x), F^(n-2)(x), and so on
  - url: "https://www.rfc-editor.org/rfc/rfc2289"
    title: Neil Haller, Craig Metz, Philip Nesser and Mike Straw, RFC 2289, A One-Time Password System, February 1998
    locator: Section 6 (initial step and computation step), Section 7 (verification), Section 9 (race attack), Appendix A (folding to 64 bits), Appendix C (test vectors for MD4, MD5 and SHA1)
  - url: "https://www.rfc-editor.org/rfc/rfc1760"
    title: Neil Haller, RFC 1760, The S/KEY One-Time Password System, February 1995
    locator: the Bellcore S/KEY system that RFC 2289 standardizes
  - url: "https://www.rfc-editor.org/rfc/rfc1320"
    title: Ronald Rivest, RFC 1320, The MD4 Message-Digest Algorithm, April 1992
    locator: Section 3 (the algorithm) and Appendix A.5 (test suite)
  - url: "https://www.rfc-editor.org/rfc/rfc4082"
    title: Adrian Perrig, Dawn Song, Ran Canetti, J. D. Tygar and Bob Briscoe, RFC 4082, TESLA, June 2005
    locator: the key chain of TESLA, with keys disclosed after a delay and checked by hashing forward
  - paper: "Markus Jakobsson, Fractal hash sequence representation and traversal, IEEE International Symposium on Information Theory (ISIT), 2002"
    locator: traversal of a chain of length n with O(log n) stored values and O(log n) hash calls per output
  - paper: "Stuart Haber and W. Scott Stornetta, How to time-stamp a digital document, Journal of Cryptology 3(2), 1991"
    locator: linked time stamps, where each certificate includes the hash of the one before
---

A hash chain is the sequence $x_0 = s$, $x_i = f(x_{i-1})$ for a one-way function $f$ and a secret seed $s$. The owner gives the end value $x_n$, the *anchor*, to a verifier, then reveals the values backward: $x_{n-1}$, then $x_{n-2}$, and so on. The verifier checks each new value with one hash, $f(y) = $ the last accepted value. A listener who sees $x_i$ can compute $x_{i+1}, \ldots, x_n$, which are already used, but not $x_{i-1}$, which would mean inverting $f$. Leslie Lamport proposed this in 1981 for one-time passwords; it is the basis of S/KEY and the OTP system of RFC 2289, of the TESLA broadcast authentication protocol, and of the chains inside [Winternitz signatures](/winternitz-one-time-signature/).

**Notation.** $f$ is the step function, $f^i$ is $f$ applied $i$ times, $x_i = f^i(s)$, $n$ is the chain length, $v$ is the value the verifier holds, and $t$ is the spacing of stored checkpoints. In RFC 2289, $f(x) = \mathrm{FOLD}(H(x))$, where $H$ is MD4, MD5 or SHA-1 and FOLD reduces the digest to 64 bits, and $\|$ is concatenation. Security rests on the [preimage resistance](/preimage-resistance/) of $f$ on the values of the chain. With $f$ a random oracle the bound is tight; for a general one-way function an iterate need not be one way, see Correctness.

## In plain words

You pick a secret and hash it 100 times. You give the server the last result. To log in, you send the value from step 99. The server hashes it once, sees that it gets the stored value, lets you in, and now stores your step 99. Next time you send step 98, and so on.

A spy who records your login learns step 99. From it he can compute step 100, which is useless, but not step 98, because that would mean undoing a hash. So each password works once, and the server never stores anything that lets someone log in.

## The abstract type

A hash chain is a one-time token generator with a public check. The prover side has GENERATE$(s, n)$, which returns the anchor, and NEXT, which returns the next unused value. The verifier side holds one value $v$ and has VERIFY$(y)$, which accepts when $f(y) = v$ and then sets $v \leftarrow y$. Each accepted value can be used only once, and values are used in the order $x_{n-1}, x_{n-2}, \ldots, x_0$.

## Representation

The verifier stores one value. The prover can store the seed only, all $n + 1$ values, or checkpoints.

**Invariant (prover).** For each $c$ that is a multiple of $t$ with $0 \le c \le n$, the prover stores $x_c$. Any $x_i$ is $f^{i - c}(x_c)$ for the largest checkpoint $c \le i$, which takes $i \bmod t$ hash calls.

**Invariant (verifier).** After $u$ accepted values, the verifier holds $v = x_{n - u}$.

With $t = 1$ the prover stores everything and outputs each value at once. With $t > n$ it stores only the seed and spends up to $n$ calls per value. Jakobsson's fractal traversal moves the checkpoints as the chain is used and needs only $O(\log n)$ stored values and $O(\log n)$ calls per output.

## Operations

```pseudo id=main
GENERATE(s, n, t)                        ▷ t is the checkpoint spacing
L1  x ← s; store x as checkpoint 0
L2  for i ← 1 to n: x ← f(x); if t divides i then store x as checkpoint i
L3  give the anchor v ← x = f^n(s) to the verifier

NEXT()                                   ▷ the u-th call returns x_(n−u)
L4  i ← n − u; c ← t·⌊i / t⌋; return f^(i − c)(checkpoint c)

VERIFY(y)                                ▷ the verifier holds v
L5  if f(y) = v then v ← y; return accept
L6  return reject

OTP(pass, seed, count, H)                ▷ RFC 2289, Sections 6 and 7
L7  S ← FOLD(H(lower(seed) ‖ pass)); return f^count(S), with f(x) = FOLD(H(x))
```

**OTP.** RFC 2289 makes the seed $s$ from the user's pass phrase and a public seed string sent by the server, $S = \mathrm{FOLD}(H(\mathrm{lower}(\mathit{seed}) \| \mathit{pass}))$, so one pass phrase gives different chains on different servers. The server sends the challenge (hash name, count, seed). The client returns $f^{\mathit{count}}(S)$, and the server applies $f$ once and compares with its stored value from the last login, as in lines L5 and L6. FOLD xors the two halves of an MD4 or MD5 digest. For SHA-1 it xors the 32-bit words as $d_0 \oplus d_2 \oplus d_4$ and $d_1 \oplus d_3$ and writes the two words in little endian order, as in Appendix A of the RFC.

## Example

The first RFC 2289 vector with MD5: pass phrase `This is a test.`, seed `TeSt`.

| step | input | MD5 digest | folded 64 bits |
|---|---|---|---|
| initial, count 0 | `testThis is a test.` | `afffa66b89f06d393178c75f50f4f4e4` | `9e876134d90499dd` |
| count 1 | the 8 bytes `9e876134d90499dd` | `25f2b71d9a6f5a105c975749ac9a588f` | `7965e05436f5029f` |

The folded values are those of RFC 2289, Appendix C. The full digests are not in the RFC; they are MD5 values that fold to the published results. For example, `afffa66b89f06d39` xor `3178c75f50f4f4e4` = `9e876134d90499dd`.

Now take a chain of length 1. The server stores $x_1$ = `7965e05436f5029f`. At login with count 0, the client sends $x_0$ = `9e876134d90499dd`. The server computes $f(x_0)$ = `7965e05436f5029f`, sees that it equals the stored value, accepts, and stores $x_0$. If a listener replays $x_0$, the server computes $f(x_0) = x_1 \ne x_0$ and rejects. The RFC value for count 99 is `50fe1962c4965880`, which is 99 more steps of the same $f$.

## Correctness

**Completeness.** By the verifier invariant, before the $u$-th login $v = x_{n-u+1}$, and the honest prover sends $x_{n-u}$. Then $f(x_{n-u}) = x_{n-u+1} = v$, so VERIFY accepts and sets $v = x_{n-u}$, which keeps the invariant. The checkpoint invariant gives NEXT the right value, because $f^{i-c}(x_c) = f^{i-c}(f^c(s)) = x_i$.

**Soundness.** Suppose an adversary has seen $x_n, \ldots, x_{j}$ and the verifier holds $v = x_j$. To be accepted it must output $y$ with $f(y) = x_j$. Any such $y$ is a preimage of $x_j$. So an adversary that logs in breaks preimage resistance of $f$ on the value $x_j$. All the values it saw are $f^k(x_j)$ for $k \ge 0$, which it could compute from $x_j$ itself, so they give no extra help.

The catch is the distribution: $x_j = f^j(s)$ is not a uniform output of $f$. If $f$ is a permutation, $f^j(s)$ is uniform when $s$ is, and the reduction loses only a factor $n$ for guessing which login the adversary attacks. For a general one-way function, iterates need not be one way, so the usual argument models $f$ as a random oracle with $m$-bit output. Then an adversary with $q$ queries succeeds with probability at most about $q / 2^m$ per value. For the 64 bits of RFC 2289, $2^{64}$ work is far less than modern security levels.

The proofs file has the details.

## Complexity

GENERATE takes $n$ calls to $f$ and stores $\lfloor n / t \rfloor + 1$ values. NEXT takes at most $t - 1$ calls, and $n (t - 1) / 2$ calls over the whole chain when $t$ divides $n$. With $t = \lceil \sqrt{n} \rceil$, storage and the worst cost per value are both about $\sqrt{n}$. VERIFY takes one call to $f$ and stores one value. For RFC 2289, each call to $f$ is one compression of MD4, MD5 or SHA-1, because the 8-byte input fits in one block.

## Variants

- **Lamport's scheme and S/KEY.** Lamport (1981) gave the idea; Phil Karn's S/KEY at Bellcore made it a product with MD4; RFC 2289 added MD5 and SHA-1 and the folding rules. A 64-bit value is shown to the user as six short English words from a 2048-word dictionary (RFC 2289, Appendix D).
- **TESLA.** A sender of a broadcast stream signs only the anchor of a key chain. Each packet carries a MAC under key $x_i$, and $x_i$ is disclosed a little later. A receiver checks a disclosed key by hashing it forward to an earlier key, so lost packets do not matter.
- **Winternitz and Lamport signatures.** A Winternitz one-time signature uses many short hash chains, and a signature reveals one value of each chain; see [Winternitz one-time signature](/winternitz-one-time-signature/) and [Lamport signature](/lamport-signature/).
- **Time-memory trade-off chains.** [Hellman tables](/hellman-time-memory-tradeoff/) and [rainbow tables](/rainbow-table/) store only the start and end of many chains of a reduction function and a hash. The goal there is to invert a hash, not to authenticate.
- **Linked time stamps and logs.** Each entry includes the hash of the one before (Haber and Stornetta, 1991), so the last hash commits to the whole history. A [Merkle tree](/merkle-tree/) gives shorter proofs for single entries.
- **Hash chain with traversal.** Jakobsson's fractal traversal and later work by Coppersmith and Jakobsson cut prover storage and time to $O(\log n)$.

## When to use it

Use a hash chain when a verifier must check a long series of one-time values with only a hash function and one stored value, and must not hold any secret: one-time passwords on devices with no public-key code, delayed key disclosure in broadcast, micropayment schemes such as PayWord, and the chains of hash-based signatures. For normal logins today, use TOTP or HOTP, or a FIDO2 or WebAuthn key. Those have their own trade-offs, but they avoid the 64-bit values and the fixed length of RFC 2289.

## Pitfalls

- **Small count attack.** A fake server that asks for a small count, such as 1, learns $x_1$, and from it can compute every value with a larger index, which are exactly the ones the real server will ask for. A client should warn when the count is low or when it drops by more than expected.
- **Race attack.** RFC 2289, Section 9, notes that an attacker who sees most of a password being typed can guess the rest and log in first. Servers must defend against this, for example by refusing a second login session for a user while one is open, with a timeout.
- **Active attacks.** OTP stops passive listening and replay only. It does not stop session hijacking after the login (RFC 2289, Section 10).
- **Weak pass phrase.** The chain is only as strong as the seed. An eavesdropper who records one OTP can test pass phrases offline, so RFC 2289 requires at least 10 characters.
- **Short output.** 64 bits allow about $2^{64}$ work to invert one value, and less with a [time-memory trade-off](/hellman-time-memory-tradeoff/) shared over many targets.
- **The chain runs out.** After $n$ logins the user must set up a new chain, with a new seed, over a trusted channel.
- **Endianness of SHA-1 folding.** The RFC folds the SHA-1 words and then writes them little endian; reading the digest as bytes and folding them as for MD5 gives different values, which the tests would catch.

## Implementations

The Python code is for study only. It is not constant time and must not protect real data. MD4, MD5 and SHA-1 are broken for collisions, and RFC 2289 passwords have only 64 bits. For real one-time passwords use HOTP or TOTP from a maintained library such as pyotp, or better a FIDO2 or WebAuthn authenticator.

`HashChain` holds the checkpoints and the anchor (lines L1 to L3) and returns values with `next` (line L4). `Verifier.verify` checks one step (lines L5 and L6), and `verify_skip` accepts a value a few steps back, as a TESLA receiver does after losses. `otp` computes an RFC 2289 password (line L7) with `fold` and `otp_hash`. MD4 is not in hashlib with OpenSSL 3, so the module has a short MD4 of its own, as in RFC 1320; MD5 and SHA-1 come from hashlib. The tests check the 7 MD4 vectors of RFC 1320, Appendix A.5; all 27 MD4, MD5 and SHA1 vectors of RFC 2289, Appendix C, and its parity example and input checks; the fold of MD5 against hashlib as a second check; that the server accepts count 98 after 99 and rejects a replay and a wrong value; that checkpoints of every spacing give the same values; the exact cost $n(t-1)/2$; and that one changed input bit changes about half the output bits of a step. The six-word encoding of Appendix D is not implemented.

## History

Lamport described the scheme in 1981. Phil Karn proposed S/KEY at Bellcore, and Neil Haller described it at NDSS in 1994 and in RFC 1760 (1995). The IETF made it the OTP standard, first as RFC 1938 (1996) and then as RFC 2289 (1998), with MD5 required and SHA-1 recommended. Haber and Stornetta used chains of hashes for time stamps in 1991. Perrig, Canetti, Tygar and Song built TESLA on key chains in 2000, and RFC 4082 (2005) describes it. Jakobsson (2002) and Coppersmith and Jakobsson (2002) showed how to traverse a chain with logarithmic storage and time.

## References
