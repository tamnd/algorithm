---
tag: 47TX1V
kind: algorithm
slug: banker-algorithm
name: Banker's algorithm
aliases:
- Dijkstra's banker's algorithm
- banker's algorithm
- Habermann's algorithm
area: concurrency/mutual-exclusion
level: core
summary: Deadlock avoidance. Each process declares its maximum claim, and a request is granted only if the new state is safe, which an O(m n^2) check decides.
model: word-ram
complexity:
  vars: {n: the number of processes, m: the number of resource types}
  time:
    worst: "O(m n^2)"
  space:
    extra: "O(m + n)"
history:
  year: 1965
  people: [Edsger W. Dijkstra, A. Nico Habermann]
  note: Dijkstra described the banker for one kind of resource in EWD 108 and in Cooperating Sequential Processes (EWD 123). Habermann (1969) treated several resource types.
prereqs: [deadlock, resource-allocation-graph]
see_also: [deadlock-detection, deadlock-prevention, coffman-conditions, resource-allocation-graph, mutual-exclusion-deadlock-handling, lock-ordering, dining-philosophers-problem, deadlock]
sources:
  - url: "https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html"
    title: Edsger W. Dijkstra, Cooperating Sequential Processes, EWD 123 (1965)
    locator: section 6, The problem of the deadly embrace, and sections 6.1, The Banker's Algorithm, and 6.2, The Banker's Algorithm Applied
  - url: "https://www.cs.utexas.edu/~EWD/ewd01xx/EWD108.PDF"
    title: Edsger W. Dijkstra, EWD 108, a note in Dutch on the prevention of the deadly embrace
    locator: the whole note, for one kind of resource
  - paper: doi:10.1145/363156.363160
    title: A. N. Habermann, Prevention of system deadlocks, Communications of the ACM 12(7), 1969, pages 373 to 377 and 385
    locator: the safe state and the test for several types of resources
  - paper: doi:10.1007/978-1-4612-5695-3_54
    title: Edsger W. Dijkstra, The mathematics behind the Banker's Algorithm, EWD 623 (1977), in Selected Writings on Computing, A Personal Perspective, Springer, 1982, pages 308 to 312
    locator: the whole note, for one kind of resource
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition (2018)
    locator: Chapter 8, Deadlocks, the sections on safe state, the banker's algorithm, the safety algorithm, and the resource-request algorithm
---

The banker's algorithm is a method of deadlock *avoidance*. Each process declares in advance the most units of each resource type it may ever hold, its *maximum claim*. The system grants a request only if, after the grant, there is still an order in which every process could get its full claim and finish. Such a state is *safe*, and a system that stays in safe states never reaches a [deadlock](/deadlock/). Dijkstra described it for one kind of resource around 1965, with a banker who lends money to customers. Habermann (1969) gave the form for several resource types.

## In plain words

A banker has a fixed amount of money. Each customer says up front the most it will ever borrow. A customer borrows in parts, and pays everything back once it has borrowed its full amount and finished its business.

When a customer asks for more, the banker does not look only at the cash in the safe. The banker asks: if I lend this, can I still find an order of customers such that the first can get its full amount from the cash I have, pay back, then the second can get its full amount, and so on to the last? If yes, the banker lends. If no, the customer waits, even when the cash is there.

A computer does the same with memory, devices or locks. The order is a plan, not a promise of what happens. It only shows that a way out exists.

## The problem

A system has $n$ processes and $m$ resource types, with $t(r)$ units of type $r$. Units are reusable and are lent, not used up.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j$ are process indices |
| $m$ | the number of resource types (the shared objects) |
| $t$ | the vector of total units |
| $\mathit{max}[i]$ | the maximum claim of process $i$, with $\mathit{max}[i] \le t$ |
| $\mathit{alloc}[i]$ | the units that $i$ holds now |
| $\mathit{need}[i]$ | $\mathit{max}[i] - \mathit{alloc}[i]$, what $i$ may still ask for |
| $\mathit{avail}$ | $t - \sum_i \mathit{alloc}[i]$, the free units |

For vectors, $x \le y$ means $x[r] \le y[r]$ for every type $r$.

The model has asynchronous processes and one allocator. Processes call REQUEST and RELEASE, and the allocator runs each call as one atomic step, for example under a [mutex](/mutex/), so the shared tables are sequentially consistent. A process that the allocator refuses waits and asks again later. A process is assumed to keep its declaration: it never asks for more than $\mathit{need}[i]$, and once it holds its full claim it finishes in finite time and releases everything. A process may also release units earlier, or finish without using its full claim.

A state is **safe** if there is an order $i_1, i_2, \ldots, i_n$ of all the processes (a *safe sequence*) such that for every $k$:

$$\mathit{need}[i_k] \le \mathit{avail} + \sum_{s < k} \mathit{alloc}[i_s].$$

That is, $i_1$ can get its full claim from the free units, and each later process can get its full claim from the free units plus what the earlier ones returned. A state that is not safe is *unsafe*. The task is to keep the system in safe states while granting as many requests as possible. The safety property obtained is [deadlock freedom](/deadlock-freedom/): no reachable state is a deadlock.

## The algorithm

```pseudo id=main
SAFE(avail, alloc, need)                ▷ returns a safe sequence, or nil
L1  work ← avail; finish[i] ← false for each i; order ← empty list
L2  repeat
L3      progress ← false
L4      for i ← 0 to n − 1 do
L5          if not finish[i] and need[i] ≤ work then
L6              work ← work + alloc[i]; finish[i] ← true; progress ← true; append i to order
L7  until not progress
L8  if finish[i] for every i then return order else return nil

REQUEST(i, req)                         ▷ requires a safe state
L9   if req ≰ need[i] then error: the process exceeded its claim
L10  if req ≰ avail then return WAIT
L11  avail ← avail − req; alloc[i] ← alloc[i] + req; need[i] ← need[i] − req
L12  if SAFE(avail, alloc, need) ≠ nil then return GRANTED
L13  undo line L11; return WAIT

RELEASE(i, rel)                         ▷ requires rel ≤ alloc[i]
L14  avail ← avail + rel; alloc[i] ← alloc[i] − rel; need[i] ← need[i] + rel
```

**The safety check** (lines L1 to L8). The vector $\mathit{work}$ is the pool of units that would be free if the processes marked finished had run to the end. Line L5 looks for a process whose whole remaining claim fits in the pool. Line L6 assumes that it gets its claim, finishes, and returns all it holds. It is the same loop as the reduction of [deadlock detection](/deadlock-detection/), with $\mathit{need}$ in place of the current requests: detection asks whether the current requests can be met, and the safety check asks whether the worst future requests can be met.

**The request** (lines L9 to L13). A request beyond the claim is an error. A request that does not fit must wait in any case. Otherwise the banker grants it tentatively, runs the safety check, and keeps the grant only if the new state is safe.

**Release** (line L14) can only make a state safer, so it needs no check. A process that waits should retry after each release.

## Example

Three processes and two types, with $t = (3, 3)$:

| process | $\mathit{max}$ | $\mathit{alloc}$ | $\mathit{need}$ |
|---|---|---|---|
| $p_0$ | $(2, 2)$ | $(1, 0)$ | $(1, 2)$ |
| $p_1$ | $(2, 1)$ | $(1, 1)$ | $(1, 0)$ |
| $p_2$ | $(1, 3)$ | $(0, 1)$ | $(1, 2)$ |

So $\mathit{avail} = (1, 1)$. SAFE starts with $\mathit{work} = (1, 1)$. In the first pass, $p_0$ does not fit, since $(1, 2) \not\le (1, 1)$; $p_1$ fits, and $\mathit{work}$ becomes $(2, 2)$; then $p_2$ fits, and $\mathit{work}$ becomes $(2, 3)$. In the second pass $p_0$ fits. The state is safe, with the safe sequence $p_1, p_2, p_0$.

Now $p_0$ asks for $(0, 1)$. It is within its need and fits. After the tentative grant, $\mathit{avail} = (1, 0)$ and $\mathit{need}[0] = (1, 1)$. SAFE finds $p_1$, then $p_0$ (with $\mathit{work} = (2, 1)$), then $p_2$ (with $\mathit{work} = (3, 2)$), so the grant stays.

Next $p_2$ asks for $(1, 0)$. A unit of the first type is free, so the request fits. After the tentative grant, $\mathit{avail} = (0, 0)$, and the needs are $(1, 1)$, $(1, 0)$ and $(0, 2)$. No process fits in $(0, 0)$, so the state would be unsafe. The banker undoes the grant, and $p_2$ waits although the unit is free. If the banker had lent it, and then every process asked for its full claim, no request could be met.

## Correctness

[The proof file](proofs/correctness.md) proves four facts.

1. SAFE returns a sequence if and only if a safe sequence exists, and the sequence it returns is one. The order in which it tries processes does not matter, by the same monotonicity argument as for graph reduction.
2. Every state the banker reaches is safe. REQUEST keeps a grant only after the check, and a release keeps a safe state safe.
3. From a safe state, all processes can finish: let the processes of a safe sequence, in turn, ask for their full remaining claims; the banker grants each request, because the state after it is safe with the same sequence. In particular no state reached under the banker is a deadlock: at any time, the first process of a safe sequence either is running or has a request that the banker grants.
4. An unsafe state need not be a deadlock, and need not lead to one.

For the last fact, take one type with $t = 3$, and two processes $p$ and $q$ with claims $3$ that hold $1$ unit each. The free unit cannot complete either claim, so the state is unsafe. But if $p$ finishes without asking for more and returns its unit, $q$ can get its whole claim and finish, and no deadlock happens. Safety is a guarantee against the worst case of future requests, not a description of a deadlock. The banker is therefore conservative: it refuses some requests that would have done no harm.

## Complexity

The safety check runs at most $n + 1$ passes of at most $n$ tests, each comparing $m$ entries, so it takes $O(m n^2)$ time and $O(m + n)$ extra space. A request costs one check, $O(m n^2)$. A release costs $O(m)$. The tables take $\Theta(m n)$ space.

A faster check keeps, for each type, the processes sorted by their need of that type, and a counter per process of the types for which it already fits; each process enters the pool once, and the scan per type moves forward only. This gives $O(m n \log n)$ per check, as for detection.

With one type ($m = 1$), the state is safe if and only if the processes, sorted by increasing need, form a safe sequence: if any process fits, the one with the least need fits. The check then takes $O(n \log n)$, or $O(n)$ if the sorted order is kept up to date.

## Properties

- **Avoidance, not prevention.** The four [Coffman conditions](/coffman-conditions/) all stay possible. The banker steers around the states from which a deadlock could follow. It needs knowledge of the future, the maximum claims, which [deadlock prevention](/deadlock-prevention/) does not need.
- **Conservative.** Some refused requests would have been harmless, as in the unsafe example.
- **Deadlock freedom, not starvation freedom.** The banker never deadlocks, but its rule says nothing about which waiting process is served next. A process with a large claim can wait while smaller ones are served again and again. A fair retry order is a separate policy.
- **Single allocator.** The check reads the whole state, so all requests go through one serialized allocator.

## Variants and improvements

- **One resource type.** Dijkstra's original banker, with one currency, sorted by need as above.
- **The claim graph.** When every type has one unit, the safety check is equivalent to the absence of a cycle in the [resource allocation graph](/resource-allocation-graph/) with claim edges.
- **An early stop.** The check after a tentative grant to process $i$ can stop as soon as $i$ enters the pool. The state before the grant was safe, and in the pool at that moment $i$ can return everything, including the new units, so the rest of the old safe sequence still works. Proof file, Lemma 3.
- **Detection instead of avoidance.** Most systems that can tolerate rare deadlocks run [deadlock detection](/deadlock-detection/) from time to time, which needs no claims, and recover by aborting a victim.

## When to use it

Use it when processes can state their maximum needs in advance, the number of processes and types is small, and refusing or delaying a request is cheaper than recovering from a deadlock. Batch systems with declared job requirements fit this. General purpose operating systems do not use it for locks or memory, since programs rarely know their maximum needs and the check on every request is too slow for frequent locking.

## Pitfalls

- Dijkstra's names differ from the modern ones. In EWD 123, *need* is the maximum claim, *loan* is the current allocation, and *claim* is what is still to come. Read each source with its own names.
- The check must use the remaining need, $\mathit{max} - \mathit{alloc}$, not the maximum claim.
- A request that fits is not automatically safe. The test of line L10 is not enough.
- The guarantee holds only if every process keeps its declared maximum. A process that asks for more breaks the proof, so line L9 must reject it.
- Unsafe is not deadlocked. Do not report an unsafe state as a deadlock.
- The safety check and the grant must form one atomic step. If two requests are checked concurrently against the same state, both can pass and together lead to an unsafe state.

## Implementations

## History

Dijkstra described the banker in EWD 108, a note in Dutch, and in Cooperating Sequential Processes (EWD 123, 1965), section 6.1, as part of his treatment of the "deadly embrace". He used one currency: a banker with a finite capital in florins lends to customers who declare their need in advance. In section 6.2 he remarks that some of the reasoning no longer holds when more than one type of facility is shared. Habermann (1969) treated the case of several resource types and proved the properties of safe states. Dijkstra returned to the single resource case in EWD 623, "The mathematics behind the Banker's Algorithm" (1977). The name and the form with the matrices $\mathit{max}$, $\mathit{alloc}$ and $\mathit{need}$ are those of operating systems textbooks, for example Silberschatz, Galvin and Gagne.

## References
