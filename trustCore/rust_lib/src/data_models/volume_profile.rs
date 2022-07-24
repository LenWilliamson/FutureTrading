use serde::Deserialize;
use std::error::Error;
use ordered_float::OrderedFloat;

#[allow(dead_code)]
#[derive(Debug, Deserialize)]
pub struct VolumeProfileCsvRecord {
    price: f32,
    volume: f32,
}

#[derive(Debug, Deserialize)]
pub struct VolumeProfile {
    time_interval: (u64, u64),
    pub poc: f32,
    vol_area_low: f32,
    vol_area_high: f32,
    pub records: Vec<VolumeProfileCsvRecord>,
}

impl VolumeProfile {
    pub fn read_from_path(path: &str) -> Result<VolumeProfile, Box<dyn Error>> {
        let mut vol_data = VolumeProfile {
            time_interval: (0, 0),
            poc: 0.0,
            vol_area_low: 0.0,
            vol_area_high: 0.0,
            records: Vec::new(),
        };

        let mut rdr = csv::ReaderBuilder::new().from_path(path)?;
        for result in rdr.deserialize() {
            let record: VolumeProfileCsvRecord = result?;
            vol_data.records.push(record);
        }

        vol_data.poc = VolumeProfile::compute_poc(&vol_data.records);
        vol_data.vol_area_low = VolumeProfile::compute_vol_area_low(&vol_data.records);
        vol_data.vol_area_high = VolumeProfile::compute_vol_area_high(&vol_data.records);

        Ok(vol_data)
    }

    fn compute_poc(records: &Vec<VolumeProfileCsvRecord>) -> f32 {
        records.iter().max_by_key(|&x| OrderedFloat(x.volume)).unwrap().price
    }

    fn compute_vol_area_low(records: &Vec<VolumeProfileCsvRecord>) -> f32 {
        0.0
    }

    fn compute_vol_area_high(records: &Vec<VolumeProfileCsvRecord>) -> f32 {
        0.0
    }
}