# -*- coding: utf-8 -*-
import html.parser as HP
import urllib.request as UR
import urllib.error as UE
import ssl
import xlwt

# import openpyxl

# Html tag Sample
'''
<tbody id="normalthread_4213790">
<tr>
<td class="icn">
<a href="forum.php?mod=viewthread&amp;tid=4213790&amp;extra=page%3D14%26filter%3Dauthor%26orderby%3Ddateline" title="新窗口打开" target="_blank">
<img src="static/image/common/folder_common.gif">
</a>
</td>
<th class="common">
<a href="javascript:;" id="content_4213790" class="showcontent y" title="更多操作" onclick="CONTENT_TID='4213790';CONTENT_ID='normalthread_4213790';showMenu({'ctrlid':this.id,'menuid':'content_menu'})"></a>
<a href="forum.php?mod=viewthread&amp;tid=4213790&amp;extra=page%3D14%26filter%3Dauthor%26orderby%3Ddateline" onclick="atarget(this)" class="s xst">我做了一个梦</a>
<img src="static/image/filetype/image_s.gif" alt="attach_img" title="图片附件" align="absmiddle">
<span class="tps">&nbsp;...<a href="forum.php?mod=viewthread&amp;tid=4213790&amp;extra=page%3D14%26filter%3Dauthor%26orderby%3Ddateline&amp;page=2">2</a></span>
</th>
<td class="by">
<cite>
<a href="space-uid-119604.html" c="1" mid="card_2726">疯狂的舌头</a></cite>
<em><span>2017-9-10</span></em>
</td>
<td class="num"><a href="forum.php?mod=viewthread&amp;tid=4213790&amp;extra=page%3D14%26filter%3Dauthor%26orderby%3Ddateline" class="xi2">11</a><em>492</em></td>
<td class="by">
<cite><a href="space-username-%E6%B5%B7%E5%B1%B1%E7%9F%B3.html" c="1" mid="card_9312">海山石</a></cite>
<em><a href="forum.php?mod=redirect&amp;tid=4213790&amp;goto=lastpost#lastpost">2017-9-10 18:44</a></em>
</td>
</tr>
</tbody>
'''

ROOT_PATH = 'http://www.incnjp.com/'


class DataHandler:
    def __init__(self, name):
        self.excel_name = name
        self.excel = xlwt.Workbook()
        self.current_sheet = self.excel.add_sheet(u'sheet1', cell_overwrite_ok=True)
        self.current_col = 0
        self.current_row = 0

    def on_start(self):
        print('Start')
        # Table head
        row_head = [u'Title', u'Author', u'Date', u'Reply', u'View', u'Reader']
        for i in range(0, len(row_head)):
            self.current_sheet.write(0, i, row_head[i])
        ++self.current_row

    def on_stop(self):
        print('Stop')
        self.excel.save(self.excel_name)

    def on_item_begin(self):
        print('>>>>>>>>>>>>')
        self.current_col = 0

    def on_item_end(self):
        print('<<<<<<<<<<<<')
        self.current_row += 1

    def on_title(self, data):
        print('[Title ]\t', data)
        self.current_sheet.write(self.current_row, self.current_col, data)
        self.current_col += 1

    def on_writer(self, data):
        print('[Author]\t', data)
        self.current_sheet.write(self.current_row, self.current_col, data)
        self.current_col += 1

    def on_date(self, data):
        print('[Date  ]\t', data)
        self.current_sheet.write(self.current_row, self.current_col, data)
        self.current_col += 1

    def on_viewer(self, data):
        print('[Reader]\t', data)
        self.current_sheet.write(self.current_row, self.current_col, data)
        self.current_col += 1

    def on_reply(self, data):
        print('[Reply ]\t', data)
        self.current_sheet.write(self.current_row, self.current_col, data)
        self.current_col += 1

    def on_view(self, data):
        print('[View  ]\t', data)
        self.current_sheet.write(self.current_row, self.current_col, data)
        self.current_col += 1


class MyHTMLParser(HP.HTMLParser):
    begin = False

    start_common = False
    start_num = False
    start_by = False

    in_title = False
    in_writer = False
    in_viewer = False
    in_date = False

    data_handler = None

    def set_listener(self, listener):
        self.data_handler = listener

    def handle_starttag(self, tag, attrs):
        attr_dict = dict()
        for (variable, value) in attrs:
            attr_dict[variable] = value

        if tag == 'table':
            if attr_dict.get('id', None) == 'threadlisttableid':
                self.begin = True
                if self.data_handler:
                    self.data_handler.on_start()

        # print '@', self.get_starttag_text()

        elif tag == 'tbody':
            if 'id' in attr_dict and attr_dict.get('id', None).startswith('normalthread_'):
                # print('Hit the target', value) #debug
                self.start_common = True
                if self.data_handler:
                    self.data_handler.on_item_begin()
        elif tag == 'td':
            if attr_dict.get('class', None) == 'num':
                self.start_num = True
            elif attr_dict.get('class', None) == 'by':
                self.start_by = True
        elif tag == 'th':
            if attr_dict.get('class', None) == 'common':
                self.start_common = True
        elif tag == 'a':
            if attr_dict.get('class', None) == 's xst':
                self.in_title = True
                print(ROOT_PATH + attr_dict.get('href', None))
            elif attr_dict.get('c', None) == '1' and 'href' in attr_dict and self.start_by:
                if attr_dict.get('href', None).startswith('space-uid-'):
                    self.in_writer = True
                elif attr_dict.get('href', None).startswith('space-username-'):
                    self.in_viewer = True
        elif tag == 'span':
            if len(attr_dict) == 0 and self.start_by:
                self.in_date = True

    # Value getter
    def handle_data(self, data):
        if self.begin and self.data_handler:
            if self.in_title:
                self.in_title = False
                self.data_handler.on_title(data)
            elif self.in_writer:
                self.in_writer = False
                self.data_handler.on_writer(data)
            elif self.in_date:
                self.in_date = False
                self.data_handler.on_date(data)
            elif self.in_viewer:
                self.in_viewer = False
                self.data_handler.on_viewer(data)
            elif self.start_num:
                if self.lasttag == 'a':
                    self.data_handler.on_reply(data)
                elif self.lasttag == 'em':
                    self.data_handler.on_view(data)

    def handle_endtag(self, tag):
        if self.begin:
            if tag == 'table':
                if self.data_handler:
                    self.data_handler.on_stop()
            elif tag == 'tbody':
                if self.data_handler:
                    self.data_handler.on_item_end()
            elif tag == 'tbody':
                if self.start_common:
                    self.start_common = False
            elif tag == 'td':
                if self.start_by:
                    self.start_by = False
                elif self.start_num:
                    self.start_num = False


# =============Define===================
URL = 'https://www.incnjp.com/forum.php?mod=forumdisplay&fid=92&orderby=dateline&filter=author&page=14'
# =============Run entry================
data_handler = DataHandler('out.xls')
try:
    request_headers = {'User-Agent': 'PeekABoo/1.3.7'}
    request = UR.Request(URL, None, request_headers)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    response = UR.urlopen(request, context=ssl_context)
    the_page = response.read()
    if the_page:
        #    print("Body:", the_page) #Debug
        parser = MyHTMLParser()
        parser.set_listener(data_handler)
        parser.feed(the_page.decode('utf-8'))
except UE.URLError as e:
    print("Error:", e)
