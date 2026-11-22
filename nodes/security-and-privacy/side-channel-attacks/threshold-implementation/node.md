---
tag: 2V6QRX
kind: technique
slug: threshold-implementation
name: Threshold implementation
aliases:
- TI masking
area: security-and-privacy/side-channel-attacks
level: research
summary: "Masking based on secret sharing with correctness, non-completeness and uniformity, which stays secure in hardware with glitches."
prereqs: [boolean-masking, probing-model]
see_also: [isw-private-circuits, test-vector-leakage-assessment, side-channel-attack, secret-sharing, s-box, advanced-encryption-standard, boolean-circuit, differential-power-analysis]
sources:
  - paper: doi:10.1007/11935308_38
    title: "Svetla Nikova, Christian Rechberger and Vincent Rijmen, Threshold implementations against side-channel attacks and glitches, ICICS 2006, LNCS 4307, pages 529 to 545"
    locator: "the definition of a threshold implementation by correctness and non-completeness, and the proof that it resists first-order attacks with glitches"
  - paper: "Svetla Nikova, Vincent Rijmen and Martin Schläffer, Secure hardware implementation of nonlinear functions in the presence of glitches, Journal of Cryptology 24(2), 2011, pages 292 to 321"
    locator: "the properties of correctness, non-completeness and uniformity, the bound of d + 1 shares for a function of degree d, and the sharing of the AND gate"
  - paper: "Yuval Ishai, Amit Sahai and David Wagner, Private circuits: securing hardware against probing attacks, CRYPTO 2003, LNCS 2729, pages 463 to 481"
    locator: the t-probing model and the masked AND gate with fresh random bits, which threshold implementations are compared with
---

A threshold implementation (TI) is a form of [Boolean masking](/boolean-masking/) for hardware. It splits each value into shares, and it splits each function into component functions, so that each component function does not read at least one share of each input. Then even if a glitch in the circuit makes a wire carry any function of the inputs of its component, that wire depends on at most all but one share, and so it is independent of the secret. Nikova, Rechberger and Rijmen proposed the method in 2006, and Nikova, Rijmen and Schläffer (2011) added the uniformity property that lets one stage feed the next. A function of algebraic degree $d$ needs at least $d + 1$ shares for a first-order TI, so the AND gate and every quadratic [S-box](/s-box/) need three.

## In plain words

Masking puts a secret into pieces so that no single piece says anything. In software, the device works on one piece at a time. In hardware, a gate gets all its inputs at once, and while the inputs arrive at slightly different times, the output can flicker through values that mix several pieces. Such flickers, called glitches, also use power, so a first-order attack can see a mix of all the pieces of a secret and learn the secret. A threshold implementation makes sure that no gate ever has all the pieces: each output piece is computed from the other pieces only. So even the worst flicker shows at most all but one piece, which looks random. A register stores each output before the next stage starts, so that flickers do not travel from one stage to the next.

## When it applies

- **Hardware with glitches.** The combinational logic between two registers can leak any function of its inputs during one clock cycle. TI assumes this, and it assumes that registers stop glitches.
- **First-order security.** The classic TI targets attacks of order 1, in the model in which a probe on a wire is extended to all the inputs of the logic that drives it.
- **Functions of low degree.** The number of shares grows with the algebraic degree of the function. An S-box of degree 3 is often written as a composition of quadratic functions, each with its own TI and a register after it.
- **Uniform inputs.** The proof needs each input of a stage to be a uniform sharing. If a stage does not make a uniform output, the next stage needs fresh random bits.

## The template

The template is the TI of $z = xy$ for two bits $x$ and $y$, each in three shares, with the option of two fresh bits to make the output uniform.

```pseudo id=main
TI-AND(x_1, x_2, x_3, y_1, y_2, y_3, optional r_1, r_2)     ▷ SHARES: 3 for degree 2
L1  z_1 ← x_2 y_2 ⊕ x_2 y_3 ⊕ x_3 y_2        ▷ COMPONENTS: no share 1
L2  z_2 ← x_3 y_3 ⊕ x_1 y_3 ⊕ x_3 y_1        ▷ no share 2
L3  z_3 ← x_1 y_1 ⊕ x_1 y_2 ⊕ x_2 y_1        ▷ no share 3
L4  if UNIFORM needs it then z_1 ← z_1 ⊕ r_1; z_2 ← z_2 ⊕ r_2; z_3 ← z_3 ⊕ r_1 ⊕ r_2
L5  store (z_1, z_2, z_3) in a REGISTER
L6  return (z_1, z_2, z_3)
```

The holes are:

- **SHARES.** The number $s$ of input shares. For first-order security of a function of degree $d$, $s \ge d + 1$, because a product of $d$ shares can use $d$ different share indices, and it must go into a component that misses one more index.
- **COMPONENTS.** The component functions $f_1, \ldots, f_s$. **Correctness:** $f_1 \oplus \cdots \oplus f_s = f$ on the shares. **Non-completeness:** $f_i$ does not depend on share $i$ of any input. Lines L1 to L3 are correct, because the 9 products $x_i y_j$ appear once each and their sum is $(x_1 \oplus x_2 \oplus x_3)(y_1 \oplus y_2 \oplus y_3) = xy$.
- **UNIFORM.** **Uniformity:** for a uniform input sharing, every sharing of the output value is equally likely. Lines L1 to L3 alone are not uniform; line L4 adds a uniform sharing of 0, which makes the output uniform.
- **REGISTER.** The register after each stage stops glitches, so that the inputs of the next stage are the stored shares and nothing else.

The first-order argument: for a uniform sharing, any two of the three shares of a value are uniform and independent of it. A glitch on $z_1$ can carry any function of $x_2, x_3, y_2, y_3$ and $r_1$, and these are independent of $(x, y)$. The same holds for $z_2$ and $z_3$. The proof file gives the details.

The cost is 9 AND gates and 6 XOR gates for the three components, with 2 random bits and 4 more XOR gates for line L4, and one register stage, against one AND gate unmasked.

## Classic examples

The code of this page is a small abstract model of a masked gate. It works on bits in tuples, models a glitch as a probe that sees all the inputs of one component function, and enumerates all sharings; it never reads a device, a file or a clock. The tests check every claim below.

**The AND gate.** Over the 16 pairs of input sharings for each of the 4 pairs $(x, y)$, the output of lines L1 to L3 always XORs to $xy$, and each component does not change when share $i$ of both inputs changes. The inputs of each component have the same distribution for all 4 pairs $(x, y)$, so a glitch-extended probe on one output share learns nothing.

**Uniformity.** Without line L4, the output sharing is not uniform: for $xy = 0$ the sharing $(0, 0, 0)$ appears 7 times out of 16 and each of the other three sharings 3 times, and for $x = y = 1$ the sharings $(0, 0, 1)$, $(0, 1, 0)$ and $(1, 0, 0)$ appear 5 times each and $(1, 1, 1)$ once. A component of the next stage that reads $z_1$ and $z_2$ then sees different distributions for $xy = 0$ and $xy = 1$, so the non-uniform output breaks the next stage. With the fresh bits of line L4, each of the 4 sharings of $xy$ appears 16 times out of 64.

**A two-share AND without non-completeness.** The first-order AND with two shares and one random bit, $c_1 = a_1 b_1 \oplus a_1 b_2 \oplus r$ and $c_2 = a_2 b_1 \oplus a_2 b_2 \oplus r$, is correct, and each output share alone is uniform, as in the [ISW](/isw-private-circuits/) gadget for two shares. But the logic of $c_1$ reads both $b_1$ and $b_2$, so a glitch can show $b$. The tests find that the inputs of that component have different distributions for $b = 0$ and $b = 1$.

**Block ciphers.** The 4-bit S-box of PRESENT has degree 3. With three shares, it is computed as two quadratic functions, each with a TI and a register, so that each stage has degree 2. TIs of the [AES](/advanced-encryption-standard/) S-box use its decomposition into operations in smaller fields, with fresh bits where uniformity fails. Such designs are tested with [TVLA](/test-vector-leakage-assessment/): the expected result for a first-order TI is a first-order pass and a second-order fail.

## Variations

- **More shares, no randomness.** For some functions, a uniform sharing exists with more shares than $d + 1$, or for a different split of the monomials. Classic TI searches for such sharings to avoid fresh random bits.
- **Decomposition.** Write a function of high degree as a composition of quadratic or cubic functions, each with a uniform TI, so that fewer shares are needed.
- **Higher orders.** Later work extends the rules to security against more probes, with more shares. The extension needs care, because an argument for one clock cycle does not cover attacks that combine values from several cycles.
- **Gadgets with $t + 1$ shares.** Other hardware masking schemes use $t + 1$ shares and fresh random bits in each AND gadget, as in [ISW](/isw-private-circuits/), with registers placed so that no glitch combines all shares of a value. They use fewer shares than TI at the cost of more randomness.

## Pitfalls

- **Missing registers.** If the output of a stage goes into the next stage without a register, a glitch can travel through both stages, and a wire of the second stage can depend on all shares.
- **Non-uniform outputs.** Composing non-uniform stages can leak at first order in a later stage, as the example shows. Check uniformity, or add fresh bits.
- **Shares that meet in the place and route.** Two shares on wires close to each other can couple, so that the physical leak depends on both. Non-completeness on the netlist does not prevent this.
- **The synthesis tool.** A tool that optimizes the logic can merge component functions, or share gates between them, and break non-completeness. Keep each component in its own module, and stop optimizations across modules.
- **Only first order.** A three-share TI is first-order secure. A second-order attack, which combines two shares, finds the secret with enough traces.

## Exercises

1. Check that lines L1 to L3 are correct by expanding $(x_1 \oplus x_2 \oplus x_3)(y_1 \oplus y_2 \oplus y_3)$.
2. Show that no correct and non-complete sharing of $xy$ with two shares exists.
3. Show that adding $(r_1, r_2, r_1 \oplus r_2)$ to any sharing of $z$, with uniform $r_1$ and $r_2$, gives a uniform sharing of $z$.
4. Count the output sharings of lines L1 to L3 for $x = y = 1$ by hand, and find a pair of output shares whose distribution depends on $xy$.
5. A function has degree 3. How many shares does a first-order TI need, and how can a decomposition into quadratic functions reduce this?

## References
