import glob
import os
import shutil
import sys

import editdistance
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow

from libs import subscraper, youtube_scraper, gui


def read_settings():
    settings = {}
    with open('settings' + os.sep + 'settings.txt', 'rb') as f:
        lines = f.readlines()
        for line in lines:
            k, v = line.strip().split('=')
            settings[k] = v
    return settings


def get_stuff(subreddit, settings, count):
    urls = subscraper.get_urls(subreddit, settings, count)
    print urls
    youtube_scraper.url_to_file(urls, settings)
    source_files = os.getcwd() + os.sep + '*.' + settings['preferredcodec']
    target_folder = settings['target'] + os.sep + 'scraped_' + subreddit
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    file_list = glob.glob(source_files)
    for single_file in file_list:
        shutil.move(single_file, target_folder)
    return urls


class App(QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_clicked)
        self.lineEdit.textChanged.connect(self.sub_changed)

    def sub_changed(self):
        with open('libs' + os.sep + 'genres' + os.sep + 'subs.txt') as f:
            subs = list(set(eval(''.join(f.readlines()))))
        model = QStandardItemModel(self.listView)
        typed = str(self.lineEdit.text())
        scored = map(lambda sub: (sub, int(long(editdistance.eval(typed, sub)))), subs)
        subs = zip(*sorted(scored, key=lambda x: x[1]))[0]
        for sub in subs:
            item = QStandardItem(sub)
            model.appendRow(item)
        self.listView.setModel(model)
        self.listView.show()

    def button_clicked(self):
        subreddit = str(self.lineEdit.text())
        settings = read_settings()
        try:
            count = int(float(self.lineEdit_2.text()))
        except:
            count = int(settings['default_count'])
        urls = get_stuff(subreddit, settings, count)
        print urls

def parse_genres():
    with open('libs' + os.sep + 'genres' + os.sep + 'raw.txt', 'rb') as f:
        raw_text = ' '.join([a.strip() for a in f.readlines()])
        subreddits = filter(lambda a: (a[:3] == '/r/' and str.isalnum(a[3:])), raw_text.split())
        subreddits = map(lambda x: x[3:].lower(), subreddits)
    with open('libs' + os.sep + 'genres' + os.sep + 'subs.txt', 'wb') as f:
        f.write(str(subreddits))


if __name__ == '__main__':
    parse_genres()
    app = QApplication(sys.argv)
    form = App()
    form.show()
    sys.exit(app.exec_())
