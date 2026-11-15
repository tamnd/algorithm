---
tag: 48RQSB
kind: concept
slug: decision-problem
name: Decision problem
aliases:
- decision version
- yes-no problem
area: complexity/np-completeness
level: intro
summary: A problem whose answer is yes or no, written as a language of bit strings under a fixed encoding; P, NP and NP-completeness are defined for such problems.
prereqs: [input-size, turing-machine, polynomial-time]
see_also: [polynomial-time-reduction, search-problem, optimization-to-decision-reduction, unary-encoding, pseudo-polynomial-time, decidable-language, np, certificate]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 2.1 (decision problems, languages and encoding schemes) and Section 4.2 (number problems)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.1 (abstract problems, encodings and the formal-language framework)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.1 (measuring complexity) and Section 7.2 (the class P and reasonable encodings)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 0 (representing objects as strings, decision problems as languages)
---

A decision problem is a problem whose answer is yes or no for every input, for example "does this graph have a clique of $k$ vertices?". To study its complexity, each input is written as a bit string under a fixed encoding, and the problem becomes a language: the set $L \subseteq \{0,1\}^*$ of strings that encode yes-instances. The classes [P](/p/), [NP](/np/) and [coNP](/co-np/) and the notions [NP-hard](/np-hard/) and [NP-complete](/np-complete/) are all defined for decision problems. The choice of encoding does not change these classes as long as it is reasonable, and in particular as long as numbers are written in binary.

## In plain words

A decision problem asks a question with a yes or no answer, such as "is this number prime?" or "can these cities be visited on a route of length at most 500?". Every input is first written as a string of bits. The problem is then the set of strings for which the answer is yes, and an algorithm solves it if it says yes on exactly those strings. Problems that ask for a best value, such as the shortest route, have a yes or no version that adds a bound to the question. The way that numbers are written matters. A number written in binary is short, but the same number written as a row of ones is very long. An algorithm can be slow for the short form and fast for the long form, because its speed is measured against the length of the input.

## The idea

**Instances, encodings and languages.** A decision problem $\Pi$ has a set $D_\Pi$ of instances and a subset $Y_\Pi \subseteq D_\Pi$ of yes-instances. Garey and Johnson write it in two lines, an Instance line that describes $D_\Pi$ and a Question line that describes $Y_\Pi$:

- Instance: a graph $G = (V, E)$ and a positive integer $k \le |V|$.
- Question: does $G$ contain a clique of size $k$ or more?

An encoding $e$ maps each instance to a string over a fixed alphabet, usually $\{0,1\}$. The language of $\Pi$ under $e$ is
$$L[\Pi, e] = \{\, e(I) : I \in Y_\Pi \,\}.$$
Strings that encode no instance are not in the language. For the usual encodings, a [multitape Turing machine](/multitape-turing-machine/) can check in [polynomial time](/polynomial-time/) whether a string encodes an instance, so this choice does not change any class at or above P.

**Deciding a language.** A deterministic [Turing machine](/turing-machine/) decides $L$ if it halts on every input and accepts exactly the strings in $L$. The complexity classes of this area are defined on the multitape Turing machine; the classes P, NP and EXP do not change under the polynomial-time simulations of the [multitape simulation theorem](/multitape-simulation-theorem/) and of [RAM to Turing machine simulation](/ram-turing-equivalence/), but exact exponents do change. A language that some machine decides, in any amount of time, is a [decidable language](/decidable-language/). The [halting problem](/halting-problem/) is a decision problem that no machine decides.

**Reasonable encodings.** Garey and Johnson (Section 2.1) call an encoding reasonable when it is concise (no padding beyond what the instance needs) and decodable, and when numbers are written in base 2 or any other fixed base of at least 2. Any two reasonable encodings of the same problem have lengths within a polynomial of each other, and each can be converted to the other in polynomial time. Thus "$\Pi$ is in P" means the same thing for every reasonable encoding. A graph with $n$ vertices and $m$ edges, for example, takes $n^2$ bits as an [adjacency matrix](/adjacency-matrix/) and $O((n + m)\log n)$ bits as an [adjacency list](/adjacency-list/). Since $m \le n^2$, each length is at most a polynomial in the other.

**Why the encoding of numbers matters.** The [input size](/input-size/) of a number $N$ in binary is $\lceil \log_2(N+1) \rceil$ bits. In [unary encoding](/unary-encoding/) it is $N$ symbols, which is exponentially longer. An algorithm whose time is polynomial in the value $N$ is polynomial in the unary length but can be exponential in the binary length. Such an algorithm is [pseudo-polynomial](/pseudo-polynomial-time/). A problem that stays NP-hard when its numbers are written in unary is [strongly NP-hard](/strong-np-hardness/). The encoding is part of the problem, so a page that states a complexity result for a number problem must say which encoding it uses; this encyclopedia uses binary unless a page says otherwise.

**Decision, search and optimization.** A [search problem](/search-problem/) asks for a solution, not only for a yes or no. An optimization problem asks for a solution of least cost or greatest value. Its decision version adds a bound $k$ to the instance and asks whether a solution of value at least $k$ (or at most $k$) exists. The decision version is never harder than the optimization version: an optimal value answers every bound. In the other direction, binary search over $k$ finds the optimal value with $\lceil \log_2(U + 1) \rceil$ calls to the decision version when the value is an integer in $\{0, \ldots, U\}$ (see [optimization to decision reduction](/optimization-to-decision-reduction/)). For many NP problems, a [search to decision reduction](/search-to-decision-reduction/) also finds a solution with polynomially many calls, by [self-reducibility](/self-reducibility/). This is why complexity theory can study decision problems only and still say something about search and optimization.

**Complement.** The complement of $\Pi$ has the same instances and swaps the answers: its yes-instances are $D_\Pi \setminus Y_\Pi$. The complement of a class C, written coC, holds the complements of the problems in C. For NP this gives [coNP](/co-np/).

## Examples

**Primality and the binary encoding.** Take the problem PRIMES. Instance: a positive integer $N$ in binary. Question: is $N$ prime? Trial division tries every divisor from 2 to $\lfloor \sqrt N \rfloor$. A script counted the divisors to try and the binary length:

| $N$ | bits in binary | divisors tried by trial division |
|---|---|---|
| 97 | 7 | 8 |
| 1000003 | 20 | 999 |
| $2^{61} - 1$ | 61 | 1518500248 |

The number of divisors grows like $2^{b/2}$ in the bit length $b$, so [trial division](/trial-division/) is exponential in the input size, although it is polynomial in the value $N$. If $N$ were written in unary, the input would have length $N$ and trial division would be a polynomial-time algorithm for that encoding. With the binary encoding, PRIMES is in P by the [AKS primality test](/aks-primality-test/) (Agrawal, Kayal and Saxena 2004), which runs in time polynomial in $b$.

**Optimization to decision by binary search.** Take the graph on vertices $0, \ldots, 5$ with edges $01, 02, 12, 23, 34, 45, 35, 13$. The optimization question asks for the size of a [maximum clique](/maximum-clique/). The decision version, the [clique problem](/clique-problem/), takes $(G, k)$ and asks whether a clique of size $k$ exists. Binary search over $k \in \{0, \ldots, 6\}$ asked the decision version for $k = 3$ (yes), $k = 5$ (no) and $k = 4$ (no), and returned 3 after $3 = \lceil \log_2 7 \rceil$ calls. The cliques $\{0, 1, 2\}$, $\{1, 2, 3\}$ and $\{3, 4, 5\}$ have size 3.

**Non-examples.** "Find a shortest path from $s$ to $t$" is a search problem, not a decision problem; its decision version is "is there an $s$ to $t$ path of length at most $k$?". "How many satisfying assignments does this formula have?" is a counting problem; see [model counting](/model-counting/). Each of these has a decision problem that is polynomial-time equivalent to it or that it solves, but they are different objects.

**A decision problem that no machine decides.** HALT $= \{\langle M, w\rangle : M \text{ halts on } w\}$ is a well-defined language, so it is a decision problem. No Turing machine decides it ([halting problem](/halting-problem/)). Being a decision problem says nothing about being solvable.

## Where it is used

- Complexity classes. [P](/p/), [NP](/np/), [coNP](/co-np/), [PSPACE](/pspace/) and [EXPTIME](/exptime/) are classes of languages, so they contain decision problems only. [FNP](/fnp/) and [FP](/fp/) are the classes of search and function problems that go with them.
- Reductions. A [polynomial-time reduction](/polynomial-time-reduction/) (Karp reduction) maps instances of one decision problem to instances of another and keeps the answer. NP-hardness and NP-completeness are defined with it.
- Catalogues. The [Garey and Johnson compendium](/garey-johnson-compendium/) and [Karp's 21 problems](/karps-21-np-complete-problems/) state each problem in decision form.
- Certificates. A [certificate](/certificate/) proves that an instance is a yes-instance; a [polynomial-time verifier](/polynomial-time-verifier/) checks it. Both need a yes or no question.
- Practice. A [SAT](/sat/) solver answers a decision problem and, when the answer is yes, also returns a satisfying assignment, which is a certificate for that answer.

## References
