---
tag: CK4JH0
kind: theorem
slug: loop-formulas
name: Lin-Zhao loop formula theorem
aliases:
- loop formulas
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: The stable models of a finite normal program are exactly the models of its completion that satisfy one loop formula for each loop of the positive dependency graph.
prereqs: [fages-theorem, clark-completion, stable-model-semantics, strongly-connected-components]
see_also: [sat, cdcl, conflict-driven-answer-set-solving, answer-set-programming, gelfond-lifschitz-reduct, tarjan-scc, smodels-algorithm, unit-propagation]
sources:
  - paper: doi:10.1016/j.artint.2004.04.004
    title: "Fangzhen Lin and Yuting Zhao, ASSAT: computing answer sets of a logic program by SAT solvers, Artificial Intelligence 157(1-2), 115 to 137 (2004)"
    locator: the definitions of loops and loop formulas, the main theorem and the ASSAT procedure
  - paper: "Vladimir Lifschitz and Alexander Razborov, Why are there so many loop formulas?, ACM Transactions on Computational Logic 7(2), 261 to 268 (2006)"
    locator: the lower bound on the size of translations without new atoms
  - paper: "François Fages, Consistency of Clark's completion and existence of stable models, Methods of Logic in Computer Science 1(1), 51 to 60 (1994)"
    locator: the case of programs without positive cycles
  - book: isbn:9781608459711
    title: Martin Gebser, Roland Kaminski, Benjamin Kaufmann and Torsten Schaub, Answer Set Solving in Practice, Morgan and Claypool (2012)
    locator: the chapter on the characterization of stable models by completion and loop nogoods, and their use in clasp
---

The Lin-Zhao theorem gives a classical description of the [stable models](/stable-model-semantics/) of any finite normal program. The [Clark completion](/clark-completion/) admits extra models in which atoms on a positive cycle support each other, and [Fages' theorem](/fages-theorem/) says this is the only problem. Lin and Zhao (2004) found the formulas that remove exactly these extra models: one *loop formula* for each loop of the program. With them, a [SAT](/sat/) solver can compute stable models of programs that are not tight, which their system ASSAT did, and the same formulas, as loop nogoods, are part of modern answer set solvers.

## Statement

Let $P$ be a finite ground normal program over the atoms $A$, with rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$. The *positive dependency graph* $G_P$ has the vertices $A$ and an edge $h \to b_i$ for each rule and each positive body atom $b_i$.

- A *loop* is a nonempty set $L \subseteq A$ such that for all $a, b \in L$ there is a path of length at least one from $a$ to $b$ in $G_P$ that stays inside $L$. A single atom is a loop only if it has a self edge.
- The *external support* $\mathrm{ES}(L)$ is the set of rules whose head is in $L$ and which have no positive body atom in $L$.
- The *loop formula* of $L$ is
$$\mathrm{LF}(L) = \Big(\bigvee_{a \in L} a\Big) \rightarrow \bigvee_{r \in \mathrm{ES}(L)} \mathrm{body}(r),$$
where $\mathrm{body}(r) = b_1 \wedge \cdots \wedge b_m \wedge \neg c_1 \wedge \cdots \wedge \neg c_k$ and the empty disjunction is $\bot$.

**Theorem** (Lin and Zhao 2004). A set $M \subseteq A$ is a stable model of $P$ if and only if $M$ is a model of $\mathrm{Comp}(P)$ and of $\mathrm{LF}(L)$ for every loop $L$ of $P$.

A loop formula says: if some atom of the loop is true, the loop must get support from outside itself.

## In plain words

Two facts can hold each other up with nothing else under them: "the door is locked because the alarm is on, and the alarm is on because the door is locked". The plain reading of a program as "true when a rule applies" accepts such a pair. The stable model reading does not, because nothing starts the chain. The theorem finds every group of atoms that can lean on each other in this way, and adds one condition per group: if any member of the group is true, then some rule must make it true without using the group. With these extra conditions, the plain reading gives exactly the stable models, and a general solver for logic formulas can find them.

## Proof

The theorem is from Lin and Zhao (2004). The short proof below goes through the least model of the [reduct](/gelfond-lifschitz-reduct/), $\mathrm{lm}(P^M)$, and uses Steps 1 and 2 of the proof of [Fages' theorem](/fages-theorem/): the models of $\mathrm{Comp}(P)$ are the supported models ($M = T_P(M)$), and every stable model is supported.

**Stable implies the loop formulas.** Let $M = \mathrm{lm}(P^M)$. It is a model of the completion by Step 2. Let $L$ be a loop with $L \cap M \neq \emptyset$. Compute $\mathrm{lm}(P^M)$ by forward chaining, adding one atom at a time, and let $a$ be the first atom of $L$ that is added. It is added by a rule $a \leftarrow b_1, \ldots, b_m$ of $P^M$ whose $b_i$ were added before $a$, so they are in $M$ and not in $L$. This rule comes from a rule $r$ of $P$ with no $c_j \in M$. So $r \in \mathrm{ES}(L)$, its body is true in $M$, and $\mathrm{LF}(L)$ holds.

**The loop formulas imply stable.** Let $M$ be a model of $\mathrm{Comp}(P)$ and of all loop formulas. Then $M$ is supported, and $\mathrm{lm}(P^M) \subseteq M$ as in Step 3 of Fages' proof. Suppose that $D = M \setminus \mathrm{lm}(P^M)$ is not empty. For each $a \in D$, take any rule $r$ with head $a$ and body true in $M$; one exists because $M$ is supported. If all positive atoms of $r$ were in $\mathrm{lm}(P^M)$, the rule $a \leftarrow b_1, \ldots, b_m$ of $P^M$ would put $a$ in $\mathrm{lm}(P^M)$. So $r$ has a positive body atom in $D$. Hence every vertex of the subgraph of $G_P$ induced by $D$ has an edge inside $D$. Take a [strongly connected component](/strongly-connected-components/) $C$ of this subgraph that is a sink: no edge leaves $C$ to the rest of $D$. Each vertex of $C$ has an edge inside $D$, so inside $C$, and $C$ is a loop. Since $C \subseteq M$, $\mathrm{LF}(C)$ gives a rule $r \in \mathrm{ES}(C)$ whose body is true in $M$. Its head is in $C \subseteq D$, so by the argument above it has a positive body atom $b \in D$, and $b \notin C$ because $r$ is external. The edge from the head to $b$ leaves $C$ inside $D$, which contradicts the choice of $C$. So $D = \emptyset$ and $M = \mathrm{lm}(P^M)$.

**A check by hand.** Take

```text
p ← q.    q ← p.    p ← not r.    r.
```

The completion is $p \leftrightarrow q \vee \neg r$, $q \leftrightarrow p$, $r$. Its models are $\{r\}$ and $\{p, q, r\}$. The only loop is $\{p, q\}$, with external support $p \leftarrow \mathit{not}\ r$, so $\mathrm{LF}(\{p, q\}) = p \vee q \rightarrow \neg r$. It is false in $\{p, q, r\}$ and true in $\{r\}$, which is the only stable model: the reduct by $\{p, q, r\}$ is $\{p \leftarrow q,\ q \leftarrow p,\ r\}$, whose least model is $\{r\}$.

## Consequences

- **ASSAT.** Lin and Zhao compute stable models with a SAT solver: solve the clauses of the completion; if the model $M$ is not stable, the proof above finds a violated loop in $M \setminus \mathrm{lm}(P^M)$ in linear time with [Tarjan's algorithm](/tarjan-scc/); add its loop formula and solve again. Each round removes $M$, and the loop formulas are added only when they are needed.
- **Fages' theorem.** A tight program has no loops, so the theorem reduces to the completion alone.
- **Conflict-driven solvers.** In [conflict-driven answer set solving](/conflict-driven-answer-set-solving/), the solver clasp treats the completion as nogoods for [unit propagation](/unit-propagation/) and adds loop nogoods when an unfounded set is found during the search (Gebser et al. 2012).
- **Many loops.** The number of loops can be exponential. If $P$ has the rules $a_i \leftarrow a_j$ for all $i \neq j$ among $n$ atoms, every set of at least two atoms is a loop, which gives $2^n - n - 1$ loops. Lifschitz and Razborov (2006) proved that this cannot be avoided by a cleverer formula in the same atoms: if $\mathrm{P} \not\subseteq \mathrm{NC}^1/\mathrm{poly}$, there is no translation of programs into propositional formulas over the same atoms that preserves the models and has polynomial size. Translations with new atoms of polynomial size exist, so the bound is about the vocabulary.

## Tightness

- **All loops are needed, not only the maximal ones.** Take $a$, $a \leftarrow b$ and $b \leftarrow a, b$. The loops are $\{b\}$, from the self edge, and $\{a, b\}$. The completion $a \leftrightarrow \top$, $b \leftrightarrow a \wedge b$ has the models $\{a\}$ and $\{a, b\}$, and the only stable model is $\{a\}$. The maximal loop $\{a, b\}$ has the fact $a$ as external support, so its formula is always true. The loop $\{b\}$ has no external support, and $\mathrm{LF}(\{b\}) = b \rightarrow \bot$ removes $\{a, b\}$.
- **The completion is needed.** For $p \leftarrow \mathit{not}\ q$ there are no loops, so the loop formulas alone allow every set of atoms. The completion makes $\{p\}$ the only model.
- **Finiteness is needed.** The infinite program $p_i \leftarrow p_{i+1}$ for $i = 0, 1, 2, \ldots$ has no loops, as its graph has no cycle, yet its completion has the model in which every $p_i$ is true, which is not stable.

## History

Lin and Zhao presented loop formulas and ASSAT at AAAI 2002 and published the full version in 2004. The home page of ASSAT gives a correction to the definition of loops in the published paper. Later work extended loop formulas to disjunctive programs and to arbitrary propositional formulas. Lifschitz and Razborov (2006) explained why the number of loop formulas has to be large, and solvers such as clasp turned loop formulas into learned nogoods (Gebser et al. 2012).

## References
