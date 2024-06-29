using AutoMapper;
using RocketSource.Models;

namespace RocketSource
{
    public class MapperProfile : Profile
    {
        public MapperProfile()
        {
            CreateMap<Data, StandingScanData>()
                .ForMember(dest => dest.ASIN, opt => opt.MapFrom(src=>src.asin))
                .ForMember(dest => dest.Brand, opt => opt.MapFrom(src => src.brand))
                //.ForMember(dest => dest.BuyBoxPrice, opt => opt.MapFrom(src => src.buybox_price))
                .ForMember(dest => dest.Category, opt => opt.MapFrom(src => src.category))
                //.ForMember(dest => dest.Width, opt => opt.MapFrom(src => src.dimensions.item_dimensions.width))
                //.ForMember(dest => dest.Height, opt => opt.MapFrom(src => src.dimensions.item_dimensions.height))
                //.ForMember(dest => dest.Length, opt => opt.MapFrom(src => src.dimensions.item_dimensions.length))
                //.ForMember(dest => dest.Weight, opt => opt.MapFrom(src => src.dimensions.item_dimensions.weight))             
                .ForMember(dest => dest.EAN, opt => opt.MapFrom(src => src.identifiers.ean))
                .ForMember(dest => dest.Time_Datestamp, opt => opt.MapFrom(src => DateTime.Now))
                ;

        }
    }
}
