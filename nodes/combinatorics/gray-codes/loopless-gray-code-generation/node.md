---
tag: 32MDEZ
kind: algorithm
slug: loopless-gray-code-generation
name: Loopless Gray code generation (Ehrlich)
aliases:
- Ehrlich's algorithm
- focus pointer algorithm
- Algorithm L (loopless Gray binary generation)
- Bitner-Ehrlich-Reingold algorithm
area: combinatorics/gray-codes
level: advanced
summary: Uses a focus pointer to find the next codeword in constant time per step, with no loop.
solves: [gray-code-generation]
model: word-ram
complexity:
  vars: {n: the length of the strings, N: the number of strings (2^n)}
  time: {worst: Θ(2^n), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1976
  people: [James R. Bitner, Gideon Ehrlich, Edward M. Reingold]
  note: Ehrlich defined loopless generation in 1973. Bitner, Ehrlich and Reingold gave the focus pointer generator for the reflected Gray code in 1976, and Knuth presents it as Algorithm L.
prereqs: [binary-reflected-gray-code, ruler-sequence, loopless-generation]
see_also: [gray-code-generation, k-ary-gray-code, constant-amortized-time-generation, trailing-zero-count, binary-counter-increment, ehrlich-loopless-combinations, power-set-enumeration, tower-of-hanoi]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (Algorithm G, Gray binary generation; Algorithm L, loopless Gray binary generation, with its focus pointers and the trace for n = 4)
  - paper: doi:10.1145/360336.360343
    title: James R. Bitner, Gideon Ehrlich and Edward M. Reingold, Efficient generation of the binary reflected Gray code and its applications, Communications of the ACM 19(9), 517 to 521, 1976
    locator: the loopless generator of the reflected Gray code
  - paper: doi:10.1145/321765.321781
    title: Gideon Ehrlich, Loopless algorithms for generating permutations, combinations, and other combinatorial configurations, Journal of the ACM 20(3), 500 to 513, 1973
    locator: the definition of a loopless algorithm
---

Loopless Gray code generation visits all $N = 2^n$ binary strings of length $n$ in the order of the [binary reflected Gray code](/binary-reflected-gray-code/), and does only a fixed number of operations between two visits. It keeps the string in an array and adds an array of $n + 1$ *focus pointers*; the first pointer always names the next bit to flip, which is the [ruler function](/ruler-sequence/) $\rho(k)$ at step $k$. The method is due to Bitner, Ehrlich and Reingold (1976), and Knuth presents it as Algorithm L. It needs no word operations beyond assignment and comparison, so it works for any $n$, not only for $n$ up to the word size.

## In plain words

Picture a row of $n$ lamps, all off. At each step one lamp changes, and after $2^n - 1$ steps every on and off pattern has been seen once. The rule for which lamp to change is the Gray code rule: the first lamp at odd steps, and otherwise the lamp just after the first lamp that is on.

A simple program finds that lamp by scanning from the left, which can take many checks. This method keeps a small note for each lamp that says where the scan would end. Each step reads one note, changes two notes, and changes one lamp. So each step takes the same small amount of work, however many lamps there are.

## The problem

Given $n \ge 0$, visit each string of $\{0,1\}^n$ once, in the order $\Gamma_n$ of the reflected Gray code, with $O(1)$ worst-case time between two visits. This is [Gray code generation](/gray-code-generation/) with the strongest delay bound. The generator keeps the current string in an array $a_{n-1} \ldots a_0$, where $a_j$ is bit $j$, and *visits* it: the caller reads the array in place and does not get a copy. Step $k$, for $1 \le k < N$, changes the string from $g(k - 1)$ to $g(k)$, where $g(k) = k \oplus \lfloor k/2 \rfloor$, and the bit it flips is $\rho(k)$, the number of trailing zeros of $k$.

## The algorithm

The focus pointers are $f_0, \ldots, f_n$. In the proof, $f_0$ is the number of trailing ones of the step counter, so it is the next bit to flip. A pointer $f_j$ with $j \ge 1$ is either $j$ itself or the end of a run of ones in the counter that starts at bit $j$.

```pseudo id=main
LOOPLESS-GRAY(n)
L1  for j ← 0 to n − 1 do a_j ← 0; f_j ← j
L2  f_n ← n
L3  loop
L4      visit a_{n−1} … a_1 a_0
L5      j ← f_0; f_0 ← 0                     ▷ j = ρ(k) at the k-th time here
L6      if j = n then return                ▷ all 2^n strings visited
L7      f_j ← f_{j+1}; f_{j+1} ← j + 1      ▷ move the focus
L8      a_j ← 1 − a_j                       ▷ flip bit j
```

Lines L1 and L2 run once and take $\Theta(n)$ time. Each pass through lines L4 to L8 does at most four assignments, one test and one visit.

## Example

For $n = 4$ the table shows the state at line L4 each time. The pointer row is $f_0 f_1 f_2 f_3 f_4$.

| $k$ | $a_3 a_2 a_1 a_0$ | $f_0 \ldots f_4$ | next $j$ | | $k$ | $a_3 a_2 a_1 a_0$ | $f_0 \ldots f_4$ | next $j$ |
|---|---|---|---|---|---|---|---|---|
| 0 | 0000 | 0 1 2 3 4 | 0 | | 8 | 1100 | 0 1 2 4 4 | 0 |
| 1 | 0001 | 1 1 2 3 4 | 1 | | 9 | 1101 | 1 1 2 4 4 | 1 |
| 2 | 0011 | 0 2 2 3 4 | 0 | | 10 | 1111 | 0 2 2 4 4 | 0 |
| 3 | 0010 | 2 1 2 3 4 | 2 | | 11 | 1110 | 2 1 2 4 4 | 2 |
| 4 | 0110 | 0 1 3 3 4 | 0 | | 12 | 1010 | 0 1 4 3 4 | 0 |
| 5 | 0111 | 1 1 3 3 4 | 1 | | 13 | 1011 | 1 1 4 3 4 | 1 |
| 6 | 0101 | 0 3 2 3 4 | 0 | | 14 | 1001 | 0 4 2 3 4 | 0 |
| 7 | 0100 | 3 1 2 3 4 | 3 | | 15 | 1000 | 4 1 2 3 4 | 4, stop |

Look at $k = 6$, binary 0110. The counter has no trailing ones, so $f_0 = 0$. Bit 0 of the counter is 0 and a run of two ones starts at bit 1, so $f_1 = 1 + 2 = 3$. Bits 1 and 2 of the counter are 1, so $f_2 = 2$ and $f_3 = 3$. At $k = 7$, line L5 reads $j = f_0 = 3$, line L7 sets $f_3 \leftarrow f_4 = 4$ and $f_4 \leftarrow 4$, and line L8 flips bit 3, which gives 1100 at $k = 8$. At $k = 15$, $f_0 = 4 = n$, and the generator stops after 16 visits.

## Correctness

For $0 \le k < 2^n$, let $t_j(k)$ be the length of the run of ones in the binary form of $k$ that starts at bit $j$, that is, the largest $t$ with bits $j, \ldots, j + t - 1$ of $k$ all equal to 1. Bits at positions $n$ and higher are 0. The proof in `proofs/correctness.md` shows this invariant at the $k$-th arrival at line L4, counting from 0:

- $a_{n-1} \ldots a_0 = g(k)$;
- for each $0 \le j \le n$: if $j = 0$ or bit $j - 1$ of $k$ is 0, then $f_j = j + t_j(k)$, and otherwise $f_j = j$.

So line L5 reads $j = f_0 = t_0(k)$, the number of trailing ones of $k$, which is $\rho(k + 1)$. If $k < 2^n - 1$ then $j < n$, and flipping bit $\rho(k+1)$ of $g(k)$ gives $g(k+1)$. If $k = 2^n - 1$ then $j = n$ and the loop stops. Lines L7 and L8 restore the invariant for $k + 1$: the run of ones at the bottom of $k$ becomes zeros in $k + 1$, so their pointers reset, and the run above bit $j$ grows by one, so its pointer moves to $f_j$. Since $g$ is one-to-one on $[0, 2^n)$, each string is visited once.

## Complexity

- **Time.** Initialization takes $\Theta(n)$. After that, each visit costs $O(1)$ in the worst case, independent of $n$: the algorithm is loopless. The total is $\Theta(n + N) = \Theta(N)$, which meets the $\Omega(N)$ lower bound for any method that visits $N$ strings.
- **Space.** The string has $n$ entries and the pointers $n + 1$, so the extra space is $\Theta(n)$.
- **Output.** The string is changed in place, one entry per step. A caller that copies each string pays $\Theta(n)$ per string, $\Theta(nN)$ in total.
- **Model.** The pointers hold values up to $n$, so they fit in a word whenever an index into the array does. No shift, exclusive or or bit count is used, so $n$ may be larger than the word size $w$.

## Properties

- **Same list as the reflected code.** The output order is exactly $\Gamma_n$, and the flipped bits form the ruler sequence $0, 1, 0, 2, 0, 1, 0, 3, \ldots$.
- **Deterministic delay.** The worst case and the average case per step are the same constant. This matters when each visit must meet a deadline.
- **In place.** The visited array is the state itself, and one entry changes per step.
- **Not resumable from a string alone.** The pointers depend on the step counter $k$, not only on the string $g(k)$. To start in the middle, compute $k$ from the string with [Gray to binary conversion](/gray-to-binary-conversion/) and then set the pointers from the invariant.

## Variants and improvements

- **Parity rule (Knuth, Algorithm G).** Keep the parity of the number of ones. If it is even, flip bit 0; if it is odd, flip the bit to the left of the lowest 1. Finding the lowest 1 by a scan costs $O(n)$ in the worst case, but $O(1)$ amortized, so this generator is CAT, not loopless. See [constant amortized time generation](/constant-amortized-time-generation/).
- **Counter and trailing zero count.** Keep a counter $k$ in a word and flip bit $\rho(k)$, computed with a [trailing zero count](/trailing-zero-count/) instruction. This is $O(1)$ worst case too, but it needs $n \le w$ and the instruction.
- **Mixed radix.** The same focus pointers drive the reflected Gray code for digits with radices $m_0, \ldots, m_{n-1}$, with one direction flag per digit: see [k-ary Gray code](/k-ary-gray-code/).
- **Other objects.** Ehrlich's idea of a loopless generator applies to permutations, combinations and other families. For combinations, see [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/).

## When to use it

Use it when you walk through all subsets of a set and each step must take a bounded time, for example in a real-time loop or in a generator that hands each subset to a caller before computing the next. It is also the right choice when $n$ is larger than a machine word, since it uses only array indexing. If the loop body costs much more than one step, the simpler parity rule or a counter with a trailing zero count is as fast in practice. If you need random access to the list, use [binary to Gray conversion](/binary-to-gray-conversion/) instead.

## Pitfalls

- **Wrong order of the two writes in line L5.** Writing "$f_0 \leftarrow 0$; $j \leftarrow f_0$" makes $j$ always 0, so the generator flips bit 0 forever. Line L5 must read $f_0$ into $j$ first, then set $f_0 \leftarrow 0$.
- **Wrong order in line L7.** Writing "$f_{j+1} \leftarrow j + 1$; $f_j \leftarrow f_{j+1}$" sets $f_j$ to $j + 1$ and loses the end of the run. For $n = 3$ the delta sequence becomes 0, 1, 0, 1, 0, 1, ..., which returns to 000 after four steps and never ends. Line L7 must copy $f_{j+1}$ into $f_j$ before it resets $f_{j+1}$.
- **No sentinel.** Without line L2, the test in line L6 never sees $j = n$, and line L7 reads $f_{n+1}$ out of bounds. Line L2 must set $f_n \leftarrow n$, and the array must have $n + 1$ entries.
- **Keeping the visited array.** The generator yields the same array each time. Storing the reference in a list without a copy stores $N$ references to the last string. Copy the array at line L4 if you keep it.

## Implementations

## History

Gideon Ehrlich introduced loopless generation in 1973: an algorithm is loopless when the number of operations between two visits is bounded in advance. James Bitner, Ehrlich and Edward Reingold applied the idea to the reflected Gray code in 1976 with the focus pointers above. Knuth presents it as Algorithm L in Section 7.2.1.1, next to the parity based Algorithm G, and uses the same pointers for the reflected mixed-radix code in Algorithm H.

## References
