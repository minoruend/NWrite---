import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QHBoxLayout, QWidget, QFileDialog, QMessageBox, 
                             QAction, QMenuBar, QStatusBar, QDialog, QLabel, 
                             QPushButton, QLineEdit, QSplitter, QStackedWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

try:
    from .models import Project
    from .styles import DARK_THEME_STYLE, LIGHT_THEME_STYLE
    from .views import (ProjectDashboard, CharacterManager, LocationManager, 
                        OutlineManager, NovelEditor, RelationshipManager, WorldManager, BookReader)
    from .library_view import LibraryWidget, get_current_theme
except ImportError:
    from models import Project
    from styles import DARK_THEME_STYLE, LIGHT_THEME_STYLE
    from views import (ProjectDashboard, CharacterManager, LocationManager, 
                       OutlineManager, NovelEditor, RelationshipManager, WorldManager, BookReader)
    from library_view import LibraryWidget, get_current_theme

def get_icon_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "icon.png")
    return os.path.join(os.path.dirname(__file__), "icon.png")

class NwriteMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project = None
        self.needs_save = False
        
        self.setWindowTitle("Nwrite — Планировщик новелл")
        self.resize(1100, 750)
        
        # Установка иконки
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # QStackedWidget для переключения между библиотекой и редактором
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Виджет библиотеки
        self.library_widget = LibraryWidget(self)
        self.library_widget.project_selected.connect(self.open_project_from_path)
        self.library_widget.theme_toggled.connect(self.apply_theme)
        self.stacked_widget.addWidget(self.library_widget)
        
        # Инициализируем UI редактора
        self.init_menu()
        self.init_tabs()
        
        self.stacked_widget.addWidget(self.tabs)
        self.stacked_widget.setCurrentIndex(0) # Начинаем с библиотеки
        
        # Таймер для автосохранения (каждые 5 секунд)
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.auto_save)
        self.autosave_timer.start(5000)

        # Строка состояния
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")

    def init_menu(self):
        menu_bar = self.menuBar()
        
        # Меню Файл
        file_menu = menu_bar.addMenu("&Файл")
        
        new_action = QAction("&Новый проект", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Открыть проект...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project_dialog)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.manual_save)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Сохранить &как...", self)
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        close_action = QAction("&Закрыть роман (к библиотеке)", self)
        close_action.setShortcut("Ctrl+W")
        close_action.triggered.connect(self.close_project)
        file_menu.addAction(close_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Выход", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def init_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        
        # Кнопка возврата к библиотеке в углу вкладок
        back_btn = QPushButton("🚪 К списку книг")
        back_btn.setObjectName("backToLibraryButton")
        back_btn.clicked.connect(self.close_project)
        self.tabs.setCornerWidget(back_btn, Qt.TopRightCorner)
        
        # Создаем страницы
        self.dashboard_tab = ProjectDashboard()
        self.dashboard_tab.project_updated.connect(self.mark_dirty)
        
        self.characters_tab = CharacterManager()
        self.characters_tab.data_changed.connect(self.mark_dirty)

        self.locations_tab = LocationManager()
        self.locations_tab.data_changed.connect(self.mark_dirty)

        self.world_tab = WorldManager()
        self.world_tab.data_changed.connect(self.mark_dirty)

        self.outline_tab = OutlineManager()
        self.outline_tab.data_changed.connect(self.mark_dirty)
        self.outline_tab.open_in_editor_requested.connect(self.on_open_scene_in_editor)

        self.editor_tab = NovelEditor()
        self.editor_tab.scene_text_changed.connect(self.mark_dirty)

        self.reader_tab = BookReader()

        self.relationships_tab = RelationshipManager()
        self.relationships_tab.data_changed.connect(self.mark_dirty)
        
        # Добавляем в QTabWidget без эмодзи для минималистичного Apple-стиля
        self.tabs.addTab(self.dashboard_tab, "Инфо")
        self.tabs.addTab(self.characters_tab, "Персонажи")
        self.tabs.addTab(self.locations_tab, "Локации")
        self.tabs.addTab(self.world_tab, "Мир")
        self.tabs.addTab(self.outline_tab, "Структура")
        self.tabs.addTab(self.editor_tab, "Редактор")
        self.tabs.addTab(self.reader_tab, "Чтение")
        self.tabs.addTab(self.relationships_tab, "Связи")
        
        # Слушаем переключение вкладок для обновления статистики дашборда или синхронизации данных
        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        if index == 0: # Dashboard
            self.dashboard_tab.update_stats()
        elif index == 1: # Characters list
            self.characters_tab.set_project(self.project)
        elif index == 2: # Locations
            self.locations_tab.set_project(self.project)
        elif index == 3: # World building
            self.world_tab.set_project(self.project)
        elif index == 4: # Outline
            self.outline_tab.set_project(self.project)
        elif index == 6: # Book Reader
            self.reader_tab.set_project(self.project)
        elif index == 7: # Relationships
            self.relationships_tab.set_project(self.project)

    def on_open_scene_in_editor(self, chapter, scene):
        # Передаем сцену редактору
        self.editor_tab.open_scene(chapter, scene)
        # Переключаем вкладку на Редактор (индекс 5)
        self.tabs.setCurrentIndex(5)

    def open_project_from_path(self, path):
        if self.check_unsaved_changes() == QMessageBox.Cancel:
            return
        try:
            loaded_proj = Project.load(path)
            self.set_project(loaded_proj)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть проект:\n{str(e)}")

    def close_project(self):
        if self.project:
            if self.check_unsaved_changes() == QMessageBox.Cancel:
                return
            self.auto_save()
            self.project = None
            self.needs_save = False
            self.update_window_title()
            self.library_widget.refresh_library()
            self.stacked_widget.setCurrentIndex(0)

    def set_project(self, project):
        self.project = project
        self.needs_save = False
        
        # Обновляем заголовок окна
        self.update_window_title()

        # Раздаем проект по всем вкладкам
        self.dashboard_tab.set_project(project)
        self.characters_tab.set_project(project)
        self.locations_tab.set_project(project)
        self.world_tab.set_project(project)
        self.outline_tab.set_project(project)
        self.editor_tab.set_project(project)
        self.reader_tab.set_project(project)
        self.relationships_tab.set_project(project)
        
        self.status_bar.showMessage(f"Проект '{project.title}' успешно загружен.", 3000)
        self.stacked_widget.setCurrentIndex(1) # Переключаемся на редактор

    def update_window_title(self):
        star = " *" if self.needs_save else ""
        if self.project:
            self.setWindowTitle(f"Nwrite — {self.project.title}{star} [{self.project.file_path}]")
        else:
            self.setWindowTitle("Nwrite — Планировщик новелл")

    def mark_dirty(self):
        if not self.needs_save:
            self.needs_save = True
            self.update_window_title()

    def auto_save(self):
        if self.project and self.needs_save:
            try:
                self.project.save()
                self.needs_save = False
                self.update_window_title()
                self.status_bar.showMessage("Проект автосохранен", 2000)
            except Exception as e:
                self.status_bar.showMessage(f"Ошибка автосохранения: {str(e)}", 4000)

    def manual_save(self):
        if not self.project:
            return
        try:
            self.project.save()
            self.needs_save = False
            self.update_window_title()
            self.status_bar.showMessage("Проект успешно сохранен!", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить проект:\n{str(e)}")

    def save_project_as(self):
        if not self.project:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить проект как", self.project.file_path, "Nwrite Projects (*.nwrite);;JSON Files (*.json)")
        if file_path:
            try:
                self.project.file_path = file_path
                self.project.save()
                self.needs_save = False
                self.update_window_title()
                self.status_bar.showMessage("Проект сохранен под новым именем", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить проект:\n{str(e)}")

    def new_project(self):
        if self.check_unsaved_changes() == QMessageBox.Cancel:
            return
            
        title_dialog = QDialog(self)
        title_dialog.setWindowTitle("Новый проект")
        t_layout = QVBoxLayout(title_dialog)
        t_layout.addWidget(QLabel("Введите название нового романа:"))
        title_input = QLineEdit("Новый Роман")
        t_layout.addWidget(title_input)
        
        btn_box = QHBoxLayout()
        ok_btn = QPushButton("Создать")
        ok_btn.setObjectName("primaryButton")
        cancel_btn = QPushButton("Отмена")
        btn_box.addWidget(ok_btn)
        btn_box.addWidget(cancel_btn)
        t_layout.addLayout(btn_box)
        
        cancel_btn.clicked.connect(title_dialog.reject)
        
        def on_ok():
            title = title_input.text().strip()
            if not title:
                return
            title_dialog.accept()
            
        ok_btn.clicked.connect(on_ok)
        
        if title_dialog.exec_() == QDialog.Accepted:
            title = title_input.text().strip()
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить проект", f"{title}.nwrite", "Nwrite Projects (*.nwrite);;JSON Files (*.json)")
            if file_path:
                try:
                    new_proj = Project(title=title, file_path=file_path)
                    new_proj.save()
                    self.set_project(new_proj)
                    # Register in library
                    self.library_widget.register_project_in_library(new_proj)
                    self.library_widget.refresh_library()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось создать проект:\n{str(e)}")

    def open_project_dialog(self):
        if self.check_unsaved_changes() == QMessageBox.Cancel:
            return
            
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть проект", "", "Nwrite Projects (*.nwrite);;JSON Files (*.json)")
        if file_path:
            try:
                loaded_proj = Project.load(file_path)
                self.set_project(loaded_proj)
                # Register in library
                self.library_widget.register_project_in_library(loaded_proj)
                self.library_widget.refresh_library()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть проект:\n{str(e)}")

    def check_unsaved_changes(self):
        if self.project and self.needs_save:
            reply = QMessageBox.question(self, "Несохраненные изменения", 
                                          "В проекте есть несохраненные изменения. Сохранить их перед переходом?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.manual_save()
                return QMessageBox.Yes
            return reply
        return QMessageBox.Yes

    def apply_theme(self, theme_name):
        app = QApplication.instance()
        if app:
            if theme_name == "dark":
                app.setStyleSheet(DARK_THEME_STYLE)
            else:
                app.setStyleSheet(LIGHT_THEME_STYLE)

    def closeEvent(self, event):
        reply = self.check_unsaved_changes()
        if reply == QMessageBox.Cancel:
            event.ignore()
        else:
            self.autosave_timer.stop()
            event.accept()


def main():
    app = QApplication(sys.argv)
    
    # Применяем сохраненную тему (светлую или темную)
    theme = get_current_theme()
    if theme == "dark":
        app.setStyleSheet(DARK_THEME_STYLE)
    else:
        app.setStyleSheet(LIGHT_THEME_STYLE)
    
    main_window = NwriteMainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
