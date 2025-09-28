from PySide6.QtWidgets import QFileDialog, QMessageBox

class MainWindowManager():
    def __init__(self):
        self.input_data = ""
        self.output_data = ""


    def open_file(self):
        filePath, _ = QFileDialog.getOpenFileName(None, "Select an input file")

        if filePath:
            with open(filePath, "r") as f:
                self.input_data = f.read()
                return self.input_data

                
    def save_file(self):
        filePath, _ = QFileDialog.getSaveFileName(None, "Save the file")
        
        if filePath:
            try:
                with open(filePath, "w") as f:
                    f.write(self.output_data)
            except Exception as e:
                QMessageBox.information(None, "Error", f"Failed to save the image.\n{str(e)}")


    def dragEnterEvent(self, event):
        if event.mimeData():
            event.acceptProposedAction()


    def dropEvent(self, event):
        pos = event.position().toPoint()                
        source = event.source()                         
        index = self.find_insert_index(pos)             

        # Check if the source is a valid FunctionBox
        if source and isinstance(source, self.Toolbox):
            self.pipeline.move_step(source, index)              
            self.contentLayout.removeWidget(source)             
            self.contentLayout.insertWidget(index, source)      

            event.acceptProposedAction()            
            self.pipeline_on_change()                     


    def find_insert_index(self, pos):
        for i in range(self.contentLayout.count()):
            widget = self.contentLayout.itemAt(i).widget()
            if widget and widget != self.add_new_box:
                if widget.geometry().contains(pos):
                    return i
        return self.contentLayout.count() - 1



"""
    def init_ui_variables(self, toolbox_wrapper, footer_toolbox, in_im_canvas, out_im_canvas, 
                          left_title, right_title, vis_mod_list, color_chan_list, zoom_btns):
        self.toolbox_wrapper = toolbox_wrapper
        self.footer_toolbox = footer_toolbox
        self.in_im_canvas = in_im_canvas
        self.out_im_canvas = out_im_canvas
        self.left_title = left_title
        self.right_title = right_title
        self.vis_mod_list = vis_mod_list
        self.color_chan_list = color_chan_list
        self.zoom_btn_1, self.zoom_btn_2, self.zoom_btn_3 = zoom_btns

        # Initialize the pipeline
        #self.pipeline = Pipeline()  

        # Modes and their corresponding methods which are called when the mode is activated.
        self.view_handlers = {      
            "Image": lambda: self.display_images(self.get_color_channels()),  
            "Histogram": lambda: self.display_histogram(),
            "Frequency": lambda: self.display_images(self.fourier_transform())
        }

        # Declares which widgets will be shown and which widgets will be hidden based on the selected mode.
        self.widgets_per_mode = {
            "Image": [self.left_title, self.right_title],
            "Histogram": [self.zoom_btn_1, self.zoom_btn_2, self.zoom_btn_3],
            "Frequency": [self.left_title, self.right_title]
        }


    def init_variables(self):
        self.input_BGRA = None                      # input image variable
        self.output_BGRA = None                     # output image variable
        self.view_mode = "Image"                    # name of the currently active view mode
        self.color_channel = "RGBA"            # name of the currently active color channel   
    
    @Slot(str)
    def insert_toolbox(self, toolbox_name):
        # Create a new method box based on the selected method name
        for toolbox in constants.TOOLBOXES.values():
            if toolbox_name == toolbox['NAME']:
                toolbox_class = getattr(toolboxes, toolbox['CLASS'])  
                new_toolbox = toolbox_class()  # create an instance of the toolbox class
                break

        # connect the toolbox signals
        new_toolbox.updateTrigger.connect(self.pipeline_on_change)   
        new_toolbox.removeTrigger.connect(self.remove_toolbox) 

        new_toolbox.update_toolbox(self.input_BGRA)                 # update the toolbox with the input image

        self.pipeline.add_step(new_toolbox)                         # add the toolbox to the pipeline

        self.toolbox_wrapper.removeWidget(self.footer_toolbox)      # remove the special footer widget
        self.footer_toolbox.setParent(None)           
        self.toolbox_wrapper.addWidget(new_toolbox)                 # add the toolbox to the layout
        self.toolbox_wrapper.addWidget(self.footer_toolbox)         # add the special footer widget back

        self.pipeline_on_change()                                   # trigger the update method to rerun the updated pipeline 


    @Slot(str)
    def remove_toolbox(self, id):
        # remove the toolbox from the layout
        for i in range(self.toolbox_wrapper.count()):
            widget = self.toolbox_wrapper.itemAt(i).widget()
            if widget and widget.id == id:
                self.toolbox_wrapper.removeWidget(widget)
                widget.setParent(None)
                break
        
        self.pipeline.remove_step(id)               # remove toolbox from the pipeline
        self.pipeline_on_change()                   # rerun the pipeline
   

    def pipeline_on_change(self):
        if self.input_BGRA is not None:
            self.output_BGRA = self.pipeline.run(self.input_BGRA)               # run the pipeline on the input image
            self.view_handlers[self.view_mode]()                                # update the ui based on the current mode


    def switch_view(self, mode_name):
        if self.input_BGRA is None:
            return
        
        if self.vis_mod_list.currentText() != mode_name:
            self.vis_mod_list.setCurrentText(mode_name)

        # Uncheck the zoom buttons
        self.zoom_btn_1.setChecked(False)  
        self.zoom_btn_2.setChecked(False)

        # show or hide the relevant widgets based on the selected mode
        widgets_to_show = []
        for w in self.widgets_per_mode.keys():
            if w == mode_name:
                for widget in self.widgets_per_mode[w]:
                    widgets_to_show.append(widget)
            else:
                for widget in self.widgets_per_mode[w]:
                    widget.hide()

        for widget in widgets_to_show:
            widget.show()

        # Update the view mode and color channel variables
        self.view_mode = mode_name                  
        self.color_channel = VISUALIZATION_TYPES[mode_name][0].split(" ")[0]                   

        # Clear existing color channels and add new ones based on selected mode
        self.color_chan_list.blockSignals(True)
        self.color_chan_list.clear()
        self.color_chan_list.blockSignals(False)
        self.color_chan_list.addItems(VISUALIZATION_TYPES[mode_name])  # This will trigger the switch_color_chan method and update the view


    def switch_color_chan(self, channel_name):
        if self.input_BGRA is None:
            return
        
        # Reset the input and output image canvases       
        self.in_im_canvas.reset_plot()
        self.out_im_canvas.reset_plot()

        self.color_channel = channel_name.split(" ")[0]     # get the color channel name from the button text
        self.view_handlers[self.view_mode]()                # update the view based on the current view mode


    def display_images(self, images):
        # Toggle visibility of titles based on the color channel
        if self.color_channel == "RGBA":
            self.left_title.hide()
            self.right_title.hide()
        else:
            self.left_title.show()
            self.right_title.show()
            self.left_title.setText(f"{self.color_channel} Channel")
            self.right_title.setText(f"{self.color_channel} Channel")

        # Convert the images to BGRA format if they are 1-channel grayscale images
        for i in range(len(images)):
            if len(images[i].shape) == 2:
                images[i] = cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGRA)

        # Plot the images on the respective canvases
        for image, canvas in zip(images, [self.in_im_canvas, self.out_im_canvas]):
            
            # clear the current canvas and plot the new image
            canvas.set_plot_type("image")
            canvas._axes.imshow(image[:, :, [2, 1, 0, 3]], interpolation="none")    # convert BGRA to RGBA and display it
            canvas.configure_imgae_plot()
            canvas.draw()
 

    def display_histogram(self):
        for image, canvas in zip(self.get_color_channels(), [self.in_im_canvas, self.out_im_canvas]):
            canvas.set_plot_type("histogram")
            
            # image can be in the form of 1-channel grayscale or 4-channel BGRA
            channel_count = image.shape[2] if len(image.shape) == 3 else 1
            # plot the histogram for each channel if the image has more than 1 channel
            for i in range(channel_count):
                channel = image if channel_count == 1 else image[:, :, i]       

                # Calculate histogram values and bin edges
                hist_vals, bin_edges = np.histogram(channel, bins=255, range=(0, 256))

                # Use midpoints for x-axis
                bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                
                # Set the color for the histogram
                if self.color_channel == "RGBA":
                    colors = ['blue', 'green', 'red', 'black']
                elif self.color_channel == "Red" or self.color_channel == "Green" or self.color_channel == "Blue":
                    colors = [self.color_channel]
                else:
                    colors = ['black']

                # Plot the histogram
                canvas._axes.step(bin_centers, hist_vals, color=colors[i], where='mid', linewidth=1)
                canvas._axes.set_title(f"{self.color_channel} Channel")
                canvas.configure_hist_plot()

            canvas.draw()


    def get_color_channels(self):
        channel_maps = {
            "Red":       ("BGR", 2),
            "Green":     ("BGR", 1),
            "Blue":      ("BGR", 0),
            "Alpha":     ("BGR", 3),
            "Hue":       ("HSV", 0),
            "Saturation":("HSV", 1),
            "Value":     ("HSV", 2),
        }

        # If the color channel is not specified or is RGBA, return the input and output images as they are (4 channel BGRA images)
        if self.color_channel not in channel_maps or self.color_channel == "RGBA":
            return [self.input_BGRA, self.output_BGRA]

        space, index = channel_maps[self.color_channel]

        def extract_channel(image, space, index):
            if space == "BGR":
                channel = image[:, :, index]
            else:
                converted = cv2.cvtColor(image[:, :, :3], getattr(cv2, f'COLOR_BGR2{space}'))
                channel = converted[:, :, index]
            return channel

        # Return the extracted channels (1 channel grayscale images)
        return [
            extract_channel(self.input_BGRA, space, index),
            extract_channel(self.output_BGRA, space, index)
        ]


    def fourier_transform(self):
        magnitude_spectrums = []  

        for channel in self.get_color_channels():
            
            ch_float = np.float32(channel)         # convert the channel to float32   
            dft = cv2.dft(ch_float, flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            magnitude = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])
            magnitude_log = np.log(magnitude + 1)
            magnitude_norm = cv2.normalize(magnitude_log, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            mag_im = cv2.cvtColor(magnitude_norm, cv2.COLOR_GRAY2BGRA)  
            magnitude_spectrums.append(mag_im)

        return magnitude_spectrums


"""