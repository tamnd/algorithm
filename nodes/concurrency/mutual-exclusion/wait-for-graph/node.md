---
tag: T6DVQD
kind: data-structure
slug: wait-for-graph
name: Wait-for graph
aliases:
- waits-for graph
- WFG
area: concurrency/mutual-exclusion
level: core
summary: A directed graph with an edge from each blocked process to each process it waits for. With single unit resources, a cycle is a deadlock.
history:
  year: 1983
  people: [K. Mani Chandy, Jayadev Misra, Laura M. Haas]
  note: The graph is the process projection of Holt's 1972 resource graphs. Chandy, Misra and Haas (1983) gave the probe method that finds its cycles across sites.
prereqs: [resource-allocation-graph, cycle-detection]
see_also: [deadlock-detection, resource-allocation-graph, deadlock, wait-die-and-wound-wait, two-phase-locking, incremental-topological-ordering, global-snapshot, dijkstra-scholten]
sources:
  - paper: doi:10.1145/357360.357365
    title: K. Mani Chandy, Jayadev Misra and Laura M. Haas, Distributed deadlock detection, ACM Transactions on Computer Systems 1(2), 1983, pages 144 to 156
    locator: the resource model and its probe computation, and the communication model with its query computation
  - paper: doi:10.1145/356603.356607
    title: Richard C. Holt, Some deadlock properties of computer systems, ACM Computing Surveys 4(3), 1972, pages 179 to 196
    locator: general resource graphs, and the cycle condition for single unit resources
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition (2018)
    locator: Chapter 8, Deadlocks, the section on deadlock detection with a single instance of each resource type
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems (1987)
    locator: Chapter 3, Two Phase Locking, the section on deadlocks, with waits-for graphs, detection, and victim selection
---

A wait-for graph is a [directed graph](/directed-graph/) on the processes of a system, with an edge $p \to q$ when $p$ is blocked and waits for $q$ to release something. It is the [resource allocation graph](/resource-allocation-graph/) with the resource vertices projected away. When each resource has one unit, a [deadlock](/deadlock/) is exactly a set of processes that reach a cycle, so detection becomes [cycle detection](/cycle-detection/). Database lock managers keep this graph, and the probe method of Chandy, Misra and Haas (1983) finds its cycles when the graph is spread over many sites.

## In plain words

Write the name of each running program on a sheet. When a program must wait because another program holds a lock it needs, draw an arrow from the waiting program to the holder. When the wait ends, erase the arrow.

If you can follow the arrows from a program and come back to it, every program on that loop waits for the next one, and none of them can move. That is a deadlock. A program that waits for a program on the loop is stuck too.

You do not need to search the whole sheet each time. A loop can only appear when you draw a new arrow, so after each new arrow, check only whether you can get from its head back to its tail. When the sheet is split over many computers, the programs send small messages along the arrows to find the loop.

## The abstract type

The graph has a vertex for each process and an edge $p \to q$ for each wait. Its operations are: add a wait and report whether it closed a cycle; remove a wait when it ends; remove a process when it finishes or is aborted; and list the deadlocked processes.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j, k$ are process indices |
| $m$ | the number of shared objects (locks or other resources) |
| $e$ | the number of edges of the graph |

The model is the one of deadlock theory. Processes are asynchronous, and the memory that holds the graph is sequentially consistent (or the graph lives in one lock manager). A process that is blocked takes no step until its request is granted, so it releases nothing while it waits. Requests are AND requests: $p$ can proceed only when every process it waits for has released. This covers exclusive locks, where $p$ waits for the one holder, and also a shared lock held by several readers, where a writer waits for all of them. It does not cover a pool of identical units, where $p$ needs only one of several holders to release. For pools, keep the resource graph and use the reduction of [deadlock detection](/deadlock-detection/).

The safety property of a detector is that it reports only real deadlocks. Its progress property is that every deadlock is eventually reported.

## Representation

Keep two hash maps of sets: $\mathit{succ}[p]$, the processes that $p$ waits for, and $\mathit{pred}[q]$, the processes that wait for $q$. The second map lets the structure remove a process in time proportional to its degree. A lock manager builds the edges from its lock table: when $p$ blocks on lock $\ell$, it adds an edge from $p$ to each current holder of $\ell$ whose mode conflicts with the mode $p$ asked for.

**Invariant.** $q \in \mathit{succ}[p]$ if and only if $p \in \mathit{pred}[q]$, and this holds if and only if $p$ is blocked on a request that $q$ must release before it can be granted. A process with no outgoing edge is not blocked.

## Operations

```pseudo id=main
NEW()
L1  succ[p] ← ∅ and pred[p] ← ∅ for each process p

ADD-WAIT(p, q)                  ▷ p blocks on something that q holds; requires p ≠ q
L2  add q to succ[p] and p to pred[q]
L3  path ← a path q, ..., p found by depth-first search from q, or nil
L4  if path ≠ nil then return the cycle p, q, ..., back to p
L5  return nil

REMOVE-WAIT(p, q)               ▷ q released, or p got what it waited for
L6  remove q from succ[p] and p from pred[q]

REMOVE-PROCESS(p)               ▷ p finished or was aborted
L7  remove every edge into or out of p
```

**Add a wait** (lines L2 to L5). A cycle can appear only when an edge is added, since removals cannot create one. If the graph had no cycle before the new edge $p \to q$, then a cycle exists after it if and only if $q$ reaches $p$, and the cycle passes through the new edge. So one [depth-first search](/depth-first-search/) from $q$ is enough. The caller then breaks the cycle at once, by aborting a victim, and the graph stays acyclic between calls. This is the eager form that database lock managers use.

**Remove a wait and remove a process** (lines L6 and L7) keep the two maps in step. Aborting a victim is REMOVE-PROCESS followed by the grants that its released locks allow. Each grant removes the edges into the old holder and, if other waiters remain, adds edges from them to the new holder.

**List the deadlocked processes.** With single unit resources, a process is deadlocked if and only if it reaches a cycle. Repeatedly delete a vertex with no outgoing edge; the vertices that remain are the deadlocked ones. This is the reduction of [deadlock detection](/deadlock-detection/) in the single unit case, and it runs in $O(n + e)$ time.

**The probe method.** When the graph is spread over sites, no site sees all of it. Chandy, Misra and Haas (1983) find cycles by *edge chasing*. In outline, for their resource model:

1. A blocked process $i$ that suspects a deadlock sends a probe $(i, i, k)$ to each $k$ it waits for. The first entry names the initiator, the second the sender, and the third the receiver.
2. A process $k$ that gets a probe $(i, j, k)$ discards it if $k$ is not blocked. If $k$ is blocked and has not yet seen a probe of initiator $i$, it sends $(i, k, l)$ to each $l$ it waits for.
3. If the initiator $i$ gets a probe $(i, j, i)$, it declares that it is deadlocked.

The paper sends probes between the controllers of the sites, and it sends them only along edges that leave a site, so local paths are searched inside the site. The outline above keeps only the logic.

## Example

Four transactions in a lock manager. $T_1$ holds lock $a$, $T_2$ holds $b$, $T_3$ holds $c$.

| step | event | edge | ADD-WAIT returns |
|---|---|---|---|
| 1 | $T_1$ asks for $b$ | $T_1 \to T_2$ | nil |
| 2 | $T_2$ asks for $c$ | $T_2 \to T_3$ | nil |
| 3 | $T_4$ asks for $a$ | $T_4 \to T_1$ | nil |
| 4 | $T_3$ asks for $a$ | $T_3 \to T_1$ | the cycle $T_3, T_1, T_2$ |

At step 4 the search from $T_1$ finds $T_1 \to T_2 \to T_3$, so the new edge closes a cycle. All four transactions are deadlocked: $T_1$, $T_2$ and $T_3$ are on the cycle, and $T_4$ waits for $T_1$. The lock manager aborts a victim, say $T_2$. REMOVE-PROCESS$(T_2)$ deletes $T_1 \to T_2$ and $T_2 \to T_3$, lock $b$ goes to $T_1$, and the edges $T_3 \to T_1$ and $T_4 \to T_1$ remain. There is no cycle, and $T_1$ can run.

The probe method on the graph before the abort: $T_1$ sends $(T_1, T_1, T_2)$; $T_2$ is blocked and sends $(T_1, T_2, T_3)$; $T_3$ sends $(T_1, T_3, T_1)$, and $T_1$ declares a deadlock. If $T_4$ initiates instead, its probe travels $T_4 \to T_1 \to T_2 \to T_3 \to T_1$ and stops at $T_1$, which has already seen it. $T_4$ never gets its probe back. It is deadlocked, but only processes on a cycle detect a deadlock by their own probes, and it is enough to break the cycle.

## Correctness

[The proof file](proofs/correctness.md) proves four facts. First, the check of ADD-WAIT is exact: in an acyclic graph, adding $p \to q$ creates a cycle if and only if $q$ reaches $p$, and the returned list is a cycle. Second, in the AND model, every process that reaches a cycle is deadlocked. Third, with single unit resources, every deadlocked process reaches a cycle; this uses the reduction theorem of [deadlock detection](/deadlock-detection/). Fourth, on a graph that does not change during the run, the initiator of the probe method gets its own probe back if and only if it is on a cycle, and at most one probe crosses each edge.

The fourth fact is enough for a deadlock that already exists, because a deadlock is stable: the edges of a cycle stay until someone aborts a process. Chandy, Misra and Haas prove more, for a graph that changes while the probes travel: a declared deadlock is real, and a deadlock is declared if its processes initiate after it forms. The proof file covers only the static case.

## Complexity

The space is $O(n + e)$. Times are expected, with hash sets.

| operation | time |
|---|---|
| ADD-WAIT | $O(n + e)$ for the search; often much less, since it visits only what $q$ reaches |
| REMOVE-WAIT | $O(1)$ |
| REMOVE-PROCESS$(p)$ | $O(1 + \deg p)$ |
| list the deadlocked processes | $O(n + e)$ |
| probe method, one initiator | at most $e$ messages of three process names each |

A lock manager that checks on every block pays one search per wait, which is cheap when most waits are short and the graph is small. One that checks every few seconds pays $O(n + e)$ per check and lets a deadlock live until the next check.

## Variants

- **Periodic detection.** Build the graph from the lock table at fixed times and search it all. Cheaper when waits are frequent; slower to react.
- **Incremental orders.** Instead of a fresh search per edge, keep a topological order of the acyclic graph and repair it on each insertion; see [incremental topological ordering](/incremental-topological-ordering/). Only the part of the order between $q$ and $p$ needs repair.
- **Distributed detection.** Each site keeps its local part. One can collect the parts at a central site, but the parts are taken at different times, so the union can show a cycle that never existed (a *phantom deadlock*). A consistent [global snapshot](/global-snapshot/) avoids that. Edge chasing, as in the probe method, sends small messages instead. Path pushing sends whole paths of the graph between sites.
- **The communication model.** If a process waits for a message from any one of several processes (an OR request), a cycle is not enough, and the deadlock condition is a *knot*. Chandy, Misra and Haas detect it with a query and reply computation in the style of a diffusing computation; see [Dijkstra and Scholten](/dijkstra-scholten/).
- **Prevention instead of detection.** [Wait-die and wound-wait](/wait-die-and-wound-wait/) never let an edge go from an older to a younger transaction (or the reverse), so the graph can never have a cycle and is not kept at all.

## When to use it

Use it when processes hold several locks, the lock order cannot be fixed in advance, and aborting a process is acceptable, as in a database that runs [two-phase locking](/two-phase-locking/). For a program whose locks can be ordered, [lock ordering](/lock-ordering/) prevents the cycles and is cheaper. For pools of identical units, use the reduction instead, because a cycle is then not a deadlock.

## Pitfalls

- With several units per resource, a cycle can dissolve when a process outside it releases a unit. The graph gives false alarms there.
- An edge must leave the graph as soon as the wait ends, including after a timeout or a cancel. A stale edge produces a phantom deadlock and an abort for nothing.
- Aborting a victim releases its locks, and the lock manager then adds new edges for the remaining waiters. Detection must run again after the grants, not only before.
- A victim chosen by a fixed rule can be chosen again and again after it restarts. Use the age of the transaction, kept across restarts, to avoid [starvation](/starvation/).
- In the probe method, only processes on a cycle get their probe back. A process behind a cycle stays blocked until a process on the cycle detects it.

## Implementations

## History

Coffman, Elphick and Shoshani (1971) and Holt (1972) stated deadlock in terms of graphs of processes and resources, and the wait-for graph is the process part of Holt's graphs for single unit resources. Database systems of the 1970s and 1980s kept such graphs in their lock managers, as Bernstein, Hadzilacos and Goodman describe. Chandy, Misra and Haas (1983) gave the probe computation for the resource model and a diffusing query computation for the communication model.

## References
