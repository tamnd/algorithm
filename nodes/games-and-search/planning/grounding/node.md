---
tag: E2ANZJ
kind: technique
slug: grounding
name: Grounding
aliases:
- action instantiation
- operator instantiation
area: games-and-search/planning
level: intro
summary: Instantiating lifted action schemas with all objects to obtain propositional actions.
prereqs: [action-schema]
see_also: [strips, pddl, sas-plus, datalog, relational-join, semi-naive-evaluation, delete-relaxation, combinatorial-explosion]
sources:
  - paper: doi:10.1016/j.artint.2008.10.013
    title: "Malte Helmert, Concise finite-domain representations for PDDL planning tasks, Artificial Intelligence 173(5-6) (2009)"
    locator: Section 6 (grounding; 6.1.2 static predicates, 6.1.3 relaxed reachability, 6.2 grounding as a Datalog program)
  - paper: doi:10.1613/jair.1705
    title: "Malte Helmert, The Fast Downward planning system, Journal of Artificial Intelligence Research 26 (2006)"
    locator: pp. 191 to 246 (the translator component, which grounds the task before the search)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 2, Section 2.3 (operators and their ground instances, actions)
---

Grounding turns a lifted planning task, written with [action schemas](/action-schema/), into a ground [STRIPS](/strips/) task, by replacing the parameters of each schema by objects in every useful way. A naive grounder tries every tuple of objects, which gives up to $o^k$ actions for a schema with $k$ parameters and $o$ objects. Good grounders build only the tuples that can matter: they join the precondition atoms of a schema with the facts that can become true, which is a [Datalog](/datalog/) computation. Most planners ground first and search the ground task afterwards.

## In plain words

A planning domain says things like "a truck can drive from one place to another if there is a road". To search for a plan, most planners need every concrete action: truck 1 drives from Paris to Lyon, truck 2 drives from Lyon to Nice, and so on. Grounding makes this list. The simple way is to try every truck with every pair of places, but most of these pairs have no road, so the actions are useless. A better way starts from the roads that exist and builds only the drives along them. The best way also skips actions that can never become possible from the start state.

## When it applies

- The task is lifted: a domain of schemas, a finite set of objects, an initial state and a goal, as in [PDDL](/pddl/).
- The planner needs ground actions: forward search with most heuristics, [Graphplan](/graphplan/), [SATPLAN](/satplan/), and the translation into [SAS+](/sas-plus/).
- The number of useful instances is manageable. For schemas of high arity over many objects, even the useful instances can be too many, and lifted planning (search over partially bound schemas) is the alternative.

## The template

```pseudo id=main
GROUND(D, O, I)                          ▷ D: schemas; O: typed objects; I: initial state
L1  S ← the predicates that no schema of D adds or deletes   ▷ static predicates
L2  A ← ∅
L3  for each schema o in D do
L4      B ← { the empty substitution }
L5      for each atom p of pre(o) with a predicate in S do    ▷ hole: the order of the joins
L6          B ← { σ ∪ τ : σ ∈ B, τ maps the variables of p so that pσ τ ∈ I, types agree }
L7      for each σ in B do
L8          for each choice of typed objects for the variables that σ leaves free do
L9              extend σ by the choice
L10             if σ satisfies the constraints x ≠ y of o then
L11                 A ← A ∪ { oσ }          ▷ hole: keep or drop the static atoms of pre(oσ)
L12 return A

GROUND-REACHABLE(D, O, I)               ▷ optional second pass
L13 A ← GROUND(D, O, I); R ← I; K ← ∅
L14 repeat
L15     for each a in A \ K with pre(a) ⊆ R do
L16         K ← K ∪ { a }; R ← R ∪ add(a)     ▷ deletes are ignored
L17 until no action enters K
L18 return K
```

**The holes.** The join order of line L5 decides the size of the intermediate set $B$; put first the atoms that bind the most variables with the fewest matches. Line L11 may drop the static atoms from the precondition, since they hold in every reachable state. The second pass is optional: it costs one more fixpoint, and it removes the actions that can never be applied.

**Why GROUND is exact.** Let $\mathit{brute}$ be the set of all typed tuples that satisfy the inequality constraints. A static atom has the same truth value in every reachable state as in $I$, because no action adds or deletes it. So an instance with a static precondition atom not in $I$ is never applicable, and dropping it changes no plan. Lines L5 and L6 keep exactly the substitutions on the static variables whose static atoms are in $I$, and lines L8 to L11 extend them in every typed way. So $\mathrm{GROUND}$ returns exactly $\mathit{brute}$ minus the tuples with a false static precondition, and builds no tuple that a static atom rules out.

**Why GROUND-REACHABLE keeps every useful action.** Let $s_0 = I, s_1, \ldots$ be the states along any action sequence. By induction, $s_i \subseteq R$ at the end of the loop: $s_0 = I \subseteq R$, and if $s_{i-1} \subseteq R$ and $a_i$ is applicable in $s_{i-1}$, then $\mathit{pre}(a_i) \subseteq R$, so $a_i$ enters $K$ and $\mathit{add}(a_i) \subseteq R$, which gives $s_i \subseteq (s_{i-1} \setminus \mathit{del}) \cup \mathit{add} \subseteq R$. So every action that is applicable in a reachable state is in $K$. The converse fails: $R$ is the set of facts reachable when deletes are ignored, the [delete relaxation](/delete-relaxation/), and some actions in $K$ can still be useless.

**Cost.** The brute force loop takes time proportional to $\sum_o \prod_i |O_{t(x_i)}|$ times the size of a schema. The join takes time proportional to the sizes of the intermediate sets $B$ plus the output. The fixpoint takes $O(|A| \cdot |F|)$ set operations per round and at most $|A| + 1$ rounds, since each round but the last adds an action; a [semi-naive](/semi-naive-evaluation/) evaluation that only retries actions with a new precondition fact makes it close to linear in the total size.

## Classic examples

### Logistics with static roads

The schemas are $\mathit{drive}(t, a, b)$ with precondition $\mathit{at}(t, a)$ and $\mathit{road}(a, b)$, $\mathit{load}(p, t, l)$ and $\mathit{unload}(p, t, l)$. No schema changes $\mathit{road}$, so it is static. Take 2 trucks, 3 packages and 4 locations on a ring with roads in both directions (8 directed roads).

- Every typed tuple: $\mathit{drive}$ has $2 \cdot 4 \cdot 4 = 32$, and $\mathit{load}$ and $\mathit{unload}$ have $3 \cdot 2 \cdot 4 = 24$ each, a total of 80.
- After the static test: $\mathit{drive}$ keeps $2 \cdot 8 = 16$, one for each truck and road, and the other two schemas have no static atom, so 64 remain. The join builds exactly these 64 and never builds the 16 drives without a road.

In general the join gives $|T| \cdot |\mathit{roads}| + 2 |P| |T| |L|$ actions.

### Relaxed reachability

Take 2 trucks, 2 packages, 4 locations, and roads only between $l_1$ and $l_2$ and between $l_3$ and $l_4$. Truck $t_1$ and package $p_1$ are at $l_1$, truck $t_2$ is at $l_3$ and package $p_2$ is at $l_4$. The join gives $2 \cdot 4 + 2 \cdot (2 \cdot 2 \cdot 4) = 40$ actions. The fixpoint keeps 12: the 4 drives along the roads from the trucks' sides, $t_1$ loading and unloading $p_1$ at $l_1$ and $l_2$, and $t_2$ loading and unloading $p_2$ at $l_3$ and $l_4$. These 12 are exactly the actions that are applicable in some reachable state; here the relaxation loses nothing.

### The move domain

The three move schemas of the [blocks world](/blocks-world/), with the constraints that all parameters differ, ground to $n(n-1)(n-2) + 2n(n-1) = n^2(n-1)$ actions for $n$ blocks: 18 for 3 blocks and 100 for 5. No predicate is static, so the join does nothing here and the inequality test does all the filtering.

## Variations

- Grounding as Datalog (Helmert 2009). Each schema becomes a rule whose head is an applicability atom for the schema and whose body is the precondition, and each add effect becomes a rule from the applicability atom to the effect atom. The least model of this program, computed by [Datalog evaluation](/datalog-evaluation/) with [joins](/relational-join/), gives the relaxed reachable facts and actions in one pass. This is the grounder of the Fast Downward translator.
- Grounding with richer languages: negative preconditions, disjunctions and quantifiers are first normalized, for example by moving negations inward and splitting disjunctions into several schemas, and then grounded; quantified effects become one ground effect for each object.
- Pruning by goal relevance: a backward pass from the goal removes actions that cannot contribute to any goal fact.
- Lifted planning: skip grounding and search with partially bound schemas, unifying variables as needed. This avoids the blow-up on schemas of high arity, at the cost of slower successor generation.

## Pitfalls

- Self-application without inequalities. The competition version of the four-operator blocks world has no `:equality`, so the grounder builds $\mathit{stack}(A, A)$ and $\mathit{unstack}(A, A)$: 24 actions for 3 blocks instead of 18. They are never applicable, but a weak grounder keeps them, and a planner that reasons about them, such as an invariant finder, can draw wrong conclusions.
- Forgetting types. Without types, the logistics load schema also builds actions that load one truck into another at a package. They are not applicable, but they multiply the count.
- Static atoms that are not really static. A predicate is static only if no schema adds or deletes it, including through conditional effects. Testing only the plain effects drops useful actions.
- Exponential blow-up. A schema with $k$ parameters and $o$ objects can have $o^k$ instances, and a join cannot help if the preconditions do not restrict the parameters. Large tasks fail in the grounder before the search starts.

## Exercises

1. A domain has the schema $\mathit{fly}(p : \mathit{plane}, a : \mathit{airport}, b : \mathit{airport})$ with the static precondition $\mathit{route}(a, b)$. With 3 planes, 10 airports and 25 directed routes, how many instances does a brute force grounder build, and how many does the join build?
2. Give a task in which GROUND-REACHABLE keeps an action that is not applicable in any reachable state. (Hint: two facts that the relaxation makes true together but that delete each other.)
3. Write the Datalog program for the logistics schemas, and evaluate it by hand on one truck, one package and two locations with one road.
4. Show that with the brute force grounder the number of ground actions can be exponential in the size of the domain description, even for a fixed number of objects.

## References
