---
tag: YSK2J8
kind: algorithm
slug: fkm-algorithm
name: FKM algorithm
aliases:
- Fredricksen-Kessler-Maiorana algorithm
- Ford's Lyndon-word generation
area: strings/string-combinatorics
level: core
summary: Generates Lyndon words in lexicographic order, yielding necklaces and de Bruijn sequences.
solves: [necklace-enumeration, de-bruijn-sequence]
model: word-ram
complexity:
  vars: {n: the length of the words, k: the size of the alphabet (k ≥ 2), N: the number of necklaces of length n}
  time: {worst: Θ(N), best: Θ(N)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [lyndon-word, necklace, lexicographic-order]
see_also: [necklace-enumeration, de-bruijn-sequence, duval-algorithm, cattell-necklace-generation, necklace-counting, constant-amortized-time-generation, bracelet, combinatorial-generation]
sources:
  - paper: doi:10.1016/0012-365X(78)90002-X
    title: Harold Fredricksen and James Maiorana, Necklaces of beads in k colors and k-ary de Bruijn sequences, Discrete Mathematics 23(3), 1978, 207-210
    locator: the successor rule for necklaces in lexicographic order and the concatenation of the Lyndon words whose length divides n into a de Bruijn sequence
  - paper: "Harold Fredricksen and Irving J. Kessler, An algorithm for generating necklaces of beads in two colors, Discrete Mathematics 61(2-3), 1986, 181-188"
    title: Harold Fredricksen and Irving J. Kessler, An algorithm for generating necklaces of beads in two colors
    locator: the binary necklace generation algorithm
  - paper: doi:10.1016/0196-6774(92)90047-G
    title: Frank Ruskey, Carla Savage and Terry Min Yih Wang, Generating necklaces, Journal of Algorithms 13(3), 1992, 414-430
    locator: the analysis showing that the FKM algorithm runs in constant amortized time per necklace
  - paper: doi:10.1006/jagm.2000.1108
    title: Kevin Cattell, Frank Ruskey, Joe Sawada, Micaela Serra and C. Robert Miers, Fast algorithms to generate necklaces, unlabeled necklaces, and irreducible polynomials over GF(2), Journal of Algorithms 37(2), 2000, 267-282
    locator: the fundamental theorem of necklaces (extension of a prenecklace by one letter and the new longest Lyndon prefix)
  - paper: doi:10.1016/j.aam.2003.10.002
    title: Eduardo Moreno, On the theorem of Fredricksen and Maiorana about de Bruijn sequences, Advances in Applied Mathematics 33(2), 2004, 413-415
    locator: a short proof that the concatenation of the Lyndon words whose length divides n is a de Bruijn sequence, and that it is the lexicographically least one
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (Algorithm F, prime and preprime strings in lexicographic order, and the de Bruijn cycle built from them)
---

The FKM algorithm, after Fredricksen, Kessler and Maiorana, lists all prenecklaces of length $n$ over the alphabet $\{0, \ldots, k-1\}$ in lexicographic order, where a prenecklace is a prefix of a power of a [Lyndon word](/lyndon-word/). Along the way it knows the length $p$ of the longest Lyndon prefix of each word, which tells whether the word is a [necklace](/necklace/) ($p$ divides $n$) or a Lyndon word ($p = n$). Concatenating the Lyndon words whose length divides $n$, in the order produced, gives the lexicographically least [de Bruijn sequence](/de-bruijn-sequence/). The total time is proportional to the number of necklaces, a constant amortized time per necklace for $k \ge 2$.

## In plain words

Think of an odometer whose digits run from 0 to $k - 1$. To move on from the current word, find the rightmost digit that is not yet at its largest value and increase it. Then, instead of resetting the digits to its right to 0, fill them by repeating the prefix that ends at the increased digit, again and again, until the word has length $n$. This one rule jumps over every word that cannot start a necklace, and it lands exactly on the next word that can. The position of the increased digit also tells how long the repeating block is, and so whether the new word is a necklace, a Lyndon word, or neither.

## The problem

The alphabet is $\{0, 1, \ldots, k-1\}$ with the usual order, $k \ge 1$, and words are compared in [lexicographic order](/lexicographic-order/). Indices are 0-based. A word is a necklace if it is not larger than any of its rotations, and a [Lyndon word](/lyndon-word/) if it is strictly smaller than all its other rotations. A word is a prenecklace if it is a prefix of $v v v \cdots$ for some Lyndon word $v$; every necklace is a prenecklace, since it is a power of a Lyndon word. For a nonempty word $a$, $\mathrm{lyn}(a)$ is the length of its longest prefix that is a Lyndon word.

Given $k \ge 1$ and $n \ge 1$, the task is to list all prenecklaces of length $n$ in increasing order, each with $\mathrm{lyn}(a)$, and from them the necklaces, the Lyndon words, or a de Bruijn sequence of order $n$. This is [necklace enumeration](/necklace-enumeration/), and its count is given by [necklace counting](/necklace-counting/).

## The algorithm

The array $a[0..n-1]$ holds the current prenecklace and $p = \mathrm{lyn}(a)$. The procedure VISIT receives both.

```pseudo id=main
FKM(k, n)                              ▷ alphabet {0, ..., k − 1}, n ≥ 1
L1  a[0 .. n − 1] ← 0, p ← 1
L2  loop
L3      VISIT(a, p)                    ▷ a is a prenecklace and p = lyn(a)
L4      j ← n − 1
L5      while j ≥ 0 and a[j] = k − 1 do j ← j − 1
L6      if j < 0 then return
L7      a[j] ← a[j] + 1, p ← j + 1
L8      for i ← p to n − 1 do a[i] ← a[i − p]
```

Lines L4 and L5 find the rightmost letter that can be increased; if there is none, the word was $(k-1)^n$, the last prenecklace, and line L6 stops. Line L7 increases it, and the new prefix $a[0..j]$ is a Lyndon word, so $p = j + 1$. Line L8 fills the rest of the word with copies of that prefix.

Three uses differ only in VISIT:

- **Necklaces.** Output $a$ when $p$ divides $n$.
- **Lyndon words.** Output $a$ when $p = n$.
- **De Bruijn sequence.** When $p$ divides $n$, append $a[0..p-1]$ to the output. The final output has length $k^n$, and read cyclically, it contains each word of length $n$ exactly once.

## Example

Let $k = 2$ and $n = 4$. The column "$j$" is the index increased to reach the row from the row above.

| step | $a$ | $j$ | $p = \mathrm{lyn}(a)$ | necklace | Lyndon | de Bruijn block |
|---|---|---|---|---|---|---|
| 1 | `0000` | | 1 | yes | | `0` |
| 2 | `0001` | 3 | 4 | yes | yes | `0001` |
| 3 | `0010` | 2 | 3 | | | |
| 4 | `0011` | 3 | 4 | yes | yes | `0011` |
| 5 | `0101` | 1 | 2 | yes | | `01` |
| 6 | `0110` | 2 | 3 | | | |
| 7 | `0111` | 3 | 4 | yes | yes | `0111` |
| 8 | `1111` | 0 | 1 | yes | | `1` |

In step 3 the last letter of `0001` is already 1, so $j = 2$ and $a[2]$ becomes 1; the prefix `001` is repeated, and the word becomes `0010` with $p = 3$, a prenecklace that is not a necklace, since 3 does not divide 4. In step 5, from `0011`, the index is $j = 1$, the prefix `01` is repeated, and the result `0101` is a necklace with $p = 2$. From `0111` the index is $j = 0$, and the prefix `1` repeated gives `1111`.

There are 8 prenecklaces, 6 necklaces and 3 Lyndon words. The de Bruijn blocks give `0 0001 0011 01 0111 1`, that is, `0000100110101111`. Read cyclically, its 16 windows of length 4 are the 16 binary words of length 4, each once. For $k = 3$ and $n = 3$, the 14 prenecklaces start `000`, `001`, `002`, `010`, `011`, `012`, `020`, and there are 11 necklaces and 8 Lyndon words.

## Correctness

The proof rests on the fundamental extension lemma: if $a$ is a nonempty prenecklace of length $m$ with $q = \mathrm{lyn}(a)$ and $b$ is a letter, then $ab$ is a prenecklace if and only if $b \ge a[m - q]$, and $\mathrm{lyn}(ab)$ is $q$ if $b = a[m - q]$ and $m + 1$ if $b > a[m - q]$. It gives three facts. Each prenecklace $a$ is $u^\infty$ cut to length $n$, where $u$ is its prefix of length $\mathrm{lyn}(a)$. After line L7 the prefix $a[0..j]$ is a Lyndon word, so line L8 makes the new word a prenecklace with $\mathrm{lyn} = j + 1$. And every word strictly between the old and the new word agrees with the new word up to some position where it has a smaller letter than the repetition requires, so it is not a prenecklace. The algorithm starts at the least word $0^n$ and ends at $(k-1)^n$, so it visits all prenecklaces of length $n$ in increasing order. A prenecklace with $\mathrm{lyn}(a) = p$ is a necklace exactly when $p$ divides $n$, and a Lyndon word exactly when $p = n$. The full proof is in the proof file.

The de Bruijn property of the concatenation is the theorem of Fredricksen and Maiorana; a short proof was given by Moreno (2004), and it is discussed on the [de Bruijn sequence](/de-bruijn-sequence/) page.

## Complexity

- **Cost per step.** If the new word has $\mathrm{lyn} = q$, lines L4 to L8 cost $O(n - q + 1)$: line L5 scans from $n - 1$ down to $q - 1$, and line L8 writes $n - q$ letters.
- **Total.** The map $u \mapsto (u^\infty$ cut to length $n)$ is a bijection from the Lyndon words of length $q \le n$ onto the prenecklaces of length $n$ with $\mathrm{lyn} = q$. So, with $L_k(q)$ the number of Lyndon words of length $q$, the total cost is $O\big(\sum_{q=1}^{n} L_k(q)(n - q + 1)\big)$. Since $L_k(q) \le k^q / q$, the terms with $q \ge n/2$ sum to at most $\frac{2}{n} k^n \sum_{t \ge 0} (t+1) k^{-t} = \frac{2}{n} k^n \big(\frac{k}{k-1}\big)^2$, and the terms with $q < n/2$ sum to at most $n(n+1)k^{n/2}$. The number $N$ of necklaces is at least $k^n / n$, because each necklace class has at most $n$ words. Hence for $k \ge 2$ the total is $O(N)$, a constant amortized time per necklace, and also $O(k^n/n)$.
- **Counts.** The same argument shows that the ratio of prenecklaces to necklaces tends to $k/(k-1)$. For $k = 2$ and $n = 22$ there are 401428 prenecklaces and 190746 necklaces.
- **De Bruijn sequence.** The blocks have total length $k^n$, so the sequence is produced in $\Theta(k^n)$ time, linear in its length.
- **Space.** The array $a$ and two indices: $\Theta(n)$.
- **The model.** These bounds assume that VISIT reads $a$ in place. Copying each word out costs $n$ per word, $\Theta(nN)$ in total.

For $k = 1$ there is one prenecklace, $0^n$, and the run costs $\Theta(n)$.

## Properties

- **Lexicographic order.** Prenecklaces, necklaces and Lyndon words all come out in increasing order.
- **Iterative.** No recursion and no stack; the state is the array and $p$.
- **Online output.** Each word is reported as soon as it is formed, and the generation can be stopped and resumed from any prenecklace $a$ if $\mathrm{lyn}(a)$ is known, or computed with the extension lemma in $O(n)$ time.
- **The least de Bruijn sequence.** The de Bruijn sequence it builds is the lexicographically least among all de Bruijn sequences of order $n$ over $\{0, \ldots, k-1\}$, written as words of length $k^n$.

## Variants and improvements

- **Recursive form.** The [Cattell-Ruskey-Sawada algorithm](/cattell-necklace-generation/) generates the same prenecklaces by a recursion that extends a prefix one letter at a time with the extension lemma. It adapts to restricted classes, such as necklaces with a fixed content and unlabeled necklaces.
- **Bracelets.** Necklaces that are also least under reversal are [bracelets](/bracelet/); Sawada gave a constant amortized time algorithm for them.
- **Successor only.** Lines L4 to L8 compute the next prenecklace from any prenecklace, so the next necklace can be found by repeating them until $p$ divides $n$; the amortized bound above still applies to a full run.
- **Ranking.** Computing the rank of a necklace in this order without generating the ones before it needs a separate method, based on counting prenecklaces with a given prefix.

## When to use it

Use FKM to list necklaces or Lyndon words of a given length, to build a de Bruijn sequence of order $n$ in time linear in its length, or as a successor function for prenecklaces. The code is a few lines with no recursion. For necklaces with constraints on the content or on forbidden factors, the recursive [Cattell-Ruskey-Sawada](/cattell-necklace-generation/) framework is easier to adapt.

## Pitfalls

- **Resetting to 0.** Setting the letters after $j$ to 0, as an odometer does, gives all $k^n$ words, not the prenecklaces, and $j + 1$ is then not $\mathrm{lyn}(a)$.
- **Testing the wrong condition.** A necklace needs $p \mid n$, not $p = n$. With $p = n$ only Lyndon words are kept, and the de Bruijn sequence misses the periodic necklaces such as `0101`: for $k = 2$, $n = 4$ it would have length 12, not 16.
- **Appending whole words.** For the de Bruijn sequence, append only $a[0..p-1]$; appending all of $a$ gives a sequence of length $nN$ with repeated windows.
- **Copying in the wrong direction.** Line L8 must run $i$ upward, so that $a[i - p]$ is already final when it is copied.
- **Counting the cost per word.** The constant amortized time holds per necklace with the word read in place. A loop that prints every word as a string costs $\Theta(n)$ per word.

## Implementations

## History

Fredricksen and Maiorana (1978) gave the rule for the next necklace in lexicographic order and observed that the Lyndon words whose length divides $n$, concatenated in that order, form a de Bruijn sequence; Fredricksen and Kessler (1986) described the binary necklace algorithm. The same de Bruijn sequence is associated with earlier greedy constructions, and L. R. Ford Jr. considered such cyclic arrangements of $m$-tuples in a 1957 report, which is the source of the alias. Ruskey, Savage and Wang (1992) proved that the algorithm runs in constant amortized time per necklace. Cattell, Ruskey, Sawada, Serra and Miers (2000) stated the extension lemma as the fundamental theorem of necklaces and used it for a recursive generator, and Knuth presents the method as Algorithm F in Volume 4A of The Art of Computer Programming.

## References
