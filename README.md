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
      - yesterday_cost_total
      - yesterday_cost_consumption
      - yesterday_cost_generation
      - cost_difference
      - cost_difference_message
      - kwh_percentage_difference
      - yesterday_total_usage
      - yesterday_total_consumption
      - yesterday_total_consumption_peak
      - yesterday_total_consumption_offpeak
      - yesterday_total_consumption_shoulder
      - yesterday_total_consumption_controlled_load
      - yesterday_total_generation
      - yesterday_suburb_average
      - previous_total_usage
      - previous_total_consumption
      - previous_total_generation
```

**Configuration variables:**

- **username** (Required): Username used to log into the Jemena Electricity Outlook website.
- **password** (Required): Password used to log into the Jemena Electricity Outlook website
- **monitored_variables** array (Required): Variables to monitor.
  - **yesterday_cost_total** ($): \*** Total Nett cost of energy usage Yesterday
  - **yesterday_cost_consumption** ($): \*** Total cost of consumed energy for Yesterday
  - **yesterday_cost_generation** ($): \*** Total rebate of generated energy for Yesterday
  - **cost_difference** ($): \*** Cost increase or decrease in comparision to previous day 
  - **cost_difference_message** (text): \*** A text message with difference from previous day
  - **kwh_percentage_difference** (%): Total rebate of generated energy for Yesterday  
  - **yesterday_total_usage** (kwh): Total Nett energy usage for Yesterday (Consumption - Generation)
  - **yesterday_total_consumption** (kwh) : Total consumption usage for Yesterday (Peak + Offpeak + Shoulder + Controlled_Load)
  - **yesterday_total_consumption_peak** (kwh) : Total peak energy usage for Yesterday
  - **yesterday_total_consumption_offpeak** (kwh) : Total off peak energy usage for Yesterday
  - **yesterday_total_consumption_shoulder** (kwh) : Total shoulder energy usage for Yesterday
  - **yesterday_total_consumption_controlled_load** (kwh) : Total controlled load energy usage for Yesterday
  - **yesterday_total_generation** (kwh) : Total energy generation feed into the Grid for Yesterday
  - **previous_total_usage** (kwh) : Total Nett energy usage for day previous to Yesterday
  - **previous_total_consumption** (kwh) : Total energy consumption usage for day previous to Yesterday
  - **previous_total_generation** (kwh) : Total energy generation feed into grid for day previous to Yesterday
  - **yesterday_suburb_average** (kwh) : Your suburbs average consumption

\*** For the cost based variables to be reported correctly you must setup your account with your current tarrif from your electricity retailer. These values can be obtained from your latest electricity bill. 

