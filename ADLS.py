import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from azure.storage.blob import BlobServiceClient
import os
import time


class AzureStorageExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Azure Storage connection
        self.connection_string = "connection -  string"
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        # Container name
        self.container_name = "Container Name"
        self.path = "/"
        self.navigate = []

        # Track copied items
        self.copied_items = []

        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(),
                         QApplication.desktop().screenGeometry().height())
        self.setWindowTitle("AzureStorageExplorer")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.labels_widget = QWidget()  # Widget to hold labels side by side
        self.labels_layout = QHBoxLayout(self.labels_widget)
        self.labels_layout.setAlignment(Qt.AlignLeft)  # Align labels to the left
        self.labels_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.labels_widget)

        self.combo_label = QLabel("Select Option:")
        self.combo_box = QComboBox()
        self.combo_box.addItems(['/','/dipak/', '/dipak/tiwari/', '/dipak/tiwari/kumar/'])  # Add items to the combo box
        self.combo_box.setCurrentIndex(0)  # Set default index
        self.combo_box.activated.connect(self.on_combo_box_activated)  # Connect activated signal to handler

        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.combo_label)
        combo_layout.addWidget(self.combo_box)
        #combo_layout.addStretch(1)
        combo_layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addLayout(combo_layout)

        

        self.data = self.populate_files()
        self.table = self.create_table(self.data)
        self.layout.addWidget(self.table)

        self.exit_button = QPushButton("Exit Full Screen", self)
        self.exit_button.clicked.connect(self.exit_full_screen)
        self.exit_button.setFocusPolicy(Qt.NoFocus)  # Remove focus from the button
        self.layout.addWidget(self.exit_button)

        self.showFullScreen()  # Make the window full screen

    def create_table(self, data):

        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["File Name", "Modified Date", "Size"])

        # Set column widths
        total_width = QApplication.desktop().screenGeometry().width()  # Get screen width
        column_width = total_width // 3  # Divide by number of columns
        for col in range(table.columnCount()):
            table.setColumnWidth(col, column_width)

        for row, file_data in enumerate(data):
            for col, value in enumerate(file_data):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)

        # Set alternate row background colors
        for i in range(table.rowCount()):
            if i % 2 == 0:
                table.item(i, 0).setBackground(QColor(200, 200, 255))
                table.item(i, 1).setBackground(QColor(200, 200, 255))
                table.item(i, 2).setBackground(QColor(200, 200, 255))
            else:
                table.item(i, 0).setBackground(QColor(220, 220, 255))
                table.item(i, 1).setBackground(QColor(220, 220, 255))
                table.item(i, 2).setBackground(QColor(220, 220, 255))

        table.doubleClicked.connect(self.on_item_double_clicked)  # Connect double-click event to handler

        return table
    
    def create_second_table(self, data):
        table = self.create_table(data)
        self.layout.replaceWidget(self.table, table)
        self.table.deleteLater()  # Remove the previous table from memory
        self.table = table  # Update reference to the new table

    def on_item_double_clicked(self, index):
        table = self.centralWidget().layout().itemAt(2).widget()
        item = table.item(index.row(), index.column())

        self.clear_labels()  # Clear existing labels
        
        # Update the path with the selected item
        self.path += item.text()[2:] + '/'
        self.combo_box.setCurrentText(self.path)
        print(self.path)

        # Split the path into individual folders
        folders = self.path.split("/")
        folders = [folder for folder in folders if folder]  # Remove empty strings

        # label = QLabel(item.text()[2:] + " > ")  # Create a QLabel for the double-clicked value
        # label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.labels_layout.addWidget(label)  # Add the label to the labels layout



        #Create clickable labels for each folder
        for i, folder in enumerate(folders):
            label = QLabel(folder )  # Create a QLabel for the double-clicked value
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.mousePressEvent = lambda event, text=folder: self.print_label_text(text)  # Assign custom event handler
            self.labels_layout.addWidget(label)  # Add the label to the labels layout

            #Add a slash after each folder except the last one
            if i < len(folders) - 1:
                label = QLabel(" > ")  # Create a QLabel for the double-clicked value
                label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.labels_layout.addWidget(label)  # Add the label to the labels layout

        self.data = self.populate_files()
        self.create_second_table(self.data)

        # print(f"You double-clicked on: {item.text()}")

    def exit_full_screen(self):
        self.showNormal()  # Show the window in normal size

    def populate_files(self):
        # Clear existing items
        #self.file_tree.delete(*self.file_tree.get_children())

        # List blobs in container
        container_client = self.blob_service_client.get_container_client(self.container_name)
        blobs = container_client.list_blobs(name_starts_with=self.path)


        files = []
        path_list = self.path.split('/')
        path_list.remove('')

        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) > len(path_list)  :
                break
            else:
                name = parts[len(path_list) -1]
                file_path = os.path.join(self.path, name)
                blob_client = container_client.get_blob_client(blob=file_path)

                # Get file properties
                properties = blob_client.get_blob_properties()
                modified_date = properties.last_modified
                size = properties.size

                if name.find(".") != -1:
                    file_name  = "📄" + ' ' + name
                else:
                    file_name = "📁" + ' ' + name
                files.append([file_name, modified_date, size])

        return files
    
    def on_combo_box_activated(self, index):
        selected_option = self.combo_box.currentText()
 
        # Update the path with the selected item
        self.path = selected_option

        self.clear_labels()  # Clear existing labels

        # Split the path into individual folders
        folders = self.path.split("/")
        folders = [folder for folder in folders if folder]  # Remove empty strings

        #Create clickable labels for each folder
        for i, folder in enumerate(folders):
            label = QLabel(folder )  # Create a QLabel for the double-clicked value
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.mousePressEvent = lambda event, text=folder: self.print_label_text(text)  # Assign custom event handler
            self.labels_layout.addWidget(label)  # Add the label to the labels layout

            #Add a slash after each folder except the last one
            if i < len(folders) - 1:
                label = QLabel(" > ")  # Create a QLabel for the double-clicked value
                label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.labels_layout.addWidget(label)  # Add the label to the labels layout

        self.data = self.populate_files()
        self.create_second_table(self.data)

        print(f"Selected option: {selected_option}")

    def clear_labels(self):
        for i in reversed(range(self.labels_layout.count())):
            widget = self.labels_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def print_label_text(self, text):
        print(f"Clicked label text: {text}")
        self.clear_labels()  # Clear existing labels
        # Navigate to the specified folder 
        fol_name = []
        for x in self.path.split("/"):
            if text == x:
                 fol_name.append(x)
                 break
            else:
                fol_name.append(x)

        self.path = "/".join(fol_name) + "/" 
        self.combo_box.setCurrentText(self.path)

        # Split the path into individual folders
        folders = self.path.split("/")
        folders = [folder for folder in folders if folder]  # Remove empty strings

        #Create clickable labels for each folder
        for i, folder in enumerate(folders):
            label = QLabel(folder )  # Create a QLabel for the double-clicked value
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.mousePressEvent = lambda event, text=folder: self.print_label_text(text)  # Assign custom event handler
            self.labels_layout.addWidget(label)  # Add the label to the labels layout

            #Add a slash after each folder except the last one
            if i < len(folders) - 1:
                label = QLabel(" > ")  # Create a QLabel for the double-clicked value
                label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.labels_layout.addWidget(label)  # Add the label to the labels layout

        self.data = self.populate_files()
        self.create_second_table(self.data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AzureStorageExplorer()
    sys.exit(app.exec_())
