---
tag: 1JPBJB
kind: problem
slug: interactive-consistency
name: Interactive consistency
aliases:
- vector agreement
- Byzantine interactive consistency
area: distributed/byzantine-agreement
level: core
summary: Every process has a private value, and the correct processes must agree on one vector whose entry for each correct process is that process's value.
prereqs: [byzantine-broadcast]
see_also: [authenticated-resilience-bound, oral-messages-algorithm, dolev-strong-algorithm, byzantine-resilience-bound, byzantine-round-lower-bound, strong-validity, honeybadger-bft, consensus-problem]
sources:
  - paper: doi:10.1145/322186.322188
    title: Marshall Pease, Robert Shostak and Leslie Lamport, Reaching Agreement in the Presence of Faults, Journal of the ACM 27(2), 1980
    locator: pages 228 to 234 (definition of interactive consistency, the algorithm for n >= 3m + 1, the impossibility for n <= 3m, and the authenticated algorithm for any n >= m >= 0)
  - paper: doi:10.1016/0020-0190(82)90033-3
    title: Michael J. Fischer and Nancy A. Lynch, A lower bound for the time to assure interactive consistency, Information Processing Letters 14(4), 1982
    locator: pages 183 to 186 (m + 1 rounds are necessary)
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 1 (interactive consistency from n instances of the Byzantine generals problem, pages 383 to 384)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Section 6.3 (exponential information gathering algorithms for Byzantine agreement)
---

Interactive consistency is the problem in which each of $n$ processes has a private value, and the correct processes must all compute the same vector of $n$ values, where the entry for each correct process is that process's value. Entries for faulty processes may be anything, as long as all correct processes have the same one. Pease, Shostak and Lamport defined it in 1980 for the SIFT fault-tolerant computer, where replicated processors had to agree on all sensor readings. It is solved by $n$ parallel copies of [Byzantine broadcast](/byzantine-broadcast/), one per process, and so it has the same bounds: $n > 3t$ without signatures, any $t < n$ with them, and $t + 1$ rounds.

## In plain words

Each of a group of computers reads its own sensor. Some computers are faulty and may lie in any way. The good computers want to build the same table of readings, one row for each computer. The row of a good computer must hold its true reading. The row of a bad computer may hold any value, but all good computers must hold the same one.

Once all good computers have the same table, each can compute the same answer from it, for example the middle reading. This is why the problem is useful: it turns many private values into one shared view.

## Definition

**Model.** There are $n$ processes on a complete network of reliable links in the [synchronous model](/synchronous-model/), with at most $t$ [Byzantine](/byzantine-failure-model/) processes. Messages are oral or signed.

**Problem.** Each process $p$ has a private value $x_p \in V$. Each correct process $p$ must output a vector $W_p \in V^n$ such that:

- **termination:** every correct process outputs a vector;
- **agreement:** $W_p = W_q$ for all correct $p$ and $q$;
- **validity:** $W_p[q] = x_q$ for all correct $p$ and $q$.

Pease, Shostak and Lamport state the same two conditions: the nonfaulty processors compute exactly the same vector, and the element of this vector that belongs to a given nonfaulty processor is the private value of that processor.

## Variants

- **Byzantine broadcast** is interactive consistency with one entry. The vector of interactive consistency is the result of $n$ broadcasts.
- **Consensus.** Each process decides one value instead of a vector. A process can compute it from the vector, for example by the majority, which gives [strong validity](/strong-validity/) for $n > 2t$, or by the median, which gives median validity for ordered values.
- **Vector consensus in asynchrony.** In the [asynchronous model](/asynchronous-model/) a process cannot wait for up to $t$ slow processes, so the vector may have up to $t$ empty entries. The correct processes agree on a vector with at least $n - t$ filled entries, each of them the value of its process if that process is correct.
- **Agreement on a common subset.** The correct processes agree on a set of at least $n - t$ proposals. [HoneyBadgerBFT](/honeybadger-bft/) uses this form to order transactions.

## Examples

**One equivocating process.** The implementation runs $n = 4$ processes with $t = 1$ and inputs $(0, 1, 2, 0)$. Process 1 is faulty and signs a different value for each correct process. Each correct process then sees two values for entry 1, so the Dolev-Strong instance for process 1 outputs the default 0 at all of them. The correct processes 0, 2 and 3 all output the vector $(0, 0, 2, 0)$. Entries 0, 2 and 3 are the true inputs, and entry 1 is the same at all of them.

**Failure-free cost.** With $n = 4$, $t = 1$ and no faults, the same run ends after 2 rounds with the vector $(0, 1, 2, 0)$ at every process. The correct processes send 36 messages, $n (n - 1)^2$: each of the 4 instances costs $(n - 1)^2 = 9$ messages.

**Too few processes.** With $n = 3$, $t = 1$ and oral messages, no algorithm works. The entry of process $A$ is a broadcast with $A$ as the sender, and the [Byzantine resilience bound](/byzantine-resilience-bound/) shows that this broadcast fails for three processes.

## Known algorithms

| Algorithm | Model | Faults | Rounds |
| --- | --- | --- | --- |
| Pease, Shostak and Lamport 1980 | oral | $n \ge 3t + 1$ | $t + 1$ |
| $n$ parallel copies of [OM(t)](/oral-messages-algorithm/) | oral | $n \ge 3t + 1$ | $t + 1$ |
| Exponential information gathering, Lynch Section 6.3 | oral | $n \ge 3t + 1$ | $t + 1$ |
| Pease, Shostak and Lamport 1980, authenticated | signed | any $t < n$ | $t + 1$ |
| $n$ parallel copies of [Dolev-Strong](/dolev-strong-algorithm/) | signed | any $t < n$ | $t + 1$ |

The algorithm of Pease, Shostak and Lamport builds a tree of reports of the form "$q$ told me that $r$ told him that $x_r$ is ...", as OM(m) does for one sender. The exponential information gathering algorithms in Lynch's book are the same idea in a uniform data structure.

## Bounds

- **Processes.** Without signatures, $n \ge 3t + 1$ is necessary and enough, since one entry is a broadcast. With signatures, any $t < n$ works.
- **Rounds.** Fischer and Lynch (1982) proved that $t + 1$ rounds are necessary, for $t \le n - 2$. This was the first proof of the [round lower bound](/byzantine-round-lower-bound/) for Byzantine faults.
- **Messages.** $n$ broadcasts cost $n$ times the cost of one in the worst case. With Dolev-Strong, the correct processes send $O(n^3)$ messages. Each instance needs $\Omega(n + t^2)$ messages by the [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/).

## Reductions

1. **From broadcast, for any $n$ and $t$.** Run $n$ broadcasts in parallel, with process $q$ as the sender of instance $q$ and $x_q$ as its value. Let $W_p[q]$ be the output of $p$ in instance $q$. Agreement of each instance gives agreement of the vectors. Validity of instance $q$ for a correct $q$ gives $W_p[q] = x_q$. With signatures, each signature must name its instance, so that a chain from one instance is not valid in another one.
2. **To broadcast, for any $n$ and $t$.** Run interactive consistency with the sender's value as its private value, and output entry $s$.
3. **To consensus with strong validity, for $n > 2t$.** Decide the strict majority of the vector, or a default if there is none. If all correct processes have input $v$, at least $n - t > n/2$ entries are $v$.
4. **To consensus with weak validity, for any $n$ and $t$.** Decide entry $p_0$ of the vector.

The implementation checks reduction 1 for $n = 3, 4, 5$ with $t = n - 2$, every faulty set of size at most $t$ and three attack strategies, and reductions 2, 3 and 4 on the cases listed on the [Byzantine broadcast](/byzantine-broadcast/) page.

## Applications

- **Replicated sensors.** In SIFT, each processor read sensors and the processors used interactive consistency to agree on all readings before they computed the next control output. Each correct processor then applies the same function to the same vector.
- **Clock synchronization.** Each process contributes its clock value, and all compute the same correction from the same vector.
- **Consensus with special validity.** For real values, the median of the vector gives median validity, and a trimmed mean gives a value in the range of the correct inputs, see [strong validity](/strong-validity/).
- **Secure multiparty computation.** Many protocols start with every party broadcasting a commitment to its input, which is interactive consistency.

## References
