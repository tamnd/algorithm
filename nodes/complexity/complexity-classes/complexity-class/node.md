---
tag: 2HA8YK
kind: concept
slug: complexity-class
name: Complexity class
aliases:
- complexity classes
area: complexity/complexity-classes
level: intro
summary: A set of languages defined by a machine model, a resource such as time or space, and a bound on that resource as a function of the input length.
prereqs: [turing-machine, time-complexity, space-complexity, decision-problem]
see_also: [p, np, exptime, class-inclusions-chain, multitape-turing-machine, nondeterministic-turing-machine, time-hierarchy-theorem, polynomial-time]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 1 (DTIME and the class P, the robustness of the model), Section 2.6 (coNP, EXP and NEXP) and Chapter 4 (space classes)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.1 (measuring complexity, TIME, the relation between models), Section 7.3 (NTIME), Section 8.4 (the classes L and NL) and Section 9.1 (hierarchy theorems)
  - paper: doi:10.1090/S0002-9947-1965-0170805-7
    title: J. Hartmanis and R. E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117 (1965), 285 to 306
    locator: the definition of time-bounded complexity classes of multitape machines
  - paper: doi:10.1016/S0019-9958(65)90399-2
    title: F. C. Hennie, One-tape, off-line Turing machine computations, Information and Control 8(6) (1965), 553 to 578
    locator: the quadratic lower bound for one-tape machines by crossing sequences
  - paper: doi:10.1145/321679.321691
    title: A. Borodin, Computational complexity and the existence of complexity gaps, Journal of the ACM 19(1) (1972), 158 to 174
    locator: the gap theorem
  - url: https://complexityzoo.net/Complexity_Zoo
    title: Scott Aaronson and others, The Complexity Zoo
    locator: the list of classes
---

A complexity class is a set of [decision problems](/decision-problem/), written as languages, that is fixed by three choices: a model of computation, a resource that the model uses, and a bound on that resource as a function of the input length. The class [P](/p/) is the set of languages that a deterministic [multitape Turing machine](/multitape-turing-machine/) decides in polynomial time. The class [NP](/np/) uses a [nondeterministic machine](/nondeterministic-turing-machine/) with the same bound. Most questions of complexity theory are questions about the inclusions between classes, and about which of them are strict.

## In plain words

Sort problems into boxes by how much work a machine needs to answer them. A box has a label with three parts. The first part names the kind of machine, for example an ordinary machine or a machine that can guess. The second part names what you count, for example the steps or the memory cells. The third part gives the budget, as a rule that says how the budget grows with the length of the input.

A problem goes into a box when some machine of that kind answers every input of the problem within the budget. One problem can be in many boxes, because a bigger budget gives a bigger box. The main open questions ask whether two boxes with different labels hold the same problems. For most pairs of boxes nobody knows.

## The idea

### Languages

Fix the alphabet $\Sigma = \{0, 1\}$. A language is a set $L \subseteq \Sigma^*$. A machine *decides* $L$ when it halts on every input $x$ and accepts exactly when $x \in L$. A decision problem becomes a language after we fix an encoding of its instances as strings, and the input length $n = |x|$ is the length of that encoding. Numbers are written in binary and graphs as adjacency lists or matrices, unless a page says otherwise.

### The basic classes

The standard model is the deterministic multitape [Turing machine](/turing-machine/). Let $f : \mathbb{N} \to \mathbb{N}$.

- $\mathsf{DTIME}(f(n))$ is the set of languages that some deterministic multitape machine decides within $O(f(n))$ steps on every input of length $n$.
- $\mathsf{NTIME}(f(n))$ is the set of languages that some nondeterministic multitape machine decides with every computation path of length $O(f(n))$. The machine accepts $x$ when at least one path accepts.
- $\mathsf{DSPACE}(f(n))$ and $\mathsf{NSPACE}(f(n))$ use a read-only input tape and count only the cells that the machine visits on its work tapes. This lets the bound be smaller than $n$. For these classes we assume $f(n) \ge \log n$.

Most named classes are unions over a family of bounds:

$$\mathsf{P} = \bigcup_{k \ge 1} \mathsf{DTIME}(n^k), \qquad \mathsf{NP} = \bigcup_{k \ge 1} \mathsf{NTIME}(n^k), \qquad \mathsf{PSPACE} = \bigcup_{k \ge 1} \mathsf{DSPACE}(n^k),$$

$$\mathsf{EXP} = \bigcup_{k \ge 1} \mathsf{DTIME}(2^{n^k}), \qquad \mathsf{L} = \mathsf{DSPACE}(\log n), \qquad \mathsf{NL} = \mathsf{NSPACE}(\log n).$$

For a class $\mathcal{C}$, the class $\mathsf{co}\mathcal{C}$ is $\{\, \Sigma^* \setminus L : L \in \mathcal{C} \,\}$. So [coNP](/co-np/) holds the complements of the languages in NP. A deterministic class is closed under complement: swap the accepting and rejecting states. For nondeterministic time classes this argument fails, because "some path accepts" turns into "every path rejects".

Other models give other classes. A [probabilistic machine](/probabilistic-turing-machine/) with a bound on its error gives [BPP](/bpp/) and [RP](/rp/). An [alternating machine](/alternating-turing-machine/) gives the [polynomial hierarchy](/polynomial-hierarchy/) when the number of alternations is bounded. Families of [Boolean circuits](/boolean-circuit/) with a bound on size and depth give [P/poly](/p-poly/), [NC](/nc/) and [AC0](/ac0/). A machine with an [oracle](/oracle-turing-machine/) for a set $A$ gives relativized classes such as $\mathsf{P}^A$.

### What does not depend on the model

The class P does not change when the multitape machine is replaced by a one-tape machine or by a random-access machine with the logarithmic cost. A one-tape machine simulates $k$ tapes with a quadratic slowdown ([multitape simulation theorem](/multitape-simulation-theorem/)), and a RAM and a Turing machine simulate each other with a polynomial slowdown ([RAM and Turing machine equivalence](/ram-turing-equivalence/)). So P, NP, PSPACE and EXP are the same in all these models.

The exact exponent changes. A class such as $\mathsf{DTIME}(n)$ or $\mathsf{DTIME}(n^2)$ depends on the number of tapes. Constant factors do not matter for a fixed model, because the [linear speedup theorem](/linear-speedup-theorem/) removes them. This is why the definition uses $O(f(n))$.

### Constructible bounds

The bound $f$ must be a reasonable function. A function $f$ with $f(n) \ge n$ is *time-constructible* when some machine computes $f(n)$ in binary from the input $1^n$ in $O(f(n))$ steps. Polynomials, $n \log n$ and $2^n$ are time-constructible. The [time hierarchy theorem](/time-hierarchy-theorem/) needs this condition, and without it strange things happen. Borodin's gap theorem (1972) shows that for every total computable $g$ with $g(m) \ge m$ there is a total computable $t$ with $\mathsf{DTIME}(g(t(n))) = \mathsf{DTIME}(t(n))$. With $g(m) = 2^m$, an exponential increase of the time bound adds no language at all. The function $t$ from this theorem is not time-constructible.

### Relations between classes

Classes are compared by inclusion. There are three standard tools.

- **Simulation** gives inclusions. A deterministic machine is a nondeterministic machine with one choice, so $\mathsf{DTIME}(f) \subseteq \mathsf{NTIME}(f)$. A machine that runs for $f(n)$ steps visits at most $f(n)$ cells, so $\mathsf{DTIME}(f) \subseteq \mathsf{DSPACE}(f)$.
- **Diagonalization** gives separations between classes of the same model with bounds that are far enough apart. The [time hierarchy theorem](/time-hierarchy-theorem/) and the [space hierarchy theorem](/space-hierarchy-theorem/) give $\mathsf{P} \subsetneq \mathsf{EXP}$ and $\mathsf{NL} \subsetneq \mathsf{PSPACE}$.
- **Completeness** finds the hardest problems of a class under a type of reduction. A class that is closed under that reduction contains a complete problem of a larger class only if the two classes are equal. For example, if an [NP-complete](/np-complete/) problem is in P, then $\mathsf{P} = \mathsf{NP}$.

The [chain of inclusions](/class-inclusions-chain/) $\mathsf{L} \subseteq \mathsf{NL} \subseteq \mathsf{P} \subseteq \mathsf{NP} \subseteq \mathsf{PSPACE} \subseteq \mathsf{EXP}$ is proved by simulation. No single step of it is known to be strict.

### Pitfalls

- **A class holds problems, not algorithms.** "Sorting is in P" is loose. Sorting is a function problem, and its class is [FP](/fp/). A decision version, for example "is the array sorted?", is in P.
- **Membership is an upper bound.** A problem is in a class when *some* machine meets the bound. To show that a problem is *not* in a class needs a lower bound for every machine, and such proofs are rare.
- **NP does not mean "not polynomial".** NP means nondeterministic polynomial time, and $\mathsf{P} \subseteq \mathsf{NP}$. Every problem in P is in NP.
- **The encoding is part of the problem.** The same question about numbers can be in P with the numbers in unary and NP-complete with the numbers in binary. See [pseudo-polynomial time](/pseudo-polynomial-time/).
- **Time classes with an exact exponent need a model.** "$\mathsf{DTIME}(n)$" without the number of tapes is not well defined, as the first example below shows.

## Examples

**Palindromes on one tape and on two tapes.** Let $\mathrm{PAL} = \{ w \in \{a, b\}^* : w \text{ equals its reverse} \}$. A one-tape machine erases the first symbol, remembers it in its state, walks to the right end, compares and erases the last symbol, walks back, and repeats. On a palindrome of length $n$ it takes exactly $(n+1)(n+2)/2$ steps. A two-tape machine copies the input to the second tape, moves the first head back, and then compares with the two heads moving in opposite directions, in $3n + 3$ steps. A simulation of both machines gives these counts:

| $n$ | one tape | two tapes |
|---|---|---|
| 8 | 45 | 27 |
| 16 | 153 | 51 |
| 32 | 561 | 99 |
| 64 | 2145 | 195 |
| 128 | 8385 | 387 |

Hennie (1965) proved by a crossing-sequence argument that every one-tape machine for PAL needs $\Omega(n^2)$ steps. So PAL is in $\mathsf{DTIME}(n)$ for two-tape machines but not for one-tape machines. Both machines are polynomial, so PAL is in P in both models.

**The labels of some classes.**

| class | model | resource | bound |
|---|---|---|---|
| [L](/logspace/) | deterministic TM | work space | $O(\log n)$ |
| [NL](/nondeterministic-logspace/) | nondeterministic TM | work space | $O(\log n)$ |
| [P](/p/) | deterministic TM | time | $n^{O(1)}$ |
| [NP](/np/) | nondeterministic TM | time | $n^{O(1)}$ |
| [BPP](/bpp/) | probabilistic TM, two-sided error at most 1/3 | time | $n^{O(1)}$ |
| [PSPACE](/pspace/) | deterministic TM | space | $n^{O(1)}$ |
| [EXP](/exptime/) | deterministic TM | time | $2^{n^{O(1)}}$ |
| [NEXP](/nexptime/) | nondeterministic TM | time | $2^{n^{O(1)}}$ |
| [P/poly](/p-poly/) | Boolean circuit family, non-uniform | size | $n^{O(1)}$ |

**Problems and their classes.** [Graph reachability](/graph-reachability/) in directed graphs is in NL. The [2-SAT](/2-sat/) problem is in P. [SAT](/sat/) is in NP, and the set of unsatisfiable formulas is in coNP. Deciding the winner of [generalized geography](/generalized-geography/) is in PSPACE.

**Non-example.** "The problems that can be solved in time $n^2$" is not a definition of a class until it names the model. On one tape PAL is not in it, on two tapes PAL is in it.

## Where it is used

Classes give a common language to state what is known about a problem. A proof that a problem is complete for a class, for example [NP-complete](/np-complete/) or PSPACE-complete, says that an efficient algorithm for it would put the whole class into P. Upper bounds put a problem into a class, and reductions place the problem relative to the others.

The open questions of the field are questions about classes: the [P versus NP problem](/p-versus-np-problem/), NP against coNP, P against PSPACE, and L against P. The known separations come from the hierarchy theorems and are listed on the page on the [chain of inclusions](/class-inclusions-chain/).

The idea goes back to Hartmanis and Stearns (1965), who defined the classes of languages that a multitape machine decides within a time bound $T(n)$ and proved the first hierarchy theorem. The Complexity Zoo, an online catalogue maintained by Scott Aaronson and others, lists several hundred classes.

## References
