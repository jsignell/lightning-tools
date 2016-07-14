'''
Setup the variable space for lightning data
'''

from pointprocess.common import to_decimal
import matplotlib.cm as cm

out = '/home/jsignell/erddapData/Cloud_to_Ground_Lightning/'
out_path = out+'US/'

cmap = cm.get_cmap('gnuplot_r', 9)
cmap.set_under('None')

months = {1: 'January', 2:'February', 3:'March', 4: 'April', 5:'May',6: 'June', 
          7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

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
