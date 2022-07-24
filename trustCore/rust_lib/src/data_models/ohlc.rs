use serde::Deserialize;
use std::error::Error;

#[allow(dead_code)]
#[derive(Debug, Deserialize)]
pub struct OhlcCsvRecord {
    pub ots: i64,    // OpenTime
    open: f32,   // Open
    pub high: f32,   // High
    pub low: f32,    // Low
    pub close: f32,  // Close
    vol: f32,    // Volume
    cts: i64,    // CloseTime
    qav: f32,    // QuoteAssetVol
    not: u32,    // NumberOfTrades
    tbbav: f32,  //  TakerBuyBaseAssetVol
    tbqav: f32,  //  TakerBuyQuoteAssetVol
    ignore: i32, // Ignore
}
#[derive(Debug, Deserialize)]
pub struct OhlcData {
    pub time_interval: (i64, i64),
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
        ohlc_data.time_interval = OhlcData::compute_time_interval(&ohlc_data.records);
        Ok(ohlc_data)
    }

    fn compute_time_interval(records: &Vec<OhlcCsvRecord>) -> (i64, i64) {
        (records.first().unwrap().ots, records.last().unwrap().cts)
    }
}
