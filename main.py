from cropScreen import crop
import asyncio
from pyppeteer import launch
import requests
from bs4 import BeautifulSoup
from PIL import Image
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("word", help="The word to look for in articles")
    parser.add_argument("numPages", type=int, default=5,
                        help="Number of pages to look through")
    args = parser.parse_args()
    print(args)
    word = args.word.lower()
    baseUrl = "https://www.bbc.co.uk/search?q=" + word + "&page="

    articles = []
    for i in range(args.numPages):
        article = requests.get(baseUrl + str(i))

        soup = BeautifulSoup(article.text, 'html.parser')

        lists = soup.find_all(class_='ssrcss-v19xcd-Stack e1y4nx260')[0].find_all(
            "li")

        for l in lists:
            href = l.find_all("a")[0]["href"]
            if "news" in href and "articles" not in href:
                print(href)
                articles.append(href)

    print(articles)
    print(f"\nNumber of articles: {len(articles)}\n")
    getArticles(articles, "omicron")


def makeGif(images):
    images[0].save('output.gif',
                   save_all=True, append_images=images[1:], optimize=False, duration=120, loop=0)

    print("Saved GIF")


def getArticles(articles, word):
    images = []
    for article in articles:
        name = article.split("/")[-1]
        asyncio.get_event_loop().run_until_complete(saveScreenshot(article, name))
        found = crop(f'articles/{name}.png', name, word)
        if found[0]:
            print(f"found {word} in {article}")
            pil_image = Image.fromarray(found[1])
            images.append(pil_image)
        else:
            print(f"could not find {word} in {article}")

    print(f"\nNumber of images: {len(images)}\n")

    makeGif(images)


async def saveScreenshot(articleURL, name):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({
        "width": 1920,
        "height": 1080,
        "deviceScaleFactor": 2,
    })
    await page.goto(articleURL)
    await page.screenshot({'path': f'articles/{name}.png'})
    await browser.close()


if __name__ == '__main__':
    main()
