---
tag: 2H1XG6
kind: model
slug: probing-model
name: Probing model
aliases:
- t-probing model
- ISW probing model
area: security-and-privacy/side-channel-attacks
level: advanced
summary: "Models an attacker who can read the values of up to t wires of a circuit, and calls the circuit secure if those values reveal nothing."
prereqs: [boolean-masking, boolean-circuit]
see_also: [isw-private-circuits, threshold-implementation, side-channel-attack, test-vector-leakage-assessment, secret-sharing, noninterference, circuit-complexity, differential-power-analysis]
sources:
  - paper: "Yuval Ishai, Amit Sahai and David Wagner, Private circuits: securing hardware against probing attacks, CRYPTO 2003, LNCS 2729, pages 463 to 481"
    locator: "the definition of t-private circuits by a simulator, the stateless and stateful variants, and the compiler with 2t + 1 shares"
  - paper: doi:10.1007/978-3-642-15031-9_28
    title: "Matthieu Rivain and Emmanuel Prouff, Provably secure higher-order masking of AES, CHES 2010, LNCS 6225, pages 413 to 427"
    locator: "the proof that the multiplication gadget is secure against t probes with t + 1 shares"
  - paper: doi:10.1007/978-3-662-43933-3_21
    title: "Jean-Sébastien Coron, Emmanuel Prouff, Matthieu Rivain and Thomas Roche, Higher-order side channel security and mask refreshing, FSE 2013, LNCS 8424, pages 410 to 424"
    locator: the flaw in the composition of gadgets with a weak mask refresh, and the refresh based on the multiplication gadget
  - paper: doi:10.1007/978-3-642-38348-9_9
    title: "Emmanuel Prouff and Matthieu Rivain, Masking against side-channel attacks: a formal security proof, EUROCRYPT 2013, LNCS 7881, pages 142 to 159"
    locator: the noisy leakage model and the proof of masked computation in it
  - paper: doi:10.1007/978-3-642-55220-5_24
    title: "Alexandre Duc, Stefan Dziembowski and Sebastian Faust, Unifying leakage models: from probing attacks to noisy leakage, EUROCRYPT 2014, LNCS 8441, pages 423 to 440"
    locator: the reduction from the noisy leakage model to the random probing and the t-probing models
  - paper: doi:10.1145/2976749.2978427
    title: "Gilles Barthe, Sonia Belaïd, François Dupressoir, Pierre-Alain Fouque, Benjamin Grégoire, Pierre-Yves Strub and Rébecca Zucchini, Strong non-interference and type-directed higher-order masking, ACM CCS 2016, pages 116 to 129"
    locator: the definitions of t-non-interference and t-strong non-interference and the composition theorems
---

The probing model is a model of the attacker against a masked implementation. The implementation is a [Boolean circuit](/boolean-circuit/) that also has gates that output fresh random bits. Before a run, the attacker chooses a set of at most $t$ wires, and after the run it learns the values on those wires. The circuit is secure at order $t$ if the values on any such set have a distribution that does not depend on the secret. Ishai, Sahai and Wagner (2003) defined the model and gave a compiler that makes any circuit secure in it. The model abstracts a [side-channel attack](/side-channel-attack/) of order $t$: an attacker who combines the leaks of $t$ intermediate values, each with no noise. It counts the number of shares and the gates and random bits needed for a given $t$.

## The machine

- **The circuit.** A circuit over GF(2) with gates for XOR, AND and NOT, and random gates with no inputs, each of which outputs a fresh uniform bit in each run. Other works use circuits over a larger field, such as GF($2^8$) for the [AES](/advanced-encryption-standard/), with the same rules.
- **The encoding.** A secret input $x$ enters as a sharing: $n$ shares $x_1, \ldots, x_n$ with $x = x_1 \oplus \cdots \oplus x_n$, made by an encoder from $n - 1$ fresh random values, as in [Boolean masking](/boolean-masking/). The output leaves as a sharing too. The encoder and the decoder are outside the attack; the attacker can probe only the wires of the circuit between them.
- **The attacker.** The attacker chooses a set $P$ of at most $t$ wires before the run. In one run, it sees the values of the wires in $P$ and nothing else. The wires carry one value each, and they do not leak anything that is not on them.
- **Security.** The circuit is $t$-probing secure if for every set $P$ with $|P| \le t$ there is a simulator that, without the secret, outputs values with the same joint distribution as the wires in $P$. For a fixed $P$, this is the same as asking that the distribution of the values on $P$ is the same for every secret.
- **Stateful circuits.** Ishai, Sahai and Wagner also define circuits with memory that run for many clock cycles. The memory holds a sharing that is refreshed in each cycle, and the attacker may choose a new set of $t$ wires in each cycle.

A small example from the [ISW](/isw-private-circuits/) page: the masked AND gate for two shares has 13 wires. Each single wire has the same distribution for each of the 4 pairs of input bits, so the gate is 1-probing secure. But 22 of the 78 pairs of wires depend on the inputs, so it is not 2-probing secure. With 3 shares the gate has 30 wires, every set of at most 2 wires is secure, and 197 of the 4060 sets of 3 wires are not.

## What it counts

- **The order $t$.** The largest number of probes for which the circuit is secure. Order 1 is first-order masking.
- **The number of shares $n$.** At least $t + 1$ shares are needed, because $t$ probes on the shares of a value with $n \le t$ shares give the value.
- **The size.** The number of gates of the compiled circuit, against the size $s$ of the original circuit, and the number of random bits. For a multiplication with $n$ shares, the ISW gadget uses $n(n - 1)/2$ random bits and $\Theta(n^2)$ gates.
- **Exhaustive checks.** For a small gadget, security can be checked by listing every set of at most $t$ wires and comparing the distributions for every secret. The number of sets grows as $\binom{W}{t}$ for $W$ wires, so this works only for small gadgets and small $t$; tools that verify masking use more clever methods.

## Relation to other models

- **The noisy leakage model.** Each operation leaks a noisy function of all its inputs, as in the model of Chari, Jutla, Rao and Rohatgi for [Boolean masking](/boolean-masking/) and in the model of Prouff and Rivain (2013). This is closer to real power traces. Duc, Dziembowski and Faust (2014) showed that security in the probing model implies security in the noisy leakage model, through the random probing model, with a loss in the noise parameter.
- **The random probing model.** Each wire leaks its value with a fixed probability $\varepsilon$, independently of the others. It sits between the noisy model and the $t$-probing model in the reduction of Duc and others.
- **Non-interference.** The security of a gadget can be stated as a [noninterference](/noninterference/) property: the values on the probed wires depend on at most a given number of shares of each input. Barthe and others (2016) define $t$-non-interference ($t$-NI) and $t$-strong non-interference ($t$-SNI), in which the probes on internal wires must be simulated with a number of input shares that does not grow with the probes on the outputs.
- **Glitches and transitions.** The model assumes that a wire carries one value. In hardware, a glitch can carry a function of several shares, and a register can leak the [Hamming distance](/hamming-distance/) of two values. [Threshold implementations](/threshold-implementation/) were made for this case. Later work extends the probes so that one probe on a wire also gives the inputs of the gates that feed it, back to the last register.
- **Statistics of attacks.** A $t$-th order [DPA](/differential-power-analysis/) or a $t$-th order [TVLA](/test-vector-leakage-assessment/) test combines $t$ samples of the traces. The probing model says such attacks and tests find nothing for a $t$-probing secure circuit, if each sample depends on one wire.

## Known results in the model

- **The ISW compiler.** Ishai, Sahai and Wagner (2003) compile any circuit of size $s$ into one that is $t$-probing secure, with $2t + 1$ shares of each wire and a size of $O(s t^2)$. Linear gates work share by share; each AND gate uses the ISW gadget with random bits.
- **$t + 1$ shares.** Rivain and Prouff (2010) proved that the ISW multiplication is $t$-probing secure with $t + 1$ shares, which is optimal, and used it in GF($2^8$) to mask the AES S-box at any order.
- **Composition.** Secure gadgets do not always compose into a secure circuit. Coron, Prouff, Rivain and Roche (2013) found a flaw in the composition of the gadgets of Rivain and Prouff with a weak mask refresh, and fixed it with a refresh based on the multiplication gadget. Barthe and others (2016) showed that the ISW multiplication is $t$-SNI and that a circuit made of $t$-NI and $t$-SNI gadgets, with SNI refresh gadgets at the right places, is $t$-probing secure.
- **Noisy leakage.** Prouff and Rivain (2013) proved the security of masked computation in a noisy leakage model, and Duc, Dziembowski and Faust (2014) reduced the noisy model to the probing model, so that a $t$-probing secure circuit with enough noise resists attacks on noisy traces.
- **Lower bound on shares.** No circuit with $n \le t$ shares of a secret input is $t$-probing secure, because the $n$ input wires together give the secret.

## References
