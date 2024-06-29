using System.Text.Json.Serialization;

namespace RocketSource.Models
{
    public class USScanData
    {
        [JsonPropertyName("asin")]
        public string ASIN { get; set; }
        [JsonPropertyName("US_average_bsr_30")]
        public double? US_Average_BSR_30 { get; set; }
        [JsonPropertyName("US_average_bsr_90")]
        public double? US_Average_BSR_90 { get; set; }
        [JsonIgnore]
        private double? _usBSRPercentage;
        [JsonPropertyName("bsr_percentage")]
        public double? US_BSR_Percentage { get { return Math.Round((_usBSRPercentage ?? 0) / 100/100, 2); } set { _usBSRPercentage = value; } }

        [JsonIgnore] 
        private double? _usBuyBoxPrice;
        [JsonPropertyName("buy_box_price")]
        public double? US_Buybox_Price { get { return Math.Round((_usBuyBoxPrice ?? 0)/100, 2); } set { _usBuyBoxPrice = value; } }
        [JsonPropertyName("competitive_sellers_count")]
        public int? US_Competitive_Sellers { get; set; }
        private double? _usFBAFee { get; set; }
        [JsonPropertyName("fba_fees")]
        public double? US_FBA_Fees { get { return Math.Round((_usFBAFee ?? 0)/100, 2); } set { _usFBAFee = value; } }
        [JsonIgnore]
        private double? _usFBALowestPrice { get; set; }
        [JsonPropertyName("fba_lowest_price")]
        public double? US_Lowest_Price_FBA { get { return Math.Round((_usFBALowestPrice ?? 0) / 100, 2); } set { _usFBALowestPrice = value; } }
        [JsonIgnore]
        private double? _usFBMLowestPrice { get; set; }
        [JsonPropertyName("fbm_lowest_price")]
        public double? US_Lowest_Price_FBM { get { return Math.Round((_usFBMLowestPrice ?? 0) / 100, 2); } set { _usFBMLowestPrice = value; } }

        [JsonPropertyName("fbm_offers")]
        public int? US_FBM_Offers { get; set; }
        [JsonPropertyName("fba_offers")]
        public int? US_FBA_Offers { get; set; }
        [JsonPropertyName("BSR")]
        public double? US_BSR { get; set; }
        [JsonIgnore]
        private double? _usReferralFee { get; set; }
        [JsonPropertyName("referral_fee")]
        public double? US_Referral_Fee { get { return Math.Round((_usReferralFee ?? 0) / 100, 2); } set { _usReferralFee = value; } }
        [JsonIgnore]
        private double? _usSalesPerMonth { get; set; }
        [JsonPropertyName("sales_per_month")]
        public double? US_Sales_Per_Month { get { return Math.Round((_usSalesPerMonth ?? 0) / 100, 2); } set { _usSalesPerMonth = value; } }
        [JsonPropertyName("total_offers")]
        public double? US_Total_Offers { get; set; }
        [JsonPropertyName("unit_per_month")]
        public double? US_Units_Per_Month { get; set; }
        [JsonIgnore]
        private double? _usVariableClosingFee{ get; set; }
        [JsonPropertyName("variable_closing_fee")]
        public double? US_Variable_Closing_Fee { get { return Math.Round((_usVariableClosingFee ?? 0) / 100, 2); } set { _usVariableClosingFee = value; } }
        [JsonPropertyName("no_of_variation")]
        public int? US_Number_Variations { get; set; }
        [JsonPropertyName("marketplace_id")]
        public int? AMZ_Marketplace { get; set; }

        [JsonPropertyName("DateTime")]
        public DateTime US_Time_Datestamp { get; set; }


    }
}
