# Medium to Jekyll Blog

A simple script to convert exported Medium posts to Jekyll posts. The script takes a directory with exported Medium posts and a Jekyll root directory as inputs, and then does the following...

1. Iterate through all .html files in the Medium exported posts directory
2. Download the source images in the img tags from Medium posts and output them to an `img/` directory in the Jekyll root directory.
3. Updates all of the image sources in your blog post from Medium CDN URLs to the absolute path of your Jekyll directory (e.g. /img/filename.jpg)
4. Strips unnecessary HTML from the Medium posts (header, footer, CSS, etc.)
5. Converts the HTML into Markdown (using [markdownify](https://github.com/matthewwithanm/python-markdownify))
6. Formats the Jekyll frontmatter and prepends it to the converted Markdown
7. Writes the Markdown files into the Jekyll `_posts/` directory with the proper formatting

## Setup

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
python medium_to_jekyll.py <path-to-Medium-posts-directory> <path-to-Jekyll-root-directory>
```

## Configuring Jekyll

Add the following to your Jekyll `_config.yml` to serve images from the `img/` directory:

```
defaults:
  - scope:
      path: "img"
    values:
      image: true
```

## Copyright

Copyright &copy; Brian Donohue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
