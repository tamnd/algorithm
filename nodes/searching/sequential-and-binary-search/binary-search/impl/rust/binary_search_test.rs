// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

use algo_binary_search::binary_search;

#[test]
fn examples() {
    let a = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91];
    assert_eq!(binary_search(&a, &23), Some(5));
    assert_eq!(binary_search(&a, &2), Some(0));
    assert_eq!(binary_search(&a, &91), Some(9));
    assert_eq!(binary_search(&a, &30), None);
    assert_eq!(binary_search(&a, &1), None);
    assert_eq!(binary_search(&a, &100), None);
}

#[test]
fn edges() {
    let empty: [i32; 0] = [];
    assert_eq!(binary_search(&empty, &1), None);
    assert_eq!(binary_search(&[7], &7), Some(0));
    assert_eq!(binary_search(&["ant", "bee", "cat"], &"bee"), Some(1));
    let a = [1, 3, 3, 3, 5];
    assert_eq!(a[binary_search(&a, &3).unwrap()], 3);
}

#[test]
fn random_against_linear_scan() {
    // A small linear congruential generator, so that the test needs no crate.
    let mut s: u64 = 2150;
    let mut next = |m: u64| {
        s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (s >> 33) % m
    };
    for _ in 0..2000 {
        let n = next(31) as usize;
        let mut a: Vec<i64> = (0..n).map(|_| next(41) as i64 - 20).collect();
        a.sort();
        let x = next(51) as i64 - 25;
        match binary_search(&a, &x) {
            Some(i) => assert_eq!(a[i], x),
            None => assert!(!a.contains(&x)),
        }
    }
}
