---
tag: H7YXSN
kind: technique
slug: boolean-masking
name: Boolean masking
aliases:
- masking countermeasure
- secret sharing countermeasure
area: security-and-privacy/side-channel-attacks
level: core
summary: "Splits each secret intermediate value into random shares whose XOR is the value, so that no single leaking point depends on the secret."
prereqs: [side-channel-attack, secret-sharing]
see_also: [probing-model, isw-private-circuits, threshold-implementation, differential-power-analysis, test-vector-leakage-assessment, hamming-weight, s-box, one-time-pad]
sources:
  - paper: doi:10.1007/3-540-48405-1_26
    title: "Suresh Chari, Charanjit S. Jutla, Josyula R. Rao and Pankaj Rohatgi, Towards sound approaches to counteract power-analysis attacks, CRYPTO 1999, LNCS 1666, pages 398 to 412"
    locator: "the model in which each share leaks with Gaussian noise, and the result that the number of traces for an attack grows exponentially in the number of shares"
  - paper: doi:10.1007/3-540-48059-5_15
    title: "Louis Goubin and Jacques Patarin, DES and differential power analysis, the duplication method, CHES 1999, LNCS 1717, pages 158 to 172"
    locator: "the duplication method, which splits each variable of DES into two shares and computes on the shares"
  - paper: "Stefan Mangard, Elisabeth Oswald and Thomas Popp, Power Analysis Attacks, Springer, 2007, ISBN 978-0-387-30857-9"
    locator: "Chapter 9, Masking, pages 223 to 244"
  - paper: "Yuval Ishai, Amit Sahai and David Wagner, Private circuits: securing hardware against probing attacks, CRYPTO 2003, LNCS 2729, pages 463 to 481"
    locator: the t-probing model and the masking of every wire with several shares
  - paper: doi:10.1007/978-3-540-74735-2_31
    title: "Andrey Bogdanov and others, PRESENT, an ultra-lightweight block cipher, CHES 2007, LNCS 4727"
    locator: the description of the substitution layer (the table of the 4-bit S-box used in the examples of this page)
---

Boolean masking is a countermeasure against [side-channel attacks](/side-channel-attack/) such as [DPA](/differential-power-analysis/). The implementation never stores or computes a secret intermediate value $x$ directly. It stores shares $x_1, \ldots, x_d$ with $x = x_1 \oplus \cdots \oplus x_d$, where all shares but one are fresh uniform random values, and it computes on the shares. Any $d - 1$ shares are then uniform and independent of $x$, as in the [one-time pad](/one-time-pad/) and in additive [secret sharing](/secret-sharing/). Goubin and Patarin (1999) proposed the idea for DES as the duplication method. Chari, Jutla, Rao and Rohatgi (1999) showed that, when each share leaks with Gaussian noise, the number of traces that an attack needs grows exponentially in the number of shares. Linear operations are easy on shares; the nonlinear parts, such as an [S-box](/s-box/), need a special gadget, and that is where most of the work and most of the errors are.

## In plain words

A device leaks a little about each value it handles, for example its [Hamming weight](/hamming-weight/). If the value is the secret, the leak is about the secret. Masking replaces the secret by two or more random-looking pieces that combine to the secret by XOR. Each piece alone is a random number, so a leak of one piece tells nothing. The device must do all its work on the pieces and never put them back together before the end. An attacker who can see two pieces at the same time can still combine them, so the protection is only against attacks that look at fewer pieces than there are. Two pieces protect against first-order attacks; more pieces protect against higher-order attacks, at a higher cost.

## When it applies

- **Leakage of each value, not of the whole computation.** Masking helps when the leak at each moment depends on a small number of intermediate values. An attacker who combines $d$ moments, or who has a leak that depends on $d$ shares at once, defeats masking with $d$ shares.
- **Enough noise.** The security against an attacker with many traces comes from the noise. With low noise, a higher-order attack needs few traces; the exponential growth of Chari and others assumes that each share is hidden in noise.
- **A source of randomness.** The masks must be fresh, uniform and secret for each run. A weak random number generator, or a mask that is reused across runs, removes the protection.
- **Software and hardware.** In software, one instruction usually handles one share, and the leak is close to the [probing model](/probing-model/). In hardware, glitches and transitions can combine shares in one wire, and the plain scheme needs the extra rules of a [threshold implementation](/threshold-implementation/).

## The template

The template masks one S-box lookup $y = S(p \oplus k)$ with two shares, for a public input $p$ and a key $k$. It is first-order masking by table recomputation, the classic method for software.

```pseudo id=main
MASKED-SBOX(p, k, S)            ▷ S is a table of 2^w entries
L1  m_in, m_out ← SHARE: two fresh uniform w-bit masks
L2  a ← p ⊕ m_in                  ▷ mask before the key enters
L3  x' ← a ⊕ k                    ▷ LINEAR: x' ⊕ m_in = p ⊕ k
L4  for u = 0 .. 2^w - 1 do T[u] ← S(u ⊕ m_in) ⊕ m_out    ▷ NONLINEAR
L5  y' ← T[x']                    ▷ y' ⊕ m_out = S(p ⊕ k)
L6  return (y', m_out)            ▷ REFRESH before the next use
```

The holes are:

- **SHARE.** How to split a value into shares. With $d$ shares, draw $d - 1$ uniform values $m_1, \ldots, m_{d-1}$ and set the last share to $x \oplus m_1 \oplus \cdots \oplus m_{d-1}$.
- **LINEAR.** A function $L$ that is linear over GF(2), such as XOR with a key, a bit permutation or the MixColumns step of the [AES](/advanced-encryption-standard/), is applied to each share separately, because $L(x_1) \oplus L(x_2) = L(x)$. XOR with a constant goes into one share only.
- **NONLINEAR.** A nonlinear function does not split into shares. Line L4 builds a masked table $T$ with $T[u \oplus m_{in}] = S(u) \oplus m_{out}$, at a cost of $2^w$ lookups. For higher orders, the S-box is written as a polynomial or a circuit of AND gates and each multiplication uses a gadget such as [ISW](/isw-private-circuits/).
- **REFRESH.** When one sharing is used twice, or before two sharings are combined, XOR fresh randomness into the shares so that no two wires share a mask.

Line L5 is correct because $T[x'] = S(x' \oplus m_{in}) \oplus m_{out} = S(p \oplus k) \oplus m_{out}$. Each wire alone is uniform or does not depend on $k$: $m_{in}$, $m_{out}$ and $a$ do not contain $k$; $x' = (p \oplus k) \oplus m_{in}$ is uniform because $m_{in}$ is; each entry of $T$ is uniform because $m_{out}$ is, and it does not depend on $k$; and $y'$ is uniform because $m_{out}$ is. So one probe gives nothing. A pair of wires can leak: $(m_{in}, x')$ gives $p \oplus k$, $(a, x')$ gives $k$, and $(m_{out}, y')$ gives $S(p \oplus k)$. The proof file shows this, and the tests check all 210 pairs of the 21 wires.

The cost of the template is $\Theta(2^w)$ time and space for each fresh pair of masks, against $\Theta(1)$ for an unmasked lookup.

## Classic examples

The code of this page is a small abstract model of a masked computation. It uses the 4-bit PRESENT S-box, draws the masks from a seeded `random.Random` or takes them from the caller, and returns every intermediate value as a list of named wires. It never reads a device, a file or a clock. The tests check the claims below by exhaustive enumeration of the masks, for all 16 keys.

**One masked S-box lookup.** Take $p = \texttt{3}$, $k = \texttt{B}$, $m_{in} = \texttt{5}$ and $m_{out} = \texttt{9}$. Then $a = \texttt{6}$ and $x' = \texttt{D}$. The table entry is $T[\texttt{D}] = S(\texttt{D} \oplus \texttt{5}) \oplus \texttt{9} = S(\texttt{8}) \oplus \texttt{9} = \texttt{3} \oplus \texttt{9} = \texttt{A}$. So $y' = \texttt{A}$, and $y' \oplus m_{out} = \texttt{3} = S(\texttt{3} \oplus \texttt{B})$. Over all 256 pairs of masks, each of the 21 wires has the same distribution for every key, and exactly the 3 pairs above out of 210 depend on the key.

**First-order DPA fails, second-order DPA works.** Against the unmasked lookup, a [differential power analysis](/differential-power-analysis/) or a [correlation power analysis](/correlation-power-analysis/) on $\mathrm{HW}(S(p \oplus k))$ finds the key. With masking, the mean leak of each wire is the same for every key: $\mathrm{E}[\mathrm{HW}(x \oplus m)] = 2$ for a uniform 4-bit $m$ and every $x$. But the centred product of the leaks of $x'$ and $m_{in}$ has the mean

$$\mathrm{E}\big[(\mathrm{HW}(x \oplus m) - 2)(\mathrm{HW}(m) - 2)\big] = 1 - \frac{\mathrm{HW}(x)}{2}, \qquad x = p \oplus k,$$

which depends on the key. A second-order attack correlates this product with a guess, and the [TVLA](/test-vector-leakage-assessment/) second-order test detects it.

**Masking a linear layer with three shares.** For a linear map $L$ on 4 bits and the key in three shares $k = k_1 \oplus k_2 \oplus k_3$, the device computes $x_1 = k_1 \oplus p$ and $y_i = L(x_i)$ for each share, as in a [substitution-permutation network](/substitution-permutation-network/). The tests enumerate all 256 pairs $(k_1, k_2)$ and show that every set of at most 2 of the 7 wires has the same distribution for every key, and that the 3 shares together give the key. This is second-order security for the linear part; the nonlinear part needs [ISW](/isw-private-circuits/) or a similar gadget.

**Hardware with glitches.** In a circuit, a wire can take several values during one clock cycle before it settles, and a glitch can depend on two shares that enter the same gate. A [threshold implementation](/threshold-implementation/) avoids this with three or more shares and the rule that no function sees all shares of a value.

## Variations

- **Arithmetic masking.** Share $x = x_1 + x_2 \bmod 2^n$, which fits additions modulo $2^n$ in ciphers that use them and in some public key code. Conversions between Boolean and arithmetic sharings exist, and they are a common source of leaks.
- **Multiplicative masking.** Share a field element as $x \cdot m$ with $m \ne 0$, so that inversion in GF($2^8$) for the AES S-box is easy. The value $x = 0$ stays 0 under every mask, so this masking leaks whether $x = 0$ unless it is treated apart.
- **Higher-order masking.** Use $d + 1$ shares for security against $d$ probes. Linear parts work share by share; multiplications use the [ISW](/isw-private-circuits/) gadget with $\Theta(d^2)$ random bits and operations.
- **Threshold implementations.** Shares chosen so that each component function misses at least one share, which gives security with glitches in hardware ([threshold implementation](/threshold-implementation/)).
- **Shuffling.** Not a sharing, but often used with masking: the device does independent operations, such as the 16 S-box lookups of an AES round, in a random order, so that the leak of one value is spread over several moments.

## Pitfalls

- **The wrong order.** If the device computes $p \oplus k$ before it adds the mask, that wire is not masked and one probe gives the key. The tests show that the reordered gadget leaks at exactly that wire.
- **Transitions.** Many devices leak the [Hamming distance](/hamming-distance/) between the old and the new value of a register. If a register holds $x \oplus m$ and then $m$, the leak is $\mathrm{HW}(x)$, at first order. Clear the register, or schedule the shares so that two shares of one value never follow each other in the same register.
- **Reused masks.** Software often recomputes one table for each encryption and uses it for all the S-box lookups. Then two outputs $S(x_1) \oplus m_{out}$ and $S(x_2) \oplus m_{out}$ have the same mask, and their XOR, or a transition between them, does not depend on the mask.
- **The compiler.** An optimizing compiler can simplify $(x \oplus m) \oplus m$ to $x$, or keep two shares in one register. Check the machine code, not only the source.
- **Weak masks.** Masks from a biased or predictable generator, or masks that are not fresh in each run, break the argument that each share is uniform.
- **Glitches in hardware.** Two-share masking of a nonlinear function in hardware can leak at first order because of glitches. Use a threshold implementation or a gadget with registers that stop the glitches.
- **Low noise.** Masking makes an attack need more traces. The growth in the number of traces comes from the noise, so with little noise a second-order attack needs not many more traces than a first-order attack on the unmasked device.

## Exercises

1. Show that for two shares $x_1 = m$ and $x_2 = x \oplus m$ with a uniform $m$, each share alone is uniform, whatever $x$ is.
2. Show that with three shares made by line SHARE, any two shares are uniform and independent of $x$.
3. In the example, which pairs of the 21 wires give information about $k$? Explain why the pair $(y', T[u])$ does not, for every $u$.
4. Prove that $\mathrm{E}[(\mathrm{HW}(x \oplus m) - 2)(\mathrm{HW}(m) - 2)] = 1 - \mathrm{HW}(x)/2$ for a uniform 4-bit $m$. For which $x$ is the product blind?
5. Explain why the AND of two bits $a = a_1 \oplus a_2$ and $b = b_1 \oplus b_2$ cannot be computed share by share as $(a_1 b_1, a_2 b_2)$.

## References
