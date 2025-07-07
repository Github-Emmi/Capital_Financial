Status = (
    ('Pending', 'Pending'),
    ('Successful', 'Successful'),
)

Employment =(
("none","Select Type of Employment"),
("Self Employed","Self Employed"), 
("Self Employed","Public/Government Office"), 
("Self Employed","Private/Partnership Office"), 
("Self Employed","Business/Sales"), 
("Self Employed","Trading/Market"), 
("Self Employed","Military/Paramilitary"), 
("Self Employed","Politician/Celebrity"),
)

payment_method = (
    ("check", "Check"),
    ("Wire Transfer", "Wire Transfer"),
)

Salary =(
("none","Select Salary Range"),
("$100.00 - $500.00","$100.00 - $500.00"), 
("$700.00 - $1,000.00","$700.00 - $1,000.00"), 
("$1,000.00 - $2,000.00","$1,000.00 - $2,000.00"), 
("$2,000.00 - $5,000.00","$2,000.00 - $5,000.00"), 
("$5,000.00 - $10,000.00","$5,000.00 - $10,000.00"), 
("$15,000.00 - $20,000.00","$15,000.00 - $20,000.00"), 
("$25,000.00 - $30,000.00","$25,000.00 - $30,000.00"), 
("$30,000.00 - $70,000.00","$30,000.00 - $70,000.00"), 
("$80,000.00 - $140,000.00","$80,000.00 - $140,000.00"), 
("$150,000.00 - $300,000.00","$150,000.00 - $300,000.00"), 
("$300,000.00 - $1,000,000.00","$300,000.00 - $1,000,000.00"), 
)


Title = (
    ('none', 'Please Select Title'),
    ('Mr.', 'Mr.'),
    ('Mrs.', 'Mrs.'),
    ('Mr&Mrs.', 'Mr&Mrs.'),
    ('Ms.', 'Ms.'),
    ('Miss.', 'Miss.'),
)

Gender = (
    ('none', 'Please Select Gender'),
    ('Male', 'Male'),
    ('Female', 'FeMale'),
    ('Other', 'Other')
)


Account_Type = (
    ('none','Please select Account Type'),
    ('Checking Account', 'Checking Account'),
    ('Savings Account', 'Savings Account'),
    ('Fixed Deposit Account', 'Fixed Deposit Account'),
    ('Current Account','Current Account'),
    ('Business Account', 'Business Account'),
    ('Non Resident Account','Non Resident Account'),
    ('Cooperate Business Account', 'Cooperate Business Account'),
    ('Investment Account', 'Investment Account'),
)

nok_relationship = (
    ('none','Please select Relationship'),
    ('Son','Son'),
    ('Daughter','Daughter'),
    ('Father','Father'),
    ('Mother','Mother'),
    ('Husband','Husband'),
    ('Spouse','Spouse'),
    ('Hobby','Hobby'),
    ('Cousin','Cousin'),
    ('Others','Others'),
)

nok_Age = (
    ('none','Please Select Age'),
    ('18-25yrs','18-25yrs'),
    ('25-35yrs','25-35yrs'),
    ('35-50yrs','35-50yrs'),
    ('50-above','50yrs and above'),
)


Security_Question_One = (
    ("none","Please Select Question One"),
    ("What is your pet name?","What is your pet name?"),   
    ("What is your nick name?","What is your nick name?"),    
    ("What is the name of your first car?","What is the name of your first car?"),   
    ("when did you finish high school?","when did you finish high school?"),
    ("your favorite music?","your favorite music?"),
    ("your favorite movie?","your favorite movie"),
    ("your favorite role model?","your favorite role model"),    
    ("favorite state?","favorite state?"),
    
    )


Security_Question_Two = (
("none","Please Select Question Two"),
("What is the name of the road you grew up on?","What is the name of the road you grew up on?"),   
("What is your mother’s maiden name?","What is your mother’s maiden name?"),
("Where did you meet your spouse?","Where did you meet your spouse?"),
("when did you finish high school?","when did you finish high school?"),
("What is your favorite food?","What is your favorite food?"),
("What city were you born in?","What city were you born in?"),    
("Where is your favorite place to vacation?","Where is your favorite place to vacation?"),   
("What was the first company that you worked for?","What was the first company that you worked for?"),        
)


Currency = (
('USD', 'America United States Dollars – USD'),
("AFN", "Afghanistan Afghanis – AFN"),
("ALL", "Albania Leke – ALL"),
("DZD", "Algeria Dinars – DZD"),
("ARS", "Argentina Pesos – ARS"),
("AUD", "Australia Dollars – AUD"),
("ATS", "Austria Schillings – ATS"),
("BSD", "Bahamas Dollars – BSD"),
("BHD", "Bahrain Dinars – BHD"),
("BDT", "Bangladesh Taka – BDT"),
("BBD", "Barbados Dollars – BBD"),
("BEF", "Belgium Francs – BEF"),
("BMD", "Bermuda Dollars – BMD"),
 
("BRL", "Brazil Reais – BRL"),
("BGN", "Bulgaria Leva – BGN"),
("CAD", "Canada Dollars – CAD"),
("XOF", "CFA BCEAO Francs – XOF"),
("XAF", "CFA BEAC Francs – XAF"),
("CLP", "Chile Pesos – CLP"),
 
("CNY", "China Yuan Renminbi – CNY"),
("CNY", "RMB (China Yuan Renminbi), – CNY"),
("COP", "Colombia Pesos – COP"),
("XPF", "CFP Francs – XPF"),
("CRC", "Costa Rica Colones – CRC"),
("HRK", "Croatia Kuna – HRK"),
 
("CYP", "Cyprus Pounds – CYP"),
("CZK", "Czech Republic Koruny – CZK"),
("DKK", "Denmark Kroner – DKK"),
("DEM", "Deutsche (Germany), Marks – DEM"),
("DOP", "Dominican Republic Pesos – DOP"),
("NLG", "Dutch (Netherlands), Guilders – NLG"),
 
("XCD", "Eastern Caribbean Dollars – XCD"),
("EGP", "Egypt Pounds – EGP"),
("EEK", "Estonia Krooni – EEK"),
("EUR", "Euro – EUR"),
("FJD", "Fiji Dollars – FJD"),
("FIM", "Finland Markkaa – FIM"),
 
("FRF", "France Francs – FRF"),
("DEM", "Germany Deutsche Marks – DEM"),
("XAU", "Gold Ounces – XAU"),
("GRD", "Greece Drachmae – GRD"),
("GTQ", "Guatemalan Quetzal – GTQ"),
("NLG", "Holland (Netherlands), Guilders – NLG"),
("HKD", "Hong Kong Dollars – HKD"),
 
("HUF", "Hungary Forint – HUF"),
("ISK", "Iceland Kronur – ISK"),
("XDR", "IMF Special Drawing Right – XDR"),
("INR", "India Rupees – INR"),
("IDR", "Indonesia Rupiahs – IDR"),
("IRR", "Iran Rials – IRR"),
 
("IQD", "Iraq Dinars – IQD"),
("IEP", "Ireland Pounds – IEP"),
("ILS", "Israel New Shekels – ILS"),
("ITL", "Italy Lire – ITL"),
("JMD", "Jamaica Dollars – JMD"),
("JPY", "Japan Yen – JPY"),
 
("JOD", "Jordan Dinars – JOD"),
("KES", "Kenya Shillings – KES"),
("KRW", "Korea (South), Won – KRW"),
("KWD", "Kuwait Dinars – KWD"),
("LBP", "Lebanon Pounds – LBP"),
("LUF", "Luxembourg Francs – LUF"),
 
("MYR", "Malaysia Ringgits – MYR"),
("MTL", "Malta Liri – MTL"),
("MUR", "Mauritius Rupees – MUR"),
("MXN", "Mexico Pesos – MXN"),
("MAD", "Morocco Dirhams – MAD"),
("NLG", "Netherlands Guilders – NLG"),
 
("NZD", "New Zealand Dollars – NZD"),
("NGN", "Nigeria Naira – NGN"),
("NOK", "Norway Kroner – NOK"),
("OMR", "Oman Rials – OMR"),
("PKR", "Pakistan Rupees – PKR"),
("XPD", "Palladium Ounces – XPD"),
("PEN", "Peru Nuevos Soles – PEN"),
 
("PHP", "Philippines Pesos – PHP"),
("XPT", "Platinum Ounces – XPT"),
("PLN", "Poland Zlotych – PLN"),
("PTE", "Portugal Escudos – PTE"),
("QAR", "Qatar Riyals – QAR"),
("RON", "Romania New Lei – RON"),
 
("ROL", "Romania Lei – ROL"),
("RUB", "Russia Rubles – RUB"),
("SAR", "Saudi Arabia Riyals – SAR"),
("XAG", "Silver Ounces – XAG"),
("SGD", "Singapore Dollars – SGD"),
("SKK", "Slovakia Koruny – SKK"),
 
("SIT", "Slovenia Tolars – SIT"),
("ZAR", "South Africa Rand – ZAR"),
("KRW", "South Korea Won – KRW"),
("ESP", "Spain Pesetas – ESP"), 
 
("SDD", "Sudan Dinars – SDD"),
("SEK", "Sweden Kronor – SEK"),
("CHF", "Switzerland Francs – CHF"),
("TWD", "Taiwan New Dollars – TWD"),
("THB", "Thailand Baht – THB"),
("TTD", "Trinidad and Tobago Dollars – TTD"),
 
("TND", "Tunisia Dinars – TND"),
("TRY", "Turkey New Lira – TRY"),
("AED", "United Arab Emirates Dirhams – AED"),
("GBP", "United Kingdom Pounds – GBP"),
("USD", "United States Dollars – USD"),
("VEB", "Venezuela Bolivares – VEB"),
 
("VND", "Vietnam Dong – VND"),
("ZMK", "Zambia Kwacha – ZMK"),
)