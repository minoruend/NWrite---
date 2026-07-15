# -*- coding: utf-8 -*-

# Общий шрифт Apple для обеих тем
FONT_FAMILY_STACK = '-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "SF Pro", "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif'

DARK_THEME_STYLE = f"""
/* Общие стили */
QWidget {{
    background-color: #1e1e1e;
    color: #f5f5f7;
    font-family: {FONT_FAMILY_STACK};
    font-size: 14px;
    selection-background-color: #0a84ff;
    selection-color: #ffffff;
}}

/* Главные окна и диалоги */
QMainWindow, QDialog {{
    background-color: #1e1e1e;
}}

/* Метки */
QLabel {{
    background-color: transparent;
    color: #f5f5f7;
}}

QLabel#titleLabel {{
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    padding-bottom: 5px;
}}

QLabel#subtitleLabel {{
    font-size: 12px;
    color: #8e8e93;
}}

/* Поля ввода (QLineEdit, QTextEdit и др.) */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
    background-color: #161616;
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    padding: 6px 10px;
    color: #ffffff;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {{
    border: 1px solid #0a84ff;
    background-color: #1d1d1f;
}}

QLineEdit#searchBar {{
    background-color: #161616;
    border: 1px solid #2c2c2e;
    border-radius: 14px;
    padding: 5px 12px;
    color: #ffffff;
    min-height: 16px;
}}

QLineEdit#searchBar:focus {{
    border: 1px solid #0a84ff;
    background-color: #1d1d1f;
}}

/* Кнопки */
QPushButton {{
    background-color: #2c2c2e;
    border: 1px solid #3a3a3c;
    color: #f5f5f7;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 500;
    min-height: 18px;
}}

QPushButton:hover {{
    background-color: #3a3a3c;
    border-color: #48484a;
}}

QPushButton:pressed {{
    background-color: #1c1c1e;
}}

QPushButton:disabled {{
    background-color: #161616;
    border-color: #2c2c2e;
    color: #48484a;
}}

/* Акцентная/Основная кнопка */
QPushButton#primaryButton {{
    background-color: #0a84ff;
    border: none;
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#primaryButton:hover {{
    background-color: #2693ff;
}}

QPushButton#primaryButton:pressed {{
    background-color: #0062c3;
}}

/* Кнопка удаления / Опасного действия */
QPushButton#dangerButton {{
    background-color: #ff453a;
    border: none;
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#dangerButton:hover {{
    background-color: #ff6961;
}}

QPushButton#dangerButton:pressed {{
    background-color: #d63025;
}}

/* Кнопка возврата к библиотеке */
QPushButton#backToLibraryButton {{
    background-color: transparent;
    border: 1px solid #3a3a3c;
    border-radius: 6px;
    padding: 4px 10px;
    font-weight: 600;
    color: #f5f5f7;
}}

QPushButton#backToLibraryButton:hover {{
    background-color: #2c2c2e;
    border-color: #48484a;
}}

/* Кнопка переключения тем */
QPushButton#themeToggleButton {{
    background-color: transparent;
    border: 1px solid #3a3a3c;
    border-radius: 13px;
    padding: 4px 10px;
    font-weight: 500;
    color: #f5f5f7;
    min-height: 16px;
}}

QPushButton#themeToggleButton:hover {{
    background-color: #2c2c2e;
}}

/* Списки и Деревья */
QListWidget, QTreeWidget {{
    background-color: #161616;
    border: 1px solid #2c2c2e;
    border-radius: 8px;
    padding: 5px;
    outline: 0;
}}

QListWidget::item, QTreeWidget::item {{
    border-radius: 6px;
    padding: 6px 10px;
    margin: 2px 0px;
    color: #d2d2d7;
    background-color: transparent;
}}

QListWidget::item:hover, QTreeWidget::item:hover {{
    background-color: #2c2c2e;
    color: #ffffff;
}}

QListWidget::item:selected, QTreeWidget::item:selected {{
    background-color: #0a84ff;
    color: #ffffff;
    font-weight: 600;
}}

/* Таблицы */
QTableWidget {{
    background-color: #161616;
    border: 1px solid #2c2c2e;
    border-radius: 8px;
    gridline-color: #2c2c2e;
}}

QHeaderView::section {{
    background-color: #2c2c2e;
    color: #f5f5f7;
    padding: 6px;
    border: 1px solid #1e1e1e;
    font-weight: 600;
}}

/* Вкладки (QTabWidget и QTabBar в стиле Apple Segmented Control) */
QTabWidget::pane {{
    border: 1px solid #2c2c2e;
    border-radius: 8px;
    background-color: #161616;
    top: -1px;
}}

QTabBar {{
    background-color: #161616;
    border-radius: 8px;
    qproperty-drawBase: 0;
    padding: 3px;
    margin-bottom: 8px;
}}

QTabBar::tab {{
    background-color: transparent;
    color: #8e8e93;
    padding: 6px 14px;
    border-radius: 6px;
    font-weight: 500;
    margin-right: 2px;
}}

QTabBar::tab:hover {{
    color: #ffffff;
    background-color: #2c2c2e;
}}

QTabBar::tab:selected {{
    background-color: #2d2d2d;
    color: #ffffff;
    font-weight: 600;
}}

/* Выпадающие списки (QComboBox) */
QComboBox {{
    background-color: #161616;
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    padding: 6px 10px;
    color: #ffffff;
    min-width: 100px;
}}

QComboBox:hover {{
    border-color: #3a3a3c;
}}

QComboBox:focus {{
    border-color: #0a84ff;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left-width: 0px;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}}

QComboBox QAbstractItemView {{
    background-color: #1e1e1e;
    border: 1px solid #2c2c2e;
    selection-background-color: #0a84ff;
    selection-color: #ffffff;
    padding: 5px;
    outline: 0;
}}

/* Группы (QGroupBox) */
QGroupBox {{
    border: 1px solid #2c2c2e;
    border-radius: 8px;
    margin-top: 15px;
    padding: 15px;
    background-color: #1c1c1e;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    color: #0a84ff;
    font-weight: 600;
}}

/* Системные меню (QMenu) */
QMenu {{
    background-color: #1e1e1e;
    color: #f5f5f7;
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    padding: 4px;
}}

QMenu::item {{
    padding: 6px 20px;
    border-radius: 4px;
    background-color: transparent;
}}

QMenu::item:selected {{
    background-color: #0a84ff;
    color: #ffffff;
}}

QMenu::separator {{
    height: 1px;
    background-color: #2c2c2e;
    margin: 4px 0px;
}}

/* Скроллбары (Тонкие в стиле macOS) */
QScrollBar:vertical {{
    background-color: transparent;
    width: 8px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: rgba(255, 255, 255, 0.15);
    min-height: 20px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: rgba(255, 255, 255, 0.3);
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    background: none;
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: transparent;
    height: 8px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: rgba(255, 255, 255, 0.15);
    min-width: 20px;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: rgba(255, 255, 255, 0.3);
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    background: none;
    width: 0px;
}}

/* Прогресс-бар */
QProgressBar {{
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    text-align: center;
    background-color: #161616;
    color: #ffffff;
    font-weight: 600;
}}

QProgressBar::chunk {{
    background-color: #0a84ff;
    border-radius: 5px;
}}

/* Разделители */
QSplitter::handle {{
    background-color: #2c2c2e;
}}

QSplitter::handle:hover {{
    background-color: #0a84ff;
}}

/* Карточки на Книжной полке */
QFrame#bookCard {{
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 12px;
}}

QFrame#bookCard:hover {{
    background-color: #26262a;
    border: 1px solid #0a84ff;
}}

QLabel#cardTitle {{
    font-weight: 600;
    font-size: 12px;
    color: #ffffff;
}}

QLabel#cardSubtitle {{
    color: #8e8e93;
    font-size: 10px;
}}

QLabel#coverLabel {{
    border-radius: 8px;
    background-color: #161616;
}}

QPushButton#cardMenuBtn {{
    background-color: transparent;
    border: none;
    color: #8e8e93;
    font-size: 16px;
    font-weight: bold;
    padding: 0px;
    border-radius: 11px;
    min-height: 22px;
    max-height: 22px;
}}

QPushButton#cardMenuBtn:hover {{
    background-color: rgba(255, 255, 255, 0.1);
    color: #ffffff;
}}

QLabel#libraryHeaderTitle {{
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
}}

QLabel#emptyLibraryLabel {{
    color: #8e8e93;
    font-size: 14px;
    margin-top: 60px;
}}

}}

QLabel#libraryHeaderTitle {{
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
}}

QLabel#emptyLibraryLabel {{
    color: #8e8e93;
    font-size: 14px;
    margin-top: 60px;
}}

QLabel#coverPathLabel {{
    color: #8e8e93;
    font-size: 11px;
}}

QLabel#deleteDialogLabel {{
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
}}

/* Карточки категорий мира */
QFrame#categoryCard {{
    background-color: #2c2c2e;
    border: 1px solid #3a3a3c;
    border-radius: 12px;
}}
QFrame#categoryCard:hover {{
    background-color: #3a3a3c;
    border-color: #0a84ff;
}}

/* Специальные виджеты для NovelEditor и BookReader */
QTextEdit#novelTextEditor {{
    background-color: #121218;
    color: #f5f5f7;
}}

QTextEdit#sceneSummaryDisplay {{
    background-color: #181822;
    color: #a0a0b0;
}}

QLabel#sceneCharsDisplay, QLabel#sceneLocsDisplay {{
    background-color: #181822;
    color: #ffffff;
}}

QLabel#charAvatarLabel, QLabel#locPhotoLabel {{
    border: 1px solid #3f3f52;
    background-color: #13131a;
}}

QTextBrowser#readerTextBrowser {{
    background-color: #121218;
}}
"""

LIGHT_THEME_STYLE = f"""
/* Общие стили */
QWidget {{
    background-color: #f5f5f7;
    color: #1d1d1f;
    font-family: {FONT_FAMILY_STACK};
    font-size: 14px;
    selection-background-color: #007aff;
    selection-color: #ffffff;
}}

/* Главные окна и диалоги */
QMainWindow, QDialog {{
    background-color: #f5f5f7;
}}

/* Метки */
QLabel {{
    background-color: transparent;
    color: #1d1d1f;
}}

QLabel#titleLabel {{
    font-size: 20px;
    font-weight: 600;
    color: #1d1d1f;
    padding-bottom: 5px;
}}

QLabel#subtitleLabel {{
    font-size: 12px;
    color: #8e8e93;
}}

/* Поля ввода (QLineEdit, QTextEdit и др.) */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 6px;
    padding: 6px 10px;
    color: #1d1d1f;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {{
    border: 1px solid #007aff;
    background-color: #ffffff;
}}

QLineEdit#searchBar {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 14px;
    padding: 5px 12px;
    color: #1d1d1f;
    min-height: 16px;
}}

QLineEdit#searchBar:focus {{
    border: 1px solid #007aff;
}}

/* Кнопки */
QPushButton {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    color: #1d1d1f;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 500;
    min-height: 18px;
}}

QPushButton:hover {{
    background-color: #f5f5f7;
    border-color: #c7c7cc;
}}

QPushButton:pressed {{
    background-color: #e5e5ea;
}}

QPushButton:disabled {{
    background-color: #f5f5f7;
    border-color: #e5e5ea;
    color: #c7c7cc;
}}

/* Акцентная/Основная кнопка */
QPushButton#primaryButton {{
    background-color: #007aff;
    border: none;
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#primaryButton:hover {{
    background-color: #268fff;
}}

QPushButton#primaryButton:pressed {{
    background-color: #005ec3;
}}

/* Кнопка удаления / Опасного действия */
QPushButton#dangerButton {{
    background-color: #ff3b30;
    border: none;
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#dangerButton:hover {{
    background-color: #ff453a;
}}

QPushButton#dangerButton:pressed {{
    background-color: #d6251b;
}}

/* Кнопка возврата к библиотеке */
QPushButton#backToLibraryButton {{
    background-color: transparent;
    border: 1px solid #d2d2d7;
    border-radius: 6px;
    padding: 4px 10px;
    font-weight: 600;
    color: #1d1d1f;
}}

QPushButton#backToLibraryButton:hover {{
    background-color: #e8e8ed;
    border-color: #c7c7cc;
}}

/* Кнопка переключения тем */
QPushButton#themeToggleButton {{
    background-color: transparent;
    border: 1px solid #d2d2d7;
    border-radius: 13px;
    padding: 4px 10px;
    font-weight: 500;
    color: #1d1d1f;
    min-height: 16px;
}}

QPushButton#themeToggleButton:hover {{
    background-color: #e8e8ed;
}}

/* Списки и Деревья */
QListWidget, QTreeWidget {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 8px;
    padding: 5px;
    outline: 0;
}}

QListWidget::item, QTreeWidget::item {{
    border-radius: 6px;
    padding: 6px 10px;
    margin: 2px 0px;
    color: #1d1d1f;
    background-color: transparent;
}}

QListWidget::item:hover, QTreeWidget::item:hover {{
    background-color: #f5f5f7;
    color: #000000;
}}

QListWidget::item:selected, QTreeWidget::item:selected {{
    background-color: #007aff;
    color: #ffffff;
    font-weight: 600;
}}

/* Таблицы */
QTableWidget {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 8px;
    gridline-color: #e5e5ea;
}}

QHeaderView::section {{
    background-color: #f5f5f7;
    color: #1d1d1f;
    padding: 6px;
    border: 1px solid #e5e5ea;
    font-weight: 600;
}}

/* Вкладки (QTabWidget и QTabBar в стиле Apple Segmented Control) */
QTabWidget::pane {{
    border: 1px solid #d2d2d7;
    border-radius: 8px;
    background-color: #ffffff;
    top: -1px;
}}

QTabBar {{
    background-color: #e8e8ed;
    border-radius: 8px;
    qproperty-drawBase: 0;
    padding: 3px;
    margin-bottom: 8px;
}}

QTabBar::tab {{
    background-color: transparent;
    color: #8e8e93;
    padding: 6px 14px;
    border-radius: 6px;
    font-weight: 500;
    margin-right: 2px;
}}

QTabBar::tab:hover {{
    color: #1d1d1f;
    background-color: #f5f5f7;
}}

QTabBar::tab:selected {{
    background-color: #ffffff;
    color: #1d1d1f;
    font-weight: 600;
}}

/* Выпадающие списки (QComboBox) */
QComboBox {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 6px;
    padding: 6px 10px;
    color: #1d1d1f;
    min-width: 100px;
}}

QComboBox:hover {{
    border-color: #c7c7cc;
}}

QComboBox:focus {{
    border-color: #007aff;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left-width: 0px;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}}

QComboBox QAbstractItemView {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    selection-background-color: #007aff;
    selection-color: #ffffff;
    padding: 5px;
    outline: 0;
}}

/* Группы (QGroupBox) */
QGroupBox {{
    border: 1px solid #d2d2d7;
    border-radius: 8px;
    margin-top: 15px;
    padding: 15px;
    background-color: #ffffff;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    color: #007aff;
    font-weight: 600;
}}

/* Системные меню (QMenu) */
QMenu {{
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid #d2d2d7;
    border-radius: 6px;
    padding: 4px;
}}

QMenu::item {{
    padding: 6px 20px;
    border-radius: 4px;
    background-color: transparent;
}}

QMenu::item:selected {{
    background-color: #007aff;
    color: #ffffff;
}}

QMenu::separator {{
    height: 1px;
    background-color: #e5e5ea;
    margin: 4px 0px;
}}

/* Скроллбары (Тонкие в стиле macOS) */
QScrollBar:vertical {{
    background-color: transparent;
    width: 8px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: rgba(0, 0, 0, 0.15);
    min-height: 20px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: rgba(0, 0, 0, 0.3);
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    background: none;
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: transparent;
    height: 8px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: rgba(0, 0, 0, 0.15);
    min-width: 20px;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: rgba(0, 0, 0, 0.3);
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    background: none;
    width: 0px;
}}

/* Прогресс-бар */
QProgressBar {{
    border: 1px solid #d2d2d7;
    border-radius: 6px;
    text-align: center;
    background-color: #e8e8ed;
    color: #1d1d1f;
    font-weight: 600;
}}

QProgressBar::chunk {{
    background-color: #007aff;
    border-radius: 5px;
}}

/* Разделители */
QSplitter::handle {{
    background-color: #d2d2d7;
}}

QSplitter::handle:hover {{
    background-color: #007aff;
}}

/* Карточки на Книжной полке */
QFrame#bookCard {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 12px;
}}

QFrame#bookCard:hover {{
    background-color: #fafafa;
    border: 1px solid #007aff;
}}

QLabel#cardTitle {{
    font-weight: 600;
    font-size: 12px;
    color: #1d1d1f;
}}

QLabel#cardSubtitle {{
    color: #8e8e93;
    font-size: 10px;
}}

QLabel#coverLabel {{
    border-radius: 8px;
    background-color: #e8e8ed;
}}

QPushButton#cardMenuBtn {{
    background-color: transparent;
    border: none;
    color: #8e8e93;
    font-size: 16px;
    font-weight: bold;
    padding: 0px;
    border-radius: 11px;
    min-height: 22px;
    max-height: 22px;
}}

QPushButton#cardMenuBtn:hover {{
    background-color: rgba(0, 0, 0, 0.05);
    color: #1d1d1f;
}}

QLabel#libraryHeaderTitle {{
    font-size: 24px;
    font-weight: 700;
    color: #1d1d1f;
}}

QLabel#emptyLibraryLabel {{
    color: #8e8e93;
    font-size: 14px;
    margin-top: 60px;
}}

QLabel#coverPathLabel {{
    color: #8e8e93;
    font-size: 11px;
}}

QLabel#deleteDialogLabel {{
    font-size: 13px;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 10px;
}}

/* Карточки категорий мира */
QFrame#categoryCard {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
    border-radius: 12px;
}}
QFrame#categoryCard:hover {{
    background-color: #f5f5f7;
    border-color: #007aff;
}}

/* Специальные виджеты для NovelEditor и BookReader */
QTextEdit#novelTextEditor {{
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid #d2d2d7;
}}

QTextEdit#sceneSummaryDisplay {{
    background-color: #e5e5ea;
    color: #555555;
    border: 1px solid #d2d2d7;
}}

QLabel#sceneCharsDisplay, QLabel#sceneLocsDisplay {{
    background-color: #e5e5ea;
    color: #1d1d1f;
    border: 1px solid #d2d2d7;
}}

QLabel#charAvatarLabel, QLabel#locPhotoLabel {{
    border: 1px solid #d2d2d7;
    background-color: #e5e5ea;
}}

QTextBrowser#readerTextBrowser {{
    background-color: #ffffff;
    border: 1px solid #d2d2d7;
}}
"""
