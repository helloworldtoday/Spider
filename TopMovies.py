#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
A simple scrapy by python, used to get top 100 movies
"""
import string
import re
import urllib2

class Spider(object) :
    """
    this class is to get top 100 movies
    
    Attributes:
        page: current page
        cur_url: url of current page
        datas: store name of movies we got
        top_num: number of top
    """

    def __init__(self) :
        self.page = 1
        self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="
        self.datas = [] # list
        self.top_num = 1
        print "                           ready, go!"

    def get_page(self, cur_page) :
        """
        get HTML based on number of page

        Args: cur_page: page number of current page
        Returns: return HTML of whole page(unicode)
        Raises: URLError: error by url
        """
        url = self.cur_url
        try :
            my_page = urllib2.urlopen(url.format(page = (cur_page - 1) * 25)).read().decode("utf-8")
        except urllib2.URLError, e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
        return my_page

    def find_title(self, my_page) :
        """
        match top 100 movies by HTML returned
        
        Args: my_page: HTML of a page to mathc
        """
        temp_data = [] # list
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        # print movie_items
        for index, item in enumerate(movie_items) :
            # print index
            # print item
            if item.find("&nbsp") == -1 : # not find the &nbsp
                temp_data.append("Top" + str(self.top_num) + " " + item)
                self.top_num += 1

        # for item in temp_data :
            # print item
        # print temp_data
        self.datas.extend(temp_data) # append a list to a list
    
    def start_spider(self) :
        """
        entrance, control the range of page
        """

        print """
        ##################################################
                            entrance
        ##################################################
        """

        while self.page <= 4 :
            my_page = self.get_page(self.page)
            # print self.page
            # print my_page
            self.find_title(my_page)
            self.page += 1

def main() :
    print """
        ##################################################
            a simple spider for getting top 100 movies
        ##################################################
    """
    my_spider = Spider()
    my_spider.start_spider()
    for item in my_spider.datas :
        print item
    print "end of the spider..."

if __name__ == '__main__':
    main()
