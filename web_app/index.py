from flask import Flask, render_template, request, redirect, url_for, send_file
import requests
from lxml import html
from sklearn.externals import joblib
import sys, os
sys.path.append('./')
from utils import *

app = Flask(__name__)
loaded_model = joblib.load('../liblinear.pkl')

@app.route('/')
def main_page():
    return redirect((url_for('index')), code=302)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            url = request.form['input_url']
            page = requests.get(url, allow_redirects=False)
            tree = html.fromstring(page.text)
        except:
            return render_template('index.html', article='Không tồn tại bài báo này hoặc tên miền này chưa được hỗ trợ !')
        if url.startswith('https://dantri.com.vn'):
            article_name = tree.xpath("//h1[@class='fon31 mgb15']/text()")[0].strip()
            article_content = ' '.join((s.strip() for s in tree.xpath("//div[@id='divNewsContent']/p/text()"))).strip()

            article = article_name + '\n' + article_content
            article_predict = article_name + ' ' + article_content
            predict = loaded_model.predict([preprocess(article_predict)])[0]
            return render_template('index.html', article=article, predict=predict)

        if url.startswith('https://vnexpress.net'):
            article_name = tree.xpath("//h1[@class='title-detail']/text()")[0].strip()
            article_description = tree.xpath("//p[@class='description']/text()")[0].strip()
            article_content = ' '.join((s.strip() for s in tree.xpath("//p[@class='Normal']/text()"))).strip()

            article = article_name + '\n' + article_description + '\n' + article_content
            article_predict = article_name + ' ' + article_description + ' ' + article_content
            predict = loaded_model.predict([preprocess(article_predict)])[0]
            return render_template('index.html', article=article, predict=predict)
        if url.startswith('https://baomoi.com/'):
            article_name = tree.xpath("//h1[@class='article__header']/text()")[0].strip()
            article_description = ' '.join((s.strip() for s in tree.xpath("//div[@class='article__sapo']/text()"))).strip()
            article_content = ' '.join((s.strip() for s in tree.xpath("//div[@class='article__body']/p/text()"))).strip()

            article = article_name + '\n' + article_description + '\n' + article_content
            article_predict = article_name + ' ' + article_description + ' ' + article_content
            predict = loaded_model.predict([preprocess(article_predict)])[0]
            return render_template('index.html', article=article, predict=predict)
        if url.startswith('https://vietnamnet.vn/'):
            article_name = tree.xpath("//h1[@class='title f-22 c-3e']/text()")[0].strip()
            article_description = tree.xpath("//div[@class='bold ArticleLead']/p/text()")[0].strip()
            article_content = ' '.join((s.strip() for s in tree.xpath("//div[@id='ArticleContent']/p/text()"))).strip()

            article = article_name + '\n' + article_description + '\n' + article_content
            article_predict = article_name + ' ' + article_description + ' ' + article_content
            predict = loaded_model.predict([preprocess(article_predict)])[0]
            return render_template('index.html', article=article, predict=predict)
        if url.startswith('https://thanhnien.vn/'):
            article_name = tree.xpath("//h1[@class='details__headline']/text()")[0].strip()
            article_description = tree.xpath("//div[@id='chapeau']/div/text()")[0].strip()
            article_content = ' '.join((s.strip() for s in tree.xpath("//div[@id='abody']/div/text()"))).strip()

            article = article_name + '\n' + article_description + '\n' + article_content
            article_predict = article_name + ' ' + article_description + ' ' + article_content
            predict = loaded_model.predict([preprocess(article_predict)])[0]
            return render_template('index.html', article=article, predict=predict)
        return render_template('index.html')
    return render_template('index.html')

@app.route('/crawl', methods=['GET', 'POST'])
def crawl():
    if request.method == 'POST':
        start_id = request.form['start_id']
        end_id = request.form['end_id']
        os.system(f"scrapy runspider BaoMoi.py -a start_id={start_id} -a end_id={end_id} -o crawl.csv")
        return render_template('crawl.html', download_done=1)
    return render_template('crawl.html')

@app.route('/download')
def download():
    try:
        return send_file('./crawl.csv', attachment_filename='crawl.csv', as_attachment=True, cache_timeout=0)
    except Exception as e:
        try:
            return str(e)
        finally:
            e = None
            del e


if __name__ == '__main__':
    app.run(debug=True)