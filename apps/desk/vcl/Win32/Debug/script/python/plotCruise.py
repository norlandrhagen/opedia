import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import db
import timeSeries as TS
from datetime import datetime, date, timedelta
import time
from math import pi
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import DatetimeTickFormatter
from bokeh.palettes import all_palettes
from bokeh.models import HoverTool
from bokeh.embed import components


def removeNA(df, subset):
    df = df.dropna(subset=subset)
    return df

def indexTime(df, frm='%Y-%m-%d %H:%M:%S'):
    df['time'] = pd.to_datetime(df['time'], format=frm)
    df.index = df['time']
    del df['time']
    return df

def CruiseQuery(table, cruise):
    query = "SELECT [time], lat, lon FROM %s WHERE "
    query = query + "cruise='%s' "
    query = query % (table, cruise)
    return query


def getCruiseTrack(DB, source, cruise):
    df = None
    if DB:
        query = CruiseQuery(source, cruise)
        df = db.dbFetch(query)
    else:
        df = pd.read_csv(source)    
    return df


def resample(df, resampTau):
    df = indexTime(df)
    df = df.resample(resampTau).mean()
    df.reset_index(level=0, inplace=True)
    df = removeNA(df, ['lat', 'lon'])        
    return df

def dumpCruiseShape(df, source, cruise, resampTau, fname):
    df = resample(df, resampTau)
    del df['time']
    
    df['geometry'] = df.apply(lambda x: Point((float(x.lon), float(x.lat))), axis=1)
    df = gpd.GeoDataFrame(df, geometry='geometry')
    df.to_file('shape/%s.shp' % fname, driver='ESRI Shapefile')    
    return




def plotAlongTrack(tables, variables, cruiseName, track, spMargin, extV, extVV, extV2, extVV2, marker='-', msize=30, clr='purple'):
    p = []
    lw = 2
    w = 800
    h = 400
    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
    TOOLS = 'pan,wheel_zoom,zoom_in,zoom_out,box_zoom, undo,redo,reset,tap,save,box_select,poly_select,lasso_select'
    for i in range(len(tables)):
        ts, ys, y_stds = [], np.array([]), np.array([])
        for j in range(len(track)):
            startDate = track.iloc[j]['time'].strftime('%Y-%m-%d')
            endDate = startDate

            lat1 = float(track.iloc[j]['lat']) - spMargin
            lat2 = float(track.iloc[j]['lat']) + spMargin
            lon1 = float(track.iloc[j]['lon']) - spMargin
            lon2 = float(track.iloc[j]['lon']) + spMargin
            t, y, y_std = TS.timeSeries(tables[i], variables[i], startDate, endDate, lat1, lat2, lon1, lon2, extV[i], extVV[i], extV2[i], extVV2[i])
            ts.append(track.iloc[j]['time'])
            #ts.append(t[0])
            ys = np.append(ys, y[0])
            y_stds = np.append(y_stds, y_std[0])

        p1 = figure(tools=TOOLS, toolbar_location="above", plot_width=w, plot_height=h)
        #p1.xaxis.axis_label = 'Time'
        p1.yaxis.axis_label = variables[i] + ' [' + db.getVar(tables[i], variables[i]).iloc[0]['Unit'] + ']'
        leg = 'Along Track (' + cruiseName + ') ' + variables[i]
        if extV[i] != None:
            leg = leg + '   ' + extV[i] + ': ' + ( '%d' % float(extVV[i]) ) 
            if tables[i].find('Pisces') != -1:
                leg = leg + ' ' + 'm'

        fill_alpha = 0.07        
        if tables[i].find('Pisces') != -1:
            fill_alpha = 0.3
        cr = p1.circle(ts, ys, fill_color="grey", hover_fill_color="firebrick", fill_alpha=fill_alpha, hover_alpha=0.3, line_color=None, hover_line_color="white", legend=leg, size=msize)
        p1.line(ts, ys, line_color=clr, line_width=lw, legend=leg)
        p1.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))
        p1.xaxis.formatter=DatetimeTickFormatter(
                hours=["%d %B %Y %H:%M:%S"],
                days=["%d %B %Y %H:%M:%S"],
                months=["%d %B %Y %H:%M:%S"],
                years=["%d %B %Y %H:%M:%S"],
            )

        p1.xaxis.major_label_orientation = pi/4
        #p1.xaxis.visible = False
        p.append(p1)


    output_file("embed/" + fname + ".html", title="Along Track")
    show(column(p))
    
    '''
    p1_script, p1_div = components(p1)
    embedComponents('embed/scriptTS1.js', p1_script)
    embedComponents('embed/divTS1.js', p1_div)

    p2_script, p2_div = components(p2)
    embedComponents('embed/scriptTS2.js', p1_script)
    embedComponents('embed/divTS2.js', p1_div)

    p3_script, p3_div = components(p3)
    embedComponents('embed/scriptTS3.js', p1_script)
    embedComponents('embed/divTS3.js', p1_div)
    '''
    return





#dumpCruiseShape(True, 'tblSeaFlow', 'KM_1', '3T', 'shape')

DB = bool(int(sys.argv[1]))
command = int(sys.argv[2])
source = sys.argv[3]      
cruise = sys.argv[4]      
resampTau = sys.argv[5]
fname = sys.argv[6] 

df = getCruiseTrack(DB, source, cruise)
df = resample(df, resampTau)

if command == 1:
    dumpCruiseShape(df, source, cruise, resampTau, fname)
elif command == 2:
    spMargin = float(sys.argv[7])         #spatial margin 
    tables = sys.argv[8].split(',')
    variables = sys.argv[9].split(',')   
    extV = sys.argv[10].split(',')       #extra condition: var_name
    extVV = sys.argv[11].split(',')       #extra condition: var_val
    extV2 = sys.argv[12].split(',')       #extra condition: var_name
    extVV2 = sys.argv[13].split(',')       #extra condition: var_val
    
    for i in range(len(tables)):
        if extV[i].find('ignore') != -1:
            extV[i]=None
        if extVV[i].find('ignore') != -1:
            extVV[i]=None
        if extV2[i].find('ignore') != -1:
            extV2[i]=None
        if extVV2[i].find('ignore') != -1:
            extVV2[i]=None


    plotAlongTrack(tables, variables, cruise, df, spMargin, extV, extVV, extV2, extVV2, marker='-', msize=30, clr='darkturquoise')
