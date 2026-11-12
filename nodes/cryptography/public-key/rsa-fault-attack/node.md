---
tag: YCAWG0
kind: algorithm
slug: rsa-fault-attack
name: RSA fault attack on CRT
aliases:
- Bellcore attack
- Boneh-DeMillo-Lipton attack
area: cryptography/public-key
level: research
summary: One faulty RSA-CRT signature of a known message factors the modulus with a single gcd. The fix is to verify the signature before it leaves the device.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus, t: the number of binary digits of the public exponent}
  time: {worst: Θ(t b^2), average: Θ(t b^2), best: Θ(t b^2)}
  space: {extra: Θ(b)}
properties: {deterministic: true, randomized: false}
history:
  year: 1997
  people: [Dan Boneh, Richard A. DeMillo, Richard J. Lipton, Arjen K. Lenstra]
  note: Boneh, DeMillo and Lipton presented the attack at Eurocrypt 1997; the work was done at Bellcore, which gave it its other name. Lenstra's 1996 memo reduced it to one gcd with the public key alone.
prereqs: [rsa-cryptosystem, chinese-remainder-theorem]
see_also: [rsa-signature, rsa-blinding, timing-attack, rsa-problem, integer-factorization, batch-gcd, rsa-pss]
sources:
  - paper: "Dan Boneh, Richard A. DeMillo and Richard J. Lipton, On the importance of checking cryptographic protocols for faults, EUROCRYPT 1997, LNCS 1233, pages 37 to 51"
    locator: Sections 2 and 3 (the attack on RSA with the Chinese remainder theorem, and the attacks on Fiat-Shamir and Schnorr identification)
  - paper: doi:10.1007/s001450010016
    title: Dan Boneh, Richard A. DeMillo and Richard J. Lipton, On the importance of eliminating errors in cryptographic computations, Journal of Cryptology 14(2), pages 101 to 119, 2001
    locator: Section 2 (the journal version, with the register fault model and the two faulty signature variant)
  - paper: "Arjen K. Lenstra, Memo on RSA signature generation in the presence of faults, 25 September 1996, reprinted in Marc Joye and Michael Tunstall, editors, Fault Analysis in Cryptography, Springer 2012"
    locator: "the one page memo: one faulty signature and the public key give gcd(s'^e - m, N)"
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: "Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1, RSA Cryptography Specifications Version 2.2, 2016"
    locator: Section 3.2 (the CRT private key quintuple) and Section 5.2.1 (RSASP1, which is the operation that is attacked)
  - paper: doi:10.1007/s001459900055
    title: Marc Joye, Arjen K. Lenstra and Jean-Jacques Quisquater, Chinese remaindering based cryptosystems in the presence of faults, Journal of Cryptology 12(4), pages 241 to 245, 1999
    locator: the whole paper (the attack when the padded message is only partly known, and the countermeasure discussion)
  - url: "https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/razavi"
    title: Kaveh Razavi, Ben Gras, Erik Bosman, Bart Preneel, Cristiano Giuffrida and Herbert Bos, Flip Feng Shui, hammering a needle in the software stack, USENIX Security Symposium 2016
    locator: Sections 5 and 6 (Rowhammer bit flips in a co-hosted virtual machine, and the attack on an RSA public key in a page cache)
---

The Bellcore attack turns one wrong bit into the factorization of an RSA modulus. A device that signs with the [Chinese remainder theorem](/chinese-remainder-theorem/) computes two halves, $s_p = m^{d_p} \bmod p$ and $s_q = m^{d_q} \bmod q$, and glues them together. If a fault hits one half and the device publishes the result $s'$, then $s'$ is still correct modulo the other prime, so that prime divides $s'^e - m$ and it divides $N$. One greatest common divisor gives it, and with it the private key. Boneh, DeMillo and Lipton published this in 1997, and Lenstra had already reduced it to the single gcd with public data only. The countermeasure is one line: verify the signature before it leaves the device.

**Notation.** $N = pq$ is the modulus, $e$ the public exponent, $d$ the private exponent, $d_p = d \bmod (p-1)$ and $d_q = d \bmod (q-1)$ the CRT exponents, $q^{-1} \bmod p$ the Garner coefficient, $m$ the message representative with $0 \le m < N$, $s = m^d \bmod N$ the correct signature and $s'$ the faulty one.

## In plain words

A smart card signs with a short cut: it does the work twice with the two secret primes, each half the size, and then glues the halves together. This is about four times faster than the direct way.

Now make the card slip once. Heat it, starve its power supply, flash a light at the chip, or hammer its memory from another program. One wrong bit in one half is enough. The card glues a broken half to a good half and hands out the answer.

That answer is right for one of the two secret primes and wrong for the other. Anybody who has it, together with the message and the public key, can find the prime that was handled correctly with one simple school computation, and from the primes comes the whole private key.

So a device must never publish a result it has not checked.

## The problem

The attack solves [integer factorization](/integer-factorization/) for this one modulus, with the help of a faulty output. The attacker is given the public key $(N, e)$, a message $m$, and one value $s'$ that the signer produced for $m$ while a fault was present in one CRT half. The goal is $p$, $q$ and $d$. Nothing about the shape of the fault needs to be known: not which bit, not which half, not how many bits inside one half.

The model is the one of Boneh, DeMillo and Lipton: a *register fault*, which changes the value of one intermediate variable at one moment, with the rest of the computation running normally on the changed value. In practice faults come from voltage glitches, clock glitches, temperature, laser or light pulses on a decapped chip, and from Rowhammer in a shared machine.

## The algorithm

```pseudo id=main
BELLCORE-ATTACK(N, e, m, s')
L1  if s'^e mod N = m mod N then return FAILURE      ▷ the signature is correct
L2  g ← gcd((s'^e - m) mod N, N)
L3  if g = 1 or g = N then return FAILURE            ▷ both halves were faulty
L4  r ← N / g                                        ▷ g and r are the two primes
L5  d ← e^{-1} mod lcm(g - 1, r - 1)
L6  return (g, r, d)
```

**The walk-through.** Line 1 is the sanity check: if the output verifies, no fault happened and there is nothing in it. Line 2 is the whole attack. The faulty signature agrees with the correct one modulo the prime whose half was computed correctly, call it $r$; so $s'^e \equiv m \pmod r$ and $r$ divides both $s'^e - m$ and $N$. It does *not* agree modulo the other prime, except by accident, so the gcd is exactly $r$ and not $N$. Line 3 catches the two cases where the gcd says nothing: a fault in both halves, which leaves no good half, and the accident where the faulty half still gives $s'^e \equiv m$ modulo the bad prime, whose probability is about $1/p$. Line 4 divides. Line 5 rebuilds the private exponent from the factors, which is the key generation step of [RSA](/rsa-cryptosystem/) run backwards. The reduction modulo $\mathrm{lcm}(g-1, r-1)$ gives the smallest such $d$; any $d$ with $ed \equiv 1$ modulo that value works.

The signer that is attacked, and the two countermeasures, are three more short procedures.

```pseudo id=signer
SIGN-CRT(m, p, q, d_p, d_q, qInv)
L1  s_p ← m^{d_p} mod p
L2  s_q ← m^{d_q} mod q
L3  h ← (s_p - s_q) * qInv mod p                     ▷ Garner recombination
L4  return (s_q + q*h) mod N

SIGN-CRT-VERIFIED(m, ...)                            ▷ countermeasure 1
L5  s ← SIGN-CRT(m, ...)
L6  if s^e mod N ≠ m mod N then return ERROR         ▷ never publish an unchecked value
L7  return s

SIGN-CRT-SHAMIR(m, ..., r)                           ▷ countermeasure 2, r a small prime
L8  s_p* ← m^d mod (p*r); s_q* ← m^d mod (q*r)
L9  if s_p* mod r ≠ s_q* mod r then return ERROR     ▷ both are m^d mod r
L10 return GARNER(s_p* mod p, s_q* mod q)
```

## Example

A key small enough to check by hand: $p = 61$, $q = 53$, so $N = 3233$, with $e = 17$. Then $\lambda(N) = \mathrm{lcm}(60, 52) = 780$ and $d = 17^{-1} \bmod 780 = 413$, so $d_p = 413 \bmod 60 = 53$, $d_q = 413 \bmod 52 = 49$ and $q^{-1} \bmod p = 38$.

Sign $m = 65$.

| step | correct run | faulty run |
|---|---|---|
| $s_p = 65^{53} \bmod 61$ | 39 | 38, one flipped bit |
| $s_q = 65^{49} \bmod 53$ | 5 | 5 |
| recombination | $s = 588$ | $s' = 1807$ |
| verification $s^e \bmod N$ | $588^{17} \equiv 65$, correct | $1807^{17} \equiv 1867 \ne 65$ |

The attack now computes $s'^e - m = 1867 - 65 = 1802$ and

$$\gcd(1802, 3233) = 53 = q ,$$

because $1802 = 2 \cdot 17 \cdot 53$. The fault was in the half modulo $p$, so the prime that comes out is $q$, the one whose half was right. Dividing gives $p = 3233/53 = 61$, and $d = 17^{-1} \bmod 780 = 413$. The key is gone.

The test file runs the same attack on a toy key with two primes of 128 binary digits,

$$p = 273864138845241657029075268143536711069, \qquad q = 173710947069375085680776429514357002701,$$

for 20 random messages with one flipped bit at a random position in a random half, and it recovers both primes every time. It also checks the three failure cases of lines 1 and 3, and that both countermeasures turn the faulty run into an error.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The statement is that if $s' \equiv m^d \pmod r$ for exactly one prime $r \in \{p, q\}$ of $N$, and $s'^e \not\equiv m$ modulo the other one, then line 2 returns $r$, and the pair $(g, N/g)$ is the factorization. The only probabilistic part is the phrase "and not modulo the other one": for a fault that lands on a uniform wrong value, the chance that the wrong half still satisfies $s'^e \equiv m$ modulo the bad prime is about $1/p$, which for a real key is below $2^{-500}$.

## Complexity

One exponentiation with the public exponent and one gcd. With schoolbook arithmetic on $b$ binary digits and a public exponent of $t$ binary digits, the exponentiation is $\Theta(t b^2)$ and the gcd is $\Theta(b^2)$, so the attack costs $\Theta(t b^2)$. For $b = 2048$ and $e = 65537$ this is 17 squarings, one multiplication and one gcd: a few microseconds. Line 5 adds one modular inverse, also $\Theta(b^2)$.

The cost of the *physical* part is the whole cost in practice. The attacker needs one fault in the right window, which is a laboratory task on a card and a Rowhammer task on a server, and one signature of a message that is known.

| variant | faulty signatures needed | other data needed |
|---|---|---|
| Lenstra 1996, the one on this page | 1 | $m$ and the public key |
| Boneh, DeMillo and Lipton 1997, first form | 1 | $m$ and the correct signature $s$, then $\gcd(s - s', N)$ |
| Boneh, DeMillo and Lipton 1997, no message | 2 faulty signatures of the same unknown $m$ | the public key |
| Joye, Lenstra and Quisquater 1999 | 1 | a partly known padded message, and a search over the unknown part |

## Properties

- **Deterministic.** Given the inputs, the attack is a gcd. There is no search and no probability of failure beyond the $1/p$ accident above.
- **It needs the CRT.** A signer that computes $m^d \bmod N$ directly is not open to this attack; a fault there gives a wrong signature and no factor, because $s'^e - m$ is then a random number modulo $N$ with no common factor. CRT signing is about four times faster, so almost every implementation uses it, and almost every implementation needs the countermeasure.
- **The fault can be anywhere in one half.** Any number of wrong bits, in the exponent $d_p$, in the modulus used for the half, in an intermediate square, or in the stored $s_p$, all give the same equation. This is why the attack is robust and why "my fault model is more realistic" rarely saves an implementation.
- **It breaks signatures and decryption alike.** The target is the private operation $x \mapsto x^d \bmod N$, so a decryption that returns a faulty plaintext for a known ciphertext leaks the same way. For decryption the attacker usually does not know the plaintext, which is why the signature case is the famous one.
- **Padding does not stop it.** With deterministic padding such as [full domain hash](/rsa-fdh/) the attacker knows $m$ exactly, so the attack applies as written. Randomized padding such as [PSS](/rsa-pss/) hides part of $m$, which moves the attack to the Joye, Lenstra and Quisquater form or to the two signature form, so it slows the attacker and does not stop the attack.

## Variants and improvements

- **The difference form.** With both the correct and the faulty signature of the same message, $\gcd(s - s', N)$ is the good prime, with no exponentiation at all. This was the original statement, and it needs the device to sign the same message twice.
- **Two faulty signatures, unknown message.** From $s_1'$ and $s_2'$ with faults in *different* halves of the same unknown $m$, the value $s_1'^e - s_2'^e$ is divisible by neither prime, but $\gcd(s_1' - s_2', N)$ is not 1 when the faults hit the same half, which gives a factor after a few tries. The journal version of 1997 gives this form, which needs no knowledge of $m$.
- **Faults in the recombination.** A fault in $h$ or in the final addition gives a signature that is wrong modulo both primes. A fault in the stored $q^{-1}$ still leaves $s' \equiv s_q \pmod q$, so the gcd works.
- **Faults in the public modulus.** Flipping bits of $N$ in memory before a verification turns a verifier into an oracle; Flip Feng Shui (2016) used Rowhammer to do this to a public key file in a co-hosted virtual machine.
- **Safe-error attacks.** A countermeasure that only *detects* a fault still leaks: the attacker learns whether the fault changed anything, which for a square-and-multiply loop says whether a dummy operation was used, and so names an exponent bit. A detecting countermeasure must therefore also hide the detection.

## When to use it

As an attack, it belongs to a security evaluation of a device that holds an RSA key and can be made to slip: smart cards, hardware security modules, secure elements, TPMs, and any signing service in a shared machine. The practical questions are how a fault is injected and whether the device publishes unchecked output.

As a defender, the rules are short:

1. **Verify before output.** Compute $s^e \bmod N$ and compare with $m$. With $e = 65537$ this adds about 17 multiplications to a signature that costs thousands, so it is under one percent. This is the standard countermeasure, and RFC 8017 implementations that follow the guidance do it.
2. **If the public exponent is not available**, use Shamir's trick or one of its infective descendants, which check the two halves against each other modulo a small random prime.
3. **Blind the input** as well; see [RSA blinding](/rsa-blinding/). The attack needs the message that matches the faulty output, and a blinded signer exponentiates a value the attacker cannot compute.
4. **Do not return a partial result on an error.** One error value, no debugging output, and a counter that locks the device after repeated faults.

## Pitfalls

- **Verifying with a faulty modulus.** If the verification reads the same memory that the fault can reach, a single fault can corrupt both the signature and the check. Keep a separate copy of $N$ and $e$, or recompute them.
- **A second fault defeats the check.** An attacker who can inject two faults can break the signature and then break the comparison. Devices therefore also randomize the time of the check and count failures.
- **Checking only the halves.** Comparing $s_p$ against a recomputed $s_p$ doubles the work and still misses a fault in the recombination. The public-key check covers the whole computation.
- **Shamir's trick is not complete.** It does not cover a fault in the recombination that happens after the comparison, and it needs $d$, not only $d_p$ and $d_q$, unless one of its later variants is used.
- **Assuming a fault is hard.** Rowhammer makes bit flips a software problem in a shared machine, and an unprivileged program can flip a bit in another tenant's memory. The paper of 2016 is the citation.
- **Reusing a faulty output in a protocol.** A device that caches a signature and sends it twice gives the attacker both forms of the attack.
- **This is not a break of RSA.** The modulus, the padding and the exponent are all fine. The attack is against an implementation that publishes an unchecked result, which is why the countermeasure is so cheap.

**The code of this page is for study only.** The signatures are raw RSA with no padding, the key is a toy, the code is not constant time, and the "fault" is a function argument in the same process, not an attack on any device.

## Implementations

## History

Richard Lipton and his colleagues at Bellcore found in 1996 that an error in a cryptographic computation is not only a bug but a key recovery channel. Boneh, DeMillo and Lipton circulated the result in September 1996 and presented it at Eurocrypt 1997 under the title "On the importance of checking cryptographic protocols for faults", with attacks on RSA with the CRT, on Rabin signatures, on Fiat-Shamir and on Schnorr identification. The journal version of 2001 carries the fuller fault model.

Arjen Lenstra's memo of 25 September 1996, one page long, is the form everyone uses: the single gcd that needs only the public key and the message. Joye, Lenstra and Quisquater extended the attack in 1999 to the case where the padded message is only partly known, which answered the hope that padding alone would be a countermeasure.

The field that grew out of this is fault analysis, which now covers differential fault analysis on AES (Biham and Shamir 1997, Piret and Quisquater 2003), attacks on elliptic curve scalar multiplication, and the safe-error attacks that read out the countermeasures themselves. On the other side, the 2016 Flip Feng Shui work and the Rowhammer line that led to it moved fault injection from a laboratory bench to a rented virtual machine, which is why the cheap check at the end of a signature is still worth writing.

## References
