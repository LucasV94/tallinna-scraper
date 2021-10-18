import asyncio
from pyppeteer import launch
import json

async def main():

# Open headless chromium to the Tallinn Airport website
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.tallinn-airport.ee/en/flight-info/realtime-flights/?type=departures#destination-tabs')

# Wait for Departures table to be visible on the screen before it proceeds
    await page.waitForSelector("div[data-flights-type^='departures'",{'visible':True})

# Evaluate selector to get each departing flights information (carrier, destination, name, time) and output to JSON
    flights_list = await page.evaluate('''() => { 

        var flightList = []
        var departureTableRow = $("div[data-flights-type^='departures'] .t-body .track-flight__row")

        departureTableRow.each(function() {
            var flightButton = $(this).find('#startTracking')

            var flightData = {
                'carrier': $(flightButton).attr('data-carrier'),
                'destination': $(flightButton).attr('data-destination'),
                'name': $(flightButton).attr('data-name'),
                'time': $(flightButton).attr('data-time'),
            }
            flightList.push(flightData)
        })

        var flightListJson = JSON.stringify(flightList)
        return flightListJson
    }''')

# Load flights_list as json object        
    flights_json = json.loads(flights_list)

# For each item in flights_json if the carrier is Finnair print the flight
    print("Finnair Flight List")
    for flight in flights_json:
        airline = flight["carrier"]
        output = flight["time"], flight["name"], flight["destination"]
        if airline == "Finnair":
            print (output)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())