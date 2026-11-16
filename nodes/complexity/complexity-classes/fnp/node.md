---
tag: GJXHRQ
kind: definition
slug: fnp
name: FNP
aliases:
- function NP
area: complexity/complexity-classes
level: advanced
summary: "Search problems for a polynomially balanced relation that is decidable in polynomial time: find a solution or say that none exists. FP = FNP if and only if P = NP."
prereqs: [fp, np, search-problem]
see_also: [fp, tfnp, np, search-problem, search-to-decision-reduction, self-reducibility, levin-reduction, certificate]
sources:
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Section 10.3, Function problems (FNP, reductions between function problems, FSAT, and FP = FNP if and only if P = NP)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press, 2008
    locator: Chapter 2, the classes PF and PC, and Section 2.2.3 on self-reducibility of search problems
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 2.5, Decision versus search
  - paper: doi:10.1016/0304-3975(91)90200-L
    title: Nimrod Megiddo and Christos H. Papadimitriou, On total functions, existence theorems and computational complexity, Theoretical Computer Science 81(2) (1991)
    locator: pp. 317 to 324 (FNP, the total subclass TFNP, and the relation to NP and coNP)
---

FNP (function NP) is the class of search problems that go with [NP](/np/). An NP language asks whether a short, easily checked solution exists. The FNP problem for the same relation asks for the solution itself, or for the answer "no" when there is none. Finding a satisfying assignment of a formula is the main example. FNP stands to NP as [FP](/fp/) stands to [P](/p/), and the two pairs are tied together: $\mathsf{FP} = \mathsf{FNP}$ if and only if $\mathsf{P} = \mathsf{NP}$.

## Definition

Fix the alphabet $\{0, 1\}$. Machines are deterministic [multitape Turing machines](/multitape-turing-machine/).

**Polynomially balanced relations.** A binary relation $R \subseteq \{0, 1\}^* \times \{0, 1\}^*$ is *polynomially balanced* if there is a polynomial $p$ such that $(x, y) \in R$ implies $|y| \le p(|x|)$. It is *polynomial-time decidable* if some deterministic machine decides, given $x$ and $y$, whether $(x, y) \in R$ in time polynomial in $|x| + |y|$.

**The class.** Each relation $R$ of both kinds defines a search problem: given $x$, output some $y$ with $(x, y) \in R$, or output "no" if there is no such $y$. FNP is the class of these search problems. Goldreich (Chapter 2) calls the class PC, for "polynomial check".

**The link with NP.** The relation $R$ defines the language $L_R = \{x : \exists y\ (x, y) \in R\}$, and $L_R \in \mathsf{NP}$, with $y$ as the [certificate](/certificate/). Conversely, every NP language is $L_R$ for some such $R$, namely the relation of its [polynomial-time verifier](/polynomial-time-verifier/). One language has many relations, so FNP is a class of relations, not of languages. Graph 3-coloring with "find a coloring" and with "find a coloring in which vertex 1 has color red" give two FNP problems for the same language.

**Reductions.** A search problem $R$ reduces to a search problem $R'$ if there are two maps $f$ and $g$ in FP such that: $f(x)$ is an instance of $R'$; if $z$ is a solution of $f(x)$, then $g(x, z)$ is a solution of $x$; and if $f(x)$ has no solution, then $x$ has none. A problem is FNP-complete if it is in FNP and every FNP problem reduces to it. FSAT, the problem "find a satisfying assignment of a CNF formula or say 'no'", is FNP-complete (Papadimitriou, Section 10.3). The proof is the [Cook-Levin](/cook-levin-theorem/) construction read as a [Levin reduction](/levin-reduction/), which carries witnesses in both directions.

**Theorem.** $\mathsf{FP} = \mathsf{FNP}$ if and only if $\mathsf{P} = \mathsf{NP}$. Here FP means the search problems that a deterministic polynomial-time algorithm solves.

*Proof.* Suppose that $\mathsf{FP} = \mathsf{FNP}$, and let $L \in \mathsf{NP}$ with verifier relation $R$, so $L = L_R$. The search problem of $R$ is in FNP, so some polynomial-time algorithm solves it. Run that algorithm on $x$ and accept when it outputs a string, not "no". This decides $L$ in polynomial time, so $L \in \mathsf{P}$.

Suppose that $\mathsf{P} = \mathsf{NP}$, and let $R$ be in FNP with balance polynomial $p$. Define the *prefix language*
$$\mathrm{Pre}_R = \{(x, u) : \text{there is } v \text{ with } |uv| \le p(|x|) \text{ and } (x, uv) \in R\}.$$
It is in NP, with $v$ as the certificate, so it is in P. The search algorithm on $x$ first tests $(x, \varepsilon) \in \mathrm{Pre}_R$, where $\varepsilon$ is the empty string. If the answer is no, it outputs "no". Otherwise it keeps a prefix $u$ with $(x, u) \in \mathrm{Pre}_R$. If $(x, u) \in R$, it outputs $u$. If not, every solution that extends $u$ is longer than $u$, so it extends $u0$ or $u1$, and the algorithm sets $u$ to the one of them that is in $\mathrm{Pre}_R$. The prefix grows by one bit in each round and never passes $p(|x|)$ bits, so there are at most $p(|x|) + 1$ rounds, each with at most three polynomial-time tests. $\square$

For FSAT the second half is shorter, because SAT is self-reducible: fix one variable at a time and ask the SAT decider whether the rest is still satisfiable. See [self-reducibility](/self-reducibility/) and [search-to-decision reduction](/search-to-decision-reduction/).

## Examples and non-examples

**A worked search.** Let $\varphi = (x_1 \lor x_2) \land (\lnot x_1 \lor x_3) \land (\lnot x_2 \lor \lnot x_3)$. Of the 8 assignments $(x_1, x_2, x_3)$, exactly two satisfy $\varphi$: $(0, 1, 0)$ and $(1, 0, 1)$. The self-reduction asks a SAT decider four questions:

1. Is $\varphi$ satisfiable? Yes.
2. Is $\varphi$ with $x_1 = 0$ satisfiable? Yes, so fix $x_1 = 0$.
3. Is it satisfiable with $x_1 = 0, x_2 = 0$? No, because the first clause fails. Fix $x_2 = 1$.
4. Is it satisfiable with $x_1 = 0, x_2 = 1, x_3 = 0$? Yes. Fix $x_3 = 0$.

The output is $(0, 1, 0)$, after $n + 1 = 4$ calls for $n = 3$ variables. A script that runs these calls with a brute-force decider gives the same answer and the same count.

**Examples in FNP.**

- *FSAT*, as above. It is FNP-complete.
- *Find a Hamiltonian cycle* in a graph, or a clique with $k$ vertices, or a 3-coloring. The solution is a list of vertices or colors, and the check is direct.
- *Factoring.* The relation holds between $N$ and a list of primes whose product is $N$. The list has at most $\log_2 N$ entries, and the check multiplies them and tests each for primality, which is in polynomial time by the [AKS test](/aks-primality-test/). Every $N \ge 2$ has a solution, so factoring lies in the total part [TFNP](/tfnp/).

**Non-examples.**

- *Relations that are not balanced.* "Given $\varphi$, list all its satisfying assignments" has outputs of up to $2^n$ assignments, so its relation is not polynomially balanced.
- *Relations that are not known to be decidable in polynomial time.* "Given a graph, find a maximum clique" has short answers, but checking that no larger clique exists is a coNP question. So the relation is not known to be decidable in polynomial time, and the problem is not known to be in FNP. It is solved in polynomial time with an NP oracle, by binary search on the size and then self-reduction, so it is in $\mathsf{FP}^{\mathsf{NP}}$.

**A common mistake.** An easy decision version does not make the search easy. The language of factoring is trivial, because every $N \ge 2$ has an answer, but no polynomial-time algorithm on a classical computer is known that finds the factors. The hardness of an FNP problem is a property of the relation, not of the language $L_R$.

## Related definitions

- **[FP](/fp/)** is the part of FNP that a polynomial-time algorithm solves.
- **[TFNP](/tfnp/)** is the part of FNP where every instance has a solution, so the answer "no" never occurs. Its subclasses [PLS](/pls/) and [PPAD](/ppad/) group total problems by the reason a solution exists.
- **[NP](/np/)** is the class of the languages $L_R$. A decision problem in NP and its search problem in FNP use the same [certificate](/certificate/).
- **[Search problem](/search-problem/)** gives the general definition, and **[Levin reduction](/levin-reduction/)** is the reduction type that maps witnesses both ways.
- **[Search-to-decision reduction](/search-to-decision-reduction/)** and **[self-reducibility](/self-reducibility/)** are the tools in the proof above.

## References
