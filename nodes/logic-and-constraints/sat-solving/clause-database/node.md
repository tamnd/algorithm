---
tag: K9N1A5
kind: data-structure
slug: clause-database
name: Clause database
aliases:
- clause arena
- clause store
area: logic-and-constraints/sat-solving
level: advanced
summary: Storage of the input and learned clauses of a CDCL solver in one flat array, with a header per clause, watch lists, lazy deletion and garbage collection that compacts the array.
model: word-ram
prereqs: [clause, two-watched-literals, dynamic-array]
see_also: [clause-database-reduction, literal-block-distance, cdcl, clause-learning, arena-allocation, mark-compact, incremental-sat]
sources:
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, Lecture Notes in Computer Science 2919, 2004
    locator: pages 502 to 518 (the clause representation, watch lists, learned clauses and their removal in MiniSat)
  - paper: doi:10.1145/378239.379017
    title: Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang and Sharad Malik, Chaff, engineering an efficient SAT solver, Proceedings of the 38th Design Automation Conference, 2001
    locator: pages 530 to 535 (watched literals and the deletion of learned clauses)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik, the sections on data structures and clause deletion
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the memory layout of Algorithm C (clauses stored as consecutive cells with watch links)
  - paper: "Gilles Audemard and Laurent Simon, Predicting learnt clauses quality in modern SAT solvers, Proceedings of IJCAI 2009, pages 399 to 404"
    locator: the LBD of a learned clause, stored with the clause and used to choose the clauses to delete
---

A clause database is the store of all clauses of a [CDCL](/cdcl/) solver: the input clauses and the [learned clauses](/clause-learning/), each with a small header, plus the watch lists of the [two watched literals](/two-watched-literals/) scheme. It supports adding a clause, deleting a clause, moving a watch, and a garbage collection that removes deleted clauses and compacts memory. This page is about the storage. Which learned clauses to delete, and when, is a separate policy, described on the [clause database reduction](/clause-database-reduction/) page.

## In plain words

A solver keeps all its rules in one long notebook. Each rule starts with a short label: how long it is, whether the solver learned it, and a quality score. The words of the rule follow the label. The solver finds a rule by the page where its label starts.

For each possible value of each variable, the solver also keeps a list of the rules that watch it, so that it can find fast the rules that may now force something.

To throw a rule away, the solver only marks its label as dead, because rewriting the notebook and all the lists at each removal costs too much. When many rules are dead, it copies the live rules into a fresh notebook, without gaps, and tells everyone the new page of each rule.

## The abstract type

The database stores clauses over the variables $x_1, \ldots, x_n$. Each stored clause has at least two literals over distinct variables; unit clauses go straight to the trail. A clause is named by a reference $r$, an integer. The operations are:

- `add(C, learned, g)`: store the clause $C$ with a learned flag and an [LBD](/literal-block-distance/) value $g$, watch its first two literals, and return its reference.
- `delete(r)`: remove the clause $r$.
- `swap-watch(r, i, k)`: make the literal at position $k \ge 2$ a watched literal in place of the one at position $i \in \{0, 1\}$.
- `watchers(ℓ)`: the live clauses that watch the literal $\ell$.
- `collect()`: free the space of deleted clauses and return the map from old to new references.
- reading: the literals, the size, the flags and the LBD of a clause, and the list of live clauses.

## Representation

All clauses live in one [dynamic array](/dynamic-array/) $A$ of integers, an [arena](/arena-allocation/). A clause of $k$ literals is a record of $k + 3$ cells: the size $k$, a flags word (bit 0 marks a learned clause, bit 1 a deleted one), the LBD, and then the literals. The reference of a clause is the index of its size cell. The literals at positions 0 and 1 are the watched ones. For each literal $\ell$, the watch list $W[\ell]$ is a list of references. A counter `wasted` holds the number of cells of deleted records.

**Invariant.** (A) The records tile the array: from index 0, stepping over each record by its size visits all of them and ends at $|A|$. (W) The live entries of $W[\ell]$ are distinct, and they are exactly the live clauses with $\ell$ at position 0 or 1. (V) `wasted` is the total size of the deleted records.

Deleted references may stay in the watch lists until the next collection; readers skip them. Real solvers store more in the header, such as an activity for learned clauses, a "used" bit, and flags for clauses that were moved or are being probed, and they put a blocking literal next to each reference in the watch lists.

## Operations

```pseudo id=main
ADD(D, C, learned, g)                         ▷ |C| ≥ 2, distinct variables
L1  r ← |A|
L2  append |C|, the flags, g and the literals of C to A
L3  append r to W[C[0]] and to W[C[1]]
L4  return r

DELETE(D, r)                                  ▷ r is live and not the reason of an assigned literal
L5  set the deleted flag of r
L6  wasted ← wasted + 3 + |r|

SWAP-WATCH(D, r, i, k)                        ▷ i ∈ {0, 1}, 2 ≤ k < |r|
L7  u ← r[i]; v ← r[k]; swap r[i] and r[k]
L8  remove r from W[u]; append r to W[v]

COLLECT(D)
L9  A' ← empty array; M ← empty map
L10 for each record r of A, in order do
L11     if r is live then M[r] ← |A'|; append the record r to A'
L12 for each literal ℓ do W[ℓ] ← [M[x] : x ∈ W[ℓ], x is live]
L13 A ← A'; wasted ← 0
L14 return M
```

**Add** (lines L1 to L4) appends a record at the end of the arena and puts its reference on two watch lists.

**Delete** (lines L5 and L6) only sets a flag and counts the freed cells. Removing the reference from the two watch lists at once would cost a scan of each list. The reason precondition matters: a clause that is the reason of a literal on the trail holds the edges of the [implication graph](/implication-graph/) that conflict analysis reads.

**Swap-watch** (lines L7 and L8) is what [unit propagation](/unit-propagation/) does when a watched literal becomes false and the clause has another literal that is not false. In a real propagation loop, line L8 does not search $W[u]$: the loop is already walking $W[u]$ and simply does not copy the entry back.

**Collect** (lines L9 to L14) is a [mark-compact](/mark-compact/) pass in one sweep: it copies each live record to the front, in order, and maps the references in the watch lists. The caller applies $M$ to every other reference it keeps, such as the reason of each assigned variable. Solvers call it when `wasted` passes a fixed share of $|A|$, often after a [reduction](/clause-database-reduction/).

## Example

Let $n = 5$. Add the input clause $\{x_1, x_2, x_3\}$, then the learned clauses $\{\neg x_1, x_4\}$ with LBD 2 and $\{\neg x_2, \neg x_4, x_5\}$ with LBD 3. Then make $x_5$ a watch of the third clause in place of $\neg x_4$, delete the second clause and collect. Literals are written as signed integers.

| step | arena | watch lists that change |
|---|---|---|
| add $\{x_1, x_2, x_3\}$ at $r = 0$ | `3 0 0 1 2 3` | $W[x_1] = [0]$, $W[x_2] = [0]$ |
| add $\{\neg x_1, x_4\}$ at $r = 6$ | `3 0 0 1 2 3 2 1 2 -1 4` | $W[\neg x_1] = [6]$, $W[x_4] = [6]$ |
| add $\{\neg x_2, \neg x_4, x_5\}$ at $r = 11$ | `3 0 0 1 2 3 2 1 2 -1 4 3 1 3 -2 -4 5` | $W[\neg x_2] = [11]$, $W[\neg x_4] = [11]$ |
| swap-watch(11, 1, 2) | `3 0 0 1 2 3 2 1 2 -1 4 3 1 3 -2 5 -4` | $W[\neg x_4] = []$, $W[x_5] = [11]$ |
| delete(6) | `3 0 0 1 2 3 2 3 2 -1 4 3 1 3 -2 5 -4` | none; 6 stays in $W[\neg x_1]$ and $W[x_4]$; wasted = 5 |
| collect | `3 0 0 1 2 3 3 1 3 -2 5 -4` | $M = \{0 \mapsto 0, 11 \mapsto 6\}$; $W[\neg x_1] = W[x_4] = []$, $W[\neg x_2] = W[x_5] = [6]$ |

The arena shrinks from 17 cells to 12, which is 17 minus `wasted`. The third clause keeps its content, its flags and its LBD, and now has the reference 6.

## Correctness

The invariant holds for the empty database. ADD appends a record where the walk of (A) ends and puts its reference on the lists of its two different first literals. DELETE only shrinks the set of live records, which both sides of (W) speak about, and adds the size to `wasted`. SWAP-WATCH changes one watched literal of one record and moves its reference between the two matching lists. COLLECT copies each live record unchanged, in order, so the copies tile the new array, and the map $M$ is one to one, so the mapped watch lists keep (W); the new length is $|A|$ minus `wasted`. By induction, the live records, read through the maps, are exactly the clauses added and not deleted, with their content. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $k$ be the size of the clause, $w$ the length of a watch list and $|A|$ the arena size.

| operation | time |
|---|---|
| add | $O(k)$ amortized, as for a dynamic array |
| delete | $O(1)$ |
| swap-watch | $O(k)$ to find the new literal in propagation, plus $O(w)$ for a stand-alone removal; $O(1)$ inside a propagation loop |
| watchers | $O(w)$ |
| collect | $O(|A|)$, since each record has two watch entries and at least 5 cells |
| space | $O(|A| + n)$ |

If COLLECT runs only when `wasted` is at least half of $|A|$, the arena is never more than twice the live size, and each collection costs at most a constant times the cells freed since the one before. The arena layout also matters for speed: a clause is read in one sweep of adjacent cells, while a clause allocated on its own sits somewhere else in memory, and propagation spends most of its time on such reads.

## Variants

- **One object per clause.** Early solvers and many teaching solvers allocate each clause as its own object, with a pointer as its reference. Deletion frees the object at once, and no collection is needed, but memory gets fragmented and reads are slower. The Python code of the [CDCL](/cdcl/) page uses this form, with `None` for a deleted clause.
- **Binary clauses in the watch lists.** A clause of two literals can live entirely in the watch lists: the entry for $\ell$ holds the other literal. Such clauses take no arena space and need no clause read during propagation.
- **Tiers of learned clauses.** Solvers in the line of Glucose and its successors keep learned clauses in groups by LBD, for example "core" clauses with LBD at most 2 that are kept for good, a middle tier and a local tier. The tier is a header field, and the [reduction](/clause-database-reduction/) policy reads it.
- **Occurrence lists.** Preprocessors such as [bounded variable elimination](/bounded-variable-elimination/) and [subsumption](/clause-subsumption/) need, for each literal, all clauses that contain it, not only the two watches. They build full occurrence lists for a while and drop them before the search resumes.
- **Incremental use.** In [incremental SAT](/incremental-sat/), clauses are added between calls, and clauses with a selector literal are deleted when the user retracts them; the same arena serves.

## When to use it

Use an arena database in any CDCL solver that learns many clauses, which is all of them: a solver can learn millions of clauses in one run and delete most of them again. For a short teaching solver, one list per clause with lazy deletion is simpler and fast enough.

## Pitfalls

- **Stale references after a collection.** Every reference held outside the watch lists, such as the reason of each assigned variable or a list of clauses under analysis, must be mapped by $M$. A forgotten one points into the middle of another record.
- **Deleting a reason clause.** A clause that is the reason of a literal on the trail is "locked". Deleting it breaks conflict analysis at the next conflict. Check that the reason of the first literal of the clause is the clause itself before deleting.
- **Reading deleted clauses from watch lists.** With lazy deletion, the watch lists contain dead entries. Propagation must skip them, or drop them as it walks the list.
- **Duplicate watches.** A clause with the same literal at positions 0 and 1 is watched twice by one literal and once by none. Remove repeated literals before ADD.
- **Integer overflow of references.** With 32-bit references, a very large arena overflows. Solvers check the size before they add and grow the reference type or collect first.

## Implementations

The Python class keeps the arena as one list of integers and the watch lists as a list indexed by literal. It follows the main block line by line, and `check_invariant` tests (A), (W) and (V).

## History

Chaff (2001) introduced watch lists and deleted learned clauses that it judged no longer relevant. MiniSat (Eén and Sörensson, 2003) gave the design that later solvers copied: one record per clause with a header, learned clauses marked by a flag, and a scheme to delete learned clauses that are not locked. Later versions of MiniSat (2.2) moved all clauses into one region with 32-bit references and a relocating garbage collection. Audemard and Simon added the LBD to the header in Glucose (2009). Knuth's Algorithm C in Volume 4B stores clauses as consecutive cells of one memory array in the same way.

## References
