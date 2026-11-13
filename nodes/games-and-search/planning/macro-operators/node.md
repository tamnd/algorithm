---
tag: 8C2C7V
kind: technique
slug: macro-operators
name: Macro-operators
aliases:
- macro actions
- macros
area: games-and-search/planning
level: advanced
summary: Precomputed action sequences added as single operators to shorten plans and search.
prereqs: [strips, forward-state-space-search, effective-branching-factor]
see_also: [rubiks-cube-problem, sokoban-problem, sliding-tile-puzzle, iterative-deepening-a-star, enforced-hill-climbing, fast-forward-planner, htn-planning, means-ends-analysis]
sources:
  - paper: doi:10.1016/0004-3702(72)90051-3
    title: "Richard E. Fikes, Peter E. Hart and Nils J. Nilsson, Learning and executing generalized robot plans, Artificial Intelligence 3 (1972)"
    locator: pp. 251 to 288 (MACROPS, plans of STRIPS stored as triangle tables and reused as single operators; general locator)
  - paper: doi:10.1016/0004-3702(85)90012-8
    title: "Richard E. Korf, Macro-operators: a weak method for learning, Artificial Intelligence 26(1) (1985)"
    locator: pp. 35 to 77 (macro tables, serial decomposability, and puzzles solved without search; general locator)
  - paper: doi:10.1016/0004-3702(87)90051-8
    title: "Richard E. Korf, Planning as search: a quantitative approach, Artificial Intelligence 33(1) (1987)"
    locator: pp. 65 to 88 (how subgoals, macro-operators and abstraction reduce the search effort; general locator)
  - paper: doi:10.1016/0004-3702(90)90059-9
    title: "Steven Minton, Quantitative results concerning the utility of explanation-based learning, Artificial Intelligence 42(2-3) (1990)"
    locator: pp. 363 to 391 (the utility problem of learned knowledge; general locator)
  - paper: doi:10.1613/jair.1696
    title: "Adi Botea, Markus Enzenberger, Martin Müller and Jonathan Schaeffer, Macro-FF: improving AI planning with automatically learned macro-operators, Journal of Artificial Intelligence Research 24 (2005)"
    locator: pp. 581 to 621 (macro-operators learned from solved training tasks and added to the domain; general locator)
  - paper: doi:10.1613/jair.2077
    title: "Andrew Coles and Amanda Smith, Marvin: a heuristic search planner with online macro-action learning, Journal of Artificial Intelligence Research 28 (2007)"
    locator: pp. 119 to 156 (action sequences that escape plateaus, stored and reused during the search; general locator)
---

A macro-operator is a sequence of actions that a planner treats as one operator. For [STRIPS](/strips/) actions, the sequence composes into one action with its own preconditions, add list and delete list, and the composed action has the same effect as the sequence in every state where the sequence can run. Added to the actions of a task, macro-operators let a search reach deep states in few steps: the solution depth goes down and the [branching factor](/effective-branching-factor/) goes up. The states that can be reached do not change, and a plan found with macro-operators expands to a plan of primitive actions. The cost is that the expanded plan can be longer than an optimal plan, and that each new operator must be tested in every state. Fikes, Hart and Nilsson (1972) stored the plans of STRIPS as MACROPS, and Korf (1985) built tables of macro-operators that solve puzzles with no search at all.

## In plain words

Some short series of moves come up again and again. To move a parcel, you load it, drive and unload it. Give such a series a name, and let the planner use it as if it were one move.

Then the planner needs fewer moves to reach the goal, so it has fewer levels to look through. But it has more choices at each level, because the old moves are still there and the new ones are added. The trade pays off when the new moves are few and useful. It does not pay off when there are many of them and most lead nowhere.

The plan that comes out can always be written back as plain moves, and it is always correct. It is not always the shortest one.

## When it applies

- The task is a [STRIPS](/strips/) task, or any task with deterministic actions whose sequences can be composed.
- The search has no duplicate detection, such as [iterative deepening](/iterative-deepening-a-star/), and the cost grows with the solution depth. Each level saved cuts the tree by a factor of about the branching factor.
- A heuristic search gets stuck on plateaus, where many steps give no progress in the heuristic, as in [enforced hill-climbing](/enforced-hill-climbing/). A macro-operator crosses such a region in one step.
- Many tasks of the same domain must be solved, so that the cost of finding good macro-operators is paid once.
- The problem is serially decomposable: the goal can be reached one subgoal at a time, and fixed sequences can achieve the next subgoal while they restore the earlier ones. Then a table of macro-operators replaces the search, as in the [Rubik's cube](/rubiks-cube-problem/) and the [sliding tile puzzle](/sliding-tile-puzzle/).

## The template

```pseudo id=main
MACRO-SEARCH(A, I, G)
L1  S ← a set of action sequences   ▷ hole: the source of the sequences
L2  M ← the macro-operator of each sequence of S that some state allows
L3  π ← SEARCH(A ∪ M, I, G)   ▷ hole: the search algorithm
L4  return π with each macro-operator replaced by its sequence, recursively
```

**Line L2: composition.** For two actions $a$ and $b$ with disjoint add and delete lists, the sequence $a, b$ can run in some state exactly when $\mathrm{del}(a) \cap \mathrm{pre}(b) = \emptyset$. Then it composes into the action $ab$ with

$$\mathrm{pre}(ab) = \mathrm{pre}(a) \cup (\mathrm{pre}(b) \setminus \mathrm{add}(a)), \qquad \mathrm{add}(ab) = (\mathrm{add}(a) \setminus \mathrm{del}(b)) \cup \mathrm{add}(b),$$

$$\mathrm{del}(ab) = (\mathrm{del}(a) \cup \mathrm{del}(b)) \setminus \mathrm{add}(ab).$$

A longer sequence composes from the left, one action at a time, and is dropped if some step fails the test.

**Why the composition is exact.** Let $s$ be a state. The action $a$ can run in $s$ when $\mathrm{pre}(a) \subseteq s$, and gives $s_a = (s \setminus \mathrm{del}(a)) \cup \mathrm{add}(a)$. The action $b$ can then run when $\mathrm{pre}(b) \subseteq s_a$. A fact of $\mathrm{pre}(b)$ in $\mathrm{add}(a)$ is in $s_a$. A fact of $\mathrm{pre}(b)$ outside $\mathrm{add}(a)$ is in $s_a$ exactly when it is in $s$, because it is not in $\mathrm{del}(a)$. So $a, b$ can run in $s$ exactly when $\mathrm{pre}(ab) \subseteq s$. The state after $b$ is

$$(s \setminus (\mathrm{del}(a) \cup \mathrm{del}(b))) \cup (\mathrm{add}(a) \setminus \mathrm{del}(b)) \cup \mathrm{add}(b),$$

and a fact of $\mathrm{del}(a) \cup \mathrm{del}(b)$ that is also in $\mathrm{add}(ab)$ is added back anyway, so this is $(s \setminus \mathrm{del}(ab)) \cup \mathrm{add}(ab)$. If $\mathrm{del}(a) \cap \mathrm{pre}(b)$ is not empty, then $b$ needs a fact that $a$ has just deleted, and no state allows the sequence.

**Line L3: what the search sees.** Each macro-operator moves between states that the primitive actions connect, so the set of reachable states is the same with or without $M$. Each operator of $A$ is still present, so a search that is complete stays complete, and the depth of a shortest solution can only go down. The number of operators that apply in a state goes up by the number of macro-operators that apply there.

**Line L4: expansion.** A step by a macro-operator is replaced by its sequence, and the composition is exact, so the expanded plan is valid. A step can be a macro-operator of macro-operators, so the expansion is recursive.

**Cost.** Composing a sequence of $k$ actions costs $O(k n)$ for $n$ facts. Each macro-operator adds one applicability test per generated state. With $b$ operators and solution depth $d$, a search without duplicate detection generates about $b^d$ nodes. With $b'$ operators and depth $d'$, it generates about $b'^{d'}$, which is smaller when the saved depth outweighs the larger branching factor.

## Classic examples

### Carry a parcel

A truck is at $l_1$ with parcels $p_1$ and $p_2$, and the goal is both parcels at $l_2$. The primitive actions are $\mathit{load}$, $\mathit{drive}$ and $\mathit{unload}$. Add the macro-operator $\mathit{carry}(p, l, l')$, the sequence $\mathit{load}(p, l)$, $\mathit{drive}(l, l')$, $\mathit{unload}(p, l')$, for each parcel and direction. Composition gives $\mathit{carry}(p_1, l_1, l_2)$ the preconditions $\mathit{at}(p_1, l_1)$ and $\mathit{truck}(l_1)$, the add list $\mathit{at}(p_1, l_2)$ and $\mathit{truck}(l_2)$, and the delete list $\mathit{at}(p_1, l_1)$, $\mathit{in}(p_1)$ and $\mathit{truck}(l_1)$. The fact $\mathit{in}(p_1)$ is not a precondition and is not added, because $\mathit{load}$ adds it and $\mathit{unload}$ deletes it.

Measured on the code of this page:

| | operators | mean branching factor | solution depth | nodes of iterative deepening |
|---|---|---|---|---|
| 2 parcels, primitive actions | 10 | 2.33 | 5 | 218 |
| 2 parcels, with $\mathit{carry}$ | 14 | 3.00 | 3 | 53 |
| 3 parcels, primitive actions | 14 | | 7 | 6434 |
| 3 parcels, with $\mathit{carry}$ | 20 | | 5 | 1449 |

The mean branching factor is over the 18 reachable states of the task with 2 parcels. The search with $\mathit{carry}$ finds the plan $\mathit{load}(p_1, l_1)$, $\mathit{carry}(p_2, l_1, l_2)$, $\mathit{unload}(p_1, l_2)$, which expands to the optimal plan of 5 actions. A breadth-first search with duplicate detection gains nothing here: it visits all 18 states in both cases, because the operators do not add states.

### A macro table for the 2 by 3 sliding tile puzzle

Korf (1985) solves a puzzle one piece at a time in a fixed order. The table has a column for each piece and a row for each location where the piece can be. Entry $(i, j)$ is a sequence of moves that brings piece $i$ from location $j$ to its home, and leaves the pieces before $i$ at their homes. During the sequence, the moves may disturb the earlier pieces, but at the end they are all back. The solver looks up one entry per piece and needs no search.

For the puzzle with 2 rows and 3 columns, take the blank first and then the tiles 1, 2 and 3. Tiles 4 and 5 are then home by parity. With the blank and the earlier tiles at home, the effect of a move sequence does not depend on the other tiles, so one breadth-first search over the 360 reachable states gives a shortest sequence for each entry. Measured on the code of this page, the table has 14 nonempty entries:

| column | entries | longest |
|---|---|---|
| blank | 5 | 3 |
| tile 1 | 4 | 10 |
| tile 2 | 3 | 14 |
| tile 3 | 2 | 12 |

The table solves all 360 states. The longest solution has 39 moves, the sum of the longest entry of each column, and the mean is 21.0 moves. The optimal solutions have at most 21 moves and a mean of 12.6 moves. So the table gives up length for a solver with no search.

### Human methods for the Rubik's cube

The layer by layer methods for the [Rubik's cube](/rubiks-cube-problem/) are macro tables in all but name. Each memorized sequence moves a few pieces into place and returns all the other solved pieces. A person learns a small set of sequences and solves any cube, with solutions much longer than the shortest.

### Sokoban

In the [Sokoban](/sokoban-problem/) solver of Junghanns and Schaeffer, a box in a tunnel is pushed to the end of the tunnel in one step, and a box near the goal area is pushed straight to a goal. These macro moves cut the depth of the search. In a tunnel, the positions between the pushes give no useful new options, so little is lost.

## Variations

- **Generalized plans.** STRIPS stored each plan as a triangle table, generalized it by replacing constants with parameters, and reused any part of it as a MACROP (Fikes, Hart and Nilsson 1972). The same table let the executor find the latest part of the plan that still applied and continue from there, an early form of [execution monitoring](/execution-monitoring/).
- **Macro tables.** Korf (1985) learns a full table by search and then solves without search. It needs serial decomposability, and it gives a bound on the solution length but not short solutions.
- **Learned from training tasks.** Macro-FF (Botea, Enzenberger, Müller and Schaeffer 2005) takes sequences from the plans of small tasks of a domain, ranks them by how much they help, and adds the best ones to the domain for larger tasks.
- **Learned during the search.** Marvin (Coles and Smith 2007) records the action sequences that its hill climbing used to escape a plateau and reuses them later in the same search.
- **Parameterized operators.** A macro-operator can be built from lifted [action schemas](/action-schema/), so that one schema covers many ground sequences. Grounding then multiplies the number of operators.
- **Tasks that contain sequences.** [HTN planning](/htn-planning/) goes further: methods state how compound tasks break down into sequences, and the planner uses only those.

## Pitfalls

- **Too many macro-operators.** Each one adds a test in every state and raises the branching factor. Minton (1990) showed that learned knowledge can slow a solver down when the cost to match it outweighs what it saves. This is the utility problem. Keep few macro-operators, and keep the useful ones.
- **Expecting gains with duplicate detection.** A breadth-first search over a small state space visits the same states with or without macro-operators, as in the carry example. The gain is in the depth of tree searches and in the crossing of plateaus.
- **Losing optimality.** The expanded plan can be longer than optimal, both in random tasks and in macro tables. A step count that treats a macro-operator as one step is not the plan length. For optimal plans, give each macro-operator the total cost of its sequence, and use it with an algorithm that minimizes cost.
- **A sequence that never runs.** If an action deletes a precondition of a later action and no action between them adds it back, no state allows the sequence. Drop it at composition time.
- **Add and delete of the same fact.** The formulas assume that each action has disjoint add and delete lists. A composed operator must keep that property, or its semantics depend on the order in which deletes and adds are applied.
- **Heuristics and macro-operators.** An admissible heuristic for unit costs is not admissible when a macro-operator of length $k$ counts as one step. Count it as $k$.

## Exercises

1. Show that composition is associative: the macro-operators of $(ab)c$ and $a(bc)$ have the same preconditions, add list and delete list.
2. Give a task where breadth-first search with a macro-operator returns a plan whose expansion is longer than the optimal plan.
3. In a macro table, why is the longest solution at most the sum of the longest entry of each column? When is it equal?

## References
