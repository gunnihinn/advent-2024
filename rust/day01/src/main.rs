use std::collections::HashMap;

fn parse(stdin: std::io::Stdin) -> (Vec<u64>, Vec<u64>) {
    let mut fst: Vec<u64> = vec![];
    let mut snd: Vec<u64> = vec![];

    for line in stdin.lines() {
        let s = line.unwrap();
        let mut it = s.split_whitespace();
        fst.push(u64::from_str_radix(it.next().unwrap(), 10).unwrap());
        snd.push(u64::from_str_radix(it.next().unwrap(), 10).unwrap());
    }

    return (fst, snd);
}

fn part1(data: (Vec<u64>, Vec<u64>)) -> u64 {
    let (mut fst, mut snd) = data;
    fst.sort();
    snd.sort();

    return std::iter::zip(fst, snd).map(|(a,b)| a.abs_diff(b) ).sum()
}

fn part2(data: (Vec<u64>, Vec<u64>)) -> u64 {
    let (fst, snd) = data;

    let mut counts: HashMap<u64, u64> = HashMap::new();
    for n in snd {
        *counts.entry(n).or_insert(0) += 1
    }

    return fst.into_iter().map(|a| a * *counts.entry(a).or_default()).sum()
}

fn main() {
    let data = parse(std::io::stdin());

    let p1 = part1(data.clone());
    let p2 = part2(data.clone());
    println!("part1={p1}");
    println!("part2={p2}");
}
