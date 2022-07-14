pub mod market_profile;
pub mod ohlc;
pub mod profit_and_loss;
pub mod volume_profile;

use std::error::Error;

pub trait Csv<T> {
    fn read_from_path(
        &self,
        path: String,
    ) -> Result<Vec<market_profile::MarketProfile<T>>, Box<dyn Error>>;

    fn write_to_path(
        &self,
        path: String,
    ) -> Result<(), Box<dyn Error>>;
}

impl Csv<ohlc::OhlcData> for ohlc::OhlcData {
    fn read_from_path(
        &self,
        path: String,
    ) -> Result<Vec<market_profile::MarketProfile<ohlc::OhlcData>>, Box<dyn Error>>
    {
        let m = market_profile::MarketProfile::<ohlc::OhlcData> {
            time_interval: (0, 0),
            period_length: 0,
            depth: Vec::new(),
        };
        let mut vec: Vec<market_profile::MarketProfile<ohlc::OhlcData>> = Vec::new();
        vec.push(m);
        Ok(vec)
    }

    fn write_to_path(
        &self,
        path: String,
    ) -> Result<(), Box<dyn Error>>
    {
        Ok(())
    }
}
