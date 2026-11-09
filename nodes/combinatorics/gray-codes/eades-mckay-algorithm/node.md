---
tag: W2DJTJ
kind: algorithm
slug: eades-mckay-algorithm
name: Eades-McKay algorithm
aliases:
- Eades-McKay subset Gray code
- strong minimal change subset ordering
- homogeneous combination Gray code
- Eades-McKay order
area: combinatorics/gray-codes
level: research
summary: Generates fixed-size subsets with the strong minimal change property.
solves: [combination-gray-code-generation]
model: word-ram
complexity:
  vars: {n: the length of the bit strings, k: the number of ones, N: the number of strings (n choose k)}
  time: {worst: Θ(n + N), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: true}
history:
  year: 1984
  people: [Peter Eades, Brendan McKay]
  note: Eades and McKay published this homogeneous order in Information Processing Letters in 1984. Éva Tőrők published a homogeneous scheme in 1968, and Ehrlich gave a loopless homogeneous generator in 1973.
prereqs: [revolving-door-ordering, binomial-coefficient, fixed-weight-binary-strings]
see_also: [combination-gray-code-generation, chase-sequence, revolving-door-ordering, ehrlich-loopless-combinations, minimal-change-ordering, cool-lex-order, k-subset-enumeration, constant-amortized-time-generation]
sources:
  - paper: doi:10.1016/0020-0190(84)90091-7
    title: Peter Eades and Brendan McKay, An algorithm for generating subsets of fixed size with a strong minimal change property, Information Processing Letters 19(3), 131 to 133, 1984
    locator: the homogeneous list of k-subsets and its recursive generator
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3 (homogeneous schemes, the recursion (31) for K_st, and the lists (32) and (33) for s = t = 3; the answers to its exercises note the 1968 scheme of Tőrők)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Chapter 5, Section 5.3 (the homogeneous transposition condition, the list E(n, k) of (5.5), Lemma 5.3, and Algorithm 5.8)
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 4.1 (homogeneous Gray codes for combinations by Chase and by Eades and McKay, and the piano picture), Section 5.6 (homogeneous Gray codes for multiset permutations)
---

The Eades-McKay algorithm lists all $N = C(n, k)$ subsets of size $k$ of an $n$-element set so that each step moves one element to a new value and passes over no other element of the subset. In the bit string view a 1 moves left or right and every bit it passes is 0, a step that is called homogeneous or strong minimal change. Knuth writes the list as $K_{st}$ with $s = n - k$ zeros and $t = k$ ones, defined by the recursion $K_{st} = 0K_{(s-1)t},\ 10K^R_{(s-1)(t-1)},\ 11K_{s(t-2)}$. The recursive generator takes $\Theta(N)$ time after $\Theta(n)$ setup, so $O(1)$ amortized per subset.

## In plain words

You must play every chord of $k$ notes on a piano with $n$ keys, one chord after the other. Between two chords you may lift one finger and put it down on a new key. The rule is that the finger may not cross another finger. So the hand never has to twist.

The plan works from the left end of the keyboard. First play all chords that leave the leftmost key free. Then hold the leftmost key, leave the next key free, and play the chords of the remaining fingers backward. Last, hold the two leftmost keys and play the rest. At each seam, one finger slides over free keys only.

## The problem

Given $n \ge 0$ and $0 \le k \le n$, list every bit string $a_{n-1} \ldots a_1 a_0$ with exactly $k$ ones once, so that consecutive strings differ by a transposition $10^p \leftrightarrow 0^p1$ with $p \ge 1$: one 1 and one 0 trade places and all bits between them are 0. This is [combination Gray code generation](/combination-gray-code-generation/) under the homogeneous rule. Bit $a_j = 1$ means that element $j$ is in the subset. In the index form $c_k \ldots c_1$, with $c_k > \cdots > c_1$, a homogeneous step changes exactly one index $c_i$, so no element passes another.

Let $s = n - k$ and $t = k$. Knuth's recursion (31) is $K_{s0} = 0^s$, $K_{0t} = 1^t$, $K_{s(-1)}$ empty, and for $st > 0$

$$K_{st} = 0K_{(s-1)t},\ \ 10K^R_{(s-1)(t-1)},\ \ 11K_{s(t-2)},$$

where $L^R$ is $L$ reversed and $10L$ puts the bits 10 in front of each string of $L$. The list starts at $0^s1^t$ and ends at $1^t0^s$.

## The algorithm

The walk keeps the string in an array $a_{n-1} \ldots a_0$. A call for $(s, t)$ works on the low $s + t$ bits, whose top position is $m = s + t - 1$. In the forward direction it walks the three parts in order and makes one move at each of the two seams.

```pseudo id=main
EADES-MCKAY(s, t)                           ▷ s zeros, t ones, n = s + t
L1  a_{n−1} … a_0 ← 0^s 1^t
L2  WALK(s, t, forward)

WALK(s, t, d)                               ▷ visits K_st on a_{s+t−1} … a_0, reversed if d = reverse
L3  if s = 0 or t = 0 then visit a; return  ▷ a single string
L4  m ← s + t − 1
L5  if d = forward then
L6      WALK(s − 1, t, forward)             ▷ the part 0K
L7      a_{m−1} ← 0; a_m ← 1                ▷ the 1 at m − 1 moves up one place
L8      WALK(s − 1, t − 1, reverse)         ▷ the part 10K^R
L9      if t ≥ 2 then
L10         a_{t−2} ← 0; a_{m−1} ← 1        ▷ the 1 at t − 2 jumps over s − 1 zeros
L11         WALK(s, t − 2, forward)         ▷ the part 11K
L12 else
L13     if t ≥ 2 then
L14         WALK(s, t − 2, reverse)
L15         a_{m−1} ← 0; a_{t−2} ← 1
L16     WALK(s − 1, t − 1, forward)
L17     a_m ← 0; a_{m−1} ← 1
L18     WALK(s − 1, t, reverse)
```

The calls never touch positions above $m$. The recursion depth is at most $n$, and an explicit stack replaces it in the implementation.

## Example

For $s = 3$ zeros and $t = 2$ ones ($n = 5$, $k = 2$) the generator visits these ten strings. The move column gives the 1 that moves to reach the next string.

| step | $a_4 \ldots a_0$ | index form | move |
|---|---|---|---|
| 0 | 00011 | 10 | 1 to 2 |
| 1 | 00101 | 20 | 0 to 1 |
| 2 | 00110 | 21 | 2 to 3 |
| 3 | 01010 | 31 | 1 to 0 |
| 4 | 01001 | 30 | 0 to 2, over 1 |
| 5 | 01100 | 32 | 3 to 4 |
| 6 | 10100 | 42 | 2 to 1 |
| 7 | 10010 | 41 | 1 to 0 |
| 8 | 10001 | 40 | 0 to 3, over 1 and 2 |
| 9 | 11000 | 43 | |

Rows 0 to 5 are $0K_{22}$, rows 6 to 8 are $10K^R_{21}$, and row 9 is $11K_{30}$. The move after row 5 is line L7 with $m = 4$, and the move after row 8 is line L10: the 1 at $t - 2 = 0$ jumps to $m - 1 = 3$ over two zeros. In each step one index changes and passes no other index. For $s = t = 3$ the generator gives the 20 strings of Knuth's list (32), from 000111 to 111000, and the finger patterns (33) begin 210, 310, 320, 321, 421.

## Correctness

The proof in `proofs/correctness.md` shows three things.

- **The list.** By induction on $s + t$, $K_{st}$ contains each string with $s$ zeros and $t$ ones once. The three parts hold the strings that start with 0, with 10, and with 11, and $C(n-1, t) + C(n-2, t-1) + C(n-2, t-2) = C(n, t)$.
- **The ends and the steps.** $K_{st}$ starts at $0^s1^t$ and ends at $1^t0^s$. At the first seam $0\,1^t0^{s-1}$ meets $10\,1^{t-1}0^{s-1}$, a swap of two neighbor bits. At the second seam $10\,0^{s-1}1^{t-1}$ meets $11\,0^s1^{t-2}$, a move of the 1 at position $t - 2$ to position $m - 1$ over $s - 1$ zeros. Steps inside a part are homogeneous by induction.
- **The walk.** Each call starts at the first string of its list (the last one if $d$ is reverse), visits the list in order, and ends at the other end. Lines L7, L10, L15 and L17 do exactly the seam moves.

**The same list as Eades and McKay.** Ruskey's form $E(n, k) = E(n-1, k)0,\ E(n-2, k-1)^R01,\ E(n-2, k-2)11$, with base case $E(n, 1) = 10^{n-1}, 010^{n-2}, \ldots, 0^{n-1}1$, builds the strings $b_1 \ldots b_n$ from the right end. Reading each string of $K_{st}$ backward gives $E(s + t, t)$, so the two lists hold the same subsets in the same order when element $j$ of $K$ is element $j + 1$ of $E$. A script checked this for all $s, t \le 8$.

## Complexity

- **Time.** The calls form a tree whose leaves are the $N$ visits. A call with $s, t \ge 1$ makes two or three calls, each for a list that is not empty, so the tree has at most $N - 1$ inner nodes. Each call does $O(1)$ work outside its children, so the walk takes $\Theta(N)$ time, plus $\Theta(n)$ for line L1. The amortized time per subset is $O(1)$, so the generator is CAT.
- **Delay.** Between two visits the walk may return from and enter up to $n$ levels, so the worst-case delay is $\Theta(n)$. Ehrlich's loopless method gives a homogeneous list with $O(1)$ worst-case time per step: see [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/).
- **Space.** The array and a stack of depth at most $n$: $\Theta(n)$ extra space.
- **Output.** Two bits change per step, but a move may cover up to $s$ positions, at the second seam of the top call. In index form exactly one $c_i$ changes.
- **Lower bound.** Any generator visits $N$ strings, so $\Omega(N)$ time is needed, and the recursion meets it.

## Properties

- **Homogeneous.** Each step is $10^p \leftrightarrow 0^p1$, so in the index form only one $c_i$ changes, and it passes no other index.
- **Genlex.** Strings with the same prefix appear together. In the [revolving door order](/revolving-door-ordering/), which is also genlex, some steps change two indices at once; for $n = 6$, $k = 3$ there are nine such steps.
- **Not near-perfect.** A move may cover up to $s$ places, such as 10001 to 11000 above. [Chase's sequence](/chase-sequence/) limits every move to one or two places.
- **Cyclic only for small cases.** The ends $0^s1^t$ and $1^t0^s$ differ in $2\min(s, t)$ bits. For $t = 1$ they are one homogeneous step apart. For $s, t \ge 2$ they are not one transposition apart, for example 0011 and 1100.

## Variants and improvements

- **Chase's near-perfect lists.** [Chase's sequence](/chase-sequence/) keeps the homogeneous rule and also limits each move to $01 \leftrightarrow 10$ or $001 \leftrightarrow 100$.
- **Loopless.** Ehrlich (1973) gave a loopless homogeneous generator that can start at any string $0^p1^k0^{n-p-k}$ (Ruskey, notes to Chapter 5).
- **Adjacent transpositions.** Only moves of one place are possible for all $(s, t)$ exactly when $k \le 1$, $n - k \le 1$, or both $k$ and $n - k$ are odd (Buck and Wiedemann; Eades, Hickey and Read).
- **Multiset permutations.** Ruskey gave a Gray code for multiset permutations by homogeneous transpositions, in which every entry between the two swapped entries is at most the smaller of them. It generalizes the Eades-McKay code (Mütze, Section 5.6).

## When to use it

Use the Eades-McKay order when the elements of a subset are physical objects on a line that must not pass each other, such as fingers on a keyboard, read heads on a track, or markers in a list, and a long move costs about as much as a short one. It is also a simple base for homogeneous lists of other objects, such as compositions, where one homogeneous step changes only two neighbor parts. If long moves are costly, use [Chase's sequence](/chase-sequence/). If only the number of changed elements matters, the [revolving door order](/revolving-door-ordering/) has a simpler rank formula.

## Pitfalls

- **The jump target.** Line L10 written as "$a_{t-1} \leftarrow 0$" takes the wrong 1: position $t - 1$ holds a 0 at that time, so the walk gains a 1. For $s = t = 2$ the walk gives 0011, 0101, 0111. Line L10 must clear $a_{t-2}$, the top 1 of the block $1^{t-1}$ at the low end.
- **The direction of the middle part.** The middle part is $10K^R$, so line L8 walks it in reverse and line L16 forward. With the two directions swapped, for $s = t = 2$ the walk visits 1010 twice. Line L8 must use reverse.
- **The start string.** Line L1 must set $0^s1^t$, with the ones at the low end. Ruskey writes the same list with $b_1$ first and starts at $1^k0^{n-k}$; mixing the two conventions starts the walk at the last string of $K_{st}$ instead of the first.
- **The seam moves in reverse.** Lines L15 and L17 must undo lines L10 and L7. Copying "$a_{m-1} \leftarrow 0$; $a_m \leftarrow 1$" from line L7 into line L17 changes nothing, because at that time $a_{m-1}$ is already 0 and $a_m$ is already 1. The next part then starts from the wrong string.

## Implementations

## History

Éva Tőrők published the first homogeneous revolving door scheme for combinations in Matematikai Lapok in 1968, motivated by the generation of multiset permutations (Knuth, answers to the exercises of Section 7.2.1.3). Ruskey notes that Lathroum found a homogeneous algorithm that Chase implemented in 1970, and that Ehrlich published a loopless homogeneous generator in 1973. Peter Eades and Brendan McKay published the simple recursive list given here in Information Processing Letters in 1984, under the name strong minimal change property. Knuth presents it as the genlex scheme $K_{st}$ and uses it to play all chords on a keyboard by moving one finger at a time.

## References
