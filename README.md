# ha-jemenaoutlook

This is a [Home Assistant](https://home-assistant.io) sensor component to retrieve information from the [Jemena Electricity Outlook](https://electricityoutlook.jemena.com.au/) website, they are an electricity distributor within Victoria, Australia.

This component will retrieve your electricity usage details from their website, and only cover a limited area around the northern and north western suburbs of Melbourne, Victoria.

To use this component you will need to register for an account via the Electricity Outlook website.

If Jemena are not your electricity distributor then this will be of no use to you.

The component will only retrieve Yesterdays usage, which will also retrieve the previous days if you wish do do some other comparisions. It could easily be extended to retrieve weekly, monthly or seasonal figures as well. (I haven't got that far yet)

The component is based on an older version of the [Hydro-Québec](https://home-assistant.io/components/sensor.hydroquebec/) energy sensor which is part fo the standard Home Assistant components. Thank you to the writer of that component it helpd a lot.

This component is not endorsed by Jemena, nor have a I asked for their endorsement.

## Installing the component

Copy the included file 'jemenaoutlook.py' to the sensor directory within custom_components directory where the configuration for your installation of home assistant sits. The custom_components directory does not exist in default installation state will will need to be created if it does not already exist.

```
<homeassistant-user-configuration-directory>/custom_components/sensor/jemenaoutlook.py
```
For me this is :-
```
/home/ha/.homeassistant/custom_components/sensor/jemenaoutlook.py
```

## Configuring the sensor

```
# Example configuration.yaml entry

sensor:
  - platform: jemenaoutlook
    username: MYUSERNAME
    password: MYPASSWORD
    monitored_variables:
      - supply_charge
      - weekday_peak_cost
      - weekday_offpeak_cost
      - weekday_shoulder_cost
      - controlled_load_cost
      - weekend_offpeak_cost
      - single_rate_cost
      - generation_cost
      - yesterday_user_type
      - yesterday_usage
      - yesterday_consumption
      - yesterday_consumption_peak
      - yesterday_consumption_offpeak
      - yesterday_consumption_shoulder
      - yesterday_consumption_controlled_load
      - yesterday_generation
      - yesterday_cost_total
      - yesterday_cost_consumption
      - yesterday_cost_generation
      - yesterday_cost_difference
      - yesterday_percentage_difference
      - yesterday_difference_message
      - yesterday_consumption_difference
      - yesterday_consumption_change
      - yesterday_suburb_average
      - previous_day_usage
      - previous_day_consumption
      - previous_day_generation
      - this_week_user_type
      - this_week_usage
      - this_week_consumption
      - this_week_consumption_peak
      - this_week_consumption_offpeak
      - this_week_consumption_shoulder
      - this_week_consumption_controlled_load
      - this_week_generation
      - this_week_cost_total
      - this_week_cost_consumption
      - this_week_cost_generation
      - this_week_cost_difference
      - this_week_percentage_difference
      - this_week_difference_message
      - this_week_consumption_difference
      - this_week_consumption_change
      - this_week_suburb_average
      - last_week_usage
      - last_week_consumption
      - last_week_generation
      - this_month_user_type
      - this_month_usage
      - this_month_consumption
      - this_month_consumption_peak
      - this_month_consumption_offpeak
      - this_month_consumption_shoulder
      - this_month_consumption_controlled_load
      - this_month_generation
      - this_month_cost_total
      - this_month_cost_consumption
      - this_month_cost_generation
      - this_month_cost_difference
      - this_month_percentage_difference
      - this_month_difference_message
      - this_month_consumption_difference
      - this_month_consumption_change
      - this_month_suburb_average
      - last_month_usage
      - last_month_consumption
      - last_month_generation
```

**Configuration variables:**

- **username** (Required): Username used to log into the Jemena Electricity Outlook website.
- **password** (Required): Password used to log into the Jemena Electricity Outlook website
- **monitored_variables** array (Required): Variables to monitor.
    - **supply_charge** (AUD): **\*\*\*** Daily supply charge to properly
    - **weekday_peak_cost** (AUD): **\*\*\*** Cost per kilowatt hour for peak usage
    - **weekday_offpeak_cost** (AUD): **\*\*\*** Cost per kilowatt hour for offpeak usage
    - **weekday_shoulder_cost** (AUD): **\*\*\*** Cost per kilowatt hour for shoulder usage
    - **controlled_load_cost** (AUD): **\*\*\*** Cost per kilowatt hour for controlled load usage
    - **weekend_offpeak_cost** (AUD): **\*\*\*** Cost per kilowatt hour for weekend offpeak usage
    - **single_rate_cost** (AUD): **\*\*\*** Cost per kilowatt hour for single rate usage
    - **generation_cost** (AUD): **\*\*\*** Amount paid per kilowatt hour feed into the grid
    - **yesterday_user_type** (text): Type of grid user [consumer | generator]
    - **yesterday_usage** (kwh): Net consumption of power usage for yesterday all consumption type - generation
    - **yesterday_consumption** (kwh): Total of consuption for yesterday
    - **yesterday_consumption_peak** (kwh): Total peak consumption for yesterday
    - **yesterday_consumption_offpeak** (kwh): Total offpeak consumption for yesterday
    - **yesterday_consumption_shoulder** (kwh): Total shoulder consumption for yesterday
    - **yesterday_consumption_controlled_load** (kwh): Total controlled load consumption for yesterday
    - **yesterday_generation** (kwh): total of generated electricity feed into the grid for yesterday
    - **yesterday_cost_total** (AUD): **\*\*\***Total cost of new consumption for yesterday (concumption - generation) (does not include daily supply)
    - **yesterday_cost_consumption** (AUD): **\*\*\***Total cost of consumption for yesterday (does not include daily supply)
    - **yesterday_cost_generation** (AUD): **\*\*\***Total cost of generated electricity feed into the grid.
    - **yesterday_cost_difference** (AUD): **\*\*\***Difference in cost from previous day
    - **yesterday_percentage_difference** (%): percentage increase in net consumption compared to previous day
    - **yesterday_difference_message** (text): Message displayed in Electicity Outlook to describe differnce from previous day
    - **yesterday_consumption_difference** (KWH): difference in kilowatt hours of net consumption to previous day
    - **yesterday_consumption_change** (text): One of increase or decrease
    - **yesterday_suburb_average** (kwh): Average net consumption for entire suburb
    - **previous_day_usage** (kwh): Net consumption for previous day previous to Yesterday (2 days ago)
    - **previous_day_consumption** (kwh): Consumption for previous day previous to Yesterday (2 days ago)
    - **previous_day_generation** (kwh): Generation for previous day previous to Yesterday (2 days ago) feed into grid
    - this_week_user_type
    - this_week_usage
    - this_week_consumption
    - this_week_consumption_peak
    - this_week_consumption_offpeak
    - this_week_consumption_shoulder
    - this_week_consumption_controlled_load
    - this_week_generation
    - this_week_cost_total
    - this_week_cost_consumption
    - this_week_cost_generation
    - this_week_cost_difference
    - this_week_percentage_difference
    - this_week_difference_message
    - this_week_consumption_difference
    - this_week_consumption_change
    - this_week_suburb_average
    - last_week_usage
    - last_week_consumption
    - last_week_generation
    - this_month_user_type
    - this_month_usage
    - this_month_consumption
    - this_month_consumption_peak
    - this_month_consumption_offpeak
    - this_month_consumption_shoulder
    - this_month_consumption_controlled_load
    - this_month_generation
    - this_month_cost_total
    - this_month_cost_consumption
    - this_month_cost_generation
    - this_month_cost_difference
    - this_month_percentage_difference
    - this_month_difference_message
    - this_month_consumption_difference
    - this_month_consumption_change
    - this_month_suburb_average
    - last_month_usage
    - last_month_consumption
    - last_month_generation


\*** For the cost based variables to be reported correctly you must setup your account with your current tarrif from your electricity retailer. These values can be obtained from your latest electricity bill. 

