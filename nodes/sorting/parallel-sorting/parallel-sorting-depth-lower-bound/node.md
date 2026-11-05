---
tag: 2WYJPS
kind: theorem
slug: parallel-sorting-depth-lower-bound
name: Parallel sorting depth lower bound
aliases:
- Omega(log n) depth lower bound for sorting
area: sorting/parallel-sorting
level: advanced
summary: Any parallel sorting circuit or PRAM algorithm with bounded fan-in needs Omega(log n) depth, since every output depends on all inputs.
prereqs: [parallel-sorting-problem, sorting-network, comparison-sort-lower-bound, crew-pram, boolean-circuit]
see_also: [network-depth, aks-sorting-network, cole-merge-sort, comparison-sort-lower-bound, crcw-pram, zero-one-principle, valiant-parallel-merge, decision-tree-model]
sources:
  - paper: doi:10.1137/0204030
    title: Leslie G. Valiant, Parallelism in comparison problems, SIAM Journal on Computing 4(3), 1975
    locator: the parallel comparison model with p processors, in which one round is p comparisons whose pairs may depend on earlier answers
  - paper: doi:10.1137/0215006
    title: Stephen Cook, Cynthia Dwork and Rüdiger Reischuk, Upper and lower time bounds for parallel random access machines without simultaneous writes, SIAM Journal on Computing 15(1), 1986
    locator: the main lower bound, that a CREW PRAM with any number of processors needs at least log_b n steps to compute the OR of n bits, with b = (5 + sqrt 21)/2
  - paper: doi:10.1145/65950.65958
    title: Paul Beame and Johan Håstad, Optimal bounds for decision problems on the CRCW PRAM, Journal of the ACM 36(3), 1989
    locator: the lower bound of Omega(log n / log log n) time for the parity of n bits on the CRCW PRAM with a polynomial number of processors
  - paper: doi:10.1137/0217049
    title: Richard Cole, Parallel merge sort, SIAM Journal on Computing 17(4), 1988
    locator: sorting in O(log n) time with n processors on the CREW and the EREW PRAM
  - paper: "Sanguthevar Rajasekaran and John H. Reif, Optimal and sublogarithmic time randomized parallel sorting algorithms, SIAM Journal on Computing 18(3), 1989, 594-607"
    locator: the randomized sublogarithmic time general sort on the CRCW PRAM
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 10, Lower bounds
---

The parallel sorting depth lower bound says that sorting $n$ keys in parallel needs $\Omega(\log n)$ steps in every model where one step combines a bounded number of values: circuits and [sorting networks](/sorting-network/) with gates of fan-in 2, the parallel comparison model with $O(n)$ processors, and the [CREW PRAM](/crew-pram/) with any number of processors. The reason is that some output depends on all $n$ inputs, and with fan-in 2 the number of inputs that can reach one value at most doubles per step. The [AKS network](/aks-sorting-network/) and [Cole's merge sort](/cole-merge-sort/) meet the bound. The [CRCW PRAM](/crcw-pram/) is the exception, and there the bound drops to $\Omega(\log n / \log \log n)$.

## Statement

Let $n \ge 2$.

**(a) Circuits.** Every circuit of gates of fan-in at most 2 that sorts $n$ inputs has depth at least $\lceil \lg n \rceil$. This holds for Boolean circuits that sort $n$ bits, and for [comparator](/comparator/) networks, where one comparator is a gate with two inputs and two outputs.

**(b) Parallel comparison model.** In the parallel comparison model of Valiant with $p$ processors, each round makes $p$ comparisons whose pairs may depend on all earlier answers, and all other work is free. Every algorithm in this model that sorts $n$ distinct keys uses at least $\lceil \lg n! \rceil / p$ rounds in the worst case. For $p = O(n)$ this is $\Omega(\log n)$.

**(c) Sorting networks, a sharper bound.** Every comparator network that sorts $n$ inputs has depth at least $\lceil \lg n! \rceil / \lfloor n/2 \rfloor$, which is $2 \lg n - O(1)$.

**(d) CREW PRAM.** Every CREW PRAM algorithm that sorts $n$ keys, with the input in cells $0, \ldots, n-1$ and the output in the same cells, takes at least $\log_b n$ steps, with $b = (5 + \sqrt{21})/2 \approx 4.79$, for any number of processors and any local computation. So it takes $\Omega(\log n)$ time. The same holds for the [EREW PRAM](/erew-pram/), which is weaker.

**(e) CRCW PRAM.** Every CRCW PRAM algorithm with a number of processors polynomial in $n$ that sorts $n$ keys takes $\Omega(\log n / \log \log n)$ time.

## In plain words

Look at the smallest output of a sort. To know it, you must look at every input in some way, because any input could be the smallest. In one step, a gate or a comparison joins only two values. So after one step a value knows about at most two inputs, after two steps at most four, after three steps at most eight, and so on. To reach a million inputs takes at least twenty steps.

A second way is to count answers. A million keys can come in a huge number of orders, and each comparison gives one yes-or-no answer. A million processors get a million answers per round, and the sort needs about nineteen million answers, so about nineteen rounds.

A machine whose processors can all write to one cell in one step can do a little better, but not much.

## Proof

**(a).** For a value $v$ computed in the circuit, let $D(v)$ be the set of inputs on which $v$ depends, that is, the inputs $x_i$ such that changing $x_i$ alone can change $v$. An input wire depends on one input. A gate of fan-in at most 2 at depth $t$ computes a function of two values of depth at most $t - 1$, so by induction on $t$, $|D(v)| \le 2^t$. Now restrict the inputs to the bits $0$ and $1$. A sorting circuit then puts the minimum of the bits, which is their AND, on its first output. Fix an input $x_i$, set all other inputs to $1$, and change $x_i$ from $1$ to $0$: the first output changes from $1$ to $0$. So the first output depends on all $n$ inputs, and the depth $t$ of the circuit satisfies $2^t \ge n$. For a comparator network, each output of a comparator is the minimum or the maximum of its two inputs, so it is a gate of fan-in 2, and the same argument applies. $\square$

**(b).** The run of an algorithm in this model on the inputs with $n$ distinct keys is a tree. A node is the state after some rounds. The algorithm chooses its $p$ pairs from the answers so far, and the $p$ answers lead to at most $2^p$ children. So after $r$ rounds the tree has at most $2^{pr}$ leaves. As in the [comparison sorting lower bound](/comparison-sort-lower-bound/), two orders of the keys that reach the same leaf get the same output permutation, so at most one of them is sorted correctly. So the $n!$ orders need $n!$ leaves, $2^{pr} \ge n!$, and $r \ge \lg n! / p$. Because $\lg n! \ge n \lg n - n \lg e$, for $p \le c n$ this gives $r \ge (\lg n - \lg e)/c = \Omega(\log n)$. $\square$

**(c).** A comparator network of depth $t$ is an algorithm of the parallel comparison model: each layer has at most $\lfloor n/2 \rfloor$ comparators on disjoint wires, so it is one round with $p = \lfloor n/2 \rfloor$, and the pairs do not depend on the answers. So by (b), $t \ge \lg n! / \lfloor n/2 \rfloor \ge 2 \lg n - 2 \lg e$. $\square$

**(d).** Cook, Dwork and Reischuk proved that a CREW PRAM with any number of processors and unbounded local computation, with $n$ input bits in cells $0, \ldots, n-1$, needs at least $\log_b n$ steps to write the OR of the bits into a cell. Their proof counts how many inputs can affect the state of one processor or one cell after $t$ steps, and shows that this number grows by at most a factor $b$ per step. We do not repeat it. Now take a CREW PRAM algorithm that sorts $n$ keys in $T(n)$ steps, and give it inputs in $\{0, 1\}$. Its last output cell $n - 1$ then holds the maximum of the bits, which is their OR. So $T(n) \ge \log_b n$. The EREW PRAM is a special case of the CREW PRAM, so the bound holds there too. $\square$

**(e).** Beame and Håstad proved that a CRCW PRAM with a number of processors polynomial in $n$ needs $\Omega(\log n / \log \log n)$ time to compute the parity of $n$ bits. Take a CRCW PRAM sorting algorithm with polynomially many processors and time $T(n)$, and give it $n$ bits. After the sort, the bits are $0^{n-c} 1^c$, where $c$ is the number of ones. Add $n$ processors. In the first step, processor $i$ reads $y_i$, and processor $0$ also writes $0$ into the output cell. In the second step, processor $i$ reads $y_{i-1}$ for $i \ge 1$. In the third step, the one processor $i$ with $y_i = 1$ and either $i = 0$ or $y_{i-1} = 0$ writes $(n - i) \bmod 2$ into the output cell. If $c = 0$ no processor writes, and the cell keeps $0$. So the parity is computed in $T(n) + 3$ steps, and $T(n) = \Omega(\log n / \log \log n)$. $\square$

## Consequences

- **Optimal parallel sorts.** On the EREW and CREW PRAM, an algorithm that sorts $n$ keys in $O(\log n)$ time with $n$ processors is optimal in both time and work, since it does $O(n \log n)$ work, which is the [comparison sorting lower bound](/comparison-sort-lower-bound/). [Cole's merge sort](/cole-merge-sort/) is such an algorithm.
- **Merge sort with a slow merge is not optimal.** [Parallel merge sort](/parallel-merge-sort/) with a merge of span $\Theta(\log^2 n)$ has span $\Theta(\log^3 n)$, far above $\Omega(\log n)$.
- **Merging is easier than sorting.** Merging two sorted lists of length $n$ takes $\Theta(\log \log n)$ rounds in the parallel comparison model with $n$ processors, as [Valiant's merge](/valiant-parallel-merge/) shows. Part (a) does not apply to merging in that model, because a round there is not a gate of fan-in 2. For merging circuits, the same argument as in (a) gives depth at least $\lceil \lg 2n \rceil$.
- **Depth of networks.** Batcher's [bitonic sort](/bitonic-sort/) and [odd-even merge sort](/odd-even-merge-sort/) have depth $\frac{1}{2} \lg n (\lg n + 1)$ for $n$ a power of 2, which is $\Theta(\log n)$ times the bound in (c). See [network depth](/network-depth/).

Numbers for (b) and (c), with $p = n$ for (b), and Batcher's depth for $n = 2^k$:

| $n$ | $\lceil \lg n! \rceil$ | (b), rounds with $p = n$ | (c), network depth | Batcher's depth $k(k+1)/2$ |
| --- | --- | --- | --- | --- |
| 4 | 5 | 2 | 3 | 3 |
| 8 | 16 | 2 | 4 | 6 |
| 16 | 45 | 3 | 6 | 10 |
| 32 | 118 | 4 | 8 | 15 |
| 1024 | 8770 | 9 | 18 | 55 |
| $2^{20}$ | 19458756 | 19 | 38 | 210 |

## Tightness

- **Sorting networks.** The [AKS network](/aks-sorting-network/) has depth $O(\log n)$, so (a) and (c) are tight up to a constant factor. Its constant is very large, and the networks in use have depth $\Theta(\log^2 n)$.
- **Parallel comparison model.** The AKS network sorts in $O(\log n)$ rounds with $\lfloor n/2 \rfloor$ processors, so (b) is tight up to a constant factor for $p = \Theta(n)$. With $p = \binom{n}{2}$ processors, one round compares every pair and the order follows, so the bound $\lg n! / p$ is far from tight for large $p$.
- **CREW and EREW PRAM.** Cole's merge sort runs in $O(\log n)$ time with $n$ processors on both, so (d) is tight up to a constant factor.
- **CRCW PRAM.** Rajasekaran and Reif gave a randomized sort for the CRCW PRAM that runs in sublogarithmic time. So the CRCW PRAM does not have an $\Omega(\log n)$ bound for sorting, and the gap between (d) and (e) is real.

## History

Valiant defined the parallel comparison model in 1975 and studied merging, sorting and finding the maximum in it. The bound of (b) is the counting argument of the sequential sorting bound applied to rounds. Ajtai, Komlós and Szemerédi showed in 1983 that sorting networks of depth $O(\log n)$ exist, which settled the order of the depth. Cook, Dwork and Reischuk proved the bound for the CREW PRAM in 1986, and Cole gave a matching PRAM sort in 1988. Beame and Håstad proved the bound for parity on the CRCW PRAM in 1989.

## References
