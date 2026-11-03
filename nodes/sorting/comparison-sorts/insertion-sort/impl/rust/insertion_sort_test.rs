// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

use algo_insertion_sort::insertion_sort;

#[test]
fn example() {
    let mut a = [5, 2, 4, 6, 1, 3];
    insertion_sort(&mut a);
    assert_eq!(a, [1, 2, 3, 4, 5, 6]);
}

#[test]
fn edges() {
    let mut e: [i32; 0] = [];
    insertion_sort(&mut e);
    let mut a = [3, 2, 1, 1];
    insertion_sort(&mut a);
    assert_eq!(a, [1, 1, 2, 3]);
}

#[test]
fn random_against_std() {
    let mut s: u64 = 2150;
    let mut next = |m: u64| {
        s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (s >> 33) % m
    };
    for _ in 0..500 {
        let n = next(41) as usize;
        let a: Vec<i64> = (0..n).map(|_| next(101) as i64 - 50).collect();
        let mut b = a.clone();
        let mut want = a.clone();
        insertion_sort(&mut b);
        want.sort();
        assert_eq!(b, want);
    }
}
