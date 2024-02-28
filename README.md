# VoronBRDS

---
## ToDo list
---

- [ ] LED animation
- [ ] Neopixel RGB LED management
- [ ] Nozzle cleaning (Scrub nozzle)
- [ ] ERCF support

---

## Features offered :

### Features
- Arc support (ArcWelder)
- Pretty GCode
- Management of the moonraker configuration file
- Management of the mainsail configuration file
- Multiple configuration management
- Extensibility

### Mods extension
- Klicky probe
- Voron TAP
- Auto-Z-calibration
- Stealthburner
- CanBus
- Nevermore

### Calibration
- 3 types of Bed Mesh (with one optimized before printing, no need to add this in your slicer !)
- Heaters
- Homing
- Input Shaper
- Pressure advance
- Z-Offset

### Lights
- Case
- Display
- Doors
- Stealthburner led management 
- Neopixel RGB LED management

### Moving
- Center toolhead
- Homing

### Sensors
- Filament
- Thermals

### Events
- Pause print
- Start print
- End print
- idle timeout

### MCU
- Raspberry Pi
- Spider (V1.0, V1.1, V2.2, V2.3)
- Octopus (V1.0)
- EBB36 (V1.1, V1.2)
- FLY SHT36 (V2)

### Menus
- Calibration
- Lights
- Moving
- Preheat

> Share your macros and tuning to the community !

## Prerequisites
- Klipper (Required)
- Moonraker (Required)
- Klicky probe (Recommanded)
- Klipper auto-z-calibration (Recommanded)

## Installation

### Prerequisites II
> Not needed if you are using [VoronNUC](https://gitlab.black-rider-studio.eu/Adri/partagevoron/-/tree/master/Mods/VoronNUC)
Follow this [tutorial](https://www.klipper3d.org/RPi_microcontroller.html) in order to activate the PI as an MCU and retrieve information from it

### Preparing the Raspberry Pi
Open an SSH terminal on your Raspberry Pi and run the following commands to retrieve the repository on your Pi :

```
cd ~
git clone https://github.com/Adri-Donn/voronbrds.git
```

### Prepare the configuration file
In the terminal, execute the following command to copy the configuration file to the right place :

```
cp ~/voronbrds/voron-brds-variables.cfg ~/printer_data/config/voron-brds-variables.cfg
```

You can then open this file, adapt it to your needs and finally save it.

### Install the wrapper in moonraker
This allows to update the voronbrds extension via the web interface.
Copy the following code block in the "moonraker.conf" file.

```
# Include Voron-BRDS config
#[include ../voronbrds/Moonraker/base.conf]         # From klipper_config
#[include ../../voronbrds/Moonraker/base.conf]      # From printer_data/config
```

### Make the extension active
We just have to add the following code block at the end of the "printer.cfg" file and then reboot to make the configuration effective.

```
#####################################################################
#	Macros
#####################################################################
[include ./voron-brds-variables.cfg]
```

### Patch klipper
ln -sf ~/voronbrds/klipper/Extras/mesh_print_size.py ~/klipper/klippy/extras/mesh_print_size.py" 

### Adapt the print start sequence in your slicer

Cura:

start :
```

START_PRINT EXTRUDER_TEMP={material_print_temperature_layer_0} BED_TEMP={material_bed_temperature_layer_0}

```

end : 
```

END_PRINT

```

*(Cura slicer plugin) To make the macro to work in Cura slicer, you need to install the post process plugin by frankbags - In cura menu Help -> Show configuration folder. - Copy the python script from the above link in to scripts folder. - Restart Cura - In cura menu Extensions -> Post processing -> Modify G-Code and select Mesh Print Size

Finally, in the Cura MarketPlace, install the ARC Welder plugin

Prusa slicer: 

start :
```

START_PRINT EXTRUDER_TEMP={material_print_temperature_layer_0} BED_TEMP={material_bed_temperature_layer_0}

```

end : 
```

END_PRINT

```

### Convert from klicky to Voron TAP
> Soon klicky and auto-z-calibration will be removed so it is recommended to convert your printer

- [ ] Be sure to remove any automatically saved [stepper_z]  position_endstop: ... value that may be found at the bottom of your printer.cfgfile.
- [ ] If you have a [homing_override] make sure that it moves the toolhead to the center of the bed before calling G28 Z
- [ ] You'll need to manually calibrate the probe's Z offset by using PROBE_CALIBRATE

### Configure the thumbnail
[Mainsail documentation](https://github.com/emtrax-ltd/Cura2MoonrakerPlugin)

## Documentation
- [Other documentation like pinout](https://gitlab.black-rider-studio.eu/Adri/partagevoron)

## Example files
| File name and link to example                                                                             | When you need it   |
| -----------                                                                       | -----------   |
| [can0](./Examples/can0.example)                                                   | Only if you are using CanBUS |
| [moonraker.conf](./Examples/moonraker.conf.example)                               | Everytime |
| [printer.conf](./Examples/printer.cfg.example)                                    | Everytime |
| [voron-brds-variables.cfg](./Examples/voron-brds-variables(octopus%20V1.0).cfg)   | Everytime with board octopus V1.0 |
| [voron-brds-variables.cfg](./Examples/voron-brds-variables(spider%20V1.X).cfg)    | Everytime with board Spider V1.X |
| [voron-brds-variables.cfg](./Examples/voron-brds-variables(spider%20V2.X).cfg)    | Everytime with board Spider V2.X |

## References
- https://github.com/jlas1/Klicky-Probe
- https://github.com/protoloft/klipper_z_calibration
- https://github.com/simplisticton/
- https://3dprintbeginner.com/faster-klipper-bed-probing-macro/
- https://gist.github.com/frankbags/c85d37d9faff7bce67b6d18ec4e716ff
- https://www.klipper3d.org/RPi_microcontroller.html
- https://gist.github.com/bistory/917be092c1fe3b169ec366476644afbb
- https://github.com/rootiest/zippy-klipper_config/blob/master/guides/GUIDE-macros.md

## You may like
- https://github.com/th33xitus/kiauh
- https://github.com/Kragrathea/pgcode
- https://github.com/jordanruthe/KlipperScreen

## Notes
```
EXTRUDER_TEMP=[first_layer_temperature] BED_TEMP=[first_layer_bed_temperature]
```

### Klipper-z-calibration patch
This variable disable Klipper-z-calibration and define a fixed offset.
When setted to 0.0 it re-enable klipper-z-calibration.

This thing was develop to be able to print when kzc have a problem.

```
variable_auto_z_offset_force_value :            0.0     # Set 0.0 to disable or set a value tu use the value
```