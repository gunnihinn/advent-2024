use std::str::FromStr;

fn parse(stdin: std::io::Stdin) -> Vec<Vec<u64>> {
    let mut reports: Vec<Vec<u64>> = vec![];

    for line in stdin.lines() {
        reports.push(line.unwrap().split_whitespace().map(|d| u64::from_str(d).unwrap()).collect());
    }

    return reports;
}

fn part1(reports: Vec<Vec<u64>>) -> u64 {
    return 0
}

fn main() {
    let data = parse(std::io::stdin());
    println!("data: {data:#?}")
}
