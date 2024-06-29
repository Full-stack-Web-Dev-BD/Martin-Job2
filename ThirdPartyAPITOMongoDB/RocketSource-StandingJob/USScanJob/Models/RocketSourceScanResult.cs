using System.Text.Json.Serialization;

namespace RocketSource.Models
{
    public class RocketSourceScanResult
    {
        public RocketSourceScanResult()
        {
                
        }

        [JsonPropertyName("count")]
        public int? Count { get; set; }
        [JsonPropertyName("data")]
        public List<Data> Data { get; set; }

    }

    // Root myDeserializedClass = JsonConvert.DeserializeObject<Root>(myJsonResponse);
    public class AmazonFees
    {
        public object per_item_fee { get; set; }
        public double? fba_fees { get; set; }
        public double? variable_closing_fee { get; set; }
        public int? referral_fee { get; set; }
        public object error { get; set; }
    }

    public class BuyboxEligibleOffer
    {
        public string condition { get; set; }
        public string fulfillment_channel { get; set; }
        public int? offer_count { get; set; }
    }

    public class BuyBoxPrice
    {
        public string condition { get; set; }
        public object offerType { get; set; }
        public object quantityTier { get; set; }
        public object quantityDiscountType { get; set; }
        public int? landedPrice { get; set; }
        public int? listingPrice { get; set; }
        public int? shipping { get; set; }
        public object points { get; set; }
        public object sellerId { get; set; }
    }

    public class Dimensions
    {
        public PackageDimensions package_dimensions { get; set; }
        public ItemDimensions item_dimensions { get; set; }
    }

    public class Financials
    {
        public int? inbound_shipping { get; set; }
        public int? prep_cost { get; set; }
        public object fba_storage_fees { get; set; }
        public int? net_revenue { get; set; }
        public int? profit { get; set; }
        public int? margin { get; set; }
        public object roi { get; set; }
    }

    public class Identifiers
    {
        public List<string> ean { get; set; }
    }

    public class Image
    {
        public string marketplace_id { get; set; }
        public List<Image> image { get; set; }
    }

    public class Image2
    {
        public int? height { get; set; }
        public int? width { get; set; }
        public string link { get; set; }
        public string variant { get; set; }
    }

    public class Inputs
    {
        public string identifier { get; set; }
        public object cost { get; set; }
        public object stock { get; set; }
        public object map { get; set; }
        public object supplier_title { get; set; }
        public object supplier_sku { get; set; }
        public object supplier_image { get; set; }
        public int? supplier_pack_quantity { get; set; }
        public object discount_per_product { get; set; }
        public object discount_supplier { get; set; }
        public object discount_cost { get; set; }
        public object total_cogs { get; set; }
        public object custom_columns { get; set; }
        public object source_link { get; set; }
    }

    public class ItemDimensions
    {
        public double? length { get; set; }
        public double? width { get; set; }
        public double? height { get; set; }
        public double? weight { get; set; }
        public string length_unit { get; set; }
        public string width_unit { get; set; }
        public string height_unit { get; set; }
        public string weight_unit { get; set; }
    }

    public class LowestPrice
    {
        public string condition { get; set; }
        public string fulfillment_channel { get; set; }
        public object offer_type { get; set; }
        public object quantity_tier { get; set; }
        public object quantity_discount_type { get; set; }
        public int? landed_price { get; set; }
        public int? listing_price { get; set; }
        public int? shipping { get; set; }
        public object points { get; set; }
    }

    public class NumberOfOffer
    {
        public string condition { get; set; }
        public string fulfillment_channel { get; set; }
        public int? offer_count { get; set; }
    }

    public class Offers
    {
        public int? total_offers_count { get; set; }
        public object list_price { get; set; }
        public List<BuyboxEligibleOffer> buybox_eligible_offers { get; set; }
        public List<NumberOfOffer> number_of_offers { get; set; }
        public List<LowestPrice> lowest_prices { get; set; }
        public List<BuyBoxPrice> buy_box_prices { get; set; }
    }

    public class PackageDimensions
    {
        public double? length { get; set; }
        public double? width { get; set; }
        public double? height { get; set; }
        public double? weight { get; set; }
        public string length_unit { get; set; }
        public string width_unit { get; set; }
        public string height_unit { get; set; }
        public string weight_unit { get; set; }
    }

    public class Data
    {
        public int? id { get; set; }
        public Identifiers identifiers { get; set; }
        public object errors { get; set; }
        public string asin { get; set; }
        public AmazonFees amazon_fees { get; set; }
        public int? number_of_variations { get; set; }
        public string brand { get; set; }

        public Dimensions dimensions { get; set; }
        public int? buybox_price { get; set; }
        public int? competitive_sellers { get; set; }
        public double? lowest_price_new_fba { get; set; }
        public double? lowest_price_used_fba { get; set; }
        public int? lowest_price_new_fbm { get; set; }
        public object lowest_price_used_fbm { get; set; }
        public object new_fba_offers_count { get; set; }
        public int? new_fbm_offers_count { get; set; }
        public int? total_offers_count { get; set; }




        public int? bsr_percentage { get; set; }
        public int? marketplace_id { get; set; }
        public int? units_per_month { get; set; }
        public int? sales_per_month { get; set; }
        public int? profit_per_month { get; set; }
        public int? rank { get; set; }
        public string category { get; set; }
    }



}
