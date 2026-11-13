---
tag: HH14ZB
kind: definition
slug: action-schema
name: Action schema
aliases:
- operator schema
- lifted action
- planning operator
area: games-and-search/planning
level: intro
summary: Parameterized action with precondition and effects, instantiated over objects.
prereqs: [strips]
see_also: [grounding, pddl, substitution, classical-planning, blocks-world, macro-operators]
sources:
  - paper: doi:10.1016/0004-3702(71)90010-5
    title: "Richard E. Fikes and Nils J. Nilsson, STRIPS: A new approach to the application of theorem proving to problem solving, Artificial Intelligence 2(3-4) (1971)"
    locator: pp. 189 to 208 (operators with parameters, instantiated during the search)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 2, Section 2.3 (classical representation, planning operators and their ground instances)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.1 (action schemas)
  - paper: "Drew McDermott and others, PDDL, The Planning Domain Definition Language, Version 1.2, Technical Report CVC TR-98-003/DCS TR-1165, Yale Center for Computational Vision and Control, 1998"
    title: McDermott et al. 1998
    locator: the sections on domains and on actions (general locator)
---

An action schema is an action with parameters: a name, a list of variables, and a precondition, an add list and a delete list written with those variables. Each way to replace the variables by objects gives one ground [STRIPS](/strips/) action. One schema thus describes a whole family of actions, such as "move block $b$ from $x$ to $y$" for every choice of $b$, $x$ and $y$. Schemas are the `:action` blocks of [PDDL](/pddl/), and [grounding](/grounding/) turns them into ground actions.

## Definition

Fix a set of predicate symbols, each with an arity, and a set of objects (constants). An atom is a predicate applied to terms, where a term is a variable or an object; a ground atom has no variables.

An action schema $o$ consists of

- a name and a parameter list $x_1, \ldots, x_k$ of distinct variables, each with an optional type;
- a precondition $\mathit{pre}(o)$, a set of atoms;
- an add list $\mathit{add}(o)$ and a delete list $\mathit{del}(o)$, sets of atoms;
- optionally, a set of constraints $x_i \ne x_j$ (in PDDL, `(not (= ?x ?y))` under the `:equality` requirement).

Every variable that occurs in the precondition or in the effects must be one of $x_1, \ldots, x_k$.

A [substitution](/substitution/) $\sigma$ that maps each $x_i$ to an object of its type, and that satisfies the constraints, gives the ground action $o\sigma$: its name is $o(\sigma(x_1), \ldots, \sigma(x_k))$, and its three sets are $\mathit{pre}(o)\sigma$, $\mathit{add}(o)\sigma$ and $\mathit{del}(o)\sigma$. The ground action is applicable and has a result exactly as a STRIPS action: in state $s$ it needs $\mathit{pre}(o)\sigma \subseteq s$ and gives $(s \setminus \mathit{del}(o)\sigma) \cup \mathit{add}(o)\sigma$.

With $o_t$ objects of the type of each parameter, a schema has at most $\prod_i o_{t(x_i)}$ instances, and at most $o^k$ when all $o$ objects are allowed for every parameter. The number $k$ is the arity of the schema. A planning domain is a set of predicates and a set of schemas; a problem adds the objects, the initial state and the goal. So the same domain describes tasks of every size.

## Examples and non-examples

### Examples

- The move schema of the [blocks world](/blocks-world/):

  $\mathit{move}(b, x, y)$: $\mathit{pre} = \{\mathit{on}(b, x), \mathit{clear}(b), \mathit{clear}(y)\}$, $\mathit{add} = \{\mathit{on}(b, y), \mathit{clear}(x)\}$, $\mathit{del} = \{\mathit{on}(b, x), \mathit{clear}(y)\}$, with $b \ne x$, $b \ne y$, $x \ne y$.

  The substitution $b \mapsto A$, $x \mapsto C$, $y \mapsto B$ gives the ground action $\mathit{move}(A, C, B)$, with precondition $\{\mathit{on}(A, C), \mathit{clear}(A), \mathit{clear}(B)\}$. The table is not a block: it is always clear, so moves to and from the table need two more schemas. With $n$ blocks, the three schemas have $n(n-1)(n-2)$, $n(n-1)$ and $n(n-1)$ instances, a total of $n^2(n-1)$; for $n = 3$ that is 18.

- The four schemas $\mathit{pickup}(x)$, $\mathit{putdown}(x)$, $\mathit{stack}(x, y)$ and $\mathit{unstack}(x, y)$ of the four-operator blocks world. With the constraint $x \ne y$ they have $n + n + n(n-1) + n(n-1) = 2n^2$ instances. Without it, as in the competition version of the domain, $\mathit{stack}$ and $\mathit{unstack}$ have $n^2$ instances each, and three blocks give $3 + 3 + 9 + 9 = 24$ ground actions. The 6 extra actions, such as $\mathit{stack}(A, A)$, can never be applied in a reachable state, because $\mathit{stack}(A, A)$ needs $\mathit{holding}(A)$ and $\mathit{clear}(A)$, which never hold together. They are harmless but cost time.

- A typed schema from a logistics domain: $\mathit{drive}(t : \mathit{truck}, a : \mathit{location}, b : \mathit{location})$ with $\mathit{pre} = \{\mathit{at}(t, a), \mathit{road}(a, b)\}$, $\mathit{add} = \{\mathit{at}(t, b)\}$, $\mathit{del} = \{\mathit{at}(t, a)\}$. Types cut the instances to $|T| \cdot |L|^2$, and a reachable instance must also have $\mathit{road}(a, b)$ in the initial state, since no schema changes $\mathit{road}$.

- A ground action is a schema with $k = 0$. A STRIPS task is the special case of a domain in which every schema has no parameters.

### Non-examples

- A schema with the effect $\mathit{on}(b, z)$, where $z$ is not a parameter. The effect does not say which fact becomes true, so the schema has no meaning. A planner rejects it.
- A schema whose effect depends on the state, such as "move the briefcase, and every object in it moves too". This needs a quantified [conditional effect](/conditional-effects/), which is not part of the STRIPS fragment.
- A schema with a precondition $\lnot \mathit{on}(b, x)$. A negative precondition is outside plain STRIPS, although PDDL allows it under `:negative-preconditions`.
- The fact $\mathit{on}(A, B)$ alone. It is a ground atom, part of a state, not an action.

## Related definitions

- Ground action: the result $o\sigma$ of a schema and a substitution. A planner that searches over ground actions is a grounded planner; a lifted planner keeps the variables and unifies them during the search, as the original STRIPS system of Fikes and Nilsson did.
- [Grounding](/grounding/): the process that computes all the useful instances of all schemas.
- Static predicate: a predicate that no schema adds or deletes, such as $\mathit{road}$ above. Its atoms are fixed by the initial state, so a grounder can drop each instance whose static preconditions are false.
- Partially instantiated action: a schema with some variables bound. Backward search by [goal regression](/goal-regression/) and plan-space planners such as [POP](/pop-partial-order-planning/) use them to postpone the choice of objects.
- [Macro-operators](/macro-operators/): schemas built by composing a sequence of schemas.
- [Horn clauses](/horn-clause/) and [Datalog](/datalog/) rules: a schema with its delete list removed is a rule "if the precondition holds, the add atoms hold", which is how grounders compute the reachable instances.
- [Herbrand universe](/herbrand-universe/): the set of ground terms over which the variables range; in planning it is the finite set of objects.

## References
