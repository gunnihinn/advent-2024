use std::str::FromStr;
use regex::Regex;

#[derive(Debug)]
enum Item{
    Mul(i64, i64),
    Do,
    Dont
}

fn parse(stdin: std::io::Stdin) -> Vec<Vec<Item>> {
    let re = Regex::new(r"don't|do|mul\((\d+),(\d+)\)").unwrap();
    let mut data: Vec<Vec<Item>> = vec![];

    for line in stdin.lines() {
        let mut pairs: Vec<Item> = vec![];
        for cap in re.captures_iter(&line.unwrap()) {
            let m = cap.get(0).unwrap().as_str();
            let item = match m {
                "do" => Item::Do,
                "don't" => Item::Dont,
                _ => {
                    let a = cap.get(1).unwrap().as_str();
                    let b = cap.get(2).unwrap().as_str();
                    Item::Mul(i64::from_str(a).unwrap(), i64::from_str(b).unwrap())
                },
            };
            pairs.push(item)
        }
        data.push(pairs);
    }

    data
}

fn part1(data: &Vec<Vec<Item>>) -> i64 {
    let pairs = data.iter().flatten();
    pairs.fold(0, |acc, item| { 
        acc + match item{
            Item::Mul(a, b) => a * b,
            _ => 0,
        }
    })
}

fn part2(data: &Vec<Vec<Item>>) -> i64 {
    let mut sum = 0;

    let mut _do = true;
    let items = data.iter().flatten();
    for item in items {
        match item {
            Item::Do => _do = true,
            Item::Dont => _do = false,
            Item::Mul(a, b) => {
                if _do {
                    sum += a * b;
                }
            },
        }
    }

    sum
}

fn main() {
    let data = parse(std::io::stdin());

    let p1 = part1(&data);
    println!("part1={p1}");

    let p2 = part2(&data);
    println!("part2={p2}");
}
