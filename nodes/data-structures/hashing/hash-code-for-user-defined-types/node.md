---
tag: QBFHDJ
kind: technique
slug: hash-code-for-user-defined-types
name: Hash code for user-defined types
aliases: [hashCode, __hash__, hash combining, hash_combine]
area: data-structures/hashing
level: intro
summary: Method for computing hash codes for custom objects by combining the hashes of their fields, usually with a multiplier such as 31.
prereqs: [hash-function, hash-table, hash-collision]
see_also: [polynomial-rolling-hash, hash-consing, zobrist-hashing, fnv-hash, murmurhash, equivalence-relation, algorithmic-complexity-attack, universal-hashing]
sources:
  - book: isbn:9780134685991
    title: Joshua Bloch, Effective Java, third edition, Addison-Wesley, 2018
    locator: Item 11, Always override hashCode when you override equals
  - url: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html
    title: Java SE 21 API, class java.lang.Object
    locator: the methods hashCode and equals (the general contract)
  - url: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html
    title: Java SE 21 API, interface java.util.List
    locator: the method hashCode (the formula 31 * hashCode + element hash, from 1)
  - url: https://docs.python.org/3/reference/datamodel.html
    title: The Python Language Reference, Data model
    locator: Section 3.3.1, Basic customization, object.__hash__
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4, Hash Tables (hashing user-defined types)
---

A hash code for a user-defined type is an integer computed from the fields of an object, so that the object can be a key of a [hash table](/hash-table/). The usual method starts from a constant and, for each field that takes part in equality, multiplies the running value by a small odd number such as 31 and adds the hash of the field. The one hard rule is that two equal objects must have equal hash codes; a good spread of values for unequal objects is a quality goal, not a rule. Java's `List.hashCode`, `Objects.hash` and `String.hashCode` use this method, and Python's advice is to hash a tuple of the fields.

## In plain words

A hash table puts each key into a bucket by its hash code. For numbers and strings, the language already knows how to make this code. For your own type, such as a point or a date, you must write it.

The idea is to mix the codes of the parts. Take the parts that decide if two objects are the same, in a fixed order. Start with a fixed number. For each part, multiply what you have by a small odd number and add the code of the part. The result changes when any part changes, and it changes in a different way for each position, so swapped parts do not give the same code.

The rule you must never break: if two objects are equal, their codes must be equal. Otherwise the table looks in the wrong bucket and misses a key that is there.

## When it applies

- You define a type whose objects are compared by value, not by identity, and you want to use them as keys of a [dictionary](/dictionary/) or members of a hash set.
- The type has an equality method, and equality depends on a fixed list of fields. The hash code must use the same fields, or a subset of them.
- The fields do not change while the object is in a table. If a field can change, either leave it out of both equality and hash, or do not change the object while it is a key.
- The keys come from friendly sources. If an attacker picks the keys, an unseeded combination of this kind is open to an [algorithmic complexity attack](/algorithmic-complexity-attack/); see the variations below.

## The template

```pseudo id=main
HASH-RECORD(x)
L1  h ← c                                        ▷ hole: the start value, a nonzero constant such as 1 or 17
L2  for each field f of x that EQUALS uses, in a fixed order   ▷ hole: the list of fields
L3      v ← FIELD-HASH(x.f)                        ▷ hole: the hash of one field
L4      h ← (a · h + v) mod 2^w                    ▷ hole: the multiplier a, odd, such as 31
L5  return FINISH(h)                             ▷ hole: an optional final mix, often the identity
```

Line L2 decides correctness. If EQUALS$(x, y)$ is true, then each field in the list has equal values in $x$ and $y$, so each FIELD-HASH on line L3 gives equal results, and the loop computes the same $h$ for both. This holds for any choice of $c$, $a$, $w$ and FINISH, so the other holes only change the quality of the spread.

Line L3 uses the hash of the field type: the value itself for a small integer, the language's hash for a string, 0 for a null field, and a recursive HASH-RECORD for a nested record. For an array or a list field, use a hash of all its elements in order, not the hash of the reference, if equality compares the elements.

Line L4 is a polynomial in $a$. With fields $v_1, \ldots, v_k$, the result is

$$h = c \cdot a^k + v_1 a^{k-1} + v_2 a^{k-2} + \cdots + v_k \pmod{2^w}.$$

An odd $a$ is invertible modulo $2^w$, so for fixed other fields, distinct values of one field modulo $2^w$ give distinct $h$, and no information is lost at that step. Different positions get different powers of $a$, so swapping two fields usually changes $h$. A nonzero $c$ makes leading fields equal to zero still count, because they change the power that multiplies $c$. The multiplier 31 is the classic choice because it is an odd prime and $31 h = 32 h - h$ is a shift and a subtraction.

## Classic examples

- **A point.** For a point with integer fields $x$ and $y$, $c = 1$ and $a = 31$, the code is $31 (31 + x) + y$. For the point $(1, 2)$ it is $31 \cdot 32 + 2 = 994$, and the point $(2, 1)$ gets $31 \cdot 33 + 1 = 1024$.
- **Java strings.** `String.hashCode` is the template with $c = 0$, $a = 31$, $w = 32$ and the character codes as fields. The string `ab` gets $97 \cdot 31 + 98 = 3105$. The same sum read as a polynomial is the [polynomial rolling hash](/polynomial-rolling-hash/), which a sliding window can update in $O(1)$.
- **Java lists and `Objects.hash`.** `List.hashCode` is the template with $c = 1$, $a = 31$ and the element hashes, with 0 for a null element. `Objects.hash(x, y, z)` gives the same value as the list of its arguments, so it is a one-line hash code for a class with these fields.
- **Python tuples.** The Python data model advises that `__hash__` return `hash((self.x, self.y))`, a hash of a tuple of the fields that `__eq__` compares. The tuple hash of CPython is a version of the template with a strong mix in place of 31.
- **[Hash consing](/hash-consing/).** A table of unique tree nodes hashes a node from its label and the hash codes of its children, which is the template with one recursive call per child.
- **[Zobrist hashing](/zobrist-hashing/).** A board position is a record with one field per square. Zobrist hashing uses $h = \bigoplus_i R[i][v_i]$ with a random table $R$ instead of line L4, so that a change of one square updates the code in $O(1)$. The random table prevents the symmetry problems of a plain XOR.

## Variations

- **Sum or XOR of the field hashes.** These are correct, but they are symmetric: the points $(1, 2)$ and $(2, 1)$ collide, and with XOR every point $(x, x)$ gets 0. On the $10\,000$ points with $0 \le x, y < 100$, XOR gives 128 distinct codes and the sum gives 199. Use them only when the order of the fields should not matter, as for the hash of a set.
- **Larger odd multiplier.** With $a = 31$ and $c = 1$ the same grid gives only 3169 distinct codes, because $31 x + y$ overlaps when $y$ ranges over more than 31 values; for example $(0, 31)$ and $(1, 0)$ both get 992. A 64-bit odd multiplier such as `0x9E3779B97F4A7C15` gives all $10\,000$ codes distinct on this grid.
- **A final mix.** Tables with $2^p$ buckets often use the low $p$ bits of the code. If the fields are small, these low bits depend only on the last fields. A FINISH step that mixes high bits into low bits, such as a multiply and shift, fixes this. Java's `HashMap` does a small mix of this kind on each key's code.
- **Other combiners.** Boost's `hash_combine` uses $h \leftarrow h \oplus (v + \texttt{0x9e3779b9} + (h \ll 6) + (h \gg 2))$. Byte-oriented hashes such as [FNV](/fnv-hash/) or [MurmurHash](/murmurhash/) can hash a fixed binary encoding of all the fields at once.
- **Seeded combining.** If the keys may come from an attacker, start from a secret random seed and use a keyed function such as [SipHash](/siphash/) over an encoding of the fields. A secret $c$ alone is not enough for the template with $a = 31$, because collisions such as `Aa` and `BB` do not depend on $c$.
- **Cached hash codes.** An immutable object can compute its code once and store it, as Java's `String` does. This is safe only if no field that the code uses can change.

## Pitfalls

- **Equality and hash that disagree.** If you override equality and not the hash, two equal objects can get the identity hash of the default and land in different buckets, so a search for an equal key fails. The reverse also breaks: a hash that uses a field that equality ignores gives equal objects different codes. In Python, a class that defines `__eq__` and not `__hash__` gets `__hash__ = None`, so its objects cannot be keys at all.
- **Mutable fields.** If a field that the hash uses changes while the object is in a table, the object stays in the bucket of its old code. The table can then not find it, and it can hold two equal keys.
- **Floating point fields.** Equality and hash must agree on the special values: in Java, `Double.equals` treats `0.0` and `-0.0` as different and all NaN values as equal, which differs from `==`. Hash the same bit pattern that equality compares.
- **Fields that cancel.** Java's `Long.hashCode` is the XOR of the high and low 32 bits, so the value $2^{32} + 1$ hashes to 0, as does every long whose two halves are equal. Combining such fields with XOR makes this worse.
- **The value -1 in Python.** CPython uses $-1$ as an error code, so a `__hash__` that returns $-1$ is changed to $-2$. Then $\text{hash}(-1) = \text{hash}(-2)$, and code that expects all small integers to have distinct hashes is wrong for these two.
- **Expensive hashes.** A code that walks a deep structure on each call makes each table operation slow. Cache it for immutable objects, or hash only a few fields that already spread the keys well, as long as equality uses all of them.
- **Collisions on purpose.** An unseeded combination is easy to invert, so an attacker can make many keys with one code. See [algorithmic complexity attack](/algorithmic-complexity-attack/).

## Exercises

1. Show that for $c = 1$, $a = 31$ and two integer fields, the points $(x, y)$ and $(x + 1, y - 31)$ always collide. Give a pair of fields for which the sum combiner collides but the template does not.
2. A class `Interval` has fields `lo` and `hi`, and two intervals are equal when both fields are equal. Write its hash code with the template. Then change equality so that the empty intervals, those with `lo > hi`, are all equal, and fix the hash code so that the rule still holds.
3. Prove that for odd $a$, the map $h \mapsto a h + v \bmod 2^w$ is a bijection of $\{0, \ldots, 2^w - 1\}$ for each fixed $v$.
4. Find two distinct strings of length 4 with the same Java `String.hashCode`, using the blocks `Aa` and `BB`.

## References
