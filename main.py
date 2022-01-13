from cropScreen import crop
import asyncio
from pyppeteer import launch
import requests
from bs4 import BeautifulSoup
from PIL import Image


def main():
    word = "omicron"
    baseUrl = "https://www.bbc.co.uk/search?q=" + word + "&page="

    articles = []
    for i in range(30):
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
    print(f"Length: {len(articles)}")
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
        if found:
            print(f"found {word} in {article}")
            pil_image = Image.fromarray(found)
            images.append(pil_image)
        else:
            print(f"could not find {word} in {article}")

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
