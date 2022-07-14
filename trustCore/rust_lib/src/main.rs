/**
 * Links:
 *  - https://doc.rust-lang.org/book/ch10-00-generics.html
 *  - https://rust-lang.github.io/api-guidelines/checklist.html
 *  - https://doc.rust-lang.org/rust-by-example/primitives/array.html
 */

use std::error::Error;
use std::process;

use chrono::prelude::*;

mod data_models;
pub use crate::data_models::ohlc;

fn example() -> Result<Vec<ohlc::OhlcCsvRecord>, Box<dyn Error>> {
    let mut records: Vec<ohlc::OhlcCsvRecord> = Vec::new();
    // let mut rdr = csv::ReaderBuilder::new().from_path("./td1.csv")?;
    let mut rdr = csv::ReaderBuilder::new().from_path("./BTCUSDT-1h-2022-07-11.csv")?;
    for result in rdr.deserialize() {
        let record: ohlc::OhlcCsvRecord = result?;
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
    let utc: DateTime<Local> = Local::now();
    let ts = utc.timestamp_millis();
    match Utc.datetime_from_str("2022-07-01 00:00:00", "%Y-%m-%d %H:%M:%S") {
        Ok(v) => println!("{:?}", v.timestamp()),
        Err(e) => println!("error")
    }
    println!("{:?} {:?}", utc.format("%Y-%m-%d %H:%M:%S").to_string(), ts);
    
}