from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QRadioButton, QLabel, QLineEdit, \
    QPushButton, QComboBox, QHBoxLayout, QButtonGroup, QFileDialog


class GameSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # create left-side options
        crossword_radio = QRadioButton("Crossword")
        placeholder_radio1 = QRadioButton("Placeholder 1")
        placeholder_radio2 = QRadioButton("Placeholder 2")

        # create crossword options
        grid_size_label = QLabel("Grid Size:")
        self.grid_size_combo = QComboBox()
        self.grid_size_combo.addItems(["10x10", "15x15", "20x20"])
        input_type_label = QLabel("Input Type:")
        self.user_input_radio = QRadioButton("User Input")
        self.predefined_category_radio = QRadioButton("Predefined Category")
        self.file_upload_radio = QRadioButton("File Upload")
        self.user_input_radio.setChecked(True)
        input_type_group = QButtonGroup()
        input_type_group.addButton(self.user_input_radio)
        input_type_group.addButton(self.predefined_category_radio)
        input_type_group.addButton(self.file_upload_radio)
        crossword_file_label = QLabel("Crossword File:")
        self.crossword_file_input = QLineEdit()
        self.crossword_file_input.setEnabled(False)
        crossword_file_button = QPushButton("Browse")
        crossword_file_button.clicked.connect(self.browse_for_crossword_file)

        # create start button
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_crossword)

        # create category options
        category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Animals", "Foods", "Sports", "Movies"])
        self.category_combo.setEnabled(False)

        # create user input options
        user_input_label = QLabel("Enter Words:")
        self.user_input_input = QLineEdit()
        self.user_input_input.setEnabled(False)
        self.user_input_input.setFixedHeight(50)

        # create right-side layout
        options_layout = QGridLayout()
        options_layout.addWidget(grid_size_label, 0, 0)
        options_layout.addWidget(self.grid_size_combo, 0, 1)
        options_layout.addWidget(input_type_label, 1, 0)
        options_layout.addWidget(self.user_input_radio, 1, 1)
        options_layout.addWidget(self.predefined_category_radio, 1, 2)
        options_layout.addWidget(self.file_upload_radio, 1, 3)
        options_layout.addWidget(category_label, 2, 0)
        options_layout.addWidget(self.category_combo, 2, 1)
        options_layout.addWidget(user_input_label, 3, 0)
        options_layout.addWidget(self.user_input_input, 3, 1)
        options_layout.addWidget(crossword_file_label, 4, 0)
        options_layout.addWidget(self.crossword_file_input, 4, 1)
        options_layout.addWidget(crossword_file_button, 4, 2)
        options_layout.addWidget(start_button, 5, 0)

        # create crossword options group box
        crossword_group_box = QGroupBox("Crossword Options")
        crossword_group_box.setLayout(options_layout)

        # create right-side layout
        right_layout = QVBoxLayout()
        right_layout.addWidget(crossword_group_box)

        # create main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(crossword_radio)
        main_layout.addWidget(placeholder_radio1)
        main_layout.addWidget(placeholder_radio2)
        main_layout.addLayout(right_layout)

        # set layout
        self.setLayout(main_layout)

        # connect signals
        crossword_radio.toggled.connect(self.on_crossword_selected)
        self.user_input_radio.toggled.connect(self.on_input_type_selected)
        self.file_upload_radio.toggled.connect(self.on_input_type_selected)
        self.predefined_category_radio.toggled.connect(self.on_category_selected)

    def on_crossword_selected(self, checked):
        if checked:
            self.grid_size_combo.setEnabled(True)
            self.user_input_radio.setEnabled(True)
            self.predefined_category_radio.setEnabled(True)
            self.file_upload_radio.setEnabled(True)
            self.category_combo.setEnabled(self.predefined_category_radio.isChecked())
            self.user_input_input.setEnabled(self.user_input_radio.isChecked())
            self.crossword_file_input.setEnabled(False)
        else:
            self.grid_size_combo.setEnabled(False)
            self.user_input_radio.setEnabled(False)
            self.predefined_category_radio.setEnabled(False)
            self.file_upload_radio.setEnabled(False)
            self.category_combo.setEnabled(False)
            self.user_input_input.setEnabled(False)
            self.crossword_file_input.setEnabled(False)

    def on_input_type_selected(self, checked):
        if checked and self.user_input_radio.isChecked():
            self.user_input_input.setEnabled(True)
            self.category_combo.setEnabled(False)
            self.crossword_file_input.setEnabled(False)
        elif checked and self.predefined_category_radio.isChecked():
            self.category_combo.setEnabled(True)
            self.user_input_input.setEnabled(False)
            self.crossword_file_input.setEnabled(False)
        elif checked and self.file_upload_radio.isChecked():
            self.category_combo.setEnabled(False)
            self.user_input_input.setEnabled(False)
            self.crossword_file_input.setEnabled(True)

    def on_category_selected(self, checked):
        if checked:
            self.category_combo.setEnabled(True)
            self.user_input_input.setEnabled(False)
            self.crossword_file_input.setEnabled(False)

    def browse_for_crossword_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Crossword File", "", "Text Files (*.txt)",
                                                   options=options)
        if file_name:
            self.crossword_file_input.setText(file_name)

    def start_crossword(self):
        grid_size = self.grid_size_combo.currentText()
        input_type = ""
        if self.user_input_radio.isChecked():
            input_type = "User Input"
            user_input = self.user_input_input.text()
        elif self.predefined_category_radio.isChecked():
            input_type = "Predefined Category"
            category = self.category_combo.currentText()
        else:
            input_type = "File Upload"
            crossword_file = self.crossword_file_input.text()

        # TODO add logic for which game to launch

        # create an instance of Crossword and call StartCrossword with the selected options
        crossword = Crossword()
        crossword.StartCrossword(grid_size, input_type, user_input=user_input, category=category,
                                 crossword_file=crossword_file)


class Crossword():
    def StartCrossword(self, grid_size, input_type, user_input=None, category=None, crossword_file=None):
        print(
            f"size: {grid_size}, input type: {input_type}, user input: {user_input}, category: {category}, file: {crossword_file}")


if __name__ == '__main__':
    app = QApplication([])
    game_selector = GameSelector()
    game_selector.show()
    app.exec_()
