---
tag: EZSSDM
kind: model
slug: aspic-plus
name: ASPIC+
aliases:
- ASPIC+ framework
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: research
summary: Structured argumentation with strict and defeasible rules, attacks by undermining, rebutting and undercutting, and preferences among arguments.
prereqs: [abstract-argumentation-framework, complete-extension]
see_also: [assumption-based-argumentation, defeasible-logic-programming, value-based-argumentation, grounded-extension, preferred-extension, default-logic, nonmonotonic-reasoning, argumentation-sat-encoding]
sources:
  - paper: doi:10.1016/j.artint.2012.10.008
    title: Sanjay Modgil and Henry Prakken, A general account of argumentation with preferences, Artificial Intelligence 195, 361 to 397 (2013)
    locator: "Definitions 2 to 21 (argumentation systems, arguments, attacks, defeats, well defined SAFs, reasonable orderings, last link and weakest link), Theorems 12 to 15 and Proposition 16, numbered as in the corrected version, arXiv:1804.06763"
  - paper: doi:10.1016/j.artint.2018.05.001
    title: Sanjay Modgil and Henry Prakken, Corrigendum to A general account of argumentation with preferences, Artificial Intelligence 263, 107 to 110 (2018)
    locator: the whole note (corrections to the 2013 definitions that the results depend on)
  - paper: doi:10.1016/j.artint.2007.02.003
    title: Martin Caminada and Leila Amgoud, On the evaluation of argumentation formalisms, Artificial Intelligence 171(5-6), 286 to 310 (2007)
    locator: the rationality postulates (closure, direct and indirect consistency), restricted rebut, transposition, and the example of the man who wears a ring and goes out late
  - paper: doi:10.1080/19462160903564592
    title: Henry Prakken, An abstract framework for argumentation with structured arguments, Argument and Computation 1(2), 93 to 124 (2010)
    locator: the whole paper (the first definition of ASPIC+, and ABA as a special case)
  - paper: doi:10.1080/19462166.2013.869766
    title: Sanjay Modgil and Henry Prakken, The ASPIC+ framework for structured argumentation, a tutorial, Argument and Computation 5(1), 31 to 62 (2014)
    locator: the whole tutorial
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: the abstract frameworks and semantics that ASPIC+ instantiates
---

ASPIC+ is a framework for structured argumentation. It does not take arguments and attacks as given, as an [abstract argumentation framework](/abstract-argumentation-framework/) does. It builds arguments from a knowledge base with strict and defeasible rules, it derives three kinds of attack from the inner structure of the arguments, and it uses preferences to decide which attacks succeed as defeats. The result is a Dung framework, so all the usual semantics apply. Henry Prakken defined ASPIC+ in 2010, and Sanjay Modgil and Prakken gave its general form in 2013. Its main use is as a meta-model: if a rule-based formalism fits ASPIC+ and meets some conditions, then its conclusions satisfy the rationality postulates of Caminada and Amgoud (2007).

## The machine

The definitions follow Modgil and Prakken (2013), with the numbering of the corrected version.

**Argumentation system (Definition 2).** A tuple $(\mathcal{L}, \overline{\phantom{x}}, \mathcal{R}, n)$, where:

- $\mathcal{L}$ is a logical language;
- $\overline{\phantom{x}}$ maps each formula $\psi$ to a set $\overline{\psi} \subseteq \mathcal{L}$ of formulas in conflict with it. $\varphi$ is a contrary of $\psi$ if $\varphi \in \overline{\psi}$ and $\psi \notin \overline{\varphi}$, and $\varphi$ and $\psi$ are contradictories, written $\varphi = -\psi$, if each is in the set of the other. Every formula has at least one contradictory;
- $\mathcal{R} = \mathcal{R}_s \cup \mathcal{R}_d$ is a set of strict rules $\varphi_1, \dots, \varphi_n \rightarrow \varphi$ and defeasible rules $\varphi_1, \dots, \varphi_n \Rightarrow \varphi$;
- $n$ gives each defeasible rule a name in $\mathcal{L}$, so that other rules can conclude that a rule does not apply.

**Knowledge base (Definition 4).** $\mathcal{K} = \mathcal{K}_n \cup \mathcal{K}_p$, with axioms $\mathcal{K}_n$, which cannot be attacked, and ordinary premises $\mathcal{K}_p$, which can.

**Arguments (Definition 5).** Each $\varphi \in \mathcal{K}$ is an argument with conclusion $\varphi$. If $A_1, \dots, A_n$ are arguments and $\mathrm{Conc}(A_1), \dots, \mathrm{Conc}(A_n) \rightarrow \psi$ is a strict rule, then $A_1, \dots, A_n \rightarrow \psi$ is an argument, and in the same way with $\Rightarrow$ for a defeasible rule. Each argument has its premises $\mathrm{Prem}$, its sub-arguments $\mathrm{Sub}$, its defeasible rules $\mathrm{DefRules}$ and its top rule. An argument is strict if it has no defeasible rule, and firm if all its premises are axioms.

**Attacks (Definition 8).** $A$ attacks $B$ if one of these holds:

| attack | target in $B$ | condition |
|---|---|---|
| undercut on $B'$ | a sub-argument $B'$ with a defeasible top rule $r$ | $\mathrm{Conc}(A) \in \overline{n(r)}$ |
| rebut on $B'$ | a sub-argument $B' = B''_1, \dots, B''_m \Rightarrow \varphi$ | $\mathrm{Conc}(A) \in \overline{\varphi}$ |
| undermine on $\varphi$ | an ordinary premise $\varphi \in \mathrm{Prem}(B) \cap \mathcal{K}_p$ | $\mathrm{Conc}(A) \in \overline{\varphi}$ |

Rebut is restricted: a conclusion of a strict rule cannot be rebutted. The attack must go to the defeasible step or the ordinary premise below it.

**Defeat (Definition 9).** Let $\preceq$ be an order on arguments, with strict part $\prec$. Undercuts, and rebuts or underminings by a contrary, always succeed. Other attacks succeed only on preferences: $A$ defeats $B$ if $A$ attacks $B$ on $B'$ and the attack is of the first kind, or $A \not\prec B'$. Note that the preference compares $A$ with the attacked sub-argument $B'$, not with $B$.

**Structured framework (Definitions 11 to 15).** The SAF is $(\mathcal{A}, \mathcal{C}, \preceq)$ with all finite arguments $\mathcal{A}$ and the attack relation $\mathcal{C}$. The c-SAF keeps only the arguments whose premises are consistent. The extensions are those of the Dung framework $(\mathcal{A}, \mathcal{D})$ with the defeat relation $\mathcal{D}$. Conflict-freeness can be defined on attacks or on defeats.

**Preferences from rules and premises (Definitions 19 to 21).** Take preorders on $\mathcal{R}_d$ and on $\mathcal{K}_p$. A set comparison $\Gamma \lhd \Gamma'$ is false if $\Gamma = \emptyset$, true if $\Gamma' = \emptyset \ne \Gamma$, and otherwise:

- Elitist: some $X \in \Gamma$ has $X < Y$ for all $Y \in \Gamma'$;
- Democratic: each $X \in \Gamma$ has some $Y \in \Gamma'$ with $X < Y$.

Under the last-link principle, $B \prec A$ if the last defeasible rules of $B$ compare below those of $A$, or both have none and the ordinary premises compare below. Under the weakest-link principle, all defeasible rules and all ordinary premises are compared.

## What it counts

ASPIC+ counts arguments and defeats. A query asks whether a formula is the conclusion of an argument in one extension (credulous) or in every extension (sceptical). The cost has two parts:

- **Argument construction.** The number of arguments can grow exponentially with the knowledge base. Take ordinary premises $a_i$ and $b_i$, rules $a_i \Rightarrow c_i$ and $b_i \Rightarrow c_i$ for $i = 1, \dots, k$, and one strict rule $c_1, \dots, c_k \rightarrow g$. Then there are $2^k$ arguments for $g$.
- **Evaluation.** After construction, the problem is a Dung problem on $(\mathcal{A}, \mathcal{D})$. The [grounded extension](/grounded-extension/) takes polynomial time in the size of the framework, and [preferred](/preferred-extension/) acceptance has the complexity of the abstract case, which [SAT encodings](/argumentation-sat-encoding/) handle.

**A worked example.** This is the example of Caminada and Amgoud (2007). The axioms are $wr$ (John wears a ring) and $go$ (John often goes out late). The defeasible rules are $d_1: wr \Rightarrow m$ (he is married) and $d_2: go \Rightarrow b$ (he is a bachelor). The strict rules are $m \rightarrow hw$ (he has a wife) and $b \rightarrow \neg hw$. The arguments are:

| name | argument | conclusion |
|---|---|---|
| $A_1$, $A_2$ | $wr$, $go$ | $wr$, $go$ |
| $A_3$ | $A_1 \Rightarrow m$ | $m$ |
| $A_4$ | $A_2 \Rightarrow b$ | $b$ |
| $A_5$ | $A_3 \rightarrow hw$ | $hw$ |
| $A_6$ | $A_4 \rightarrow \neg hw$ | $\neg hw$ |

$A_5$ and $A_6$ conflict, but their top rules are strict, so restricted rebut gives no attack. There is no attack at all, and the grounded extension contains all six arguments. Its conclusions include $hw$ and $\neg hw$, which breaks consistency.

Now close the strict rules under transposition. This adds $\neg hw \rightarrow \neg m$ and $hw \rightarrow \neg b$, and two new arguments: $A_7 = A_6 \rightarrow \neg m$ and $A_8 = A_5 \rightarrow \neg b$. $A_7$ rebuts $A_3$ on $A_3$, so it attacks $A_3$, $A_5$ and $A_8$. $A_8$ rebuts $A_4$, so it attacks $A_4$, $A_6$ and $A_7$. Without preferences:

- the grounded extension is $\{A_1, A_2\}$;
- the preferred extensions have the conclusions $\{wr, go, m, hw, \neg b\}$ and $\{wr, go, b, \neg hw, \neg m\}$.

A scratch script built the arguments and computed these extensions. Now add the preference $d_2 < d_1$ with last link. $A_7$ has the last defeasible rule $d_2$, and it attacks $A_3$, whose last rule is $d_1$, so $A_7 \prec A_3$ and the attack fails. $A_8$ defeats $A_4$. The grounded extension is $\{A_1, A_2, A_3, A_5, A_8\}$ with the conclusions $wr$, $go$, $m$, $hw$ and $\neg b$. This set is closed under the strict rules and is consistent. The script confirmed this case too.

## Relation to other models

- **Abstract frameworks.** ASPIC+ produces a Dung framework. The [complete](/complete-extension/), grounded, preferred and stable semantics apply without change. Admissible sets and Dung's fundamental lemma carry over when the SAF is well defined and the ordering is reasonable (Propositions 10 and 11).
- **Assumption-based argumentation.** Prakken (2010) shows that flat [ABA](/assumption-based-argumentation/) frameworks are a special case. The assumptions become premises that can be attacked, the ABA contraries become ASPIC+ contraries, and all rules are strict. Prakken used a separate kind of assumption premise, and Modgil and Prakken (2013) note that the result also holds with ordinary premises.
- **Defeasible logic programming.** [DeLP](/defeasible-logic-programming/) also has strict and defeasible rules and compares arguments, but it uses dialectical trees instead of extensions and generalized specificity as its default comparison.
- **Value-based argumentation.** A [VAF](/value-based-argumentation/) applies preferences at the abstract level, from the values of the arguments. ASPIC+ derives the preferences from rules and premises.
- **Classical logic.** With $\mathcal{L}$ a propositional language, $\mathcal{R}_s$ all valid classical inferences and no defeasible rules, ASPIC+ gives a form of deductive argumentation. Modgil and Prakken (2013) study this instance with c-SAFs and compare it with the classical-logic approach of Besnard and Hunter.
- **Default reasoning.** Defeasible rules play the role of normal defaults in [default logic](/default-logic/), and undercuts express exceptions, as in Pollock's work on [nonmonotonic reasoning](/nonmonotonic-reasoning/).

## Known results in the model

Caminada and Amgoud (2007) proposed rationality postulates for the conclusions of an extension $E$:

| postulate | statement |
|---|---|
| sub-argument closure | every sub-argument of an argument in $E$ is in $E$ |
| closure under strict rules | the conclusions of $E$ are closed under $\mathcal{R}_s$ |
| direct consistency | the conclusions of $E$ have no $\varphi, \psi$ with $\varphi \in \overline{\psi}$ |
| indirect consistency | the closure of the conclusions under $\mathcal{R}_s$ is consistent |

Modgil and Prakken (2013) prove when ASPIC+ satisfies them:

- **Conditions.** The SAF or c-SAF is well defined (Definition 12): the strict closure of the axioms is consistent, the theory is well formed (a formula with a contrary is not an axiom and is not the head of a strict rule), and the strict rules are closed under transposition or under contraposition. A c-SAF must also be c-classical. The argument ordering is reasonable (Definition 18): strict and firm arguments are above all others, and adding strict rules or axioms to one argument does not change its strength.
- **Theorems 12 and 13.** Every complete extension is closed under sub-arguments, and its conclusions are closed under strict rules.
- **Theorem 14.** Every admissible extension is directly consistent.
- **Theorem 15.** Every complete extension is indirectly consistent.
- **Proposition 16.** Under these conditions, the extensions with attack-based conflict-freeness are the same as those with defeat-based conflict-freeness, for the admissible, complete, grounded, preferred and stable semantics. So the postulates hold for both readings.
- **Semantics covered.** Grounded, preferred and stable extensions are complete, so all the results hold for them.
- **Orderings that are reasonable (Propositions 19 to 22).** Last link and weakest link are reasonable when built on a reasonable-inducing set comparison, and both the Elitist and the Democratic comparisons are reasonable-inducing.

Some notes on the conditions:

- **Why the conditions are needed.** The worked example shows the effect of transposition: without it, the grounded extension is inconsistent. Caminada and Amgoud also show that unrestricted rebut, which allows attacks on strict conclusions, breaks the consistency postulates.
- **Corrections.** The 2018 corrigendum corrects errors in the 2013 paper, and the arXiv version 1804.06763 includes the corrections. The theorem numbers above follow the corrected text. The 2013 paper itself repairs two earlier errors of Prakken (2010): a definition of well-formedness that allowed counterexamples, and a weakest-link comparison that treated premises and rules in different ways.

## References
