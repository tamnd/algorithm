---
tag: EX8YJV
kind: problem
slug: distributed-grep
name: Distributed grep
aliases:
- parallel grep
- pattern search over a cluster
area: parallel/mapreduce-and-bsp
level: intro
summary: Report every line of a very large text that matches a pattern, as a map-only MapReduce job with no shuffle beyond the matches.
prereqs: [mapreduce-model, grep]
see_also: [regex-search, thompson-nfa-simulation, string-matching, aho-corasick, boyer-moore, parallel-map, word-count, shuffle-phase]
sources:
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 2.3 (distributed grep, the map emits a matching line and the reduce is the identity) and Section 5.2 (the grep benchmark on 10^10 records)
  - book: isbn:9781491901632
    title: Tom White, Hadoop, The Definitive Guide, fourth edition, O'Reilly, 2015
    locator: Chapter 8 (MapReduce Types and Formats), the part on input splits and text input, where a split reads past its end to finish its last line
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020
    locator: Section 2.2 (MapReduce, map tasks and the case with no reduce work) and Section 2.5 (the communication-cost model)
---

Distributed grep is the problem of reporting every line of a very large text that matches a pattern, using many machines. Dean and Ghemawat give it as the simplest [MapReduce](/mapreduce-model/) example (Section 2.3): the map function emits a line when it matches, and the reduce function is the identity. Each machine scans its own part of the input, so the job is a [parallel map](/parallel-map/) with one pass over the data and no [shuffle](/shuffle-phase/) beyond the matching lines. It is the single-machine [grep](/grep/) made parallel, and its cost is the cost of reading the input.

## In plain words

You have a huge log file spread over many computers and you want all lines that contain some pattern, for example the lines that start with "error". Each computer looks through the lines it already holds and keeps the ones that match. No computer needs anything from another one, because each line can be checked on its own. The answer is the kept lines, read in file order. The only data that must move is the answer itself, and if the answer can stay in pieces, nothing moves at all. The one detail to get right is a line that crosses the border between two pieces: exactly one computer must check it.

## Definition

**Input.** A text $T$ of $N$ bytes, a sequence of lines separated by newline characters, and a pattern $Q$ (a fixed string or a [regular expression](/regex-search/)).

**Output.** The list of pairs (offset, line) for each line of $T$ that contains a match of $Q$, in increasing offset.

**Cost model.** The [MapReduce model](/mapreduce-model/): rounds, the pairs and bytes of the [shuffle](/shuffle-phase/), and the work of the map tasks. Let $K$ be the number of matching lines and $B_K$ their total size in bytes. The input is cut into $M$ splits of about $N/M$ bytes.

## Variants

- **Map-only job.** With zero reduce tasks, which Hadoop allows, each map task writes its matches to its own output file and nothing is shuffled. The output is $M$ files whose concatenation in split order is the answer.
- **One reduce task.** Dean and Ghemawat's form, with the identity reduce and $R = 1$. The shuffle carries exactly the $K$ matches, and the output is one file sorted by key.
- **Counting only (grep -c).** Each map task counts its matches and sends one pair, so the shuffle has $M$ pairs. This is [word count](/word-count/) with one key and a [combiner](/combiner/).
- **Many patterns.** For a set of fixed strings, each map task runs [Aho-Corasick](/aho-corasick/) once over its split instead of one scan per pattern.
- **Matches that cross lines.** For a fixed string of length $m$ in a text with no line structure, split $[a, b)$ reads up to byte $b + m - 2$ and reports only the matches that start in $[a, b)$. Every occurrence starts in exactly one split and ends at most $m - 1$ bytes after its start, so each occurrence is found exactly once.

## Examples

Take the 39-byte text with the lines "error: disk", "ok", "warn: fan", "error: net", "ok" (each ending with a newline), the pattern "^error", and splits of 10 bytes. A line belongs to the split that holds its first byte. A split that starts inside a line skips to the next line, and a split reads past its end to finish its last line.

| map task | byte range | lines read (offset) | matches |
|---|---|---|---|
| 0 | 0 to 9 | "error: disk" (0) | (0, "error: disk") |
| 1 | 10 to 19 | "ok" (12), "warn: fan" (15) | none |
| 2 | 20 to 29 | "error: net" (25) | (25, "error: net") |
| 3 | 30 to 38 | "ok" (36) | none |

Each of the 5 lines is read once. As a map-only job, the round shuffles 0 pairs. With one reduce task, it shuffles the 2 matching pairs.

**The benchmark of Dean and Ghemawat (Section 5.2).** The input was $10^{10}$ records of 100 bytes (about 1 TB), the pattern was a rare three-character string that occurs in 92,337 records, $M = 15{,}000$ splits of about 64 MB, and $R = 1$. The job took about 150 seconds, including about one minute of startup, and the input rate peaked above 30 GB/s with 1,764 workers. The shuffle was tiny, so the time was the scan plus the startup.

## Known algorithms

**On one machine.** A [grep](/grep/) scans the lines and tests each one. For a fixed string of length $m$, [Knuth-Morris-Pratt](/knuth-morris-pratt/) takes $O(N + m)$ time and [Boyer-Moore](/boyer-moore/) is often sublinear in practice. For a regular expression of size $m$, the [Thompson NFA simulation](/thompson-nfa-simulation/) takes $O(Nm)$ time, and a DFA takes $O(N)$ time after its construction. See [string matching](/string-matching/).

**In MapReduce.** One map task per split runs the one-machine algorithm on the lines of its split. With the line rule of the example (a line belongs to the split that holds its first byte), each line is tested exactly once: the split that holds the first byte reads the whole line even past its end, and every other split skips it. The round costs:

| Measure | Map-only | One reduce task |
|---|---|---|
| rounds | 1 | 1 |
| bytes read | $N$, plus at most one line per split | the same |
| pairs shuffled | 0 | $K$ |
| bytes shuffled | 0 | $B_K$ plus the keys |
| largest reducer input | none | $K$ pairs |
| work | $O(N)$ for a DFA, $O(Nm)$ for an NFA | the same, plus a sort of $K$ pairs |

With $p$ machines that each scan at $\beta$ bytes per second, the map phase takes about $N/(p\beta)$ seconds when the splits are spread evenly, plus the startup of the job.

## Bounds

- **Work.** For a pattern of one character, every byte that is not a newline can decide whether its line matches, so any algorithm reads all $N$ bytes: $\Omega(N)$ work in the worst case. The DFA method meets it.
- **Time on $p$ machines.** At least $N/(p\beta)$ when all bytes must be read, since each machine reads at most $\beta$ bytes per second. The map-only job reaches this up to the imbalance of the splits and the startup cost.
- **Communication.** Zero for the map-only job, which is optimal. If the output must be one file, at least $B_K$ bytes must reach it.
- **Rounds.** One. The map-only round is the best case of the model: replication rate 1 and no reduce.

## Reductions

- Distributed grep is a [parallel map](/parallel-map/) followed by a filter: the lines are independent, so any test that looks at one line at a time runs the same way. Distributed selection in a database (a scan with a predicate) is the same job.
- Counting the matches reduces to [word count](/word-count/) with a single key.
- Single-machine [grep](/grep/), [regex search](/regex-search/) and [string matching](/string-matching/) are the subroutines of the map function.

## Applications

- Searching logs and crawled pages for lines with an error code, a URL or a user id.
- Filtering a large dataset as the first step of a longer pipeline, where the output is the input of a later MapReduce round.
- A benchmark of the scan rate of a cluster, as in Dean and Ghemawat's measurement, since it moves almost no data between machines.

## References
