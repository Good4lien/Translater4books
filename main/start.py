import wx
from string import ascii_letters
from yandex_translate import YandexTranslate


def translate(word):
    key = 'trnsl.1.1.20180709T094228Z.c8c944f05e9d5ff1.aecb0458d185c3588404b25731a72a199bd68e4e'
    translate = YandexTranslate(key)
    trans=translate.translate(word, 'ru').get('text')[0].__str__()
    return trans

def validate(word):
    return all(map(lambda c: c in ascii_letters, word))

class TextDropTarget(wx.TextDropTarget):
    def __init__(self, object):
        wx.TextDropTarget.__init__(self)
        self.object = object

    def OnDropText(self, x, y, data):
        p = ' — '
        self.object.SetValue(self.object.GetValue()+data+p+translate(data)+'\n')
        return True

class Window(wx.Frame):
    def __init__(self, parent, title):
        global text
        text='''
        \n\n\n  Для простмотра слов откройте текстовый файл
        '''
        wx.Frame.__init__(self, parent, title=title, size=(720, 575))
        self.SetBackgroundColour((50, 200, 100))
        self.main_frame()

    def main_frame(self):
        global text
        self.help_text = wx.TextCtrl(self, pos=(207, 5),size=(91, 25), style=wx.TE_READONLY)
        self.help_text.SetValue('Перевод фраз')
        self.trans_text = wx.TextCtrl(self, pos=(300, 5), size=(400, 500), style=wx.TE_MULTILINE)
        self.get_text = wx.TextCtrl(self, pos=(207, 35), size=(90, 25))
        self.trans_button = wx.Button(self, pos=(207, 65), label='Перевести')
        self.total_words = wx.TextCtrl(self, pos=(300, 505), size=(400, 25), style=wx.TE_READONLY)
        self.main_text = wx.TextCtrl(self, pos=(5,5), size=(200,500),style=wx.TE_MULTILINE)
        self.total_text = wx.TextCtrl(self, pos = (5,505), size=(200,25), style=wx.TE_READONLY)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText)
        self.txt_button = wx.Button(self, pos=(208, 350), label="Text")
        self.learn_button = wx.Button(self,pos=(208, 380),label="Learn")
        self.clean_button = wx.Button(self, pos=(208, 410), label="Clean")
        self.open_button = wx.Button(self, pos=(208, 440), label="Open")
        self.save_button = wx.Button(self, pos=(208, 470), label="Save")
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.main_text.SetValue(text)
        self.get_text.SetFocus()

    def listview(self, words):
        self.main_text.Hide()
        self.main_list=wx.ListCtrl(self, pos=(5,5), size=(200,500), style = wx.LC_LIST)
        words.reverse()
        for word in words:
            self.main_list.InsertItem(0,word)
        self.main_list.SetFocus()
        self.trans_text.SetDropTarget(TextDropTarget(self.trans_text))
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnDragInit)

    def OnDragInit(self, event):
        text = self.main_list.GetItemText(event.GetIndex())
        tobj = wx.TextDataObject(text)
        src = wx.DropSource(self.main_list)
        src.SetData(tobj)
        src.DoDragDrop(True)
        self.Total()

    def Total(self):
        p = ' — '
        total = self.trans_text.GetValue().count(p)
        total_text = ' Total: ' + total.__str__() + ' words'
        self.total_words.SetValue(total_text)

    def OnButton(self, event):
        btn = event.GetEventObject().GetLabel()
        if btn=='Clean':
            self.trans_text.Clear()
            self.total_words.SetValue('')
        elif btn=="Learn":
            learn_window = Learn(None, "Learn")
            learn_window.Center()
            learn_window.Show(True)
        elif btn=="Save":
            self.OnSave()
        elif btn=="Open":
            self.OnOpen()
        elif btn=="Перевести":
            self.OnText(event)

    def OnText(self,e):
        val = self.get_text.GetValue().__str__()
        display_text = self.trans_text.GetValue().__str__()
        p=' — '
        t=''
        for _ in val:
            if _ == "":
                t=''
            else:
                t+=_
        words=t.split('\n')
        for word in words:
            if word:
                display_text+=word+p+translate(word)+'\n'
        self.trans_text.SetValue(display_text)
        self.get_text.Clear()
        self.Total()

    def OnOpen(self):
        global text
        text=''
        self.open = wx.FileDialog(self, "Choose a file to open", "books", '', "*.*", wx.FC_OPEN)
        if self.open.ShowModal() == wx.ID_OK:
            name = self.open.GetFilename()
            dir = self.open.GetDirectory()
            with open(dir+'\\'+name, 'r') as book:
                for _ in book:
                    _ = _.replace('\n', '!')
                    text += _.strip()
            words = []
            Eng = ['']
            s = ['(', ')', ',', '{', '-', '}', '”', '<', '>', '«', '»', '…', '"', ':',
                 ';', '!', '?', '.', '[', '*', ']', '“', '"', '.', ',']
            for _ in s:
                text = text.replace(_, ' ').strip()
            M = text.split(' ')
            for word in M:
                word = word.lower()
                if word in Eng:
                    pass
                else:
                    if validate(word):
                        Eng.append(word)
            Eng.pop(0)
            for _ in Eng:
                words.append(_)
            total = ' Total: ' + len(Eng).__str__() + ' words'
            self.total_text.SetValue(total)
            main_window.SetTitle(name)
            self.listview(words)

    def OnSave(self):
        save = wx.FileDialog(self, "Save", "saved words", " ", "*.*", wx.FC_SAVE)
        if save.ShowModal() == wx.ID_OK:
            name=save.GetDirectory()+'\\'+save.GetFilename()+'.txt'
            with open(name, 'w', encoding='utf-8') as f:
                f.write(self.trans_text.GetValue().__str__())

class Learn(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(720, 500))
        self.main_learn()

    def main_learn(self):
        pass

if __name__ == '__main__':
    app = wx.App()
    main_window = Window(None, "words")
    main_window.Centre()
    main_window.Show(True)
    app.MainLoop()