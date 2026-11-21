---
tag: BGVEK1
kind: model
slug: denning-lattice-model
name: Lattice model of information flow
aliases:
- Denning lattice model
- security class lattice
area: security-and-privacy/access-control-and-information-flow
level: core
summary: Puts security classes in a lattice and allows information to flow from one class to another only when the first is below the second.
model: word-ram
prereqs: [join-semilattice, mandatory-access-control]
see_also: [noninterference, implicit-flow, security-type-system, bell-lapadula-model, biba-integrity-model, decentralized-label-model, covert-channel, taint-analysis]
sources:
  - paper: doi:10.1145/360051.360056
    title: Dorothy E. Denning, A lattice model of secure information flow, Communications of the ACM 19(5), 1976
    locator: pp. 236 to 243, the flow model, the argument that the security classes form a lattice, and static and run-time mechanisms
  - paper: doi:10.1145/359636.359712
    title: Dorothy E. Denning and Peter J. Denning, Certification of programs for secure information flow, Communications of the ACM 20(7), 1977
    locator: "pp. 504 to 513; Section 2.1 (the lattice of classes, Figs. 1 and 2), Section 2.2 (explicit and implicit flows), Section 2.3 (exact security is undecidable), Section 3 (the certification mechanism and its theorem, Fig. 3)"
  - paper: doi:10.1109/JSAC.2002.806121
    title: Andrei Sabelfeld and Andrew C. Myers, Language-based information-flow security, IEEE Journal on Selected Areas in Communications 21(1), 2003
    locator: pp. 5 to 19, the survey of the field that grew from the lattice model
  - paper: doi:10.3233/JCS-1996-42-304
    title: Dennis Volpano, Cynthia Irvine and Geoffrey Smith, A sound type system for secure flow analysis, Journal of Computer Security 4(2-3), 1996
    locator: pp. 167 to 187, the certification of Denning and Denning as a type system, with a proof of noninterference
  - paper: doi:10.1093/comjnl/17.2.143
    title: J. S. Fenton, Memoryless subsystems, The Computer Journal 17(2), 1974
    locator: pp. 143 to 147, the data mark machine, a run-time check of flows
---

The lattice model of information flow, from Dorothy Denning (1976), gives each object of a system a security class and puts the classes in a lattice. Information may flow from class $a$ to class $b$ only when $a \le b$, and a value computed from several objects gets the join of their classes. A system is secure in the model if no sequence of its operations makes a flow that the order does not allow. The model is the base of the [security type systems](/security-type-system/), of the dynamic monitors on the later pages, and of the modern definition of [noninterference](/noninterference/).

## The machine

**Classes.** A security lattice is $(\mathcal{L}, \le, \sqcup, \sqcap)$. The relation $\ell_1 \le \ell_2$ reads "information may flow from $\ell_1$ to $\ell_2$". The join $\ell_1 \sqcup \ell_2$ is the least upper bound, the meet $\ell_1 \sqcap \ell_2$ is the greatest lower bound. The least class $\bot$ is the class of public data and of constants. The order is a [join-semilattice](/join-semilattice/) with a least element. A finite join-semilattice with a least element is a lattice: its greatest element $\top$ is the join of all classes, and the meet of two classes is the join of the classes below both.

**Flow model.** Denning's flow model has five parts: a set of objects (variables, files, the program counter), a set of processes, the set of security classes, a class-combining operator (the join) and the flow relation (the order). Each object $x$ has a class $\Gamma(x)$. In the static form of the model the class of an object is fixed. In the dynamic form it can change during the run.

**Why a lattice.** Denning and Denning (1977, Section 2.1) give the argument. The flow relation is reflexive, since an object may flow to itself, and transitive, since a flow from $a$ to $b$ and from $b$ to $c$ is a flow from $a$ to $c$. A value computed from objects $x_1, \dots, x_k$ must go to a class that is above each $\Gamma(x_i)$, and the least such class is the natural one to give it. So the classes need a least upper bound for each finite set, and a finite set of classes with such bounds and a least class is a lattice. A finite order without joins can be made into a lattice by adding classes.

**Transitions.** A transition is one operation of a process. An operation $b \leftarrow f(a_1, \dots, a_k)$ makes an *explicit flow* from each $a_i$ to $b$, and it is allowed when $\Gamma(a_1) \sqcup \dots \sqcup \Gamma(a_k) \le \Gamma(b)$. An operation that runs only when a condition on $c$ holds also makes an *implicit flow* from $c$ to $b$ (see [implicit flow](/implicit-flow/)). In a program the second kind is written with the class of the program counter: an assignment $x := e$ under a program counter of class $pc$ is allowed when $\mathrm{label}(e) \sqcup pc \le \Gamma(x)$.

**Common lattices.**

| lattice | classes | order | join |
|---|---|---|---|
| two-point | $L, H$ | $L \le H$ | $L \sqcup H = H$ |
| linear | unclassified, confidential, secret, top secret | the listed order | the larger level |
| subsets | all subsets of a set $K$ of categories | $A \le B$ if $A \subseteq B$ | $A \cup B$ |
| military | pairs $(c, A)$ of a level and a set of categories | $(c_1, A_1) \le (c_2, A_2)$ if $(c_2, A_2)$ dom $(c_1, A_1)$ | $(\max(c_1, c_2), A_1 \cup A_2)$ |

The figures of Denning and Denning show the linear lattice (Fig. 1) and the lattice of subsets of three properties (Fig. 2). The military lattice is the one of [Bell-LaPadula](/bell-lapadula-model/) and of [mandatory access control](/mandatory-access-control/).

## What it counts

The model decides two things.

- **Is one flow allowed?** For classes $a$ and $b$ this is the test $a \le b$. In the [word-RAM](/word-ram/) with a subset lattice over $k \le w$ categories, a class is one machine word, the test is $a \mathbin{\&} \lnot b = 0$ and the join is $a \mathbin{|} b$, so both take $O(1)$ time. For a general finite lattice of $n$ classes, a table of the order or of the join takes $O(n^2)$ space and gives $O(1)$ time per operation.
- **Is a program or a system secure?** A program is secure if each run makes only allowed flows, so that the final value of each object $y$ depends only on the initial values of objects $x$ with $\Gamma(x) \le \Gamma(y)$. The modern semantic form of this is [noninterference](/noninterference/).

A mechanism is *sound* if each program it accepts is secure, and *precise* if it accepts each secure program. Denning (1976) separates static mechanisms, which check a program before it runs, from run-time mechanisms, which check each operation.

## Relation to other models

- **[Bell-LaPadula](/bell-lapadula-model/).** BLP controls access: a subject may read objects at or below its level and write objects at or above it. The lattice model controls flows inside a program. A program that obeys BLP can still leak through its control flow, which the lattice model counts. Both use the same order, and BLP's levels form one lattice of the table above.
- **[Biba](/biba-integrity-model/).** Biba uses the same structure for integrity, with trusted data at the bottom: $T \le U$, so information may flow from trusted to untrusted data and not back. Biba's papers write the order the other way.
- **[Decentralized label model](/decentralized-label-model/).** Myers and Liskov keep the lattice, but a label is a set of policies of several owners, and each owner can relax its own policy.
- **[Taint analysis](/taint-analysis/).** Taint tracking is the two-point lattice with only explicit flows in most tools. It drops the program counter class, so it misses implicit flows.
- **[Covert channels](/covert-channel/).** Flows through time, resource use or termination are outside the model unless the objects include them.

## Known results in the model

- **Lattice structure.** Under the assumptions above, the classes form a finite lattice (Denning 1976; Denning and Denning 1977, Section 2.1).
- **Exact security is undecidable.** Whether a program makes a disallowed flow is undecidable. Denning and Denning (Section 2.3) use the program "if $f(x)$ halts then $y := 0$". The question is also an instance of [Rice's theorem](/rice-theorem/). So each sound static mechanism rejects some secure programs, for example "if $x = 0$ then if $x \ne 0$ then $y := z$".
- **Certification theorem.** Denning and Denning (Section 3) check each statement at compile time: for an assignment, the join of the source classes must be below the target class, and for an if or a while statement, the class of the condition must be below the meet of the classes of the targets in its body. Their theorem: a program is certified only if it is secure, by induction on the structure of the program. The check is linear in the size of the program.
- **Soundness for noninterference.** Volpano, Irvine and Smith (1996) recast the certification as a [type system](/security-type-system/) and proved that a typable program is termination-insensitive noninterferent ([TINI](/termination-insensitive-noninterference/)). The proof does not cover leaks through termination or time.
- **Run-time checks.** Fenton's data mark machine (1974) showed that a run-time check that looks only at the branch that runs can leak through the branch that does not run. The [no-sensitive-upgrade](/no-sensitive-upgrade/) check, [secure multi-execution](/secure-multi-execution/) and [faceted execution](/faceted-execution/) are three ways to make a run-time mechanism sound.

## References
