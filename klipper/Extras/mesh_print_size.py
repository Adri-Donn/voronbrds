import re, logging

####################################################################################################
# Documentation
####################################################################################################
### Add this to your config file to activate this plugin :
# [mesh_print_size]
#
####################################################################################################
### Replace your call to the BED_MESH_CALIBRATE macro in your start print macro by this :
# PROBE_OPTIMIZED_AREA
#
####################################################################################################

class MeshPrintSizeHelper:
    cmd_PROBE_OPTIMIZED_AREA_help = "Compute bed mesh minimal print size"

    ####################################################################################################

    def __init__(self, config):
        self.printer = config.get_printer()

        # Register commands
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode_macro = self.printer.lookup_object('gcode_macro')
        self.gcode.register_command("PROBE_OPTIMIZED_AREA", self.cmd_PROBE_OPTIMIZED_AREA,
                                   desc=self.cmd_PROBE_OPTIMIZED_AREA_help)

    ####################################################################################################

    def cmd_PROBE_OPTIMIZED_AREA(self, gcmd):
        vcard = self.printer.objects["virtual_sdcard"]

        if vcard.current_file is None:
            logging.info("Mesh print size : Not SD printing.")
            self.RunDefaultBedMesh()
        else:
            logging.info("Mesh print size : Computing area to probe.")
            min_max_x_y = self.ExtractFirstLayerGCodeXYMinMaxAndProcessIt(vcard.current_file.name)
            self.RunOptimizedBedMesh(min_max_x_y)

    ####################################################################################################

    def ExtractFirstLayerGCodeXYMinMaxAndProcessIt(self, filename):
        xy_bounds = {'MINX': 10000, 'MINY': 10000, 'MAXX': -10000, 'MAXY': -10000}
        record = 0

        regex_x = re.compile("X(\d*\.\d*)")
        regex_y = re.compile("Y(\d*\.\d*)")

        # Opening file
        with open(filename, 'r') as gcode_file:
            count = 0
            
            for line in gcode_file:
                count += 1

                if ";LAYER:0" in line:
                    record = 1
                elif ";LAYER:1" in line:
                    record = 0
                    break
                elif record == 1:
                    search_x_result = regex_x.search(line)
                    search_y_result = regex_y.search(line)

                    if search_x_result is not None:
                        newValueX = self.ParseXYValue(search_x_result.group(1))

                        if newValueX != "x":
                            xy_bounds['MAXX'] = max(xy_bounds['MAXX'], newValueX + 1)
                            xy_bounds['MINX'] = min(xy_bounds['MINX'], newValueX - 1)

                    if search_y_result is not None:
                        newValueY = self.ParseXYValue(search_y_result.group(1))

                        if newValueY != "x":
                            xy_bounds['MAXY'] = max(xy_bounds['MAXY'], newValueY + 1)
                            xy_bounds['MINY'] = min(xy_bounds['MINY'], newValueY - 1)

        return xy_bounds

    ####################################################################################################

    def ParseXYValue(self, value):
        try:
            return int(float(value))
        except:
            logging.info("ERROR COMPUTING VALUE: %s", value)
            return "x"

    ####################################################################################################

    def RunOptimizedBedMesh(self, min_max_x_y):
        logging.info("Sending are to BED_MESH_CALIBRATE (optimized)")

        logging.info("Mesh print size : AREA_MIN_X : '%d'", min_max_x_y['MINX'])
        logging.info("Mesh print size : AREA_MAX_X : '%d'", min_max_x_y['MAXX'])
        logging.info("Mesh print size : AREA_MIN_Y : '%d'", min_max_x_y['MINY'])
        logging.info("Mesh print size : AREA_MAX_Y : '%d'", min_max_x_y['MAXY'])

        # Run BedMeshMacro  
        gcmd_bed_mesh = "BED_MESH_CALIBRATE AREA_MIN_X=" + str(min_max_x_y['MINX']) + " AREA_MIN_Y=" + str(min_max_x_y['MINY']) + " AREA_MAX_X=" + str(min_max_x_y['MAXX']) + " AREA_MAX_Y=" + str(min_max_x_y['MAXY'])

        logging.info("Mesh print size : '%s'", gcmd_bed_mesh)

        self.gcode.run_script_from_command(gcmd_bed_mesh)

    ####################################################################################################

    def RunDefaultBedMesh(self):
        logging.info("Sending are to BED_MESH_CALIBRATE (default)")

        # Run BedMeshMacro  
        gcmd_bed_mesh = "BED_MESH_CALIBRATE"

        logging.info("Mesh print size : '%s'", gcmd_bed_mesh)

        self.gcode.run_script_from_command(gcmd_bed_mesh)

    ####################################################################################################

####################################################################################################
# Module section
####################################################################################################
def load_config(config):
    return MeshPrintSizeHelper(config)