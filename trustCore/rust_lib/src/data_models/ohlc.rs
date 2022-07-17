use serde::Deserialize;
use std::error::Error;

#[allow(dead_code)]
#[derive(Debug, Deserialize)]
pub struct OhlcCsvRecord {
    ots: u64,    // OpenTime
    open: f32,   // Open
    high: f32,   // High
    low: f32,    // Low
    close: f32,  // Close
    vol: f32,    // Volume
    cts: u64,    // CloseTime
    qav: f32,    // QuoteAssetVol
    not: u32,    // NumberOfTrades
    tbbav: f32,  //  TakerBuyBaseAssetVol
    tbqav: f32,  //  TakerBuyQuoteAssetVol
    ignore: i32, // Ignore
}
#[derive(Debug, Deserialize)]
pub struct OhlcData {
    pub time_interval: (u64, u64),
    pub records: Vec<OhlcCsvRecord>,
}

impl OhlcData {
    pub fn read_from_path(path: &str) -> Result<OhlcData, Box<dyn Error>> {
        let mut ohlc_data = OhlcData {
            time_interval: (0, 0),
            records: Vec::new(),
        };

        let mut rdr = csv::ReaderBuilder::new().from_path(path)?;
        for result in rdr.deserialize() {
            let record: OhlcCsvRecord = result?;
            ohlc_data.records.push(record);
        }
        Ok(ohlc_data)
    }
}
