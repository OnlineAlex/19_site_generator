import markdown as md
import uuid
import os, glob
import json
import collections as cl
import html

from jinja2 import Environment, FileSystemLoader


RU_TITLES = json.load(open('config.json', encoding='utf-8'))


def get_topic_title(topic_slug):
    if topic_slug.find('-') > 0:
        topic_slug = topic_slug.replace('-', '_')
    for topic in RU_TITLES['topics']:
        if topic['slug'] == topic_slug:
            return topic['title']


def get_frendly_url(url):
    frendly_url = url[url.find('_')+1:]
    if frendly_url.find('_') > 0:
        frendly_url = frendly_url.replace('_', '-')
    elif frendly_url.find(' ') > 0:
        frendly_url = frendly_url.replace(' ', '-')
    return '{}.html'.format(html.unescape(frendly_url))


def convert_md_to_html(file_source):
    with open(os.path.join('articles', file_source), encoding='utf-8') as file_md:
        return md.markdown(file_md.read(), extensions=['codehilite'])


def generate_article_page(title, article, static):
    template = Environment(
        loader=FileSystemLoader(searchpath='templates')
    ).get_template('article.html')
    return template.render(
                title=title,
                STATIC_URL='../../{}'.format(static),
                article=article
            )


def add_article_to_site(article_path, article):
    with open(os.path.join('article', article_path), 'w', encoding='utf-8') as new_article:
        new_article.write(article)


def get_article_info(url, title):
    return {'name': title, 'url': 'article/{}'.format(url)}


def get_index_page(topics, static):
    template = Environment(
        loader=FileSystemLoader(searchpath='templates')
    ).get_template('index.html')
    return template.render(
                title='Статьи',
                STATIC_URL=static,
                topics=topics
    )


def add_index_page(page):
    with open('index.html', 'w', encoding='utf-8') as index_html:
        index_html.write(page)


if __name__ == '__main__':
    static_url = glob.glob(os.path.join(os.getcwd(), "static.*"))[0]
    new_static_url = 'static.{}'.format(uuid.uuid4().hex[:8])
    os.rename(static_url, new_static_url)
    sitemap = cl.defaultdict(list)
    for article_info in RU_TITLES['articles']:
        article_url = get_frendly_url(os.path.split(article_info['source'])[-1][:-3])
        if not os.path.exists(os.path.join('article', article_info['topic'])):
            os.mkdir(os.path.join('article', article_info['topic']))

        html_article = convert_md_to_html(article_info['source'])
        article_page = generate_article_page(
            html.escape(article_info['title']),
            html_article,
            new_static_url
        )
        add_article_to_site(
            os.path.join(article_info['topic'], article_url),
            article_page
        )
        topic_title = get_topic_title(article_info['topic'])
        sitemap[topic_title].append(get_article_info(
            '{}/{}'.format(article_info['topic'], article_url),
            html.escape(article_info['title'])
        ))

    index_page = get_index_page(sitemap, new_static_url)
    add_index_page(index_page)
