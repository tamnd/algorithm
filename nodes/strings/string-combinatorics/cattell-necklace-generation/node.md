---
tag: QYDXYF
kind: algorithm
slug: cattell-necklace-generation
name: CAT necklace generation
aliases:
- constant amortized time necklace generation
- Cattell-Ruskey-Sawada-Serra-Miers algorithm
area: strings/string-combinatorics
level: advanced
summary: Generates necklaces in constant amortized time per necklace.
solves: [necklace-enumeration]
model: word-ram
complexity:
  vars: {n: the length of the words, k: the size of the alphabet (k ≥ 2), N: the number of necklaces of length n}
  time: {worst: Θ(N), best: Θ(N)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, online: true}
prereqs: [necklace, lyndon-word, fkm-algorithm]
see_also: [fkm-algorithm, necklace-enumeration, constant-amortized-time-generation, necklace-counting, bracelet, de-bruijn-sequence, irreducible-polynomial, combinatorial-generation]
sources:
  - paper: doi:10.1006/jagm.2000.1108
    title: Kevin Cattell, Frank Ruskey, Joe Sawada, Micaela Serra and C. Robert Miers, Fast algorithms to generate necklaces, unlabeled necklaces, and irreducible polynomials over GF(2), Journal of Algorithms 37(2), 2000, 267-282
    locator: the recursive algorithm for necklaces and Lyndon words, the fundamental theorem of necklaces, the proof of constant amortized time, the binary unlabeled necklaces and the listing of irreducible polynomials
  - paper: doi:10.1016/0196-6774(92)90047-G
    title: Frank Ruskey, Carla Savage and Terry Min Yih Wang, Generating necklaces, Journal of Algorithms 13(3), 1992, 414-430
    locator: the first proof that necklaces can be listed in constant amortized time (the FKM algorithm)
  - paper: doi:10.1016/s0304-3975(03)00049-5
    title: Joe Sawada, A fast algorithm to generate necklaces with fixed content, Theoretical Computer Science 301(1-3), 2003, 477-489
    locator: the modification of the recursive necklace algorithm to necklaces with a fixed number of each letter, in constant amortized time
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (prime and preprime strings and their generation)
---

The CAT necklace generation algorithm of Cattell, Ruskey, Sawada, Serra and Miers lists all [necklaces](/necklace/) of length $n$ over $k$ letters, or all [Lyndon words](/lyndon-word/), in lexicographic order by a short recursion GEN$(t, p)$. It extends a prefix one letter at a time and keeps $p$, the length of the longest Lyndon prefix, which is all it needs to know which letters may come next. The total time is proportional to the number of necklaces produced, that is, constant amortized time (CAT) per necklace. The recursive form is easy to restrict, and it is the base of later CAT algorithms for necklaces with fixed content, binary unlabeled necklaces, and bracelets.

## In plain words

Build the words letter by letter, from left to right, like walking down a tree. At each step you remember one number: how long the first repeating block of the word is so far. That number tells you the smallest letter you may add next: the letter one block back. Adding that same letter keeps the block; adding a larger letter makes the whole word so far one new block. A smaller letter can never lead to a necklace, so that branch is never tried. When the word is full, it is a necklace if its block length divides the word length, and a Lyndon word if the block is the whole word.

## The problem

The alphabet is $\{0, 1, \ldots, k-1\}$ with $k \ge 1$, ordered as integers; words are compared in [lexicographic order](/lexicographic-order/). Indices are 0-based. A necklace is a word that is not larger than any of its rotations, the least representative of its rotation class. A prenecklace is a prefix of some word $u^\infty = uuu\cdots$ with $u$ a Lyndon word; every necklace is a prenecklace. For a nonempty word $x$, $\mathrm{lyn}(x)$ is the length of its longest prefix that is a Lyndon word. Given $n \ge 1$ and $k$, output every necklace (or every Lyndon word) of length $n$, each once.

## The algorithm

The word is held in the array $a[0..n-1]$. The call GEN$(t, p)$ is made when $a[0..t-1]$ is a prenecklace $x$ with $p = \mathrm{lyn}(x)$; it fills $a[t]$ with each letter that keeps a prenecklace.

```pseudo id=main
NECKLACES(k, n)                            ▷ n ≥ 1
L1  for c ← 0 to k − 1 do a[0] ← c, GEN(1, 1)

GEN(t, p)                                  ▷ a[0 .. t − 1] is a prenecklace, p = lyn
L2  if t = n then
L3      if n mod p = 0 then VISIT(a[0 .. n − 1])   ▷ a necklace; use p = n for Lyndon words
L4  else
L5      a[t] ← a[t − p], GEN(t + 1, p)
L6      for c ← a[t − p] + 1 to k − 1 do
L7          a[t] ← c, GEN(t + 1, t + 1)
```

The rule behind lines L5 to L7 is the fundamental theorem of necklaces. If $x$ is a prenecklace of length $t$ with $p = \mathrm{lyn}(x)$, then $xb$ is a prenecklace exactly when $b \ge x[t - p]$. If $b = x[t - p]$, the word keeps repeating its Lyndon prefix and $\mathrm{lyn}(xb) = p$; if $b > x[t - p]$, the whole word $xb$ is a Lyndon word and $\mathrm{lyn}(xb) = t + 1$. So the recursion never enters a branch that has no output below it.

## Example

Let $k = 2$ and $n = 4$. The calls at $t = 4$ reach the 8 binary prenecklaces of length 4, in increasing order:

| $a$ | $p$ | necklace ($p \mid 4$) | Lyndon word ($p = 4$) |
|---|---|---|---|
| `0000` | 1 | yes | |
| `0001` | 4 | yes | yes |
| `0010` | 3 | | |
| `0011` | 4 | yes | yes |
| `0101` | 2 | yes | |
| `0110` | 3 | | |
| `0111` | 4 | yes | yes |
| `1111` | 1 | yes | |

For instance, at $a[0..2] = $ `011` with $p = 3$, line L5 sets $a[3] = a[0] = 0$, giving `0110` with $p = 3$, and line L7 sets $a[3] = 1$, giving the Lyndon word `0111` with $p = 4$. At `010`, with $p = 2$, line L5 adds $a[1] = 1$ to get `0101`, and the loop of line L6 is empty. The 6 necklaces and 3 Lyndon words agree with the counts $\frac{1}{4}\sum_{d \mid 4} \varphi(d)\, 2^{4/d} = 6$ and $\frac{1}{4}\sum_{d \mid 4} \mu(d)\, 2^{4/d} = 3$. The run makes 19 calls: the root, and one call for each of the $2 + 3 + 5 + 8$ prenecklaces of lengths 1 to 4.

## Correctness

By induction on $t$, the call GEN$(t, p)$ is made exactly once for each prenecklace of length $t$, with $p$ equal to its $\mathrm{lyn}$: at $t = 1$ every letter is a Lyndon word, and the step from $t$ to $t + 1$ is the fundamental theorem above. Children are made in increasing order of the new letter, so the leaves at depth $n$ come in lexicographic order. A prenecklace $a$ of length $n$ is $u^\infty[0..n-1]$ with $u = a[0..p-1]$ Lyndon; it is a necklace exactly when $p$ divides $n$, since then $a = u^{n/p}$, and it is a Lyndon word exactly when $p = n$. The proof file proves the theorem and these tests in full.

## Complexity

- **Calls.** There is one call per prenecklace of length at most $n$, plus the root. A prenecklace of length $t$ with $\mathrm{lyn} = q$ is fixed by its Lyndon prefix, so the number of prenecklaces of length $t$ is $P_k(t) = \sum_{q \le t} L_k(q)$, where $L_k(q)$ counts the Lyndon words of length $q$. The total is $1 + \sum_{q=1}^{n} L_k(q)(n - q + 1)$.
- **Time.** With $L_k(q) \le k^q/q$, this sum is at most $2(k/(k-1))^2 k^n/n + n(n+1)k^{n/2} + 1$. The number of necklaces is $N \ge k^n/n$, so for $k \ge 2$ the number of calls is $O(N)$, and each call does $O(1)$ work besides its children: $\Theta(N)$ total time, constant amortized time per necklace. Listing only the Lyndon words is CAT too: the necklaces that are not Lyndon words have a smallest period $d < n$ dividing $n$, so there are at most $\sum_{d \le n/2} k^d \le 2k^{n/2}$ of them, and $L_k(n) = \Theta(N)$. Copying each output word costs $O(n)$ more per word; the CAT bound counts only the changes to $a$.
- **Space.** The array $a$ and a recursion stack of depth $n$: $\Theta(n)$.
- **One letter.** For $k = 1$ there is one necklace, $0^n$, found in $\Theta(n)$ time.

## Properties

- **Same order as FKM.** It visits the same prenecklaces, in the same order and with the same values of $p$, as the iterative [FKM algorithm](/fkm-algorithm/); only the control structure differs.
- **Prefix tree.** The calls form the trie of all prenecklaces of length at most $n$, and every leaf at depth $n$ is a prenecklace. No branch is a dead end, which is why the time is proportional to the output.
- **Online.** Each necklace is output as soon as its last letter is set, in lexicographic order.
- **de Bruijn sequences.** Writing $a[0..p-1]$ at each visit with $p \mid n$ concatenates the Lyndon words whose length divides $n$, which gives the lexicographically least [de Bruijn sequence](/de-bruijn-sequence/).

## Variants and improvements

- **Lyndon words and prenecklaces.** Change the test of line L3 to $p = n$ for Lyndon words, or drop it for all prenecklaces.
- **Fixed content.** Sawada (2003) restricted the recursion to words with a given number of each letter and kept the time CAT; the recursive form makes such restrictions local to the loop of line L6.
- **Binary unlabeled necklaces.** Cattell et al. extended the recursion to binary necklaces taken up to rotation and exchange of the two letters, also in CAT time.
- **Irreducible polynomials.** The binary Lyndon words of length $n$, read as exponents $e$, pick one exponent from each class $\{e, 2e, 4e, \ldots\} \bmod 2^n - 1$ of size $n$, and the minimal polynomials of the powers $\alpha^e$ of a primitive element $\alpha$ of GF$(2^n)$ are then the [irreducible polynomials](/irreducible-polynomial/) of degree $n$, each once. Cattell et al. used the recursion to list the irreducible and the primitive polynomials of degree $n$ quickly.
- **Bracelets and more.** Sawada later gave CAT algorithms for [bracelets](/bracelet/) and other restricted necklaces from the same recursion.

## When to use it

Use it to list necklaces, Lyndon words or prenecklaces of a fixed length when you also want to restrict the words, for example by content, forbidden factors or a density of ones: a test placed before a recursive call prunes whole subtrees. For plain necklaces in lexicographic order, the iterative FKM algorithm does the same work without a stack.

## Pitfalls

- **Starting the recursion.** The first letter has no letter $p$ positions back. Line L1 tries every letter with $p = 1$; a common alternative is a 1-based array with a sentinel $a[0] = 0$ and the call GEN$(1, 1)$. Mixing the two conventions shifts every index.
- **Reading $a[t - p]$ after the first call.** Line L6 reads $a[t - p]$ after GEN$(t + 1, p)$ returns. That cell has index below $t$, so the deeper calls do not change it; reading $a[t]$ instead would be wrong.
- **Testing $p = n$ for necklaces.** That outputs only the Lyndon words; the necklace test is $n \bmod p = 0$, which also accepts periodic necklaces such as `0101`.
- **Deep recursion.** The depth is $n$. In languages with a small call stack, use an explicit stack for large $n$ with $k = 1$ or $k = 2$, where $n$ can be large before the output is.

## Implementations

## History

Fredricksen, Kessler and Maiorana gave the iterative algorithm in the 1970s and 1980s, and Ruskey, Savage and Wang proved in 1992 that it runs in constant amortized time. Cattell, Ruskey, Sawada, Serra and Miers published the recursive form in the Journal of Algorithms in 2000, with a proof of the CAT bound based on the fundamental theorem of necklaces, the first CAT algorithm for binary unlabeled necklaces, and an application to irreducible polynomials over GF(2). Sawada and others then used the recursion for necklaces with fixed content, bracelets and other restricted classes.

## References
