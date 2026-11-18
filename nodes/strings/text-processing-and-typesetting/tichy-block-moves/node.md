---
tag: ZJTFAN
kind: algorithm
slug: tichy-block-moves
name: Tichy's block move algorithm
aliases:
- string-to-string correction with block moves
area: strings/text-processing-and-typesetting
level: core
summary: Build the target from the fewest copied blocks of the source and added symbols, by taking the longest block of the source that matches at each position.
model: word-ram
complexity:
  vars: {m: the length of the source S, n: the length of the target T}
  time: {worst: O(m n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: true, greedy: true}
prereqs: [edit-distance, greedy-stays-ahead]
see_also: [block-edit-distance, lz77, delta-encoding, rolling-checksum, suffix-tree, suffix-automaton, heckel-diff, longest-common-substring]
sources:
  - paper: doi:10.1145/357401.357404
    title: Walter F. Tichy, The string-to-string correction problem with block moves, ACM Transactions on Computer Systems 2(4), 1984, 309-321
    locator: the block move model, the minimal covering set of common substrings, the greedy longest match at each position with its proof of minimality, the O(mn) method and the linear method with a suffix tree
  - url: https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1377&context=cstech
    title: Walter F. Tichy, The string-to-string correction problem with block moves, Purdue University, Department of Computer Science technical report, 1983
    locator: the earlier report version of the paper
---

Tichy's block move algorithm writes a target string $T$ as a list of moves: a copy of a block of the source string $S$, or an add of one symbol that does not occur in $S$. At each position of $T$ it takes the longest block of $S$ that matches there. Walter Tichy proved in 1984 that this greedy rule gives the fewest moves. A block of $S$ may be copied many times and in any order, so the method expresses moved and repeated text directly, which an [edit distance](/edit-distance/) or a line diff such as [Heckel's algorithm](/heckel-diff/) cannot do. It is the model of copy and add deltas, and the same parse as [LZ77](/lz77/) when the copies come from a separate source instead of the text already written. This kind of file delta is a different thing from [delta encoding](/delta-encoding/) of numbers. In [block edit distance](/block-edit-distance/) the blocks of the source can be used only once, and that problem is much harder.

## In plain words

You have an old text and a new text, and you want to describe the new text with as few instructions as possible. An instruction either says "copy this many characters from that place in the old text", or "add this character", for a character that the old text does not have.

Start at the beginning of the new text. Find the longest piece of the old text that matches the new text here, and copy it. Then do the same at the position after the copy. If no piece matches, the character is new, so add it.

Taking the longest copy each time is always best. A shorter copy can never let a later copy reach further.

## The problem

The input is a source $S = S[0 \ldots m - 1]$ and a target $T = T[0 \ldots n - 1]$ over some alphabet. A *move* is a copy $(p, \ell)$ with $\ell \ge 1$, which appends $S[p \ldots p + \ell - 1]$, or an add of one symbol. A *cover* of $T$ is a list of moves that, run in order, produce $T$. The goal is a cover with the fewest moves. Tichy calls the copied blocks a covering set of common substrings of $T$ with respect to $S$. Every symbol of $T$ that does not occur in $S$ needs an add, and other symbols can always be copied, so the goal is the same as the fewest copies.

## The algorithm

```pseudo id=main
BLOCK-MOVES(S[0 .. m - 1], T[0 .. n - 1])
L1  q ← 0; M ← an empty list
L2  while q < n do
L3      for p ← 0 to m - 1 do ℓ_p ← the length of the longest common prefix of S[p .. m - 1] and T[q .. n - 1]
L4      ℓ ← the largest ℓ_p, and p* ← the first p with ℓ_p = ℓ
L5      if ℓ = 0 then append add(T[q]) to M; q ← q + 1      ▷ T[q] does not occur in S
L6      else append copy(p*, ℓ) to M; q ← q + ℓ
L7  return M
```

Lines L3 and L4 find the longest prefix of the rest of $T$ that occurs in $S$, by comparing it with each suffix of $S$. Tichy also gives a linear version: build a [suffix tree](/suffix-tree/) of $S$, and walk it along $T[q \ldots]$ until the next symbol has no branch. The implementation of this page has the direct version and a linear version with the [suffix automaton](/suffix-automaton/) of $S$, which accepts exactly the substrings of $S$. Both take the first occurrence on ties, so they return the same moves.

## Example

Take $S = abcde$ and $T = cdeabxe$.

| $q$ | rest of $T$ | longest prefix found in $S$ | move |
| --- | --- | --- | --- |
| 0 | cdeabxe | cde, at $p = 2$ | copy(2, 3) |
| 3 | abxe | ab, at $p = 0$ | copy(0, 2) |
| 5 | xe | none, $x$ is not in $S$ | add(x) |
| 6 | e | e, at $p = 4$ | copy(4, 1) |

The result has 4 moves: three copies and the add that $x$ needs. The block cde moved in front of ab, and the cover says so with two copies. A diff that only deletes and inserts symbols keeps a [longest common subsequence](/longest-common-subsequence/), here of length 3, such as cde, and needs $5 + 7 - 2 \cdot 3 = 6$ operations, with ab deleted at one place and inserted at another.

Copies may repeat and overlap in the source: for $S = ab$ and $T = ababab$ the cover is copy(0, 2) three times.

## Correctness

The proof file uses the method of [greedy stays ahead](/greedy-stays-ahead/). Let $G(q)$ be the position after the greedy move at $q$. Any move of any cover that starts at $q$ ends at most at $G(q)$, because a copy produces a substring of $S$ that starts at $q$, and line L4 takes the longest one. And $G$ is monotone: if $q \le q'$ then $G(q) \le G(q')$, since every substring of a block of $S$ is also a block of $S$. So by induction, after $i$ moves the greedy cover is at least as far along $T$ as any other cover after $i$ moves, and it reaches the end of $T$ with no more moves than the best cover. The moves are valid because each one produces the next part of $T$, and the adds are exactly the symbols of $T$ that are not in $S$.

## Complexity

Count in the [word-RAM](/word-ram/), with symbols compared in $O(1)$.

- **Time, direct.** At position $q$, line L3 compares at most $L + 1$ pairs for each of the $m$ starts, where $L$ is the length of the copy that follows; then $q$ moves by at least $\max(1, L)$. Over the whole target this is $O(m n)$.
- **Time, linear.** A suffix tree or a suffix automaton of $S$ is built in $O(m)$ time for a fixed alphabet, or expected time with hash tables for the edges. Each round reads the symbols of its copy plus one failed step, so the scan of $T$ is $O(n)$, and the total is $O(m + n)$.
- **Space.** The direct version needs $O(1)$ space besides the inputs and the list of moves. The linear version needs $O(m)$ for the index.

## Properties

- **Optimal.** The greedy cover has the fewest moves, and so the fewest copies.
- **Online in the target.** The method reads $T$ from left to right and writes each move as soon as it is found, so the target can be streamed through.
- **Moves and repeats.** A block of $S$ can be copied any number of times, in any order, so moved and duplicated text costs one copy per block.
- **Deletes are free.** Parts of $S$ that no copy uses are dropped without a move.
- **Not unique.** Ties between starts change only where the copies come from, not their number or lengths.

## Variants and improvements

- **Costs per move.** A real delta encodes a copy with an offset and a length, and an add with its symbols. If a copy costs more than an add of one symbol, short copies may not pay off, and the greedy count of moves is no longer the right measure of size. Delta formats then use a minimum copy length.
- **Each block used once.** If each part of $S$ may be used by at most one copy, the problem is the [block edit distance](/block-edit-distance/) family, where many versions are NP-hard.
- **Copies from the target itself.** Allowing copies from the part of $T$ already written turns the method into a parse of the [LZ77](/lz77/) kind, with $S$ as a dictionary in front of the text.
- **Fingerprints instead of an index.** Delta tools for large files find candidate blocks by hashing fixed windows with a [rolling checksum](/rolling-checksum/), as rsync does, and then extend each match. This finds long copies quickly but not always the longest.
- **Line units.** The same rule works with lines or tokens as symbols, which gives a diff that reports moved blocks of lines.

## When to use it

Use it to store or send a new version of a file as a delta against an old version, when moved and repeated blocks are common, for example in binary files, generated files and reordered source. Use a [suffix automaton](/suffix-automaton/) or a suffix tree for large inputs. For a delta that people read line by line, use a line diff such as [Myers' algorithm](/myers-diff/); for a measure in which text may move but not be copied twice, see [block edit distance](/block-edit-distance/).

## Pitfalls

- **Overlapping copies.** Two copies of the cover may take the same or overlapping blocks of $S$. A decoder that assumes disjoint blocks fails.
- **Ties.** The direct version and an index may pick different occurrences on ties. Tests should compare the lengths, or fix the rule, as this page does with the first occurrence.
- **Cost model.** The theorem counts moves. When copies are encoded with more bytes than adds, a cover with fewest moves can be larger than another cover.
- **Quadratic time.** The direct version is $O(m n)$ even when the delta is short. Long inputs need the linear version or fingerprints.

## Implementations

## History

Walter Tichy, at Purdue University, wrote the method in a technical report in 1983 and published it in ACM Transactions on Computer Systems in 1984. He set it against the diff programs of the time, which compute a longest common subsequence, and showed that block moves give a cover with the fewest blocks by a simple greedy rule, in linear time with a suffix tree. Copy and add deltas of this kind are used in later delta formats and version control storage.

## References
