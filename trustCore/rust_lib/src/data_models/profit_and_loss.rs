use serde::Deserialize;

#[allow(dead_code)]
#[derive(Debug, Deserialize)]
struct ProfitAndLossCsvRecord {
    ots: u64, // OpenTime
    cts: u64, // CloseTime
    sl1: f32, // Stop-Loss 1
    sl2: f32, // Stop-Loss 2
}

#[derive(Debug, Deserialize)]
struct ProfiAndLossData {
    time_interval: (u64, u64),
    strategy: String,
    records: Vec<ProfitAndLossCsvRecord>,
}