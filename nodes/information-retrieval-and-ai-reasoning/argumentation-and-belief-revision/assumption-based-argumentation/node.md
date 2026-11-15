---
tag: WC2X2F
kind: model
slug: assumption-based-argumentation
name: Assumption-based argumentation
aliases:
- ABA framework
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Builds arguments as deductions from assumptions in a rule system, with attacks on assumptions through their contraries.
prereqs: [abstract-argumentation-framework, admissible-set]
see_also: [aspic-plus, defeasible-logic-programming, stable-model-semantics, well-founded-semantics, default-logic, negation-as-failure, answer-set-programming, nonmonotonic-reasoning]
sources:
  - paper: doi:10.1016/S0004-3702(97)00015-5
    title: Andrei Bondarenko, Phan Minh Dung, Robert A. Kowalski and Francesca Toni, An abstract, argumentation-theoretic approach to default reasoning, Artificial Intelligence 93(1-2), 63 to 101 (1997)
    locator: the whole paper (the abstract framework, attacks on sets of assumptions, stable, admissible and preferred semantics, and the instances for logic programming, default logic, autoepistemic logic, circumscription and Theorist)
  - paper: doi:10.1080/19462166.2013.869878
    title: Francesca Toni, A tutorial on assumption-based argumentation, Argument and Computation 5(1), 89 to 117 (2014)
    locator: the whole tutorial (ABA frameworks, arguments as trees, attacks, the semantics for flat frameworks, the link with abstract argumentation, and dispute derivations)
  - paper: doi:10.1016/j.artint.2005.07.002
    title: Phan Minh Dung, Robert A. Kowalski and Francesca Toni, Dialectic proof procedures for assumption-based, admissible argumentation, Artificial Intelligence 170(2), 114 to 159 (2006)
    locator: the whole paper (dispute derivations for the admissible semantics)
  - paper: doi:10.1016/j.artint.2007.05.003
    title: Phan Minh Dung, Paolo Mancarella and Francesca Toni, Computing ideal sceptical argumentation, Artificial Intelligence 171(10-15), 642 to 674 (2007)
    locator: the whole paper (the ideal semantics, and dispute derivations for grounded and ideal sets)
  - paper: doi:10.1016/S0004-3702(02)00245-X
    title: Yannis Dimopoulos, Bernhard Nebel and Francesca Toni, On the computational complexity of assumption-based argumentation for default reasoning, Artificial Intelligence 141(1-2), 57 to 78 (2002)
    locator: the whole paper (credulous and sceptical reasoning under the admissible and preferred semantics for each instance)
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: the abstract semantics, and the link between stable extensions and stable models of logic programs
---

Assumption-based argumentation (ABA) is a model of argumentation in which an argument is a deduction from assumptions, and the only way to attack an argument is to deduce the contrary of one of its assumptions. Andrei Bondarenko, Phan Minh Dung, Robert Kowalski and Francesca Toni defined it in 1997 as a common frame for default reasoning. With suitable choices of rules, assumptions and contraries, ABA gives the stable models of [logic programs](/logic-programming/), the extensions of [default logic](/default-logic/), and the expansions of [autoepistemic logic](/autoepistemic-logic/). Its semantics are the semantics of [abstract argumentation](/abstract-argumentation-framework/), lifted to sets of assumptions.

## The machine

**Framework.** An ABA framework is a tuple $(\mathcal{L}, \mathcal{R}, \mathcal{A}, \overline{\phantom{x}})$, where:

- $(\mathcal{L}, \mathcal{R})$ is a deductive system: a language $\mathcal{L}$ and a set $\mathcal{R}$ of rules $\sigma_0 \leftarrow \sigma_1, \dots, \sigma_m$ with $m \ge 0$ and all $\sigma_i \in \mathcal{L}$;
- $\mathcal{A} \subseteq \mathcal{L}$ is a nonempty set of assumptions;
- $\overline{\phantom{x}}$ maps each assumption $\alpha$ to its contrary $\overline{\alpha} \in \mathcal{L}$.

The framework is flat if no assumption is the head of a rule. Most work, and this page from here on, uses flat frameworks.

**Arguments.** An argument for the claim $\sigma$ supported by $A \subseteq \mathcal{A}$, written $A \vdash \sigma$, is a finite tree:

- the root is labelled $\sigma$;
- each inner node is labelled by the head of a rule, and its children are labelled by the body of the rule, or by a special symbol $\tau$ if the body is empty;
- the leaves are assumptions or $\tau$;
- $A$ is the set of the assumptions at the leaves.

Each assumption $\alpha$ gives the argument $\{\alpha\} \vdash \alpha$.

**Attacks.** The argument $A \vdash \sigma$ attacks the argument $B \vdash \pi$ if $\sigma = \overline{\beta}$ for some $\beta \in B$. A set of assumptions $A$ attacks a set $B$ if some argument supported by a subset of $A$ attacks some argument supported by a subset of $B$. In other words, $A$ deduces the contrary of an assumption in $B$.

**Semantics.** A set $A \subseteq \mathcal{A}$ is:

| name | condition |
|---|---|
| conflict-free | $A$ does not attack itself |
| admissible | conflict-free, and $A$ attacks every set of assumptions that attacks $A$ |
| preferred | a maximal admissible set |
| complete | admissible, and contains every assumption it defends |
| grounded | the least complete set |
| stable | conflict-free, and attacks $\{\beta\}$ for every assumption $\beta \notin A$ |
| ideal | the largest admissible set contained in every preferred set |

Here $A$ defends $\alpha$ if $A$ attacks every set that attacks $\{\alpha\}$. A claim $\sigma$ is credulously accepted if some extension supports an argument for $\sigma$, and sceptically accepted if every extension does.

**Arguments and assumptions agree.** For flat frameworks, build the abstract framework whose arguments are all $A \vdash \sigma$ and whose attacks are as above. Then the extensions on assumptions and the extensions on arguments correspond under each semantics: a set of assumptions is an extension if and only if the set of all arguments it supports is an extension of the abstract framework (Toni 2014). So ABA is an instance of Dung's model with a compact syntax.

## What it counts

ABA works on sets of assumptions, not on arguments. This matters for the cost: the number of arguments can be exponential in the number of rules, but the number of assumptions is fixed and attacks are tested by deduction.

- **Attack test.** $A$ attacks $B$ if the contrary of some $\beta \in B$ is in the closure of $A$ under the rules. For a finite propositional framework, this is the forward chaining of Horn clauses, linear in the size of the rules.
- **Defence test.** $A$ defends $\alpha$ if and only if $\overline{\alpha}$ cannot be deduced from the assumptions that $A$ does not attack. If $\overline{\alpha}$ can be deduced from such a set $T$, then $T$ attacks $\{\alpha\}$ and $A$ does not attack $T$. If it cannot, then every set that deduces $\overline{\alpha}$ contains an assumption that $A$ attacks. So the defence test also takes one closure.
- **Grounded set.** Start from the empty set and add the defended assumptions until nothing changes. This takes at most $|\mathcal{A}|$ rounds of the defence test, so the grounded set takes polynomial time.

**A worked example.** Take the normal logic program $p \leftarrow \mathit{not}\ q$, $q \leftarrow \mathit{not}\ p$, $r \leftarrow p$. As an ABA framework, the assumptions are $\mathit{np}$, $\mathit{nq}$ and $\mathit{nr}$ (read as "not $p$" and so on), the rules are $p \leftarrow \mathit{nq}$, $q \leftarrow \mathit{np}$ and $r \leftarrow p$, and the contraries are $\overline{\mathit{np}} = p$, $\overline{\mathit{nq}} = q$ and $\overline{\mathit{nr}} = r$. The arguments besides the assumptions are $\{\mathit{nq}\} \vdash p$, $\{\mathit{nq}\} \vdash r$ and $\{\mathit{np}\} \vdash q$. So $\{\mathit{nq}\}$ attacks every set that contains $\mathit{np}$ or $\mathit{nr}$, and $\{\mathit{np}\}$ attacks every set that contains $\mathit{nq}$.

| semantics | sets of assumptions |
|---|---|
| admissible | $\emptyset$, $\{\mathit{np}\}$, $\{\mathit{nq}\}$, $\{\mathit{np}, \mathit{nr}\}$ |
| complete | $\emptyset$, $\{\mathit{nq}\}$, $\{\mathit{np}, \mathit{nr}\}$ |
| grounded, ideal | $\emptyset$ |
| preferred, stable | $\{\mathit{nq}\}$, $\{\mathit{np}, \mathit{nr}\}$ |

$\{\mathit{np}\}$ is admissible but not complete. The only sets that attack $\{\mathit{nr}\}$ deduce $r$, so they contain $\mathit{nq}$, and $\{\mathit{np}\}$ attacks all of them. So $\{\mathit{np}\}$ defends $\mathit{nr}$ and must contain it to be complete. The stable set $\{\mathit{nq}\}$ deduces $p$ and $r$, and $\{\mathit{np}, \mathit{nr}\}$ deduces $q$. These are the two stable models $\{p, r\}$ and $\{q\}$ of the program. The grounded set is empty, and in the well-founded model of the program $p$, $q$ and $r$ are all undefined. A scratch script enumerated all 8 sets of assumptions and confirmed the table.

## Relation to other models

- **Abstract argumentation.** Every flat ABA framework gives a Dung framework with the same extensions, as above. In the other direction, an abstract framework $(Ar, att)$ is the ABA framework with one assumption per argument, the contrary of $a$ written $\overline{a}$, and a rule $\overline{b} \leftarrow a$ for each attack $(a, b)$.
- **Logic programming.** With the negation-as-failure literals $\mathit{not}\ p$ as assumptions and $\overline{\mathit{not}\ p} = p$, the stable sets are the [stable models](/stable-model-semantics/) (Bondarenko et al. 1997), the grounded set gives the [well-founded model](/well-founded-semantics/), and the preferred sets give the regular models, the maximal partial stable models of the program. This is how [negation as failure](/negation-as-failure/) becomes an argument.
- **Default logic.** With assumptions $M\beta$ for the justifications of defaults, rules for the defaults and classical inference, and $\overline{M\beta} = \neg\beta$, the stable sets give the extensions of Reiter's default logic. Autoepistemic logic, [circumscription](/circumscription/) and Theorist are instances in the same way.
- **ASPIC+.** A flat ABA framework is a special case of [ASPIC+](/aspic-plus/) with only strict rules, where the assumptions are the attackable premises. ASPIC+ adds defeasible rules, undercuts and preferences. ABA+ (Čyras and Toni) adds preferences to ABA directly.
- **Defeasible logic programming.** [DeLP](/defeasible-logic-programming/) also starts from a logic program, but its arguments are sets of defeasible rules, and it decides queries with dialectical trees.

## Known results in the model

- **Instances (Bondarenko et al. 1997).** Stable sets of the logic programming, default logic and autoepistemic logic instances are exactly the stable models, the extensions and the stable expansions of the original formalisms.
- **Correspondence with Dung frameworks (Toni 2014).** For flat frameworks, the assumption-level and argument-level semantics agree for the admissible, preferred, complete, grounded, stable and ideal semantics.
- **Properties of flat frameworks (Bondarenko et al. 1997).** Every flat framework has at least one preferred set, every admissible set is contained in a preferred set, and every stable set is preferred. A stable set need not exist.
- **Dispute derivations.** Dung, Kowalski and Toni (2006) give dispute derivations that decide whether a claim is supported by an admissible set, as a game between a proponent and an opponent that builds arguments top down, in the style of [SLD resolution](/sld-resolution/). Dung, Mancarella and Toni (2007) extend them to the grounded and ideal semantics.
- **Complexity (Dimopoulos, Nebel and Toni 2002).** The complexity depends on the instance. For logic programs, credulous reasoning under the admissible and preferred semantics is NP-complete, the same as under the stable semantics, and sceptical reasoning under the preferred semantics is $\Pi_2^p$-complete. For the richer instances it is often higher than under the stable semantics: for autoepistemic logic, sceptical reasoning under the preferred semantics is at the fourth level of the [polynomial hierarchy](/polynomial-hierarchy/), while under the stable semantics it is at the second level.
- **Non-flat frameworks.** If assumptions can be heads of rules, admissibility must be defined on closed sets of assumptions, which contain every assumption they deduce. Toni (2014) notes that reasoning with non-flat frameworks is computationally demanding.

## References
