
# -------------------------- main windows constants --------------------------

# main windows placements
VERTICAL_LAYOUT_RATIOS = [55, 10, 35]
MAIN_WINDOW_MARGINS = [5,5,5,5]
MAIN_WINDOW_SPACING = 15

# main window texts
ADD_TOOLBOX_TITLE = "Add New"
OPEN_BUTTON = "Open"
HISTOGRAM_BUTTON = "Histogram"
CHANNELS_BUTTON = "Channels"
FREQUENCY_BUTTON = "Frequency"
SAVE_BUTTON = "Save"

# add new toolbox list
TOOLBOXES = {
    "BRIGHTNESS": {
        "NAME": "Brightness",
        "CLASS": "BrightnessBox"
    },

    "SATURATION": {
        "NAME": "Saturation",
        "CLASS": "SaturationBox"
    },

    "CONTRAST": {
        "NAME": "Contrast",
        "CLASS": "ContrastBox"
    },
}




#---------------------------- old old old old old old old  -------------------------------------------


# Visualization types and  available color channels for each visualization type.
VISUALIZATION_TYPES = {"Image":["RGBA", "Red (RGBA)", "Green (RGBA)", "Blue (RGBA)", "Alpha (RGBA)", "Hue (HSV)", "Saturation (HSV)",
                                    "Value (HSV)"],

                        "Histogram": ["RGBA", "Red (RGBA)", "Green (RGBA)", "Blue (RGBA)", "Alpha (RGBA)", "Hue (HSV)", "Saturation (HSV)",
                                    "Value (HSV)"],

                        "Frequency": ["Red (RGBA)", "Green (RGBA)", "Blue (RGBA)", "Alpha (RGBA)", "Hue (HSV)", "Saturation (HSV)",
                                    "Value (HSV)"]
                        }

