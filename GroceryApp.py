import sys
from PyQt5.QtGui import QColor, QIcon, QFont
from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QMessageBox,
    QToolBar, QPlainTextEdit, QVBoxLayout, QWidget, QAction, QDialog,
    QStatusBar, QStyleFactory, QColorDialog, QLabel, QHBoxLayout, QPushButton, QListWidget, QGroupBox,
    QSystemTrayIcon, QMenu, QGridLayout
)
from PyQt5.QtPrintSupport import QPrintDialog
import os, requests, webbrowser
from fpdf import FPDF
import PyPDF2


class RecipeDialog(QDialog):
    def __init__(self, suggested_recipes_provider):
        super().__init__()

        self.setWindowTitle("Suggested Recipes")
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #2C3E50;
                color: #ECF0F1;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ECF0F1;
            }
            QListWidget {
                font-size: 16px;
                background-color: #34495E;
                color: #ECF0F1;
                padding: 5px;
            }
            QPushButton {
                font-size: 16px;
                background-color: #1ABC9C;
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)

        self.suggested_recipes_provider = suggested_recipes_provider

        layout = QVBoxLayout()

        self.recipe_label = QLabel("Suggested Recipes:")
        self.recipe_list = QListWidget()
        self.recipe_list.addItems(self.suggested_recipes_provider.get_suggested_recipes())

        layout.addWidget(self.recipe_label)
        layout.addWidget(self.recipe_list)

        regenerate_button = QPushButton("Regenerate")
        regenerate_button.setIcon(QIcon.fromTheme("view-refresh"))
        regenerate_button.clicked.connect(self.regenerate_recipes)
        layout.addWidget(regenerate_button)

        self.setLayout(layout)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        screen_center = QApplication.desktop().screen().rect().center()
        self_center = self.rect().center()
        self.move(screen_center - self_center)
        self.animation.setStartValue(QRect(self.x(), self.y() - 50, self.width(), self.height()))
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.animation.start()

        self.recipe_list.itemSelectionChanged.connect(self.on_item_selection_changed)

    def regenerate_recipes(self):
        self.recipe_list.clear()
        self.recipe_list.addItems(self.suggested_recipes_provider.get_suggested_recipes())

    def on_item_selection_changed(self):
        selected_items = self.recipe_list.selectedItems()
        if selected_items:
            selected_item_text = selected_items[0].text()
            youtube_query_url = f"https://www.youtube.com/results?search_query={selected_item_text} recipe"
            webbrowser.open(youtube_query_url)


class GroceryApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(GroceryApp, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Grocery Manager")
        self.path = None

        self.setStyleSheet("""
            QMainWindow {
                background-color: #34495E;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ECF0F1;
            }
            QPlainTextEdit {
                font-size: 16px;
                background-color: #2C3E50;
                color: #ECF0F1;
                padding: 8px;
                border: 2px solid #1ABC9C;
                border-radius: 10px;
            }
            QListWidget {
                font-size: 16px;
                background-color: #2C3E50;
                color: #ECF0F1;
                border: 2px solid #1ABC9C;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton {
                font-size: 16px;
                background-color: #1ABC9C;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                color: #ECF0F1;
                border: 2px solid #1ABC9C;
                border-radius: 10px;
                margin-top: 20px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()

        self.feedback_label = QLabel("Enter Items for Shopping List")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.feedback_label)

        self.editor = QPlainTextEdit()
        layout.addWidget(self.editor)

        shopping_list_group = QGroupBox("Shopping List")
        shopping_list_layout = QVBoxLayout()
        self.shopping_list_widget = QListWidget()
        shopping_list_layout.addWidget(self.shopping_list_widget)
        shopping_list_group.setLayout(shopping_list_layout)
        layout.addWidget(shopping_list_group)

        button_group = QGroupBox("Actions")
        button_layout = QGridLayout()

        self.add_button = QPushButton("Add to List")
        self.add_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_button.clicked.connect(self.add_to_list)
        button_layout.addWidget(self.add_button, 0, 0)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.setIcon(QIcon.fromTheme("edit-delete"))
        self.remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_button, 0, 1)

        self.suggest_recipes_button = QPushButton("Suggest Recipes")
        self.suggest_recipes_button.setIcon(QIcon.fromTheme("applications-education"))
        self.suggest_recipes_button.clicked.connect(self.show_recipe_dialog)
        button_layout.addWidget(self.suggest_recipes_button, 1, 0, 1, 2)

        self.download_pdf_button = QPushButton("Download List as PDF")
        self.download_pdf_button.setIcon(QIcon.fromTheme("document-save"))
        self.download_pdf_button.clicked.connect(self.download_list_as_pdf)
        button_layout.addWidget(self.download_pdf_button, 2, 0)

        self.upload_pdf_button = QPushButton("Upload List from PDF")
        self.upload_pdf_button.setIcon(QIcon.fromTheme("document-open"))
        self.upload_pdf_button.clicked.connect(self.upload_list_from_pdf)
        button_layout.addWidget(self.upload_pdf_button, 2, 1)

        button_group.setLayout(button_layout)
        layout.addWidget(button_group)

        notification_group_box = QGroupBox("Notifications")
        notification_layout = QVBoxLayout()
        self.expiry_notification = QLabel()
        notification_layout.addWidget(self.expiry_notification)
        notification_group_box.setLayout(notification_layout)
        layout.addWidget(notification_group_box)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("dialog-information"))
        self.tray_icon.setToolTip("Grocery Manager")
        self.tray_menu = QMenu()
        self.tray_icon.setContextMenu(self.tray_menu)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_expiry_notification)
        self.timer.start(1000 * 60 * 60)  # 1 hour interval

        self.show()

   

    def add_to_list(self):
        items = self.editor.toPlainText().strip()
        if items:
            items_list = items.splitlines()
            for item in items_list:
                self.shopping_list_widget.addItem(item)
            self.editor.clear()

    def remove_selected(self):
        selected_items = self.shopping_list_widget.selectedItems()
        for item in selected_items:
            self.shopping_list_widget.takeItem(self.shopping_list_widget.row(item))

    def show_recipe_dialog(self):
        if not self.shopping_list_widget.count():
            item = self.editor.toPlainText().strip()
            if item:
                self.add_to_list()
                self.show_recipe_dialog()
            else:
                QMessageBox.warning(self, "No Items", "Please add items to your shopping list first.")
        else:
            suggested_recipes = self.get_suggested_recipes()
            recipe_dialog = RecipeDialog(self)
            recipe_dialog.exec()

    def get_shopping_list_text(self):
        items = []
        for index in range(self.shopping_list_widget.count()):
            items.append(self.shopping_list_widget.item(index).text())
        return ','.join(items)

    def get_suggested_recipes(self):
        api_url = "https://api.spoonacular.com/recipes/findByIngredients"
        api_key = "f8bb48b03837434c9285702f58c8064b"
        ingredients = self.get_shopping_list_text()
        params = {'ingredients': ingredients, 'number': 5, 'apiKey': api_key}
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        recipe_data = response.json()
        return [recipe['title'] for recipe in recipe_data]

    def update_expiry_notification(self):
        expiring_items_text = "Expiring Items:\n"
        for i in range(1, 4):
            expiring_items_text += f"Item {i}: {i} days left\n"
        self.expiry_notification.setText(expiring_items_text)

        if any(i <= 2 for i in range(1, 4)):
            self.tray_icon.showMessage("Expiring Items", "Some items in your list are about to expire!", QSystemTrayIcon.Information, 5000)

    def change_bg_color(self):
        color = QColorDialog.getColor(initial=QColor("#ececec"), parent=self, title="Choose Background Color")
        if color.isValid():
            palette = self.palette()
            palette.setColor(self.backgroundRole(), color)
            self.setPalette(palette)

    def create_action(self, toolbar, text, slot):
        action = QAction(text, self)
        action.triggered.connect(slot)
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        action.setFont(font)
        toolbar.addAction(action)
        return action

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self, file=None):
        if file:
            path = file
        else:
            path, _ = QFileDialog.getOpenFileName(
                self, "Open file", "", "All files (*);;Text files (*.txt);;CSV files (*.csv)"
            )

        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.shopping_list_widget.clear()
                self.shopping_list_widget.addItems(text.splitlines())
                self.update_title()
                self.status.showMessage(f"Opened: {path}")

    def file_save(self):
        if self.path is None:
            return self.file_saveas()
        self._save_to_path(self.path)
        self.status.showMessage(f"Saved: {self.path}")

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "Text files (*.txt);"
        )
        if not path:
            return
        self._save_to_path(path)
        self.status.showMessage(f"Saved As: {path}")

    def _save_to_path(self, path):
        items = [self.shopping_list_widget.item(i).text() for i in range(self.shopping_list_widget.count())]
        text = "\n".join(items)
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            pass

    def download_list_as_pdf(self):
        items = [self.shopping_list_widget.item(i).text() for i in range(self.shopping_list_widget.count())]
        if items:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Shopping List", ln=True, align='C')
            pdf.ln(10)
            for item in items:
                pdf.cell(200, 10, txt=item, ln=True)
            save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
            if save_path:
                pdf.output(save_path)
                QMessageBox.information(self, "Success", "Shopping list saved as PDF!")

    def upload_list_from_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    items = text.splitlines()
                    for item in items:
                        if item.strip():
                            self.shopping_list_widget.addItem(item.strip())
                    QMessageBox.information(self, "Success", "Shopping list loaded from PDF!")
            except Exception as e:
                self.dialog_critical(str(e))

    def update_title(self):
        self.setWindowTitle("%s - Grocery Manager" % (os.path.basename(self.path) if self.path else "Untitled"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Grocery Manager")
    window = GroceryApp()
    sys.exit(app.exec_())
