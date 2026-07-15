import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QPushButton, QLabel, QLineEdit, QTextEdit, 
                             QComboBox, QFileDialog, QListWidget, QListWidgetItem, 
                             QTreeWidget, QTreeWidgetItem, QSplitter, QGroupBox, 
                             QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox, 
                             QFrame, QProgressBar, QScrollArea, QAbstractItemView,
                             QDialog, QStackedWidget, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from fpdf import FPDF
try:
    from .models import Character, Location, Chapter, Scene, Relationship, WorldNote
except ImportError:
    from models import Character, Location, Chapter, Scene, Relationship, WorldNote

# Класс PDF с поддержкой кириллицы
class CyrillicPDF(FPDF):
    def __init__(self, title=""):
        super().__init__()
        self.doc_title = title
        # Загружаем шрифт с поддержкой кириллицы
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        if os.path.exists(font_path):
            self.add_font("Arial", "", font_path)
            self.add_font("Arial", "B", "C:\\Windows\\Fonts\\arialbd.ttf")
        else:
            # Резервный вариант, если Arial не найден
            pass

    def header(self):
        if "arial" in self.fonts:
            self.set_font("Arial", "B", size=10)
        else:
            self.set_font("Helvetica", "B", size=10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, self.doc_title, border=0, ln=1, align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        if "arial" in self.fonts:
            self.set_font("Arial", "", size=8)
        else:
            self.set_font("Helvetica", "", size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Страница {self.page_no()}", border=0, ln=0, align="C")


# --- VIEW 1: DASHBOARD ---
class ProjectDashboard(QWidget):
    project_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Левая часть - Общая информация
        left_box = QGroupBox("Общие сведения о проекте")
        left_layout = QGridLayout(left_box)
        left_layout.setSpacing(10)

        left_layout.addWidget(QLabel("Название романа:"), 0, 0)
        self.title_input = QLineEdit()
        self.title_input.textChanged.connect(self.save_data)
        left_layout.addWidget(self.title_input, 0, 1)

        left_layout.addWidget(QLabel("Автор:"), 1, 0)
        self.author_input = QLineEdit()
        self.author_input.textChanged.connect(self.save_data)
        left_layout.addWidget(self.author_input, 1, 1)

        left_layout.addWidget(QLabel("Жанр:"), 2, 0)
        self.genre_input = QLineEdit()
        self.genre_input.textChanged.connect(self.save_data)
        left_layout.addWidget(self.genre_input, 2, 1)

        left_layout.addWidget(QLabel("Логлайн (одно предложение):"), 3, 0)
        self.logline_input = QLineEdit()
        self.logline_input.textChanged.connect(self.save_data)
        left_layout.addWidget(self.logline_input, 3, 1)

        left_layout.addWidget(QLabel("Синопсис (краткий сюжет):"), 4, 0)
        self.synopsis_input = QTextEdit()
        self.synopsis_input.textChanged.connect(self.save_data)
        left_layout.addWidget(self.synopsis_input, 4, 1)

        left_layout.addWidget(QLabel("Темы и идеи:"), 5, 0)
        self.themes_input = QTextEdit()
        self.themes_input.textChanged.connect(self.save_data)
        left_layout.addWidget(self.themes_input, 5, 1)

        layout.addWidget(left_box, 3)

        # Правая часть - Статистика
        right_box = QGroupBox("Статистика и Прогресс")
        right_layout = QVBoxLayout(right_box)
        right_layout.setSpacing(15)

        self.stats_label = QLabel("Нет активного проекта")
        self.stats_label.setStyleSheet("font-size: 14px; line-height: 1.5;")
        self.stats_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        right_layout.addWidget(self.stats_label)

        right_layout.addWidget(QLabel("Прогресс написания книги:"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        right_layout.addWidget(self.progress_bar)

        # Целевой объем слов
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Цель (слов):"))
        self.target_words_input = QLineEdit("50000")
        self.target_words_input.setFixedWidth(80)
        self.target_words_input.textChanged.connect(self.update_stats)
        target_layout.addWidget(self.target_words_input)
        target_layout.addStretch()
        right_layout.addLayout(target_layout)

        right_layout.addStretch()
        layout.addWidget(right_box, 2)

    def set_project(self, project):
        self.project = project
        if not project:
            self.setEnabled(False)
            return

        self.setEnabled(True)
        # Блокируем сигналы на время загрузки
        self.block_signals(True)
        
        self.title_input.setText(project.title)
        self.author_input.setText(project.author)
        self.genre_input.setText(project.genre)
        self.logline_input.setText(project.logline)
        self.synopsis_input.setPlainText(project.synopsis)
        self.themes_input.setPlainText(project.themes)
        
        self.block_signals(False)
        self.update_stats()

    def block_signals(self, block):
        self.title_input.blockSignals(block)
        self.author_input.blockSignals(block)
        self.genre_input.blockSignals(block)
        self.logline_input.blockSignals(block)
        self.synopsis_input.blockSignals(block)
        self.themes_input.blockSignals(block)

    def save_data(self):
        if not self.project:
            return
        self.project.title = self.title_input.text()
        self.project.author = self.author_input.text()
        self.project.genre = self.genre_input.text()
        self.project.logline = self.logline_input.text()
        self.project.synopsis = self.synopsis_input.toPlainText()
        self.project.themes = self.themes_input.toPlainText()
        self.project_updated.emit()

    def update_stats(self):
        if not self.project:
            self.stats_label.setText("Нет активного проекта")
            self.progress_bar.setValue(0)
            return

        total_words = self.project.get_total_words()
        num_chapters = len(self.project.chapters)
        num_scenes = sum(len(ch.scenes) for ch in self.project.chapters)
        num_chars = len(self.project.characters)
        num_locs = len(self.project.locations)

        stats_text = (
            f"<b>Всего слов:</b> {total_words}<br><br>"
            f"<b>Главы:</b> {num_chapters}<br>"
            f"<b>Сцены:</b> {num_scenes}<br><br>"
            f"<b>Персонажи:</b> {num_chars}<br>"
            f"<b>Локации:</b> {num_locs}<br><br>"
            f"<b>Создан:</b> {self.project.created_at}<br>"
            f"<b>Изменен:</b> {self.project.last_modified}"
        )
        self.stats_label.setText(stats_text)

        # Вычисление прогресса
        try:
            target = int(self.target_words_input.text())
        except ValueError:
            target = 50000

        if target > 0:
            percentage = min(100, int((total_words / target) * 100))
            self.progress_bar.setValue(percentage)
        else:
            self.progress_bar.setValue(0)


# --- VIEW 2: CHARACTERS ---
class CharacterManager(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.selected_char = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Сплиттер для регулировки ширины списка и редактора
        splitter = QSplitter(Qt.Horizontal)

        # Левая колонка - Список персонажей
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        list_group = QGroupBox("Персонажи")
        list_layout = QVBoxLayout(list_group)

        self.char_list = QListWidget()
        self.char_list.currentItemChanged.connect(self.on_char_selected)
        list_layout.addWidget(self.char_list)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.add_character)
        btn_layout.addWidget(self.add_btn)

        self.del_btn = QPushButton("Удалить")
        self.del_btn.setObjectName("dangerButton")
        self.del_btn.clicked.connect(self.delete_character)
        btn_layout.addWidget(self.del_btn)
        
        list_layout.addLayout(btn_layout)
        left_layout.addWidget(list_group)
        splitter.addWidget(left_panel)

        # Правая колонка - Редактор деталей
        self.right_panel = QScrollArea()
        self.right_panel.setWidgetResizable(True)
        self.right_panel.setFrameShape(QFrame.NoFrame)
        
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(5, 5, 5, 5)

        self.editor_group = QGroupBox("Карточка персонажа")
        grid = QGridLayout(self.editor_group)
        grid.setSpacing(12)

        # Аватар
        avatar_box = QGroupBox("Аватар")
        avatar_layout = QVBoxLayout(avatar_box)
        self.avatar_label = QLabel("Нет фото")
        self.avatar_label.setObjectName("charAvatarLabel")
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setFixedSize(120, 150)
        self.avatar_label.setStyleSheet("border-radius: 4px;")
        avatar_layout.addWidget(self.avatar_label)
        
        self.avatar_btn = QPushButton("Выбрать")
        self.avatar_btn.clicked.connect(self.select_avatar)
        avatar_layout.addWidget(self.avatar_btn)
        grid.addWidget(avatar_box, 0, 0, 4, 1)

        # Текстовые поля справа от аватара
        grid.addWidget(QLabel("Имя персонажа:"), 0, 1)
        self.name_input = QLineEdit()
        self.name_input.textChanged.connect(self.save_character)
        grid.addWidget(self.name_input, 0, 2)

        grid.addWidget(QLabel("Роль в сюжете:"), 1, 1)
        self.role_input = QComboBox()
        self.role_input.addItems(["Главный герой", "Антагонист", "Второстепенный персонаж", "Эпизодический персонаж", "Ментор"])
        self.role_input.setEditable(True)
        self.role_input.currentTextChanged.connect(self.save_character)
        grid.addWidget(self.role_input, 1, 2)

        grid.addWidget(QLabel("Возраст:"), 2, 1)
        self.age_input = QLineEdit()
        self.age_input.textChanged.connect(self.save_character)
        grid.addWidget(self.age_input, 2, 2)

        grid.addWidget(QLabel("Пол / Гендер:"), 3, 1)
        self.gender_input = QLineEdit()
        self.gender_input.textChanged.connect(self.save_character)
        grid.addWidget(self.gender_input, 3, 2)

        # Большие блоки ниже
        grid.addWidget(QLabel("Внешность:"), 4, 0)
        self.appearance_input = QTextEdit()
        self.appearance_input.textChanged.connect(self.save_character)
        grid.addWidget(self.appearance_input, 4, 1, 1, 2)

        grid.addWidget(QLabel("Характер и Личность:"), 5, 0)
        self.personality_input = QTextEdit()
        self.personality_input.textChanged.connect(self.save_character)
        grid.addWidget(self.personality_input, 5, 1, 1, 2)

        grid.addWidget(QLabel("Главная цель:"), 6, 0)
        self.goal_input = QTextEdit()
        self.goal_input.textChanged.connect(self.save_character)
        grid.addWidget(self.goal_input, 6, 1, 1, 2)

        grid.addWidget(QLabel("Биография / Предыстория:"), 7, 0)
        self.backstory_input = QTextEdit()
        self.backstory_input.textChanged.connect(self.save_character)
        grid.addWidget(self.backstory_input, 7, 1, 1, 2)

        # Раздел дополнительных свойств
        traits_box = QGroupBox("Дополнительные свойства / Факты")
        traits_layout = QVBoxLayout(traits_box)
        
        self.traits_table = QTableWidget(0, 2)
        self.traits_table.setHorizontalHeaderLabels(["Свойство (напр. Секрет)", "Значение"])
        self.traits_table.horizontalHeader().setStretchLastSection(True)
        self.traits_table.cellChanged.connect(self.on_trait_cell_changed)
        traits_layout.addWidget(self.traits_table)

        traits_btn_layout = QHBoxLayout()
        self.add_trait_btn = QPushButton("Добавить свойство")
        self.add_trait_btn.clicked.connect(self.add_trait)
        traits_btn_layout.addWidget(self.add_trait_btn)
        
        self.del_trait_btn = QPushButton("Удалить свойство")
        self.del_trait_btn.setObjectName("dangerButton")
        self.del_trait_btn.clicked.connect(self.delete_trait)
        traits_btn_layout.addWidget(self.del_trait_btn)
        traits_layout.addLayout(traits_btn_layout)

        grid.addWidget(traits_box, 8, 0, 1, 3)

        detail_layout.addWidget(self.editor_group)
        self.right_panel.setWidget(detail_widget)
        splitter.addWidget(self.right_panel)

        # Настраиваем пропорции сплиттера
        splitter.setSizes([200, 500])
        layout.addWidget(splitter)

        self.editor_group.setEnabled(False)

    def set_project(self, project):
        self.project = project
        self.selected_char = None
        self.char_list.clear()
        
        if not project:
            self.setEnabled(False)
            return

        self.setEnabled(True)
        for char in project.characters:
            item = QListWidgetItem(char.name)
            item.setData(Qt.UserRole, char.id)
            self.char_list.addItem(item)
            
        self.editor_group.setEnabled(False)

    def on_char_selected(self, current, previous):
        if not current:
            self.selected_char = None
            self.editor_group.setEnabled(False)
            return

        char_id = current.data(Qt.UserRole)
        self.selected_char = self.project.get_character_by_id(char_id)
        
        if self.selected_char:
            self.editor_group.setEnabled(True)
            self.block_inputs_signals(True)
            
            self.name_input.setText(self.selected_char.name)
            self.role_input.setCurrentText(self.selected_char.role)
            self.age_input.setText(self.selected_char.age)
            self.gender_input.setText(self.selected_char.gender)
            self.appearance_input.setPlainText(self.selected_char.appearance)
            self.personality_input.setPlainText(self.selected_char.personality)
            self.goal_input.setPlainText(self.selected_char.goal)
            self.backstory_input.setPlainText(self.selected_char.backstory)
            
            # Обновление аватара
            self.update_avatar_display()
            
            # Заполнение таблицы дополнительных свойств
            self.traits_table.blockSignals(True)
            self.traits_table.setRowCount(0)
            for key, val in self.selected_char.custom_fields.items():
                row = self.traits_table.rowCount()
                self.traits_table.insertRow(row)
                self.traits_table.setItem(row, 0, QTableWidgetItem(key))
                self.traits_table.setItem(row, 1, QTableWidgetItem(val))
            self.traits_table.blockSignals(False)
            
            self.block_inputs_signals(False)

    def block_inputs_signals(self, block):
        self.name_input.blockSignals(block)
        self.role_input.blockSignals(block)
        self.age_input.blockSignals(block)
        self.gender_input.blockSignals(block)
        self.appearance_input.blockSignals(block)
        self.personality_input.blockSignals(block)
        self.goal_input.blockSignals(block)
        self.backstory_input.blockSignals(block)

    def add_character(self):
        if not self.project:
            return
        new_char = Character()
        self.project.characters.append(new_char)
        
        item = QListWidgetItem(new_char.name)
        item.setData(Qt.UserRole, new_char.id)
        self.char_list.addItem(item)
        self.char_list.setCurrentItem(item)
        self.name_input.setFocus()
        self.data_changed.emit()

    def delete_character(self):
        if not self.selected_char:
            return
        
        reply = QMessageBox.question(self, "Удалить персонажа?", 
                                     f"Вы действительно хотите удалить персонажа {self.selected_char.name}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.project.characters.remove(self.selected_char)
            # Удаляем связи
            self.project.relationships = [r for r in self.project.relationships 
                                          if r.char_a != self.selected_char.id and r.char_b != self.selected_char.id]
            # Удаляем из сцен
            for ch in self.project.chapters:
                for sc in ch.scenes:
                    if self.selected_char.id in sc.characters:
                        sc.characters.remove(self.selected_char.id)
            
            # Обновляем список
            row = self.char_list.currentRow()
            self.char_list.takeItem(row)
            self.data_changed.emit()

    def save_character(self):
        if not self.selected_char:
            return
        self.selected_char.name = self.name_input.text()
        self.selected_char.role = self.role_input.currentText()
        self.selected_char.age = self.age_input.text()
        self.selected_char.gender = self.gender_input.text()
        self.selected_char.appearance = self.appearance_input.toPlainText()
        self.selected_char.personality = self.personality_input.toPlainText()
        self.selected_char.goal = self.goal_input.toPlainText()
        self.selected_char.backstory = self.backstory_input.toPlainText()
        
        # Обновляем имя в списке
        current_item = self.char_list.currentItem()
        if current_item:
            current_item.setText(self.selected_char.name)
        self.data_changed.emit()

    def select_avatar(self):
        if not self.selected_char:
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать аватар", "", "Изображения (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.selected_char.image_path = file_path
            self.update_avatar_display()
            self.data_changed.emit()

    def update_avatar_display(self):
        if self.selected_char and self.selected_char.image_path and os.path.exists(self.selected_char.image_path):
            pixmap = QPixmap(self.selected_char.image_path)
            scaled_pixmap = pixmap.scaled(self.avatar_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.avatar_label.setPixmap(scaled_pixmap)
        else:
            self.avatar_label.clear()
            self.avatar_label.setText("Нет фото")

    def add_trait(self):
        if not self.selected_char:
            return
        self.traits_table.blockSignals(True)
        row = self.traits_table.rowCount()
        self.traits_table.insertRow(row)
        
        # Инициализируем пустыми элементами
        key_item = QTableWidgetItem("Новое свойство")
        val_item = QTableWidgetItem("Значение")
        self.traits_table.setItem(row, 0, key_item)
        self.traits_table.setItem(row, 1, val_item)
        
        # Записываем в модель
        self.selected_char.custom_fields[key_item.text()] = val_item.text()
        self.traits_table.blockSignals(False)
        self.data_changed.emit()

    def delete_trait(self):
        row = self.traits_table.currentRow()
        if row < 0:
            return
        
        key_item = self.traits_table.item(row, 0)
        if key_item and self.selected_char:
            key = key_item.text()
            if key in self.selected_char.custom_fields:
                del self.selected_char.custom_fields[key]
        
        self.traits_table.removeRow(row)
        self.data_changed.emit()

    def on_trait_cell_changed(self, row, column):
        if not self.selected_char:
            return
            
        key_item = self.traits_table.item(row, 0)
        val_item = self.traits_table.item(row, 1)
        
        if key_item and val_item:
            # Обновляем словарь custom_fields
            # Так как ключ мог измениться, мы перестраиваем словарь по таблице
            self.selected_char.custom_fields.clear()
            for r in range(self.traits_table.rowCount()):
                k = self.traits_table.item(r, 0)
                v = self.traits_table.item(r, 1)
                if k and v:
                    self.selected_char.custom_fields[k.text()] = v.text()
            self.data_changed.emit()


# --- VIEW 3: LOCATIONS ---
class LocationManager(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.selected_loc = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        splitter = QSplitter(Qt.Horizontal)

        # Список локаций
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        list_group = QGroupBox("Локации")
        list_layout = QVBoxLayout(list_group)

        self.loc_list = QListWidget()
        self.loc_list.currentItemChanged.connect(self.on_loc_selected)
        list_layout.addWidget(self.loc_list)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.add_location)
        btn_layout.addWidget(self.add_btn)

        self.del_btn = QPushButton("Удалить")
        self.del_btn.setObjectName("dangerButton")
        self.del_btn.clicked.connect(self.delete_location)
        btn_layout.addWidget(self.del_btn)
        
        list_layout.addLayout(btn_layout)
        left_layout.addWidget(list_group)
        splitter.addWidget(left_panel)

        # Редактор деталей
        self.right_panel = QScrollArea()
        self.right_panel.setWidgetResizable(True)
        self.right_panel.setFrameShape(QFrame.NoFrame)
        
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(5, 5, 5, 5)

        self.editor_group = QGroupBox("Карточка локации")
        grid = QGridLayout(self.editor_group)
        grid.setSpacing(12)

        # Фото локации
        photo_box = QGroupBox("Иллюстрация")
        photo_layout = QVBoxLayout(photo_box)
        self.photo_label = QLabel("Нет изображения")
        self.photo_label.setObjectName("locPhotoLabel")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setFixedSize(150, 110)
        self.photo_label.setStyleSheet("border-radius: 4px;")
        photo_layout.addWidget(self.photo_label)
        
        self.photo_btn = QPushButton("Выбрать")
        self.photo_btn.clicked.connect(self.select_photo)
        photo_layout.addWidget(self.photo_btn)
        grid.addWidget(photo_box, 0, 0, 3, 1)

        # Текстовые поля справа
        grid.addWidget(QLabel("Название локации:"), 0, 1)
        self.name_input = QLineEdit()
        self.name_input.textChanged.connect(self.save_location)
        grid.addWidget(self.name_input, 0, 2)

        grid.addWidget(QLabel("Климат / Окружение:"), 1, 1)
        self.climate_input = QLineEdit()
        self.climate_input.textChanged.connect(self.save_location)
        grid.addWidget(self.climate_input, 1, 2)

        # Большие блоки ниже
        grid.addWidget(QLabel("Значение для сюжета:"), 3, 0)
        self.significance_input = QTextEdit()
        self.significance_input.textChanged.connect(self.save_location)
        grid.addWidget(self.significance_input, 3, 1, 1, 2)

        grid.addWidget(QLabel("Описание локации:"), 4, 0)
        self.description_input = QTextEdit()
        self.description_input.textChanged.connect(self.save_location)
        grid.addWidget(self.description_input, 4, 1, 1, 2)

        # Раздел дополнительных свойств
        traits_box = QGroupBox("Дополнительные факты / детали")
        traits_layout = QVBoxLayout(traits_box)
        
        self.traits_table = QTableWidget(0, 2)
        self.traits_table.setHorizontalHeaderLabels(["Деталь", "Описание"])
        self.traits_table.horizontalHeader().setStretchLastSection(True)
        self.traits_table.cellChanged.connect(self.on_trait_cell_changed)
        traits_layout.addWidget(self.traits_table)

        traits_btn_layout = QHBoxLayout()
        self.add_trait_btn = QPushButton("Добавить деталь")
        self.add_trait_btn.clicked.connect(self.add_trait)
        traits_btn_layout.addWidget(self.add_trait_btn)
        
        self.del_trait_btn = QPushButton("Удалить деталь")
        self.del_trait_btn.setObjectName("dangerButton")
        self.del_trait_btn.clicked.connect(self.delete_trait)
        traits_btn_layout.addWidget(self.del_trait_btn)
        traits_layout.addLayout(traits_btn_layout)

        grid.addWidget(traits_box, 5, 0, 1, 3)

        detail_layout.addWidget(self.editor_group)
        self.right_panel.setWidget(detail_widget)
        splitter.addWidget(self.right_panel)

        splitter.setSizes([200, 500])
        layout.addWidget(splitter)

        self.editor_group.setEnabled(False)

    def set_project(self, project):
        self.project = project
        self.selected_loc = None
        self.loc_list.clear()
        
        if not project:
            self.setEnabled(False)
            return

        self.setEnabled(True)
        for loc in project.locations:
            item = QListWidgetItem(loc.name)
            item.setData(Qt.UserRole, loc.id)
            self.loc_list.addItem(item)
            
        self.editor_group.setEnabled(False)

    def on_loc_selected(self, current, previous):
        if not current:
            self.selected_loc = None
            self.editor_group.setEnabled(False)
            return

        loc_id = current.data(Qt.UserRole)
        self.selected_loc = self.project.get_location_by_id(loc_id)
        
        if self.selected_loc:
            self.editor_group.setEnabled(True)
            self.block_inputs_signals(True)
            
            self.name_input.setText(self.selected_loc.name)
            self.climate_input.setText(self.selected_loc.climate)
            self.significance_input.setPlainText(self.selected_loc.significance)
            self.description_input.setPlainText(self.selected_loc.description)
            
            self.update_photo_display()
            
            # Заполнение таблицы дополнительных свойств
            self.traits_table.blockSignals(True)
            self.traits_table.setRowCount(0)
            for key, val in self.selected_loc.custom_fields.items():
                row = self.traits_table.rowCount()
                self.traits_table.insertRow(row)
                self.traits_table.setItem(row, 0, QTableWidgetItem(key))
                self.traits_table.setItem(row, 1, QTableWidgetItem(val))
            self.traits_table.blockSignals(False)
            
            self.block_inputs_signals(False)

    def block_inputs_signals(self, block):
        self.name_input.blockSignals(block)
        self.climate_input.blockSignals(block)
        self.significance_input.blockSignals(block)
        self.description_input.blockSignals(block)

    def add_location(self):
        if not self.project:
            return
        new_loc = Location()
        self.project.locations.append(new_loc)
        
        item = QListWidgetItem(new_loc.name)
        item.setData(Qt.UserRole, new_loc.id)
        self.loc_list.addItem(item)
        self.loc_list.setCurrentItem(item)
        self.name_input.setFocus()
        self.data_changed.emit()

    def delete_location(self):
        if not self.selected_loc:
            return
        
        reply = QMessageBox.question(self, "Удалить локацию?", 
                                     f"Вы действительно хотите удалить локацию {self.selected_loc.name}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.project.locations.remove(self.selected_loc)
            
            # Удаляем локацию из сцен
            for ch in self.project.chapters:
                for sc in ch.scenes:
                    if self.selected_loc.id in sc.locations:
                        sc.locations.remove(self.selected_loc.id)
            
            row = self.loc_list.currentRow()
            self.loc_list.takeItem(row)
            self.data_changed.emit()

    def save_location(self):
        if not self.selected_loc:
            return
        self.selected_loc.name = self.name_input.text()
        self.selected_loc.climate = self.climate_input.text()
        self.selected_loc.significance = self.significance_input.toPlainText()
        self.selected_loc.description = self.description_input.toPlainText()
        
        current_item = self.loc_list.currentItem()
        if current_item:
            current_item.setText(self.selected_loc.name)
        self.data_changed.emit()

    def select_photo(self):
        if not self.selected_loc:
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Изображения (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.selected_loc.image_path = file_path
            self.update_photo_display()
            self.data_changed.emit()

    def update_photo_display(self):
        if self.selected_loc and self.selected_loc.image_path and os.path.exists(self.selected_loc.image_path):
            pixmap = QPixmap(self.selected_loc.image_path)
            scaled_pixmap = pixmap.scaled(self.photo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(scaled_pixmap)
        else:
            self.photo_label.clear()
            self.photo_label.setText("Нет изображения")

    def add_trait(self):
        if not self.selected_loc:
            return
        self.traits_table.blockSignals(True)
        row = self.traits_table.rowCount()
        self.traits_table.insertRow(row)
        
        key_item = QTableWidgetItem("Деталь")
        val_item = QTableWidgetItem("Описание")
        self.traits_table.setItem(row, 0, key_item)
        self.traits_table.setItem(row, 1, val_item)
        
        self.selected_loc.custom_fields[key_item.text()] = val_item.text()
        self.traits_table.blockSignals(False)
        self.data_changed.emit()

    def delete_trait(self):
        row = self.traits_table.currentRow()
        if row < 0:
            return
        
        key_item = self.traits_table.item(row, 0)
        if key_item and self.selected_loc:
            key = key_item.text()
            if key in self.selected_loc.custom_fields:
                del self.selected_loc.custom_fields[key]
        
        self.traits_table.removeRow(row)
        self.data_changed.emit()

    def on_trait_cell_changed(self, row, column):
        if not self.selected_loc:
            return
            
        key_item = self.traits_table.item(row, 0)
        val_item = self.traits_table.item(row, 1)
        
        if key_item and val_item:
            self.selected_loc.custom_fields.clear()
            for r in range(self.traits_table.rowCount()):
                k = self.traits_table.item(r, 0)
                v = self.traits_table.item(r, 1)
                if k and v:
                    self.selected_loc.custom_fields[k.text()] = v.text()
            self.data_changed.emit()


# --- VIEW 4: PLOT OUTLINE ---
class OutlineManager(QWidget):
    open_in_editor_requested = pyqtSignal(object, object) # Signal: (Chapter, Scene)
    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.selected_item = None # Can be Chapter or Scene
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        splitter = QSplitter(Qt.Horizontal)

        # Левая часть - Дерево Глав и Сцен
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        tree_group = QGroupBox("Структура произведения")
        tree_layout = QVBoxLayout(tree_group)

        self.outline_tree = QTreeWidget()
        self.outline_tree.setHeaderLabel("Главы и Сцены")
        self.outline_tree.currentItemChanged.connect(self.on_item_selected)
        tree_layout.addWidget(self.outline_tree)

        # Кнопки для дерева
        btn_layout_1 = QHBoxLayout()
        self.add_chapter_btn = QPushButton("Добавить главу")
        self.add_chapter_btn.clicked.connect(self.add_chapter)
        btn_layout_1.addWidget(self.add_chapter_btn)

        self.add_scene_btn = QPushButton("Добавить сцену")
        self.add_scene_btn.clicked.connect(self.add_scene)
        btn_layout_1.addWidget(self.add_scene_btn)

        btn_layout_2 = QHBoxLayout()
        self.up_btn = QPushButton("Вверх")
        self.up_btn.clicked.connect(self.move_up)
        btn_layout_2.addWidget(self.up_btn)

        self.down_btn = QPushButton("Вниз")
        self.down_btn.clicked.connect(self.move_down)
        btn_layout_2.addWidget(self.down_btn)

        self.del_btn = QPushButton("Удалить")
        self.del_btn.setObjectName("dangerButton")
        self.del_btn.clicked.connect(self.delete_item)
        btn_layout_2.addWidget(self.del_btn)

        tree_layout.addLayout(btn_layout_1)
        tree_layout.addLayout(btn_layout_2)
        left_layout.addWidget(tree_group)
        splitter.addWidget(left_panel)

        # Правая часть - Редактор свойств Сцены / Главы
        self.right_panel = QScrollArea()
        self.right_panel.setWidgetResizable(True)
        self.right_panel.setFrameShape(QFrame.NoFrame)

        detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(detail_widget)
        self.detail_layout.setContentsMargins(5, 5, 5, 5)

        # Группа для Главы
        self.chapter_group = QGroupBox("Свойства главы")
        chap_form = QVBoxLayout(self.chapter_group)
        chap_form.addWidget(QLabel("Название главы:"))
        self.chapter_title_input = QLineEdit()
        self.chapter_title_input.textChanged.connect(self.save_chapter_data)
        chap_form.addWidget(self.chapter_title_input)
        chap_form.addStretch()

        # Группа для Сцены
        self.scene_group = QGroupBox("Свойства сцены")
        scene_grid = QGridLayout(self.scene_group)
        scene_grid.setSpacing(10)

        scene_grid.addWidget(QLabel("Название сцены:"), 0, 0)
        self.scene_title_input = QLineEdit()
        self.scene_title_input.textChanged.connect(self.save_scene_data)
        scene_grid.addWidget(self.scene_title_input, 0, 1, 1, 2)

        scene_grid.addWidget(QLabel("Статус сцены:"), 1, 0)
        self.scene_status_combo = QComboBox()
        self.scene_status_combo.addItems(["В плане", "В процессе", "Завершено"])
        self.scene_status_combo.currentTextChanged.connect(self.save_scene_data)
        scene_grid.addWidget(self.scene_status_combo, 1, 1, 1, 2)

        scene_grid.addWidget(QLabel("Краткое содержание / Задачи сцены:"), 2, 0)
        self.scene_summary_input = QTextEdit()
        self.scene_summary_input.textChanged.connect(self.save_scene_data)
        scene_grid.addWidget(self.scene_summary_input, 2, 1, 1, 2)

        # Участники сцены
        scene_grid.addWidget(QLabel("Участники персонажи:"), 3, 0)
        self.char_checkbox_scroll = QScrollArea()
        self.char_checkbox_scroll.setWidgetResizable(True)
        self.char_checkbox_widget = QWidget()
        self.char_checkbox_layout = QVBoxLayout(self.char_checkbox_widget)
        self.char_checkbox_layout.setContentsMargins(5, 5, 5, 5)
        self.char_checkbox_scroll.setWidget(self.char_checkbox_widget)
        self.char_checkbox_scroll.setMaximumHeight(120)
        scene_grid.addWidget(self.char_checkbox_scroll, 3, 1, 1, 2)

        # Локации сцены
        scene_grid.addWidget(QLabel("Локации действия:"), 4, 0)
        self.loc_checkbox_scroll = QScrollArea()
        self.loc_checkbox_scroll.setWidgetResizable(True)
        self.loc_checkbox_widget = QWidget()
        self.loc_checkbox_layout = QVBoxLayout(self.loc_checkbox_widget)
        self.loc_checkbox_layout.setContentsMargins(5, 5, 5, 5)
        self.loc_checkbox_scroll.setWidget(self.loc_checkbox_widget)
        self.loc_checkbox_scroll.setMaximumHeight(120)
        scene_grid.addWidget(self.loc_checkbox_scroll, 4, 1, 1, 2)

        # Кнопка открытия редактора текста
        self.open_editor_btn = QPushButton("Начать писать сцену")
        self.open_editor_btn.setObjectName("primaryButton")
        self.open_editor_btn.clicked.connect(self.trigger_open_editor)
        scene_grid.addWidget(self.open_editor_btn, 5, 0, 1, 3)

        self.detail_layout.addWidget(self.chapter_group)
        self.detail_layout.addWidget(self.scene_group)
        self.right_panel.setWidget(detail_widget)
        splitter.addWidget(self.right_panel)

        splitter.setSizes([300, 450])
        layout.addWidget(splitter)

        self.chapter_group.hide()
        self.scene_group.hide()

    def set_project(self, project):
        self.project = project
        self.outline_tree.clear()
        
        if not project:
            self.setEnabled(False)
            return

        self.setEnabled(True)
        self.rebuild_tree()

    def rebuild_tree(self):
        self.outline_tree.blockSignals(True)
        self.outline_tree.clear()
        
        for ch_idx, ch in enumerate(self.project.chapters):
            ch_item = QTreeWidgetItem(self.outline_tree)
            ch_item.setText(0, f"Глава {ch_idx + 1}: {ch.title}")
            ch_item.setData(0, Qt.UserRole, ("chapter", ch.id))
            ch_item.setExpanded(True)
            
            for sc in ch.scenes:
                sc_item = QTreeWidgetItem(ch_item)
                status_icon = "⚪"
                if sc.status == "В процессе":
                    status_icon = "🟡"
                elif sc.status == "Завершено":
                    status_icon = "🟢"
                sc_item.setText(0, f"{status_icon} {sc.title}")
                sc_item.setData(0, Qt.UserRole, ("scene", ch.id, sc.id))
                
        self.outline_tree.blockSignals(False)
        self.chapter_group.hide()
        self.scene_group.hide()

    def on_item_selected(self, current, previous):
        if not current:
            self.chapter_group.hide()
            self.scene_group.hide()
            return

        data = current.data(0, Qt.UserRole)
        if not data:
            return

        if data[0] == "chapter":
            self.scene_group.hide()
            self.chapter_group.show()
            ch_id = data[1]
            
            # Находим главу
            self.selected_item = next((c for c in self.project.chapters if c.id == ch_id), None)
            if self.selected_item:
                self.chapter_title_input.blockSignals(True)
                self.chapter_title_input.setText(self.selected_item.title)
                self.chapter_title_input.blockSignals(False)

        elif data[0] == "scene":
            self.chapter_group.hide()
            self.scene_group.show()
            ch_id = data[1]
            sc_id = data[2]
            
            parent_ch = next((c for c in self.project.chapters if c.id == ch_id), None)
            if parent_ch:
                self.selected_item = next((s for s in parent_ch.scenes if s.id == sc_id), None)
                if self.selected_item:
                    self.scene_title_input.blockSignals(True)
                    self.scene_status_combo.blockSignals(True)
                    self.scene_summary_input.blockSignals(True)
                    
                    self.scene_title_input.setText(self.selected_item.title)
                    self.scene_status_combo.setCurrentText(self.selected_item.status)
                    self.scene_summary_input.setPlainText(self.selected_item.summary)
                    
                    self.scene_title_input.blockSignals(False)
                    self.scene_status_combo.blockSignals(False)
                    self.scene_summary_input.blockSignals(False)
                    
                    # Перестраиваем чекбоксы персонажей и локаций
                    self.rebuild_involvement_checkboxes()

    def rebuild_involvement_checkboxes(self):
        # Персонажи
        # Удаляем старые
        for i in reversed(range(self.char_checkbox_layout.count())):
            item = self.char_checkbox_layout.itemAt(i)
            if item:
                w = item.widget()
                if w:
                    w.setParent(None)
                    w.deleteLater()
            
        for char in self.project.characters:
            cb = QCheckBox(f"{char.name} ({char.role})")
            cb.setChecked(char.id in self.selected_item.characters)
            cb.setProperty("char_id", char.id)
            cb.stateChanged.connect(self.on_character_involvement_changed)
            self.char_checkbox_layout.addWidget(cb)
            
        # Локации
        for i in reversed(range(self.loc_checkbox_layout.count())):
            item = self.loc_checkbox_layout.itemAt(i)
            if item:
                w = item.widget()
                if w:
                    w.setParent(None)
                    w.deleteLater()
            
        for loc in self.project.locations:
            cb = QCheckBox(loc.name)
            cb.setChecked(loc.id in self.selected_item.locations)
            cb.setProperty("loc_id", loc.id)
            cb.stateChanged.connect(self.on_location_involvement_changed)
            self.loc_checkbox_layout.addWidget(cb)

    def on_character_involvement_changed(self, state):
        if not self.selected_item or not isinstance(self.selected_item, Scene):
            return
        sender = self.sender()
        char_id = sender.property("char_id")
        
        if state == Qt.Checked:
            if char_id not in self.selected_item.characters:
                self.selected_item.characters.append(char_id)
        else:
            if char_id in self.selected_item.characters:
                self.selected_item.characters.remove(char_id)
        self.data_changed.emit()

    def on_location_involvement_changed(self, state):
        if not self.selected_item or not isinstance(self.selected_item, Scene):
            return
        sender = self.sender()
        loc_id = sender.property("loc_id")
        
        if state == Qt.Checked:
            if loc_id not in self.selected_item.locations:
                self.selected_item.locations.append(loc_id)
        else:
            if loc_id in self.selected_item.locations:
                self.selected_item.locations.remove(loc_id)
        self.data_changed.emit()

    def add_chapter(self):
        if not self.project:
            return
        order = len(self.project.chapters)
        new_chap = Chapter(title=f"Глава {order + 1}", order=order)
        self.project.chapters.append(new_chap)
        
        self.rebuild_tree()
        # Выделяем новую главу
        for i in range(self.outline_tree.topLevelItemCount()):
            item = self.outline_tree.topLevelItem(i)
            if item.data(0, Qt.UserRole)[1] == new_chap.id:
                self.outline_tree.setCurrentItem(item)
                break
        self.chapter_title_input.setFocus()
        self.data_changed.emit()

    def add_scene(self):
        if not self.project:
            return
        current_item = self.outline_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите главу, в которую хотите добавить сцену.")
            return

        data = current_item.data(0, Qt.UserRole)
        # Если выбрана сцена, добавляем сцену к её родителю (главе)
        ch_id = data[1]
        
        parent_ch = next((c for c in self.project.chapters if c.id == ch_id), None)
        if parent_ch:
            new_sc = Scene(title=f"Сцена {len(parent_ch.scenes) + 1}")
            parent_ch.scenes.append(new_sc)
            
            self.rebuild_tree()
            # Находим и выделяем сцену
            for i in range(self.outline_tree.topLevelItemCount()):
                ch_item = self.outline_tree.topLevelItem(i)
                if ch_item.data(0, Qt.UserRole)[1] == ch_id:
                    ch_item.setExpanded(True)
                    for j in range(ch_item.childCount()):
                        sc_item = ch_item.child(j)
                        if sc_item.data(0, Qt.UserRole)[2] == new_sc.id:
                            self.outline_tree.setCurrentItem(sc_item)
                            break
            self.scene_title_input.setFocus()
            self.data_changed.emit()

    def delete_item(self):
        if not self.selected_item:
            return
            
        if isinstance(self.selected_item, Chapter):
            reply = QMessageBox.question(self, "Удалить главу?", 
                                         f"Вы действительно хотите удалить главу '{self.selected_item.title}' и ВСЕ её сцены?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.project.chapters.remove(self.selected_item)
                # Переиндексируем
                for idx, c in enumerate(self.project.chapters):
                    c.order = idx
                self.rebuild_tree()
                self.data_changed.emit()
                
        elif isinstance(self.selected_item, Scene):
            reply = QMessageBox.question(self, "Удалить сцену?", 
                                         f"Вы действительно хотите удалить сцену '{self.selected_item.title}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Находим родительскую главу
                current_item = self.outline_tree.currentItem()
                data = current_item.data(0, Qt.UserRole)
                ch_id = data[1]
                parent_ch = next((c for c in self.project.chapters if c.id == ch_id), None)
                if parent_ch:
                    parent_ch.scenes.remove(self.selected_item)
                    self.rebuild_tree()
                    self.data_changed.emit()

    def move_up(self):
        current_item = self.outline_tree.currentItem()
        if not current_item:
            return
        data = current_item.data(0, Qt.UserRole)
        
        if data[0] == "chapter":
            ch_id = data[1]
            ch_idx = next((i for i, c in enumerate(self.project.chapters) if c.id == ch_id), None)
            if ch_idx is not None and ch_idx > 0:
                # Меняем местами в массиве
                self.project.chapters[ch_idx], self.project.chapters[ch_idx - 1] = \
                    self.project.chapters[ch_idx - 1], self.project.chapters[ch_idx]
                # Корректируем order
                self.project.chapters[ch_idx].order = ch_idx
                self.project.chapters[ch_idx - 1].order = ch_idx - 1
                self.rebuild_tree()
                self.outline_tree.setCurrentItem(self.outline_tree.topLevelItem(ch_idx - 1))
                self.data_changed.emit()
                
        elif data[0] == "scene":
            ch_id = data[1]
            sc_id = data[2]
            parent_ch = next((c for c in self.project.chapters if c.id == ch_id), None)
            if parent_ch:
                sc_idx = next((i for i, s in enumerate(parent_ch.scenes) if s.id == sc_id), None)
                if sc_idx is not None and sc_idx > 0:
                    parent_ch.scenes[sc_idx], parent_ch.scenes[sc_idx - 1] = \
                        parent_ch.scenes[sc_idx - 1], parent_ch.scenes[sc_idx]
                    self.rebuild_tree()
                    # Восстанавливаем выделение
                    ch_item = self.outline_tree.findItems(f"* Глава*", Qt.MatchWildcard)[0] # Упрощенно найдем
                    # Находим нужный элемент дерева
                    for i in range(self.outline_tree.topLevelItemCount()):
                        ti = self.outline_tree.topLevelItem(i)
                        if ti.data(0, Qt.UserRole)[1] == ch_id:
                            self.outline_tree.setCurrentItem(ti.child(sc_idx - 1))
                            break
                    self.data_changed.emit()

    def move_down(self):
        current_item = self.outline_tree.currentItem()
        if not current_item:
            return
        data = current_item.data(0, Qt.UserRole)
        
        if data[0] == "chapter":
            ch_id = data[1]
            ch_idx = next((i for i, c in enumerate(self.project.chapters) if c.id == ch_id), None)
            if ch_idx is not None and ch_idx < len(self.project.chapters) - 1:
                self.project.chapters[ch_idx], self.project.chapters[ch_idx + 1] = \
                    self.project.chapters[ch_idx + 1], self.project.chapters[ch_idx]
                self.project.chapters[ch_idx].order = ch_idx
                self.project.chapters[ch_idx + 1].order = ch_idx + 1
                self.rebuild_tree()
                self.outline_tree.setCurrentItem(self.outline_tree.topLevelItem(ch_idx + 1))
                self.data_changed.emit()
                
        elif data[0] == "scene":
            ch_id = data[1]
            sc_id = data[2]
            parent_ch = next((c for c in self.project.chapters if c.id == ch_id), None)
            if parent_ch:
                sc_idx = next((i for i, s in enumerate(parent_ch.scenes) if s.id == sc_id), None)
                if sc_idx is not None and sc_idx < len(parent_ch.scenes) - 1:
                    parent_ch.scenes[sc_idx], parent_ch.scenes[sc_idx + 1] = \
                        parent_ch.scenes[sc_idx + 1], parent_ch.scenes[sc_idx]
                    self.rebuild_tree()
                    for i in range(self.outline_tree.topLevelItemCount()):
                        ti = self.outline_tree.topLevelItem(i)
                        if ti.data(0, Qt.UserRole)[1] == ch_id:
                            self.outline_tree.setCurrentItem(ti.child(sc_idx + 1))
                            break
                    self.data_changed.emit()

    def save_chapter_data(self):
        if not self.selected_item or not isinstance(self.selected_item, Chapter):
            return
        self.selected_item.title = self.chapter_title_input.text()
        # Обновляем в дереве
        current_item = self.outline_tree.currentItem()
        if current_item:
            data = current_item.data(0, Qt.UserRole)
            # Находим индекс главы
            ch_idx = next((i for i, c in enumerate(self.project.chapters) if c.id == data[1]), 0)
            current_item.setText(0, f"Глава {ch_idx + 1}: {self.selected_item.title}")
        self.data_changed.emit()

    def save_scene_data(self):
        if not self.selected_item or not isinstance(self.selected_item, Scene):
            return
        self.selected_item.title = self.scene_title_input.text()
        self.selected_item.status = self.scene_status_combo.currentText()
        self.selected_item.summary = self.scene_summary_input.toPlainText()
        
        # Обновляем в дереве статус-иконку
        current_item = self.outline_tree.currentItem()
        if current_item:
            status_icon = "⚪"
            if self.selected_item.status == "В процессе":
                status_icon = "🟡"
            elif self.selected_item.status == "Завершено":
                status_icon = "🟢"
            current_item.setText(0, f"{status_icon} {self.selected_item.title}")
        self.data_changed.emit()

    def trigger_open_editor(self):
        if not self.selected_item or not isinstance(self.selected_item, Scene):
            return
            
        current_item = self.outline_tree.currentItem()
        ch_id = current_item.data(0, Qt.UserRole)[1]
        parent_ch = next((c for c in self.project.chapters if c.id == ch_id), None)
        
        if parent_ch and self.selected_item:
            self.open_in_editor_requested.emit(parent_ch, self.selected_item)


# --- VIEW 5: NOVEL EDITOR ---
class NovelEditor(QWidget):
    scene_text_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.chapter = None
        self.scene = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        splitter = QSplitter(Qt.Horizontal)

        # Левая часть - Текстовый редактор
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        
        # Шапка редактора
        self.header_label = QLabel("Выберите сцену в структуре для начала написания")
        self.header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #9d4edd; padding-bottom: 5px;")
        editor_layout.addWidget(self.header_label)

        # Текстовое поле
        self.text_editor = QTextEdit()
        self.text_editor.setObjectName("novelTextEditor")
        self.text_editor.setStyleSheet("font-size: 15px; line-height: 1.6; padding: 15px;")
        self.text_editor.setPlaceholderText("Начните писать вашу историю здесь...")
        self.text_editor.textChanged.connect(self.on_text_changed)
        editor_layout.addWidget(self.text_editor)

        # Нижняя панель
        bottom_bar = QHBoxLayout()
        self.word_count_label = QLabel("Слов: 0 | Символов: 0")
        self.word_count_label.setStyleSheet("color: #8a8a9f;")
        bottom_bar.addWidget(self.word_count_label)
        bottom_bar.addStretch()
        
        # Кнопка Экспорта
        self.export_btn = QPushButton("Экспортировать текст")
        self.export_btn.setObjectName("primaryButton")
        self.export_btn.clicked.connect(self.show_export_dialog)
        bottom_bar.addWidget(self.export_btn)
        
        editor_layout.addLayout(bottom_bar)
        splitter.addWidget(editor_widget)

        # Правая часть - Боковая панель заметок сцены
        sidebar = QGroupBox("Информация о сцене")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(12)

        sidebar_layout.addWidget(QLabel("Задачи / Синопсис сцены:"))
        self.scene_summary_display = QTextEdit()
        self.scene_summary_display.setObjectName("sceneSummaryDisplay")
        self.scene_summary_display.setReadOnly(True)
        self.scene_summary_display.setMaximumHeight(100)
        self.scene_summary_display.setStyleSheet("")
        sidebar_layout.addWidget(self.scene_summary_display)

        sidebar_layout.addWidget(QLabel("Участники персонажи:"))
        self.chars_display = QLabel("Не выбраны")
        self.chars_display.setObjectName("sceneCharsDisplay")
        self.chars_display.setWordWrap(True)
        self.chars_display.setStyleSheet("padding: 6px; border-radius: 4px;")
        sidebar_layout.addWidget(self.chars_display)

        sidebar_layout.addWidget(QLabel("Локации:"))
        self.locs_display = QLabel("Не выбраны")
        self.locs_display.setObjectName("sceneLocsDisplay")
        self.locs_display.setWordWrap(True)
        self.locs_display.setStyleSheet("padding: 6px; border-radius: 4px;")
        sidebar_layout.addWidget(self.locs_display)

        sidebar_layout.addStretch()
        splitter.addWidget(sidebar)

        splitter.setSizes([500, 200])
        layout.addWidget(splitter)

        self.setEnabled(False)

    def set_project(self, project):
        self.project = project
        self.chapter = None
        self.scene = None
        self.text_editor.clear()
        self.header_label.setText("Выберите сцену в структуре для начала написания")
        self.setEnabled(False)

    def open_scene(self, chapter, scene):
        self.setEnabled(True)
        self.chapter = chapter
        self.scene = scene

        # Обновляем шапку
        ch_idx = next((i for i, c in enumerate(self.project.chapters) if c.id == chapter.id), 0)
        self.header_label.setText(f"Глава {ch_idx + 1}: {chapter.title} > {scene.title}")

        # Устанавливаем текст без вызова сигнала textChanged во избежание ложной перезаписи
        self.text_editor.blockSignals(True)
        self.text_editor.setPlainText(scene.content)
        self.text_editor.blockSignals(False)

        # Обновляем сайдбар
        self.scene_summary_display.setPlainText(scene.summary)
        
        # Обновляем участников
        char_names = []
        for cid in scene.characters:
            char = self.project.get_character_by_id(cid)
            if char:
                char_names.append(char.name)
        self.chars_display.setText(", ".join(char_names) if char_names else "Не выбраны")

        # Обновляем локации
        loc_names = []
        for lid in scene.locations:
            loc = self.project.get_location_by_id(lid)
            if loc:
                loc_names.append(loc.name)
        self.locs_display.setText(", ".join(loc_names) if loc_names else "Не выбраны")

        self.update_counts()

    def on_text_changed(self):
        if not self.scene:
            return
        # Сохраняем в модель
        self.scene.content = self.text_editor.toPlainText()
        self.scene.update_word_count()
        self.update_counts()
        self.scene_text_changed.emit()

    def update_counts(self):
        if not self.scene:
            return
        text = self.text_editor.toPlainText()
        words = len([w for w in text.strip().split() if w])
        chars = len(text)
        self.word_count_label.setText(f"Слов: {words} | Символов: {chars}")

    def show_export_dialog(self):
        if not self.scene:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Экспорт произведения")
        dialog.setFixedWidth(350)
        dialog_layout = QVBoxLayout(dialog)

        dialog_layout.addWidget(QLabel("<b>Выберите область экспорта:</b>"))
        
        scope_combo = QComboBox()
        scope_combo.addItems(["Текущая сцена", "Текущая глава", "Вся книга"])
        dialog_layout.addWidget(scope_combo)

        dialog_layout.addWidget(QLabel("<b>Выберите формат:</b>"))
        format_combo = QComboBox()
        format_combo.addItems(["Текстовый файл (.txt)", "Книга FB2 (.fb2)", "Документ PDF (.pdf)"])
        dialog_layout.addWidget(format_combo)

        btn_box = QHBoxLayout()
        export_run = QPushButton("Экспорт")
        export_run.setObjectName("primaryButton")
        cancel_btn = QPushButton("Отмена")
        btn_box.addWidget(export_run)
        btn_box.addWidget(cancel_btn)
        dialog_layout.addLayout(btn_box)

        cancel_btn.clicked.connect(dialog.reject)
        
        def run_export():
            scope = scope_combo.currentText()
            fmt = format_combo.currentText()
            dialog.accept()
            self.execute_export(scope, fmt)

        export_run.clicked.connect(run_export)
        dialog.exec_()

    def generate_fb2(self, scope):
        def esc(text):
            if not text:
                return ""
            return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        author_name = esc(self.project.author)
        first_name = author_name
        last_name = ""
        if " " in author_name:
            parts = author_name.split(" ", 1)
            first_name = parts[0]
            last_name = parts[1]

        book_title = esc(self.project.title)
        genre = "prose"
        synopsis = esc(self.project.synopsis)
        
        fb2_data = []
        fb2_data.append('<?xml version="1.0" encoding="utf-8"?>')
        fb2_data.append('<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">')
        
        fb2_data.append('  <description>')
        fb2_data.append('    <title-info>')
        fb2_data.append(f'      <genre>{genre}</genre>')
        fb2_data.append('      <author>')
        fb2_data.append(f'        <first-name>{first_name}</first-name>')
        if last_name:
            fb2_data.append(f'        <last-name>{last_name}</last-name>')
        fb2_data.append('      </author>')
        fb2_data.append(f'      <book-title>{book_title}</book-title>')
        if synopsis:
            fb2_data.append('      <annotation>')
            fb2_data.append(f'        <p>{synopsis}</p>')
            fb2_data.append('      </annotation>')
        fb2_data.append('      <lang>ru</lang>')
        fb2_data.append('    </title-info>')
        
        fb2_data.append('    <document-info>')
        fb2_data.append('      <author>')
        fb2_data.append(f'        <first-name>{first_name}</first-name>')
        if last_name:
            fb2_data.append(f'        <last-name>{last_name}</last-name>')
        fb2_data.append('      </author>')
        fb2_data.append('      <program-used>Nwrite</program-used>')
        fb2_data.append(f'      <id>{esc(self.project.title)}</id>')
        fb2_data.append('      <version>1.0</version>')
        fb2_data.append('    </document-info>')
        fb2_data.append('  </description>')
        
        fb2_data.append('  <body>')
        fb2_data.append(f'    <title><p>{book_title}</p></title>')
        
        if scope == "Текущая сцена":
            fb2_data.append('    <section>')
            fb2_data.append(f'      <title><p>{esc(self.scene.title)}</p></title>')
            for p in self.scene.content.split('\n'):
                p_s = p.strip()
                if p_s:
                    fb2_data.append(f'      <p>{esc(p_s)}</p>')
            fb2_data.append('    </section>')
            
        elif scope == "Текущая глава":
            fb2_data.append('    <section>')
            fb2_data.append(f'      <title><p>{esc(self.chapter.title)}</p></title>')
            for sc in self.chapter.scenes:
                fb2_data.append('      <section>')
                fb2_data.append(f'        <title><p>{esc(sc.title)}</p></title>')
                for p in sc.content.split('\n'):
                    p_s = p.strip()
                    if p_s:
                        fb2_data.append(f'        <p>{esc(p_s)}</p>')
                fb2_data.append('      </section>')
            fb2_data.append('    </section>')
            
        elif scope == "Вся книга":
            for ch_idx, ch in enumerate(self.project.chapters):
                fb2_data.append('    <section>')
                fb2_data.append(f'      <title><p>Глава {ch_idx + 1}: {esc(ch.title)}</p></title>')
                for sc in ch.scenes:
                    fb2_data.append('      <section>')
                    fb2_data.append(f'        <title><p>{esc(sc.title)}</p></title>')
                    for p in sc.content.split('\n'):
                        p_s = p.strip()
                        if p_s:
                            fb2_data.append(f'        <p>{esc(p_s)}</p>')
                    fb2_data.append('      </section>')
                fb2_data.append('    </section>')
                
        fb2_data.append('  </body>')
        fb2_data.append('</FictionBook>')
        
        return '\n'.join(fb2_data)

    def generate_pdf_book(self, scope, file_path):
        pdf = CyrillicPDF(title=self.project.title)
        
        def set_font_style(style="", size=12):
            font_name = "Arial" if "arial" in pdf.fonts else "Helvetica"
            pdf.set_font(font_name, style=style, size=size)

        # 1. Титульный лист (только для всей книги)
        if scope == "Вся книга":
            pdf.add_page()
            
            # Вертикальное центрирование названия и автора на первом листе
            pdf.set_y(100)
            
            # Название
            set_font_style("B", 26)
            pdf.cell(0, 15, self.project.title, ln=1, align="C")
            pdf.ln(10)
            
            # Автор
            if self.project.author:
                set_font_style("", 16)
                pdf.set_text_color(60, 60, 60)
                pdf.cell(0, 10, self.project.author, ln=1, align="C")
                pdf.set_text_color(0, 0, 0)
                
            # Переходим на вторую страницу для Аннотации
            pdf.add_page()
            
            # Аннотация на втором листе
            if self.project.synopsis:
                pdf.ln(30)
                set_font_style("B", 16)
                pdf.cell(0, 12, "Аннотация", ln=1, align="C")
                pdf.ln(10)
                set_font_style("", 12)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(0, 7, self.project.synopsis, align="C")
                pdf.set_text_color(0, 0, 0)
                
            pdf.add_page()

        # 2. Добавление содержимого
        if scope == "Текущая сцена":
            pdf.add_page()
            set_font_style("B", 18)
            pdf.cell(0, 12, self.scene.title, ln=1, align="L")
            pdf.ln(10)
            
            set_font_style("", 12)
            for p in self.scene.content.split('\n'):
                p_s = p.strip()
                if p_s:
                    pdf.cell(10, 8, "") # Абзацный отступ
                    pdf.multi_cell(0, 8, p_s)
                    pdf.ln(2)

        elif scope == "Текущая глава":
            pdf.add_page()
            set_font_style("B", 20)
            pdf.cell(0, 15, self.chapter.title, ln=1, align="C")
            pdf.ln(10)
            
            for sc in self.chapter.scenes:
                set_font_style("B", 14)
                pdf.cell(0, 10, sc.title, ln=1, align="L")
                pdf.ln(5)
                
                set_font_style("", 12)
                for p in sc.content.split('\n'):
                    p_s = p.strip()
                    if p_s:
                        pdf.cell(10, 8, "")
                        pdf.multi_cell(0, 8, p_s)
                        pdf.ln(2)
                pdf.ln(10)

        elif scope == "Вся книга":
            for ch_idx, ch in enumerate(self.project.chapters):
                pdf.add_page()
                pdf.ln(20)
                
                set_font_style("B", 20)
                pdf.cell(0, 15, f"Глава {ch_idx + 1}: {ch.title}", ln=1, align="C")
                pdf.ln(15)
                
                for sc in ch.scenes:
                    set_font_style("B", 14)
                    pdf.cell(0, 10, sc.title, ln=1, align="L")
                    pdf.ln(5)
                    
                    set_font_style("", 12)
                    for p in sc.content.split('\n'):
                        p_s = p.strip()
                        if p_s:
                            pdf.cell(10, 8, "")
                            pdf.multi_cell(0, 8, p_s)
                            pdf.ln(2)
                    pdf.ln(10)
                    
        pdf.output(file_path)

    def execute_export(self, scope, fmt):
        export_title = ""
        export_content = ""

        if scope == "Текущая сцена":
            export_title = f"{self.chapter.title} - {self.scene.title}"
            export_content = f"=== {self.scene.title} ===\n\n{self.scene.content}"
        elif scope == "Текущая глава":
            export_title = self.chapter.title
            export_content = f"=== {self.chapter.title} ===\n\n"
            for sc in self.chapter.scenes:
                export_content += f"--- {sc.title} ---\n\n{sc.content}\n\n"
        elif scope == "Вся книга":
            export_title = self.project.title
            export_content = f"====== {self.project.title} ======\n"
            if self.project.author:
                export_content += f"Автор: {self.project.author}\n"
            export_content += "\n\n"
            
            for ch_idx, ch in enumerate(self.project.chapters):
                export_content += f"Глава {ch_idx + 1}: {ch.title}\n"
                export_content += "=" * 30 + "\n\n"
                for sc in ch.scenes:
                    export_content += f"[{sc.title}]\n\n{sc.content}\n\n"
                export_content += "\n"

        # Сохранение в файл
        if "txt" in fmt:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить TXT", f"{export_title}.txt", "Text Files (*.txt)")
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(export_content)
                    QMessageBox.information(self, "Успех", "Текст успешно экспортирован!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
                    
        elif "fb2" in fmt:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить FB2", f"{export_title}.fb2", "FictionBook Files (*.fb2)")
            if file_path:
                try:
                    fb2_content = self.generate_fb2(scope)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(fb2_content)
                    QMessageBox.information(self, "Успех", "Книга FB2 успешно экспортирована!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить FB2:\n{str(e)}")
                    
        elif "pdf" in fmt:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить PDF", f"{export_title}.pdf", "PDF Files (*.pdf)")
            if file_path:
                try:
                    self.generate_pdf_book(scope, file_path)
                    QMessageBox.information(self, "Успех", "PDF успешно экспортирован!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить PDF:\n{str(e)}")


# --- VIEW 6: RELATIONSHIPS ---
class RelationshipManager(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        table_group = QGroupBox("Связи между персонажами")
        table_layout = QVBoxLayout(table_group)

        self.rel_table = QTableWidget(0, 3)
        self.rel_table.setHorizontalHeaderLabels(["Персонаж А", "Связь (тип отношений)", "Персонаж Б"])
        self.rel_table.horizontalHeader().setStretchLastSection(True)
        self.rel_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.rel_table.setSelectionMode(QAbstractItemView.SingleSelection)
        table_layout.addWidget(self.rel_table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить связь")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.add_relationship)
        btn_layout.addWidget(self.add_btn)

        self.del_btn = QPushButton("Удалить связь")
        self.del_btn.setObjectName("dangerButton")
        self.del_btn.clicked.connect(self.delete_relationship)
        btn_layout.addWidget(self.del_btn)
        
        table_layout.addLayout(btn_layout)
        layout.addWidget(table_group)

    def set_project(self, project):
        self.project = project
        self.rel_table.setRowCount(0)
        
        if not project:
            self.setEnabled(False)
            return

        self.setEnabled(True)
        self.rebuild_table()

    def rebuild_table(self):
        self.rel_table.blockSignals(True)
        self.rel_table.setRowCount(0)
        
        char_list = [c.name for c in self.project.characters]
        
        for rel in self.project.relationships:
            row = self.rel_table.rowCount()
            self.rel_table.insertRow(row)

            # Combo A
            combo_a = QComboBox()
            combo_a.addItems(char_list)
            char_a_obj = self.project.get_character_by_id(rel.char_a)
            if char_a_obj:
                combo_a.setCurrentText(char_a_obj.name)
            combo_a.currentTextChanged.connect(lambda text, r=row: self.update_relation_char(r, "char_a", text))
            self.rel_table.setCellWidget(row, 0, combo_a)

            # Input Description
            desc_input = QLineEdit(rel.description)
            desc_input.textChanged.connect(lambda text, r=row: self.update_relation_desc(r, text))
            self.rel_table.setCellWidget(row, 1, desc_input)

            # Combo B
            combo_b = QComboBox()
            combo_b.addItems(char_list)
            char_b_obj = self.project.get_character_by_id(rel.char_b)
            if char_b_obj:
                combo_b.setCurrentText(char_b_obj.name)
            combo_b.currentTextChanged.connect(lambda text, r=row: self.update_relation_char(r, "char_b", text))
            self.rel_table.setCellWidget(row, 2, combo_b)

        self.rel_table.blockSignals(False)

    def add_relationship(self):
        if not self.project or len(self.project.characters) < 2:
            QMessageBox.warning(self, "Внимание", "Для установления связей необходимо создать минимум двух персонажей.")
            return

        # Берём первых двух персонажей
        char_a = self.project.characters[0].id
        char_b = self.project.characters[1].id
        
        new_rel = Relationship(char_a, char_b, "Знакомые")
        self.project.relationships.append(new_rel)
        
        self.rebuild_table()
        self.data_changed.emit()

    def delete_relationship(self):
        row = self.rel_table.currentRow()
        if row < 0:
            return
        
        self.project.relationships.pop(row)
        self.rebuild_table()
        self.data_changed.emit()

    def update_relation_char(self, row, key, name):
        if not self.project or row >= len(self.project.relationships):
            return
        
        # Ищем ID персонажа по имени
        char_obj = next((c for c in self.project.characters if c.name == name), None)
        if char_obj:
            if key == "char_a":
                self.project.relationships[row].char_a = char_obj.id
            else:
                self.project.relationships[row].char_b = char_obj.id
        self.data_changed.emit()

    def update_relation_desc(self, row, text):
        if not self.project or row >= len(self.project.relationships):
            return
        self.project.relationships[row].description = text
        self.data_changed.emit()


# --- VIEW 7: WORLD BUILDER ---
class CategoryCard(QFrame):
    clicked = pyqtSignal(str) # category name

    def __init__(self, title, desc, icon, parent=None):
        super().__init__(parent)
        self.title = title
        self.setObjectName("categoryCard")
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)
        
        # Icon
        self.icon_label = QLabel(icon)
        self.icon_label.setStyleSheet("font-size: 28px; background: transparent;")
        layout.addWidget(self.icon_label)
        
        # Text layout (vertical)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 15px; font-weight: bold; background: transparent;")
        
        self.desc_label = QLabel(desc)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("font-size: 11px; color: #8e8e93; background: transparent;")
        
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.desc_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Add chevron at the end
        chevron = QLabel("›")
        chevron.setStyleSheet("font-size: 20px; color: #8e8e93; background: transparent;")
        layout.addWidget(chevron)

    def mousePressEvent(self, event):
        self.clicked.emit(self.title)


# --- VIEW 7: WORLD BUILDER ---
class WorldManager(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.selected_note = None
        self.current_category = ""
        
        self.categories = [
            "История",
            "Экономика",
            "Политика",
            "Религия",
            "География и физические законы",
            "Культура",
            "Обитатели",
            "Магия"
        ]
        self.category_descriptions = {
            "История": "Эпоха. Исторические события. Технологии.",
            "Экономика": "Валюты. Ресурсы. Известные компании.",
            "Политика": "Системы правления. Социальная структура.",
            "Религия": "Божества. Мифы и легенды. Ритуалы.",
            "География и физические законы": "Карта мира.",
            "Культура": "Языки. Предметы искусства. Мода.",
            "Обитатели": "Расы. Животные. Растения.",
            "Магия": "Виды магии. Ограничения. Заклинания."
        }
        self.category_icons = {
            "История": "📜",
            "Экономика": "🪙",
            "Политика": "⚖️",
            "Религия": "🙏",
            "География и физические законы": "🗺️",
            "Культура": "🎭",
            "Обитатели": "🌿",
            "Магия": "✨"
        }
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # QStackedWidget для переключения между категориями и списком заметок
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # --- СТРАНИЦА 1: КАТЕГОРИИ (Dashboard) ---
        self.categories_page = QWidget()
        cat_layout = QVBoxLayout(self.categories_page)
        cat_layout.setContentsMargins(15, 15, 15, 15)
        cat_layout.setSpacing(15)

        # Шапка
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        self.header_title = QLabel("Мир")
        self.header_title.setObjectName("titleLabel")
        self.header_subtitle = QLabel("Загрузка...")
        self.header_subtitle.setObjectName("subtitleLabel")
        header_layout.addWidget(self.header_title)
        header_layout.addWidget(self.header_subtitle)
        cat_layout.addLayout(header_layout)

        # Сетка с карточками
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(12)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # Заполняем сетку
        self.cards = {}
        for idx, cat in enumerate(self.categories):
            desc = self.category_descriptions[cat]
            icon = self.category_icons[cat]
            card = CategoryCard(cat, desc, icon)
            card.clicked.connect(self.on_category_clicked)
            self.cards[cat] = card
            
        self.adjust_grid_layout()

        scroll_area.setWidget(scroll_content)
        cat_layout.addWidget(scroll_area)
        self.stacked_widget.addWidget(self.categories_page)

        # --- СТРАНИЦА 2: ЗАПИСИ (Редактор категории) ---
        self.editor_page = QWidget()
        ed_layout = QVBoxLayout(self.editor_page)
        ed_layout.setContentsMargins(15, 15, 15, 15)
        ed_layout.setSpacing(10)

        # Верхняя панель (кнопка назад и название)
        top_bar = QHBoxLayout()
        back_btn = QPushButton("⬅ Назад к категориям")
        back_btn.clicked.connect(self.show_categories)
        top_bar.addWidget(back_btn)
        
        self.category_label = QLabel("")
        self.category_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0a84ff; margin-left: 10px;")
        top_bar.addWidget(self.category_label)
        top_bar.addStretch()
        ed_layout.addLayout(top_bar)

        # Сплиттер
        splitter = QSplitter(Qt.Horizontal)

        # Левая часть - Список записей
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        list_group = QGroupBox("Записи")
        list_layout = QVBoxLayout(list_group)
        
        self.notes_list = QListWidget()
        self.notes_list.currentItemChanged.connect(self.on_note_selected)
        list_layout.addWidget(self.notes_list)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.add_note)
        btn_layout.addWidget(self.add_btn)

        self.del_btn = QPushButton("Удалить")
        self.del_btn.setObjectName("dangerButton")
        self.del_btn.clicked.connect(self.delete_note)
        btn_layout.addWidget(self.del_btn)
        list_layout.addLayout(btn_layout)
        
        left_layout.addWidget(list_group)
        splitter.addWidget(left_panel)

        # Правая часть - Редактор содержания
        self.right_panel = QWidget()
        self.right_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.editor_group = QGroupBox("Содержание записи")
        editor_layout = QVBoxLayout(self.editor_group)
        editor_layout.setSpacing(12)
        editor_layout.setContentsMargins(15, 20, 15, 15)

        # Horizontal layout for metadata (title and category side-by-side)
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(15)

        # Title input layout
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        title_label = QLabel("Название:")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Введите название записи...")
        self.title_input.textChanged.connect(self.save_note)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        meta_layout.addLayout(title_layout, 3) # Stretch factor 3

        # Category combo layout
        cat_layout = QHBoxLayout()
        cat_layout.setSpacing(8)
        cat_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories)
        self.category_combo.currentTextChanged.connect(self.save_note)
        cat_layout.addWidget(cat_label)
        cat_layout.addWidget(self.category_combo)
        meta_layout.addLayout(cat_layout, 2) # Stretch factor 2

        editor_layout.addLayout(meta_layout)

        # Content text label and area
        editor_layout.addWidget(QLabel("Описание / Текст:"))
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Введите подробное описание или текст для этой записи...")
        self.content_input.textChanged.connect(self.save_note)
        self.content_input.setStyleSheet("font-size: 14px; line-height: 1.5; padding: 10px;")
        editor_layout.addWidget(self.content_input, 1) # Stretch factor 1

        right_layout.addWidget(self.editor_group)
        splitter.addWidget(self.right_panel)

        splitter.setSizes([240, 760])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        ed_layout.addWidget(splitter, 1)
        self.stacked_widget.addWidget(self.editor_page)

        self.stacked_widget.setCurrentIndex(0)
        self.editor_group.setEnabled(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_grid_layout()

    def adjust_grid_layout(self):
        if not hasattr(self, 'grid_layout') or not hasattr(self, 'cards'):
            return
            
        width = self.width()
        
        # Calculate dynamic columns based on actual width
        if width < 550:
            cols = 1
        elif width < 950:
            cols = 2
        elif width < 1400:
            cols = 3
        else:
            cols = 4
            
        # Clear existing row/column stretch configurations
        for r in range(self.grid_layout.rowCount()):
            self.grid_layout.setRowStretch(r, 0)
        for c in range(self.grid_layout.columnCount()):
            self.grid_layout.setColumnStretch(c, 0)
            
        for cat, card in self.cards.items():
            self.grid_layout.removeWidget(card)
            
        # Re-add widgets based on the new layout cols
        for idx, cat in enumerate(self.categories):
            card = self.cards[cat]
            row = idx // cols
            col = idx % cols
            self.grid_layout.addWidget(card, row, col)
            
        # Set stretch factor on columns to distribute width evenly
        for c in range(cols):
            self.grid_layout.setColumnStretch(c, 1)
            
        # Set row stretch at the bottom row to prevent cards from stretching vertically
        last_row = len(self.categories) // cols
        if len(self.categories) % cols != 0:
            last_row += 1
        self.grid_layout.setRowStretch(last_row, 1)

    def map_category(self, cat):
        mapping = {
            "Политика": "Политика",
            "Экономика": "Экономика",
            "Магия / Технологии": "Магия",
            "История мира": "История",
            "География / Климат": "География и физические законы",
            "Фауна и Флора": "Обитатели",
            "Другое": "Культура"
        }
        return mapping.get(cat, cat)

    def set_project(self, project):
        self.project = project
        self.selected_note = None
        
        if not project:
            self.setEnabled(False)
            return

        self.setEnabled(True)
        
        # Нормализуем категории у старых записей
        for note in self.project.world_notes:
            note.category = self.map_category(note.category)
            
        self.header_subtitle.setText(project.title)
        self.show_categories()

    def show_categories(self):
        self.stacked_widget.setCurrentIndex(0)
        self.selected_note = None

    def on_category_clicked(self, category_name):
        self.current_category = category_name
        self.category_label.setText(category_name)
        self.rebuild_list()
        self.editor_group.setEnabled(False)
        self.stacked_widget.setCurrentIndex(1)

    def rebuild_list(self):
        self.notes_list.blockSignals(True)
        self.notes_list.clear()
        
        notes = self.project.world_notes if self.project else []
        
        for note in notes:
            if note.category == self.current_category:
                item = QListWidgetItem(note.title)
                item.setData(Qt.UserRole, note.id)
                self.notes_list.addItem(item)
                
        self.notes_list.blockSignals(False)

    def on_note_selected(self, current, previous):
        if not current:
            self.selected_note = None
            self.editor_group.setEnabled(False)
            return

        note_id = current.data(Qt.UserRole)
        self.selected_note = next((n for n in self.project.world_notes if n.id == note_id), None)
        
        if self.selected_note:
            self.editor_group.setEnabled(True)
            self.block_inputs_signals(True)
            
            self.title_input.setText(self.selected_note.title)
            self.category_combo.setCurrentText(self.selected_note.category)
            self.content_input.setPlainText(self.selected_note.content)
            
            self.block_inputs_signals(False)

    def block_inputs_signals(self, block):
        self.title_input.blockSignals(block)
        self.category_combo.blockSignals(block)
        self.content_input.blockSignals(block)

    def add_note(self):
        if not self.project:
            return
            
        new_note = WorldNote(title="Новая запись", category=self.current_category, content="")
        self.project.world_notes.append(new_note)
        
        self.rebuild_list()
        
        for i in range(self.notes_list.count()):
            item = self.notes_list.item(i)
            if item.data(Qt.UserRole) == new_note.id:
                self.notes_list.setCurrentItem(item)
                break
                
        self.title_input.setFocus()
        self.data_changed.emit()

    def delete_note(self):
        if not self.selected_note:
            return
        
        reply = QMessageBox.question(self, "Удалить запись?", 
                                     f"Вы действительно хотите удалить запись '{self.selected_note.title}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.project.world_notes.remove(self.selected_note)
            self.selected_note = None
            self.rebuild_list()
            self.editor_group.setEnabled(False)
            self.data_changed.emit()

    def save_note(self):
        if not self.selected_note:
            return
        
        old_category = self.selected_note.category
        self.selected_note.title = self.title_input.text()
        self.selected_note.category = self.category_combo.currentText()
        self.selected_note.content = self.content_input.toPlainText()
        
        current_item = self.notes_list.currentItem()
        if current_item:
            current_item.setText(self.selected_note.title)
            
        # Если категория сменилась, запись должна исчезнуть из текущего списка
        if old_category != self.selected_note.category:
            self.rebuild_list()
            self.editor_group.setEnabled(False)
            
        self.data_changed.emit()


# --- VIEW 8: BOOK READER (PREVIEW) ---
from PyQt5.QtWidgets import QTextBrowser

class BookReader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.font_size = 16
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Панель управления (вверху)
        controls_layout = QHBoxLayout()
        
        self.title_label = QLabel("<b>Режим чтения: Предпросмотр книги</b>")
        self.title_label.setStyleSheet("font-size: 14px; color: #0a84ff;")
        controls_layout.addWidget(self.title_label)
        controls_layout.addStretch()

        # Кнопки изменения размера шрифта
        self.zoom_out_btn = QPushButton("А-")
        self.zoom_out_btn.setToolTip("Уменьшить шрифт")
        self.zoom_out_btn.setFixedWidth(40)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        controls_layout.addWidget(self.zoom_out_btn)

        self.zoom_in_btn = QPushButton("А+")
        self.zoom_in_btn.setToolTip("Увеличить шрифт")
        self.zoom_in_btn.setFixedWidth(40)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        controls_layout.addWidget(self.zoom_in_btn)

        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.setToolTip("Обновить текст книги")
        self.refresh_btn.clicked.connect(self.update_content)
        controls_layout.addWidget(self.refresh_btn)

        layout.addLayout(controls_layout)

        # Сплиттер для оглавления и текста
        splitter = QSplitter(Qt.Horizontal)

        # Левая панель - Оглавление
        toc_group = QGroupBox("Содержание")
        toc_layout = QVBoxLayout(toc_group)
        self.toc_list = QListWidget()
        self.toc_list.currentItemChanged.connect(self.on_toc_item_selected)
        toc_layout.addWidget(self.toc_list)
        splitter.addWidget(toc_group)

        # Правая панель - Текст книги
        self.text_browser = QTextBrowser()
        self.text_browser.setObjectName("readerTextBrowser")
        self.text_browser.setOpenExternalLinks(False)
        self.text_browser.setStyleSheet("padding: 20px; border-radius: 8px;")
        splitter.addWidget(self.text_browser)

        splitter.setSizes([200, 600])
        layout.addWidget(splitter)

    def set_project(self, project):
        self.project = project
        if not project:
            self.setEnabled(False)
            self.text_browser.clear()
            self.toc_list.clear()
            return
        
        self.setEnabled(True)
        self.update_content()

    def update_content(self):
        if not self.project:
            return

        # Заполняем оглавление
        self.toc_list.blockSignals(True)
        self.toc_list.clear()
        
        # Обложка / Титульный лист
        cover_item = QListWidgetItem("📖 Титульный лист")
        cover_item.setData(Qt.UserRole, "cover")
        self.toc_list.addItem(cover_item)

        # Аннотация (если есть)
        if self.project.synopsis:
            syn_item = QListWidgetItem("📝 Аннотация")
            syn_item.setData(Qt.UserRole, "synopsis")
            self.toc_list.addItem(syn_item)

        # Главы
        for ch_idx, ch in enumerate(self.project.chapters):
            ch_item = QListWidgetItem(f"Глава {ch_idx + 1}: {ch.title}")
            ch_item.setData(Qt.UserRole, f"chapter_{ch_idx}")
            self.toc_list.addItem(ch_item)

        self.toc_list.blockSignals(False)

        # Генерируем HTML для всей книги
        html = self.generate_html()
        self.text_browser.setHtml(html)

    def generate_html(self):
        theme = "dark"
        try:
            from library_view import get_current_theme
            theme = get_current_theme()
        except Exception:
            pass

        # Цвета в зависимости от темы
        if theme == "dark":
            bg_color = "#121218"
            text_color = "#f5f5f7"
            muted_color = "#8e8e93"
            border_color = "#2c2c2e"
        else:
            bg_color = "#fdfdfd"
            text_color = "#1d1d1f"
            muted_color = "#6e6e73"
            border_color = "#d2d2d7"

        # CSS-стили для премиального книжного оформления (Times New Roman / Georgia)
        css = f"""
        <style>
            body {{
                font-family: 'Georgia', 'Times New Roman', serif;
                font-size: {self.font_size}px;
                line-height: 1.7;
                color: {text_color};
                background-color: {bg_color};
                margin: 0 auto;
                padding: 30px;
                max-width: 650px;
            }}
            .cover-page {{
                margin-top: 15%;
                margin-bottom: 25%;
                text-align: center;
            }}
            .cover-title {{
                font-size: 2.2em;
                font-weight: bold;
                margin-bottom: 15px;
                color: {text_color};
            }}
            .cover-author {{
                font-size: 1.4em;
                font-style: italic;
                color: {muted_color};
                margin-bottom: 50px;
            }}
            .synopsis-page {{
                margin-top: 50px;
                margin-bottom: 100px;
                border-top: 1px solid {border_color};
                padding-top: 25px;
            }}
            .synopsis-title {{
                font-size: 1.6em;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }}
            .synopsis-text {{
                text-align: justify;
                font-style: italic;
            }}
            .chapter-page {{
                margin-top: 80px;
                margin-bottom: 50px;
                border-top: 1px dashed {border_color};
                padding-top: 40px;
            }}
            .chapter-title {{
                font-size: 1.8em;
                font-weight: bold;
                text-align: center;
                margin-bottom: 30px;
            }}
            .scene-title {{
                font-size: 1.2em;
                font-weight: bold;
                margin-top: 30px;
                margin-bottom: 15px;
                color: #0a84ff;
            }}
            p {{
                text-indent: 1.5em;
                margin-top: 0;
                margin-bottom: 12px;
                text-align: justify;
            }}
        </style>
        """

        html_body = []
        
        # 1. Титульный лист
        html_body.append(f'<div class="cover-page" id="cover">')
        html_body.append(f'  <div class="cover-title">{self.project.title}</div>')
        if self.project.author:
            html_body.append(f'  <div class="cover-author">{self.project.author}</div>')
        html_body.append(f'</div>')

        # 2. Аннотация
        if self.project.synopsis:
            html_body.append(f'<div class="synopsis-page" id="synopsis">')
            html_body.append(f'  <div class="synopsis-title">Аннотация</div>')
            html_body.append(f'  <div class="synopsis-text">')
            for line in self.project.synopsis.split('\n'):
                l = line.strip()
                if l:
                    html_body.append(f'    <p>{l}</p>')
            html_body.append(f'  </div>')
            html_body.append(f'</div>')

        # 3. Главы и сцены
        for ch_idx, ch in enumerate(self.project.chapters):
            html_body.append(f'<div class="chapter-page" id="chapter_{ch_idx}">')
            html_body.append(f'  <div class="chapter-title">Глава {ch_idx + 1}: {ch.title}</div>')
            for sc in ch.scenes:
                if sc.title and not sc.title.startswith("Сцена"):
                    html_body.append(f'  <div class="scene-title">{sc.title}</div>')
                for p in sc.content.split('\n'):
                    p_s = p.strip()
                    if p_s:
                        html_body.append(f'  <p>{p_s}</p>')
            html_body.append(f'</div>')

        return f"<html><head>{css}</head><body>" + "\n".join(html_body) + "</body></html>"

    def on_toc_item_selected(self, current, previous):
        if not current:
            return
        anchor = current.data(Qt.UserRole)
        if anchor:
            self.text_browser.scrollToAnchor(anchor)

    def zoom_in(self):
        if self.font_size < 32:
            self.font_size += 2
            self.update_content()

    def zoom_out(self):
        if self.font_size > 10:
            self.font_size -= 2
            self.update_content()
