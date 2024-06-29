using System.Text.Json.Serialization;

namespace RocketSource.Models
{
    public class UKScanData
    {
        [JsonPropertyName("asin")]
        public string ASIN { get; set; }
        [JsonPropertyName("UK_average_bsr_30")]
        public double? UK_Average_BSR_30 { get; set; }
        [JsonPropertyName("UK_average_bsr_90")]
        public double? UK_Average_BSR_90 { get; set; }
        [JsonIgnore]
        private double? _ukBSRPercentage;
        [JsonPropertyName("bsr_percentage")]
        public double? UK_BSR_Percentage { get { return Math.Round((_ukBSRPercentage ?? 0) / 100 / 100, 2); } set { _ukBSRPercentage = value; } }

        [JsonIgnore]
        private double? _ukBuyBoxPrice;
        [JsonPropertyName("buy_box_price")]
        public double? UK_Buybox_Price { get { return Math.Round((_ukBuyBoxPrice ?? 0) / 100, 2); } set { _ukBuyBoxPrice = value; } }
        [JsonPropertyName("competitive_sellers_count")]
        public int? UK_Competitive_Sellers { get; set; }
        private double? _ukFBAFee { get; set; }
        [JsonPropertyName("fba_fees")]
        public double? UK_FBA_Fees { get { return Math.Round((_ukFBAFee ?? 0) / 100, 2); } set { _ukFBAFee = value; } }
        [JsonIgnore]
        private double? _ukFBALowestPrice { get; set; }
        [JsonPropertyName("fba_lowest_price")]
        public double? UK_Lowest_Price_FBA { get { return Math.Round((_ukFBALowestPrice ?? 0) / 100, 2); } set { _ukFBALowestPrice = value; } }
        [JsonIgnore]
        private double? _ukFBMLowestPrice { get; set; }
        [JsonPropertyName("fbm_lowest_price")]
        public double? UK_Lowest_Price_FBM { get { return Math.Round((_ukFBMLowestPrice ?? 0) / 100, 2); } set { _ukFBMLowestPrice = value; } }

        [JsonPropertyName("fbm_offers")]
        public int? UK_FBM_Offers { get; set; }
        [JsonPropertyName("fba_offers")]
        public int? UK_FBA_Offers { get; set; }
        [JsonPropertyName("BSR")]
        public double? UK_BSR { get; set; }
        [JsonIgnore]
        private double? _ukReferralFee { get; set; }
        [JsonPropertyName("referral_fee")]
        public double? UK_Referral_Fee { get { return Math.Round((_ukReferralFee ?? 0) / 100, 2); } set { _ukReferralFee = value; } }
        [JsonIgnore]
        private double? _ukSalesPerMonth { get; set; }
        [JsonPropertyName("sales_per_month")]
        public double? UK_Sales_Per_Month { get { return Math.Round((_ukSalesPerMonth ?? 0) / 100, 2); } set { _ukSalesPerMonth = value; } }
        [JsonPropertyName("total_offers")]
        public double? UK_Total_Offers { get; set; }
        [JsonPropertyName("unit_per_month")]
        public double? UK_Units_Per_Month { get; set; }
        [JsonIgnore]
        private double? _ukVariableClosingFee { get; set; }
        [JsonPropertyName("variable_closing_fee")]
        public double? UK_Variable_Closing_Fee { get { return Math.Round((_ukVariableClosingFee ?? 0) / 100, 2); } set { _ukVariableClosingFee = value; } }
        [JsonPropertyName("no_of_variation")]
        public int? UK_Number_Variations { get; set; }
        [JsonPropertyName("marketplace_id")]
        public int? AMZ_Marketplace { get; set; }

        [JsonPropertyName("DateTime")]
        public DateTime UK_Time_Datestamp { get; set; }
    }
}
