# Raw data

This directory contains the raw data used to extract information.

The main source are the pdf files released by the Veneto Region everyday in the afternoon (at around 17:00 CET).
Note that there are usually two daily releases, in the morning and in the afternoon. 
Here, unless otherwise specified, the information are always based on the afternoon briefing.


## PDF reports

These are stored in `pdf` and have the following naming convention: `YYYYMMDDhHH.pdf`, where:

* `YYYY` is the year (4 digits)
* `MM` is the month (2 digits)
* `DD` is the day of the month (2 digits)
* `HH` is the hour of the release (2 digits, 0-24 format)

The pdf is usually structured with 2 tables:

* the first table gives the current positive case by province. 
  Starting from March 17th also the number of people in isolation is included.
  
* the second table gives some statistics for the hospitals.
  Statistics include: 
  * daily hospitalized persons in non critical conditions;
  * daily persons in intensive care 
  * number of people discharged since the beginning (cumulative info)
  * number of deaths since the beginning (cumulative info)
  * for some of these, the delta w.r.t. the previous day is given


## Tabula extraction

The original pdf have been processed with Tabula (https://tabula.technology/) to extract a cvs representation of the tables on the pdf.
The raw csv can be found in `tabula`


## Raw csv files

Each Tabula file has been manually processed to generate two cvs files, one for each table of the original pdf.

### cases csv files

The content of the first table can be found in the cvs files named with the following convention `casesYYYYMMDD.cvs` where the data follow the same convention as the pdf file.
Note that some minor cleaning and fixing has been done w.r.t. the Tabula files.

### hospitals csv files

The content of the second table can be found in the cvs files named with the following convention `hospitalsYYYYMMDD.cvs` where the data follow the same convention as the pdf file.
Note that some minor cleaning and fixing has been done w.r.t. the Tabula files.