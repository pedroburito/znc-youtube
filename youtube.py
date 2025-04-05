import znc
from threading import Thread
from requests import get

from secret import API_KEY as API_KEY

class youtube(znc.Module):
    description = "youtube announcer"
    module_types = [znc.CModInfo.UserModule ]

    def __init__(self):
        pass
        # self.cre = re.compile("youtu\.be/([\d\w_\-]{5,11})|youtube\.com/watch\?v=([\d\w\-_]*)")

    # def OnUserTextMessage(self, message):
    #     self.youtube(message)
    #
    # def OnChanTextMessage(self, message):
    #     self.youtube(message)

    def _async_yt(self, func, args):
        t = Thread(target=func, args=args)
        t.start()
        t.join(timeout=None)

    @staticmethod
    def _yt_api(yt_id, callback, chan_name):
        api_ep = "https://www.googleapis.com/youtube/v3/videos?part=snippet&fields=items/snippet/title&id={}&key={}".format(yt_id, API_KEY)
        r = get(api_ep)
        if r:
            res = r.json()
            callback(res, chan_name)

    def _extract_id(self, message):
        if 'youtube.com' in message:
            if 'v=' in message:
                r = message.split('v=')[-1]
                r = r.split()[0]
                if '&' in r:
                    return r.split('&')[0]
                else:
                    return r.strip()
            else:
                return ''
        elif 'youtu.be/' in message:
            r = message.split('youtu.be/')[-1]
            r = r.split()[0]
            if '?' in r:
                return r.split('?')[0].strip()
            else:
                return r.strip()
        else:
            return ''

    def youtube(self, message):
        try:
            s = message.GetText()
            yt_id = self._extract_id(s)
            if not yt_id:
#                self.PutModule("no match: " + yt_id)
                return znc.CONTINUE

            else:
#                self.PutModule("go async: " + yt_id)
                self._async_yt(self._yt_api, (yt_id,  self.callback, message.GetChan().GetName()))
        except Exception as e:
            self.PutModule('Caught Exception youtube:')
            self.PutModule(str(e))


    def callback(self, results, chan_name):
        # self.PutModule("Callback: {} for {}".format(results, chan_name))
        # self.PutModule(str(results))
        for itm in results['items']:
            itm.get('snippet', {}).get('title','\x0304,01CRAZYOUTUBERROR')

        title = results['items'][0]['snippet']['title']
        m = "PRIVMSG {} :\x0301,00You \x0300,04Tube`\x03: {}".format(chan_name, title)

        _nick = self.GetUser().GetNick()
        _hostname = self.GetUser().GetBindHost()
        _ident = self.GetUser().GetIdent()
        # self.PutModule(':{}!{}@{} {}'.format(_nick, _ident, _hostname, m))
        self.PutUser(':{}!{}@{} {}'.format(_nick, _ident, _hostname, m))
        self.PutIRC(m)


    def OnLoad(self, args, message):
        try:
            self.PutStatus("Loaded youtube.py")
        # self.PutModule('args: {} message: {}'.format(args, message))
        except Exception as e:
            self.PutModule('Caught Exception OnLoad:')
            self.PutModule(str(i))
        return znc.CONTINUE

    # def OnUserRaw(self, s):
        # return znc.CONTINUE

    def OnUserTextMessage(self, message):
        try:
            self.youtube(message)
        except Exception as e:
            self.PutModule('Caught Exception OnUserTextMessage:')
            for i in str(e).split('\n'):
                self.PutModule(i)
        return znc.CONTINUE

    def OnChanTextMessage(self, message):
        try:
            self.youtube(message)
        except Exception as e:
            self.PutModule('Caught Exception OnChanTextMessage: ')
            for i in str(e).split('\n'):
                self.PutModule(i)
        return znc.CONTINUE

#        def OnChanMsg(self, nick, channel, message):
#            return self.youtube_depr(nick, channel, message)
