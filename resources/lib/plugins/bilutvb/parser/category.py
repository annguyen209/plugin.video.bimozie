#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

class Parser:
    def get(self, response):

        category = []

        soup = BeautifulSoup(response, "html.parser", from_encoding='utf8')

        for item in soup.select('div.navbar-collapse ul.navbar-nav > li')[1:-2]:
            category.append({
                'title': item.select_one('a').text.encode('utf-8'),
                'link': item.select_one('a').get('href'),
                'subcategory': self.getsubmenu(item)
            })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('> ul.dropdown-menu > li'):
            category.append({
                'title': item.select_one('a').text.encode('utf8'),
                'link': item.select_one('a').get('href')
            })
        return category
