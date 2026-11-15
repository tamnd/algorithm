---
tag: FYKMXS
kind: model
slug: value-based-argumentation
name: Value-based argumentation framework
aliases:
- VAF
- Bench-Capon framework
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Assigns each argument a value promoted, so an attack succeeds for an audience only if it does not prefer the attacked value.
prereqs: [abstract-argumentation-framework, preferred-extension]
see_also: [aspic-plus, defeasible-logic-programming, assumption-based-argumentation, argument-acceptance-problem, preferred-semantics-complexity, grounded-extension, directed-acyclic-graph, nonmonotonic-reasoning]
sources:
  - paper: doi:10.1093/logcom/13.3.429
    title: Trevor J. M. Bench-Capon, Persuasion in practical argument using value-based argumentation frameworks, Journal of Logic and Computation 13(3), 429 to 448 (2003)
    locator: "Sections 5 and 6 (VAFs, audience-specific VAFs, defeat for an audience, conflict-free, admissible and preferred sets for an audience, objective and subjective acceptance, the unique preferred extension when there is no single-valued cycle) and Figure 2"
  - paper: "Value based argumentation frameworks"
    title: Trevor Bench-Capon and Paul Dunne, Technical Report ULCS-02-001, Department of Computer Science, University of Liverpool (2002)
    locator: Definitions 7 to 12 (VAF, defeat, V-acceptable, V-conflict-free, V-admissible, V-preferred), Section 4 (monochromatic and polychromatic cycles) and the procedure EXTEND
  - paper: doi:10.1007/978-3-540-30227-8_31
    title: Paul E. Dunne and Trevor Bench-Capon, Complexity in value-based argument systems, in Logics in Artificial Intelligence (JELIA 2004), LNCS 3229, Springer, 360 to 371 (2004)
    locator: the main results (subjective acceptance is NP-complete and objective acceptance is coNP-complete)
  - paper: doi:10.1016/j.artint.2011.03.001
    title: Eun Jung Kim, Sebastian Ordyniak and Stefan Szeider, Algorithms and complexity results for persuasive argumentation, Artificial Intelligence 175(9-10), 1722 to 1736 (2011)
    locator: the abstract and main results (hardness under structural restrictions, and tractable classes defined by the graph structure)
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: the abstract frameworks, preferred extensions, and the unique extension of a well-founded framework
---

A value-based argumentation framework (VAF) extends an [abstract argumentation framework](/abstract-argumentation-framework/) with values. Each argument promotes a value, such as safety, liberty or economy, and each audience ranks the values. An attack succeeds as a defeat for an audience unless that audience prefers the value of the attacked argument to the value of the attacker. Trevor Bench-Capon introduced VAFs in 2003 to model practical and legal argument, where rational people can accept the same arguments and still disagree, because they rank values in different ways. The model explains how a dispute can be resolved for each audience, and which arguments every audience must accept.

## The machine

The definitions follow Bench-Capon (2003) and the report of Bench-Capon and Dunne (2002).

**VAF.** A value-based argumentation framework is a tuple $\langle AR, \mathit{attacks}, V, \mathit{val}, P \rangle$, where:

- $\langle AR, \mathit{attacks} \rangle$ is a Dung framework;
- $V$ is a nonempty set of values;
- $\mathit{val} : AR \to V$ gives the value that each argument promotes;
- $P$ is a set of possible audiences.

**Audience.** An audience $a$ has a preference $\succ_a$ on $V$ that is transitive, irreflexive and asymmetric. An audience-specific VAF (AVAF) is the tuple with $P$ replaced by one $\succ_a$. A specific audience is one whose preference is a total order on $V$.

**Defeat for an audience.** $A$ defeats $B$ for $a$ if $A$ attacks $B$ and not $\mathit{val}(B) \succ_a \mathit{val}(A)$. So an attack between two arguments with the same value always succeeds, and so does an attack between values that the audience does not compare.

**Semantics for an audience.** For an audience $a$, an argument $A$ and a set $S \subseteq AR$:

| notion | condition |
|---|---|
| $S$ is conflict-free | for all $A, B \in S$: $A$ does not attack $B$, or $\mathit{val}(B) \succ_a \mathit{val}(A)$ |
| $A$ is acceptable with respect to $S$ | every $B$ that defeats $A$ for $a$ is defeated for $a$ by some member of $S$ |
| $S$ is admissible | $S$ is conflict-free, and every member of $S$ is acceptable with respect to $S$ |
| $S$ is a preferred extension | $S$ is a maximal admissible set |

A conflict-free set may contain an attack, as long as the attack fails for the audience. These definitions are exactly Dung's semantics on the defeat graph of the audience.

**Acceptance over audiences.** An argument is objectively acceptable if it is in every preferred extension for every audience in $P$, subjectively acceptable if it is in some preferred extension for some audience, and indefensible if it is in none.

## What it counts

A VAF counts audiences as well as arguments. With $k$ values there are $k!$ specific audiences, and a naive test of objective or subjective acceptance computes the extension for each. For one specific audience, the work is small:

- **Unique extension.** A cycle is single-valued if all its arguments have the same value. If the attack graph has no single-valued cycle, the defeat graph of a specific audience has no cycle at all. Take a cycle $x_1 \to x_2 \to \dots \to x_m \to x_1$ of defeats. Each defeat $x_i \to x_{i+1}$ means $\mathit{val}(x_i) \succeq_a \mathit{val}(x_{i+1})$, because the order is total. Around the cycle this gives $\mathit{val}(x_1) \succeq_a \dots \succeq_a \mathit{val}(x_1)$, so all the values are equal and the cycle was single-valued.
- **Computing it.** A finite framework without cycles is well founded, so by Dung (1995) its grounded, preferred and stable extensions are the same set, and the set is nonempty when $AR$ is nonempty. Process the arguments in a [topological order](/topological-sort/) of the [acyclic](/directed-acyclic-graph/) defeat graph: an argument is in if no argument already in defeats it. This takes $O(|AR| + |\mathit{attacks}|)$ time. The procedure EXTEND of Bench-Capon and Dunne computes the same set in rounds: take the undefeated arguments, remove what they defeat, and repeat.

**A worked example.** This is Figure 2 of Bench-Capon (2003). $A$ attacks $B$ and $B$ attacks $C$. $A$ promotes red and $B$ and $C$ promote blue.

| audience | defeats | preferred extension |
|---|---|---|
| red $\succ$ blue | $A \to B$, $B \to C$ | $\{A, C\}$ |
| blue $\succ$ red | $B \to C$ | $\{A, B\}$ |

For the red audience, $A$ defeats $B$, and $C$ is reinstated. For the blue audience, the attack of $A$ on $B$ fails, so $B$ stands and defeats $C$. So $A$ is objectively acceptable, and $B$ and $C$ are only subjectively acceptable. Now add an attack from $C$ to $A$. As a plain Dung framework this is an odd cycle, and its only preferred extension is empty. With the values, the red audience drops $C \to A$ and the blue audience drops $A \to B$, so each audience again gets one nonempty extension, $\{A, C\}$ and $\{A, B\}$. A scratch script computed all four results with a brute-force preferred-extension routine.

## Relation to other models

- **Abstract frameworks.** For each audience, a VAF is a Dung framework on the defeat relation. With one value, every attack succeeds and the VAF is the plain framework. With no single-valued cycle and a specific audience, the framework has a unique [preferred extension](/preferred-extension/), which is also the [grounded extension](/grounded-extension/).
- **Preference-based frameworks.** The preference-based frameworks of Amgoud and Cayrol compare arguments directly. A VAF with a specific audience is the case where the order on arguments comes from the order on their values. Later work, for example by Kaci and van der Torre, lets an argument promote several values.
- **Structured argumentation.** [ASPIC+](/aspic-plus/) and [DeLP](/defeasible-logic-programming/) take preferences from the rules and premises inside the arguments. A VAF takes them from outside, from the audience, and keeps the arguments abstract.
- **Practical reasoning.** Atkinson and Bench-Capon use VAFs with an argument scheme for action: in the current state, do an action to reach a new state that promotes a value. Critical questions to the scheme give the attacks.

## Known results in the model

- **Unique extension (Bench-Capon 2003).** Every AVAF for a specific audience whose attack graph has no single-valued cycle has a unique, nonempty preferred extension. The argument above gives a short proof.
- **Cycles (Bench-Capon and Dunne 2002).** In a single-valued cycle the VAF behaves like a Dung framework: an odd cycle gives an empty extension and an even cycle gives two. A cycle with two or more values is broken for each specific audience at an attack from a less preferred value. Whether a VAF has a single-valued cycle can be tested in polynomial time, one value at a time.
- **Complexity of acceptance (Dunne and Bench-Capon 2004).** For VAFs without single-valued cycles, deciding whether an argument is subjectively acceptable is [NP-complete](/np-complete/), and deciding whether it is objectively acceptable is [coNP-complete](/co-np/). The hardness comes from the choice of audience, since for each fixed audience the test takes linear time. Compare the plain case in [argument acceptance](/argument-acceptance-problem/) and [preferred semantics complexity](/preferred-semantics-complexity/).
- **Restricted structure (Kim, Ordyniak and Szeider 2011).** Both acceptance problems stay intractable under several structural restrictions that make the plain problems tractable. The authors also find nontrivial classes, defined by the graph structure, where both problems take polynomial time, and they show that two classes conjectured by Dunne (2007) to be tractable are in fact intractable.
- **Few values.** With $k$ values, testing all $k!$ specific audiences takes $O(k! \cdot (|AR| + |\mathit{attacks}|))$ time, which is polynomial when $k$ is a constant.

## References
