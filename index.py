"""
Created on 20. 5. 2020

@author: ibisek
"""

import sys
import flask
import getopt

from configuration import dbConnectionInfo
from db.DbSource import DbSource
from dao.logbookDao import listDepartures, listArrivals,listFlights
from dao.stats import getNumFlightsToday, getTotNumFlights, getLongestFlightTimeToday, getHighestTrafficToday


app = flask.Flask(__name__)


@app.route('/')
def index():
    departures, arrivals, flights = _prepareData()

    totNumFlights = getTotNumFlights()
    numFlightsToday = getNumFlightsToday()
    longestFlightTime = getLongestFlightTimeToday()
    highestTrafficLocation, highestTrafficCount = getHighestTrafficToday()

    return flask.render_template('index.html', departures=departures, arrivals=arrivals, flights=flights,
                                 numFlightsToday=numFlightsToday, totNumFlights=totNumFlights,
                                 longestFlightTime=longestFlightTime, highestTrafficLocation=highestTrafficLocation,
                                 highestTrafficCount=highestTrafficCount)


@app.route('/loc/<icaoCode>', methods=['GET'])
def filterByIcaoCode(icaoCode):
    departures, arrivals, flights = _prepareData(icaoCode=icaoCode)
    return flask.render_template('index.html', departures=departures, arrivals=arrivals, flights=flights)


@app.route('/reg/<registration>', methods=['GET'])
def filterByRegistration(registration):
    departures, arrivals, flights = _prepareData(registration=registration)
    return flask.render_template('index.html', departures=departures, arrivals=arrivals, flights=flights)


def _prepareData(icaoCode=None, registration=None):

    if icaoCode:
        icaoCode = _saninitise(icaoCode)

    if registration:
        registration = _saninitise(registration)

    departures = listDepartures(icaoCode=icaoCode, registration=registration)
    arrivals = listArrivals(icaoCode=icaoCode, registration=registration)
    flights = listFlights(icaoCode=icaoCode, registration=registration)

    return departures, arrivals, flights


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)  # method not allowed
@app.errorhandler(413)
def handle_error(error):
    return flask.render_template("error40x.html", code=error.code, message=error.description)


# @app.errorhandler(Exception)
# def unhandled_exception(error):
#     msg = "Unhandled Exception: {}".format(error)
#     # logger.error(msg)
#     # app.logger.error(msg)
#     return flask.render_template('error40x.html', code=500), 500

def _saninitise(s):
    return s.replace('\\', '').replace(';', '').replace('\'', '').replace('--', '')


if __name__ == '__main__':

    debugMode = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d")
        for optPair in opts:

            if optPair[0] == "-d":

                debugMode = True

    # handle invalid script arguments
    except getopt.GetoptError as e: 
        
        # print error message to stderr
        print("Argument error: " + e.msg, file=sys.stderr)
        # exit application
        sys.exit(1)

    app.run(debug=debugMode)