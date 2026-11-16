---
tag: TPP97Z
kind: model
slug: query-model
name: Query model
aliases:
- oracle model
- decision tree query model
area: complexity/communication-and-query-complexity
level: intro
summary: "An algorithm reads its input x in {0,1}^n only by queries of single bits x_i. The cost is the number of queries, and all other work is free."
prereqs: [boolean-function, decision-tree-model]
see_also: [query-complexity, decision-tree-complexity, randomized-query-complexity, quantum-query-model, oracle-turing-machine, cell-probe-model, communication-model, adversary-argument]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 12, Decision trees (the query model, certificates, randomized trees and lower bounds)
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 2 (the deterministic, randomized and quantum query models), Section 5 (relations between the measures)
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (the quantum query model, the polynomial lower bound, the bounds for OR, PARITY and MAJORITY)
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (block sensitivity, certificates and the bound on randomized decision trees)
---

The query model is a model of computation in which an algorithm sees its input only through a black box. The input is a string $x \in \{0,1\}^n$, and the algorithm asks questions of the form "what is $x_i$?". Each question is one query and costs one unit; all other work, such as the choice of the next query and the final computation of the answer, is free. The model is the common base of [query complexity](/query-complexity/), the concept, and of measures such as [decision tree complexity](/decision-tree-complexity/), the deterministic measure. This page defines the machine; those pages define the numbers that are measured on it.

## The machine

The task is a Boolean function $f : \{0,1\}^n \to \{0,1\}$. On this page and on the other pages of this group, $f$ is **total** (defined on all $2^n$ inputs) unless the page says that it is **partial**. A partial function is defined only on a set $P \subseteq \{0,1\}^n$, the promise, and the algorithm can do anything on inputs outside $P$. Some sources allow an alphabet larger than $\{0,1\}$; the definitions below carry over with no change.

The input $x$ is not given to the algorithm. The algorithm has access to an oracle that holds $x$. A **query** sends an index $i \in \{1, \ldots, n\}$ to the oracle, and the oracle returns the bit $x_i$. The algorithm can choose each index from the answers it already has, so the queries are **adaptive**. At the end the algorithm outputs one bit.

There are four common kinds of query algorithm. They differ in what the algorithm can do between queries and in what counts as a correct answer.

- **Deterministic.** The algorithm is a fixed rule that maps the answers so far to the next index or to the output. Such a rule is a binary [decision tree](/decision-tree-model/): each inner node holds an index $i$, the two edges below it are the answers $x_i = 0$ and $x_i = 1$, and each leaf holds an output bit. The algorithm must output $f(x)$ on every input.
- **Randomized.** The algorithm also flips coins. Equivalently, it is a probability distribution over deterministic trees. With bounded two-sided error, it must output $f(x)$ with probability at least $2/3$ on every input $x$. With zero error, it must always be correct, and the cost is the expected number of queries. See [randomized query complexity](/randomized-query-complexity/).
- **Quantum.** The oracle is a unitary map $O_x$ with $O_x \lvert i, b \rangle = \lvert i, b \oplus x_i \rangle$, and the algorithm applies any unitary maps between two queries. A query can act on a superposition of indices. See the [quantum query model](/quantum-query-model/) and [quantum oracle](/quantum-oracle/).
- **Nondeterministic.** A prover points to a set of positions, and the verifier reads only those. The verifier must accept exactly the inputs with $f(x) = 1$, whatever the prover shows. The least number of positions is the [certificate complexity](/certificate-complexity/).

A **non-adaptive** algorithm chooses all its indices before it sees any answer. It is a weaker variant. For example, a non-adaptive deterministic algorithm for OR must read all $n$ bits on every input, while an adaptive one can stop at the first 1.

The model is **non-uniform**. An algorithm is one tree for one input length $n$, and a family of trees, one for each $n$, handles all lengths. No condition says that the trees can be computed efficiently.

## What it counts

The cost of an algorithm on an input $x$ is the number of queries that it makes on $x$. The cost of the algorithm is the largest cost over all inputs $x$ (for a zero-error randomized algorithm, the largest expected cost). The **query complexity** of $f$ in a model is the least cost of an algorithm in that model that computes $f$. The standard names are:

| measure | model | correctness |
|---|---|---|
| $D^{dt}(f)$ | deterministic | always correct |
| $R_0(f)$ | randomized, expected queries | always correct |
| $R(f)$ | randomized | correct with probability at least $2/3$ |
| $Q_E(f)$ | quantum | correct with probability 1 |
| $Q(f)$ | quantum | correct with probability at least $2/3$ |
| $C(f)$ | nondeterministic | the verifier is always correct |

The superscript in $D^{dt}$ keeps the deterministic query measure apart from the communication measure $D^{cc}$ on the [deterministic communication complexity](/deterministic-communication-complexity/) page. The constant $2/3$ is not special. Any constant above $1/2$ gives the same measure up to a constant factor, because the algorithm can run $k$ times and output the majority answer, and the error then falls exponentially in $k$.

Each measure is at most $n$, because an algorithm that reads all bits knows $x$ and then knows $f(x)$. A lower bound in the model is therefore a statement about information: it says how many bits of $x$ an algorithm must see. It does not say anything about running time. In the other direction, an upper bound can hide a large amount of free computation between the queries.

A small worked example: majority of three bits, $\mathrm{MAJ}_3(x) = 1$ when at least two of $x_1, x_2, x_3$ are 1. A deterministic algorithm reads $x_1$ and $x_2$. If they are equal, it outputs that value. If they differ, it reads $x_3$ and outputs $x_3$. The worst case is 3 queries. No algorithm does better: an adversary answers the first query with 0 and the second query with 1. After two queries, both answers of the third bit are still possible, and they give different values of $\mathrm{MAJ}_3$. So $D^{dt}(\mathrm{MAJ}_3) = 3$. The same kind of [adversary argument](/adversary-argument/) gives $D^{dt} = n$ for OR, AND, PARITY and MAJORITY on $n$ bits.

## Relation to other models

The deterministic query model is the [decision tree model](/decision-tree-model/) with one fixed set of queries: the $n$ queries "what is $x_i$?". The [comparison model](/comparison-model/) is the same tree model with comparisons "$a_i < a_j$?" as the queries. The [algebraic decision tree](/algebraic-decision-tree/) and [linear decision tree](/linear-decision-tree/) models allow stronger queries. A lower bound in the query model with bit queries does not carry over to those models, because a single strong query can combine many bits.

An [oracle Turing machine](/oracle-turing-machine/) also asks an oracle questions at unit cost, but it pays for its other steps too, and the oracle is a set of strings of all lengths. Query lower bounds are the main tool for oracle results. For example, a machine that runs in polynomial time can query only polynomially many of the $2^n$ strings of length $n$. To decide whether the oracle holds some string of length $n$ is the OR of $2^n$ bits, and it needs $2^n$ queries deterministically. This is the core of the [Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/) and of other [relativization](/relativization/) results.

In the [cell-probe model](/cell-probe-model/) and the [bit-probe model](/bit-probe-model/), the algorithm also pays only for reads of memory cells. The difference is that a data structure first stores the input in a table of its own choice, and the cost counts probes into that table. The query model has no preprocessing: the input is fixed and given bit by bit.

In the [communication model](/communication-model/), two players each hold a part of the input. A query algorithm for $f$ gives a protocol for the function $F(x, y) = f(x_1 \wedge y_1, \ldots, x_n \wedge y_n)$: for each query $i$, Alice sends $x_i$ and Bob sends $y_i$. This protocol uses $2 D^{dt}(f)$ bits. The reverse direction is much harder and needs special gadgets.

The [quantum query model](/quantum-query-model/) gives the largest known gaps with the classical models. For total functions, the gaps are at most polynomial (see below). For partial functions they can be exponential; [Simon's algorithm](/simon-algorithm/) is the standard example.

## Known results in the model

For the four basic symmetric functions on $n$ bits, the measures are known up to constant factors.

| function | $D^{dt}$ | $R$ | $Q$ |
|---|---|---|---|
| OR (and AND) | $n$ | $\Theta(n)$ | $\Theta(\sqrt{n})$ |
| PARITY | $n$ | $n$ | $\lceil n/2 \rceil$ |
| MAJORITY | $n$ | $\Theta(n)$ | $\Theta(n)$ |

The upper bound $Q(\mathrm{OR}) = O(\sqrt n)$ comes from [Grover search](/grover-search/), and the matching lower bound is [Grover optimality](/grover-optimality/). The quantum values for PARITY and MAJORITY come from the [polynomial method](/polynomial-method/) (Beals, Buhrman, Cleve, Mosca and de Wolf 2001). See the [parity problem](/parity-problem/) and the [majority problem](/majority-problem/) pages for the proofs.

For total functions, every pair of the measures in the table of the previous section is polynomially related. Some of the main bounds are:

- $D^{dt}(f) \le C_0(f) \, C_1(f)$, where $C_0$ and $C_1$ are the certificate sizes for 0-inputs and 1-inputs (see [decision tree complexity](/decision-tree-complexity/)).
- $D^{dt}(f) \le 27 \, R(f)^3$ (Nisan 1991; see [randomized query complexity](/randomized-query-complexity/)).
- $D^{dt}(f) = O(Q(f)^6)$ (Beals et al. 2001), improved to $O(Q(f)^4)$ by Aaronson, Ben-David, Kothari, Rao and Tal in 2021.
- $\mathrm{bs}(f) \le \mathrm{s}(f)^4$ (Huang 2019; see the [sensitivity theorem](/sensitivity-theorem/)).

None of these relations holds for partial functions in general. The promise can remove all the hard inputs, and this is why the quantum speedups for promise problems can be exponential.

## References
