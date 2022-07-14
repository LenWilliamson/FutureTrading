use serde::Deserialize;
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
    time_interval: (u64, u64),
    records: Vec<OhlcCsvRecord>,
}