---
tag: 25MA47
kind: model
slug: rewriting-logic
name: Rewriting logic
aliases:
- Meseguer's rewriting logic
area: automata-and-parsing/term-rewriting
level: research
summary: A logical framework in which concurrent computation is modelled by rewrite rules, as in Maude.
prereqs: [term-rewriting-system, rewriting-modulo-equations, equational-theory]
see_also: [petri-net, labelled-transition-system, ltl-model-checking, kripke-structure, narrowing, ac-matching, parallel-rewriting, reachability-problem]
sources:
  - paper: doi:10.1016/0304-3975(92)90182-F
    title: José Meseguer, Conditional rewriting logic as a unified model of concurrency, Theoretical Computer Science 96(1) (1992)
    locator: pp. 73 to 155 (rewrite theories, the four rules of deduction, proof terms and the model T_R, soundness and completeness, initial models, and the encodings of models of concurrency)
  - paper: doi:10.1016/0890-5401(90)90013-8
    title: José Meseguer and Ugo Montanari, Petri nets are monoids, Information and Computation 88(2) (1990)
    locator: pp. 105 to 155 (a place/transition net as a graph over the free commutative monoid of places, and its computations as a commutative monoidal category)
  - paper: doi:10.1016/S0304-3975(01)00366-8
    title: Patrick Viry, Equational rules for rewriting logic, Theoretical Computer Science 285(2) (2002)
    locator: pp. 487 to 517 (coherence of rules with respect to oriented equations, so that rewriting modulo the equations can be done on canonical forms)
  - paper: doi:10.1016/S0304-3975(01)00357-7
    title: Narciso Martí-Oliet and José Meseguer, Rewriting logic, roadmap and bibliography, Theoretical Computer Science 285(2) (2002)
    locator: pp. 121 to 154 (survey of the logic, its models, its use as a logical and semantic framework, and its languages)
  - book: doi:10.1007/978-3-540-71999-1
    title: Manuel Clavel, Francisco Durán, Steven Eker, Patrick Lincoln, Narciso Martí-Oliet, José Meseguer and Carolyn Talcott, All About Maude, A High-Performance Logical Framework, LNCS 4350, Springer, 2007
    locator: chapter System Modules, pp. 131 to 157 (rules, the rewrite and search commands, executability), chapter Model Checking Invariants Through Search, pp. 373 to 384, and chapter LTL Model Checking, pp. 385 to 418
  - paper: doi:10.1016/S1571-0661(05)82534-4
    title: Steven Eker, José Meseguer and Ambarish Sridharanarayanan, The Maude LTL model checker, Electronic Notes in Theoretical Computer Science 71 (2004)
    locator: pp. 162 to 187 (Kripke structures from rewrite theories with state predicates, and on-the-fly LTL model checking for finite reachable state spaces)
---

**Rewriting logic** is a logic, and a model of computation, in which a rewrite rule $l \to r$ is read as a local change of state and not as an equation. A system is a **rewrite theory**: a signature, a set $E$ of equations that say which terms are the same state, and a set of rules that say how a state can change. Meseguer introduced it in 1992 as a unified model of concurrency, in which a deduction in the logic is a concurrent computation and the models of a theory are concurrent systems. The language Maude runs rewrite theories, and its tools search and model check them.

## The machine

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, $\to^*$ for the reflexive transitive closure, positions as sequences of positive integers, and substitutions $\sigma$. For a set $E$ of equations, $[t]_E$ is the class of $t$ under the equational theory of $E$, and we drop the index when $E$ is clear.

**Rewrite theories.** A rewrite theory is a triple $\mathcal{R} = (\Sigma, E, R)$, where $\Sigma$ is a signature, $E$ is a set of $\Sigma$-equations, and $R$ is a set of labelled rules $\ell : l \to r$ with $l, r \in T(\Sigma, V)$. Meseguer also allows conditional rules $\ell : l \to r$ if $u_1 \to v_1 \wedge \dots \wedge u_k \to v_k$; we keep to the unconditional case. The two parts have different jobs:

- the equations $E$ fix the **states**: a state is a class $[t]_E$, so equal terms are the same state. Typical equations make an operator associative and commutative, so that a state can be a multiset or a set.
- the rules $R$ fix the **transitions**: $l \to r$ says that a part of the state that matches $l$ can change into $r$. It does not say that $l$ equals $r$, and it is not read from right to left.

**Sentences and deduction.** A sentence is a sequent $[t] \to [t']$, read as "the state $[t]$ can evolve into the state $[t']$ by a finite, possibly concurrent, computation". The sequents of $\mathcal{R}$ are those derived by four rules. In the replacement rule, $l(\vec w/\vec x)$ is $l$ with $w_i$ in place of its variable $x_i$.

1. **Reflexivity.** $[t] \to [t]$ for every term $t$.
2. **Congruence.** For each $f \in \Sigma$ of arity $n$: from $[t_1] \to [t_1'], \dots, [t_n] \to [t_n']$ derive $[f(t_1, \dots, t_n)] \to [f(t_1', \dots, t_n')]$.
3. **Replacement.** For each rule $\ell : l \to r$ with variables $x_1, \dots, x_n$: from $[w_1] \to [w_1'], \dots, [w_n] \to [w_n']$ derive $[l(\vec w/\vec x)] \to [r(\vec w'/\vec x)]$.
4. **Transitivity.** From $[t_1] \to [t_2]$ and $[t_2] \to [t_3]$ derive $[t_1] \to [t_3]$.

There is no symmetry rule. That is the difference from [equational logic](/equational-theory/), where the same rules with symmetry derive $t = t'$.

**Kinds of steps.** A sequent is a **one-step concurrent rewrite** if it can be derived by rules 1 to 3 with at least one use of replacement, and a **one-step sequential rewrite** if it can be derived with exactly one use of replacement. A one-step sequential rewrite is a [rewrite step](/rewrite-step/) of $R$ modulo $E$: some $t_0 \in [t]$ has a subterm $l\sigma$ at a position $p$, and $t_0[r\sigma]_p \in [t']$. This is the relation $\to_{R/E}$ of [rewriting modulo equations](/rewriting-modulo-equations/). Congruence lets independent replacements happen in different arguments in one step, and replacement with nontrivial $[w_i] \to [w_i']$ lets steps inside the matched part happen at the same time as the step at the top. So a one-step concurrent rewrite is a [parallel rewriting](/parallel-rewriting/) step modulo $E$, and in general more.

**Proof terms.** Each derivation can be written as a term: $t$ for reflexivity, $f(\alpha_1, \dots, \alpha_n)$ for congruence, $\ell(\alpha_1, \dots, \alpha_n)$ for replacement, and $\alpha ; \beta$ for transitivity. In the model $\mathcal{T}_\mathcal{R}$ that Meseguer builds, the states are the classes $[t]$, the arrows are the proof terms modulo a set of equations, and these equations say when two derivations are the same computation:

- $;$ is associative, and $[t]$ is an identity for it;
- each $f \in \Sigma$ acts as a functor: $f(\alpha_1 ; \beta_1, \dots, \alpha_n ; \beta_n) = f(\vec\alpha) ; f(\vec\beta)$;
- the equations of $E$ hold also between proof terms;
- **exchange**: for $\ell : l \to r$ and $\alpha_i : [w_i] \to [w_i']$, $\ell(\vec\alpha) = \ell(\vec w) ; r(\vec\alpha/\vec x) = l(\vec\alpha/\vec x) ; \ell(\vec w')$.

The exchange law says that a step at the top and steps inside the matched part can be done in either order, or at the same time, and still be one computation.

**An example.** A vending machine. The sort $\mathit{State}$ is made of the constants $\$$ (a dollar), $q$ (a quarter), $a$ (an apple) and $c$ (a cake), an empty state $\mathbf{1}$, and a binary operator written by juxtaposition. The equations $E$ make juxtaposition associative and commutative with identity $\mathbf{1}$, so a state is a multiset. The rules are

$$\mathit{buy\text{-}c} : \$ \to c \qquad \mathit{buy\text{-}a} : \$ \to a\, q \qquad \mathit{change} : q\, q\, q\, q \to \$.$$

From the state $\$\, \$\, q\, q\, q$, a script that enumerates the multisets finds 12 reachable states, 15 one-step sequential rewrites between them, and 4 states with no successor: $c\, c\, q\, q\, q$, $a\, c\, c$, $a\, a\, c\, q$ and $a\, a\, a\, q\, q$. There are 11 maximal sequential runs, the longest with 4 steps, for example $\mathit{buy\text{-}a}$, $\mathit{change}$, $\mathit{buy\text{-}c}$, $\mathit{buy\text{-}c}$, which goes through $\$\, a\, q^4$ and $a\, \$\, \$$. The proof term $\mathit{buy\text{-}c} \, \mathit{buy\text{-}a} \, q\, q\, q$ (congruence on juxtaposition, with a replacement in each of the first two places) is one concurrent step from $\$\, \$\, q\, q\, q$ to $c\, a\, q^4$. By functoriality it is equal to both orders of the two sequential steps. If two runs are called the same when they differ by swapping two adjacent steps whose left sides fit side by side in the state, the 11 runs fall into 4 classes, one for each final state. Each swap is an instance of the functoriality equation, so runs in one class give equal proof terms.

## What it counts

Rewriting logic is a model for specifying systems, not a model with one fixed cost. The usual measures are these.

- **Sequential length.** The number of one-step sequential rewrites in a computation. In the example, every maximal run has 2 or 4 steps.
- **Concurrent length.** The number of one-step concurrent rewrites, which is a measure of parallel time. A maximal set of non-overlapping rule instances can fire in one step. In the example, $c\, c\, q\, q\, q$ is 2 sequential steps but 1 concurrent step away, and the other three final states are 4 sequential steps but 3 concurrent steps away: the two dollars are spent at once, then $\mathit{change}$ fires, then the new dollar is spent.
- **States modulo $E$.** For search and model checking, the cost is the number of reachable classes $[t]$, not the number of terms. In the example, $q\, \$\, q\, \$\, q$ and $\$\, \$\, q\, q\, q$ are one state. The equations are what keeps the state space small: without commutativity, the same machine has a different state for each order of the coins.
- **Cost of one step.** Equational steps are not transitions. To compute one transition, an implementation matches $l$ modulo the axioms and puts the result into a canonical form for $E$. Matching modulo associativity and commutativity is the hard part; see [AC matching](/ac-matching/).

In Maude, $E$ is split as $E_0 \cup A$, where $A$ is a set of axioms such as associativity, commutativity and identity that matching handles directly, and $E_0$ is a set of equations used as rules that are [confluent](/confluence/) and [terminating](/termination/) modulo $A$. A state is then represented by its $E_0$ normal form modulo $A$.

## Relation to other models

- **[Term rewriting systems](/term-rewriting-system/).** A term rewriting system $R$ is the rewrite theory $(\Sigma, \emptyset, R)$, and $[t] \to [t']$ is derivable exactly when $t \to_R^* t'$. The difference is in the reading. Term rewriting is often used to decide the equational theory of $R$, where [confluence](/confluence/) and [termination](/termination/) matter. In rewriting logic the rules are transitions, and a rewrite theory that is not confluent and not terminating, such as a server that runs forever and chooses among requests, is the normal case.
- **[Equational logic](/equational-theory/).** The equational part $(\Sigma, E)$ of a rewrite theory is an equational theory, and its initial algebra is the set of states. A rewrite theory whose rules are all reversible, so that each rule $l \to r$ has a rule $r \to l$, derives $[t] \to [t']$ exactly when $t$ and $t'$ are equal under $E \cup R$.
- **[Petri nets](/petri-net/).** A place/transition net is a rewrite theory whose states are multisets of places, with juxtaposition associative and commutative with an identity, and one rule $\ell : m \to m'$ for each transition with input marking $m$ and output marking $m'$. The vending machine above is such a net, with places $\$$, $q$, $a$ and $c$. Meseguer and Montanari (1990) show that the computations of a net form a commutative monoidal category, which is the model $\mathcal{T}_\mathcal{R}$ in this case. So [Petri net reachability](/petri-net-reachability-decidability/) is reachability in this class of rewrite theories.
- **[Labelled transition systems](/labelled-transition-system/).** A finite transition system with states $s_i$ and labelled transitions is a rewrite theory with one constant per state and one rule $\ell : s_i \to s_j$ per transition. Meseguer (1992) treats this case and also encodes grammars, CCS, the chemical abstract machine and actor systems.
- **[Kripke structures](/kripke-structure/).** A rewrite theory with a chosen sort of states, an initial state, and equations that define which atomic propositions hold in a state, gives a Kripke structure: the states are the reachable classes, and the transitions are the one-step sequential rewrites. This is the bridge to [LTL model checking](/ltl-model-checking/).
- **[Narrowing](/narrowing/).** Rewriting a term with variables needs matching; narrowing uses unification instead, and so runs a rewrite theory on symbolic states that stand for infinitely many concrete states.
- **Logical framework.** Martí-Oliet and Meseguer use rewriting logic as a logical framework: the inference rules of another logic become rewrite rules, a sequent of that logic becomes a state, and a proof becomes a computation.

## Known results in the model

**Soundness and completeness.** Meseguer (1992) defines the models of a rewrite theory as categories with a $\Sigma$-structure in which $E$ holds and each rule is interpreted by a natural transformation, and proves that the four rules of deduction are sound and complete for them: $[t] \to [t']$ is derivable from $\mathcal{R}$ exactly when it holds in every model. The model $\mathcal{T}_\mathcal{R}$ of proof terms is initial. The same paper shows that every proof term is equal, by the equations above, to a sequence of one-step sequential rewrites, so every concurrent computation can be interleaved.

**Reachability is undecidable in general.** Given $\mathcal{R}$, $t$ and $t'$, it is undecidable whether $[t] \to [t']$ is derivable, already with $E = \emptyset$. Proof sketch: write a configuration of a [Turing machine](/turing-machine/) as a term, with a rule for each transition, and add rules that erase the tape once the machine is in its halting state and leave a constant $h$. Then the machine halts on its input $w$ exactly when $[t_w] \to [h]$, where $t_w$ is the initial configuration. The halting problem is undecidable, so this [reachability problem](/reachability-problem/) is too.

**Reachability is semi-decidable for executable theories.** If $E$ is decidable and each state has finitely many one-step sequential successors that can be computed, a breadth-first search from $[t]$ visits every reachable state after finitely many steps, and so it finds $[t']$ whenever $[t] \to [t']$ holds. It need not stop when $[t']$ is not reachable. Maude's search command is such a search; with a bound on the depth or a finite reachable state space it always stops (Clavel et al., chapter Model Checking Invariants Through Search).

**Executability needs coherence.** With $E = E_0 \cup A$ as in the section above, the natural way to run $\mathcal{R}$ is: put the term into its $E_0$ normal form modulo $A$, apply one rule modulo $A$, and normalize again. This finds every one-step rewrite modulo $E$ only if the rules are **coherent** with $E_0$ modulo $A$ (Viry 2002): whenever $t$ rewrites by a rule to $t'$, the $E_0$ normal form of $t$ rewrites by a rule to a term with the same $E_0$ normal form as $t'$. A small failure: let $E_0 = \{g(a) \to b\}$ and $R = \{a \to c\}$. Then $[g(a)] \to [g(c)]$ is a one-step rewrite, but the normal form $b$ of $g(a)$ has no redex, so the strategy misses it. Adding the rule $b \to g(c)$ restores coherence. Viry's paper gives a completion procedure that adds such rules, in the style of [critical pairs](/critical-pair/).

**Model checking.** If the set of states reachable from the initial state is finite, a rewrite theory with state predicates is a finite Kripke structure, and every [linear temporal logic](/linear-temporal-logic/) property can be checked on it. Eker, Meseguer and Sridharanarayanan (2004) describe the Maude LTL model checker, which builds the states on the fly from the rules and uses the automata-theoretic method. Invariants can also be checked by the search command, which returns a counterexample path when one exists.

**Petri nets as a special case.** For theories whose states are multisets and whose rules are as in the Petri net item above, the model $\mathcal{T}_\mathcal{R}$ is the category of computations of the net of Meseguer and Montanari (1990), and the equations on proof terms identify the runs that differ by the order of independent firings, as in the 11 runs and 4 classes of the vending machine.

## References
