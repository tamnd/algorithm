---
tag: 208V6S
kind: technique
slug: two-watched-literals
name: Two watched literals
aliases:
- watched literals
- 2WL
- two-literal watching
area: logic-and-constraints/sat-solving
level: advanced
summary: Watch two literals of each clause, and look at a clause only when one of its watches becomes false. Unit propagation then touches few clauses and needs no work on backtrack.
prereqs: [unit-propagation, clause]
see_also: [unit-clause, cdcl, dpll, clause-database, clause-learning, non-chronological-backtracking, implication-graph, horn-sat]
sources:
  - paper: doi:10.1145/378239.379017
    title: Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang and Sharad Malik, Chaff, engineering an efficient SAT solver, Proceedings of the 38th Design Automation Conference, 2001
    locator: pages 530 to 535 (the two watched literal scheme for Boolean constraint propagation, and why backtracking needs no update of the watches)
  - paper: "Hantao Zhang and Mark E. Stickel, Implementing the Davis-Putnam method, Journal of Automated Reasoning 24(1-2), 2000, pages 277 to 296"
    locator: the head and tail list scheme of SATO, a lazy scheme with two pointers per clause that must be restored on backtrack
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, Lecture Notes in Computer Science 2919, 2004
    locator: pages 502 to 518 (the propagation loop of MiniSat, with the false literal kept at the second position of the clause)
  - paper: "Ian P. Gent, Optimal implementation of watched literals and more general techniques, Journal of Artificial Intelligence Research 48, 2013, pages 231 to 252"
    locator: the cost of the search for a new watch, and the circular search that makes it optimal along a branch
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (lazy data structures for unit propagation and watched literals)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (watched literals in the backtracking and CDCL algorithms)
---

Two watched literals is the data structure scheme for [unit propagation](/unit-propagation/) in which each [clause](/clause/) of length at least 2 marks two of its literals as watched, and the solver looks at the clause only when one of these two becomes false. Then it moves the watch to another literal that is not false, or, if there is none, finds that the clause is unit or false. As long as both watches are not false, the clause cannot be unit or false, so all other clauses can be skipped. The scheme came with Chaff in 2001, and almost every [CDCL](/cdcl/) solver uses it, because it needs no work at all when the solver backtracks.

## In plain words

A rule with many options is in danger only when it is down to one open option. To notice that moment, the solver does not have to watch all the options. It is enough to watch two that are still open. While both watched options are open, the rule has at least two open options and is safe.

When one watched option is ruled out, the solver looks at the rule once. If some other option is still open, it watches that one instead and moves on. If not, the rule is down to its last option, which is forced, or to none, which is a dead end.

When the solver takes back some of its choices, ruled-out options become open again. Watched options can only get safer this way, so the solver leaves the watches where they are and does no work.

## When it applies

- The formula is in [CNF](/conjunctive-normal-form/), and a search assigns literals and undoes them in the reverse order, as [DPLL](/dpll/) and CDCL do. Each undo removes a suffix of the trail.
- The task is to find, after each new assignment, every clause that becomes unit or false. Clauses that are satisfied or that still have two open literals do not matter.
- Clauses are long or many, so that a full occurrence list of each literal would be expensive to visit on every assignment. For binary clauses, solvers keep a separate list of implications with the same meaning.
- The scheme detects units and conflicts lazily. It cannot report how many literals of a clause are false or whether a clause is satisfied, so it does not fit heuristics that need these counts, such as some [lookahead](/lookahead-sat/) heuristics or the pure literal rule.

## The template

Each clause $c$ of length at least 2 stores its literals in an array, and its watches are $c[0]$ and $c[1]$. For each literal $\ell$, the watch list $W[\ell]$ holds the clauses that watch $\ell$. The trail holds the true literals in order, and the literals from position $q$ on are not yet processed.

```pseudo id=main
PROPAGATE(trail, q)                           ▷ returns a false clause, or none
L1  while q < |trail| do
L2      p ← trail[q]; q ← q + 1                 ▷ p is true, so ¬p is false
L3      for each clause c in W[¬p] do           ▷ hole VISIT: test a blocking literal first
L4          if c[0] = ¬p then swap c[0] and c[1] ▷ now c[1] = ¬p
L5          if c[0] is true then continue        ▷ c is satisfied; it keeps watching ¬p
L6          if some k ≥ 2 has c[k] not false then ▷ hole SEARCH: where the search starts
L7              swap c[1] and c[k]; move c from W[¬p] to W[c[1]]; continue
L8          if c[0] is false then return c       ▷ conflict: every literal of c is false
L9          assign c[0] with reason c; append it to the trail ▷ c is unit
L10 return none
```

Backtracking unassigns a suffix of the trail and sets $q$ to the new trail length. It does not touch the watches.

The holes:

- **VISIT.** MiniSat 2.2 stores with each entry of $W[\neg p]$ a blocking literal of the clause. If it is true, the clause is satisfied and line L3 skips it without reading the clause from memory.
- **SEARCH.** MiniSat starts at position 2 each time. Gent (2013) showed that a circular search, which starts where the last search in that clause stopped, makes the total cost of watch moves for a clause linear in its length along one branch of the search.
- **ORDER.** As in [unit propagation](/unit-propagation/), the trail itself is the queue.

**Correctness.** Say that a false literal $w$ is *processed* when $\neg w$ is on the trail before position $q$. The proof is about the invariant:

(I) For every clause $c$ and each of its watches $w$ with other watch $w'$: if $w$ is false and processed, then $w'$ is true and $\mathrm{level}(w') \le \mathrm{level}(w)$.

*Lemma 1 (initialization).* With an empty trail, no literal is false, so (I) holds. When a learned clause is added with $c[0]$ the asserting literal and $c[1]$ a literal of the jump level $b$, and $c[0]$ is assigned at level $b$ at once, the only false watch is $c[1]$ and the other watch is true at level $b = \mathrm{level}(c[1])$.

*Lemma 2 (propagation keeps (I)).* Assume (I) when line L2 is about to run. Processing $p$ makes $\neg p$ processed, and $\neg p$ has the current level $d$, which is the largest level on the trail. Only clauses that watch $\neg p$ can break (I), and the loop of line L3 visits all of them; (I) holds again when the loop ends. For such a clause $c$, the other watch $c[0]$ is not false and processed: if it were, (I) would have required $\neg p$ to be true, but the variable of $p$ was unassigned until $p$ was assigned. Then one of four cases holds. At line L5, $c[0]$ is true with a level at most $d$. At line L7, $c$ no longer watches $\neg p$, and its new watch is not false. At line L9, $c[0]$ becomes true at level $d$. At line L8, the procedure stops with a conflict, and the solver then jumps to a level below $d$, which unassigns $p$ and every literal of level $d$, so all the watches visited or skipped in this call are no longer false.

*Lemma 3 (backtracking keeps (I)).* Backtracking to level $b$ unassigns exactly the literals of level above $b$ and marks the rest processed. Let $w$ be a watch that is false after the backtrack. Its level is at most $b$, so it was false before, and processed, since every literal at a level below the current one was processed before a decision was made. By (I), $w'$ was true with $\mathrm{level}(w') \le \mathrm{level}(w) \le b$, so $w'$ is still true. A watch that became unassigned imposes nothing.

*Theorem (no unit and no conflict is missed).* Suppose that PROPAGATE returns none. Then no clause of length at least 2 is unit or false. *Proof.* When it returns none, $q = |\mathrm{trail}|$, so every false literal is processed. Let $c$ be a clause. If one of its watches is false, then by (I) the other watch is true, and $c$ is satisfied. Otherwise both watches are not false, so $c$ has two literals that are not false, and it is neither unit nor false. $\blacksquare$

*Soundness.* Line L9 runs only when $c[0]$ is unassigned, $c[1] = \neg p$ is false and the search at line L6 found every $c[k]$ with $k \ge 2$ false, so $c$ is unit with $c[0]$. Line L8 runs only when all literals of $c$ are false. So every reported unit and conflict is real.

The level condition in (I) is what lets backtracking do nothing. Without it, a backtrack could unassign the true watch $w'$ while keeping the false watch $w$, and the clause could later become unit with no watch event to report it.

**Cost.** Assigning a literal $p$ costs time proportional to $|W[\neg p]|$ plus the literals read in the searches at line L6. Backtracking costs $O(1)$ per unassigned literal, with no clause work. Watch lists hold exactly two entries per clause, so the space is $O(m)$ beyond the clauses. A clause that watches only literals that stay unassigned is never visited, however many of its other literals become false. In the worst case, watched literals give no better bound than counters per clause, which cost $O(|F|)$ for a full propagation, and with the search from position 2 they can be worse along a branch (exercise 2). The gain is measured: Moskewicz et al. report that propagation takes the largest part of a solver's run time, and that Chaff, with watched literals and VSIDS, was one to two orders of magnitude faster than GRASP and SATO on their benchmarks.

**Example.** Take $C_1 = \{\neg x_1, x_2\}$, $C_2 = \{\neg x_2, x_3\}$, $C_3 = \{\neg x_3, \neg x_1, x_4\}$, $C_4 = \{\neg x_4, x_5, x_6\}$, $C_5 = \{\neg x_2, \neg x_5\}$, $C_6 = \{\neg x_4, \neg x_6\}$, with each clause watching its first two literals. The solver decides $x_1$.

| processed $p$ | clauses in $W[\neg p]$ | event |
|---|---|---|
| $x_1$ | $C_1$ | no other literal is open, $C_1$ is unit, assign $x_2$ |
| $x_1$ | $C_3$ | move the watch from $\neg x_1$ to $x_4$ |
| $x_2$ | $C_2$ | unit, assign $x_3$ |
| $x_2$ | $C_5$ | unit, assign $\neg x_5$ |
| $x_3$ | $C_3$ | watches $\neg x_3$ and $x_4$, no other open literal, unit, assign $x_4$ |
| $\neg x_5$ | $C_4$ | move the watch from $x_5$ to $x_6$ |
| $x_4$ | $C_4$ | unit, assign $x_6$ |
| $x_4$ | $C_6$ | both literals false, conflict |

Here every clause holds at most three literals, so the watches save no visit: the 8 visits match the 8 entries of the occurrence lists of $\neg x_1, \neg x_2, \neg x_3, x_5$ and $\neg x_4$. After the conflict, a backtrack to any level leaves all watches valid, while a counter-based scheme would have updated, and must now undo, one counter for each of these 8 entries. The saving on visits shows with longer clauses: for the clause $\{x_1, \ldots, x_6\}$ watching $x_1$ and $x_2$, the assignments $\neg x_6, \neg x_5, \neg x_4, \neg x_3$ cost no visit, and $\neg x_1$ costs one visit that finds the clause unit with $x_2$. Full occurrence lists would visit the clause five times.

## Classic examples

- **Chaff.** Moskewicz, Madigan, Zhao, Zhang and Malik introduced the scheme in 2001 together with [VSIDS](/vsids/) and first UIP learning.
- **SATO head and tail lists.** Zhang and Stickel's earlier lazy scheme keeps two pointers that move only toward each other, so they must be moved back on backtrack. Watched literals drop the order and with it the restore step.
- **MiniSat.** Eén and Sörensson keep the false watch at position 1 and the other at position 0, as in lines L4 and L5, and use the trail as the propagation queue. This layout is the one in the template and in most current solvers.
- **CDCL with learned clauses.** A learned clause is attached with its asserting literal and a literal of the jump level as watches, as in Lemma 1; the [clause database](/clause-database/) page shows the watch lists next to the clause store.

## Variations

- **Blocking literals.** As in VISIT. The test usually avoids reading the clause from memory, which matters because propagation is limited by memory access.
- **Special binary clauses.** For a clause $\{a, b\}$, both literals are watched forever. Solvers store $b$ directly in the watch list of $\neg a$ and the reverse, so the clause itself is never read.
- **Watching for other constraints.** Cardinality constraints "at least $k$ of these literals" can be watched with $k + 1$ literals, and pseudo-Boolean constraints with enough literals to cover the slack. The same invariant argument applies.
- **Counters instead of watches.** The linear-time [Horn-SAT](/horn-sat/) algorithm of Dowling and Gallier keeps a count of false literals per clause. Counters give exact counts but must be undone on backtrack; watched literals are lazy and do not give counts.
- **Chronological backtracking.** When a literal can sit on the trail at a level below the current one, a true watch can have a higher level than the false watch, which breaks the level condition of (I). The solver must then give each implied literal the largest level of the other literals of its reason, and check the levels when it backtracks.

## Pitfalls

- **Not checking the other watch at line L8.** If the search fails, the other watch may be false but not yet processed. Treating the clause as unit then assigns a literal that is already false, which hides a conflict.
- **Moving the watch to a false literal.** The new watch must be unassigned or true. A false new watch breaks (I) at once, because its complement was already processed.
- **Wrong watches on a new clause.** A learned clause must watch its asserting literal and a literal of the highest remaining level. Watching a literal of a lower level breaks the level condition of (I). After a later backjump below level $b$, the clause can become unit when its unwatched literal of level $b$ turns false again, and no watch event reports it.
- **Iterating over a watch list while changing it.** Line L7 removes clauses from $W[\neg p]$ during the loop over it. Use an index with in-place compaction, as MiniSat does, or a copy.
- **Dropping the rest of the list on a conflict.** When line L8 returns, the clauses not yet visited must stay in $W[\neg p]$; they are not checked now, but they must still watch $\neg p$ after the backtrack.
- **Unit and empty input clauses.** Clauses of length 0 and 1 have no two watches. Handle them before the search: an empty clause makes $F$ unsatisfiable, and a unit is assigned at level 0.

## Exercises

1. Show that the level condition in (I) holds automatically when propagation is complete before each decision and backtracking removes whole levels, but can fail when a literal is assigned at a level below the current one.
2. Give a clause and a sequence of assignments and backtracks in which MiniSat's search from position 2 reads $\Theta(k^2)$ literals in total along one branch for a clause of length $k$, and show that the circular search reads $O(k)$.
3. Extend the invariant and its proof to cardinality constraints "at least $k$ of these literals are true", watched with $k + 1$ literals.
4. Prove that the scheme visits a clause only when one of its watches becomes false, and use it to show that a clause whose watched variables are never assigned costs nothing during the whole search.

## References
