---
tag: WA43N8
kind: definition
slug: pp
name: PP
aliases:
- probabilistic polynomial time (unbounded error)
area: complexity/complexity-classes
level: advanced
summary: The decision problems where a polynomial-time probabilistic machine accepts with probability above 1/2 exactly on the yes-instances. The gap can be exponentially small.
prereqs: [probabilistic-turing-machine, bpp, np, polynomial-time-reduction]
see_also: [bpp, bqp, toda-theorem, model-counting, permanent-computation, counting-problem, pspace, polynomial-hierarchy]
sources:
  - paper: doi:10.1137/0206049
    title: John Gill, Computational complexity of probabilistic Turing machines, SIAM Journal on Computing 6(4), 675 to 695 (1977)
    locator: the definition of PP and the bounds NP in PP and PP in PSPACE
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 189 to 201 (1979)
    locator: the class #P and the #P-completeness of the permanent
  - paper: doi:10.1137/0220053
    title: Seinosuke Toda, PP is as hard as the polynomial-time hierarchy, SIAM Journal on Computing 20(5), 865 to 877 (1991)
    locator: the main theorem (PH in P^PP)
  - paper: doi:10.1006/jcss.1995.1017
    title: Richard Beigel, Nick Reingold and Daniel Spielman, PP is closed under intersection, Journal of Computer and System Sciences 50(2), 191 to 202 (1995)
    locator: the main theorem
  - paper: doi:10.1137/S0097539795293639
    title: Leonard M. Adleman, Jonathan DeMarrais and Ming-Deh A. Huang, Quantum computability, SIAM Journal on Computing 26(5), 1524 to 1540 (1997)
    locator: the inclusion of BQP in PP
  - paper: doi:10.1098/rspa.2005.1546
    title: Scott Aaronson, Quantum computing, postselection, and probabilistic polynomial-time, Proceedings of the Royal Society A 461(2063), 3473 to 3482 (2005)
    locator: the theorem PostBQP = PP and the new proof that PP is closed under intersection
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 17, Complexity of counting (the classes #P and PP)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 11, Randomized computation, and Chapter 18, Computation that counts
---

PP (probabilistic polynomial time) is the class of decision problems for which a polynomial-time [probabilistic Turing machine](/probabilistic-turing-machine/) accepts with probability greater than $1/2$ on every yes-instance and at most $1/2$ on every no-instance. Unlike [BPP](/bpp/), PP asks for no gap between the two cases, so a difference of one coin sequence out of $2^{p(n)}$ is enough. For this reason repetition does not reduce the error, and PP is a counting class rather than a class of practical algorithms. PP contains [NP](/np/) and [BQP](/bqp/), is contained in [PSPACE](/pspace/), and by [Toda's theorem](/toda-theorem/) a polynomial-time machine with a PP oracle decides every problem in the [polynomial hierarchy](/polynomial-hierarchy/).

## Definition

**Model.** A deterministic [multitape Turing machine](/multitape-turing-machine/) $M$ reads an input $x$ and a string $r$ of $p(|x|)$ coin flips, and runs in time polynomial in $|x|$ for every $r$. Here $p$ is a polynomial.

**Definition (Gill 1977).** A language $L$ is in $\mathsf{PP}$ if there are such a machine $M$ and polynomial $p$ that, with $r$ uniform on $\{0,1\}^{p(|x|)}$, for every input $x$:

$$x \in L \iff \Pr_r[M(x, r) = 1] > 1/2.$$

In counting terms, let $\mathrm{acc}(x)$ be the number of strings $r$ with $M(x, r) = 1$. Then $x \in L$ if and only if $\mathrm{acc}(x) > 2^{p(|x|) - 1}$. The class does not change if "$> 1/2$" on yes-instances and "$\le 1/2$" on no-instances are replaced by "$\ge 1/2$" and "$< 1/2$", or by "$> 1/2$" and "$< 1/2$".

**Why amplification fails.** Suppose a single run is right with probability $1/2 + \gamma$. The Chernoff-Hoeffding bound gives error at most $e^{-2\gamma^2 k}$ for a majority of $k$ runs, and for a constant error the number of runs must grow like $1/\gamma^2$. In PP the gap $\gamma$ can be $2^{-p(n)}$, so about $4^{p(n)}$ runs are needed. For example, with $\gamma = 2^{-10}$, a majority of $1001$ runs still has error $0.475$, compared with $0.499$ for one run. This is the difference between PP and BPP: BPP is the subclass in which some machine has a gap of at least an inverse polynomial.

**Counting functions and #P.** The class #P (Valiant 1979) is the set of functions $f : \{0,1\}^* \to \mathbb{N}$ such that $f(x)$ is the number of accepting computation paths of some polynomial-time [nondeterministic Turing machine](/nondeterministic-turing-machine/) on $x$. Two examples are #SAT, the number of satisfying assignments of a Boolean formula ([model counting](/model-counting/)), and the [permanent](/permanent-computation/) of a 0-1 matrix, which counts the perfect matchings of a bipartite graph. Both are #P-complete: #SAT because the [Cook-Levin](/cook-levin-theorem/) reduction is [parsimonious](/parsimonious-reduction/), and the permanent by Valiant (1979). PP is the decision version of #P: "is $f(x) > 2^{p(|x|) - 1}$?" for an #P function $f$. See [counting problem](/counting-problem/).

## Examples and non-examples

**MAJSAT.** The language MAJSAT is the set of Boolean formulas $\varphi$ in $n$ variables with more than $2^{n-1}$ satisfying assignments. It is in PP: choose a random assignment and accept if it satisfies $\varphi$. For example, $x_1 \lor (x_2 \land x_3)$ has $5$ of $8$ satisfying assignments and is in MAJSAT. The formula $(x_1 \lor x_2) \land (\lnot x_1 \lor x_3)$ has the satisfying assignments $010$, $011$, $101$ and $111$, which is exactly half of $8$, so it is not in MAJSAT.

**MAJSAT is PP-complete.** Let $M$ be a PP machine with $p$ coins for $L$. The Cook-Levin construction gives, in polynomial time from $x$, a formula $\varphi(r, z)$ with $N = p + m$ variables whose satisfying assignments are in bijection with the accepting coin strings $r$; the variables $z$ record the computation and are determined by $r$. So $\#\varphi = \mathrm{acc}(x)$, and $x \in L$ if and only if $\#\varphi > 2^{p-1}$. To move the threshold to half of all assignments, add a variable $y$ and let

$$\psi = (\lnot y \land \varphi(r, z)) \lor (y \land (r_1 \lor z_1 \lor \cdots \lor z_m)).$$

The second part has $2^N - 2^{p-1}$ satisfying assignments: all of them except those with $r_1 = 0$ and $z = 0$. So $\#\psi = \#\varphi + 2^N - 2^{p-1}$, and $\psi$ has $N + 1$ variables. Then $\#\psi > 2^N$ if and only if $\#\varphi > 2^{p-1}$, so $x \mapsto \psi$ is a polynomial-time reduction from $L$ to MAJSAT.

**NP is in PP.** Let $N$ be a verifier for an NP language that uses $t$ coins (the certificate) and has $a(x)$ accepting strings. A PP machine flips one more coin $b$. If $b = 0$ it accepts. If $b = 1$ it runs $N$. It accepts on $2^t + a(x)$ of the $2^{t+1}$ coin strings, which is more than half if and only if $a(x) \ge 1$. With $t = 3$, the acceptance probabilities for $a = 0$, $1$ and $5$ are $8/16$, $9/16$ and $13/16$. Since PP is closed under complement (below), also $\mathsf{coNP} \subseteq \mathsf{PP}$. And $\mathsf{BPP} \subseteq \mathsf{PP}$ directly from the definitions, because $2/3 > 1/2 \ge 1/3$.

**Closure under complement.** Let $M$ have $p$ coins and $A$ accepting strings, and let $R = 2^p - A$. A new machine flips a coin $b$ and $p$ more coins $r$. If $b = 0$, it accepts if and only if $M(x, r)$ rejects. If $b = 1$, it accepts if and only if $r \le 2^{p-1}$ as a binary number. The number of accepting strings is $R + 2^{p-1} + 1$, which is more than $2^p$ if and only if $A \le 2^{p-1}$, that is, if and only if $x \notin L$. The extra $+1$ handles the case of a tie. So $\mathsf{PP} = \mathsf{coPP}$.

**Closure under union and intersection.** This is harder. Gill asked the question in 1977, and Beigel, Reingold and Spielman answered it in 1991 with rational functions that approximate the sign function: PP is closed under intersection and union. Aaronson (2005) gave a second proof with [quantum circuits](/quantum-circuit-model/): PP equals PostBQP, the class of quantum computations with postselection, and PostBQP is clearly closed under intersection.

**PP and #P as oracles.** $\mathsf{P}^{\mathsf{PP}} = \mathsf{P}^{\#\mathsf{P}}$. One direction: a PP oracle decides "$\#\varphi \ge k$?". The machine flips $b$ and an assignment $r$ of $n$ bits; if $b = 0$ it accepts if $\varphi(r)$ holds, and if $b = 1$ it accepts if $r < 2^n - k + 1$. It accepts on $\#\varphi + 2^n - k + 1$ strings out of $2^{n+1}$, which is more than half if and only if $\#\varphi \ge k$, for every $1 \le k \le 2^n + 1$. Binary search then finds $\#\varphi$ with $n + 1$ queries. The other direction is direct from the definition.

**Inclusions.**

- $\mathsf{NP} \cup \mathsf{coNP} \subseteq \mathsf{PP}$, $\mathsf{BPP} \subseteq \mathsf{PP}$, and $\mathsf{BQP} \subseteq \mathsf{PP}$ (Adleman, DeMarrais and Huang 1997; see [BQP](/bqp/)).
- $\mathsf{PP} \subseteq \mathsf{PSPACE}$: count the accepting strings one by one in polynomial space (Gill 1977).
- $\mathsf{PH} \subseteq \mathsf{P}^{\mathsf{PP}}$ ([Toda's theorem](/toda-theorem/)). So if $\mathsf{PP}$ were in $\Sigma_k^p$ for some $k$, then $\mathsf{PH} \subseteq \mathsf{P}^{\Sigma_k^p} \subseteq \Sigma_{k+1}^p$ and the polynomial hierarchy would collapse.
- Whether $\mathsf{PP} = \mathsf{PSPACE}$ is open, and so is whether $\mathsf{P} = \mathsf{PP}$.

**Non-examples.**

- *Problems with no efficient random test.* Membership in PP says nothing about practical speed. A PP machine for MAJSAT can have acceptance probability $1/2 + 2^{-n}$, and no polynomial number of runs tells this from $1/2$.
- *Search versions.* PP is a class of decision problems. Computing $\#\varphi$ exactly is a #P function. It is in $\mathsf{FP}^{\mathsf{PP}}$ by binary search, but it is not itself a PP language.
- *Undecidable problems.* $\mathsf{PP} \subseteq \mathsf{PSPACE}$, so every PP language is decidable.

## Related definitions

- [BPP](/bpp/): the subclass with a gap of at least an inverse polynomial.
- [NP](/np/): "at least one accepting path" in place of "more than half".
- #P: the counting functions behind PP, with complete problems [#SAT](/model-counting/) and the [permanent](/permanent-computation/).
- [Toda's theorem](/toda-theorem/): $\mathsf{PH} \subseteq \mathsf{P}^{\mathsf{PP}}$.
- [BQP](/bqp/) $\subseteq \mathsf{PP}$, and PostBQP $= \mathsf{PP}$.

## References
