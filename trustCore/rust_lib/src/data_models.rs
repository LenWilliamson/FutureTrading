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
