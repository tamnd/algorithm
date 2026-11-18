---
tag: JVDGBF
kind: data-structure
slug: packed-trie
name: Packed trie
aliases:
- Liang packed trie
area: strings/text-processing-and-typesetting
level: advanced
summary: A trie whose node arrays are overlapped in one table by first fit, so that sparse nodes share space and lookup stays one index per character.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {m: the length of the key, F: the number of families (nodes with children), S: the number of slots of the table, sigma: the size of the alphabet}
  time: {worst: O(m)}
  space: {extra: Θ(S)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1983
  people: [Franklin Mark Liang]
  note: Liang introduced the packed trie in his Stanford thesis of 1983 to store the hyphenation patterns of TeX82, with first-fit packing inspired by Tarjan and Yao.
prereqs: [trie]
see_also: [trie, double-array-trie, louds-trie, ternary-search-tree, trie-serialization, liang-hyphenation, dfa-minimization, first-fit-decreasing]
sources:
  - url: http://bitsavers.trailing-edge.com/pdf/stanford/Stanford_CS_TR_Collection_2025-12-12/PDF/1983/CS-TR-83-977.pdf
    title: "Franklin Mark Liang, Word Hy-phen-a-tion by Com-put-er, PhD thesis, Stanford University, August 1983, report STAN-CS-83-977"
    locator: "Chapter 2 (packed tries, first-fit packing, suffix compression and Table 1) and Table 5 (the size of the TeX82 pattern trie)"
  - paper: doi:10.1145/359168.359175
    title: "Robert Endre Tarjan and Andrew Chi-Chih Yao, Storing a sparse table, Communications of the ACM 22(11), 606-611, 1979"
    locator: "row displacement and the first-fit-decreasing method with the harmonic decay condition"
  - book: isbn:0201134373
    title: "Donald E. Knuth, TeX: The Program, Computers and Typesetting volume B, Addison-Wesley, 1986"
    locator: "the parts on the hyphenation trie and its packing"
---

A packed trie stores an indexed [trie](/trie/) in one table. In an indexed trie every node with children (a *family*) has an array with one slot per letter, and most slots are empty. The packed trie gives each family a base $b$ and puts its transition on the letter $c$ at slot $b + \mathrm{code}(c)$ of a shared table, so that the families fill each other's holes. Each slot also stores its letter, and no two families get the same base, so a lookup can tell its own transitions from the others. Franklin Liang designed it in 1983 to hold the hyphenation patterns of TeX82, and a lookup costs one table index per letter, as in the full indexed trie.

## In plain words

A trie node for a word list usually has only a few of the 26 possible children. Giving it a full row of 26 slots wastes most of them. A packed trie slides all the rows over one long table, like combs with missing teeth pushed into each other, so that the teeth of one row fall into the gaps of the others.

To read a child, go to the row's start plus the letter's number. The slot there may belong to another row. So each slot also keeps its letter: if the letter matches, the slot is yours, because two rows never start at the same place. The rows are placed one at a time, each at the first place where it fits.

## The abstract type

A packed trie is a static map from nonempty strings to values: a [string symbol table](/string-symbol-table/) without insertions after the build. It supports:

- `build(D)`: the table for a finite map $D$;
- `get(x)`: the value $D(x)$, or nothing if $x$ is not a key;
- `prefix_values(t, i)`: the keys that are prefixes of $t[i \ldots]$, with their values, which is the walk of [Liang's hyphenation](/liang-hyphenation/) at one start position.

## Representation

Give the letters the codes $1, \ldots, \sigma$. The table has $S$ slots, and slot $s$ holds three fields:

- $\mathrm{char}[s]$: the letter of the transition in this slot, or empty;
- $\mathrm{link}[s]$: the base of the family of the child, or nil if the child has no children;
- $\mathrm{out}[s]$: the value of the key that ends with this transition, or nil.

The root has a base $\beta_0$. The invariant:

- (I1) the families have distinct bases;
- (I2) each slot holds the transition of at most one family;
- (I3) the transition of the family with base $b$ on the letter $c$ is in slot $b + \mathrm{code}(c)$, with $\mathrm{char} = c$ and the right link and output.

In TeX82 a transition takes 4 bytes, for the letter, the link and an index into a separate table of digit lists. TeX82 also merges equal subtries before packing (suffix compression), so a family can have several parents.

## Operations

```pseudo id=main
SLOT(b, c)                                 ▷ the slot of the transition on c, or nil
L1  s ← b + code(c)
L2  if s < S and char[s] = c then return s
L3  return nil

GET(x)
L4  b ← β0; for each letter c of x do
L5      s ← SLOT(b, c)
L6      if s = nil then return nil         ▷ no key has this prefix
L7      b ← link[s]
L8  return out[s]

FIRST-FIT(C)                               ▷ C: the codes of the letters of one family
L9  b ← 0
L10 loop
L11     if b is not a base yet and slot b + a is empty for every a in C then
L12         return b
L13     b ← b + 1

BUILD(D)                                   ▷ the trie of D is built first
L14 for each family φ in breadth-first order do
L15     b ← FIRST-FIT(the codes of the letters of φ)
L16     mark b as a base
L17     for each child of φ on a letter c do
L18         char[b + code(c)] ← c; out[b + code(c)] ← the value of the child, if any
L19         queue the child if it has children
L20     link[the slot of φ in its parent] ← b  (or β0 ← b for the root)
```

**Lookup** (lines L1 to L8). One step reads one slot and compares one letter, so `get(x)` takes $O(|x|)$ time. Line L2 is the ownership test: if the letter matches, the slot belongs to the current family, by (I1). `prefix_values` is the same walk, and it reports $\mathrm{out}[s]$ at each step where it is not nil.

**Build** (lines L9 to L20). Line L11 accepts a base when no other family uses it and all the slots the family needs are free. Slots past the end of the table count as free, and the table grows. A plain scan from 0, as here, costs $O(S \sigma)$ per family in the worst case, so $O(F S \sigma)$ in all. Faster builds keep a list of the free slots and try only the bases that put the first letter of the family on a free slot. First fit is a heuristic: it does not promise the smallest table.

## Example

Pack the nine patterns of TeXbook Appendix H as keys: hyph, hen, hena, henat, na, nat, tio, io and on. The letters are a, e, h, i, n, o, p, t, y with codes 1 to 9. The trie has 13 families and 18 transitions. In breadth-first order, first fit places them as follows:

| family | letters (codes) | base | slots used |
|---|---|---|---|
| root | h i n o t (3 4 5 6 8) | 0 | 3 4 5 6 8 |
| h | e y (2 9) | 5 | 7 14 |
| i | o (6) | 3 | 9 |
| n | a (1) | 1 | 2 |
| o | n (5) | 6 | 11 |
| t | i (4) | 8 | 12 |
| he | n (5) | 10 | 15 |
| hy | p (7) | 9 | 16 |
| na | t (8) | 2 | 10 |
| ti | o (6) | 7 | 13 |
| hen | a (1) | 16 | 17 |
| hyp | h (3) | 15 | 18 |
| hena | t (8) | 11 | 19 |

For the family "h", the bases 0 to 4 fail: base 0 is taken, and the bases 1 to 4 put e on one of the full slots 3 to 6. Base 5 puts e on slot 7 and y on slot 14, both free. The family "hen" needs one slot only, but every base from 0 to 15 is taken or puts a on a full slot, so it goes to 16. The table has 20 slots, of which 18 hold a transition (slots 0 and 1 stay empty), so the density is 0.9. An unpacked indexed trie needs $13 \times 9 = 117$ slots.

Two lookups:

- `get("hen")`: from base 0, h is slot 3 (char h, link 5); e is slot $5 + 2 = 7$ (char e, link 10); n is slot $10 + 5 = 15$ (char n, out he2n). Found.
- `get("ho")`: h is slot 3, link 5; o is slot $5 + 6 = 11$, which holds n, the transition of the family "o". The letter does not match, so "ho" is not a prefix of any key.

## Correctness

The build keeps (I1) to (I3): FIRST-FIT returns a base that is free and whose slots are free, line L16 marks the base, and lines L17 to L20 fill only those slots and the link of the parent. For the lookup: if the current family $\phi$ has a child on $c$, slot $\beta(\phi) + \mathrm{code}(c)$ holds $c$ by (I3). If it has none but the slot holds $c$, the slot belongs to a family $\psi$ with $\beta(\psi) + \mathrm{code}(c) = \beta(\phi) + \mathrm{code}(c)$, so $\beta(\psi) = \beta(\phi)$ and $\psi = \phi$ by (I1), a contradiction. So line L2 accepts exactly the transitions of the current family, and by induction on the letters `get` follows the path of $x$ in the trie. The full proof is in the proof file.

## Complexity

| operation | time | notes |
|---|---|---|
| `get(x)` | $O(\lvert x \rvert)$ worst | one slot and one comparison per letter |
| `prefix_values(t, i)` | $O(\text{depth})$ worst | stops when the walk leaves the trie |
| `build(D)` with the plain scan | $O(F S \sigma)$ worst | plus the trie build, $O(\sum \lvert x \rvert)$ |
| space | $\Theta(S)$ | $S \le F(\sigma + 1)$ |

The bound on $S$ holds because the base equal to the current table length is always free, so each family adds at most $\sigma + 1$ slots. This bound is no better than the unpacked trie. The real gain is a measurement. In Liang's Table 1, the suffix-compressed trie of his pocket dictionary list of 31,036 words has 38,619 nodes, and the packed table has 38,638 slots, so almost no slot is wasted. The TeX82 patterns pack into 5943 locations. On the random set of 1000 keys in the tests of this page, the density is 0.975. Tarjan and Yao prove a bound for a related method: if the families are packed in decreasing order of size and the number $n(l)$ of transitions in families with more than $l$ transitions satisfies $n(l) \le n/(l+1)$ (harmonic decay), every base is less than the total number $n$ of transitions.

## Variants

- **Suffix compression.** Merge equal subtries before packing. For an acyclic machine this is state minimization ([DFA minimization](/dfa-minimization/)). TeX82 packs a suffix-compressed trie, so families are shared.
- **Dynamic packed trie.** Liang's pattern generator must insert patterns while it counts, so it uses a packed trie that supports insertion. A family that gets a new letter whose slot is full must move to a new base where all its slots fit.
- **First fit decreasing.** Pack the large families first; this is the method of the theorem of Tarjan and Yao. See [first fit decreasing](/first-fit-decreasing/) for the same idea in bin packing.
- **Double-array trie.** The [double-array trie](/double-array-trie/) also packs nodes by displacement, but it stores for each slot the index of the parent node (the check array), keeps separate base and check arrays, and supports insertion by moving siblings. Liang's version stores the letter, which needs fewer bits, uses one table, and is static.
- **Succinct tries.** A [LOUDS trie](/louds-trie/) uses about two bits per node plus the letters, but each step needs rank and select operations.

## When to use it

Use a packed trie for a static set of strings that is searched very often, when the alphabet is small and memory is tight, as for the hyphenation patterns in TeX. A [hash table](/hash-table/) is simpler for exact lookup, but it does not give the prefix walk. A [ternary search tree](/ternary-search-tree/) or a list of children per node supports changes but makes each step slower. When keys change often, use a [double-array trie](/double-array-trie/), which supports insertion.

## Pitfalls

- **Two families on one base.** If line L11 does not check that the base is free, two families with disjoint letters can share a base, and a lookup from one accepts the letters of the other: the stored letter matches, but it is not a transition of the current family.
- **No stored letter.** Without the test $\mathrm{char}[s] = c$ in line L2, a lookup reads any full slot as its own. The test `test_no_slot_is_shared_and_lookups_never_cross_families` checks both rules.
- **The end of the table.** Slots past the end count as free in the build but must fail in the lookup; line L2 checks $s < S$.
- **Changes after suffix compression.** A shared family has several parents, so a change made for one key changes the others too.
- **Expecting the best packing.** First fit depends on the order of the families, and another order can give a smaller or a larger table. Measure the density on real data.

## Implementations

## History

Liang described the packed trie in Chapter 2 of his 1983 thesis. He wrote that the first-fit method was inspired by the paper "Storing a sparse table" of Tarjan and Yao (1979), and that storing the letter with each transition seemed to be new. TeX82 keeps its hyphenation patterns in a packed trie, and the format file stores the packed table.

## References
