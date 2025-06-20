use std::str::FromStr;
use std::iter::zip;

fn parse(stdin: std::io::Stdin) -> Vec<Vec<u64>> {
    let mut reports: Vec<Vec<u64>> = vec![];

    for line in stdin.lines() {
        reports.push(line.unwrap().split_whitespace().map(|d| u64::from_str(d).unwrap()).collect());
    }

    return reports;
}

fn safe(report: &Vec<u64>) -> bool {
    let inc = zip(report.iter(), report.iter().skip(1))
        .filter(|(a,b)| a <= b )
        .count();
    let monotone = inc == 0 || inc == report.len() - 1;

    monotone && 
    zip(report.iter(), report.iter().skip(1))
        .all(|(a,b)| 1 <= a.abs_diff(*b) && a.abs_diff(*b) <= 3)
}

fn part1(reports: Vec<Vec<u64>>) -> usize {
    reports.iter().filter(|rep| {
        safe(rep)
    }).count()
}

fn tolerate(report: &Vec<u64>) -> bool {
    report.iter().enumerate().map(|(i, _)| {
        let tmp: Vec<u64> = report.iter().enumerate().filter(|(j, _)| *j != i).map(|(_, val)| *val).collect();
        safe(&tmp)
    }).any(|x| x)
}

fn part2(reports: Vec<Vec<u64>>) -> usize {
    reports.iter().filter(|rep| {
        tolerate(rep)
    }).count()
}

fn main() {
    let data = parse(std::io::stdin());

    let res1 = part1(data.clone());
    println!("part1: {res1:#?}");

    let res2 = part2(data);
    println!("part2: {res2:#?}");
}
