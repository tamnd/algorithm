---
tag: 4GWDJ7
kind: definition
slug: redundant-fault
name: Redundant fault
aliases:
- untestable fault
- undetectable fault
area: eda/test-and-diagnosis
level: core
summary: A fault that no input can detect because the faulty and good circuits compute the same function; ATPG that proves this also finds logic that can be removed.
prereqs: [stuck-at-fault-model]
see_also: [fault-coverage, automatic-test-pattern-generation, observability-dont-care, miter-circuit, sat-based-atpg, boolean-network, fault-collapsing, equivalence-checking]
sources:
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapters on fault modeling and test generation (redundant faults, their effect on other tests, and redundancy identification)
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapters Fault Modeling and Combinational Circuit Test Generation (redundant faults and their identification by ATPG)
  - paper: "Oscar H. Ibarra and Sartaj K. Sahni, Polynomially complete fault detection problems, IEEE Transactions on Computers C-24(3), 242 to 249, 1975"
    title: O. H. Ibarra and S. K. Sahni, Polynomially complete fault detection problems, IEEE Transactions on Computers C-24(3), 242 to 249, 1975
    locator: deciding whether a single stuck-at fault is detectable is NP-complete, so proving a fault redundant is coNP-complete
---

A redundant fault is a fault that no input vector can detect: the circuit with the fault computes the same function as the good circuit. For a [single stuck-at fault](/stuck-at-fault-model/) on a line, this means that the line can be tied to the stuck value without any change at the outputs, so the logic that drives it, or that the constant now fixes, can be removed. A test generator that proves a fault redundant has therefore found logic to remove. Of the [fault coverage](/fault-coverage/) ratios, one counts such a fault as covered and one leaves it out of the count.

## Definition

Let $C$ be a combinational circuit with inputs $x \in \{0, 1\}^n$, and let $C(x)$ be its vector of output values. For a fault $f$, let $C_f$ be the circuit with the fault. A vector $x$ **detects** $f$ if $C_f(x) \ne C(x)$. The fault $f$ is **redundant** (or undetectable) if no vector detects it, that is, if $C_f(x) = C(x)$ for all $x$. A fault that some vector detects is detectable, or irredundant.

For the stuck-at fault $\ell/v$, the faulty circuit $C_{\ell/v}$ is the circuit $C$ with line $\ell$ cut from its driver and connected to the constant $v$. So the definition gives at once:

**Proposition.** The fault $\ell/v$ is redundant if and only if tying line $\ell$ to the constant $v$ leaves the function of the circuit unchanged.

*Proof.* Tying $\ell$ to $v$ gives exactly the circuit $C_{\ell/v}$, and $\ell/v$ is redundant exactly when $C_{\ell/v}$ and $C$ compute the same function. $\square$

After the tie, the circuit gets smaller in two ways. The gates whose only path to an output runs through $\ell$ now drive nothing and can be deleted. A gate fed by the constant either becomes constant, as an AND gate with a 0 input, or loses that input, as an AND gate with a 1 input. Each such step keeps the function, so the result is an equivalent and smaller circuit. This is how test generation is used for redundancy removal in logic synthesis of a [Boolean network](/boolean-network/).

The condition can be stated with the [observability don't-cares](/observability-dont-care/) of $\ell$, the vectors under which no output depends on $\ell$. The fault $\ell/v$ is redundant if and only if every vector that gives $\ell$ the value $\lnot v$ in the good circuit is an observability don't-care of $\ell$: either the fault is never activated, or its effect never reaches an output.

Deciding whether a stuck-at fault is detectable is NP-complete (Ibarra and Sahni, 1975), so proving that a fault is redundant is coNP-complete. In practice it is done by [automatic test pattern generation](/automatic-test-pattern-generation/), which must search the whole space before it can answer that no test exists, or by a [SAT solver](/sat-based-atpg/) on a [miter](/miter-circuit/) of $C$ and $C_f$, where an unsatisfiable miter is a proof of redundancy.

## Examples and non-examples

**The consensus term.** The circuit $p = \mathrm{AND}(a, b)$, $q = \mathrm{AND}(\lnot a, c)$, $r = \mathrm{AND}(b, c)$, $z = \mathrm{OR}(p, q, r)$ computes $z = ab + \bar{a}c + bc$. The term $bc$ is the consensus of $ab$ and $\bar{a}c$: if $b = c = 1$, then $ab + \bar{a}c = a + \bar{a} = 1$. So $r$ never decides the output, and $r/0$ is redundant. The faults $b_r/0$ and $c_r/0$ on the branches into $r$ only force $r = 0$, so they are redundant too. Trying all 8 input vectors shows that the other 25 of the 28 single stuck-at faults are detectable, and the tests of the [parallel fault simulation](/parallel-fault-simulation/) page check this. Tying $r$ to 0 removes the AND gate $r$ and one input of the OR gate, and leaves the multiplexer $z = ab + \bar{a}c$.

**The other value is detectable.** In the same circuit, $r/1$ is detectable: the vector $abc = 010$ gives $z = 0$ in the good circuit and $z = 1$ with $r/1$. A redundant line is redundant for one stuck value, not always for both.

**Two redundant faults that are not redundant together.** In $p_1 = \mathrm{AND}(a, b)$, $p_2 = \mathrm{AND}(a, b)$, $z = \mathrm{OR}(p_1, p_2)$, each of $p_1/0$ and $p_2/0$ is redundant, since the other copy still gives $z = ab$. But with both faults, $z = 0$, which the vector 11 detects. So redundant faults cannot all be removed at once. Removal goes one fault at a time, and after each removal the test generator must check the next fault again, since a fault may become detectable.

**A redundant fault can hide another.** In the consensus circuit, the fault $c_r/1$ is detected by 010, which makes $r = 1$ while $z$ should be 0. If $r/0$ is present too, $r$ stays 0, and no vector detects $c_r/1$. A chip with an untested redundant fault can thus pass a test that would catch its second fault on a chip without it.

**Non-example: not detected by a given test set.** A fault that a given test set misses is not redundant unless no vector at all detects it. The fault coverage of a set below 100% does not show redundancy.

**Non-example: hard to detect.** A fault detected by only one of $2^n$ vectors is detectable, and random patterns may never hit it. Such faults are called random-pattern resistant, not redundant.

**Fanout-free circuits.** In a circuit of AND, OR, NAND, NOR and NOT gates with one output, where every line feeds at most one gate, no single stuck-at fault is redundant. The proof is on the [stuck-at fault model](/stuck-at-fault-model/) page. Redundancy needs reconvergent fanout, as in both circuits above.

## Related definitions

- **Equivalent faults.** Two faults are equivalent if their faulty circuits compute the same function. A fault is redundant exactly when it is equivalent to the fault-free circuit. [Fault collapsing](/fault-collapsing/) groups equivalent faults.
- **Untestable fault.** In a sequential circuit, or under the constraints of a test setup, a fault can be untestable without being redundant: it changes the function, but no test that the setup can apply detects it. Tools often class such faults with the redundant ones, which matters for the [fault coverage](/fault-coverage/) ratios.
- **Aborted fault.** A fault for which a test generator stopped before it found a test or a proof of redundancy.
- **Redundancy and equivalence.** Checking that tying a line does not change the function is a case of [equivalence checking](/equivalence-checking/) between $C$ and $C_{\ell/v}$.

## References
