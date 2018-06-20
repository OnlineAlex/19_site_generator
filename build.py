import markdown
import os

from jinja2 import Template


BASIC_TEMPLATE = Template(open('templates/_basic.html').read())
HEADER_TEMPLATE = Template(open('templates/_header.html', encoding='utf-8').read())
FOOTER_TEMPLATE = Template(open('templates/_footer.html', encoding='utf-8').read())


def get_frendly_url(url):
    frendly_url = url[url.find('_')+1:]
    if frendly_url.find('_') != -1:
        frendly_url = frendly_url.replace('_', '-')
    return frendly_url


def get_title(file_name):
    title = file_name[file_name.find('_')+1:-3]
    if title.find('_') != -1:
        title = title.replace('_', ' ')
    return title.capitalize()


def convert_md_to_html(folder, files):
    for file in files:
        title = get_title(file)
        with open(os.path.join(folder, file), encoding='utf-8') as file_md:
            yield {
                'title': title,
                'code': markdown.markdown(file_md.read())
            }


def generate_templates_articles(articles):
    template = BASIC_TEMPLATE
    article_template = Template(open('templates/article.html', encoding='utf-8').read())
    for article in articles:
        yield {
            'url': article['title'].replace(' ', '-').lower(),
            'page': template.render(
                title=article['title'],
                header=HEADER_TEMPLATE.render(title=article['title']),
                footer=FOOTER_TEMPLATE.render(),
                body=article_template.render(article=article['code'])
            )
        }


def add_article_to_site(topic, articles):
    for article in articles:
        with open(
            'article/{}/{}.html'.format(topic, article['url']),
            'w',
            encoding='utf-8'
        ) as new_article:
            new_article.write(article['page'])


def add_article_info(topic, articles_name):
    for article_name in articles_name:
        yield {
            'name': get_title(article_name),
            'url': 'article/{}/{}.html'.format(topic, get_frendly_url(article_name)[:-3])
        }


def get_index_page(topics):
    template = BASIC_TEMPLATE
    article_list = Template(open('templates/index.html', encoding='utf-8').read())
    return template.render(
                title='Статьи',
                header=HEADER_TEMPLATE.render(title='Статьи'),
                footer=FOOTER_TEMPLATE.render(),
                body=article_list.render(topics=topics)
    )


def add_index_page(page):
    with open('index.html', 'w', encoding='utf-8') as index_html:
        index_html.write(page)


if __name__ == '__main__':
    article_folder = os.path.join(os.getcwd(), 'articles')
    sitemap = {}
    for root, dirs, file_names in os.walk(article_folder):
        topic_articles = get_frendly_url(os.path.basename(root))
        if file_names and not os.path.exists(os.path.join('article', topic_articles)):
            os.mkdir(os.path.join('article', topic_articles))
        if file_names:
            html_articles = convert_md_to_html(root, file_names)
            html_templates = generate_templates_articles(html_articles)
            add_article_to_site(topic_articles, html_templates)

            topic_name = topic_articles.replace('-', ' ').capitalize()
            sitemap[topic_name] = add_article_info(topic_articles, file_names)

    index_page = get_index_page(sitemap)
    add_index_page(index_page)
