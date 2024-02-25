import pandas as pd
import datetime
from datetime import date, timedelta
import httplib2
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from collections import defaultdict
from dateutil import relativedelta
import argparse
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import re
import os
from urllib.parse import urlparse


def authorize_creds(creds):
    # Variable parameter that controls the set of resources that the access token permits.
    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

    # Path to client_secrets.json file
    CLIENT_SECRETS_PATH = creds

    # Create a parser to be able to open browser for Authorization
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, parents=[tools.argparser]
    )
    flags = parser.parse_args([])

    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS_PATH,
        scope=SCOPES,
        message=tools.message_if_missing(CLIENT_SECRETS_PATH),
    )

    # Prepare credentials and authorize HTTP
    # If they exist, get them from the storage object
    # credentials will get written back to a file.
    storage = file.Storage("core/core/authorizedcreds.dat")
    credentials = storage.get()

    # If authenticated credentials don't exist, open Browser to authenticate
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())
    webmasters_service = build("webmasters", "v3", http=http)
    return webmasters_service


def execute_request(service, property_uri, request):
    return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()


# Create function to extract all the data
def extract_data(site, creds, num_days):
    webmasters_service = authorize_creds(creds)

    # Set up Dates
    end_date = datetime.date.today() - relativedelta.relativedelta(days=num_days)
    start_date = end_date - relativedelta.relativedelta(days=num_days)
    delta = datetime.timedelta(days=1)  # This will let us loop one day at the time
    scDict = defaultdict(list)

    while start_date <= end_date:
        print("Start date at beginning: %s" % start_date)

        maxRows = 25000  # Maximum 25K per call
        numRows = 0  # Start at Row Zero
        status = ""  # Initialize status of extraction

        while (
            status != "Finished"
        ):  # Test with i < 10 just to see how long the task will take to process.
            request = {
                "startDate": datetime.datetime.strftime(start_date, "%Y-%m-%d"),
                "endDate": datetime.datetime.strftime(start_date, "%Y-%m-%d"),
                "dimensions": ["date", "page", "query"],
                "rowLimit": maxRows,
                "startRow": numRows,
            }

            response = execute_request(webmasters_service, site, request)

            try:
                # Process the response
                for row in response["rows"]:
                    scDict["date"].append(row["keys"][0] or 0)
                    scDict["page"].append(row["keys"][1] or 0)
                    scDict["query"].append(row["keys"][2] or 0)
                    scDict["clicks"].append(row["clicks"] or 0)
                    scDict["ctr"].append(row["ctr"] or 0)
                    scDict["impressions"].append(row["impressions"] or 0)
                    scDict["position"].append(row["position"] or 0)
                print("successful at %i" % numRows)

            except:
                print("error occurred at %i" % numRows)

            # Add response to dataframe
            df = pd.DataFrame(data=scDict)
            df["clicks"] = df["clicks"].astype("int")
            df["ctr"] = df["ctr"] * 100
            df["impressions"] = df["impressions"].astype("int")
            df["position"] = df["position"].round(2)

            print("Numrows at the start of loop: %i" % numRows)

            try:
                numRows = numRows + len(response["rows"])
            except:
                status = "Finished"

            print("Numrows at the end of loop: %i" % numRows)
            if numRows % maxRows != 0:
                status = "Finished"

        start_date += delta
        print("Start date at end: %s" % start_date)
    return df
