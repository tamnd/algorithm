---
tag: T4QQ2K
kind: definition
slug: tfnp
name: TFNP
aliases:
- total function NP
area: complexity/complexity-classes
level: advanced
summary: "Search problems in FNP where every instance has a solution. No such problem is FNP-complete unless NP = coNP. Subclasses such as PLS and PPAD group the problems by the reason a solution exists."
prereqs: [fnp, search-problem]
see_also: [fnp, fp, pls, ppad, co-np, local-search-problem, nash-equilibrium-computation, integer-factorization]
sources:
  - paper: doi:10.1016/0304-3975(91)90200-L
    title: Nimrod Megiddo and Christos H. Papadimitriou, On total functions, existence theorems and computational complexity, Theoretical Computer Science 81(2) (1991)
    locator: pp. 317 to 324 (the class TFNP, the list of total problems, and the result that TFNP has an FNP-complete problem if and only if NP = coNP)
  - paper: doi:10.1016/S0022-0000(05)80063-7
    title: Christos H. Papadimitriou, On the complexity of the parity argument and other inefficient proofs of existence, Journal of Computer and System Sciences 48(3) (1994)
    locator: pp. 498 to 532 (the subclasses PPAD, PPA and PPP and their inclusions)
  - paper: doi:10.1016/0022-0000(88)90046-3
    title: David S. Johnson, Christos H. Papadimitriou and Mihalis Yannakakis, How easy is local search?, Journal of Computer and System Sciences 37(1) (1988)
    locator: pp. 79 to 100 (the subclass PLS)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Section 10.3, Function problems (FNP and total functions)
---

TFNP (total function NP) is the class of [FNP](/fnp/) search problems in which every instance has a solution. The answer "no" never occurs, so the decision version of each problem is trivial, and the only question is how fast a solution can be found. Megiddo and Papadimitriou (1991) named the class. Their examples include factoring, local optima, Brouwer fixed points, Sperner's lemma and equilibria of two-player games. In each case a mathematical theorem says that a solution exists, but its proof does not give a fast way to find one.

## Definition

Fix the alphabet $\{0, 1\}$. Machines are deterministic [multitape Turing machines](/multitape-turing-machine/).

A binary relation $R$ is in TFNP if:

1. $R$ is *polynomially balanced*: there is a polynomial $p$ with $|y| \le p(|x|)$ whenever $(x, y) \in R$;
2. $R$ is *decidable in polynomial time*: a deterministic machine decides whether $(x, y) \in R$ in time polynomial in $|x| + |y|$;
3. $R$ is *total*: for every $x$ there is a $y$ with $(x, y) \in R$.

The search problem of $R$ is: given $x$, output some $y$ with $(x, y) \in R$. The first two conditions say that $R$ is in FNP. The third is a promise about all inputs, not a condition that a machine can check. For this reason TFNP is called a *semantic* class, and no complete problem for TFNP is known. Its well-studied subclasses are *syntactic*: each one is defined by a complete problem whose totality follows from a simple counting principle, and every problem that reduces to it is then total for the same reason.

Reductions are the ones of FNP: a pair of maps $(f, g)$ in [FP](/fp/), where $f$ maps an instance $x$ to an instance $f(x)$, and $g(x, z)$ maps each solution $z$ of $f(x)$ to a solution of $x$.

**Theorem (Megiddo and Papadimitriou, 1991).** TFNP contains an FNP-complete problem if and only if $\mathsf{NP} = \mathsf{coNP}$.

*Proof.* Suppose that $R \in \mathsf{TFNP}$ is FNP-complete. Then FSAT reduces to $R$ by some pair $(f, g)$, where $g$ may output "no" and "no" is the correct answer for an unsatisfiable formula. Let $\varphi$ be unsatisfiable. Since $R$ is total, $f(\varphi)$ has a solution $z$, and $g(\varphi, z)$ must be a correct answer for $\varphi$, so it is "no". If $\varphi$ is satisfiable, every solution $z$ of $f(\varphi)$ gives a satisfying assignment $g(\varphi, z)$, never "no". So $\varphi$ is unsatisfiable exactly when some $z$ has $(f(\varphi), z) \in R$ and $g(\varphi, z) = \text{no}$. The string $z$ has length polynomial in $|\varphi|$, and the check runs in polynomial time. So the unsatisfiable formulas form a language in NP. This language is coNP-complete, so $\mathsf{coNP} \subseteq \mathsf{NP}$, and then $\mathsf{NP} = \mathsf{coNP}$.

Conversely, suppose that $\mathsf{NP} = \mathsf{coNP}$. Then unsatisfiability has a polynomial-time verifier $V$ with certificates of polynomial length. Let $R$ hold between $\varphi$ and $y$ when $y = (1, a)$ with $a$ a satisfying assignment, or $y = (0, c)$ with $V(\varphi, c) = 1$. Every formula is satisfiable or not, so $R$ is total, and $R$ is in FNP. FSAT reduces to $R$ with $f$ the identity and $g$ that returns $a$ from $(1, a)$ and "no" from $(0, c)$. $\square$

The same argument works for a polynomial-time Turing reduction from SAT to a TFNP problem, as long as the reduction is correct for every valid choice of answers to its queries: a nondeterministic machine guesses the answers and checks them. So "TFNP problems are NP-hard" would give $\mathsf{NP} = \mathsf{coNP}$. This is the evidence that problems in TFNP are easier than NP-complete problems. It is not a proof that they are easy.

## Examples and non-examples

**Pigeonhole.** The problem PIGEON is: given a Boolean circuit $C$ with $n$ inputs and $n$ outputs, find an $x$ with $C(x) = 0^n$, or two strings $x \ne y$ with $C(x) = C(y)$. A solution always exists by the [pigeonhole principle](/pigeonhole-principle/): if no input maps to $0^n$, then $2^n$ inputs map into $2^n - 1$ values. Take $n = 3$ and read the strings as numbers $0$ to $7$, with $C(x) = x^2 + x \bmod 8$. The values for $x = 0, \ldots, 7$ are $0, 2, 6, 4, 4, 6, 2, 0$. The solutions are $x = 0$ and $x = 7$, which map to 0, and the four pairs $\{0, 7\}$, $\{1, 6\}$, $\{2, 5\}$ and $\{3, 4\}$. A circuit with a large $n$ has $2^n$ inputs, so listing the values does not run in polynomial time. PIGEON is complete for the subclass PPP (Papadimitriou 1994).

**Other total problems.**

- *Factoring.* Every $N \ge 2$ has a prime factorization, and a claimed one is checked by multiplication and the [AKS test](/aks-primality-test/). See [integer factorization](/integer-factorization/).
- *Local optima.* Every instance of a [local search problem](/local-search-problem/) on a finite set has a local optimum. These problems form [PLS](/pls/).
- *Nash equilibria.* Every finite game has a mixed equilibrium by [Nash's theorem](/nash-existence-theorem/). A two-player game with rational payoffs has an equilibrium with rational coordinates of polynomial size, so the problem is in TFNP, and it is complete for [PPAD](/ppad/) (see [Nash equilibrium computation](/nash-equilibrium-computation/)).
- *Problems from NP and coNP.* Let $L \in \mathsf{NP} \cap \mathsf{coNP}$, with a verifier relation $R_1$ for $L$ and $R_0$ for its complement. The relation that holds between $x$ and $(b, y)$ when $(x, y) \in R_b$ is total and in FNP, and a solution tells whether $x \in L$. So if every TFNP problem were in FP, then $\mathsf{NP} \cap \mathsf{coNP} = \mathsf{P}$.

**Non-examples.**

- *FSAT.* An unsatisfiable formula has no assignment, so FSAT is not total. Adding the answer "no" does not help, because "no" cannot be checked in polynomial time unless $\mathsf{NP} = \mathsf{coNP}$.
- *Total but not known to be in FNP.* "Given $\varphi$, output the number of satisfying assignments" always has an answer, but no polynomial-time check of a claimed count is known.

**A common mistake.** Totality is a fact about the problem, not about one instance. A relation for which the given instance happens to have a solution is not in TFNP for that reason. Totality must hold for every input, and it often holds only because the problem is written in a careful form, as PIGEON allows the answer $C(x) = 0^n$.

## Related definitions

- **[FNP](/fnp/)** is the class of search problems with a balanced relation decidable in polynomial time. TFNP is its total part.
- **[FP](/fp/)**: the total problems that a polynomial-time algorithm solves are in TFNP, and they are contained in each subclass below.
- **[PLS](/pls/)** (polynomial local search, Johnson, Papadimitriou and Yannakakis 1988): totality because every finite set with a cost has a local optimum.
- **[PPAD](/ppad/)** (polynomial parity argument, directed, Papadimitriou 1994): totality because a directed graph of in-degree and out-degree at most 1 with a known source has another end of a line.
- **PPA** and **PPP** (Papadimitriou 1994): the undirected parity argument and the pigeonhole principle. Papadimitriou showed $\mathsf{PPAD} \subseteq \mathsf{PPA}$ and $\mathsf{PPAD} \subseteq \mathsf{PPP}$.
- **CLS** (continuous local search): Fearnley, Goldberg, Hollender and Savani (2021) proved $\mathsf{CLS} = \mathsf{PPAD} \cap \mathsf{PLS}$.

## References
