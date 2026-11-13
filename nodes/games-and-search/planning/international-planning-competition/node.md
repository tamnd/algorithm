---
tag: WKN77P
kind: concept
slug: international-planning-competition
name: International Planning Competition
aliases:
- IPC
area: games-and-search/planning
level: intro
summary: A recurring competition, first held at AIPS-98, that runs planners on shared benchmark tasks in PDDL, with tracks for classical, probabilistic and learning planning.
prereqs: [classical-planning, pddl]
see_also: [optimal-planning, hsp-planner, fast-forward-planner, satplan, graphplan, blocks-world, temporal-planning, pomdp-planning]
sources:
  - paper: doi:10.1609/aimag.v21i2.1506
    title: "Drew McDermott, The 1998 AI Planning Systems Competition, AI Magazine 21(2) (2000)"
    locator: the first competition at AIPS-98, its STRIPS and ADL tracks, and the first version of PDDL (general locator)
  - paper: doi:10.1609/aimag.v33i1.2392
    title: "Amanda Coles, Andrew Coles, Angel García Olaya, Sergio Jiménez, Carlos Linares López, Scott Sanner and Sungwook Yoon, A survey of the Seventh International Planning Competition, AI Magazine 33(1) (2012)"
    locator: the history of the competition since 1998 and the deterministic, learning and uncertainty tracks of 2011 (general locator)
  - paper: doi:10.1002/aaai.12169
    title: "Ayal Taitler and others, The 2023 International Planning Competition, AI Magazine (2024)"
    locator: the five tracks of 2023, classical, numeric, HTN, learning, and probabilistic and reinforcement learning (general locator)
---

The International Planning Competition (IPC) is a series of events in which automated planners are run on a common set of benchmark tasks, under the same time and memory limits, and their results are compared. The first one was held at the AIPS conference in 1998, organized by Drew McDermott, and it is also where the planning language [PDDL](/pddl/) was introduced. Later editions were held with the AIPS conference and, after it merged into ICAPS, with ICAPS. The competition is not held at a fixed interval: there were editions every two years from 1998 to 2008, then in 2011, 2014, 2018 and 2023. Its benchmark domains, such as the [blocks world](/blocks-world/), logistics and many others, are the standard test set of [classical planning](/classical-planning/) research.

## In plain words

Many groups write programs that make plans. To see which ideas work, they meet and run all the programs on the same set of puzzles, with the same computers and the same time limits. Each program gets a score for how many puzzles it solves and how good its plans are.

The puzzles are written in one shared language, so every program can read them. After each meeting, the puzzles are made public, and other people use them to test new programs for years.

## The idea

**A shared language.** Before 1998, each planner had its own input format, and results from different papers were hard to compare. PDDL gave one format for the domain, which holds the action schemas, and for the problem, which holds the objects, the initial state and the goal. Later editions extended the language with numeric fluents and durative actions (PDDL2.1, 2002), derived predicates and timed initial literals (PDDL2.2, 2004), preferences and trajectory constraints (PDDL3, 2006), action costs (PDDL 3.1, 2008), and probabilistic effects (PPDDL, 2004). Since 2011 the probabilistic tracks have also used RDDL.

**Tracks.** Each edition has several tracks, and each track fixes the kind of planning and the measure.

- *Deterministic or classical tracks*, held since 1998, for fully observable tasks with deterministic actions. They are split by goal: optimal planners must return plans of minimum cost (see [optimal planning](/optimal-planning/)), satisficing planners any plan of low cost, agile planners any plan fast, and some editions had tracks for multicore planners, for temporal and numeric planning (see [temporal planning](/temporal-planning/)), and for planners with domain knowledge written by hand (2000 and 2002).
- *Probabilistic or uncertainty tracks*, held since 2004, for actions with random outcomes, and in later editions also partial observability (see [POMDP planning](/pomdp-planning/)) and nondeterministic actions.
- *Learning tracks*, held in 2008, 2011, 2014 and 2023, where planners may first train on small tasks of a domain and are then tested on larger ones.
- *Other tracks*, for example the HTN track and the numeric track of 2023 (see [HTN planning](/htn-planning/)).

**Measures.** The results are measurements on one benchmark set with one set of limits, not proofs. A typical score counts the solved tasks, and for satisficing planners weights each solved task by the ratio of the best known plan cost to the plan cost found. Optimal planners are compared by the number of tasks solved, since all their plans have the same cost. A different set of domains, limits or hardware can change the order of the planners.

**Benchmarks.** The organizers of each edition choose new domains, often from applications or from puzzles, and generate tasks of growing size. The tasks of all editions are kept public. Because of this, a new planner is usually evaluated on the IPC domains, and the results of different papers can be compared.

## Examples

- **1998.** The first competition at AIPS-98 had a STRIPS track and an ADL track, with domains that included logistics and the gripper domain. The [HSP planner](/hsp-planner/) took part in it, together with planners built on [Graphplan](/graphplan/) and on SAT encodings in the line of [SATPLAN](/satplan/).
- **2000 and 2002.** The 2000 edition added a track for planners with hand-coded domain knowledge. The 2002 edition introduced PDDL2.1 and with it numeric and temporal domains. The [FF planner](/fast-forward-planner/) and other heuristic search planners took part in these editions.
- **2004.** The first probabilistic track, with PPDDL as its input language.
- **2008.** The first learning track, and the deterministic track used action costs, so cost-optimal and satisficing planners were compared by cost and not only by length.
- **2023.** Five tracks: classical, numeric, HTN, learning, and probabilistic and reinforcement learning.

## Where it is used

- **Evaluation of planners.** Most papers in classical planning report results on IPC domains, often on all optimal or all satisficing tasks of several editions.
- **Benchmarks for heuristics.** Heuristics such as [h-max](/h-max-heuristic/), [h-add](/h-add-heuristic/) and the [landmark heuristics](/landmark-heuristic/) are compared by the number of states expanded and the tasks solved on IPC tasks.
- **Development of PDDL.** New language features were defined for the competitions and became the standard input of planners.
- **Planner portfolios.** Because no single planner is best on every domain, the results led to portfolios that choose or combine planners per task.

## References
