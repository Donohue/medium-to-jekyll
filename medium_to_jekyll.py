#!/usr/bin/env
from __future__ import print_function

from lxml import etree
import lxml.html
from markdownify import markdownify
import os
import requests
import shutil
import sys
import re

def usage():
    print('Usage: %s <path-to-medium-articles> <path-to-jekyll-root-directory>' % sys.argv[0])

def save_images(doc, image_directory):
    for img in doc.xpath('//img'):
        if not 'src' in img.attrib:
            continue
        url = img.attrib['src']
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            filename = url.split('/')[-1]
            filepath = os.path.join(image_directory, filename)
            with open(filepath, 'wb') as w:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, w)
            img.attrib['src'] = '/%s/%s' % (image_directory.split('/')[-1], filename)
        else:
            print('Error processing image (%s): %d' % (url, r.status_code))

def extract_metadata(doc):
    title = etree.tostring(doc.xpath('//title')[0], method='text', encoding='unicode')
    date = doc.xpath('//time/@datetime')[0][:10]
    return title, date

def convert_post(doc):
    drop_xpaths = [
        '//head',
        '//header',
        '//*[contains(@class, "graf--title")]',
        '//section[@data-field="subtitle"]',
        '//footer'
    ]
    for xpath in drop_xpaths:
        elem = doc.xpath(xpath)
        if elem:
            elem[0].drop_tree()
    html = etree.tostring(doc, encoding='unicode')
    return markdownify(html)

def format_frontmatter(markdown, title, date):
    post = '---\n'
    post += 'layout:\tpost\n'
    post += 'title:\t"%s"\n' % title
    post += 'date:\t%s\n' % date
    post += '---\n\n%s'% markdown
    return post

def format_output_filename(filename):
    # Jekyll expects all seperators to be hyphens
    filename = filename.lower().replace('_', '-')
    # Strip the extra characters Medium has at the end of its URLs
    return re.sub(r'-*?\w*?\.html$', '', filename) + '.markdown'

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(-1)

    medium_directory = sys.argv[1]
    if not os.path.isdir(medium_directory):
        usage()
        print('Invalid Medium directory')
        sys.exit(-1)

    jekyll_directory = sys.argv[2]
    if not os.path.isdir(jekyll_directory):
        usage()
        print('Invalid Jekyll directory')
        sys.exit(-1)

    img_directory = os.path.join(jekyll_directory, 'img')
    if not os.path.isdir(img_directory):
        os.mkdir(img_directory)
    elif os.path.isfile(img_directory):
        usage()
        print('Jekyll directory contains `img` file instead of directory')
        sys.exit(-1)

    for filename in os.listdir(sys.argv[1]):
        if filename.startswith('draft') or not filename.endswith('.html'):
            continue
        with open(os.path.join(medium_directory, filename)) as f:
            html = f.read()
            doc = lxml.html.document_fromstring(html)
            title, date = extract_metadata(doc)
            save_images(doc, img_directory)
            markdown = convert_post(doc)
            post = format_frontmatter(markdown, title, date)
            output_filename = format_output_filename(filename)
            with open(os.path.join(jekyll_directory, '_posts', output_filename), 'wb') as out:
                out.write(post.encode('utf-8'))
                print('Converted %s (Published %s)' % (title, date))

if __name__ == "__main__":
    main()
