---
tag: GPGX6R
kind: algorithm
slug: re-pair
name: Re-Pair
aliases:
- RePair
- recursive pairing
area: compression-and-coding/dictionary-compression
level: advanced
summary: Repeatedly replaces the most frequent pair of adjacent symbols with a new nonterminal, an off-line grammar compressor.
model: word-ram
complexity:
  vars: {n: the input length}
  time: {expected: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1999
  people: [N. Jesper Larsson, Alistair Moffat]
  note: Presented at the Data Compression Conference in 1999, with the journal version in the Proceedings of the IEEE in 2000.
prereqs: [grammar-based-compression, priority-queue, doubly-linked-list, hash-table]
see_also: [straight-line-program-grammar, smallest-grammar-problem, byte-pair-encoding, sequitur, bucket-queue, lz78, compressed-indexing, smallest-grammar-np-hardness]
sources:
  - paper: doi:10.1109/5.892708
    title: N. Jesper Larsson and Alistair Moffat, Off-line dictionary-based compression, Proceedings of the IEEE 88(11), 2000, pages 1722 to 1732
    locator: the Re-Pair algorithm, its data structures (the sequence array with links, the pair hash table, the priority queue of lists by frequency) and the proof of linear expected time
  - paper: "N. Jesper Larsson and Alistair Moffat, Offline dictionary-based compression, Data Compression Conference (DCC 1999), pages 296 to 305"
    locator: the first description of Re-Pair
  - paper: doi:10.1109/TIT.2005.850116
    title: Moses Charikar, Eric Lehman, Ding Liu, Rina Panigrahy, Manoj Prabhakaran, Amit Sahai and abhi shelat, The smallest grammar problem, IEEE Transactions on Information Theory 51(7), 2005
    locator: Section VI (Re-Pair, upper bound O((n/log n)^(2/3)) and lower bound Omega(sqrt(log n)) on the approximation ratio)
  - paper: doi:10.1109/TIT.2020.3038147
    title: Hideo Bannai, Momoko Hirayama, Danny Hucke, Shunsuke Inenaga, Artur Jeż, Markus Lohrey and Carl Philipp Reh, The smallest grammar problem revisited, IEEE Transactions on Information Theory 67(1), 2021
    locator: the lower bound Omega(log n / log log n) on the approximation ratio of Re-Pair
---

Re-Pair is an off-line [grammar-based compression](/grammar-based-compression/) algorithm: it replaces the most frequent pair of adjacent symbols by a new nonterminal, and repeats until no pair occurs twice. The result is a [straight-line program](/straight-line-program-grammar/) with rules $A \to xy$ and a short final sequence. With a [hash table](/hash-table/), a [doubly linked list](/doubly-linked-list/) and a [priority queue](/priority-queue/) of frequencies, it runs in linear expected time (Larsson and Moffat, 1999) or in $O(n \log n)$ expected time with a binary heap. It is a heuristic for the [smallest grammar problem](/smallest-grammar-problem/), and it often gives small grammars on repetitive text.

## In plain words

Look at each pair of neighbouring letters in a text and count how often each pair appears. Take the most common pair, say "th", and invent a new letter for it. Replace every "th" in the text by the new letter, and write down "new letter means th". The text is now shorter.

Do it again with the new text. Pairs can now contain the invented letters, so a later step can join "th" with "e" into a letter for "the". Stop when no pair appears twice. The output is the short text plus the list of pairs. To decompress, replace each invented letter by its pair until only real letters are left.

## The problem

The input is a string $w = w_1 \cdots w_n$ over the alphabet $\{0, \ldots, \sigma - 1\}$. The output is a straight-line program for $w$: a list of rules $A \to xy$, each with a new symbol $A \ge \sigma$, and a final sequence $s$ such that expanding $s$ with the rules gives $w$. The size of the grammar is $2r + |s|$ for $r$ rules. Re-Pair does not promise the smallest size; it promises that on return no pair occurs twice in $s$ without overlap.

The **frequency** of a pair $xy$ in $s$ is the number of its occurrences that do not overlap. For $x \ne y$ occurrences never overlap. For $x = y$, a run of $L$ equal symbols counts $\lfloor L/2 \rfloor$ times, so aaa holds one occurrence of aa, not two.

## The algorithm

```pseudo id=main
RE-PAIR(w)                                  ▷ w = w[1 .. n] over {0, ..., σ − 1}
L1  put w in a doubly linked list s
L2  for each pair xy of s: occ[xy] ← its positions, cnt[xy] ← its frequency
L3  put each pair with cnt ≥ 2 in a priority queue Q, keyed by cnt
L4  R ← empty list, A ← σ
L5  while Q is not empty do
L6      remove from Q the pair ab of largest cnt (skip entries that are out of date)
L7      for each occurrence i of ab, from left to right do
L8          remove the pairs (p, a) and (b, q), with p, q the neighbours, from cnt and occ
L9          write A at position i and unlink the node of b
L10         add the pairs (p, A) and (A, q) to cnt, occ and Q
L11     append A → ab to R, A ← A + 1
L12 return R and s
```

Line L2 scans $s$ once. For a pair of two different symbols it records each position. For a pair $aa$ it records each maximal run of $a$ of length at least 2, by its two ends and its length, and adds $\lfloor L/2 \rfloor$ to the frequency. Line L6 takes the pair of largest frequency, and on a tie the smallest pair. The queue does not support a change of key, so each change of a frequency pushes a new entry, and line L6 drops entries whose count is not the current one.

Lines L7 to L10 replace the occurrences. Only the two pairs around each occurrence change, so the frequencies stay exact after $O(1)$ work per occurrence. When the left neighbour $p$ holds $a$, node $i$ is the end of a run of $a$, and line L8 shortens that run. When $p$ already holds $A$ from the previous occurrence, line L10 extends a run of $A$. For a pair $aa$, line L7 goes over the runs, and lines L9 and L10 turn a run of length $L$ into $\lfloor L/2 \rfloor$ copies of $A$, plus one $a$ when $L$ is odd.

## Example

Take $w$ = xabcabcyabcabc, with $n = 14$. New symbols are named $A, B, C$.

| step | chosen pair | frequency | new rule | sequence $s$ | $\lvert s \rvert$ |
|---|---|---|---|---|---|
| start | | | | x a b c a b c y a b c a b c | 14 |
| 1 | ab | 4 | $A \to ab$ | x A c A c y A c A c | 10 |
| 2 | Ac | 4 | $B \to Ac$ | x B B y B B | 6 |
| 3 | BB | 2 | $C \to BB$ | x C y C | 4 |

In step 1, the frequencies are ab 4, bc 4, ca 2, and 1 for xa, cy and ya. The pairs ab and bc tie, and ab wins as the smaller pair. After step 3, every pair of xCyC occurs once, so the loop stops. The grammar has 3 rules and size $2 \cdot 3 + 4 = 10$. The smallest grammar for this string has size 9 ($A \to abc$, $S \to xAAyAA$), so Re-Pair is close but not optimal.

**A run.** For $w$ = aaaaaaa, the pair aa has frequency $\lfloor 7/2 \rfloor = 3$. Line L9 makes AAAa. Now AA has frequency $\lfloor 3/2 \rfloor = 1$, and the loop stops with the rule $A \to aa$ and $s$ = AAAa.

## Correctness

The proof keeps an invariant at line L5: expanding $s$ with $R$ gives $w$, and $\mathit{cnt}$, $\mathit{occ}$ and the run tables hold the exact frequencies and positions of every pair in $s$. A replacement of one occurrence changes only the two neighbouring pairs, and lines L8 and L10 update exactly these. Processing the occurrences from left to right ensures that the right neighbour never holds the new symbol yet. At the end the queue is empty, so no pair has frequency 2 or more. The proof also shows that the output is the same as that of the plain method that recounts all pairs after each step. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each replacement of one occurrence shortens $s$ by 1, so there are at most $n - 1$ of them, and each one does $O(1)$ hash table operations and $O(1)$ pushes to $Q$. The scan of line L2 does $O(n)$ operations. So $Q$ receives $O(n)$ entries in total, and each one is removed at most once.

- With a [binary heap](/binary-heap/), each push and removal costs $O(\log n)$, and sorting the occurrences in line L7 costs $O(n \log n)$ in total. The time is $O(n \log n)$, expected because of the hash tables. This is the version on this page.
- Larsson and Moffat (2000) reach $O(n)$ expected time. Their queue is an array of lists indexed by frequency for frequencies below $\sqrt{n}$, plus one list for the larger ones; at most $\sqrt{n}$ pairs can have frequency $\sqrt{n}$ or more, so that list is short. They also keep the occurrences of each pair as a linked list threaded through the sequence, in text order, so no sorting is needed. This queue is a form of [bucket queue](/bucket-queue/).
- The space is $O(n)$ words: the list, the hash tables and the queue each hold $O(n)$ items. In practice this is several machine words per input symbol, which is the main cost of Re-Pair on large inputs.
- The number of rules is at most $(n - 1)/2$, because each rule shortens $s$ by at least 2.

## Properties

- **Off-line.** Re-Pair needs the whole input before it makes the first rule.
- **Binary rules.** Each rule has two symbols on the right. The output is an SLP in a form close to [Chomsky normal form](/chomsky-normal-form/), so random access and other SLP algorithms apply after building a balanced version.
- **No pair repeats in $s$.** The final sequence has no pair of frequency 2 or more. The rules themselves can still share pairs, because a rule is never rewritten after it is made.
- **Deterministic.** With a fixed rule for ties, the output depends only on $w$.
- **Approximation ratio.** Charikar et al. (2005) show an upper bound $O((n / \log n)^{2/3})$ for their version of Re-Pair, and a lower bound $\Omega(\sqrt{\log n})$. Bannai et al. (2021) raise the lower bound to $\Omega(\log n / \log \log n)$. So Re-Pair can be far from the smallest grammar in the worst case, even though it does well in practice.

## Variants and improvements

- **Encoding the output.** Larsson and Moffat encode the rules and the final sequence with entropy coding. The grammar of this page is the intermediate form.
- **Byte-pair encoding.** [Byte-pair encoding](/byte-pair-encoding/) is the same pair replacement inside a fixed budget: a new symbol must be a byte value that does not occur in the block, so it stops after at most 255 rules per block, and it often uses a minimum frequency. Re-Pair has no such limit.
- **The tie rule and overlaps.** Implementations differ in how they break ties and in how they count runs. Each choice changes the output, but not the guarantee at the end.
- **Versions in the analysis.** Charikar et al. analyze a version that differs in details from the original, so their bounds do not transfer word for word.

## When to use it

Use Re-Pair when the whole input is available, when it is highly repetitive (versions of a document, genomes of one species, logs), and when you want a grammar to compute on, for example a grammar-based [compressed index](/compressed-indexing/). If the data arrives as a stream and the grammar must grow with it, use an on-line method such as [Sequitur](/sequitur/). Do not use it when memory is tight compared with the input. For general files, an LZ77 compressor is faster and good enough.

## Pitfalls

- **Counting overlapping pairs.** If line L2 counts aaa as two occurrences of aa, Re-Pair makes a rule for a pair that can be replaced only once, and the grammar grows. Count $\lfloor L/2 \rfloor$ for a run of length $L$.
- **Forgetting the runs in the updates.** In line L8, when the left neighbour holds $a$, the old pair is $aa$ and it lives in a run. Removing it as a single occurrence gives wrong counts on inputs such as aab repeated. The same holds for the right neighbour and for $AA$ in line L10.
- **Using a stale entry.** Line L6 must check that the count of the removed entry is still current. Without this check, Re-Pair can replace a pair that no longer occurs twice.
- **Processing occurrences out of order.** Line L7 must go from left to right. In abab, the second occurrence gets the new $A$ as its left neighbour. If it is processed first, the first occurrence later sees $A$ as its right neighbour, and line L10 records $(A, A)$ as a pair of two different symbols instead of a run, so the counts of $AA$ go wrong.
- **Recursive expansion.** A chain of rules can be as deep as the number of rules. A recursive expand function can overflow the stack; use an explicit stack.

## Implementations

## History

N. Jesper Larsson and Alistair Moffat presented Re-Pair (recursive pairing) at the Data Compression Conference in 1999, and published the full paper, "Off-line dictionary-based compression", in the Proceedings of the IEEE in 2000. They gave the linear expected time algorithm and an encoding of the resulting grammar. Philip Gage's byte-pair encoding (1994) applied the same pair replacement within a byte budget. Charikar et al. (2005) analyzed Re-Pair as an approximation algorithm for the smallest grammar problem.

## References
