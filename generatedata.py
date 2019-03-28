import random
import logging
import os
import time
import sys


#BUILT TO RUN ON A LINUX MACHINE WITH PYTHON 3.6

#NOTE THIS SIMULATION DOES NOT INCLUDE THE EQUIPMENT FOR PROCESSING THE TIRES, THE CUBING UNITS, THE VALVES AND OTHER
#SENSORS THAT WILL BE PRESENT THROUGHOUT THE PLANT, EMISSIONS DATA FOR TURBINES, MSW DRYER, VIDEO STREAMS, THE ORGANICS
#PROCESSING LINES, OR OTHER ANCILLARY POINTS OF DATA COLLECTION FOR THE FACILITY.

# This establishes a scenario to allow for the probability of different conditions to exist as it will in an actual
# plant
class Msw_Weight():

    def generate_data(self):
        equip_name = 'MSW_Trucks_Receiving_Scale'
        scenario_select = random.randint(1, 100)
        # This is the green condition scenario for everything in its ideal range
        if scenario_select <= 70:
            status_indicator = 'GREEN'
            mt5_trucks = random.randint(10, 11)
            mt25_trucks = random.randint(14, 15)
            mt20B_trucks = random.randint(2, 3)
            truck_num_t = mt5_trucks + mt25_trucks + mt20B_trucks
            msw_weight_total = (mt5_trucks * 5) + (mt25_trucks * 25) + (mt20B_trucks * 20)

        # This is the yellow condition scenario for a warning of an issue being present
        elif scenario_select >= 71 & scenario_select <= 90:
            status_indicator = 'YELLOW'
            mt5_trucks = random.randint(1, 9)
            mt25_trucks = random.randint(1, 13)
            mt20B_trucks = 1
            truck_num_t = mt5_trucks + mt25_trucks + mt20B_trucks
            msw_weight_total = (mt5_trucks * 5) + (mt25_trucks * 25) + (mt20B_trucks * 20)
    # This is the red condition scenario for inoperable or dangerous data readings
        else:
            status_indicator = 'RED'
            mt5_trucks = 0
            mt25_trucks = 0
            mt20B_trucks = 0
            truck_num_t = mt5_trucks + mt25_trucks + mt20B_trucks
            msw_weight_total = (mt5_trucks * 5) + (mt25_trucks * 25) + (mt20B_trucks * 20)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        msw_scale_out = {'equip_name':equip_name,
                         'total_number_of_trucks_received': truck_num_t,'total_msw_received': msw_weight_total,
                         'trucks_weighing_5_metric_tons': mt5_trucks,'trucks_weighing_25_metric_tons': mt25_trucks,
                         'trucks_weighing_20_metric_tons_of_biomass':mt20B_trucks}
        return msw_scale_out



# Loads the scenarios for GYR conditions
class Tdf_Trucks_Received():

    def generate_tire_data(self):
        equip_name = 'TDF_Trucks_Receiving_Scale'
        scenario_select2 = random.randint(1, 100)

        # Green condition
        if scenario_select2 <=80:
            status_indicator = 'GREEN'
            truck_Tdf_num = random.randint(3, 4)
            truck_tdf_num_T = truck_Tdf_num
            tdf_weight_total = (truck_tdf_num_T * 30)

        # yellow condition
        elif scenario_select2 >= 81 & scenario_select2 <= 90:
            status_indicator = 'YELLOW'
            truck_Tdf_num = random.randint(1, 2)
            truck_tdf_num_T = truck_Tdf_num
            tdf_weight_total = (truck_tdf_num_T * 30)

        # Red condition
        else:
            status_indicator = 'RED'
            truck_Tdf_num = 0
            truck_tdf_num_T = truck_Tdf_num
            tdf_weight_total = (truck_tdf_num_T * 30)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        tdf_scale_out = {'equip_name':equip_name,
                         'number of trucks received': truck_tdf_num_T, 'total tdf received': tdf_weight_total}
        return tdf_scale_out


class Msw_1_Shredder():

    def generate_shredder_1_data(self):
        equip_name = 'MSW_Primary_Shredder'
        scenario_select3 = random.randint(1, 100)

        # Green condition
        if scenario_select3 <= 85:
            status_indicator = 'GREEN'
            feed_rate = random.uniform(19.64, 24)
            shaft_speed = random.randint(16, 40)
            oil_temperatur = random.randint(5, 35)
            voltage = random.randint(400, 460)

        # Yellow condition, with independent probabilities for results to be either high or low from the optimal range
        elif scenario_select3 >=86 & scenario_select3 <=95:
            status_indicator = 'YELLOW'
            low_hi_sel = random.randint(1, 4)
            if low_hi_sel >=1 <=2:
                feed_rate = random.randint(1, 19)
                shaft_speed = random.randint(1, 15)
                oil_temperatur = random.uniform(1,4.95)
                voltage = random.uniform(350, 399.99)
            else:
                feed_rate = random.randint(24, 42)
                shaft_speed = random.randint(41, 50)
                oil_temperatur = random.randint(36, 72)
                voltage = random.randint(461, 500)
        # Red conditions with the probability of high low readings for faults
        else:
            status_indicator = 'RED'
            feed_rate = 0
            shaft_speed = 0
            oil_temperatur = random.randint(0, 80)
            volt_scen = random.randint(1, 2)
            if volt_scen(1):
                voltage = random.randint(1, 350)
            else:
                voltage = random.randint(510, 560)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        msw_shredder_1_out = {'equip_name':equip_name,'feed rate': feed_rate,
                              'shaft_speed': shaft_speed, 'oil temperature': oil_temperatur,'voltage': voltage}
        return msw_shredder_1_out


class Magnet():

    def generate_magnet_data(self):
        equip_name = 'Ferrous_Metals_Separation'
        pre_sort_weight = random.uniform(19.62, 19.64)
        scenario_select4 = random.randint(1, 100)

        # Green condition
        if scenario_select4 <=90:
            status_indicator = 'GREEN'
            removed = random.uniform(0.03, 0.04)
            post_sort_weight = (pre_sort_weight - removed)

        # Yellow condition
        elif scenario_select4 >=91 & scenario_select4 <=98:
            status_indicator = 'YELLOW'
            removed = random.uniform(0.01, 0.02)
            post_sort_weight = (pre_sort_weight - removed)
        # Red condition
        else:
            status_indicator = 'RED'
            removed = 0
            post_sort_weight = (pre_sort_weight - removed)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        magnet_out = {'equip_name':equip_name,'pre sort weight': pre_sort_weight,
                      'weight removed': removed, 'post sort weight': post_sort_weight}
        return magnet_out

# Next is the sifter which inherits the weight data from the magnet above to maintain consistency.
class sifter():

    def generate_sifter_data(Magnet):
        equip_name = 'MSW_Sifter'
        scenario_select5 = random.randint(1, 100)

        # Green scenario
        if scenario_select5 <=85:
            status_indicator = 'GREEN'
            removed = random.uniform(0.3, 0.7)
            pre_sort_weight_sift = random.uniform(19.4, 19.6)
            oil_pressure = random.randint(40, 50)
            gearbox_rpm = random.randint(725, 775)
            motor_rpm = random.randint(1450, 1500)
            motor_voltage = random.randint(198, 208)
            motor_amps = random.randint(139, 149)
            post_sort_weight = (pre_sort_weight_sift - removed)

        # Yellow scenario with high/low variables independant of one another for data readings back to the NOC
        elif scenario_select5 >=86 & scenario_select5 <= 96:
            status_indicator = 'YELLOW'
            pre_sort_weight_sift = random.uniform(19.4, 19.6)
            removed = random.uniform(0.09, 0.2)
            oil_pressure_var = random.randint(1, 2)
            if oil_pressure_var==1:
                oil_pressure = random.randint(26, 39)
            else:
                oil_pressure = random.randint(51, 64)
            gearbox_rpm_var = random.randint(1, 2)
            if gearbox_rpm_var==1:
                gearbox_rpm = random.randint(711, 720)
            else:
                gearbox_rpm = random.randint(780, 789)
            motor_rpm_var = random.randint(1, 2)
            if motor_rpm_var==1:
                motor_rpm = random.randint(1351, 1400)
            else:
                motor_rpm = random.randint(1550, 1599)
            motor_voltage_var = random.randint(1, 2)
            if motor_voltage_var==1:
                motor_voltage = random.randint(1, 188)
            else:
                motor_voltage = 209
            motor_amps_var = random.randint(1, 2)
            if motor_amps_var==1:
                motor_amps = random.randint(129, 138)
            else:
                motor_amps = 150
            post_sort_weight = (pre_sort_weight_sift - removed)

        # Red scenario with high/low variables independant of one another for data readings back to the NOC
        else:
            status_indicator = 'RED'
            pre_sort_weight_sift = random.uniform(19.4, 19.6)
            removed = 0
            oil_pressure_var = random.randint(1, 2)
            if oil_pressure_var==1:
                oil_pressure = random.randint(0, 25)
            else:
                oil_pressure = random.randint(65, 90)
            gearbox_rpm_var = random.randint(1, 2)
            if gearbox_rpm_var==1:
                gearbox_rpm = random.randint(0, 710)
            else:
                gearbox_rpm = random.randint(790, 900)
            motor_rpm_var = random.randint(1, 2)
            if motor_rpm_var==1:
                motor_rpm = random.randint(0, 1350)
            else:
                motor_rpm = random.randint(2000, 1600)
            motor_voltage = random.randint(210, 300)
            motor_amps = random.randint(151, 200)
            post_sort_weight = (pre_sort_weight_sift - removed)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        sifter_out = {'equip_name':equip_name,'equip_name':equip_name,'status_indicator':status_indicator,'removed': removed, 'oil pressure': oil_pressure, 'gearbox rpm': gearbox_rpm, 'motor rpm': motor_rpm,
                      'motor voltage ': motor_voltage, 'motor amperage': motor_amps,
                      'weight after sifter': post_sort_weight}
        return sifter_out


# This section is for the spreader which spreads out the MSW before the next stage, and contains the data for all
# potential conditions.
class Spreader():

    def generate_spreader_data(self):
        equip_name = 'MSW_Spreader'
        scenario_select6 = random.randint(1, 100)

        # Green scenario
        if scenario_select6 <=85:
            status_indicator = 'GREEN'
            disk1_rpm = random.randint(1400, 1410)
            disk2_rpm = random.randint(1400, 1410)
            disk_rpm_diff = (disk1_rpm - disk2_rpm)
            motor_rpm = random.randint(1400, 1500)
            motor_voltage = random.randint(220, 230)

        # Yellow scenario with provisions for high and low reading conditinos
        elif scenario_select6 >=86 & scenario_select6 <=95:
            status_indicator = 'YELLOW'
            disk_rpm_var = random.randint(1, 2)
            if disk_rpm_var ==1:
                disk1_rpm = random.randint(1384, 1399)
                disk2_rpm = random.randint(1369, 1384)
                disk_rpm_diff = (disk1_rpm - disk2_rpm)
                motor_rpm = random.randint(1369, 1399)
                motor_voltage = random.randint(201, 221)
            else:
                disk1_rpm = random.randint(1511, 1525)
                disk2_rpm = random.randint(1525, 1540)
                disk_rpm_diff = (disk1_rpm - disk2_rpm)
                motor_rpm = random.randint(1510, 1545)
                motor_voltage = random.randint(230, 234)

        # Red condition with provisions for high, low, and non operational settings
        else:
            status_indicator = 'RED'
            disk_rpm_var = random.randint(1, 3)
            if disk_rpm_var==1:
                disk1_rpm = random.randint(1350, 1380)
                disk2_rpm = random.randint(1330, 1350)
                disk_rpm_diff = (disk1_rpm - disk2_rpm)
                motor_rpm = random.randint(1320, 1380)
                motor_voltage = random.randint(0, 200)
            elif disk_rpm_var==2:
                disk1_rpm = random.randint(1550, 1570)
                disk2_rpm = random.randint(1570, 1590)
                disk_rpm_diff = (disk1_rpm - disk2_rpm)
                motor_rpm = random.randint(1550, 1600)
                motor_voltage = random.randint(235, 300)
            else:
                disk1_rpm = 0
                disk2_rpm = 0
                disk_rpm_diff = 0
                motor_rpm = 0
                motor_voltage = random.randint(0, 300)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        spreader_out = {'equip_name':equip_name,'disk 1 rpm': disk1_rpm, 'disk 2 rpm': disk2_rpm, 'difference in rpm': disk_rpm_diff,
                        'motor rpm': motor_rpm, 'motor voltage': motor_voltage}
        return spreader_out


# This section is for the eddy current separator to remove all non ferrous metals. This block takes in data for
# the weight of the MSW from the previous seperation mechanism to show sorting is still occuring.
class Eddy_Current():

    def generate_eddy_current_data(self):
        equip_name = 'Eddy_Current_separator'
        # Probability generator to select a scenario
        eddy_current_scenario7 = random.randint(1, 100)
        #print('Eddy Current Separation Information')
        # Green condition for eddy current seperator with 88% chance of occuring
        if eddy_current_scenario7 <=88:
            status_indicator = 'GREEN'
            pre_sort_weight_eddy_current = random.uniform(18.8,19.1)
            belt_drive_motor_output = random.uniform(3.5, 4)
            pole_drive_motor_output = random.uniform(5, 5.5)
            material_removed = random.uniform(0.08, 0.18)
            materail_remaining = (pre_sort_weight_eddy_current - material_removed)

        # Yellow condition for eddy current seperator with 8% chance of occuring
        elif eddy_current_scenario7 >=89 & eddy_current_scenario7  <=96:
            status_indicator = 'YELLOW'
            # low high value selection variable
            eddy_current_var = random.randint(1, 2)
            #print('Yellow condition')
            # low readings
            if eddy_current_var==1:
                pre_sort_weight_eddy_current = random.uniform(18.8,19.1)
                belt_drive_motor_output = random.uniform(1.50, 3.49)
                pole_drive_motor_output = random.uniform(1, 4.90)
                material_removed = random.uniform(0.04, 0.07)
                materail_remaining = (pre_sort_weight_eddy_current - material_removed)
            # high readings
            else:
                pre_sort_weight_eddy_current=random.uniform(18.8,19.1)
                belt_drive_motor_output = random.uniform(4.1, 6.4)
                pole_drive_motor_output = random.uniform(5.5, 7.9)
                material_removed = random.uniform(0.04, 0.07)
                materail_remaining = (pre_sort_weight_eddy_current - material_removed)
        # Red condition for eddy current seperator with 4% chance of occuring
        else:
            status_indicator = 'RED'
            # variable for high, low, and not running status
            eddy_current_var_r = random.randint(1, 3)
            #print('Red condition')
            # low readings
            if eddy_current_var_r==1:
                pre_sort_weight_eddy_current = random.uniform(18.8,19.1)
                belt_drive_motor_output = random.randint(0, 1.49)
                pole_drive_motor_output = random.randint(0, 0.99)
                material_removed = random.randint(0, 0.03)
                materail_remaining = (pre_sort_weight_eddy_current - material_removed)
            # high readings
            elif eddy_current_var_r==2:
                pre_sort_weight_eddy_current = random.uniform(18.8, 19.1)
                belt_drive_motor_output = random.randint(6.5, 8)
                pole_drive_motor_output = random.randint(8, 8.5)
                material_removed = random.randint(0.04, 0.07)
                materail_remaining = (pre_sort_weight_eddy_current - material_removed)
            # non operational readings
            else:
                #print('Eddy current separation not operational')
                pre_sort_weight_eddy_current = random.uniform(18.8,19.1)
                belt_drive_motor_output = 0
                pole_drive_motor_output = 0
                material_removed = 0
                materail_remaining = pre_sort_weight_eddy_current
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        eddy_current_out = {'equip_name':equip_name,'belt drive motor output': belt_drive_motor_output,
                            'pole drive motor output': pole_drive_motor_output, 'material removed': material_removed,
                            'material remaining': materail_remaining}
        return eddy_current_out


# first RDF pyrolysis unit data output, data may be different for each unit, and temperatures vary for RDF
# and TDF units.
class Msw_Pyrolysis_1():

    def generate_data(self):
        equip_name = 'RED_Pyrolysis_Unit_1'
        # first pyrolysis unit condition probability generator
        pyrolysis1_var = random.randint(1, 100)
        # green condition with a probability of 70% of occuring
        if pyrolysis1_var <=70:
            status_indicator = 'GREEN'
            gas_discharge = random.randint(2, 3)
            second_scrub_temp = random.randint(100, 120)
            third_scrub_temp = random.randint(50, 70)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure = random.randint(-4, -2)
            feed_rate = random.uniform(0.95, 1.05)
            gas_consumption = random.uniform(222.55, 242.55)
            air_fuel_ratio = random.randint(25, 35)
            flue_gas_volume = random.randint(95975, 96175)
            internal_temperature = random.randint(1032, 1072)

        # yellow condition with a 20% chance of occuring
        elif pyrolysis1_var >=71 & pyrolysis1_var <=90:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate.
            gas_discharge_var = random.randint(1, 2)
            if gas_discharge_var==1:
                gas_discharge = random.uniform(0.01, 1.19)
            else:
                gas_discharge = random.uniform(3.1, 4.9)
            second_scrub_temp_var = random.randint(1,2)
            if second_scrub_temp_var ==1:
                second_scrub_temp = random.uniform(121, 139.9)
            else:
                second_scrub_temp = random.uniform(91.9, 109.9)
            third_scrub_temp = random.randint(71, 89)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure_var = random.randint(1, 2)
            if retort_pressure_var==1:
                retort_pressure = random.uniform(-1.9, 0)
            else:
                retort_pressure = random.uniform(-5.9, -4.1)
            feed_rate_var = random.randint(1, 2)
            if feed_rate_var==1:
                feed_rate = random.uniform(0.51, 0.94)
            else:
                feed_rate = random.uniform(1.06, 1.99)
            gas_consumption_var = random.randint(1, 2)
            if gas_consumption_var==1:
                gas_consumption = random.uniform(212.56, 222.54)
            else:
                gas_consumption = random.uniform(242.56, 252.54)
            air_fuel_ratio_var = random.randint(1, 2)
            if air_fuel_ratio_var==1:
                air_fuel_ratio = random.uniform(20.1, 25.1)
            else:
                air_fuel_ratio = random.uniform(35.1, 39.9)
            flue_gas_volume_var = random.randint(1, 2)
            if flue_gas_volume_var==1:
                flue_gas_volume = random.randint(95776, 95974)
            else:
                flue_gas_volume = random.randint(96176, 96376)
            internal_temperature_var = random.randint(1, 2)
            if internal_temperature_var==1:
                internal_temperature = random.randint(993, 1031)
            else:
                internal_temperature = random.randint(1073, 1111)

        # red condition with a probability of 10% of this occuring
        else:
            status_indicator = 'RED'
            # variable to determine if the unit is operational or giving bad readings
            operational_or_not_var = random.randint(1, 4)
            # non operational readings with internal temperature set at ambient air temperature
            if operational_or_not_var == 4:
                #print('Unit down')
                gas_discharge = 0
                second_scrub_temp = 0
                third_scrub_temp = 0
                temperature_change_scrub = 0
                retort_pressure = 0
                feed_rate = 0
                gas_consumption = 0
                air_fuel_ratio = 0
                flue_gas_volume = 0
                internal_temperature = 60
            else:
                # red condition data
                gas_discharge = random.randint(5, 7)
                second_scrub_temp = random.randint(140, 170)
                third_scrub_temp = random.randint(90, 120)
                temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
                retort_pressure = random.randint(-8, -6)
                # high low variables and data output ranges for red condition, each parameter has its own
                # probability generator
                feed_rate_var = random.randint(1, 2)
                if feed_rate_var==1:
                    feed_rate = random.randint(2, 3)
                else:
                    feed_rate = random.randint(0.01, 0.5)
                gas_consumption_var = random.randint(1, 2)
                if gas_consumption_var==1:
                    gas_consumption = random.uniform(1, 212.50)
                else:
                    gas_consumption = random.uniform(252.55, 300)
                air_fuel_ratio_var = random.randint(1, 2)
                if air_fuel_ratio_var==1:
                    air_fuel_ratio = random.randint(1, 20)
                else:
                    air_fuel_ratio = random.randint(40, 60)
                flue_gas_volume_var = random.randint(1, 2)
                if flue_gas_volume_var==1:
                    flue_gas_volume = random.randint(96377, 98377)
                else:
                    flue_gas_volume = random.randint(93973, 95973)
                internal_temperature_var = random.randint(1, 2)
                if internal_temperature_var==1:
                    internal_temperature = random.randint(60, 992)
                else:
                    internal_temperature = random.randint(1112, 1900)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        rdf_1_out = {'equip_name':equip_name,'gas discharge': gas_discharge, 'second scrub temp': second_scrub_temp,
                     'third scrub temp': third_scrub_temp, 'retort pressure': retort_pressure,
                     'feed rate': feed_rate,
                     'gas consumption': gas_consumption, 'air fuel ratio': air_fuel_ratio,
                     'flue gas volume': flue_gas_volume, 'internal temperature': internal_temperature,
                     'temperature change scrub': temperature_change_scrub}
        return rdf_1_out


# second RDF pyrolysis unit data output, data may be different for each unit, and temperatures vary for RDF
# and TDF units.
class Msw_Pyrolysis_2():

    def generate_data(self):
        equip_name = 'RDF_Pyrolysis_Unit_2'
        #print('MSW Pyrolysis Unit 2')
        # second RDF pyrolysis unit condition probability generator
        pyrolysis2_var = random.randint(1, 100)
        # green condition with a probability of 70% of occuring
        if pyrolysis2_var <=70:
            status_indicator = 'GREEN'
            gas_discharge = random.randint(2, 3)
            second_scrub_temp = random.randint(100, 120)
            third_scrub_temp = random.randint(50, 70)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure = random.randint(-4, -2)
            feed_rate = random.uniform(0.95, 1.05)
            gas_consumption = random.uniform(222.55, 242.55)
            air_fuel_ratio = random.randint(25, 35)
            flue_gas_volume = random.randint(95975, 96175)
            internal_temperature = random.randint(1032, 1072)

        # yellow condition with a 20% chance of occuring
        elif pyrolysis2_var >=71 & pyrolysis2_var <=90:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate.
            gas_discharge_var = random.randint(1, 2)
            if gas_discharge_var==1:
                gas_discharge = random.uniform(0.01, 1.9)
            else:
                gas_discharge = random.uniform(3.1, 4.9)
            second_scrub_temp_var = random.randint
            if second_scrub_temp_var==1:
                second_scrub_temp = random.uniform(121, 139.9)
            else:
                second_scrub_temp = random.uniform(91.9, 109.9)
            third_scrub_temp = random.randint(71, 89)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if retort_pressure_var==1:
                retort_pressure = random.uniform(-1.9, 0.01)
            else:
                retort_pressure = random.uniform(-5.9, -4.1)
            feed_rate_var = random.randint(1, 2)
            if feed_rate_var==1:
                feed_rate = random.uniform(0.51, 0.94)
            else:
                feed_rate = random.uniform(1.06, 1.99)
            gas_consumption_var = random.randint(1, 2)
            if gas_consumption_var==1:
                gas_consumption = random.uniform(212.56, 222.54)
            else:
                gas_consumption = random.uniform(242.56, 252.54)
            air_fuel_ratio_var = random.randint(1, 2)
            if air_fuel_ratio_var==1:
                air_fuel_ratio = random.uniform(20.1, 25.1)
            else:
                air_fuel_ratio = random.uniform(35.1, 39.9)
            flue_gas_volume_var = random.randint(1, 2)
            if flue_gas_volume_var==1:
                flue_gas_volume = random.randint(95776, 95974)
            else:
                flue_gas_volume = random.randint(96176, 96376)
            internal_temperature_var = random.randint(1, 2)
            if internal_temperature_var==1:
                internal_temperature = random.randint(993, 1031)
            else:
                internal_temperature = random.randint(1073, 1111)

        # red condition with a probability of 10% of this occuring
        else:
            status_indicator = 'RED'
            # variable to determine if the unit is operational or giving bad readings
            operational_or_not_var = random.randint(1, 4)
            # non operational readings with internal temperature set at ambient air temperature
            if operational_or_not_var == 4:
                #print('Unit Down')
                gas_discharge = 0
                second_scrub_temp = 0
                third_scrub_temp = 0
                temperature_change_scrub = 0
                retort_pressure = 0
                feed_rate = 0
                gas_consumption = 0
                air_fuel_ratio = 0
                flue_gas_volume = 0
                internal_temperature = 60
            else:
                # red condition data
                gas_discharge = random.randint(5, 7)
                second_scrub_temp = random.randint(140, 170)
                third_scrub_temp = random.randint(90, 120)
                temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
                retort_pressure = random.randint(-8, -6)
                # high low variables and data output ranges for red condition, each parameter has its own
                # probability generator
                feed_rate_var = random.randint(1, 2)
                if feed_rate_var==1:
                    feed_rate = random.randint(2, 3)
                else:
                    feed_rate = random.uniform(0.01, 0.5)
                gas_consumption_var = random.randint(1, 2)
                if gas_consumption_var==1:
                    gas_consumption = random.uniform(1, 212.50)
                else:
                    gas_consumption = random.uniform(252.55, 300)
                air_fuel_ratio_var = random.randint(1, 2)
                if air_fuel_ratio_var==1:
                    air_fuel_ratio = random.randint(1, 20)
                else:
                    air_fuel_ratio = random.randint(40, 60)
                flue_gas_volume_var = random.randint(1, 2)
                if flue_gas_volume_var==1:
                    flue_gas_volume = random.randint(96377, 98377)
                else:
                    flue_gas_volume = random.randint(93973, 95973)
                internal_temperature_var = random.randint(1, 2)
                if internal_temperature_var==1:
                    internal_temperature = random.randint(60, 992)
                else:
                    internal_temperature = random.randint(1112, 1900)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        rdf_2_out = {'equip_name':equip_name,'gas discharge': gas_discharge, 'second scrub temp': second_scrub_temp,
                     'third scrub temp': third_scrub_temp, 'retort pressure': retort_pressure,
                     'feed rate': feed_rate,
                     'gas consumption': gas_consumption, 'air fuel ratio': air_fuel_ratio,
                     'flue gas volume': flue_gas_volume, 'internal temperature': internal_temperature,
                     'temperature change scrub': temperature_change_scrub}
        return rdf_2_out


# third RDF pyrolysis unit data output, data may be different for each unit, and temperatures vary for RDF
# and TDF units.
class Msw_Pyrolysis_3():

    def generate_data(self):
        equip_name = 'RDF_Pyrolysis_Unit_3'
        #print('MSW Pyrolysis Unit 3')
        # third RDF pyrolysis unit condition probability generator
        pyrolysis3_var = random.randint(1, 100)
        # green condition with a probability of 70% of occuring
        if pyrolysis3_var <=70:
            status_indicator = 'GREEN'
            gas_discharge = random.randint(2, 3)
            second_scrub_temp = random.randint(100, 120)
            third_scrub_temp = random.randint(50, 70)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure = random.randint(-4, -2)
            feed_rate = random.uniform(0.95, 1.05)
            gas_consumption = random.uniform(222.55, 242.55)
            air_fuel_ratio = random.randint(25, 35)
            flue_gas_volume = random.randint(95975, 96175)
            internal_temperature = random.randint(1032, 1072)

        # yellow condition with a 20% chance of occuring
        elif pyrolysis3_var >=71 <=90:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate.
            gas_discharge_var = random.randint(1, 2)
            if gas_discharge_var==1:
                gas_discharge = random.uniform(0, 1.9)
            else:
                gas_discharge = random.uniform(3.1, 4.9)
            second_scrub_temp_var = random.randint(1,2)
            if second_scrub_temp_var==1:
                second_scrub_temp = random.uniform(121, 139.9)
            else:
                second_scrub_temp = random.uniform(91.9, 109.9)
            third_scrub_temp = random.randint(71, 89)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if retort_pressure_var==1:
                retort_pressure = random.uniform(-1.9, 0)
            else:
                retort_pressure = random.uniform(-5.9, -4.1)
            feed_rate_var = random.randint(1, 2)
            if feed_rate_var==1:
                feed_rate = random.uniform(0.51, 0.94)
            else:
                feed_rate = random.uniform(1.06, 1.99)
            gas_consumption_var = random.randint(1, 2)
            if gas_consumption_var==1:
                gas_consumption = random.uniform(212.56, 222.54)
            else:
                gas_consumption = random.uniform(242.56, 252.54)
            air_fuel_ratio_var = random.randint(1, 2)
            if air_fuel_ratio_var==1:
                air_fuel_ratio = random.uniform(20.1, 25.1)
            else:
                air_fuel_ratio = random.uniform(35.1, 39.9)
            flue_gas_volume_var = random.randint(1, 2)
            if flue_gas_volume_var==1:
                flue_gas_volume = random.randint(95776,95974)
            else:
                flue_gas_volume = random.randint(96176, 96376)
            internal_temperature_var = random.randint(1, 2)
            if internal_temperature_var==1:
                internal_temperature = random.randint(993, 1031)
            else:
                internal_temperature = random.randint(1073, 1111)

        # red condition with a probability of 10% of this occuring
        else:
            status_indicator = 'RED'
            # variable to determine if the unit is operational or giving bad readings
            operational_or_not_var = random.randint(1, 4)
            # non operational readings with internal temperature set at ambient air temperature
            if operational_or_not_var == 4:
                #print('Unit down')
                gas_discharge = 0
                second_scrub_temp = 0
                third_scrub_temp = 0
                temperature_change_scrub = 0
                retort_pressure = 0
                feed_rate = 0
                gas_consumption = 0
                air_fuel_ratio = 0
                flue_gas_volume = 0
                internal_temperature = 60
            else:
                # red condition data
                gas_discharge = random.randint(5, 7)
                second_scrub_temp = random.randint(140, 170)
                third_scrub_temp = random.randint(90, 120)
                temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
                retort_pressure = random.randint(-8, -6)
                # high low variables and data output ranges for red condition, each parameter has its own
                # probability generator
                feed_rate_var = random.randint(1, 2)
                if feed_rate_var==1:
                    feed_rate = random.randint(2, 3)
                else:
                    feed_rate = random.uniform(0.01, 0.5)
                gas_consumption_var = random.randint(1, 2)
                if gas_consumption_var==1:
                    gas_consumption = random.uniform(1, 212.50)
                else:
                    gas_consumption = random.uniform(252.55, 300)
                air_fuel_ratio_var = random.randint(1, 2)
                if air_fuel_ratio_var==1:
                    air_fuel_ratio = random.randint(1, 20)
                else:
                    air_fuel_ratio = random.randint(40, 60)
                flue_gas_volume_var = random.randint(1, 2)
                if flue_gas_volume_var==1:
                    flue_gas_volume = random.randint(96377, 98377)
                else:
                    flue_gas_volume = random.randint(93973, 95973)
                internal_temperature_var = random.randint(1, 2)
                if internal_temperature_var==1:
                    internal_temperature = random.randint(60, 992)
                else:
                    internal_temperature = random.randint(1112, 1900)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        rdf_3_out = {'equip_name':equip_name,'gas discharge': gas_discharge, 'second scrub temp': second_scrub_temp,
                     'third scrub temp': third_scrub_temp, 'retort pressure': retort_pressure,
                     'feed rate': feed_rate,
                     'gas consumption': gas_consumption, 'air fuel ratio': air_fuel_ratio,
                     'flue gas volume': flue_gas_volume, 'internal temperature': internal_temperature,
                     'temperature change scrub': temperature_change_scrub}
        return rdf_3_out


# fourth RDF pyrolysis unit data output, data may be different for each unit, and temperatures vary for RDF
# and TDF units.
class Msw_Pyrolysis_4():

    def generate_data(self):
        equip_name = 'RDF_Pyrolysis_Unit_4'
        # fourth RDF pyrolysis unit condition probability generator
        pyrolysis4_var = random.randint(1, 100)
        # green condition with a probability of 70% of occuring
        if pyrolysis4_var <=70:
            status_indicator = 'GREEN'
            gas_discharge = random.randint(2, 3)
            second_scrub_temp = random.randint(100, 120)
            third_scrub_temp = random.randint(50, 70)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure = random.randint(-4, -2)
            feed_rate = random.uniform(0.95, 1.05)
            gas_consumption = random.uniform(222.55, 242.55)
            air_fuel_ratio = random.randint(25, 35)
            flue_gas_volume = random.randint(95975, 96175)
            internal_temperature = random.randint(1032, 1072)

        # yellow condition with a 20% chance of occuring
        elif pyrolysis4_var >=71 & pyrolysis4_var <=90:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate.
            gas_discharge_var = random.randint(1, 2)
            if gas_discharge_var==1:
                gas_discharge = random.uniform(0.01, 1.9)
            else:  # this is a pointless comment to see if you are really reading this
                gas_discharge = random.uniform(3.1, 4.9)
            second_scrub_temp_var = random.randint
            if second_scrub_temp_var==1:
                second_scrub_temp = random.uniform(121, 139.9)
            else:
                second_scrub_temp = random.uniform(91.9, 109.9)
            third_scrub_temp = random.randint(71, 89)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if retort_pressure_var==1:
                retort_pressure = random.uniform(-1.9, -0.01)
            else:
                retort_pressure = random.uniform(-5.9, -4.1)
            feed_rate_var = random.randint(1, 2)
            if feed_rate_var==1:
                feed_rate = random.uniform(0.51, 0.94)
            else:
                feed_rate = random.uniform(1.06, 1.99)
            gas_consumption_var = random.randint(1, 2)
            if gas_consumption_var==1:
                gas_consumption = random.uniform(212.56, 222.54)
            else:
                gas_consumption = random.uniform(242.56, 252.54)
            air_fuel_ratio_var = random.randint(1, 2)
            if air_fuel_ratio_var==1:
                air_fuel_ratio = random.uniform(20.1, 25.1)
            else:
                air_fuel_ratio = random.uniform(35.1, 39.9)
            flue_gas_volume_var = random.randint(1, 2)
            if flue_gas_volume_var==1:
                flue_gas_volume = random.randint(95776, 95974)
            else:
                flue_gas_volume = random.randint(96176, 96376)
            internal_temperature_var = random.randint(1, 2)
            if internal_temperature_var==1:
                internal_temperature = random.randint(993, 1031)
            else:
                internal_temperature = random.randint(1073, 1111)

        else:
            status_indicator = 'RED'
            # red condition with a probability of 10% of this occuring
            operational_or_not_var = random.randint(1, 4)
            # non operational readings with internal temperature set at ambient air temperature
            if operational_or_not_var == 4:
                #print('Unit Down')
                gas_discharge = 0
                second_scrub_temp = 0
                third_scrub_temp = 0
                temperature_change_scrub = 0
                retort_pressure = 0
                feed_rate = 0
                gas_consumption = 0
                air_fuel_ratio = 0
                flue_gas_volume = 0
                internal_temperature = 60
            else:
                gas_discharge = random.randint(5, 7)
                second_scrub_temp = random.randint(140, 170)
                third_scrub_temp = random.randint(90, 120)
                temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
                retort_pressure = random.randint(-8, -6)
                # high low variables and data output ranges for red condition, each parameter has its own
                # probability generator
                feed_rate_var = random.randint(1, 2)
                if feed_rate_var==1:
                    feed_rate = random.randint(2, 3)
                else:
                    feed_rate = random.uniform(0.01, 0.5)
                gas_consumption_var = random.randint(1, 2)
                if gas_consumption_var==1:
                    gas_consumption = random.uniform(1, 212.50)
                else:
                    gas_consumption = random.uniform(252.55, 300)
                air_fuel_ratio_var = random.randint(1, 2)
                if air_fuel_ratio_var==1:
                    air_fuel_ratio = random.randint(1, 20)
                else:
                    air_fuel_ratio = random.randint(40, 60)
                flue_gas_volume_var = random.randint(1, 2)
                if flue_gas_volume_var==1:
                    flue_gas_volume = random.randint(96377, 98377)
                else:
                    flue_gas_volume = random.randint(93973, 95973)
                internal_temperature_var = random.randint(1, 2)
                if internal_temperature_var==1:
                    internal_temperature = random.randint(60, 992)
                else:
                    internal_temperature = random.randint(1112, 1900)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        rdf_4_out = {'equip_name':equip_name,'gas discharge': gas_discharge, 'second scrub temp': second_scrub_temp,
                     'third scrub temp': third_scrub_temp, 'retort pressure': retort_pressure,
                     'feed rate': feed_rate,
                     'gas consumption': gas_consumption, 'air fuel ratio': air_fuel_ratio,
                     'flue gas volume': flue_gas_volume, 'internal temperature': internal_temperature,
                     'temperature change scrub': temperature_change_scrub}
        return rdf_4_out


# fifth RDF pyrolysis unit data output, data may be different for each unit, and temperatures vary for RDF
# and TDF units.
class Msw_Pyrolysis_5():

    def generate_data(self):
        equip_name = 'RDF_Pyrolysis_Unit_5'
        # fifth RDF pyrolysis unit condition probability generator
        pyrolysis5_var = random.randint(1, 100)
        # green condition with a probability of 70% of occuring
        if pyrolysis5_var <=70:
            status_indicator = 'GREEN'
            gas_discharge = random.randint(2, 3)
            second_scrub_temp = random.randint(100, 120)
            third_scrub_temp = random.randint(50, 70)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure = random.randint(-4, -2)
            feed_rate = random.uniform(0.95, 1.05)
            gas_consumption = random.uniform(222.55, 242.55)
            air_fuel_ratio = random.randint(25, 35)
            flue_gas_volume = random.randint(95975,96175)
            internal_temperature = random.randint(1032, 1072)

        # yellow condition with a 20% chance of occuring
        elif pyrolysis5_var >=71 & pyrolysis5_var <=90:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate.
            gas_discharge_var = random.randint(1, 2)
            if gas_discharge_var ==1:
                gas_discharge = random.uniform(0.01, 1.9)
            else:
                gas_discharge = random.uniform(3.1, 4.9)
            second_scrub_temp_var = random.randint(1,2)
            if second_scrub_temp_var ==1:
                second_scrub_temp = random.uniform(121, 139.9)
            else:
                second_scrub_temp = random.uniform(91.9, 109.9)
            third_scrub_temp = random.randint(71, 89)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if retort_pressure_var==1:
                retort_pressure = random.uniform(-1.9, 0)
            else:
                retort_pressure = random.uniform(-5.9, -4.1)
            feed_rate_var = random.randint(1, 2)
            if feed_rate_var==1:
                feed_rate = random.uniform(0.51, 0.94)
            else:
                feed_rate = random.uniform(1.06, 1.99)
            gas_consumption_var = random.randint(1, 2)
            if gas_consumption_var==1:
                gas_consumption = random.uniform(212.56, 222.54)
            else:
                gas_consumption = random.uniform(242.56, 252.54)
            air_fuel_ratio_var = random.randint(1, 2)
            if air_fuel_ratio_var==1:
                air_fuel_ratio = random.uniform(20.1, 25.1)
            else:
                air_fuel_ratio = random.uniform(35.1, 39.9)
            flue_gas_volume_var = random.randint(1, 2)
            if flue_gas_volume_var==1:
                flue_gas_volume = random.randint(95776, 95974)
            else:
                flue_gas_volume = random.randint(96176, 96376)
            internal_temperature_var = random.randint(1, 2)
            if internal_temperature_var==1:
                internal_temperature = random.randint(993, 1031)
            else:
                internal_temperature = random.randint(1073, 1111)

        else:
            status_indicator = 'RED'
            # red condition with a probability of 10% of this occuring
            operational_or_not_var = random.randint(1, 4)
            # non operational readings with internal temperature set at ambient air temperature
            if operational_or_not_var == 4:
                #print('Unit not operational')
                gas_discharge = 0
                second_scrub_temp = 0
                third_scrub_temp = 0
                temperature_change_scrub = 0
                retort_pressure = 0
                feed_rate = 0
                gas_consumption = 0
                air_fuel_ratio = 0
                flue_gas_volume = 0
                internal_temperature = 60
            else:
                gas_discharge = random.randint(5, 7)
                second_scrub_temp = random.randint(140, 170)
                third_scrub_temp = random.randint(90, 120)
                temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
                retort_pressure = random.randint(-8, -6)
                # high low variables and data output ranges for red condition, each parameter has its own
                # probability generator
                feed_rate_var = random.randint(1, 2)
                if feed_rate_var==1:
                    feed_rate = random.randint(2, 3)
                else:
                    feed_rate = random.uniform(0.01, 0.5)
                gas_consumption_var = random.randint(1, 2)
                if gas_consumption_var==1:
                    gas_consumption = random.uniform(1, 212.50)
                else:
                    gas_consumption = random.uniform(252.55, 300)
                air_fuel_ratio_var = random.randint(1, 2)
                if air_fuel_ratio_var==1:
                    air_fuel_ratio = random.randint(1, 20)
                else:
                    air_fuel_ratio = random.randint(40, 60)
                flue_gas_volume_var = random.randint(1, 2)
                if flue_gas_volume_var==1:
                    flue_gas_volume = random.randint(96377, 98377)
                else:
                    flue_gas_volume = random.randint(93973, 95973)
                internal_temperature_var = random.randint(1, 2)
                if internal_temperature_var==1:
                    internal_temperature = random.randint(60, 992)
                else:
                    internal_temperature = random.randint(1112, 1900)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        rdf_5_out = {'equip_name':equip_name,'gas discharge': gas_discharge, 'second scrub temp': second_scrub_temp,
                     'third scrub temp': third_scrub_temp, 'retort pressure': retort_pressure,
                     'feed rate': feed_rate,
                     'gas consumption': gas_consumption, 'air fuel ratio': air_fuel_ratio,
                     'flue gas volume': flue_gas_volume, 'internal temperature': internal_temperature,
                     'temperature change scrub': temperature_change_scrub}
        return rdf_5_out


# first TDF pyrolysis unit data output, data may be different for each unit, and temperatures vary for RDF
# and TDF units.
class Tdf_Unit_1():
    def generate_data(self):
        equip_name = 'TDF_Pyrolysis_Unit_1'
        # first TDF pyrolysis unit condition probability generator
        tdf_pyrolysis_1_var = random.randint(1, 100)
        # green condition with a probability of 72% of occuring
        if tdf_pyrolysis_1_var <=72:
            status_indicator = 'GREEN'
            gas_discharge = random.randint(2, 3)
            second_scrub_temp = random.randint(100, 120)
            third_scrub_temp = random.randint(50, 70)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure = random.randint(-4, -2)
            feed_rate = random.uniform(0.95, 1.05)
            gas_consumption = random.uniform(222.55, 242.55)
            air_fuel_ratio = random.randint(25, 35)
            flue_gas_volume = random.randint(95975, 96175)
            internal_temperature = random.randint(937, 977)

        # yellow condition with a 19% chance of occuring
        elif tdf_pyrolysis_1_var >=72 & tdf_pyrolysis_1_var <=91:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate.
            gas_discharge_var = random.randint(1, 2)
            if gas_discharge_var==1:
                gas_discharge = random.uniform(0.01, 1.9)
            else:
                gas_discharge = random.uniform(3.1, 4.9)
            second_scrub_temp_var = random.randint (1,2)
            if second_scrub_temp_var==1:
                second_scrub_temp = random.uniform(121, 139.9)
            else:
                second_scrub_temp = random.uniform(91.9, 109.9)
            third_scrub_temp = random.randint(71, 89)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if retort_pressure_var==1:
                retort_pressure = random.uniform(-1.9, 0.01)
            else:
                retort_pressure = random.uniform(-5.9, -4.1)
            feed_rate_var = random.randint(1, 2)
            if feed_rate_var==1:
                feed_rate = random.uniform(0.51, 0.94)
            else:
                feed_rate = random.uniform(1.06, 1.99)
            gas_consumption_var = random.randint(1, 2)
            if gas_consumption_var==1:
                gas_consumption = random.uniform(212.56, 222.54)
            else:
                gas_consumption = random.uniform(242.56, 252.54)
            air_fuel_ratio_var = random.randint(1, 2)
            if air_fuel_ratio_var==1:
                air_fuel_ratio = random.uniform(20.1, 25.1)
            else:
                air_fuel_ratio = random.uniform(35.1, 39.9)
            flue_gas_volume_var = random.randint(1, 2)
            if flue_gas_volume_var==1:
                flue_gas_volume = random.randint(95776, 95974)
            else:
                flue_gas_volume = random.randint(96176, 96376)
            internal_temperature_var = random.randint(1, 2)
            if internal_temperature_var==1:
                internal_temperature = random.randint(894, 937)
            else:
                internal_temperature = random.randint(977, 1016)

        else:
            status_indicator = 'RED'
            # red condition with a probability of 9% of this occuring
            operational_or_not_var = random.randint(1, 4)
            # non operational readings with internal temperature set at ambient air temperature
            if operational_or_not_var == 4:
                #print('Unit Down')
                gas_discharge = 0
                second_scrub_temp = 0
                third_scrub_temp = 0
                temperature_change_scrub = 0
                retort_pressure = 0
                feed_rate = 0
                gas_consumption = 0
                air_fuel_ratio = 0
                flue_gas_volume = 0
                internal_temperature = 60
            else:
                gas_discharge = random.randint(5, 7)
                second_scrub_temp = random.randint(140, 170)
                third_scrub_temp = random.randint(90, 120)
                temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
                retort_pressure = random.randint(-8, -6)
                # high low variables and data output ranges for red condition, each parameter has its own
                # probability generator
                feed_rate_var = random.randint(1, 2)
                if feed_rate_var==1:
                    feed_rate = random.randint(2, 3)
                else:
                    feed_rate = random.uniform(0.01, 0.5)
                gas_consumption_var = random.randint(1, 2)
                if gas_consumption_var==1:
                    gas_consumption = random.uniform(1, 212.50)
                else:
                    gas_consumption = random.uniform(252.55, 300)
                air_fuel_ratio_var = random.randint(1, 2)
                if air_fuel_ratio_var==1:
                    air_fuel_ratio = random.randint(1, 20)
                else:
                    air_fuel_ratio = random.randint(40, 60)
                flue_gas_volume_var = random.randint(1, 2)
                if flue_gas_volume_var==1:
                    flue_gas_volume = random.randint(96377, 98377)
                else:
                    flue_gas_volume = random.randint(93973, 95973)
                internal_temperature_var = random.randint(1, 2)
                if internal_temperature_var==1:
                    internal_temperature = random.randint(60, 893)
                else:
                    internal_temperature = random.randint(1017, 1800)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        tdf_1_out = {'equip_name':equip_name,'gas discharge': gas_discharge, 'second scrub temp': second_scrub_temp,
                     'third scrub temp': third_scrub_temp, 'retort pressure': retort_pressure,
                     'feed rate': feed_rate,
                     'gas consumption': gas_consumption, 'air fuel ratio': air_fuel_ratio,
                     'flue gas volume': flue_gas_volume, 'internal temperature': internal_temperature,
                     'temperature change scrub': temperature_change_scrub}
        return tdf_1_out


# second TDF pyrolysis unit data output, data may be different for each unit, and temperatures vary for RDF
# and TDF units
class Tdf_Unit_2():

    def generate_data(self):
        equip_name = 'TDF_Pyrolysis_Unit_2'
        #print('TDF Pyrolysis Unit 2')
        # second TDF pyrolysis unit condition probability generator
        tdf_pyrolysis_2_var = random.randint(1, 100)
        # green condition with a probability of 72% of occuring
        if tdf_pyrolysis_2_var <=72:
            status_indicator = 'GREEN'
            #print('Green condition')
            gas_discharge = random.randint(2, 3)
            second_scrub_temp = random.randint(100, 120)
            third_scrub_temp = random.randint(50, 70)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure = random.randint(-4, -2)
            feed_rate = random.uniform(0.95, 1.05)
            gas_consumption = random.uniform(222.55, 242.55)
            air_fuel_ratio = random.randint(25, 35)
            flue_gas_volume = random.randint(95975, 96175)
            internal_temperature = random.randint(937, 977)

        # yellow condition with a 19% chance of occuring
        elif tdf_pyrolysis_2_var >=72 & tdf_pyrolysis_2_var <=91:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate.
            gas_discharge_var = random.randint(1, 2)
            if gas_discharge_var==1:
                gas_discharge = random.uniform(0.01, 1.9)
            else:
                gas_discharge = random.uniform(3.1, 4.9)
            second_scrub_temp_var = random.randint
            if second_scrub_temp_var==1:
                second_scrub_temp = random.uniform(121, 139.9)
            else:
                second_scrub_temp = random.uniform(91.9, 109.9)
            third_scrub_temp = random.randint(71, 89)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if retort_pressure_var==1:
                retort_pressure = random.uniform(-1.9, 0.01)
            else:  # something something comment
                retort_pressure = random.uniform(-5.9, -4.1)
            feed_rate_var = random.randint(1, 2)
            if feed_rate_var==1:
                feed_rate = random.uniform(0.51, 0.94)
            else:
                feed_rate = random.uniform(1.06, 1.99)
            gas_consumption_var = random.randint(1, 2)
            if gas_consumption_var==1:
                gas_consumption = random.uniform(212.56, 222.54)
            else:
                gas_consumption = random.uniform(242.56, 252.54)
            air_fuel_ratio_var = random.randint(1, 2)
            if air_fuel_ratio_var==1:
                air_fuel_ratio = random.uniform(20.1, 25.1)
            else:
                air_fuel_ratio = random.uniform(35.1, 39.9)
            flue_gas_volume_var = random.randint(1, 2)
            if flue_gas_volume_var==1:
                flue_gas_volume = random.randint(95776, 95974)
            else:
                flue_gas_volume = random.randint(96176, 96376)
            internal_temperature_var = random.randint(1, 2)
            if internal_temperature_var==1:
                internal_temperature = random.randint(894, 937)
            else:
                internal_temperature = random.randint(977, 1016)

        else:
            status_indicator = 'RED'
            # red condition with a probability of 9% of this occuring
            operational_or_not_var = random.randint(1, 4)
            # non operational readings with internal temperature set at ambient air temperature
            if operational_or_not_var == 4:
                #print('Unit Down')
                gas_discharge = 0
                second_scrub_temp = 0
                third_scrub_temp = 0
                temperature_change_scrub = 0
                retort_pressure = 0
                feed_rate = 0
                gas_consumption = 0
                air_fuel_ratio = 0
                flue_gas_volume = 0
                internal_temperature = 60
            else:
                gas_discharge = random.randint(5, 7)
                second_scrub_temp = random.randint(140, 170)
                third_scrub_temp = random.randint(90, 120)
                temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
                retort_pressure = random.randint(-8, -6)
                # high low variables and data output ranges for red condition, each parameter has its own
                # probability generator
                feed_rate_var = random.randint(1, 2)
                if feed_rate_var==1:
                    feed_rate = random.randint(2, 3)
                else:
                    feed_rate = random.uniform(0.01, 0.5)
                gas_consumption_var = random.randint(1, 2)
                if gas_consumption_var==1:
                    gas_consumption = random.uniform(1, 212.50)
                else:
                    gas_consumption = random.uniform(252.55, 300)
                air_fuel_ratio_var = random.randint(1, 2)
                if air_fuel_ratio_var==1:
                    air_fuel_ratio = random.randint(1, 20)
                else:
                    air_fuel_ratio = random.randint(40, 60)
                flue_gas_volume_var = random.randint(1, 2)
                if flue_gas_volume_var==1:
                    flue_gas_volume = random.randint(96377, 98377)
                else:
                    flue_gas_volume = random.randint(93973, 95973)
                internal_temperature_var = random.randint(1, 2)
                if internal_temperature_var==1:
                    internal_temperature = random.randint(60, 893)
                else:
                    internal_temperature = random.randint(1017, 1800)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        tdf_2_out = {'equip_name':equip_name,'gas discharge': gas_discharge, 'second scrub temp': second_scrub_temp,
                     'third scrub temp': third_scrub_temp, 'retort pressure': retort_pressure,
                     'feed rate': feed_rate,
                     'gas consumption': gas_consumption, 'air fuel ratio': air_fuel_ratio,
                     'flue gas volume': flue_gas_volume, 'internal temperature': internal_temperature,
                     'temperature change scrub': temperature_change_scrub}
        return tdf_2_out


# third TDF pyrolysis unit data output, data may be different for each unit, and temperatures vary for RDF
# and TDF units
class Tdf_Unit_3():

    def generate_data(self):
        equip_name = 'TDF_Pyrolysis_Unit_3'
        #print('TDF Pyrolysis Unit 3')
        # second TDF pyrolysis unit condition probability generator
        tdf_pyrolysis_3_var = random.randint(1, 100)
        # green condition with a probability of 72% of occuring
        if tdf_pyrolysis_3_var <=72:
            status_indicator = 'GREEN'
            #print('Green condition')
            gas_discharge = random.randint(2, 3)
            second_scrub_temp = random.randint(100, 120)
            third_scrub_temp = random.randint(50, 70)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure = random.randint(-4, -2)
            feed_rate = random.uniform(0.95, 1.05)
            gas_consumption = random.uniform(242.55, 222.55)
            air_fuel_ratio = random.randint(25, 35)
            flue_gas_volume = random.randint(95975, 96175)
            internal_temperature = random.randint(937, 977)

        # yellow condition with a 19% chance of occuring
        elif tdf_pyrolysis_3_var >=72 & tdf_pyrolysis_3_var <=91:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate.
            gas_discharge_var = random.randint(1, 2)
            if gas_discharge_var==1:
                gas_discharge = random.uniform(0.01, 1.9)
            else:
                gas_discharge = random.uniform(3.1, 4.9)
            second_scrub_temp_var = random.randint
            if second_scrub_temp_var==1:
                second_scrub_temp = random.uniform(121, 139.9)
            else:
                second_scrub_temp = random.uniform(91.9, 109.9)
            third_scrub_temp = random.randint(71, 89)
            temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
            retort_pressure_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if retort_pressure_var==1:
                retort_pressure = random.uniform(-1.9, 0.01)
            else:
                retort_pressure = random.uniform(-5.9, -4.1)
            feed_rate_var = random.randint(1, 2)
            if feed_rate_var==1:
                feed_rate = random.uniform(0.51, 0.94)
            else:
                feed_rate = random.uniform(1.06, 1.99)
            gas_consumption_var = random.randint(1, 2)
            if gas_consumption_var==1:
                gas_consumption = random.uniform(212.56, 222.54)
            else:
                gas_consumption = random.uniform(242.56, 252.54)
            air_fuel_ratio_var = random.randint(1, 2)
            if air_fuel_ratio_var==1:
                air_fuel_ratio = random.uniform(20.1, 25.1)
            else:
                air_fuel_ratio = random.uniform(35.1, 39.9)
            flue_gas_volume_var = random.randint(1, 2)
            if flue_gas_volume_var==1:
                flue_gas_volume = random.randint(95776, 95974)
            else:
                flue_gas_volume = random.randint(96176, 96376)
            internal_temperature_var = random.randint(1, 2)
            if internal_temperature_var==1:
                internal_temperature = random.randint(894, 937)
            else:
                internal_temperature = random.randint(977, 1016)

        else:
            status_indicator = 'RED'
            # red condition with a probability of 9% of this occuring
            operational_or_not_var = random.randint(1, 4)
            # non operational readings with internal temperature set at ambient air temperature
            if operational_or_not_var == 4:
                #print('Unit Down')
                gas_discharge = 0
                second_scrub_temp = 0
                third_scrub_temp = 0
                temperature_change_scrub = 0
                retort_pressure = 0
                feed_rate = 0
                gas_consumption = 0
                air_fuel_ratio = 0
                flue_gas_volume = 0
                internal_temperature = 60
            else:
                gas_discharge = random.randint(5, 7)
                second_scrub_temp = random.randint(140, 170)
                third_scrub_temp = random.randint(90, 120)
                temperature_change_scrub = (second_scrub_temp - third_scrub_temp)
                retort_pressure = random.randint(-8, -6)
                # high low variables and data output ranges for red condition, each parameter has its own
                # probability generator
                feed_rate_var = random.randint(1, 2)
                if feed_rate_var==1:
                    feed_rate = random.randint(2, 3)
                else:
                    feed_rate = random.uniform(0.01, 0.5)
                gas_consumption_var = random.randint(1, 2)
                if gas_consumption_var==1:
                    gas_consumption = random.uniform(1, 212.50)
                else:
                    gas_consumption = random.uniform(252.55, 300)
                air_fuel_ratio_var = random.randint(1, 2)
                if air_fuel_ratio_var==1:
                    air_fuel_ratio = random.randint(1, 20)
                else:
                    air_fuel_ratio = random.randint(40, 60)
                flue_gas_volume_var = random.randint(1, 2)
                if flue_gas_volume_var==1:
                    flue_gas_volume = random.randint(96377, 98377)
                else:
                    flue_gas_volume = random.randint(93973, 95973)
                internal_temperature_var = random.randint(1, 2)
                if internal_temperature_var==1:
                    internal_temperature = random.randint(60, 893)
                else:
                    internal_temperature = random.randint(1017, 1800)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        tdf_3_out = {'equip_name':equip_name,'gas discharge': gas_discharge, 'second scrub temp': second_scrub_temp,
                     'third scrub temp': third_scrub_temp, 'retort pressure': retort_pressure, 'feed rate': feed_rate,
                     'gas consumption': gas_consumption, 'air fuel ratio': air_fuel_ratio,
                     'flue gas volume': flue_gas_volume, 'internal temperature': internal_temperature,
                     'temperature change scrub': temperature_change_scrub}
        return tdf_3_out


# This is the class for generating the data from the first turbine and allows for red, green, and yellow
# conditions. This also has the provision for different conditions that the turbine may experience when it is in
# the red condition range
class Turbine_1():

    def generate_data(self):
        equip_name = 'Turbine_1'
        #print('Solar Turbine 1')
        # This is the probability generator for determining which condition the turbine will transmit in the
        # simulation.
        turbine_perf_var = random.randint(1, 100)
        # This is the green condition probability range, which indicates that there is an 85% chance that the data
        # will be within the anticipated range.
        if turbine_perf_var <=85:
            status_indicator = 'GREEN'
            #print('Green Condition')
            voltage_at_genset = random.randint(456, 466)
            lighting_hvac_voltage = random.randint(116, 126)
            genset_rpm = random.randint(1751, 1849)
            turbine_output = random.randint(27460, 27860)
            fuel_constumption = random.uniform(263.2, 283.2)
            compressor_power_consumption = random.randint(1752, 1792)
            turbine_auxillary_power = random.randint(44, 64)
            condensate_pump_power = random.randint(3, 5)
            turbine_inlet_pressure_loss = random.uniform(3.5, 4.5)
            turbine_outlet_pressure_loss = random.uniform(7.5, 8.5)
            gas_inlet_pressure = random.randint(339, 349)
            exhaust_gas_temperature = random.randint(907, 927)
            blowdown = random.randint(2318, 2418)
            exhaust_flow = random.randint(759701, 760701)
            compressor_intake_gas = random.randint(10, 20)
            post_scr_egt = random.randint(305, 325)
            fuel_btu_value = random.randint(263, 283)

            # This is the yellow condition, which has a 10%  chance of occuring and contains ranges for data that is
            # out of the anticipated range.
        elif turbine_perf_var >=86 & turbine_perf_var <=95:
            status_indicator = 'YELLOW'
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate independantly.
            #print('Yellow Condition')
            voltage_at_genset_var = random.randint(1, 2)
            if voltage_at_genset_var == 1:
                voltage_at_genset = random.randint(445, 455)
            else:
                voltage_at_genset = random.randint(467, 477)
            lighting_hvac_voltage_var = random.randint(1, 2)
            if lighting_hvac_voltage_var == 1:
                lighting_hvac_voltage = random.randint(105, 115)
            else:
                lighting_hvac_voltage = random.randint(127, 137)
            genset_rpm_var = random.randint(1, 2)
            if genset_rpm_var == 1:
                genset_rpm = random.randint(1651, 1750)
            else:
                genset_rpm = random.randint(1850, 1951)
            turbine_output_var = random.randint(1, 2)
            if turbine_output_var == 1:
                turbine_output = random.randint(27259, 27459)
            else:  # sudo apt-get install comment
                turbine_output = random.randint(27861, 28061)
            fuel_constumption_var = random.randint(1, 2)
            if fuel_constumption_var == 1:
                fuel_constumption = random.uniform(253.1, 263.1)
            else:
                fuel_constumption = random.uniform(283.3, 293.3)
            compressor_power_consumption_var = random.randint(1, 2)
            if compressor_power_consumption_var == 1:
                compressor_power_consumption = random.randint(1731, 1751)
            else:
                compressor_power_consumption = random.randint(1793, 1803)
            turbine_auxillary_power_var = random.randint(1, 2)
            if turbine_auxillary_power_var == 1:
                turbine_auxillary_power = random.randint(33, 43)
            else:
                turbine_auxillary_power = random.randint(65, 75)
            condensate_pump_power_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if condensate_pump_power_var == 1:
                condensate_pump_power = random.uniform(1, 2.9)
            else:
                condensate_pump_power = random.uniform(5.1, 6.1)
            turbine_inlet_pressure_loss_var = random.randint(1, 2)
            if turbine_inlet_pressure_loss_var == 1:
                turbine_inlet_pressure_loss = random.uniform(2.9, 3.4)
            else:
                turbine_inlet_pressure_loss = random.uniform(4.6, 5.1)
            turbine_outlet_pressure_loss_var = random.randint(1, 2)
            if turbine_outlet_pressure_loss_var == 1:
                turbine_outlet_pressure_loss = random.uniform(6.9, 7.4)
            else:
                turbine_outlet_pressure_loss = random.uniform(8.6, 9.1)
            gas_inlet_pressure_var = random.randint(1, 2)
            if gas_inlet_pressure_var == 1:
                gas_inlet_pressure = random.randint(333, 338)
            else:
                gas_inlet_pressure = random.randint(350, 355)
            exhaust_gas_temperature_var = random.randint(1, 2)
            if exhaust_gas_temperature_var == 1:
                exhaust_gas_temperature = random.randint(896, 906)
            else:
                exhaust_gas_temperature = random.randint(928, 938)
            blowdown_var = random.randint(1, 2)
            if blowdown_var == 1:
                blowdown = random.randint(2267, 2317)
            else:
                blowdown = random.randint(2419, 2469)
            exhaust_flow_var = random.randint(1, 2)
            if exhaust_flow_var == 1:
                exhaust_flow = random.randint(759200, 759700)
            else:
                exhaust_flow = random.randint(760701, 761201)
            compressor_intake_gas_var = random.randint(1, 2)
            if compressor_intake_gas_var == 1:
                compressor_intake_gas = random.uniform(4.4, 9.9)
            else:
                compressor_intake_gas = random.randint(21, 26)
            post_scr_egt_var = random.randint(1, 2)
            if post_scr_egt_var == 1:
                post_scr_egt = random.randint(294, 304)
            else:
                post_scr_egt = random.randint(326, 336)
            fuel_btu_value_var = random.randint(1, 2)
            if fuel_btu_value_var == 1:
                fuel_btu_value = random.randint(252, 262)
            else:
                fuel_btu_value = random.randint(284, 294)

        # This is the red condition, which has a 5%  chance of occuring and contains ranges for data that is
        # out of the anticipated range.
        else:
            status_indicator = 'RED'
            # this is the operational condition of the turbine which will determine which state of red condition the
            # turbine is operating or not operating under.
            turbine_condition_var = random.randint(1, 6)
            # this is the condition for when the turbine is down for repair, maintenance, or taken offline due to a
            # lack of demand
            if turbine_condition_var == 1:
                #print('turbine down for repair or maintenance')
                voltage_at_genset = 0
                lighting_hvac_voltage = 0
                genset_rpm = 0
                turbine_output = 0
                fuel_constumption = 0
                compressor_power_consumption = 0
                turbine_auxillary_power = 0
                condensate_pump_power = 0
                turbine_inlet_pressure_loss = 0
                turbine_outlet_pressure_loss = 0
                gas_inlet_pressure = 0
                exhaust_gas_temperature = 0
                blowdown = 0
                exhaust_flow = 0
                compressor_intake_gas = 0
                post_scr_egt = 0
                fuel_btu_value = random.randint(242, 304)
            elif turbine_condition_var == 2:
                # this is the condition for when the turbine is down due to a malfunction. the data on some aspects
                # will fluctuate because they could still be present on the turbine at the plant which has not been
                # disconnected yet as the fault has just occured.
                #print('turbine down due to malfunction')
                voltage_at_genset = random.randint(0, 487)
                lighting_hvac_voltage = random.randint(0, 147)
                genset_rpm = 0
                turbine_output = 0
                fuel_constumption = 0
                compressor_power_consumption = random.randint(0, 1803)
                turbine_auxillary_power = random.randint(0, 85)
                condensate_pump_power = random.uniform(0, 7.1)
                turbine_inlet_pressure_loss = 0
                turbine_outlet_pressure_loss = 0
                gas_inlet_pressure = random.randint(0, 361)
                exhaust_gas_temperature = 0
                blowdown = 0
                exhaust_flow = 0
                compressor_intake_gas = random.randint(0, 32)
                post_scr_egt = 0
                fuel_btu_value = random.randint(241, 304)
            else:
                # this is the other option for the red condition which is a turbine still running, but showing data
                # that is out of spec and needs to be addressed as soon as possible.
                voltage_at_genset_var = random.randint(1, 2)
                # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
                # separated due to the fact that these conditions can fluctuate independantly.
                if voltage_at_genset_var == 1:
                    voltage_at_genset = random.randint(1, 444)
                else:
                    voltage_at_genset = random.randint(478, 488)
                lighting_hvac_voltage_var = random.randint(1, 2)
                if lighting_hvac_voltage_var == 1:
                    lighting_hvac_voltage = random.randint(1, 104)
                else:
                    lighting_hvac_voltage = random.randint(138, 148)
                genset_rpm_var = random.randint(1, 2)
                if genset_rpm_var == 1:
                    genset_rpm = random.randint(1, 1650)
                else:
                    genset_rpm = random.randint(1952, 2052)
                turbine_output_var = random.randint(1, 2)
                if turbine_output_var == 1:
                    turbine_output = random.randint(1, 27258)
                else:
                    turbine_output = random.randint(28062, 28262)
                fuel_constumption_var = random.randint(1, 2)
                if fuel_constumption_var == 1:
                    fuel_constumption = random.randint(1, 253)
                else:
                    fuel_constumption = random.uniform(293.4, 303.4)
                compressor_power_consumption_var = random.randint(1, 2)
                if compressor_power_consumption_var == 1:
                    compressor_power_consumption = random.randint(1, 1730)
                else:
                    compressor_power_consumption = random.randint(1804, 1824)
                turbine_auxillary_power_var = random.randint(1, 2)
                if turbine_auxillary_power_var == 1:
                    turbine_auxillary_power = random.randint(1, 32)
                else:
                    turbine_auxillary_power = random.randint(76, 86)
                condensate_pump_power_var = random.randint(1, 2)
                # high low variables and data output ranges for yellow condition, each parameter has its own
                # probability generator
                if condensate_pump_power_var == 1:
                    condensate_pump_power = random.uniform(0.01, 0.9)
                else:
                    condensate_pump_power = random.uniform(6.2, 7.2)
                turbine_inlet_pressure_loss_var = random.randint(1, 2)
                if turbine_inlet_pressure_loss_var == 1:
                    turbine_inlet_pressure_loss = random.uniform(0.01, 2.8)
                else:
                    turbine_inlet_pressure_loss = random.uniform(5.2, 5.7)
                turbine_outlet_pressure_loss_var = random.randint(1, 2)
                if turbine_outlet_pressure_loss_var == 1:
                    turbine_outlet_pressure_loss = random.uniform(0.01, 6.8)
                else:
                    turbine_outlet_pressure_loss = random.uniform(9.2, 9.7)
                gas_inlet_pressure_var = random.randint(1, 2)
                if gas_inlet_pressure_var == 1:
                    gas_inlet_pressure = random.randint(1, 332)
                else:
                    gas_inlet_pressure = random.randint(356, 361)
                exhaust_gas_temperature_var = random.randint(1, 2)
                if exhaust_gas_temperature_var == 1:
                    exhaust_gas_temperature = random.randint(1, 895)
                else:
                    exhaust_gas_temperature = random.randint(943, 949)
                blowdown_var = random.randint(1, 2)
                if blowdown_var == 1:
                    blowdown = random.randint(1, 2266)
                else:
                    blowdown = random.randint(2470, 2520)
                exhaust_flow_var = random.randint(1, 2)
                if exhaust_flow_var == 1:
                    exhaust_flow = random.randint(1, 759199)
                else:
                    exhaust_flow = random.randint(761202, 761702)
                compressor_intake_gas_var = random.randint(1, 2)
                if compressor_intake_gas_var == 1:
                    compressor_intake_gas = random.uniform(0.01, 4.3)
                else:
                    compressor_intake_gas = random.randint(27, 32)
                post_scr_egt_var = random.randint(1, 2)
                if post_scr_egt_var == 1:
                    post_scr_egt = random.randint(1, 293)
                else:
                    post_scr_egt = random.randint(337, 347)
                fuel_btu_value_var = random.randint(1, 2)
                if fuel_btu_value_var == 1:
                    fuel_btu_value = random.randint(241, 251)
                else:
                    fuel_btu_value = random.randint(295, 305)
        # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
        # to load into the ELK stack.
        turbine_1_out = {'equip_name':equip_name,'Voltage at genset': voltage_at_genset, 'hvac/ lighting voltage': lighting_hvac_voltage,
                         'genset RPM': genset_rpm, 'turbine output': turbine_output,
                         'fuel consumption': fuel_constumption,
                         'compressor power consumption': compressor_power_consumption,
                         'turbine auxillary power': turbine_auxillary_power,
                         'condensate pump power consumption': condensate_pump_power,
                         'turbine inlet pressure loss': turbine_inlet_pressure_loss,
                         'turbine outlet pressure loss': turbine_outlet_pressure_loss,
                         'gas inlet pressure': gas_inlet_pressure,
                         'exhaust gas temperature': exhaust_gas_temperature, 'blowdown': blowdown,
                         'exhaust flow': exhaust_flow, 'compressor intake gas': compressor_intake_gas,
                         'post scr egt': post_scr_egt, 'fuel btu value': fuel_btu_value}
        return turbine_1_out


# This is the function for generating the data from the second turbine and allows for red, green, and yellow
# conditions. This also has the provision for different conditions that the turbine may experience when it is in
# the red condition range
class Turbine_2():

    def generate_data(self):
        equip_name = 'Turbine_2'
        #print('Solar Turbine 2')
        # This is the probability generator for determining which condition the turbine will transmit in the
        # simulation.
        turbine_perf_var = random.randint(1, 100)
        # This is the green condition probability range, which indicates that there is an 85% chance that the data
        # will be within the anticipated range.
        if turbine_perf_var <=85:
            status_indicator = 'GREEN'
            voltage_at_genset = random.randint(456, 466)
            lighting_hvac_voltage = random.randint(116, 126)
            genset_rpm = random.randint(1751, 1849)
            turbine_output = random.randint(27460, 27860)
            fuel_constumption = random.uniform(263.2, 283.2)
            compressor_power_consumption = random.randint(1752, 1792)
            turbine_auxillary_power = random.randint(44, 64)
            condensate_pump_power = random.randint(3, 5)
            turbine_inlet_pressure_loss = random.uniform(3.5, 4.5)
            turbine_outlet_pressure_loss = random.uniform(7.5, 8.5)
            gas_inlet_pressure = random.randint(339, 349)
            exhaust_gas_temperature = random.randint(907, 927)
            blowdown = random.randint(2318, 2418)
            exhaust_flow = random.randint(759701, 760701)
            compressor_intake_gas = random.randint(10, 20)
            post_scr_egt = random.randint(305, 325)
            fuel_btu_value = random.randint(263, 283)

            # This is the yellow condition, which has a 10%  chance of occuring and contains ranges for data that is
            # out of the anticipated range.
        elif turbine_perf_var >=86 & turbine_perf_var <=95:
            status_indicator = 'YELLOW'
            #print('Yellow condition')
            # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
            # separated due to the fact that these conditions can fluctuate independantly.
            voltage_at_genset_var = random.randint(1, 2)
            if voltage_at_genset_var == 1:
                voltage_at_genset = random.randint(445, 455)
            else:
                voltage_at_genset = random.randint(467, 477)
            lighting_hvac_voltage_var = random.randint(1, 2)
            if lighting_hvac_voltage_var == 1:
                lighting_hvac_voltage = random.randint(105, 115)
            else:
                lighting_hvac_voltage = random.randint(127, 137)
            genset_rpm_var = random.randint(1, 2)
            if genset_rpm_var == 1:
                genset_rpm = random.randint(1651, 1750)
            else:
                genset_rpm = random.randint(1850, 1951)
            turbine_output_var = random.randint(1, 2)
            if turbine_output_var == 1:
                turbine_output = random.randint(27259, 27459)
            else:  # sudo apt-get install comment
                turbine_output = random.randint(27861, 28061)
            fuel_constumption_var = random.randint(1, 2)
            if fuel_constumption_var == 1:
                fuel_constumption = random.uniform(253.1, 263.1)
            else:
                fuel_constumption = random.uniform(283.3, 293.3)
            compressor_power_consumption_var = random.randint(1, 2)
            if compressor_power_consumption_var == 1:
                compressor_power_consumption = random.randint(1731, 1751)
            else:
                compressor_power_consumption = random.randint(1793, 1803)
            turbine_auxillary_power_var = random.randint(1, 2)
            if turbine_auxillary_power_var == 1:
                turbine_auxillary_power = random.randint(33, 43)
            else:
                turbine_auxillary_power = random.randint(65, 75)
            condensate_pump_power_var = random.randint(1, 2)
            # high low variables and data output ranges for yellow condition, each parameter has its own
            # probability generator
            if condensate_pump_power_var == 1:
                condensate_pump_power = random.uniform(1, 2.9)
            else:
                condensate_pump_power = random.uniform(5.1, 6.1)
            turbine_inlet_pressure_loss_var = random.randint(1, 2)
            if turbine_inlet_pressure_loss_var == 1:
                turbine_inlet_pressure_loss = random.uniform(2.9, 3.4)
            else:
                turbine_inlet_pressure_loss = random.uniform(4.6, 5.1)
            turbine_outlet_pressure_loss_var = random.randint(1, 2)
            if turbine_outlet_pressure_loss_var == 1:
                turbine_outlet_pressure_loss = random.uniform(6.9, 7.4)
            else:
                turbine_outlet_pressure_loss = random.uniform(8.6, 9.1)
            gas_inlet_pressure_var = random.randint(1, 2)
            if gas_inlet_pressure_var == 1:
                gas_inlet_pressure = random.randint(333, 338)
            else:
                gas_inlet_pressure = random.randint(350, 355)
            exhaust_gas_temperature_var = random.randint(1, 2)
            if exhaust_gas_temperature_var == 1:
                exhaust_gas_temperature = random.randint(896, 906)
            else:
                exhaust_gas_temperature = random.randint(928, 938)
            blowdown_var = random.randint(1, 2)
            if blowdown_var == 1:
                blowdown = random.randint(2267, 2317)
            else:
                blowdown = random.randint(2419, 2469)
            exhaust_flow_var = random.randint(1, 2)
            if exhaust_flow_var == 1:
                exhaust_flow = random.randint(759200, 759700)
            else:
                exhaust_flow = random.randint(760701, 761201)
            compressor_intake_gas_var = random.randint(1, 2)
            if compressor_intake_gas_var == 1:
                compressor_intake_gas = random.uniform(4.4, 9.9)
            else:
                compressor_intake_gas = random.randint(21, 26)
            post_scr_egt_var = random.randint(1, 2)
            if post_scr_egt_var == 1:
                post_scr_egt = random.randint(294, 304)
            else:
                post_scr_egt = random.randint(326, 336)
            fuel_btu_value_var = random.randint(1, 2)
            if fuel_btu_value_var == 1:
                fuel_btu_value = random.randint(252, 262)
            else:
                fuel_btu_value = random.randint(284, 294)

        # This is the red condition, which has a 5%  chance of occuring and contains ranges for data that is
        # out of the anticipated range.
        else:
            status_indicator = 'RED'
            # this is the operational condition of the turbine which will determine which state of red condition the
            # turbine is operating or not operating under.
            turbine_condition_var = random.randint(1, 6)
            #print('Red condition')
            # this is the condition for when the turbine is down for repair, maintenance, or taken offline due to a
            # lack of demand
            if turbine_condition_var == 1:
                #print('turbine down for repair or maintenance')
                voltage_at_genset = 0
                lighting_hvac_voltage = 0
                genset_rpm = 0
                turbine_output = 0
                fuel_constumption = 0
                compressor_power_consumption = 0
                turbine_auxillary_power = 0
                condensate_pump_power = 0
                turbine_inlet_pressure_loss = 0
                turbine_outlet_pressure_loss = 0
                gas_inlet_pressure = 0
                exhaust_gas_temperature = 0
                blowdown = 0
                exhaust_flow = 0
                compressor_intake_gas = 0
                post_scr_egt = 0
                fuel_btu_value = random.randint(242, 304)
            elif turbine_condition_var == 2:
                # this is the condition for when the turbine is down due to a malfunction. the data on some aspects
                # will fluctuate because they could still be present on the turbine at the plant which has not been
                # disconnected yet as the fault has just occured.
                #print('turbine down due to malfunction')
                voltage_at_genset = random.randint(0, 487)
                lighting_hvac_voltage = random.randint(0, 147)
                genset_rpm = 0
                turbine_output = 0
                fuel_constumption = 0
                compressor_power_consumption = random.randint(0, 1803)
                turbine_auxillary_power = random.randint(0, 85)
                condensate_pump_power = random.randint(0, 7.1)
                turbine_inlet_pressure_loss = 0
                turbine_outlet_pressure_loss = 0
                gas_inlet_pressure = random.randint(0, 361)
                exhaust_gas_temperature = 0
                blowdown = 0
                exhaust_flow = 0
                compressor_intake_gas = random.randint(0, 32)
                post_scr_egt = 0
                fuel_btu_value = random.randint(241, 304)
            else:
                # this is the other option for the red condition which is a turbine still running, but showing data
                # that is out of spec and needs to be addressed as soon as possible.
                voltage_at_genset_var = random.randint(1, 2)
                # high or low condition variable, with 1 being the low numbers, and 2 being the high numbers
                # separated due to the fact that these conditions can fluctuate independantly.
                if voltage_at_genset_var == 1:
                    voltage_at_genset = random.randint(1, 444)
                else:
                    voltage_at_genset = random.randint(478, 488)
                lighting_hvac_voltage_var = random.randint(1, 2)
                if lighting_hvac_voltage_var == 1:
                    lighting_hvac_voltage = random.randint(1, 104)
                else:
                    lighting_hvac_voltage = random.randint(138, 148)
                genset_rpm_var = random.randint(1, 2)
                if genset_rpm_var == 1:
                    genset_rpm = random.randint(1, 1650)
                else:
                    genset_rpm = random.randint(1952, 2052)
                turbine_output_var = random.randint(1, 2)
                if turbine_output_var == 1:
                    turbine_output = random.randint(1, 27258)
                else:
                    turbine_output = random.randint(28062, 28262)
                fuel_constumption_var = random.randint(1, 2)
                if fuel_constumption_var == 1:
                    fuel_constumption = random.randint(1, 253)
                else:
                    fuel_constumption = random.randint(293.4, 303.4)
                compressor_power_consumption_var = random.randint(1, 2)
                if compressor_power_consumption_var == 1:
                    compressor_power_consumption = random.randint(1, 1730)
                else:
                    compressor_power_consumption = random.randint(1804, 1824)
                turbine_auxillary_power_var = random.randint(1, 2)
                if turbine_auxillary_power_var == 1:
                    turbine_auxillary_power = random.randint(1, 32)
                else:
                    turbine_auxillary_power = random.randint(76, 86)
                condensate_pump_power_var = random.randint(1, 2)
                # high low variables and data output ranges for yellow condition, each parameter has its own
                # probability generator
                if condensate_pump_power_var == 1:
                    condensate_pump_power = random.uniform(0.01, 0.9)
                else:
                    condensate_pump_power = random.uniform(6.2, 7.2)
                turbine_inlet_pressure_loss_var = random.randint(1, 2)
                if turbine_inlet_pressure_loss_var == 1:
                    turbine_inlet_pressure_loss = random.uniform(0.01, 2.8)
                else:
                    turbine_inlet_pressure_loss = random.uniform(5.2, 5.7)
                turbine_outlet_pressure_loss_var = random.randint(1, 2)
                if turbine_outlet_pressure_loss_var == 1:
                    turbine_outlet_pressure_loss = random.uniform(0.01, 6.8)
                else:
                    turbine_outlet_pressure_loss = random.uniform(9.2, 9.7)
                gas_inlet_pressure_var = random.randint(1, 2)
                if gas_inlet_pressure_var == 1:
                    gas_inlet_pressure = random.randint(1, 332)
                else:
                    gas_inlet_pressure = random.randint(356, 361)
                exhaust_gas_temperature_var = random.randint(1, 2)
                if exhaust_gas_temperature_var == 1:
                    exhaust_gas_temperature = random.randint(1, 895)
                else:
                    exhaust_gas_temperature = random.randint(943, 949)
                blowdown_var = random.randint(1, 2)
                if blowdown_var == 1:
                    blowdown = random.randint(1, 2266)
                else:
                    blowdown = random.randint(2470, 2520)
                exhaust_flow_var = random.randint(1, 2)
                if exhaust_flow_var == 1:
                    exhaust_flow = random.randint(1, 759199)
                else:
                    exhaust_flow = random.randint(761202, 761702)
                compressor_intake_gas_var = random.randint(1, 2)
                if compressor_intake_gas_var == 1:
                    compressor_intake_gas = random.uniform(0.01, 4.3)
                else:
                    compressor_intake_gas = random.randint(27, 32)
                post_scr_egt_var = random.randint(1, 2)
                if post_scr_egt_var == 1:
                    post_scr_egt = random.randint(1, 293)
                else:
                    post_scr_egt = random.randint(337, 347)
                fuel_btu_value_var = random.randint(1, 2)
                if fuel_btu_value_var == 1:
                    fuel_btu_value = random.randint(241, 251)
                else:
                    fuel_btu_value = random.randint(295, 305)
            # dict for the data to be written to so that it can be written to a sys log file for logstash to retriecve
            # to load into the ELK stack.
        self.turbine_2_out = {'equip_name':equip_name,'Voltage at genset': voltage_at_genset, 'hvac/ lighting voltage': lighting_hvac_voltage,
                             'genset RPM': genset_rpm, 'turbine output': turbine_output,
                             'fuel consumption': fuel_constumption,
                             'compressor power consumption': compressor_power_consumption,
                             'turbine auxillary power': turbine_auxillary_power,
                             'condensate pump power consumption': condensate_pump_power,
                             'turbine inlet pressure loss': turbine_inlet_pressure_loss,
                             'turbine outlet pressure loss': turbine_outlet_pressure_loss,
                             'gas inlet pressure': gas_inlet_pressure,
                             'exhaust gas temperature': exhaust_gas_temperature, 'blowdown': blowdown,
                             'exhaust flow': exhaust_flow, 'compressor intake gas': compressor_intake_gas,
                             'post scr egt': post_scr_egt, 'fuel btu value': fuel_btu_value}
        return self.turbine_2_out


# file path for depositing log files configured to allow for creation of this file on any linux machine
path = "/tmp/Equip_log_files"

#create log file directory to collect logs
try:
    os.makedirs(path)
except OSError:
    print("Directory %s not created" % path)
else:
    print("Directory %s created" % path)
    #Once the directory is created it can be found under your file explorer in the /home section. THIS SCRIPT IS FOR A
    #LINUX OS CURRENTLY

#preliminary setup for the logger to log the output of the generators above
def setup_equip_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

# main method to run the simulations, and record the data into .log files
def main():

    #run the MSW scale simulation
    def run_msw_in():
        msw_weight_logs = Msw_Weight()
        msw_weight_logs.generate_data()
        return msw_weight_logs.generate_data()

    #run the TDF scale simulation
    def run_tdf_in():
        tdf_weight_logs = Tdf_Trucks_Received()
        tdf_weight_logs.generate_tire_data()
        return tdf_weight_logs.generate_tire_data()

    #run the primary shredder simulation
    def run_shredder_1():
        msw_shredder_logs = Msw_1_Shredder()
        msw_shredder_logs.generate_shredder_1_data()
        return msw_shredder_logs.generate_shredder_1_data()

    #run the magnet simulation
    def run_magnet():
        magnet_logs = Magnet()
        magnet_logs.generate_magnet_data()
        return magnet_logs.generate_magnet_data()

    #run the sifter simulation
    def run_sifter():
        sifter_logs = sifter()
        sifter_logs.generate_sifter_data()
        return sifter_logs.generate_sifter_data()

    #run the spreader simulation
    def run_spreader():
        spreader_logs = Spreader()
        spreader_logs.generate_spreader_data()
        return spreader_logs.generate_spreader_data()

    #run the eddy current simulation
    def run_eddy_current():
        eddy_current_logs = Eddy_Current()
        eddy_current_logs.generate_eddy_current_data()
        return eddy_current_logs.generate_eddy_current_data()

    #run the msw pyrolysis unit 1 simulation
    def run_msw_pyrolysis_1():
        msw_pyrolysis_1_logs = Msw_Pyrolysis_1()
        msw_pyrolysis_1_logs.generate_data()
        return msw_pyrolysis_1_logs.generate_data()

    #run the msw pyrolysis unit 2 simulation
    def run_msw_pyrolysis_2():
        msw_pyrolysis_2_logs = Msw_Pyrolysis_2()
        msw_pyrolysis_2_logs.generate_data()
        return msw_pyrolysis_2_logs.generate_data()

    #run the msw pyrolysis unit 3 simulation
    def run_msw_pyrolysis_3():
        msw_pyrolysis_3_logs = Msw_Pyrolysis_3()
        msw_pyrolysis_3_logs.generate_data()
        return msw_pyrolysis_3_logs.generate_data()

    #run the msw pyrolysis unit 4 simulation
    def run_msw_pyrolysis_4():
        msw_pyrolysis_4_logs = Msw_Pyrolysis_4()
        msw_pyrolysis_4_logs.generate_data()
        return msw_pyrolysis_4_logs.generate_data()

    #run the msw pyrolysis unit 5 simulation
    def run_msw_pyrolysis_5():
        msw_pyrolysis_5_logs = Msw_Pyrolysis_5()
        msw_pyrolysis_5_logs.generate_data()
        return msw_pyrolysis_5_logs.generate_data()

    #run the tdf pyrolysis unit 1 simulation
    def run_tdf_pyrolysis_1():
        tdf_pyrolysis_1_logs = Tdf_Unit_1()
        tdf_pyrolysis_1_logs.generate_data()
        return tdf_pyrolysis_1_logs.generate_data()

    #run the tdf pyrolysis unit 2 simulation
    def run_tdf_pyrolysis_2():
        tdf_pyrolysis_2_logs = Tdf_Unit_2()
        tdf_pyrolysis_2_logs.generate_data()
        return tdf_pyrolysis_2_logs.generate_data()

    #run the tdf pyrolysis unit 3 simulation
    def run_tdf_pyrolysis_3():
        tdf_pyrolysis_3_logs = Tdf_Unit_3()
        tdf_pyrolysis_3_logs.generate_data()
        return tdf_pyrolysis_3_logs.generate_data()

    #run the turbine 1 simulation
    def run_turbine_1():
        turbine_1_logs = Turbine_1()
        turbine_1_logs.generate_data()
        return turbine_1_logs.generate_data()

    #run the turbine 2 simulation
    def run_turbine_2():
        turbine_2_logs = Turbine_2()
        turbine_2_logs.generate_data()
        return turbine_2_logs.generate_data()

    # setting up the logger to give each log of each simulation its title and the file path to follow of where to log
    #the data to
    setup_equip_logger('MSW_intake_weight', r'/tmp/Equip_log_files/MSW_intake_weight.log')
    setup_equip_logger('TDF_intake_weight', r'/tmp/Equip_log_files/TDF_intake_weight.log')
    setup_equip_logger('MSW_primary_shredder', r'/tmp/Equip_log_files/MSW_primary_shredder.log')
    setup_equip_logger('Ferrous_metals_separation', r'/tmp/Equip_log_files/Ferrous_metals_separation.log')
    setup_equip_logger('MSW_sifter', r'/tmp/Equip_log_files/MSW_sifter.log')
    setup_equip_logger('MSW_spreader', r'/tmp/Equip_log_files/MSW_spreader.log')
    setup_equip_logger('Eddy_current_separation', r'/tmp/Equip_log_files/Eddy_current_separation.log')
    setup_equip_logger('MSW_pyrolysis_unit_1', r'/tmp/Equip_log_files/MSW_pyrolysis_unit_1.log')
    setup_equip_logger('MSW_pyrolysis_unit_2', r'/tmp/Equip_log_files/MSW_pyrolysis_unit_2.log')
    setup_equip_logger('MSW_pyrolysis_unit_3', r'/tmp/Equip_log_files/MSW_pyrolysis_unit_3.log')
    setup_equip_logger('MSW_pyrolysis_unit_4', r'/tmp/Equip_log_files/MSW_pyrolysis_unit_4.log')
    setup_equip_logger('MSW_pyrolysis_unit_5', r'/tmp/Equip_log_files/MSW_pyrolysis_unit_5.log')
    setup_equip_logger('TDF_pyrolysis_unit_1', r'/tmp/Equip_log_files/TDF_pyrolysis_unit_1.log')
    setup_equip_logger('TDF_pyrolysis_unit_2', r'/tmp/Equip_log_files/TDF_pyrolysis_unit_2.log')
    setup_equip_logger('TDF_pyrolysis_unit_3', r'/tmp/Equip_log_files/TDF_pyrolysis_unit_3.log')
    setup_equip_logger('Turbine_1', r'/tmp/Equip_log_files/Turbine_1.log')
    setup_equip_logger('Turbine_2', r'/tmp/Equip_log_files/Turbine_2.log')

    # process for attatching the log infastructure to its log path and file name to allow it to receive simulation data
    msw_intake_weight = logging.getLogger('MSW_intake_weight')
    tdf_intake_weight = logging.getLogger('TDF_intake_weight')
    msw_primary_shredder = logging.getLogger('MSW_primary_shredder')
    ferrous_metals_separation = logging.getLogger('Ferrous_metals_separation')
    msw_sifter = logging.getLogger('MSW_sifter')
    msw_spreader = logging.getLogger('MSW_spreader')
    eddy_current_separation = logging.getLogger('Eddy_current_separation')
    msw_pyrolysis_unit_1 = logging.getLogger('MSW_pyrolysis_unit_1')
    msw_pyrolysis_unit_2 = logging.getLogger('MSW_pyrolysis_unit_2')
    msw_pyrolysis_unit_3 = logging.getLogger('MSW_pyrolysis_unit_3')
    msw_pyrolysis_unit_4 = logging.getLogger('MSW_pyrolysis_unit_4')
    msw_pyrolysis_unit_5 = logging.getLogger('MSW_pyrolysis_unit_5')
    tdf_pyrolysis_unit_1 = logging.getLogger('TDF_pyrolysis_unit_1')
    tdf_pyrolysis_unit_2 = logging.getLogger('TDF_pyrolysis_unit_2')
    tdf_pyrolysis_unit_3 = logging.getLogger('TDF_pyrolysis_unit_3')
    turbine_1 = logging.getLogger('Turbine_1')
    turbine_2 = logging.getLogger('Turbine_2')

    #loop to iterate through 19 runs of the simulation with each run representing 1 hour for a total of 19 hours of
    #MSW and TDF receiving
    scale = 0
    while scale <=19:
        msw_intake_weight.info(run_msw_in())
        tdf_intake_weight.info(run_tdf_in())
        scale+=1
        #time.sleep(1)
    sorting = 0
    #loop to iterate through 68400 runs of the stage 1 MSW sorting process with each run representing 1 second, this
    #number can be changed to effect the rate of samples and is here to give a scope of what the data being received in
    #a 24 hour period (19 hours of operation in each 24 hour period) would look like by the second.
    #NOTE: THIS LOOP AND THE SIMULATIONS ABOVE DO NOT INCLUDE THE ORGANICS PROCESSING LINE WHICH CAN BE ADDED LATER
    while sorting <=68400:
        msw_primary_shredder.info(run_shredder_1())
        ferrous_metals_separation.info(run_magnet())
        msw_sifter.info(run_sifter())
        msw_spreader.info(run_spreader())
        eddy_current_separation.info(run_eddy_current())
        sorting+=1
        #time.sleep(1)
    other = 0
    #loop to populate the log files for each RDF pyrolysis units (msw) and each of the TDF units, as well as both
    #turbines. This loop is set at 86400 so that data files from an actual 24 hour processing period for these pieces of
    #equipment can be viewed
    while other <= 86400:
        msw_pyrolysis_unit_1.info(run_msw_pyrolysis_1())
        msw_pyrolysis_unit_2.info(run_msw_pyrolysis_2())
        msw_pyrolysis_unit_3.info(run_msw_pyrolysis_3())
        msw_pyrolysis_unit_4.info(run_msw_pyrolysis_4())
        msw_pyrolysis_unit_5.info(run_msw_pyrolysis_5())
        tdf_pyrolysis_unit_1.info(run_tdf_pyrolysis_1())
        tdf_pyrolysis_unit_2.info(run_tdf_pyrolysis_2())
        tdf_pyrolysis_unit_3.info(run_tdf_pyrolysis_3())
        turbine_1.info(run_turbine_1())
        turbine_2.info(run_turbine_2())
        #time.sleep(1)
        other +=1

if __name__ == "__main__":
    main()
#NOTE THIS SIMULATION DOES NOT INCLUDE THE EQUIPMENT FOR PROCESSING THE TIRES, THE CUBING UNITS, THE VALVES AND OTHER
#SENSORS THAT WILL BE PRESENT THROUGHOUT THE PLANT, EMISSIONS DATA FOR TURBINES, MSW DRYER, VIDEO STREAMS, THE ORGANICS
#PROCESSING LINES, OR OTHER ANCILLARY POINTS OF DATA COLLECTION FOR THE FACILITY.
