        US_BSR_Percentage { get { return Math.Round((_usBSRPercentage ?? 0) / 100/100, 2); } set { _usBSRPercentage = value; } }
        US_Buybox_Price { get { return Math.Round((_usBuyBoxPrice ?? 0)/100, 2); } set { _usBuyBoxPrice = value; } }
        US_FBA_Fees { get { return Math.Round((_usFBAFee ?? 0)/100, 2); } set { _usFBAFee = value; } }
        US_Lowest_Price_FBA { get { return Math.Round((_usFBALowestPrice ?? 0) / 100, 2); } set { _usFBALowestPrice = value; } }
        US_Lowest_Price_FBM { get { return Math.Round((_usFBMLowestPrice ?? 0) / 100, 2); } set { _usFBMLowestPrice = value; } }
        US_Referral_Fee { get { return Math.Round((_usReferralFee ?? 0) / 100, 2); } set { _usReferralFee = value; } }
        US_Sales_Per_Month { get { return Math.Round((_usSalesPerMonth ?? 0) / 100, 2); } set { _usSalesPerMonth = value; } }
        US_Variable_Closing_Fee { get { return Math.Round((_usVariableClosingFee ?? 0) / 100, 2); } set { _usVariableClosingFee = value; } }
