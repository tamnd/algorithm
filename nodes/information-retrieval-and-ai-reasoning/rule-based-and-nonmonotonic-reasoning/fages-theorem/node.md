---
tag: YYCJPC
kind: theorem
slug: fages-theorem
name: Fages' theorem
aliases:
- tight program theorem
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: If no atom of a normal program depends positively on itself, the stable models of the program are exactly the models of its Clark completion, so a SAT solver can find them.
prereqs: [clark-completion, stable-model-semantics]
see_also: [loop-formulas, sat, cdcl, answer-set-programming, conflict-driven-answer-set-solving, strongly-connected-components, gelfond-lifschitz-reduct, stable-model-np-completeness]
sources:
  - paper: "François Fages, Consistency of Clark's completion and existence of stable models, Methods of Logic in Computer Science 1(1), 51 to 60 (1994)"
    locator: the main theorem on positive-order-consistent programs
  - paper: doi:10.1017/S1471068403001765
    title: Esra Erdem and Vladimir Lifschitz, Tight logic programs, Theory and Practice of Logic Programming 3(4-5), 499 to 518 (2003)
    locator: Corollary 2
  - paper: doi:10.1007/978-1-4684-3384-5_11
    title: Keith L. Clark, Negation as failure, in Hervé Gallaire and Jack Minker (eds.), Logic and Data Bases, Plenum Press, New York, 293 to 322 (1978)
    locator: the definition of the completion
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the definition of stable models
  - paper: doi:10.1016/j.artint.2004.04.004
    title: "Fangzhen Lin and Yuting Zhao, ASSAT: computing answer sets of a logic program by SAT solvers, Artificial Intelligence 157(1-2), 115 to 137 (2004)"
    locator: the generalization of the theorem to programs with loops
---

Fages' theorem says when the two main readings of [negation as failure](/negation-as-failure/) agree. Every [stable model](/stable-model-semantics/) of a normal program is a model of its [Clark completion](/clark-completion/), but the completion can have more models, because it accepts atoms that support each other in a positive cycle. Fages (1994) proved that if the program has no such cycles, the two sets of models are the same. The result is the reason why the stable models of many programs can be found by a [SAT](/sat/) solver, and [loop formulas](/loop-formulas/) extend it to all programs.

## Statement

Let $P$ be a ground normal program over a set $A$ of atoms, possibly infinite. A rule has the form $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$, and $\mathrm{Comp}(P)$ is its completion: for each $a \in A$, the formula $a \leftrightarrow \bigvee \mathrm{body}(r)$ over the rules $r$ with head $a$, with $\bigvee \emptyset = \bot$.

$P$ is *tight* if there is a level mapping $\lambda : A \to \mathbb{N}$ such that, for every rule of $P$ and every positive body atom $b_i$ of it, $\lambda(h) > \lambda(b_i)$. For a finite program, this means that the *positive dependency graph*, with an edge from $h$ to each $b_i$, has no cycle.

**Theorem** (Fages 1994). If $P$ is tight, then a set $M \subseteq A$ is a stable model of $P$ if and only if $M$ is a model of $\mathrm{Comp}(P)$.

Negative body literals play no part in the hypothesis. Fages called such programs *positive-order-consistent*; the name *tight* is from Erdem and Lifschitz (2003), who proved a more general form (their Corollary 2 covers this case).

## In plain words

A logic program can be read in two ways. In the first, an atom is true when one of its rules applies, and false when none does. In the second, which is the stable model reading, an atom is true only if it can be built up step by step from facts. The first reading allows a circle: "p because q, and q because p" makes both true with no outside reason. The second does not. If the program has no such circle among its positive conditions, the two readings give the same answers. Then each atom can be checked with a simple local rule, and a solver for plain logic formulas can do the work.

## Proof

The proof has three steps. Write $T_P(M)$ for the set of heads of rules whose body is true in $M$, and $\mathrm{lm}(P^M)$ for the least model of the [reduct](/gelfond-lifschitz-reduct/) of $P$ by $M$.

**Step 1: the models of the completion are the sets with $M = T_P(M)$.** The formulas $a \leftarrow \bigvee \mathrm{body}(r)$ hold in $M$ exactly when $T_P(M) \subseteq M$. The formulas $a \rightarrow \bigvee \mathrm{body}(r)$ hold exactly when each $a \in M$ is the head of a rule whose body is true in $M$, that is $M \subseteq T_P(M)$. Such sets are the *supported models*.

**Step 2: every stable model is supported, for any $P$.** Let $M = \mathrm{lm}(P^M)$. If the body of a rule $r$ is true in $M$, then no $c_j$ is in $M$, so $P^M$ contains $h \leftarrow b_1, \ldots, b_m$ with all $b_i \in M = \mathrm{lm}(P^M)$, and $h \in M$. So $T_P(M) \subseteq M$. If $a \in M = \mathrm{lm}(P^M)$, then some rule $a \leftarrow b_1, \ldots, b_m$ of $P^M$ has all $b_i \in M$. It comes from a rule of $P$ with no $c_j \in M$, so the body of that rule is true in $M$ and $a \in T_P(M)$.

**Step 3: if $P$ is tight, every supported model is stable.** Let $M = T_P(M)$. First, $\mathrm{lm}(P^M) \subseteq M$, because $M$ is closed under the rules of $P^M$: such a rule comes from a rule $r$ of $P$ with no $c_j \in M$, and if its $b_i$ are in $M$, the body of $r$ is true in $M$, so its head is in $T_P(M) = M$. Second, we show $a \in \mathrm{lm}(P^M)$ for each $a \in M$, by induction on $\lambda(a)$. Since $a \in T_P(M)$, some rule $r$ with head $a$ has its body true in $M$. Its positive atoms $b_i$ are in $M$ and have $\lambda(b_i) < \lambda(a)$, so by the induction hypothesis they are in $\mathrm{lm}(P^M)$. No $c_j$ is in $M$, so $a \leftarrow b_1, \ldots, b_m$ is in $P^M$, and $a \in \mathrm{lm}(P^M)$. The induction is valid because the levels are natural numbers. Hence $M = \mathrm{lm}(P^M)$.

Steps 1 and 2 give "stable implies a model of the completion" for every program, and Steps 1 and 3 give the converse for tight programs. This is the argument of Fages (1994); Erdem and Lifschitz (2003) give the same structure in a more general setting.

**A check by hand.** Take $p \leftarrow \mathit{not}\ q$, $q \leftarrow \mathit{not}\ p$, $r \leftarrow p, \mathit{not}\ s$. The only positive edge is $r \to p$, so the program is tight. The completion is $p \leftrightarrow \neg q$, $q \leftrightarrow \neg p$, $r \leftrightarrow p \wedge \neg s$, $\neg s$. Its models are $\{q\}$ and $\{p, r\}$. The reduct by $\{q\}$ is $\{q,\ r \leftarrow p\}$ with least model $\{q\}$, and the reduct by $\{p, r\}$ is $\{p,\ r \leftarrow p\}$ with least model $\{p, r\}$, so both are stable, as the theorem says.

## Consequences

- **Answer sets by SAT.** For a finite tight program, the clausal form of the completion, which is linear in the size of the program after one new atom per rule body, is a SAT instance whose models are the stable models. The first answer set solvers built on SAT solvers used this for tight programs.
- **Consistency.** The title of Fages' paper: a tight program has a stable model if and only if its completion is consistent.
- **The search problem stays hard.** Tight programs are enough to encode SAT: for each variable $x$, the rules $x \leftarrow \mathit{not}\ \bar{x}$ and $\bar{x} \leftarrow \mathit{not}\ x$, and for each clause a constraint that is violated when all its literals are false. The program is tight, so deciding whether a tight program has a stable model is still [NP-complete](/stable-model-np-completeness/).
- **Testing the hypothesis.** Tightness of a finite program is decided in linear time by a search for a cycle in the positive dependency graph, for example with the [strongly connected components](/strongly-connected-components/).
- **Programs with loops.** For a program that is not tight, the stable models are the models of the completion that also satisfy the [loop formulas](/loop-formulas/) of Lin and Zhao (2004). Fages' theorem is the case in which there are no loops.

## Tightness

The hypothesis cannot be dropped. The program $p \leftarrow p$ has the positive cycle $p \to p$. Its completion $p \leftrightarrow p$ has the models $\emptyset$ and $\{p\}$, while the only stable model is $\emptyset$.

For infinite programs, an acyclic positive dependency graph is not enough. The program $p_i \leftarrow p_{i+1}$ for $i = 0, 1, 2, \ldots$ has no cycle, but it has no level mapping into $\mathbb{N}$, because $\lambda(p_0) > \lambda(p_1) > \cdots$ is impossible. Its completion has the model in which every $p_i$ is true, while the only stable model is $\emptyset$. The induction of Step 3 needs a well-founded order.

The condition is sufficient, not necessary: $\{p \leftarrow p,\ p\}$ is not tight, but its completion and its stable models are both $\{p\}$. Erdem and Lifschitz (2003) weaken the hypothesis to tightness on a set $X$ of atoms, which constrains only the rules whose head and positive body atoms lie in $X$; the conclusion then holds for the models contained in $X$.

## History

Clark (1978) defined the completion, and Gelfond and Lifschitz (1988) defined stable models. Fages (1994) proved that the two agree on positive-order-consistent programs. Erdem and Lifschitz (2003) gave the name tight programs, and extended the result to programs with nested expressions and to tightness relative to a set of atoms. Lin and Zhao (2004) removed the hypothesis by adding loop formulas to the completion.

## References
