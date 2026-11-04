---
tag: 3THY5A
kind: theorem
slug: zero-one-principle
name: Zero-one principle
aliases:
- 0-1 principle
- Knuth's 0-1 principle
area: sorting/sorting-networks
level: core
summary: A comparator network sorts all inputs iff it sorts all 0-1 inputs.
prereqs: [sorting-network, comparator]
see_also: [sorting-network-verification, bitonic-merger, odd-even-merge-sort, merging-network, pairwise-sorting-network, minimum-size-sorting-network]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting, Theorem Z (the zero-one principle)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Section 27.2, The zero-one principle (Lemma 27.1 and Theorem 27.2)
  - paper: doi:10.1007/BFb0035109
    title: Ian Parberry, On the computational complexity of optimal sorting network verification, PARLE 91, Lecture Notes in Computer Science (1991)
    locator: Section 1 (the zero-one principle and the single exception sorting networks of Chung and Ravikumar)
  - paper: doi:10.1016/0022-0000(89)90017-2
    title: M. J. Chung and B. Ravikumar, Strong nondeterministic Turing reduction, a technique for proving intractability, Journal of Computer and System Sciences 39(1) (1989)
    locator: pp. 2 to 20
---

The zero-one principle says that a network of [comparators](/comparator/) sorts every input if and only if it sorts every input whose items are only 0 and 1. So to prove that a [sorting network](/sorting-network/) on $n$ wires is correct, it is enough to check $2^n$ inputs instead of all $n!$ orders of $n$ items, or to give a proof that handles only zeros and ones. Knuth states it as Theorem Z, and it is the tool behind the proofs of [bitonic sort](/bitonic-sort/), [odd-even merge sort](/odd-even-merge-sort/) and most other networks.

## Statement

Let $N$ be a comparator network on $n$ wires, with standard or general comparators. For a totally ordered set $X$ and $x \in X^n$, write $N(x)$ for the output of $N$ on the input $x$. Say that $N$ *sorts* $x$ when $N(x)_0 \le N(x)_1 \le \cdots \le N(x)_{n-1}$.

**Theorem (zero-one principle).** If $N$ sorts each $x \in \{0, 1\}^n$, then $N$ sorts each $x \in X^n$, for each totally ordered set $X$.

The converse is true because $\{0, 1\}$ is a totally ordered set. When all comparators of $N$ are standard, a sorted input passes through $N$ unchanged, so it is enough to check the $2^n - n - 1$ inputs of zeros and ones that are not sorted.

**Lemma (monotone maps).** Let $f : X \to Y$ be a non-decreasing map between totally ordered sets, and write $f(x) = (f(x_0), \ldots, f(x_{n-1}))$. Then $N(f(x)) = f(N(x))$ for each $x \in X^n$.

## In plain words

A network makes the same comparisons whatever the input is. Suppose the network makes a mistake on some list of numbers: at the end, a larger number sits just before a smaller one. Now replace each number by 0 if it is smaller than the larger of those two numbers, and by 1 if it is not. Each comparison of the new list has the same result as the comparison of the old list, so the zeros and ones move exactly as the numbers moved. At the end, a 1 sits just before a 0, which is also a mistake. So a network that never fails on lists of zeros and ones never fails at all.

## Proof

*Proof of the lemma.* By induction on the number $s$ of comparators. For $s = 0$ both sides are $f(x)$. Let $s \ge 1$, let $N'$ be the first $s - 1$ comparators and let $c$ be the last one, so $N = c \circ N'$. By the induction hypothesis, $N'(f(x)) = f(N'(x))$. A single comparator on wires $i$ and $j$ commutes with $f$, because for $a \le b$ we have $f(a) \le f(b)$, so $\min(f(a), f(b)) = f(a) = f(\min(a, b))$ and $\max(f(a), f(b)) = f(b) = f(\max(a, b))$; the case $a > b$ is the same with the roles exchanged, and the other wires do not change. This holds whichever of the two wires gets the minimum. So $N(f(x)) = c(f(N'(x))) = f(c(N'(x))) = f(N(x))$. $\square$

*Proof of the theorem.* Suppose that $N$ sorts each input in $\{0, 1\}^n$ but does not sort some $x \in X^n$. Let $y = N(x)$. Then there is an index $k$ with $y_k > y_{k+1}$. Define $f : X \to \{0, 1\}$ by $f(t) = 0$ if $t < y_k$ and $f(t) = 1$ if $t \ge y_k$. This map is non-decreasing. By the lemma, $N(f(x)) = f(y)$. Here $f(y_k) = 1$ because $y_k \ge y_k$, and $f(y_{k+1}) = 0$ because $y_{k+1} < y_k$. So the output $N(f(x))$ has a 1 at position $k$ and a 0 at position $k + 1$, and $N$ does not sort the input $f(x) \in \{0, 1\}^n$. This contradicts the assumption. $\square$

*Sorted inputs.* Let all comparators be standard and let $x \in \{0, 1\}^n$ be sorted. A comparator $[i{:}j]$ with $i < j$ sees $x_i \le x_j$ and changes nothing, so by induction each comparator sees a sorted list and $N(x) = x$. So only the $2^n - (n + 1)$ unsorted inputs need a check, because exactly $n + 1$ lists of zeros and ones of length $n$ are sorted. $\blacksquare$

**Example.** The network $[0{:}1], [1{:}2]$ on 3 wires does not sort. On $x = (2, 3, 1)$, the comparator $[0{:}1]$ changes nothing and $[1{:}2]$ gives $y = (2, 1, 3)$, with $y_0 > y_1$. The proof takes $f(t) = 1$ for $t \ge 2$ and $0$ else, so $f(x) = (1, 1, 0)$, and the network gives $(1, 0, 1) = f(y)$: a failure on zeros and ones, at the same position.

## Consequences

- **Testing a network.** A network on $n$ wires can be tested with $2^n$ inputs. With one machine word per wire that holds one bit for each of $w$ inputs, a comparator becomes a bitwise AND and a bitwise OR, so the test of all $2^n$ inputs takes $O(s \cdot 2^n / w)$ word operations for a network of size $s$. The 4-wire network $[0{:}1], [2{:}3], [0{:}2], [1{:}3], [1{:}2]$ needs only the $2^4 - 4 - 1 = 11$ unsorted inputs. See [sorting network verification](/sorting-network-verification/), which shows that no test is fast in the worst case.
- **Proofs of constructions.** The correctness proofs of the [bitonic merger](/bitonic-merger/), of Batcher's [odd-even merge](/odd-even-merge-sort/) and of the [pairwise sorting network](/pairwise-sorting-network/) count zeros instead of reasoning about arbitrary items.
- **Merging networks.** The same proof shows that a network merges each pair of sorted sequences of lengths $p$ and $q$ if it merges each pair of sorted 0-1 sequences, because $f$ maps a sorted sequence to a sorted sequence. There are only $(p + 1)(q + 1)$ such pairs. See [merging network](/merging-network/).
- **Searches for optimal networks.** The searches that proved the values of the [minimum size](/minimum-size-sorting-network/) and the [minimum depth](/minimum-depth-sorting-network/) for small $n$ represent a partial network by the set of 0-1 outputs that it can still produce.

## Tightness

The set of $2^n - n - 1$ unsorted 0-1 inputs can not be made smaller, as a test for all standard networks. For each unsorted $x \in \{0, 1\}^n$ there is a comparator network that sorts each other input of zeros and ones but does not sort $x$. Such a network is a *single exception sorting network*. Chung and Ravikumar gave a construction of polynomial size and depth, and used it to show that the verification problem is [co-NP-complete](/co-np-complete/) (Parberry 1991, Section 1). So a test that uses only 0-1 inputs must use each of them.

The principle needs the network to be made only of comparators. A step that exchanges two wires depending on the value of a third wire does not commute with non-decreasing maps, and the proof of the lemma fails for it.

## History

Knuth gives the principle as Theorem Z in Section 5.3.4 of *The Art of Computer Programming*, and CLRS (second edition) proves it as Theorem 27.2 with the monotone lemma as Lemma 27.1. Batcher's networks of 1968 and the work of Floyd and Knuth on optimal networks of the 1960s use the same reduction to zeros and ones.

## References
