using AutoMapper;
using Microsoft.Extensions.Configuration;
using RocketSource.Models;

namespace RocketSource
{
    public class MapperProfile : Profile
    {
        public MapperProfile(IConfigurationRoot config)
        {
            var _usdToGbp = Convert.ToDouble(config["Units:USDtoGBP"]);

            CreateMap<Data, USScanData>()
                .ForMember(dest => dest.ASIN, opt => opt.MapFrom(src => src.asin))
                //.ForMember(dest => dest.AverageBSR30, opt => opt.MapFrom(src => src.))
                //.ForMember(dest => dest.AverageBSR90, opt => opt.MapFrom(src => src.))
                .ForMember(dest => dest.US_BSR_Percentage, opt => opt.MapFrom(src => src.bsr_percentage))
                .ForMember(dest => dest.US_Buybox_Price, opt => opt.MapFrom(src => src.buybox_price/_usdToGbp))
                .ForMember(dest => dest.US_Competitive_Sellers, opt => opt.MapFrom(src => src.competitive_sellers))
                .ForMember(dest => dest.US_FBA_Fees, opt => opt.MapFrom(src => src.amazon_fees.fba_fees / _usdToGbp))
                .ForMember(dest => dest.US_Lowest_Price_FBA, opt => opt.MapFrom(src => src.lowest_price_new_fba / _usdToGbp))
                .ForMember(dest => dest.US_Lowest_Price_FBM, opt => opt.MapFrom(src => src.lowest_price_new_fbm / _usdToGbp))
                .ForMember(dest => dest.US_FBA_Offers, opt => opt.MapFrom(src => src.new_fba_offers_count))
                .ForMember(dest => dest.US_FBM_Offers, opt => opt.MapFrom(src => src.new_fbm_offers_count))
                .ForMember(dest => dest.US_BSR, opt => opt.MapFrom(src => src.rank))
                .ForMember(dest => dest.US_Referral_Fee, opt => opt.MapFrom(src => src.amazon_fees.referral_fee / _usdToGbp))
                .ForMember(dest => dest.US_Sales_Per_Month, opt => opt.MapFrom(src => src.sales_per_month))
                .ForMember(dest => dest.US_Total_Offers, opt => opt.MapFrom(src => src.total_offers_count))
                .ForMember(dest => dest.US_Units_Per_Month, opt => opt.MapFrom(src => src.units_per_month))
                .ForMember(dest => dest.US_Variable_Closing_Fee, opt => opt.MapFrom(src => src.amazon_fees.variable_closing_fee / _usdToGbp))
                .ForMember(dest => dest.US_Number_Variations, opt => opt.MapFrom(src => src.number_of_variations))
                .ForMember(dest => dest.AMZ_Marketplace, opt => opt.MapFrom(src => src.marketplace_id))
                .ForMember(dest => dest.US_Time_Datestamp, opt => opt.MapFrom(src => DateTime.Now))
                ;
        }
    }
}
