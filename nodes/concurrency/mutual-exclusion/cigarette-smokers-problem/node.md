---
tag: JBBYWT
kind: problem
slug: cigarette-smokers-problem
name: Cigarette smokers problem
aliases:
- cigarette smokers
- cigarette smoker's problem
area: concurrency/mutual-exclusion
level: advanced
summary: A fixed agent puts out two of three ingredients, and the smoker with the third must take them. Patil (1971) claimed semaphores cannot solve it without conditionals; Parnas (1975) disputed this.
history:
  year: 1971
  people: [Suhas S. Patil, David L. Parnas]
  note: Patil posed the problem in 1971 to argue that Dijkstra's semaphores are too weak. Parnas answered in 1975 with a solution that uses arrays of semaphores and no conditionals.
prereqs: [semaphore]
see_also: [semaphore, deadlock, bounded-buffer-problem, sleeping-barber-problem, dining-philosophers-problem, readers-writers-problem, mutex, condition-variable]
sources:
  - paper: "Suhas S. Patil, Limitations and capabilities of Dijkstra's semaphore primitives for coordination among processes, MIT Project MAC, Computation Structures Group, Memo 57, February 1971"
    locator: the statement of the cigarette smokers problem, the restrictions on solutions, and the Petri net argument that semaphore primitives cannot solve it
  - paper: doi:10.1145/360680.360709
    title: D. L. Parnas, On a solution to the cigarette smoker's problem (without conditional statements), Communications of the ACM 18(3), 1975, pages 181 to 183
    locator: the criticism of Patil's restrictions and a solution with helper processes, arithmetic on a shared value, and an array of semaphores
  - url: "https://greenteapress.com/wp/semaphores/"
    title: Allen B. Downey, The Little Book of Semaphores, version 2.2
    locator: Chapter 4, the section Cigarette smokers problem, with the agent code, the deadlock of the naive smokers, the pushers with the flags isTobacco, isPaper and isMatch, and the generalized problem
---

In the cigarette smokers problem, three smokers sit at a table. To smoke, a smoker needs tobacco, paper and a match. Each smoker has an endless supply of one of the three, and a different one from the others. An agent puts two different ingredients on the table; the smoker who has the third should take them, make a cigarette, smoke, and let the agent know, and the agent then puts out another pair. Patil posed the problem in 1971 with the agent's code fixed and conditional statements forbidden, and claimed that no solution with Dijkstra's [semaphores](/semaphore/) exists under these rules. Parnas showed in 1975 that the claim fails when arrays of semaphores are allowed.

## In plain words

Three people want to smoke. One has only tobacco, one has only paper, one has only matches. A dealer puts two of the three things on the table at a time, and only the person who has the missing third thing can use them.

The dealer just rings a bell for each item: "tobacco is here", "paper is here". If each smoker grabs the first item they need as soon as they hear its bell, two of them may each grab one item from the same pair. Then each one waits for a second item that never comes, and nobody smokes.

The fix is a helper for each item who notes what has arrived and, when two items are there, calls the one smoker who can use both.

## Definition

The model has $n$ asynchronous processes in a sequentially consistent memory: three agent processes, three smokers, and in some solutions helper processes. A process may crash between steps, but the problem asks for nothing when one does. The shared objects are counting [semaphores](/semaphore/) with P and V, and in some solutions shared integers or booleans under a semaphore used as a [mutex](/mutex/).

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes: 3 agents, 3 smokers, and any helpers |
| $p, q$ | process names; $i, j$ index ingredients |
| $k$ | the contention: the number of smokers that wait for the same ingredient |
| $m$ | the number of shared objects: the semaphores tobacco, paper, match and agentSem, and those of the solution |

**The agent.** The semaphores tobacco, paper and match start at 0, and agentSem starts at 1. The agent is three processes, one per pair, each running

```text
loop
  P(agentSem)
  V(x); V(y)        { (x, y) is (tobacco, paper), (paper, match) or (tobacco, match) }
```

Which of the three goes on after a V(agentSem) is up to the semaphore, so the agent picks a pair in a way the smokers cannot predict. A V on an ingredient does not say which pair it belongs to.

**The task.** Write the smokers, and if needed extra processes, so that each time the agent puts out a pair, the smoker who has the third ingredient (and only that smoker) takes the pair, smokes, and does V(agentSem). The run must never deadlock.

**Patil's restrictions.** (1) The agent's code may not be changed. (2) The solution may not use conditional statements. Under these restrictions, and with P and V on single semaphores as the only primitives, Patil claimed that no solution exists, and he argued with a Petri net model that a more powerful primitive is needed.

## Variants

- **Arrays of semaphores allowed.** Parnas's setting: still no conditional statements, but a process may compute an index and do V on an element of an array of semaphores.
- **Conditionals allowed.** Downey's setting: the agent stays fixed, but the solution may use if statements; then helper processes (pushers) solve it.
- **The generalized problem.** The agent does not wait for the smokers: it does not do P(agentSem), so ingredients can pile up on the table. Downey solves it with counters in place of boolean flags.
- **A simultaneous P.** With a primitive that waits on several semaphores at once and takes all of them in one step, each smoker simply does that P on the two semaphores it needs.

## Examples

**The naive smokers deadlock.** Let the smoker who has matches run "P(tobacco); P(paper); smoke; V(agentSem)", and the others the same with their own two ingredients. Suppose the agent puts out tobacco and match, for the smoker who has paper. The smoker who has matches needs tobacco and paper; it takes the tobacco and then waits on paper. The smoker who has paper needs tobacco and match; it waits on tobacco, which is gone. The match lies on the table. Nobody smokes, the agent waits on agentSem, and the system is [deadlocked](/deadlock/). The simulator finds this state at once with a search over all interleavings: the agent for (tobacco, match) runs, and the smoker who has matches takes the tobacco.

**The pushers (Downey's solution, with conditionals).** Add a mutex, three booleans isTobacco, isPaper and isMatch, which start false, three semaphores smokerTobacco, smokerPaper and smokerMatch, which start at 0, and three pushers. The pusher for tobacco runs

```text
loop
  P(tobacco)
  P(mutex)
  if isPaper then isPaper := false; V(smokerMatch)
  else if isMatch then isMatch := false; V(smokerPaper)
  else isTobacco := true
  V(mutex)
```

and the other two pushers are the same with the ingredients exchanged. The smoker who has tobacco runs "loop P(smokerTobacco); make a cigarette; V(agentSem); smoke". The first pusher of an offer only notes its ingredient; the second one sees the first ingredient's flag and wakes the smoker who has the third ingredient. Each ingredient is taken by exactly one pusher, so the naive race is gone.

**An indexed solution without conditionals (in the style of Parnas).** Give the ingredients the weights tobacco 1, paper 2 and match 4, add a shared integer t (start 0) and an array of semaphores S[1..7] (all 0). The pusher for an ingredient of weight w runs

```text
loop
  P(ingredient)
  P(mutex); t := t + w; V(S[t]); V(mutex)
```

and the smoker who needs ingredients of weights a and b runs "loop P(S[a + b]); t := 0; smoke; V(agentSem)". After the first ingredient of an offer, t is 1, 2 or 4, and the V goes to a semaphore that nobody waits on; after the second, t is the sum of the pair, 3, 5 or 6, which names the right smoker. The smoker resets t before it lets the agent go on. There is no conditional statement: the arithmetic does the work of the if. Parnas's own program also uses helper processes and arithmetic on a shared value to choose an element of a semaphore array; the program here is a simplified version in that spirit, not his exact text.

**What the tests check.** For the pushers, the indexed solution and the simultaneous P, a search over all interleavings for two offers finds no deadlock and no smoker who smokes without its offer, and in every final state each smoker has smoked as often as its pair was offered. Seeded random runs with 12 offers end the same way. For the model to be finite, the smoker who smokes the last cigarette does not do V(agentSem); this stop rule is not part of the protocol.

## Known algorithms

| solution | conditionals | arrays of semaphores | extra processes |
|---|---|---|---|
| naive smokers | no | no | none; deadlocks |
| pushers (Downey) | yes | no | 3 pushers |
| indexed, in the style of Parnas | no | yes | 3 pushers (Parnas uses helper processes too) |
| simultaneous P | no | no | none, but needs a P on several semaphores |

Each offer costs a constant number of semaphore operations in each solution.

## Bounds

**Patil's impossibility claim.** Patil claimed that, with the agent fixed, no conditional statements, and only P and V on single semaphores, no set of smoker processes solves the problem. The intuition: without a conditional, a process that is woken by V(tobacco) must do the same next operation whatever the second ingredient is, so a process that waits on one ingredient cannot choose between the two smokers who might need it. Patil made the argument with Petri nets and took it as evidence that semaphores are not a complete set of primitives.

**Parnas's answer.** Parnas argued that Patil's proof does not cover programs that use arrays of semaphores, and that restrictions that forbid either conditionals or semaphore arrays are artificial. His solution needs neither conditional statements nor a new primitive, so the claim, read as "semaphores are too weak", does not hold. What remains true is narrower: with a fixed number of named semaphores, P and V on one semaphore each, and straight line code with no data dependent choice, a process cannot route a wakeup by the value of shared data, and the impossibility argument is about that model.

**The first restriction is sound.** Downey notes that forbidding changes to the agent models a real constraint: the agent stands for an operating system that allocates resources, and it would be unreasonable to change it for each application.

## Reductions

- The smokers problem is a resource allocation problem in which a process needs two resources at once, like the [dining philosophers](/dining-philosophers-problem/): the naive smokers deadlock for the same reason, a process holds one resource while it waits for another. The pushers remove the hold and wait.
- With a simultaneous P (all of a set of semaphores at once), both problems become easy, which is the AND synchronization that later systems added: for example, System V semaphore sets let one semop call change several semaphores atomically.
- The pushers form a small [monitor](/monitor/): a mutex, shared state, and a way to wake one chosen process. With [condition variables](/condition-variable/) the same logic is a while loop on "my two ingredients are there".

## Applications

- **Expressive power of primitives.** The problem was posed, and is still used, as a test of what a synchronization primitive can express without help from data dependent code.
- **Teaching.** It is a standard exercise in semaphore programming, in which the natural first answer deadlocks.
- **Resource managers.** A process that needs a set of resources from a manager it cannot change, and must not take some of them and then wait, is in the same position.

### History

Suhas Patil posed the problem in an MIT Project MAC memo of 1971, "Limitations and capabilities of Dijkstra's semaphore primitives for coordination among processes" (Computation Structures Group Memo 57), as evidence that semaphores need a stronger primitive. David Parnas replied in the Communications of the ACM in March 1975, "On a solution to the cigarette smoker's problem (without conditional statements)", with a solution that uses an array of semaphores and arithmetic in place of conditionals, and argued that the restrictions were artificial. Downey's Little Book of Semaphores made the pusher solution and a generalized version widely known.

### Exercises

1. Find a schedule in which the naive smokers deadlock even though the agent's offer is for the smoker who runs first.
2. Prove that in the pusher solution, for each offer, exactly one pusher sets a flag and exactly one pusher wakes a smoker.
3. In the indexed solution, why must the smoker reset t before V(agentSem), and not after it?
4. Solve the generalized problem, where the agent does not wait on agentSem, with pushers and counters.
5. Explain why the naive smokers do not deadlock if each smoker does one P on both of its semaphores at once.

## References
