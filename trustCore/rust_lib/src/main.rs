use chrono::prelude::*;
use std::process;
use substring::Substring;

mod data_models;
mod strategies;
pub use crate::data_models::*;
pub use crate::strategies::*;

static OFFSET: usize = "BTCUSDT-aggTrades-2000-01".len();
static TIME_STANDARD: usize = "YYYY-MM-DD_HH:MM:SS".len();
static SEPERATOR: usize = "__".len();


#[derive(Debug)]
struct TimeObject {
    start: String,
    start_ts: i64,
    end: String,
    end_ts: i64,
}

use chrono::format::ParseResult;
fn csv_file_name_decomposer(csv_file: &str) -> ParseResult<TimeObject> {
    let start = csv_file
        .substring(OFFSET + SEPERATOR, OFFSET + SEPERATOR + TIME_STANDARD)
        .to_string();
    let start_ts = Local
        .datetime_from_str(&start, "%Y-%m-%d_%H:%M:%S")?
        .timestamp();
    let end = csv_file
        .substring(
            OFFSET + SEPERATOR + TIME_STANDARD + SEPERATOR,
            OFFSET + SEPERATOR + TIME_STANDARD + SEPERATOR + TIME_STANDARD,
        )
        .to_string();
    let end_ts = Local
        .datetime_from_str(&end, "%Y-%m-%d_%H:%M:%S")?
        .timestamp();

    Ok(TimeObject {
        start,
        start_ts,
        end,
        end_ts,
    })
}

fn main() {
    match ohlc::OhlcData::read_from_path("./BTCUSDT-1h-2022-07-11.csv") {
        Ok(v) => println!("recors size = {:?}: {:?}", v.records.len(), v),
        Err(e) => {
            println!("error running example: {}", e);
            process::exit(1);
        }
    }

    match volume_profile::VolumeProfile::read_from_path("./BTCUSDT-aggTrades-2021-12__2021-12-25_00-00-00__2021-12-31_00-00-00.csv") {
        Ok(v) => println!("recors size = {:?}: {:?}", v.records.len(), v.poc),
        Err(e) => {
            println!("error running example: {}", e);
            process::exit(1);
        }
    }

    let s = "BTCUSDT-aggTrades-2000-01__2000-01-29_00:00:00__2000-02-01_00:00:00.csv";
    let x = csv_file_name_decomposer(s);
    println!("{:?}", x);

    strategies::weekly_poc::compute();
}
