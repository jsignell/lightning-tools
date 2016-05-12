out = '/home/jsignell/erddapData/Cloud_to_Ground_Lightning/'
out_path = out+'US/'

def to_decimal(degree, minute, second):
    return(degree+(minute/60.)+(second/3600.))

cities={'cedar': {'path': out+'Cedar_City_UT/',
                  'lat': to_decimal(37, 35, 27),
                  'lon': -to_decimal(112, 51, 44),
                  'r': 3},
        'phoenix': {'path': out+'Phoenix_AZ/',
                    'lat': to_decimal(33, 17, 21),
                    'lon': -to_decimal(111, 40, 12),
                    'r': 3},
        'greer': {'path': out+'Greer_SC/',
                  'lat': to_decimal(34, 53, 0),
                  'lon': -to_decimal(82, 13, 12),
                  'r': 3},
        'sterling':{'path': out+'Sterling_VA/',
                    'lat': to_decimal(38, 58, 31),
                    'lon': -to_decimal(77, 28, 40),
                    'r': 3},
        'denver':{'path': out+'Denver_CO/',
                  'lat': to_decimal(39, 47, 12),
                  'lon': -to_decimal(104, 32, 45),
                  'r': 3},
        'columbia': {'path': out+'Columbia_Plateau/',
                     'lat': 45,
                     'lon': -119,
                     'r': 4}
       }