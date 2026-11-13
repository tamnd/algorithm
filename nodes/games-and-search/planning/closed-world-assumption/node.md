---
tag: VM7HVH
kind: definition
slug: closed-world-assumption
name: Closed-world assumption
aliases:
- CWA
area: games-and-search/planning
level: intro
summary: Facts not stated to hold in a state are taken to be false.
prereqs: [state-space]
see_also: [strips, pddl, frame-problem, horn-clause, datalog, sldnf-resolution, logic-programming, conformant-planning]
sources:
  - paper: doi:10.1007/978-1-4684-3384-5_3
    title: "Raymond Reiter, On closed world data bases, in H. Gallaire and J. Minker (editors), Logic and Data Bases, Plenum Press, 1978"
    locator: pp. 55 to 76 (the definition of the closed world assumption, and its consistency for Horn databases)
  - paper: doi:10.1016/0004-3702(80)90011-9
    title: "John McCarthy, Circumscription: A form of non-monotonic reasoning, Artificial Intelligence 13(1-2) (1980)"
    locator: the definition of circumscription of a predicate (general locator)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 2, Section 2.3 (classical representation, states as sets of ground atoms)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.1 (states as conjunctions of ground fluents, with the closed world assumption)
---

The closed world assumption is the rule that a fact which is not stated, or cannot be derived, is false. Reiter (1978) named it in the theory of deductive databases, where a query about a missing row gets the answer "no" and not "unknown". In planning, it is what lets a [STRIPS](/strips/) or [PDDL](/pddl/) state be a plain set of true facts: every fact outside the set is false. It keeps states small and makes them complete, but it is wrong for a world that the agent does not fully know.

## Definition

### For a logical database

Let $T$ be a set of first-order sentences (a database) over a language with finitely many constants. The closed world assumption adds the negation of every ground atom that $T$ does not entail:

$$\mathrm{CWA}(T) = T \cup \{\lnot p : p \text{ a ground atom and } T \not\models p\}.$$

A query is then answered from $\mathrm{CWA}(T)$ instead of $T$. The rule is nonmonotonic: adding a sentence to $T$ can remove a conclusion, since a new fact $p$ removes $\lnot p$.

$\mathrm{CWA}(T)$ can be inconsistent when $T$ is. It can also be inconsistent when $T$ is consistent but has disjunctions: $T = \{P(a) \lor P(b)\}$ entails neither $P(a)$ nor $P(b)$, so $\mathrm{CWA}(T)$ contains $\lnot P(a)$ and $\lnot P(b)$, which contradict $T$. Reiter proved that for a consistent set of [Horn clauses](/horn-clause/), $\mathrm{CWA}(T)$ is consistent. The ground atoms it makes true are then exactly those of the least Herbrand model of $T$. This is the case of [Datalog](/datalog/) and of ground STRIPS states.

### For planning states

Fix a set $F$ of ground facts. Under the closed world assumption a state is a subset $s \subseteq F$, and

- $s \models f$ if and only if $f \in s$;
- $s \models \lnot f$ if and only if $f \notin s$.

So a state is a complete truth assignment to $F$, written by listing only its true facts. The initial state of a PDDL problem, the `:init` section, is read this way. The goal is not: a goal $G \subseteq F$ says that some facts must be true, and leaves every other fact free.

## Examples and non-examples

### Examples

- The [blocks world](/blocks-world/) state with $C$ on $A$, and $A$ and $B$ on the table, is $\{\mathit{on}(C, A), \mathit{ontable}(A), \mathit{ontable}(B), \mathit{clear}(C), \mathit{clear}(B), \mathit{handempty}\}$. With three blocks there are 16 facts, so these 6 facts also say that the other 10, such as $\mathit{on}(A, B)$ and $\mathit{clear}(A)$, are false.
- A flight database with the rows $\mathit{flight}(\mathit{Paris}, \mathit{Rome})$ and $\mathit{flight}(\mathit{Rome}, \mathit{Oslo})$ answers "no" to "is there a flight from Paris to Oslo?", although nothing in it says so.
- Negation as failure in [logic programming](/logic-programming/): a query $\mathit{not}\ p$ succeeds when every attempt to prove $p$ fails finitely, as in [SLDNF resolution](/sldnf-resolution/). This is a procedural form of the closed world assumption.
- The Horn database $\{P(a), \forall x\,(P(x) \to Q(x))\}$ with the constants $a$ and $b$: it entails $P(a)$ and $Q(a)$, so $\mathrm{CWA}$ adds $\lnot P(b)$ and $\lnot Q(b)$, and the result is consistent.

### Non-examples

- A goal. The goal $\{\mathit{on}(A, B), \mathit{on}(B, C)\}$ does not say that $C$ is not on the table; any state with the two facts is a goal state.
- [Conformant planning](/conformant-planning/) and other planning with incomplete knowledge. The initial state is a set of possible states, or a set of known literals in which a fact can be true, false or unknown. This is the open world assumption.
- The disjunctive database $\{P(a) \lor P(b)\}$ above. The closed world assumption makes it inconsistent, so it is not a correct reading of that database.
- A web page that does not mention a fact. On the open web the absence of a statement says nothing, and languages for it, such as description logics, use the open world assumption.

## Related definitions

- Open world assumption: a fact that is not stated is unknown. A state is then a set of literals, or a set of possible worlds.
- Unique names assumption: distinct constants denote distinct objects. PDDL makes it, so `(not (= a b))` holds for distinct objects `a` and `b`.
- Domain closure assumption: the only objects are those that the constants name. PDDL makes it too, and this is why a schema has finitely many ground instances.
- Circumscription (McCarthy 1980): a logical form of the same idea, which keeps only the models in which chosen predicates are true of as few objects as possible.
- The STRIPS assumption: an action changes only the facts in its add and delete lists. It is a closed world assumption about change, and it is how STRIPS answers the [frame problem](/frame-problem/).
- Completion: Clark's completion of a logic program reads each set of rules for a predicate as "if and only if", which justifies negation as failure for a class of programs.

## References
