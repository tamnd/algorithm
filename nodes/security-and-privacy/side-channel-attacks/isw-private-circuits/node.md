---
tag: F6CSK5
kind: algorithm
slug: isw-private-circuits
name: ISW private circuits
aliases:
- Ishai-Sahai-Wagner construction
area: security-and-privacy/side-channel-attacks
level: advanced
summary: "Compiles any circuit into one secure against t probes by masking each wire with 2t+1 shares and a randomized AND gadget; later work showed t+1 shares suffice for the gadget."
model: word-ram
complexity:
  vars: {n: the number of shares of each wire, t: the number of probes}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n^2)}
history:
  year: 2003
  people: [Yuval Ishai, Amit Sahai, David Wagner]
  note: "Ishai, Sahai and Wagner defined the probing model and the construction at CRYPTO 2003, with 2t + 1 shares; Rivain and Prouff (CHES 2010) proved the AND gadget secure with t + 1 shares."
prereqs: [probing-model, boolean-masking]
see_also: [threshold-implementation, secret-sharing, boolean-circuit, side-channel-attack, differential-power-analysis, test-vector-leakage-assessment, advanced-encryption-standard, circuit-complexity]
sources:
  - paper: "Yuval Ishai, Amit Sahai and David Wagner, Private circuits: securing hardware against probing attacks, CRYPTO 2003, LNCS 2729, pages 463 to 481"
    locator: "the definition of the t-probing model, the AND gadget with its random bits, and the theorem for circuits with 2t + 1 shares"
  - paper: doi:10.1007/978-3-642-15031-9_28
    title: "Matthieu Rivain and Emmanuel Prouff, Provably secure higher-order masking of AES, CHES 2010, LNCS 6225, pages 413 to 427"
    locator: "the proof that the ISW multiplication is secure against t probes with t + 1 shares, and its use over the field of 256 elements for the AES S-box"
  - paper: doi:10.1007/978-3-662-43933-3_21
    title: "Jean-Sébastien Coron, Emmanuel Prouff, Matthieu Rivain and Thomas Roche, Higher-order side channel security and mask refreshing, FSE 2013, LNCS 8424, pages 410 to 424"
    locator: the flaw in the composition of gadgets with the refresh of Rivain and Prouff, and the corrected refresh
  - paper: doi:10.1145/2976749.2978427
    title: "Gilles Barthe and others, Strong non-interference and type-directed higher-order masking, CCS 2016, pages 116 to 129"
    locator: the definition of strong non-interference and the proof that the ISW multiplication has it, which makes gadgets compose
  - paper: doi:10.1007/978-3-642-55220-5_24
    title: "Alexandre Duc, Stefan Dziembowski and Sebastian Faust, Unifying leakage models: from probing attacks to noisy leakage, EUROCRYPT 2014, LNCS 8441, pages 423 to 440"
    locator: the reduction from security in the noisy leakage model to security in the probing model
  - paper: doi:10.1007/978-3-642-38348-9_9
    title: "Emmanuel Prouff and Matthieu Rivain, Masking against side-channel attacks: a formal security proof, EUROCRYPT 2013, LNCS 7881, pages 142 to 159"
    locator: the noisy leakage model and the security proof of masked computation in it
---

The ISW construction of Ishai, Sahai and Wagner (2003) turns any Boolean circuit into a circuit that computes the same function but is secure against an attacker who can read the values of up to $t$ wires. Each bit is carried as $n$ random shares whose XOR is the bit, as in [Boolean masking](/boolean-masking/). XOR and NOT gates work on each share apart. The AND gate is replaced by a gadget that multiplies every share of one input with every share of the other and mixes in fresh random bits so that no small set of wires depends on the secret. The original theorem uses $n = 2t + 1$ shares; Rivain and Prouff (2010) proved that the AND gadget is secure against $t$ probes with $t + 1$ shares. The model of the attacker is the [probing model](/probing-model/).

## In plain words

Split each secret bit into several random bits that combine back into the secret, so that a spy who sees fewer than all of them learns nothing. Adding two split bits is easy: add the matching pieces. Multiplying is harder, because each piece of the result must depend on pieces of both inputs. The ISW method multiplies every piece of one input with every piece of the other, and adds a fresh random bit to each cross product before it is combined. The random bits cancel when the result is put back together, but they hide each partial result. The order of the additions is part of the method: adding the cross products before the random bit gives a wire that shows part of the secret.

## The problem

A circuit has XOR, NOT and AND gates on bits. A $t$-probing attacker chooses, before the run, a set of at most $t$ wires of the circuit and sees their values in one run (Ishai, Sahai and Wagner). A circuit with random input sharings and random bits is $t$-probing secure if, for every set $P$ of at most $t$ wires, the joint distribution of the values on $P$ is the same for every value of the secret inputs.

The goal is a compiler that maps a circuit $C$ to a circuit $C'$ that computes the shares of $C(x)$ from shares of $x$, and that is $t$-probing secure. This page gives the AND gadget, which is the core of the compiler, and its check for $t = 1$ and $t = 2$. The cost model is the [word RAM](/word-ram/), with one step for each AND, XOR or random bit on single bits; the cost of a defense is counted in gates and random bits.

## The algorithm

Inputs are $a_1, \ldots, a_n$ with $\bigoplus_i a_i = a$ and $b_1, \ldots, b_n$ with $\bigoplus_i b_i = b$.

```pseudo id=main
ISW-AND(a_1 .. a_n, b_1 .. b_n)
L1  for i = 1 .. n do
L2      for j = i + 1 .. n do
L3          r_ij ← a fresh uniform random bit
L4          r_ji ← (r_ij ⊕ a_i b_j) ⊕ a_j b_i      ▷ in this order
L5  for i = 1 .. n do
L6      c_i ← a_i b_i
L7      for each j ≠ i do c_i ← c_i ⊕ r_ij
L8  return c_1 .. c_n
```

The output shares satisfy $\bigoplus_i c_i = a b$. A full circuit is compiled gate by gate: an XOR of two sharings is the XOR of the matching shares, a NOT flips the first share, and each AND is one call of ISW-AND with fresh random bits.

Line L4 is where the order matters. In the order shown, the first intermediate value is $r_{ij} \oplus a_i b_j$, which is hidden by the fresh bit $r_{ij}$. If the code computes $a_i b_j \oplus a_j b_i$ first, that wire is not hidden by any random bit, and with two shares it shows whether $a = b = 0$ (see Pitfalls).

## Example

Take $n = 2$, $a = 1$ with shares $(1, 0)$, $b = 1$ with shares $(0, 1)$, and the random bit $r_{12} = 1$. Line L4 computes $a_1 b_2 = 1$, then $r_{12} \oplus 1 = 0$, then $a_2 b_1 = 0$, so $r_{21} = 0$. Lines L5 to L7 give $c_1 = a_1 b_1 \oplus r_{12} = 0 \oplus 1 = 1$ and $c_2 = a_2 b_2 \oplus r_{21} = 0 \oplus 0 = 0$. The output $(1, 0)$ is a sharing of $1 = a b$.

The gadget for $n = 2$ has 13 wires: the 4 input shares, the 5 wires of line L4, and the 4 wires of lines L6 and L7. With 2 shares for each input and 1 random bit, each secret $(a, b)$ has 8 runs of equal probability. Each of the 13 wires alone has the same distribution for the 4 secrets, so the gadget is 1-probing secure. With 2 probes it is not: 22 of the 78 pairs of wires depend on the secret, for example $(a_1, a_2)$, which gives $a$.

For $n = 3$ the gadget has 30 wires and each secret has 128 runs. All 30 single wires and all 435 pairs have a distribution independent of the secret, so the gadget is 2-probing secure with $t + 1 = 3$ shares; 197 of the 4060 sets of 3 wires depend on the secret. These are exhaustive enumerations, made by the tests.

## Correctness

**Correct output.** For each pair $i < j$, lines L4 give $r_{ij} \oplus r_{ji} = a_i b_j \oplus a_j b_i$. The XOR of all outputs is

$$\bigoplus_i c_i = \bigoplus_i a_i b_i \oplus \bigoplus_{i < j} (r_{ij} \oplus r_{ji}) = \bigoplus_{i, j} a_i b_j = \Big(\bigoplus_i a_i\Big)\Big(\bigoplus_j b_j\Big) = a b .$$

**Probing security.** If the input sharings are uniform and independent and $n \ge 2t + 1$, every set of at most $t$ wires of the gadget has a distribution that does not depend on $(a, b)$. The proof is a simulation: each probe names at most 2 share indices, so the probes depend on at most $2t < n$ shares of each input, and any $n - 1$ shares of a uniform sharing are uniform and independent of the secret. The random bit of a pair with only one probed index hides the partial sums that use it. Both claims are theorems, proved in the [proof](proofs/correctness.md). The stronger statement with $n = t + 1$ shares is a theorem of Rivain and Prouff (2010); the tests verify it by exhaustive enumeration for $t = 1$ and $t = 2$. The theorem for a whole compiled circuit, where gadgets share wires, is the theorem of Ishai, Sahai and Wagner with $2t + 1$ shares and their refresh of the sharings; it is cited, not proved here.

## Complexity

One AND gadget computes $n^2$ products $a_i b_j$, draws $n(n - 1)/2$ random bits, and does $2n(n - 1)$ XORs: two for each pair in line L4 and $n - 1$ for each output in line L7. So the time is $\Theta(n^2)$ and the extra space is $\Theta(n^2)$ for the bits $r_{ij}$; the bits can be used as soon as they are made, which brings the space down to $\Theta(n)$. XOR and NOT gates cost $\Theta(n)$. A circuit with $s$ AND gates and $u$ other gates costs $\Theta(s n^2 + u n)$. With $n = t + 1$ the cost of a gadget grows as $t^2$; with $n = 2t + 1$ it is about four times larger for large $t$.

The tests count the gates for $n = 1$ to $6$ and find exactly $n^2$, $n(n-1)/2$ and $2n(n-1)$.

## Properties

- **Correct for every choice of random bits.** The output is a sharing of $a b$ whatever the random bits are; the random bits only affect security.
- **Linear gates are free of randomness.** XOR and NOT need no random bits, so the cost of a masked circuit is in its AND gates. This is why masked ciphers are designed or written with few non-linear operations.
- **Uniform outputs.** For fixed input shares, the output $c$ is a uniform sharing of $ab$: each $c_i$ with $i < n$ contains the random bit $r_{in}$, which no other $c_j$ with $j < n$ contains, so $c_1, \ldots, c_{n-1}$ are uniform and independent. The tests check this for $n \le 4$. A uniform output is still not enough for composition, because the probes inside two gadgets can be combined.
- **Order of operations.** Security depends on the exact order of the XORs in line L4. A compiler that reorders XORs as if they were free can break it.
- **A model, not a device.** The theorem is about wires in the probing model. A real device leaks noisy functions of many values at once, and its glitches can combine shares. The reduction of Duc, Dziembowski and Faust (2014) links the probing model to noisy leakage; for glitches, see [threshold implementations](/threshold-implementation/).

## Variants and improvements

- **t + 1 shares.** Rivain and Prouff (2010) proved the gadget secure with $n = t + 1$ and used it over the field of 256 elements to mask the [AES](/advanced-encryption-standard/) S-box at any order. The product $a_i b_j$ becomes a field product and $\oplus$ the field addition.
- **Refresh.** Between gadgets that use the same sharing twice, a refresh adds fresh random sharings of 0. Coron, Prouff, Rivain and Roche (2013) showed that with the simple refresh of Rivain and Prouff, the masked AES S-box is not secure at the claimed order, and proposed a refresh based on the ISW gadget.
- **Strong non-interference.** Barthe and others (2016) defined strong non-interference, a property of a gadget that makes compositions $t$-probing secure without a global proof. The ISW multiplication has it, and their tool places refresh gadgets automatically.
- **Noisy leakage.** Prouff and Rivain (2013) proved security of masking in a model of noisy leakage of every value, and Duc, Dziembowski and Faust (2014) reduced that model to the probing model.
- **Hardware with glitches.** In hardware, a glitch can make a gate briefly show a function of several shares. [Threshold implementations](/threshold-implementation/) use non-completeness to stay secure with glitches.

## When to use it

Use the ISW gadget, or a variant, when a cipher must be protected against higher-order side-channel attacks with a proof. Choose $n = t + 1$ for a software implementation with a refresh strategy proved by strong non-interference. Use first-order [Boolean masking](/boolean-masking/) with table recomputation when $t = 1$ is enough, and a threshold implementation in hardware. Check the result with a [leakage test](/test-vector-leakage-assessment/), because the proof holds in the model and not for every effect of the device.

## Pitfalls

- **No random bits.** The gadget $c_i = \bigoplus_j a_i b_j$ is correct but $c_i = a_i b$, so the last partial sum of $c_1$ shows $b$ whenever $a_1 = 1$. The tests find it with one probe, for 2 and 3 shares.
- **The wrong order in line L4.** Computing $r_{ji} = r_{ij} \oplus (a_i b_j \oplus a_j b_i)$ gives the wire $a_1 b_2 \oplus a_2 b_1 = a_1 b \oplus a b_1$ for 2 shares. It is always 0 when $a = b = 0$, and it is 1 with probability $1/2$ for the other three secrets, so one probe leaks. For 3 shares the same mistake leaks with 2 probes, for example on $a_3$ and $a_1 b_2 \oplus a_2 b_1$: the tests find 9 such pairs, and none for the correct order.
- **Reused random bits.** If two gadgets use the same $r_{ij}$, a probe on one gadget and a probe on the other can cancel it.
- **Composition without refresh.** A gadget that is $t$-probing secure on its own can fail when its two inputs are not independent sharings, for example $a$ and a linear function of $a$. Refresh one input, or use gadgets with strong non-interference.
- **Too few shares in the claim.** With $n$ shares, the $n$ input shares of one input together give the secret, so no gadget is $n$-probing secure. The tests find $(a_1, a_2)$ for $n = 2$.

## Implementations

The code of this page is an abstract model of a circuit. It works on bits in Python lists, draws the random bits from a seeded `random.Random`, and never reads a device, a file or a clock. The function `isw_and_wires` returns the output and every intermediate wire of the gadget. The tests enumerate all input sharings and all random bits for each of the 4 secrets and compare the distributions of every set of 1 probe for $n = 2$ and of every set of at most 2 probes for $n = 3$. They also show the leaks of the gadget without random bits and of the wrong order, count the gates, and compare a masked evaluation of 500 random circuits with the plain evaluation.

## History

Ishai, Sahai and Wagner presented private circuits at CRYPTO 2003. They defined the $t$-probing model, gave the AND gadget, and proved that $2t + 1$ shares give $t$-probing security for any circuit. Masking itself was older: Chari, Jutla, Rao and Rohatgi (1999) and Goubin and Patarin (1999) proposed secret sharing of intermediate values against power analysis. Rivain and Prouff (2010) proved the gadget with $t + 1$ shares and applied it to AES. Coron, Prouff, Rivain and Roche (2013) found a flaw in the composition with refresh, and Barthe and others (2016) gave strong non-interference as a rule for composition.

## References
