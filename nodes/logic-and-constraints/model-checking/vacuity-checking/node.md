---
tag: FJVT93
kind: concept
slug: vacuity-checking
name: Vacuity checking
area: logic-and-constraints/model-checking
level: research
summary: Detect properties that pass for a trivial reason, such as an implication whose condition never holds, by testing whether some subformula can be replaced without changing the result.
prereqs: [linear-temporal-logic, computation-tree-logic, ltl-model-checking]
see_also: [ltl-satisfiability, predicate-specification-patterns, counterexample-generation, ctl-model-checking, ltl-model-checking, temporal-logic]
sources:
  - paper: "Ilan Beer, Shoham Ben-David, Cindy Eisner and Yoav Rodeh, Efficient detection of vacuity in ACTL formulas, Computer Aided Verification (CAV 1997), Lecture Notes in Computer Science 1254, Springer, 1997"
    locator: the definition of vacuous passes, their frequency in industrial use, and witness formulas for a subset of ACTL
  - paper: "Ilan Beer, Shoham Ben-David, Cindy Eisner and Yoav Rodeh, Efficient detection of vacuity in temporal model checking, Formal Methods in System Design 18(2), 2001"
    locator: the journal version, with the treatment of vacuity in the RuleBase model checker
  - paper: "Orna Kupferman and Moshe Y. Vardi, Vacuity detection in temporal model checking, Correct Hardware Design and Verification Methods (CHARME 1999), Lecture Notes in Computer Science 1703, Springer, 1999"
    locator: vacuity for CTL* by replacing a subformula of pure polarity with true or false, interesting witnesses, and the cost of the check
  - paper: "Roy Armoni, Limor Fix, Alon Flaisher, Orna Grumberg, Nir Piterman, Andreas Tiemeyer and Moshe Y. Vardi, Enhanced vacuity detection in linear temporal logic, Computer Aided Verification (CAV 2003), Lecture Notes in Computer Science 2725, Springer, 2003"
    locator: trace vacuity, which also covers subformulas of mixed polarity
---

A property passes *vacuously* in a model when it holds for a trivial reason: some part of the formula has no influence on the result. The standard case is an implication whose condition never holds, such as "every request is eventually granted" in a model that never makes a request. Beer, Ben-David, Eisner and Rodeh (1997) found that such passes are common in industrial model checking and often hide errors in the model or in the formula. Kupferman and Vardi (1999) gave a general definition and showed that, for a subformula that occurs with one polarity, vacuity is decided by one extra run of the model checker on the formula with that subformula replaced by $\mathsf{false}$ or $\mathsf{true}$.

## In plain words

A model checker answers yes or no. A yes looks like good news, but it can be empty. Suppose the rule is "whenever a request arrives, it is eventually answered". If the model contains a mistake so that no request ever arrives, the rule is never tested, and the checker still says yes.

Vacuity checking looks for such empty yeses. For each part of the rule, it asks: would the answer still be yes if this part were replaced by something that is always false, or always true? If so, that part played no role, and the user is warned. The warning often points to a bug in the model, such as a signal that is stuck, or to a rule that does not say what its author meant.

## The idea

**Definition.** Let $\varphi$ be a formula of [LTL](/linear-temporal-logic/), [CTL](/computation-tree-logic/) or CTL*, and let $\psi$ be an occurrence of a subformula of $\varphi$. Write $\varphi[\psi \leftarrow \xi]$ for the result of replacing that occurrence by the formula $\xi$. Following Kupferman and Vardi, $\psi$ *does not affect* $\varphi$ in a model $M$ if $M \models \varphi[\psi \leftarrow \xi]$ holds for every formula $\xi$ or for none. The model $M$ satisfies $\varphi$ *vacuously* if $M \models \varphi$ and some occurrence $\psi$ does not affect $\varphi$ in $M$. A subformula that does affect $\varphi$ in this sense is relevant to the pass.

**Polarity.** An occurrence of $\psi$ in $\varphi$ is *positive* if it is under an even number of negations, and *negative* if under an odd number. Here $\to$ counts as a negation on its left side, and an occurrence under $\leftrightarrow$ or exclusive or has both polarities, or *mixed* polarity.

**Theorem** (Kupferman and Vardi 1999). Let $M \models \varphi$, and let $\psi$ be an occurrence of pure polarity. If it is positive, $\psi$ does not affect $\varphi$ in $M$ iff $M \models \varphi[\psi \leftarrow \mathsf{false}]$. If it is negative, iff $M \models \varphi[\psi \leftarrow \mathsf{true}]$.

*Proof.* Write $\varphi$ in negation normal form, with negations only on atomic propositions and with the dual operators ($\vee$, $\mathsf{R}$, $\mathsf{A}$, $\mathsf{E}$), keeping the occurrence $\psi$ in place; a positive occurrence is then not under any negation. *Monotonicity:* if $\xi_1 \to \xi_2$ holds at every state (or path) of $M$, then so does $\varphi[\psi \leftarrow \xi_1] \to \varphi[\psi \leftarrow \xi_2]$. This holds by induction on the structure of $\varphi$, because each operator of negation normal form, namely $\wedge$, $\vee$, $\mathsf{X}$, $\mathsf{U}$, $\mathsf{R}$, $\mathsf{E}$ and $\mathsf{A}$, is monotone in each argument: making an argument true in more places can only make the result true in more places. Now let $\psi$ be positive. Since $\mathsf{false} \to \xi$ holds everywhere for every $\xi$, $M \models \varphi[\psi \leftarrow \mathsf{false}]$ gives $M \models \varphi[\psi \leftarrow \xi]$ for every $\xi$, so $\psi$ does not affect $\varphi$. Conversely, if $\psi$ does not affect $\varphi$, then, as $M \models \varphi = \varphi[\psi \leftarrow \psi]$, the replacement holds for every $\xi$, in particular for $\mathsf{false}$. A negative occurrence is the same with $\mathsf{true}$ and the order reversed. $\square$

**The check.** For each occurrence of pure polarity, run the model checker on $\varphi[\psi \leftarrow \mathsf{false}]$ or $\varphi[\psi \leftarrow \mathsf{true}]$. If it passes, report $\psi$ as irrelevant. If an occurrence does not affect $\varphi$, then neither do the occurrences inside it, because a change inside $\psi$ is a replacement of $\psi$. So $\varphi$ passes vacuously iff some atomic occurrence does not affect it, and it suffices to check the atomic occurrences. The cost is at most one model checking run per occurrence, so $O(|\varphi|)$ runs in all. For LTL each run is PSPACE-complete, like the original; for CTL each run is linear.

**Interesting witnesses.** When $\psi$ does affect $\varphi$, the failed check of $\varphi[\psi \leftarrow \mathsf{false}]$ gives a counterexample, which is a path of $M$ on which $\varphi$ holds and the role of $\psi$ is visible. Kupferman and Vardi call it an *interesting witness*. It shows the user that the property was really exercised, for example a path on which a request occurs and is then granted.

**Mixed polarity.** For an occurrence under $\leftrightarrow$, neither replacement is enough, and the definition with all $\xi$ is harder to check. Armoni et al. (2003) proposed *trace vacuity* for LTL, which quantifies over the values of a new proposition put in place of $\psi$ along a path. It covers mixed polarity, and the check is an LTL model checking run of $\varphi[\psi \leftarrow x]$ on $M$ extended with a new proposition $x$ that may take any value at any step.

**Relation to other checks.** Vacuity is a sanity check of a *pass*. [LTL satisfiability](/ltl-satisfiability/) checks the formula alone: an unsatisfiable formula fails on every model, and a valid one passes on every model. Coverage asks the dual question about the model: which parts of the model could be changed without changing the pass. A [counterexample](/counterexample-generation/) explains a fail; an interesting witness explains a pass.

## Examples

**A request that never comes.** Let $\varphi = \mathsf{G}(\mathit{req} \to \mathsf{F}\, \mathit{grant})$, and let $M$ be a model in which $\mathit{req}$ is stuck at $0$ because of a wiring error. Then $M \models \varphi$. The occurrence of $\mathit{grant}$ is positive, and $\varphi[\mathit{grant} \leftarrow \mathsf{false}] = \mathsf{G}(\mathit{req} \to \mathsf{F}\, \mathsf{false})$ is equivalent to $\mathsf{G} \neg\mathit{req}$, which holds. So the pass is vacuous, and the warning leads to the stuck signal.

**A grant that comes anyway.** Let $M$ cycle through three states labelled $\emptyset$, $\{\mathit{req}\}$ and $\{\mathit{grant}\}$. Again $M \models \varphi$, and now $\varphi[\mathit{grant} \leftarrow \mathsf{false}] \equiv \mathsf{G} \neg\mathit{req}$ fails, so $\mathit{grant}$ is relevant. The occurrence of $\mathit{req}$ is negative, and $\varphi[\mathit{req} \leftarrow \mathsf{true}] = \mathsf{G}\mathsf{F}\, \mathit{grant}$ holds. So the pass is vacuous in $\mathit{req}$: grants come infinitely often whether or not there are requests. This is not always a bug, but it tells the user that the property did not test the link between requests and grants.

**A real pass.** If $M$ may also stay forever in the state $\emptyset$, then $\mathsf{G}\mathsf{F}\, \mathit{grant}$ fails, while $\varphi$ still holds, since no request is made on that path. Both occurrences are now relevant, and the counterexample of $\mathsf{G}\mathsf{F}\, \mathit{grant}$ is an interesting witness for $\mathit{req}$.

**CTL.** For $\mathsf{AG}(\mathit{req} \to \mathsf{AF}\, \mathit{grant})$ the same replacements give $\mathsf{AG} \neg\mathit{req}$ and $\mathsf{AG}\,\mathsf{AF}\, \mathit{grant}$, and each is a linear-time CTL check.

**Mixed polarity.** In $\mathsf{G}(\mathit{ack} \leftrightarrow \mathsf{X}\, \mathit{done})$, each occurrence has mixed polarity, and neither $\mathsf{true}$ nor $\mathsf{false}$ alone decides whether it matters; trace vacuity is needed.

## Where it is used

- **Industrial model checking.** Beer et al. built vacuity detection into IBM's RuleBase model checker, and reported that vacuous passes were frequent and that they often revealed real errors in the design or in the specification. Commercial formal verification tools report vacuous passes in the same way.
- **Assertion-based verification.** The assertion languages PSL and SystemVerilog Assertions define *vacuous success* of an implication whose antecedent does not match, and simulators and formal tools count vacuous and real successes separately.
- **Specification patterns.** Most [specification patterns](/predicate-specification-patterns/) are implications of the form "after Q, if P then R", which can pass vacuously when Q or P never happens. A vacuity check is the natural companion of a pattern library.
- **Debugging a specification.** Together with satisfiability, validity and coverage checks, vacuity checking is part of the routine sanity checks run before trusting a pass.

## References
