# SSC DESIGN PROGRAM

* `Ctrl + z` turns on word wrap vscode
* `py -3.7-64 -m pip install python-docx`

## Using program

### Input file

```json
{
    "project_name": "project title",
    "project_description": "description of project geometry",
    "project_location": "project location",
    "design_code": "710_asd | 710_lfrd",
    "roof_dead_load":"load in kN/m2",
    "roof_live_load":"load in kN/m2",
    "services_load":"load in kN/m2",
    "wind_speed": "wind speed in km/hr",
    "height_above_ground_level_in_m": "roof height in m",
    "roof_angle": "roof angle in degrees",
    "temprature_load": "temperature in degrees C",
    "enclosure_specification": "open | closed",
    "parapet_load": "false | true: indicates presence of parapet load",
    "roof_x_length": "length in mm",
    "roof_y_length": "length in mm",
    "design_for_seismic": "true | false: tells program to look out for seimic data"
}
```
