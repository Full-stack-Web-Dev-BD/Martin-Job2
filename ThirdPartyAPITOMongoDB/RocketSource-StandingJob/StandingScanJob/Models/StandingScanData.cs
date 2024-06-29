using System.Text.Json.Serialization;

namespace RocketSource.Models
{
    public class StandingScanData
    {
        [JsonPropertyName("asin")]
        public string ASIN { get; set; }
        //[JsonPropertyName("amazon_title")]
        //public string Amazon_Title { get; set; }
        [JsonPropertyName("brand")]
        public string Brand { get; set; }
        //[JsonPropertyName("buy_box_price")]
        //public double? BuyBoxPrice { get; set; }
        [JsonPropertyName("category")]
        public string Category { get; set; }
        //[JsonPropertyName("width")]
        //public double? Width { get; set; }

        //[JsonPropertyName("height")]
        //public double? Height { get; set; }

        //[JsonPropertyName("length")]
        //public double? Length { get; set; }
        //[JsonPropertyName("weight")]
        //public double? Weight { get; set; }
        //[JsonPropertyName("fba_fee")]
        //public double? FBAFee { get; set; }
        [JsonPropertyName("ean")]
        public List<string>? EAN { get; set; }
        [JsonPropertyName("datetime_stamp")]
        public DateTime Time_Datestamp{ get; set; }
    }
}
