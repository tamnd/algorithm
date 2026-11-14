---
tag: AVZMQ8
kind: data-structure
slug: majority-inverter-graph
name: Majority-inverter graph
aliases:
- MIG
area: eda/logic-synthesis
level: research
summary: A Boolean network of three-input majority nodes with inverted edges, with an algebra of five axioms for restructuring, from Amaru, Gaillardon and De Micheli.
model: word-ram
complexity:
  vars: {N: the number of majority nodes, n: the number of primary inputs, w: the number of bits in a machine word}
  time: {maj: O(1) expected, simulate: O(N 2^n / w), levels: O(N)}
  space: {nodes: O(N)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 2014
  people: [Luca Amaru, Pierre-Emmanuel Gaillardon, Giovanni De Micheli]
  note: Amaru, Gaillardon and De Micheli introduced the majority-inverter graph and its axioms at DAC 2014 and gave the full theory, with soundness and completeness of the axioms, in IEEE TCAD in 2016.
prereqs: [boolean-network, hash-consing, and-inverter-graph]
see_also: [aig-rewriting, aig-balancing, exact-synthesis, technology-mapping, binary-decision-diagram, rewrite-rule, equational-theory, sorting-network]
sources:
  - paper: doi:10.1145/2593069.2593158
    title: Luca Amaru, Pierre-Emmanuel Gaillardon and Giovanni De Micheli, Majority-inverter graph, a novel data-structure and algorithms for efficient logic optimization, Proceedings of the 51st Design Automation Conference, 2014
    locator: the definition of the MIG, the axioms Omega, and the depth and size optimization by axiom application
  - paper: doi:10.1109/TCAD.2015.2488484
    title: Luca Amaru, Pierre-Emmanuel Gaillardon and Giovanni De Micheli, Majority-inverter graph, a new paradigm for logic optimization, IEEE Transactions on Computer-Aided Design 35(5), 2016, pages 806 to 819
    locator: the axioms Omega, the derived rules Psi, the soundness and completeness of Omega, and the optimization algorithms
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.1.1, the median operation and its laws
---

A majority-inverter graph, or MIG, is a [Boolean network](/boolean-network/) in which every inner node is the majority of three inputs and every edge may carry an inverter. The majority $\langle x y z \rangle = xy + xz + yz$ is 1 when at least two of its inputs are 1. With one input fixed to 0 it is AND, and with one input fixed to 1 it is OR, so every [and-inverter graph](/and-inverter-graph/) is an MIG with the same number of nodes. Amaru, Gaillardon and De Micheli gave the MIG an algebra of five axioms, and they restructure the graph by applying these axioms, mainly to make it shallower.

## In plain words

Build a circuit from one kind of gate that takes three wires and outputs the value that at least two of them carry. A dot on a wire flips its value. If you tie one input of the gate to 0, it becomes an AND gate. If you tie it to 1, it becomes an OR gate. So this gate can do all that an AND gate can do, and often more in one step: one gate gives the carry of an adder.

As with AND gates, keep a dictionary of the gates you have built, keyed by their three input wires, and reuse a gate when you see it again.

A small set of rules says when two drawings of majority gates compute the same thing. Tools apply these rules to move late signals near the output and so make the circuit faster.

## The abstract type

An MIG over the inputs $x_1, \ldots, x_n$ stores a set of nodes, each one a Boolean function of the inputs. A *literal* names a node and a phase, as on the [AIG](/and-inverter-graph/) page. The operations are:

- INPUT(i): the literal of $x_i$.
- MAJ(a, b, c): a literal whose function is $\langle f_a f_b f_c \rangle$. NOT is free. AND(a, b) is MAJ(a, b, 0) and OR(a, b) is MAJ(a, b, 1).
- SIMULATE(o_1, ..., o_k): the truth tables of the given literals.
- LEVELS: the depth of each node, the number of majority nodes on the longest path from an input.

The contract of MAJ is that the function is right, that the result is the same for all six orders of $a, b, c$ and for the call on $\neg a, \neg b, \neg c$ with the phase flipped, and that no node is added twice for the same normal form. As in an AIG, two literals with the same function can still differ.

The equalities that the tools use are the axioms $\Omega$ of the TCAD 2016 paper. For all functions $x, y, z, u, v$:

| axiom | identity |
|---|---|
| $\Omega.C$, commutativity | $\langle x y z \rangle = \langle y x z \rangle = \langle z y x \rangle$ |
| $\Omega.M$, majority | $\langle x x z \rangle = x$ and $\langle x \bar{x} z \rangle = z$ |
| $\Omega.A$, associativity | $\langle x u \langle y u z \rangle \rangle = \langle z u \langle y u x \rangle \rangle$ |
| $\Omega.D$, distributivity | $\langle x y \langle u v z \rangle \rangle = \langle \langle x y u \rangle \langle x y v \rangle z \rangle$ |
| $\Omega.I$, inverter propagation | $\overline{\langle x y z \rangle} = \langle \bar{x} \bar{y} \bar{z} \rangle$ |

The paper also derives three rules from them. Relevance, $\Psi.R$, says that $\langle x y z \rangle = \langle x y z_{x/\bar{y}} \rangle$, where $z_{x/\bar{y}}$ is $z$ with every $x$ replaced by $\bar{y}$: the value of $z$ matters only where $x \ne y$. Complementary associativity, $\Psi.C$, says that $\langle x u \langle y \bar{u} z \rangle \rangle = \langle x u \langle y x z \rangle \rangle$. Substitution, $\Psi.S$, splits a node on a variable $v$ and a second signal $u$. The authors prove that $\Omega$ is sound and complete for the functions of majority and complement: two MIGs compute the same function if and only if a finite sequence of axioms turns one into the other. These identities are the laws of the median operation in Knuth's treatment, Section 7.1.1 of Volume 4A.

## Representation

A literal is the integer $2v + c$ as in the AIG: node 0 is the constant 0, so literal 1 is the constant 1, nodes 1 to $n$ are the inputs, and every later node $v$ holds three fanin literals of older nodes. A node is stored in a normal form. Its fanins $a < b < c$ are sorted, lie on three different nodes, and at most one of them is complemented. A hash table maps the triple $(a, b, c)$ to $v$. The constant 1 counts as a complemented edge to node 0, so an AND node is stored as $(0, a, b)$ and an OR node as $(1, a, b)$.

## Operations

```pseudo id=main
MAJ(a, b, c)
L1  sort a, b, c so that a ≤ b ≤ c                  ▷ Ω.C
L2  if a = b or b = c then return b                 ▷ Ω.M, ⟨x x z⟩ = x
L3  if a = b xor 1 then return c; if b = c xor 1 then return a   ▷ Ω.M, ⟨x x̄ z⟩ = z
L4  if two or more of a, b, c are odd then return MAJ(a xor 1, b xor 1, c xor 1) xor 1   ▷ Ω.I
L5  if T holds the key (a, b, c) then return 2·T[a, b, c]   ▷ structural hashing
L6  v ← a new node with fanins (a, b, c); T[a, b, c] ← v; return 2v

SIMULATE(o_1, ..., o_k)                ▷ truth tables as integers of 2^n bits
L7  val[0] ← 0; val[i] ← the table of x_i for i = 1 to n
L8  for v ← n + 1 to the last node: val[v] ← ⟨lit(a_v) lit(b_v) lit(c_v)⟩ bitwise
L9  return lit(o_1), ..., lit(o_k)     ▷ lit(2u + c) = val[u], complemented if c = 1
```

Line L1 applies $\Omega.C$, so that the six orders of a call give one key. In sorted order the two literals of one node are next to each other, so lines L2 and L3 find every pair on one node and apply $\Omega.M$. After them the three fanins lie on three different nodes. Line L4 applies $\Omega.I$ when it lowers the number of complemented fanins, which leaves at most one. The inner call does not reach line L4 again. Line L8 computes the majority of three words with $(x \wedge y) \vee (x \wedge z) \vee (y \wedge z)$, so all $2^n$ points are simulated at once.

The axioms $\Omega.A$ and $\Omega.D$ are not applied by MAJ. They change the shape of the graph over more than one node, and an optimizer applies them where they lower the depth or the size.

## Example

Build a full adder over $a, b, c$ with the literals 2, 4 and 6. The carry is one majority node, and the sum $a \oplus b \oplus c$ takes two more.

| step | call | normal form | result | nodes |
|---|---|---|---|---|
| 1 | MAJ(2, 4, 6), the carry $\langle a b c \rangle$ | (2, 4, 6) | new node 4, literal 8 | 1 |
| 2 | MAJ(2, 4, 7), the inner node $\langle a b \bar{c} \rangle$ | (2, 4, 7) | new node 5, literal 10 | 2 |
| 3 | MAJ(9, 6, 10), the sum $\langle \overline{\text{carry}}\, c\, \langle a b \bar{c} \rangle \rangle$ | (6, 9, 10) | new node 6, literal 12 | 3 |
| 4 | MAJ(4, 6, 2), the carry again | (2, 4, 6) | found node 4, literal 8 | 3 |
| 5 | MAJ(3, 5, 7), the complement of the carry | (2, 4, 6) by L4 | literal 9 | 3 |

SIMULATE gives 232 (the bits 11101000) for the carry and 150 (the bits 10010110) for the sum. The MIG has 3 nodes and depth 2, while the AIG of the same adder on the [and-inverter graph](/and-inverter-graph/) page has 7 AND nodes and depth 4. No MIG with fewer than 3 nodes computes both outputs, because the sum of three inputs is not the majority of three literals. Steps 4 and 5 show $\Omega.C$ and $\Omega.I$ at work: a permuted call and the call on three complemented literals find node 4 again.

$\Omega.A$ lowers the depth when a late signal sits deep in the graph. Over seven inputs, let $z = \langle p q \langle r t (p \wedge r) \rangle \rangle$, which has depth 3. Then $f = \langle x u \langle y u z \rangle \rangle$ has depth 5, because $z$ enters at the bottom. $\Omega.A$ swaps $x$ and $z$ and gives $\langle z u \langle y u x \rangle \rangle$, which has depth 4 and the same truth table.

## Correctness

The [full proof](proofs/correctness.md) shows that every node stays in the normal form: three sorted fanins on three different older nodes, at most one of them complemented, and a table that maps each triple to its node and holds no other key. It then shows that MAJ returns a literal whose function is $\langle f_a f_b f_c \rangle$, since each line uses an axiom that is true for all values, and that MAJ gives the same literal for all orders of its inputs and the complemented literal for complemented inputs. So no two nodes have the same normal form. SIMULATE is right by induction on the node number. The five axioms hold for all 0 and 1 values, which the test file checks on all $2^3$, $2^4$ and $2^5$ points.

## Complexity

MAJ sorts three numbers, makes at most one inner call and does one hash lookup, so it takes $O(1)$ expected time. SIMULATE takes $O(N 2^n / w)$ word operations for $N$ nodes and $n$ inputs. LEVELS is one pass in $O(N)$. The space is three integers for each node and one table entry, $O(N)$.

An MIG never needs more nodes than an AIG of the same function, and never more depth, because each AND node becomes one majority node with a constant input. The full adder shows that it can need fewer. A node costs three fanins in place of two, so the memory per node is higher.

## Variants

- **Depth optimization.** The 2014 and 2016 papers push critical signals up with $\Omega.A$, $\Psi.C$ and $\Omega.D$ from left to right, then clean up with $\Omega.M$ and $\Omega.D$ from right to left. The papers report depth and size results on benchmark circuits against AIG optimization in ABC. These are measured results, not proved bounds.
- **Size optimization.** The same axioms, applied to remove nodes, with $\Omega.M$ and $\Omega.D$ from right to left as the main steps.
- **Cut rewriting.** As in [AIG rewriting](/aig-rewriting/), a small cut of a node is replaced by a smaller MIG of the same function, which [exact synthesis](/exact-synthesis/) finds for small numbers of inputs.
- **XOR-majority graphs.** Adding a three-input XOR node gives a graph that suits arithmetic, since the sum of a full adder is then one node.
- **Mapping.** An MIG can be mapped to cells or to lookup tables by [technology mapping](/technology-mapping/) over [cuts](/k-feasible-cut/), in the same way as an AIG.

## When to use it

Use an MIG when the target logic has majority gates, as in several proposed nanotechnologies, or when you want to restructure for depth with algebraic rules that are stronger than AND and OR rules. Arithmetic circuits gain most, since carries are majorities. Use an [AIG](/and-inverter-graph/) when you need the common format of the tool chain, its large set of tested passes, and a node of two fanins. Use a [BDD](/binary-decision-diagram/) when you need a canonical form.

## Pitfalls

- **Sorting without looking at pairs.** The checks of lines L2 and L3 rely on the sorted order, which puts $x$ next to $\bar{x}$. A check of only $a = b$ misses $\langle x \bar{x} z \rangle$ and keeps a node that is really a wire.
- **A normal form with complemented edges on both sides.** Without line L4, $\langle x y z \rangle$ and $\overline{\langle \bar{x} \bar{y} \bar{z} \rangle}$ get two nodes. The constant 1 must count as a complemented 0, or AND and OR nodes are stored in two forms.
- **Reading completeness as an algorithm.** Completeness says that a sequence of axioms joins two equal MIGs. It does not say how to find a short sequence, or how to find the smallest MIG. The optimizers that apply the axioms are heuristics.
- **Counting depth with constant inputs.** An AND node of an MIG has the constant 0 as a fanin. The constant is at level 0 and adds no depth, but a node with a constant input is still a node.

## Implementations

## History

The majority function is the heart of threshold logic and of the early work on switching circuits, and the median laws of $\langle x y z \rangle$ were studied by Birkhoff and Kiss and later by Knuth. Amaru, Gaillardon and De Micheli (DAC 2014) made the majority node the single gate of a logic network, gave it the axioms $\Omega$ and the derived rules $\Psi$, and showed depth optimization by axiom application. Their 2016 paper in IEEE TCAD proved that $\Omega$ is sound and complete. Later work added exact synthesis of small MIGs, cut rewriting and XOR-majority graphs, and the EPFL logic synthesis libraries made MIGs one of their main network types.

## References
