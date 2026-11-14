---
tag: 10EBSW
kind: problem
slug: latch-mapping
name: Latch mapping
aliases:
- register matching
- register correspondence for equivalence checking
area: eda/hardware-verification
level: core
summary: Pair the registers of two sequential designs so that combinational equivalence checking can compare their next-state and output functions.
prereqs: [miter-circuit, boolean-equivalence-checking, sequential-equivalence-checking]
see_also: [retiming, signal-correspondence, cutpoint-equivalence-checking, gemini-netlist-comparison, graph-isomorphism-problem, partition-refinement, safe-replaceability, product-machine]
sources:
  - paper: "Jerry R. Burch and Vigyan Singhal, Robust latch mapping for combinational equivalence checking, Proceedings of the International Conference on Computer-Aided Design, 563 to 569, 1998"
    title: J. R. Burch and V. Singhal, Robust latch mapping for combinational equivalence checking, ICCAD 1998, 563 to 569
    locator: the latch mapping problem, the functional method that does not rely on names, and its results on industrial designs
  - paper: "Jerry R. Burch and Vigyan Singhal, Tight integration of combinational verification methods, Proceedings of the International Conference on Computer-Aided Design, 570 to 576, 1998"
    title: J. R. Burch and V. Singhal, Tight integration of combinational verification methods, ICCAD 1998, 570 to 576
    locator: the combinational check that runs after the latches are mapped
  - book: doi:10.1007/978-1-4615-0817-5_13
    title: A. Kuehlmann and C. A. J. van Eijk, Combinational and sequential equivalence checking, in S. Hassoun and T. Sasao (editors), Logic Synthesis and Verification, Kluwer, 2002, 343 to 372
    locator: the reduction of sequential equivalence to combinational equivalence by a register correspondence, and register correspondence by induction
---

Latch mapping pairs each latch of one sequential design with a latch of the other, so that two designs with the same register structure can be compared by a combinational check. Once each latch output and its partner are the same free variable, the next-state function of each latch and the output functions become combinational functions of the inputs and the latch values, and a [miter](/miter-circuit/) compares them. On this page "mapping" means this correspondence between latches, not technology mapping. If the paired functions are equal and the initial values agree, the designs are [sequentially equivalent](/sequential-equivalence-checking/). The converse fails: designs changed by [retiming](/retiming/) or by state re-encoding have no such pairing, and then a sequential method is needed. Burch and Singhal (1998) made latch mapping robust to the loss of names in synthesis.

## In plain words

Two versions of a chip should do the same thing. The memory cells of one usually have partners in the other, but synthesis tools rename cells, so you cannot match them by name. If you can find the right partner for every cell, you can cut the chips open at the memory cells and check the logic between them, one cell at a time, as if there were no memory at all. That check is much easier. The hard part is to find the partners, and to notice when there are none.

## Definition

**Input.** Two synchronous circuits $C_1$ and $C_2$ with the same primary inputs $x$ and outputs. $C_1$ has latches $r_1, \ldots, r_L$ with next-state functions $\delta_i$ and initial values $a_i$, and $C_2$ has latches $r'_1, \ldots, r'_L$ with $\delta'_j$ and $a'_j$. The output functions are $\lambda$ and $\lambda'$. All are functions of the inputs and the latch outputs.

**Mapping.** A bijection $\varphi : \{1, \ldots, L\} \to \{1, \ldots, L\}$, with an optional polarity $\sigma_i \in \{0, 1\}$ for latches that store an inverted value. Under $\varphi$, the latch output $r'_{\varphi(i)}$ is replaced by the variable $r_i \oplus \sigma_i$, so that all functions are over $x$ and $r$.

**Output.** A mapping that is *valid*:

- $\delta'_{\varphi(i)}(x, r) = \delta_i(x, r) \oplus \sigma_i$ for every $i$ and every $(x, r)$;
- $\lambda'(x, r) = \lambda(x, r)$ for every $(x, r)$;

or the answer that none exists. The initial values are checked apart: $a'_{\varphi(i)} = a_i \oplus \sigma_i$.

**Proposition (soundness).** If $\varphi$ is valid and the initial values agree, then $C_1$ and $C_2$ are sequentially equivalent.

*Proof.* Let $\rho(r)$ be the state of $C_2$ with $r'_{\varphi(i)} = r_i \oplus \sigma_i$. We show by induction on $t$ that after any $t$ inputs, $C_2$ is in $\rho(s)$ when $C_1$ is in $s$. At $t = 0$ this is the agreement of the initial values. If it holds at $t$ with input $x$, then latch $\varphi(i)$ of $C_2$ gets $\delta'_{\varphi(i)}$ at $\rho(s)$, which is $\delta_i(x, s) \oplus \sigma_i$ by validity, so the next state is $\rho(\delta(s, x))$. The output functions agree at every $(x, s)$, so the outputs agree at every step. $\square$

## Variants

- **Many to one.** Synthesis can duplicate a latch, or remove one that is constant or that copies another. Then the mapping pairs classes of latches, not single latches, and constant latches are mapped to constants.
- **Unequal latch counts.** After [retiming](/retiming/), the counts differ, and no mapping exists. Methods then check the retimed circuit against the original with the retiming lags, or fall back on [sequential equivalence](/sequential-equivalence-checking/).
- **Register correspondence by induction.** Ask only that paired latches hold equal values in every reachable state, not that the next-state functions be equal everywhere. This weaker notion is the latch part of [signal correspondence](/signal-correspondence/); its combinational check is relative to the assumption that the pairs are equal.
- **Partial mapping.** Map what is clear, cut the rest as free inputs, and accept the risk of false negatives.

## Examples

**Swapped latches.** $C_1$ has latches $p, q$ with $p^+ = a$, $q^+ = p \wedge b$ and output $q$. $C_2$ has latches $u, v$ with $u^+ = v \wedge b$, $v^+ = a$ and output $u$. The mapping $p \mapsto v$, $q \mapsto u$ is valid: $v^+ = a = p^+$, $u^+ = v \wedge b$ becomes $p \wedge b = q^+$, and the outputs are $u$ and $q$. The mapping $p \mapsto u$, $q \mapsto v$ is not: it would need $u^+ = v \wedge b$, which becomes $q \wedge b$, to equal $p^+ = a$.

**An inverted latch.** If $C_2$ stores $\neg p$ in a latch $w$ with $w^+ = \neg a$ and uses $\neg w$ where $C_1$ uses $p$, the mapping $p \mapsto w$ with polarity 1 is valid.

**Equivalent, but no valid mapping.** $C_1$ has latches $p, q$, both with next value $p \oplus x$ and initial value 0, and output $p \wedge q$. $C_2$ has latches $u, w$, both with next value $u \oplus x$ and initial value 0, and output $u$. In $C_1$ the invariant $p = q$ holds, so the output is $p$, and the circuits are equivalent. The mapping $p \mapsto u$, $q \mapsto w$ fails at the output: $p \wedge q \ne p$ at the unreachable state $p = 1, q = 0$. The other mapping fails at $w^+ = u \oplus x$, which becomes $q \oplus x$, against $p^+ = p \oplus x$. Register correspondence by induction proves this pair, because it assumes $p = q$.

**Retiming.** The example on the [sequential equivalence](/sequential-equivalence-checking/) page has 1 latch against 2, so no mapping exists.

## Known algorithms

- **By name.** Match the latch names, with rules for the renaming of the synthesis tool. Fast, but it breaks when names are lost.
- **By structure.** Compare the fanin cones of the latches, as a [graph isomorphism](/graph-isomorphism-problem/) problem on the two netlists. [Gemini](/gemini-netlist-comparison/) does this kind of netlist comparison by iterative labelling of vertices.
- **By function.** Burch and Singhal (1998) map latches by their functions, not their names: a latch and its partner must have equal next-state functions once their fanin latches are mapped. A natural way to find partners is [partition refinement](/partition-refinement/) of the latches of both designs: give the latches of one class the same random value, simulate, and split a class when the next-state values of its members differ, until no class splits. We describe this scheme only in outline; the exact procedure of Burch and Singhal is in their paper.
- **The check after the mapping.** Any combinational method works; see [cutpoint equivalence checking](/cutpoint-equivalence-checking/) and [SAT sweeping](/sat-sweeping/).
- **By induction.** [Signal correspondence](/signal-correspondence/) restricted to latches computes the coarsest register correspondence that is inductive. It also covers the invariant case above.

## Bounds

The problem of deciding whether a valid mapping exists is coNP-hard and in $\Sigma_2^p$.

*Proof.* *coNP-hard.* With no latches, the only mapping is the empty one, and it is valid exactly when the output functions are equal. That is [combinational equivalence](/boolean-equivalence-checking/), which is coNP-complete. *In $\Sigma_2^p$.* Guess $\varphi$ and $\sigma$, then check validity, which is the statement that a combinational miter has no satisfying input, a coNP question. $\square$

We do not know a tighter bound; the search over the $L!$ bijections is the part that heuristics attack. In practice signatures from simulation leave few candidates, and each candidate costs one combinational check.

## Reductions

- **To combinational equivalence.** A fixed mapping turns the check into combinational equivalence of $L + m$ pairs of functions, by the proposition above.
- **From sequential equivalence, as a sound step.** A valid mapping proves sequential equivalence. No mapping proves nothing, as the examples show.
- **To signal correspondence.** Register correspondence by induction is signal correspondence with only latches in the classes.

## Applications

- **Combinational equivalence checking of netlists.** Commercial checkers compare RTL with gates, or gates before and after optimization, by mapping latches first and then running a combinational check on each cone.
- **Engineering change orders.** After a small change to a netlist, most latches keep their partners, and the mapping is quick.
- **Diagnosis.** A latch with no partner, or a mapped pair whose functions differ, points at the location of a bug.

## References
