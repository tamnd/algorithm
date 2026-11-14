---
tag: 749N61
kind: definition
slug: safe-replaceability
name: Safe replaceability
aliases:
- Pixley equivalence
area: eda/hardware-verification
level: advanced
summary: A design safely replaces another if every output sequence that it can give from any power-up state, the old design can also give from some power-up state.
prereqs: [mealy-machine, product-machine, sequential-equivalence-checking]
see_also: [retiming, product-construction, trace-equivalence, simulation-relation, latch-mapping, state-assignment, minimum-area-retiming, dfa-equivalence]
sources:
  - paper: "Vigyan Singhal and Carl Pixley, The verification problem for safe replaceability, Computer Aided Verification (CAV 1994), Lecture Notes in Computer Science 818, 311 to 323, 1994"
    title: V. Singhal and C. Pixley, The verification problem for safe replaceability, CAV 1994, LNCS 818, 311 to 323
    locator: the definition of safe replacement with no assumption on the initial state, and the methods to check it
  - paper: "Carl Pixley, Vigyan Singhal, Adnan Aziz and Robert K. Brayton, Multi-level synthesis for safe replaceability, Proceedings of the International Conference on Computer-Aided Design, 442 to 449, 1994"
    title: C. Pixley, V. Singhal, A. Aziz and R. K. Brayton, Multi-level synthesis for safe replaceability, ICCAD 1994, 442 to 449
    locator: the use of safe replacement as the correctness notion for sequential logic optimization
  - paper: "Vigyan Singhal, Carl Pixley, Adnan Aziz and Robert K. Brayton, Theory of safe replacements for sequential circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 20(2), 249 to 265, 2001"
    title: V. Singhal, C. Pixley, A. Aziz and R. K. Brayton, Theory of safe replacements for sequential circuits, IEEE TCAD 20(2), 249 to 265, 2001
    locator: the full theory, its comparison with other notions of equivalence for designs without reset, and its use in any environment
  - paper: "Vigyan Singhal, Carl Pixley, Richard L. Rudell and Robert K. Brayton, The validity of retiming sequential circuits, Proceedings of the 32nd Design Automation Conference, 316 to 321, 1995"
    title: V. Singhal, C. Pixley, R. L. Rudell and R. K. Brayton, The validity of retiming sequential circuits, DAC 1995, 316 to 321
    locator: when a retimed circuit is a safe replacement of the original, and the delay after which it becomes one
  - paper: "Carl Pixley, A theory and implementation of sequential hardware equivalence, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 11(12), 1469 to 1478, 1992"
    title: C. Pixley, A theory and implementation of sequential hardware equivalence, IEEE TCAD 11(12), 1469 to 1478, 1992
    locator: equivalence of designs without reset based on aligning sequences, the earlier notion that safe replacement is compared with
---

Safe replaceability is a correctness notion for designs that have no reset, so that they can power up in any state. A new design $D'$ safely replaces an old design $D$ if, for every power-up state of $D'$ and every input sequence, some power-up state of $D$ gives the same output sequence. Then no environment that only drives the inputs and watches the outputs can tell that $D$ was replaced, because whatever $D'$ does, $D$ could also have done. Singhal and Pixley (1994) defined it. It needs no initial state and no aligning input sequence. So it differs from [sequential equivalence checking](/sequential-equivalence-checking/) from a reset state, which is a reachability question on the [product machine](/product-machine/), and from the earlier notion of Pixley (1992), which asks that some input sequence bring the two designs to states with the same behaviour.

## Definition

Let $M = (X, Y, S, \delta, \lambda)$ and $M' = (X, Y, S', \delta', \lambda')$ be deterministic [Mealy machines](/mealy-machine/) with the same inputs and outputs and no initial state. For a state $s$ and an input sequence $\pi = x^0 \cdots x^t$, write $\lambda(s, \pi)$ for the output sequence that $M$ gives from $s$ on $\pi$.

$M'$ is a *safe replacement* for $M$, written $M' \sqsubseteq M$, if

$$\forall s' \in S'\ \ \forall \pi \in X^*\ \ \exists s \in S : \quad \lambda'(s', \pi) = \lambda(s, \pi).$$

The state $s$ may depend on $\pi$. A state of $M$ that agrees with $s'$ on every input sequence is not required.

**Proposition 1 (preorder).** $\sqsubseteq$ is reflexive and transitive, and it is not symmetric.

*Proof.* Reflexive: take $s = s'$. Transitive: if $M'' \sqsubseteq M'$ and $M' \sqsubseteq M$, then for $s''$ and $\pi$ there is $s'$ with $\lambda''(s'', \pi) = \lambda'(s', \pi)$, and then $s$ with $\lambda'(s', \pi) = \lambda(s, \pi)$. The fanout example below is not symmetric. $\square$

**Proposition 2 (a language inclusion).** Let $N$ be $M$ read as a nondeterministic machine in which every state is initial, and let $T(N)$ be the set of input-output sequences of $N$. Then $M' \sqsubseteq M$ if and only if $T(M') \subseteq T(N)$, where $M'$ also starts in every state.

*Proof.* Both sides say that every pair $(\pi, \lambda'(s', \pi))$ equals $(\pi, \lambda(s, \pi))$ for some $s$. $\square$

So an exact check is an inclusion into a nondeterministic machine. It follows sets of states of $M$ that are still consistent with the outputs seen, as in the subset construction, and $M' \sqsubseteq M$ fails exactly when some input sequence from some state of $M'$ makes that set empty. The number of such sets can be exponential in the number of states of $M$, which is why cheaper sufficient tests, such as a simulation relation (see below), are attractive.

## Examples and non-examples

**Retiming forward across a fanout.** $D$ has one latch $r$ with next value $a$ and two outputs $o_1 = r$ and $o_2 = r$. Retiming the latch forward across the fanout gives $D'$ with two latches $r_1, r_2$, both with next value $a$, and outputs $o_1 = r_1$ and $o_2 = r_2$.

- $D$ is a safe replacement for $D'$. For a state $r$ of $D$, take $r_1 = r_2 = r$; the outputs then agree on every input sequence.
- $D'$ is *not* a safe replacement for $D$. The power-up state $r_1 r_2 = 01$ gives $o_1 o_2 = 01$ on the first cycle for every input, and $D$ always gives $o_1 = o_2$. So no state of $D$ matches.
- After one clock cycle, $D'$ is in a state with $r_1 = r_2$, and from then on it behaves like $D$. One cycle of any input brings every pair of states of the two designs to a pair with the same behaviour, so the two designs are equivalent in the sense of Pixley (1992), but not in both directions in the sense of safe replacement. Safe replacement counts the first cycle; the earlier notion does not.

Singhal, Pixley, Rudell and Brayton (1995) studied this effect of [retiming](/retiming/) in general: a retimed circuit need not be a safe replacement, but it becomes one after a bounded number of clock cycles. We do not prove their bound here.

**A different state encoding.** If $M'$ is $M$ with its states renamed by a bijection, then $M' \sqsubseteq M$ and $M \sqsubseteq M'$: take the matching state. This is the case of [state assignment](/state-assignment/) with all codes used.

**Safe replacement, but not equivalence from reset.** Let $M$ be a 2-bit counter that outputs 1 when it holds 3, and let $M'$ output 1 when it holds 2. Both count up by 1 on every clock and ignore the input. From state $c$, $M'$ outputs 1 at the clocks $t$ with $c + t \equiv 2 \pmod 4$, and $M$ from state $c + 1 \bmod 4$ outputs 1 at the same clocks. So each state of $M'$ is matched by a state of $M$ for all input sequences, the reverse holds in the same way, and the two are safe replacements of each other. With a reset to 0, the same designs are not equivalent: the first 1 comes at clock 2 in $M'$ and at clock 3 in $M$. Without a reset, the environment cannot know the phase.

## Related definitions

- [Sequential equivalence checking](/sequential-equivalence-checking/) fixes one initial state for each design and asks for equal outputs. It is the right notion when a reset exists.
- The earlier notion of Pixley (1992) asks for an aligning sequence after which the two designs are in states with the same behaviour. Safe replacement needs no such sequence and holds from the first cycle.
- [Trace equivalence](/trace-equivalence/) of transition systems is the symmetric closure of the inclusion in Proposition 2, with all states initial.
- A [simulation relation](/simulation-relation/) from $M'$ to $M$ that relates each state of $M'$ to some state of $M$ is a sufficient condition for $M' \sqsubseteq M$: the related state matches $s'$ on every sequence at once. It is not necessary, because safe replacement lets the state of $M$ depend on $\pi$.
- [Latch mapping](/latch-mapping/) with a combinational check gives equivalence from all states of a matched pair, so it also gives safe replacement in both directions when the mapping is a bijection of all latches.

## References
