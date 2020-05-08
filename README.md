> **Notes**
> 
> 26/03/2020 - Added Marzana hospital for the first time
>
> 27/03/2020 - Added Ospedale di comunità Villa Maria - Padova for the first time
>
> 28/03/2020 - Added Casa di cura Villa Maria - Padova for the first time
>
> 29/03/2020 - Added ODC Belluno for the first time
>
> 31/03/2020 - Added new categories negativizzati virologici, attualmente positivi, totale decessi
>
> 01/04/2020 - Added new hospitals Adria, Ormelle, Vedelago, Rizzola
>
> 03/04/2020 - Added new hospitals Marostica and different tables for health care centers
>
> 03/04/2020 - Switching to accented chars
>
> 17/04/2020 - Reports are now only at 8:00 AM
>
> 04/05/2020 - Reports are now back at 17:00
>
> 08/05/2020 - new table format

## Repository structure

The repository is organized with the following folders:

* `raw_data` contains all raw data extracted and manually pre-processed to generate the dataset. 
  See the inner [README](raw_data/README.md) for more detail on the extraction process

* `csv_data` contains the cvs files of the dataset

* `json_data` contains the json representation of the dataset

## Available data

There are two major sources of data:

* The daily positive persons and those in isolation (`provinces`), broken down by city (actually, by city of residence, so there is a small amount of persons accounted from other cities outside the region)

* The daily statistics for all the hospitals of the regions (`hospitals`). Those include:
  * daily hospitalized persons in non critical conditions;
  * daily persons in intensive care 
  * number of people discharged since the beginning (cumulative info)
  * number of deaths since the beginning (cumulative info)

## Data source

The data has been collected mostly from the daily reports by Regione Veneto that can be found on most local newspapers:

* L'Arena [daily updates](https://www.larena.it/territori/citt%C3%A0/verona-81-nuovi-casi-e-17-morti-nelle-ultime-24-ore-1.7976616)

* [Il Giornale di Vicenza](https://www.ilgiornaledivicenza.it/) 