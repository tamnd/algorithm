---
tag: EYTCX4
kind: technique
slug: simple-power-analysis
name: Simple power analysis
aliases:
- SPA
area: security-and-privacy/side-channel-attacks
level: core
summary: "Reads secret-dependent operations, such as squarings and multiplications in exponentiation, directly from one or a few power traces."
prereqs: [side-channel-attack, binary-exponentiation]
see_also: [differential-power-analysis, timing-attack, modular-exponentiation, rsa-blinding, elliptic-curve-cryptography, data-encryption-standard, constant-time-programming, template-attack]
sources:
  - paper: "Paul Kocher, Joshua Jaffe and Benjamin Jun, Differential power analysis, CRYPTO 1999, LNCS 1666, pages 388 to 397"
    locator: the section on simple power analysis (the visible rounds and operations of DES and of modular exponentiation, and the defence by avoiding secret-dependent branches)
  - paper: "Stefan Mangard, Elisabeth Oswald and Thomas Popp, Power Analysis Attacks, Springer, 2007, ISBN 978-0-387-30857-9"
    locator: "Chapter 5, pages 101 to 118 (simple power analysis: visual inspection, template-based SPA and collision attacks)"
  - paper: "Paul C. Kocher, Timing attacks on implementations of Diffie-Hellman, RSA, DSS, and other systems, CRYPTO 1996, LNCS 1109, pages 104 to 113"
    locator: the secret-dependent operations of square and multiply, which a timing attack sees as a sum and a power trace shows one by one
---

Simple power analysis (SPA) reads a secret from the shape of one power trace, or of a few. If the sequence of operations of a program depends on the secret, and different operations draw power in different patterns, then the trace shows the sequence and the sequence shows the secret. The classic case is square and multiply [exponentiation](/binary-exponentiation/), where a multiplication follows a squaring only for the 1 bits of the exponent. Kocher, Jaffe and Jun (1999) described SPA together with [differential power analysis](/differential-power-analysis/). SPA needs no statistics over many runs, but it needs a leak that is large compared to the noise; DPA works when the leak is small.

## In plain words

Imagine you can hear a calculator. Each kind of key press makes its own sound. If the calculator presses "multiply" only when a secret digit is 1, you can write down the secret while you listen. A chip is like that. Its power use over time has a shape, and different operations have different shapes. When a program chooses its next operation by looking at a secret bit, one recording of the power can show every choice it made. The attacker does not need to guess and test. It only needs to recognise the shapes and know the program. The defence is to make the program do the same operations in the same order for every secret.

## When it applies

SPA applies when all of these hold:

- **Secret-dependent control flow or data.** The sequence of operations, or the operand of a very leaky operation, depends on the secret. Branches on key bits, early exits, and table lookups with a secret index are the usual causes.
- **Distinguishable operations.** The operations that the secret selects differ in their power pattern by more than the noise of one trace: a squaring and a general multiplication, a point doubling and a point addition, or a conditional extra step.
- **Known algorithm.** The attacker knows, or can learn from a copy, how the sequence of operations maps to the secret.
- **Few runs.** The secret is used once or a few times with no change in between. Ephemeral keys and keys that are blinded between runs reduce the attack to one trace, and SPA is often the only option there.

It does not apply to an implementation whose sequence of operations is fixed for every secret and whose data-dependent leakage is small compared to the noise in one trace. That case needs a statistical attack such as DPA or a [template attack](/template-attack/).

## The template

The pseudo code names the stages of the published method. Each line in capitals is a hole that depends on the target.

```pseudo id=main
SPA(trace of one run, description of the algorithm)
L1  segments ← SEGMENT(trace)                 ▷ cut the trace at the start of each operation
L2  for each segment s do
L3      type(s) ← CLASSIFY(s)                  ▷ which operation of the algorithm it is
L4  bits ← DECODE(sequence of types)          ▷ invert the control flow of the algorithm
L5  if some types are unclear then
L6      candidates ← all secrets that agree with the clear types
L7  return the candidate that passes VERIFY(input, output)
```

Line L1 finds where each operation starts, from a repeated pattern in the trace. Line L3 assigns each segment to a type. In the textbook case the types differ visibly; with a profiled device, the classification can use [templates](/template-attack/) of each operation. Line L4 is the inverse of the control flow: in square and multiply, "S M" is a 1 bit and "S" followed by "S" is a 0 bit. Lines L5 and L6 cover segments that were not classified with confidence: each unclear segment doubles the number of candidates. Line L7 tests each candidate with one known pair of input and output, for example by checking a signature.

The cost is one pass over the trace for lines L1 to L4, and $2^u$ checks in line L7 for $u$ unclear segments. This count is exact for the template; how many segments are unclear in practice is a measurement on each device.

## Classic examples

All examples are abstract: the traces are sequences of operation names, not real measurements.

**Square and multiply.** Left-to-right [modular exponentiation](/modular-exponentiation/) computes $x^e \bmod N$ from the top bit of $e$ down. For each bit it squares, and for each 1 bit it then multiplies by $x$. Starting from 1, the exponent $e = 1011_2$ gives the sequence S M S S M S M. If a squaring and a multiplication look different in the trace, line L4 reads 1, 0, 1, 1. The same holds for the square and multiply step of [binary exponentiation](/binary-exponentiation/) in [RSA](/rsa-cryptosystem/) decryption and signing, where the exponent is the private key $d$.

**Double and add on an elliptic curve.** Scalar multiplication $kP$ in [elliptic curve cryptography](/elliptic-curve-cryptography/) does a point doubling for each bit of $k$ and a point addition for each 1 bit. Doubling and addition use different sequences of field operations, so the trace shows the bits of $k$ as in the previous example. With an ephemeral key of a signature, one trace is all the attacker gets, so the attack must work in one trace.

**DES rounds and key schedule.** Kocher, Jaffe and Jun show that a trace of [DES](/data-encryption-standard/) shows its 16 rounds, and that within a round the shifts of the key schedule and the permutations can be seen. They note that conditional branches and the operations on key bits in an implementation of DES can leak key bits directly.

**A conditional final subtraction.** [Montgomery multiplication](/montgomery-multiplication/) ends with a subtraction only when the intermediate result is too large. If the subtraction is visible, each multiplication shows one bit that depends on the operands. Kocher (1996) used the time of such steps; in a power trace they can be seen one by one.

## Variations

- **Regular algorithms.** The defence is an algorithm with a fixed sequence of operations: square and multiply always, with a dummy multiplication for 0 bits, or a Montgomery ladder, which does one squaring and one multiplication for each bit and uses the bit only to choose the operands. A dummy operation whose result is thrown away is open to a fault attack that disturbs it and checks whether the output changes.
- **Unified formulas.** On elliptic curves, formulas that use the same field operations for addition and doubling remove the difference that line L3 detects.
- **Template-based SPA.** With a copy of the device, the attacker profiles each operation and classifies the segments by likelihood, as in a [template attack](/template-attack/), which works with smaller differences (Mangard, Oswald and Popp, Chapter 5).
- **Collision attacks.** Two operations on the same unknown value give similar segments. Comparing segments within one trace can show that two intermediate values are equal, even when the operations are the same.
- **Blinding.** [RSA blinding](/rsa-blinding/) of the private exponent, $d' = d + r \varphi(N)$ for a random $r$, gives a different sequence in each run. It defeats attacks that average many traces, but one trace still shows $d'$, which is as good as $d$ for an attacker who reads it in full.

## Pitfalls

- **Dummy operations that are not equal.** A dummy multiplication must look the same as a real one. If it uses a fixed operand or a buffer that is never read, it can still be seen.
- **Data-dependent timing inside a fixed sequence.** A fixed sequence of high-level operations is not enough if each operation takes a data-dependent time, as with a final subtraction or an early exit in a comparison. See [constant-time programming](/constant-time-programming/).
- **One trace is enough.** A defence that randomizes between runs, such as exponent blinding, does not stop an attack that reads everything from one run.
- **SPA in a DPA defence.** Masking hides the values, not the control flow. A masked implementation with a branch on a key bit is still open to SPA.

## Exercises

1. Write the sequence of squarings and multiplications for $e = 110010_2$ in left-to-right square and multiply, starting from 1, and decode it back.
2. In right-to-left square and multiply, the multiplication by the current power of $x$ happens before the squaring. Write the sequence for $e = 1011_2$ and give the decoding rule.
3. A Montgomery ladder for $x^e$ keeps $(R_0, R_1) = (x^j, x^{j+1})$ and does one squaring and one multiplication for each bit. Write the update for a 0 bit and for a 1 bit, and explain why the sequence of operations is the same.
4. Suppose that 10 of the 1024 segments of a trace are unclear. How many candidates does line L7 test? What if the attacker can also use the fact that the operation after a multiplication is always a squaring?

## References
