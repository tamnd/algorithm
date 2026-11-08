---
tag: E3TY1F
kind: algorithm
slug: dual-ec-drbg
name: Dual_EC_DRBG
aliases:
- Dual Elliptic Curve Deterministic Random Bit Generator
- Dual EC
area: numerical/random-number-generation
level: advanced
summary: A withdrawn NIST generator that steps a secret s by s = x(sP) and outputs most of x(sQ); anyone who knows e with P = eQ recovers the state from about 32 output bytes.
model: word-ram
complexity:
  vars: {m: the number of output blocks in one request, ℓ: the base 2 logarithm of the field prime, w: the word size}
  time: {worst: Θ(m ℓ^3 / w^2)}
  space: {extra: Θ(ℓ / w)}
properties: {deterministic: true, recursive: false, cryptographic: true}
history:
  year: 2006
  people: [Elaine Barker, John Kelsey, Dan Shumow, Niels Ferguson]
  note: Standardized in NIST SP 800-90 (2006) after ANSI X9.82 drafts; Shumow and Ferguson described the possible backdoor in 2007; NIST recommended against it in 2013 and removed it in SP 800-90A Revision 1 (2015).
prereqs: [cryptographically-secure-prng, elliptic-curve-cryptography, elliptic-curve-discrete-logarithm-problem]
see_also: [hash-drbg, hmac-drbg, ctr-drbg, blum-micali, computational-diffie-hellman, trapdoor-one-way-function, entropy-source, pseudorandom-generator]
sources:
  - paper: doi:10.6028/NIST.SP.800-90A
    title: Elaine Barker and John Kelsey, NIST Special Publication 800-90A, Recommendation for Random Number Generation Using Deterministic Random Bit Generators, January 2012
    locator: Section 10.3.1 (Dual_EC_DRBG instantiate, reseed and generate), Section 10.4.1 (Hash_df), Appendix A.1 (the points P and Q for P-256, P-384 and P-521) and Appendix A.2 (generating alternative points)
  - paper: doi:10.6028/NIST.SP.800-90Ar1
    title: Elaine Barker and John Kelsey, NIST Special Publication 800-90A Revision 1, Recommendation for Random Number Generation Using Deterministic Random Bit Generators, June 2015
    locator: Appendix on revisions (removal of Dual_EC_DRBG)
  - paper: "Dan Shumow and Niels Ferguson, On the possibility of a back door in the NIST SP800-90 Dual Ec Prng, rump session talk at CRYPTO 2007"
    locator: the observation that knowing e with P = eQ lets one recover the state from one output block, and the suggestion to generate Q verifiably at random
  - paper: "Berry Schoenmakers and Andrey Sidorenko, Cryptanalysis of the dual elliptic curve pseudorandom generator, Cryptology ePrint Archive, Report 2006/190, 2006"
    locator: the distinguisher showing that the truncated x coordinates are measurably biased
  - paper: "Daniel R. L. Brown and Kristian Gjøsteen, A security analysis of the NIST SP 800-90 elliptic curve random number generator, CRYPTO 2007, Lecture Notes in Computer Science 4622, Springer, 2007"
    locator: the reduction of pseudorandomness to the decisional Diffie-Hellman problem and two further assumptions, under the hypothesis that Q is chosen independently at random
  - paper: "Stephen Checkoway, Matthew Fredrikson, Ruben Niederhagen, Adam Everspaugh, Matthew Green, Tanja Lange, Thomas Ristenpart, Daniel J. Bernstein, Jake Maskiewicz and Hovav Shacham, On the practical exploitability of Dual EC in TLS implementations, 23rd USENIX Security Symposium, 2014"
    locator: the attacks on RSA BSAFE, Windows SChannel and OpenSSL-FIPS with a replaced point Q
  - paper: "Daniel J. Bernstein, Tanja Lange and Ruben Niederhagen, Dual EC: a standardized back door, in The New Codebreakers, Lecture Notes in Computer Science 9100, Springer, 2016"
    locator: the history of the standardization and of the public warnings
  - url: https://github.com/openssl/openssl/blob/OpenSSL-fips-2_0/fips/rand/fips_drbg_selftest.h
    title: OpenSSL FIPS Object Module 2.0, DRBG self-test data
    locator: the Dual_EC_DRBG known-answer data for P-256 with SHA-1 and SHA-256, used by the tests
---

Dual_EC_DRBG is a pseudorandom generator built on elliptic curves that NIST standardized in SP 800-90 in 2006, recommended against in 2013 and removed in 2015. Its state is a number $s$; each step computes $s \leftarrow x(sP)$ and outputs the low 240 bits of $x(sQ)$, where $P$ and $Q$ are two fixed points of the curve P-256. The design invites a reduction to the elliptic curve Diffie-Hellman problem, and it is about a thousand times slower than the other DRBGs of SP 800-90A. Its flaw is structural: whoever knows the number $e$ with $P = eQ$ can turn one output block into the next internal state and predict all later output. The standard fixed $Q$ without saying where it came from, so nobody outside could rule out that such an $e$ was known. Separately, the output is slightly biased because too few bits are discarded.

## In plain words

The generator keeps a secret number. To make output it multiplies a fixed point $Q$ on an elliptic curve by the secret number, takes the first coordinate of the result, drops its top two bytes and hands out the rest. To move on, it multiplies a different fixed point $P$ by the secret number and uses the first coordinate as the new secret. Recovering the secret from the output is believed hard, because that would mean solving a discrete logarithm problem.

But suppose someone knows a number $e$ with $P = eQ$. That person can take an output, guess the two dropped bytes, rebuild the curve point, multiply it by $e$, and read off the next secret. Two more output bytes check the guess, and from then on everything is predictable. Such an $e$ exists for any pair of points; the question is who knows it.

## The problem

Build a pseudorandom generator whose security reduces to a number-theoretic problem, in the spirit of the [Blum-Micali generator](/blum-micali/), but on an elliptic curve and producing many output bits per step. The standard needed concrete parameters, fixed points, and compatibility with the instantiate, reseed and generate interface of SP 800-90.

In the notation of generators, the state is $s \in \{0, \ldots, 2^{256} - 1\}$, the transition is $f(s) = x(sP)$, and the output of a step is $g(s) = x(sQ) \bmod 2^{240}$, where $x(R)$ is the $x$ coordinate of the point $R$ read as an integer. The cost model counts word operations on 256-bit field elements.

**Parameters (SP 800-90A, 2012, Section 10.3.1 and Appendix A.1).** Three NIST prime curves are allowed. For P-256, the security strength is at most 128, $\mathit{seedlen} = 256$, and $\mathit{outlen} = 240$; for P-384 they are 192, 384 and 368; for P-521 they are 256, 521 and 504. In each case $P$ is the standard base point and $Q$ is a fixed point given in Appendix A.1. For P-256,

- $Q_x$ = `c97445f45cdef9f0d3e05e1e585fc297235b82b5be8ff3efca67c59852018192`
- $Q_y$ = `b28ef557ba31dfcbdd21ac46e2a91e3c304f44cb87058ada2cb815151e610046`.

Appendix A.2 describes how to generate other points verifiably at random, but validation against the standard required the fixed ones.

## The algorithm

**Instantiate.** $s \leftarrow \mathrm{Hash\_df}(e \| \nu \| \pi, \mathit{seedlen})$ for entropy input $e$, nonce $\nu$ and personalization string $\pi$, with the same Hash_df as [Hash_DRBG](/hash-drbg/); the block counter $c$ starts at 0.

**Reseed.** $s \leftarrow \mathrm{Hash\_df}(s \| e \| a, \mathit{seedlen})$ with $s$ written in $\mathit{seedlen}$ bits, and $c \leftarrow 0$.

**Generate.**

```pseudo id=main
DUAL-EC-GENERATE(s, c, n, a)           ▷ state s and block counter c; n output bits; optional additional input a
L1  if c + ⌈n / outlen⌉ > reseed_interval then return "reseed required"
L2  if a is not empty then t ← s ⊕ Hash_df(a, seedlen) else t ← s
L3  W ← empty string
L4  repeat
L5      s ← x(t · P)
L6      r ← x(s · Q); W ← W ‖ (r mod 2^outlen); c ← c + 1; t ← s
L7  until |W| ≥ n
L8  s ← x(s · P)
L9  return the leftmost n bits of W, with the new state (s, c)
```

Line L8, an extra state update at the end of each request, gives backtracking resistance between requests. Prediction resistance works as for the other DRBGs: reseed with fresh entropy and the additional input, then generate without additional input.

**The trapdoor (Shumow and Ferguson 2007).** Suppose $P = eQ$ for a known $e$. Observe one output block $r_1 = x(s_1 Q) \bmod 2^{240}$ and the first 16 bits of the next block of the same request. For each of the $2^{16}$ values $h$ of the missing high bits, set $X = h \cdot 2^{240} + r_1$; if $X$ is the $x$ coordinate of a curve point $R$, then $R = \pm s_1 Q$, so $eR = \pm s_1 P$ and $x(eR) = x(s_1 P) = s_2$, the next state. Compute the next output from the candidate $s_2$ and keep the candidates that match the observed 16 bits. Once $s_2$ is known, every later block of the request and the state $x(s_m P)$ that starts the next request follow.

## Example

P-256 with the standard points and SHA-256, entropy input $\texttt{00 01} \ldots \texttt{0f}$, nonce $\texttt{10 11} \ldots \texttt{17}$, no personalization string. Then

- $s_0$ = `708ec7422c7aa710d4fbaa5623920897af68f4d605c219a10f095ea46d77ab4b`,
- $s_1 = x(s_0 P)$ = `d3b55dd4953127ffa3d481a1899b6843ea3a9ad9cb734e0067b7444f7067abfb`,
- $x(s_1 Q)$ = `46ad` `d22141a0d0d283fe402ae812084d6a2a3e6500e630425cbff6740f9806b6`, and the output block is the last 30 bytes, `d22141a0…740f9806b6`,
- the state after the request is $x(s_1 P)$ = `5ab823fa…0fdbc86b4c`.

**The trapdoor in action.** Pick a secret $d$ (here the SHA-256 hash of the string "backdoor", reduced modulo the group order), set $Q = dP$ and $e = d^{-1} \bmod n$, so that $P = eQ$. Run the generator with the same inputs and request 120 bytes, four blocks. The attacker sees the first 30 bytes and the next 2. Of the 65536 values of the hidden 16 bits, 33005 give a valid $x$ coordinate; exactly one of the resulting candidates for $s_2$ reproduces the 2 observed bytes. It is `5ab823fa…0fdbc86b4c`, the same state as above (the state sequence does not depend on $Q$), and it predicts the remaining 88 bytes exactly. In pure Python the whole search took about 107 seconds; optimized code does it in well under a second.

**Known answers.** The tests reproduce the four P-256 known-answer tests of the OpenSSL FIPS Object Module 2.0 (SHA-1 and SHA-256, with reseeding or with prediction resistance), check that $Q$ is on the curve and has order $n$, and run the state recovery on a window of candidates.

## Correctness

The proof page shows that the pseudocode produces the blocks $x(s_j Q) \bmod 2^{240}$ for the states $s_j = x(s_{j-1} P)$, and proves the trapdoor property: if $P = eQ$ and $R$ is any point with $x(R) = x(sQ)$, then $x(eR) = x(sP)$. The second fact holds for every pair of points in the group, so the only question about a given $Q$ is whether someone knows $e$.

**What is known about security.**

- *Proved, under assumptions.* Brown and Gjøsteen (2007) showed that the output is pseudorandom if the decisional Diffie-Hellman problem is hard on the curve, if truncated $x$ coordinates are close to uniform, and if $Q$ is an independent random point. The last hypothesis is exactly what a fixed, unexplained $Q$ does not provide.
- *Bias.* Dropping only 16 of 256 bits leaves the output distinguishable from uniform: Schoenmakers and Sidorenko (2006), and independently Gjøsteen, gave distinguishers. The standard did not change.
- *Trapdoor.* Shumow and Ferguson (2007) presented the state recovery above. It needs $e$; computing $e$ from $P$ and $Q$ is an [elliptic curve discrete logarithm problem](/elliptic-curve-discrete-logarithm-problem/), infeasible on P-256.
- *Deployment.* In 2014 Checkoway et al. showed that TLS implementations using Dual_EC_DRBG (RSA BSAFE, Windows SChannel, OpenSSL-FIPS) leaked enough output in handshake nonces to recover session keys, given $e$; they demonstrated it with their own $Q$. In 2015 Juniper disclosed that unauthorized code had changed the $Q$ in its ScreenOS firewalls.

No public proof shows that anyone knows $e$ for the standard $Q$.

## Complexity

Each block costs two scalar multiplications by 256-bit scalars, and each request one more. With double-and-add, a scalar multiplication is $\Theta(\ell)$ point operations, and each point operation is a constant number of field multiplications of $\Theta((\ell / w)^2)$ word operations with schoolbook arithmetic, so a request of $m$ blocks costs $\Theta(m \ell^3 / w^2)$ word operations. For P-256 one block of 30 bytes takes two full scalar multiplications, which makes Dual_EC_DRBG hundreds to thousands of times slower per byte than CTR_DRBG with AES. The state is one field element. The trapdoor search costs up to $2^{16}$ square roots and scalar multiplications per block.

## Properties

- **Withdrawn.** Not approved since SP 800-90A Revision 1 (June 2015); NIST advised against it in September 2013.
- **Kleptographic structure.** The designer of the points can hold a key that breaks the generator, while everyone else sees a generator that is secure under standard assumptions. The output does not reveal whether such a key exists.
- **Biased output**, because only 16 bits of each coordinate are discarded.
- **Slow**, because each output block needs two elliptic curve scalar multiplications.

## Variants and improvements

- **Random $Q$.** Generating $Q$ verifiably from a public seed, as in Appendix A.2, removes the doubt about who knows $e$, and Brown and Gjøsteen's argument then applies; dropping more bits removes the bias. With both changes the design is sound but still slow.
- **Number-theoretic generators** in general, such as [Blum-Blum-Shub](/blum-blum-shub/) and [Blum-Micali](/blum-micali/), have reductions to standard problems without hidden parameters, at a similar or higher cost.
- **The approved alternatives** are [Hash_DRBG](/hash-drbg/), [HMAC_DRBG](/hmac-drbg/) and [CTR_DRBG](/ctr-drbg/).

## When to use it

Never for new systems. Its use today is as a case study: in the analysis of standards, of kleptography, and of how a generator's output in protocol messages can leak its state.

## Pitfalls

- **Public output exposes the state.** TLS sends 28 or 32 bytes of random nonce in the clear; with Dual_EC_DRBG that is enough for the holder of $e$ to predict the session keys generated next. Checkoway et al. found that extensions requesting more nonce bytes made attacks easier.
- **A fixed $Q$ is a trust assumption.** Nothing in the output reveals whether $e$ is known, and later replacement of $Q$ (as at Juniper) leaves the generator working normally.
- **Statistical tests do not detect it.** The output passes ordinary test batteries; the bias needs targeted tests, and the trapdoor is invisible.
- **Additional input is applied only before the first block.** It cannot help against an attacker who learns the state in the middle of a request.

## Implementations

## History

Dual_EC_DRBG came from the ANSI X9.82 drafts of the early 2000s and was published by NIST in SP 800-90 (June 2006), with Elaine Barker and John Kelsey as authors, alongside Hash_DRBG, HMAC_DRBG and CTR_DRBG. Gjøsteen and then Schoenmakers and Sidorenko (2006) showed that its output is biased. Brown and Gjøsteen (2007) gave a security analysis that assumed a random $Q$. At the CRYPTO 2007 rump session, Dan Shumow and Niels Ferguson of Microsoft showed that whoever knows the relation between $P$ and $Q$ can predict the output. After press reports in September 2013, NIST reopened SP 800-90A for comment and recommended against the generator; it was removed in Revision 1 in June 2015. Checkoway et al. (2014) measured how exploitable it was in TLS libraries, and the Juniper ScreenOS incident of 2015 showed an attacker replacing $Q$ in deployed devices.

## References
