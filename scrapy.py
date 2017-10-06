# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib2

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

class MyHTMLParser(HTMLParser):
    begin = False

    start_common = False
    start_num = False
    start_by = False

    in_title = False
    in_writer = False
    in_viewer = False
    in_date = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict()
        for (variable, value) in attrs:
            attr_dict[variable] = value

        if tag == 'table':
            if attr_dict.get('id', None) == 'threadlisttableid':
                self.begin = True
                print 'Start output...'

        # print '@', self.get_starttag_text()

        elif tag == 'tbody':
            if attr_dict.has_key('id') and attr_dict.get('id', None).startswith('normalthread_'):
                print 'Hit the target[list]', value
                self.start_common = True
                print '-----------------------------------------------------------------------'
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
                print ROOT_PATH + attr_dict.get('href', None)
            elif attr_dict.get('c', None) == '1' and attr_dict.has_key('href') and self.start_by:
                if attr_dict.get('href', None).startswith('space-uid-'):
                    self.in_writer = True
                elif attr_dict.get('href', None).startswith('space-username-'):
                    self.in_viewer = True
        elif tag == 'span':
            if len(attr_dict) == 0 and self.start_by:
                self.in_date = True

    #Value getter
    def handle_data(self, data):
        if self.begin:
            if self.in_title:
                self.in_title = False
                print 'Hit the target[title]', data
            elif self.in_writer:
                self.in_writer = False
                print 'Hit the target[writer]', data
            elif self.in_date:
                self.in_date = False
                print 'Hit the target[date]', data
            elif self.in_viewer:
                self.in_viewer = False
                print 'Hit the target[viewer]', data
            elif self.start_num:
                if self.lasttag == 'a':
                    print 'Hit the target[reply]', data
                elif self.lasttag == 'em':
                    print 'Hit the target[view]', data

    def handle_endtag(self, tag):
        if self.begin:
            if tag == 'tbody':
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
request_headers = {'User-Agent': 'PeekABoo/1.3.7'}
request = urllib2.Request(URL, None, request_headers)

try:
    response = urllib2.urlopen(request)
    the_page = response.read()

    parser = MyHTMLParser()
    parser.feed(the_page)
except urllib2.HTTPError as e:
    print e
