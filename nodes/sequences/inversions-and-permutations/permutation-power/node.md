---
tag: 34E513
kind: technique
slug: permutation-power
name: Applying a permutation k times
area: sequences/inversions-and-permutations
level: core
summary: Computes the k-th power of a permutation in logarithmic steps by squaring, instead of applying it k times one by one.
prereqs: [permutation, permutation-cycles, binary-exponentiation]
see_also: [permutation-inverse, symmetric-group, faro-shuffle, binary-lifting, least-common-multiple, chinese-remainder-theorem, matrix-exponentiation, cycle-leader-permutation]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.3.3 (applications to permutations, products of permutations and their cycle forms)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3 (evaluation of powers, the binary method)
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 4.3 (cycle decomposition, and the order of a permutation as the least common multiple of its cycle lengths)
---

The $k$-th power $\pi^k$ of a [permutation](/permutation/) $\pi$ is $\pi$ applied $k$ times, $\pi^k(i) = \pi(\pi(\cdots \pi(i)))$. Applying $\pi$ step by step costs $\Theta(nk)$, which is useless for $k = 10^{18}$. [Binary exponentiation](/binary-exponentiation/) computes $\pi^k$ with about $2\lg k$ compositions of $O(n)$ time each, and the [cycle decomposition](/permutation-cycles/) does better: on a cycle of length $L$, $\pi^k$ moves every element $k \bmod L$ places forward, so $\pi^k$ takes $\Theta(n)$ time for any $k$. The same ideas give negative powers, the order of $\pi$, and the smallest $k$ with $\pi^k = \sigma$.

## In plain words

Suppose a fixed shuffle of a deck is repeated many times, and you want the order of the deck after a billion shuffles. Doing the shuffle a billion times is too slow.

One way is doubling. Doing the shuffle twice is itself a shuffle, and you can work it out once. Doing that twice gives four shuffles, then eight, and so on. Any number of shuffles is a sum of such doublings, so about thirty combined shuffles reach a billion.

A faster way looks at the loops of the shuffle. Each card travels around a loop of positions and comes back after as many steps as the loop is long. So after a billion shuffles a card on a loop of 7 positions has moved a billion modulo 7 places along its loop, and you can place it directly.

## When it applies

- A fixed rearrangement is applied many times: a card shuffle, a step of a puzzle, the moves of a game, a relabeling repeated in each round of a simulation.
- The step is a bijection on a finite set, so its functional graph is a union of cycles. If the step is any function, not a bijection, the graph also has tails leading into cycles, and [binary lifting](/binary-lifting/) or doubling replaces the cycle method.
- The array of items should end up rearranged as if the step were done $k$ times: if one step is the gather $A'[i] = A[\pi(i)]$, then $k$ steps give $A^{(k)}[i] = A[\pi^k(i)]$.

## The template

**Composition.** For permutations as arrays, $(\sigma\tau)(i) = \sigma(\tau(i))$ takes one pass, $\Theta(n)$ time. Powers of one permutation commute, so the order of the factors in $\pi^a \pi^b = \pi^{a+b}$ does not matter.

**By squaring.** Write $k$ in binary and keep $R = \pi^{(\text{bits seen})}$ and $S = \pi^{2^t}$:

```pseudo
POWER-BY-SQUARING(π, k)                    ▷ k ≥ 0
1  R ← identity, S ← π
2  while k > 0 do
3      if k is odd then R ← R ∘ S
4      S ← S ∘ S, k ← ⌊k / 2⌋
5  return R
```

It makes $\lfloor \lg k \rfloor + 1 + \nu(k)$ compositions for $k \ge 1$, where $\nu(k)$ is the number of 1 bits of $k$, one fewer if the last squaring is skipped, so $O(n \log k)$ time and three arrays of $n$ entries.

**By cycles.** Each cycle $(c_0\, c_1 \cdots c_{L-1})$ of $\pi$ satisfies $\pi^k(c_j) = c_{(j + k) \bmod L}$.

```pseudo
POWER-BY-CYCLES(π, k)                      ▷ any integer k, also negative
1  seen[i] ← false for all i
2  for i ← 1 to n do
3      if not seen[i] then
4          collect the cycle c_0 = i, c_1 = π(c_0), ..., c_{L−1}, marking each seen
5          s ← k mod L                     ▷ in 0 .. L − 1, also for k < 0
6          for j ← 0 to L − 1 do R[c_j] ← c_{(j + s) mod L}
7  return R
```

Every element is collected and written once, so the time is $\Theta(n)$ for every $k$, plus the cost of reducing $k$ modulo each cycle length, which is one division per cycle.

**Order.** The least $m > 0$ with $\pi^m = \mathrm{id}$ is the [least common multiple](/least-common-multiple/) of the cycle lengths. So $\pi^k = \pi^{k \bmod m}$, and $\pi^{-1} = \pi^{m-1}$.

## Classic examples

- **Inverse and negative powers.** $\pi = 3\,6\,4\,1\,5\,2$ has the cycles $(1\,3\,4)(2\,6)(5)$ and order $\operatorname{lcm}(3, 2, 1) = 6$. So $\pi^{-1} = \pi^5 = 4\,6\,1\,3\,5\,2$, the [inverse](/permutation-inverse/).
- **A huge exponent.** For the same $\pi$, $\pi^{100}$ shifts the 3-cycle by $100 \bmod 3 = 1$ and the 2-cycle by $100 \bmod 2 = 0$, so $\pi^{100} = 3\,2\,4\,1\,5\,6$: it agrees with $\pi$ on $\{1, 3, 4\}$ and fixes 2 and 6.
- **A single cycle.** $\pi = 3\,1\,4\,5\,2$ is the 5-cycle $(1\,3\,4\,5\,2)$. Its square moves each element two places along the cycle, $\pi^2 = 4\,3\,5\,2\,1$, and $\pi^5$ is the identity.
- **Perfect shuffles.** The out-shuffle of a 52-card deck, which interleaves the two halves and keeps the top card on top, sends position $i$ to $2i \bmod 51$ for $0 \le i \le 50$ and fixes position 51. The order of 2 modulo 51 is 8, so 8 out-shuffles restore the deck. See the [faro shuffle](/faro-shuffle/).
- **Repeated moves in a contest problem.** "Apply this rearrangement $k$ times, $k \le 10^{18}$" is solved by the cycle method in $O(n)$ time, avoiding the $\Theta(nk)$ simulation.

## Variations

- **Discrete logarithm in $S_n$.** Given $\pi$ and $\sigma$, find the least $k \ge 0$ with $\pi^k = \sigma$. On each cycle of $\pi$ of length $L$, $\sigma$ must act as a shift by some $s$, which gives the congruence $k \equiv s \pmod L$. The system of congruences has a solution exactly when it is consistent, and the generalized [Chinese remainder theorem](/chinese-remainder-theorem/) finds the least one in $O(n)$ arithmetic operations on numbers up to the order of $\pi$.
- **Roots.** Finding $\sigma$ with $\sigma^k = \pi$ is the reverse problem. For $k = 2$, a cycle of odd length has a square root that is a cycle of the same length, and two cycles of the same even length combine into one square root cycle of twice the length. A square root exists exactly when for every even $L$ the number of cycles of length $L$ is even.
- **Powers of a function.** For an arbitrary map $f : [n] \to [n]$, the [functional graph](/functional-graph/) has tails as well as cycles. Doubling tables $f^{2^t}$ answer $f^k(i)$ for one $i$ in $O(\log k)$ time after $O(n \log k)$ preprocessing, which is [binary lifting](/binary-lifting/). The cycle method extends by walking the tail first and then reducing the rest of $k$ modulo the cycle length.
- **Applying the power in place.** POWER-BY-CYCLES produces $\pi^k$ as a new array. To rearrange an array $A$ by $\pi^k$ without building it, rotate each cycle of $A$ by $k \bmod L$ places, using the methods of [in-place permutation](/in-place-permutation/).
- **Other groups.** Binary exponentiation works in any monoid, for example for [matrix powers](/matrix-exponentiation/). The cycle method is special to permutations: it is what makes $\pi^k$ cheaper to compute than a generic power.

## Pitfalls

- **Composition order.** $(\sigma\tau)(i) = \sigma(\tau(i))$ applies $\tau$ first. For powers of a single $\pi$ the order is irrelevant, but in POWER-BY-SQUARING with two different permutations, as when combining a fixed prefix with a power, the wrong order gives a wrong answer.
- **Scatter versus gather.** Repeating the gather $A'[i] = A[\pi(i)]$ gives $A[\pi^k(i)]$, but repeating the scatter $A'[\pi(i)] = A[i]$ gives $A'[\pi^k(i)] = A[i]$, which is the gather by $\pi^{-k}$. Check with a 3-cycle.
- **Negative remainders.** In C, C++ and Java, $k \bmod L$ is negative for negative $k$. Add $L$ when the remainder is negative.
- **Overflow of the order.** The largest order of a permutation of $[n]$, Landau's function, is the largest lcm of numbers that sum to $n$. It exceeds $2^{32}$ from $n = 120$ and $2^{64}$ from $n = 358$. Reduce $k$ modulo each cycle length separately instead of modulo the order.
- **Mixing up position and value.** Writing $R[c_{(j+s) \bmod L}] \leftarrow c_j$ instead of $R[c_j] \leftarrow c_{(j+s) \bmod L}$ computes $\pi^{-k}$.

## Exercises

1. Compute $\pi^{7}$ and $\pi^{-2}$ for $\pi = 2\,3\,1\,5\,4$ by the cycle method, and check the first by squaring.
   <details><summary>Hint</summary>The cycles are $(1\,2\,3)$ and $(4\,5)$. Reduce 7 modulo 3 and modulo 2.</details>
2. Show that POWER-BY-SQUARING keeps the invariant $R \circ S^{k} = \pi^{k_0}$, where $k_0$ is the input exponent and $k$ the current one, and conclude that it returns $\pi^{k_0}$.
3. Find the least $k > 0$ with $\pi^k = \sigma$ for $\pi = 2\,3\,1\,5\,4$ and $\sigma = 3\,1\,2\,4\,5$, or show that none exists.
   <details><summary>Hint</summary>On $(1\,2\,3)$, $\sigma$ is a shift by 2; on $(4\,5)$ it is a shift by 0.</details>
4. Prove that the order of $\pi$ is the least common multiple of its cycle lengths.
5. Give a permutation of $[5]$ with no square root, and one of $[4]$ that has a square root although it has a cycle of even length.
6. A deck of $2m$ cards is out-shuffled $k$ times. Express the position of the card that started at position $i$ in terms of $2^k \bmod (2m - 1)$, and compute the number of out-shuffles that restore a deck of 10 cards.

## References
