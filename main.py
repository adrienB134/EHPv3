from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import threading
import ehp_functions as ehp
import pandas as pd
import sys
import os.path
from PySide6.QtCore import (
    Qt,
    QObject,
    QThreadPool,
    QRunnable,
    Signal,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QGroupBox,
    QFileDialog,
    QProgressBar,
    QDialog,
    QLineEdit,
    QFormLayout,
    QCheckBox,
)
from PySide6.QtGui import QPixmap


class CtrlClickButton(QPushButton):
    def __init__(self, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def mousePressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if self.callback:
                self.callback()
        else:
            super().mousePressEvent(event)


class WorkerSignals(QObject):
    progress_updated = Signal(int)


class LoadDataWorker(QRunnable):
    def __init__(self, file_name, app_mode, pee, seg):
        super().__init__()
        self.file_name = file_name
        self.signals = WorkerSignals()
        self.app_mode = app_mode
        self.pee = pee
        self.seg = seg

    def run(self):
        # Data Formatter
        ehp_data = pd.read_csv(self.file_name, sep=";", skiprows=20)
        ehp_data = pd.DataFrame(ehp_data)
        ehp_data = ehp_data.rename(columns={"Horodatage": "index"}).set_index(
            "index", drop=False
        )
        ehp_data = ehp_data.iloc[::10, :]

        # Folders creation
        word_folder = "courbes_word"
        png_folder = "courbes_png"
        hc_folder = "Hors_critères"

        word_folder_path = os.path.join(os.getcwd(), word_folder)
        if not os.path.exists(word_folder_path):
            os.mkdir(word_folder_path)

        png_folder_path = os.path.join(os.getcwd(), png_folder)
        if not os.path.exists(png_folder_path):
            os.mkdir(png_folder_path)

        hc_folder_path = os.path.join(os.getcwd(), hc_folder)
        if not os.path.exists(hc_folder_path):
            os.mkdir(hc_folder_path)

        # # Figures plotting

        # Define a list of functions and their arguments to be executed in parallel
        tasks = [
            (
                ehp.rcp,
                (ehp_data, self.pee),
            ),
            (
                ehp.pression_refoulement_mule,
                (ehp_data, self.app_mode, self.pee),
            ),
            (
                ehp.pression_refoulement_mule_detail,
                (ehp_data, self.app_mode, self.pee),
            ),
            (
                ehp.temperature_gros_composants_fond_de_cuve,
                (ehp_data, self.pee),
            ),
            (
                ehp.temperature_gros_composants_couvercle_et_pressu,
                (ehp_data, self.pee),
            ),
            (
                ehp.temperature_gros_composants_gv,
                (ehp_data, self.app_mode, self.pee),
            ),
            (
                ehp.pgrad,
                (ehp_data, self.pee),
            ),
            (
                ehp.tmoy,
                (ehp_data, self.pee),
            ),
            (
                ehp.tgrad,
                (ehp_data, self.pee, self.seg),
            ),
            (
                ehp.tfluid1,
                (ehp_data, self.app_mode, self.pee),
            ),
            (
                ehp.tfluid2,
                (ehp_data, self.app_mode, self.pee),
            ),
            (
                ehp.tfluid3,
                (ehp_data, self.app_mode, self.pee),
            ),
            (
                ehp.tmetal1,
                (ehp_data, self.pee),
            ),
            (
                ehp.tmetal2,
                (ehp_data, self.pee),
            ),
            (
                ehp.tmetal3,
                (ehp_data, self.app_mode, self.pee),
            ),
            (
                ehp.evolution_pression_epreuve,
                (ehp_data, self.pee),
            ),
            (
                ehp.evolution_pression_epreuve_palier,
                (ehp_data, self.pee),
            ),
            (
                ehp.hors_criteres,
                (ehp_data, self.seg),
            ),
        ]

        # Calculate the number of worker processes
        num_cores = multiprocessing.cpu_count()
        max_workers = num_cores // 2

        # Initialize a shared progress variable and a lock for thread-safe updates
        progress = 0
        progress_lock = threading.Lock()

        def callback():
            nonlocal progress
            with progress_lock:
                progress += 100 / 16
                self.signals.progress_updated.emit(progress)

        # Run tasks in parallel using a ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for index, (func, args) in enumerate(tasks):
                future = executor.submit(func, *args)
                future.add_done_callback(lambda _: callback())
                futures.append(future)

            # Wait for all tasks to complete
            for future in futures:
                future.result()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set the main window properties
        self.setWindowTitle("EHP v3")
        self.setMinimumSize(1280, 720)

        # Create the main container widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create the vertical layout for the controls
        controls_layout = QVBoxLayout()

        # Create a "Palier" selector
        self.palier = QComboBox()
        self.palier.addItems(["900", "PQY", "DPY"])
        palier_label = QLabel("Palier")
        palier_layout = QVBoxLayout()
        palier_layout.addWidget(palier_label)
        palier_layout.addWidget(self.palier)
        palier_container = QGroupBox()
        palier_container.setLayout(palier_layout)

        # PEE & Site Edit
        self.pee_site = QLineEdit("D02-ARV-01-156-210")
        self.pee_site_arret = QLineEdit()
        pee_site_layout = QFormLayout()
        pee_site_layout.addRow(self.pee_site)
        pee_site_layout.addRow(QLabel("Site/Arret:"), self.pee_site_arret)
        pee_site_container = QGroupBox()
        pee_site_container.setLayout(pee_site_layout)

        # Checkbox for "segregation Carbone"
        checkbox_container = QGroupBox()
        checkbox_layout = QVBoxLayout()
        self.checkbox_seg = QCheckBox("Segrégation Carbone")
        checkbox_layout.addWidget(self.checkbox_seg)
        checkbox_container.setLayout(checkbox_layout)

        # "Tracer" button
        self.load_data_button = QPushButton("Tracer")
        self.about_button = CtrlClickButton(
            callback=self.tracer_special,
            text="About",
        )

        # Progress Bar
        self.progress_bar_label = QLabel("Traçage des courbes:")
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        progress_bar_layout = QVBoxLayout()
        progress_bar_layout.addWidget(self.progress_bar_label)
        progress_bar_layout.addWidget(self.progress_bar)
        progress_bar_container = QGroupBox()
        progress_bar_container.setLayout(progress_bar_layout)
        progress_bar_container.setFixedHeight(55)

        # Create a controls layout and populate it
        controls_layout.addWidget(pee_site_container)
        controls_layout.addWidget(palier_container)
        # controls_layout.addWidget(tempsup50_container)
        # controls_layout.addWidget(tempinf50_container)
        controls_layout.addWidget(checkbox_container)
        controls_layout.addWidget(self.load_data_button)
        controls_layout.addWidget(progress_bar_container)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.about_button)

        # Create a controls container
        controls_container = QGroupBox()
        controls_container.setLayout(controls_layout)
        controls_container.setFixedWidth(190)

        # Create the image selector layout
        image_selector_layout = QHBoxLayout()

        # Create and add the image selector widgets to the layout
        self.selection_courbe = QComboBox()
        self.selection_courbe.addItems(
            [
                "Evolution de la pression RCP pendant l'EHP",
                "Evolution de la pression de refoulement de la pompe de charge",
                "Evolution de la pression de refoulement de la pompe de charge - détail",
                "Température des gros composants du CPP - Fond de cuve",
                "Température des gros composants du CPP - couvercle et pressu",
                "Température des gros composants du CPP - GVs",
                "Gradients de Pression de l'EHP",
                "Suivi de la Tmoy de l'EHP",
                "Suivi du gradient de Tmoy de l'EHP",
                "Suivi des températures fluide pendant l'EHP - 1",
                "Suivi des températures fluide pendant l'EHP - 2",
                "Suivi des températures fluide pendant l'EHP - 3",
                "Gradient des températures métal pendant l'EHP - Fond de cuve",
                "Gradient des températures métal pendant l'EHP - Couvercle et Pressu",
                "Gradient des températures métal pendant l'EHP - GV",
                "Evolution de la pression pendant le palier d'épreuve",
                "Evolution de la pression pendant le palier d'épreuve - détail",
            ]
        )
        image_selector_layout.addWidget(self.selection_courbe)
        image_selector_container = QGroupBox()
        image_selector_container.setLayout(image_selector_layout)
        image_selector_container.setFixedHeight(45)

        # Create the image label
        self.image_label = QLabel()
        self.image_label.setStyleSheet("border: 0.5px solid grey;")
        self.image_label.setAlignment(Qt.AlignCenter)

        # Create and populate the image display layout
        image_display_layout = QVBoxLayout()
        image_display_layout.addWidget(image_selector_container)
        image_display_layout.addWidget(self.image_label)

        # Create an image display container
        image_display_container = QGroupBox()
        image_display_container.setLayout(image_display_layout)

        # Add the containers to the main layout
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addWidget(controls_container)
        main_layout.addWidget(image_display_container)

        self.load_data_button.clicked.connect(self.get_file_window)
        self.resizeEvent = lambda event: self.tracer()
        self.selection_courbe.currentIndexChanged.connect(self.tracer)
        self.about_button.clicked.connect(self.about_window)

    def ehp_function_selector(self):
        index = self.selection_courbe.currentIndex()

        if index == 0:
            name = "rcp"
        if index == 1:
            name = "pression_refoulement_mule"
        if index == 2:
            name = "pression_refoulement_mule_detail"
        if index == 3:
            name = "temperature_gros_composants_fond_de_cuve"
        if index == 4:
            name = "temperature_gros_composants_brides_JEP"
        if index == 5:
            name = "temperature_gros_composants_gv"
        if index == 6:
            name = "gradients_de_pression"
        if index == 7:
            name = "Tmoy"
        if index == 8:
            name = "Tgrad"
        if index == 9:
            name = "Tfluide1"
        if index == 10:
            name = "Tfluide2"
        if index == 11:
            name = "Tfluide3"
        if index == 12:
            name = "Tmetal1"
        if index == 13:
            name = "Tmetal2"
        if index == 14:
            name = "Tmetal3"
        if index == 15:
            name = "P_primaire_epreuve"
        if index == 16:
            name = "P_primaire_palier"

        fig = "courbes_png/" + name + ".png"
        return fig

    def tracer(self):
        fig = self.ehp_function_selector()
        pixmap = QPixmap(fig)
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def tracer_special(self):
        # Function used to define the image path when packaged with pyinstaller
        def resource_path(relative_path):
            base_path = getattr(
                sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))
            )
            return os.path.join(base_path, relative_path)

        fig = resource_path("photo_cv.jpg")
        pixmap = QPixmap(fig)
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def load_data(self, file_name):
        app_mode = self.palier.currentText()
        pee = self.pee_site.text() + " " + self.pee_site_arret.text()
        seg = 50
        if self.checkbox_seg.isChecked():
            seg = 60
        worker = LoadDataWorker(file_name, app_mode, pee, seg)
        worker.signals.progress_updated.connect(self.update_progress)
        QThreadPool.globalInstance().start(worker)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            self.tracer()

    def get_file_window(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Load File",
            "",
            "*.csv",
            options=options,
        )
        if file_name:
            self.load_data(file_name)

    def about_window(self):
        about_window = QDialog(self)
        about_window.setWindowTitle("About")
        about_window.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        text_label1 = QLabel("Réalisé par Adrien Berthélémé")
        text_label2 = QLabel("adrien.bertheleme@gmail.com")
        text_label3 = QLabel("06.72.65.24.97")
        text_label4 = QLabel(
            "Code source dispo ici: https://github.com/adrienB134/EHPv3"
        )
        layout.addWidget(text_label1)
        layout.addWidget(text_label2)
        layout.addWidget(text_label3)
        layout.addWidget(text_label4)

        about_window.setLayout(layout)
        about_window.show()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
