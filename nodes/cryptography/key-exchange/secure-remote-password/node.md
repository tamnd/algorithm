---
tag: KNRW9R
kind: algorithm
slug: secure-remote-password
name: Secure Remote Password protocol
aliases:
- SRP
- SRP-6a
area: cryptography/key-exchange
level: advanced
summary: An augmented PAKE. The server stores a verifier v = g^x, and both sides reach g^(b(a + ux)) mod N. RFC 2945 and RFC 5054 (TLS). Widely deployed, but it has no proof in a standard model.
solves: [password-authenticated-key-exchange]
model: word-ram
complexity:
  vars: {n: the number of binary digits of the modulus N}
  time: {worst: O(n^3), average: O(n^3), best: O(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 1998
  people: [Thomas Wu]
  note: Wu presented SRP at NDSS 1998. SRP-6 and SRP-6a (2002) fixed a two-for-one guessing attack. RFC 2945 (2000) and RFC 5054 (2007, SRP in TLS) standardized it.
prereqs: [password-authenticated-key-exchange, diffie-hellman, safe-prime]
see_also: [opaque, encrypted-key-exchange, spake2, cpace, password-hashing, sha-1, tls-handshake]
sources:
  - paper: "Thomas Wu, The secure remote password protocol, Network and Distributed System Security Symposium (NDSS) 1998, pages 97 to 111"
    locator: the protocol (SRP-3 with B = v + g^b), the verifier, and the informal security discussion
  - paper: "Thomas Wu, SRP-6: improvements and refinements to the Secure Remote Password protocol, submission to the IEEE P1363 working group, October 2002"
    locator: the multiplier k, the two-for-one guessing attack on SRP-3, and the scrambler u = H(A, B)
  - url: "https://www.rfc-editor.org/rfc/rfc2945"
    title: Thomas Wu, RFC 2945, The SRP Authentication and Key Exchange System, September 2000
    locator: the protocol and the evidence messages M1 and M2
  - url: "https://www.rfc-editor.org/rfc/rfc5054"
    title: David Taylor, Thomas Wu, Nikos Mavrogiannopoulos and Trevor Perrin, RFC 5054, Using the Secure Remote Password (SRP) Protocol for TLS Authentication, November 2007
    locator: Section 2.4 (verifier), Sections 2.5.3 and 2.5.4 (B, A and the checks B % N and A % N), Section 2.6 (premaster secret), Sections 3.2 to 3.4 (security), Appendix A (groups), Appendix B (test vectors)
---

The Secure Remote Password protocol (SRP) is an augmented [password-authenticated key exchange](/password-authenticated-key-exchange/) designed by Thomas Wu in 1998. The server does not store the password. It stores a salt $s$ and a verifier $v = g^x \bmod N$, where $x$ is a hash of the salt and the password. In a login, the client and the server run a variant of [Diffie-Hellman](/diffie-hellman/) in which the server blinds its share with the verifier, and both reach the same secret $S = g^{b(a + ux)} \bmod N$ only if the client knows the password. The current form is SRP-6a, standardized for TLS in RFC 5054 (2007). SRP is widely deployed, but it has no security proof in a standard model, and the CFRG did not select it in its PAKE selection of 2019 and 2020.

**Notation.** $N = 2q + 1$ a [safe prime](/safe-prime/) and $g$ a generator of $\mathbb{Z}_N^*$ (RFC 5054, Appendix A). $H$ the hash function (SHA-1 in RFC 5054). $I$ the user name, $P$ the password, $s$ the salt. $x = H(s \| H(I \| \texttt{":"} \| P))$ the private key and $v = g^x \bmod N$ the verifier. $k = H(N \| \mathrm{PAD}(g))$ the multiplier. $a, b$ the random secrets of the client and the server, $A = g^a$, $B = kv + g^b$, $u = H(\mathrm{PAD}(A) \| \mathrm{PAD}(B))$ the scrambler, $S$ the premaster secret, $K = H(S)$ the session key. $\mathrm{PAD}(y)$ writes $y$ in big-endian bytes, left-padded with zeros to the length of $N$. All arithmetic is modulo $N$.

## In plain words

A user wants to log in to a server with a password, without sending the password and without trusting a certificate. At sign-up, the client turns the password into a public "lock" value and gives it to the server. The server keeps only this lock, never the password.

At login, both sides pick fresh random numbers and swap blinded values. The server mixes its value with the lock. Only someone who knows the password can remove the lock again, so only the real user ends up with the same secret as the server. Each side then proves that it holds the secret.

An eavesdropper learns nothing it can test against a list of passwords. A fake server or client gets one guess per login attempt. A thief who steals the lock still has to guess the password, one candidate at a time.

## The problem

[Password-authenticated key exchange](/password-authenticated-key-exchange/) in the augmented (asymmetric) setting: the client knows a password, the server knows only a value derived from it, and they want a shared [session key](/session-key/) and mutual authentication. A passive attacker must not be able to test password guesses offline, an active attacker should get one guess per run, and an attacker who steals the server database should still need a dictionary search to log in as the user.

## The algorithm

```pseudo id=main
SRP-6a(I, P; N, g, H)                    ▷ RFC 5054 Sections 2.4 to 2.6
                                          ▷ registration, done once
L1  k ← H(N ‖ PAD(g))                    ▷ the SRP-6a multiplier
L2  x ← H(s ‖ H(I ‖ ":" ‖ P))            ▷ s a random salt
L3  v ← g^x mod N                        ▷ the server stores (I, s, v)
                                          ▷ login: client → server: I, A; server → client: s, B
L4  client: a random, A ← g^a mod N
L5  server: b random, B ← (k·v + g^b) mod N
L6  client: abort if B mod N = 0
L7  client: u ← H(PAD(A) ‖ PAD(B)); abort if u = 0
L8  client: base ← (B − k·g^x) mod N      ▷ removes the verifier: base = g^b
L9  client: S ← base^(a + u·x) mod N
L10 server: abort if A mod N = 0
L11 server: u ← H(PAD(A) ‖ PAD(B)); abort if u = 0
L12 server: S ← (A·v^u)^b mod N
L13 both: K ← H(S)
L14 client → server: M1 ← H(PAD(A) ‖ PAD(B) ‖ K)
L15 server → client: M2 ← H(PAD(A) ‖ M1 ‖ K)
L16 each side checks the proof it receives and aborts on a mismatch
```

Lines L1 to L3 are the verifier creation of RFC 5054, Section 2.4, and lines L4 to L12 are its Section 2.6. Line L5 is the key idea: the server adds $k v$ to its Diffie-Hellman share $g^b$, so only a party that can compute $k g^x$ (line L8) can unblind it. The scrambler $u$ of lines L7 and L11 is computed after both shares are fixed; it stops a thief who holds $v$ from logging in as the client, because $v^u$ enters the server's computation with an exponent that the thief cannot choose in advance. The checks of lines L6 and L10 are required by RFC 5054, Sections 2.5.3 and 2.5.4. A client that sends $A = 0$ or $A = N$ makes the server compute $S = 0$ without any password, so without line L10 anyone can log in.

Lines L14 and L15 follow Wu's paper. RFC 2945 defines a longer $M_1$ that also hashes $N$, $g$, $I$ and $s$, and RFC 5054 replaces both messages by the TLS Finished messages. Any of these forms gives key confirmation; they do not interoperate.

**About the code.** The Python code is for study only. It is not constant time, and it must not protect real data. It uses SHA-1 only because the RFC 5054 test vector uses it. SHA-1 is broken for collisions, and RFC 5054, Section 3.4, explains why this does not break these uses, but a new design should not use SHA-1, and a new design should not use SRP either: use [OPAQUE](/opaque/).

## Example

RFC 5054, Appendix B, with the 1024-bit group of Appendix A ($g = 2$), the user `alice`, the password `password123` and the salt `BEB25379 D1A8581E B5A72767 3A2441EE`. Long values are shortened to their first and last words.

| step | value (hex) |
|---|---|
| L1: $k$ | `7556AA04 5AEF2CDD 07ABAF0F 665C3E81 8913186F` |
| L2: $x$ | `94B7555A ABE9127C C58CCF49 93DB6CF8 4D16C124` |
| L3: $v$ | `7E273DE8 696FFC4F ... E2099AFB` |
| L4: $a$ and $A$ | `60975527 ... DA2D4393`, $A$ = `61D5E490 F6F1B795 ... 0769447B` |
| L5: $b$ and $B$ | `E487CB59 ... 05284D20`, $B$ = `BD0C6151 2C692C0C ... 4B117B58` |
| L7: $u$ | `CE38B959 3487DA98 554ED47D 70A7AE5F 462EF019` |
| L9 and L12: $S$ | `B0DC82BA BCF30674 ... CA686E5A` |

The client (line L9) and the server (line L12) compute the same premaster secret, which is the last value of the appendix. The tests check every value of the appendix, including all 128 bytes of $v$, $A$, $B$ and $S$.

## Correctness

**Claim.** If the client uses the password that created $v$, both sides compute $S = g^{b(a + ux)} \bmod N$. The client computes $B - k g^x = k v + g^b - k v = g^b$, so line L9 gives $(g^b)^{a + ux}$; the server computes $A v^u = g^a g^{xu}$, so line L12 gives $(g^{a + ux})^b$. With a wrong password $x' \ne x$ the client gets $\mathrm{base} = g^b + k(g^x - g^{x'})$, and the two values of $S$ differ except with negligible probability, so the check of $M_1$ in line L16 fails. The [full proof](/secure-remote-password/proofs/correctness/) also covers the abort conditions.

**Security.** SRP has no proof in a standard model. The original paper argues informally that the protocol resists offline dictionary attacks, and the RFCs repeat that argument. The mix of addition ($kv + g^b$) and multiplication modulo $N$ does not fit the group-based reductions used for [EKE](/encrypted-key-exchange/), [SPAKE2](/spake2/) or [CPace](/cpace/), and the protocol cannot be moved to an elliptic curve group, where adding points and multiplying them are not both available. Analyses that do exist need the [random oracle model](/random-oracle-model/) and new assumptions. Known weaknesses:

- **Two-for-one guessing (SRP-3).** With $k = 1$, an active attacker who plays the server can test two passwords per run. SRP-6 added $k = 3$, and SRP-6a uses $k = H(N, g)$ (RFC 5054, Section 3.4).
- **Stolen verifier.** A thief with $(s, v)$ can run a dictionary search, and it can play the server to the user. It cannot log in as the user directly, because of $u$ (RFC 5054, Section 3.3).
- **Precomputation.** The server sends the salt before any authentication, so an attacker can learn $s$ for a user and build a table of $v$ values before it steals the database. Then a breach reveals weak passwords at once. [OPAQUE](/opaque/) was designed to remove this.

## Complexity

Each side does three [modular exponentiations](/modular-exponentiation/) per login: the client computes $g^a$, $g^x$ and $\mathrm{base}^{a + ux}$; the server computes $g^b$, $v^u$ and $(A v^u)^b$. Registration adds one more for $v$. With schoolbook multiplication, an exponentiation modulo an $n$-digit $N$ with an exponent of at most $n$ binary digits costs $O(n^3)$ word operations, so a run costs $O(n^3)$; the exponents $a$ and $b$ have 256 binary digits in RFC 5054, which makes the constant smaller. The protocol has four messages in two round trips: $(I, A)$, $(s, B)$, $M_1$ and $M_2$. Each side stores $O(1)$ numbers of $n$ binary digits.

## Properties

- **Augmented.** The server stores $(I, s, v)$, not a password equivalent. A thief must still guess the password before it can log in as the user.
- **Mutual authentication** through $M_1$ and $M_2$, and a fresh session key per run.
- **Forward secrecy.** $S$ depends on the fresh $a$ and $b$; a later theft of the password or of $v$ does not reveal old session keys to an eavesdropper.
- **Not quantum-safe**, like every protocol based on the [discrete logarithm problem](/discrete-logarithm-problem/).
- **Needs a trusted group.** The client must check that $N$ is a known safe prime (RFC 5054, Section 3.2); a server that picks a trapdoored $N$ can learn the password.

## Variants and improvements

- **SRP-3** (1998, RFC 2945): $B = v + g^b$ and a $u$ from $B$ alone. It allows the two-for-one guessing attack.
- **SRP-6** (2002): $k = 3$ and $u = H(A, B)$. **SRP-6a**: $k = H(N, \mathrm{PAD}(g))$; this is the form of RFC 5054 and of this page.
- **TLS-SRP** (RFC 5054): cipher suites that run SRP inside the TLS 1.2 handshake. TLS 1.3 has no SRP mode.
- **Augmented EKE** (Bellovin and Merritt 1993) is an earlier verifier-based design built on [EKE](/encrypted-key-exchange/).
- **[OPAQUE](/opaque/)** (2018, RFC 9807): an augmented PAKE with a proof in the UC model and security against precomputation; the CFRG selected it in 2020.

## When to use it

Use SRP only to interoperate with an existing system that speaks it. For a new design, use [OPAQUE](/opaque/) when the server must store a verifier, or a balanced PAKE such as [CPace](/cpace/) or [SPAKE2](/spake2/) when both sides hold the password. These have security proofs and run on elliptic curves, which makes them much faster than SRP with a 2048-bit or larger modulus.

## Pitfalls

- **No check of A.** Without line L10, a client that sends $A = 0$, $N$ or $2N$ forces $S = 0$ on the server and logs in with no password. Several implementations had this bug. Check $A \bmod N \ne 0$ before line L12.
- **No check of B.** Without line L6, a fake server can send $B \equiv 0$ and learn about the client's computation; check it before line L8.
- **Wrong multiplier.** SRP-6 ($k = 3$) and SRP-6a ($k = H(N, g)$) do not interoperate, and $k = 1$ (SRP-3) allows two guesses per run. Use line L1 exactly.
- **Unpadded hashing.** RFC 5054 hashes $\mathrm{PAD}(A)$ and $\mathrm{PAD}(B)$ in lines L7 and L11; hashing the minimal-length bytes gives a different $u$ for some values and breaks interoperation.
- **A group from the server.** Accept only the groups of RFC 5054, Appendix A, or a locally configured trusted group.
- **A fast hash of the password.** $x$ in line L2 is one hash call, so a thief tests guesses very fast. Applications harden $x$ with a slow [password hash](/password-hashing/) such as [scrypt](/scrypt/) or [Argon2](/argon2/); RFC 5054 does not.

## Implementations

The Python code gives `multiplier`, `private_key`, `verifier`, `client_public`, `server_public`, `client_premaster`, `server_premaster`, `session_key`, `client_proof`, `server_proof` and `run`, with the line markers of the pseudocode. The tests check every value of RFC 5054, Appendix B, that $N$ is a safe prime, agreement on random runs, a wrong password, the rejection of $A \in \{0, N, 2N\}$ and of $B = N$, and that a stolen verifier allows a dictionary search.

## History

Bellovin and Merritt introduced password-based key exchange with EKE in 1992 and the verifier idea with Augmented EKE in 1993. Wu presented SRP at NDSS 1998 as a simpler verifier-based protocol without symmetric encryption, and RFC 2945 (2000) standardized that version, SRP-3. Wu described SRP-6 in 2002 to fix the two-for-one guessing attack, and SRP-6a with $k = H(N, g)$ became the form of RFC 5054 (2007), which added SRP to TLS. SRP was then used in products such as password managers and cloud key escrow. When the CFRG selected PAKEs for the IETF in 2019 and 2020, SRP was not a candidate; the CFRG chose [CPace](/cpace/) and [OPAQUE](/opaque/).

## References
