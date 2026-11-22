---
tag: 2DGQ49
kind: technique
slug: differential-fault-analysis
name: Differential fault analysis
aliases:
- DFA attack
- Biham-Shamir fault attack
area: security-and-privacy/side-channel-attacks
level: core
summary: A fault attack on ciphers that compares the correct output and a faulty output for the same input, and keeps only the keys that some fault of the model can explain.
prereqs: [block-cipher, differential-cryptanalysis]
see_also: [rsa-fault-attack, rowhammer, differential-power-analysis, side-channel-attack, advanced-encryption-standard, s-box, error-detection, timing-attack]
sources:
  - paper: "Eli Biham and Adi Shamir, Differential fault analysis of secret key cryptosystems, CRYPTO 1997, LNCS 1294, pages 513-525"
    locator: the fault model of random transient bit errors, the analysis of DES from pairs of correct and faulty ciphertexts, and the extension to unknown ciphers
  - paper: "Dan Boneh, Richard A. DeMillo and Richard J. Lipton, On the importance of checking cryptographic protocols for faults, EUROCRYPT 1997, LNCS 1233, pages 37-51"
    locator: the fault attacks on RSA with the Chinese remainder theorem and on other public key schemes, and the defense of checking the result before output
  - paper: "Gilles Piret and Jean-Jacques Quisquater, A differential fault attack technique against SPN structures, with application to the AES and KHAZAD, CHES 2003, LNCS 2779"
    locator: the byte fault model in the last rounds of a substitution-permutation network
---

Differential fault analysis is a method that learns the key of a cipher from faulty outputs. The attacker runs the device on an input and gets the correct output, then runs it on the same input while a fault disturbs the computation and gets a faulty output. The difference of the two outputs depends on the key and on the fault, and a model of the possible faults lets the attacker keep only the keys that explain the pair. Biham and Shamir (1997) gave the method for block ciphers such as DES, after Boneh, DeMillo and Lipton (1997) had shown that one fault in RSA with the Chinese remainder theorem gives away the key; see [RSA fault attack](/rsa-fault-attack/). The defenses check the result before the device outputs it, and stop faults with sensors and redundancy.

## In plain words

A safe gives the same answer to the same question every time. Suppose you can shake the safe at the right moment, so that it makes a small mistake while it computes the answer. Now you have two answers to one question, a right one and a wrong one.

The wrong answer is not random. It is the right computation with one small change in the middle, and the size and place of the change are limited. If you guess the key, you can check whether some small change explains the two answers. Most guesses fail that check. With a few pairs, only the true key is left. The cure is for the safe to check its answer before it gives it out.

## When it applies

### Threat model

The attacker holds or controls a device that computes with a secret key, such as a smart card, a hardware module or a process on a shared machine. He can choose or repeat the input, he can disturb the computation, and he sees the output. He cannot read the key directly. The fault model says which faults he can cause: for example one random bit, or one random byte, in a chosen part of the computation. The defenses below are stated against this attacker and this fault model.

### Conditions

1. **REPEAT.** The attacker can get outputs for the same input with and without a fault. Some variants need only faulty outputs, with a known or a statistical input.
2. **FAULT.** He can cause a fault that fits the model, by a change of supply voltage or clock, by light or an electromagnetic pulse on the chip, or from software through effects such as [Rowhammer](/rowhammer/) or a change of the operating voltage.
3. **OUTPUT.** The device gives out the faulty result.
4. **STRUCTURE.** The fault reaches the output through only a few rounds of the cipher, so that the key of those rounds can be tested piece by piece.

### What removes a condition

| defense | condition it removes | cost |
|---|---|---|
| compute twice, or compute and invert, and output only if the results agree | 3, for faults that hit only one of the two computations | about twice the work, or the work of the inverse |
| check the result before output, as Boneh, DeMillo and Lipton propose | 3 | the work of the check, for RSA one public operation |
| error detecting codes on the state, such as parity on each byte | 3, for the faults the code detects | extra logic in each round |
| sensors for voltage, clock, light and temperature, and an active shield | 2 | chip area and false alarms |
| randomized inputs that the attacker cannot repeat, and limits on the number of operations | 1 | a protocol change |

**Claim (theorem, in an abstract model).** Let the device compute $y = E_K(x)$ twice and output $y$ only if both results agree. If the attacker can change at most one of the two computations, then every value that the device outputs is the correct $E_K(x)$, so a faulty output never leaves the device. *Proof.* If neither computation is changed, both give $E_K(x)$. If exactly one is changed and its result differs, the results differ and nothing is output. If its result does not differ, the output is $E_K(x)$. The model fails when the same fault hits both computations in the same way, which is why devices also put the two computations apart in time or use different code for them.

## The template

The stages are those of the published method at the level of the abstract of Biham and Shamir, with named holes and no parameters.

```pseudo id=main
FAULT-ANALYSIS-SHAPE(device D with key K, fault model F)
L1  obtain the correct output of D for an input              ▷ hole REPEAT
L2  obtain an output of D for the same input under a fault   ▷ hole FAULT: removed by sensors
L3  for each candidate value of a small part of the key do
L4      keep it if some fault in F explains the pair           ▷ hole MODEL: the faults that F allows
L5  repeat with new pairs until one candidate is left
L6  the attack fails if D checks its result before output     ▷ the defense of Boneh, DeMillo and Lipton
```

### An abstract model

Take a made-up last round $y = S(u) \oplus k$, where $u$ is the state before a 4-bit [S-box](/s-box/) $S$ and $k$ is a 4-bit round key. A fault of the model flips one bit of $u$, giving $u \oplus e$ with $e$ of weight 1, and the faulty output is $y^* = S(u \oplus e) \oplus k$. Then

$$y \oplus y^* = S(u) \oplus S(u \oplus e),$$

so the round key cancels out of the difference of the outputs. For a candidate key $\hat k$, the value $\hat u = S^{-1}(y \oplus \hat k)$ is the state that the candidate predicts. The candidate stays only if $S(\hat u) \oplus S(\hat u \oplus e) = y \oplus y^*$ for some $e$ of weight 1. The true key always stays. Each pair removes the candidates whose predicted state does not fit, in the same way as a differential characteristic does in [differential cryptanalysis](/differential-cryptanalysis/). If the device checks its result, neither $y^*$ nor any other faulty value is output, and the set of candidates stays the full set.

### Differential fault analysis and the RSA fault attack

The [RSA fault attack](/rsa-fault-attack/) of Boneh, DeMillo and Lipton is algebraic: in RSA with the Chinese remainder theorem, one faulty signature is correct modulo one prime factor and wrong modulo the other, and this difference reveals the factor. Differential fault analysis is statistical and works on symmetric ciphers, where no such algebra exists: each pair only narrows the set of key candidates. Both have the same cure, a check of the result before output.

## Classic examples

- **Boneh, DeMillo and Lipton, 1997.** One fault in an RSA signature with the [Chinese remainder theorem](/chinese-remainder-theorem/) reveals a factor of the modulus. They also gave fault attacks on other public key schemes and proposed the check before output.
- **Biham and Shamir, 1997.** They applied the idea to DES and to other secret key ciphers, under a model of random transient bit errors in the last rounds, and showed that the method works even when the cipher is unknown.
- **AES, 2003.** Piret and Quisquater gave a differential fault analysis of substitution-permutation networks, with the [Advanced Encryption Standard](/advanced-encryption-standard/) as an example, under a model of a fault in one byte of the state in the last rounds.
- **Software faults, from 2014 on.** [Rowhammer](/rowhammer/) and later the control of the operating voltage of processors showed that some faults need no physical access, which brought fault analysis to shared machines.

## Variations

- **Fault models.** A bit, a byte or a word; random or chosen value; a skipped instruction; a stuck bit. The analysis changes with the model, and the defense must cover the models that the attacker can reach.
- **Statistical fault analysis.** Use only faulty outputs, and look for a bias in the distribution of the state that the fault causes.
- **Safe-error and ineffective faults.** Learn from whether a fault changes the output at all, which can defeat a defense that hides the output of a detected fault but still shows that a fault was detected.
- **Combined attacks.** A fault that switches off a defense against [power analysis](/differential-power-analysis/), or a power trace that guides a fault.

## Pitfalls

- **Checking with the same code.** Two runs of the same code can fail in the same way under the same fault. Use an inverse, a different code path or a separation in time.
- **Giving a fault signal.** An error message that says a fault was detected tells the attacker that his fault worked, which is enough for some variants. Some designs answer with a random output instead.
- **Trusting a rare fault.** The attacker repeats; a fault that works once in many tries is enough.
- **Mixing up names.** In this area the method is called differential fault analysis in full. The short form used for it elsewhere also names the deterministic finite automaton of automata theory.

## References
