---
tag: 3PEQ9N
kind: technique
slug: rsa-blinding
name: RSA blinding
area: cryptography/public-key
level: advanced
summary: Multiply the ciphertext by a random r^e before the private exponentiation and divide the result by r. The secret operation then runs on an input the attacker cannot choose or see.
prereqs: [rsa-cryptosystem]
see_also: [timing-attack, rsa-fault-attack, montgomery-multiplication, modular-exponentiation, chaum-blind-signature, rsa-signature, rsa-problem]
sources:
  - paper: "Paul C. Kocher, Timing attacks on implementations of Diffie-Hellman, RSA, DSS, and other systems, CRYPTO 1996, LNCS 1109, pages 104 to 113"
    locator: the countermeasure section, where the blinding of the input by a random r^e and the unblinding by r^{-1} are proposed
  - url: "https://www.usenix.org/legacy/events/sec03/tech/brumley.html"
    title: David Brumley and Dan Boneh, Remote timing attacks are practical, USENIX Security Symposium 2003
    locator: the defence section (blinding, which OpenSSL had but did not switch on)
  - url: "https://openssl-library.org/news/secadv/20030317.txt"
    title: OpenSSL Security Advisory, Timing-based attacks on RSA keys, 17 March 2003
    locator: "the whole file: the patch switches blinding on by default, CAN-2003-0147, and the sentence \"The performance impact of blinding appears to be small (a few percent).\""
  - paper: "Werner Schindler, Exclusive exponent blinding may not suffice to prevent timing attacks on RSA, CHES 2015, LNCS 9293, pages 229 to 247"
    locator: the attack on exponent blinding alone, and the number of random bits it needs
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 11, Note 11.6 and the blind signature section (the same multiplicative blinding, used for a different purpose)
---

RSA blinding hides the input of the private-key operation. Instead of computing $c^d \bmod N$ on the ciphertext $c$ that the attacker sent, the implementation draws a random $r$, computes $(c \cdot r^e)^d \bmod N$, and multiplies the result by $r^{-1} \bmod N$. The answer is the same, because $r^{ed} \equiv r$, but the number that goes through the secret exponentiation is uniform and unknown. Every side channel that needs a known or a repeated input, such as the [timing attack](/timing-attack/) of Kocher (1996) and of Brumley and Boneh (2003), or the [CRT fault attack](/rsa-fault-attack/), loses its handle. This page is about the defence. The same algebra used so that a signer cannot see the message is a [blind signature](/chaum-blind-signature/), which is a different goal.

## In plain words

A side channel attack watches the machine while it uses the private key, and it learns most when it can choose what the machine works on and ask the same question again and again. Blinding takes that away.

Before the secret step, the program mixes the incoming data with a fresh random value in a way that the public key can undo later. The secret step now runs on a random number. The attacker still sees how long it took, or how much power it drew, but that measurement belongs to a number the attacker does not know and cannot repeat.

The cost is a few extra multiplications for each operation, which is under one percent of the work. OpenSSL has done this for every RSA private key operation since March 2003.

## When it applies

- **The secret operation reads attacker-controlled data.** A TLS server decrypts whatever the client sends. A signing service signs what it is given. This is the normal case, and it is the case blinding is for.
- **The leak depends on the data, not only on the key.** Montgomery extra reductions, the branch on operand size, a cache line chosen by a word of the input, and the fault equation $\gcd(s'^e - m, N)$ all need the plaintext or the ciphertext. Blinding removes all of them at one stroke. A leak that depends only on the exponent, such as a square-and-multiply pattern in a power trace, needs exponent blinding or constant-time code instead.
- **The inverse of the blinding is public.** For RSA it is: $r \mapsto r^e$ uses the public exponent, so the implementation can blind without any extra secret. The same trick works for any [trapdoor permutation](/trapdoor-one-way-function/) with a group structure, and for scalar multiplication on an elliptic curve.
- **A few extra multiplications are acceptable.** If the budget does not allow this, the budget does not allow RSA.
- **It does not apply to public operations.** Verification and encryption use no secret, so there is nothing to hide.

## The template

```pseudo id=main
BLINDED-PRIVATE-OPERATION(c, N, e, d)
L1  r ← uniform random in {1, ..., N-1} with gcd(r, N) = 1   ▷ hole: the random source
L2  (A, Ai) ← (r^e mod N, r^{-1} mod N)                      ▷ hole: fresh, or updated from a cache
L3  c' ← c · A mod N                                         ▷ blind: the input is now uniform
L4  d' ← d                                                   ▷ hole: exponent blinding, optional
L5  m' ← (c')^{d'} mod N                                     ▷ hole: plain or CRT exponentiation
L6  m ← m' · Ai mod N                                        ▷ unblind
L7  return m
```

**Why the answer is unchanged.** In line 5 with $d' = d$,

$$m' = (c r^e)^d = c^d \cdot r^{ed} = c^d \cdot r \pmod N ,$$

because $ed \equiv 1 \pmod{\lambda(N)}$ gives $r^{ed} \equiv r$ for every $r$. Line 6 then returns $c^d \bmod N$. If line 4 uses $d' = d + t\lambda(N)$ for any integer $t \ge 0$, then $(c')^{d'} \equiv (c')^{d}$ as well, by the same identity, for every $c'$ including the ones that share a factor with $N$.

**The holes.**

- *The random source.* A cryptographic generator. The value $r$ must be unpredictable; see the pitfalls.
- *The pair $(A, A_i)$.* Computing $r^e$ and $r^{-1}$ from scratch costs one short exponentiation plus one [extended Euclid](/extended-euclidean-algorithm/) run. OpenSSL instead keeps the pair and squares both entries after each use, $A \leftarrow A^2$ and $A_i \leftarrow A_i^2$, which is two multiplications and keeps the relation $A = (A_i^{-1})^e$. It draws a fresh pair after a fixed number of uses.
- *Exponent blinding.* Add a random multiple of $\lambda(N)$, or of $p-1$ and $q-1$ in the CRT halves, so that the exponent itself differs on every run.
- *The exponentiation.* Any method. Blinding is orthogonal to the choice of [square and multiply](/modular-exponentiation/), a window method or a [Montgomery ladder](/binary-exponentiation/).

### The cost model

Count modular multiplications of $b$-bit numbers, with $b = 2048$, $e = 65537$ and CRT halves of 1024 bits. One CRT exponentiation with a 1024-bit exponent costs about 1024 squarings and about 200 multiplications on 1024-bit operands, and a 1024-bit multiplication costs about a quarter of a 2048-bit one. So a plain RSA-CRT decryption is about 2450 half-size multiplications, which is about 610 full-size ones.

| step | without blinding | base blinding | base and exponent blinding |
|---|---|---|---|
| draw $r$, build $(A, A_i)$ | none | 17 full modmuls plus one inverse, once in every 32 operations | the same |
| refresh the pair | none | 2 full modmuls | the same |
| blind and unblind | none | 2 full modmuls | the same |
| exponentiation | about 610 full modmuls | about 610 | about 650, for a 64-bit $t$ in each half |
| total | about 610 | about 615 | about 655 |
| overhead | 0 | under 1 percent | about 7 percent |

The 2003 OpenSSL advisory reports the measured impact of base blinding as "small (a few percent)", which is the same order. Now the list that matters, the quantities an attacker can correlate with the key:

| observable | without blinding | with base blinding |
|---|---|---|
| the input of the exponentiation | the chosen $c$ | $c r^e \bmod N$, uniform and unknown |
| extra Montgomery reductions in the first squarings | a function of $c$ and of $p$, so the time of a chosen $c$ reveals where $c$ sits with respect to $p$ | a function of a fresh random value |
| repeated queries with the same $c$ | the same trace every time, so averaging removes the noise | a new input every time, so averaging removes the signal |
| a fault in one CRT half | $\gcd(s'^e - m, N) = p$ with the known $m$ | the attacker does not know the blinded input, so the gcd is 1 |
| the square-and-multiply pattern | a function of $d$ only, and it repeats | a function of $d$ only, and it repeats |

The last row is the limit of the technique. Base blinding makes the *data* random; it does nothing about the *exponent*, so a trace that shows the shape of the computation still reveals bits of $d$. That is the job of exponent blinding and of constant-time exponentiation.

## Classic examples

- **The OpenSSL fix of 2003.** [Brumley and Boneh](/timing-attack/) recovered an RSA factor from a network service by timing SSL handshakes, using the Montgomery extra reductions and the switch between multiplication routines, both of which depend on the ciphertext. OpenSSL had `RSA_blinding_on` already, but TLS servers could not reach it, so the advisory of 17 March 2003 switched blinding on for every key. The attack needed about a million queries with the same chosen ciphertexts; with blinding those queries all run on different numbers.
- **The Bellcore fault attack.** The [RSA CRT fault attack](/rsa-fault-attack/) needs the message $m$ that matches the faulty signature $s'$, because the factor comes out of $\gcd(s'^e - m, N)$. Blinding the input of a [signature](/rsa-signature/) means the signer exponentiates a value the attacker cannot compute, so the gcd gives nothing. Blinding is a cheap second line behind the real countermeasure, which is to verify the signature before it leaves the device.
- **Scalar blinding on elliptic curves.** The same idea in the additive group: replace the secret scalar $k$ by $k + t n$ for a random $t$ and the group order $n$, and randomize the projective representation of the input point. [Elliptic curve cryptography](/elliptic-curve-cryptography/) implementations such as the ones behind [ECDH](/ecdh/) use both.
- **Blind signatures, the same algebra for the other side.** In a [Chaum blind signature](/chaum-blind-signature/) the *client* sends $m r^e$ and divides the answer by $r$, so that the *signer* never sees $m$. The computation is the one on this page; the party that draws $r$ and the property that is wanted are different. Do not mix up the two.

## Variations

- **Base blinding, or message blinding.** The template above. Randomizes the data.
- **Exponent blinding.** $d' = d + t \lambda(N)$, or $d_p' = d_p + t_1 (p-1)$ and $d_q' = d_q + t_2 (q-1)$ in the CRT. A random $t$ of 32 or 64 bits is the usual choice. Randomizes the operation sequence.
- **Modulus blinding.** Work modulo $rN$ for a small random $r$, then reduce modulo $N$ at the end. This randomizes the intermediate values of the reduction and adds a check: the result modulo $r$ can be verified. It is used against fault attacks.
- **Exponent splitting.** Write $d = d_1 + d_2$ with a random $d_1$, and compute $c^{d_1} c^{d_2}$. This doubles the work and is used when the exponent must never appear in memory as one value.
- **Additive and multiplicative masking of the CRT recombination.** Garner's formula leaks through its subtraction and its multiplication by $q^{-1}$; the masked versions randomize both.
- **Re-randomization inside Montgomery form.** Multiply the Montgomery representation by a random $u$ and divide the result by $u$ at the end, so that even the representation of the same value changes between runs.

## Pitfalls

- **Blinding is not constant time.** It hides the data, not the code path. A sliding-window exponentiation with blinding still reads a table at indexes that come from $d$, which is what the cache attacks of Percival (2005) and the Flush+Reload work of 2014 read out. Use blinding *and* a constant-time exponentiation.
- **A weak random source removes the protection.** If the attacker can predict $r$, the attacker can compute the blinded input, and every data-dependent leak is back. The squaring update of the cached pair makes the values of one chain related, so a single leaked $r$ exposes the rest of that chain; this is why the pair is refreshed.
- **Exponent blinding alone is not enough.** Schindler (CHES 2015) showed that a timing attack can still work when only the exponent is blinded, if the number of random bits is small. Blind the base as well.
- **Blind before the CRT split and unblind after the recombination.** If the implementation blinds inside each half, or unblinds before the final multiplication, the known input is still present where it matters.
- **The blinded value must not leak through the error path.** If the code returns different errors for a blinded value that is 0 or that shares a factor with $N$, the error itself is an oracle. Reject nothing: $c = 0$ and $\gcd(c, N) > 1$ have the correct answers anyway with $d' = d + t\lambda(N)$.
- **Blinding does not fix a bad padding scheme.** A [padding oracle](/padding-oracle-attack/) reads the output of the decryption, not its timing. Bleichenbacher's attack works just as well against a blinded implementation. Use [OAEP](/rsa-oaep/) or a [KEM](/key-encapsulation-mechanism/) for that.
- **Do not reuse the blinding factor across keys or across processes.** The pair belongs to one key and one modulus, and a shared cache needs a lock.
- **It is not a blind signature.** The goal here is to hide the input from an observer of the machine, not from the key holder.

## Exercises

1. Show that $(c r^e)^d \equiv c^d r \pmod N$ for every $c$ and every $r$, including the ones with $\gcd(c, N) > 1$. Where is $ed \equiv 1 \pmod{\lambda(N)}$ used, and why is $\varphi(N)$ in place of $\lambda(N)$ also sound?
2. The cached pair is updated by $A \leftarrow A^2$ and $A_i \leftarrow A_i^2$. Prove that the relation $A \equiv (A_i^{-1})^e$ is kept, so the unblinding stays correct. How many uses of one chain give the attacker an advantage, if one blinded input is ever revealed?
3. Count the modular multiplications of the table above for a 3072-bit modulus with $e = 3$, and give the overhead of base blinding. Does a smaller $e$ make blinding cheaper or dearer, in relative terms?
4. An implementation blinds the input but reports an error when the blinded value is not coprime to $N$. Describe the oracle this gives, and the factor it leaks.

## References
