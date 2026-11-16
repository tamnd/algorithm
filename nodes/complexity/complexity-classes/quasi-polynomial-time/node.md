---
tag: 2YZ77S
kind: definition
slug: quasi-polynomial-time
name: Quasi-polynomial time (QP)
aliases:
- quasipolynomial time
area: complexity/complexity-classes
level: advanced
summary: The problems solvable in time 2^((log n)^c) for some constant c, such as n^(log n). The class lies strictly between P and SUBEXP and contains graph isomorphism and parity games.
prereqs: [polynomial-time, time-hierarchy-theorem]
see_also: [subexponential-time, p, exptime, graph-isomorphism-problem, parity-game, fredman-khachiyan-algorithm, planted-clique, set-cover]
sources:
  - paper: doi:10.1145/2897518.2897542
    title: László Babai, Graph isomorphism in quasipolynomial time, 48th ACM Symposium on Theory of Computing, 684 to 697 (2016)
    locator: the main theorem
  - paper: doi:10.1145/3055399.3055409
    title: Cristian S. Calude, Sanjay Jain, Bakhadyr Khoussainov, Wei Li and Frank Stephan, Deciding parity games in quasipolynomial time, 49th ACM Symposium on Theory of Computing, 252 to 263 (2017)
    locator: the main theorem
  - paper: doi:10.1006/jcss.1996.0058
    title: Christos H. Papadimitriou and Mihalis Yannakakis, On limited nondeterminism and the complexity of the V-C dimension, Journal of Computer and System Sciences 53(2), 161 to 170 (1996)
    locator: the classes of problems with log-length witnesses, tournament dominating set and VC dimension
  - paper: doi:10.1145/174130.174138
    title: Nathan Linial, Yishay Mansour and Noam Nisan, Constant depth circuits, Fourier transform, and learnability, Journal of the ACM 40(3), 607 to 620 (1993)
    locator: the quasi-polynomial time learning algorithm for AC0
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 634 to 652 (1998)
    locator: the hardness result under the assumption that NP is not in DTIME(n^(O(log log n)))
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 3, Diagonalization (the time hierarchy theorem)
---

Quasi-polynomial time is the class of problems that a deterministic algorithm solves in time $2^{(\log n)^c}$ for some constant $c$, where $n$ is the input length. With $c = 1$ this is polynomial time, and with $c = 2$ it includes running times such as $n^{\log n}$. These bounds grow faster than every polynomial and slower than $2^{n^\varepsilon}$ for every $\varepsilon > 0$, so the class QP lies strictly between [P](/p/) and [subexponential time](/subexponential-time/). It is the home of several problems that are not known to be in P but are believed not to be NP-complete, such as [graph isomorphism](/graph-isomorphism-problem/) and [parity games](/parity-game/), and the assumption "NP is not in QP" is a common hypothesis behind hardness results.

## Definition

**The class.**

$$\mathsf{QP} = \bigcup_{c \ge 1} \mathsf{DTIME}\big(2^{(\log n)^c}\big),$$

where $\mathsf{DTIME}(t(n))$ is the class of languages decided by a deterministic multitape Turing machine in time $O(t(n))$. A function $t$ is quasi-polynomial if $t(n) \le 2^{(\log n)^c}$ for some $c$ and all large $n$. Another common form is $n^{(\log n)^k}$, which equals $2^{(\log n)^{k+1}}$ with logarithms to base 2, so the two forms give the same class. The definition does not depend on the base of the logarithm or on the machine model, since a change of base or a polynomial simulation overhead only changes the constant $c$.

**Closure.** Quasi-polynomial functions are closed under composition: if $t_1(n) = 2^{(\log n)^a}$ and $t_2(m) = 2^{(\log m)^b}$, then $t_2(t_1(n)) = 2^{(\log n)^{ab}}$. So an algorithm that runs in quasi-polynomial time, with a subroutine that also runs in quasi-polynomial time on inputs of quasi-polynomial length, still runs in quasi-polynomial time. In particular QP is closed under quasi-polynomial-time reductions, and if an NP-complete problem is in QP then $\mathsf{NP} \subseteq \mathsf{QP}$.

**Place among other classes.**

$$\mathsf{P} \subsetneq \mathsf{QP} \subsetneq \mathsf{SUBEXP} \subsetneq \mathsf{EXP}.$$

All three separations come from the [time hierarchy theorem](/time-hierarchy-theorem/), which gives $\mathsf{DTIME}(t') \subsetneq \mathsf{DTIME}(t)$ when $t' \log t' = o(t)$ and $t$ is time-constructible.

- $\mathsf{P} \subseteq \mathsf{DTIME}(n^{\log n}) \subsetneq \mathsf{DTIME}(n^{\log^2 n}) \subseteq \mathsf{QP}$.
- Let $g(n) = (\log n)^{\log \log n}$. It grows faster than every power of $\log n$ and slower than every power $n^\varepsilon$. So QP is inside $\mathsf{DTIME}(2^{g(n)/2})$, the class $\mathsf{DTIME}(2^{g(n)})$ is inside SUBEXP, and the hierarchy theorem separates the two.
- $\mathsf{SUBEXP} \subseteq \mathsf{DTIME}(2^{\sqrt{n}}) \subsetneq \mathsf{DTIME}(2^n) \subseteq \mathsf{EXP}$.

In the other direction, the relation of QP to nondeterministic classes is open: P versus NP is open, and so is whether $\mathsf{NP} \subseteq \mathsf{QP}$.

## Examples and non-examples

**How the bounds compare.** The table gives $\log_2$ of four running times.

| $n$ | $n^3$ | $n^{\log_2 n}$ | $2^{\sqrt{n}}$ | $2^n$ |
|---|---|---|---|---|
| $2^{4} = 16$ | $12$ | $16$ | $4$ | $16$ |
| $2^{10} = 1024$ | $30$ | $100$ | $32$ | $1024$ |
| $2^{16} = 65536$ | $48$ | $256$ | $256$ | $65536$ |
| $2^{20}$ | $60$ | $400$ | $1024$ | $1048576$ |
| $2^{30}$ | $90$ | $900$ | $32768$ | $1073741824$ |

With $n = 2^t$, the bound $n^{\log_2 n}$ is $2^{t^2}$ and $2^{\sqrt{n}}$ is $2^{2^{t/2}}$. The two are equal at $t = 16$, that is $n = 65536$. Between $n \approx 2.36$ and $n = 65536$ the quasi-polynomial bound is the larger one, and only above $n = 65536$ does the subexponential bound overtake it for good. Asymptotic order says little about practical sizes here.

**Graph isomorphism.** Babai (2016) gave an algorithm that decides whether two graphs on $n$ vertices are isomorphic in time $2^{(\log n)^{O(1)}}$. Before that, the best bound was $2^{O(\sqrt{n \log n})}$ (Babai and Luks 1983), a subexponential bound. Graph isomorphism is not known to be in P, and it is not NP-complete unless the [polynomial hierarchy](/polynomial-hierarchy/) collapses. Group isomorphism, for groups given by multiplication tables of size $n \times n$, is solved in time $n^{\log_2 n + O(1)}$ by choosing a generating set of at most $\log_2 n$ elements and trying all images of it.

**Parity games.** Calude, Jain, Khoussainov, Li and Stephan (2017) solved [parity games](/parity-game/) in quasi-polynomial time. Parity games are in $\mathsf{NP} \cap \mathsf{coNP}$, and whether they are in P is open.

**Problems with witnesses of logarithmic length.** Many problems ask whether some set of $O(\log n)$ elements exists. Trying all such sets takes time $n^{O(\log n)}$, a quasi-polynomial bound.

- *Dominating set in a tournament.* In a tournament on $n$ vertices, a dominating set is a set $D$ such that every vertex outside $D$ loses to some vertex in $D$. A greedy choice, always taking a vertex that beats the most remaining vertices, finds one of at most $\lfloor \log_2(n+1) \rfloor$ vertices, because each step removes at least half of the remaining vertices. So the minimum can be found by trying all sets of that size. In one random tournament on $32$ vertices, no set of $1$ or $2$ vertices dominates, among the $32 + 496$ candidates, and the greedy method and the exhaustive search both find a dominating set of $3$ vertices. The bound $\lfloor \log_2 33 \rfloor$ is $5$.
- *VC dimension.* Given a family of $m$ sets over a ground set of $n$ elements, the [VC dimension](/vc-dimension/) is at most $\log_2 m$, so it can be computed in time $(n m)^{O(\log m)}$. Papadimitriou and Yannakakis (1996) defined classes for such problems and showed that computing the VC dimension is complete for one of them. These problems are probably not in P, but they are not NP-complete unless NP is in QP.
- *Planted clique.* In a random graph on $n$ vertices, the largest clique has about $2 \log_2 n$ vertices, so a brute-force search over sets of $O(\log n)$ vertices finds a [planted clique](/planted-clique/) of size above that in quasi-polynomial time. Polynomial-time algorithms are known only for planted cliques of size about $\sqrt{n}$.
- *Monotone duality.* The [Fredman-Khachiyan algorithm](/fredman-khachiyan-algorithm/) decides whether two monotone DNFs are dual in time $N^{O(\log N)}$ for input size $N$. The problem is not known to be in P.

**Learning.** Linial, Mansour and Nisan (1993) learned [AC0](/ac0/) functions from uniform random examples in time $n^{\mathrm{poly}(\log n)}$.

**Hardness assumptions.** Hardness proofs that use reductions of quasi-polynomial size need the assumption that NP is not in QP, or a weaker form. Feige (1998) proved that [set cover](/set-cover/) cannot be approximated within $(1 - \varepsilon) \ln n$ unless $\mathsf{NP} \subseteq \mathsf{DTIME}(n^{O(\log \log n)})$. Hardness results based on [label cover](/label-cover/) with parallel repetition use similar assumptions. These assumptions follow from the exponential time hypothesis: a 3-SAT formula with $n$ variables has length polynomial in $n$, so a quasi-polynomial algorithm for 3-SAT would run in time $2^{(\log n)^{O(1)}} = 2^{o(n)}$.

**Non-examples.** Problems complete for EXP under polynomial-time reductions are not in QP, since $\mathsf{QP} \subsetneq \mathsf{EXP}$. NP-complete problems are not in QP unless $\mathsf{NP} \subseteq \mathsf{QP}$, which is open but would refute the exponential time hypothesis.

## Related definitions

- [Subexponential time](/subexponential-time/): time $2^{n^\varepsilon}$ for every $\varepsilon > 0$, a larger class.
- [Polynomial time](/polynomial-time/): the case $c = 1$.
- Quasi-polynomial size circuits: circuits of size $2^{(\log n)^{O(1)}}$, the non-uniform analogue. Murray and Williams (2018) proved that NQP, nondeterministic quasi-polynomial time, is not in ACC0.
- [Graph isomorphism](/graph-isomorphism-problem/) and [parity games](/parity-game/): the best-known problems in QP not known to be in P.

## References
