---
tag: 6GRW00
kind: algorithm
slug: coverage-guided-fuzzing
name: Coverage-guided greybox fuzzing
aliases:
- greybox fuzzing
- coverage-guided fuzzing
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: Mutates inputs from a queue and keeps those that reach new code coverage, measured by lightweight instrumentation.
model: word-ram
complexity:
  vars: {N: the number of executions, T: the largest number of steps of one run, Q: the size of the queue, E: the number of edges of the control flow graph, V: the number of visits of queue entries, k: the number of parameters}
  time: {worst: O(N T + V (Q E + E log E))}
  space: {extra: O(Q (k + E))}
properties: {deterministic: false, randomized: true}
history:
  year: 2013
  people: [Michał Zalewski]
  note: American fuzzy lop (AFL) made edge coverage with hit-count buckets, a queue of interesting inputs and queue culling the standard design of mutation fuzzers.
prereqs: [control-flow-graph]
see_also: [concolic-testing, generational-search, grammar-based-fuzzing, delta-debugging, differential-testing, property-based-testing, markov-chain, set-cover]
sources:
  - url: "https://raw.githubusercontent.com/google/AFL/master/docs/technical_details.txt"
    title: Michał Zalewski, Technical whitepaper for afl-fuzz, AFL documentation
    locator: sections 1 to 6 (coverage measurements, detecting new behaviors, evolving the input queue, culling the corpus, trimming input files, fuzzing strategies)
  - paper: doi:10.1145/2976749.2978428
    title: Marcel Böhme, Van-Thuan Pham and Abhik Roychoudhury, Coverage-based greybox fuzzing as Markov chain, Proceedings of CCS 2016
    locator: pp. 1032 to 1043, the Markov chain model and the power schedules of AFLFast
  - paper: doi:10.1109/TSE.2019.2946563
    title: Valentin J. M. Manès, HyungSeok Han, Choongwoo Han, Sang Kil Cha, Manuel Egele, Edward J. Schwartz and Maverick Woo, The art, science, and engineering of fuzzing, a survey, IEEE Transactions on Software Engineering 47(11), 2021
    locator: pp. 2312 to 2331, the general fuzzing loop and the sections on greybox fuzzing and seed scheduling
  - paper: doi:10.1145/96267.96279
    title: Barton P. Miller, Lars Fredriksen and Bryan So, An empirical study of the reliability of UNIX utilities, Communications of the ACM 33(12), 1990
    locator: pp. 32 to 44, the first fuzz testing study with random inputs
---

Coverage-guided greybox fuzzing tests a program by running it on a very large number of mutated inputs. Light instrumentation tells the fuzzer which edges of the [control flow graph](/control-flow-graph/) each run took and about how often. An input that makes the program do something new, by this measure, goes into a queue, and later inputs are mutations of the inputs in the queue. So the fuzzer climbs step by step into code that blind random inputs almost never reach, without the cost of a solver. This is the design of AFL and of most fuzzers after it. A fuzzer gives no completeness guarantee: when it finds no crash, nothing follows about the program.

## In plain words

Start with a few example inputs. Take one of them, change it a little, and run the program. Each run leaves a trace of the jumps it took between blocks of code, with rough counts. If the trace has a jump, or a count range, that no earlier run had, keep the new input in a list; otherwise throw it away. If the run crashes, save the input for a person to look at. Go through the list again and again, changing each input in many small ways. A program check that needs three exact values in a row is too hard to guess at once, but the fuzzer can pass it one value at a time, because each correct value opens a new jump and so is kept. To save time, prefer the small set of fast inputs that together reach every jump seen so far.

## The problem

The input is a program $P$ of the toy IR with $k$ integer parameters, a list of seed inputs, a budget of $N$ executions and a seed for the random number generator. The output is the queue of kept inputs, the crashing inputs found, and the coverage reached. A crash here is a trap, a division by zero or a shift out of range.

What a fuzzer can promise is limited by decidability. Whether some input reaches a given edge, or a given trap, is undecidable for programs with loops over unbounded integers, by a reduction from the halting problem. For loop-free programs with products over unbounded integers it contains [Hilbert's tenth problem](/hilberts-tenth-problem/). Over a finite box of inputs it is decidable by trying every input, but real input spaces are far too large for that. A fuzzer does not try to decide it. It samples. Every crash it reports is real, because it ran, but a run with no crash proves nothing, and full edge coverage does not mean that every path, or every value on a path, was tested. The tests of this page check only coverage properties of one fixed-seed run, never that a bug or a path is found.

## The algorithm

The instrumentation follows AFL. A run counts how often it takes each edge $(u, v)$ of the control flow graph and puts the count in one of the buckets 1, 2, 3, 4 to 7, 8 to 15, 16 to 31, 32 to 127 and 128 or more. The *coverage* of a run is the set of pairs (edge, bucket). The fuzzer keeps the union of the coverage of all queue entries, AFL's *virgin map*, and a second one for the crashes.

```pseudo id=main
FUZZ(P, seeds, N, rng)
L1  queue <- the seeds, each with its coverage; virgin <- the union of their coverage
L2  while fewer than N runs were made do
L3      for each entry q of queue, in order, including entries added during the walk do
L4          favored <- CULL(queue)
L5          if q is not in favored then skip q with probability 0.9
L6          the first time q is used, try each mutation of the deterministic stage; then try HAVOC(q) 32 times. To try an input x:
L7              (kind, cov) <- run P on x with edge counters
L8              if kind is a trap then save x as a crash if cov has a pair that no crash had
L9              else if kind is a return and cov has a pair not in virgin then
L10                 virgin <- virgin union cov; append x to queue

CULL(queue)
L11 for each edge e covered by the queue, best[e] <- the entry with the fewest steps that covers e (the earliest on ties)
L12 favored <- empty; covered <- empty
L13 for each edge e, in a fixed order: if e is not in covered then add best[e] to favored and its edges to covered
L14 return favored
```

The deterministic stage changes one thing at a time, in a fixed order: it flips each of the low 8 bits of each parameter, adds and subtracts 1 to 35, and sets each parameter to each value of the list $-128, -1, 0, 1, 16, 32, 64, 100, 127$, the 8-bit interesting values of AFL. HAVOC stacks 2 to 8 random changes of the same kinds, plus random values and copies of one parameter into another. In this implementation a run that uses up its fuel is neither kept nor reported.

CULL is AFL's queue culling. For each edge it chooses the cheapest entry that covers it, and a greedy pass picks entries until every edge is covered, a fast approximation of [set cover](/set-cover/). The fuzzer spends most of its time on this favored set, and the other entries are skipped with probability 0.9 on each visit.

## Example

The parameters are $a$, $b$ and $c$. The trap needs three exact values, one after the other.

```
entry:
  t = a == 17
  br t l1 out
l1:
  d = b - a
  t = d == 4
  br t l2 out
l2:
  e = c - 100
  z = a / e
  ret z
out:
  ret 0
```

The trap happens only for $(17, 21, 100)$. A blind random tester that draws each parameter from $-128$ to $127$ hits it with probability $2^{-24}$ per run. With the seed $(0, 0, 0)$, a budget of 20000 runs and the generator seed 0, the fuzzer of this page does this:

| run | input | event | coverage added |
|---|---|---|---|
| 1 | (0, 0, 0) | the seed, 3 steps | `entry`→`out` |
| 58 | (17, 0, 0) | kept, 6 steps | `entry`→`l1`, `l1`→`out` |
| 426 | (17, 21, 0) | kept, 8 steps | `l1`→`l2` |
| 841 | (17, 21, 100) | crash | |

All three steps come from the deterministic stage. Run 58 is the 17th addition to $a$ in the stage of the seed. Run 426 is the 21st addition to $b$ in the stage of $(17, 0, 0)$, which became a queue entry because it took two new edges. Run 841 sets $c$ to the interesting value 100 in the stage of $(17, 21, 0)$. The generator seeds 1 to 4 give the same four lines; the havoc runs in between add nothing to the queue. Blind random testing with the same budget over $[-128, 127]^3$ finds no crash for the seeds 0 to 4, and for the seeds 1 and 3 it does not even take the edge `l1`→`l2`.

The example also shows the limit. Change the constant 100 to 99 and the deterministic stage cannot make it from 0; the fuzzer then depends on havoc and luck. A check against a 32-bit constant or a checksum gives no partial reward at all, and the fuzzer has nothing to climb.

## Correctness

The proof file shows the invariants that the implementation keeps. They are the whole of what the algorithm guarantees.

1. **Every kept input is real.** Each queue entry and each crash was produced by a run of the program, and replaying it gives the same coverage and the same outcome, because the runs are deterministic. In particular every reported crash traps.
2. **The virgin map is exact.** After each run, the virgin map equals the union of the coverage of the queue entries, and each entry after the seeds added at least one new pair when it was added.
3. **The favored set covers the queue.** Every edge covered by some queue entry is covered by some favored entry, so skipping the other entries never hides an edge of the queue from the mutations.
4. **Covered edges are edges of the program.** Each pair names an edge of the control flow graph, so the queue has at most $8E$ entries beyond the seeds: each one adds a new pair, and there are at most 8 buckets per edge.

**No completeness.** None of this says that the fuzzer finds an edge, a path or a trap that some input reaches. The problem it would solve is undecidable in general, and even on a finite box the fuzzer makes random choices with no bound on the number of runs it needs.

## Complexity

Let $N$ be the number of runs, $T$ the largest number of steps of a run, $Q$ the size of the queue, $E$ the number of edges and $V$ the number of queue visits. Each run costs $O(T)$ for the program and the counters, plus $O(E)$ to compare its coverage with the virgin map. Each visit calls CULL, which reads the coverage of every entry, $O(Q E)$, sorts the edges, $O(E \log E)$, and builds the favored set in $O(Q E)$. The total is $O(N T + V (Q E + E \log E))$. Since $Q \le 8E$ plus the seeds, the queue stays small. The space is $O(Q (k + E))$ for the queue.

AFL makes each run much cheaper than this: its map is a fixed array of 64 kB indexed by a hash of the edge, compared with the virgin map word by word, and it culls only after the queue changes. The cost of a fuzzer is dominated by the runs of the target, which is why AFL runs thousands of them per second and avoids anything as slow as a solver.

## Properties

- **Randomized.** The havoc stage and the skipping of entries use random numbers. With a fixed seed the whole run can be repeated exactly.
- **No false alarms.** Every reported crash is a real run of the program.
- **No completeness.** A run of any length can miss an edge, a path or a crash; the fuzzer never says that none exists.
- **Edge coverage, not path coverage.** Two runs with the same edges and buckets look the same, though their paths can differ. The buckets also merge counts: a loop of 4 and a loop of 7 trips give the same coverage.
- **Monotone queue.** Entries are only added, and each one added a new pair.

## Variants and improvements

- **Power schedules.** Böhme, Pham and Roychoudhury model the fuzzer as a [Markov chain](/markov-chain/) whose states are paths, and observe that AFL spends most runs on a few high-frequency paths. AFLFast assigns more mutations to entries that reach rarely seen paths. Seed scheduling is also studied as a [multi-armed bandit](/multi-armed-bandit/) problem.
- **Hashed edge maps.** AFL computes the index of an edge as the hash `cur_location ^ prev_location`, with `prev_location` shifted right by one after each block, into a 64 kB array. Collisions can hide new edges. This page uses exact edges, which a small toy program allows.
- **Trimming.** AFL shortens each new queue entry by removing blocks of the input as long as the coverage stays the same, a cheap relative of [delta debugging](/delta-debugging/).
- **Structure-aware mutation.** Dictionaries of tokens and [grammar-based fuzzing](/grammar-based-fuzzing/) produce inputs that pass the parser of the program.
- **Hybrid fuzzing.** When coverage stops growing, a [concolic](/concolic-testing/) or [generational](/generational-search/) engine solves the path condition of a queue entry to pass a narrow check, such as a magic number, and gives the result back to the fuzzer.
- **Oracles.** A crash is the cheapest oracle. Sanitizers turn silent memory errors into crashes, and [differential testing](/differential-testing/) compares two implementations on each input.

## When to use it

Use coverage-guided fuzzing on code that parses or transforms untrusted input, such as file formats, network protocols, compilers and libraries with a byte-buffer interface. It needs only a way to run the program many times quickly and to measure coverage, and it scales to large programs where symbolic methods time out. Start with small valid seeds. Add a solver-based tool when coverage stops at checks of exact values, and use a verifier when you need a proof: a fuzzer never gives one.

## Pitfalls

- **Reading "no crash" as "no bug".** A fuzzing campaign gives evidence, never a proof. Report it as coverage reached in a given time.
- **Magic values and checksums.** A comparison of many bytes at once gives no partial coverage. Split the comparison, add a dictionary, or use a solver.
- **Coverage is not behavior.** Two inputs with the same edge coverage can compute different values, and a bug can hide in a value on a covered path.
- **Nondeterministic targets.** If the coverage of a run depends on time, threads or global state, the fuzzer keeps inputs that are not new and the queue grows with noise.
- **Comparing fuzzers on one run.** Results vary a lot with the seed. Compare many runs with a statistical test.
- **Seeds that crash or hang.** A seed that traps adds nothing to the queue and wastes the stage; check the seeds first.

## Implementations

## History

Fuzz testing started with the study of Miller, Fredriksen and So in 1990, who fed random characters to UNIX utilities and crashed or hung between a quarter and a third of them. Random testing of that kind is blackbox. Michał Zalewski released American fuzzy lop (AFL) in 2013. Its contribution was a practical combination: compile-time edge instrumentation into a small shared map, hit-count buckets, a queue of inputs that add coverage, deterministic stages followed by havoc, and queue culling. AFL found many bugs in widely used libraries and made the design the default; libFuzzer, honggfuzz and AFL++ follow it. Böhme, Pham and Roychoudhury gave it a Markov chain model in 2016. The survey of Manès and others (2021) places greybox fuzzing between blackbox random testing and whitebox methods such as [generational search](/generational-search/).

## References
