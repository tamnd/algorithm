---
title: A sort with a random comparator does not give a uniform order
proves: [correctness, termination]
status: full
---

This file proves that the random-comparator shuffle fails for $n \ge 3$, and it gives the exact output distribution of COIN-INSERTION-SHUFFLE. The correct sort-based method, with random keys, is proved on [permute by sorting](/permute-by-sorting/).

## The general theorem

**Model.** A comparison sort is a procedure that, on an input of $n$ items, asks questions LESS$(x, y)$ and gets yes or no answers. We assume only that it stops for every sequence of answers, and that there is a number $B$ such that it never asks more than $B$ questions. In the random-comparator shuffle each answer is an independent fair coin.

**Theorem 1.** Under this model, for each output order $\tau$ there is an integer $m_\tau \ge 0$ with $\Pr[\text{output} = \tau] = m_\tau / 2^B$. For $n \ge 3$, no order has probability $1/n!$, so the output is not uniform.

*Proof.* Extend each run with unused coins so that every run reads exactly $B$ coins; the extra coins do not change the output. Then a run is a function of a sequence in $\{0, 1\}^B$, all $2^B$ sequences have probability $2^{-B}$, and $\Pr[\text{output} = \tau] = m_\tau / 2^B$, where $m_\tau$ is the number of sequences with output $\tau$. If $m_\tau / 2^B = 1/n!$, then $n! \, m_\tau = 2^B$. For $n \ge 3$, 3 divides the left side and not the right side. $\square$

**Every sort has a bound $B$.** A sort that stops for every answer sequence has a finite decision tree (by König's lemma, since each node has two children and no path is infinite). Its depth is the bound $B$. Concretely, insertion sort makes at most $\binom{n}{2}$ comparisons, and top-down merge sort makes at most $n \lceil \log_2 n \rceil$. So Theorem 1 applies to every practical comparison sort.

For $n \le 2$ the theorem says nothing, and in fact the method is fair: with two items, one comparison decides the order, and it is a fair coin.

## The exact distribution for insertion sort

**Termination.** In COIN-INSERTION-SHUFFLE, the inner loop of line L3 decreases $j$ at each turn and stops at $j = -1$ at the latest. So the iteration for $i$ reads at most $i + 1$ coins, and the whole run reads at most $\sum_{i=1}^{n-1}(i+1)$ coins.

**Theorem 2.** Let $K_i$ be the number of places that item $x = A[i]$ moves to the left in the iteration for $i$. Then $K_1, \ldots, K_{n-1}$ are independent, and
$$\Pr[K_i = k] = 2^{-(k+1)} \text{ for } 0 \le k < i, \qquad \Pr[K_i = i] = 2^{-i}.$$
The output is determined by $(K_1, \ldots, K_{n-1})$, and different sequences give different outputs. So the output $\tau$ with move sequence $(k_1, \ldots, k_{n-1})$ has probability $\prod_i \Pr[K_i = k_i]$.

*Proof.* In the iteration for $i$, the loop moves $x$ one place left for each coin 0 and stops at the first coin 1 or when $j < 0$. So $K_i = k < i$ means $k$ zeros and then a one, with probability $2^{-k} \cdot \frac12$, and $K_i = i$ means $i$ zeros, with probability $2^{-i}$. The coins of different iterations are disjoint, so the $K_i$ are independent.

The sequence $(K_i)$ is the inversion table of the output read in a fixed way: after the iteration for $i$, the item that started at position $i$ stands at position $i - K_i$ among the first $i + 1$ items, and later iterations only insert items before or after it without changing the relative order of the first $i + 1$ items. So the relative order of the first $i + 1$ items in the output is fixed by $K_1, \ldots, K_i$, and conversely $K_i$ is read from the output as the number of items with start position less than $i$ that come after item $i$. This is a bijection between the $n!$ sequences with $0 \le k_i \le i$ and the $n!$ orders (the [Lehmer code](/lehmer-code/)). $\square$

**Consequences.**

- The identity has $K_i = 0$ for all $i$, so its probability is $2^{-(n-1)}$. For $n \ge 3$, $2^{-(n-1)} > 1/n!$, since $n! > 2^{n-1}$.
- The reversed order has $K_i = i$ for all $i$, so its probability is $\prod_i 2^{-i} = 2^{-\binom{n}{2}}$.
- $E[K_i] = 1 - 2^{-i} < 1$. In a uniform order, the corresponding count is uniform on $\{0, \ldots, i\}$, with mean $i/2$.

**Example, $n = 3$.** $K_1 \in \{0, 1\}$ with probabilities $\frac12, \frac12$. $K_2 \in \{0, 1, 2\}$ with probabilities $\frac12, \frac14, \frac14$. The products give $\frac14$ for $[0,1,2]$ and $[1,0,2]$ ($K_2 = 0$), and $\frac18$ for each of the four orders with $K_2 \ge 1$. This matches the table of the page and the exact enumeration in the test file.

## Merge sort for n = 3

The left half is $[0]$ and the right half is $[1, 2]$. Sorting the right half reads one coin: 0 gives $[2, 1]$ and 1 gives $[1, 2]$, each with probability $\frac12$. Call the right run $[r_0, r_1]$. The merge of $[0]$ with $[r_0, r_1]$ reads a coin: 1 takes 0 first, and the output is $[0, r_0, r_1]$ with probability $\frac12$. A coin 0 takes $r_0$, and then a second coin places 0 before or after $r_1$, with probability $\frac14$ each. So the orders $[0, 1, 2]$ and $[0, 2, 1]$ have probability $\frac12 \cdot \frac12 = \frac14$ each, and the other four orders $\frac12 \cdot \frac14 = \frac18$ each. The total variation distance to uniform is $\frac12 (2 \cdot \frac1{12} + 4 \cdot \frac1{24}) = \frac16$.
