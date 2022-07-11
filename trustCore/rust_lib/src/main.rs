/**
 * Links:
 *  - https://doc.rust-lang.org/book/ch10-00-generics.html
 *  - https://rust-lang.github.io/api-guidelines/checklist.html
 *  - https://doc.rust-lang.org/rust-by-example/primitives/array.html
 */

use std::error::Error;
use std::io;
use std::process;
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct AggTrade {
    atid: u64, // AggTradeId
    px: f32, //'Price'
    qx: f32, // 'Quantity'
    ftid: u64, // 'FirstTradeId',
    ltid: u64, // 'LastTradeId',
    ts: u64, // 'Timestamp',
    bm: bool, // 'Buyer=Maker',
    btpm: bool, // 'BestTradPriceMatch'
}

fn example() -> Result<Vec<AggTrade>, Box<dyn Error>> {
    let mut records: Vec<AggTrade> = Vec::new();
    let mut rdr = csv::ReaderBuilder::new().from_path("./td1.csv")?;
    for result in rdr.deserialize() {
        let record: AggTrade = result?;
        records.push(record);
    }
    Ok(records)
}

fn main() {
    match example() {
        Ok(v) => println!("recors size = {:?}: {:?}", v.len(), v),
        Err(e) => {
            println!("error running example: {}", e);
            process::exit(1);
        }
    }
}