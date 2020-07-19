# formula1

There is a lot of information and data on the internet that can ideally be used to gain insights into the sport. 
The aim of this project is to bring some of this information into one place for use in analytical projects. 

This was my first attempt at scraping a website for data. As for the process, it turns out to be quite a slow algorithm, and as time goes on, 
I will make changes to the code to improve its performance. 

The main source of information for the race meeting results is the official [Formula 1 website](www.formula1.com).
The table url's can be accessed with 3 parameters:
* The **year** of the race
  * the website has results dating back to 1950, although there are completeness issues and race weekend structure changes to deal with here. This is discussed later. 
* The **meetingKey** of the race (in the format *number/country*)
  * This is likely an internal key used to by the developers to store race results.
* The **resultType**
  * The options here are race, qualifying and practice results, starting grid, pit stop summary & fastest lap. 

The url has the structure www.formula1.com/en/results.html/year/races/meetingKey/resultType.html
