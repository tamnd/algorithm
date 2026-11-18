---
tag: 482Z67
kind: algorithm
slug: sase-event-matching
name: NFA-based event pattern matching (SASE)
aliases:
- SASE
- NFA with match buffer
area: databases/stream-and-incremental-processing
level: research
summary: "Evaluate event sequence patterns with an automaton over the stream and a shared buffer of partial matches, then apply predicates and windows."
solves: [complex-event-processing]
model: word-ram
complexity:
  vars: {k: the number of positive components of the pattern, n: the number of events of one partition in the last W time units, M: the number of matches that end with the current event}
  time: {worst: "O(k^2 M + k n)", amortized: "O(k^2 M + k)"}
  space: {extra: "O(k n)"}
properties: {deterministic: true, exact: true, online: true, external: false, in_place: false, recursive: true}
history:
  year: 2006
  people: [Eugene Wu, Yanlei Diao, Shariq Rizvi]
  note: "SASE came from work on complex event processing over RFID streams. SASE+ (Agrawal, Diao, Gyllstrom and Immerman, 2008) added Kleene closure, the NFA with a match buffer and four event selection strategies."
prereqs: [stack, depth-first-search, nondeterministic-finite-automaton, complex-event-processing]
see_also: [nfa-simulation, regular-expression, kleene-star, event-time-watermark, continuous-query, time-based-window, sliding-window-join, symmetric-hash-join]
sources:
  - paper: doi:10.1145/1142473.1142520
    title: "Eugene Wu, Yanlei Diao and Shariq Rizvi, High-performance complex event processing over streams, Proceedings of ACM SIGMOD 2006, pages 407 to 418"
    locator: "the SASE language with SEQ, negation, WHERE and WITHIN, the query plan with sequence scan and construction over active instance stacks followed by selection, window, negation and transformation, and the optimizations that push the window and the equivalence tests into the scan with partitioned stacks (general locator)"
  - paper: doi:10.1145/1376616.1376634
    title: "Jagrati Agrawal, Yanlei Diao, Daniel Gyllstrom and Neil Immerman, Efficient pattern matching over event streams, Proceedings of ACM SIGMOD 2008, pages 147 to 160"
    locator: "the SASE+ language with Kleene closure, the NFA with a shared match buffer, and the event selection strategies strict contiguity, partition contiguity, skip till next match and skip till any match (general locator)"
  - paper: doi:10.1145/2187671.2187677
    title: "Gianpaolo Cugola and Alessandro Margara, Processing flows of information: from data stream to complex event processing, ACM Computing Surveys 44(3), 2012, article 15"
    locator: the survey of event processing languages and of automaton-based detection, which places SASE among the systems that use automata (general locator)
---

SASE, by Wu, Diao and Rizvi (2006), finds sequence patterns such as "an item leaves a shelf, then passes the exit, with no checkout in between, all within 12 hours" in a stream of events. Its matcher reads the stream like a [nondeterministic automaton](/nondeterministic-finite-automaton/) with one state per component of the pattern, but it keeps the partial matches in shared *active instance stacks*. Each stack entry points to the newest entry of the previous stack, and the matches are built from these pointers by a [depth-first search](/depth-first-search/) at the moment their last event arrives. Predicates, the time window and negation are then checked on each match, and the window and equality tests are pushed into the stacks to prune them early.

## In plain words

You watch a stream of events and must report every time an A was followed later by a B and then by a C within five minutes. Other events may come in between. Keep one pile of cards for A, one for B and one for C. When a B arrives, put its card on the B pile and write on it how many A cards were on the A pile at that moment: any of those A cards can come before this B. Do the same for C with the B pile. When a C arrives, follow its note to the B cards that came before it, then their notes to the A cards, and read out each chain. Throw away cards older than five minutes. A chain is found once, when its C arrives.

## The problem

The input is a stream of events in time order, each with a type, a timestamp and attributes. A pattern in the core of the SASE language has the form

```text
EVENT SEQ(E_1 e_1, ..., E_k e_k)  WHERE conditions  WITHIN W
```

where some components may be negated, written $!(E\ e)$. A match is a choice of events $e_1, \dots, e_k$ with the given types, in stream order, with $e_k.ts - e_1.ts \le W$, that satisfies the conditions, and with no event of a negated type, satisfying its conditions, between its neighbours. This is the problem of [complex event processing](/complex-event-processing/) for sequence patterns. SASE uses the selection that SASE+ later called *skip till any match*: other events may lie between the events of a match, and every combination is reported, so one event can be part of many matches. Conditions of the form $e_1.\mathrm{id} = e_2.\mathrm{id} = \cdots$ are *equivalence tests*; they say that a match is about one object.

## The algorithm

```pseudo id=main
SASE(SEQ(E_1, ..., E_k) WITHIN W)            ▷ stack i holds instances of E_i; each entry is (event, RIP)

PUSH(e)                                      ▷ events come in timestamp order
L1  S ← the stacks of the partition of e     ▷ one set of stacks per value of the equivalence attribute
L2  drop the entries older than e.ts - W from the bottom of every stack of S; keep e if its type is negated
L3  for i ← k down to 1 with E_i = type of e do
L4      if i = 1 or stack i - 1 of S is not empty then
L5          push (e, RIP = the index of the top of stack i - 1) onto stack i
L6          if i = k then CONSTRUCT(e)

CONSTRUCT(e)
L7  for each path from e that steps from an entry of stack i to an entry of stack i - 1 at or below its RIP, down to stack 1 do
L8      if the path fits the window, no negated event lies between its neighbours, and the WHERE conditions hold then
L9          emit the path in stream order as a match
```

The automaton has one state per positive component. An event of type $E_i$ moves a run from state $i - 1$ to state $i$, and a run may also stay in its state when an event does not fit. A plain automaton would copy a run for each choice; the stacks share all runs: an entry on stack $i$ stands for every run that reached state $i$ with this event, and its RIP stands for all the runs that it extends.

Line L3 goes from the last component down, so an event whose type occurs twice in the pattern does not extend a run with itself. The search of line L7 tries the candidates from the top of the RIP range down and stops at the first one from which it finds no path; the correctness proof shows that the lower ones cannot have a path either.

## Example

The pattern is $\mathrm{SEQ}(a, b, c)$ WITHIN 5, without equivalence tests. The stream is $a@1, b@2, a@3, c@4, b@5, c@6, c@9$, and the stacks count their entries from 0.

| event | stack a | stack b (RIP) | stack c (RIP) | matches |
|---|---|---|---|---|
| a@1 | a@1 | | | |
| b@2 | a@1 | b@2 (0) | | |
| a@3 | a@1, a@3 | b@2 (0) | | |
| c@4 | a@1, a@3 | b@2 (0) | c@4 (0) | (a@1, b@2, c@4) |
| b@5 | a@1, a@3 | b@2 (0), b@5 (1) | c@4 (0) | |
| c@6 | a@1, a@3 | b@2 (0), b@5 (1) | c@4 (0), c@6 (1) | (a@1, b@5, c@6), (a@3, b@5, c@6), (a@1, b@2, c@6) |
| c@9 | | b@5 (1) | c@4 (0), c@6 (1), c@9 (1) | none |

At c@4, the RIP of c@4 is 0, so the only candidate is b@2, whose RIP 0 gives a@1; the entry a@3 came after b@2 and is above its RIP. At c@6, the search tries b@5 first, whose RIP 1 allows both a@3 and a@1, and then b@2. At c@9, the pruning of line L2 removes every entry older than 4, which is a@1, a@3 and b@2. The entry b@5 remains, but its RIP range on stack a is now empty, so the search stops at once.

With the negation $\mathrm{SEQ}(a, !b, c)$ WITHIN 5 on the same stream, the only match is (a@3, c@4). The pairs (a@1, c@4), (a@1, c@6) and (a@3, c@6) each have a $b$ between them, and c@9 is more than 5 after both $a$ events.

The SASE papers use as an example a shoplifting query over RFID readings: a SHELF reading, then an EXIT reading for the same tag, with no COUNTER reading for that tag in between, within 12 hours. The equality on the tag is an equivalence test, so each tag gets its own stacks.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md); every statement there is a theorem for the code on this page.

- **RIP.** The entries of stack $i - 1$ at or below the RIP of an entry are exactly the entries that came before it.
- **Completeness.** Each event of a window match is on its stack when the last event arrives, because the window keeps it from being pruned and the earlier events of the match make each stack non-empty when the next one arrives.
- **Search.** A lower entry on a stack has a smaller RIP, so if it has a path to stack 1, every entry above it has one too. So the search, which stops at the first candidate without a path, still finds all paths, and each path once.
- **Theorem.** Every match is emitted exactly once, at the arrival of its last event. The negation test is exact because the negated events between two events of a match are not older than the first event of the match, so pruning keeps them.

## Complexity

Costs are per event in the word RAM, for one partition.

- **Theorem.** The search of a construction visits at most $k^2 M + k$ entries, where $M$ is the number of window matches that end with the event. So its cost is output-sensitive: it never follows a path that does not end in a window match, apart from one failed probe per entry on a match path. This is a worst-case bound per event.
- **Pushes and pruning.** Lines L3 to L5 cost $O(k)$ per event. Line L2 may remove up to $k n$ entries in one step, which is the worst case, but each entry is removed once, so it costs $O(1)$ amortized per pushed entry.
- **Space.** Each event of the last $W$ time units is on at most $k$ stacks, so the stacks use $O(k n)$ space for a partition with $n$ such events.
- **The output.** With skip till any match, the number of matches can grow as $n^k$ in a window of $n$ events, so no algorithm can report them all in less time. This is the reason for the more selective strategies of SASE+.
- **The paper's measurements.** Wu et al. report experiments on the effect of pushing the window and the equivalence tests into the stacks. These are measurements, and this page does not repeat their numbers.

## Properties

- **Online.** A match is emitted as soon as its last event arrives, and no earlier time is possible, since the match is not complete before.
- **Exact and deterministic** for a stream in timestamp order.
- **Late data.** The stacks and the RIP pointers need the events in timestamp order. The code on this page refuses an event that is older than the previous one. A stream with bounded disorder goes through a K-slack buffer first: it holds each event until an event at least $D$ time units newer has arrived, and then releases the events in order. The tests shuffle the stream within a bounded delay with a seeded generator, pass it through the buffer, and get the same matches as on the sorted stream. Each match is then reported up to $D$ time units later. An event later than $D$ breaks the order, so a system must drop it, count it, or send it to a side output; it cannot join a match whose last event was already processed.

## Variants and improvements

- **Pushing the window down.** Without pruning, the stacks grow with the whole stream and the search builds sequences that the window test later rejects. Pruning by $e.ts - W$, as in line L2, is the SASE optimization that pushes the window into the scan.
- **Partitioned stacks.** With an equivalence test, one set of stacks per value of the attribute keeps unrelated events apart, so the RIP ranges hold only candidates that pass the test. This is the other main optimization of the paper.
- **SASE+ and the match buffer.** SASE+ (2008) adds Kleene closure, written $E+$, and four event selection strategies: strict contiguity (the events of a match are adjacent in the stream), partition contiguity (adjacent within the partition), skip till next match (irrelevant events are skipped, but a relevant event is not ignored), and skip till any match. Its automaton, an NFA with a buffer, keeps the runs of the automaton and stores their events in one shared match buffer, so that runs with a common prefix share it. This page does not give the details of that buffer, because it could not confirm them.
- **Other engines.** Cayuga, ZStream and the CEP libraries of stream processors such as Flink use other automata or trees of operators. The [complex event processing](/complex-event-processing/) page compares the main approaches.

## When to use it

Use the stack-based scheme for sequence patterns with time windows where many combinations are wanted, for example in monitoring, fraud detection and RFID tracking, and where the events can be ordered by time first. Use a selection strategy such as skip till next match when only the first or a few matches per start event matter, because skip till any match can produce very many matches. For patterns that are plain joins over windows, a [sliding window join](/sliding-window-join/) may be simpler.

## Pitfalls

- **Too many matches.** Skip till any match reports every combination, which can be exponential in $k$. Set the window and the selection strategy with care.
- **Negation at the ends.** A negation before the first or after the last positive component needs a different rule: the code on this page allows negation only between two positive components, and a trailing negation can be decided only when the window has passed.
- **Equal timestamps.** Events with the same timestamp need a fixed order, such as the order of arrival or an event id, or the meaning of "followed by" is not defined.
- **Predicates checked late.** Conditions that are checked only after the search cost time for every rejected match. Push equivalence tests into the partitions, and simple conditions on one event into the scan.
- **Disorder.** Feeding out-of-order events into the stacks gives wrong RIP ranges. Reorder first, with a bound on the delay.

## Implementations

This page did not confirm the details of the authors' implementation. The Python code on this page has the stacks with RIP pointers, the pruning by the window, partitioned stacks for one equivalence attribute, negation between positive components, a predicate on the whole match, and a K-slack buffer for bounded disorder. Its tests compare the matches with a brute-force search over all tuples of events, check that each match is emitted at the arrival of its last event, and check the bound on the number of visited entries.

## History

Wu, Diao and Rizvi presented SASE at SIGMOD 2006, with the language, the plan of a sequence scan followed by selection, window, negation and transformation, and the optimizations for windows and equivalence tests. Agrawal, Diao, Gyllstrom and Immerman extended the language with Kleene closure in SASE+ at SIGMOD 2008, with a formal automaton model and the event selection strategies. Cugola and Margara (2012) surveyed this line of work together with data stream systems.

## References
