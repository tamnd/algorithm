---
tag: MG2E7C
kind: concept
slug: small-subgroup-attack
name: Small subgroup attack
area: cryptography/key-exchange
level: advanced
summary: An attacker sends group elements of small order in place of a Diffie-Hellman public key. The answers leak the secret key modulo small primes, and the CRT joins the pieces.
prereqs: [diffie-hellman, pohlig-hellman, chinese-remainder-theorem]
see_also: [diffie-hellman, ecdh, x25519, pohlig-hellman, safe-prime, man-in-the-middle-attack, discrete-logarithm-problem, computational-diffie-hellman]
sources:
  - paper: doi:10.1007/BFb0052240
    title: Chae Hoon Lim and Pil Joong Lee, A key recovery attack on discrete log-based schemes using a prime order subgroup, CRYPTO 1997, LNCS 1294, pages 249 to 263
    locator: the key recovery attack on Diffie-Hellman with a static key in a prime-order subgroup of Z_p^* when p - 1 has small factors, and the proposed countermeasures
  - paper: doi:10.1007/3-540-68339-9_29
    title: Paul C. van Oorschot and Michael J. Wiener, On Diffie-Hellman key agreement with short exponents, EUROCRYPT 1996, LNCS 1070, pages 332 to 343
    locator: the attack that combines Pohlig-Hellman on the small factors of p - 1 with a search for a short exponent
  - url: "https://www.rfc-editor.org/rfc/rfc2785"
    title: Robert Zuccherato, RFC 2785, Methods for Avoiding the Small-Subgroup Attacks on the Diffie-Hellman Key Agreement Method for S/MIME, March 2000
    locator: Section 1.2 (brief description of the attack), Section 3.1 (public key validation, y^q mod p = 1), Sections 3.3 to 3.5 (choice of p and cofactor exponentiation)
  - url: "https://eprint.iacr.org/2016/995"
    title: Luke Valenta, David Adrian, Antonio Sanso, Shaanan Cohney, Joshua Fried, Marcella Hastings, J. Alex Halderman and Nadia Heninger, Measuring small subgroup attacks against Diffie-Hellman, NDSS 2017
    locator: the measurements of non-safe-prime groups, missing validation and exponent reuse in TLS, SSH and IPsec, and the OpenSSL case CVE-2016-0701
  - paper: doi:10.1007/3-540-36288-6_16
    title: Adrian Antipa, Daniel Brown, Alfred Menezes, René Struik and Scott Vanstone, Validation of elliptic curve public keys, PKC 2003, LNCS 2567
    locator: the invalid-curve attack on ECDH, and the public key validation that stops it
  - url: "https://csrc.nist.gov/pubs/sp/800/56/a/r3/final"
    title: Elaine Barker, Lily Chen, Allen Roginsky, Apostol Vassilev and Richard Davis, NIST SP 800-56A Rev. 3, Recommendation for Pair-Wise Key-Establishment Schemes Using Discrete Logarithm Cryptography, April 2018
    locator: Section 5.6.2.3 (assurance of public key validity, with the full validation of FFC and ECC public keys)
---

A small subgroup attack is an active attack on [Diffie-Hellman](/diffie-hellman/) in which the attacker sends, in place of a public key, a group element of small order, and learns the victim's secret exponent modulo that order from the victim's reply. Repeated with elements of several small prime orders, it gives the secret modulo each prime, and the [Chinese remainder theorem](/chinese-remainder-theorem/) joins the pieces, as in the [Pohlig-Hellman](/pohlig-hellman/) algorithm. Lim and Lee described it in 1997 for groups where $p - 1$ has small factors. The defences are to validate every received element, to use a group with no small subgroups such as a [safe prime](/safe-prime/) group, or to use a curve built to make all inputs safe, such as [X25519](/x25519/).

**Notation.** $p$ is a prime and $g$ generates a subgroup of prime order $q$ of $\mathbb{Z}_p^*$, so $q \mid p - 1$. The victim has a static secret $x$ with $1 \le x < q$. $\ell$ denotes a small prime factor of $p - 1$ with $\ell \ne q$, and $h_\ell$ an element of order $\ell$. $\mathrm{tag}(Z)$ is any reply that the victim computes from the shared value $Z$, such as a MAC under a key derived from $Z$.

## In plain words

In Diffie-Hellman, each side sends a number and the other side raises it to a secret power. If the number comes from a small cycle, raising it to any power lands on one of only a few values.

So the attacker sends a number from a cycle of length 7. The victim's reply depends on which of the 7 values it got, and the attacker tries all 7 to find a match. That tells her the remainder of the secret when divided by 7.

She does the same with cycles of length 3, 5, 11, 13 and so on, until the product of the lengths is larger than the secret. Then the remainders fix the secret. The victim could stop all of this with a single check that each received number is in the right group.

## The idea

**Why it works.** If $h_\ell$ has order $\ell$, then $h_\ell^x = h_\ell^{x \bmod \ell}$, so the victim's shared value is one of only $\ell$ values. If the victim answers with $\mathrm{tag}(h_\ell^x)$, the attacker computes $\mathrm{tag}(h_\ell^t)$ for $t = 0, 1, \dots, \ell - 1$ and finds $t = x \bmod \ell$. Elements of order $\ell$ exist exactly when $\ell \mid p - 1$: raise a random element to the power $(p - 1)/\ell$, and retry if the result is 1.

```pseudo id=main
SMALL-SUBGROUP-ATTACK(p, ℓ_1, …, ℓ_r)       ▷ ℓ_i are small primes that divide p − 1
L1  for i ← 1 to r do
L2      h ← an element of order ℓ_i           ▷ h = y^((p − 1)/ℓ_i) mod p with h ≠ 1
L3      c ← the victim's reply to the public key h
L4      x_i ← the t in {0, …, ℓ_i − 1} with tag(h^t) = c
L5  return x mod ℓ_1 ⋯ ℓ_r from the x_i, by the CRT
```

If $\ell_1 \cdots \ell_r > q$, line L5 gives $x$ itself. The attack makes $r$ queries and about $\ell_1 + \dots + \ell_r$ exponentiations. If the product is smaller than $q$, the attacker still learns $x \bmod \ell_1 \cdots \ell_r$, and can find the rest with a [kangaroo](/pollard-kangaroo/) or [baby-step giant-step](/baby-step-giant-step/) search in time about $\sqrt{q / (\ell_1 \cdots \ell_r)}$, given the victim's public key $g^x$.

**What the victim must have done wrong.** The attack needs three things: a static (or reused) secret $x$, a group in which $p - 1$ has small factors besides $q$, and no check that the received element lies in the subgroup of order $q$. An ephemeral secret used once leaks only a few bits that are then thrown away. In a safe prime group, $p = 2q + 1$, the only small subgroups have order 1 and 2, so at most one bit, $x \bmod 2$, leaks.

**Defences.**

- **Full validation.** Check $2 \le y \le p - 2$ and $y^q \equiv 1 \pmod p$ (RFC 2785, Section 3.1; SP 800-56A, Section 5.6.2.3). This costs one exponentiation.
- **A group without small subgroups.** With a safe prime, the range check $2 \le y \le p - 2$ removes the elements of order 1 and 2; RFC 7919 groups are safe primes.
- **Cofactor exponentiation.** Raise to $j x$, where $j = (p - 1)/q$, so that any component outside the subgroup of order $q$ is killed (RFC 2785, Sections 3.4 and 3.5); abort if the result is 1.
- **Ephemeral keys.** Use a fresh $x$ for each exchange.

**On elliptic curves.** A curve with cofactor $h > 1$ has points of order dividing $h$; [X25519](/x25519/) clamps the scalar to a multiple of 8, so such points give the output 0. The stronger form is the invalid-curve attack: an implementation that does not check that a received point is on the curve can be fed points on another curve with the same $a$ but a different $b$, chosen to have a small-order point; the addition formulas do not use $b$, so the victim computes on the wrong curve (Antipa et al., 2003). [ECDH](/ecdh/) public key validation, or the x-only ladder on a twist-secure curve, stops it.

## Examples

**One bit by hand.** Take $p = 23$, $q = 11$ and $g = 2$, which has order 11. The victim's secret is $x = 7$. The attacker sends $h = 22 = -1$, of order 2. The victim computes $22^7 = -1 = 22$, while $x$ even would give 1, so the reply shows that $x$ is odd. This is the one bit that any group of even order $p - 1$ leaks without validation.

**Full recovery in a toy group.** The Python code of this page uses $q = 16777289$, a prime near $2^{24}$, and $p = 2q \cdot 111546435 + 1 = 3742893553829431$, where $111546435 = 3 \cdot 5 \cdot 7 \cdot 11 \cdot 13 \cdot 17 \cdot 19 \cdot 23$. The victim answers each element $h$ with SHA-256 of $h^x$. The attacker sends eight elements, one of each small prime order, tries at most $3 + 5 + \dots + 23 = 98$ exponents in all, and since $111546435 > q$, the CRT gives $x$ exactly. When the victim checks $h^q \equiv 1$, the first query is rejected. In the safe-prime group $p = 140737488356903 = 2q + 1$, without validation the attack can only learn $x \bmod 2$, and with validation the elements of order 2 and $2q$ are rejected. The code is for study only: the groups are tiny, nothing is constant time, and the victim is a local simulation.

**OpenSSL, 2016.** Valenta et al. found that OpenSSL reused DH exponents with the RFC 5114 groups, whose $p - 1$ has small factors, and did not check the subgroup; together these allowed a small subgroup attack on the server key (CVE-2016-0701). OpenSSL then added the check.

## Where it is used

- **Protocol design.** Every DH standard now states a validation rule: RFC 2785 for S/MIME, SP 800-56A for NIST schemes, and the TLS 1.3 rule (RFC 8446, Section 4.2.8.1) that a peer's finite field share must satisfy $1 < Y < p - 1$, in safe prime groups.
- **Choice of groups.** The attack is one reason to prefer safe prime groups (RFC 3526, RFC 7919) over DSA-style groups such as those of RFC 5114, and to prefer twist-secure curves such as Curve25519 and Curve448.
- **Static Diffie-Hellman.** Schemes with long-term DH keys, such as ECIES servers, [MQV](/mqv/) and the static keys of [Noise](/noise-protocol-framework/), depend on validation or on curves that make it automatic.
- **Analysis of the static DH oracle.** The attack is a concrete case of the general rule that a party who computes $y \mapsto y^x$ for attacker-chosen $y$ gives an oracle that may leak $x$.

## References
