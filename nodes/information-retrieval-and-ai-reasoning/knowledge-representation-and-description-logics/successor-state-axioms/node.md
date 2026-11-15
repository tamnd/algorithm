---
tag: FWNBAC
kind: definition
slug: successor-state-axioms
name: Successor state axioms
aliases:
- Reiter's solution to the frame problem
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: One axiom per fluent saying that it holds after an action exactly when the action made it true, or it held before and the action did not make it false.
prereqs: [situation-calculus, frame-problem]
see_also: [situation-calculus-regression, conditional-effects, strips, ramification-problem, qualification-problem, event-calculus, goal-regression, circumscription]
sources:
  - paper: doi:10.1016/B978-0-12-450010-5.50026-8
    title: Raymond Reiter, The frame problem in the situation calculus, a simple solution (sometimes) and a completeness result for goal regression, in Vladimir Lifschitz (ed.), Artificial Intelligence and Mathematical Theory of Computation, Academic Press, 1991, pages 359 to 380
    locator: effect axioms in normal form, the causal completeness assumption, explanation closure axioms, and the successor state axioms that combine them; the earlier proposals of Pednault, Haas and Schubert that the solution combines (general locator)
  - book: isbn:9780262182188
    title: Raymond Reiter, Knowledge in Action, Logical Foundations for Specifying and Implementing Dynamical Systems, MIT Press, 2001
    locator: Chapter 3 from page 17 (the derivation of successor state axioms for relational and functional fluents, with the consistency condition), Chapter 4 from page 45 (successor state axioms as part of a basic action theory)
  - paper: doi:10.1145/316542.316545
    title: Fiora Pirri and Raymond Reiter, Some contributions to the metatheory of the situation calculus, Journal of the ACM 46(3), 1999, pages 325 to 361
    locator: the form of successor state axioms in a basic action theory and their role in the regression theorem (general locator)
---

A successor state axiom is the axiom of the [situation calculus](/situation-calculus/) that defines the value of one fluent after any action in terms of the situation before it. A basic action theory has exactly one such axiom for each fluent. Reiter (1991) obtained the axioms from effect axioms by assuming that the effect axioms list every way a fluent can change, and so gave a solution to the [frame problem](/frame-problem/) in classical logic, without frame axioms for each pair of an action and a fluent. The frame problem page explains the problem and compares this solution with the others; this page states the exact definition, the conditions it needs, and how the axioms are derived.

## Definition

Fix a situation calculus language with a set of action functions. A formula is **uniform in $s$** if the only situation term in it is the variable $s$, and it does not mention $Poss$ or $\sqsubset$.

**Relational fluents.** A successor state axiom for a relational fluent $F$ is a sentence of the form

$$F(\vec{x}, do(a, s)) \leftrightarrow \gamma^+_F(\vec{x}, a, s) \vee \big(F(\vec{x}, s) \wedge \neg \gamma^-_F(\vec{x}, a, s)\big),$$

with all free variables universally quantified, where $\gamma^+_F$ and $\gamma^-_F$ are uniform in $s$. The formula $\gamma^+_F$ describes the actions and conditions that make $F$ true, and $\gamma^-_F$ those that make it false. The axiom is used together with the unique names axioms for actions $\mathcal{D}_{una}$ and must satisfy the **consistency condition**

$$\mathcal{D}_{una} \models \neg \exists \vec{x}\, \exists a\, \exists s\, \big(\gamma^+_F(\vec{x}, a, s) \wedge \gamma^-_F(\vec{x}, a, s)\big),$$

which says that no action both makes $F$ true and makes it false.

**Functional fluents.** For a functional fluent $f$, whose value is an object, the axiom has the form

$$f(\vec{x}, do(a, s)) = y \leftrightarrow \gamma_f(\vec{x}, y, a, s) \vee \big(f(\vec{x}, s) = y \wedge \neg \exists y'\, \gamma_f(\vec{x}, y', a, s)\big),$$

with $\gamma_f$ uniform in $s$, and the consistency condition says that $\gamma_f$ gives at most one value $y$ for each $\vec{x}$, $a$ and $s$ (Reiter 2001, Chapter 3).

**Derivation (Reiter 1991).** Write the effects of the actions on $F$ in normal form, as two axioms

$$\gamma^+_F(\vec{x}, a, s) \rightarrow F(\vec{x}, do(a, s)), \qquad \gamma^-_F(\vec{x}, a, s) \rightarrow \neg F(\vec{x}, do(a, s)).$$

The **causal completeness assumption** says that these are the only ways $F$ changes, which is written as two explanation closure axioms:

$$\neg F(\vec{x}, s) \wedge F(\vec{x}, do(a, s)) \rightarrow \gamma^+_F(\vec{x}, a, s), \qquad F(\vec{x}, s) \wedge \neg F(\vec{x}, do(a, s)) \rightarrow \gamma^-_F(\vec{x}, a, s).$$

Under the consistency condition, the four axioms together are equivalent to the successor state axiom. Reiter (1991) combined the normal form of Pednault with the explanation closure axioms of Haas and of Schubert to get this result.

## Examples and non-examples

**Example: unconditional effects.** For a robot that opens and closes a door and picks up and drops objects,

$$Open(do(a, s)) \leftrightarrow a = open \vee (Open(s) \wedge a \ne close),$$
$$Holding(x, do(a, s)) \leftrightarrow a = pickup(x) \vee (Holding(x, s) \wedge a \ne drop(x)).$$

Here $\gamma^+_{Holding}(x, a, s)$ is $a = pickup(x)$ and $\gamma^-_{Holding}(x, a, s)$ is $a = drop(x)$. The consistency condition holds because $pickup(x) \ne drop(x)$ follows from $\mathcal{D}_{una}$.

**Example: conditional and quantified effects.** A simplified version of an example in Reiter (2001, Chapter 3) has an object that breaks when it is dropped while fragile, or when a bomb next to it explodes, and is fixed by a repair:

$$Broken(x, do(a, s)) \leftrightarrow \big(a = drop(x) \wedge Fragile(x, s)\big) \vee \exists b\, \big(a = explode(b) \wedge NextTo(b, x, s)\big) \vee \big(Broken(x, s) \wedge a \ne repair(x)\big).$$

The condition $Fragile(x, s)$ and the existential over bombs are allowed, since $\gamma^+$ is uniform in $s$. Dropping a fragile object $A$ breaks it, and $\mathcal{D}_{una}$ gives $drop(A) \ne repair(A)$, so a broken object stays broken under every action except $repair$.

**Example: a functional fluent.** A robot at one location at a time:

$$loc(do(a, s)) = y \leftrightarrow a = go(y) \vee \big(loc(s) = y \wedge \neg \exists y'\, a = go(y')\big).$$

The consistency condition holds because $go(y) = go(y')$ implies $y = y'$ by $\mathcal{D}_{una}$.

**Non-example: an effect axiom alone.** $Holding(x, do(pickup(x), s))$ says what $pickup$ does, but not what happens to $Holding$ under the other actions. It is one half of a successor state axiom, and the explanation closure axioms are missing.

**Non-example: a state constraint.** $Wet(do(a, s)) \leftrightarrow InWater(do(a, s))$ relates two fluents in the same situation. Its right side mentions $do(a, s)$, so it is not uniform in $s$. Such indirect effects are the [ramification problem](/ramification-problem/); one approach compiles them into the $\gamma$ formulas, after which the axioms are successor state axioms again.

**Non-example: an inconsistent pair.** A toggle action written as the two effect axioms $\neg Light(s) \rightarrow Light(do(flip, s))$ and $\top \rightarrow \neg Light(do(flip, s))$ violates the consistency condition, since in a situation where the light is off, $flip$ satisfies both $\gamma^+$ and $\gamma^-$. The effect axioms are then contradictory, while the formula of the successor state axiom gives $Light$, so the two are not equivalent. The correct effects are $\gamma^+ = (a = flip \wedge \neg Light(s))$ and $\gamma^- = (a = flip \wedge Light(s))$.

**Non-example: without unique names.** Without $\mathcal{D}_{una}$, the theory cannot prove $drop(A) \ne pickup(A)$, so the axiom for $Holding$ does not entail that $pickup(A)$ leaves $Holding(A, s)$ true. The successor state axioms solve the frame problem only together with the unique names axioms.

## Related definitions

- **Frame axiom.** An axiom that says one action leaves one fluent unchanged. A successor state axiom replaces all frame axioms of one fluent.
- **Precondition axiom.** $Poss(A(\vec{x}), s) \leftrightarrow \Pi_A(\vec{x}, s)$, one for each action function, the other uniform part of a basic action theory; the [qualification problem](/qualification-problem/) concerns it.
- **Basic action theory.** The foundational axioms, the successor state axioms, the precondition axioms, the unique names axioms and the initial database, defined on the [situation calculus](/situation-calculus/) page.
- **Regression.** Because each right side is uniform in $s$, a fluent at $do(a, s)$ can be replaced by a formula at $s$. The [regression](/situation-calculus-regression/) operator does this repeatedly.
- **STRIPS add and delete lists.** A [STRIPS](/strips/) action $A$ gives $\gamma^+_F$ as the disjunction of $a = A$ over the actions with $F$ in the add list, and $\gamma^-_F$ in the same way for the delete list. STRIPS allows an atom in both lists and then lets the add list win, which is what the axiom gives when the consistency condition fails.
- **[Conditional effects](/conditional-effects/)** in planning languages are the propositional case of conditions such as $Fragile(x, s)$ in $\gamma^+$.
- **Event calculus axioms.** The [event calculus](/event-calculus/) states persistence once, for all fluents, with *Initiates* and *Terminates* in the roles of $\gamma^+$ and $\gamma^-$, and uses [circumscription](/circumscription/) to make the lists of effects complete.

## References
