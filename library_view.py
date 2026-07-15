import os
import json
import base64
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QScrollArea, QPushButton, QLabel, QLineEdit, 
                             QMenu, QAction, QDialog, QFormLayout, QMessageBox, 
                             QFileDialog, QFrame, QStyleOption, QStyle)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QLinearGradient, QFont, QCursor

try:
    from .models import Project
except ImportError:
    from models import Project

LIBRARY_DIR = os.path.expanduser("~/.nwrite")
LIBRARY_FILE = os.path.join(LIBRARY_DIR, "library.json")
COVERS_DIR = os.path.join(LIBRARY_DIR, "covers")

def ensure_library_dirs():
    if not os.path.exists(LIBRARY_DIR):
        os.makedirs(LIBRARY_DIR)
    if not os.path.exists(COVERS_DIR):
        os.makedirs(COVERS_DIR)

def load_library_data():
    ensure_library_dirs()
    if not os.path.exists(LIBRARY_FILE):
        return {"books": [], "theme": "dark"}
    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return {"books": data, "theme": "dark"}
            if isinstance(data, dict):
                if "books" not in data:
                    data["books"] = []
                if "theme" not in data:
                    data["theme"] = "dark"
                return data
    except Exception:
        return {"books": [], "theme": "dark"}
    return {"books": [], "theme": "dark"}

def load_library():
    return load_library_data()["books"]

def save_library(library_data):
    data = load_library_data()
    data["books"] = library_data
    ensure_library_dirs()
    try:
        with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving library: {e}")

def get_current_theme():
    return load_library_data().get("theme", "dark")

def set_current_theme(theme_name):
    data = load_library_data()
    data["theme"] = theme_name
    ensure_library_dirs()
    try:
        with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving theme: {e}")

def cache_project_cover(project_id, cover_base64_str):
    ensure_library_dirs()
    cache_path = os.path.join(COVERS_DIR, f"{project_id}.jpg")
    if not cover_base64_str:
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
            except Exception:
                pass
        return None
        
    try:
        if "," in cover_base64_str:
            cover_base64_str = cover_base64_str.split(",")[1]
        img_data = base64.b64decode(cover_base64_str)
        with open(cache_path, "wb") as f:
            f.write(img_data)
        return cache_path
    except Exception as e:
        print(f"Error caching cover: {e}")
        return None

def get_cached_cover_path(project_id):
    cache_path = os.path.join(COVERS_DIR, f"{project_id}.jpg")
    if os.path.exists(cache_path):
        return cache_path
    return None

def resize_and_convert_to_base64(file_path):
    try:
        image = QImage(file_path)
        if image.isNull():
            return ""
        resized = image.scaled(300, 400, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        if resized.width() > 300 or resized.height() > 400:
            x = (resized.width() - 300) // 2
            y = (resized.height() - 400) // 2
            resized = resized.copy(x, y, 300, 400)
            
        ba = QByteArray()
        buffer = QBuffer(ba)
        buffer.open(QIODevice.WriteOnly)
        resized.save(buffer, "JPG", 80)
        return base64.b64encode(ba.data()).decode('utf-8')
    except Exception as e:
        print(f"Error resizing cover: {e}")
        return ""

def generate_procedural_cover(title, author, width=160, height=210):
    pixmap = QPixmap(width, height)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)
    
    gradient = QLinearGradient(0, 0, width, height)
    val = sum(ord(c) for c in title) if title else 0
    gradient_index = val % 4
    
    # Спокойные тона в стиле Apple
    if gradient_index == 0:
        gradient.setColorAt(0, QColor("#007aff")) # Apple Blue
        gradient.setColorAt(1, QColor("#5a7fa4"))
    elif gradient_index == 1:
        gradient.setColorAt(0, QColor("#3a3a3c")) # Graphite
        gradient.setColorAt(1, QColor("#1c1c1e"))
    elif gradient_index == 2:
        gradient.setColorAt(0, QColor("#2f80ed")) # Calm Blue
        gradient.setColorAt(1, QColor("#56ccf2"))
    else:
        gradient.setColorAt(0, QColor("#434343")) # Silver/Coal
        gradient.setColorAt(1, QColor("#000000"))
        
    painter.fillRect(0, 0, width, height, gradient)
    
    painter.setPen(QColor(255, 255, 255, 30))
    painter.drawRect(0, 0, width - 1, height - 1)
    
    # Используем шрифты Apple/системные
    font_title = QFont("Georgia", 11, QFont.Bold)
    painter.setFont(font_title)
    painter.setPen(QColor("#ffffff"))
    painter.drawText(10, 30, width - 20, height - 80, Qt.AlignCenter | Qt.TextWordWrap, title)
    
    painter.setPen(QColor(255, 255, 255, 60))
    painter.drawLine(width // 4, height - 45, (3 * width) // 4, height - 45)
    
    # Замена Segoe UI на системный стек Apple через QFont
    font_author = QFont()
    font_author.setFamily("-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif")
    font_author.setPointSize(8)
    painter.setFont(font_author)
    painter.setPen(QColor("#f5f5f7"))
    painter.drawText(10, height - 35, width - 20, 25, Qt.AlignCenter | Qt.TextWordWrap, author if author else "Nwrite")
    
    painter.end()
    return pixmap


class BookCardWidget(QFrame):
    clicked = pyqtSignal(str)
    menu_triggered = pyqtSignal(str, str)
    
    def __init__(self, book_data, parent=None):
        super().__init__(parent)
        self.book_data = book_data
        self.setObjectName("bookCard")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedWidth(180)
        self.setFixedHeight(280)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)
        
        self.cover_label = QLabel()
        self.cover_label.setFixedSize(160, 210)
        self.cover_label.setObjectName("coverLabel")
        self.cover_label.setAlignment(Qt.AlignCenter)
        
        project_id = self.book_data["id"]
        title = self.book_data["title"]
        author = self.book_data.get("author", "")
        genre = self.book_data.get("genre", "")
        
        cover_path = get_cached_cover_path(project_id)
        if cover_path:
            pixmap = QPixmap(cover_path)
            if not pixmap.isNull():
                self.cover_label.setPixmap(pixmap.scaled(160, 210, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            else:
                self.cover_label.setPixmap(generate_procedural_cover(title, author))
        else:
            self.cover_label.setPixmap(generate_procedural_cover(title, author))
            
        layout.addWidget(self.cover_label)
        
        meta_layout = QHBoxLayout()
        meta_layout.setContentsMargins(0, 0, 0, 0)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")
        
        metrics = self.title_label.fontMetrics()
        elided = metrics.elidedText(title, Qt.ElideRight, 125)
        self.title_label.setText(elided)
        text_layout.addWidget(self.title_label)
        
        author_text = f"{author} | {genre}" if author and genre else (author or genre or "Новелла")
        self.sub_label = QLabel(author_text)
        self.sub_label.setObjectName("cardSubtitle")
        elided_sub = metrics.elidedText(author_text, Qt.ElideRight, 125)
        self.sub_label.setText(elided_sub)
        text_layout.addWidget(self.sub_label)
        
        meta_layout.addLayout(text_layout)
        
        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setFixedSize(22, 22)
        self.menu_btn.setObjectName("cardMenuBtn")
        self.menu_btn.clicked.connect(self.show_context_menu)
        meta_layout.addWidget(self.menu_btn)
        
        layout.addLayout(meta_layout)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.childAt(event.pos()) == self.menu_btn:
                return
            self.clicked.emit(self.book_data["file_path"])
            
    def show_context_menu(self):
        menu = QMenu(self)
        
        open_action = QAction("Открыть новеллу", self)
        open_action.triggered.connect(lambda: self.menu_triggered.emit("open", self.book_data["id"]))
        
        cover_action = QAction("Изменить обложку...", self)
        cover_action.triggered.connect(lambda: self.menu_triggered.emit("change_cover", self.book_data["id"]))
        
        rename_action = QAction("Переименовать...", self)
        rename_action.triggered.connect(lambda: self.menu_triggered.emit("rename", self.book_data["id"]))
        
        export_action = QAction("Экспорт...", self)
        export_action.triggered.connect(lambda: self.menu_triggered.emit("export", self.book_data["id"]))
        
        delete_action = QAction("Удалить...", self)
        delete_action.triggered.connect(lambda: self.menu_triggered.emit("delete", self.book_data["id"]))
        
        menu.addAction(open_action)
        menu.addAction(cover_action)
        menu.addAction(rename_action)
        menu.addAction(export_action)
        menu.addSeparator()
        menu.addAction(delete_action)
        
        menu.exec_(QCursor.pos())


class LibraryWidget(QWidget):
    project_selected = pyqtSignal(str)
    theme_toggled = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.books = []
        self.init_ui()
        self.refresh_library()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        self.header_title = QLabel("✍️ Nwrite")
        self.header_title.setObjectName("libraryHeaderTitle")
        header_layout.addWidget(self.header_title)
        
        header_layout.addStretch()
        
        self.btn_theme = QPushButton()
        self.btn_theme.setObjectName("themeToggleButton")
        self.update_theme_button_text()
        self.btn_theme.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.btn_theme)
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchBar")
        self.search_input.setPlaceholderText("Поиск новелл...")
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(self.filter_books)
        header_layout.addWidget(self.search_input)
        
        self.btn_new = QPushButton("Создать новеллу")
        self.btn_new.setObjectName("primaryButton")
        self.btn_new.clicked.connect(self.create_new_book)
        header_layout.addWidget(self.btn_new)
        
        self.btn_import = QPushButton("Добавить книгу...")
        self.btn_import.clicked.connect(self.import_book)
        header_layout.addWidget(self.btn_import)
        
        main_layout.addLayout(header_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.scroll_area.setWidget(self.grid_container)
        main_layout.addWidget(self.scroll_area)

    def update_theme_button_text(self):
        theme = get_current_theme()
        if theme == "dark":
            self.btn_theme.setText("☀️ Светлая")
        else:
            self.btn_theme.setText("🌙 Темная")

    def toggle_theme(self):
        theme = get_current_theme()
        new_theme = "light" if theme == "dark" else "dark"
        set_current_theme(new_theme)
        self.update_theme_button_text()
        self.theme_toggled.emit(new_theme)
        self.refresh_library()
        
    def refresh_library(self):
        self.books = load_library()
        
        existing_books = []
        changed = False
        for book in self.books:
            if os.path.exists(book["file_path"]):
                project_id = book["id"]
                if not get_cached_cover_path(project_id):
                    try:
                        proj = Project.load(book["file_path"])
                        if proj.cover_image:
                            cache_project_cover(project_id, proj.cover_image)
                    except Exception:
                        pass
                existing_books.append(book)
            else:
                changed = True
                
        if changed:
            self.books = existing_books
            save_library(self.books)
            
        self.books.sort(key=lambda x: x.get("last_modified", ""), reverse=True)
        self.render_grid()
        
    def render_grid(self, filter_text=""):
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
                
        filtered_books = []
        for book in self.books:
            if filter_text.lower() in book["title"].lower() or filter_text.lower() in book.get("author", "").lower():
                filtered_books.append(book)
                
        if not filtered_books:
            empty_lbl = QLabel("В библиотеке пока нет созданных новелл. Нажмите кнопку выше, чтобы начать!" if not filter_text else "Книги не найдены.")
            empty_lbl.setObjectName("emptyLibraryLabel")
            empty_lbl.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(empty_lbl, 0, 0, 1, 4, Qt.AlignCenter)
            return
            
        width = self.scroll_area.width()
        card_width = 180 + 20
        columns = max(1, width // card_width)
        
        for idx, book in enumerate(filtered_books):
            row = idx // columns
            col = idx % columns
            card = BookCardWidget(book, self)
            card.clicked.connect(self.project_selected.emit)
            card.menu_triggered.connect(self.handle_card_menu)
            self.grid_layout.addWidget(card, row, col)
            
    def filter_books(self, text):
        self.render_grid(text)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.scroll_area.width()
        card_width = 180 + 20
        columns = max(1, width // card_width)
        
        widgets = []
        for i in range(self.grid_layout.count()):
            w = self.grid_layout.itemAt(i).widget()
            if w:
                widgets.append(w)
                
        for w in widgets:
            self.grid_layout.removeWidget(w)
            
        for idx, w in enumerate(widgets):
            row = idx // columns
            col = idx % columns
            self.grid_layout.addWidget(w, row, col)
            
    def create_new_book(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Новая новелла")
        dialog.setFixedSize(400, 320)
        
        layout = QFormLayout(dialog)
        layout.setSpacing(12)
        
        title_input = QLineEdit("Моя Новелла")
        author_input = QLineEdit(os.getlogin() if hasattr(os, "getlogin") else "")
        genre_input = QLineEdit()
        
        cover_path_label = QLabel("Обложка не выбрана (будет создана стандартная)")
        cover_path_label.setWordWrap(True)
        cover_path_label.setObjectName("coverPathLabel")
        
        selected_cover_path = [None]
        
        def choose_cover():
            file_path, _ = QFileDialog.getOpenFileName(dialog, "Выбрать обложку", "", "Изображения (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                selected_cover_path[0] = file_path
                cover_path_label.setText(os.path.basename(file_path))
                
        btn_cover = QPushButton("Выбрать обложку...")
        btn_cover.clicked.connect(choose_cover)
        
        layout.addRow("Название новеллы:", title_input)
        layout.addRow("Автор:", author_input)
        layout.addRow("Жанр:", genre_input)
        layout.addRow("Обложка:", btn_cover)
        layout.addRow("", cover_path_label)
        
        btn_box = QHBoxLayout()
        ok_btn = QPushButton("Далее")
        ok_btn.setObjectName("primaryButton")
        cancel_btn = QPushButton("Отмена")
        btn_box.addWidget(ok_btn)
        btn_box.addWidget(cancel_btn)
        layout.addRow("", btn_box)
        
        cancel_btn.clicked.connect(dialog.reject)
        
        def on_ok():
            if not title_input.text().strip():
                QMessageBox.warning(dialog, "Внимание", "Название проекта не может быть пустым.")
                return
            dialog.accept()
            
        ok_btn.clicked.connect(on_ok)
        
        if dialog.exec_() == QDialog.Accepted:
            title = title_input.text().strip()
            author = author_input.text().strip()
            genre = genre_input.text().strip()
            
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить проект", f"{title}.nwrite", "Nwrite Projects (*.nwrite);;JSON Files (*.json)")
            if file_path:
                try:
                    proj = Project(title=title, file_path=file_path)
                    proj.author = author
                    proj.genre = genre
                    
                    if selected_cover_path[0]:
                        base64_cover = resize_and_convert_to_base64(selected_cover_path[0])
                        proj.cover_image = base64_cover
                        
                    proj.save()
                    
                    if proj.cover_image:
                        cache_project_cover(proj.id, proj.cover_image)
                        
                    self.register_project_in_library(proj)
                    self.refresh_library()
                    self.project_selected.emit(proj.file_path)
                    
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось создать проект:\n{str(e)}")

    def register_project_in_library(self, project):
        library_data = load_library()
        existing = next((b for b in library_data if b["id"] == project.id or b["file_path"] == project.file_path), None)
        if existing:
            library_data.remove(existing)
            
        library_data.append({
            "id": project.id,
            "title": project.title,
            "author": project.author,
            "genre": project.genre,
            "file_path": project.file_path,
            "last_modified": project.last_modified
        })
        save_library(library_data)

    def import_book(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Добавить книгу в Nwrite", "", "Nwrite Projects (*.nwrite);;JSON Files (*.json)")
        if file_path:
            try:
                proj = Project.load(file_path)
                if proj.cover_image:
                    cache_project_cover(proj.id, proj.cover_image)
                self.register_project_in_library(proj)
                self.refresh_library()
                QMessageBox.information(self, "Успех", f"Книга '{proj.title}' добавлена в библиотеку!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")

    def handle_card_menu(self, action, project_id):
        book = next((b for b in self.books if b["id"] == project_id), None)
        if not book:
            return
            
        if action == "open":
            self.project_selected.emit(book["file_path"])
            
        elif action == "change_cover":
            file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать обложку", "", "Изображения (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                try:
                    proj = Project.load(book["file_path"])
                    base64_cover = resize_and_convert_to_base64(file_path)
                    proj.cover_image = base64_cover
                    proj.save()
                    
                    cache_project_cover(project_id, base64_cover)
                    self.refresh_library()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить обложку:\n{str(e)}")
                    
        elif action == "rename":
            new_title, ok = QLineEdit.getText(self, "Переименовать", "Введите новое название новеллы:", text=book["title"])
            if ok and new_title.strip():
                try:
                    proj = Project.load(book["file_path"])
                    proj.title = new_title.strip()
                    proj.save()
                    
                    library_data = load_library()
                    for b in library_data:
                        if b["id"] == project_id:
                            b["title"] = proj.title
                            b["last_modified"] = proj.last_modified
                    save_library(library_data)
                    self.refresh_library()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось переименовать книгу:\n{str(e)}")
                    
        elif action == "export":
            save_path, _ = QFileDialog.getSaveFileName(self, "Экспортировать новеллу", f"{book['title']}.nwrite", "Nwrite Projects (*.nwrite);;JSON Files (*.json)")
            if save_path:
                try:
                    import shutil
                    shutil.copy(book["file_path"], save_path)
                    QMessageBox.information(self, "Экспорт", "Книга успешно экспортирована!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать:\n{str(e)}")
                    
        elif action == "delete":
            delete_dialog = QDialog(self)
            delete_dialog.setWindowTitle("Удалить новеллу?")
            delete_dialog.setFixedSize(380, 160)
            
            lbl = QLabel(f"Вы действительно хотите удалить '{book['title']}' из библиотеки?")
            lbl.setWordWrap(True)
            lbl.setObjectName("deleteDialogLabel")
            
            layout = QVBoxLayout(delete_dialog)
            layout.addWidget(lbl)
            
            btn_remove_index = QPushButton("Убрать только из списка")
            btn_remove_file = QPushButton("Удалить файл проекта с диска")
            btn_remove_file.setObjectName("dangerButton")
            btn_cancel = QPushButton("Отмена")
            
            layout.addWidget(btn_remove_index)
            layout.addWidget(btn_remove_file)
            layout.addWidget(btn_cancel)
            
            result = [None]
            
            btn_remove_index.clicked.connect(lambda: [result.__setitem__(0, "remove_index"), delete_dialog.accept()])
            btn_remove_file.clicked.connect(lambda: [result.__setitem__(0, "remove_file"), delete_dialog.accept()])
            btn_cancel.clicked.connect(delete_dialog.reject)
            
            if delete_dialog.exec_() == QDialog.Accepted:
                if result[0] == "remove_index":
                    library_data = load_library()
                    library_data = [b for b in library_data if b["id"] != project_id]
                    save_library(library_data)
                    cache_project_cover(project_id, "")
                    self.refresh_library()
                    
                elif result[0] == "remove_file":
                    try:
                        if os.path.exists(book["file_path"]):
                            os.remove(book["file_path"])
                        library_data = load_library()
                        library_data = [b for b in library_data if b["id"] != project_id]
                        save_library(library_data)
                        cache_project_cover(project_id, "")
                        self.refresh_library()
                        QMessageBox.information(self, "Удаление", "Книга и файл проекта успешно удалены.")
                    except Exception as e:
                        QMessageBox.critical(self, "Ошибка", f"Не удалось удалить файл:\n{str(e)}")
