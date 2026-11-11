---
tag: YGHDZH
kind: algorithm
slug: deadlock-detection
name: Deadlock detection
aliases:
- Wait-for graph deadlock detection
- cycle detection in wait-for graph
- deadlock detection algorithm
- graph reduction
area: concurrency/mutual-exclusion
level: core
summary: Find the deadlocked processes of a state. With one unit per resource, look for a cycle in the wait-for graph; with several units, use Holt's graph reduction in O(m n^2) time.
model: word-ram
complexity:
  vars: {n: the number of processes, m: the number of resource types}
  time:
    worst: "O(m n^2)"
  space:
    extra: "O(m + n)"
history:
  year: 1972
  people: [Richard C. Holt, Edward G. Coffman, Arie Shoshani]
  note: Coffman, Elphick and Shoshani surveyed detection in 1971. Holt's 1972 survey gave graph reduction, proved that its order does not matter, and gave a faster method with sorted requests.
prereqs: [wait-for-graph, resource-allocation-graph]
see_also: [cycle-detection, banker-algorithm, deadlock-prevention, coffman-conditions, mutual-exclusion-deadlock-handling, deadlock-freedom-checking, topological-sort, wait-die-and-wound-wait]
sources:
  - paper: doi:10.1145/356603.356607
    title: Richard C. Holt, Some deadlock properties of computer systems, ACM Computing Surveys 4(3), 1972, pages 179 to 196
    locator: graph reduction, the theorem that all complete reductions agree, and the detection algorithms for reusable resources
  - paper: doi:10.1145/356586.356588
    title: E. G. Coffman, M. J. Elphick and A. Shoshani, System deadlocks, ACM Computing Surveys 3(2), 1971, pages 67 to 78
    locator: the section on deadlock detection and recovery
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition (2018)
    locator: Chapter 8, Deadlocks, the sections on deadlock detection (single instance and several instances of each resource type) and on recovery from deadlock
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition (2015)
    locator: Chapter 6, Deadlocks, the sections on detection with one resource and with several resources of each type, and on recovery
---

Deadlock detection finds the [deadlocked](/deadlock/) processes in a state of a system that grants requests without checking for deadlock first. When each resource has one unit, the deadlocked processes are those that can reach a cycle of the [wait-for graph](/wait-for-graph/), and a [cycle detection](/cycle-detection/) by depth-first search finds them in linear time. With several units per resource type, a cycle is not enough, and the exact test is Holt's *graph reduction*: pretend that each process whose request fits finishes and gives back its units, and repeat. The processes that remain are exactly the deadlocked ones, the order of the steps does not matter, and the simple loop takes $O(m n^2)$ time for $n$ processes and $m$ resource types.

## In plain words

A detector takes a snapshot: who holds what, who waits for what, and what is free. Then it plays an optimistic game. Find a program whose request can be met with the free resources. Assume it gets them, finishes, and returns everything it held. The free pool grows. Look again for a program whose request now fits. Keep going until no program fits.

If every program got crossed out, nothing is stuck: there is an order in which all of them can finish. The programs that are left can never move, because even in the best case the pool never grows enough for any of them. They are the deadlock. To end it, the system picks a victim among them, aborts it or rolls it back, takes its resources, and runs the game again.

## The problem

**Model.** There are $n$ asynchronous processes and $m$ resource types with $t(r)$ units of type $r$. Resources are reusable. A request is blocking and asks for a vector of units, all of which must be free (an AND request). A blocked process takes no step and releases nothing. A process that is not blocked may finish and release everything.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes; $i, j$ are indices |
| $p, q$ | process names |
| $m$ | the number of resource types |
| $\mathit{avail}[r]$ | the free units of type $r$ |
| $\mathit{alloc}[i][r]$, $\mathit{req}[i][r]$ | units of $r$ that process $i$ holds, and that it waits for |

For vectors, $x \le y$ means $x[r] \le y[r]$ for every $r$.

**Input.** The vectors $\mathit{avail}$, $\mathit{alloc}[i]$ and $\mathit{req}[i]$ for $i = 0, \ldots, n - 1$, with $\mathit{alloc}[i] + \mathit{req}[i] \le t$.

**Output.** The set of processes that are deadlocked: blocked in every state that the system can reach.

Detection looks only at the current requests. It does not need the maximum claims that [avoidance](/banker-algorithm/) needs, and it does not restrict the order of requests as [prevention](/deadlock-prevention/) does. The price is that a deadlock happens first and must then be broken.

## The algorithm

```pseudo id=main
DETECT(avail, alloc, req)           ▷ returns the deadlocked processes
L1  work ← avail; finish[i] ← false for each i
L2  repeat
L3      progress ← false
L4      for i ← 0 to n − 1 do
L5          if not finish[i] and req[i] ≤ work then
L6              work ← work + alloc[i]; finish[i] ← true; progress ← true
L7  until not progress
L8  return { i : finish[i] = false }
```

Line L5 asks whether the request of process $i$ fits in the pool. If it does, line L6 assumes that $i$ finishes, and returns its units to the pool. The loop of lines L2 to L7 runs passes until a pass removes nobody.

**Single unit resources.** When every type has one unit, line L5 holds exactly when every holder of every type that $i$ waits for is already finished, so the loop removes the vertices of the wait-for graph that have no remaining successor. What is left is the set of processes that can reach a cycle. In practice one runs a depth-first search on the wait-for graph and reports a cycle, which is enough to pick a victim; the page on the [wait-for graph](/wait-for-graph/) gives the incremental check that runs at each new wait.

**Recovery.** If DETECT returns a nonempty set, the system must take resources away from some process of the set:

1. Choose a victim $v$ among the deadlocked processes, by a cost: its priority, how long it has run, how much work a restart loses, how many units it holds, how many times it was already a victim.
2. Abort $v$, or roll it back to a checkpoint taken before it got the units, and return its units to the pool.
3. Run DETECT again, and repeat until the set is empty.

Aborting all deadlocked processes at once is simpler but loses more work. Choosing one victim at a time costs a new detection after each abort. A victim that may be chosen again and again starves; counting earlier rollbacks in the cost prevents this.

**When to run it.** Running DETECT at every request that blocks finds each deadlock at once, and with single units an incremental cycle check through the new edge suffices. Running it every few seconds, or when the processor is idle while processes wait, costs less and finds the deadlock later. Database systems often wait a short time before they look for a cycle, because most lock waits end on their own.

## Example

Four processes and three types $A, B, C$ with $t = (3, 2, 2)$. No unit is free.

| process | $\mathit{alloc}$ | $\mathit{req}$ |
|---|---|---|
| $p_0$ | $(1, 0, 1)$ | $(0, 1, 0)$ |
| $p_1$ | $(1, 1, 0)$ | $(0, 0, 1)$ |
| $p_2$ | $(0, 1, 0)$ | $(1, 0, 0)$ |
| $p_3$ | $(1, 0, 1)$ | $(0, 0, 0)$ |

The trace of DETECT, with $\mathit{work}$ after each line L6:

| pass | removed in order | $\mathit{work}$ after the pass |
|---|---|---|
| start | | $(0, 0, 0)$ |
| 1 | $p_3$ | $(1, 0, 1)$ |
| 2 | $p_1$, then $p_2$ | $(2, 2, 1)$ |
| 3 | $p_0$ | $(3, 2, 2)$ |
| 4 | nobody | $(3, 2, 2)$ |

In pass 1, $p_0$, $p_1$ and $p_2$ do not fit in $(0, 0, 0)$, and $p_3$ requests nothing. In pass 2, $p_0$ still needs a $B$, but $p_1$ fits, and its units let $p_2$ fit in the same pass. DETECT returns the empty set: the order $p_3, p_1, p_2, p_0$ lets everyone finish. The wait-for graph has the cycle $p_0 \to p_1 \to p_0$ ($p_0$ waits for a $B$ held by $p_1$ and $p_2$, and $p_1$ waits for a $C$ held by $p_0$ and $p_3$), so a cycle test alone would raise a false alarm.

Now let $p_0$, $p_1$ and $p_2$ each request one $B$, that is $\mathit{req} = (0, 1, 0)$ for each, and $p_3$ nothing. Pass 1 removes $p_3$ and gives $\mathit{work} = (1, 0, 1)$. No other process fits, since both units of $B$ are held by $p_1$ and $p_2$, which wait for each other's unit. DETECT returns $\{p_0, p_1, p_2\}$. Here $p_0$ is on no cycle, yet it is deadlocked: it waits for $p_1$ and $p_2$, which never release. Aborting $p_1$ returns $(1, 1, 0)$, and then $p_2$ and $p_0$ can finish.

## Correctness

The proof is in [the proof file](proofs/correctness.md). It has two parts.

First, the order of the reductions does not matter. Reducing a process only adds units to the pool, so a process that fits at some moment fits at every later moment. If two complete sequences removed different sets, take the first process of one sequence that the other misses: everything before it was removed by the other sequence too, so the other pool is at least as large, and the process fits there. That contradicts completeness. This is why DETECT can scan the processes in any order and why it does not need to backtrack.

Second, the result is exact. A removed process is not deadlocked: the removal order is a real future in which each process in turn gets its request and releases its units. A process that remains is deadlocked: the pool can never exceed the pool at the end of the reduction, because the remaining processes are blocked and keep their units, and that pool does not hold any of their requests.

## Complexity

**Time.** Each pass of lines L2 to L7 either finishes at least one more process or is the last pass, so there are at most $n + 1$ passes. A pass tests $n$ processes, and each test and each update touches $m$ entries. The total is $O(m n^2)$ time in the worst case. The bound is tight for the loop as written: if the processes fit only in reverse order of their index, each pass removes one process and scans all the others. The extra space is $O(m + n)$ for $\mathit{work}$ and $\mathit{finish}$.

**A faster version.** For each type $r$, sort the processes by $\mathit{req}[i][r]$, and keep for each process a count of the types on which its request does not fit yet. A pointer per type walks along the sorted list as $\mathit{work}[r]$ grows, and decrements the counts; a process whose count reaches 0 is removed and its units are added. Each pointer moves at most $n$ times, so after the sorts the work is $O(mn)$, and the total with the sorts is $O(m n \log n)$. Holt (1972) describes a method of this kind.

**Single units.** The wait-for graph has $n$ vertices and at most one edge per blocked request, and a depth-first search finds a cycle in $O(n + e)$ time for $e$ edges.

## Properties

- Exact: it reports a process if and only if the process is deadlocked, under the model above.
- Needs no advance knowledge of the requests, unlike the [banker's algorithm](/banker-algorithm/).
- Deterministic, and independent of the scan order of the processes.
- It looks at one consistent snapshot. In a distributed system no process has one, and the [wait-for graph](/wait-for-graph/) page outlines the probe method of Chandy, Misra and Haas.

## Variants and improvements

- **Textbook detection with $\mathit{finish}[i]$ preset.** Silberschatz, Galvin and Gagne start with $\mathit{finish}[i] = \mathit{true}$ for each process that holds nothing. Such a process cannot be on a cycle, but it can still be blocked forever behind a deadlock, as $p_0$ would be in the second example if it held nothing; this variant then does not report it. Holt's definition counts it as deadlocked.
- **Incremental detection.** With single units, a new edge $p \to q$ creates a cycle only if $p$ is reachable from $q$. A search from $q$ at each new wait finds every cycle when it forms.
- **Timeouts.** Many systems skip the graph and abort a transaction that waits longer than a fixed time. This needs no graph, but it aborts some transactions that were not deadlocked and finds real deadlocks late.
- **Distributed detection.** Probes along the edges of a global wait-for graph (Chandy, Misra and Haas 1983) avoid building the graph in one place.
- **Model checking.** A [model checker](/deadlock-freedom-checking/) searches all states of a program for a state with no enabled step, which detects deadlocks before the program runs.

## When to use it

Use detection when deadlocks are rare and the work lost by aborting a victim is acceptable, and when the system cannot know the needs of the processes in advance. Database systems are the main case: transactions lock rows in an order that depends on the data, and an abort is a normal event that the application must handle anyway. Do not use it where a process cannot be rolled back, such as a process that has already printed or sent data, unless the recovery can undo or tolerate that.

## Pitfalls

- With several units per type, a cycle in the wait-for graph is not a deadlock. Use reduction, or accept false alarms.
- The snapshot must be consistent. A detector that reads the lock table without locking it can see a cycle that never existed, or miss one.
- A process that waits behind a deadlock is also stuck, even when it is on no cycle. Aborting a process on the cycle frees it; aborting it frees nothing.
- Choosing the same victim each time starves it. Add the number of earlier rollbacks to the cost.
- After a victim is aborted, its units go to the waiting processes, and the state can still hold another deadlock. Run the detection again.

## Implementations

## History

Coffman, Elphick and Shoshani (1971) treated detection and recovery as one of the three strategies, next to prevention and avoidance. Holt (1972) formalized resource graphs, defined graph reduction, proved that complete reductions agree, and showed that a state is free of deadlock exactly when its graph is completely reducible. The probe method for distributed systems is due to Chandy, Misra and Haas (1983).

## References
