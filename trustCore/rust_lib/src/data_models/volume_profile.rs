use serde::Deserialize;
#[derive(Debug, Deserialize)]
struct VolumeProfileCsvRecord {
    price: f32,
    volume: f32,
}

#[derive(Debug, Deserialize)]
struct VolumeProfile {
    time_interval: (u64, u64),
    poc: f32,
    vol_area_low: f32,
    vol_area_high: f32,
    records: Vec<VolumeProfileCsvRecord>,
}