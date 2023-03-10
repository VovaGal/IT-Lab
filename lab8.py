import psycopg2
import sys
import datetime
from datetime import date
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox, QInputDialog)


today = date.today()
num = int(today.isocalendar().week)
if (num % 2) == 0:
   this_week = "timetable_week2"
else:
   this_week = "timetable_week1"




# main window created
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("BVT2201 Information")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_schedule_tab()
        self._create_teacher_tab()
        self._create_timetable_week1_tab()
        self._create_timetable_week2_tab()

    # connect to db
    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="timestable_db",
                                     user="postgres",
                                     password="password",
                                     host="localhost",
                                     port="5433")

        self.cursor = self.conn.cursor()

    # define teacher tab
    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teacher")

        self.teacher_gbox = QGroupBox("Teacher")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.teacher_gbox)

        self._create_teacher_table()

        self.update_teacher_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_teacher_button)
        self.update_teacher_button.clicked.connect(self._update_teacher)

        self.teacher_tab.setLayout(self.svbox)

    # display teacher table
    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(3)
        self.teacher_table.setHorizontalHeaderLabels(["Full Name", "Subject", ""])

        self._update_teacher_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox)

    # create and fill teacher table
    def _update_teacher_table(self):
        self.cursor.execute("SELECT * FROM teacher")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            updateButton = QPushButton("Update")

            self.teacher_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 2, updateButton)

            updateButton.clicked.connect(lambda ch, num=i: self._update_teacher_info())

        self.teacher_table.resizeRowsToContents()

    # update teacher information
    #    def _update_teacher_info(self, full_name, subject):
    #        psql_teach = "update teacher set full_name = %s, subject = %s"
    #
    #        try:
    #            self.cursor.execute(psql_teach, (full_name, subject))
    #            self.updated_rows = self.cursor.rowcount
    #            self.conn.commit()
    #        except (Exception, psycopg2.DatabaseError) as error:
    #            print(error)
    #        self._update_teacher_info('Lapaev L L', 'english')

    def _update_teacher(self):
        self._update_teacher_table()

    # display timetable week1
    def _create_timetable_week1_tab(self):
        self.timetable_week1_tab = QWidget()
        self.tabs.addTab(self.timetable_week1_tab, "Week1")

        self.timetable_week1_gbox = QGroupBox("Week1")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.timetable_week1_gbox)

        self._create_timetable_week1_table()

        self.update_timetable_week1_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_timetable_week1_button)
        self.update_timetable_week1_button.clicked.connect(self._update_timetable_week1)

        self.timetable_week1_tab.setLayout(self.svbox)

    # display timetable week1
    def _create_timetable_week1_table(self):
        self.timetable_week1_table = QTableWidget()
        self.timetable_week1_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.timetable_week1_table.setColumnCount(3)
        self.timetable_week1_table.setHorizontalHeaderLabels(["Day", "Lessons", ""])

        self._update_timetable_week1_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.timetable_week1_table)
        self.timetable_week1_gbox.setLayout(self.mvbox)

    # define display timetable week1
    def _update_timetable_week1_table(self):
        self.cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, timetable_week1.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from timetable_week1, teacher where teacher.subject = timetable_week1.subject order by start_time)timetable_week1 group by 1 order by case when day = 'Monday' then 1 when day = 'Tuesday' then 2 when day = 'Wednesday' then 3 when day = 'Thursday' then 4 else 5 end;")
        records = list(self.cursor.fetchall())

        self.timetable_week1_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            updateButton = QPushButton("Update")

            self.timetable_week1_table.setItem(i, 0,
                                               QTableWidgetItem(str(r[0])))
            self.timetable_week1_table.setItem(i, 1,
                                               QTableWidgetItem(str(r[1])))
            self.timetable_week1_table.setCellWidget(i, 2, updateButton)

            updateButton.clicked.connect(lambda ch, num=i: self._update_timetable_week1_info())

        self.timetable_week1_table.resizeRowsToContents()

    def _update_timetable_week1(self):
        self._update_timetable_week1_table()

        # display timetable week2
    def _create_timetable_week2_tab(self):
        self.timetable_week2_tab = QWidget()
        self.tabs.addTab(self.timetable_week2_tab, "Week2")

        self.timetable_week2_gbox = QGroupBox("Week2")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.timetable_week2_gbox)

        self._create_timetable_week2_table()

        self.update_timetable_week2_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_timetable_week2_button)
        self.update_timetable_week2_button.clicked.connect(self._update_timetable_week2)

        self.timetable_week2_tab.setLayout(self.svbox)

    # display timetable week2
    def _create_timetable_week2_table(self):
        self.timetable_week2_table = QTableWidget()
        self.timetable_week2_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.timetable_week2_table.setColumnCount(3)
        self.timetable_week2_table.setHorizontalHeaderLabels(["Day", "Lessons", ""])

        self._update_timetable_week2_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.timetable_week2_table)
        self.timetable_week2_gbox.setLayout(self.mvbox)

    # define display timetable week2
    def _update_timetable_week2_table(self):
        self.cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, timetable_week2.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from timetable_week2, teacher where teacher.subject = timetable_week2.subject order by start_time)timetable_week2 group by 1 order by case when day = 'Monday' then 1 when day = 'Tuesday' then 2 when day = 'Wednesday' then 3 when day = 'Thursday' then 4 else 5 end;")
        records = list(self.cursor.fetchall())

        self.timetable_week2_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            updateButton = QPushButton("Update")

            self.timetable_week2_table.setItem(i, 0,
                                                   QTableWidgetItem(str(r[0])))
            self.timetable_week2_table.setItem(i, 1,
                                                   QTableWidgetItem(str(r[1])))
            self.timetable_week2_table.setCellWidget(i, 2, updateButton)

            updateButton.clicked.connect(lambda ch, num=i: self._update_timetable_week2_info())

        self.timetable_week2_table.resizeRowsToContents()

    def _update_timetable_week2(self):
        self._update_timetable_week2_table()



    # display timetable tab by days
    def _create_schedule_tab(self):
        self.day = 'Monday'
        self.schedule_tab = QWidget()
        self.tabs.addTab(self.schedule_tab, "Schedule")

        self.schedule_gbox = QGroupBox("{}".format(self.day))

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)

        self.shbox1.addWidget(self.schedule_gbox)

        self._create_schedule_table()


        self.svbox.addLayout(self.shbox2)
        self.update_schedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_schedule)

        self.shboxm = QHBoxLayout()
        self.svbox.addLayout(self.shboxm)
        self.monday_schedule_button = QPushButton("Monday")
        self.shboxm.addWidget(self.monday_schedule_button)
        self.monday_schedule_button.clicked.connect(lambda ch: self.btnstate('Monday'))

        self.shboxt = QHBoxLayout()
        self.shboxm.addLayout(self.shboxt)
        self.tuesday_schedule_button = QPushButton("Tuesday")
        self.shboxt.addWidget(self.tuesday_schedule_button)
        self.tuesday_schedule_button.clicked.connect(lambda ch: self.btnstate('Tuesday'))

        self.shboxw = QHBoxLayout()
        self.shboxm.addLayout(self.shboxw)
        self.wednesday_schedule_button = QPushButton("Wednesday")
        self.shboxw.addWidget(self.wednesday_schedule_button)
        self.wednesday_schedule_button.clicked.connect(lambda ch: self.btnstate('Wednesday'))

        self.shboxth = QHBoxLayout()
        self.shboxm.addLayout(self.shboxth)
        self.thursday_schedule_button = QPushButton("Thursday")
        self.shboxth.addWidget(self.thursday_schedule_button)
        self.thursday_schedule_button.clicked.connect(lambda ch: self.btnstate('Thursday'))

        self.shboxf = QHBoxLayout()
        self.shboxm.addLayout(self.shboxf)
        self.friday_schedule_button = QPushButton("Friday")
        self.shboxf.addWidget(self.friday_schedule_button)
        self.friday_schedule_button.clicked.connect(lambda ch: self.btnstate('Friday'))

        self.shboxa = QHBoxLayout()
        self.shbox1.addLayout(self.shboxa)
        self.alter_lesson_button = QPushButton("Alter")
        self.shboxa.addWidget(self.alter_lesson_button)
        self.alter_lesson_button.clicked.connect(lambda ch: self.update_lesson('Alter'))

        self.shboxd = QHBoxLayout()
        self.shbox1.addLayout(self.shboxd)
        self.delete_lesson_button = QPushButton("Delete")
        self.shboxd.addWidget(self.delete_lesson_button)
        self.delete_lesson_button.clicked.connect(lambda ch: self.update_lesson('Delete'))

        self.shboxrow = QHBoxLayout()
        self.shbox1.addLayout(self.shboxrow)
        self.add_row_button = QPushButton("Add Row")
        self.shboxrow.addWidget(self.add_row_button)
        self.add_row_button.clicked.connect(lambda ch: self.update_lesson('Add Row'))

        self.schedule_tab.setLayout(self.svbox)




    # display schedule for the day
    def _create_schedule_table(self):
        self.schedule_table = QTableWidget()
        self.schedule_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(["Subject", "Room numb", "Start time", "Finish time", "",""])

        self._update_schedule_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.schedule_table)
        self.schedule_gbox.setLayout(self.mvbox)


    def btnstate(self, wday):
        self.day = wday


    def _update_schedule_table(self):
        self.cursor.execute(
            "SELECT subject, room_numb, start_time, finish_time FROM {} WHERE day = '{}'".format(this_week, self.day))
        records = list(self.cursor.fetchall())

        self.schedule_table.setRowCount(len(records) + 1)
        self.schedule_gbox.setTitle(self.day)
        for i, r in enumerate(records):
            r = list(r)
#            updateButton = QPushButton("Update")
#            deleteButton = QPushButton("Delete")
#            addRow = QPushButton("Add Row")

            self.schedule_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.schedule_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.schedule_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.schedule_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.schedule_table.setItem(len(records), 0, QTableWidgetItem(str('')))
            self.schedule_table.setItem(len(records), 1, QTableWidgetItem(str('')))
            self.schedule_table.setItem(len(records), 2, QTableWidgetItem(str('')))
            self.schedule_table.setItem(len(records), 3, QTableWidgetItem(str('')))

#            self.schedule_table.setCellWidget(i, 4, updateButton)

#            updateButton.clicked.connect(lambda ch, num=i: self._update_lesson(num))

        self.schedule_table.resizeRowsToContents()


    def update_lesson(self, query):
        if query == 'Alter':
            print('alter')
#            text, alter = QInputDialog.getText(self, 'Alter Room Number', 'Enter New Room:')
#            if alter:
#                try:
#                    self.cursor.execute("UPDATE {} SET room_numb = %s WHERE day = {}, start_time = {}".format(this_week, self.day, self.schedule_table.item(0, 2).text()), (text),)
#                    self.conn.commit()
#                except:
#                    self.conn.commit()
#                    QMessageBox.about(self, "Error", "Enter all fields")
        elif query == 'Delete':
            print('delete')
#            row = list()
#            for i in range(self.schedule_table.columnCount()):
#                try:
#                    self.cursor.execute("UPDATE {} SET subject = {}, room_numb = {} WHERE day = {}, start_time = {};".format(this_week, self.schedule_table.item(rowNum, 0).text(), self.schedule_table.item(rowNum, 1).text(), self.day, self.schedule_table.item(rowNum, 2)), (row[0],))
#                    self.conn.commit()
#                except:
#                    QMessageBox.about(self, "Error", "Enter all fields")
        elif query == 'Add Row':
            print(self.schedule_table.item(0, 3).text())

#    def _update_lesson(self, rowNum):
#        row = list()
#        for i in range(4):
#            try:
#                row.append(self.schedule_table.item(rowNum, i).text())
#            except:
#                row.append(None)
#
#            try:
#                self.cursor.execute("UPDATE {} SET subject = {}, room_numb = {} WHERE day = {}, start_time = {};".format(this_week, self.schedule_table.item(rowNum, 0).text(), self.schedule_table.item(rowNum, 1).text(), self.day, self.schedule_table.item(rowNum, 2)), (row[0],))
#                self.conn.commit()
#            except:
#                QMessageBox.about(self, "Error", "Enter all fields")



    def _update_schedule(self):
        self._update_schedule_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
