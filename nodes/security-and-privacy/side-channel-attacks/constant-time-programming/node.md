---
tag: 7C93VR
kind: technique
slug: constant-time-programming
name: Constant-time programming
aliases:
- constant-time implementation
area: security-and-privacy/side-channel-attacks
level: core
summary: Writes code whose branches, memory addresses and variable-time instructions do not depend on secrets, to stop timing and cache attacks.
prereqs: [timing-attack, bit-manipulation]
see_also: [constant-time-verification, branchless-programming, twos-complement, binary-exponentiation, x25519, flush-and-reload, prime-and-probe, boolean-masking]
sources:
  - url: "https://cr.yp.to/antiforgery/cachetiming-20050414.pdf"
    title: Daniel J. Bernstein, Cache-timing attacks on AES, 2005
    locator: the AES table lookup leak, and why a load from a secret index is not constant time
  - paper: "José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir and Michael Emmi, Verifying constant-time implementations, 25th USENIX Security Symposium, 2016, pages 53-70"
    locator: "Section 2 (the constant-time disciplines: the selection by masks, the comparisons built from bit operations, and the subarray copy that reads every cell) and Section 3 (the leakage models)"
  - paper: "Paul C. Kocher, Timing attacks on implementations of Diffie-Hellman, RSA, DSS, and other systems, CRYPTO 1996, LNCS 1109, pages 104 to 113"
    locator: the timing leak of square and multiply, and the countermeasures
  - paper: "Dag Arne Osvik, Adi Shamir and Eran Tromer, Cache attacks and countermeasures, the case of AES, CT-RSA 2006, LNCS 3860, pages 1 to 20"
    locator: the cache attacks on table-based AES and the section on countermeasures
  - paper: "Daniel J. Bernstein, Curve25519, new Diffie-Hellman speed records, PKC 2006, LNCS 3958"
    locator: the design of the curve and the ladder so that a natural implementation has no secret branches and no secret indices
  - paper: doi:10.23919/DATE.2017.7927267
    title: "Oscar Reparaz, Josep Balasch and Ingrid Verbauwhede, Dude, is my code constant time?, DATE 2017, pages 1697-1702"
    locator: the statistical test of the run time of a binary on two classes of inputs
---

Constant-time programming is a discipline for code that handles secrets: no branch, no memory address, no loop count and no operand of a variable-time instruction may depend on a secret. A program that follows it gives the same observable trace for every secret, so a [timing attack](/timing-attack/) or a cache attack sees nothing that depends on the key. The tools are masks and bit operations instead of `if`, full scans instead of secret table indices, and fixed loop bounds. [Constant-time verification](/constant-time-verification/) is the check that a given program really follows the discipline.

## In plain words

A program that keeps a secret should do the same work in the same order, whatever the secret is. It should not skip a step for one key and do it for another. It should not stop early when a check fails. It should not pick a table cell with the secret, because the cache remembers which cell was read. Instead, the program does both sides of a choice and keeps one result with a bit trick. It reads every cell of a table and keeps the one it needs. It always runs a loop the same number of times. An observer who watches the time, or the cache, then sees the same thing for every secret.

## When it applies

### The observer

The discipline is a defense against an observer who sees, for each run, the control flow and the memory addresses of the program, and the time of instructions whose cost depends on their operands. That observer covers a stopwatch on the whole run, a remote timing over a network and a cache attack such as [Flush+Reload](/flush-and-reload/) or [Prime+Probe](/prime-and-probe/) on a shared machine. The guarantee holds only against this observer and only for the leakage model that the code was written for.

### The policy

Almeida et al. (2016) state the policy as a property of two runs: the sequence of branch decisions and memory addresses does not depend on the secret inputs. Many libraries add the operands of variable-time instructions, such as division, to the list. Public values may still change all three. The policy is a 2-safety property, so a single run never shows a violation; see [self-composition](/self-composition/).

### What it does not stop

- **Power and electromagnetic leaks of values.** The values still go through the wires. Against [differential power analysis](/differential-power-analysis/), add [masking](/boolean-masking/).
- **Faults.** A glitch that changes a value is outside the model. See [differential fault analysis](/differential-fault-analysis/).
- **Transient execution.** A processor can run a mispredicted path for a short time, and that path is not in the program trace. See [Spectre](/spectre-attack/).
- **Leaks of public data.** Constant time is about secrets. The policy lets the run depend on public values, such as the length of a message, so these must really be public.

## The template

```pseudo id=main
MAKE-CONSTANT-TIME(F, S)             ▷ F: a routine, S: the secret inputs and every value computed from them
L1  for each branch of F with a guard that depends on S do
L2      compute both arms and keep one with SELECT(m, a, b)   ▷ hole SELECT: m is all ones or all zeros
L3  for each memory access of F with an index that depends on S do
L4      replace it by SCAN(table, index)                       ▷ hole SCAN: read every cell, or a bitsliced form
L5  for each loop of F with a count that depends on S do
L6      run it to a public bound and mask the work of the extra iterations
L7  for each early exit of F on a condition that depends on S do
L8      collect the condition in a flag and test the flag once at the end
L9  for each instruction of F whose time depends on an operand in S do
L10     replace it by a fixed-time sequence                    ▷ hole: the variable-time instructions of the target
L11 check the result against the policy                        ▷ hole CHECK: a verifier, a type system or a test
```

**The masks.** Let $b \in \{0, 1\}$ be a secret bit in a $w$-bit word. Then $m = 0 - b$ is all ones when $b = 1$ and all zeros when $b = 0$, in [two's complement](/twos-complement/). The select is

$$\text{SELECT}(m, a, c) = (a \mathbin{\&} m) \mid (c \mathbin{\&} \lnot m),$$

which is $a$ when $m$ is all ones and $c$ when $m$ is zero, with the same operations in both cases. Comparisons give the bit $b$ without a branch. For words $x$ and $y$, let $d = x \oplus y$. The top bit of $d \mid (0 - d)$ is 1 exactly when $d \ne 0$, so

$$\text{EQ}(x, y) = 1 - \big((d \mid (0 - d)) \gg (w - 1)\big).$$

A less-than test is built in the same way from the top bit of $x - y$ with a correction for the overflow, as in the `ct_lt` of Almeida et al.

**The scan.** To read $T[s]$ for a secret $s$ in a table of $k$ cells, compute

$$r = \bigvee_{j=0}^{k-1} \big(T[j] \mathbin{\&} (0 - \text{EQ}(j, s))\big).$$

The addresses are $T[0], \ldots, T[k-1]$ for every $s$, so the cache sees the same accesses. The cost is $k$ loads instead of 1. Bitsliced code avoids tables altogether: it computes the S-box as a fixed circuit of AND, XOR and NOT on many blocks at once.

**Why it works (theorem, in the model).** If every branch guard, every address and every variable-time operand is a function of public values only, then by induction on the run, two runs with the same public inputs take the same steps with the same addresses, so they give the same trace. Any cost that is a function of the trace, such as the hit and miss count of an abstract cache with $S$ sets, $W$ ways and LRU replacement, is then the same too. This is the statement that [constant-time verification](/constant-time-verification/) checks.

## Classic examples

- **Comparing a tag.** A byte-wise `memcmp` that returns at the first difference runs longer when more leading bytes match, so the observer learns the length of the matching prefix. The constant-time form computes $d = \bigvee_i (t_i \oplus g_i)$ over all bytes and returns EQ$(d, 0)$. Every check of a [message authentication code](/message-authentication-code/) tag and every padding check should look like this; see [padding oracle attack](/padding-oracle-attack/).
- **Exponentiation.** Square and multiply does an extra multiplication for each 1 bit, which Kocher (1996) measured. The Montgomery ladder of [binary exponentiation](/binary-exponentiation/) does one squaring and one multiplication for each bit, and a conditional swap by masks picks the operands, so the trace is the same for every exponent of the same length.
- **AES tables.** The fast table form of the [Advanced Encryption Standard](/advanced-encryption-standard/) reads tables at indices that depend on the key and the data. Bernstein (2005) and Osvik, Shamir and Tromer (2006) recovered keys from the cache. Bitsliced code, or the AES instructions of the processor, removes the secret indices.
- **X25519.** [X25519](/x25519/) was designed with a ladder of fixed length and field arithmetic without data-dependent branches, so a direct implementation already follows the policy.
- **Full-scan lookup.** The masked lookup in the example of [constant-time verification](/constant-time-verification/) reads all 4 cells of a table and keeps one. The verifier accepts it, and it rejects the direct lookup.

## Variations

- **Constant-time selection libraries.** Most cryptographic libraries put the masks in a few small functions, such as select, equal and less-than, and build everything else from them, so that one review covers them.
- **Bitslicing.** Store bit $i$ of many blocks in one word, and compute an S-box as a fixed Boolean circuit. There are no tables and no secret indices.
- **Hardware instructions.** AES and carry-less multiply instructions of the processor have a fixed time on the processors that document them. Some processors also offer a mode in which a list of instructions has a time that does not depend on the data.
- **Compilers for the policy.** Languages and compilers for cryptographic code check the policy on the source and keep it through the compilation.
- **Blinding instead.** [RSA blinding](/rsa-blinding/) does not remove the leak, but it makes the leak a function of a fresh random value. It works with constant-time code, not instead of it.

## Pitfalls

- **The compiler.** An optimizer can turn a masked select back into a branch, or a scan into a lookup, because the result is the same. Check the machine code, or use the verifier on the compiled form.
- **Variable-time instructions.** Division, and on some processors multiplication, take a time that depends on the operands. A loop with a fixed count is not constant time if its body uses them on secrets.
- **The bit from a comparison.** `x == y` in C may compile to a branch. Build the bit from the formula above.
- **Early returns on errors.** An error path that returns sooner is a leak. Compute the result and the error flag with the same work, and return one value at the end.
- **A test is not a proof.** A statistical test such as dudect measures one machine on some inputs. It can show a leak, but it cannot show that there is none.
- **A model is not the hardware.** The policy says nothing about speculation, power or faults. Name the observer that the code defends against.

## Exercises

1. Show that SELECT$(0 - b, a, c)$ is $a$ for $b = 1$ and $c$ for $b = 0$ in any word size.
2. Write a constant-time function that returns the index of the first zero byte of a buffer of public length, with the same accesses for every buffer.
3. A routine runs a loop $\lceil \log_2 (s + 1) \rceil$ times for a secret $s < 2^{64}$. Change it so that it is constant time, and give the cost of the change.

## References
