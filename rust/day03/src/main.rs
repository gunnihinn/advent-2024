use std::str::FromStr;
use regex::Regex;

fn parse(stdin: std::io::Stdin) -> Vec<Vec<(i64, i64)>> {
    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    let mut data: Vec<Vec<(i64, i64)>> = vec![];

    for line in stdin.lines() {
        let mut pairs: Vec<(i64, i64)> = vec![];
        for (_, [a, b]) in re.captures_iter(&line.unwrap()).map(|c| c.extract()) {
            pairs.push((i64::from_str(a).unwrap(), i64::from_str(b).unwrap()));
        }
        data.push(pairs);
    }

    data
}

fn part1(data: &Vec<Vec<(i64, i64)>>) -> i64 {
    let pairs = data.iter().flatten();
    pairs.fold(0, |acc, (a, b)| acc + a * b)
}

fn main() {
    let data = parse(std::io::stdin());

    let p1 = part1(&data);
    println!("part1={p1}");
}
