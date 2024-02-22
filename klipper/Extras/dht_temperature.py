# Support for Raspberry Pi DHT temperature sensor
#
# Copyright (C) 2020  Al Crate <al3ph@users.noreply.github.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging

RPI_REPORT_TIME = 1.0
PROC_TEMP_FILE = "/sys/bus/iio/devices/iio:device0/in_temp_input"

class DHTTemperature:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.name = config.get_name().split()[-1]

        self.temp = self.min_temp = self.max_temp = 0.0

        self.printer.add_object("dht_temperature " + self.name, self)
        if self.printer.get_start_args().get('debugoutput') is not None:
            return
        self.sample_timer = self.reactor.register_timer(
            self._sample_dht_temperature)
        try:
            self.file_handle = open(PROC_TEMP_FILE, "r")
        except:
            raise config.error("Unable to open temperature file '%s'"
                               % (PROC_TEMP_FILE,))

        self.printer.register_event_handler("klippy:connect",
                                            self.handle_connect)

    def handle_connect(self):
        self.reactor.update_timer(self.sample_timer, self.reactor.NOW)

    def setup_minmax(self, min_temp, max_temp):
        self.min_temp = min_temp
        self.max_temp = max_temp

    def setup_callback(self, cb):
        self._callback = cb

    def get_report_time_delta(self):
        return RPI_REPORT_TIME

    def _sample_dht_temperature(self, eventtime):
        try:
            self.file_handle.seek(0)
            currtemp = float(self.file_handle.read())/1000.0
        except Exception:
            #logging.exception("dht_temperature: Error reading data")
            if self.temp < self.min_temp:
               self.temp = self.min_temp
            currtemp = self.temp
            #return self.reactor.NEVER

        self.temp = currtemp
        if self.temp < self.min_temp:
            self.printer.invoke_shutdown(
                "DHT temperature %0.1f below minimum temperature of %0.1f."
                % (self.temp, self.min_temp,))
        if self.temp > self.max_temp:
            self.printer.invoke_shutdown(
                "DHT temperature %0.1f above maximum temperature of %0.1f."
                % (self.temp, self.max_temp,))

        mcu = self.printer.lookup_object('mcu')
        measured_time = self.reactor.monotonic()
        self._callback(mcu.estimated_print_time(measured_time), self.temp)
        return measured_time + RPI_REPORT_TIME

    def get_status(self, eventtime):
        return {
            'temperature': self.temp,
        }

def load_config(config):
    # Register sensor
    pheaters = config.get_printer().load_object(config, "heaters")
    pheaters.add_sensor_factory("dht_temperature", DHTTemperature)