import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import data_structure
import project_flow

class InputWidget(QWidget):
    def __init__(self, flow_dict):
        super().__init__()
        self.WIDGET_NAME        = ['NAME', 'CAUSE', 'SYMPTOM', 'DIAGNOSTICS/RESULT', 'TREATMENT', 'NOTE']
        self.BUTTON_NAME        = ['SUBMIT', 'EXIT']
        self.COMBO_DEPARTMENT   = ['Cardio', 'Pulmo', 'Nephro','GI','Infection','Alle','Rheuma','Pediatrics', 'Surgery']
        self.CATEGORY_NUM = len(self.WIDGET_NAME)
        self.flow_dict = flow_dict
        self.initUI()

    def initUI(self):
        self.create_grid_layout()

    def button_group_function(self, id):
        if id == 0: # SUBMIT
            self.submit_connect_function()
        elif id == 1: #EXIT
            project_flow.terminate_project(self.flow_dict)
            print('EXIT______________________')
            qApp.quit()

    def submit_connect_function(self):
        submit_list = []
        for category in self.WIDGET_NAME:
            editor = self.widget_dict[category][1]
            text = editor.text() if category == 'NAME' else editor.toPlainText()
            submit_list.append(text)
        data_structure.input_trimmer(submit_list)
        data_structure.Disease_oriented_object('new',submit_list, self.flow_dict)
        for item in self.text_editor_list:
            item.clear()
        for key, dict in self.flow_dict['meta_data'].state_dict.items():
            print(key)
            print(dict)
        print('submit_done')
        self.flow_dict['meta_data'].instance_to_json()

    def checkbox_function_generator(self, _dict, cat, editor):
        def return_function():
            self.subwindow = CheckboxSubWindow(_dict, cat, editor)
        return return_function

    def create_grid_layout(self):
        self.widget_dict = {}
        self.checkbox_button_list = []
        self.text_editor_list = []

        name_ = self.WIDGET_NAME[0]
        name_editor = QLineEdit(self)
        self.widget_dict[name_] = (QLabel(name_, self), name_editor)
        self.text_editor_list.append(name_editor)

        for category in self.WIDGET_NAME[1:-1]:
            checkbox_selector = QPushButton('checkbox_{}'.format(category), self)
            checkbox_selector.setFixedSize(20,20)
            checkbox_selector.setText('+')
            self.checkbox_button_list.append(checkbox_selector)
            text_editor = QTextEdit(self)
            text_editor.setTabChangesFocus(1)
            checkbox_selector.clicked.connect(self.checkbox_function_generator(self.flow_dict, category, text_editor))
            checkbox_selector.setAutoDefault(True)
            self.text_editor_list.append(text_editor)
            self.widget_dict[category] = (QLabel(category, self),
                                          text_editor,
                                          checkbox_selector)

        note_ = self.WIDGET_NAME[-1]
        note_editor = QTextEdit(self)
        note_editor.setTabChangesFocus(1)
        self.widget_dict[note_] = (QLabel(note_, self), note_editor)
        self.text_editor_list.append(note_editor)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(self.COMBO_DEPARTMENT)

        for value in self.widget_dict.values():
            value[0].setText('[{}]'.format(value[0].text()))

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setSpacing(5)

        sub_layout_top = QGridLayout()
        sub_layout_top.addWidget(self.widget_dict[name_][0], 0, 0)
        sub_layout_top.addWidget(self.widget_dict[name_][1], 1, 0)
        sub_layout_top.addWidget(self.widget_dict[note_][0], 2, 2)
        sub_layout_top.addWidget(self.widget_dict[note_][1], 3, 2, 7, 1)
        for i in range(1,self.CATEGORY_NUM-1):
            sub_layout_top.addWidget(self.widget_dict[self.WIDGET_NAME[i]][0], 2*i, 0)
            sub_layout_top.addWidget(self.widget_dict[self.WIDGET_NAME[i]][1], 2*i+1, 0, 1, 2)
            sub_layout_top.addWidget(self.widget_dict[self.WIDGET_NAME[i]][2], 2*i, 1)
        sub_layout_top.addWidget(self.combo_box, 1,2,Qt.AlignRight)

        sub_layout_bottom = QHBoxLayout()
        sub_layout_bottom.addStretch(5)
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(False)
        self.button_group.buttonClicked[int].connect(self.button_group_function)
        for j in range(len(self.BUTTON_NAME)):
            button = QPushButton(self.BUTTON_NAME[j], self)
            button.setAutoDefault(True)
            self.button_group.addButton(button, id=j)
            sub_layout_bottom.addWidget(button)

        layout.addLayout(sub_layout_top,0,0)
        layout.addLayout(sub_layout_bottom,1,0)
class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.flow_dict = project_flow.initiate_project()
        self.initUI()

    def initUI(self):
        self.central_wg = InputWidget(self.flow_dict)
        self.setCentralWidget(self.central_wg)
        self.create_menu_status_bar()

        self.setWindowTitle('Disease_Writer ')
        self.setWindowIcon(QIcon(r'icon\icon_database.png'))
        self.setGeometry(100,100,800,800)
        self.show()

    def add_action_menu_bar(self, action_name, shortcut, func, file_menu):
        _action = QAction(QIcon(r'icon\icon_{}.png'.format(action_name)), action_name, self)
        _action.setShortcut('Ctrl+{}'.format(shortcut.capitalize()))
        _action.setStatusTip('{} application'.format(action_name))
        _action.triggered.connect(func)
        file_menu.addAction(_action)

    def search_action_function_generator(self):
        self.subwindow_search = SearchSubWindow(self.flow_dict)

    def terminate_function(self):
        project_flow.terminate_project(self.flow_dict)
        print('EXIT______________________')
        qApp.quit()

    def create_menu_status_bar(self):
        def dummy():
            print('DUMMY')

        status_bar = self.statusBar()
        status_bar.showMessage('Write Description')

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu('File')

        self.add_action_menu_bar('Exit', 'Q', self.terminate_function, file_menu)
        self.add_action_menu_bar('Search', 'F', self.search_action_function_generator, file_menu)
        self.add_action_menu_bar('Save', 'S', dummy, file_menu)
        self.add_action_menu_bar('Export', 'P', self.terminate_function, file_menu)

class CheckboxWidget(QWidget):
    def __init__(self, flow_dict, category, editor):
        super().__init__()
        self.flow_dict = flow_dict
        self.category = category
        self.editor = editor
        self.checklist = []
        max_row = self.initUI(self.category)
        self.max_row = max_row

    def set_mother_object(self, mother):
        self.mother = mother

    def subwindow_close(self):
        self.editor.setText(self.editor.toPlainText() + ' : \n'.join(self.checklist)+ ' : ')
        self.mother.close()

    def initUI(self, category):
        max_row = self.create_grid_layout(category)
        return max_row

    def check_list_append_function(self, checkbox):
        def return_function():
            if checkbox.isChecked():
                self.checklist.append(checkbox.text())
                # self.mother.statusBar.status_bar_object.showMessage('/'.join(self.checklist))
            else:
                self.checklist.remove(checkbox.text())
                # self.mother.statusBar.status_bar_object.showMessage('/'.join(self.checklist))
        return return_function

    def create_grid_layout(self, category):
        layout = QGridLayout()
        self.setLayout(layout)

        sub_layout_top = QGridLayout()
        sub_layout_bottom = QHBoxLayout()
        layout.addLayout(sub_layout_top, 0, 0)
        layout.addLayout(sub_layout_bottom, 1, 0)

        key_list = list(self.flow_dict['meta_data'].state_dict[category].keys())
        key_list.sort()
        key_num = len(key_list)
        self.checkbox_object = []
        max_row = (key_num - 1) // 3 + 1
        for ind, key in enumerate(key_list):
            checkbox = QCheckBox(key)
            checkbox.clicked.connect(self.check_list_append_function(checkbox))
            self.checkbox_object.append(checkbox)
            sub_layout_top.addWidget(checkbox, ind//3, ind%3)

        sub_layout_bottom.addStretch(5)
        button = QPushButton('RETURN', self)
        button.setAutoDefault(True)
        button.clicked.connect(self.subwindow_close)
        sub_layout_bottom.addWidget(button)
        return max_row
class CheckboxSubWindow(QMainWindow):
    def __init__(self, flow_dict, category, editor):
        super().__init__()
        self.category = category
        self.flow_dict = flow_dict
        self.editor = editor
        self.initUI()

    def initUI(self):
        self.central_wg = CheckboxWidget(self.flow_dict, self.category, self.editor)
        self.setCentralWidget(self.central_wg)
        self.central_wg.set_mother_object(self)
        self.create_menu_status_bar()
        print('mother_set')
        self.setWindowTitle('{} checkbox'.format(self.category))
        self.setWindowIcon(QIcon(r'icon\icon_database.png'))
        self.setGeometry(200, 200, 300, self.central_wg.max_row * 20)
        self.show()

    def create_menu_status_bar(self):
        self.status_bar_object = self.statusBar()
        self.status_bar_object.showMessage('Checkbox Selector')

class SearchWidget(QWidget):
    def __init__(self,flow_dict):
        super().__init__()
        self.flow_dict = flow_dict
        self.CATEGORY_LIST = flow_dict['meta_data'].category_list
        self.search_category = 'CAUSE'
        self.button_list = []
        self.initUI()

    def funcgen_disease_display(self, name):
        def disease_display():
            self.display = DisplaySubWindow(self.flow_dict, name)
        return disease_display

    def search_button(self):
        search_target = self.search_editor.text()
        try:
            disease_list = self.flow_dict['meta_data'].state_dict[self.search_category][search_target]
            disease_list.sort()
            disease_num = len(disease_list)
            # divider = 1 if not (disease_num>10) else 2
            self.empty_label.deleteLater()
            del self.empty_label
            for button in self.button_list:
                button.deleteLater()
                del button
            for ind, disease_name in enumerate(disease_list):
                disease_button = QPushButton(disease_name, self)
                disease_button.clicked.connect(self.funcgen_disease_display(disease_name))
                disease_button.setFixedSize(225,25)
                self.sub_layout_bottom.addWidget(disease_button, ind//2,ind%2)
                disease_button.setFlat(1)
                self.button_list.append(disease_button)
            self.empty_label = QLabel(self)
            self.empty_label.setFixedSize(500, 450-25*disease_num/2)
            self.sub_layout_bottom.addWidget(self.empty_label,ind//2+1, 0,1,2)
        except KeyError:
            self.garbage = MessageBox(search_target)

    def combobox_return(self):
        self.search_category = self.combo_box.currentText()
        self.completer = QCompleter(list(self.flow_dict['meta_data'].state_dict[self.search_category].keys()))
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_editor.setCompleter(self.completer)
        self.search_editor.clear()

    def initUI(self):
        layout = QVBoxLayout()
        self.sub_layout_top = QGridLayout()
        self.sub_layout_bottom = QGridLayout()

        # layout.addStretch(1)
        layout.addLayout(self.sub_layout_top)
        # layout.addStretch(1)
        layout.addLayout(self.sub_layout_bottom)
        # layout.addStretch(1)
        self.setLayout(layout)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(self.CATEGORY_LIST)
        self.combo_box.currentTextChanged.connect(self.combobox_return)
        self.combo_box.setFixedSize(100,25)

        model = [list(self.flow_dict['meta_data'].state_dict[index].keys())
                      for index in self.CATEGORY_LIST]
        self.completer = QCompleter(list(self.flow_dict['meta_data'].state_dict['CAUSE'].keys()))
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.search_editor = QLineEdit(self)
        self.search_editor.setCompleter(self.completer)
        self.search_editor.returnPressed.connect(self.search_button)

        self.search_botton = QPushButton("\U0001F50E", self)
        self.search_botton.clicked.connect(self.search_button)
        self.search_botton.setShortcut(Qt.Key_Return)
        self.search_botton.setFixedSize(25, 25)

        self.sub_layout_top.addWidget(self.combo_box, 0, 0)
        self.sub_layout_top.addWidget(self.search_editor, 0, 1)
        self.sub_layout_top.addWidget(self.search_botton, 0, 2)

        self.sub_layout_top.setSpacing(5)

        self.empty_label = QLabel(self)
        self.empty_label.setFixedSize(500,450)
        self.sub_layout_bottom.addWidget(self.empty_label)
class SearchSubWindow(QMainWindow):
    def __init__(self, flow_dict):
        super().__init__()
        self.flow_dict = flow_dict
        self.initUI()

    def initUI(self):
        self.central_wg = SearchWidget(self.flow_dict)
        self.setCentralWidget(self.central_wg)
        self.create_menu_status_bar()

        self.setWindowTitle('Search Window')
        self.setWindowIcon(QIcon(r'icon\icon_Save.png'))
        self.setGeometry(500, 200, 500, 500)
        self.setFixedSize(500,500)
        self.show()

    def add_action_menu_bar(self, action_name, shortcut, func, file_menu):
        _action = QAction(QIcon(r'icon\icon_{}.png'.format(action_name)), action_name, self)
        _action.setShortcut('Ctrl+{}'.format(shortcut.capitalize()))
        _action.setStatusTip('{} application'.format(action_name))
        _action.triggered.connect(func)
        file_menu.addAction(_action)

    def close_window(self):
        self.close()

    def create_menu_status_bar(self):
        status_bar = self.statusBar()
        status_bar.showMessage('Search')

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu('File')

        self.add_action_menu_bar('Exit', 'Q', self.close_window, file_menu)

class DisplayWidget(QWidget):
    def __init__(self, flow_dict, name):
        super().__init__()
        self.flow_dict = flow_dict
        self.disease = name
        self.initUI()

    def initUI(self):
        disease_instance = self.flow_dict['meta_data'].\
                            restore_disease_instance(self.disease, self.flow_dict)
        data = disease_instance.format_representation()
        print('#'*10,'\n', data)

        layout = QVBoxLayout()

        self.text = QLabel(self.disease, self)
        self.text.setText(data)
        self.text.setAlignment(Qt.AlignTop)
        scroll = QScrollArea()
        scroll.setWidget(self.text)
        scroll.setWidgetResizable(True)

        layout.addWidget(scroll)

        self.setLayout(layout)
class DisplaySubWindow(QMainWindow):
    def __init__(self, flow_dict, name):
        super().__init__()
        self.flow_dict = flow_dict
        self.disease = name
        self.initUI()

    def add_action_menu_bar(self, action_name, shortcut, func, file_menu):
        _action = QAction(QIcon(r'icon\icon_{}.png'.format(action_name)), action_name, self)
        _action.setShortcut(Qt.Key_Enter)
        _action.setStatusTip('{} application'.format(action_name))
        _action.triggered.connect(func)
        file_menu.addAction(_action)

    def create_menu_status_bar(self):
        status_bar = self.statusBar()
        status_bar.showMessage('Description: {}'.format(self.disease))

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu('File')

        self.add_action_menu_bar('Exit', 'Q', self.close_window, file_menu)

    def close_window(self):
        self.close()

    def initUI(self):
        self.central_wg = DisplayWidget(self.flow_dict, self.disease)
        self.setCentralWidget(self.central_wg)
        self.create_menu_status_bar()

        self.setWindowTitle(self.disease)
        self.setWindowIcon(QIcon(r'icon\icon_database.png'))
        self.setGeometry(800, 300, 800, 800)
        self.show()

class FilesaveWidget(QWidget):
    def __init__(self, flow_dict, name):
        super().__init__()
        self.flow_dict = flow_dict
        self.disease = name
        self.initUI()

class MessageBox(QMessageBox):
    def __init__(self, wrong_key):
        QMessageBox.__init__(self)
        self.setText('Key Error')
        self.setInformativeText("{} not in the library".format(wrong_key.upper()))
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    # font = QFont('SansSerif')
    # ex.setFont(font)
    sys.exit(app.exec_())
