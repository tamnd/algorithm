---
tag: 0JT58E
kind: technique
slug: bitstate-hashing
name: Bitstate hashing
aliases:
- Supertrace
- Hash compaction
- bitstate search
area: logic-and-constraints/model-checking
level: advanced
summary: Store the visited set of an explicit-state search as k bits per state in a large bit array, like a Bloom filter, so that far larger state spaces fit in memory at the price of skipping some states.
prereqs: [explicit-state-model-checking, bloom-filter, hash-function, depth-first-search]
see_also: [bloom-filter, bloom-filter-optimal-hash-count, explicit-state-model-checking, state-explosion-problem, birthday-paradox, uniform-hashing-assumption, union-bound, nested-depth-first-search]
sources:
  - paper: "Gerard J. Holzmann, An improved protocol reachability analysis technique, Software, Practice and Experience 18(2), 1988"
    locator: the supertrace algorithm, with one bit per state in a large hash array
  - paper: "Gerard J. Holzmann, An analysis of bitstate hashing, Formal Methods in System Design 13(3), 1998"
    locator: the coverage of bitstate search with several hash functions, and the choice of their number
  - paper: "Pierre Wolper and Denis Leroy, Reliable hashing without collision detection, Computer Aided Verification (CAV 1993), Lecture Notes in Computer Science 697, Springer, 1993"
    locator: hash compaction (a short signature per state in a hash table) and its probability of a missed state
  - paper: "Peter C. Dillinger and Panagiotis Manolios, Fast and accurate bitstate verification for SPIN, SPIN 2004, Lecture Notes in Computer Science 2989, Springer, 2004"
    locator: the Bloom filter view of bitstate hashing, and cheap ways to compute many hash positions
  - book: isbn:9780321228628
    title: Gerard J. Holzmann, The SPIN Model Checker, Primer and Reference Manual, Addison-Wesley, 2003
    locator: Chapter 9, Search optimization (bitstate hashing, hash compaction, and how to read the coverage statistics)
---

Bitstate hashing, also called *supertrace*, is a way to store the set of visited states of an [explicit-state](/explicit-state-model-checking/) search in very little memory. Instead of keeping each state, the search sets $k$ bits of a large bit array, at positions given by $k$ hash functions of the state, and it treats a state as visited when all its $k$ bits are already set. The array is a [Bloom filter](/bloom-filter/) of the visited set: it never forgets a visited state, but it can wrongly report an unvisited state as visited, and the search then skips it together with the states that only it leads to. So the search is sound, every error it reports is real, but incomplete, and the probability of skipping a state can be bounded under the [uniform hashing assumption](/uniform-hashing-assumption/). Holzmann introduced it in 1987 and 1988 for protocol verification, and it is a standard option of the SPIN model checker.

## In plain words

An exhaustive search must remember every state it has seen, so that it does not explore the same state twice. Each state may take a hundred bytes, and a large system has billions of states, so the memory runs out long before the search ends.

Bitstate hashing remembers each state as a few bits in one long row of bits. A state is turned into a few positions by hash functions, and the search switches those bits on. A new state whose bits all happen to be on already is taken as old, and the search skips it. This mistake is rare when the row is long, and it never causes a false error report. It only means that some states may not be checked. With the same memory, the search covers far more states than an exact search could.

## When it applies

Use bitstate hashing for a search of reachable states, with a property checked in each state (an invariant, deadlocks, assertions), or with a [nested depth-first search](/nested-depth-first-search/) for liveness, when:

- the reachable state space is too large to store exactly, even with compression;
- an incomplete answer is useful, as when the goal is to find bugs: a clean run is evidence, not proof;
- the hash functions behave like random functions on the states of the model, which good hash functions of the state vector give in practice.

It does not apply when a proof that the property holds is required. Then use exact storage, a reduction such as [partial-order reduction](/partial-order-reduction/), or [symbolic model checking](/symbolic-model-checking/).

## The template

The array has $m$ bits, all $0$ at the start. The holes are in capitals.

```pseudo id=main
BITSTATE-DFS(s₀, NEXT, P)
L1  TEST-AND-SET(s₀)
L2  stack ← [an iterator over NEXT(s₀)]
L3  while the stack is not empty do
        t ← the next successor from the top iterator;  if there is none, pop and continue
L4      if TEST-AND-SET(t) then continue           ▷ all its bits were set: taken as visited
        if not P(t) then report the stack as a counterexample
L5      push an iterator over NEXT(t)

TEST-AND-SET(s)                                    ▷ true if all k bits were set already
    seen ← true
L6  for j ← 1 to K do h ← HASH_j(s) mod M
L7      if bit h is 0 then set bit h to 1;  seen ← false
    return seen
```

The holes:

- **M.** The size of the bit array, as large as the memory allows. With $2^{32}$ bits, $512$ MiB, the array has room for about $10^8$ states with few omissions, where an exact table at 100 bytes per state would need 10 GB.
- **K.** The number of hash functions. Holzmann's first supertrace used $k = 1$; SPIN later used more. For $n$ states the Bloom filter is most accurate at $k \approx (m/n) \ln 2$, see [the optimal number of hash functions](/bloom-filter-optimal-hash-count/), but each extra function costs time, and $k = 2$ to $4$ already gives most of the gain.
- **HASH.** $k$ hash functions of the state vector, such as $k$ slices of one long hash, or two hashes combined as $h_1 + j h_2$ (Dillinger and Manolios).
- **P and NEXT.** As in [explicit-state model checking](/explicit-state-model-checking/).

### Example

Take three counters modulo $4$ that move one at a time: $4^3 = 64$ reachable states. With $m = 2^{16}$ bits and $k = 2$ the search finds all 64 states. With $m = 64$ bits and $k = 1$, one bit per possible state on average, collisions are frequent and the search covers only part of the states; each state it reports is reachable.

For a system of $81$ states (four counters modulo $3$), the bound below says that the search is complete with probability at least $0.802$ for $m = 2^{14}$ and $k = 1$, at least $0.958$ for $m = 2^{12}$ and $k = 2$, and at least $0.995$ for $m = 2^{12}$ and $k = 3$: with a quarter of the memory, more hash functions give more confidence.

For a large model with $n = 10^8$ states and $m = 2^{32}$ bits, the Bloom estimate $\sum_j (1 - e^{-kj/m})^k$ of the number of new states wrongly taken as visited is about $1.2 \cdot 10^6$ for $k = 1$ (about 1.2% of the states), $7 \cdot 10^4$ for $k = 2$, $7.8 \cdot 10^3$ for $k = 3$ and $1.3 \cdot 10^3$ for $k = 4$. This counts only the first omission of each state; states reachable only through omitted states are lost as well, so it is an estimate, not a bound.

### Why it is correct

**Soundness.** The search only follows NEXT from $s_0$, so every state it explores is reachable, and the DFS stack is a real path. A reported violation of $P$ is a real error with a real counterexample.

**What can go wrong.** TEST-AND-SET never answers "new" for a state already explored, since its bits stay set; so no state is explored twice, and the search ends after at most as many steps as the exact search. It can answer "seen" for a new state $t$ when all $k$ bits of $t$ were set by other states. The search then skips $t$, and also each state whose only paths from $s_0$ go through skipped states.

**The probability of a complete search.** Assume that the $k$ hash values of each state are uniform on $\{0, \ldots, m - 1\}$ and independent, for different states and different $j$. Let $s_1, s_2, \ldots, s_n$ be the reachable states in the order in which the same search with an exact visited set first tests them. As long as no new state has been wrongly skipped, the bitstate search makes exactly the same moves, so its $j$-th new state is $s_j$, and before $s_j$ is tested at most $k(j - 1)$ bits are set, all by $s_1, \ldots, s_{j-1}$. The state $s_j$ is wrongly skipped only if each of its $k$ positions falls among these bits; as its hash values are independent of those of earlier states, this has probability at most $(k(j - 1)/m)^k$. By the [union bound](/union-bound/) over $j$:

$$\Pr[\text{the search explores every reachable state}] \;\ge\; 1 - \sum_{j=1}^{n} \left(\frac{k(j - 1)}{m}\right)^{k}.$$

For $k = 1$ this is $1 - n(n - 1)/(2m)$, the [birthday](/birthday-paradox/) bound: one bit per state needs $m \gg n^2$ for a guarantee. For larger $k$ the sum is about $k^k n^{k+1} / ((k + 1) m^k)$, so the guarantee holds with far fewer bits. The bound is pessimistic, since it counts every set bit as a possible collision; the Bloom estimate $(1 - e^{-k(j-1)/m})^k$ for the $j$-th state is the usual approximation of the same probability.

### Size and time

Memory is $m$ bits plus the DFS stack, whatever the size of a state. Time is $O(k)$ hash computations per transition, plus the cost of NEXT, and the number of explored states is at most the number of reachable states. There is no table to resize or to search, so a bitstate search is often faster per state than an exact one. The price is incompleteness: the coverage depends on the ratio $m/n$ and on $k$, and it cannot be known exactly without the exact search. As with every reduction, the worst case of the [state explosion problem](/state-explosion-problem/) is unchanged; bitstate hashing only changes the constant per state.

## Classic examples

- **SPIN.** The option for bitstate search (supertrace) stores the states in a bit array of a size chosen by the user, with a configurable number of hash functions, and reports statistics that indicate the coverage.
- **Murphi.** Stern and Dill used *hash compaction* in the Murphi verifier: a hash table holds a short signature of each state instead of the state, which is a middle ground between exact storage and one bit per state.
- **Swarm verification.** Holzmann, Joshi and Groce run many small bitstate searches in parallel, each with different hash functions and search orders. Since each run skips different states, their union covers far more states than one run with the same total memory.
- **Bug hunting in protocols.** Holzmann's first uses of supertrace found errors in protocol models whose full state spaces could not be stored.

## Variations

- **Hash compaction** (Wolper and Leroy 1993; Stern and Dill 1995). Store a $b$-bit signature of each state in a hash table with collision resolution. Two of $n$ states share a signature with probability at most $n(n - 1)/2^{b+1}$, by the birthday bound, so 64-bit signatures make an omission very unlikely for $10^8$ states.
- **Sequential runs.** Repeat the bitstate search with independent hash functions. A state is missed by all $r$ runs only if it is missed by each; the coverage grows quickly with $r$.
- **Bitstate nested search.** Two bits per state slot, or two arrays, record whether a state has been seen by the outer and by the inner search of [nested depth-first search](/nested-depth-first-search/); CVWY designed their algorithm to work with bitstate storage.
- **Breadth-first bitstate search.** The same array can serve a breadth-first search, which finds shorter counterexamples but needs a queue of full states.
- **State-space caching.** Keep only part of the visited states, and evict some when memory is full. No state is missed, but evicted states can be explored many times; [sleep sets](/sleep-sets/) remove most of these repeated visits.

## Pitfalls

- **Reading a clean run as a proof.** A bitstate search that finds no error has not shown that there is none. Report the coverage estimate, and use exact storage when a proof is needed.
- **An array that is too small.** With $m$ close to $n$ and $k = 1$, a large share of the states is skipped, and the search may stop early with no warning. Check the number of set bits at the end: if more than a small fraction of the array is set, the run is not reliable.
- **Too many hash functions.** For a fixed $m$, more hash functions fill the array faster. Past the optimum $k \approx (m/n) \ln 2$, coverage gets worse.
- **Correlated hash functions.** The analysis assumes independent hash values. Hash functions that depend on few bits of the state vector, or $k$ functions that are shifts of one another, collide far more often.
- **Fairness and cycles.** In a nested search for liveness, a skipped state can hide an accepting cycle; a found cycle is still real.

## Exercises

1. For $n = 10^4$ states and $m = 2^{27}$ bits, compute the bound of the page for $k = 1$, $2$ and $3$. For which $k$ is it above $0.99$?
2. Show that for $k = 1$ the bound is $1 - n(n - 1)/(2m)$, and find the smallest $m$ for which it is at least $1/2$ when $n = 10^6$.
3. Explain why the bitstate search never explores a state twice, and conclude that it terminates on every finite system.
4. Two runs with independent hash functions each skip a given state with probability $q$. What is the probability that the union of the runs skips it? Why is the true coverage of two runs less easy to compute than this?

## References
