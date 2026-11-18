---
tag: GBVPJX
kind: definition
slug: unicode-code-point
name: Unicode code point
aliases:
- Unicode scalar value
area: strings/text-processing-and-typesetting
level: intro
summary: "An integer in the Unicode codespace 0 to 10FFFF. Only some code points are assigned to characters, and the scalar values are all code points except the surrogates D800 to DFFF."
prereqs: [alphabet]
see_also: [utf-8, utf-16, extended-grapheme-cluster, canonical-equivalence, unicode-normalization-forms, unicode-case-folding, alphabet, variable-length-code]
sources:
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: "Chapter 3: Section 3.4 Characters and Encoding (D7 abstract character, D9 codespace, D10 code point, D10a code point type, D11 encoded character, D14 noncharacter, D15 reserved code point), Section 3.8 Surrogates (D71, D73) and Section 3.9 (D76 Unicode scalar value, D77 code unit)"
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: Chapter 23, Section 23.6 Surrogates Area and Section 23.7 Noncharacters
  - url: https://www.unicode.org/versions/Unicode16.0.0/core-spec/
    title: The Unicode Standard, Version 16.0.0, core specification (online)
    locator: Chapter 3, Sections 3.4, 3.8 and 3.9
  - url: https://docs.python.org/3/library/unicodedata.html
    title: Python documentation, unicodedata
    locator: unicodedata.category and unicodedata.unidata_version
---

A Unicode code point is an integer in the range 0 to 10FFFF (hexadecimal), the codespace of the Unicode Standard. Unicode gives each character it encodes one code point, and a string of text is, at this level, a sequence of code points over this [alphabet](/alphabet/) of 1,114,112 values. Only some code points are assigned to characters: most of the codespace is reserved for the future, and some parts can never hold a character. The code points that an encoding form such as [UTF-8](/utf-8/) or [UTF-16](/utf-16/) can represent are the scalar values, which are all code points except the 2,048 surrogates.

## Definition

The definitions below are from chapter 3 of the core specification of Unicode 16.0.0.

**Codespace (D9).** The range of integers from 0 to 10FFFF.

**Code point (D10).** Any value in the codespace. It is written "U+" followed by at least four hexadecimal digits, for example U+0041 or U+1F600. A range is written U+D800..U+DFFF.

The codespace has 17 *planes* of 65,536 code points each. Plane 0, U+0000..U+FFFF, is the Basic Multilingual Plane (BMP). Planes 1 to 16 are the supplementary planes.

**Code point type (D10a).** Each code point has exactly one of seven types. A reserved code point can be assigned in a later version, so the type can change from one version to the next. The general category of the Unicode Character Database tells the types apart.

| type | general category | count in Unicode 16.0.0 |
|---|---|---|
| graphic, format and control | all categories except Cs, Co and Cn | 155,063 |
| private-use | Co | 137,468 |
| surrogate | Cs | 2,048 |
| noncharacter | Cn | 66 |
| reserved | Cn | 819,467 |

The first row joins three types. The 65 control characters (Cc) are U+0000..U+001F and U+007F..U+009F, so the graphic and format characters number 154,998, which is the count of characters that Unicode 16.0.0 reports. The counts come from Python's `unicodedata`, whose data version is 16.0.0 in Python 3.14, and they add up to 1,114,112.

**Surrogate code point (D71, D73).** A code point in U+D800..U+DFFF. The 1,024 high-surrogate code points are U+D800..U+DBFF and the 1,024 low-surrogate code points are U+DC00..U+DFFF. They are reserved for the pairs of UTF-16 and are never assigned to characters.

**Unicode scalar value (D76).** A code point that is not a surrogate: U+0000..U+D7FF or U+E000..U+10FFFF. There are $1{,}114{,}112 - 2{,}048 = 1{,}112{,}064$ of them. UTF-8, UTF-16 and UTF-32 encode exactly the scalar values, so a well-formed string in any of them is a sequence of scalar values.

**Noncharacter (D14).** One of 66 code points that are set aside for internal use and will never be assigned: U+FDD0..U+FDEF and the last two code points of each plane, U+FFFE, U+FFFF, U+1FFFE, U+1FFFF and so on up to U+10FFFF. Section 23.7 says that they are not prohibited in interchange: they are scalar values, and the encoding forms encode them like any other.

**Reserved code point (D15).** A code point that the standard has not yet assigned and that is not a surrogate or a noncharacter.

**Encoded character (D11).** The pair of a code point and the abstract character (D7) assigned to it. A character has a name written in capitals, for example U+00E9 LATIN SMALL LETTER E WITH ACUTE.

## Examples and non-examples

- U+0041 LATIN CAPITAL LETTER A is a code point, a scalar value and an assigned graphic character. In UTF-8 it is the byte 41.
- U+20AC EURO SIGN is one code point. It is the three bytes E2 82 AC in UTF-8 and the one code unit 20AC in UTF-16. A code point is not a byte and not a code unit (D77).
- U+1F600 GRINNING FACE is in plane 1. It is the four bytes F0 9F 98 80 in UTF-8 and the two UTF-16 code units D83D DE00, so a language that counts UTF-16 units, such as Java or JavaScript, gives it the length 2.
- U+D800 is a code point but not a scalar value. No well-formed string in a Unicode encoding form contains it. A Python `str` can still hold it, as `"\ud800"`, and `"\ud800".encode("utf-8")` raises an error.
- U+E000 is the first private-use code point. It is a scalar value with no meaning defined by Unicode, and parties may agree on a meaning for it.
- U+FFFE is a noncharacter. It is a scalar value, and UTF-8 encodes it as EF BF BE.
- U+0378 is reserved in Unicode 16.0.0. A later version may assign it, so a program must not treat it as forbidden.
- The integer 110000 (hexadecimal) is not a code point. It is outside the codespace, and Python's `chr(0x110000)` raises an error.
- The letter é can be one code point, U+00E9, or two, U+0065 U+0301. The two strings show the same text: they are [canonically equivalent](/canonical-equivalence/). So a code point is not the same as a character that a reader sees, which is an [extended grapheme cluster](/extended-grapheme-cluster/).

## Related definitions

- **Code unit (D77).** The unit of storage of an encoding form: 8 bits in UTF-8, 16 bits in UTF-16 and 32 bits in UTF-32. A code point takes 1 to 4 code units in UTF-8, 1 or 2 in UTF-16, and always 1 in UTF-32.
- **Encoding form.** A map from scalar values to code unit sequences: [UTF-8](/utf-8/), [UTF-16](/utf-16/) and UTF-32. UTF-8 and UTF-16 are [variable-length codes](/variable-length-code/).
- **Grapheme cluster.** A sequence of code points that a reader sees as one character. See [extended grapheme cluster](/extended-grapheme-cluster/).
- **Normalization form.** A choice of one sequence of code points among the sequences that show the same text. See [Unicode normalization forms](/unicode-normalization-forms/).
- **Alphabet.** In the theory of strings, a finite set of symbols. For Unicode text it is the set of scalar values. See [alphabet](/alphabet/).

## References
