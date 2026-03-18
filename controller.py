import time
import flet as ft
import model as md


class SpellChecker:

    def __init__(self, view):
        self._modality = None
        self._txtInTesto = None
        self._multiDic = md.MultiDictionary()
        self._view = view
        self._language=None

    def handleLanguage(self,e):
        self._view._lvOut.controls.clear()
        self._language=self._view.language_dd.value
        self._view.page.update()
        return
    def handleModality(self,e):
        self._view._lvOut.controls.clear()
        self._modality=self._view._txtMod_dd.value
        self._view.page.update()
        return


    def handleSpellcheck(self,e):
        self._txtInTesto=self._view._txtTesto.value
        traduzione=self.handleSentence(self._txtInTesto,self._language, self._modality)
        self._view._lvOut.controls.clear()
        self._view._lvOut.controls.append(ft.Text(f"Selected language: {self._language}", size=22))
        self._view._lvOut.controls.append(ft.Text(f"Selected modality: {self._modality}", size=22))

        self._view._lvOut.controls.append(ft.Text(f"Text: {self._view._txtTesto.value}", size=22))
        self._view._lvOut.controls.append(ft.Text(f"Unknown words: {traduzione[0]} ", size=22))
        self._view._lvOut.controls.append(ft.Text(f"Search time: {traduzione[1]} s", size=22))
        self._view.page.update()

        return



    def handleSentence(self, txtIn, language, modality):
        txtIn = replaceChars(txtIn.lower())

        words = txtIn.split()
        paroleErrate = " - "

        match modality:
            case "Default":
                t1 = time.time()
                parole = self._multiDic.searchWord(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Linear":
                t1 = time.time()
                parole = self._multiDic.searchWordLinear(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Dichotomic":
                t1 = time.time()
                parole = self._multiDic.searchWordDichotomic(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1
            case _:
                return None


    def printMenu(self):
        print("______________________________\n" +
              "      SpellChecker 101\n"+
              "______________________________\n " +
              "Seleziona la lingua desiderata\n"
              "1. Italiano\n" +
              "2. Inglese\n" +
              "3. Spagnolo\n" +
              "4. Exit\n" +
              "______________________________\n")


def replaceChars(text):
    chars = "\\`*_{}[]()>#+-.!$?%^;,=_~"
    for c in chars:
        text = text.replace(c, "")
    return text
