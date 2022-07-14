use serde::Deserialize;
#[derive(Debug, Deserialize)]
pub struct MarketProfile<T> {
    pub time_interval: (u64, u64), // über Konstruktur initailisieren. Der Konstruktor nimmt "%Y-%m-%d %H:%M:%S"
    pub period_length: u32,        // wir nehmen eine Woche (überlegen wie man das kodiert)
    pub depth: Vec<T>,
}